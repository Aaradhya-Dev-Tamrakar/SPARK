# SPARK — Rupesh's Quick Start Guide

**For:** Rupesh Kadel (79034 / BEI — Firmware Engineer)  
**Created:** October 20, 2026  
**Purpose:** One-stop onboarding document. Read this first, then move to the detailed task briefing.

---

## 1. What is SPARK?

**SPARK** = *Signal Pattern Analysis & Real-time Kinetics*

It's a **wearable fall detection system** for elderly people. A small device worn on the wrist detects if the person has fallen, and instantly sends an alert with an AI-generated clinical report to a caregiver's laptop.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        HOW SPARK WORKS                                  │
│                                                                         │
│   👤 Person wears device on wrist                                       │
│         │                                                               │
│         ▼                                                               │
│   ┌─────────────────────┐                                               │
│   │  ESP32-S3 Wearable  │  ◄── YOUR WORK LIVES HERE                    │
│   │  • MPU6050 IMU      │      (firmware/ directory)                    │
│   │  • Layer 1: Is this │                                               │
│   │    a possible fall?  │                                               │
│   │  • Layer 2: AI CNN  │                                               │
│   │    confirms fall     │                                               │
│   └────────┬────────────┘                                               │
│            │ BLE Bluetooth                                              │
│            ▼                                                            │
│   ┌─────────────────────┐                                               │
│   │  Laptop Gateway     │  ◄── Aaradhya's work                         │
│   │  • Receives alert   │      (gateway/ directory)                     │
│   │  • Runs SHAP AI     │                                               │
│   │    explainability    │                                               │
│   │  • Generates 1-page │                                               │
│   │    clinical PDF      │                                               │
│   └────────┬────────────┘                                               │
│            │ Local WiFi / REST API                                      │
│            ▼                                                            │
│   ┌─────────────────────┐                                               │
│   │  Phone/Web Display  │  ◄── Sonia's work                            │
│   │  • Shows fall events│      (gateway/server.py)                      │
│   │  • Downloads PDF    │                                               │
│   └─────────────────────┘                                               │
└─────────────────────────────────────────────────────────────────────────┘
```

### The Two-Layer Gate — Why It Matters

The wearable doesn't run the heavy AI model all the time (that would drain the battery in hours). Instead:

- **Layer 1 (Your code):** A simple math check runs 200 times per second. It calculates total acceleration: $|a| = \sqrt{a_x^2 + a_y^2 + a_z^2}$. If $|a| > 2.5g$ for over 300 ms → *"this might be a fall"* → wake up Layer 2.
- **Layer 2 (Your code):** A tiny 18.5 KB neural network (INT8 quantized CNN) runs on the ESP32-S3 and confirms whether it's actually a fall. Takes < 15 ms.

This saves ~80% battery because Layer 2 only runs when Layer 1 says "something happened."

---

## 2. The Team

| Person | Role | What They Own |
| :-- | :-- | :-- |
| **Aaradhya Dev Tamrakar** | Project Lead | ML model training, gateway SHAP explainability, clinical PDF reports, overall architecture |
| **Rupesh Kadel (You)** | Firmware Engineer | ESP32-S3 firmware, MPU6050 sensor driver, Layer 1 gate, TFLite Micro inference, BLE communication |
| **Sankalpa Lamsal** | Hardware/CAD | 3D-printed TPU wrist bracer enclosure, physical assembly |
| **Sonia Thapa** | Display Client | Mobile/web dashboard that shows fall events and PDF reports |

---

## 3. Repository Map — Where Your Code Lives

```
SPARK/
├── firmware/                        ◄◄◄ YOUR DIRECTORY ◄◄◄
│   ├── main/
│   │   ├── app_main.cpp             ← Entry point (has 2 modes: detector + data logger)
│   │   ├── drivers/
│   │   │   ├── mpu6050.cpp/h        ← IMU sensor I2C driver
│   │   ├── layer1/
│   │   │   ├── gate.cpp/h           ← Layer 1 threshold gate logic
│   │   ├── tflite/
│   │   │   ├── inference.cpp/h      ← TFLite Micro model loader + invoker
│   │   ├── comms/
│   │   │   ├── output.cpp/h         ← BLE GATT event transmission
│   │   │   ├── peak_features.cpp/h  ← Peak acceleration/gyro extraction
│   │   ├── models/
│   │   │   ├── spark_cnn_int8.h     ← THE AI MODEL (18.5 KB, don't edit manually)
│   │   ├── data_logger.cpp/h        ← 200 Hz continuous streaming mode
│   ├── test/
│   │   ├── test_gate.cpp            ← Layer 1 unit tests (21 tests)
│   │   ├── test_wire_format.cpp     ← JSON output format tests
│   ├── CMakeLists.txt               ← ESP-IDF build file
│   └── sdkconfig.defaults           ← ESP32-S3 target config
│
├── gateway/                         ← Aaradhya's gateway code
├── training/                        ← ML training pipeline (Aaradhya)
├── tools/
│   ├── record_cohort_data.py        ← You'll use this to test data logger streaming
│   └── verify_cohort_dataset.py
├── docs/
│   ├── WIRE_FORMAT_v1.md            ← JSON format your firmware must output (READ THIS)
│   ├── team_briefings/
│   │   └── RUPESH_FIRMWARE_PRE_HARDWARE_GUIDE.md  ← Your detailed task list
│   └── DATA_COLLECTION_PROTOCOL.md  ← 34-activity trial protocol
└── dev_logs/
    └── SPARK_TRACKER.md             ← Master project decision log
```

---

## 4. Getting Started — First Day Checklist

### Step 1: Clone the Repository

```bash
git clone https://github.com/Aaradhya-Dev-Tamrakar/SPARK.git
cd SPARK
```

### Step 2: Read These 3 Files (in order)

1. **This file** — you're reading it now ✓
2. [`docs/WIRE_FORMAT_v1.md`](file:///f:/Aaradhya-Dev-Tamrakar/SPARK/docs/WIRE_FORMAT_v1.md) — the JSON contract between your firmware and the gateway. Everything you transmit over BLE must match this format exactly.
3. [`docs/team_briefings/RUPESH_FIRMWARE_PRE_HARDWARE_GUIDE.md`](file:///f:/Aaradhya-Dev-Tamrakar/SPARK/docs/team_briefings/RUPESH_FIRMWARE_PRE_HARDWARE_GUIDE.md) — your complete 12-task checklist with acceptance criteria.

### Step 3: Run the Existing Unit Tests (No Hardware Needed)

```bash
cd firmware/test
mkdir -p build && cd build
cmake ..
cmake --build .
ctest --output-on-failure
```

**Expected:** 21/21 tests pass. This proves the Layer 1 gate math and wire format serialization are correct.

### Step 4: Set Up ESP-IDF Toolchain

1. Install [ESP-IDF v5.x](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/get-started/)
2. Set target:
   ```bash
   cd firmware
   idf.py set-target esp32s3
   ```
3. Build (no board needed to verify compilation):
   ```bash
   idf.py build
   ```

### Step 5: Simulate Without Hardware (Wokwi)

If physical boards haven't arrived yet:
1. Install the **Wokwi Simulator** VS Code extension.
2. Create `firmware/diagram.json` with an `esp32-s3-devkitc-1` and `mpu6050`.
3. Wire virtual I2C: SDA→GPIO 21, SCL→GPIO 22.
4. Press `F1` → `Wokwi: Start Simulator`.

### Step 6: When Physical Boards Arrive

Follow Tasks 5–8 in [`RUPESH_FIRMWARE_PRE_HARDWARE_GUIDE.md`](file:///f:/Aaradhya-Dev-Tamrakar/SPARK/docs/team_briefings/RUPESH_FIRMWARE_PRE_HARDWARE_GUIDE.md):
- Wire ESP32-S3 ↔ MPU6050 (SDA→GPIO 4, SCL→GPIO 5, INT→GPIO 6)
- Flash data logger mode, verify 200 Hz stream
- Compile full autonomous firmware, run memory audit
- Set up BLE GATT notifications

---

## 5. Key Specs to Keep in Your Head

| Parameter | Value | Why It Matters |
| :-- | :-- | :-- |
| **MCU** | ESP32-S3 WROOM-1 (Xtensa LX7 dual-core) | Has SIMD vector instructions for fast INT8 inference |
| **Sensor** | MPU6050 (3-axis accel + 3-axis gyro) | Mounted on top of wrist (dorsal side) |
| **Sampling Rate** | 200 Hz | 200 readings/sec × 6 axes = 1,200 values/sec |
| **I2C Address** | `0x68` | MPU6050 default |
| **I2C Pins** | SDA→GPIO 4, SCL→GPIO 5, INT→GPIO 6 | Locked in firmware and protocol docs |
| **Layer 1 Threshold** | $\|a\| > 2.5g$ for > 300 ms | Triggers CNN inference |
| **Layer 2 Model Size** | 18.5 KB (INT8 quantized) | Fits easily in ESP32-S3 Flash |
| **Tensor Arena** | 35–36.2 KB SRAM budget | TFLite Micro workspace for inference |
| **Layer 2 Latency Target** | < 15 ms per inference | ESP32-S3 + esp-nn SIMD acceleration |
| **Battery** | 1100 mAh LiPo + TP4056 charger | 8–11 hours active, 16–28 hours gated |
| **Communication** | BLE 5.0 GATT | JSON payload ~250–350 bytes per event |
| **Serial Baud (Logger)** | 921,600 baud | For high-speed 200 Hz data collection mode |

---

## 6. Two Firmware Modes (Important!)

The firmware has two compile-time modes controlled by `SPARK_FIRMWARE_MODE` in [`app_main.cpp`](file:///f:/Aaradhya-Dev-Tamrakar/SPARK/firmware/main/app_main.cpp):

| Mode | `#define` Value | When to Use |
| :-- | :-- | :-- |
| **Autonomous Detector** | `0` (default) | Normal operation — detects falls and sends BLE alerts |
| **Data Logger** | `1` | Data collection sessions — streams raw 200 Hz CSV over USB serial |

Switch modes by setting `-DSPARK_FIRMWARE_MODE=1` in your build config or `idf.py menuconfig`.

---

## 7. GitHub Issues Assigned to You

| Issue | Title | Priority |
| :-- | :-- | :-- |
| [**#1**](https://github.com/Aaradhya-Dev-Tamrakar/SPARK/issues/1) | Firmware: Integrate MPU6050 I2C Driver and Layer 1 Gate | 🔴 High — physical I2C + BLE |
| [**#11**](https://github.com/Aaradhya-Dev-Tamrakar/SPARK/issues/11) | ESP-IDF compilation, static memory audit & esp-nn SIMD validation | 🔴 High — verify firmware compiles and fits in memory |

---

## 8. Who to Ask

- **"How does the AI model work / what do the input tensors look like?"** → Ask Aaradhya. The model takes a $200 \times 6$ INT8 tensor (200 timesteps × 6 axes) and outputs `P(fall)`.
- **"What JSON format should the BLE payload be?"** → Read [`docs/WIRE_FORMAT_v1.md`](file:///f:/Aaradhya-Dev-Tamrakar/SPARK/docs/WIRE_FORMAT_v1.md). Don't guess.
- **"Where do I get the updated model after fine-tuning?"** → Aaradhya will give you a new `spark_cnn_int8.h`. Drop it into `firmware/main/models/` and rebuild.
- **"What activities do we record during data collection?"** → Read [`docs/DATA_COLLECTION_PROTOCOL.md`](file:///f:/Aaradhya-Dev-Tamrakar/SPARK/docs/DATA_COLLECTION_PROTOCOL.md) — 15 fall types + 19 daily activities.

---

> **Next step:** Open [`RUPESH_FIRMWARE_PRE_HARDWARE_GUIDE.md`](file:///f:/Aaradhya-Dev-Tamrakar/SPARK/docs/team_briefings/RUPESH_FIRMWARE_PRE_HARDWARE_GUIDE.md) and start working through the task checklist from Task 1.
