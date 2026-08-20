# ANTIGRAVITY.md — Google Antigravity & Gemini Guidelines

Guidelines for Google Antigravity and Gemini-based agents working on **SPARK**:

## Rules & Behavioral Constraints
1. **Planning First**: Any non-trivial refactor or architecture change requires planning mode review and user alignment.
2. **Deterministic Tooling**: Prefer `uv` for python execution and dependency isolation.
3. **No Direct Secret/Data Leakage**: Do not commit raw accelerometer data (`data/raw/`) or credentials.
4. **Git Sync Protocol**: Stage and commit via `sync.ps1` to ensure `docs/CHANGELOG.md` and `dev_logs/SPARK_TRACKER.md` stay synchronized.

## Fast Navigation
- Project Tracker: [`dev_logs/SPARK_TRACKER.md`](dev_logs/SPARK_TRACKER.md)
- Wire Format Schema: [`docs/WIRE_FORMAT_v1.md`](docs/WIRE_FORMAT_v1.md)
- Procurement Form: [`docs/SPARK_Component_Order_Form.xlsx`](docs/SPARK_Component_Order_Form.xlsx)
- ML Training: [`training/train_cnn.py`](training/train_cnn.py)
- Firmware Layer 1: [`firmware/main/`](firmware/main/)
