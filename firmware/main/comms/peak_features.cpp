#include "comms/peak_features.h"

#include <cmath>

namespace spark::comms {

PeakFeatures ComputePeakFeatures(const tflite_stub::InferenceInput& window) {
    PeakFeatures peaks{0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f};
    float* channel_peaks[6] = {&peaks.a_x, &peaks.a_y, &peaks.a_z,
                                &peaks.w_x, &peaks.w_y, &peaks.w_z};

    for (int sample = 0; sample < tflite_stub::kWindowSamples; ++sample) {
        for (int channel = 0; channel < tflite_stub::kChannelsPerSample; ++channel) {
            const float value =
                window.data[sample * tflite_stub::kChannelsPerSample + channel];
            const float value_abs = std::fabs(value);
            if (value_abs > std::fabs(*channel_peaks[channel])) {
                *channel_peaks[channel] = value;  // keep sign, compare by magnitude
            }
        }
    }
    return peaks;
}

}  // namespace spark::comms
