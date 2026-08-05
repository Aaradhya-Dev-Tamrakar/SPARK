idf_component_register(
    SRCS
        "app_main.cpp"
        "drivers/mpu6050.cpp"
        "layer1/gate.cpp"
        "tflite/inference.cpp"
        "comms/output.cpp"
    INCLUDE_DIRS
        "."
    REQUIRES
        driver
        esp_timer
)

# TFLite Micro is not yet vendored/registered as an ESP-IDF component --
# `tflite/inference.cpp` is a compile-checked stub against a placeholder
# API surface (see tflite/inference.h), not a real TFLM link target yet.
