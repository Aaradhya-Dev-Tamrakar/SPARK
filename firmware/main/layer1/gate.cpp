#include "layer1/gate.h"

#include <cmath>

namespace spark::layer1 {

float ComputeMagnitudeG(const AccelSample& sample) {
    return std::sqrt(sample.accel_x_g * sample.accel_x_g +
                      sample.accel_y_g * sample.accel_y_g +
                      sample.accel_z_g * sample.accel_z_g);
}

void ThresholdGate::Reset() {
    above_threshold_ = false;
    above_threshold_since_ms_ = 0;
    last_peak_ms_ = 0;
    queued_ = false;
    has_seen_sample_ = false;
}

GateDecision ThresholdGate::Evaluate(const AccelSample& sample) {
    const float magnitude = ComputeMagnitudeG(sample);
    const bool exceeds = magnitude >= kMagnitudeThresholdG;

    if (!has_seen_sample_) {
        has_seen_sample_ = true;
    }

    // §2.5 step 4: 10s with no new peak clears the queue. Checked before
    // the current sample's own threshold logic so a stale queued_ state
    // never survives a timeout even if this sample itself is below
    // threshold.
    if (queued_ && (sample.timestamp_ms - last_peak_ms_) > kQueueTimeoutMs) {
        queued_ = false;
    }

    if (exceeds) {
        if (!above_threshold_) {
            above_threshold_ = true;
            above_threshold_since_ms_ = sample.timestamp_ms;
        }
        last_peak_ms_ = sample.timestamp_ms;

        const uint32_t held_ms = sample.timestamp_ms - above_threshold_since_ms_;
        if (held_ms > kDurationThresholdMs) {
            queued_ = true;
            return GateDecision::kTriggerCnn;
        }
        return GateDecision::kSkip;
    }

    // Below threshold: §2.5 step 2 condition ("magnitude < 2.5g for >300ms")
    // resets the above-threshold hold clock. Note this is the *skip*
    // condition's own duration check, distinct from the trigger's duration
    // check above -- both use the same 300ms constant per the locked spec,
    // which only names one duration value.
    above_threshold_ = false;
    above_threshold_since_ms_ = sample.timestamp_ms;
    return GateDecision::kSkip;
}

}  // namespace spark::layer1
