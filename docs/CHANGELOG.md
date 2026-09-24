# CHANGELOG

All notable changes and repository sync events for the **SPARK** project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

- Hardware bring-up and physical on-chip testing on ESP32-S3 boards.
- KEC cohort experimental collection campaign.

## [v57] - 2026-09-24

### Subject-Agnostic Kinetic Platform & Robotics Extension

- **Bipedal & Humanoid Robotics Safety Module Extension (`docs/SPARK_Proposal/Chapters/`)**:
  - `chapter1_introduction.tex`: Formalized Domain #7 (*Autonomous Bipedal Robotics & Humanoid Training*) under Section 1.5 Application of the Project for out-of-band crash telemetry, instantaneous reflex compliance triggering, and Sim-to-Real RL episode termination.
  - `chapter5_methodology.tex`: Generalized Strategy Pattern sensitivity labels from human-exclusive tags to descriptive kinetic dynamics: `HighSensitivity` (frail gait / low-torque threshold), `Standard` (default), and `SportMode` (dynamic locomotion / agile maneuvers).
  - `chapter6_expected_output.tex`: Added formal subsection on *Bipedal Robotics Safety & Sim-to-Real Crash Mitigation* outlining synthetic pre-training in physics engines (MuJoCo, Isaac Sim), hardware GPIO optoisolated E-stop integration, and industrial CAN FD / ROS 2 diagnostic topics.
- **Wire Format Specification Updated (`docs/WIRE_FORMAT_v1.md`)**:
  - Documented v2 `subject_type` metadata field (`"human"` vs `"bipedal_robot"`) enabling automated template switching between clinical incident reports and robotics engineering diagnostic logs.
- **Master Guidelines & Architecture Alignment (`AGENT.md`, `CLAUDE.md`, `README.md`)**:
  - Re-aligned high-level project framing with official title ("*Explainable Edge AI for Kinetic Pattern Recognition and Distress Signaling*"), emphasizing core kinetic pattern recognition engine and dual applicability across wearable healthcare and autonomous robotics.
- **Quality Assurance & Verification**:
  - Verified complete Python test suite passing cleanly (**56/56 unit tests passed**, 0 regressions).

## [v56] - 2026-08-22

### Thesis Figures Verified & Drive Asset Repository Linked

- Thesis Diagram Audit & Redesign Completed: `fig_system_flow.png`, `fig_two_layer_flow.png`, and `fig_cnn_architecture.png` redesigned with orthogonal layout matching locked firmware/gateway specs.
- Project Assets & Google Drive Link Registered.
- Automated thesis PDF compilation integrated into `sync.ps1 -Build`.

## [v55] - 2026-08-22

### Deep-Research Synthesis & Board Exam Pause

- **19-Track Deep-Research Synthesis (`docs/SPARK_research_board_merged.md`)**: Completed and merged 19 focused research tracks covering novelty claim narrowing (Claims 1, 3, 4), ML sensitivity strategy (Focal Loss over architecture swap), SisFall protocol mapping (F09–F15, D15–D19), cohort sample sizing ($N=12\text{--}20$), TPU 95A DFM guidelines (brass heat-set inserts), power budget sharpening ($90\text{--}130\text{ mA}$ active, $35\text{--}60\text{ mA}$ event-gated BLE), commercial landscape analysis, and publication venue identification (ICACT 2027 / IEEE Healthcom).
- **Post-Boards Master Resumption Plan (`docs/SPARK_POST_BOARDS_MASTER_PLAN.md`)**: Created comprehensive context preservation archive and 5-phase execution roadmap (Protocol Lockdown → Hardware Logger Rig → Nepal Cohort Collection → Transfer Learning & Quantization → Live Validation & Defense) for resumption after board examinations.
- **Tracker Updated**: Added board exam pause notice and post-boards plan cross-reference to `dev_logs/SPARK_TRACKER.md`.

---

## [v54] - 2026-08-20

### Pipeline Execution & Explainability

- **Full Workflow Execution**: End-to-end pipeline run from SisFall dataset extraction (38,426 windows), subject-grouped 1D CNN training ($0.9185$ AUC-ROC), and INT8 quantization ($18.5\text{ KB}$ flash) to firmware C-header export.
- **Diverse Fall Replay Simulation (`gateway/main.py`)**: Generated 4 distinct clinical fall archetypes (Forward Trip, Lateral Slip, Syncope Collapse, Rotational Twist) verifying differentiated SHAP saliency bars and ReportLab clinical PDFs.
- **Aquatic & Drowning Detection Roadmap**: Formulated and documented secondary modular aquatic safety architecture (stroke cadence, IDR struggle index, submersion timer) as a future research expansion.

