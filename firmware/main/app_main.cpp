// app_main.cpp -- ESP-IDF entry point. Wires the autonomous detection pipeline
// and the high-speed 200 Hz raw data logging mode for Nepal cohort collection.

#include "comms/output.h"
#include "data_logger.h"
#include "drivers/mpu6050.h"
#include "layer1/gate.h"
#include "models/spark_cnn_int8.h"
#include "tflite/inference.h"

// Operating Modes:
// 0: SPARK_MODE_AUTONOMOUS_DETECTOR (Layer 1 Gate -> Layer 2 INT8 CNN -> BLE Event)
// 1: SPARK_MODE_DATA_LOGGER (Continuous 200 Hz Raw 6-Axis Stream to Host CLI)
#define SPARK_MODE_AUTONOMOUS_DETECTOR 0
#define SPARK_MODE_DATA_LOGGER         1

#ifndef SPARK_FIRMWARE_MODE
#define SPARK_FIRMWARE_MODE SPARK_MODE_AUTONOMOUS_DETECTOR
#endif

extern "C" void app_main(void) {
    spark::drivers::Mpu6050Driver imu;
    imu.Init();

#if (SPARK_FIRMWARE_MODE == SPARK_MODE_DATA_LOGGER)
    // -------------------------------------------------------------
    // DATA LOGGER MODE: High-speed continuous 200 Hz streaming
    // -------------------------------------------------------------
    spark::logger::DataLogger logger;
    spark::logger::DataLoggerConfig log_cfg{
        .sampling_rate_hz = 200,
        .baud_rate = 921600,
        .channel = spark::logger::StreamChannel::kUsbSerial,
        .emit_csv_header = true,
    };
    logger.Init(log_cfg);

    spark::drivers::Mpu6050Sample sample;
    while (logger.IsActive()) {
        if (imu.ReadSample(&sample)) {
            logger.StreamSample(sample);
        }
        // In full timer ISR deployment, sampling is driven by 5 ms hardware timer.
        // Single read iteration for skeleton compilation.
        break;
    }

#else
    // -------------------------------------------------------------
    // AUTONOMOUS DETECTOR MODE: Layer 1 Gate -> Layer 2 INT8 CNN
    // -------------------------------------------------------------
    spark::layer1::ThresholdGate gate;
    spark::tflite_stub::TfliteModel model;
    spark::comms::OutputTransport transport(spark::comms::OutputChannel::kBle);

    transport.Init();
    // Load the flash-resident INT8 quantized CNN model
    model.LoadModel(spark_cnn_model, spark_cnn_model_len);

    spark::drivers::Mpu6050Sample raw_sample;
    imu.ReadSample(&raw_sample);

    spark::layer1::AccelSample accel_sample{
        .accel_x_g = static_cast<float>(raw_sample.accel_x_raw) / 2048.0f,  // ±16g scale
        .accel_y_g = static_cast<float>(raw_sample.accel_y_raw) / 2048.0f,
        .accel_z_g = static_cast<float>(raw_sample.accel_z_raw) / 2048.0f,
        .timestamp_ms = raw_sample.timestamp_us / 1000,
    };

    const spark::layer1::GateDecision decision = gate.Evaluate(accel_sample);
    if (decision == spark::layer1::GateDecision::kTriggerCnn) {
        spark::tflite_stub::InferenceInput input{};
        spark::tflite_stub::InferenceOutput output;
        model.Invoke(input, &output);

        const spark::comms::PeakFeatures peaks =
            spark::comms::ComputePeakFeatures(input);

        spark::comms::FallEvent event{
            .event_id = "evt_live_001",
            .device_id = "SPARK-01",
            .firmware_version = "v1.2.0-int8",
            .timestamp_ms = accel_sample.timestamp_ms,
            .gate_decision = decision,
            .inference = output,
            .peak_features = peaks,
        };
        transport.SendFallEvent(event);
    }
#endif
}

