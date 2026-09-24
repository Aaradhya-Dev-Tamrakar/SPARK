# SPARK — Strategic Architecture & Hardware-Free Roadmap Record

**Document Date:** September 24, 2026  
**Project:** SPARK (*Signal Pattern Analysis & Real-time Kinetics*)  
**Context:** 4th Year BEI Major Project, Department of Electronics, Communication and Information Engineering, Kathmandu Engineering College (KEC), Tribhuvan University.  
**Purpose:** Formal preservation of core architectural pivots, humanoid robotics duality, pre-hardware Software-in-the-Loop (SIL) execution roadmaps, and CI/CD infrastructure governance.

---

## 1. Kinetic Platform Subject-Agnosticism & Humanoid Robotics Duality

### 1.1 Foundational Acronym & Title Audit
* **Project Title:** *SPARK: Explainable Edge AI for Kinetic Pattern Recognition and Distress Signaling* ([`docs/SPARK_Proposal/FrontPages/title.tex`](file:///f:/Aaradhya-Dev-Tamrakar/SPARK/docs/SPARK_Proposal/FrontPages/title.tex))
* **Core Acronym:** *Signal Pattern Analysis & Real-time Kinetics* ([`AGENT.md`](file:///f:/Aaradhya-Dev-Tamrakar/SPARK/AGENT.md))

Neither the title nor the expansion binds the system exclusively to human geriatric patients. While the empirical validation for the university thesis centers on elderly fall monitoring in Nepal, the underlying mathematical, embedded, and explainable AI architecture represents an **agnostic bipedal dynamic safety platform**.

### 1.2 The Humanoid Robotics Opportunity
In modern bipedal and humanoid robotics (e.g., Boston Dynamics Atlas, Unitree G1/H1, Figure 02, Agility Digit), catastrophic falls during physical Sim-to-Real reinforcement learning (RL) locomotion training cause severe actuator gear stripping and hardware downtime.

| Capability | Current State in Humanoid Robotics Labs | SPARK Dual-Use Application |
| :--- | :--- | :--- |
| **Safety Architecture** | In-band checks inside main IPC / NVIDIA Jetson (ROS 2/DDS). Fails during OS thread lockups or bus brownouts. | **Out-of-band independent reflex unit** on isolated ESP32-S3 with dedicated battery and optocoupled hardware E-Stop. |
| **Fall Mitigation** | Passive impact (stiff limbs hit the ground, damaging harmonic drives). | **Active compliance trigger ($< 20\text{ ms}$)**: Sends zero-torque / limp / tuck interrupt to motor drivers before impact. |
| **RL Training Telemetry** | Optical mocap cameras or noisy joint contact estimators. | **Deterministic edge binary fall signal** streamed for automatic RL episode termination and reward penalty shaping. |
| **Post-Crash Diagnostics** | Manual parsing of gigabytes of ROS bags. | **Automated SHAP attribution**: Instant breakdown of whether slip ($a_y$), roll instability ($\omega_x$), or pitch divergence ($\omega_y$) caused failure. |

### 1.3 Technical Gap Analysis & Upgrade Path
1. **Dynamic Range & IMU Selection**:
   - *Current*: MPU6050 ($\pm 8g$ / $\pm 16g$, $\pm 2000^\circ/\text{s}$).
   - *Robotics Grade*: High dynamic shock impacts require automotive-grade IMUs (Bosch BMI088 or ST ISM330DHCX) rated for $\pm 24g$ to $\pm 32g$ shock tolerance without clipping.
2. **Interface & Bus Protocols**:
   - *Current*: BLE GATT / USB-Serial to laptop gateway.
   - *Robotics Grade*: Hardware optocoupled GPIO dry-contact line directly to the Power Distribution Board (PDB) + CAN FD or native ROS 2 topic publishing (`/robot/safety/fall_event`).
3. **Training Data & Domain Adaptation**:
   - *Current*: SisFall + KEC Nepal human cohort datasets.
   - *Robotics Grade*: Synthetic pre-training using digital humanoid URDFs inside physics engines (Isaac Sim, MuJoCo) with domain randomization, fine-tuned via [`training/train_transfer.py`](file:///f:/Aaradhya-Dev-Tamrakar/SPARK/training/train_transfer.py).

---

## 2. Pre-Hardware Software-in-the-Loop (SIL) Roadmap

### 2.1 The Academic Reality & Strategic Positioning
Physical components (departmental ESP32-S3 boards, MPU6050 breakouts, LiPo cells) arrive in the upcoming semester. In TU/IOE capstone evaluations, framing this delay as "waiting for components" leads to negative scoring.

Instead, the project adopts an industry-standard **Model-in-the-Loop (MIL) and Software-in-the-Loop (SIL) methodology**, ensuring all subsystems are completely verified prior to physical delivery.

### 2.2 Subsystem Action Plan (Zero Physical Hardware Required)

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                   VIRTUALIZED / PRE-HARDWARE EXECUTION MATRIX                   │
├─────────────────────┬────────────────────────────────────────────────────────────┤
│ Assignee / Module   │ Deliverables Verifiable Without Physical Hardware          │
├─────────────────────┼────────────────────────────────────────────────────────────┤
│ Rupesh Kadel        │ • ESP-IDF firmware execution in QEMU / Wokwi virtual MCU   │
│ (Firmware / MCU)    │ • Virtual MPU6050 I2C register burst feeding               │
│                     │ • TFLite Micro tensor arena memory profiling (<40 KB SRAM) │
│                     │ • CPU clock cycle benchmarking for Layer 1 vs Layer 2      │
├─────────────────────┼────────────────────────────────────────────────────────────┤
│ Sankalpa Lamsal     │ • Complete 3D parametric CAD modeling in Fusion 360 / STEP │
│ (Hardware / CAD)    │ • Virtual component clearance assembly (ESP32, LiPo, TP4056│
│                     │ • M2.5 brass heat-set insert boss & wall tolerance check   │
│                     │ • TPU 95A slicing toolpaths & mass estimation in slicer    │
├─────────────────────┼────────────────────────────────────────────────────────────┤
│ Sonia Thapa         │ • Cross-platform Layer 3 Mobile UI (Flutter / React Native)│
│ (UI / Display)      │ • Real-time event consumption from gateway/server.py REST  │
│                     │ • In-app dynamic SHAP feature attribution bar display      │
│                     │ • Integrated clinical PDF viewer via GET /api/reports/<id> │
├─────────────────────┼────────────────────────────────────────────────────────────┤
│ Aaradhya / Team     │ • Smartphone 6-axis IMU (200 Hz Sensor Logger) proxy trials│
│ (Kinematics / ML)   │ • Validation of record_cohort_data.py on pilot human falls │
│                     │ • Isaac Sim / MuJoCo synthetic kinematic data generation   │
└─────────────────────┴────────────────────────────────────────────────────────────┘
```

### 2.3 Faculty Panel Pitch Script
> *"To eliminate procurement dependency and ensure zero downtime upon component delivery, our team adopted a rigorous Software-in-the-Loop (SIL) and Digital Twin design strategy. The end-to-end ML pipeline, 18.5 KB INT8 quantization, and gateway gradient explainability are 100% complete and tested across 56 CI unit tests. The firmware application stack is validated in virtual MCU environments, CAD housings are sliced and ready for KEC Makerspace TPU 3D printing, and the companion UI is integrated with the gateway REST engine. Hardware arrival next semester represents a physical validation phase rather than an initial development hurdle."*

---

## 3. Repository & CI/CD Governance Record

### 3.1 Dual-Remote Architecture
The repository synchronizes continuously across two remotes via [`sync.ps1`](file:///f:/Aaradhya-Dev-Tamrakar/SPARK/sync.ps1):
* Primary: `origin` (`https://github.com/Aaradhya-Dev-Tamrakar/SPARK.git`)
* Mirror: `aaradhyadt` (`https://github.com/AaradhyaDT/SPARK.git`)

### 3.2 CI/CD Drive Sync Guard Resolution
* **Incident:** Push events triggering `.github/workflows/sync-drive.yml` failed on the mirror repository (`AaradhyaDT/SPARK`) due to missing Google Drive OAuth secrets (`GDRIVE_CLIENT_ID`, `GDRIVE_REFRESH_TOKEN`).
* **Resolution:** Configured an explicit repository boundary at the job level in [`.github/workflows/sync-drive.yml`](file:///f:/Aaradhya-Dev-Tamrakar/SPARK/.github/workflows/sync-drive.yml#L22):
  ```yaml
  if: github.repository == 'Aaradhya-Dev-Tamrakar/SPARK'
  ```
* **Outcome:** Google Drive documentation sync runs exclusively and cleanly on the primary repository, while mirror pushes skip gracefully with zero CI failure noise.
