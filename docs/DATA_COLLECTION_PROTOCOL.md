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

### 4.1 Fall Simulation Trials (15 Trials across 8 Mechanisms)

| Code | Activity Description | Biomechanical Mechanism | Execution Instructions |
| :--- | :--- | :--- | :--- |
| **F01** | Forward trip while walking | Forward Trip | Walk 3 paces on approach, simulate tripping on obstacle, fall forward onto hands/mat. |
| **F02** | Forward fall from slip | Forward Slip | Walk forward, feet slip forward, fall forward/lateral onto mat. |
| **F03** | Forward stumble with failed recovery | Forward Stumble | Stumble forward, attempt 2 recovery steps, collapse onto crash mat. |
| **F04** | Backward slip while walking | Backward Slip | Walk forward, heel slips forward, fall backward onto buttocks/back on mat. |
| **F05** | Backward fall while sitting | Backward Miss | Attempt to sit on chair, miss seat, fall backward onto crash mat. |
| **F06** | Backward collapse from sit-to-stand | Postural Collapse | Rise from chair, experience sudden weakness, collapse backward onto mat. |
| **F07** | Lateral fall (Left flank) | Lateral Slip | Walk forward, lose balance to the left, fall on left flank/arm onto mat. |
| **F08** | Lateral fall (Right flank) | Lateral Slip | Walk forward, lose balance to the right, fall on right flank/arm onto mat. |
| **F09** | Sideways stumble over obstacle | Lateral Obstacle | Stumble sideways over raised obstacle, roll onto lateral torso on mat. |
| **F10** | Syncope / Fainting vertical collapse | Syncope / Faint | Stand still, simulate sudden loss of consciousness, vertical knee buckle onto mat. |
| **F11** | Wall-sliding vertical collapse | Syncope / Faint | Stand near wall, slide vertically downward in collapse onto mat. |
| **F12** | Slow dizzy collapse from chair | Syncope / Faint | Slump sideways/forward from seated chair position onto floor mat. |
| **F13** | Torso twist slip during rapid turn | Rotational Twist | Make 90-degree turn, foot slips, twist torso while falling onto mat. |
| **F14** | Step-down twist fall from low platform | Rotational Step | Step down from 15 cm platform, misjudge step, twist fall onto mat. |
| **F15** | Rolling out of bed onto mat | Rolling Fall | Lie on low cot/bench, roll over edge onto crash mat. |

### 4.2 Activities of Daily Living (ADL) Trials (19 Trials)

| Code | Activity Description | Category | Duration / Repetitions |
| :--- | :--- | :--- | :--- |
| **D01** | Normal level-ground walking | Locomotion | 10 meters continuous walking |
| **D02** | Fast walking / brisk pace | Locomotion | 10 meters continuous |
| **D03** | Jogging | Locomotion | 10 meters continuous |
| **D04** | Ascending stairs | Locomotion | 1 flight of stairs (10–12 steps) |
| **D05** | Descending stairs | Locomotion | 1 flight of stairs (10–12 steps) |
| **D06** | Sit-to-stand from chair | Postural Transition | 5 repetitions at natural pace |
| **D07** | Stand-to-sit onto chair | Postural Transition | 5 repetitions at natural pace |
| **D08** | Bending to pick up object from floor | Postural Transition | 5 repetitions |
| **D09** | Reaching upward to high shelf | Postural Transition | 5 repetitions |
| **D10** | Violent coughing & sneezing | Physiological ADL | 3 simulated episodes |
| **D11** | Stumbling / near-fall recovery | Dynamic Recovery | Trip on mat edge but catch balance without falling (3 reps) |
| **D12** | Clapping, waving, and gesturing | Upper-Limb Dynamics | 30 seconds active arm movement |
| **D13** | Typing on computer keyboard | Fine Motor | 60 seconds continuous typing |
| **D14** | Writing on paper / notebook | Fine Motor | 60 seconds continuous writing |
| **D15** | Sweeping floor with broom | Domestic Task | 60 seconds continuous sweeping |
| **D16** | Drinking water from glass / bottle | Arm Posture | 5 repetitions of lifting, drinking, placing glass |
| **D17** | Tying shoelaces while seated | Postural Flexion | 3 repetitions of bending forward to tie shoes |
| **D18** | Squatting and rising | Lower-Limb ADL | 5 repetitions of deep squat and standing |
| **D19** | Turning around 360 degrees | Rotational ADL | 5 complete turns while standing |

---

## 5. Elderly Kinematic Gap & Klenk Lean-and-Release Protocol

Elderly real-world falls exhibit significantly lower impact accelerations ($3.5\text{--}6.0g$) compared to vigorous young adult simulations ($8.0\text{--}12.0g$). To simulate frail elderly kinematics safely among young volunteers:
* **Klenk Lean-and-Release Method**: Participants lean against an elastic tether attached to a quick-release mechanism at $15^\circ\text{--}25^\circ$ angles.
* **Controlled Muscle Release**: Upon tether release, participants simulate delayed muscle reflex response, collapsing into the crash mat without protective arm braking.
* **Partial-Freeze Fine-Tuning**: Captured low-impact trials calibrate the classifier decision threshold $\tau^*$ via Youden's $J$ statistic without altering pre-trained convolutional feature weights.

---

## 6. Data File Format & Storage Schema

To ensure $100\%$ interoperability with SPARK's training pipeline (`prepare_nepal_cohort.py`), all recorded files conform to the SisFall schema:

### 6.1 Directory & File Naming
```
data/
  nepal_cohort/
    F01_SA01_R01.csv
    F01_SA01_R02.csv
    ...
    D19_SA20_R03.csv
```

### 6.2 File Schema (CSV with Header)
```csv
Ax,Ay,Az,Gx,Gy,Gz
-0.1245,0.4521,0.9812,1.25,-4.10,0.32
-0.1189,0.4498,0.9754,1.40,-3.95,0.28
```
* Accelerations in $g$ ($1g = 9.80665\text{ m/s}^2$).
* Angular rates in $^\circ/\text{s}$ (degrees per second).

---

## 7. Informed Consent & Ethics Checklist (KEC)

1. [ ] **Informed Consent**: Participant reviews and signs the KEC Ethics Information Sheet.
2. [ ] **Physical Check**: Screening for bone fractures, joint pain, or vestibular conditions.
3. [ ] **Rig Fitment**: Wearable node mounted securely on dorsal wrist over compression sleeve.
4. [ ] **Crash Mat Verification**: 20–30 cm gymnastic mat in place with 2 spotters ready.
5. [ ] **Trial Capture**: Operator runs `python tools/record_cohort_data.py --subject SA01 --activity F01 --trial R01`.
6. [ ] **Verification**: Run `python tools/verify_cohort_dataset.py` before participant departs.
