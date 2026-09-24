# CLAUDE.md — Assistant Guidelines for SPARK

## Project Overview
**SPARK** (*Signal Pattern Analysis & Real-time Kinetics*) is a two-layer gated edge-AI fall detection and kinetic distress signaling platform. Validated empirically on human gait for elderly monitoring in Nepal (Layer 1 IMU threshold on ESP32-S3 $\rightarrow$ Layer 2 TFLite INT8 CNN on ESP32-S3) with laptop-based SHAP explainability and incident reports, with modular extensibility as an out-of-band safety module for bipedal and humanoid robotics training.

## Key Developer Commands

### Python Environment & Tests
```bash
# Run unit tests across all modules
uv run pytest

# Lint and auto-fix with Ruff
uv run ruff check --fix

# Format code with Ruff
uv run ruff format
```

### Firmware Build & Host Tests (ESP-IDF)
```bash
# Run host-based unit tests
cd firmware/test
# Build and run native test runner

# ESP-IDF target build & flash (ESP32-S3)
cd firmware
idf.py set-target esp32s3
idf.py build
idf.py -p COM_PORT flash monitor
```

### LaTeX Thesis / Proposal Build
```bash
cd docs/SPARK_Proposal/ThesisReports
# Build report using latexmk or pdflatex
latexmk -pdf thesis_report.tex
```

### Local Git Synchronization
```bash
# Auto-staged conventional commit & rebase push
.\sync.ps1
.\sync.ps1 -m "feat(training): message"
.\sync.ps1 -Build           # compile thesis_report.tex PDF first, then sync
.\sync.ps1 -PullOnly
```

## Architecture & Code Conventions
- **Module boundaries**: `firmware/` (C/C++ ESP-IDF), `training/` (Python/TensorFlow/scikit-learn), `gateway/` (Python/ReportLab/SHAP).
- **Communication Protocol**: Always follow [`docs/WIRE_FORMAT_v1.md`](docs/WIRE_FORMAT_v1.md).
- **Single Source of Truth**: Hardware specs and procurement live in `docs/SPARK_Component_Order_Form.xlsx`. Milestones and project status live in `dev_logs/SPARK_TRACKER.md`.
