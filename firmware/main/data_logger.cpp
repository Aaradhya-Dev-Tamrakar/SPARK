// data_logger.cpp -- Implementation of 200 Hz raw IMU data logger for SPARK.

#include "data_logger.h"
#include <cstdio>
#include <cstring>

namespace spark {
namespace logger {

bool DataLogger::Init(const DataLoggerConfig& config) {
    config_ = config;
    sample_count_ = 0;
    is_active_ = true;

    if (config_.emit_csv_header) {
        printf("Timestamp_ms,Ax_raw,Ay_raw,Az_raw,Gx_raw,Gy_raw,Gz_raw\n");
    }
    return true;
}

size_t DataLogger::FormatCsvFrame(const drivers::Mpu6050Sample& sample, char* out_buf, size_t max_len) {
    if (!out_buf || max_len == 0) {
        return 0;
    }

    uint32_t timestamp_ms = static_cast<uint32_t>(sample.timestamp_us / 1000);
    int written = snprintf(out_buf, max_len, "%u,%d,%d,%d,%d,%d,%d\n",
                           timestamp_ms,
                           sample.accel_x_raw,
                           sample.accel_y_raw,
                           sample.accel_z_raw,
                           sample.gyro_x_raw,
                           sample.gyro_y_raw,
                           sample.gyro_z_raw);

    if (written < 0 || static_cast<size_t>(written) >= max_len) {
        return 0;
    }
    return static_cast<size_t>(written);
}

bool DataLogger::StreamSample(const drivers::Mpu6050Sample& sample) {
    if (!is_active_) {
        return false;
    }

    char frame_buf[128];
    size_t len = FormatCsvFrame(sample, frame_buf, sizeof(frame_buf));
    if (len == 0) {
        return false;
    }

    // Direct stdout / UART transmission at configured baud
    fputs(frame_buf, stdout);
    sample_count_++;
    return true;
}

}  // namespace logger
}  // namespace spark
