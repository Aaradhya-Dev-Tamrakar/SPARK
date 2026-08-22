# SPARK — Signal Pattern Analysis & Real-time Kinetics

> **A Two-Layer Gated Edge-AI Wearable Fall Detection System with Clinical Explainability**  
> Major Project (8th Semester) — Department of Electronics & Computer Engineering, Kathmandu Engineering College (KEC), Institute of Engineering (IOE), Tribhuvan University, Nepal.

---

## 👥 Project Team & Supervision

| Role | Name | Primary Focus |
| :--- | :--- | :--- |
| **Project Lead** | **Aaradhya Dev Tamrakar** | Gateway Pipeline, SHAP Explainability & ML Modeling |
| **Firmware Engineer** | **Rupesh Kadel** | ESP32-S3 ESP-IDF Firmware, Layer 1 Gate & TFLite Micro |
| **Hardware Engineer** | **Sankalpa Lamsal** | 3D TPU Enclosure Design, Sensor Integration & Power |
| **Gateway / UI Engineer** | **Sonia Thapa** | Gateway Receiver, Clinical PDF Report & Web Dashboard |
| **Project Supervisor** | **Er. Dipen Manandhar** | Academic & Technical Supervision |

---

## 📊 Project Progress & Roadmap

> [!NOTE]
> **Board Exam Pause (August 22, 2026)**: Active development paused for board examinations. All context, 19-track deep-research synthesis, and phase-by-phase post-boards execution roadmap preserved in [`docs/SPARK_POST_BOARDS_MASTER_PLAN.md`](docs/SPARK_POST_BOARDS_MASTER_PLAN.md).

```
Overall Integrated Progress: [█████████░░░░░░░░░░░] 45% (Core ML/Gateway/Research Complete; Hardware Assembly, CAD, Nepal Cohort & Mobile UI Pending)
```

### Module Breakdown by Assignee

| Module / Workstream | Assignee | Status / Progress | Deliverable Reality |
| :--- | :--- | :---: | :--- |
| **ML Modeling & Quantization** | **Aaradhya Dev Tamrakar** | `[████████████████████] 100%` | SisFall ingestion, 1D CNN ($0.9185$ AUC-ROC), $18.5\text{ KB}$ INT8 quantizer & C-header export. |
| **Gateway & SHAP Subsystem** | **Aaradhya Dev Tamrakar** | `[████████████████████] 100%` | BLE client, multi-scenario SHAP explainer, PDF reports, and local REST server. |
| **Protocol & BOM Architecture** | **Aaradhya Dev Tamrakar** | `[████████████████████] 100%` | `WIRE_FORMAT_v1.md`, `DATA_COLLECTION_PROTOCOL.md`, and order form locked. |
| **Deep-Research Synthesis (19 Tracks)** | **Aaradhya Dev Tamrakar** | `[████████████████████] 100%` | Novelty claims narrowed (1, 3, 4), ML strategy locked (Focal Loss), protocol mapped (F09–F15, D15–D19), power budget sharpened, DFM guidelines, venue targets (ICACT 2027). |
| **Physical ESP32-S3 Firmware** | **Rupesh Kadel** | `[░░░░░░░░░░░░░░░░░░░░] 0%` | Host C++ tests pass, but **0% physical progress** (awaiting board delivery for on-chip I2C/BLE & silicon inference). |
| **Enclosure CAD & 3D Printing** | **Sankalpa Lamsal** | `[░░░░░░░░░░░░░░░░░░░░] 0%` | Concept art only; **0% CAD progress** (no `.step`/`.stl` parametric model, no TPU slicer profile, no prints). |
| **Layer 3 Mobile Display Client** | **Sonia Thapa** | `[░░░░░░░░░░░░░░░░░░░░] 0%` | Gateway backend REST API ready; **0% mobile UI progress** (no mobile app or frontend client built yet). |
| **Physical Nepal Trial Collection** | **Team (KEC Cohort)** | `[░░░░░░░░░░░░░░░░░░░░] 0%` | Protocol drafted; **0% trial data recorded** (pending physical hardware assembly & crash-mat sessions). |

