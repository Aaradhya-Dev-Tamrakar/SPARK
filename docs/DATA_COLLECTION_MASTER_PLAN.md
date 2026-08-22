# SPARK — Nepal Cohort Data Collection Setup & Execution Master Plan

**Document Status:** High-Priority Post-Boards Execution Plan  
**Target Window:** Week 1 (Days 4–7) to Week 2 Post-Board Exams  
**Location:** Kathmandu Engineering College (KEC) Robotics & Electronics Lab  
**Lead Author:** Aaradhya Dev Tamrakar  
**Related Documents:** [`docs/DATA_COLLECTION_PROTOCOL.md`](file:///d:/Aaradhya-Dev-Tamrakar/SPARK/docs/DATA_COLLECTION_PROTOCOL.md), [`docs/SPARK_POST_BOARDS_MASTER_PLAN.md`](file:///d:/Aaradhya-Dev-Tamrakar/SPARK/docs/SPARK_POST_BOARDS_MASTER_PLAN.md)

---

## 1. Executive Summary

To validate the SPARK system against real South Asian biomechanics, bridge the elderly kinematic gap ($8\text{--}12g$ youth vs. $3.5\text{--}6g$ elderly), and train the transfer-learned edge classifier, we establish a standardized **3-Tier Data Collection Setup**:

```
┌────────────────────────────────────────────────────────┐
│ 1. WEARABLE LOGGER NODE (ESP32-S3 + MPU6050)           │
│    • Continuous 200 Hz Hardware Timer ISR (5 ms delta) │
│    • Raw register reads (±16g accel, ±2000 dps gyro)   │
│    • Un-gated raw streaming over USB-Serial / BLE      │
└──────────────────────────┬─────────────────────────────┘
                           │ (USB-Serial @ 921600 baud / BLE GATT Stream)
                           ▼
┌────────────────────────────────────────────────────────┐
│ 2. GATEWAY INGESTION & ANNOTATION CLI TOOL             │
│    • Interactive Session CLI (Subject, Activity, Trial)│
│    • Live Packet Health & Rate Monitor (200 Hz verify) │
│    • Automated SisFall-Compatible CSV Exporter         │
│    • Output: data/nepal_cohort/F01_SA01_R01.csv        │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ 3. POST-PROCESSING & MODEL TRANSFER PIPELINE           │
│    • Window Slicer (38,426 SisFall + Nepal Cohort)     │
│    • Partial-Freeze Fine-Tuning (Conv1D Freeze)        │
│    • INT8 Re-quantization & C-Header Export            │
└────────────────────────────────────────────────────────┘
```

---

## 2. Hardware & Firmware Logger Configuration

### 2.1 Hardware Wiring
* **Microcontroller**: ESP32-S3 (WROOM-1-CAM / N16R8)
* **Sensor**: InvenSense MPU6050 6-axis IMU breakout
* **Pin Connections**:
  * `SDA`: GPIO 21 (or GPIO 4)
  * `SCL`: GPIO 22 (or GPIO 5)
  * `INT`: GPIO 6 (hardware motion interrupt pin)
  * `VCC`: 3.3V DC rail
  * `GND`: Common Ground
* **Mounting**: Dorsal (top) side of non-dominant/dominant wrist, secured with an elastic Velcro bracer over a compression arm sleeve base layer.

### 2.2 Firmware Architecture (`firmware/main/data_logger.cpp`)
* **Operating Mode**: `SPARK_MODE_DATA_LOGGER` (bypasses Layer 1 gating and Layer 2 inference).
* **Sampling Rate**: Exact $200\text{ Hz}$ clock generated via ESP32-S3 hardware timer ISR ($\Delta t = 5.0\text{ ms}$).
* **Sensor Ranges**:
  * Accelerometer: $\pm 16g$ ($2048\text{ LSB}/g$)
  * Gyroscope: $\pm 2000^\circ/\text{s}$ ($16.4\text{ LSB}/(^\circ/\text{s})$)
* **Serial Stream Protocol**:
  * Baud Rate: **921,600 baud** over USB-C CDC.
  * CSV Frame Format: `TIMESTAMP_MS,AX_RAW,AY_RAW,AZ_RAW,GX_RAW,GY_RAW,GZ_RAW\n`

---

## 3. Gateway Ingestion & Labeling Tooling

### 3.1 Interactive CLI Recorder (`tools/record_cohort_data.py`)
A dedicated Python tool for the recording operator:
1. **Participant Enrollment**: Prompts for Subject ID (`SA01` through `SA20`), age, gender, height (cm), and weight (kg).
2. **Activity Selection**: Quick-select menu for all 34 activities (**F01–F15**, **D01–D19**).
3. **Automated Trial Increment**: Auto-tracks repetitions (`R01`, `R02`, `R03`).
4. **Recording Flow**:
   * Visual/audible 3-2-1 countdown.
   * Starts capture buffer.
   * Real-time sample counter & frequency lock ($200 \pm 1\text{ Hz}$).
   * Operator presses `[SPACE]` to stop trial upon completion.
5. **Validation & Quality Control**:
   * Checks for frame drops or jitter ($>10\text{ ms}$ interval flags warning).
   * Checks for sensor saturation/clipping at $\pm 16g$.
   * Confirms minimum duration ($3\text{ s}$ for falls, $10\text{--}120\text{ s}$ for ADLs).
6. **Storage Schema**:
   * Saves to `data/nepal_cohort/<Activity>_<Subject>_<Trial>.csv` (e.g. `data/nepal_cohort/F01_SA01_R01.csv`).
   * Headers: `Ax,Ay,Az,Gx,Gy,Gz` (calibrated units: $g$ and $^\circ/\text{s}$).

### 3.2 Dataset Verifier (`tools/verify_cohort_dataset.py`)
* Scans `data/nepal_cohort/` and generates a 34-activity completion grid per subject.
* Highlights missing trials or corrupted files before participants leave the laboratory.

---

## 4. Physical Lab Setup & Experimental Protocol (KEC)

### 4.1 Safety & Environment
* **Location**: KEC Electronics & Robotics Laboratory.
* **Crash Mat**: High-density multi-layer gymnastic crash mat ($20\text{--}30\text{ cm}$ thickness, $2.0\text{ m} \times 1.5\text{ m}$ surface).
* **Personnel**: 2 trained spotters positioned on the mat flanks to assist participants during fall recovery.
* **Warm-Up**: 5-minute guided joint warm-up (wrists, shoulders, knees).

### 4.2 Cohort Demographics & Sample Size
* **Target Cohort**: $N = 12\text{--}20$ healthy student and faculty volunteers (aged 18–35).
* **Statistical Basis**: Grounded in pilot clinical study sample size conventions (*Julious, 2005*).
* **Ethics**: Standardized KEC informed consent form signed prior to recording.

### 4.3 Standardized 34-Activity Matrix

| Code | Activity Category | Description | Target Trials |
| :--- | :--- | :--- | :--- |
| **F01** | Forward Fall | Forward trip while walking | 3 trials |
| **F02** | Forward Fall | Forward slip on slick surface | 3 trials |
| **F03** | Forward Fall | Forward stumble with failed recovery | 3 trials |
| **F04** | Backward Fall | Backward slip on heels while walking | 3 trials |
| **F05** | Backward Fall | Backward loss of balance while sitting | 3 trials |
| **F06** | Backward Fall | Backward collapse from sit-to-stand | 3 trials |
| **F07** | Lateral Fall | Lateral slip to the Left | 3 trials |
| **F08** | Lateral Fall | Lateral slip to the Right | 3 trials |
| **F09** | Lateral Fall | Sideways stumble over obstacle | 3 trials |
| **F10** | Syncope / Faint | Vertical collapse (knees buckle) | 3 trials |
| **F11** | Syncope / Faint | Wall-sliding vertical collapse | 3 trials |
| **F12** | Syncope / Faint | Slow dizzy collapse from chair | 3 trials |
| **F13** | Rotational Fall | Torso twist slip during rapid turn | 3 trials |
| **F14** | Rotational Fall | Step-down twist fall from low platform | 3 trials |
| **F15** | Rolling Fall | Rolling out of bed onto mat | 3 trials |
| **D01–D05** | Locomotion ADLs | Normal walk, brisk walk, jogging, stair climbing (up/down) | 3–5 trials |
| **D06–D12** | Postural ADLs | Sit-to-stand, stand-to-sit, bending, tying shoes, squatting, reaching | 3–5 trials |
| **D13–D19** | Upper-Limb ADLs | Clapping, arm waving, sweeping, typing, writing, coughing/sneezing | 30–120s blocks |

---

## 5. Machine Learning Ingestion & Transfer Learning

1. **Window Segmentation (`training/data_prep/prepare_nepal_cohort.py`)**:
   * Slices continuous CSVs into $200 \times 6$ windows ($1.0\text{ s}$ duration) with 50% overlap during impact zones.
   * Merges with the 38,426 SisFall baseline windows.
2. **Partial-Freeze Fine-Tuning (`training/train_transfer.py`)**:
   * **Frozen Layers**: Conv1D Block 1 (32 filters) & Conv1D Block 2 (64 filters) pre-trained on SisFall.
   * **Trainable Layers**: Classification Dense Head (32 ReLU + 2 Softmax).
   * **Loss Function**: Focal Loss ($\gamma=2.0, \alpha=0.75$) with positive class weighting ($1.25\times$) to drive sensitivity $\ge 90\%$.
3. **Quantization & Firmware Deployment**:
   * INT8 Post-Training Quantization with class-balanced representative dataset.
   * Auto-export of `spark_cnn_int8.h` ($18.5\text{ KB}$) into `firmware/main/models/`.

---

## 6. Execution Checklist & Resumption Timeline

| Step | Action Item | Target Window |
| :--- | :--- | :--- |
| **1** | Assemble physical ESP32-S3 + MPU6050 dorsal wrist rig with Velcro strap | Week 1, Day 4 |
| **2** | Implement `firmware/main/data_logger.cpp` & test 921600 baud streaming | Week 1, Day 5 |
| **3** | Build `tools/record_cohort_data.py` & verify 0-drop loopback recording | Week 1, Day 6 |
| **4** | Conduct crash-mat dry-run with team members at KEC | Week 1, Day 7 |
| **5** | Execute 34-activity collection across $N=12\text{--}20$ volunteers | Week 2 (Days 1–5) |
| **6** | Run `prepare_nepal_cohort.py` and execute Partial-Freeze Fine-Tuning | Week 3, Days 1–3 |
| **7** | Re-quantize INT8 model, flash autonomous firmware, and run live mat validation | Week 3, Days 4–7 |
