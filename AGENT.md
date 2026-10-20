# AGENT.md — Developer & AI Agent Guidelines

This repository contains **SPARK** (*Signal Pattern Analysis & Real-time Kinetics*), a proposed two-layer gated human fall detection and explainability system with offline SisFall artifacts and host-testable software. Physical wrist-worn, clinical, and integrated MCU validation remain pending. Robot fall monitoring is an open research extension requiring separate data, adaptation, and validation. All developers and AI coding agents operating on this codebase must adhere to the rules, architecture constraints, and conventions detailed below.

---

## 1. Non-Negotiable Project Architecture & Constraints

1. **Two-Layer Gated Fall Detection Pipeline**:
   - **Layer 1 (Intended MCU Gate)**: Host-testable threshold code currently triggers at magnitude $\ge 2.5g$ held for $>300\text{ ms}$. This differs from the older short-spike prose and requires design review and recall evaluation before deployment; pre-impact timing is not measured.
   - **Layer 2 (Intended MCU Classifier)**: Existing training preprocessing uses **100 Hz, 200 samples, six channels (2 s)**. The planned logger uses 200 Hz; a 200 Hz three-second model would require 600 samples and new evaluation. `tflite/inference.cpp` remains a stub, not running TFLite Micro. Resolve unit scaling, window buffering, model generation, and thresholds before integration.
   - **Gateway (Laptop Compute)**: BLE receiver, local JSON storage, peak-feature explanation fallback, optional raw-window gradient-times-input attribution, and PDF reporting (`reportlab`). Gradient attribution is not exact SHAP; v1 events omit raw windows, so waveform attribution requires a separately validated input path.
   - **Mobile Phone Client**: **Display-only** local-network reader. **DO NOT** implement on-phone BLE drivers or mobile-native SHAP/PDF compilation.

2. **Wire Format Protocol Invariance (`docs/WIRE_FORMAT_v1.md`)**:
   - Firmware-to-gateway event schema is strictly governed by `docs/WIRE_FORMAT_v1.md`.
   - v1 JSON payload includes `event_id`, `device_id`, `firmware_version`, `timestamp_ms`, `confidence` ($P(\text{fall}) = \text{class\_probs}[1]$), and six signed per-axis `peak_features` in g and degrees/s. It does not send `layer1_triggered` or a raw waveform; any such addition requires a versioned contract change.
   - Any modification to the protocol requires synchronized updates across both `firmware/` and `gateway/`.

3. **Hardware & Enclosure Locks**:
   - **MCU**: ESP32-S3 WROOM-1 (3 units departmental-ordered).
   - **Sensor**: MPU6050 6-axis IMU (mounted dorsal / top-of-wrist).
   - **Power**: 1100 mAh LiPo (Giga Nepal) + TP4056 charge/protection circuit.
   - **Enclosure**: Two-zone 3D-printed **TPU 95A** dorsal bracer, hook-and-loop Velcro closure, compression arm sleeve base layer.
   - **Electrical Safety Constraint**: Off-body charging only. Dual single-purpose USB-C ports (ESP32-S3 programming vs. TP4056 battery charge). Never operated on-body during charging.