---

## 🏗️ System Architecture

```
                                  WEARABLE NODE (ESP32-S3)
   ┌──────────────────┐        ┌────────────────────────────────────────────────────────┐
   │ MPU6050 6-DOF    │        │  [Layer 1: Pre-Impact Gate]                            │
   │ IMU @ 200 Hz     │───────>│  |a| > 2.5g, Δt < 300 ms (Host-testable C/C++)         │
   └──────────────────┘        └───────────────────────────┬────────────────────────────┘
                                                           │ (Triggered: Motion Window)
                               ┌───────────────────────────▼────────────────────────────┐
                               │  [Layer 2: Edge ML Classifier]                         │
                               │  Quantized 1D CNN on TFLite Micro (spark_cnn_int8.h)   │
                               └───────────────────────────┬────────────────────────────┘
                                                           │ BLE Notification (WIRE_FORMAT_v1)
                                                           ▼
                                  LOCAL GATEWAY (Laptop / Local Server)
   ┌────────────────────────────────────────────────────────────────────────────────────┐
   │  [BleReceiver / Replay / Serial] ──> [JSON Store] ──> [SHAP Attribution Engine]    │
   │                                                                 │                  │
   │                                                                 ▼                  │
   │                                                   [ReportLab Clinical PDF Report]  │
   │                                                                 │                  │
   │                                 ┌───────────────────────────────┘                  │
   │                                 ▼                                                  │
   │  [Gateway REST API & Embedded Web Dashboard Server] (gateway/server.py)           │
   └───────────────────────────────────────────────────────┬────────────────────────────┘
                                                           │ Local Network (HTTP / REST)
                                                           ▼
                                  DISPLAY CLIENT (Smartphone / Web UI)
   ┌────────────────────────────────────────────────────────────────────────────────────┐
   │  Layer 3 Read-Only Responsive Dashboard (Live Alert Feed & Clinical PDF Viewer)    │
   └────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🌿 Branching & Workstreams

| Branch | Lead / Assignee | Workstream Scope | Status |
| :--- | :--- | :--- | :---: |
| `main` | Team | Production stable, integrated deliverables & LaTeX reports | **STABLE** 🟢 |
| `feat/firmware-layer1` | `@RupeshKadel` | ESP32-S3 physical firmware, MPU6050 I2C driver & on-device TFLite Micro | **NOT STARTED / 0%** 🔴 |
| `feat/enclosure-cad` | `@SankalpaLamsal` | Parametric 3D CAD modeling, TPU 95A slicer tuning & physical print | **NOT STARTED / 0%** 🔴 |
| `feat/gateway-dashboard` | `@SoniaThapa` | Mobile display client UI & live gateway frontend | **NOT STARTED / 0%** 🔴 |
| `feat/training-pipeline` | `@AaradhyaDT` | SisFall raw ingestion, CNN architecture, and TFLite model quantizer | **MERGED** ✅ |
| `feat/gateway-shap` | `@AaradhyaDT` | BLE receiver, wire format parser, SHAP feature attribution & PDF report | **MERGED** ✅ |

---

---

## 📌 Active Development Tracking & Remaining Works

### ✅ Completed Milestones
- [x] **Proposal Defense**: Successfully defended mid-term proposal (Passed July 9, 2026).
- [x] **BOM & Procurement Lock**: Component order form finalized (`docs/SPARK_Component_Order_Form.xlsx`, Daraz/Himalayan Solution/Giga Nepal).
- [x] **Electrical Safety & Charging Architecture**: Dual single-purpose USB-C ports locked (Action #38, off-body charging only).
- [x] **Two-Layer ML Pipeline**: 1D CNN trained on SisFall with subject-grouped isolation ($0.9185$ AUC-ROC, $87.81\%$ sensitivity) and quantized to $18.5\text{ KB}$ INT8 (`spark_cnn_int8.tflite`).
- [x] **Firmware Model Embedding**: INT8 model byte array generated and wired into `firmware/main/models/spark_cnn_int8.h`.
- [x] **Gateway & Explainability**: BLE GATT client (`BleReceiver`), diverse clinical SHAP explainer, automated ReportLab PDF generator, and local REST API (`gateway/server.py`) delivered.
- [x] **Gateway Hardware Acceleration**: Intel Core Ultra 7 155H NPU and Arc iGPU benchmarked via OpenVINO (Action #27 resolved).
- [x] **Nepal Cohort Protocol**: 34-activity standardized trial protocol drafted (`docs/DATA_COLLECTION_PROTOCOL.md`, Action #23).

### ⏳ Remaining Works to Final Deployment
- [ ] **Physical Hardware Delivery & Bench Verification (Action #16 / #18)**: Receive departmental ESP32-S3 N16R8 boards, MPU6050 breakout, 1100mAh LiPo cells, and TP4056 modules for electrical bring-up.
- [ ] **Parametric 3D CAD & Slicing (Action #17)**: Finalize two-zone dorsal wrist bracer in CAD (`.step`/`.stl`), verify M2.5 screw boss wall thicknesses, and tune TPU 95A 3D print profile.
- [ ] **Nepal Cohort Data Collection Execution (Issue #6)**: Execute controlled crash-mat fall simulations and ADL recordings at KEC to fine-tune the CNN on real dorsal-wrist kinematics.
- [ ] **On-Hardware BLE & Layer 1 Validation**: Flash firmware to physical ESP32-S3, verify real-time Layer 1 threshold triggering on wrist motion, and validate end-to-end BLE event reception.
- [ ] **Layer 3 Mobile Display Client Integration (Issue #5)**: Connect mobile web dashboard to gateway REST endpoints (`GET /api/events`).
- [ ] **Thesis Draft & Defense Prep (Action #26)**: Narrow Novelty Claims 1 & 3 against recent 2024–2025 literature and finalize LaTeX thesis report (`thesis_report.tex`).

---

## 📂 Repository Directory Layout

```
SPARK/
├── .github/                      # GitHub workflows and PR templates
│   └── pull_request_template.md  # Standard pull request checklist
├── .pre-commit-config.yaml       # Pre-commit hooks (Ruff linter, formatter, file guards)
├── pyproject.toml                # PEP 517/621 package specification, Ruff & pytest configs
├── LICENSE                       # MIT License
├── AGENT.md                      # Universal AI agent & developer guidelines
├── AGENTS.md                     # Quick agent guidelines & command index
├── CLAUDE.md                     # Claude developer instructions
├── ANTIGRAVITY.md                # Google Antigravity & Gemini instructions
├── sync.ps1                      # Local git workflow: auto-stage, commit, rebase-pull, push
├── README.md                     # Master project documentation
│
├── firmware/                     # ESP-IDF C/C++ Firmware (Wearable Node)
│   ├── CMakeLists.txt            # ESP-IDF build configuration
│   ├── sdkconfig.defaults        # ESP32-S3 default hardware configuration
│   ├── main/                     # Application entry, sensor drivers, Layer 1 filter
│   │   └── models/               # Flash-resident INT8 model array (spark_cnn_int8.h)
│   └── test/                     # Host-executable unit tests (21/21 passed)
│
├── training/                     # Machine Learning & Data Pipelines
│   ├── data_prep/                # Dataset ingestion scripts (prepare_sisfall.py)
│   ├── notebooks/                # ML exploration & classical baselines (RF / XGBoost)
│   ├── train_cnn.py              # Primary 1D CNN training pipeline ($0.9185$ AUC-ROC)
│   ├── quantize_model.py         # INT8 post-training quantizer & C header exporter
│   └── requirements.txt          # ML training Python dependencies
│
├── gateway/                      # Local Gateway & Explainability Pipeline
│   ├── main.py                   # Gateway service entry point (BLE, Replay, Serial)
│   ├── server.py                 # Local REST API & Web Dashboard server
│   ├── receiver/                 # BleReceiver (bleak), ReplayReceiver, SerialReceiver
│   ├── shap_pipeline/            # CnnShapExplainer & PeakFeatureExplainer
│   ├── report/                   # ReportLab clinical PDF generator
│   └── storage/                  # JsonEventStore local JSON record archiving
│
├── tests/                        # Repository Python Test Suite (48/48 Passing)
│   ├── test_ble_receiver.py
│   ├── test_gateway_pipeline.py
│   ├── test_gateway_server.py
│   ├── test_json_store.py
│   ├── test_pdf_report.py
│   ├── test_quantize_model.py
│   ├── test_shap_pipeline.py
│   ├── test_train_cnn.py
│   └── test_wire_format.py
│
├── data/                         # Datasets & Trial Recordings (Gitignored)
│   ├── README.md                 # SisFall setup & Nepal trial dataset instructions
│   └── .gitkeep
│
├── docs/                         # Specifications & Academic Reports
│   ├── CHANGELOG.md              # Project change log (v55)
│   ├── DATA_COLLECTION_PROTOCOL.md # Nepal cohort human-subject trial protocol
│   ├── WIRE_FORMAT_v1.md         # Locked BLE event protocol schema
│   ├── SPARK_POST_BOARDS_MASTER_PLAN.md # Post-boards resumption roadmap & context archive
│   ├── SPARK_research_board_merged.md   # 19-track deep-research evidence base
│   ├── SPARK_Component_Order_Form.xlsx # Canonical hardware BOM procurement spreadsheet
│   ├── SPARK_Presentation_Mid_Term_Defense_v6.pptx # Mid-term defense slide deck
│   └── SPARK_Proposal/           # Complete LaTeX thesis proposal source
│       └── ThesisReports/        # LaTeX report (thesis_report.tex, compiling to PDF)
│
└── dev_logs/                     # Engineering Journals & Design Assets
    ├── SPARK_TRACKER.md          # Single source of truth master project tracker (v55)
    └── design-assets/            # 3D CAD references, master design sheet (v2), and walkthroughs
