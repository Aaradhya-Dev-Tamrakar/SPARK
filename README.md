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

- **Firmware & Layer 1 Gate**: `[████████████████████] 100%` (21/21 Unit Tests Passed, ESP-IDF Scaffold)
- **Model Training (SisFall & ML)**: `[████████████████████] 100%` (Raw Ingestion, RF/XGBoost & CNN Pipelines)
- **Wire Format & Schema**: `[████████████████████] 100%` (Locked in `docs/WIRE_FORMAT_v1.md`)
- **BOM & Procurement**: `[████████████████████] 100%` (Locked in `docs/SPARK_Component_Order_Form.xlsx`)
- **Proposal & Academic Reports**: `[████████████████████] 100%` (Proposal Defended, LaTeX Thesis Compiling)
- **Gateway & SHAP Engine**: `[████████████░░░░░░░░] 60%` (Receivers & PDF Templates Ready; SHAP Hooked to ML)
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
                               │  Quantized 1D/2D CNN on TFLite Micro                   │
                               └───────────────────────────┬────────────────────────────┘
                                                           │ BLE Notification (WIRE_FORMAT_v1)
                                                           ▼
                                  LOCAL GATEWAY (Laptop / Local Server)
   ┌────────────────────────────────────────────────────────────────────────────────────┐
   │  [Gateway Receiver] ──> [JSON Local Store] ──> [SHAP Attribution Engine]           │
   │                                                         │                          │
   │                                                         ▼                          │
   │                                           [ReportLab Clinical PDF Report]          │
   └───────────────────────────────────────────────────────┬────────────────────────────┘
                                                           │ Local Network (HTTP/WS)
                                                           ▼
                                  DISPLAY CLIENT (Smartphone / Web UI)
   ┌────────────────────────────────────────────────────────────────────────────────────┐
   │  Read-Only Responsive Dashboard (Alerts, Event Log & PDF Report Viewer)            │
   └────────────────────────────────────────────────────────────────────────────────────┘
```

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
│   └── test/                     # Host-executable unit tests (21/21 passed)
│
├── training/                     # Machine Learning & Data Pipelines
│   ├── data_prep/                # Dataset ingestion scripts (prepare_sisfall.py)
│   ├── notebooks/                # ML exploration & classical baselines (RF / XGBoost)
│   ├── train_cnn.py              # Primary CNN architecture & TFLite quantizer
│   └── requirements.txt          # ML training Python dependencies
│
├── gateway/                      # Local Gateway & Explainability Pipeline
│   ├── main.py                   # Gateway service entry point
│   ├── receiver/                 # BLE and Serial receiver handlers
│   ├── shap_pipeline/            # SHAP feature attribution engine
│   ├── report/                   # ReportLab clinical PDF generator
│   └── storage/                  # Local JSON event record storage
│
├── data/                         # Datasets & Trial Recordings (Gitignored)
│   ├── README.md                 # SisFall setup & Nepal trial dataset instructions
│   └── .gitkeep
│
├── docs/                         # Specifications & Academic Reports
│   ├── CHANGELOG.md              # Project change log
│   ├── WIRE_FORMAT_v1.md         # Locked BLE event protocol schema
│   ├── SPARK_Component_Order_Form.xlsx # Canonical hardware BOM procurement spreadsheet
│   ├── SPARK_Presentation_Mid_Term_Defense_v6.pptx # Mid-term defense slide deck
│   └── SPARK_Proposal/           # Complete LaTeX thesis proposal source
│       └── ThesisReports/        # LaTeX report (thesis_report.tex, compiling to PDF)
│
└── dev_logs/                     # Engineering Journals & Design Assets
    ├── SPARK_TRACKER.md          # Single source of truth master project tracker (v48)
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
