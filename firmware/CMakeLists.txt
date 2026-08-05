# SPARK wearable node -- ESP32-S3, ESP-IDF project root.
# Target set via `idf.py set-target esp32s3` (not invoked here; local build step, Action #18 gates board-in-hand testing).

cmake_minimum_required(VERSION 3.16)
include($ENV{IDF_PATH}/tools/cmake/project.cmake)
project(spark_wearable)
