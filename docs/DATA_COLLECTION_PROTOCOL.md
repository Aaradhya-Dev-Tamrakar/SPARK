# SPARK Human-Subject Movement & Fall Simulation Protocol (Nepal Cohort)

**Project:** Signal Pattern Analysis & Real-time Kinetics (SPARK)  
**Document ID:** `SPARK-PROTO-01-v1`  
**Institution:** Kathmandu Engineering College (KEC), Tribhuvan University  
**Lead Author / Lead:** Aaradhya Dev Tamrakar  
**Related Tracker Actions:** Action #23, Issue #6  

---

## 1. Objective & Scope

This protocol specifies the standardized procedure for recording human-subject kinematic data (3-axis linear acceleration and 3-axis angular velocity at 200 Hz) using the SPARK wearable device. The resulting dataset will serve to:
1. Validate and calibrate the **Layer 1 Pre-Impact Fall Gate** ($|a| > 2.5g, \Delta t < 300\text{ ms}$).
2. Fine-tune the **Layer 2 Quantized 1D CNN Classifier** on wrist-worn kinematics specific to the Nepali participant cohort.
3. Benchmark the gateway's **SHAP Explainability Subsystem** on real human fall trajectories.

---

## 2. Ethical Compliance & Safety Standards

### 2.1 Participant Safety & Fall Simulation Environment
* **Crash Mat Protection:** All simulated falls must be performed onto a dedicated high-density gymnastic crash mat with minimum thickness of **$30\text{ cm}$** and dimensions of at least $2.0\text{ m} \times 1.5\text{ m}$.
* **Spotters:** Two trained team spotters must be positioned at the sides of the mat to guide descent if necessary.
* **Warm-up:** Participants must complete a 5-minute guided joint warm-up before performing simulated falls.

### 2.2 Inclusion & Exclusion Criteria
* **Inclusion Criteria:**
  - Healthy adults aged 18–35 (KEC student/faculty volunteers for active fall simulations).
  - Willingness to wear the dorsal wrist device and execute daily activities and controlled falls.
  - Signed informed consent form.
* **Exclusion Criteria:**
  - History of recent bone fractures or musculoskeletal injuries within the past 12 months.
  - Vestibular disorders, vertigo, or chronic balance impairment.
  - Cardiovascular conditions or unmanaged hypertension.
  - Pregnancy.

---

## 3. Sensor Hardware Configuration & Mounting

### 3.1 Device Placement
* **Location:** Dorsal (top) side of the non-dominant wrist (or dominant wrist per experimental block).
* **Attachment:** Compression arm sleeve base layer worn under the 3D-printed TPU bracer, secured firmly using hook-and-loop Velcro closure to eliminate skin-motion slippage artifacts.

### 3.2 Coordinate Reference Frame
* **$+X$ Axis:** Longitudinal, pointing along the forearm toward the fingertips.
* **$+Y$ Axis:** Lateral, pointing toward the thumb (radial direction).
* **$+Z$ Axis:** Normal to the wrist surface, pointing outward (away from the dorsal skin surface).

### 3.3 Sampling Specifications
* **Sampling Rate:** $200\text{ Hz}$ ($\Delta t = 5.0\text{ ms}$).
* **Accelerometer Range:** $\pm 16g$ ($2048\text{ LSB}/g$).
* **Gyroscope Range:** $\pm 2000^\circ/\text{s}$ ($16.4\text{ LSB}/(^\circ/\text{s})$).
* **Units:** Acceleration in $g$ ($9.80665\text{ m/s}^2$), Angular Velocity in $^\circ/\text{s}$ (dps) or $\text{rad/s}$.

---

## 4. Experimental Activity Protocol Matrix

Each participant executes a total of **34 standardized activity trials** (15 falls and 19 activities of daily living).

### 4.1 Fall Simulation Trials (15 Trials)

| Code | Activity Description | Execution Instructions |
| :--- | :--- | :--- |
| **F01** | Forward trip while walking | Walk 3 paces on approach, simulate tripping on obstacle, fall forward onto hands/mat. |
| **F02** | Forward fall from slip | Walk forward, feet slip forward, fall forward/lateral onto mat. |
| **F03** | Backward slip while walking | Walk forward, heel slips forward, fall backward onto buttocks/back on mat. |
| **F04** | Backward fall while sitting | Attempt to sit on chair, miss seat, fall backward onto crash mat. |
| **F05** | Lateral fall (Left) | Walk forward, lose balance to the left, fall on left flank/arm onto mat. |
| **F06** | Lateral fall (Right) | Walk forward, lose balance to the right, fall on right flank/arm onto mat. |
| **F07** | Syncope / Fainting collapse | Stand still, simulate sudden loss of consciousness, vertical knee collapse onto mat. |
| **F08** | Fall while standing up from chair | Rise from seated position, experience dizziness, collapse onto nearby mat. |

### 4.2 Activities of Daily Living (ADL) Trials (19 Trials)

| Code | Activity Description | Duration / Repetitions |
| :--- | :--- | :--- |
| **D01** | Normal level-ground walking | 10 meters continuous walking |
| **D02** | Fast walking / brisk pace | 10 meters continuous |
| **D03** | Jogging | 10 meters continuous |
| **D04** | Ascending stairs | 1 flight of stairs (10–12 steps) |
| **D05** | Descending stairs | 1 flight of stairs (10–12 steps) |
| **D06** | Sit-to-stand from chair | 5 repetitions at natural pace |
| **D07** | Stand-to-sit onto chair | 5 repetitions at natural pace |
| **D08** | Bending to pick up object from floor | 5 repetitions |
| **D09** | Reaching upward to high shelf | 5 repetitions |
| **D10** | Violent coughing & sneezing | 3 simulated episodes |
| **D11** | Stumbling / near-fall recovery | Trip on mat edge but catch balance without falling |
| **D12** | Clapping, waving, and gesturing | 30 seconds active arm movement |
| **D13** | Typing on computer keyboard | 60 seconds continuous typing |
| **D14** | Writing on paper / notebook | 60 seconds continuous writing |

---

## 5. Data File Format & Storage Schema

To ensure $100\%$ interoperability with SPARK's existing training pipeline (`prepare_sisfall.py`), all recorded files must conform to the following format:

### 5.1 Directory Structure
```
data/
  raw_nepal_cohort/
    README.txt
    Subject_SA01/
      FALL_F01_SA01_R01.txt
      FALL_F02_SA01_R01.txt
      ADL_D01_SA01_R01.txt
      ...
    Subject_SA02/
      ...
```

### 5.2 File Format
* Plain text ASCII, comma-separated values (CSV format without header).
* 6 columns per line:
  ```
  accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z
  ```
* Sample line:
  ```
  -0.1245, 0.4521, 0.9812, 1.25, -4.10, 0.32
  ```

---

## 6. Checklist & Execution Protocol

1. [ ] Inspect crash mat position and secure perimeter.
2. [ ] Fit wearable on participant with snug Velcro tension.
3. [ ] Verify BLE telemetry stream active on gateway laptop.
4. [ ] Record subject metadata: Subject ID, age, gender, height (cm), weight (kg).
5. [ ] Execute ADL protocol block (D01–D14).
6. [ ] Rest interval (3 minutes).
7. [ ] Execute Fall simulation block (F01–F08).
8. [ ] Verify file integrity and absence of dropped packets.
