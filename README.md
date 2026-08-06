# SPARK — Signal Pattern Analysis & Real-time Kinetics

Two-layer gated wearable fall detection system, targeting healthy independent elderly people in a Nepal context. Major project, 8th semester, Kathmandu Engineering College (KEC), IOE, Tribhuvan University.

## Team

| Role | Name |
|---|---|
| Lead | Aaradhya Dev Tamrakar |
| Firmware / Layer 1 | Rupesh Kadel |
| Enclosure / Hardware | Sankalpa Lamsal |
| Dashboard / Gateway | Sonia Thapa |
| Supervisor | Er. Dipen Manandhar |

## Status

Proposal submitted (v35, signed hardcopy) and defended July 9, 2026 — panel optimistic. Dataset collection protocol under discussion with HOD, not yet finalized (tracker Action #23). RPi 4B dropped from the design; gateway runs on a laptop (Acer Swift Go 16), no Mosquitto/FastAPI/PostgreSQL stack. Firmware and gateway skeletons committed with wire format locked (`docs/WIRE_FORMAT_v1.md`) — Layer 1 threshold gate, TFLite Micro call interface, and JSON event encode/parse implemented and host-tested; BLE/serial peripheral wiring still stubbed. First training code (`prepare_sisfall.py`) and two SisFall notebooks also committed. Enclosure: wrist-worn, 3D-printed PLA, electronics top-of-wrist/dorsal (Action #34); battery, BLE modality, and bring-up hardware locked in BOM. See `dev_logs/SPARK_TRACKER.md` (current: v29) for full status.

## Structure

- `firmware/` — ESP32-S3 wearable node: Layer 1 hardware-gated thresholding, TFLite Micro inference stub, MPU6050 driver, JSON event encoding per `docs/WIRE_FORMAT_v1.md`
- `training/` — model training, quantization, TFLite conversion (`prepare_sisfall.py`, SisFall notebooks, `train_cnn.py`)
- `gateway/` — laptop-side BLE/serial receiver, wire-format parsing, SHAP attribution stub, clinical PDF report template, local JSON storage
- `data/` — dataset (not committed — see `.gitignore`)
- `docs/` — proposal, presentation, `WIRE_FORMAT_v1.md` (locked firmware↔gateway schema)
- `dev_logs/` — `SPARK_TRACKER.md`, the project's single source of truth for status/decisions/actions

## Demo target

March 2027, n=2 nodes.
