// peak_features.h -- per-axis peak extraction from a trigger window, for
// WIRE_FORMAT_v1.md's `peak_features` field.
//
// Computes one peak value per channel (a_x,a_y,a_z,w_x,w_y,w_z) over the
// same 200x6 window already built for TfliteModel::Invoke -- no separate
// buffering, no change to ThresholdGate (accel-only, hardware-agnostic by
// design; extending it with gyro would break that scoping per gate.h's
// own doc comment). This lives alongside tflite/ instead since it reads
// tflite_stub::InferenceInput's exact layout (flat, row-major
// [sample][channel], channel order ax,ay,az,gx,gy,gz -- see inference.h).
//
// "Peak" = max absolute value per channel across all 200 samples in the
// window (WIRE_FORMAT_v1.md: "max magnitude sample per axis"). Pure
// function, no I2C/hardware -- host-testable like layer1/gate.h.

#pragma once

#include "tflite/inference.h"

namespace spark::comms {

// Field order matches wire_format.py's IMU_CHANNELS = (a_x, a_y, a_z,
// w_x, w_y, w_z) -- keep in sync if that tuple's order ever changes.
struct PeakFeatures {
    float a_x;
    float a_y;
    float a_z;
    float w_x;
    float w_y;
    float w_z;
};

// Scans `window` (must be a fully-populated 200x6 buffer, same one passed
// to TfliteModel::Invoke) and returns the max-absolute-value sample per
// channel. Channel-to-axis mapping fixed by inference.h's documented
// layout: index 0..5 per sample = ax,ay,az,gx,gy,gz.
PeakFeatures ComputePeakFeatures(const tflite_stub::InferenceInput& window);

}  // namespace spark::comms
