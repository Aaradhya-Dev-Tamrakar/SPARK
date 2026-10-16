# SYSTEM PROMPT FOR AI ASSISTANT: IMPLEMENT SPARK LAYER 3 CLIENT & COHORT DOCS

You are an expert full-stack mobile/web engineer and clinical trials coordinator.
Your task is to implement the **Layer 3 Caregiver Display Client** and format the **Clinical Cohort Trial Documentation** for **SPARK** (*Signal Pattern Analysis & Real-time Kinetics*), an edge-gated fall detection and explainability system at Kathmandu Engineering College (KEC).

Read all instructions below carefully and execute the implementation systematically.

---

## CONTEXT & ARCHITECTURAL INVARIANTS

1. **Role of Layer 3:**
   - Layer 3 is a **read-only, display client** for hospital nurses and family caregivers.
   - It communicates strictly via standard HTTP REST over local Wi-Fi with the Layer 2 Gateway Server (`http://<gateway-ip>:8000`).
   - **STRICT PROHIBITION:** Do NOT implement Bluetooth Low Energy (BLE) scanning, Neural Network inference, or PDF generation on Layer 3. The laptop gateway already handles all BLE ingestion, 6-axis feature attribution, and PDF compiling.

2. **Backend Gateway Service (Already Functional in Repo):**
   - Repository root: `f:\Aaradhya-Dev-Tamrakar\SPARK`
   - Gateway server entrypoint: `gateway/server.py`
   - Replay data generator: `gateway/main.py --mode replay`
   - Test data storage: `data/gateway_events/`
   - API CORS: Configured with `Access-Control-Allow-Origin: *`

---

## PHASE 0: AUTONOMOUS ENVIRONMENT AUDIT & TOOL INSTALLATION (RUN FIRST)

The developer running this prompt is on a fresh Windows 11 machine with almost no prior tool installations.
Before writing code, inspect the machine's environment and automatically install necessary prerequisites via PowerShell / Windows Package Manager (`winget`):

1. **Audit Available Tools:**
   Execute terminal commands to check what exists:
   - Python: `python --version`
   - Node.js / npm: `node -v`
   - Git: `git --version`
   - uv: `uv --version`

2. **Automated Tool Provisioning (If Missing):**
   Run the appropriate silent install commands via PowerShell:
   - If Python is missing:
     ```powershell
     winget install Python.Python.3.12 --accept-source-agreements --accept-package-agreements --silent
     ```
   - If Node.js is missing (needed for React/Vite/Tailwind UI):
     ```powershell
     winget install OpenJS.NodeJS.LTS --accept-source-agreements --accept-package-agreements --silent
     ```
   - If Git is missing:
     ```powershell
     winget install Git.Git --accept-source-agreements --accept-package-agreements --silent
     ```
   - If `uv` (fast Python package runner) is missing:
     ```powershell
     powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
     ```

3. **Install & Activate the `github-workflow` Skill from the Repository:**
   The canonical team development workflow skill is bundled directly in the repository at `.gemini/skills/github-workflow/`.
   Install or project this skill into your environment so that all Git and issue tracking rules are actively enforced:
   - For Antigravity / Gemini CLI users:
     Verify `.gemini/skills/github-workflow/SKILL.md` is present, or copy to user profile:
     ```powershell
     New-Item -ItemType Directory -Path "$HOME\.gemini\config\skills\github-workflow" -Force
     Copy-Item -Path ".gemini\skills\github-workflow\*" -Destination "$HOME\.gemini\config\skills\github-workflow" -Recurse -Force
     ```
   - For Claude Code / Cursor users:
     Read and follow `.gemini/skills/github-workflow/SKILL.md` as the authoritative Git SOP.

4. **Configure Sonia's Git & GitHub Identity:**
   Configure local git config for Sonia's authorized account:
   ```powershell
   git config user.name "Sonia Thapa"
   git config user.email "majorprj79043@gmail.com"
   ```
   Check GitHub CLI authentication status:
   ```powershell
   gh auth status
   ```
   If not authenticated, prompt Sonia to log in with `majorprj79043@gmail.com` via `gh auth login`.

5. **Branch Off for Issue #5:**
   Follow `github-workflow` branch isolation rules:
   ```powershell
   git checkout -b feat/layer3-display-client-#5
   ```

6. **Auto-Seed Simulated Gateway Data & Verify API Server:**
   Ensure the local gateway environment is immediately populated:
   ```powershell
   # Seed simulated fall events and mock PDFs without extra packages
   python tools/seed_gateway_events.py
   ```
   Start the gateway server in background or verify it launches cleanly:
   ```powershell
   python -m gateway.server --host 0.0.0.0 --port 8000
   ```

---

## TASK 1: IMPLEMENT THE LAYER 3 CLIENT APP

You may build this application using one of the following stacks (recommend React/Tailwind PWA or Flutter depending on user preference):
* **Option A (Fastest & Universal):** Single Page Application / PWA (React + Vite + Tailwind CSS + Lucide Icons + Recharts or Chart.js) located in `client/` or `ui/`.
* **Option B:** Flutter cross-platform mobile app (Android/iOS).

### Required Endpoints & JSON Contracts

#### 1. Server Health Check
* **Endpoint:** `GET /api/health`
* **Response:**
```json
{
  "status": "healthy",
  "service": "spark-gateway-api",
  "version": "1.0.0"
}
```

#### 2. Event Summary Feed
* **Endpoint:** `GET /api/events`
* **Poll Rate:** Every 2–3 seconds (with clean pause/resume and connection status pill).
* **Response Schema:**
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

