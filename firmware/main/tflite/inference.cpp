// inference.cpp -- stub bodies. No TFLM MicroInterpreter constructed,
// no tensor arena allocated, no real .tflite FlatBuffer parsed beyond a
// size/null check. Wiring real TFLM is future work once the library is
// vendored as an ESP-IDF component.

#include "tflite/inference.h"

namespace spark::tflite_stub {

ModelStatus TfliteModel::LoadModel(const uint8_t* model_data, size_t model_size) {
    if (model_data == nullptr || model_size == 0) {
        return ModelStatus::kInvalidModelBuffer;
    }
    // TODO: real path is tflite::GetModel(model_data) + schema version
    // check + MicroInterpreter construction with a sized tensor arena.
    // Stub just records the pointer/size and marks itself loaded so
    // Invoke() has something to validate against.
    model_data_ = model_data;
    model_size_ = model_size;
    loaded_ = true;
    return ModelStatus::kOk;
}

ModelStatus TfliteModel::Invoke(const InferenceInput& input, InferenceOutput* output) {
    if (!loaded_) {
        return ModelStatus::kModelNotLoaded;
    }
    if (output == nullptr) {
        return ModelStatus::kInvalidModelBuffer;
    }
    // Stub inference: no real forward pass. Returns a fixed, deliberately
    // ambiguous 50/50 split rather than a fake-confident class, so callers
    // relying on ArgmaxClass() in tests don't accidentally treat stub
    // output as a real trained decision.
    (void)input;  // real path feeds this into interpreter->input(0)->data.f
    output->class_probs[0] = 0.5f;
    output->class_probs[1] = 0.5f;
    return ModelStatus::kOk;
}

}  // namespace spark::tflite_stub
