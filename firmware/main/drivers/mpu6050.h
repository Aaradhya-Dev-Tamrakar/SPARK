// mpu6050.h -- MPU6050 I2C driver, clean rewrite skeleton.
//
// Action #24 (reuse-vs-rewrite vs FallGuard driver) is still OPEN --
// this is a fresh-written interface, not a port of the FallGuard driver.
// Rationale: no FallGuard driver source is present in this repo to diff
// against or reuse from, so a clean skeleton is the only buildable option
// right now. Swap-in of the FallGuard driver, if Rupesh/Aaradhya decide
// to reuse it, replaces this file's .cpp body only -- this header's
// interface is written to be a plausible target for that swap (raw
// accel/gyro read + init only, no filtering/fusion baked in).
//
// I2C bus timing, pin assignment, and clock speed are BLOCKED pending
// board-in-hand (Action #18) -- see mpu6050.cpp for stub bus calls.

#pragma once

#include <cstdint>

namespace spark::drivers {

// Raw sensor sample, one IMU read. Units: LSB (raw register values), not
// yet converted to g / deg-per-sec -- scale factors depend on the FS_SEL /
// AFS_SEL config, which isn't locked yet (Action #24 dependent).
struct Mpu6050Sample {
    int16_t accel_x;
    int16_t accel_y;
    int16_t accel_z;
    int16_t gyro_x;
    int16_t gyro_y;
    int16_t gyro_z;
    uint32_t timestamp_us;  // esp_timer_get_time() at read
};

enum class Mpu6050Status {
    kOk,
    kI2cError,
    kNotInitialized,
    kInvalidWhoAmI,
};

class Mpu6050Driver {
public:
    Mpu6050Driver() = default;

    // Bus/pin config intentionally NOT plumbed through yet -- blocked on
    // Action #18 (board in hand). init() signature is stable; body is a
    // stub until real I2C timing/calibration work starts.
    Mpu6050Status Init();

    // Blocking single-sample read at whatever ODR was set in Init().
    // 200 Hz target per §2.5 (locked spec) -- ODR register write is stubbed.
    Mpu6050Status ReadSample(Mpu6050Sample* out_sample);

    bool IsInitialized() const { return initialized_; }

private:
    bool initialized_ = false;
};

}  // namespace spark::drivers
