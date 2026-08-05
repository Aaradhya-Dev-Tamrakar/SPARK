// inference.h -- TFLite Micro stub: model-loading interface + inference
// call signature only. TFLM library is NOT vendored/linked yet -- this
// compiles standalone against a placeholder .tflite byte blob, no real
// tensor arena or interpreter wired up.
//
// I/O shape locked from training/train_cnn.py (Stage 3, §2.4):
//   Input:  200 x 6 float32 window (200 samples, 6 channels: ax,ay,az,gx,gy,gz)
//   Output: 2 x float32 (Softmax: [P(NON_FALL), P(FALL)], class 1 = FALL)
// Quantization: INT8 per proposal, but this stub's public interface stays
// float32 in/out -- dequantization at the API boundary is an inference.cpp
// implementation detail, not exposed here, so callers (app_main, tests)
// don't need to know the on-device tensor dtype.

#pragma once

#include <cstddef>
#include <cstdint>

namespace spark::tflite_stub {

constexpr int kWindowSamples = 200;
constexpr int kChannelsPerSample = 6;  // ax, ay, az, gx, gy, gz
constexpr int kInputSize = kWindowSamples * kChannelsPerSample;
constexpr int kOutputClasses = 2;      // [NON_FALL, FALL]

enum class ModelStatus {
    kOk,
    kModelNotLoaded,
    kInvalidModelBuffer,
    kArenaAllocFailed,   // reserved -- stub never actually allocates
    kInvokeFailed,       // reserved -- stub never actually invokes TFLM
};

// One flattened window, row-major [sample][channel]. Matches the .npy
// layout prepare_sisfall.py/train_cnn.py already use (windows.npy shape
// (N, 200, 6)) so a real implementation can memcpy from that format later.
struct InferenceInput {
    float data[kInputSize];
};

struct InferenceOutput {
    float class_probs[kOutputClasses];  // Softmax output, sums to ~1.0

    int ArgmaxClass() const {
        return class_probs[1] > class_probs[0] ? 1 : 0;
    }
};

// Model-loading + inference interface. Real implementation (TFLM
// MicroInterpreter, AllOpsResolver, tensor arena sizing) is TBD --
// this class's job right now is to give app_main.cpp and tests a
// stable call signature to build against.
class TfliteModel {
public:
    TfliteModel() = default;

    // model_data must outlive this object (TFLM convention: models are
    // typically flash-resident `const unsigned char[]` arrays, not
    // copied). model_size in bytes.
    ModelStatus LoadModel(const uint8_t* model_data, size_t model_size);

    // Blocking single-window inference. Returns kModelNotLoaded if
    // LoadModel() wasn't called or failed.
    ModelStatus Invoke(const InferenceInput& input, InferenceOutput* output);

    bool IsLoaded() const { return loaded_; }

private:
    bool loaded_ = false;
    const uint8_t* model_data_ = nullptr;
    size_t model_size_ = 0;
};

}  // namespace spark::tflite_stub
