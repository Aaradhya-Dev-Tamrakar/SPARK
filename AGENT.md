# AGENT.md — Developer & AI Agent Guidelines

This repository contains **SPARK** (*Signal Pattern Analysis & Real-time Kinetics*), a two-layer gated wearable fall detection and clinical explainability system. All developers and AI coding agents operating on this codebase must adhere to the rules, architecture constraints, and conventions detailed below.

---

## 1. Non-Negotiable Project Architecture & Constraints

1. **Two-Layer Gated Fall Detection Pipeline**:
   - **Layer 1 (Pre-Impact Gate on MCU)**: Fast, host-testable threshold filter ($|a| > 2.5g$, $\Delta t < 300\text{ ms}$) on ESP32-S3 to filter mundane Activities of Daily Living (ADL) without waking heavy ML compute.
   - **Layer 2 (Post-Impact Classifier on MCU)**: Quantized CNN model running under **TFLite Micro** on ESP32-S3 evaluating the 200 Hz 3-second motion window ($200 \times 6$).
   - **Gateway (Laptop Compute)**: BLE receiver, local JSON record storage, per-event **SHAP explainability** computation, and automated clinical PDF report generation (`reportlab`).
   - **Mobile Phone Client**: **Display-only** local-network reader. **DO NOT** implement on-phone BLE drivers or mobile-native SHAP/PDF compilation.

2. **Wire Format Protocol Invariance (`docs/WIRE_FORMAT_v1.md`)**:
   - Firmware-to-gateway event schema is strictly governed by `docs/WIRE_FORMAT_v1.md`.
   - JSON payload includes `timestamp_ms`, `event_id`, `layer1_triggered`, `confidence` ($P(\text{fall}) = \text{class\_probs}[1]$), and `peak_features` ($a_{\max}, \omega_{\max}$).
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
