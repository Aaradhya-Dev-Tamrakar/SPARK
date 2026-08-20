# SPARK — Signal Pattern Analysis & Real-time Kinetics — Project Tracker (v51)

_Optimized for day-to-day use. Full history/rationale archive moved to §7
(Appendix) — read once, not needed for weekly tracking._

**Last updated:** August 20, 2026 (v51 — 5 Model Sensitivity & Accuracy Enhancements delivered: Youden threshold tuning, class-balanced INT8 calibration, time-series augmentation, positive class weighting boost, and dropout/batchnorm regularization; test suite expanded to 36 passing tests) ·

**v51 change log (August 20, 2026 — 5 Accuracy & Sensitivity Techniques implemented & verified):**

- **`training/train_cnn.py` enhanced with 5 key optimization techniques:**
  1. **Optimal Decision Threshold Tuning**: Implemented `find_optimal_threshold()` using Youden's $J$ statistic ($J = \text{Sensitivity} + \text{Specificity} - 1$) on the validation split. Evaluates and reports held-out test metrics at both default $0.50$ and optimal operating thresholds, exporting metadata to `model/model_config.json`.
  2. **Class-Balanced Calibration Support**: Enables balanced 50/50 sampling for INT8 calibration.
  3. **Time-Series Data Augmentation**: Implemented `augment_windows()` with temporal shift ($\pm 5$ samples / $\pm 25\text{ ms}$), sensor magnitude scaling ($\pm 5\%$), and Gaussian noise jitter to prevent subject overfitting.
  4. **Loss Weighting / Positive Class Boost**: Added configurable `--pos-weight-boost` (default $1.25\times$) to penalize missed falls (False Negatives) and steer gradient descent toward target $\ge 90\%$ sensitivity.
  5. **Regularization (Dropout / Batch Normalization)**: Added `--dropout` (default $0.20$) and optional `--use-batch-norm` to stabilize feature learning across diverse subjects without altering MCU inference memory contracts.
- **`training/quantize_model.py` upgraded:**
  - `build_representative_dataset()` updated with class-balanced sampling (50% FALL, 50% NON_FALL) to prevent high-acceleration impact clipping during INT8 post-training quantization.
  - Added threshold-aware evaluation loading calibrated thresholds from `model_config.json` or `--threshold` CLI flag.
- **Test suite expanded (`tests/`):**
  - Added `tests/test_train_cnn.py` with 8 unit tests covering data augmentation, threshold tuning, architecture construction, and leakage-free splitting.
  - Added balanced calibration and custom threshold tests to `tests/test_quantize_model.py`.
  - All 36 repository tests passing cleanly (`uv run pytest`).

**v50 change log (August 20, 2026 — Gateway & SHAP Explainability Subsystem delivered & verified):**

- **`gateway/shap_pipeline/explainer.py` implemented.**
  - `CnnShapExplainer`: Computes gradient-based feature attribution ($X \times \nabla_X Y$) over 6 IMU channels on raw $200 \times 6$ waveforms using trained Keras CNN.
  - `PeakFeatureExplainer`: Analytical attribution fallback for compact peak telemetry frames.
  - `get_explainer()`: Dynamic factory binding to `spark_cnn.keras`.
- **`gateway/receiver/receiver.py` updated.**
  - `ReplayReceiver`: Implemented for replaying recorded/simulated events during tests and demos.
  - `SerialReceiver`: Line-delimited JSON stream reader for USB-Serial tethering.
- **`gateway/report/pdf_report.py` upgraded.**
  - One-page clinical PDF report generator with metadata, confidence badges, narrative summary, horizontal SHAP attribution chart, and clinician sign-off block.
- **`gateway/main.py` upgraded.**
  - CLI service entry point supporting `--mode {null, replay, serial}`, `--model`, and `--out-dir`.
- **`tests/` test suite expanded.** Added `test_shap_pipeline.py`, `test_pdf_report.py`, and `test_gateway_pipeline.py`. All 26 repository tests passing cleanly.

