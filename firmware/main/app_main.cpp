// app_main.cpp -- ESP-IDF entry point. Wires the stubbed pipeline
// (driver -> Layer 1 gate -> TFLite stub -> comms stub) together so the
// project builds/flashes end-to-end, even though every stage but the
// gate logic is a stub. No real hardware loop timing yet.

#include "comms/output.h"
#include "drivers/mpu6050.h"
#include "layer1/gate.h"
#include "tflite/inference.h"

extern "C" void app_main(void) {
    spark::drivers::Mpu6050Driver imu;
    spark::layer1::ThresholdGate gate;
    spark::tflite_stub::TfliteModel model;
    spark::comms::OutputTransport transport(spark::comms::OutputChannel::kBle);

    imu.Init();
    transport.Init();
    // model.LoadModel() intentionally not called here yet -- no placeholder
    // model is flash-embedded into this build (tools/make_placeholder_model.py
    // output is gitignored, local-only). Real embed step is future work
    // once the actual quantized model exists (Action #3).

    // Real sample loop (200 Hz per §2.5) is NOT implemented -- would need
    // esp_timer periodic callback or FreeRTOS task with vTaskDelay, both
    // blocked on I2C bus timing (explicit scope exclusion this session).
    // This is a structural placeholder so app_main compiles and the
    // pipeline's call order is visible/reviewable.
    spark::drivers::Mpu6050Sample raw_sample;
    imu.ReadSample(&raw_sample);

    spark::layer1::AccelSample accel_sample{
        .accel_x_g = 0.0f,  // TODO: apply AFS_SEL scale factor once locked (Action #24)
        .accel_y_g = 0.0f,
        .accel_z_g = 0.0f,
        .timestamp_ms = raw_sample.timestamp_us / 1000,
    };

    const spark::layer1::GateDecision decision = gate.Evaluate(accel_sample);
    if (decision == spark::layer1::GateDecision::kTriggerCnn) {
        spark::tflite_stub::InferenceInput input{};
        spark::tflite_stub::InferenceOutput output;
        model.Invoke(input, &output);

        spark::comms::FallEvent event{
            .timestamp_ms = accel_sample.timestamp_ms,
            .gate_decision = decision,
            .inference = output,
        };
        transport.SendFallEvent(event);
    }
}
