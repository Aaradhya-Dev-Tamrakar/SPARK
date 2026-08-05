// mpu6050.cpp -- stub bodies only. No real I2C transaction issued.
// Blocked: bus timing/calibration (explicit scope exclusion this session).

#include "drivers/mpu6050.h"

namespace spark::drivers {

Mpu6050Status Mpu6050Driver::Init() {
    // TODO(Action #24 + #18): once board is in hand and reuse-vs-rewrite is
    // decided, this becomes either:
    //   (a) a real i2c_master_bus_add_device() + WHO_AM_I read + config
    //       register writes (this-driver path), or
    //   (b) a thin call into the ported FallGuard init routine.
    // Neither happens here -- stub always reports success so callers
    // (Layer 1 gate, app_main) can be built/tested against this interface
    // without hardware.
    initialized_ = true;
    return Mpu6050Status::kOk;
}

Mpu6050Status Mpu6050Driver::ReadSample(Mpu6050Sample* out_sample) {
    if (!initialized_) {
        return Mpu6050Status::kNotInitialized;
    }
    if (out_sample == nullptr) {
        return Mpu6050Status::kI2cError;
    }
    // Stub: zeroed sample, no bus read. Real read + esp_timer_get_time()
    // stamping is blocked (I2C bus timing, explicit scope exclusion).
    *out_sample = Mpu6050Sample{0, 0, 0, 0, 0, 0, 0};
    return Mpu6050Status::kOk;
}

}  // namespace spark::drivers
