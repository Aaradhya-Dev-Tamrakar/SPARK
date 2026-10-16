## Objective
Implement the SPARK Layer 3 Caregiver Display Client and finalize clinical cohort trial documentation for ethics review and crash-mat data collection.

## Subsystem Ownership
- **Assignee**: @Majorprj79043-Sonia (`majorprj79043@gmail.com`)
- **Subsystem**: Layer 3 Display Client & Validation Protocols
- **Architecture**: Display-only client reading over HTTP from the local laptop gateway (`http://<gateway-ip>:8000`). No on-phone BLE drivers or ML inference.

## Technical Briefings & Guides
- **Human Overview**: [`docs/team_briefings/SONIA_HIGH_LEVEL_OVERVIEW.md`](docs/team_briefings/SONIA_HIGH_LEVEL_OVERVIEW.md)
- **AI Agent Execution Prompt**: [`docs/team_briefings/SONIA_AI_AGENT_PROMPT.md`](docs/team_briefings/SONIA_AI_AGENT_PROMPT.md)
- **Clinical Protocol**: [`docs/DATA_COLLECTION_PROTOCOL.md`](docs/DATA_COLLECTION_PROTOCOL.md)

## Acceptance Criteria & Checklist

### Track A: Layer 3 Caregiver Display Client (Mobile / Web App)
- [ ] Connect to local gateway server (`GET /api/health` and `GET /api/events`) with configurable host IP
- [ ] Real-time incident feed with priority badges:
  - High Priority (Red): Confidence >= 0.85
  - Moderate Priority (Amber): 0.75 <= Confidence < 0.85
  - Routine Check (Blue): Confidence < 0.75
- [ ] 6-Axis kinematic explanation modal (`GET /api/events/<id>`):
  - Horizontal bar chart of `shap.values` across $a_x, a_y, a_z, \omega_x, \omega_y, \omega_z$
  - Plain-language `clinical_summary` callout box
  - Raw `peak_features` table with units ($g$, $^\circ/\text{s}$)
- [ ] Embedded 1-page clinical PDF report viewer / share action (`GET /api/reports/<id>`)
- [ ] Phone-to-laptop local Wi-Fi verification with demo screenshots

### Track B: Clinical Trial Protocols & Ethics Forms
- [ ] Scaffold `docs/cohort_forms/VOLUNTEER_CONSENT_FORM.md` with KEC institutional header, screening criteria, and participant metadata block
- [ ] Scaffold `docs/cohort_forms/34_ACTIVITY_CLIPBOARD_LOG.md` tracking all 15 Fall Trials (`F01`–`F15`) and 19 ADL Trials (`D01`–`D19`)
- [ ] Verify dataset schema compliance with `tools/verify_cohort_dataset.py`

## Git Workflow
- Branch: `feat/layer3-display-client-#5`
- Commit & Sync via wrapper: `.\sync.bat -m "feat(ui): implement layer 3 caregiver display client (#5)"`
