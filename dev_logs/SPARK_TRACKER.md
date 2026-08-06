# SPARK — Signal Pattern Analysis & Real-time Kinetics — Project Tracker (v27)

_Optimized for day-to-day use. Full history/rationale archive moved to §7
(Appendix) — read once, not needed for weekly tracking._

**Last updated:** August 6, 2026 (v27 — firmware/gateway skeletons + wire format lock committed) ·
**Proposal submitted:** July 2 (v33, hardcopy) → resubmitted July 6 (v35, hardcopy) ·
**Proposal defence:** July 9, 2026 — **occurred as scheduled, panel optimistic** (Action #25 resolved v20) ·
**Mid-term defence:** July 13, 2026 — **status not confirmed this session, see §6.5** · **Demo/thesis boards:** March 2027

**v27 change log (August 6, 2026 — parallel-track skeleton code landed, wire format locked, BOM reviewed):**

**(1) `firmware-skeleton` and `gateway-skeleton` branches merged to `main`** (commits `7f41839`, `6ed2cb6`, `fc30674`, `44dbf08`, `0db8b98`), split per `SPARK_PreProcurement_Orchestration.md`'s empty-scaffold boundary (nothing under `firmware/`/`gateway/` needed a physical board — only flashing/on-device testing does).

- **Firmware (Rupesh's WP1/WP2 scope):** ESP32-S3 ESP-IDF project scaffold, MPU6050 driver stub (rewrite path chosen per Action #24 default — reuse-vs-rewrite itself still open, this is scaffold only), Layer 1 gate (`|a| > 2.5g`, `Δt < 300ms`, §2.5 spec) as pure host-testable functions — 21/21 unit tests pass with no hardware, TFLite Micro model-load/inference call interface against a placeholder `.tflite`, peak-feature extraction, JSON event encode.
- **Gateway (Aaradhya's WP2 scope minus training):** BLE/serial receiver skeleton, SHAP integration stub (interface only — real values blocked on a trained model, separate WP2 gate), clinical PDF report template (layout/fields built, dummy data), JSON local storage stub.
- **Wire format resolved and locked** (`docs/WIRE_FORMAT_v1.md`): BLE transport, JSON payload, `confidence` = firmware's `class_probs[1]` only (`class_probs[0]` dropped, redundant under softmax), `raw_window` deferred to v2 (real SHAP explainer input, not needed by the v1 stub), `peak_features` = per-axis peak magnitude over the gate-triggered window. Payload ~250–350 bytes, no chunking needed for v1. Both sides implement against this doc; blocking comments referencing "wire format not confirmed" removed.
- **Still explicitly stubbed, not done:** live BLE pairing, real multi-client hotspot behavior (Action #20), I2C bus timing/calibration, real board flashing, battery draw measurement, actual patient PDF content.
- README updated to match (RPi/Mosquitto stack language fully removed, `dev_logs/` pointer added).

**(2) `SPARK_BOM_Procurement.xlsx` reviewed against §2.6 — no changes needed.** Line items, quantities, vendor (RoboNepal), and unit prices match §2.6 exactly; `E13=SUM(E2:E11)` sums correctly to **NPR 3,958** (only the ESP32-S3 line is priced — MPU6050/battery/USB-C/enclosure/laptop/BLE are all NPR 0 or unpriced placeholders, per Actions #16/#18/#19). File's own footer (I15) already flags the gap against the tracker's long-carried **"~NPR 15,004"** total.

**Flagging, not fixing:** that NPR 15,004 figure is itself untraceable — §2.6 has never published a full itemized breakdown that sums to it (v13's confirmation was a total, not a per-line reconciliation), so it's tracker-level debt, not a BOM-file bug. Left as-is in both places rather than force a number neither source can substantiate. Action #16's spare-ESP32-S3 unit is **not yet added** as a BOM row — still 1 line, 2 units (1 self-funded + 1 dept ask), matching current confirmed-order state; adding the spare row is real future work once #16 is actually actioned, not done here.

**Nothing in §2 (Locked Design), §5 (Data/Training spec), or §6 (Pending Benchmark) changed.** §3 (WBS) ownership lines (Rupesh→firmware, Aaradhya→gateway/SHAP) are unchanged — this session executed against existing WBS, didn't reassign it.

---

**v26 change log (August 1, 2026 — all markdown tables converted to ordered/bulleted lists):**

All markdown tables throughout the document (§0.5, §1, §7) have been converted to ordered lists with field-name prefixes or bullet formatting, improving compatibility with markdownlint and readability in plain-text contexts. No content facts changed; structure only.

---

**v25 change log (August 1, 2026 — additive tutorial notebook, no BOM/design/scope-lock change, no change to any existing file):**

**(1) `SPARK_SisFall_ML_Pipeline_Tutorial.ipynb` added**
— purely additive, does not modify `SPARK_SisFall_ML_Pipeline.ipynb` (v24's working notebook, already fixed for the zip-extraction bug this same session — see below) or any other existing file. 36 cells (12 code, 24 markdown): for each of the 6 pipeline stages, a concept explainer → a worked example run against real SisFall/SPARK data (same mount/clone Setup as the working notebook) → an exercise cell (`# TODO` stub) → a collapsible answer. Built to teach the concepts _as embedded in this specific pipeline_ (e.g. why feature engineering is needed for RF/XGBoost but not for `train_cnn.py`'s CNN, why subject-grouped splitting matters here specifically, why Sensitivity is the safety-critical metric for a fall detector) rather than as generic ML-pipeline material disconnected from SPARK's actual task and data.

Per Rule 4, built and `nbformat`-validated only — never executed.

**Same-session context, logged for the record:** immediately before this, the working v24 notebook (`SPARK_SisFall_ML_Pipeline.ipynb`) was patched (commit `385c02b`, already pushed, not part of this v25 entry) to fix two real bugs surfaced by the user actually running it in Colab: (a) Stage 1's `SISFALL_SRC` assumed an already-extracted folder, but the user's Drive holds `SisFall_dataset.zip` — a zip-extraction step (with a nested-folder-layout fallback, since the zip's internal structure wasn't independently confirmed) was added before the `prepare_sisfall.py` call; (b) the mount cell's comment referenced a nonexistent `SISFALL_ZIP_PATH` variable, which appears to have prompted an incorrect manual edit to `drive.mount()` itself (`drive.mount()` only ever accepts `/content/drive` — it cannot target a subpath directly) — comment corrected to remove the confusion. That fix is v24-adjacent, not v25's own content; noted here only so this session's full sequence stays traceable in one place.

**Nothing in §2 (Locked Design), §3 (Team/WBS), §4 (Timeline), §5 (Data/Training target spec), or §6 (Pending Benchmark) changed** — purely additive learning material plus a prior bugfix already logged via its own commit message.

---

**v24 change log (August 1, 2026 — notebook deliverable added, no BOM/design/scope-lock change):**

**(1) `SPARK_SisFall_ML_Pipeline.ipynb` added, now at `training/notebooks/`.** Landed via three raw commits directly on `main` (`7d7ce0f`, `17256e2`, `44d0e79`/`010eb1c`) rather than through `sync.ps1` — first at repo root, then `training/`, then its current path `training/notebooks/` — a same-session path correction, not three separate content changes; notebook content is byte-identical across all three locations (verified this session via cell-by-cell diff against the original build). Flagged here since it's a second `sync.ps1`-bypass on this exact file this session (the first was self-corrected before pushing) and per Rule 2 the script is the only permitted commit path — future edits to this file should route through it.

A 6-stage pipeline (dataset prep → preprocessing → EDA → modeling → evaluation → predictions), originating as a separate assignment requirement, deliberately scoped to complement rather than duplicate `train_cnn.py`:

- **Stage 1 reuses `prepare_sisfall.py` unmodified** via subprocess call against a user-supplied SisFall path — no raw-parsing logic re-implemented.
- **Stages 2–6 are new**: engineered per-channel statistical features (mean/std/min/max/range/RMS + SMA + peak resultant acceleration) computed from the raw 200×6 windows, feeding a **Random Forest + XGBoost** classical-ML track (both `GridSearchCV`-tuned, `GroupKFold` by subject) — a second algorithm family distinct from the CNN, satisfying the assignment's "at least 2 algorithms" requirement without redundantly re-deriving the CNN architecture the proposal already locks in.
- Same binary FALL(F*)-vs-NON_FALL(D*) collapse and same Sensitivity/Specificity/F1/AUC-ROC metric set as `train_cnn.py`, for direct comparability against its ≥90%/≥90% targets. Subject-grouped splitting (no leakage) applied consistently, matching `train_cnn.py`'s own approach.
- Framed in the notebook itself as an assignment deliverable + interpretability/sanity-check baseline (tree-based feature importances as a precursor to the SHAP work already planned for the gateway, per this tracker's curriculum-alignment table) — explicitly **not** a replacement for the CNN, which remains SPARK's actual on-device Layer-2 classifier.
- Per Rule 4 (repo-conventions), the notebook was built and validated (`nbformat.validate`) but never executed by Claude at any point this session.

Landed via three raw commits (see above note) — future edits must route through `sync.ps1`. Never executed. Byte-identical across all three intermediate paths, final path confirmed as `training/notebooks/SPARK_SisFall_ML_Pipeline.ipynb`.

**Nothing in §2 (Locked Design), §3 (Team/WBS), §4 (Timeline), §5 (Data/Training), or §6 (Pending Benchmark) changed** — this session is status updates plus one documentation/naming completion, not a new design, BOM, or scope decision.

---

**v23 change log (July 23, 2026 — first training code committed, end-to-end verified):**

**(1) `training/data_prep/prepare_sisfall.py` added and verified.** Loads SisFall from the official archive (`activities.rar`), produces 200Hz 3-second windows at 200 samples/window across all 38 subjects and 34 activity codes. Tested end-to-end with the actual 4506-file SisFall archive: 38,426 windows produced, all 38 subjects present, all 34 activity codes represented, 5 duplicate files correctly rejected by SHA256 checksum, zero truncation or corruption. Marks the first executable training code in the SPARK repo.

**(2) Two alternative Kaggle notebooks evaluated and rejected:**

- Notebook A: trains an existing scikit-learn pipeline on SisFall — but uses the pre-downsampled 32Hz archive, not the raw 200Hz files, introducing a schema mismatch and making it unsuitable as a reference for SPARK's own 200Hz pipeline.
- Notebook B: applies a deep-learning approach — but appears to silently truncate the dataset or pre-window in an undocumented way, making the exact data flow unverifiable.

**(3) Same-session process deviation:** the notebook commit message logged what should have gone through `sync.ps1`, bypassing the workflow documented in repo-conventions. Corrected immediately after this note — future commits route through the script.

**Nothing in §2–§6 or §7 changed** — this is a code-delivery session, not a design or BOM decision. §5's target-dataset text is not yet cross-linked to this new pipeline code.

---

## §0 — Status Summary

**Locked scope-invariant facts:**

1. **Wearable node:** ESP32-S3 (2 units, 1 self-funded by Aaradhya)
2. **Sensor:** MPU6050 (borrowed from lab, integration with existing driver from FallGuard)
3. **Gateway:** laptop only (RPi 4B fully dropped as of v12); procedural uptime mitigation confirmed executed (v22)
4. **Output:** local JSON + clinical PDF + SHAP explainability (Layer 2 only)
5. **Data:** self-collected SisFall-complementary dataset (protocol unconfirmed, HOD discussion held v22, confirmation pending)
6. **ML:** CNN (Layer 2, quantized TFLite on ESP32-S3) + classical baselines (RF/XGBoost for assignment + interpretability)
7. **Novelty Claims 1 & 3:** real prior art found (v18); recommendation to narrow wording before thesis finalization (Action #26, not yet decided)

**Tier 1 (RESOLVED v20):**

- #25: Defence outcome confirmed — panel optimistic, no pivot-related pivot-related questions

**Tier 2 (this week):**

- #16: Confirm or order spare ESP32-S3 board (zero bring-up spares exist post-RPi drop)
- #18: Confirm receipt of self-funded items (1 × ESP32-S3, USB-C cable) + lab-sourced MPU6050
- #19: Log USB-C cable price once purchased (self-funded, unpriced to date)

**Tier 3 (start now despite Sept label):**

- #23: Dataset protocol finalization (volunteer recruiting/scheduling lead time)
- #24: MPU6050 firmware reuse vs. rewrite decision (Rupesh)
- #26: Narrow novelty Claims 1/3 wording before panel finds same prior art

**Tier 4 (zero cost, no dependency):**

- #15: Lock gateway procedural mitigation as practice (already confirmed executed, needs formalization)
- #21: Update R-05 risk matrix (stale battery-draw figure)
- #22: Update R-04 risk matrix (unsourced claim)

**Tier 5 (wait for trigger):**

- #17: Board physical footprint vs. enclosure (need board in hand)
- #20: Mobile hotspot max-client cap (need known demo device)
- #6: C3 benchmark (need C3 unit)

**Future work only (7 items, Ch.6):**

- #27: Gateway on-die NPU capability assessment (laptop-specific)
- #28: Camera-based confirmation modality (vision-based 2nd opinion)
- #29: Cloud integration as opt-in (cold-storage archival)
- #30: Battery management firmware (wearable duty cycle optimization)
- Plus #7, #8, #9 from legacy tracking

**Key status lines:**

1. **Design status**

   - 🟢 Architecture, novelty claims, WBS all confirmed
   - 🟡 Claims 1 and 3's wording may need narrowing (Action #26)
   - 🟢 Gateway host is laptop; RPi dropped entirely, not kept as backup (Action #15 reframed)
   - 🟡 Wearable MCU: ESP32-S3 confirmed; Himalayan (v12) went out of stock; **RoboNepal confirmed as vendor: NPR 1,979/unit, +NPR 358 BOM delta** (Action #14 re-resolved, no longer net-zero)
   - 🟡 Two open gaps: spare-board firmware-bring-up-risk buffer doesn't exist (Action #16); board physical footprint unconfirmed vs. §7 assumption, low-priority (Action #17)
   - 🟡 Purchase/inventory status (units ordered, MPU6050 in hand) discussed but not confirmed (Action #18)

2. **Proposal package**

   - 🟢 `SPARK_Proposal_20260701_v35.zip` — signed hardcopy, submitted-of-record (resubmitted July 6, 2026 after deadline shift)
   - v33 → v35 diff: wording edits only
   - Separate `v36.zip` exists with Gantt chart fix, but was not submitted
   - **Not yet updated for S3 swap or RPi drop** — proposal text still names DevKit V1 and RPi 4B (acceptable since already submitted, but both changes need writing into post-defence revision or thesis proper)

3. **Submission status**

   - 🟢 Submitted: July 2 (v33), resubmitted July 6 (v35)
   - Defence: July 9, 2026 — occurred as scheduled, panel optimistic
   - No specific pivot-related questions reported
   - Action #25 resolved v20
   - Next step: negotiate new component costs with department following RPi drop (new Action #31)

4. **Table ref status**

   - 🟡 Unresolved — `Table~\ref{tab:component_cost}` compilation on Overleaf never confirmed
   - Not blocking (submission already happened), but worth checking before thesis finalization

5. **Not blocking, but decide soon**

   - 9 open items: #16, #17, #18, #19, #20, #21, #22, #23, #24
   - Resolved: #2, #4, #11, #12, #14, #15 (v22), legacy #6 (v22, repo created)
   - Still open: #3, #5 (see §1 below)

6. **Priority tiers (v16, re-scoped v19, Tier 1 resolved v20)**

   - 🟢 31 action items logged total (#1–31)
   - Tiers rank open, actionable items by dependency/lead-time
   - Resolved items and Future-Work-only items (7, above) sit outside tier system by design
   - Tier 1 resolved v20 (defence outcome confirmed)
   - Tier 3 (#23/#24/#26) has real lead time despite "Sept" association — don't wait on it
   - New #31 (department negotiation) not yet tiered

---

## §0.5 — Priority Tiers & Immediate Decisions

**Ordered list format (was 5×2 table in v25):**

1. **Tier 1 — RESOLVED July 10 (v20)**

   - **Focus:** Was "today, before/at defence" as of v16 (July 9) — rehearse the ESP32-S3/laptop-only pivot verbally, since v35 (signed, submitted-of-record) still names DevKit V1 and RPi 4B; recompile-check the Table ref if time permits.
   - **Outcome:** Defence occurred as scheduled — panel optimistic, no specific pivot-related questions reported. Whether the rehearsal itself happened is not independently confirmed, but the risk it existed to cover didn't surface as an issue.
   - **Items:** #25 (resolved) / #10
   - **Why this tier:** None — resolved. See new #31 below for the follow-on item this outcome opened.

2. **Tier 2 — this week, gates WP 2.0**

   - **Focus:** Confirm/place the ESP32-S3 order and MPU6050 lab-source; add 3rd spare unit _while already ordering_ rather than as a later emergency reorder; log the USB-C cable price once bought.
   - **Items:** #16, #18, #19
   - **Why this tier:** Real procurement lead time; bundling the spare now is cheaper than reopening the order later.

3. **Tier 3 — start now despite "Sept" label**

   - **Focus:** Define the self-collected dataset protocol; resolve MPU6050 firmware reuse-vs-rewrite with Rupesh in the same pass; narrow novelty Claims 1/3's wording before a panel member finds the same prior art this session's search did.
   - **Items:** #23, #24, #26
   - **Why this tier:** Volunteer recruiting/scheduling has real lead time a September start date doesn't account for; R-03's mitigation depends on #23 existing, not just being planned; #26 carries real urgency unlike the Ch.6-only items it was previously grouped with.

4. **Tier 4 — zero cost, no dependency**

   - **Focus:** Lock the gateway procedural mitigation in as actual practice, not stated intent; patch the R-05/R-04 risk-matrix notes.
   - **Items:** #15, #21, #22
   - **Why this tier:** Nothing blocks these — they just need a decision or a one-line edit.

5. **Tier 5 — correctly wait, trigger hasn't fired**

   - **Focus:** Board footprint vs. enclosure; mobile hotspot client cap; C3 benchmark.
   - **Items:** #17, #20, #6
   - **Why this tier:** Each needs something that doesn't exist yet (physical board in hand, known demo device, C3 unit on hand).

---

## §1 — Action Items (Active & Resolved)

**31 action items logged total. Ordered by item number (not priority tier).**

1. **#25 — Confirm defence outcome [RESOLVED v20]**

   - **Item:** Confirm what actually happened at the July 9 defence — did it occur as scheduled, was the ESP32-S3/laptop pivot explained if a panel member asked, any feedback given
   - **Owner:** Aaradhya
   - **Status:** **Resolved July 10 (v20).** Defence occurred as scheduled July 9. Outcome: panel was optimistic about the project. No specific questions reported about the ESP32-S3/laptop pivot despite the gap between v35's paper submission and the actual as-built design. Whether the verbal rehearsal itself happened is not independently confirmed, but the risk it was meant to cover didn't surface as an issue. Follow-on item opened as new **Action #31**.

2. **#26 — Narrow novelty Claims 1/3 wording (Tier 3, urgent despite v18 labeling)**

   - **Item:** Prior-art search (v18) found 2024–2025 papers on multi-stage CNNs, gated ensembles, and SHAP for fall detection. Current proposal wording needs narrowing to "MCU+local-gateway" specifically, not broader "no existing system" framing, before a panel member finds the same papers.
   - **Owner:** Aaradhya (decision + thesis wording)
   - **Status:** Open. General web search done (v18); formal IEEE Xplore/Scopus query still needed before thesis chapter finalized. Recommendation: narrow Claims 1 and 3 before defence if revising, or before thesis submission (Action #26 stays open).

3. **#27 — Gateway NPU/iGPU capability assessment (Future Work, laptop-specific)**

   - **Item:** Laptop (Acer Swift Go 16, Intel Core Ultra 7 155H) has on-die NPU (11 TOPS INT8) and iGPU (18 TOPS INT8) that RPi 4B structurally never had. Assess feasibility for gateway-side accelerated inference or real-time feature extraction.
   - **Owner:** TBD
   - **Status:** Open (Ch.6). Added v18 as a laptop-enabled opportunity post-RPi drop.

4. **#28 — Camera-based confirmation modality (Future Work, vision-based 2nd opinion)**

   - **Item:** Explore vision-based fall confirmation (e.g., optical flow, pose estimation) as a second-opinion check, contingent on #27's NPU/iGPU availability.
   - **Owner:** TBD
   - **Status:** Open (Ch.6). Added v18; cross-linked to #27 (v19) since modality requires compute #27 enables.

5. **#29 — Cloud archival integration (Future Work)**

   - **Item:** Optional cloud cold-storage sync for long-term patient records (complements local JSON + PDF).
   - **Owner:** TBD
   - **Status:** Open (Ch.6). Added v18.

6. **#30 — Wearable duty cycle optimization (Future Work)**

   - **Item:** Battery-management firmware to optimize sensor polling / wake intervals based on activity phase (e.g., idle vs. walking vs. fall-recovery).
   - **Owner:** TBD
   - **Status:** Open (Ch.6). Added v18.

7. **#24 — MPU6050 firmware reuse vs. rewrite (Tier 3, promoted from legacy)**

   - **Item:** Decide whether to reuse the existing MPU6050 driver from FallGuard (legacy project) or rewrite from scratch. Affects code review, testing, and confidence in the sensor integration.
   - **Owner:** Rupesh + Aaradhya
   - **Status:** Open. HOD discussion planned alongside #23 (dataset protocol); not yet confirmed.

8. **#23 — Dataset protocol finalization (Tier 3, promoted from legacy)**

   - **Item:** Define fall types, ADL types, subject count, and recording procedure for the self-collected dataset to complement SisFall.
   - **Owner:** Aaradhya
   - **Status:** Open. HOD discussion held (v22); confirmation from department still pending. Volunteer recruiting/scheduling lead time is real despite September gate label.

9. **#22 — R-04 risk matrix update (Tier 4)**

   - **Item:** Risk R-04 (external interference in sensor signal) lists a mitigation claim ("isolated data collection environment") that is not sourced to any Action or design decision. Patch the risk row with a cross-reference or reword the claim.
   - **Owner:** Aaradhya
   - **Status:** Open. Flagged v16; no action yet.

10. **#21 — R-05 risk matrix update (Tier 4)**

    - **Item:** Risk R-05 (battery drain from continuous polling) cites a specific battery-draw figure that is no longer in use post-RPi drop (RPi's quiescent draw was the reference; ESP32-S3's is different). Update the claim to match current design.
    - **Owner:** Aaradhya
    - **Status:** Open. Flagged v16; no action yet.

11. **#20 — Mobile hotspot max-client cap (Tier 5, low priority)**

    - **Item:** Measure the maximum number of simultaneous client connections supported by the mobile hotspot device(s) used for demo-day gateway uptime. Current assumption: n=2 (wearable + gateway). Real cap might be lower; if lower, affects single-device hotspot viability.
    - **Owner:** TBD
    - **Status:** Open. Flagged v15; low priority since n=2 is well within typical caps (usually 10+).

12. **#19 — Log USB-C cable price (Tier 2)**

    - **Item:** USB-C cable for ESP32-S3 gateway connection is self-funded but price was never recorded. Log the amount once purchased.
    - **Owner:** Aaradhya
    - **Status:** Open. Tier 2; gates WP 2.0.

13. **#18 — Confirm receipt of self-funded/lab-sourced items (Tier 2)**

    - **Item:** Confirm: (a) 1 × ESP32-S3 self-funded by Aaradhya — has it been ordered/received?; (b) MPU6050 borrowed from lab — is it in hand and ready for integration testing?
    - **Owner:** Aaradhya
    - **Status:** Open. Tier 2; gates WP 2.0.

14. **#17 — Board physical footprint vs. enclosure (Tier 5)**

    - **Item:** RoboNepal's ESP32-S3 board is a WROOM-1-**CAM** variant with an onboard camera FPC connector (unused by SPARK). Enclosure design (still not started, v23) needs to account for this footprint. Check compatibility once board is in hand.
    - **Owner:** Sankalpa + Aaradhya
    - **Status:** Open. Low priority (Tier 5); enclosure work hasn't started yet (v23).

15. **#16 — Confirm/order spare ESP32-S3 board (Tier 2)**

    - **Item:** Quantity was reduced to 2 units (no RPi backup). Zero spare board exists for firmware bring-up risk. Add 1 unit at next order to reintroduce a buffer.
    - **Owner:** Rupesh + Aaradhya
    - **Status:** Open. Tier 2; gates WP 2.0. Action items #16, #18, #19 should be bundled in the same order.

16. **#15 — Gateway procedural uptime mitigation (Tier 4) [PARTIALLY RESOLVED v22]**

    - **Item:** Confirm that laptop gateway uptime is guarded by an actual procedure (e.g., plugged in at demo, hotspot ready, restart scripts staged). Both compute and power halves need documentation.
    - **Owner:** Aaradhya
    - **Status:** Compute half resolved (v15 compared laptop vs. RPi 4B, confirmed laptop is sufficient; no longer a technical risk). Procedural half confirmed executed (v22, same-day as defence prep). Formalization still pending — lock the procedure as documented practice, not stated intent. Tier 4.

17. **#14 — ESP32-S3 vendor/pricing (Tier 2) [RESOLVED v13 with BOM delta]**

    - **Item:** Himalayan went out of stock same day v12 locked them as "confirmed." RoboNepal (existing SPARK vendor for RPi) carries the same module.
    - **Owner:** Aaradhya
    - **Status:** **Resolved v13.** RoboNepal confirmed: NPR 1,979/unit, 5 in stock. Board legitimacy checked (dual USB-C, BOOT/RST buttons, 16MB flash/8MB PSRAM/dual-core LX7 all match spec). **BOM delta:** 2 × NPR 1,979 = NPR 3,958 (was 2 × 1,800 = NPR 3,600) — **+NPR 358, no longer net-zero**. New BOM total: ~NPR 15,004 (was 14,646). Board variant is WROOM-1-CAM (has unused camera FPC) — different footprint than plain N16R8; see Action #17 (low-priority, enclosure not started).

18. **#13 — Self-funding disclosure (Tier 2) [RESOLVED v13]**

    - **Item:** Confirm whether one of the two ESP32-S3 units has been self-funded as a staged plan (1 now for quantization testing, 2nd before Sept 2026 gate).
    - **Owner:** Aaradhya
    - **Status:** **Resolved v13.** Self-funded arrangement confirmed: 1 × ESP32-S3 (NPR 1,979) self-funded by Aaradhya for immediate quantization work. Departmental ask reduced from 2 units to 1 unit, saving NPR 1,979. Also added USB-C cable as self-funded unpriced item. No change to absolute BOM (still ~NPR 15,004), but departmental request is now lower.

19. **#12 — MPU6050 sourcing (Tier 2) [RESOLVED v13]**

    - **Item:** Is MPU6050 already in the lab, ready to borrow, or does it need ordering?
    - **Owner:** Rupesh + Aaradhya
    - **Status:** **Resolved v13.** Lab-borrow plan confirmed (no purchase needed). Not tracking separately as a line-item cost.

20. **#11 — Enclosure form factor (Tier 2) [RESOLVED v13 — 3D-printed PLA]**

    - **Item:** Decide on form factor (wrist-worn vs. chest-worn vs. belt-clip) and manufacturing method.
    - **Owner:** Sankalpa
    - **Status:** **Resolved v13.** Enclosure method: 3D-printed PLA (in-house on KEC Makerspace equipment). Form factor still TBD; see Action #8 below (legacy, unresolved).

21. **#10 — Weekly gate system for 8th semester (Tier 2)**

    - **Item:** Establish a weekly check-in cadence for 8th-semester progress tracking, complementing the monthly gates already in §4 (Timeline).
    - **Owner:** Aaradhya + HOD (Er. Suramya Sharma Dahal)
    - **Status:** Unverified. §4 has monthly gates; whether a _weekly_ cadence was separately set up is not recorded. Assume monthly gates as the current standard until confirmed.

22. **#9 — RPi power supply (Tier 5) [LEGACY — no longer applicable, RPi dropped v12]**

    - **Item:** Confirm team RPi 4B PSU is available or budget NPR 300–500.
    - **Owner:** Sankalpa
    - **Status:** **Not applicable (v12).** RPi 4B dropped from the BOM entirely; no PSU needed.

23. **#8 — Enclosure form factor decision (Tier 5) [LEGACY — still open]**

    - **Item:** Wrist-worn vs. chest-worn vs. belt-clip (affects Layer 1 threshold calibration).
    - **Owner:** Sankalpa + Rupesh
    - **Status:** Unverified. Enclosure fabrication method resolved (3D-printed PLA, Action #11), but wear location still TBD. Depends on fall-simulation results from WP 1.0/2.0.

24. **#7 — Sensitivity threshold calibration (Tier 5) [LEGACY — still open]**

    - **Item:** Layer 1 |\mathbf{a}| and Δt values need empirical tuning from real fall simulations. Current design specifies fixed thresholds (2.5g / 300ms); whether empirical tuning has happened is not recorded.
    - **Owner:** Rupesh + Aaradhya
    - **Status:** Unverified. §2.2 (architecture) and §7 (appendix, 1D CNN internals) still state design values as fixed; no confirmation of empirical tuning from real fall data. Gates WP 1.0/2.0.

25. **#6 — SPARK GitHub repo + README + team access (Tier 5) [RESOLVED v22 — repo created]**

    - **Item:** Create a GitHub repo with README, .gitignore, folder scaffold, and team collaborator access (Rupesh, Sankalpa, Sonia).
    - **Owner:** Aaradhya
    - **Status:** **Resolved v22.** Repo created at `github.com/Aaradhya-Dev-Tamrakar/SPARK` — README, .gitignore, sync.ps1, and scaffold folders (firmware/training/gateway/data) in place. Team access (Rupesh, Sankalpa, Sonia as collaborators) not independently confirmed here — same non-assuming standard as the rest of this tracker; repo _existing_ is resolved, collaborator access is a separate, unconfirmed sub-item (minor).

26. **#5 — Self-collected dataset protocol (Tier 3) [PROMOTED to Action #23]**

    - **Item:** Define fall types, ADL types, subject count, recording procedure.
    - **Owner:** Aaradhya
    - **Status:** **Promoted v16 → Action #23 (Tier 3).** HOD discussion held (v22); confirmation pending.

27. **#4 — Review SPARK's formal novelty claims (Tier 2) [RESOLVED v22 — acronym confirmed]**

    - **Item:** Confirm the five novelty claims (§2.3 of proposal) are accurately cross-referenced in the tracker and any updates to wording are reflected in both places.
    - **Owner:** Aaradhya
    - **Status:** **Resolved v22.** Full acronym expansion ("Signal Pattern Analysis & Real-time Kinetics") confirmed and recorded for the first time since the June 30 FallGuard→SPARK rename. No conflicts between §2.3 and this tracker. Action #26 (v18) identified prior art needing narrowing; that's a separate decision, not a cross-reference mismatch.

28. **#3 — Quantization & deployment pipeline (Tier 2)**

    - **Item:** Define the end-to-end flow from training notebooks → quantization → TFLite export → ESP32-S3 deployment. Staging posts: Colab training, Colab quantization, local testing on laptop, device testing on ESP32-S3.
    - **Owner:** Aaradhya + Rupesh
    - **Status:** Open. Partially covered by existing training code (`prepare_sisfall.py`, notebooks); quantization recipe still TBD. Gates WP 2.0 gate (mid-September).

29. **#2 — Enclosure design finalization (Tier 2) [RESOLVED v13 — method only]**

    - **Item:** Decide enclosure manufacturing method (custom PCB vs. 3D print vs. off-the-shelf box).
    - **Owner:** Sankalpa
    - **Status:** **Resolved v13** (method only). Manufacturing: 3D-printed PLA on KEC Makerspace equipment. **Form factor still TBD** (Action #8, legacy, still open).

30. **#1 — MCU selection (Tier 1) [RESOLVED v8 → ESP32-S3 (v12 re-confirmed)]**

    - **Item:** Choose between ESP32 DevKit V1, ESP32-S3, or ARM Cortex-M for the wearable node.
    - **Owner:** Aaradhya + Rupesh
    - **Status:** **Resolved v8 → ESP32-S3** (supersedes original DevKit V1 choice). **Re-confirmed v12** after vendor disruption (Himalayan → RoboNepal). Board legitimacy checked, 2 units confirmed at NPR 1,979/unit. Spare buffer re-added as Action #16 (open).

31. **#31 — Department negotiation over new component costs (NEW v20, not yet tiered)**

    - **Item:** RPi 4B was originally ~NPR 18,699 in the departmental request. After dropping it from the BOM (v12), the department-funding ask changed, but no formal renegotiation has occurred. Coordinate with department (Er. Suramya Sharma Dahal, HOD) to finalize the revised funding ask.
    - **Owner:** Aaradhya
    - **Status:** Open. Opened v20 as a follow-on outcome of Action #25 (defence completed). Not yet tiered.

---

## §2 — Locked Design (Scope-Invariant)

### §2.1 — System Overview

**Distributed, two-layer architecture:**

1. **Layer 1 (Wearable Node):** Hardware-gated thresholding + edge detection

   - Accelerometer (MPU6050) on wrist, samples at 200 Hz
   - 1D CNN (quantized to INT8, ~20 kB TFLite model) trained on SisFall/custom dataset
   - Outputs: FALL/NON_FALL binary classification
   - On-device SHAP placeholder (not executed on device, logged for gateway interpretation)

2. **Layer 2 (Local Gateway):** SHAP explainability + report generation

   - Receives JSON streams from wearable over BLE
   - Runs full SHAP analysis (device-side) for feature importance visualization
   - Generates clinical PDF + JSON summary for caregiver/patient
   - Laptop (Acer Swift Go 16) as the sole gateway; procedure-based uptime mitigation (hotspot, staging scripts)

**Operational scope:** Fall detection for elderly care, primary use case Singapore/Nepal-context testing (SisFall-like data collection with local validation).

### §2.2 — Wearable Hardware

**Bill of Materials (as of v13, Aug 1, 2026):**

1. **Microcontroller:** 2 × ESP32-S3 (RoboNepal, NPR 1,979/unit confirmed v13)

   - Quantization testbed: 1 unit (self-funded by Aaradhya, v13)
   - Deployment wearable: 1 unit (departmental ask)
   - Spare: 0 units (risk, Action #16 to add 1 more)
   - Firmware: Arduino/ESP-IDF, same baseline as FallGuard legacy project

2. **Inertial Measurement Unit:** 1 × MPU6050 (lab-borrowed, v13, no purchase)

   - 200 Hz, 3-axis accelerometer
   - Driver: reuse/rewrite TBD with Rupesh (Action #24)

3. **Power:**

   - Lithium battery (to be sourced, not yet locked)
   - USB-C charging connector (included on ESP32-S3 devboard)
   - USB-C cable (self-funded by Aaradhya, v13, unpriced, Action #19)

4. **Enclosure:**

   - Form factor: TBD (Action #8)
   - Material: 3D-printed PLA (KEC Makerspace, v13)
   - Footprint: RoboNepal board is WROOM-1-CAM variant (has unused camera FPC); unconfirmed vs. §7 assumption (Action #17)

**Total BOM (§2.6):** ~NPR 15,004 (v13: +NPR 358 delta from v12 due to Himalayan → RoboNepal price difference)

### §2.3 — Novelty Claims (5 total)

1. **Dual-layer architecture with gated decision** (Claims 1)

   - Two-stage pipeline: hardware-gated edge detection → CNN-based confirmation
   - Prior art found (v18): multi-stage/gated/ensemble fall-detection systems exist; **narrowing recommended** to MCU+local-gateway specificity (Action #26)

2. **Nepal-context dataset** (Claim 2)

   - Self-collected data complementary to SisFall, capturing local activity patterns and fall environments
   - No direct prior art hits found (v18); consistent with claim holding

3. **Per-event SHAP explainability at local gateway** (Claim 3)

   - SHAP feature importance computed locally (no cloud dependency), viewable per fall event
   - Prior art found (v18): 2024–2025 papers apply SHAP to fall-detection data; narrowing recommended to MCU+local specificity (Action #26)

4. **Adaptive sensitivity strategy without reflash** (Claim 4)

   - Layer 1 thresholds tuned via configuration file + runtime override; no firmware modification needed
   - No direct prior art hits; consistent with claim holding

5. **Auto-generated clinical PDF reports** (Claim 5)

   - Patient/caregiver-facing summaries (timeline, key metrics, fall context) generated on gateway
   - No direct prior art hits; consistent with claim holding

**Recommendation (Action #26):** Narrow Claims 1 and 3's wording in thesis/proposal to "MCU-class hardware (ESP32-S3) with local, non-cloud gateway running SHAP" rather than broader "no existing system does this" framing, before a panel member finds the v18 papers.

### §2.4 — ML Pipeline (Locked)

**Dataset:**

- **Primary:** SisFall (38 subjects, 34 activities, 4,506 files) — public benchmark
- **Secondary (TBD protocol):** Self-collected data (volunteer subjects, local fall types/ADLs) — depends on Action #23 completion

**Training target (WP 2.0):**

- Sensitivity ≥90% (false-negative rate ≤10%; critical for safety)
- Specificity ≥90% (false-positive rate ≤10%; critical for usability)
- Metrics: Sensitivity, Specificity, F1-score, AUC-ROC (consistent across CNN and classical-ML baselines)
- Subject-grouped splitting: no data leakage between train/val/test

**Stage 1 (Data Prep):**

- Load SisFall from archive (activities.rar)
- Produce 200 Hz, 3-second windows (200 samples/window)
- Code: `training/data_prep/prepare_sisfall.py` (v23, verified end-to-end)

**Stage 2 (Classical ML Baseline):**

- Engineered features (mean, std, min, max, range, RMS, SMA, peak resultant acceleration per channel)
- Algorithms: Random Forest + XGBoost (GridSearchCV, GroupKFold)
- Code: `training/notebooks/SPARK_SisFall_ML_Pipeline.ipynb` (v24, assignment deliverable + interpretability baseline, never executed)

**Stage 3 (CNN — Layer 2):**

- Architecture: 1D CNN (exact layer config in §7 appendix)
- Input: raw 200×6 windows (200 samples, 6 channels: 3 accel + 3 gyro)
- Output: binary FALL/NON_FALL + per-sample logits for SHAP
- Quantization: INT8 TFLite for ESP32-S3 deployment
- Code: `training/train_cnn.py` (not shown here, locked design from v8)

**Stage 4 (Gateway SHAP):**

- Per-event feature importance (which sensor axes/aggregates drove the fall detection decision)
- Computed on laptop locally; no cloud calls
- Code: TBD (outline exists in proposal §6, implementation TBD during WP 2.0)

### §2.5 — Layer 1: Hardware-Gated Thresholding

**Design rationale:** Reduce false-positive load on Layer 2 CNN; save power by skipping CNN when clearly a non-fall.

**Algorithm:**

1. **Compute magnitude** of acceleration: |**a**| = √(ax² + ay² + az²)
2. **Check threshold:** If |**a**| < 2.5 g for > 300 ms, skip CNN (assumed non-fall)
3. **If threshold exceeded:** queue window → CNN inference → Layer 2 decision
4. **Timeout:** If no new peak acceleration for 10 seconds, clear the queue

**Parameters (currently fixed, not empirically tuned):**

- Magnitude threshold: 2.5 g (tuned empirically TBD, Action #7)
- Duration: 300 ms (tuned empirically TBD, Action #7)
- Timeout: 10 s (buffer between successive fall-risk windows)

**Status:** Design locked; empirical tuning pending real fall simulations (WP 1.0/2.0). Enclosure form factor (wrist vs. chest) affects threshold tuning (Action #8).

### §2.6 — Bill of Materials & Budget

**Component list (ordered list format, was 2-column table in v25):**

1. **Wearable node:**

   - 2 × ESP32-S3, RoboNepal: 2 × NPR 1,979 = NPR 3,958
   - 1 × MPU6050 (lab-borrowed): NPR 0
   - 1 × Lithium battery (unpriced, sourcing TBD): NPR 0 (placeholder)
   - 1 × USB-C cable (self-funded): Unpriced (Action #19)
   - Enclosure (3D-printed PLA): Material cost negligible; labor within KEC Makerspace

2. **Gateway (laptop):**

   - Acer Swift Go 16 (already owned): NPR 0

3. **Miscellaneous:**

   - Micro-USB → BLE dongle or built-in BLE (if using phone app, TBD): Unpriced
   - Development/test boards: Covered by above

**Total project cost:** ~NPR 15,004

**Funding breakdown:**

- Departmental ask (revised post-RPi drop): NPR 15,004 − NPR 1,979 (self-funded ESP32-S3) − unpriced USB-C ≈ **NPR 13,025** (departmental request, v22)
- Self-funded by Aaradhya: NPR 1,979 (ESP32-S3 for quantization testbed) + USB-C cable (unpriced)
- Lab-borrowed: 1 × MPU6050 (no cost)

**Cost deltas (version history):**

- v8–v11: Undocumented intermediate states (RPi backup → RPi fully dropped)
- v12: RPi dropped entirely; MCU vendor changed Himalayan → RoboNepal (price increase)
- v13: Self-funding arrangement confirmed; BOM confirmed ~NPR 15,004

### §2.7 — Risk Matrix (3 open items, 2 resolved)

**Ordered list format (was table in v25). R-01, R-02, R-03 unchanged; R-04, R-05 have unsourced mitigations (Actions #22, #21).**

1. **R-01: Fall detection latency (on-device CNN inference)**

   - **Impact:** High (must detect within 1 second for EMT dispatch relevance)
   - **Probability:** Low (quantized INT8 CNN on ESP32-S3 is <100 ms per inference; batching windows within the 10 s timeout window mitigates)
   - **Mitigation:** CNN quantization + local gateway immediate processing (no cloud round-trip)
   - **Status:** Mitigated by design. Resolved.

2. **R-02: False positives (non-fall → fall alert)**

   - **Impact:** High (caregiver alert fatigue, boy-who-cried-wolf erosion)
   - **Probability:** Medium (SisFall + self-collected data improve generalization; subject-grouped splitting prevents leakage)
   - **Mitigation:** Specificity ≥90% target (Layer 2 CNN + classical-ML sanity checks, v24 baseline), Layer 1 thresholding to pre-filter
   - **Status:** Mitigated by design. Resolved.

3. **R-03: False negatives (fall not detected)**

   - **Impact:** Critical (patient left unassisted, could lead to injury complications)
   - **Probability:** Medium (SisFall coverage is broad but self-collected protocol TBD; form factor affects Layer 1 thresholds)
   - **Mitigation:** Sensitivity ≥90% target, Layer 1 hardware gating prevents CNN skips, self-collected dataset reduces dataset bias. **See Action #23 (dataset protocol) — R-03's mitigation depends on this being defined, not just planned.**
   - **Status:** Open pending Action #23.

4. **R-04: External interference in sensor signal**

   - **Impact:** Medium (vibrations, magnetic fields could trigger false peaks)
   - **Probability:** Low (MPU6050 has built-in filters; wearable design isolates from large external vibrations)
   - **Mitigation:** Isolated data collection environment during testing
   - **Status:** Mitigation claim unsourced (Action #22 to patch). Open.

5. **R-05: Battery drain from continuous 200 Hz polling**

   - **Impact:** High (device unusable if drains in <1 hour)
   - **Probability:** Low (ESP32-S3 power budget ~5 mA @ 200 Hz sampling; assuming 1000 mAh battery → ~8–10 hour endurance; original reference was RPi 4B draw, now outdated v12)
   - **Mitigation:** Queue-based CNN triggering (only run CNN when Layer 1 threshold exceeded), sleep modes between windows
   - **Status:** Mitigation figure stale (Action #21 to update with ESP32-S3 draw). Open.

---

## §3 — Team & Work Breakdown Structure

**Ordered list format (was table in v25). Primary team + roles + WBS items.**

1. **Aaradhya Dev Tamrakar (Supervisor: Er. Dipen Manandhar)**

   - **Role:** Project Lead, ML Training, SHAP Integration, Gateway, Reporting
   - **WBS items:**
     - WP 0: Proposal (completed)
     - WP 1: Literature review + dataset protocol (HOD discussion held, confirmation pending)
     - WP 2: Training pipeline (prepare_sisfall.py ✓; notebooks v24–v25 ✓; quantization TBD; SHAP gateway TBD)
     - WP 3: Integration testing (simulator + real falls, TBD)
     - WP 4: Demo prep + thesis writing

2. **Rupesh Kadel (ID: 79034)**

   - **Role:** Firmware, Wearable Integration, Hardware Validation
   - **WBS items:**
     - WP 1: Layer 1 gated thresholding implementation
     - WP 2: CNN quantization + TFLite export, MPU6050 firmware (driver reuse/rewrite, Action #24)
     - WP 3: Hardware integration + field testing
     - WP 4: Demo + thesis sections

3. **Sankalpa Lamsal (ID: 79039)**

   - **Role:** Enclosure Design, Hardware Assembly, BOM Sourcing
   - **WBS items:**
     - WP 1: Enclosure form factor decision (Action #8)
     - WP 2: 3D-print enclosure, source remaining BOM items (ESP32-S3, MPU6050)
     - WP 3: Hardware assembly + durability testing
     - WP 4: Demo logistics

4. **Sonia Thapa (ID: 79043)**

   - **Role:** Data Collection, Clinical Requirement Gathering, Report Design
   - **WBS items:**
     - WP 1: Fall type/ADL type taxonomy definition (Action #23 dataset protocol)
     - WP 2: Volunteer recruitment + data collection
     - WP 3: Clinical PDF report design + feedback iteration
     - WP 4: Demo + thesis sections

---

## §4 — Timeline & Gates

**Monthly gates (ordered list, was table in v25). WP = Work Package.**

1. **WP 0 — Proposal (COMPLETED)**

   - Deadline: July 9, 2026 (defence)
   - Status: ✅ Submitted (v33 July 2, v35 July 6), defence occurred July 9 as scheduled, panel optimistic
   - Handoff: Aaradhya designs, Rupesh firmware specs

2. **WP 1 — Setup & Literature Review (July–August 2026)**

   - Deadline: August 31, 2026
   - Scope: GitHub repo scaffold (✅ v22), dataset protocol (HOD discussion held v22, confirmation pending), layer 1 thresholding design (locked §2.5), hardware procurement (Action #16/#18/#19 — Tier 2)
   - Gate: Confirm dataset protocol (Action #23), finalize BOM, order boards
   - Handoff: Training code (via WP 2)

3. **WP 2 — Training & Quantization (September–October 2026)**

   - Deadline: October 31, 2026
   - Scope: Prepare SisFall (✅ v23), classical-ML baseline (✅ v24–v25), CNN training, INT8 quantization (Rupesh), SHAP gateway code (Aaradhya), clinical PDF template (Sonia)
   - Gate: Achieve Sensitivity ≥90% & Specificity ≥90% on test set
   - Handoff: Quantized models to firmware (Rupesh)

4. **WP 3 — Integration & Field Testing (November–December 2026)**

   - Deadline: December 31, 2026
   - Scope: Firmware integration (Rupesh), enclosure assembly (Sankalpa), self-collected data (Sonia + volunteers), full-system testing, demo-day dry-runs
   - Gate: Pass integration test on real hardware, conduct minimum 10 simulated falls with ≥90% detection rate
   - Handoff: Thesis chapters

5. **WP 4 — Thesis & Demo Prep (January–March 2027)**

   - Deadline: January 2027 (expected graduation), March 2027 (demo/thesis boards)
   - Scope: Thesis writing (all), demo preparation, final hardware/software polish, presentation rehearsal
   - Gate: Thesis submitted by January 2027; demo runs without intervention

---

## §5 — Data & Training Target Specification

**Scope locked; protocol confirmation pending (Action #23).**

1. **Primary dataset: SisFall (public benchmark)**

   - 38 subjects, 34 activity codes, 4,506 files
   - 200 Hz, 3-axis accelerometer + 3-axis gyroscope
   - Activities: 12 fall types (backwards, forwards, etc.) + 22 ADL types (walking, sitting, etc.)
   - Status: Loaded and windowed via `prepare_sisfall.py` (v23 verified end-to-end)

2. **Secondary dataset: Self-collected (Nepal-context)**

   - Subjects: TBD (Action #23 — volunteer count in protocol)
   - Fall types: TBD (Action #23)
   - ADL types: TBD (Action #23)
   - Recording procedure: TBD (Action #23, HOD discussion held, confirmation pending)
   - Status: Dataset protocol unresolved; recruiting/scheduling begins once protocol locked

3. **Training-test split:**

   - Subject-grouped cross-validation (GroupKFold): no data leakage between subjects
   - Train/val/test: 60%/20%/20% by subject groups
   - Metrics: Sensitivity (recall for fall class), Specificity (recall for non-fall class), F1-score, AUC-ROC

4. **Target performance:**

   - Sensitivity ≥90% (minimize false negatives, critical for elderly safety)
   - Specificity ≥90% (minimize false positives, improve usability)
   - Latency: CNN inference <100 ms on ESP32-S3 (quantized INT8)

---

## §6 — Pending Benchmark & Milestones

### §6.1 — Training Benchmark (WP 2, due October 31, 2026)

**Gate condition:** Achieve Sensitivity ≥90% & Specificity ≥90% on held-out test set.

**Test method:** Subject-grouped K-fold (Sensitivity/Specificity computed per fold, reported as mean ± std).

**What triggers release to WP 3 (Integration):** both metrics ≥90% on SisFall + hold-out subset of self-collected data.

### §6.2 — Integration Benchmark (WP 3, due December 31, 2026)

**Gate condition:** Full system (firmware + gateway + reports) passes end-to-end test on real ESP32-S3 hardware with minimum 10 simulated falls, ≥90% detection rate.

**Simulation scope:** Controlled environment (lab or Makerspace); fall types matched to dataset protocol (Action #23).

**What this verifies:**

- Layer 1 gating works as specified (no false positives during normal movement)
- CNN inference latency acceptable on device
- Gateway receives, logs, and reports correctly
- PDF generation works end-to-end

### §6.3 — Demo Benchmark (March 2027)

**Gate condition:** Live system demonstration (wearable + gateway) on student-collected subject or trained volunteer, falls triggered by safe simulated fall types, report generated in real-time.

**What this verifies:** System end-to-end reliability under observation; presentation of findings to academic panel.

### §6.4 — Thesis Chapters (January 2027)

**Expected content:**

- Ch. 1–2: Introduction, related work, novelty claims (narrowed per Action #26)
- Ch. 3: System design & architecture (§2 of this tracker)
- Ch. 4: Dataset & methodology (§5, Action #23 results)
- Ch. 5: Experimental results & analysis
- Ch. 6: Future work (Actions #27–30, laptop-enabled components + security gaps)
- Appendix: LaTeX renderings of designs, full hyperparameter sweeps, code listings

### §6.5 — Presentation Reformatting & Rebuild (TBD, placeholder)

**Scope (requested but details TBD):** Reformat and rebuild the proposal/defence presentation for March 2027 demo day.

**What's known from outside this tracker:** A presentation deliverable is expected alongside the thesis, likely using the SPARK_Template_2027.pptx established for the Mid-Term Defence (July 13, 2026).

**What's unverified here:** Specific slides, messaging, or audience adaptations — carry forward only what was confirmed in prior sessions (template exists, slide master inheritance documented).

**Open questions:**

- Slides targeted at which audience (academic panel, students, family/clinicians)?
- How much of the March demo should the presentation cover (design, results, live demo, all)?
- Reuse of v35 presentation structure or new format?

**Status:** Placeholder section. No reformatting/rebuild specifics decided yet.

---

## §7 — Full History, Rationale & Design Justifications (Appendix)

_Read once for context. Not needed for weekly tracking. Collapsed in this version; see historical tracker versions for full details._

### Legacy Items (moved here at v16; most now promoted to Actions)

**Ordered list (was table in v25):**

1. **Legacy #1 — MCU selection (PROMOTED → Action #1, resolved v8)**

   - Status: Resolved. ESP32-S3 chosen; vendor disruption managed via Action #14.

2. **Legacy #2 — Enclosure manufacturing method (PROMOTED → Action #2, resolved v13)**

   - Status: Resolved (method only). 3D-printed PLA via KEC Makerspace. Form factor TBD → Action #8.

3. **Legacy #3 — Proposal formulation & submission (PROMOTED → Action #4, resolved v22)**

   - Status: Resolved. Proposal v35 submitted and defended; minor wording edits throughout.

4. **Legacy #4 — Dataset sourcing: SisFall or custom? (PROMOTED → Action #24, open)**

   - Status: Open. Using both: SisFall (primary) + self-collected (secondary, protocol TBD → Action #23).

5. **Legacy #5 — GitHub repo & collaboration setup (PROMOTED → Action #6, resolved v22)**

   - Status: Resolved. Repo created; team access pending confirmation (minor).

6. **Legacy #6 — Self-collected dataset protocol (PROMOTED → Action #7, now Action #23, open)**

   - Status: Open (Tier 3). HOD discussion held (v22); confirmation pending. **Volunteer recruiting/scheduling lead time is real despite September gate label.**

7. **Legacy #7 — Wearable enclosure form factor (PROMOTED → Action #8, open)**

   - Status: Open (Tier 5). Depends on fall-simulation results from WP 1.0/2.0.

8. **Legacy #8 — Layer 1 sensitivity calibration (PROMOTED → Action #9, now Action #7 in §1, open)**

   - Status: Open (Tier 5). Empirical tuning pending real fall data (WP 1.0/2.0).

9. **Legacy #9 — RPi 4B power supply budgeting (NOT applicable v12, no longer tracked)**

   - Status: Superseded. RPi dropped entirely; no PSU needed.

---

## Supersedes

v25, v24, v23, v22, v21, v20, v19, v18, v17, v16, v15, v14, v13, v12, v9–v11, v8, v7, v6, v5, v4, consolidated v1, FallGuard master v3, etc. All originals retained as historical record.

**Key version milestones:**

- **v35 proposal:** Signed hardcopy, submitted July 2 & resubmitted July 6 (still names DevKit V1, RPi 4B; updates TBD for thesis)
- **v8:** MCU choice (DevKit V1 → ESP32-S3)
- **v12:** RPi drop + vendor churn (Himalayan → RoboNepal)
- **v13:** Self-funding + BOM confirmation
- **v16:** Priority tier system introduced
- **v18:** Literature-gap check (Action #26 identified prior art needing narrowing)
- **v19:** Self-consistency audit (5 stale cross-references fixed)
- **v20:** Defence outcome confirmed (Action #25 resolved)
- **v22:** Full acronym confirmed, Action #15 finalized (procedural), Action #23 advanced
- **v23:** First training code (`prepare_sisfall.py`), process deviation corrected
- **v24:** Classical-ML notebook (`SPARK_SisFall_ML_Pipeline.ipynb`), 6-stage pipeline
- **v25:** Tutorial notebook (`SPARK_SisFall_ML_Pipeline_Tutorial.ipynb`), 6-stage walkthrough, prior bugfix to v24
- **v26:** All tables converted to ordered/bulleted lists per user preference
- **v27:** `firmware-skeleton`/`gateway-skeleton` merged, wire format locked (`WIRE_FORMAT_v1.md`), BOM reviewed (no changes needed, NPR 15,004 gap flagged not fixed)
