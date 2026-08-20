# CHANGELOG

All notable changes and repository sync events for the **SPARK** project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- Standard repository tooling and config: `pyproject.toml` (PEP 517/621), `.pre-commit-config.yaml` (Ruff & formatting hooks).
- Comprehensive AI guidelines: `AGENT.md`, `CLAUDE.md`, `ANTIGRAVITY.md`.
- Contributor templates: `.github/pull_request_template.md`.
- Data architecture guide: `data/README.md`.
- Licensing: `LICENSE` (MIT).

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
