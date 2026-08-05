// test_gate.cpp -- host-testable unit tests for layer1/gate.h.
// No hardware, no ESP-IDF headers, no I2C. Compiles/runs on the dev
// machine (x86/laptop gateway) against mock AccelSample arrays.
//
// Build (no ESP-IDF needed):
//   g++ -std=c++17 -I../main test_gate.cpp ../main/layer1/gate.cpp -o test_gate
//   ./test_gate
//
// Minimal hand-rolled assertions -- no external test framework dependency,
// keeps this buildable with just a system g++/clang.

#include <cstdio>
#include <cstdlib>
#include <vector>

#include "layer1/gate.h"

using spark::layer1::AccelSample;
using spark::layer1::ComputeMagnitudeG;
using spark::layer1::GateDecision;
using spark::layer1::ThresholdGate;

namespace {

int g_failures = 0;
int g_checks = 0;

void Check(bool condition, const char* description) {
    ++g_checks;
    if (!condition) {
        ++g_failures;
        std::fprintf(stderr, "FAIL: %s\n", description);
    }
}

// Mock sensor array: constant-magnitude samples at a fixed step, useful
// for constructing "held above threshold for N ms" scenarios.
std::vector<AccelSample> MakeConstantMagnitudeSeries(float magnitude_g,
                                                       uint32_t start_ms,
                                                       uint32_t step_ms,
                                                       int count) {
    std::vector<AccelSample> series;
    series.reserve(count);
    // Put all magnitude on the x-axis for simplicity -- ComputeMagnitudeG
    // is axis-agnostic (sqrt of sum of squares), tested separately below.
    for (int i = 0; i < count; ++i) {
        series.push_back(AccelSample{
            .accel_x_g = magnitude_g,
            .accel_y_g = 0.0f,
            .accel_z_g = 0.0f,
            .timestamp_ms = start_ms + static_cast<uint32_t>(i) * step_ms,
        });
    }
    return series;
}

void TestComputeMagnitudeG() {
    // 3-4-5 triangle scaled: 0.3^2 + 0.4^2 = 0.25 -> sqrt = 0.5
    AccelSample s{0.3f, 0.4f, 0.0f, 0};
    Check(std::abs(ComputeMagnitudeG(s) - 0.5f) < 1e-5f,
          "ComputeMagnitudeG: 3-4-5 triangle gives magnitude 0.5g");

    AccelSample zero{0.0f, 0.0f, 0.0f, 0};
    Check(ComputeMagnitudeG(zero) == 0.0f,
          "ComputeMagnitudeG: zero vector gives zero magnitude");

    // Pure single-axis at exactly the locked threshold.
    AccelSample at_threshold{2.5f, 0.0f, 0.0f, 0};
    Check(std::abs(ComputeMagnitudeG(at_threshold) - 2.5f) < 1e-5f,
          "ComputeMagnitudeG: single-axis 2.5g reads back as 2.5g");
}

void TestGate_StaysBelowThreshold_NeverTriggers() {
    ThresholdGate gate;
    // Mock array: 5 samples at 1.0g (well below 2.5g threshold), 100ms apart.
    auto series = MakeConstantMagnitudeSeries(1.0f, 0, 100, 5);
    bool any_trigger = false;
    for (const auto& sample : series) {
        if (gate.Evaluate(sample) == GateDecision::kTriggerCnn) {
            any_trigger = true;
        }
    }
    Check(!any_trigger,
          "Gate: sustained 1.0g (below 2.5g threshold) never triggers CNN");
    Check(!gate.IsQueued(), "Gate: not queued after sustained sub-threshold input");
}

void TestGate_ExceedsThreshold_ButBriefSpike_DoesNotTrigger() {
    ThresholdGate gate;
    // Single spike sample well above threshold, then drops -- held time is
    // 0ms (only one sample seen), must not cross the >300ms duration gate.
    AccelSample spike{3.0f, 0.0f, 0.0f, 1000};
    Check(gate.Evaluate(spike) == GateDecision::kSkip,
          "Gate: single instantaneous spike above threshold does not trigger "
          "(no held duration yet)");
}

void TestGate_SustainedAboveThreshold_TriggersAfter300ms() {
    ThresholdGate gate;
    // 3.0g held from t=0 to t=400ms in 50ms steps -- should cross the
    // 300ms duration gate partway through and trigger.
    auto series = MakeConstantMagnitudeSeries(3.0f, 0, 50, 9);  // 0..400ms
    GateDecision last_decision = GateDecision::kSkip;
    uint32_t trigger_at_ms = 0;
    for (const auto& sample : series) {
        last_decision = gate.Evaluate(sample);
        if (last_decision == GateDecision::kTriggerCnn) {
            trigger_at_ms = sample.timestamp_ms;
            break;
        }
    }
    Check(last_decision == GateDecision::kTriggerCnn,
          "Gate: 3.0g sustained past 300ms eventually triggers CNN");
    Check(trigger_at_ms > 300,
          "Gate: trigger timestamp occurs strictly after the 300ms duration mark");
    Check(gate.IsQueued(), "Gate: queued flag set after trigger");
}

void TestGate_DropBelowThreshold_ResetsHoldClock() {
    ThresholdGate gate;
    // 3.0g for 200ms (not enough to trigger), drop to 1.0g for one sample,
    // then 3.0g again for 200ms more -- total *would* exceed 300ms if the
    // clock weren't reset, but per §2.5 dropping below threshold should
    // reset the hold timer.
    Check(gate.Evaluate(AccelSample{3.0f, 0, 0, 0}) == GateDecision::kSkip, "pre-check A");
    Check(gate.Evaluate(AccelSample{3.0f, 0, 0, 200}) == GateDecision::kSkip, "pre-check B");
    Check(gate.Evaluate(AccelSample{1.0f, 0, 0, 250}) == GateDecision::kSkip,
          "Gate: drop below threshold mid-hold does not trigger");
    Check(gate.Evaluate(AccelSample{3.0f, 0, 0, 300}) == GateDecision::kSkip,
          "Gate: hold clock reset after drop -- re-crossing threshold does not "
          "immediately trigger");
    auto decision = gate.Evaluate(AccelSample{3.0f, 0, 0, 700});  // 400ms after reset-cross
    Check(decision == GateDecision::kTriggerCnn,
          "Gate: after reset, a fresh >300ms hold does trigger");
}

void TestGate_QueueTimeout_ClearsAfter10s() {
    ThresholdGate gate;
    // Trigger once at t=0..400ms.
    auto trigger_series = MakeConstantMagnitudeSeries(3.0f, 0, 50, 9);
    for (const auto& sample : trigger_series) {
        gate.Evaluate(sample);
    }
    Check(gate.IsQueued(), "Gate: queued immediately after initial trigger");

    // No new peak for >10s (§2.5 step 4) -- feed one below-threshold sample
    // far in the future, queue should clear.
    gate.Evaluate(AccelSample{0.5f, 0, 0, 400 + 10001});
    Check(!gate.IsQueued(),
          "Gate: queue clears after 10s with no new peak acceleration");
}

void TestGate_QueueTimeout_DoesNotClearBeforeTenSeconds() {
    ThresholdGate gate;
    auto trigger_series = MakeConstantMagnitudeSeries(3.0f, 0, 50, 9);
    for (const auto& sample : trigger_series) {
        gate.Evaluate(sample);
    }
    Check(gate.IsQueued(), "Gate: queued after initial trigger (timeout pre-check)");

    // Only 5s elapsed -- queue must still be set.
    gate.Evaluate(AccelSample{0.5f, 0, 0, 400 + 5000});
    Check(gate.IsQueued(),
          "Gate: queue remains set before the 10s timeout elapses");
}

void TestGate_Reset_ClearsAllState() {
    ThresholdGate gate;
    auto trigger_series = MakeConstantMagnitudeSeries(3.0f, 0, 50, 9);
    for (const auto& sample : trigger_series) {
        gate.Evaluate(sample);
    }
    Check(gate.IsQueued(), "Gate: queued before manual Reset() (pre-check)");
    gate.Reset();
    Check(!gate.IsQueued(), "Gate: Reset() clears queued state");

    // After reset, gate should behave like a fresh instance -- a single
    // spike shouldn't trigger immediately.
    Check(gate.Evaluate(AccelSample{3.0f, 0, 0, 0}) == GateDecision::kSkip,
          "Gate: post-Reset() behaves like fresh instance (no immediate trigger)");
}

}  // namespace

int main() {
    TestComputeMagnitudeG();
    TestGate_StaysBelowThreshold_NeverTriggers();
    TestGate_ExceedsThreshold_ButBriefSpike_DoesNotTrigger();
    TestGate_SustainedAboveThreshold_TriggersAfter300ms();
    TestGate_DropBelowThreshold_ResetsHoldClock();
    TestGate_QueueTimeout_ClearsAfter10s();
    TestGate_QueueTimeout_DoesNotClearBeforeTenSeconds();
    TestGate_Reset_ClearsAllState();

    std::printf("%d/%d checks passed\n", g_checks - g_failures, g_checks);
    return g_failures == 0 ? 0 : 1;
}
