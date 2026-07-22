# SPARK — Signal Pattern Analysis & Real-time Kinetics — Project Tracker (v22)

*Optimized for day-to-day use. Full history/rationale archive moved to §7 (Appendix) — read once, not needed for weekly tracking.*

**Last updated:** July 23, 2026 (v22 — full acronym expansion confirmed; Action #15 resolved; Action #23 status updated — HOD discussion held, confirmation pending; GitHub repo created, closing legacy item #6; v37 report reconciliation logged) · **Proposal submitted:** July 2 (v33, hardcopy) → resubmitted July 6 (v35, hardcopy) · **Proposal defence:** July 9, 2026 — **occurred as scheduled, panel optimistic** (Action #25 resolved v20) · **Mid-term defence:** July 13, 2026 — **status not confirmed this session, see §6.5** · **Demo/thesis boards:** March 2027

**v22 change log (July 23, 2026 — five items, all from Aaradhya directly this session; no BOM/design/scope-lock change):**

**(1) SPARK full-form confirmed.** "Signal Pattern Analysis & Real-time Kinetics." Not previously recorded anywhere in v1–v21 — the project was renamed from FallGuard on June 30, 2026 (per standing memory note) but the acronym itself was never expanded in this tracker until now. Title line above updated accordingly. No project fact changes as a result — purely a naming/documentation completion.

**(2) Action #15 resolved.** Gateway procedural mitigation (disable sleep/auto-lock, keep laptop plugged in, use as dedicated machine during demo window) confirmed as executed. This was the one open half of Action #15 — the compute half was already confirmed as a non-issue back in v15; the procedural half is now closed too. §2.7 R-06's sub-risk note and §0's status line both updated to reflect this below.

**(3) Action #23 — new development, not yet resolved.** Aaradhya has discussed dataset-protocol-related changes directly with the HOD. **Confirmation from HOD is still pending** — this is progress on the item, not closure. No specifics on what changes were discussed were given this session, so none are invented here, same non-assuming standard as this tracker's other entries. R-03's "paper-only" flag (§2.7) stays as-is until the protocol itself is actually finalized post-confirmation. Action #23's own table row (§1) updated to reflect this intermediate state rather than left at its v16 wording.

**(4) GitHub repo created — closes legacy item #6.** `https://github.com/Aaradhya-Dev-Tamrakar/SPARK` now exists with initial scaffold (`README.md`, `.gitignore`, `sync.ps1`, `firmware/`, `training/`, `gateway/`, `data/` placeholder folders). This resolves legacy item #6 ("SPARK/FallGuard GitHub repo + README + team access"), which had sat unpromoted/unverified in the §7 appendix since v1. No firmware or training code committed yet — repo currently holds scaffold only, consistent with Action #23 (dataset protocol) still being unresolved and no dataset/architecture decisions being finalized for code to target yet.

**(5) v37 proposal-report reconciliation logged, not a new submission.** Two Overleaf links were provided for what Aaradhya calls the "v37" report — **this is not a formally submitted version number**, and should not be read as superseding v35 (still the signed, submitted-of-record proposal per this tracker's existing footer) or v36 (still the only previously-logged unsubmitted digital revision, Gantt-chart-only). **Actual lineage, per Aaradhya directly:** the team's official submission was made by editing **v35** directly, not v36 — v36 (the intended edit target, containing the Gantt chart fix) was bypassed in that submission process. Separately, Aaradhya edited **v36** afterward to reveal a Gantt chart that had been present but commented out. "v37" is Aaradhya's own working label for **v35-as-submitted with v36's revealed Gantt-chart edit layered back in** — a reconciliation of two divergent edit paths, not a linear successor to v36. This distinction matters: a future reader seeing "v37" without this note would reasonably assume a normal v35→v36→v37 linear progression, which is not what happened. Links (working document, not submission-of-record): Edit — `overleaf.com/6661578839jrqvyjyfprhm#ffcaee`; View — `overleaf.com/read/zdzmvzfmmnrn#1c6617`. Whether this reconciled version gets formally resubmitted, and what "submitted-of-record" means going forward if so, is undecided and not assumed here.

**Nothing in §2 (Locked Design), §3 (Team/WBS), §4 (Timeline), §5 (Data/Training), or §6 (Pending Benchmark) changed** — this session is status updates plus one documentation/naming completion, not a new design, BOM, or scope decision.

---

**v21 change log (July 11, 2026 — new section opened, placeholder only; one footer inconsistency fixed along the way):** Requested directly ("about the presentation reformatting and rebuilding as a new section for later"). Two things, kept separate since they're different in kind:

**(1) New §6.5, "Presentation — Reformatting & Rebuild."** A grep against v1–v20 confirmed zero prior mentions of the presentation deliverable anywhere in this tracker — this is a genuinely new thread, not a promotion of something already logged elsewhere. No reformatting/rebuild specifics were given this session, so §6.5 is a placeholder: it states its own scope, carries forward what's known only from outside this tracker (unverified here), and lists open questions rather than inventing progress. Structured as "X.5" (inserted between §6 and §7) rather than renumbering §7→§8, matching the precedent §0.5 set at v16 — avoids touching the many existing cross-references to "§7" scattered through this document for a purely additive change.

**(2) Footer Supersedes-list gap, found while placing the new entry.** The list of superseded filenames at the very bottom of this document runs `v18 → v17 → v16 → v15 → ...` and stops — v19 and v20 were never appended, even though the narrative "As of v19:"/"As of v20:" summaries later in that same paragraph exist and are accurate. Likely slipped through v19's own audit since v19 was checking internal section content, not its own eventual footer entry. Fixed: v20 and v19 both added to the named list, each with a one-line description matching the "As of vXX" summary already on record for it — no new claims, just closing a gap between two things this document already said in two different places.

**Nothing in §0–§5 or §7 changed** beyond the one bottom-line sentence and footer fix noted above; §6 itself is untouched (§6.5 sits after it, doesn't alter it). No BOM, design, or scope-lock fact changed — nothing here is a project fact at all, it's a documentation-structure change plus one placeholder section.

---

**v20 change log (July 10, 2026 — Action #25 resolved: defence outcome confirmed, directly from Aaradhya, same-day as v19's audit; no new facts beyond the outcome itself, no BOM/purchase/design change):** v19 (earlier the same day) audited this tracker's internal consistency but could not resolve Action #25, since that item depends on external information — what actually happened at the July 9 defence — that no amount of self-consistency checking can produce. That information is now available. **(1) Defence occurred as scheduled, July 9, 2026.** Not postponed, not missed. **(2) Outcome: panel was optimistic about the project.** **(3) No specific questions reported about the ESP32-S3/laptop-only pivot** — the exact risk Tier 1 (§0.5) had flagged as needing rehearsal, since the signed v35 submission still names DevKit V1 and RPi 4B on paper with nothing on record backing the actual as-built design. Whether the rehearsal itself happened is still not independently confirmed, but the risk it was meant to cover — a panel member noticing the paper/reality gap and asking about it — did not materialize as an issue. **(4) New, not previously tracked: next step is negotiating with the department over new component costs following the RPi drop.** RPi's ~NPR 18,699 came out of the BOM entirely (v12+, no with/without-RPi split), but the department-funding conversation about what replaces that ask has not yet happened — logged as new **Action #31** (first item to use the "#31+" numbering Action #25 itself reserved at v19). **§0.5 Tier 1 updated from "LAPSED, outcome unconfirmed" to "RESOLVED"** — this is the first tier resolution since the tier system was added at v16; Tier 2 was already treated as the practical front of the queue per v17's note, and stays so, but Tier 1 is no longer an open item hanging over it. **Action #25 itself is not deleted** — marked resolved in place, per this tracker's own convention elsewhere (cf. how resolved Actions #1, 2, 4, 11–14 are handled in §1) of keeping resolved items visible rather than removing them, so the record of what was open and when stays intact. **Nothing in §2, §3, §4, §5, or §6 changed** — same scope-limited category as v15–v19; this is an outcome update to one already-logged open item, not a design, BOM, or purchase fact.

**(1) H1 header stale.** Document title had read "Project Tracker (v16)" since at least v17 — two version bumps behind the "Last updated" line immediately below it, which did track correctly. Fixed to (v19).

**(2) §0's "Future work only" count wrong.** Read "⬜ 3 items," but §1's own Future Work table (Ch.6) lists seven: #7, #8, #9 (pre-v18) plus #27, #28, #29, #30 (added v18) — the four v18 additions never got folded into this summary line. Fixed to 7.

**(3) "24 action items" stale in two places.** §0's Priority Tiers row and §0.5's own subtitle both still said "all 24 action items" — accurate as of v16, when this line was last written, but 30 action items are now logged (#1–30) as of v18. **Not fixed by a blanket 24→30 swap**, since the tier system was never meant to rank every item ever logged — resolved items (#1, 2, 4, 11, 12, 13, 14) and Future-Work-only items (7, per fix #2 above) sit outside it by design, same as always. Both lines reworded to state the true total (30) and name what's structurally excluded, rather than repeat an "all" framing that was already loose at v16 and is more visibly so now.

**(4) Three legacy-table promotions never backlinked.** Actions #23, #24, #26 each say "was legacy item #7/#4/#1, promoted" in their own §1 entries — correct — but §7's Legacy Items table still listed all three source rows (#1, #4, #7) as plain "Unverified," with no pointer back to the action that superseded them. Two downstream consequences, both stale as a result: the table's own intro sentence ("the other nine have no corresponding record... in §1") was no longer true for three of those nine, and the closing Recommendation line still listed #1/#4/#7 among items needing a decision, when that decision already happened. Fixed: backlink notes added to all three rows, intro sentence and Recommendation line reworded to reflect six (not nine) genuinely-unpromoted legacy items.

**(5) R-03 missing the cross-reference R-04 and R-05 both carry.** When R-04's and R-05's mitigations were found unsourced/contingent (Actions #22, #21, both v16), each got an inline "see Action #X" note added directly in its §2.7 row. R-03 has the identical problem — Action #23's own text already says its mitigation is "paper-only pending Action #23" — but R-03's row never got the matching flag. Fixed.

**Three upgrades, also folded in:** **(a)** Action #26 re-tiered into §0.5 Tier 3 alongside #23/#24, rather than left excluded from tiering under the same "Future Work" note as #27–30 — #26 carries real urgency (narrow Claims 1/3 before a panel finds the same prior art) that #27–30, genuine Ch.6-only items, don't share. **(b)** Actions #27 and #28 cross-linked — the camera-based confirmation modality (#28) would need the NPU/iGPU compute #27 unlocks to function as an actual second-opinion check, and the two were logged as unrelated ideas. **(c)** Action #25's "(#26+)" forward-reference to any future panel-feedback items corrected to "(#31+)" — #26–30 are taken as of v18, so new items would start at #31.

**Nothing in §2, §3, §4, §5, or §6 changed** — this is a documentation self-consistency pass on an already-locked plan, the same category as v15–v17. No design, BOM, purchase, or scope-lock fact changed.

**v18 change log (July 10, 2026 — literature-gap check + laptop-enabled components/future-work pass; new facts, sourced, no BOM/purchase change):** Requested directly ("about the research gap, the components we can use, and the work we can do further down the line dropping the RPi and using laptop — expand into that"). Unlike v15–v17, which were explicitly no-new-facts consistency passes, this session adds genuinely new external research — the first since v8's DevKit V1→S3 decision. Three threads, each logged with its own confidence level rather than folded into one blanket claim:

**(1) Literature-gap check (legacy item #1, promoted — Action #26, partially executed, not closed).** Ran a general web search (not a formal IEEE Xplore/Scopus database query — that distinction matters and isn't overclaimed here) against §2.3's five novelty claims. **Claim 1 (two-layer gated architecture) and Claim 3 (per-event SHAP explainability) both have closer prior art than the current proposal wording accounts for:** multiple 2024–2025 papers already publish multi-stage/gated/ensemble fall-detection architectures (CNN+BiGRU ensembles, dual-stream attention CNNs, channel-attention BiLSTM on SisFall/KFall), and at least two 2025 papers already apply SHAP specifically to fall-detection sensor data — one cloud-hosted (GCP), one not clearly on-device. **What still looks defensible, based on this pass:** none of the hits found run the full pipeline on true MCU-class hardware (ESP32/microcontroller-tier, not a Raspberry Pi, phone, or cloud instance) with SHAP computed at a local, non-cloud gateway specifically — that combination, not "SHAP" or "two-layer" in isolation, is where the actual gap looks like it still sits. **Claims 2, 4, 5 (Nepal-context dataset; adaptive sensitivity strategy pattern with no reflash; auto-generated clinical PDF reports) turned up no direct hits** in this pass — consistent with, not proof of, the claims holding. **Recommendation, not yet decided by Aaradhya:** narrow Claims 1 and 3's wording in the actual proposal/thesis text to the specific MCU+local-gateway combination rather than the broader "no existing system does this" framing, before a panel member finds the same papers this search did. **Action #26 stays open** — general web search is a reasonable first pass but doesn't meet the same evidentiary bar as an actual IEEE Xplore/Scopus query; that formal check still needs to happen before the gap-defense chapter is finalized.

**(2) Components the laptop-as-gateway newly enables, that RPi 4B structurally could not (Actions #27–28).** Checked, not assumed, same standard as Action #15's CPU-clock correction: Intel's own product-spec page for the Core Ultra 7 155H confirms an on-die NPU ("Intel AI Boost," 11 TOPS INT8) and an 8-Xe-core iGPU (18 TOPS INT8), both usable via OpenVINO — RPi 4B's Cortex-A72 + VideoCore VI has neither a dedicated NPU nor an ML-capable GPU path. This means the gateway can now run a genuine second model locally — not just SHAP attribution on the existing verdict — without touching the Mosquitto/FastAPI/PostgreSQL stack (§2.2) or waiting on cloud round-trips. Logged as **Action #27** (gateway-side second-opinion/ensemble model, cross-checking the ESP32-S3's on-device verdict before alerting, a direct mitigation angle for R-01) and **Action #28** (a camera-based secondary confirmation modality — RoboNepal's ESP32-S3-**CAM** board variant, already the confirmed vendor per Action #14, has a real unused camera FPC connector per Action #17's own footprint note; this is hardware already being bought, not a new purchase, sitting unused). Both are Ch.6 Future Work candidates, not current-scope changes — §2.4's scope lock is untouched.

**(3) Work enabled further down the line (Actions #29–30).** The Fusemachines Week 8 curriculum-alignment note (§7 appendix) already lists an "LSTM fall risk trend model (gateway — rolling window of fall frequency)" as a skills-alignment bullet, never promoted into an actual planned deliverable — the laptop's headroom (confirmed non-issue per Action #15; NPU/iGPU per Action #27 above) removes the compute reason it might have stayed a curriculum footnote under RPi. Logged as **Action #29**, Ch.6 Future Work, same non-scope-creep framing as #7–#9 above it. **Action #30, the honest other side of this pivot:** a shared-use laptop is not a production-scale gateway — no sleep/auto-lock/dedicated-machine discipline (Action #15) fixes that for a real multi-user eldercare deployment beyond this thesis's n=2-node demo. Recording this now, in Ch.6 Future Work, is cheaper than a panel member raising it as an unaddressed gap later.

**Nothing in §2.2, §2.4, §2.5, §2.6, §3, §4, or §5 changed** — §2.3's novelty-claims wording itself is flagged, not rewritten (that's Aaradhya's call, see Action #26); no BOM, purchase, or scope-lock fact changed this session.

**v17 change log (July 10, 2026 — post-defence date-check: defence outcome unconfirmed, §0.5 Tier 1 lapsed, new Action #25):** Requested as a repeat of the same standalone review that produced v16 ("update/upgrade itself as a foolproof plan") — not triggered by new research or a new decision from Aaradhya. One outcome, additive: **§0.5's own Tier 1 has silently lapsed.** v16 (written and dated July 9) scoped Tier 1 as "today, before/at defence" — rehearse the ESP32-S3/laptop-only pivot verbally, since v35 (signed, submitted-of-record) still names DevKit V1 and RPi 4B and nothing on paper backs the actual design if a panel member asks; recompile-check the Table ref (#10) if time permits. Today is July 10. The defence date named at the top of this tracker (§0 header, unchanged since v12) has now passed, and **no source anywhere in this tracker records whether the rehearsal happened, what — if anything — a panel member asked, or how the defence went.** This is the same "stated intent ≠ confirmed outcome" gap this tracker has already caught twice elsewhere — Action #18 ("ordered" ≠ "received"), Action #22 ("tested" ≠ dated/sourced) — just never applied to its own top-line gate before now. Logged as **Action #25**, placed above every other open item in §1 since it's the only one referencing a deadline that has already passed. §0.5's Tier 1 row is marked lapsed rather than deleted or silently overwritten, so the historical record of what "today" actually meant on July 9 stays intact; Tier 2 is now the genuine front of the actionable queue, not second-in-line behind a still-open Tier 1. **This pass adds no assumed panel-feedback section** — doing so would mean inventing content this tracker has no basis for; if feedback exists, Action #25's own resolution is where it gets decided whether that becomes new Action items (#26+) or a dedicated section, not assumed here. **Nothing in §1 (beyond the new Action #25 and a one-line date addendum to Action #10), §2, §3, §4, §5, §6, or §7 changed** — no design, BOM, or purchase fact changed today; this is a single date-consistency finding on an already-locked plan, the same category of pass as v15 and v16.

**v16 change log (July 9, 2026 — priority-tiered gap synthesis; no new facts, no design/BOM/purchase change):** Requested as a standalone review ("what's stopping the plan from being fool proof," then "list on priority") — not triggered by new research or a new decision from Aaradhya. Four outcomes, all additive: **(1) Two internal cross-reference gaps found, neither previously flagged:** R-05's battery-life mitigation (§2.7) rests on "~80mA" — the exact figure §2.5's own target table already flags as unverified against the ESP32-S3's real draw. R-01, R-02, R-04, and R-06 all received July 9 risk-matrix updates reflecting the S3/gateway changes; R-05 didn't, even though the number it rests on is already flagged two sections over. Logged as **Action #21**. Separately, R-04's "tested in advance" mitigation is the only line in the six-row Risk Matrix without a date, vendor, or method attached — every other risk in §2.7 is sourced to a specific day/number/vendor. Not a claim that the test didn't happen, just that it doesn't meet this tracker's own evidentiary bar. Logged as **Action #22**. **(2) Two dormant legacy items promoted to active tracking:** the FallGuard-era legacy list (§7 appendix) has sat unpromoted and unverified since it was first logged. This session's priority pass singled out two of its nine items as higher-priority than their Sept 2026 association implies, given real scheduling lead time. Self-collected dataset protocol (legacy #7 — fall types, ADL types, subject count, recording procedure, still undefined) is now **Action #23**; R-03's own mitigation ("self-collected dataset bridges domain gap") structurally depends on this protocol existing, so R-03 is mitigated on paper only until it does. MPU6050 firmware reuse-vs-rewrite (legacy #4, Rupesh's minor-project code) is now **Action #24** — flagged for resolution alongside #23 since it directly changes Rupesh's WP 2.0 estimate. **The other seven legacy items (team alignment confirmation, GitHub repo, sensitivity threshold calibration, enclosure form factor, RPi 4B PSU — now moot, weekly gate cadence, IEEE Xplore gap verification) were not raised in this session's priority ranking and stay appendix-only, unpromoted** — no silent scope expansion beyond what was actually discussed. **(3) New §0.5 — Priority Tiers**, ranking all 24 action items into 5 tiers by actual dependency/lead-time rather than by which header-group they sit under in §1. **(4) Nothing in §2.2, §2.3, §2.4, §2.6, §3, §4, §5, or §6 changed** — no purchase, receipt, design, or BOM fact changed today; this is triage plus two consistency findings on an already-locked plan.

**v15 change log (July 9, 2026 — Action #15 partially addressed: gateway compute confirmed as a non-issue; new Action #20 opened for the mobile-hotspot client-cap gap this surfaced):** Two pieces of research closed one open question and opened a smaller, more precise one. **(1) Compute headroom confirmed, not assumed:** direct comparison run against the actual RPi 4B this project would have used (4× Cortex-A72 @ 1.5GHz, 4GB) vs. the actual laptop now serving as sole gateway host (Intel Core Ultra 7 155H — 16 cores/22 threads, 6P+8E+2LP; P-core **turbo 4.8GHz confirmed via Intel's own spec page**, correcting a WMI `MaxClockSpeed` readout of 1400 that reports base clock, not max; 16GB RAM). Laptop outclasses the RPi on every axis by a wide margin, and the gateway's job is lighter than raw compute headroom even suggests — Mosquitto→FastAPI→PostgreSQL is ingest/routing only, inference stays on-device at the ESP32-S3 (§2.2), so this was never actually a close call. **(2) Broker throughput load-tested, with an important scope limit preserved rather than overclaimed:** Mosquitto ramped to 1000 sequential simulated MQTT clients on this laptop, zero failures, latency flat at 0.00–0.03s the entire way — confirms large headroom for SPARK's actual ingest load (2 nodes). **This result does NOT prove anything about WiFi node capacity** — client and broker ran on the same machine, so only TCP/broker-accept throughput was measured, never the 802.11-layer WiFi client-association mechanism a real multi-device deployment would exercise. Recorded as such here, not inflated into a "supports N nodes" claim anywhere in this tracker. **(3) Action #15 partially resolved, not closed:** the compute half of the gateway-reliability question is answered — RPi was never the more capable option, laptop has large headroom. **The actual open risk was always power/uptime during the demo** (sleep/auto-lock, plugged-in, dedicated machine), not compute — that part is unchanged, still not confirmed as the actual plan, Action #15 stays open on that basis alone. **(4) New Action #20:** the broker test's same-machine limitation means R-04's actual demo-day constraint — the mobile hotspot's real WiFi client-association cap — is still genuinely unmeasured, and can't be derived from anything tested this session (different layer entirely). Low urgency at n=2 nodes, but a real unknown until checked directly against whichever device provides the hotspot (two taps in that device's OS settings). **Nothing in §2.2, §2.3, §2.4, §2.5, §2.6, §3, §4, §5, or §6 changed** — this is reliability/capacity evidence for an already-locked architecture and BOM, not a design or cost change.

**v14 change log (July 9, 2026 — self-funding disclosure confirmed; two sourcing decisions added):** Three items from Action #18 (open as of v13) are now answered. **(1) Self-funding disclosure — confirmed, written into Action #14 as offered last session:** 1 ESP32-S3 unit is self-funded/advanced by Aaradhya. Cost **stays in the BOM at NPR 1,979** — real project cost, not removed — and the **departmental ask is reduced by that amount accordingly.** §2.6 now separates "total project cost" (unchanged) from "departmental ask" (reduced) so both figures stay honest at once, per last session's resolution. **(2) USB-C cable — second self-funded item, new BOM line, price not yet confirmed.** Needed to actually connect the ESP32-S3 to a laptop for flashing/quantization testing — this is **distinct from Action #4's NPR 267/unit line**, which is the TP4056 charging-input connector/socket on the wearable node itself, not a loose USB cable. A quick check found no single clean listing/price to lock in (Daraz results were mostly category pages or out-of-stock items) — logged as **Action #19**, same self-funded/reimbursable treatment as the ESP32-S3 unit, actual price to be recorded once purchased rather than estimated. **(3) MPU6050 — not a purchase, a lab-sourcing plan.** Aaradhya will try to get one from the major project lab (department resource, presumably reused/borrowed) rather than buying new for the test rig. **Doesn't change the official 3-unit MPU6050 BOM line (Action #12)** — that line is untouched; this is specifically about sourcing one unit fast for the immediate quantization test setup. Status is "will try," not "in hand" — tracked as in-progress, not resolved. **(4) Action #18 updated, not closed:** ESP32-S3 purchase decision and cable/MPU6050 sourcing are now confirmed as *plans*, but actual receipt/in-hand status for any of the three isn't independently verifiable from here — same non-assuming standard as the rest of this tracker. **Nothing in §2.2–§2.5, §2.7, §3, §4, §5, or §6 changed.**

**v13 change log (July 9, 2026 — Action #14 re-resolved: Himalayan out of stock, RoboNepal confirmed):** v12's "Himalayan Solution, in stock, NPR 1,800/unit" was checked again same day and found wrong — **Himalayan now shows Out of Stock.** That contradicted a claim v12 had just locked as confirmed, so it's treated as wrong until re-verified, not merely stale. **(1) New vendor, confirmed:** RoboNepal (already SPARK's confirmed vendor for the RPi, Action #1, before RPi was dropped) carries the same module — **NPR 1,979/unit, 5 in stock, confirmed July 9.** Board legitimacy checked directly, not assumed: dual USB-C, BOOT/RST buttons both present (so Action #2's no-CP2102 logic still holds), 16MB flash/8MB PSRAM/dual-core LX7 all match spec. **(2) Board variant note:** RoboNepal's listing is a WROOM-1-**CAM** variant — has a real (unused) camera FPC connector, not leftover naming. Functionally irrelevant (SPARK doesn't use it, no cost/interference), but physically this board is a different footprint than the plain N16R8 §7's enclosure note assumed. **Not a blocker** — Sankalpa confirmed enclosure design hasn't started yet, so this drops to the same low-priority tier as Action #6 (C3 benchmark): revisit once WP 3.0 actually kicks off, see new Action #17. **(3) Two alternatives ruled out, kept for record:** Al Taaz/Daraz (NPR 4,477/unit, in stock) — legitimate but 2.3× RoboNepal's price, fallback-only. LEMON/Daraz (Rs 3,665) — ruled out regardless of price: bare WROOM-1 module, no dev board, shipped overseas — violates both the zero-custom-PCB and zero-import constraints at once. **(4) §2.6 BOM:** MCU line becomes 2 × NPR 1,979 = **NPR 3,958** (was 2 × 1,800 = 3,600) — **+NPR 358 delta**, no longer net-zero from the original DevKit V1 swap. **New BOM total: ~NPR 15,004** (was 14,646). **(5) Two items discussed last session but deliberately not written in as resolved, since neither was actually confirmed:** whether 1 of the 2 units has been purchased yet (discussed as a staged plan — 1 now for quantization testing, 2nd before the Sept 2026 gate — but not confirmed as executed), and whether MPU6050 is already in hand or needs ordering. Both tracked as open, see new Action #18. **Nothing in §2.3–§2.5, §2.7 R-01/R-03/R-04, §3, §4, §5, or §6 changed** — this is a vendor/price correction within the already-locked S3 decision, not a new design change.

**v12 change log (July 9, 2026 — reconciliation: RPi fully dropped + ESP32-S3 pricing locked):** v9's "RPi retained as listed backup" framing and its ESP32-S3 placeholder pricing were both superseded later the same day, in two further direction changes v9 never captured. This entry folds both into one coherent state.

**(A) RPi dropped entirely, not kept as backup.** Direction from Aaradhya: RPi issuance is conditional on showing ESP32 working early — "we might as well drop RPi and focus on ESP side." This supersedes v9's Action #15 framing outright. (1) **§2.2 architecture** — RPi reference removed; laptop is the only gateway host, no backup line. (2) **§2.6 BOM** — collapses back to a single total; **RPi's NPR 18,699 is removed outright, not relabeled as backup.** No more with-RPi/without-RPi or primary/backup split. (3) **§2.7 R-06** — the "RPi retained as backup" mitigation no longer exists; replaced with a procedural mitigation (disable sleep/auto-lock, keep the laptop plugged in, use a dedicated machine rather than one doing double duty during the demo) — **flagged as a default, not yet confirmed as the actual plan** (Action #15, reframed below). (4) **R-05** simplified — no longer needs a "regardless of gateway host choice" hedge since there's only one host now. (5) **Critical-path implication:** narrows to WP 2.0 (Rupesh — MPU6050/Layer 1) + the ESP32-S3 bring-up/benchmark (§6); WP 1.0 (backend) is single-target now, no longer tested against RPi's ARM/Raspberry Pi OS separately. Sept 2026 gate ("gateway running") is unaffected in requirement, simpler in execution — it was always host-agnostic wording. (6) **Action #1** (RPi price, NPR 18,699 confirmed) — note updated to reflect the price is now purely historical; RPi isn't in the BOM at all, backup or otherwise.

**(B) ESP32-S3 pricing confirmed, quantity dropped to 2 (no spare), net BOM delta: zero.** Action #14 resolves. Himalayan Solution (existing vendor) restocked ESP32-S3-WROOM-1-N16R8 at **NPR 1,800/unit, in stock, confirmed July 9** — supersedes v9's NPR 4,000 placeholder. Separately, Aaradhya confirmed dropping the breakdown-contingency spare (Action #12): 2 units (2 primary nodes), not 3. (1) **§2.6 BOM** — 2 × NPR 1,800 = **NPR 3,600**, which is exactly what the original 3-unit DevKit V1 line cost (3 × NPR 1,200 = NPR 3,600). **Net delta from the entire MCU swap: zero.** Total holds at the pre-swap baseline, ~NPR 14,646. (2) **§4 Timeline** unaffected — 2 units = 2 primary nodes, matches the Sept 2026 "2 nodes assembled" gate exactly; no scope reduction. (3) **Action #12 — new gap, not silently resolved:** dropping the spare removes the firmware-bring-up-risk buffer (a spare board on hand if one fails during bring-up) that the original 3-unit allocation existed for. Flagged as open, not closed by the pricing resolution. (4) §2.7 R-02 (runtime memory pressure, PSRAM mitigation) is unrelated to the spare-board question and needs no change.

**Nothing in §2.3 (novelty claims), §2.4 (scope lock), §2.7 R-01/R-03/R-04, §3 (Team/WBS), §5 (Data/Training), or §6 (S3 vs C3 benchmark plan itself) changed by either reconciliation.**

**v8 change log (July 9, 2026 — DevKit V1 → ESP32-S3 upgrade decision):** Direction from Aaradhya: swap the wearable node MCU from ESP32 DevKit V1 to ESP32-S3, on the reasoning that "DevKit V1 might just be too less for a working demo" and that the project shouldn't try to 100%-optimize on a first pass — upgrade what's upgradable, keep the architecture mostly as-is. **This is a genuine spec/BOM change, not a resync — everything below reflects a decision, not a discovery.** (1) **§2.2 architecture, §2.5 performance targets, §2.6 BOM, §2.7 risk R-02** — all updated to name ESP32-S3 as the wearable MCU. Architecture *stages* (threshold gate → CNN → MQTT → gateway) are unchanged, matching the "keep architecture mostly same" intent — this is a component swap, not a redesign. (§7's 1D CNN internals block was checked and left as-is — it describes the CNN's own architecture, not the host chip, so nothing there is S3-specific.) (2) **Why S3, technically:** classic ESP32 WROOM-32 has 520KB SRAM and no PSRAM, so at runtime the TFLite Micro interpreter arena has to share that 520KB with the WiFi stack and MQTT buffers while Layer 2 inference is running — that contention, not flash space, is the likely "too less for a demo" pressure point (flash itself was never tight: CNN target is ~80–120KB against 4MB available). ESP32-S3 adds 8MB PSRAM the interpreter arena can live in instead, plus a newer LX7 core with DSP/AI vector instructions (ESP-DSP/ESP-NN) suited to exactly this kind of on-device inference. Should *improve* the <100ms Layer 2 latency target, not threaten it — reframed in §2.7 R-02 as a mitigation, not left as a risk. (3) **Sourcing — stays inside the zero-import constraint:** Himalayan Solution (the same vendor already used for ESP32/MPU6050/TP4056/AMS1117) stocks the ESP32-S3-WROOM-1-N16R8 module (16MB flash, 8MB PSRAM, dual USB-C) — currently showing **Out of Stock, no listed price** as of this check, logged as new Action #14. BOM line uses a **placeholder estimate of NPR 4,000/unit**, sourced from a different Nepal-region electronics retailer's listing for the equivalent N16R8 DevKitC-1 SKU — not Himalayan Solution's own price, since that isn't currently listed. **Flagged for confirmation before the BOM total is treated as locked**, same as any other unconfirmed line (cf. Action #1's RPi price pre-confirmation). (4) **CP2102 rationale (Action #2) revisited, not reversed:** original resolution said DevKit V1's "onboard USB-serial covers flashing." S3 doesn't have a USB-serial *bridge chip* in the same sense — it has native USB OTG in silicon, which does the same job without a separate chip, so CP2102 is still correctly excluded, but the *reason* changes; noted in §1 so a future resync doesn't misread the old rationale as no-longer-true and reopen it. (5) **§6 Pending Benchmark reframed**: was "DevKit V1 vs C3 SuperMini" for enclosure-size purposes; since DevKit V1 is no longer the baseline, re-run as "S3 vs C3 SuperMini" — same trigger condition and decision rule, new baseline chip. (6) **Enclosure (Action #11, WP 3.0):** S3 DevKitC-1 boards are close enough in footprint/pinout to standard 30-pin DevKit boards that this shouldn't force an enclosure redesign; PLA sizing already carries a print-iteration buffer. Flagged for Sankalpa to confirm once a physical unit is in hand, not treated as a blocking concern. **Nothing in §3 (Team/WBS), §4 (Timeline), §5 (Data/Training), §8 (Software patterns), or the novelty claims changed** — this is a component-level swap within the existing architecture, not a scope change.

**v5 change log:** Proposal package advanced v24→v33 (session-driven edits). Action #2 (CP2102) executed in-source. Action #4 (Type-C) executed in-source, RPi footnote/vendor updated. Enclosure committed to 3D-printed PLA only (dropped laser-cut acrylic alt), priced by filament weight w/ print-iteration buffer. ESP32/18650/INA219 given spare units (breakdown contingency). §5.5.2 SHAP sentence reformatted (overflow fix). Current BOM total: **14,646** (without RPi) / **33,345** (with RPi) — up from v4's 12,495/31,194 due to added spares + PLA + USB-C pricing (see §1 below for full breakdown). Table~\ref cross-ref showing as `??` in Overleaf preview — needs 2× recompile to confirm resolved, unverified as of this update (sandbox has no LaTeX network access to test).

**v4 change log:** Action #2 (CP2102) decided — dropped from BOM. Total: 31,594 → 31,194 (with RPi) / 12,895 → 12,495 (without RPi).

**v2 change log:** Cross-checked against `SPARK_MASTER_v1_20260630.md` (the pre-BOM-correction, v7-LaTeX snapshot). No new facts to pull forward — that file is fully superseded on every point of conflict:
- v1's BOM (~NPR 4,770, RPi treated as free in-inventory) is the *pre-correction* estimate; current BOM (§2.6) already reflects `main.md`'s real, larger figures and already flags the RPi price as needing correction (Action #1) — v1's number isn't a fix, it's the stale baseline this doc moved past.
- v1 has no record of the CP2102/INA219 drop candidates, Type-C connector flag, or C3 SuperMini swap — all of that analysis postdates v1 and stays as-is.
- v1's LaTeX package reference is v7; current package is v10 — no action needed, just confirms v7 is obsolete.
No changes to Sections 1–6 below as a result of this check; added here for the record.

---

## 0. Status At A Glance

| | |
|---|---|
| **Design status** | 🟢 Architecture, novelty claims, WBS all confirmed — 🟡 **though Claims 1 and 3's wording may need narrowing, see Action #26.** 🟢 Gateway host is laptop, **RPi dropped entirely** — not kept as backup (Action #15 reframed, see below). 🟡 **Wearable MCU vendor changed again:** ESP32-S3 confirmed, but Himalayan (v12's source) went out of stock same day — **RoboNepal is the current confirmed vendor, NPR 1,979/unit, +NPR 358 BOM delta** (Action #14 re-resolved, no longer net-zero). Architecture/pipeline stages unaffected. 🟡 Two open gaps: spare-board firmware-bring-up-risk buffer doesn't exist (Action #16); board physical footprint unconfirmed vs. §7's assumption, low-priority (Action #17). 🟡 Purchase/inventory status (units ordered, MPU6050 in hand) discussed but not confirmed — Action #18. |
| **Proposal package** | 🟢 `SPARK_Proposal_20260701_v35.zip` — **signed hardcopy, submitted-of-record** (resubmitted July 6, 2026 after deadline shift from July 2; v33→v35 diff was wording edits only). A separate `v36.zip` exists with the Gantt chart fix, but was not submitted. **Not yet updated for the S3 swap or the RPi drop** — proposal text still names DevKit V1 and RPi 4B; that's fine since it was already submitted, but both changes need writing into any post-defence revision or the thesis proper. |
| **Submission status** | 🟢 **Submitted** — July 2 (v33) then resubmitted July 6 (v35). Defence: **July 9, 2026 — occurred as scheduled, panel optimistic, no specific pivot-related questions reported.** Action #25 resolved v20. Next step: negotiate new component costs with department following the RPi drop — new **Action #31**. |
| **Table ref status** | 🟡 Unresolved as of last verification — whether `Table~\ref{tab:component_cost}` compiled correctly on Overleaf before either submission is **not confirmed by any source**. Not re-opened as "blocking" (submission already happened) but worth checking before defence if polishing further. |
| **Not blocking, but decide soon** | 🟡 9 items — #16 (no bring-up spare), #17 (board footprint vs. enclosure assumption), #18 (confirm receipt of self-funded/lab-sourced items), #19 (log USB-C cable price once purchased), #20 (mobile hotspot max-client cap), #21 (R-05 stale battery-draw figure), #22 (R-04 unsourced claim), #23 (dataset protocol — HOD discussion held, confirmation pending, v22), #24 (MPU6050 firmware reuse, promoted from legacy); Actions #2, #4, #11, #12, #14, **#15 (v22)** executed/resolved; legacy item **#6 resolved (v22, repo created)**; #3, #5 still open, see below |
| **Priority tiers (v16, re-scoped v19, Tier 1 resolved v20)** | 🟢 See §0.5 — 31 action items now logged in total (#1–31); tiers rank open, actionable items by dependency/lead-time, cutting across §1's header-groups. Resolved items and Future-Work-only items (7, below) sit outside the tier system by design. **Tier 1 resolved v20** (defence outcome confirmed, see #25); Tier 3 (#23/#24/#26) has real lead time despite its "Sept" association — don't wait on it. New #31 (department negotiation) not yet tiered — see §0.5 note. |
| **Future work only** | ⬜ 7 items — security/reliability gaps plus laptop-enabled components (Actions #27–30, added v18), correctly deferred to Ch.6 |

**Bottom line:** proposal was submitted twice — July 2 as v33, July 6 as v35 after a signature-driven deadline shift. v35 is submitted-of-record. Defence is July 9, 2026. The Gantt chart section never made it into either signed submission (only exists in an unsubmitted v36) — a known, low-severity gap, not worth reopening pre-defence. **Both post-submission hardware changes are settled in principle; one has a same-day vendor correction:** (1) gateway host is laptop, **RPi dropped entirely** (not kept as backup) — RPi's NPR 18,699 comes out of the BOM outright, no with-RPi/without-RPi split anymore. (2) wearable MCU is ESP32-S3, 2 units — but the vendor v12 locked in (Himalayan, NPR 1,800/unit) went out of stock the same day, so Action #14 was re-resolved against **RoboNepal, NPR 1,979/unit, 5 in stock, confirmed**. This is **no longer a net-zero swap** — it's a **+NPR 358 delta** over the original DevKit V1 baseline. **Combined effect: BOM total is ~NPR 15,004** (was 14,646 in v12). Neither change touches what was already signed and sent in (v35 still names DevKit V1 and RPi 4B), but both need reflecting going forward — the S3 swap in firmware work (WP 2.0), the gateway drop in backend/deployment work (WP 1.0/4.0) and demo-day procedure (Action #15) — plus the thesis document and any post-defence proposal revision. **As of v14: the self-funding question raised last session is resolved** — 1 ESP32-S3 unit is self-funded by Aaradhya, logged in the BOM at its real NPR 1,979 (not removed), with the departmental ask reduced accordingly (§2.6). A second self-funded item (USB-C cable, Action #19) is confirmed but unpriced. MPU6050 for the test rig will come from the major project lab rather than a new purchase — doesn't touch the official 3-unit BOM line. Four open gaps, none blocking: dropping the spare board removed the firmware-bring-up-risk buffer (Action #16); the RoboNepal board is a CAM variant with an unconfirmed physical footprint against §7's enclosure assumption, deferred since enclosure design hasn't started (Action #17); receipt of the self-funded/lab-sourced items isn't yet confirmed (Action #18); and the USB-C cable's actual price still needs logging (Action #19). **As of v16:** two more consistency gaps were found by cross-referencing this tracker against itself — R-05's stale battery-draw figure (Action #21) and R-04's unsourced "tested in advance" claim (Action #22) — and two long-dormant legacy items, dataset protocol and MPU6050 firmware reuse, were promoted out of the §7 appendix into active tracking (Actions #23, #24) after this session's priority pass flagged them as higher-priority than their Sept association implies. No purchase, design, or BOM fact changed; see §0.5 for how all 24 open items now rank against each other. **As of v17:** the defence date itself (July 9) has now passed with no outcome recorded anywhere in this tracker — logged as Action #25, §0.5's Tier 1 marked lapsed rather than "today." No purchase, design, or BOM fact changed. **As of v18:** a general web search against §2.3's novelty claims found closer prior art than expected for Claims 1 and 3 (Action #26, recommend narrowing, not yet decided); the laptop gateway's on-die NPU/iGPU (confirmed via Intel's own spec page) enables gateway-side components RPi 4B structurally couldn't run (Actions #27–28); two items promoted to Ch.6 Future Work (Actions #29–30). No BOM, purchase, or scope-lock fact changed. **As of v19:** a self-consistency audit (repeat of the methodology from the "identifying discrepancies" session) found and fixed five stale cross-references this tracker had accumulated across v16–v18 — H1 header stuck at v16, Future Work count stuck at 3 (real count 7), "24 action items" stuck at v16's count (real total 30, tier system re-scoped to name what's excluded rather than claim "all"), three legacy-table promotions (#1→#26, #4→#24, #7→#23) never backlinked, and R-03 missing the same "see Action #X" note R-04/R-05 already carry — plus re-tiered Action #26 into Tier 3, cross-linked Actions #27/#28, and corrected Action #25's stale "#26+" forward-reference to "#31+." No design, BOM, or purchase fact changed this session. **As of v20 (same day as v19):** Action #25 resolved — defence occurred as scheduled July 9, panel optimistic, no specific pivot-related questions reported; §0.5 Tier 1 moved from lapsed to resolved, the first tier resolution since tiers were introduced at v16. One new item opened in its place: **Action #31**, negotiate new component costs with the department following the RPi drop — not yet tiered, since it's new this session and its actual lead time/urgency isn't yet known. No BOM, purchase, or design fact changed. **As of v21:** new §6.5 opened to track presentation reformatting/rebuild work as its own thread — placeholder only, no specifics confirmed this session. Also surfaced in passing: **this tracker has never once mentioned the July 13, 2026 mid-term defence** (only the July 9 proposal defence, resolved above) — worth a proper entry once §6.5's scope is known, given the date is now two days out. No BOM, purchase, or design fact changed.

---

## 0.5 Priority Tiers (added v16 — cross-cutting view across all open items)

*Ranks open, actionable items by dependency/lead-time, not by which header-group they sit under in §1 — 30 action items now logged in total (#1–30), up from 24 when this line was first written (v16); resolved items and Future-Work-only items (7, §1 Ch.6 table) sit outside this ranking by design, not by omission. §1's structure below is otherwise unchanged.*

| Tier | Focus | Items | Why this tier |
|---|---|---|---|
| **1 — RESOLVED July 10 (v20)** | Was "today, before/at defence" as of v16 (July 9): rehearse the ESP32-S3/laptop-only pivot verbally, since v35 (signed, submitted-of-record) still names DevKit V1 and RPi 4B; recompile-check the Table ref if time permits. **Defence occurred as scheduled — panel optimistic, no specific pivot-related questions reported.** Whether the rehearsal itself happened is still not independently confirmed, but the risk it existed to cover didn't surface as an issue. | #25 (resolved) / #10 | None — resolved. See new #31 below for the follow-on item this outcome opened. |
| **2 — this week, gates WP 2.0** | Confirm/place the ESP32-S3 order and MPU6050 lab-source; add the 3rd spare unit *while already ordering* rather than as a later emergency reorder; log the USB-C cable price once bought | #16, #18, #19 | Real procurement lead time; bundling the spare now is cheaper than reopening the order later |
| **3 — start now despite "Sept" label** | Define the self-collected dataset protocol; resolve MPU6050 firmware reuse-vs-rewrite with Rupesh in the same pass; narrow novelty Claims 1/3's wording before a panel member finds the same prior art this session's search did | #23, #24, #26 | Volunteer recruiting/scheduling has real lead time a September start date doesn't account for; R-03's mitigation depends on #23 existing, not just being planned; #26 carries real urgency unlike the Ch.6-only items it was previously grouped with |
| **4 — zero cost, no dependency** | Lock the gateway procedural mitigation in as actual practice, not stated intent; patch the R-05/R-04 risk-matrix notes | #15, #21, #22 | Nothing blocks these — they just need a decision or a one-line edit |
| **5 — correctly wait, trigger hasn't fired** | Board footprint vs. enclosure; mobile hotspot client cap; C3 benchmark | #17, #20, #6 | Each needs something that doesn't exist yet (physical board in hand, known demo device, C3 unit on hand) |

**Note (v17):** Tier 1 lapsed, it didn't complete — see Action #25 before treating Tier 2 as the genuine front of the queue. Tiers 2–5 are otherwise unchanged from v16.

**Note (v18, superseded by v19 re-tiering above):** originally excluded Actions #26–30 from tiering entirely, grouping #26 with the pure Future Work items. **Note (v19):** #26 re-tiered into Tier 3 above — it carries real urgency (narrow Claims 1/3 before a panel finds the same prior art) that #27–30 don't share. Actions #27–30 (laptop-enabled components, Future Work) still sit outside this tier ranking on purpose — same bucket as the pre-existing #7–#9 Future Work items, none of which gate WP work either. Not a gap in the tiering; Ch.6-only items were never part of it.

**Note (v20):** Tier 1 resolved — see updated row above. New Action #31 (department negotiation over post-RPi-drop component costs) is not yet placed in a tier; it's new this session and doesn't yet have enough information (actual urgency, whether it blocks anything downstream) to rank against the existing tiers. Will be tiered once that's clearer — flagged here rather than guessed at.

---

## 1. Action Items (sorted by urgency)

### 🟢 Resolved — Defence outcome (surfaced July 10 v17, resolved July 10 v20)

| # | Item | Owner | Status |
|---|---|---|---|
| 25 | Confirm what actually happened at the July 9 defence — did it occur as scheduled, was the ESP32-S3/laptop pivot explained if a panel member asked, any feedback given | Aaradhya | **Resolved July 10 (v20).** Defence occurred as scheduled July 9. Outcome: panel was optimistic about the project. No specific questions reported about the ESP32-S3/laptop pivot despite the gap between v35's paper submission and the actual as-built design. Whether the verbal rehearsal itself happened is not independently confirmed, but the risk it was meant to cover didn't surface as an issue. Follow-on item opened as new **Action #31**. |

### 🟡 New — Post-defence department negotiation (opened July 10, v20)

| # | Item | Owner | Status |
|---|---|---|---|
| 31 | Negotiate new component costs with the department following the RPi drop — RPi's ~NPR 18,699 came out of the BOM entirely, but the department-funding conversation about what replaces that ask hasn't happened yet | Aaradhya | **Open, newly surfaced July 10 (v20).** Direct consequence of the defence outcome (Action #25) — panel was optimistic, next practical step is squaring the BOM change with whoever funds departmental component purchases. Not yet tiered (see §0.5 v20 note) — urgency/lead-time unclear until a conversation with the department is actually scheduled. |

### 🟡 Pre-defence check (was 🔴 blocking submission — submission has since happened, both times, without this being confirmed resolved)

| # | Item | Owner | Status |
|---|---|---|---|
| 10 | `Table~\ref{tab:component_cost}` renders as `Table ??` in Overleaf preview | Aaradhya | Label exists at correct location in source; likely stale-aux artifact from single-pass compile. **Not confirmed resolved before either submission (July 2 or July 6) — no source verifies this either way.** Since submission already happened, this is no longer a blocker in the original sense; worth a quick Overleaf recompile check regardless — **July 9 has passed, so "before the defence" is now moot,** but the check itself is still cheap and still worth doing before any future revision or resubmission. |

### 🟡 New — Gateway host: RPi dropped entirely, laptop reliability now the only safety net

| # | Item | Owner | Status |
|---|---|---|---|
| 15 | Confirm procedural mitigation for demo-day laptop reliability: disable sleep/auto-lock, keep plugged in, use a dedicated machine (not one doing double duty for dashboard screen-share/notebooks) | Aaradhya + Sankalpa | **Partially addressed July 9 (v15) — compute confirmed as a non-issue, power/uptime gap unchanged.** RPi 4B (4× Cortex-A72 @ 1.5GHz, 4GB) vs. this laptop (Core Ultra 7 155H, 16C/22T, turbo 4.8GHz confirmed via Intel's spec page, 16GB) — laptop wins on every compute axis by a wide margin, and gateway load is ingest-only (inference stays on-device at the ESP32-S3), so compute was never the actual risk here. Mosquitto also load-tested to 1000 sequential simulated clients on this laptop, zero failures, flat latency — confirms broker headroom for the real 2-node load. **Scope limit, not overclaimed:** that test ran client+broker on one machine, so it proves TCP/broker throughput only, not WiFi client-association capacity — see new Action #20 for the gap that leaves open. **What's still unresolved:** the actual risk was always power/uptime (sleep/auto-lock, plugged in, dedicated machine), not compute — unchanged, still not confirmed as the actual plan. Revisit before WP 4.0 (Streamlit/alerts, Sonia's WP), no earlier dependency. |

### 🟡 New — spare-board coverage gap from ESP32-S3 quantity drop (2 units, no spare)

| # | Item | Owner | Status |
|---|---|---|---|
| 16 | Firmware-bring-up-risk buffer — no spare ESP32-S3 board on hand if one fails during WP 2.0 bring-up | Rupesh + Aaradhya | **Open, new as of this update.** Action #12 originally added a 3rd DevKit V1 unit specifically as a breakdown-contingency spare; dropping to 2 units (no spare, per Aaradhya's direction) removes that buffer. Not urgent — no dependency until WP 2.0 firmware bring-up starts — but shouldn't be silently dropped along with the pricing question it got bundled with. Options: order a 3rd unit later if budget allows, or accept the risk and rely on RMA/vendor turnaround if a unit fails. |

### 🟡 New — RoboNepal board physical footprint (low priority, deferred)

| # | Item | Owner | Status |
|---|---|---|---|
| 17 | Confirm RoboNepal ESP32-S3-CAM board L×W (with headers) against §7's "close to standard 30-pin DevKitC-1 footprint" enclosure assumption — the CAM connector adds board length the plain N16R8 doesn't have | Sankalpa | **Open, correctly low priority — same tier as Action #6.** Sankalpa confirmed enclosure design hasn't started, so there's no lock-in event to race against. Resolve by seller message or caliper check once a unit is physically in hand; no need to chase it before then. Everything else about the board (chip, memory, USB-C, BOOT/RST, price, stock) is already confirmed. |

### 🟡 New — Purchase/inventory status discussed but not confirmed

| # | Item | Owner | Status |
|---|---|---|---|
| 18 | Confirm actual purchase status: (a) has the ESP32-S3 unit been ordered from RoboNepal yet; (b) is MPU6050 already in hand or does it need sourcing | Aaradhya | **Sourcing decisions confirmed July 9 (v14), receipt still open.** (a) ESP32-S3: 1 unit self-funded by Aaradhya, RoboNepal NPR 1,979 — see Action #14. (b) MPU6050: **not a purchase** — Aaradhya will try to source one from the major project lab (department resource) instead of buying, specifically for the quantization test rig. Doesn't touch the official 3-unit MPU6050 BOM line (Action #12). Neither unit's actual in-hand status is independently confirmable from here — "ordered/sourcing" is not the same as "received," so this stays open rather than closing on the strength of intent. |

### 🟡 New — USB-C cable, second self-funded item, unpriced

| # | Item | Owner | Status |
|---|---|---|---|
| 19 | USB-C cable for connecting/flashing the ESP32-S3 board — needed for the quantization test setup, distinct from Action #4's TP4056 charging-connector line (NPR 267/unit, a socket on the wearable node, not a loose cable) | Aaradhya | **Open, self-funded, price TBD.** A quick check didn't turn up one clean listing/price to lock in — Daraz results were mostly category pages or an out-of-stock USB-A→C item, not the USB-C↔C cable actually needed. Same treatment as Action #14's self-funded unit: log the real price once purchased rather than estimating it, then fold into §2.6's total-vs-departmental-ask split. |

### 🟡 New — Mobile hotspot max-client cap (R-04's actual demo device), unmeasured

| # | Item | Owner | Status |
|---|---|---|---|
| 20 | Confirm the actual demo-day mobile hotspot's WiFi client-association limit — a real, vendor-set 802.11-layer cap, distinct from anything Action #15's broker/compute testing touched | Aaradhya | **Open, newly surfaced July 9 (v15).** Action #15's 1000-client Mosquitto test ran on one machine and only exercised TCP/broker throughput — it cannot and does not say anything about how many independent WiFi radios a real hotspot will let associate, since that's a separate 802.11 management-frame mechanism the test never touched. Not yet checked against the actual device. Low urgency at n=2 nodes (any hotspot handles 2 trivially) but cheap to close: phone hotspots expose this directly in OS settings (Android: Settings→Hotspot; iPhone: fixed by OS, no user-visible setting) — two taps once the actual demo-day device is known. |

### 🟡 New — Risk-matrix cross-reference gaps (found by comparing this tracker against itself, no new facts)

| # | Item | Owner | Status |
|---|---|---|---|
| 21 | R-05's battery-life mitigation cites "~80mA" — §2.5's own target table already flags this exact figure as unverified against the ESP32-S3's real draw (added at the time of the MCU swap, since S3 has more silicon than classic ESP32) | Aaradhya | **Open, newly surfaced July 9 (v16).** R-01, R-02, R-04, and R-06 all received July 9 risk-matrix updates reflecting the S3/gateway changes; R-05 didn't, even though §2.5 two sections over already flags the exact number R-05 rests on. Not a new measurement — a cross-reference gap between two parts of the same document. Resolve by re-measuring draw once S3 hardware is in hand (same trigger as §2.5's own flag), then update R-05's probability rating if the number moves. |
| 22 | R-04's mitigation ("Demo uses dedicated mobile hotspot, not campus WiFi; tested in advance") carries no date, vendor, or method — the only line in the six-row Risk Matrix (§2.7) without one | Aaradhya | **Open, newly surfaced July 9 (v16).** Not a claim that the test didn't happen — every other risk in §2.7 is sourced to a specific day/number/vendor (R-02 to the S3 swap, R-05 to INA219 telemetry, R-06 to Action #15's laptop comparison); this is the one exception. Low cost to close: log when/how it was tested, or re-test and log it fresh, whichever is faster. |

### 🟡 New — Two legacy items promoted to active tracking (previously appendix-only, unpromoted since first logged)

| # | Item | Owner | Status |
|---|---|---|---|
| 23 | Self-collected dataset protocol — define fall types, ADL types, subject count, recording procedure (§5 gives *targets*: 500 fall events + 2000 ADL windows — not a protocol for how to actually collect them) | Aaradhya | **Open, in progress (updated July 23, v22).** Originally promoted from the §7 legacy list July 9 (v16) — was legacy item #7 (FallGuard-era, status "unverified" since first logged). **As of v22: Aaradhya has discussed protocol-related changes directly with the HOD; confirmation from HOD still pending.** No specifics on the discussed changes were given this session — not invented here. Still the case that **R-03's own mitigation ("self-collected dataset bridges domain gap") structurally depends on this protocol existing** — until HOD confirmation lands and the protocol itself is finalized, R-03 stays mitigated on paper only. |
| 24 | MPU6050 firmware — confirm whether Rupesh's existing minor-project firmware is portable to the fall-detection node or needs a rewrite | Rupesh | **Open, promoted from the §7 legacy list July 9 (v16).** Was legacy item #4 (FallGuard-era, status "unverified," never carried into §1). Flagged this session alongside Action #23 since both sit upstream of WP 2.0 firmware bring-up and directly affect Rupesh's time estimate for that WP. |

**Note (v16):** only these two of the nine FallGuard-era legacy items (§7 appendix) were promoted — the other seven (team alignment confirmation, GitHub repo, sensitivity threshold calibration, enclosure form factor/wear location, RPi 4B PSU — now moot since RPi is dropped, weekly gate cadence, IEEE Xplore gap verification) weren't raised in this session's priority pass and stay appendix-only, unpromoted. Threshold calibration in particular is adjacent to Action #23 (both need real fall data) but wasn't named in this session's ranking — worth revisiting alongside #23, not treated as resolved by this note. **Note (v19):** "IEEE Xplore gap verification," listed above as still-unpromoted at v16, was itself promoted two versions later — see Action #26 (v18) and the backlink now on §7's legacy item #1. Six of the nine remain genuinely unpromoted as of v19, not seven.

### 🟡 New — Literature-gap check against novelty claims (Action #26, partial — legacy item #1 promoted July 10, v18)

| # | Item | Owner | Status |
|---|---|---|---|
| 26 | Live IEEE Xplore gap verification — check §2.3's five novelty claims against 2023–2026 literature | Aaradhya | **Open, partially executed July 10 (v18).** Was legacy item #1 (FallGuard-era, "unverified — no record of this being run"), promoted after a general web search (not the formal IEEE Xplore/Scopus query this item actually asks for) found closer prior art than expected for **Claim 1** (two-layer gated architectures) and **Claim 3** (per-event SHAP explainability) — both techniques individually have 2024–2025 published examples. No hits found for Claims 2, 4, 5. **Recommend narrowing Claims 1/3 to the specific combination not found in this pass — true MCU-class on-device inference with SHAP at a local, non-cloud gateway** — but this is a recommendation, not a decision; Aaradhya reviews and decides whether/how to reword the actual proposal or thesis text. Stays open until the formal database query (what this item originally asked for) actually runs. |

### ✅ Resolved July 1 (was 🔴 blocking)

| # | Item | Owner | Resolution |
|---|---|---|---|
| 1 | RPi 4B (4GB) BOM price | Aaradhya | Confirmed NPR 18,699 (RoboNepal, robonepal.com, in stock). BOM line updated from 22,500 → 18,699. **Note (July 9, superseded by full RPi drop):** this price is now historical only — RPi 4B was briefly reframed as listed-backup hardware, then dropped from the BOM entirely (Action #15 reframed; §2.2, §2.6). Not in the build at any tier. |
| 2 | CP2102 USB-UART module (NPR 400) | Aaradhya | **Dropped**, executed in-source (Ch.3 subsection removed, BOM row removed, footnote updated). ESP32 DevKit V1's onboard USB-serial covers flashing. **Note (July 9, S3 swap):** on ESP32-S3 the reasoning shifts slightly — S3 has no separate USB-serial *bridge chip* the way DevKit V1 does, but it has native USB OTG built into the silicon that covers the same flashing/programming role directly. Conclusion (no CP2102 needed) still holds; the underlying reason is different chip, same outcome. |
| 4 | Micro-USB → Type-C standardization | Aaradhya | **Executed in-source.** All BOM/Ch.3/Ch.5 text now says USB-C exclusively (TP4056 input narrowed from "USB-C or Micro-USB" to "USB-C"). Figure asset `micro_usb_cable.png` replaced with a verified USB-C cable photo (two prior candidate images rejected — one was USB-A→Micro-B, wrong connector). Price corrected to NPR 267/unit (Daraz, was 300 estimate) via `daraz.com.np` listing. **Note (July 9, S3 swap):** ESP32-S3 ships with dual USB-C natively, so this standardization now applies to the MCU board itself too, not just the TP4056 charger input — a small consistency win, not an action item. |
| 11 | Enclosure fabrication method + costing | Aaradhya | **3D-printed PLA committed** (dropped "laser-cut acrylic" alternative from Ch.5/Ch.6 text to match costed BOM line). Priced from Anycubic 1kg/NPR 2,000 filament: 500g allocated (125g/unit × 2 units × 2× iteration-failure buffer) = NPR 1,000. Started at flat NPR 1,000 quote, went through 125g→250g→500g buffer sizing per user direction this session. |
| 12 | Contingency spares for breakdown-sensitive parts | Aaradhya | ESP32 DevKit V1 2→3 (NPR 3,600, spare board for firmware bring-up risk). 18650 cell 2→3 (NPR 750, Li-ion degrades). INA219 2→3 (NPR 2,400, I2C/solder-sensitive). MPU6050 and AMS1117-3.3 already had spares pre-session (3 and 5 respectively), untouched. **Note (July 9, S3 quantity dropped to 2, no spare):** the ESP32 spare-board portion of this action is **reopened, not carried over** — Aaradhya confirmed 2 units (no breakdown-contingency spare) once S3 pricing landed. See new Action #16 for the resulting bring-up-risk gap. 18650 and INA219 spare counts are unaffected, still ×3. |
| 13 | §5.5.2 SHAP paragraph line overflow | Aaradhya | Reformatted six-variable inline subscript math run ($a_{x,\text{peak}}$, etc.) into compact prose form to prevent line/page overflow. |
| 14 | ESP32-S3-WROOM-1-N16R8 price + stock confirmation | Aaradhya | **Re-resolved July 9 (v13).** Himalayan's NPR 1,800/unit (locked in v12 as "in stock, confirmed") went **Out of Stock** the same day — that claim is wrong until re-verified. New confirmed vendor: **RoboNepal, NPR 1,979/unit, 5 in stock** — direct-site price, not the discounted Daraz mirror (Rs 1,838). Board checked, not assumed: dual USB-C, BOOT/RST present, spec-matched (16MB flash/8MB PSRAM/dual-core LX7). It's a WROOM-1-**CAM** variant (real, unused camera connector) — functionally irrelevant, but see Action #17 for the physical-footprint follow-up this opens. At 2 units: 2 × 1,979 = NPR 3,958 — **+NPR 358 over the original 3-unit DevKit V1 baseline**, no longer net-zero. Ruled out: Al Taaz (NPR 4,477/unit, fallback-only) and a LEMON/Daraz bare-module listing (violates zero-import + zero-custom-PCB at once, regardless of its Rs 3,665 price). **Sourcing note (v14, confirmed):** 1 of the 2 units is **self-funded/advanced by Aaradhya** — cost stays in the BOM at NPR 1,979 (real cost, not removed), departmental ask reduced by that amount accordingly. See §2.6 for the total-vs-ask split. |

### 🟡 Before WP 2.0/3.0 kickoff (Sept 2026) — not urgent, but don't let these drift

| # | Item | Owner | Recommendation | Why it can wait |
|---|---|---|---|---|
| 3 | INA219 battery telemetry — now ×3, not ×2 | Aaradhya | Superseded by Action #12 (added as breakdown spare, not the drop-to-1 originally recommended here). Original "keep 1, drop 1" logic no longer applies since a 3rd unit was added as a contingency spare, not a redundant pair. Revisit only if budget pressure returns. | Doesn't block anything until WP 3.0 hardware bring-up |
| 5 | RPi 4B RAM: 4GB vs 2GB | Sankalpa | **Moot as of July 9 — RPi dropped entirely (not just deprioritized to backup), so this question no longer applies to any tier of the build.** Kept here for record only: had RPi remained in play, 4GB was the recommended default over 2GB for demo-day safety margin (concurrent services: Mosquitto+FastAPI+PostgreSQL+Streamlit+Telegram+SHAP). | No longer applicable; RPi not in the BOM |
| 6 | ESP32-S3 → C3 SuperMini swap (was DevKit V1 → C3) | Rupesh/Sankalpa | **Deferred — still the correct call, baseline confirmed July 9.** Wearable MCU is ESP32-S3, 2 units @ NPR 1,979 confirmed (RoboNepal, Action #14) — not C3. S3 was chosen specifically for more headroom, so this remains a "stay put unless the benchmark says otherwise" item, not an active swap-in-progress. Order a C3 unit early so it's on hand; run the latency benchmark (see §6 below, framed as S3 vs C3) once hardware arrives and WP 2.0 firmware work is underway — needs resolving before WP 3.0 enclosure sizing locks around a board footprint, not before. Note: with the spare dropped (Action #12/#16), there's no longer a spare ESP32-S3 unit that could double as C3 comparison stock — a C3 unit would need to be separately ordered if this benchmark is to run. | No dependency exists yet; hardware not even in hand |

### ⬜ Future Work only (Chapter 6, not required for proposal or demo)

| # | Item | Where it belongs |
|---|---|---|
| 7 | Mosquitto MQTT — no auth/TLS | Gateway, WP 4.0. One-line Future Work mention sufficient for proposal stage. |
| 8 | No WiFi reconnect/watchdog in ESP32 firmware | Firmware, WP 2.0. Add reconnect-on-drop logic during firmware bring-up — no recovery path currently exists if AP connection drops. |
| 9 | No OTA firmware update path | Firmware, WP 2.0. Physical USB reflash only for now; fine for demo, worth a Future Work bullet for a field-deployed wearable. |
| 27 | Gateway-side second-opinion/ensemble model — cross-check the ESP32-S3's on-device verdict using the laptop's on-die NPU (11 TOPS INT8) or iGPU (18 TOPS INT8) via OpenVINO, before alerting | Gateway, WP 4.0/Ch.6. RPi 4B had no dedicated NPU/ML-capable GPU path — this wasn't a realistic option under the old gateway host. Direct mitigation angle for R-01 (false-positive rate) if pursued. **Complements #28** — the camera modality below would need this compute to actually run as a second opinion, not just capture frames. Not current scope; §2.4's scope lock unchanged. |
| 28 | Camera-based secondary confirmation modality, using RoboNepal's ESP32-S3-**CAM** board's already-present (currently unused) camera FPC connector (Action #14/#17) | Firmware + gateway, Ch.6. Zero new hardware purchase — the connector is already on the board being bought. **Depends on #27** — a captured frame only becomes a "confirmation" once something at the gateway (the NPU/iGPU path #27 describes) can actually score it; logged separately above but not independently useful without it. Not current scope. |
| 29 | LSTM fall-risk trend model (rolling window of fall frequency) at the gateway — already listed as a Fusemachines Week 8 curriculum-alignment bullet (§7 appendix), never promoted to a planned deliverable | Gateway, WP 4.0/Ch.6. Laptop's confirmed compute headroom (Action #15) plus NPU/iGPU (Action #27) removes the reason this stayed curriculum-only under RPi. Not current scope. |
| 30 | Production-scale gateway architecture — a shared-use laptop is not a dedicated always-on box; a real multi-user deployment beyond this thesis's n=2-node demo needs a proper dedicated server or cloud instance | Ch.6, honest limitation. Action #15's procedural fixes (sleep/auto-lock/dedicated machine) solve the demo case, not the production case. Worth stating explicitly rather than leaving implicit. |

### ✅ Resolved / no action needed
- Certificate page — correctly removed for proposal stage (not required until final thesis)
- Supervisor/HOD names — confirmed correct (Er. Dipen Manandhar / Er. Suramya Sharma Dahal)
- `figure1.png` orphaned asset — harmless, delete in a cleanup pass whenever convenient
- Rupesh's surname spelling — fixed everywhere (Kadel, not Kandel)
- Landscape BOM tables — removed, replaced with portrait split tables
- Data collection ethics — no approval needed (healthy adult supervised volunteers)

---

## 2. Locked Design Reference

*Condensed. Full rationale for each choice lives in §7 if you need to defend a decision later.*

### 2.1 What SPARK is
Two-layer on-device fall detection wearable + explainable gateway pipeline for eldercare, built entirely from locally-sourced components (zero imports, zero custom PCB — hard department constraint).

### 2.2 Architecture (one line per stage)
```
MPU6050 (100Hz IMU) → complementary filter → Layer 1 threshold gate (<5ms)
  → Layer 2 TFLite Micro 1D CNN, INT8 (<100ms, P(FALL)>0.85) → MQTT publish
  → Laptop (gateway host): Mosquitto → FastAPI → PostgreSQL + SHAP attribution (<200ms)
  → Streamlit dashboard + Telegram alert (<2s total) + PDF incident report
```
**Wearable MCU: ESP32-S3** (WROOM-1-N16R8-CAM variant — 16MB flash, 8MB PSRAM, dual-core LX7), 2 units, **NPR 1,979/unit confirmed (RoboNepal)** — upgraded from ESP32 DevKit V1 as of July 9, 2026; vendor corrected same day after Himalayan (v12's source) went out of stock (see v8/v12/v13 change logs above). Every stage in the diagram above is unchanged; this is a swap of *which chip* runs Layer 1/Layer 2/MQTT-publish, not a change to the stages themselves.

**Gateway host: laptop, only host** (was RPi 4B) — swapped as of July 9, 2026; RPi 4B was briefly reframed as listed backup, then dropped from the build entirely the same day (see v12 change log above). Gateway pipeline stack (Mosquitto → FastAPI → PostgreSQL + SHAP) is unchanged; this is a swap of *which machine* runs the gateway, not a change to the pipeline itself.

### 2.3 Five novelty claims (gap defense)
1. Two-layer gated TFLite Micro 1D CNN, fully on-device, no cloud
2. Nepal-context wearable IMU dataset (first of its kind)
3. Per-event SHAP explainability at gateway (no existing system does this)
4. Auto-generated clinical-format PDF incident reports
5. Configurable sensitivity strategy (High/Standard/Sport), no firmware reflash

**Flag, not yet acted on (Action #26, v18):** a general web search (not the formal IEEE Xplore/Scopus query this still needs) found 2024–2025 published examples of both gated multi-stage architectures (Claim 1) and SHAP applied to fall detection (Claim 3) individually. What wasn't found: that specific combination — true MCU-class on-device inference with SHAP computed at a local, non-cloud gateway. Recommend narrowing Claims 1/3 to that combination; Aaradhya to decide on actual wording. Claims 2/4/5 turned up no hits in this pass.

### 2.4 Scope lock
**In scope (✅ locked):** IMU acquisition (A), two-layer detection (B), alert pipeline (C), clinical dashboard (D).
**Permanently out of scope (Ch.6 Future Work):** BLE/GATT protocol, multi-node monitoring, GPS localization, 4G fallback, clinical trial/hospital pilot.

### 2.5 Performance targets
| Metric | Target |
|---|---|
| CNN sensitivity / specificity | ≥90% / ≥90% |
| False positive rate (ADL, Standard profile) | <10% |
| End-to-end fall → Telegram alert | <2s |
| Layer 2 inference latency | <100ms on ESP32-S3 (was ESP32 DevKit V1 — target unchanged; S3's PSRAM + LX7 core should help hit this more comfortably, not threaten it, see §2.7 R-02) |
| SHAP attribution latency | <200ms on gateway host (laptop, only host — was RPi 4B; target unchanged, host-agnostic figure) |
| Battery life | ≥25h @ 2000mAh, ~80mA (unverified against S3's actual power draw — S3 has more silicon than classic ESP32, so this figure needs re-checking once hardware is in hand, not assumed to carry over unchanged) |

### 2.6 Current BOM total
**~NPR 15,004 — single figure, as of July 9 (v13).** No RPi line (dropped entirely, Action #15), no with-RPi/without-RPi split. Two changes happened after submission: one nets to zero, the other adds NPR 358.

**RPi removed:** NPR 18,699 (Action #1, previously confirmed) comes out of the total outright — it was briefly framed as a listed-backup line, then dropped from the build entirely the same day. Laptop gateway host adds NPR 0 (team-owned hardware, not purchased for the project).

**ESP32-S3 swap, re-resolved, +NPR 358 delta (Action #14):** original DevKit V1 line was 3 units × NPR 1,200 = NPR 3,600 (2 primary + 1 breakdown-contingency spare, per the original Action #12). Quantity is confirmed at **2 units, no spare** (spare dropped per Aaradhya's direction). Price went through two vendor states same day: Himalayan quoted **NPR 1,800/unit, in stock** — locked into v12 as confirmed, then found **Out of Stock** on recheck. Current confirmed vendor is **RoboNepal, NPR 1,979/unit, 5 in stock**: 2 × 1,979 = **NPR 3,958**, a **+NPR 358** delta over the original 3-unit DevKit V1 line (not the net-zero v12 recorded). Unit price rose 1,200→1,979 while count fell 3→2 — this time the two don't cancel exactly.

So the BOM total moves from the pre-swap, pre-RPi-drop baseline of ~NPR 14,646 to **~NPR 15,004** (14,646 + 358). Note this figure never included RPi in the first place (v9's "without RPi" column) — what changed since v12 is purely the MCU line's vendor/price, not quantity or anything else.

**Total project cost vs. departmental ask (added v14, per last session's resolution):** the BOM total above — **~NPR 15,004** — is the real, full cost of the design and doesn't change based on who pays for what; that figure is what goes in the thesis and any departmental costing discussion. Separately, **1 ESP32-S3 unit (NPR 1,979) is self-funded/advanced by Aaradhya** (Action #14) and **the USB-C cable (Action #19, price TBD) is also self-funded** — so the **departmental ask drops to ~NPR 13,025** (15,004 − 1,979), **and lower still once the cable price is logged.** Both numbers are accurate at once: the design costs what it costs, and part of that is being personally covered rather than requested. Update the departmental-ask figure once Action #19's cable price is logged.

Actions #1, #2, #4, #11, #12, #14 all resolved. Open gaps: Action #16 (no bring-up-risk buffer for the S3 nodes), Action #17 (RoboNepal board's physical footprint unconfirmed vs. §7's enclosure assumption, low priority), Action #18 (receipt of self-funded/lab-sourced items not yet confirmed), Action #19 (USB-C cable price not yet logged).

### 2.7 Risk Matrix
*Carried forward from FallGuard master v3 (§5.3) — not previously in this tracker. No risk below references a since-dropped component (e.g. CP2102), so all six are still applicable as written. **R-02 updated July 9** to reflect the ESP32-S3 swap. **R-05, R-06 updated July 9** to reflect the RPi 4B → laptop gateway swap, then updated again same day when RPi was dropped entirely (not kept as backup).*

| Risk ID | Description | Impact | Probability | Mitigation |
|---|---|---|---|---|
| R-01 | False positive rate too high — Layer 1 triggers on non-fall motions | High | Medium | Layer 2 CNN gating is the primary mitigation; sensitivity profile tuning (Strategy pattern, §7 Appendix) as secondary |
| R-02 | Runtime memory pressure on the wearable MCU — TFLite Micro interpreter arena contending with WiFi/MQTT for RAM during concurrent inference (originally framed as "flash too small"; flash was never actually tight — CNN target ~80–120KB against 4MB was always trivial headroom. The real pressure is SRAM at runtime, which is what "DevKit V1 too less for a demo" was likely picking up on) | Medium | Low → **Lower, post-S3** | **Primary mitigation upgraded July 9:** ESP32-S3's 8MB PSRAM lets the interpreter arena run outside the WiFi/MQTT-contended SRAM entirely — this is a more direct fix than the original fallback. Original fallback (threshold-only mode still demonstrates the detection concept) retained as a secondary safety net regardless of MCU choice. |
| R-03 | UCI/SisFall datasets insufficient for Nepal-context generalization | Medium | Medium | Self-collected dataset (500+ events) bridges domain gap; published as secondary contribution. **Note (July 10, v19):** this mitigation is paper-only until the collection protocol itself exists — see Action #23, whose own text already says as much; R-03's row just never carried the flag R-04/R-05 got when the same gap was found in them (Actions #22, #21). |
| R-04 | WiFi connectivity unreliable during demo (KEC campus congestion) | Medium | Low | Demo uses dedicated mobile hotspot, not campus WiFi; tested in advance. **Note (July 9, v15):** "tested" covers connectivity, not the hotspot's own max-client cap — that specific figure is unmeasured, see Action #20. Not a probability upgrade at n=2 nodes, just an unclosed loop. **Note (July 9, v16):** this mitigation is also the one line in this table without a date/vendor/method attached — see Action #22. |
| R-05 | 18650 battery life insufficient for full demo session (wearable node only) | Low | Low | INA219 power telemetry measured in advance; 2000mAh cell @ ~80mA gives ~25 hours. **Note (July 9, v16):** the ~80mA figure this rating rests on is the same one §2.5's target table already flags as unverified post-S3-swap — this row wasn't cross-updated when R-01/R-02/R-04/R-06 got their July 9 revisions. See Action #21. |
| R-06 | Streamlit dashboard complexity exceeds Sonia's timeline; **sub-risk: laptop-as-gateway means gateway uptime depends on a general-purpose machine, not a dedicated always-on box** — sleep/lid-close, other apps competing for resources, or the same laptop being needed for something else during the demo window | Low | **Resolved on the sub-risk (July 23, v22)** | FastAPI REST endpoint is the fallback display — curl output or Postman is acceptable for thesis; dashboard is a supporting deliverable. **For the gateway-uptime sub-risk:** no RPi backup box exists (dropped entirely, not just deprioritized) — mitigation is procedural: disable sleep/auto-lock, keep the laptop plugged in, use a dedicated machine rather than one doing double duty during the demo window. **Note (July 9, v15):** compute capacity confirmed as a non-factor in this sub-risk (laptop vs. RPi comparison) — the remaining exposure was purely procedural/power, not performance. **Note (July 23, v22): Action #15 confirmed executed** — sleep/auto-lock disabled, laptop plugged in, used as dedicated machine. Both halves of this sub-risk (compute, procedural) now closed. |

### 2.8 PostgreSQL Schema — `fall_events` Table
*Carried forward from FallGuard master v3 (§3.6) — field-level detail that §2.2's architecture line ("PostgreSQL") never spelled out.*

| Column | Type | Description |
|---|---|---|
| `event_id` | UUID | Unique event identifier |
| `user_id` | VARCHAR | Wearer identifier |
| `timestamp` | TIMESTAMPTZ | ISO 8601, UTC |
| `layer1_flag` | BOOLEAN | Threshold trigger |
| `layer2_confidence` | FLOAT | CNN fall probability (0.0–1.0) |
| `fall_confirmed` | BOOLEAN | Final verdict |
| `ax_peak`, `ay_peak`, `az_peak` | FLOAT | Peak acceleration at event |
| `severity_score` | INT | 1–5 scale (derived from \|a\| magnitude) |
| `shap_top_feature` | VARCHAR | Top SHAP contributor for this event (e.g., "az_peak") |
| `shap_json` | JSONB | Full SHAP values for all 6 IMU channels at event time |
| `alert_sent` | BOOLEAN | Telegram notification status |
| `false_positive_flagged` | BOOLEAN | Caregiver can dismiss via dashboard |

---

## 3. Team & Work Packages

| Name | Roll | WP | Sept 2026 Benchmark |
|---|---|---|---|
| Aaradhya Dev Tamrakar | 79001 | 1.0 — AI & Backend | FastAPI skeleton running; CNN baseline training notebook live |
| Rupesh Kadel | 79034 | 2.0 — Firmware & IMU | MPU6050 streaming @ 100Hz via WiFi; Layer 1 firing on simulated fall |
| Sankalpa Lamsal | 79039 | 3.0 — Hardware & Enclosure | Node powered from 18650, stable; enclosure concept sketched |
| Sonia Thapa | 79043 | 4.0 — Dashboard & Alerts | Streamlit rendering mock event JSON; Telegram test notification sent |

---

## 4. Timeline (Sep 2026 → Mar 2027)

| Month | Gate Deliverable |
|---|---|
| Sep 2026 | 2 nodes assembled + gateway running + basic dashboard live |
| Oct 2026 | TFLite Micro on nodes + end-to-end <200ms confirmed |
| Nov 2026 | Full alert pipeline + enclosures + ADL false-positive battery test |
| Dec 2026 | PDF report + dataset published to GitHub + thesis Ch 1–4 draft |
| Jan 2027 | Full thesis draft (Ch 1–6) + SHAP pipeline tested on real events |
| Feb 2027 | Supervisor feedback + demo script + stress test |
| **Mar 2027** | **Thesis submitted + live demo ready (boards)** |

---

## 5. Data & Training

| Source | Use | Scale |
|---|---|---|
| UCI MHEALTH | Primary CNN training | 10 subjects, resampled to 100Hz |
| SisFall | Augmentation (15 fall types, 19 ADL types) | 38 subjects, resampled to 100Hz |
| Self-collected KEC | Domain adaptation, Nepal-context, publishable | Target: 500 fall events + 2000 ADL windows |

CNN: `Conv1D(32,k=5)→ReLU→MaxPool→Conv1D(64,k=3)→ReLU→GAP→Dense(32)→Dense(2,Softmax)`, INT8 post-training quantization.

---

## 6. Pending Benchmark: ESP32-S3 vs C3 SuperMini

*Reframed July 9, 2026 — was "DevKit V1 vs C3 SuperMini." Baseline chip changed to S3 (§2.2) since DevKit V1 is no longer what the wearable runs; the C3-swap question itself, and why it's worth checking, hasn't changed. Same trigger condition, same decision rule, new baseline.*

**Trigger condition:** run this once a C3 unit is sourced, before WP 3.0 enclosure sizing locks.

1. Baseline **ESP32-S3** inference latency (bare + with WiFi/MQTT active) — log mean/p95/max via `micros()` around `interpreter->Invoke()`, 50-100 iterations. (Worth also logging PSRAM-arena vs internal-SRAM-arena separately here, since that's the new variable S3 introduces — see §2.7 R-02.)
2. Port identical model to C3 (`esp32-c3-devkitm-1` board target), same harness
3. Compare p95 latency **with WiFi active** (the real operating condition, not bare inference — single-core C3 has no second core to offload the radio stack, and no PSRAM either, so this comparison is now starker than the old DevKit V1 baseline: dual-core+PSRAM vs single-core+no-PSRAM, not dual-core-no-PSRAM vs single-core-no-PSRAM)
4. **Decision rule:** C3 p95 comfortably <100ms → swap is safe (proceed with #6 above, now meaning "swap to C3 instead of S3"). Close to/over → stay on **ESP32-S3**, treat wearable bulk as an enclosure problem for WP 3.0 instead (same fallback logic as before, updated baseline).

Worth documenting the result in Ch.5 methodology or an appendix regardless of outcome — "we benchmarked X vs Y and chose Z because—" is stronger than an unverified assumption if a panel member asks. Given the S3 swap was itself motivated by wanting *more* headroom than DevKit V1 offered, a plain reading is that this benchmark is less likely to end in a C3 swap than it might have been from a DevKit V1 baseline — but that's a hypothesis, not a result; the benchmark still needs to actually run once a C3 unit is on hand.

---

## 6.5 Presentation — Reformatting & Rebuild (opened July 11, v21)

*New thread — confirmed via grep against v1–v20 that the presentation deliverable has never been mentioned anywhere in this tracker before now. Opened as a placeholder at Aaradhya's request; no reformatting/rebuild specifics were given this session, so nothing below is a v21 finding — it's scope-holding, not progress-reporting.*

**Carried forward from outside this tracker, not verified this session:** multi-session work on the SPARK mid-term-defence presentation (PowerPoint) has been ongoing elsewhere — hardware-pivot text corrections (ESP32-S3 replacing RPi 4B), raster-image text patching, footer date updates, and BOM/cost-table edits on slides 24–25. Listed here for continuity only; current status of any of it is unconfirmed as of v21.

**Open, not yet answered:**
- Scope of "reformatting" vs. "rebuilding" — cosmetic pass vs. structural rework, and which slides either covers
- Whether this supersedes the slide 24–25 BOM/cost-table edits above, or runs alongside them
- Target date — **the mid-term defence itself (July 13, 2026) is not tracked anywhere else in this document** (see §0 bottom line), and is 2 days out as of this entry

**No action item number assigned.** Nothing here is concrete enough to rank in §0.5 or list in §1 yet — will be actioned once scope is confirmed, same convention as Action #31 at v20.

---

## 7. Appendix — History & Rationale (reference only, not for weekly tracking)

<details>
<summary>Naming history (PrakopNet → NetSight → FallGuard → SPARK)</summary>

- **PrakopNet** (solar LoRa mesh multi-hazard EWS): killed — RYLR890 (868MHz) import-only, department no-import rule.
- **NetSight** (precision-ag soil/weather node): killed — ADS1115 overseas-only, PCB fab outside scope.
- **FallGuard**: confirmed by supervisor June 29, 2026; renamed because "Guard" implies passive protection (misrepresents active kinetic analysis) and a real 2025 commercial camera-based product shares the name.
- Renaming tried Nepali/Sanskrit (Sanket Edge, Avastha, GatiSignal) then English options (VectorShift, Tilt, Lull, EdgeFall, Brace, Keel) before landing on **SPARK** — captures the "spike → computation → digital flare" nature without the cliché Guard/Shield/Sentinel lexicon.
- Full title kept long (two-clause) rather than shortened, so the literature-gap argument's explicit novelty claims (two-layer architecture, Nepal-context dataset) survive a skimming reviewer.
</details>

<details>
<summary>Why SPARK over alternative directions</summary>

| Alternative | Killed by |
|---|---|
| PrakopNet | RYLR890 868MHz import-only; no-import rule |
| NetSight | ADS1115 overseas-only; PCB fab out of scope |
| Direction C (ESP-NOW counter-UAV mesh) | Weaker novelty vs. SPARK's two-layer + SHAP + Nepal dataset |
| **SPARK** | 100% hardware in-hand/local same-day, zero imports, zero PCB, supervisor confirmed |
</details>

<details>
<summary>1D CNN internals (what each layer does)</summary>

- Input: 200×6 INT8 matrix (2s window, 6 IMU channels)
- Conv layers: width-16 filters learn micro-patterns (spike, deceleration, rotation)
- Pooling: 200→50→12 time steps, robust to ±50ms timing jitter across different people's falls
- Feature depth grows 6→32→64 channels as time axis shrinks — by Dense layer, exact timing is discarded, only "did this pattern occur" remains, which is why it generalizes across fall speeds
- INT8 quantization: 4× faster inference, fits ≤120KB flash
</details>

<details>
<summary>Software design patterns (OOSE)</summary>

| Pattern | Application |
|---|---|
| Factory | `FallDetector` ABC → `ThresholdDetector` (L1) + `CNNDetector` (L2) |
| Observer | FastAPI gateway → Streamlit + Telegram + PostgreSQL + PDF (all observers) |
| Strategy | `FallDetectionStrategy` → High/Standard/Sport, no firmware reflash |
</details>

<details>
<summary>Demo script (for evaluators, <10 min, in-lab)</summary>

1. Baseline (ADL walking) — no fall flag, `NORMAL` state
2. Simulated fall onto crash mat — Layer 1 fires → Layer 2 confirms → Telegram alert, all <200ms
3. False positive test (sit-to-stand) — Layer 1 may pre-fire, Layer 2 correctly rejects — demonstrates two-layer value over threshold-only systems
4. Sensitivity profile switch (Standard→HighSensitivity) via dashboard, repeat gentle fall — demonstrates Strategy pattern
5. Auto PDF report generated live from the demo event
</details>

<details>
<summary>LaTeX package structure & build fix chronology</summary>

Current package: `SPARK_Proposal_20260630_v10.zip`. Compiles via single `pdflatex` pass on Overleaf, no BibTeX/makeindex dependency (self-contained longtable abbreviations, hardcoded thebibliography).

Key fixes applied: abbreviations page rewritten as self-contained longtable (was broken dynamic-registration system); duplicate nomenclature entries fixed (one canonical registration per term, 17 total); references made to work in single pdflatex pass; `fontenc` load-order fixed; name-hyphenation bug fixed with `\mbox{}`; title page rebuilt to one line for all 4 authors; certificate page commented out (not required at proposal stage); BOM converted from landscape to portrait split tables (4-col BOM + 2-col specs); Table 6.3/6.4 column overflow fixed with proportioned `p{}` widths.

Full guideline compliance audit passed: page numbers, A4 margins, justified 1.5-spacing Times-equivalent 12pt body, heading sizes, figure/table numbering (Chapter.N), caption placement, IEEE citations (12 entries, no orphans).

13 references (IEEE format): WHO (2007), CBS Nepal (2021), Kangas et al. (2008), Bourke & Lyons (2008), Sucerquia et al. SisFall (2017), Banos et al. mHealthDroid (2014), Nho et al. CNN (2021), Wang et al. LSTM (2020), David et al. TFLite Micro (2021), Kumar et al. (2022), Lundberg & Lee SHAP (2017), Yao et al. ECG (2021).
</details>

<details>
<summary>Diagram design notes (for anyone touching the SVG/PNG generator again)</summary>

Three diagrams embedded in Ch.5: overall system flow, two-layer detection logic drill-down, 1D CNN architecture.

Connector semantics (5 roles): solid = same-device sequential step; solid elbow = same, bent for layout; dashed elbow = WiFi hop (only real network-boundary crossing); plain dashed no-arrowhead = parallel fan-out taps; arrowhead present only at final landing point of a logical hop.

B&W/print-safe version uses two independent visual channels per category (fill pattern + border dash-style) so it survives photocopying.

Bugs fixed during build: WiFi connector mis-routed through occupied space; z-order issue hiding connector lines under boxes; degenerate zero-length merge-bus line from a list-comprehension bug; report-box text overflow; label collision with frame title.
</details>

<details>
<summary>Archived project directions</summary>

- **PrakopNet** — solar LoRa mesh multi-hazard EWS with federated edge AI. Archived June 29, 2026 (import-blocked).
- **NetSight** — precision-ag soil/weather sensor node. Archived June 29, 2026 (PCB/overseas part).
- **Idea C (Counter-UAV)** — distributed TinyML drone detection. Archived earlier in ideation.
</details>

<details>
<summary>v1 Master (June 30) — retained for record, fully superseded</summary>

`SPARK_MASTER_v1_20260630.md` was the operative doc immediately after the FallGuard→SPARK rename, built around the v7 LaTeX package. Superseded by the v8–v10 revisions reflected throughout this tracker. Notable deltas, in case anyone finds a v1 copy circulating:

| v1 (June 30) | Current (this doc) |
|---|---|
| BOM total ~NPR 4,770, RPi listed as NPR 0 (in team inventory) | BOM ~NPR 35,395 with RPi (§2.6) — reflects `main.md`'s real proposal figures; RPi line itself flagged as overpriced (Action #1) |
| Single 5-column landscape BOM+specs table | Split into portrait 4-col BOM + 2-col specs (§2.6, resolved in v8) |
| No CP2102/INA219 drop analysis | Both flagged as drop candidates, Actions #2–3 |
| No connector standardization note | Type-C standardization flagged, Action #4 |
| No C3 SuperMini alternative considered | Swap candidate + benchmark plan, Action #6 / §6 |
| LaTeX package v7 | v10 (guideline-audited, all known build bugs fixed) |
| Open items: 6 generic sourcing/setup tasks | Full action list (§1), sorted by urgency, tied to specific BOM/design decisions |

Everything else (team, WBS, architecture, novelty claims, performance targets, timeline) was already consistent between v1 and the current state — v1 just predates the BOM correction pass and the component-level scrutiny that followed it.
</details>

<details>
<summary>Original proposal draft — Abstract & Problem Statement (FallGuard-era, v3, June 29) — ⚠️ stale terminology, needs rewrite before reuse</summary>

**⚠️ This block predates the FallGuard→SPARK rename (June 30) and the addition of the 5th novelty claim (SHAP was already present but numbered differently — see the source doc's own claim 3/4/5 renumbering note). It uses the old short title and old "four claims" framing referenced in its own text. Do not copy this into the current Overleaf package as-is — rewrite for SPARK's title, 5-claim numbering, and confirmed supervisor before reuse.** Kept here only as the historical starting draft, for anyone reconstructing how the current abstract evolved.

**Title (as drafted, FallGuard-era):**
FallGuard: A Wearable Real-Time Fall Detection and Caregiver Alert System with Two-Layer Edge AI for Elderly Care Applications

**Abstract (as drafted, FallGuard-era):**
FallGuard is an open-hardware wearable fall detection system targeting the elderly care gap in Nepal's growing urban aging population. The system deploys an ESP32 DevKit + MPU6050 IMU node worn on the wrist or chest, implementing a two-layer detection architecture: a deterministic threshold pre-filter (Layer 1) gates a TFLite Micro INT8 quantized 1D CNN classifier (Layer 2) running entirely on the ESP32 — no cloud dependency for safety-critical fall classification. Detection latency is under 200ms end-to-end. Confirmed fall events trigger a WiFi MQTT payload to an RPi 4B gateway running a FastAPI/PostgreSQL backend, which fires a Telegram alert to the caregiver within 2 seconds, updates a Streamlit clinical dashboard, and logs the event with ISO 8601 timestamp and severity score. PDF incident reports are auto-generated in a clinical format suitable for care facility documentation. The project contributes a Nepal-context wearable IMU fall dataset (self-collected at KEC), a configurable sensitivity strategy pattern (High/Standard/Sport), and an open-source hardware + software reference design for low-cost elderly fall monitoring applicable across South Asian care settings.

**Problem Statement (as drafted, FallGuard-era):**
Falls are the leading cause of injury-related mortality among adults over 65 globally (WHO, 2021). Nepal's elderly population is projected to double by 2035 (CBS). Commercial fall detection solutions (Apple Watch, medical alert pendants) are cost-prohibitive and unavailable domestically. Existing academic systems rely on threshold-only detection (unacceptably high false-positive rate) or cloud-dependent ML (network dependency unacceptable for safety-critical applications in Nepal's connectivity environment). A low-cost, open-hardware, WiFi-enabled fall detection system with on-device edge AI addresses a real unmet need in Nepal's emerging eldercare sector.

**Gap statement (as drafted, FallGuard-era — compare against current 5-claim gap statement used in the submitted proposal):**
"Commercial fall detection systems (Apple Watch, Samsung Galaxy Watch, Withings ScanWatch) are cost-prohibitive for Nepal's elderly care context, require proprietary ecosystems, and operate as closed black-box systems — returning a binary fall verdict with no classifier explanation. Published academic systems use either threshold-only detection (high false-positive rate) or cloud-dependent ML (network-dependent safety). No published open-hardware system demonstrates: (a) a two-layer gated architecture with on-device TFLite Micro inference, (b) SHAP-based per-event explainability surfaced to caregivers, (c) adaptive sensitivity profiles, and (d) clinical-format automated reporting validated on a Nepal-context IMU dataset."
</details>

<details>
<summary>Curriculum alignment tables (BEI courses + Fusemachines/DataCamp) — for thesis Ch.1 justification section</summary>

**BEI Curriculum Alignment:**

| Subject | Application in SPARK |
|---|---|
| Embedded Systems (CT 655) | ESP32 firmware, MPU6050 ISR, TFLite Micro deployment, I2C/UART drivers |
| Artificial Intelligence | 1D CNN architecture, INT8 quantization, F1/AUC evaluation, training pipeline |
| DSAP | Sliding window algorithm, complementary filter, FFT feature extraction |
| Signal Processing | IMU noise filtering, frequency domain analysis of fall signatures |
| OOSE (CT 659) | Factory + Observer + Strategy patterns (documented in thesis Chapter 3) |
| Project Management (CT 658) | WBS, risk matrix, gate-based monthly timeline |
| RF & Microwave Engineering | WiFi 802.11 b/g/n signal propagation (gateway link characterization) |
| Wireless Communication | IEEE 802.11 CSMA/CA protocol stack (application context) |

**Fusemachines & DataCamp Alignment:**

| Skill Source | Week / Course | Direct Application in SPARK |
|---|---|---|
| Fusemachines | Week 4 — Scikit-learn ML Pipeline | StandardScaler baked into firmware (scaler params from training) |
| Fusemachines | Week 5 — XGBoost/RF + SHAP | SHAP feature importance on fall classifier input features (thesis Chapter 4) |
| Fusemachines | Week 6 — Probabilistic Models | Bayesian threshold calibration for Layer 1 sensitivity |
| Fusemachines | Week 7 — Clustering | ADL cluster analysis for false-positive characterization |
| Fusemachines | Week 8 — Time-Series Forecasting | LSTM fall risk trend model (gateway — rolling window of fall frequency) |
| Fusemachines | Week 3 — FastAPI + Docker + PostgreSQL | Entire gateway backend stack |
| DataCamp | Python Data Associate | Data pipeline, evaluation metrics |
| DataCamp | SQL Associate | PostgreSQL event log querying, report aggregation |

Names carried over verbatim from the FallGuard-era source doc — component/architecture nouns (ESP32, MPU6050, TFLite Micro, etc.) are unchanged by the SPARK rename, so no rewrite needed here unlike the abstract block above.
</details>

<details>
<summary>Legacy open items from FallGuard master (v3, June 29) — status unverified, not yet cross-checked against current project state</summary>

The FallGuard-era master kept its own open-items list (10 items). One is confirmed resolved; **three (#1, #4, #7) were subsequently promoted into active tracking as Actions #26, #24, #23 respectively — see the backlink on each row below.** The remaining six have no corresponding record anywhere in this tracker's action lists (§1) — meaning they were never explicitly marked done, dropped, or superseded. Listed here for visibility, **not** merged into §1's active list (aside from the three now cross-referenced), since — unlike §1's items — none of these have had their current status confirmed this session.

| # | Item (as originally logged) | Owner | Status here |
|---|---|---|---|
| 1 | Live IEEE Xplore gap verification — two-layer gated TFLite Micro fall detection (2023–2026) | Aaradhya | **→ Promoted to Action #26 (v18).** A general web search (not yet the formal database query this item asks for) found closer prior art than expected for novelty Claims 1/3 — see §1 for status, still open. |
| 2 | Team alignment meeting — confirm all four members agree to FallGuard (now SPARK) pivot | Aaradhya | Unverified — presumably moot given proposal was signed/submitted by the full team, but not explicitly confirmed |
| 3 | Supervisor assignment — confirm via KEC 8th semester group formation | Aaradhya | ✅ **Resolved** — Er. Dipen Manandhar confirmed (this tracker, §"Resolved / no action needed") |
| 4 | Rupesh: MPU6050 clarification — confirm whether existing minor-project firmware is portable to the fall-detection node or needs rewrite | Rupesh | **→ Promoted to Action #24 (v16).** See §1 for status, still open. |
| 5 | Sensitivity threshold calibration — Layer 1 \|a\| and Δt values need empirical tuning from real fall simulations | Rupesh + Aaradhya | Unverified — §2.2 architecture and §7 appendix (1D CNN internals) still state the design values (2.5g / 300ms) as fixed thresholds; whether empirical tuning against real fall data has happened is not recorded |
| 6 | SPARK/FallGuard GitHub repo + README + team access | Aaradhya | ✅ **Resolved (v22).** Repo created at `github.com/Aaradhya-Dev-Tamrakar/SPARK` — README, .gitignore, sync.ps1, and scaffold folders (firmware/training/gateway/data) in place. Team access (Rupesh, Sankalpa, Sonia as collaborators) not independently confirmed here — same non-assuming standard as the rest of this tracker; repo *existing* is resolved, collaborator access is a separate, unconfirmed sub-item. |
| 7 | Self-collected dataset protocol — define fall types, ADL types, subject count, recording procedure | Aaradhya | **→ Promoted to Action #23 (v16).** See §1 for status, still open — R-03's mitigation depends on it. |
| 8 | Enclosure form factor decision — wrist-worn vs. chest-worn vs. belt-clip (affects Layer 1 threshold calibration) | Sankalpa + Rupesh | Unverified — enclosure fabrication *method* was resolved (3D-printed PLA, Action #11 in §1), but form factor/wear location isn't addressed anywhere in this tracker |
| 9 | RPi 4B power supply — confirm team RPi 4B PSU is available or budget NPR 300–500 | Sankalpa | Unverified — no confirmation recorded either way |
| 10 | Weekly gate system for 8th semester | Aaradhya | Unverified — §4 (Timeline) has monthly gates; whether a *weekly* cadence was separately set up is not recorded |

**Recommendation:** worth a quick pass to close out or explicitly re-open whichever of #5, #6, #8, #9, #10 still matter — item #5 in particular looks like it'd matter before WP 1.0/2.0 dataset-collection work starts in September, and #6 (repo) is presumably trivial to just check. (#1, #4, #7 dropped from this list as of v19 — already promoted to Actions #26, #24, #23; #7's own promotion covers the dataset-protocol concern this line used to flag separately.)
</details>

---

*Supersedes `SPARK_TRACKER_v21_20260711.md` (new §6.5 opened for presentation reformatting/rebuild, placeholder only; footer supersedes-list gap fixed, v19/v20 appended; no BOM/design/scope change), `SPARK_TRACKER_v20_20260710.md` (Action #25 resolved: defence occurred as scheduled July 9, panel optimistic, no specific pivot-related questions reported; new Action #31 opened for post-RPi-drop department cost negotiation; §0.5 Tier 1 moved lapsed→resolved; no BOM/design/purchase change), `SPARK_TRACKER_v19_20260710.md` (self-consistency audit: five stale cross-references found and fixed — H1 header, Future Work count, "24 action items" in two spots, three unbacklinked legacy-table promotions, R-03's missing risk-matrix note — plus three upgrades, #26 re-tiered/#27↔#28 cross-linked/#25's forward-reference corrected; no design/BOM/purchase change), `SPARK_TRACKER_v18_20260710.md` (literature-gap check + laptop-enabled components/future-work pass: Actions #26–30 added, no design/BOM/purchase change), `SPARK_TRACKER_v17_20260710.md` (post-defence date-check: defence outcome unconfirmed, §0.5 Tier 1 marked lapsed, Action #25 added, no design/BOM/purchase change), `SPARK_TRACKER_v16_20260709.md` (priority-tiered gap synthesis: Actions #21–24 added, §0.5 priority tiers added across all 24 open items, no design/BOM/purchase change), `v15_20260709.md` (Action #15 partially addressed — gateway compute confirmed as a non-issue against actual RPi 4B and laptop hardware; new Action #20 opened for the mobile-hotspot max-client cap this surfaced), `v14_20260709.md` (Action #15 partially addressed — gateway compute/broker headroom confirmed against actual RPi 4B and laptop hardware; new Action #20 opened for the mobile-hotspot max-client cap this surfaced, since the broker test's same-machine setup couldn't measure it), `v13_20260709.md` (self-funding disclosure confirmed and written into Action #14; USB-C cable added as a second self-funded, unpriced item, Action #19; MPU6050 sourcing clarified as a lab-borrow plan, not a purchase), `v12` (Action #14 vendor/price correction: Himalayan's NPR 1,800/unit went out of stock same day, RoboNepal confirmed at NPR 1,979/unit instead), `v9` through `v11` (undocumented intermediate states — RPi-as-backup and RPi-fully-dropped, S3-placeholder and S3-confirmed-pricing — reconciled in v12), `SPARK_TRACKER_v8_20260709.md`, `SPARK_TRACKER_v7_20260709.md`, `SPARK_TRACKER_v6_20260708.md`, `SPARK_TRACKER_v5_20260701.md`, `SPARK_TRACKER_v4_20260701.md`, `SPARK_CONSOLIDATED_20260701.md`, `SPARK_MASTER_v1_20260630.md`, and `FallGuard_MASTER_v3_20260629.md` as the working tracker. All originals retained as historical record if needed; this version is optimized for weekly team use — action items first, locked design as quick reference, full history collapsed into the appendix. Proposal source itself is at `SPARK_Proposal_20260701_v35.zip` (signed hardcopy, submitted-of-record, resubmitted July 6, 2026, **still names ESP32 DevKit V1 and RPi 4B as the gateway — both changes postdate submission and aren't reflected in the signed document**) — `v36.zip` is a separate, unsubmitted digital revision with the Gantt chart fix v35 lacks. `Table~\ref{tab:component_cost}` compile status was never confirmed resolved before either submission; check on Overleaf before the July 9 defence if useful, though it's no longer submission-blocking. **Wearable MCU is ESP32-S3, 2 units, NPR 1,979/unit confirmed (RoboNepal)** (§2.2, §2.6) — Action #14 re-resolved, **+NPR 358 BOM delta** (no longer net-zero); **1 unit self-funded by Aaradhya**, departmental ask reduced accordingly. **Gateway host is laptop, only host** (§2.2) — RPi 4B dropped from the BOM entirely, not kept as backup; demo-day laptop-reliability mitigation open per Action #15. **Open gaps:** ESP32-S3 spare-board buffer removed with the quantity drop to 2 units (Action #16); RoboNepal board's physical footprint unconfirmed vs. §7's enclosure assumption, low priority (Action #17); receipt of self-funded/lab-sourced items not yet confirmed (Action #18); USB-C cable self-funded but unpriced (Action #19); mobile hotspot's max-client cap unmeasured, low priority at n=2 (Action #20). **Gateway compute confirmed as a non-issue** (laptop vs. RPi 4B comparison, Action #15) — remaining gateway-uptime exposure is procedural/power only. **Total project cost (§2.6) is ~NPR 15,004 regardless of funding source; the departmental ask is lower, reflecting the self-funded items.** **As of v16:** two risk-matrix rows (R-04, R-05) were found citing claims not sourced/cross-updated to this tracker's own standard (Actions #22, #21); two FallGuard-era legacy items — dataset protocol and MPU6050 firmware reuse — were promoted out of the §7 appendix into active tracking (Actions #23, #24); and a new §0.5 ranks all 24 open items into 5 priority tiers by actual dependency/lead-time. No design, BOM, or purchase fact changed this session. **As of v17:** the defence date named throughout this tracker has passed (July 9 → today is July 10) with no outcome recorded anywhere in it — Action #25 opened, §0.5 Tier 1 marked lapsed rather than deleted. No design, BOM, or purchase fact changed this session either. **As of v18:** first version since v8 to add genuinely new external research rather than a consistency pass — a general web search (not a formal IEEE Xplore/Scopus query) found closer prior art than expected for novelty Claims 1 and 3 (Action #26, narrowing recommended, not yet decided); the laptop gateway's confirmed on-die NPU (11 TOPS INT8) and iGPU (18 TOPS INT8) open gateway-side components RPi 4B structurally never had (Actions #27–28); two items promoted to Ch.6 Future Work as a result (Actions #29–30). No BOM, purchase, or scope-lock fact changed this session. **As of v19:** self-consistency audit — five stale cross-references (H1 header, Future Work count, "24 action items" in two spots, three unbacklinked legacy-table promotions, R-03's missing risk-matrix note) found and fixed, three upgrades applied (#26 re-tiered, #27↔#28 cross-linked, #25's forward-reference corrected). No design, BOM, or purchase fact changed this session. **As of v20:** Action #25 resolved — defence occurred as scheduled July 9, panel optimistic; new Action #31 opened for department cost negotiation; §0.5 Tier 1 moved lapsed→resolved. **As of v21:** new §6.5 opened for presentation reformatting/rebuild (placeholder only); footer supersedes-list gap fixed. **As of v22:** SPARK's full acronym ("Signal Pattern Analysis & Real-time Kinetics") confirmed and recorded for the first time since the June 30 FallGuard→SPARK rename; Action #15 fully resolved (procedural half confirmed executed, joining the already-resolved compute half); Action #23 advanced but not closed (HOD discussion held, confirmation pending); legacy item #6 resolved (GitHub repo created at `github.com/Aaradhya-Dev-Tamrakar/SPARK`, scaffold only, no firmware/training code yet); and the "v37" proposal-report label clarified as an unsubmitted working reconciliation of v35 (as actually submitted) with v36's revealed Gantt-chart fix — not a new linear version superseding either. No design, BOM, or purchase fact changed this session.***