```

---

## 🛠️ Development & Tooling

This project uses [`uv`](https://github.com/astral-sh/uv) for fast, deterministic Python environment management and linting.

### Python Environment & Tests
```bash
# Run unit test suite
uv run pytest

# Check code with Ruff linter
uv run ruff check --fix

# Format code with Ruff formatter
uv run ruff format
```

### Firmware Host Unit Tests & Flashing (ESP-IDF)
```bash
# Run host-based firmware unit tests
cd firmware/test
# Compile and execute host test runner

# Build and flash to ESP32-S3 target
cd firmware
idf.py set-target esp32s3
idf.py build
idf.py -p COM_PORT flash monitor
```

### Building Academic LaTeX Report
```bash
cd docs/SPARK_Proposal/ThesisReports
latexmk -pdf thesis_report.tex
```
*Note: Build artifacts (`.aux`, `.log`, `.toc`, etc.) are gitignored; only [`thesis_report.pdf`](docs/SPARK_Proposal/ThesisReports/thesis_report.pdf) is tracked.*

---

## 🔄 Local Git Workflow (`sync.ps1`)

To maintain clean conventional commits and keep `SPARK_TRACKER.md` synchronized, use the provided PowerShell sync script:

```powershell
# Automatically stage, generate smart commit message, pull --rebase, and push
.\sync.ps1

# Sync with a custom conventional commit message
.\sync.ps1 -m "feat(training): optimize CNN hyperparameters"

# Build thesis_report.tex PDF first, then sync
.\sync.ps1 -Build

# Pull only (with autostash) without committing
.\sync.ps1 -PullOnly
```

---

## 📜 License

This project is licensed under the MIT License — see the [`LICENSE`](LICENSE) file for details.