4. **Single Sources of Truth (SSOT)**:
   - **Procurement & BOM**: [`docs/SPARK_Component_Order_Form.xlsx`](file:///d:/Aaradhya-Dev-Tamrakar/SPARK/docs/SPARK_Component_Order_Form.xlsx).
   - **Project Decisions & Status**: [`dev_logs/SPARK_TRACKER.md`](file:///d:/Aaradhya-Dev-Tamrakar/SPARK/dev_logs/SPARK_TRACKER.md).
   - **Thesis Figures & Assets (Google Drive)**: [SPARK Figures Drive](https://drive.google.com/drive/u/0/folders/1kOiDLc77xED4q5rOCQgz22sy2Uml5lAG).
   - **Deep-Research Evidence Base (19 Tracks)**: [`docs/SPARK_research_board_merged.md`](file:///d:/Aaradhya-Dev-Tamrakar/SPARK/docs/SPARK_research_board_merged.md).
   - **Post-Boards Resumption Roadmap**: [`docs/SPARK_POST_BOARDS_MASTER_PLAN.md`](file:///d:/Aaradhya-Dev-Tamrakar/SPARK/docs/SPARK_POST_BOARDS_MASTER_PLAN.md).
   - **Supervisor Progress Report**: [`docs/SPARK_SUPERVISOR_PROGRESS_REPORT.md`](file:///d:/Aaradhya-Dev-Tamrakar/SPARK/docs/SPARK_SUPERVISOR_PROGRESS_REPORT.md).
   - **Robotics & Hardware-Free Defense Strategy**: [`docs/SPARK_STRATEGIC_ROADMAP_ROBOTICS_AND_HARDWARE_DEFENSE.md`](file:///d:/Aaradhya-Dev-Tamrakar/SPARK/docs/SPARK_STRATEGIC_ROADMAP_ROBOTICS_AND_HARDWARE_DEFENSE.md).
   - **Pre-Hardware Team Task Briefings**: [`docs/team_briefings/README.md`](file:///d:/Aaradhya-Dev-Tamrakar/SPARK/docs/team_briefings/README.md).

---

## 2. Directory Layout & Module Ownership

```
SPARK/
├── firmware/          # [Rupesh Kadel] ESP-IDF ESP32-S3 C/C++ firmware
│   ├── main/          # Application entry, sensor drivers, Layer 1 gate, TFLite micro
│   └── test/          # Host-executable unit test suite (Unity/Ceedling/native)
├── training/          # [Aaradhya Dev Tamrakar] ML models & data pipelines
│   ├── data_prep/     # SisFall dataset ingestion & preprocessing (prepare_sisfall.py)
│   ├── notebooks/     # Assignment & baseline notebooks (Random Forest, XGBoost)
│   └── train_cnn.py   # Primary 1D/2D CNN training & TFLite quantizer
├── gateway/           # [Aaradhya Dev Tamrakar / Sonia Thapa] Laptop gateway
│   ├── receiver/      # BLE / Serial transport receivers
│   ├── shap_pipeline/ # Gateway SHAP explanation engine
│   ├── report/        # Clinical PDF report generator (ReportLab)
│   └── storage/       # Local JSON event logging
├── data/              # Datasets (raw & processed data gitignored)
├── docs/              # Proposal LaTeX sources, Wire Format, BOM spreadsheets
├── dev_logs/          # Master project tracker (SPARK_TRACKER.md) & CAD assets
├── sync.ps1           # Automated conventional-commit & rebase sync script
└── pyproject.toml     # PEP 517/621 package spec & tool configs
```

---

## 3. Engineering & Workflow Standards

- **Python Development**:
  - Always use `uv` for Python tooling: `uv run pytest`, `uv run ruff check --fix`, `uv run ruff format`.
  - Type hints and docstrings are mandatory for public functions.
- **Git Sync Routine**:
  - Local commit and push operations must run through `.\sync.ps1` to maintain commit hygiene and tracking synchronization.


---

## 4. Repository Governance & Agent Skills

To maintain code hygiene, cross-platform stability, and architectural rigor across multi-agent pair programming and developer contributions, the following ecosystem skills govern this codebase:

| Skill | Primary Scope & Enforced Directives | Reference |
| :--- | :--- | :--- |
| **`github-workflow`** | Issue anchoring (`#<id>`), feature branch isolation (`<type>/<slug>-#<id>`), conventional commits, deterministic multi-remote sync, and squash PR governance. | `.gemini/skills/github-workflow/` |
| **`background-task-governance`** | Prevents deadlocked processes on Windows. Zero interactive prompts, zero elevated UAC commands, script-first execution, and proactive 60s timeout watchdogs. | `~/.gemini/config/skills/background-task-governance/` |
| **`edge-ai-model-forge`** | Quantization clipping prevention, asymmetric focal loss, sub-100KB INT8 FlatBuffers, and ESP-NN vector kernel linkage on ESP32-S3. | `~/.gemini/config/skills/edge-ai-model-forge/` |
| **`latex-thesis-architect`** | Academic thesis defense compilation (`docs/SPARK_Mid_Defense/`, `docs/SPARK_Final_Defense/`), CPM DAG orchestration, and evidence audit registers. | `~/.gemini/config/skills/latex-thesis-architect/` |
| **`compliance-report-harmonizer`** | Formatting and standardization of clinical volunteer consent forms and 34-activity clipboard logs (`docs/cohort_forms/`). | `~/.gemini/config/skills/compliance-report-harmonizer/` |
| **`design-taste-gui`** | Caregiver Layer 3 mobile/web UI ergonomics, clinical priority badges, and calm telemetry data visualizations. | `~/.gemini/config/skills/design-taste-gui/` |
