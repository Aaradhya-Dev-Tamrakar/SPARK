# Gateway & Mobile UI Engineer Task Briefing — Sonia Thapa

**Assignee:** Sonia Thapa (Roll 79043 / BEI)  
**Subsystem:** Layer 3 Mobile/Web Display Client, Gateway API Consumption & Clinical Cohort Logistics  
**Primary Directory:** [`gateway/`](file:///f:/Aaradhya-Dev-Tamrakar/SPARK/gateway/) & [`docs/DATA_COLLECTION_PROTOCOL.md`](file:///f:/Aaradhya-Dev-Tamrakar/SPARK/docs/DATA_COLLECTION_PROTOCOL.md)  
**Current Phase:** Pre-Hardware Software-in-the-Loop (SIL) & Post-Hardware Live Validation  
**Last Updated:** October 20, 2026

---

## 0. TL;DR — What You Own & What Is Already Built For You

You **do not** need to wait for physical ESP32-S3 hardware. The entire Layer 2 laptop gateway backend, replay simulator, feature attribution engine, and ReportLab PDF generator are **already built and passing all unit tests**.

Your responsibilities split into **two clear deliverables**:
1. **Software Deliverable (Layer 3 Display Client):** Build a responsive Mobile/Web UI (Flutter, React Native, or PWA/Web App) that connects to [`gateway/server.py`](file:///f:/Aaradhya-Dev-Tamrakar/SPARK/gateway/server.py) over local Wi-Fi, displays real-time fall alerts, renders a 6-axis feature attribution bar chart, and opens/shares the one-page clinical PDF report.
2. **Clinical & Cohort Deliverable (Pre-Collection Readiness):** Prepare the printable **Informed Consent Form** and **34-Activity Trial Tracking Sheet** (`F01`–`F15` falls, `D01`–`D19` ADLs) from [`docs/DATA_COLLECTION_PROTOCOL.md`](file:///f:/Aaradhya-Dev-Tamrakar/SPARK/docs/DATA_COLLECTION_PROTOCOL.md) so the team is ready for ethics clearance and crash-mat recording once hardware arrives.

### Non-Negotiable Architecture Rules (from [`AGENT.md`](file:///f:/Aaradhya-Dev-Tamrakar/SPARK/AGENT.md))
* **Display-Only Client:** Your mobile/web client talks **only** to the laptop gateway over HTTP/Wi-Fi (`http://<laptop-ip>:8000`). **Do NOT** write Bluetooth (BLE) drivers, SHAP math, or PDF generation code inside the mobile app—the laptop gateway already handles all of that.
* **Truth Boundaries for Reports/Defense:** Our gateway computes peak-feature / gradient-times-input ($\text{Input} \times \nabla$) attribution over 6 IMU channels ($a_x, a_y, a_z, \omega_x, \omega_y, \omega_z$) and generates the clinical PDF locally with zero cloud dependency.

---

## 1. Step-by-Step: How to Run the Gateway Backend on Your Laptop

Because `data/` is gitignored, a fresh clone starts with an empty event folder. Run these **two commands** from the repository root (`SPARK/`) to generate 4 realistic simulated fall incidents and start the local API server:

### Step 1A: Seed 4 Simulated Fall Events & Clinical PDFs
```powershell
uv run python -m gateway.main --mode replay
```
*What this does:* Simulates 4 distinct biomechanical falls (**Forward Trip**, **Lateral Slip**, **Vertical Collapse / Syncope**, and **Rotational Twist Fall**), runs the explainability pipeline, generates 4 clinical PDF reports (`SPARK_Report_<ID>.pdf`), and saves the JSON records into `data/gateway_events/`.

### Step 1B: Start the Local REST API & Dashboard Server
```powershell
uv run python -m gateway.server --host 0.0.0.0 --port 8000
```
*What this does:* Starts the HTTP server on port `8000` with CORS enabled (`Access-Control-Allow-Origin: *`).
* Open `http://localhost:8000` in your browser to see the reference dark-mode dashboard.
* Want to inject a brand-new fall event while the server is running? Open a second terminal and run `uv run python -m gateway.main --mode null` (or `--mode replay`) and watch it appear live!

---

## 2. API Reference & Exact JSON Schemas for Your UI

Your mobile/web app consumes 4 endpoints from `http://<laptop-ip>:8000`:

### `GET /api/health` — Server Status
```json
{
  "status": "healthy",
  "service": "spark-gateway-api",
  "version": "1.0.0"
}
```

### `GET /api/events` — List Recent Fall Incidents (Summary Feed)
Returns the 50 most recent fall events (newest first):
```json
[
  {
    "event_id": "A1B2C3D4",
    "device_id": "SPARK-NODE-01 (Forward Trip)",
    "timestamp_ms": 1760590000000,
    "confidence": 0.96,
    "shap_top_feature": "w_y",
    "report_path": "data/gateway_events/SPARK_Report_A1B2C3D4.pdf"
  }
]
```

### `GET /api/events/<event_id>` — Full Incident Detail & 6-Axis Attribution
Use this endpoint when a caregiver taps an alert card to render the 6-axis horizontal bar chart and clinical summary:
```json
{
  "event_id": "A1B2C3D4",
  "payload": {
    "event_id": "A1B2C3D4",
    "device_id": "SPARK-NODE-01 (Forward Trip)",
    "firmware_version": "v1.0.0-s3",
    "timestamp_ms": 1760590000000,
    "confidence": 0.96,
    "peak_features": {
      "a_x": 3.80,
      "a_y": 0.65,
      "a_z": 2.10,
      "w_x": 0.75,
      "w_y": 4.20,
      "w_z": 0.85
    }
  },
  "shap": {
    "top_feature": "w_y",
    "values": {
      "a_x": 0.28,
      "a_y": 0.05,
      "a_z": 0.16,
      "w_x": 0.06,
      "w_y": 0.38,
      "w_z": 0.07
    },
    "clinical_summary": "Dominant pitch angular velocity (w_y) and forward surge acceleration (a_x) consistent with a forward trip mechanism."
  },
  "report_path": "data/gateway_events/SPARK_Report_A1B2C3D4.pdf"
}
```

### `GET /api/reports/<event_id>` — Clinical PDF Report (`application/pdf`)
Streams the compiled 1-page ReportLab PDF (`SPARK_Report_<event_id>.pdf`) inline so your app can open it in an in-app PDF viewer or trigger the native OS Share/Print sheet.

---

## 3. Task Breakdown & Acceptance Checklist

### Task 1: Build the Layer 3 Caregiver Display Client
You can build this as a **Progressive Web App (PWA) / Responsive Web UI**, **Flutter app**, or **React Native app**.
- [ ] **Screen 1 — Live Alert Feed:**
  - Poll `GET /api/events` every 2–3 seconds.
  - Display a prominent status indicator (`System Active` vs. `Gateway Disconnected`).
  - Render incident cards with **Clinical Priority Badges** based on `confidence`:
    - **High Priority (Red):** `confidence >= 0.85`
    - **Moderate Priority (Amber):** `0.75 <= confidence < 0.85`
    - **Routine Check (Blue):** `confidence < 0.75`
  - Show human-readable timestamp, `device_id`, and `shap_top_feature`.
- [ ] **Screen 2 — Kinematic Explanation Drawer / Detail View:**
  - Fetch `GET /api/events/<event_id>` when an incident is selected.
  - Render a 6-axis horizontal bar chart mapping `shap.values` alongside raw `payload.peak_features`:
    - `a_x` — Longitudinal Surge Acceleration ($g$)
    - `a_y` — Lateral Sway Acceleration ($g$)
    - `a_z` — Normal / Vertical Acceleration ($g$)
    - `w_x` — Roll Angular Velocity ($^\circ/\text{s}$)
    - `w_y` — Pitch Angular Velocity ($^\circ/\text{s}$)
    - `w_z` — Yaw Angular Velocity ($^\circ/\text{s}$)
  - Display the plain-language `shap.clinical_summary` text block for non-technical caregivers.
- [ ] **Screen 3 — Clinical PDF Report Action:**
  - Button to open/download `/api/reports/<event_id>` and share/print for hospital handoff.

### Task 2: Local Wi-Fi Phone-to-Laptop Verification
- [ ] Connect your laptop and phone to the same Wi-Fi network (or laptop hotspot).
- [ ] Run `ipconfig` on your laptop to find your local IPv4 address (e.g., `192.168.1.75`).
- [ ] Point your mobile client to `http://192.168.1.75:8000`.
- [ ] Trigger a simulated fall (`uv run python -m gateway.main --mode null`) on the laptop and capture screenshots/screen-recording of the alert appearing on the phone for our defense slides.

### Task 3: Prepare Printable Cohort Consent & Clipboard Tracking Forms
Using [`docs/DATA_COLLECTION_PROTOCOL.md`](file:///f:/Aaradhya-Dev-Tamrakar/SPARK/docs/DATA_COLLECTION_PROTOCOL.md) (§2, §4, and §7), prepare two clean, print-ready documents in `docs/cohort_forms/`:
- [ ] **Document A — Volunteer Informed Consent & Screening Sheet (`VOLUNTEER_CONSENT_FORM.md`):**
  - Study title, purpose, dorsal-wrist wear instructions, and 30 cm gymnastic crash-mat + 2-spotter safety guarantee.
  - Inclusion/Exclusion screening checkboxes (age 18–35, no fractures in past 12 months, no vestibular/cardiovascular conditions).
  - Participant ID (`SA01`–`SA20`), Age, Height (cm), Weight (kg), Dominant Wrist, Date, and Signature lines.
- [ ] **Document B — 34-Activity Clipboard Trial Log (`34_ACTIVITY_CLIPBOARD_LOG.md`):**
  - Checklist table covering all **15 Fall Trials (`F01`–`F15`)** and **19 ADL Trials (`D01`–`D19`)** with columns for `Trial R01`, `Trial R02`, `Trial R03`, filename check (`<Code>_SAxx_R0x.csv`), and operator notes.

### Task 4: Connect Mobile App to Live Gateway BLE Stream (Post-Hardware)
- [ ] Switch the caregiver display client from replay mode to the live hardware gateway stream (`uv run python -m gateway.main --mode ble`).
- [ ] Verify that real falls triggered on the ESP32-S3 wearable node appear on the phone display within $\le 1.5\text{ seconds}$ over local Wi-Fi.

### Task 5: KEC Cohort Collection Execution & Dataset Verification
- [ ] Supervise participant intake, consent recording, and trial logging during crash-mat collection sessions at KEC.
- [ ] Run automated dataset integrity checks after each session:
  ```powershell
  uv run python tools/verify_cohort_dataset.py --data-dir data/nepal_cohort
  ```
- [ ] Verify 100% completion across all $N=12\text{--}20$ volunteers without missing files or corrupted headers.

### Task 6: Final Presentation Live Demo Integration
- [ ] Demonstrate real-time fall alerting on a smartphone/tablet resting on the evaluation table during the supervisor and faculty panel defense.

---

## 4. Defense Questions Sonia Must Be Prepared to Answer

**Q1: "Why is the mobile phone a display-only client rather than running BLE and SHAP directly on the phone?"**  
* **Answer:** *"Running continuous BLE scanning and heavy explainability workloads on a smartphone rapidly drains battery and suffers from mobile OS background-kill limits (Android Doze / iOS background task suspension). Offloading reception, attribution, and PDF generation to a stationary local gateway guarantees uninterrupted 24/7 monitoring, while the phone serves as a zero-overhead caregiver alert and viewing terminal."*

**Q2: "What happens if the internet goes down? Can the caregiver still receive alerts?"**  
* **Answer:** *"Yes. SPARK has zero cloud dependencies. Both the gateway server and the Layer 3 mobile client communicate strictly over the local residential or hospital Wi-Fi LAN. Incident alerts, 6-axis explanations, and PDF reports work completely offline during internet outages."*

**Q3: "How does the UI help a nurse or caregiver who doesn't understand neural networks or SHAP?"**  
* **Answer:** *"Instead of exposing raw model logits, the UI translates probabilities into clinical priority tiers—High Priority ($\ge 85\%$), Moderate Priority ($75\text{--}85\%$), and Routine Check ($<75\%$)—and pairs the 6-axis visual bar chart with a plain-language biomechanical summary (for example, highlighting dominant pitch rotation and forward surge in a forward trip) plus a one-page printable PDF incident report."*

**Q4: "How does the system ensure patient data privacy and ethical compliance?"**  
* **Answer:** *"All data remains on the local gateway storage; no telemetry or medical records are ever offloaded to public cloud servers. For our KEC trial cohort, all participant records are completely anonymized using Subject IDs (SA01–SA20), and written informed consent is secured under institutional guidelines before any data acquisition."*

**Q5: "What is the clinical value of showing SHAP feature attributions to a caregiver or doctor?"**  
* **Answer:** *"Standard fall detectors act as black boxes, simply reporting 'fall detected'. SPARK's 6-axis SHAP attribution reveals the exact biomechanical mechanism: distinguishing between a syncope collapse (dominated by vertical impact acceleration $a_z$) versus a dynamic forward slip (dominated by high pitch angular velocity $\omega_y$). This enables emergency triage to prepare the appropriate clinical intervention before reaching the patient."*