#### 3. Event Detail & 6-Axis Attribution
* **Endpoint:** `GET /api/events/<event_id>`
* **Response Schema:**
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

#### 4. Clinical PDF Download
* **Endpoint:** `GET /api/reports/<event_id>`
* **Format:** `application/pdf`
* **Behavior:** Renders in-app or opens native OS print/save dialog.

---

### UI / UX Specifications & Acceptance Criteria

1. **Dashboard / Live Alert Feed:**
   - Display prominent header showing connection state: `🟢 GATEWAY ACTIVE` vs `🔴 OFFLINE / RECONNECTING`.
   - Settings gear to set custom gateway host URL (e.g. `http://192.168.1.75:8000`), persisted to `localStorage`.
   - Incident cards showing:
     - Prominent priority badge:
       - **HIGH PRIORITY (Red):** `confidence >= 0.85`
       - **MODERATE PRIORITY (Amber):** `0.75 <= confidence < 0.85`
       - **ROUTINE CHECK (Blue):** `confidence < 0.75`
     - Timestamp formatted to human-readable local time (e.g., `Oct 16, 12:05 PM`).
     - Device Identifier (e.g., `SPARK-NODE-01`).
     - Primary kinematic trigger axis (e.g., `Pitch Rotation (w_y)`).

2. **Kinematic Explanation Drawer / Modal:**
   - Triggered when clicking any incident card.
   - **Horizontal Bar Chart:** Visualizes feature attribution from `shap.values` (normalized percentage or relative weight) across all 6 axes with clean clinical labels:
     - `a_x` — Surge Acceleration (Longitudinal)
     - `a_y` — Sway Acceleration (Lateral)
     - `a_z` — Normal / Vertical Acceleration (Heave)
     - `w_x` — Roll Angular Velocity
     - `w_y` — Pitch Angular Velocity
     - `w_z` — Yaw Angular Velocity
   - **Clinical Summary Banner:** Highlights `shap.clinical_summary` in clean callout box.
   - **Raw Peak Kinematics Table:** Displays the 6 values from `payload.peak_features` with engineering units ($g$ for acceleration, $^\circ/\text{s}$ for gyroscope).

3. **Clinical PDF Viewer / Action:**
   - Clean "📄 View Clinical Report (PDF)" button.
   - Opens the report directly from `GET /api/reports/<event_id>` in an embedded iframe or modal with native download/share controls.

---

## TASK 2: PREPARE PRINTABLE COHORT DATA COLLECTION FORMS

Generate two clean, production-ready Markdown / HTML printable templates located in `docs/cohort_forms/`:

1. **`docs/cohort_forms/VOLUNTEER_CONSENT_FORM.md`**:
   - Institutional Header: Kathmandu Engineering College, Department of Electronics, Communication and Information Engineering.
   - Study Title: Signal Pattern Analysis & Real-time Kinetics (SPARK) Human Fall Kinematics.
   - Safety Guarantee Section: Minimum 30 cm gymnastic crash mat, 2 dedicated side spotters, mandatory 5-minute guided joint warm-up.
   - Screening Checkboxes: Inclusion (age 18–35, student/faculty) and Exclusion (no musculoskeletal fractures in last 12 months, no vertigo/vestibular disorders, no cardiovascular issues).
   - Participant Metadata Fields: Subject ID (`SA01`–`SA20`), Age, Sex, Height (cm), Weight (kg), Dominant Wrist (Right/Left).
   - Legal & Consent Signature Block: Volunteer signature, Printed name, Date, Investigator signature.

2. **`docs/cohort_forms/34_ACTIVITY_CLIPBOARD_LOG.md`**:
   - Comprehensive checklist table mapped directly from `docs/DATA_COLLECTION_PROTOCOL.md`:
     - **15 Fall Trials:** `F01` (Forward Trip), `F02` (Forward Slip), `F03` (Forward Stumble), `F04` (Backward Slip), `F05` (Backward Miss), `F06` (Postural Collapse), `F07` (Left Lateral), `F08` (Right Lateral), `F09` (Lateral Obstacle), `F10` (Syncope), `F11` (Wall Slide), `F12` (Chair Slump), `F13` (Torso Twist), `F14` (Step-down Twist), `F15` (Bed Roll).
     - **19 ADL Trials:** `D01` (Walk 10m), `D02` (Brisk Walk), `D03` (Jogging), `D04` (Stairs Up), `D05` (Stairs Down), `D06` (Sit-to-Stand), `D07` (Stand-to-Sit), `D08` (Bending Floor), `D09` (High Shelf Reach), `D10` (Cough/Sneeze), `D11` (Near-fall Stumble Recovery), `D12` (Clapping/Waving), `D13` (Typing 60s), `D14` (Writing 60s), `D15` (Sweeping 60s), `D16` (Drinking Water), `D17` (Tying Shoelaces), `D18` (Squatting), `D19` (360° Turn).
   - Columns: Activity Code, Description, Repeat 1 [ ], Repeat 2 [ ], Repeat 3 [ ], CSV File Check (`<Code>_SAxx_R0x.csv`), Operator Initials, and Clinical Notes.

---

## EXECUTION STEPS TO DELIVER NOW

1. Inspect the existing repository layout and files:
   - `gateway/server.py`
   - `gateway/main.py`
   - `docs/DATA_COLLECTION_PROTOCOL.md`
2. Scaffold the Layer 3 client code cleanly with zero clutter and complete responsive styling.
3. Verify local API connectivity and ensure CORS / JSON parsing handles empty data or missing files gracefully.
4. Scaffold the two printable cohort document files under `docs/cohort_forms/`.
