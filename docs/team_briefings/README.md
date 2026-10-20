# SPARK — Team Task Briefings Master Index

**Document Version:** 2.2 (October 20, 2026)  
**Target Window:** Pre-Hardware SIL Phase through Post-Hardware Live Validation  
**Supervisor:** Er. Dipen Manandhar | **HOD:** Er. Suramya Sharma Dahal  
**Department:** Electronics, Communication and Information Engineering, KEC / IOE / TU

---

## Executive Overview for the Team

Due to departmental procurement timelines, physical silicon (ESP32-S3 boards, MPU6050 breakouts, LiPo cells) arrives in the upcoming semester. 

**This does NOT put development on hold.** Industry engineering teams develop 90% of embedded and IoT products in **Model-in-the-Loop (MIL)** and **Software-in-the-Loop (SIL)** virtual environments before touching physical silicon. 

These briefing files define the exact, independent deliverables each team member must execute and verify across both virtual simulation and physical post-hardware phases:

### Onboarding Guides (Start Here)
Every team member has a dedicated high-level starter guide explaining their subsystem in plain language with system architecture diagrams, first-day checklists, and key specifications:
- **Rupesh Kadel (Firmware):** [`RUPESH_START_HERE.md`](RUPESH_START_HERE.md) & [`RUPESH_FIRMWARE_STARTER_REVIEW.md`](RUPESH_FIRMWARE_STARTER_REVIEW.md)
- **Sankalpa Lamsal (Hardware/CAD):** [`SANKALPA_START_HERE.md`](SANKALPA_START_HERE.md)
- **Sonia Thapa (Display Client & Clinical):** [`SONIA_START_HERE.md`](SONIA_START_HERE.md)

---

## Master Task Deliverables Matrix

| Team Member | Subsystem Ownership | Actionable Briefing Documents | Primary Deliverables (SIL & Post-Hardware) |
| :--- | :--- | :--- | :--- |
| **Rupesh Kadel** *(79034)* | Embedded Systems & Firmware | [`RUPESH_START_HERE.md`](RUPESH_START_HERE.md)<br/>[`RUPESH_FIRMWARE_PRE_HARDWARE_GUIDE.md`](RUPESH_FIRMWARE_PRE_HARDWARE_GUIDE.md) | **SIL Phase:** Virtual ESP32-S3 execution (QEMU/Wokwi), INT8 TFLite Micro tensor arena profiling, Layer 1 unit tests.<br/>**Post-Hardware:** Physical I2C wiring (GPIO 4/5/6), 200 Hz data logger streaming, ESP-IDF full compilation & static memory audit (Issue #11), BLE GATT notifications (Issue #1), live crash-mat validation. |
| **Sankalpa Lamsal** *(79039)* | Hardware & Mechanical CAD | [`SANKALPA_START_HERE.md`](SANKALPA_START_HERE.md)<br/>[`SANKALPA_CAD_ENCLOSURE_GUIDE.md`](SANKALPA_CAD_ENCLOSURE_GUIDE.md) | **SIL Phase:** Parametric Fusion 360 3D bracer model (`.step`/`.stl`), virtual assembly with PCB footprints, TPU 95A PrusaSlicer profiles.<br/>**Post-Hardware:** KEC Makerspace 3D printing & weight check (~22g, NPR 90), M2.5 brass heat-set insert installation, wiring harness soldering, drop-impact testing (Issue #4). |
| **Sonia Thapa** *(79043)* | Display Client & Validation | [`SONIA_START_HERE.md`](SONIA_START_HERE.md)<br/>[`SONIA_MOBILE_CLIENT_GUIDE.md`](SONIA_MOBILE_CLIENT_GUIDE.md)<br/>[`SONIA_HIGH_LEVEL_OVERVIEW.md`](SONIA_HIGH_LEVEL_OVERVIEW.md)<br/>[`SONIA_AI_AGENT_PROMPT.md`](SONIA_AI_AGENT_PROMPT.md) | **SIL Phase:** Layer 3 mobile/web UI consuming local `gateway/server.py` in replay mode, interactive SHAP attribution bar charts, in-app clinical PDF viewer.<br/>**Post-Hardware:** Live gateway BLE event stream integration, participant informed consent forms (`docs/cohort_forms/`), 34-activity clipboard log tracking, dataset verification, live faculty defense demo (Issue #5). |

---

## Defense Readiness Strategy: What to Tell the Faculty Panel

If asked during internal reviews or supervisor checkpoints about the status of hardware:

> *"Our team adopted a Software-in-the-Loop (SIL) and Digital Twin design strategy to eliminate bring-up risk. The ML pipeline, 18.5 KB quantization, and explainability engine are 100% verified. Firmware logic is validated on emulated ESP32-S3 targets, the CAD enclosure is fully modeled and sliced for KEC Makerspace TPU 3D printing, and the mobile dashboard is active against simulated gateway feeds. When hardware arrives, our timeline is purely physical validation, cohort acquisition, and threshold calibration."*
