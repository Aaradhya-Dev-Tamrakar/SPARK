# SPARK — Post-Boards Resumption & Master Execution Plan

**Document Status:** Locked Milestone & Context Preservation Archive  
**Freeze Date:** August 22, 2026  
**Target Resumption:** Post-Board Examination Period (8th Semester B.E. Final Phase)  
**Project:** SPARK (*Signal Pattern Analysis & Real-time Kinetics*)  
**Institution:** Kathmandu Engineering College (KEC), Tribhuvan University  

---

## 1. Executive Snapshot (State as of 2026-08-22)

The SPARK project is paused in a healthy, fully verified, and mathematically defensible state across all three tiers:

```
[ ESP32-S3 Wearable Node ]  ──(BLE GATT / UART)──>  [ Local Companion Gateway ]  ──(REST/CORS)──>  [ Web/Mobile UI ]
  • MPU6050 at 200 Hz                                • Intel Core Ultra 7 155H                      • Sonia Thapa (L3)
  • Layer 1: Accel/Gyro Gate                         • CnnShapExplainer (Input × ∇)                  • Dark-mode Dashboard
  • Layer 2: 18.5 KB INT8 CNN                        • ReportLab 1-Page Clinical PDF                 • Event / Report API
  • Status: C-Header Embedded                        • Status: 48/48 Tests Passing                   • Status: Unblocked
```

