# SPARK — Signal Pattern Analysis & Real-time Kinetics

Two-layer gated wearable fall detection system, targeting healthy independent elderly people in a Nepal context. Major project, 8th semester, Kathmandu Engineering College (KEC), IOE, Tribhuvan University.

## Team

| Role | Name |
| --- | --- |
| Lead | Aaradhya Dev Tamrakar |
| Firmware / Layer 1 | Rupesh Kadel |
| Enclosure / Hardware | Sankalpa Lamsal |
| Dashboard / Gateway | Sonia Thapa |
| Supervisor | Er. Dipen Manandhar |

## Status

Proposal submitted (v35, signed hardcopy) and defended July 9, 2026 — panel optimistic. Dataset collection protocol under discussion with HOD, not yet finalized (tracker Action #23). RPi 4B dropped from the design; gateway runs on a laptop (Acer Swift Go 16), no Mosquitto/FastAPI/PostgreSQL stack — phone is a display-only client (no BLE, no local compute). Firmware and gateway skeletons committed with wire format locked (`docs/WIRE_FORMAT_v1.md`) — Layer 1 threshold gate, TFLite Micro call interface, and JSON event encode/parse implemented and host-tested; BLE/serial peripheral wiring still stubbed. First training code (`prepare_sisfall.py`) and two SisFall notebooks also committed. Enclosure: wrist-worn, 3D-printed **TPU** (switched from PLA — real KEC Makerspace stock), electronics top-of-wrist/dorsal, Velcro closure, compression arm sleeve base layer (Action #34); battery sourced (Giga Nepal, 1100mAh LiPo, NPR 550), MPU6050/USB-C/Velcro strap sourced and priced. BOM total ~NPR 9,737 — `docs/SPARK_Component_Order_Form.xlsx` is the sole canonical procurement spreadsheet. See `dev_logs/SPARK_TRACKER.md` (current: v37) for full status.

## Structure

- `firmware/` — ESP32-S3 wearable node: Layer 1 hardware-gated thresholding, TFLite Micro inference stub, MPU6050 driver, JSON event encoding per `docs/WIRE_FORMAT_v1.md`
- `training/` — model training, quantization, TFLite conversion (`prepare_sisfall.py`, SisFall notebooks, `train_cnn.py`)
- `gateway/` — laptop-side BLE/serial receiver, wire-format parsing, SHAP attribution stub, clinical PDF report template, local JSON storage
- `data/` — dataset (not committed — see `.gitignore`)
- `docs/` — proposal (`SPARK_Proposal/`, VS Code/LaTeX Workshop compile-ready via `ThesisReports/.latexmkrc`), presentation, `SPARK_Component_Order_Form.xlsx` (canonical procurement doc), `WIRE_FORMAT_v1.md` (locked firmware↔gateway schema)
- `dev_logs/` — `SPARK_TRACKER.md`, the project's single source of truth for status/decisions/actions

## Demo target

March 2027, n=2 nodes.
