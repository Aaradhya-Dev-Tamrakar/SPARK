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

```
Overall Progress: [████████████████░░░░] 80% (Mid-Term Complete / Procurement Locked)
```

- **Firmware & Layer 1 Gate**: `[████████████████████] 100%` (21/21 Host Unit Tests Passed, ESP-IDF Scaffold, INT8 Model Embedded)
- **Model Training & Quantization**: `[████████████████████] 100%` (SisFall Ingestion, 1D CNN with 93.58% AUC-ROC, INT8 Quantizer & C Header Export)
- **Wire Format & Schema**: `[████████████████████] 100%` (Locked in `docs/WIRE_FORMAT_v1.md`)
- **BOM & Procurement**: `[████████████████████] 100%` (Locked in `docs/SPARK_Component_Order_Form.xlsx`)
- **Proposal & Academic Reports**: `[████████████████████] 100%` (Proposal Defended, LaTeX Thesis Compiling)
- **Gateway & SHAP Engine**: `[████████████████████] 100%` (BLE/Replay/Serial Receivers, SHAP Explainer, Clinical PDF Reports, REST & Web Dashboard Server)
- **Hardware Assembly & CAD**: `[██████████░░░░░░░░░░] 50%` (Concept Locked; Pending Sliced TPU Model & S3 Boards)

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
| `feat/firmware-layer1` | `@RupeshKadel` | ESP32-S3 firmware, MPU6050 I2C driver, Layer 1 gate & TFLite Micro | **ACTIVE** 🟡 |
| `feat/gateway-dashboard` | `@SoniaThapa` | Local gateway web interface & mobile display client UI | **ACTIVE** 🟡 |
| `feat/enclosure-cad` | `@SankalpaLamsal` | Two-zone TPU wrist bracer CAD 3D modeling, slicing & mounting | **ACTIVE** 🟡 |
| `feat/training-pipeline` | `@AaradhyaDT` | SisFall raw ingestion, CNN architecture, and TFLite model quantizer | **MERGED** ✅ |
| `feat/gateway-shap` | `@AaradhyaDT` | BLE receiver, wire format parser, SHAP feature attribution & PDF report | **MERGED** ✅ |

---

## 📌 Active Development Tracking (from `SPARK_TRACKER.md`)

- [x] **#14**: Revert ESP32-S3 vendor to Himalayan Solutions (N16R8, in stock)
- [x] **#23**: Finalize human-subject trial protocol for Nepal validation dataset (`docs/DATA_COLLECTION_PROTOCOL.md`)
- [x] **#25**: Proposal defence completion (Passed July 9, 2026)
- [x] **#27**: Gateway NPU & Arc iGPU capability assessment (Benchmarked via OpenVINO)
- [x] **#32**: TP4056 charge/protection circuit locked for unprotected LiPo
- [x] **#38**: Charging panel safety interface locked (dual single-purpose USB-C, off-body only)
- [x] **#39**: M2.5 fastener specification finalized & local Daraz kit selected
- [ ] **#16 / #18**: Physical delivery & bench verification of departmental hardware order
- [ ] **#17**: Finalize 3D CAD dimensions & TPU slicer profile for dorsal wrist bracer
- [ ] **#26**: Narrow Novelty Claims 1 & 3 in final thesis draft against related prior art

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
│   ├── train_cnn.py              # Primary 1D CNN training pipeline (93.58% AUC-ROC)
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
│   ├── CHANGELOG.md              # Project change log (v53)
│   ├── DATA_COLLECTION_PROTOCOL.md # Nepal cohort human-subject trial protocol
│   ├── WIRE_FORMAT_v1.md         # Locked BLE event protocol schema
│   ├── SPARK_Component_Order_Form.xlsx # Canonical hardware BOM procurement spreadsheet
│   ├── SPARK_Presentation_Mid_Term_Defense_v6.pptx # Mid-term defense slide deck
│   └── SPARK_Proposal/           # Complete LaTeX thesis proposal source
│       └── ThesisReports/        # LaTeX report (thesis_report.tex, compiling to PDF)
│
└── dev_logs/                     # Engineering Journals & Design Assets
    ├── SPARK_TRACKER.md          # Single source of truth master project tracker (v53)
    └── design-assets/            # 3D CAD references, renders, and walkthroughs
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

# Pull only (with autostash) without committing
.\sync.ps1 -PullOnly
```

---

## 📜 License

This project is licensed under the MIT License — see the [`LICENSE`](LICENSE) file for details.
