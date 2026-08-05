// gate.h -- Layer 1 hardware-gated thresholding, per proposal §2.5 (locked spec).
//
// Pure functions: no I2C, no ESP-IDF headers, no hardware dependency.
// Host-testable/compilable against mock sensor arrays (see firmware/test/).
//
// Algorithm (verbatim from §2.5):
//   1. magnitude = sqrt(ax^2 + ay^2 + az^2)
//   2. if magnitude < 2.5g for > 300ms -> skip CNN (assumed non-fall)
//   3. if threshold exceeded -> queue window -> CNN inference -> Layer 2
//   4. timeout: if no new peak acceleration for 10s, clear the queue
//
// Parameters are FIXED, not empirically tuned (Action #7, open, blocked
// on real fall-simulation data -- out of scope here).

#pragma once

#include <cstddef>
#include <cstdint>

namespace spark::layer1 {

// Locked thresholds, §2.5. Do not retune here -- Action #7 owns calibration
// and Action #4 (adaptive sensitivity via config, no reflash) is the
// intended path for runtime overrides, not a code change to these constants.
constexpr float kMagnitudeThresholdG = 2.5f;
constexpr uint32_t kDurationThresholdMs = 300;
constexpr uint32_t kQueueTimeoutMs = 10000;

// One accelerometer sample for gate evaluation. Deliberately narrower than
// drivers::Mpu6050Sample (no gyro, no raw LSB) -- gate.cpp works in
// already-converted g units and milliseconds so it stays hardware-agnostic
// and trivially mockable.
struct AccelSample {
    float accel_x_g;
    float accel_y_g;
    float accel_z_g;
    uint32_t timestamp_ms;
};

enum class GateDecision {
    kSkip,       // below threshold or not yet held long enough -- don't run CNN
    kTriggerCnn, // threshold exceeded for >300ms -- queue for Layer 2
};

// sqrt(ax^2 + ay^2 + az^2). Exposed standalone since it's independently
// testable and reused by both the gate and (eventually) SHAP feature prep.
float ComputeMagnitudeG(const AccelSample& sample);

// Stateful gate: tracks how long magnitude has stayed >= threshold, and
// the queue-timeout clock. Call Evaluate() once per incoming sample in
// timestamp order. Not thread-safe -- single-producer sample loop assumed
// (matches the ESP32-S3 single sensor-read task).
class ThresholdGate {
public:
    ThresholdGate() = default;

    // Feed one sample, get a decision. Pure state machine -- no I/O.
    GateDecision Evaluate(const AccelSample& sample);

    // True from the sample that crosses kDurationThresholdMs held-above-
    // threshold until Reset() or a timeout clears it. Exposed for testing
    // the "queue" concept from §2.5 step 3 without needing a real queue.
    bool IsQueued() const { return queued_; }

    void Reset();

private:
    bool above_threshold_ = false;
    uint32_t above_threshold_since_ms_ = 0;
    uint32_t last_peak_ms_ = 0;
    bool queued_ = false;
    bool has_seen_sample_ = false;
};

}  // namespace spark::layer1