### Key Metrics Reached:
* **ML Model**: 1D CNN trained on 38,426 SisFall windows under subject-grouped split ($87.81\%$ sensitivity, $0.9185$ AUC-ROC).
* **Quantization**: INT8 Post-Training Quantization compressed model to **$18.5\text{ KB}$** (C-header byte array in [`firmware/main/models/spark_cnn_int8.h`](file:///D:/Aaradhya-Dev-Tamrakar/SPARK/firmware/main/models/spark_cnn_int8.h)).
* **Gateway Explainability**: Local companion-device $\text{Input} \times \nabla_{\text{Input}}$ gradient attribution generating one-page clinical PDF incident reports with 4 distinct simulated fall archetypes.
* **Hardware Benchmarking**: Intel Core Ultra 7 155H hardware engine execution via OpenVINO verified ($0.131\text{ ms}$ CPU, $0.200\text{ ms}$ GPU, $0.383\text{ ms}$ NPU).
* **Repository Health**: 48 unit tests passing cleanly (`uv run pytest`), Ruff lint and formatting clean.
* **Research Synthesis**: 19 deep-research tracks merged in [`docs/SPARK_research_board_merged.md`](file:///D:/Aaradhya-Dev-Tamrakar/SPARK/docs/SPARK_research_board_merged.md).

---

## 2. Deep-Research Synthesis Summary (19 Tracks)

The 19 research tracks conducted in August 2026 established the following locked parameters and academic boundaries:

| Track Domain | Locked Parameter / Finding | Academic & Engineering Impact |
|---|---|---|
| **Novelty Claim 1 (MCU Gate)** | Software threshold gate + INT8 CNN confirmation on a single commodity MCU ($<\$5$). | Defense-proof wording locked. Refutes server offload (*Xu 2021*), always-on non-gated CNNs (*TinyCNN 2023, MicroFallNet 2025*), and high-cost FPGAs (*Vigil 2024*). |
| **Novelty Claim 3 (Gateway XAI)** | Real-time gradient attribution ($\text{Input} \times \nabla$) on local companion gateway. | Contrasts against general HAR literature which only ran KernelSHAP offline on generic non-fall data. |
| **Model Sensitivity ($\ge 90\%$)** | Use **Focal Loss** ($\gamma=2.0, \alpha=0.75$) + temporal jitter over architecture changes. | Avoids heavier models (TCN / Squeeze-and-Excitation) that add $2\times\text{--}75\times$ flash overhead for minimal gain. |
| **Nepal Cohort Strategy** | **Partial-Freeze Fine-Tuning** (freeze Conv1D feature extractors, train dense head). | Prevents overfitting on small local datasets ($N=12\text{--}20$). |
| **Clinical Protocol** | Full 34-activity matrix (15 falls across 8 mechanisms, 19 ADLs) on crash mats. | Verified clean mapping against SisFall taxonomy; adapts waist frame to dorsal wrist. |
| **Elderly Kinematic Gap** | Young impact peaks ($8\text{--}12g$) vs. elderly peaks ($3.5\text{--}6g$). | Integrated Klenk lean-and-release protocol and elderly baseline ADL verification. |
| **Cohort Sample Size** | **$N = 12\text{--}20$ subjects** (minimum floor of 10). | Grounded in clinical pilot conventions (*Julious 2005*) for department ethics approval. |
| **TPU 95A Enclosure DFM** | $3\text{--}4\text{ mm}$ solid wall thickness + **M2/M2.5 brass heat-set inserts**. | Prevents thread-stripping inherent in self-tapping screws driven into flexible TPU. |
| **Power Consumption** | Active: $90\text{--}130\text{ mA}$ ($8\text{--}11\text{ hr}$). Event-gated BLE: $35\text{--}60\text{ mA}$ ($16\text{--}28\text{ hr}$). | Tightened R-05 power model; event notification mode doubles battery longevity. |
| **Thesis Ch. 6 Extensions** | Late vision-IMU fusion, aquatic bounds (cadence $0.4\text{--}1.6\text{ Hz}$, IDR $>2.5\text{ Hz}$, timeout $>15\text{ s}$), encrypted cold-storage. | Rigorous future-work boundaries for defense. |
| **Target Publications** | Target **ICACT 2027 Kathmandu** (IEEE Xplore) and **IEEE Healthcom**. | Identified real post-thesis publication targets. |

---

## 3. Post-Boards Step-by-Step Execution Roadmap

When resuming after board exams, follow this ordered 5-phase execution plan:

```mermaid
graph TD
    subgraph Phase 1: Institutional & Protocol Lockdown "Week 1 (Days 1-3)"
        P1[Complete DATA_COLLECTION_PROTOCOL.md] --> P2[Supervisor & Ethics Approval at KEC]
        P2 --> P3[Update LaTeX Thesis Chapters 1-6]
    end

    subgraph Phase 2: Hardware Logger Rig "Week 1 (Days 4-7)"
        H1[Assemble ESP32-S3 + MPU6050 Wrist Strap] --> H2[Flash SPARK_MODE_DATA_LOGGER Firmware]
        H2 --> H3[Verify 200Hz BLE/Serial CSV Stream to Gateway]
    end

    subgraph Phase 3: Cohort Data Collection "Week 2"
        C1[Execute 34-Activity Protocol at KEC Gym] --> C2[Collect N=12 to 20 Nepali Volunteers]
        C2 --> C3[Extract & Label Raw Dorsal Wrist CSVs]
    end

    subgraph Phase 4: Transfer Learning & Quantization "Week 3"
        M1[Partial-Freeze Fine-Tuning on Nepal CSVs] --> M2[Push Sensitivity to >= 90% via Focal Loss]
        M2 --> M3[Re-Quantize INT8 & Export spark_cnn_int8.h]
        M3 --> M4[Flash Autonomous Firmware Layer 1 + Layer 2]
    end

    subgraph Phase 5: End-to-End Live Validation & Defense "Week 4"
        D1[Conduct Live Wearable Fall Trials on Crash Mat] --> D2[Verify Real-Time Gateway Incident PDFs]
        D2 --> D3[Final Thesis Report & Slides Delivery]
    end

    Phase 1 --> Phase 2 --> Phase 3 --> Phase 4 --> Phase 5
```

---

### Phase 1: Academic & Protocol Lockdown (Week 1, Days 1–3)
1. **Complete Protocol Document ([`docs/DATA_COLLECTION_PROTOCOL.md`](file:///D:/Aaradhya-Dev-Tamrakar/SPARK/docs/DATA_COLLECTION_PROTOCOL.md))**:
   * Add the remaining 12 unmapped rows from Track 7 (**F09–F15** falls & **D15–D19** ADLs).
   * Include the sample size rationale ($N=12\text{--}20$) and Klenk lean-and-release protocol.
   * Submit to Supervisor (Er. Dipen Manandhar) / HOD for ethics sign-off.
2. **Update LaTeX Thesis Proposal ([`docs/SPARK_Proposal/Chapters/`](file:///D:/Aaradhya-Dev-Tamrakar/SPARK/docs/SPARK_Proposal/Chapters/))**:
   * **Chapters 1 & 2**: Integrate narrowed Claim 1 text and the 130-paper literature matrix.
   * **Chapters 3 & 5**: Integrate narrowed Claim 3 ($\text{Input} \times \nabla$) and the OpenVINO NPU/iGPU gateway benchmark numbers.
   * **Chapter 6**: Write structured sections for Multi-Modal Vision Fusion, Aquatic Safety Roadmap, and Client-Encrypted Cold Storage.
3. **BOM Reconciliation**:
   * Confirm dropping or adjusting the NPR 1,000 separate Velcro line in [`SPARK_BOM_Procurement.xlsx`](file:///D:/Aaradhya-Dev-Tamrakar/SPARK/docs/SPARK_BOM_Procurement.xlsx).

---

### Phase 2: Hardware Prototyping & Logger Setup (Week 1, Days 4–7)
1. **Physical Prototype Assembly**:
   * Mount ESP32-S3 and MPU6050 on the dorsal wrist reference using an elastic/Velcro strap.
   * Wire I2C lines (`SDA: GPIO 4`, `SCL: GPIO 5`, `INT: GPIO 6`).
2. **Firmware Logger Mode**:
   * Enable continuous $200\text{ Hz}$ 6-axis streaming mode over BLE / UART.
   * Run a test recording session with [`gateway/receiver/receiver.py`](file:///D:/Aaradhya-Dev-Tamrakar/SPARK/gateway/receiver/receiver.py) to save raw `.csv` output files matching the SisFall column format (`Ax, Ay, Az, Gx, Gy, Gz`).

---

### Phase 3: Nepali Cohort Data Collection at KEC (Week 2)
1. **Setup**:
   * KEC Robotics / Electronics Lab with high-density gymnastic crash mats ($20\text{ cm}$ thickness).
2. **Execution**:
   * Run $N=12\text{--}20$ student/faculty volunteers through the 34-activity protocol (3 trials per fall mechanism, 3–5 trials per ADL).
   * Save structured files under `data/nepal_cohort/` (e.g., `F01_SA01_R01.csv`).

---

### Phase 4: Transfer Learning & Model Quantization (Week 3)
1. **Fine-Tuning**:
   * Load pretrained `spark_cnn.keras` base weights.
   * Freeze Conv1D feature extractors and train dense classification layers on mixed SisFall + Nepal cohort data using Focal Loss ($\gamma=2.0$).
2. **Quantization & Export**:
   * Run [`quantize_model.py`](file:///D:/Aaradhya-Dev-Tamrakar/SPARK/quantize_model.py) with representative calibration.
   * Generate updated [`firmware/main/models/spark_cnn_int8.h`](file:///D:/Aaradhya-Dev-Tamrakar/SPARK/firmware/main/models/spark_cnn_int8.h).
3. **Flash ESP32-S3 Firmware**:
   * Flash the full autonomous detection firmware (Layer 1 software threshold + Layer 2 INT8 CNN + BLE incident alerting).

---

### Phase 5: Real-Time Live Validation & Final Defense (Week 4)
1. **Live Crash-Mat Validation**:
   * Perform live test falls wearing the autonomous device.
   * Confirm Layer 1 trigger $\to$ Layer 2 INT8 inference ($<15\text{ ms}$) $\to$ BLE notification transmission $\to$ Gateway $\text{Input} \times \nabla$ attribution chart $\to$ One-page clinical PDF report.
2. **Final Defense Deliverables**:
   * Compile final thesis PDF report with LaTeX.
   * Prepare slide deck ([`docs/SPARK_Presentation_Mid_Term_Defense_v6.pptx`](file:///D:/Aaradhya-Dev-Tamrakar/SPARK/docs/SPARK_Presentation_Mid_Term_Defense_v6.pptx)) with live hardware demo.

---

## 4. Key Reference Index

* **Master Tracker**: [`dev_logs/SPARK_TRACKER.md`](file:///D:/Aaradhya-Dev-Tamrakar/SPARK/dev_logs/SPARK_TRACKER.md) (v54)
* **Master Research Board (19 Tracks)**: [`docs/SPARK_research_board_merged.md`](file:///D:/Aaradhya-Dev-Tamrakar/SPARK/docs/SPARK_research_board_merged.md)
* **Data Collection Protocol**: [`docs/DATA_COLLECTION_PROTOCOL.md`](file:///D:/Aaradhya-Dev-Tamrakar/SPARK/docs/DATA_COLLECTION_PROTOCOL.md)
* **CAD Concept Reference**: [`dev_logs/design-assets/DESIGN_IDEAS.md`](file:///D:/Aaradhya-Dev-Tamrakar/SPARK/dev_logs/design-assets/DESIGN_IDEAS.md) (DI-02 Master Composite Sheet)
* **GATT Protocol Specification**: [`docs/WIRE_FORMAT_v1.md`](file:///D:/Aaradhya-Dev-Tamrakar/SPARK/docs/WIRE_FORMAT_v1.md)
* **Thesis LaTeX Sources**: [`docs/SPARK_Proposal/`](file:///D:/Aaradhya-Dev-Tamrakar/SPARK/docs/SPARK_Proposal/)
* **Test Suite**: Run `uv run pytest` (48 tests passing)

---
*Created on 2026-08-22 for Aaradhya Dev Tamrakar & SPARK Engineering Team.*
