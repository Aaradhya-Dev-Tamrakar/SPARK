// data_logger.h -- High-throughput 200 Hz raw IMU data logger for SPARK Nepal cohort data collection.
// Bypasses Layer 1 gating and Layer 2 inference to stream continuous 6-axis kinematics over Serial / BLE.

#pragma once

#include <cstdint>
#include <cstddef>
#include "drivers/mpu6050.h"

namespace spark {
namespace logger {

enum class StreamChannel {
    kUsbSerial,
    kBleGatt,
};

struct DataLoggerConfig {
    uint32_t sampling_rate_hz = 200;
    uint32_t baud_rate = 921600;
    StreamChannel channel = StreamChannel::kUsbSerial;
    bool emit_csv_header = true;
};

class DataLogger {
public:
    DataLogger() = default;
    ~DataLogger() = default;

    // Initialize the logger hardware/transport
    bool Init(const DataLoggerConfig& config);

    // Format and transmit a single 6-axis raw sample frame.
    // CSV output format: TIMESTAMP_MS,AX_RAW,AY_RAW,AZ_RAW,GX_RAW,GY_RAW,GZ_RAW\n
    bool StreamSample(const drivers::Mpu6050Sample& sample);

    // Formats a calibrated CSV frame into destination buffer.
    // Returns number of bytes written.
    static size_t FormatCsvFrame(const drivers::Mpu6050Sample& sample, char* out_buf, size_t max_len);

    uint32_t GetSampleCount() const { return sample_count_; }
    bool IsActive() const { return is_active_; }

private:
    DataLoggerConfig config_{};
    bool is_active_ = false;
    uint32_t sample_count_ = 0;
};

}  // namespace logger
}  // namespace spark