---

## [v53] - 2026-08-20

### Gateway & Protocols

- **BLE GATT Receiver (`gateway/receiver/receiver.py`)**: Implemented `BleReceiver` with asynchronous `bleak` peripheral scanning, connection, and notification callback handlers.
- **Gateway REST & Dashboard Server (`gateway/server.py`)**: Delivered standalone HTTP server (`GET /`, `/api/health`, `/api/events`, `/api/events/<id>`, `/api/reports/<id>`) with CORS support and embedded dark-mode UI, unblocking Layer 3 display client.
- **Data Collection Protocol (`docs/DATA_COLLECTION_PROTOCOL.md`)**: Formally specified 34-activity protocol (15 falls, 19 ADLs) for Nepal validation cohort (Action #23 / Issue #6).
- **Test Suite**: Expanded to 48 passing unit tests.

---

## [v52] - 2026-08-20

### Benchmarking & Firmware

- **Action #27 Resolved**: Benchmarked Intel Core Ultra 7 155H hardware engines via OpenVINO (CPU AVX-VNNI: 131 µs, Arc GPU: 200 µs / 4,993 fps, AI Boost NPU: 383 µs / 2,610 fps).
- **Firmware Model Embed**: Embedded real $18.5\text{ KB}$ C-header byte blob (`models/spark_cnn_int8.h`) into `firmware/main/app_main.cpp`.
- **Live Replay Verification**: Replay pipeline executed with real `spark_cnn.keras` model generating verified clinical PDF reports and JSON archives in `data/gateway_events/`.

---

## [v51] - 2026-08-20

### Machine Learning & Optimization

- **Model Optimization**: Implemented Youden's $J$ threshold tuning (optimal threshold $0.41$), positive class loss boost ($1.8\times$), temporal data augmentation, dropout ($0.15$), and batch normalization ($93.58\%$ AUC-ROC, $87.75\%$ sensitivity).
- **Quantization Calibration**: Balanced 50/50 FALL/NON_FALL representative sampling preserving INT8 sensitivity ($87.43\%$).

---

## [v50] - 2026-08-20

### Gateway & Explainability

- **SHAP Explainability Subsystem**: Delivered `CnnShapExplainer` and `PeakFeatureExplainer` in `gateway/shap_pipeline/explainer.py`.
- **Clinical PDF Generator**: Implemented one-page incident PDF report in `gateway/report/pdf_report.py`.
- **Receivers & Storage**: Implemented `ReplayReceiver`, `SerialReceiver`, and `JsonEventStore`.

---

## [v49] - 2026-08-20

### Machine Learning & Quantization

- **INT8 Quantizer**: Implemented standalone post-training quantization in `training/quantize_model.py` generating $18.5\text{ KB}$ `spark_cnn_int8.tflite` and C-header `spark_cnn_int8.h` ($87.7\%$ compression vs FP32).

---

## [v48] - 2026-08-11

### Sourcing & Hardware

- Action #39: Fasteners confirmed and selected via local Daraz kit (M2/M2.5/M3 machine screw assortment).
- Enclosure TPU 95A 1kg filament roll priced (NPR 4,000). Total BOM updated to ~NPR 13,877 in `SPARK_Component_Order_Form.xlsx`.

---

## [v37] - 2026-08-10

### Proposal & Tooling

- Proposal made VS Code / LaTeX Workshop compile-ready with `ThesisReports/.latexmkrc`.
- Removed stale BOM duplicate; `docs/SPARK_Component_Order_Form.xlsx` locked as sole canonical BOM.
- Added LaTeX build ignore patterns in `.gitignore`.

---

## [v27] - 2026-08-06

### Firmware & Gateway

- Merged initial `firmware-skeleton` (Layer 1 gate with 21/21 passing host tests) and `gateway-skeleton`.
- Locked communication protocol in `docs/WIRE_FORMAT_v1.md`.

---

## [v23] - 2026-07-23

### Training

- Added `training/data_prep/prepare_sisfall.py` (SisFall 200 Hz window generator).
- Proposal defence successfully defended on July 9, 2026.
