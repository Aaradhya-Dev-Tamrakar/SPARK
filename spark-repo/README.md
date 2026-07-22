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

Proposal submitted (v35, signed hardcopy) and defended July 9, 2026 — panel optimistic. Dataset collection protocol under discussion with HOD, not yet finalized. No firmware or training code committed yet.

**Latest report (v37 — working reconciliation, not submitted):** team submitted by editing v35 directly (v36 was the intended target but got bypassed); v37 is v35 with v36's Gantt-chart fix layered back in.
- [Edit (Overleaf)](https://www.overleaf.com/6661578839jrqvyjyfprhm#ffcaee)
- [View (Overleaf)](https://www.overleaf.com/read/zdzmvzfmmnrn#1c6617)

## Structure

- `firmware/` — ESP32-S3 wearable node (TFLite Micro, Layer 1 threshold + Layer 2 CNN)
- `training/` — model training, quantization, TFLite conversion
- `gateway/` — Mosquitto → FastAPI → PostgreSQL ingest stack, SHAP attribution
- `data/` — dataset (not committed — see `.gitignore`)

## Demo target

March 2027, n=2 nodes.
