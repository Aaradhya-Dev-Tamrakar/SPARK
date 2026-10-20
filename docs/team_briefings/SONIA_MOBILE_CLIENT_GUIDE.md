# Gateway & Mobile UI Engineer Task Briefing

**Assignee:** Sonia Thapa (Roll 79043 / BEI)  
**Subsystem:** Layer 3 Mobile Display Client, Gateway Telemetry Consumption & Clinical UI  
**Primary Directory:** [`gateway/`](file:///f:/Aaradhya-Dev-Tamrakar/SPARK/gateway/)  
**Last Updated:** October 20, 2026  
**Goal:** Deliver a functional caregiver mobile/web display client that receives live fall alerts, visualizes SHAP explanations, and renders clinical incident PDFs, while managing clinical trial ethics documentation and cohort logistics.

> [!NOTE]
> This guide was originally created during the Pre-Hardware / Software-in-the-Loop (SIL) phase (September 24, 2026).
> **§1–§3** cover simulation testing using the built-in gateway replay mode.
> **§4–§6** cover post-hardware live BLE streaming, cohort consent documentation, trial execution, and live defense demonstration added October 20, 2026.

---

## 1. Why You Don't Need Physical Silicon Yet (SIL Phase)
The backend gateway server is **already fully built and functional** in the repository ([`gateway/server.py`](file:///f:/Aaradhya-Dev-Tamrakar/SPARK/gateway/server.py)). It includes a built-in event replay simulator (`ReplayReceiver`) that generates realistic fall events (Forward Trip, Lateral Slip, Syncope, Rotational Twist) on command. 

You can build and test the entire mobile/tablet user experience on your phone over Wi-Fi right now.

---

## 2. Sonia's Action Checklist (Simulation Phase)

### Task 1: Run the Gateway Server in Replay Mode
1. Open terminal in the project root:
   ```bash
   # Run the gateway simulation server
   .venv\Scripts\python.exe gateway/server.py --port 8000
   ```
2. Open your browser to `http://localhost:8000` to inspect the embedded dark-mode dashboard.
3. Test the REST API endpoints using your browser or Postman/curl:
   * `GET /api/health` $\to$ Returns receiver status and uptime.
   * `GET /api/events` $\to$ Returns list of recent fall incidents.
   * `GET /api/events/<event_id>` $\to$ Returns full event details with SHAP feature attributions.
   * `GET /api/reports/<event_id>` $\to$ Downloads the compiled one-page clinical PDF report.

---

### Task 2: Build the Layer 3 Mobile App (Flutter, React Native, or PWA)
* **Design Philosophy:** Clean, accessible, high-contrast UI tailored for hospital nursing staff and caregivers.
* **Core Screens & Components to Build:**
  1. **Live Alert Feed**:
     * Real-time polling or WebSocket listener hitting `GET /api/events`.
     * Prominent high-priority alert cards when a new fall is confirmed:
       * **Red Banner**: High Confidence ($P(\text{fall}) \ge 0.85$).
       * **Amber Banner**: Moderate Confidence ($0.75 \le P(\text{fall}) < 0.85$).
       * **Blue Banner**: Routine Check ($P(\text{fall}) < 0.75$).
       * Displays Timestamp, Device ID, and primary kinetic contributor (e.g., *"Dominant Pitch Rate Divergence"*).
  2. **Kinematic Explanation Screen (SHAP Attribution)**:
     * When tapping an incident card, render an interactive horizontal bar chart displaying relative SHAP feature contributions across all 6 axes:
       * Acceleration: $a_x$ (Surge), $a_y$ (Sway), $a_z$ (Heave)
       * Gyroscope: $\omega_x$ (Roll rate), $\omega_y$ (Pitch rate), $\omega_z$ (Yaw rate)
     * Raw `peak_features` table with physical units ($g$, $^\circ/\text{s}$).
  3. **In-App Clinical PDF Viewer**:
     * Embed a native PDF viewer component displaying the formal incident report fetched directly from `/api/reports/<event_id>`.
     * Include a one-tap "Share / Print" button for medical staff handoff.

---

### Task 3: Local Network Discovery & Phone Testing
1. Connect your laptop and your smartphone to the same Wi-Fi network (or laptop mobile hotspot).
2. Find your laptop's local IPv4 address (`ipconfig` on Windows, e.g., `192.168.1.75`).
3. Run the mobile app on your phone, pointing the API base URL to `http://192.168.1.75:8000`.
4. Trigger a simulated fall on the laptop and verify the alert pops up on your phone screen in real time.

---

### Task 4: Participant Logistics & Data Collection Forms
* **Reference Document:** [`docs/DATA_COLLECTION_PROTOCOL.md`](file:///f:/Aaradhya-Dev-Tamrakar/SPARK/docs/DATA_COLLECTION_PROTOCOL.md)
* **Action:**
  * Prepare and format the standardized volunteer sign-off forms for the KEC cohort collection.
  * Formulate the 34-activity tracking checklist (15 falls F01–F15, 19 ADLs D01–D19) with participant demographic fields (Subject ID, Age, Height, Weight, Fall Trial Repeats) ready for clipboard tracking during crash-mat sessions.

---

## 3. SIL-Phase Defense Questions (Pre-Hardware)

> These Q&As cover the display-client architectural choices. See **§6** for the full updated defense questions including clinical safety and explainability triage.

---

## 4. Post-Hardware Live Integration & Clinical Execution (Phases 2–5)

> **Context:** Physical ESP32-S3 hardware streaming live over BLE to the gateway laptop, and KEC student volunteer trials underway.

### Task 5: Connect Mobile App to Live Gateway Stream
* **Objective:** Switch the caregiver display client from replay mode to the live hardware gateway stream.
* **Execution:**
  1. Have Rupesh trigger physical fall events on the wearable node.
  2. Gateway laptop running `gateway/main.py --mode ble` receives live BLE GATT events and automatically pushes them to the local event store.
  3. Verify your mobile client dynamically updates its alert feed without needing a page refresh.
* **Acceptance Criteria:** Live physical fall on crash mat appears on the smartphone screen within $\le 1.5\text{ seconds}$ with correct SHAP attribution.

---

### Task 6: Scaffold Clinical Cohort Consent & Clipboard Forms
* **Objective:** Create the institutional trial documentation in `docs/cohort_forms/`.
* **Deliverables to Scaffold:**
  1. `docs/cohort_forms/VOLUNTEER_CONSENT_FORM.md`:
     - Formal DOECIE / KEC institutional header.
     - Study purpose, non-invasive wrist device description, and participant rights.
     - Strict inclusion criteria (healthy adults aged 18–30, no active musculoskeletal injuries or cardiovascular issues).
     - Gymnastic crash mat safety briefing acknowledgment and voluntary signature block.
  2. `docs/cohort_forms/34_ACTIVITY_CLIPBOARD_LOG.md`:
     - Tabular grid covering all 15 Fall Trials (`F01`–`F15`) and 19 ADL Trials (`D01`–`D19`).
     - Columns: Subject ID (`SA01`–`SA20`), Activity Code, Trial # (1–3), CSV Filename, Completion Check, and Clinician Notes.
* **Acceptance Criteria:** Forms reviewed and cleared by Supervisor (Er. Dipen Manandhar) prior to trial sessions.

---

### Task 7: KEC Cohort Collection Execution & Dataset Verification
* **Objective:** Lead participant intake, consent recording, and trial logging during the crash-mat collection sessions.
* **Execution:**
  1. Supervise volunteer warm-ups and fit the wearable device on the dorsal wrist.
  2. Track each trial repetition on the physical clipboard.
  3. After sessions, run verification on recorded CSV files:
     ```bash
     .venv\Scripts\python.exe tools/verify_cohort_dataset.py --data-dir data/nepal_cohort
     ```
* **Acceptance Criteria:** Verification script reports 100% completion grid with zero missing files or corrupted headers across $N=12\text{--}20$ subjects.

---

### Task 8: Final Presentation Live Demo Integration
* **Objective:** Demonstrate end-to-end alerting on a live tablet/smartphone during the final faculty defense.
* **Demo Sequence:**
  1. Wearable node worn on team member's wrist.
  2. Member falls onto high-density crash mat in front of faculty panel.
  3. Smartphone resting on supervisor table triggers audible/vibration High Priority alert within 2 seconds.
  4. Panel views 6-axis SHAP attribution bar chart and opens the one-page ReportLab clinical PDF.
* **Acceptance Criteria:** Zero demo failure during live multi-device demonstration.

---

## 5. Defense Questions Sonia Must Be Prepared to Answer (Updated)

**Q1: "Why is the mobile phone a display-only client rather than running BLE and SHAP directly on the phone?"**  
* **Answer:** *"Running continuous BLE scanning and heavy mathematical explainability libraries (NumPy, SciPy, SHAP) on a mobile phone rapidly drains phone battery and introduces operating system background-kill risks (Android Doze / iOS background limits). Offloading reception and explainability to a local household or nursing station gateway guarantees 24/7 reliability, while the phone functions as a zero-overhead notification viewer."*

**Q2: "What happens if the internet goes down? Can the caregiver still receive alerts?"**  
* **Answer:** *"Yes. SPARK has zero cloud dependencies. The gateway server and mobile client operate entirely over the local residential or clinic Wi-Fi intranet. Alerts and PDF downloads function seamlessly even during total ISP or cellular outages."*

**Q3: "How does the mobile UI convey the classifier's confidence to non-technical caregivers?"**  
* **Answer:** *"Instead of presenting raw floating-point probabilities, the mobile client maps confidence scores into standardized clinical priority badges: High Priority (>85%), Moderate Priority (75–85%), and Routine Check (<75%), alongside a plain-language summary of the primary kinetic contributor."*

**Q4: "How does the system ensure patient data privacy and ethical compliance?"**  
* **Answer:** *"All data remains on the local gateway storage; no telemetry or medical records are ever offloaded to public cloud servers. For our KEC trial cohort, all participant records are completely anonymized using Subject IDs (SA01–SA20), and written informed consent is secured under institutional guidelines before any data acquisition."*

**Q5: "What is the clinical value of showing SHAP feature attributions to a caregiver or doctor?"**  
* **Answer:** *"Standard fall detectors act as black boxes, simply reporting 'fall detected'. SPARK's 6-axis SHAP attribution reveals the exact biomechanical mechanism: distinguishing between a syncope collapse (dominated by vertical impact acceleration $a_z$) versus a dynamic forward slip (dominated by high pitch angular velocity $\omega_y$). This enables emergency triage to prepare the appropriate clinical intervention before reaching the patient."*
