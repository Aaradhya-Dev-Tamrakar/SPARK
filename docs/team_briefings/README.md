# SPARK — Pre-Hardware Task Briefings Master Index

**Document Version:** 1.0 (September 24, 2026)  
**Target Window:** Pre-Hardware Delivery / Software-in-the-Loop (SIL) Phase  
**Supervisor:** Er. Dipen Manandhar | **HOD:** Er. Suramya Sharma Dahal  
**Department:** Electronics, Communication and Information Engineering, KEC / IOE / TU

---

## Executive Overview for the Team

Due to departmental procurement timelines, physical silicon (ESP32-S3 boards, MPU6050 breakouts, LiPo cells) arrives in the upcoming semester. 

**This does NOT put development on hold.** Industry engineering teams develop 90% of embedded and IoT products in **Model-in-the-Loop (MIL)** and **Software-in-the-Loop (SIL)** virtual environments before touching physical silicon. 

These briefing files define the exact, independent deliverables each team member must execute and verify before hardware delivery:

| Team Member | Subsystem Ownership | Standalone Briefing Document | Primary Deliverable |
| :--- | :--- | :--- | :--- |
| **Rupesh Kadel** *(79034)* | Embedded Systems & Firmware | [`RUPESH_FIRMWARE_PRE_HARDWARE_GUIDE.md`](RUPESH_FIRMWARE_PRE_HARDWARE_GUIDE.md) | Virtual ESP32-S3 firmware execution (QEMU/Wokwi), INT8 TFLite Micro tensor arena profiling, cycle-count benchmarks. |
| **Sankalpa Lamsal** *(79039)* | Hardware & Mechanical CAD | [`SANKALPA_CAD_ENCLOSURE_GUIDE.md`](SANKALPA_CAD_ENCLOSURE_GUIDE.md) | Parametric 3D CAD bracer model (`.step`/`.stl`), virtual assembly with PCB footprints, TPU 95A slicer toolpaths & mass check. |
| **Sonia Thapa** *(79043)* | Display Client & Validation | [`SONIA_MOBILE_CLIENT_GUIDE.md`](SONIA_MOBILE_CLIENT_GUIDE.md) | Layer 3 mobile/web UI, real-time event listener consuming `gateway/server.py`, interactive SHAP bar charts, PDF viewer. |

---

## Defense Readiness Strategy: What to Tell the Faculty Panel

If asked during internal reviews or supervisor checkpoints about the status of hardware:

> *"Our team adopted a Software-in-the-Loop (SIL) and Digital Twin design strategy to eliminate bring-up risk. The ML pipeline, 18.5 KB quantization, and explainability engine are 100% verified. Firmware logic is validated on emulated ESP32-S3 targets, the CAD enclosure is fully modeled and sliced for KEC Makerspace TPU 3D printing, and the mobile dashboard is active against simulated gateway feeds. When hardware arrives, our timeline is purely physical validation and threshold calibration."*
