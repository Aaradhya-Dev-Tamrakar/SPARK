# SPARK — Design Ideas Log

Exploratory design concepts, external render outputs, and aesthetic direction notes.
**Not implementation-locked.** Cross-reference `SPARK_TRACKER.md` Action #8 (enclosure form factor) for the resolved engineering decision this log feeds into.

---

## DI-01 — Bracer-Silhouette Enclosure, Two-Zone Internal Layout

- **Status:** Exploratory concept. Not adopted into BOM/CAD.
- **Date logged:** 2026-08-06
- **Asset:** `dev_logs/design_assets/enclosure_concept_v1_two_zone_bracer.png`
- **Source:** AI image concept render (external tool, prompt-engineered manually; not generated in-repo).

**Concept summary:**
Single-piece open-back forearm enclosure, silhouette inspired by a bracer/vambrace (reference used for form only — explicitly not for leather/Viking/medieval material or ornamentation). Wraps ~70–75% of forearm circumference, 25–30% continuous open seam along the underside for flex/ventilation/weight. Matte charcoal TPU, soft-touch micro-texture. Single wide Velcro strap closure (senior-friendly, one-handed) bridging the seam near the wrist — no buckles/rivets/lacing. USB-C port with flexible TPU dust cover + hidden status LED.

**Internal layout — two-zone architecture** (supersedes an earlier single-cavity packaging draft in the same prompt-engineering session):
- **Zone 1 (wrist, slim):** MPU6050 IMU only (~15×20×3 mm), flat against inner shell wall, dorsal/top-of-wrist position — motion-sensing reference point.
- **Zone 2 (forearm/elbow, wide):** ESP32-S3-WROOM-1 dev board (~25×50×7 mm), 1000 mAh LiPo (~32×52×7 mm), TP4056 charge/protect PCB (~15×17×2 mm). Widest cross-section of the shell lives here; USB-C access at this end.
- **Connecting spine:** thin bridge between zones, wiring only, no rigid components.
- Rationale: keeps wrist joint low-profile for daily wear/hand movement; pushes mass up the forearm, away from the wrist.

**Renders produced (6 panels):** hero (worn, annotated), isolated product (3/4 view), Velcro detail, USB-C port detail, internal two-zone cutaway, profile/side silhouette.

**Verification notes against prompt spec:**
- All 4 required renders present, plus 2 additional (internal cutaway, profile) — not requested but consistent with the stated requirement that renders show the zone width differential.
- Zone labeling correctly split (IMU/wrist vs. ESP32+battery+charge/forearm) per spec, rather than one combined callout.
- Negative-prompt compliance clean: no rivets, lacing, medieval styling, exposed screws.
- Minor deviation: shell finish reads slightly glossier/more specular than the specified matte TPU soft-touch in panels 2 and 4 (profile/product views) — cosmetic only, no dimensional or structural conflict.

**Open questions carried forward:**
- This is an aesthetic/form direction only — no dimensional validation against Action #8's locked wrist-worn/dorsal placement, no fit-check against WP 3.0 enclosure work (Sankalpa).
- Single-cavity packaging variant (from the same prompt session, pre-two-zone) was explored but not rendered/adopted — two-zone is the carried-forward direction.
- Not yet reconciled with actual PCB/battery vendor-confirmed footprints in BOM (`SPARK_BOM_Procurement.xlsx`) — dimensions used here are approximate placeholders from the prompt, not sourced from confirmed component datasheets.

---