**v49 change log (August 20, 2026 — Action #3, INT8 quantization pipeline delivered & verified):**

- **`training/quantize_model.py` implemented.** Standalone INT8 post-training quantization script using TensorFlow Lite Converter.
  - Implements representative dataset calibration using 200 randomly sampled training windows per proposal §5 methodology.
  - Produces full integer INT8 FlatBuffer (`spark_cnn_int8.tflite`) ensuring model size satisfies the $\le 120\text{ KB}$ flash budget.
  - Generates 16-byte aligned C header array (`spark_cnn_int8.h`) with optional `--firmware-out` flag for direct firmware drop-in (`firmware/main/models/`).
  - Computes and logs FP32 vs. INT8 accuracy comparison across Sensitivity, Specificity, F1-score, and AUC-ROC to quantify accuracy delta.
- **`tests/test_quantize_model.py` added.** 13 comprehensive unit tests added using synthetic models and data (no SisFall dataset dependency for CI/testing). All 18 repository tests passing cleanly.
- **`training/train_cnn.py` updated** with a next-step CLI pointer to `quantize_model.py`.
- **Action #3 status updated to Resolved (quantization & export side).**

**v48 change log (August 11, 2026 — Action #39, international-availability check, search closed):**

- **Google Images search for the original v43 spec** (M2.5 self-tapping, A2 stainless, flanged button head) returns real, genuine matches — confirming this is a normal, standard, buyable fastener, not an over-specified fiction.
- **Every visible result is UK/international**: eBay UK, Westfield Fasteners, Nuts of Chorley, TIMCO, Amazon UK, RC4WD, Fusion Fixings. No Nepal-based seller appeared. Same "not locally available" conclusion already reached for Ubuy (v44) — international stock, cross-border shipping, doesn't meet the "readily available in Nepal" bar set for this Action.
- **No new candidate, no vendor change.** This closes the spec-search loop: the ideal spec is confirmed real but confirmed non-local; the v45 Daraz kit (relaxed spec, local, in-stock) remains the sourced answer unless the person chooses to import instead.
- **No cost/BOM change.**

**v47 change log (August 11, 2026 — Action #39, Himalayan Solution candidate reviewed and rejected):**

- **Reviewed `himalayansolution.com` — "500PCS M2 M2.5 M3 KM Screw Flat Head Phillips," Rs.1,200.** Himalayan Solution is already an established BOM vendor (TP4056, breadboard, R/C assortment lines) — genuinely worth checking.
- **Rejected on two independent grounds:** (1) listing confirms **0 available / Out of Stock** — not currently purchasable regardless of spec fit; (2) product photos show a **flat/countersunk head profile**, same geometry the v43 spec explicitly excluded (needs a precisely matched conical seat in the TPU or risks a proud sharp edge / cracked boss).
- **Decision: keep the v45-sourced Daraz kit as-is.** No cost/BOM change.

**v46 change log (August 11, 2026 — Action #39, second candidate reviewed, not adopted):**

- **Reviewed `daraz.com.np/tag/self-tapping-screws/` category listing** — one product ("100pcs Small Micro Phillips...") shows dimensions M2×5/6/8/10mm, **M2.5×6/8/10/12mm**, M3×8/10mm on its card. Real size match for M2.5×6/×8mm.
- **Not adopted.** Product title itself reads "Flat Countersunk...Pan Head" — countersunk and pan head are different, mutually exclusive geometries (flat conical bearing surface vs. rounded cylindrical sides), so the title contradicts itself. Head shape can't be trusted from the card alone; would need the live listing opened to resolve, which wasn't done this session.
- **Decision: keep the v45-sourced Daraz kit as-is** rather than swap on an unconfirmed detail. This candidate logged for future reference only.
- **No cost/BOM change.**

**v45 change log (August 11, 2026 — Action #39 spec relaxed, vendor resolved):**

- **Minimum requirements re-derived, separating fixed from preferred.** Fixed: M2.5 thread, self-tapping (no insert equipment on hand), length within wall/boss thickness (unverified regardless of vendor — Action #17 CAD blocker), not countersunk (tolerance risk). Downgraded from requirement to preference: A2 stainless, flanged button head — both were precautionary for a skin-contact scenario at the fastener that was never actually confirmed to exist.
- **Length unified ×6mm/×10mm → ×8mm** for both PCB mount and shell-join. Matches the sourced kit's max size; shorter length is also lower-risk against an unverified wall thickness, so this reads as a safety-neutral-to-positive simplification rather than a pure compromise.
- **Vendor resolved: Daraz Nepal (`daraz.com.np`) M2/M2.5/M3 machine screw kit** — live listing, confirmed Kathmandu-valley delivery. Ubuy Nepal 304-stainless/button-head assortments were considered but set aside: Ubuy is cross-border resale (international stock shipped in), not local stock, same treatment already applied to other BOM sourcing decisions this session; also, the specific M2.5 size wasn't confirmed present in any Ubuy listing's size breakdown, unlike the Daraz kit which explicitly lists M2.5×3–8mm.
- **Material/head-type downgrade logged explicitly, not silently dropped** — if the CAD model later shows the fastener does contact skin, this line should be revisited against the original A2-stainless/button-head spec.
- **No cost change** — NPR 300 placeholder retained; kit's real price wasn't visible on the fetched listing page.

**v44 change log (August 11, 2026 — Action #39 vendor search, no confirmed match):**

- **Searched Nepal market for M2.5 A2-stainless flanged-button-head self-tapping screws.** General Kathmandu hardware retailers (hardwarepasal.com, confirmed via live category page) stock only construction-scale clipboard/truss-head screws (4mm–8mm shaft, 20–100mm length) — no M2.5 or electronics-scale fasteners.
- **One real match found:** Daraz Nepal (`daraz.com.np`) lists "helper 300pcs M2/M2.5/M3 Machine Screws Set" (No Brand) — includes M2.5×3/4/5/6/7/8mm, covers the ×6mm PCB-mount length. **Not adopted as the sourced vendor** — listing states material as "metal" only (stainless unconfirmed), doesn't specify button head, and has no ×10mm length (shell-join length would need a different source, or the spec relaxes to ≤8mm).
- **No cost/BOM change.** Logged as an open partial-candidate in §1 Action #39, not a resolution.

**v43 change log (August 11, 2026 — Action #39 fastener spec finalized: material, head type, safety reasoning):**

- **Material: A2 stainless.** Rejects black-oxide/plated carbon steel — sweat exposure (worn device) risks corrosion; stainless also avoids nickel-heavy alloys linked to contact dermatitis, relevant since fasteners sit against/near skin through the TPU shell.
- **Head type: flanged button head, not countersunk.** Countersunk needs a precisely matched conical seat printed into the TPU — any mismatch either leaves the head proud with a sharp rim, or over-drives and cracks the boss. Flanged button head spreads clamp force over more surface area, reducing head sink-in as TPU compresses under repeated wear-cycle flex; integrated washer face is more forgiving of print tolerance than a countersunk seat.
- **Open item flagged, not resolved:** ×6mm/×10mm lengths still unverified against actual wall/boss thickness — no CAD model exists yet (same Action #17 blocker as Action #38's charging panel). This is a real pending safety check, not just documentation debt — a screw bottoming through the inner wall toward skin is the actual failure mode to avoid, independent of head style.
- **No cost/quantity change** — same qty 20, NPR 300 total, vendor still TBD.

**v42 change log (August 11, 2026 — fasteners added to BOM, xlsx duplicate regression re-fixed):**

- **Action #39 added — fasteners were never in the BOM.** Neither `docs/SPARK_BOM_Procurement.xlsx` (pre-deletion) nor `docs/SPARK_Component_Order_Form.xlsx` had a screw/fastener line, despite the enclosure's PCB mount (locked v29) and shell-half join both needing them. Added: M2.5 self-tapping, qty 20 (mixed ×6mm PCB mount / ×10mm shell join), NPR 15/unit placeholder = NPR 300. Vendor TBD, unpriced-baseline like other placeholder lines (breadboard, R/C assortment).
- **`docs/SPARK_Component_Order_Form.xlsx` updated:** new row 11 (fasteners) inserted with merge ranges (`D:E`, `H:I` on the GRAND TOTAL row) manually unmerged/reapplied per the v15 row-insert lesson — formula drift avoided.
- **Regression re-found and fixed: `docs/SPARK_BOM_Procurement.xlsx` was still on disk.** v37's changelog claimed this file was `git rm`'d, but it remained tracked and present — identical failure class to the bug v37 itself was fixing. Actually deleted this session.
- **Total: NPR 13,577 → NPR 13,877** (+NPR 300, fasteners).

**v37 change log (August 10, 2026 — repo hygiene regression fixed, VS Code compile support added, repo decluttered):**

- **Regression fixed: `docs/SPARK_BOM_Procurement.xlsx` deletion never actually happened.** v36's changelog said "Deleted," but the file remained `git`-tracked and present on disk — same class of failure as the v30 lock-file regression. Now actually `git rm`'d; `docs/SPARK_Component_Order_Form.xlsx` is the sole canonical procurement spreadsheet, no stale duplicate remains.
- **Proposal made VS Code/LaTeX Workshop compile-ready.** `docs/SPARK_Proposal/ThesisReports/.latexmkrc` added (pdflatex-only, no glossary/bibtex hook needed — matches this proposal's `thebibliography`/`makeidx` setup). No `.vscode/settings.json` needed; LaTeX Workshop auto-discovers the `\documentclass` root.
- **Repo decluttered:** 17 duplicate PNGs at `docs/SPARK_Proposal/` root removed (canonical copies live in `Figures/`, confirmed byte-identical and unreferenced by `\graphicspath`); orphaned `docs/SPARK_Proposal_20260701_v37_md/main.md` duplicate removed; redundant `.gitkeep` removed from `docs/`, `firmware/`, `gateway/`, `training/`, and repo root (all non-empty; `data/.gitkeep` kept, `data/*` stays gitignored).
- **`.gitignore` updated:** LaTeX build artifacts (`.aux .fdb_latexmk .fls .idx .ilg .ind .lof .log .lot .out .synctex.gz .toc`) ignored repo-wide; `thesis_report.pdf` explicitly whitelisted as the tracked deliverable.
- **README synced:** status paragraph and `docs/` structure line updated to reflect TPU enclosure, sourced battery/MPU6050/USB-C/Velcro-strap, Order Form as canonical BOM, and VS Code-compilable proposal; version pointer corrected v30 → v37.
**Proposal submitted:** July 2 (v33, hardcopy) → resubmitted July 6 (v35, hardcopy) ·
**Proposal defence:** July 9, 2026 — **occurred as scheduled, panel optimistic** (Action #25 resolved v20) ·
**Mid-term defence:** July 13, 2026 — **status not confirmed this session, see §6.5** · **Demo/thesis boards:** March 2027

**v36 change log (August 10, 2026 — R-05 fixed, Velcro/enclosure conflict resolved, BOM xlsx sync gap found+fixed, task_2026-08-10_001 handoff from user5):**

- **Action #21 resolved — R-05 draw/endurance math fixed.** Old figure ("~5 mA @ 200 Hz → 8–10hr on 1000 mAh") didn't reconcile (1000/5 = 200hr). Replaced with an estimated ~110–140 mA active-draw range that actually reconciles against the sourced 1100 mAh LiPo (v34) at 8–10hr. Explicitly flagged as estimate (no INA219 telemetry exists in this design to measure it — that part is dead/RPi-era). §2.2, §2.7 updated.
- **§2.2 Velcro/enclosure conflict resolved.** Confirmed as two distinct components: the enclosure's own built-in Velcro closure tab (part of the 3D-printed shell, no separate purchase) and the BOM's separately-purchased "Velcro wrist strap" (RR-papers, NPR 500×2) for additional retention/security. §2.2 and §2.6 wording updated.
- **`docs/SPARK_BOM_Procurement.xlsx` found frozen at v30 state** (NPR 5,434, missing spare ESP32-S3, Velcro strap, TPU enclosure pricing, all v31–v35 changes) — never synced despite 5 tracker version bumps. Deleted — `docs/SPARK_Component_Order_Form.xlsx` (already at v35 state, NPR 9,737, matches tracker) is now the sole canonical procurement spreadsheet.
- **Enclosure weight (~NPR 90, v38) — improved geometric estimate, still not a real slice.** No CAD model exists to slice; see §1 Action #36 for the calculation basis. Not fully resolvable without the model.
- **Order placement — still zero confirmed.** Actions #16/#18 remain open; procurement, not tracker editing, resolves these.

**v35 change log (August 10, 2026 — gateway architecture clarified, BLE dongle dropped):**

- **§2.1 System Overview revised.** The v28-era "either/or, phone-or-laptop gateway" framing (which never had solid reasoning behind it — see below) is dropped. **Laptop remains the sole BLE gateway and sole SHAP/PDF pipeline compute**, matching the original single-gateway design. **Phone added as a new Layer 3: display-only client** — no direct BLE link to the wearable, no on-device SHAP/PDF computation, just reads a completed report from the laptop over local network.
- **BLE dongle line dropped from BOM (§2.6).** It was locked v28 on reasoning that didn't actually hold up: "phone-app-involved rules out built-in-BLE-only" doesn't follow, since ESP32-S3, laptop, and phone all have native BLE — no external hardware needed on any device. With the phone now display-only (not a BLE client at all), the justification is doubly moot. Was unpriced (NPR 0) — no cost impact, total unchanged at NPR 9,737.
- **Action #20 (hotspot max-client cap) assumption revised**: n=2 → n=3 (wearable + laptop + phone display client), still low priority.
- **Rationale for display-only over full-pipeline phone:** re-implementing/porting the SHAP + PDF stack to mobile (native rewrite or bundled Python runtime) is real, non-trivial scope this late in the timeline; duplicated pipeline logic across laptop and phone means every future fix/format change lands twice; Novelty Claim 3 ("per-event SHAP explainability at local gateway") only requires the computation to happen locally somewhere — the laptop already satisfies that, so a display-only phone doesn't weaken the claim.
- **Owner assigned v38:** Aaradhya (Project Lead, Gateway) — display client is a read-only consumer of the laptop-gateway pipeline he already owns (SHAP/PDF, local-network report serving); no new team member needed. §3 updated.

**v34 change log (August 10, 2026 — battery sourced, enclosure material switched PLA→TPU):**

- **Battery: sourced.** Giga Nepal, 3.7V **1100mAh** LiPo, **NPR 550** — live listing, pouch cell, exceeds v28's 1000mAh target. Clears the 4hr endurance floor with margin at realistic ESP32-S3+MPU6050 draw estimates. Sourcing gap closed; the underlying R-05 draw-figure staleness (Action #21) is a separate, still-open issue — not resolved by this.
- **Enclosure material: PLA → TPU, switched.** KEC Makerspace's real checkout/inventory system stocks TPU only (886g Black in stock, NPR 4/g KEC rate) — PLA was never actually verified against real makerspace stock, just assumed since v13. This also aligns the tracker with the enclosure concept render (`dev_logs/design-assets/enclosure_concept_v1_two_zone_bracer.png`), which already specified TPU — previously flagged as a render-vs-tracker conflict, now resolved by fixing the tracker side.
- **Enclosure cost: NPR 0 → ~NPR 160 → ~NPR 90 (v38, geometric estimate).** TPU is gram-priced at KEC (NPR 4/g), not free — the v13 "negligible/in-house" note assumed PLA scrap/inhouse-free fabrication that doesn't hold for TPU. v34's NPR 160 was a flat 40g eyeball guess with no basis shown. v38 replaces it with a hand-computed two-zone volume (270° arc / 75% wrap from Aaradhya's forearm measurement — 12cm band length, 16cm reference circumference, matches the render's stated 75% wrap independently; wrist zone slim + forearm zone with electronics bulge sized against DI-01's real component footprints: ESP32-S3 25×50×7mm, 1000mAh LiPo 32×52×7mm, TP4056 15×17×2mm; 2mm wall per CAD_SOFTWARE_GUIDE.md's logged spec; TPU 95A density 1.21 g/cm³) → **~18.5 cm³, ~22g, ~NPR 90**. **This is still not a real slice** — no CAD model or slicer output exists in the repo. Treat as a better-grounded placeholder, not Action #17's resolution; that needs the actual model built and sliced.
- **Total BOM: NPR 9,027 → NPR 9,737** (+NPR 550 battery, +~NPR 160 enclosure).
- **§2.2, §2.6, §0 updated.** BOM xlsx not yet synced this session — pending.

**v33 change log (August 10, 2026 — MPU6050 sourced, USB-C priced, Velcro strap re-added):**

- **MPU6050: sourced.** Himalayan Solutions, live listing, MPU-6050/GY-251 module, 17 in stock — **NPR 350/unit** (below the v31 NPR 500 placeholder). Action #18's MPU6050 half resolved.
- **USB-C cable: sourced.** Daraz, **qty 3 @ NPR 267/unit = NPR 801** (was unpriced placeholder, Action #19). Quantity raised 1→3 (spares included).
- **Velcro wrist strap re-added as a genuine separate BOM line.** RR-papers, qty 2 @ NPR 500 = NPR 1,000. Distinct from the enclosure's built-in Velcro closure (§2.2, no separate purchase) and the compression arm sleeve (base layer, different function) — user confirmed this is a real, separate item, not a duplicate.
- **AMS1117-3.3 LDO: confirmed dead, not re-added.** ESP32-S3 devboard and MPU6050 breakout both carry their own onboard regulation; no unregulated sensor in this design needs it. Same RPi-era-only part flagged dead since v28.
- **Total BOM: NPR 7,376 → NPR 9,027** (MPU6050 net −NPR 150 vs. its own NPR 500 placeholder, +NPR 801 USB-C ×3, +NPR 1,000 Velcro strap ×2, over v32's NPR 7,376).
- **§1 (Actions #18, #19), §2.2, §2.6 updated.** BOM xlsx synced.

**v32 change log (August 10, 2026 — ESP32-S3 vendor reverted Himalayan, Action #14 reopened):**

- **Action #14 reopened and re-resolved.** Himalayan (dropped v12 — went out of stock same day locked) is confirmed back in stock (152 units, live listing, WROOM-1-CAM/N16R8 variant matching spec) at **NPR 1,800/unit**, undercutting RoboNepal's NPR 1,979/unit.
- **Vendor switched: RoboNepal → Himalayan**, all 3 units (post-v31 spare-inclusive count). **BOM delta: 3 × NPR 1,979 = NPR 5,937 → 3 × NPR 1,800 = NPR 5,400, −NPR 537.**
- **Total BOM: NPR 7,913 → NPR 7,376** (v31's reconciled total, corrected for the vendor swap only — no other lines touched).
- **Legacy Table 4.1 (proposal, `chapter4_feasibility_study.tex`) re-checked, still not a source.** Contains ESP32 DevKit V1 (not S3), 18650/TP4056/AMS1117/INA219/MicroSD/RPi 4B/Velcro strap — all confirmed dead per v28's exclusion list. Not reconciled into tracker.
- **§1 (Action #14), §2.2, §2.6 updated.** BOM xlsx synced (vendor/price cells only).

**v31 change log (August 10, 2026 — funding model changed to all-departmental, spare ESP32-S3 added):**

- **Funding model changed: all BOM lines now departmental-ordered.** Self-funded (Aaradhya) and lab-borrowed statuses dropped across the board — supersedes v13's self-funding split and MPU6050's lab-borrowed status.
- **ESP32-S3: 2 → 3 units.** Action #16 spare buffer added to BOM (previously tracked as an open gap with 0 spares). All 3 units departmental-ordered, RoboNepal, NPR 1,979/unit = NPR 5,937.
- **MPU6050: lab-borrowed → departmental-ordered.** No confirmed vendor/price exists anywhere in tracker history; entered as an unsourced NPR 500 placeholder — needs a real quote before ordering (Action #18 updated to reflect this).
- **USB-C cable, arm sleeve: self-funded → departmental-ordered.** Prices/specs unchanged (cable still unpriced/Action #19; arm sleeve still NPR 136 Daraz listing, locked v30).
- **Total BOM corrected to NPR 7,913** (formula-driven per-line sum). Discovered the tracker's carried-forward "~NPR 15,004"/"~NPR 16,480" prose totals never actually equaled a real itemized sum — same gap v27 flagged but left unfixed. v31 reconciles tracker and xlsx to the real number instead of propagating it further.
- **§2.2/§2.6/§1 (Actions #16/#18/#19) updated accordingly.** BOM xlsx (`docs/SPARK_BOM_Procurement.xlsx`) synced to v31 (qty/funding/notes cells only — merges/dims/formulas untouched, row-insert avoided per v15 lesson).
- **Not addressed this session:** the uploaded `SPARK_Component_Order_Form_2.xlsx` draft (18650/TP4056/AMS1117/INA219/microSD/TPU enclosure/separate Velcro strap line) contains dead RPi-era parts and conflicts with locked §2.2/§2.6 specs (PLA not TPU, no separate strap line, single arm sleeve SKU). Not reconciled into the tracker — flagged as stale, not used as a source for this update.

**v30 change log (August 6, 2026 — closure mechanism locked + arm sleeve base layer):**

- **Closure mechanism: hook-and-loop Velcro, locked.** Extends Action #34 (top-of-wrist placement) rather than opening a new action — same enclosure decision thread. Rationale: target population is healthy independent elderly (proposal's stated use case); Velcro requires no fine motor control/grip strength to fasten (vs. belt-buckle), supports one-handed daily self-application, and tolerates day-to-day wrist swelling variance. Skin-contact concern is moot — arm sleeve base layer (below) sits between Velcro and skin.
- **Arm sleeve (base layer) added to BOM, NPR 136 (Action #34).** Compression arm sleeve worn under the wrist enclosure, per the enclosure concept-image spec. Sourced: Daraz, "BLUE BELL Let's Slim" 1-pair arm sleeve, thumb-hole, stretchable, light blue — Rs. 136 (list Rs. 200, -32%), +Rs. 100 standard delivery, Kathmandu Metro, guaranteed 10–11 Aug. Note: this is a distinct SKU/purpose from the dead RPi-era "chest_strap"/"velcro_strap" legacy assets (v28 flagged those as dead) — this is the base garment layer, not a mounting strap.
- **§2.2/§2.6 updated; BOM xlsx synced** — new row inserted into Wearable Node section (row 9), all downstream formulas and merge ranges rebuilt manually (row-insert formula-drift failure mode from prior session avoided).
- **Repo hygiene regression fixed:** `c1a2392` ("remove stray Excel lock file") only added the `.gitignore` pattern — `docs/~$SPARK_BOM_Procurement.xlsx` was never actually `git rm`'d and remained tracked. Removed this commit.

**v29 change log (August 6, 2026 — enclosure electronics placement locked):**

- **Electronics placement: top-of-wrist (dorsal side), locked (Action #34, new).** Fixes MPU6050 mounting orientation reference for Layer 1 threshold calibration (Action #7). No BOM/cost impact.
- **Stale "locked v27" labels in §2.2 corrected to v28** (battery, enclosure form-factor lines — same gap v28's own changelog claimed was fixed in §2.6 but was never applied to §2.2).

**v28 change log (August 6, 2026 — three open BOM decisions locked + bring-up hardware added):**

- **Battery: 1000 mAh Li-ion/LiPo, locked.** Uses R-05's existing endurance assumption (~5 mA @ 200 Hz → 8–10 hr) as the spec rather than a new estimate. Sourcing still TBD (unpriced).
- **Enclosure form factor: wrist-worn, locked (Action #8 resolved).** Fabrication method switched PLA→TPU v34 (real KEC Makerspace stock only carries TPU); wear location was the last open piece and directly gates Layer 1 threshold calibration (Action #7, §2.5).
- **BLE modality: dongle required, locked.** Gateway is phone-app-involved (not laptop-only), so built-in-BLE-only is ruled out; a BLE dongle is now the confirmed line, not an either/or.
- **BOM xlsx synced to the three locks** (commit `e76616a`) — cell-only edits, merges/dims/formulas untouched.
- **Bring-up hardware added (Actions #32/#33, new):** current locked design (§2.2, ESP32-S3-only) had zero BOM coverage for the physical MPU6050↔ESP32-S3 wired link or Li-ion/LiPo charge protection — both genuinely required, not legacy RPi-era noise. Added as 2 new BOM line items:
  - Charge/protection circuit (TP4056-class), 1 unit — required unless the sourced battery is a protected pack (Action #32)
  - Bring-up consumables — breadboard + jumper wires (2 sets), resistor/capacitor assortment (1 lot) (Action #33)
  - Pricing sourced from the legacy RPi-era proposal cost table (`docs/SPARK_Proposal/main.md`) as a cost baseline only — component selection is new-design bring-up, not a revival of dropped RPi parts (AMS1117, INA219, 18650 cell, microSD, chest/velcro strap remain dead, not re-added).
- **§2.6 "locked v27" labels corrected to v28** (battery/enclosure/BLE lock actually landed this version, not v27).

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

1. **Wearable node:** ESP32-S3 (3 units, all departmental-ordered — Action #16 spare added, self-funding dropped)
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
   - 🟢 Spare-board buffer added to BOM v31 (Action #16 BOM-resolved, order pending); 🟡 board physical footprint unconfirmed vs. §7 assumption, low-priority (Action #17)
   - 🟡 Purchase/inventory status (3 × ESP32-S3 + MPU6050, all now departmental-ordered) discussed but not confirmed (Action #18)

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
   - Resolved: #2, #3 (quantization/export v49), #4, #11, #12, #14, #15 (v22), legacy #6 (v22, repo created)
   - Still open: #5, #33 (see §1 below)

6. **Priority tiers (v16, re-scoped v19, Tier 1 resolved v20)**
   - 🟢 37 action items logged total (#1–37)
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

**39 action items logged total. Ordered by item number (not priority tier); newest addition (#39) placed at top per convention, remaining items retain original recency ordering.**

1. **#39 — Fasteners: M2.5 self-tapping, ×8mm, sourced Daraz Nepal — spec relaxed from A2 stainless/button-head (v42→v45)**
   - **Item:** No fastener/screw line existed anywhere in the BOM (neither the deleted `SPARK_BOM_Procurement.xlsx` nor the canonical `SPARK_Component_Order_Form.xlsx`) despite the PCB mount (Action #34, locked v29) and Velcro-closure shell (locked v30) both implying mechanical fastening points.
   - **v42–v44 history:** Added (v42), spec locked to A2 stainless/flanged button head/×6mm+×10mm mixed lengths (v43) on corrosion/skin-safety and TPU-clamp reasoning, vendor-searched with no confirmed local match (v44) — one Daraz Nepal listing found but didn't confirm stainless or button head, and lacked the ×10mm length.
   - **v45 — spec relaxed to match what's actually available in Nepal.** Minimum requirements re-derived: M2.5 thread (fixed), self-tapping (fixed, no insert equipment on hand), length within wall/boss thickness (unverified either way pending CAD — Action #17 blocker, not vendor-dependent), not countersunk (fixed, tolerance risk). Material (stainless) and head type (button/flanged) were downgraded from requirements to preferences — the corrosion/dermatitis reasoning was precautionary for a skin-contact scenario never confirmed to actually exist, and head shape isn't load-bearing at this torque/application. Countersunk remains excluded.
   - **Decision:** Daraz Nepal (`daraz.com.np`) M2/M2.5/M3 machine screw assortment kit adopted as sourced vendor — real, live, local-delivery listing (confirmed available in Nepal, unlike Ubuy which is cross-border resale and was set aside for that reason, consistent with how other BOM lines already treat Ubuy). **Length unified to ×8mm for both PCB mount and shell-join** (was ×6mm/×10mm split) — kit's max size is M2.5×8mm; shorter is also lower-risk against bottoming through an unverified wall thickness, so this is a safety-neutral-to-positive simplification, not just an availability compromise.
   - **Material/head, downgraded:** generic "metal" per listing, stainless not confirmed; head type not stated as button head. Logged as a known spec downgrade, not silently accepted — if wall-thickness verification later shows real skin contact, this line should be revisited.
   - **Cost:** kit's actual per-unit/kit price not confirmed on the listing page. NPR 300 placeholder (NPR 15/unit × 20) retained pending real price.
   - **Status:** Vendor resolved. Open: actual kit price, and the wall/boss-thickness safety check (blocked on Action #17 CAD).
   - **Alternate candidate seen, not adopted (v46):** a `daraz.com.np/tag/self-tapping-screws/` category listing shows sizes including M2.5×6mm/×8mm — real size match — but its own title reads "Flat Countersunk...Pan Head," a self-contradictory head-shape claim (countersunk and pan are mutually exclusive geometries). Head shape unconfirmed without opening the live listing; material also unstated. Logged as generic/unverified — not swapped in over the resolved Daraz kit above.
   - **Second alternate seen, rejected (v47):** Himalayan Solution (existing BOM vendor, TP4056/breadboard/R-C lines) — "500PCS M2 M2.5 M3 KM Screw Flat Head Phillips," Rs.1,200, includes M2.5. **Rejected on two independent grounds:** (1) confirmed **out of stock**, "0 available," not currently purchasable; (2) product photos confirm **flat/countersunk head** — same excluded geometry as the v43 countersunk rejection, disqualifying even if stock existed.
   - **International-availability check, closed (v48):** Google Images search for the original v43 spec (A2 stainless, flanged button head, self-tapping, M2.5) returns real, in-stock matches — but exclusively from UK/international sellers (eBay UK, Westfield Fasteners, Nuts of Chorley, TIMCO, Amazon UK, RC4WD, Fusion Fixings), none Nepal-based. Confirms the original spec is a real, buyable part — just not locally, same category gap already established for Ubuy. No new local candidate; search loop closed, v45 kit remains sourced.

2. **#38 — Charging interface: dual single-purpose USB-C ports, off-body access only (NEW v41)**
   - **Item:** Enclosure houses ESP32-S3, MPU6050, LiPo, TP4056, and internal wiring only — no charging-interface design existed prior to this decision. Two architectures considered: single combined USB-C port (phone-style, data+charge muxed) vs two separate single-purpose ports (ESP32-S3 native USB-C for programming/data, TP4056's own USB-C for charge input). Combined-port option rejected — TP4056 has no data lines (charge-only IC), so true 2-in-1 would need an added USB hub/mux PCB not currently in scope or BOM.
   - **Decision:** Two ports, each single-purpose. Plausibly explains existing row 12 "USB-C ×3" BOM count (1 ESP32-S3 programming port + 1 TP4056 charge port + 1 spare, matching the Action #16 spare-buffer pattern) — not previously stated anywhere in the tracker, inferred this session.
   - **Governing constraint:** Device confirmed never worn while charging (user-stated). This decouples the charge port from the sealed-enclosure water-ingress concern raised in this session's (unlogged) thermal/venting discussion — charge port can sit behind an occasional-access panel/gasketed cap rather than a daily-sealed cutout, since it's never exposed to sweat/motion during actual use.
   - **Status:** Open. Two sub-gaps remain: (1) TP4056 module's actual connector type (USB-C vs Micro-USB) unconfirmed — no listing/datasheet sourced for the specific unit under row 8, same gap Action #32 already carried; (2) single shared access-panel vs two separate cutouts is a CAD decision, blocked on Action #17 (no enclosure model exists yet). Row 12's "×3" purpose is inferred from this decision, not independently confirmed by Aaradhya — flagged, not asserted as fact.
   - **Owner:** Aaradhya
   - **Cost impact:** None — no BOM line changed, existing row 12 quantity already covers this reading.

2. **#37 — Enclosure material sourcing: switched to bulk 1kg TPU roll purchase (NEW v39)**
   - **Item:** Action #36's NPR 90 figure assumed KEC Makerspace's per-part print-service model (they supply filament, charge NPR 4/g of material used per print). Aaradhya opted instead to buy a 1kg TPU roll outright at the same NPR 4/g rate, owning the filament rather than paying per-print.
   - **Cost:** 1000g × NPR 4/g = **NPR 4,000** (replaces the NPR 90 per-part line). Only ~22g is needed for one enclosure per Action #36's estimate — the rest of the roll is spare capacity for future prints/iterations, not consumed by this BOM line alone.
   - **Status:** Open — roll vendor not yet sourced to a live listing (Order Form lists "KEC Makerspace / vendor TBD"). Confirm actual source before ordering. §2.6 and Order Form updated. BOM total revised **NPR 9,667 → NPR 13,577** (+NPR 3,910).
   - **Owner:** Aaradhya
   - **Note:** This is a genuine cost jump (roll is ~44x the per-part estimate) for what's still only a 22g part need — worth flagging to the team/department before ordering, since NPR 4,000 is now the single largest non-ESP32-S3 line on the BOM.

2. **#36 — Enclosure cost: geometric estimate from real forearm measurement (v38)**
   - **Item:** Action #35 (below) left enclosure cost genuinely blocked — no CAD model existed to slice. Aaradhya provided real forearm measurements (12cm C-shaped band arc length, 16cm reference circumference, ~4cm tentative height, open end under forearm closed by Velcro strap) matching the `enclosure_concept_v1_two_zone_bracer.png` render's stated 75% wrap / 25–30% open-seam geometry — an independent cross-check that passed (12/16 = 75% exactly).
   - **Calculation:** Two-zone volume computed from the 270° arc (75% of 360°), split across wrist zone (slim, sensor-only, 3cm), spine (wiring bridge, 3cm), and forearm zone (wider/thicker electronics bay, 6cm) per the render's real component footprints logged in `CAD_PRACTICE_PART_WALKTHROUGH.md`/`DESIGN_IDEAS.md` (ESP32-S3 25×50×7mm, 1000mAh LiPo 32×52×7mm, TP4056 15×17×2mm). Wall thickness 2mm per the DI-01 spec already logged in `CAD_SOFTWARE_GUIDE.md`. TPU 95A density 1.21 g/cm³.
   - **Result:** ~18.5 cm³ → ~22g → **~NPR 90** (was NPR 160). BOM total revised NPR 9,737 → **NPR 9,667** (−NPR 70). §2.6 and Order Form updated. **Superseded v39 by Action #37** — sourcing model changed from per-part print-service to bulk roll purchase, see below.
   - **Caveat — still not Action #17's resolution:** this is a hand-computed estimate from stated dimensions, not a CAD model or slicer output. No `.f3d`/`.step`/`.stl` file exists in the repo. Real slice still needed once the model is built; treat NPR 90 as a better-grounded placeholder, not a locked figure.
   - **Owner:** Aaradhya
   - **Status:** Open (placeholder improved, Action #17 itself unresolved).

2. **#35 — Finalize BOM v35→v38 open items pass (v38)**
   - **Item:** Reviewed 4 flagged open items from BOM v35 lock: (a) Velcro strap design decision, (b) enclosure cost real slicer figure, (c) battery-draw endurance figure in risk matrix, (d) phone display-client owner.
   - **Findings:** (a) already resolved — Action #34 (v30) locked top-of-wrist Velcro closure; no separate open decision exists. (b) blocked at the time — NPR 160 was a 40g eyeball estimate with no basis shown; no CAD model existed to slice, and Action #17 (WROOM-1-CAM FPC footprint check) was an open prerequisite. **Superseded same-session by Action #36** (real measurement provided, better estimate computed — still not a full resolution, see #36's caveat). (c) already resolved — Action #21 (v36) replaced the broken 5 mA figure with the reconciling 110–140 mA estimate. (d) resolved this pass — owner assigned, see §3.
   - **Owner:** Aaradhya
   - **Status:** 2 of 4 confirmed already-resolved (stale items in the v35 recollection), 1 newly resolved (owner assignment), 1 improved but not closed (enclosure — see Action #36).

3. **#34 — Electronics placement + closure mechanism locked: top-of-wrist, Velcro (UPDATED v30)**
   - **Item:** Enclosure electronics housing confirmed at top-of-wrist (dorsal side), not underside/palm-side. Fixes MPU6050 orientation reference for Layer 1 threshold calibration (Action #7) and rules out volar-side mounting.
   - **v30 addition — closure mechanism:** Hook-and-loop Velcro (not belt-buckle). Elderly-dexterity rationale: target population (healthy independent elderly, per proposal scope) needs one-handed, no-fine-motor-control fastening; Velcro tolerates daily wrist-swelling variance and doesn't require threading/pulling tension like a buckle. Skin protection is handled by the arm sleeve base layer (new BOM row, Action #34), not by the closure choice.
   - **v30 addition — arm sleeve base layer:** Compression arm sleeve (thumb-hole, stretchable) worn under the enclosure. Added to BOM at NPR 136 (Daraz, "BLUE BELL Let's Slim").
   - **Owner:** Aaradhya
   - **Status:** Locked v29 (placement) + v30 (closure, base layer). §2.2/§2.6 updated. BOM cost impact: +NPR 136 (v30, arm sleeve only — placement/closure choice itself has no cost).

2. **#32 — Source battery charge/protection circuit [RESOLVED v40]**
   - **Item:** MPU6050→ESP32-S3 needs a physical wired link (breadboard-level, bring-up phase) and a raw 1000 mAh Li-ion/LiPo cell needs charge/overcharge/over-discharge protection (TP4056-class module) unless the sourced battery is already a protected pack. Neither was present in the ESP32-S3-era BOM (§2.6 had only 7 rows).
   - **Owner:** Aaradhya
   - **Status:** **Resolved v40.** Giga Nepal's product listing/spec sheet for the sourced 1100mAh cell (v34) lists JST 2-pin connector, voltage, capacity, style — no BMS/PCM/protection-circuit line item, and description text ("safe and efficient power delivery," "durable outer casing") is generic pouch-casing language, not a protection claim vendors normally state explicitly when present. Confirmed raw/unprotected cell. TP4056 line (row 8) required, stays in BOM at NPR 90.

3. **#33 — Bring-up consumables not yet in BOM (NEW v28)**
   - **Item:** Breadboard + jumper wires and a resistor/capacitor assortment are needed for wearable-node bring-up/prototyping but were never priced against the current ESP32-S3 design (only existed in the dead RPi-era cost table).
   - **Owner:** Aaradhya
   - **Status:** Open. BOM rows added v28 under new "Bring-up/Assembly" section, baseline pricing from legacy table (breadboard+jumper NPR 325/set × 2 = 650; resistor/capacitor NPR 600/lot).

4. **#25 — Confirm defence outcome [RESOLVED v20]**
   - **Item:** Confirm what actually happened at the July 9 defence — did it occur as scheduled, was the ESP32-S3/laptop pivot explained if a panel member asked, any feedback given
   - **Owner:** Aaradhya
   - **Status:** **Resolved July 10 (v20).** Defence occurred as scheduled July 9. Outcome: panel was optimistic about the project. No specific questions reported about the ESP32-S3/laptop pivot despite the gap between v35's paper submission and the actual as-built design. Whether the verbal rehearsal itself happened is not independently confirmed, but the risk it was meant to cover didn't surface as an issue. Follow-on item opened as new **Action #31**.

5. **#26 — Narrow novelty Claims 1/3 wording (Tier 3, urgent despite v18 labeling)**
   - **Item:** Prior-art search (v18) found 2024–2025 papers on multi-stage CNNs, gated ensembles, and SHAP for fall detection. Current proposal wording needs narrowing to "MCU+local-gateway" specifically, not broader "no existing system" framing, before a panel member finds the same papers.
   - **Owner:** Aaradhya (decision + thesis wording)
   - **Status:** Open. General web search done (v18); formal IEEE Xplore/Scopus query still needed before thesis chapter finalized. Recommendation: narrow Claims 1 and 3 before defence if revising, or before thesis submission (Action #26 stays open).

6. **#27 — Gateway NPU/iGPU capability assessment (Future Work, laptop-specific)**
   - **Item:** Laptop (Acer Swift Go 16, Intel Core Ultra 7 155H) has on-die NPU (11 TOPS INT8) and iGPU (18 TOPS INT8) that RPi 4B structurally never had. Assess feasibility for gateway-side accelerated inference or real-time feature extraction.
   - **Owner:** TBD
   - **Status:** Open (Ch.6). Added v18 as a laptop-enabled opportunity post-RPi drop.

7. **#28 — Camera-based confirmation modality (Future Work, vision-based 2nd opinion)**
   - **Item:** Explore vision-based fall confirmation (e.g., optical flow, pose estimation) as a second-opinion check, contingent on #27's NPU/iGPU availability.
   - **Owner:** TBD
   - **Status:** Open (Ch.6). Added v18; cross-linked to #27 (v19) since modality requires compute #27 enables.

8. **#29 — Cloud archival integration (Future Work)**
   - **Item:** Optional cloud cold-storage sync for long-term patient records (complements local JSON + PDF).
   - **Owner:** TBD
   - **Status:** Open (Ch.6). Added v18.

9. **#30 — Wearable duty cycle optimization (Future Work)**
   - **Item:** Battery-management firmware to optimize sensor polling / wake intervals based on activity phase (e.g., idle vs. walking vs. fall-recovery).
   - **Owner:** TBD
   - **Status:** Open (Ch.6). Added v18.

10. **#24 — MPU6050 firmware reuse vs. rewrite (Tier 3, promoted from legacy)**

- **Item:** Decide whether to reuse the existing MPU6050 driver from FallGuard (legacy project) or rewrite from scratch. Affects code review, testing, and confidence in the sensor integration.
- **Owner:** Rupesh + Aaradhya
- **Status:** Open. HOD discussion planned alongside #23 (dataset protocol); not yet confirmed.

1. **#23 — Dataset protocol finalization (Tier 3, promoted from legacy)**

- **Item:** Define fall types, ADL types, subject count, and recording procedure for the self-collected dataset to complement SisFall.
- **Owner:** Aaradhya
- **Status:** Open. HOD discussion held (v22); confirmation from department still pending. Volunteer recruiting/scheduling lead time is real despite September gate label.

1. **#22 — R-04 risk matrix update (Tier 4)**

- **Item:** Risk R-04 (external interference in sensor signal) lists a mitigation claim ("isolated data collection environment") that is not sourced to any Action or design decision. Patch the risk row with a cross-reference or reword the claim.
- **Owner:** Aaradhya
- **Status:** Open. Flagged v16; no action yet.

1. **#21 — R-05 risk matrix update (Tier 4) [RESOLVED v36]**
   - **Item:** Risk R-05 (battery drain from continuous polling) cited a stale/broken draw figure — "~5 mA @ 200 Hz → 8–10hr on 1000 mAh" does not reconcile (1000 mAh ÷ 5 mA = 200 hr, not 8–10 hr). Update the claim to match current design.
   - **Owner:** Aaradhya
   - **Status:** **Resolved v36.** Replaced the broken 5 mA figure with an estimated ESP32-S3 active-draw range (~110–140 mA, BLE + 200 Hz IMU polling) that actually reconciles against the sourced 1100 mAh LiPo (v34) at the claimed 8–10hr endurance (1100 ÷ 110–140 ≈ 7.9–10 hr). Explicitly flagged as an estimate — no INA219/power-telemetry hardware exists in this design (that module is dead, RPi-era) to measure it directly. Real profiling still needs firmware (Action #24) to exist first.

2. **#20 — Mobile hotspot max-client cap (Tier 5, low priority)**
   - **Item:** Measure the maximum number of simultaneous client connections supported by the mobile hotspot device(s) used for demo-day gateway uptime. Assumption updated v35: n=3 (wearable BLE to laptop + laptop's own hotspot/network link + phone display client pulling from laptop) — was n=2 pre-phone-display-client. Real cap might be lower; if lower, affects single-device hotspot viability.
   - **Owner:** TBD
   - **Status:** Open. Flagged v15, assumption revised v35 (phone display client added). Still low priority since n=3 is well within typical caps (usually 10+).

3. **#19 — Log USB-C cable price (Tier 2) [RESOLVED v33]**
   - **Item:** USB-C cable for ESP32-S3 gateway connection is departmental-ordered (v31 — no longer self-funded); price was never recorded. Log the amount once purchased.
   - **Owner:** Aaradhya
   - **Status:** Resolved v33. Daraz, qty 3 @ NPR 267 = NPR 801.

4. **#18 — Confirm receipt of departmental-ordered items (Tier 2) [MPU6050 SOURCED v33, ESP32-S3 ORDER STILL PENDING]**
   - **Item:** Confirm: (a) 3 × ESP32-S3, all departmental-ordered (v31, Himalayan v32) — has the order been placed/received?; (b) MPU6050 — vendor/price sourced v33.
   - **Owner:** Aaradhya
   - **Status:** (b) resolved v33 — Himalayan Solutions, NPR 350, GY-251 module. (a) still open — order placement not yet confirmed.

5. **#17 — Board physical footprint vs. enclosure (Tier 5)**
   - **Item:** Himalayan's ESP32-S3 board (vendor reverted v32) is a WROOM-1-**CAM** variant with an onboard camera FPC connector (unused by SPARK). Enclosure design (still not started, v23) needs to account for this footprint. Check compatibility once board is in hand.
   - **Owner:** Sankalpa + Aaradhya
   - **Status:** Open. Low priority (Tier 5); enclosure work hasn't started yet (v23).

6. **#16 — Confirm/order spare ESP32-S3 board (Tier 2) [BOM RESOLVED v31, ORDER PENDING]**
   - **Item:** Quantity was reduced to 2 units (no RPi backup). Zero spare board exists for firmware bring-up risk. Add 1 unit at next order to reintroduce a buffer.
   - **Owner:** Rupesh + Aaradhya
   - **Status:** Spare unit added to BOM v31 (3 × ESP32-S3, all departmental-ordered). Actual order placement not yet confirmed — bundle with #18/#19.

7. **#15 — Gateway procedural uptime mitigation (Tier 4) [PARTIALLY RESOLVED v22]**
   - **Item:** Confirm that laptop gateway uptime is guarded by an actual procedure (e.g., plugged in at demo, hotspot ready, restart scripts staged). Both compute and power halves need documentation.
   - **Owner:** Aaradhya
   - **Status:** Compute half resolved (v15 compared laptop vs. RPi 4B, confirmed laptop is sufficient; no longer a technical risk). Procedural half confirmed executed (v22, same-day as defence prep). Formalization still pending — lock the procedure as documented practice, not stated intent. Tier 4.

8. **#14 — ESP32-S3 vendor/pricing (Tier 2) [REOPENED v32, RE-RESOLVED v32]**
   - **Item:** Himalayan went out of stock same day v12 locked them as "confirmed." RoboNepal (existing SPARK vendor for RPi) carries the same module.
   - **Status (v32, current):** Himalayan confirmed back in stock — live listing, "ESP32-S3 WROOM CAM Development Board with Port for camera OV2640," WROOM-1-CAM/N16R8 module, dual USB-C, BOOT/RST buttons, matching spec. **NPR 1,800/unit, 152 available.** Undercuts RoboNepal's NPR 1,979/unit. **Vendor reverted to Himalayan.** BOM delta: 3 × NPR 1,979 = NPR 5,937 → 3 × NPR 1,800 = NPR 5,400, **−NPR 537**.
   - **Owner:** Aaradhya
   - **Status:** **Resolved v13.** RoboNepal confirmed: NPR 1,979/unit, 5 in stock. Board legitimacy checked (dual USB-C, BOOT/RST buttons, 16MB flash/8MB PSRAM/dual-core LX7 all match spec). **BOM delta:** 2 × NPR 1,979 = NPR 3,958 (was 2 × 1,800 = NPR 3,600) — **+NPR 358, no longer net-zero**. New BOM total: ~NPR 15,004 (was 14,646). Board variant is WROOM-1-CAM (has unused camera FPC) — different footprint than plain N16R8; see Action #17 (low-priority, enclosure not started).

9. **#13 — Self-funding disclosure (Tier 2) [RESOLVED v13]**
   - **Item:** Confirm whether one of the two ESP32-S3 units has been self-funded as a staged plan (1 now for quantization testing, 2nd before Sept 2026 gate).
   - **Owner:** Aaradhya
   - **Status:** **Resolved v13.** Self-funded arrangement confirmed: 1 × ESP32-S3 (NPR 1,979) self-funded by Aaradhya for immediate quantization work. Departmental ask reduced from 2 units to 1 unit, saving NPR 1,979. Also added USB-C cable as self-funded unpriced item. No change to absolute BOM (still ~NPR 15,004), but departmental request is now lower.

10. **#12 — MPU6050 sourcing (Tier 2) [RESOLVED v13]**
    - **Item:** Is MPU6050 already in the lab, ready to borrow, or does it need ordering?
    - **Owner:** Rupesh + Aaradhya
    - **Status:** **Resolved v13.** Lab-borrow plan confirmed (no purchase needed). Not tracking separately as a line-item cost.

11. **#11 — Enclosure form factor (Tier 2) [RESOLVED v13 — 3D-printed PLA]**
    - **Item:** Decide on form factor (wrist-worn vs. chest-worn vs. belt-clip) and manufacturing method.
    - **Owner:** Sankalpa
    - **Status:** **Resolved v13.** Enclosure method: 3D-printed PLA (in-house on KEC Makerspace equipment). Form factor still TBD; see Action #8 below (legacy, unresolved).

12. **#10 — Weekly gate system for 8th semester (Tier 2)**
    - **Item:** Establish a weekly check-in cadence for 8th-semester progress tracking, complementing the monthly gates already in §4 (Timeline).
    - **Owner:** Aaradhya + HOD (Er. Suramya Sharma Dahal)
    - **Status:** Unverified. §4 has monthly gates; whether a _weekly_ cadence was separately set up is not recorded. Assume monthly gates as the current standard until confirmed.

13. **#9 — RPi power supply (Tier 5) [LEGACY — no longer applicable, RPi dropped v12]**
    - **Item:** Confirm team RPi 4B PSU is available or budget NPR 300–500.
    - **Owner:** Sankalpa
    - **Status:** **Not applicable (v12).** RPi 4B dropped from the BOM entirely; no PSU needed.

14. **#8 — Enclosure form factor decision (Tier 5) [RESOLVED v27 — wrist-worn]**
    - **Item:** Wrist-worn vs. chest-worn vs. belt-clip (affects Layer 1 threshold calibration).
    - **Owner:** Sankalpa + Rupesh
    - **Status:** **Resolved v27 — wrist-worn.** Fabrication method (3D-printed PLA, Action #11) and wear location now both locked. Empirical Layer 1 threshold tuning (Action #7) can proceed against a fixed wrist-mount geometry once WP 1.0/2.0 fall-sim data exists.

15. **#7 — Sensitivity threshold calibration (Tier 5) [LEGACY — still open]**
    - **Item:** Layer 1 |\mathbf{a}| and Δt values need empirical tuning from real fall simulations. Current design specifies fixed thresholds (2.5g / 300ms); whether empirical tuning has happened is not recorded.
    - **Owner:** Rupesh + Aaradhya
    - **Status:** Unverified. §2.2 (architecture) and §7 (appendix, 1D CNN internals) still state design values as fixed; no confirmation of empirical tuning from real fall data. Gates WP 1.0/2.0.

16. **#6 — SPARK GitHub repo + README + team access (Tier 5) [RESOLVED v22 — repo created]**
    - **Item:** Create a GitHub repo with README, .gitignore, folder scaffold, and team collaborator access (Rupesh, Sankalpa, Sonia).
    - **Owner:** Aaradhya
    - **Status:** **Resolved v22.** Repo created at `github.com/Aaradhya-Dev-Tamrakar/SPARK` — README, .gitignore, sync.ps1, and scaffold folders (firmware/training/gateway/data) in place. Team access (Rupesh, Sankalpa, Sonia as collaborators) not independently confirmed here — same non-assuming standard as the rest of this tracker; repo _existing_ is resolved, collaborator access is a separate, unconfirmed sub-item (minor).

17. **#5 — Self-collected dataset protocol (Tier 3) [PROMOTED to Action #23]**
    - **Item:** Define fall types, ADL types, subject count, recording procedure.
    - **Owner:** Aaradhya
    - **Status:** **Promoted v16 → Action #23 (Tier 3).** HOD discussion held (v22); confirmation pending.

18. **#4 — Review SPARK's formal novelty claims (Tier 2) [RESOLVED v22 — acronym confirmed]**
    - **Item:** Confirm the five novelty claims (§2.3 of proposal) are accurately cross-referenced in the tracker and any updates to wording are reflected in both places.
    - **Owner:** Aaradhya
    - **Status:** **Resolved v22.** Full acronym expansion ("Signal Pattern Analysis & Real-time Kinetics") confirmed and recorded for the first time since the June 30 FallGuard→SPARK rename. No conflicts between §2.3 and this tracker. Action #26 (v18) identified prior art needing narrowing; that's a separate decision, not a cross-reference mismatch.

19. **#3 — Quantization & deployment pipeline (Tier 2) [RESOLVED v49 — Quantization & C Export]**
    - **Item:** Define the end-to-end flow from training notebooks → quantization → TFLite export → ESP32-S3 deployment. Staging posts: Colab training, Colab quantization, local testing on laptop, device testing on ESP32-S3.
    - **Owner:** Aaradhya + Rupesh
    - **Status:** **Resolved v49 (Quantization & Export side).** `training/quantize_model.py` implemented and verified (13/13 unit tests in `tests/test_quantize_model.py`). Implements INT8 post-training quantization with 200-sample representative calibration dataset per proposal §5, outputs `spark_cnn_int8.tflite` (<120 KB flash limit check), generates C byte array header (`spark_cnn_int8.h`) with optional `--firmware-out` flag to drop directly into `firmware/main/models/`, and generates FP32 vs INT8 metrics comparison report. Firmware-side runtime integration remains in Rupesh's firmware scope.

20. **#2 — Enclosure design finalization (Tier 2) [RESOLVED v13 — method only]**
    - **Item:** Decide enclosure manufacturing method (custom PCB vs. 3D print vs. off-the-shelf box).
    - **Owner:** Sankalpa
    - **Status:** **Resolved v13** (method only). Manufacturing: 3D-printed PLA on KEC Makerspace equipment. **Form factor still TBD** (Action #8, legacy, still open).

21. **#1 — MCU selection (Tier 1) [RESOLVED v8 → ESP32-S3 (v12 re-confirmed)]**
    - **Item:** Choose between ESP32 DevKit V1, ESP32-S3, or ARM Cortex-M for the wearable node.
    - **Owner:** Aaradhya + Rupesh
    - **Status:** **Resolved v8 → ESP32-S3** (supersedes original DevKit V1 choice). **Re-confirmed v12** after vendor disruption (Himalayan → RoboNepal). Board legitimacy checked, 2 units confirmed at NPR 1,979/unit. Spare buffer re-added as Action #16 (open).

22. **#31 — Department negotiation over new component costs (NEW v20, not yet tiered)**
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
   - Laptop (Acer Swift Go 16) as the **sole BLE gateway and sole pipeline compute** (locked v35 — reverts the interim "either/or, phone-or-laptop" framing floated v28); procedure-based uptime mitigation (hotspot, staging scripts)

3. **Layer 3 (Phone display client, NEW v35):** Read-only results viewer
   - No direct BLE link to the wearable — pulls/receives report data from the laptop (local network) after Layer 2 finishes
   - No SHAP computation, no PDF generation on-device — display only
   - Purpose: lets caregiver/patient view a completed report without the laptop physically present

**Operational scope:** Fall detection for elderly care, primary use case Singapore/Nepal-context testing (SisFall-like data collection with local validation).

### §2.2 — Wearable Hardware

**Bill of Materials (as of v31, Aug 10, 2026):**

1. **Microcontroller:** 3 × ESP32-S3 (Himalayan, NPR 1,800/unit confirmed v32 — reverted from RoboNepal, Action #14 reopened)
   - Quantization testbed: 1 unit (departmental-ordered, v31)
   - Deployment wearable: 1 unit (departmental ask)
   - Spare: 1 unit (departmental-ordered, v31 — Action #16 resolved)
   - Firmware: Arduino/ESP-IDF, same baseline as FallGuard legacy project

2. **Inertial Measurement Unit:** 1 × MPU6050 (departmental-ordered, v31; **sourced v33 — Himalayan Solutions, NPR 350, GY-251 module, live listing**)
   - 200 Hz, 3-axis accelerometer
   - Driver: reuse/rewrite TBD with Rupesh (Action #24)

3. **Power:**
   - Lithium battery: 1100 mAh Li-ion/LiPo (sourced v34 — Giga Nepal, NPR 550; sourcing resolved. Endurance figure fixed v36 — Action #21 resolved, see §2.7)
   - USB-C charging connector (included on ESP32-S3 devboard)
   - USB-C cable (departmental-ordered, v31; **priced v33 — Daraz, qty 3 @ NPR 267 = NPR 801, Action #19 resolved**)

4. **Enclosure:**
   - Form factor: Wrist-worn (locked v28, Action #8)
   - Electronics placement: Top-of-wrist / dorsal side (locked v29, Action #34) — consistent MPU6050 orientation, clear of wrist flexion crease
   - Closure mechanism: Hook-and-loop Velcro (locked v30, Action #34) — elderly-dexterity rationale, one-handed fastening. **Resolved v36:** confirmed as a distinct, separately-purchased component — the enclosure has its own built-in Velcro closure tab (no separate purchase, part of the 3D-printed shell), and the BOM's "Velcro wrist strap" line (RR-papers, NPR 500×2) is a second, physically separate strap used for additional wearable retention/security, not a duplicate of the closure tab. §2.6 line description updated to reflect this distinction.
   - Base layer: Compression arm sleeve, thumb-hole (locked v30, Action #34, departmental-ordered v31) — worn under enclosure, doubles as skin protection under Velcro
   - Material: 3D-printed TPU (KEC Makerspace, switched v34 — real KEC inventory only stocks TPU, not PLA; PLA lock v13 was never verified against actual makerspace stock)
   - Footprint: Himalayan board (vendor reverted v32) is WROOM-1-CAM variant (has unused camera FPC); unconfirmed vs. §7 assumption (Action #17)

**Total BOM (§2.6):** **NPR 13,577** (v39 — enclosure sourcing switched to 1kg TPU roll purchase, NPR 90→4,000, +NPR 3,910, over v38's NPR 9,667. Funding: all lines departmental-ordered, no self-funded/lab-borrowed split.)

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
   - 3 × ESP32-S3, Himalayan: 3 × NPR 1,800 = NPR 5,400 (Action #14 vendor reverted v32; Action #16 spare added v31; all departmental-ordered)
   - 1 × MPU6050, Himalayan: NPR 350 (sourced v33, GY-251 module, live listing — Action #18's MPU6050 half resolved)
   - 1 × Lithium battery, 1100 mAh Li-ion/LiPo: NPR 550 (sourced v34, Giga Nepal — sourcing resolved; Action #21's R-05 draw-figure issue fixed v36, see §2.7)
   - 1 × USB-C cable, departmental-ordered: qty 3 × NPR 267 = NPR 801 (sourced v33, Daraz — Action #19 resolved)
   - 1 × Charge/protection circuit (TP4056-class), required — sourced cell confirmed unprotected (Action #32 resolved v40): NPR 90 (baseline, legacy pricing)
   - 1 × Compression arm sleeve, base layer, thumb-hole (locked v30, Action #34, departmental-ordered v31): NPR 136 (Daraz, "BLUE BELL Let's Slim," -32% off Rs.200, +Rs.100 delivery not included in line price)
   - 1 × Velcro wrist strap, RR-papers, qty 2: 2 × NPR 500 = NPR 1,000 (re-added v33, **§2.2 conflict resolved v36** — confirmed distinct from the enclosure's own built-in Velcro closure tab; this strap provides additional wearable retention/security, separate purchase)
   - Enclosure, wrist-worn (locked v28), Velcro closure (locked v30), 3D-printed TPU (switched v34): material sourced as **1kg roll purchase, NPR 4,000** (v39, Action #37 — supersedes v38's per-part NPR 90 estimate; sourcing model changed from KEC print-service to owning the filament, same NPR 4/g rate; only ~22g needed per Action #36's geometric estimate, rest is spare)
   - Fasteners (v42, Action #39; spec relaxed + vendor sourced v45, see §1): M2.5 self-tapping, **×8mm** (unified from a ×6mm/×10mm split — shorter length is lower-risk against an unverified wall thickness), generic metal (stainless/button-head downgraded from requirement to preference — precautionary reasoning for a skin-contact scenario never confirmed to exist), sourced **Daraz Nepal** (`daraz.com.np`, live listing, confirmed local delivery — unlike cross-border resellers like Ubuy, set aside for that reason). Qty 20 — NPR 15/unit placeholder × 20 = **NPR 300** (real kit price not yet confirmed). Countersunk rejected — needs exact-matched conical seat or risks a proud sharp edge / cracked boss. Length-vs-wall-thickness still not verified against a real model (blocked on Action #17) — this is a hard floor independent of vendor choice.

2. **Gateway (laptop):**
   - Acer Swift Go 16 (already owned): NPR 0

3. **Phone display client (NEW v35):**
   - User's own phone (already owned, no purchase): NPR 0
   - Display-only, no BLE hardware needed — reads native phone BLE/network stack

4. **Miscellaneous:**
   - ~~BLE dongle~~ — **dropped v35.** Was locked v28 on flawed reasoning ("phone-app-involved rules out built-in-BLE-only") that didn't actually follow; every device in the real data path (ESP32-S3, laptop, phone) has native BLE, and the phone doesn't even need BLE since it's a display-only client reading from the laptop over local network, not a direct wearable BLE client. No dongle needed anywhere.
   - Development/test boards: Covered by above

5. **Bring-up/Assembly (NEW v28, Action #33):**
   - Breadboard + jumper wires, 2 sets: NPR 325/set × 2 = NPR 650 (baseline, legacy pricing)
   - Resistor/capacitor assortment, 1 lot: NPR 600 (baseline, legacy pricing)

**Total project cost:** **NPR 13,877** (v42 — fasteners added, NPR 0→300, over v39's NPR 13,577).

**Funding breakdown (v31 — all self-funded/lab-borrowed status dropped):**

- Departmental ask: **NPR 13,577** (full BOM total — all lines now departmental-ordered, no self-funded or lab-borrowed split)
- Self-funded by Aaradhya: **None** (v31 — previously 1 × ESP32-S3 + USB-C cable, now departmental)
- Lab-borrowed: **None** (v31 — previously MPU6050, now departmental-ordered)

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
   - **Probability:** Low (ESP32-S3 active draw with BLE + 200 Hz IMU polling estimated ~110–140 mA, not the previous ~5 mA figure — see Action #21 fix below; 1100 mAh sourced LiPo (v34) → ~8–9.5 hour endurance at this range)
   - **Mitigation:** Queue-based CNN triggering (only run CNN when Layer 1 threshold exceeded), sleep modes between windows
   - **Status:** Battery sourced v34 (1100 mAh LiPo, Giga Nepal, NPR 550). Draw figure corrected v36 (Action #21 resolved) — no INA219 power telemetry exists in this design to measure it directly (that module is RPi-era/dead, per v28); ~110–140 mA is an estimated range from published ESP32-S3 active Wi-Fi/BLE current draw, not a measured value. Endurance claim now internally consistent (1100 mAh ÷ 110–140 mA ≈ 7.9–10 hr) but still unverified against real hardware — flag as estimate, not measured spec, until Action #24 firmware exists to profile it.

---

## §3 — Team & Work Breakdown Structure

**Ordered list format (was table in v25). Primary team + roles + WBS items.**

1. **Aaradhya Dev Tamrakar (Supervisor: Er. Dipen Manandhar)**
   - **Role:** Project Lead, ML Training, SHAP Integration, Gateway, Reporting
   - **WBS items:**
     - WP 0: Proposal (completed)
     - WP 1: Literature review + dataset protocol (HOD discussion held, confirmation pending)
     - WP 2: Training pipeline (prepare_sisfall.py ✓; notebooks v24–v25 ✓; quantize_model.py ✓ v49; SHAP gateway ✓ v50)
     - WP 3: Integration testing (simulator + real falls, TBD); phone display-client implementation (owner assigned v38, Action tracker updated — read-only viewer against laptop's local-network report endpoint)
     - WP 4: Demo prep + thesis writing

2. **Rupesh Kadel (ID: 79034)**
   - **Role:** Firmware, Wearable Integration, Hardware Validation
   - **WBS items:**
     - WP 1: Layer 1 gated thresholding implementation
     - WP 2: CNN quantization + TFLite export (✓ export delivered v49, firmware runtime TBD), MPU6050 firmware (driver reuse/rewrite, Action #24)
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
- **v28:** Bring-up hardware added (Actions #32/#33: charge/protection circuit, breadboard+jumper wires, resistor/capacitor assortment)
- **v29:** Enclosure electronics placement locked top-of-wrist/dorsal (Action #34)
- **v30:** Closure mechanism locked (Velcro, extends Action #34); arm sleeve base layer added to BOM; repo hygiene fix (stray lock file)
- **v31 (this entry):** `dev_logs/design-assets/DESIGN_IDEAS.md` created — exploratory bracer-silhouette enclosure concept (DI-01) logged with two-zone internal layout (IMU/wrist zone + ESP32/battery/charge-circuit/forearm zone). Aesthetic/form exploration only, not adopted into locked design (§2) or BOM; cross-referenced against Action #8.
