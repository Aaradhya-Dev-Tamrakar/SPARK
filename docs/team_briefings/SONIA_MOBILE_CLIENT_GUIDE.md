# Gateway & Mobile UI Engineer Task Briefing (Pre-Hardware Phase)

**Assignee:** Sonia Thapa (Roll 79043 / BEI)  
**Subsystem:** Layer 3 Mobile Display Client, Gateway Telemetry Consumption & Clinical UI  
**Primary Directory:** [`gateway/`](file:///f:/Aaradhya-Dev-Tamrakar/SPARK/gateway/)  
**Goal:** Deliver a functional mobile/web display client that receives live fall alerts, visualizes SHAP explanations, and renders clinical incident PDFs before hardware arrives.

---

## 1. Why You Don't Need Physical Silicon Yet
The backend gateway server is **already fully built and functional** in the repository ([`gateway/server.py`](file:///f:/Aaradhya-Dev-Tamrakar/SPARK/gateway/server.py)). It includes a built-in event replay simulator (`ReplayReceiver`) that generates realistic fall events (Forward Trip, Lateral Slip, Syncope, Rotational Twist) on command. 

You can build and test the entire mobile/tablet user experience on your phone over Wi-Fi right now.

---

## 2. Sonia's Action Checklist

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
       * Red Banner: High Confidence ($P(\text{fall}) \ge 0.85$).
       * Timestamp and Device ID.
       * Primary kinetic mechanism trigger (e.g., *"Dominant Pitch Rate Divergence"*).
  2. **Kinematic Explanation Screen (SHAP Attribution)**:
     * When tapping an incident card, render an interactive horizontal bar chart displaying relative SHAP feature contributions across all 6 axes:
       * Acceleration: $a_x$ (Surge), $a_y$ (Sway), $a_z$ (Heave)
       * Gyroscope: $\omega_x$ (Roll rate), $\omega_y$ (Pitch rate), $\omega_z$ (Yaw rate)
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

## 3. Defense Questions Sonia Must Be Prepared to Answer

**Q1: "Why is the mobile phone a display-only client rather than running BLE and SHAP directly on the phone?"**  
* **Answer:** *"Running continuous BLE scanning and heavy mathematical explainability libraries (NumPy, SciPy, SHAP) on a mobile phone rapidly drains phone battery and introduces operating system background-kill risks (Android Doze / iOS background limits). Offloading reception and explainability to a local household or nursing station gateway guarantees 24/7 reliability, while the phone functions as a zero-overhead notification viewer."*

**Q2: "What happens if the internet goes down? Can the caregiver still receive alerts?"**  
* **Answer:** *"Yes. SPARK has zero cloud dependencies. The gateway server and mobile client operate entirely over the local residential or clinic Wi-Fi intranet. Alerts and PDF downloads function seamlessly even during total ISP or cellular outages."*

**Q3: "How does the mobile UI convey the classifier's confidence to non-technical caregivers?"**  
* **Answer:** *"Instead of presenting raw floating-point probabilities, the mobile client maps confidence scores into standardized clinical priority badges: High Priority ($>85\%$), Moderate Priority ($75\text{--}85\%$), and Routine Check ($<75\%$), alongside a plain-language summary of the primary kinetic contributor."*
