# SPARK Layer 3 — Sonia's Overview & Roadmap (Read This First)

**Assignee:** Sonia Thapa (Roll 79043 / BEI)  
**Role:** Layer 3 Display Client & Cohort Logistics Lead  
**Phase:** Pre-Hardware Software-in-the-Loop (SIL)

---

## 1. Where Does Your Part Fit in SPARK?

SPARK is divided into three distinct layers:
1. **Layer 1 & 2 (Wearable Node - ESP32-S3):** Detects falls using a threshold gate + 18.5 KB INT8 CNN, then sends a compact fall event packet over Bluetooth (BLE).
2. **Layer 2 (Local Gateway Laptop):** Receives the event, runs mathematical feature attribution (gradient-times-input / peak-feature analysis) across 6 IMU axes, renders a 1-page clinical PDF incident report, and logs it to local JSON.
3. **Layer 3 (Your Subsystem - Caregiver Display Client):** A clean, high-contrast Mobile or Web App for nurses and caregivers. It pulls data from the laptop gateway over Wi-Fi, triggers immediate sound/visual alerts, visualizes which body motions caused the fall via bar charts, and lets the caregiver view/print the clinical PDF.

> [!NOTE]
> **Why Display-Only?**
> The mobile client **only** reads from the laptop gateway via HTTP (`http://<laptop-ip>:8000`). It does **not** handle Bluetooth Low Energy (BLE), neural network inference, or PDF compilation. Keeping heavy computation on the gateway laptop protects phone battery and prevents the mobile OS from killing background tasks.

---

## 2. Your Two Core Responsibilities

```
                               ┌────────────────────────────────────────────────┐
                               │                 Sonia's Scope                  │
                               └───────────────────────┬────────────────────────┘
                                                       │
                       ┌───────────────────────────────┴──────────────────────────────┐
                       ▼                                                              ▼
        ┌─────────────────────────────┐                                ┌─────────────────────────────┐
        │     1. Software Track       │                                │     2. Clinical Track       │
        │   Mobile/Web Display App    │                                │  Cohort Protocol Documents  │
        ├─────────────────────────────┤                                ├─────────────────────────────┤
        │ • Real-time Fall Alert Feed │                                │ • Participant Consent Form  │
        │ • 6-Axis Motion Bar Chart   │                                │ • 34-Activity Checklist Log │
        │ • Clinical PDF Report View  │                                │ • Inclusion/Exclusion Gate  │
        │ • Offline LAN Architecture  │                                │ • KEC Ethics Submission Ready│
        └─────────────────────────────┘                                └─────────────────────────────┘
```

### Responsibility A: The Layer 3 Display Client
* **What you are building:** A responsive mobile/web dashboard (built using your choice: **Flutter**, **React Native**, or **React/Vue/PWA**).
* **How to develop it right now:** You don't need physical hardware! The gateway in our repo has a built-in simulation mode that feeds realistic falls into a local REST API.
* **Key user flow:**
  1. Caregiver opens app on phone connected to local Wi-Fi.
  2. A fall occurs → Screen flashes an alert card with priority badge (High / Moderate / Routine).
  3. Caregiver taps the alert → App shows a 6-axis chart showing what triggered the fall (e.g. forward surge vs sudden rotational twist) and a plain-English clinical summary.
  4. Caregiver taps "View Clinical Report" → In-app PDF view of the formal incident report ready to print or hand off to doctors.

### Responsibility B: Nepal Cohort Logistics & Ethics Preparation
* **What this is:** For our final evaluation, we will record 12–20 volunteers on high-density crash mats at KEC performing 34 activities (15 falls, 19 daily living movements).
* **What you need to prepare:** Two printable documents (Word/Google Docs/LaTeX) based on [`docs/DATA_COLLECTION_PROTOCOL.md`](../DATA_COLLECTION_PROTOCOL.md):
  1. **Participant Informed Consent & Screening Form** (checking health criteria, safety precautions with 30 cm mat + 2 spotters).
  2. **34-Activity Clipboard Log Sheet** (to check off trials `F01`–`F15` and `D01`–`D19` during lab recording).

---

## 3. How to Test It in 2 Minutes on Your Laptop

Before touching any code, verify the backend on your laptop:

### If you already have `uv` installed:
```powershell
uv run python -m gateway.main --mode replay
uv run python -m gateway.server --host 0.0.0.0 --port 8000
```

### If you have standard Python on Windows 11 (Zero Extra Packages Needed):
You don't need to install anything! We created a zero-dependency seeder that works using only standard Python:
```powershell
# 1. Seed simulated fall events and sample PDFs (uses built-in Python only)
python tools/seed_gateway_events.py

# 2. Run the gateway REST API server (uses built-in http.server & json only)
python -m gateway.server --host 0.0.0.0 --port 8000
```
Open `http://localhost:8000` in Edge/Chrome on Windows 11. You will immediately see the active dashboard and working event endpoints!

---

## 4. How to Use the AI Prompt File

You do not need to write all UI boilerplate by hand. We have prepared an AI Agent prompt specification for you:
👉 **[`SONIA_AI_AGENT_PROMPT.md`](SONIA_AI_AGENT_PROMPT.md)**

**How to use it:**
1. Open your preferred AI coding tool (Claude Code, Cursor, GitHub Copilot Workspace, Antigravity, or ChatGPT/Gemini).
2. Copy and paste the entire contents of `SONIA_AI_AGENT_PROMPT.md` as the prompt.
3. The AI will inspect your chosen framework, consume the exact JSON schemas, scaffold the responsive screens, integrate the API, and draft the printable clinical forms!

---

## 5. Team Git & GitHub Workflow (`/github-workflow`)

To ensure smooth collaboration across the KEC engineering team without merge conflicts:

### A. Your Git & GitHub Account
* **Assigned Account Email:** `majorprj79043@gmail.com`
* **Configure Git identity once on your laptop:**
  ```powershell
  git config --global user.name "Sonia Thapa"
  git config --global user.email "majorprj79043@gmail.com"
  ```
* **Login to GitHub via CLI (or browser prompt on first push):**
  ```powershell
  gh auth login
  ```
  *(Select GitHub.com -> HTTPS -> Yes to authenticate via web browser -> Log in with `majorprj79043@gmail.com`)*

### B. The Golden Team Sync Rule: Always Use `.\sync.bat`
* In the SPARK repository, direct `git push` or `git commit` is replaced by our automated sync engine: **`.\sync.bat`** (or `.\sync.ps1`).
* **Why?** It automatically pulls with `--autostash`, resolves branches, formats conventional commit messages, updates project logs, and pushes to both remotes safely without breaking Windows execution policies.
* **How to commit your work:**
  ```powershell
  # When committing your mobile UI or cohort forms:
  .\sync.bat -m "feat(ui): implement layer 3 caregiver display dashboard"
  ```
* **How to safely pull latest team updates:**
  ```powershell
  .\sync.bat -PullOnly
  ```

