# SPARK — Design Ideas Log

Exploratory design concepts, external render outputs, and aesthetic direction notes.
**Not implementation-locked.** Cross-reference `SPARK_TRACKER.md` Action #8 (enclosure form factor) for the resolved engineering decision this log feeds into.

---

## DI-01 — Bracer-Silhouette Enclosure, Two-Zone Internal Layout

- **Status:** Exploratory concept. Not adopted into BOM/CAD.
- **Date logged:** 2026-08-06
- **Asset:** `dev_logs/design-assets/enclosure_concept_v1_two_zone_bracer.png`
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
---

## DI-02 — Master Composite Design Sheet (Two-Zone Ergonomic Dorsal Bracer)

- **Status:** Canonical Design Concept & CAD Blueprint Reference.
- **Date logged:** 2026-08-20
- **Asset:** [`dev_logs/design-assets/SPARK_Two_Zone_Bracer_Design_Concept_v2.jpg`](file:///D:/Aaradhya-Dev-Tamrakar/SPARK/dev_logs/design-assets/SPARK_Two_Zone_Bracer_Design_Concept_v2.jpg)
- **Visuals Included:**
  1. **Hero Render (Panel 1)**: Dorsal forearm wearable worn over compression sleeve, demonstrating $75\%$ wrap geometry, $25\text{–}30\%$ continuous open ventilation seam, matte soft-touch TPU 95A finish, and ergonomic wrist curvature.
  2. **Product Render (Panel 2)**: Single-piece ergonomic shell with seamless inner curvature and senior-friendly Velcro anchor slot.
  3. **Closure Detail (Panel 3)**: Wide hook-and-loop Velcro strap with recessed, flush anchors for skin safety.
  4. **Charging Port Detail (Panel 4)**: USB-C port with flexible hinged TPU dust/splash cover and hidden status LED indicator.
  5. **Internal Two-Zone Layout (Panel 5)**:
     - **Zone 1 (Slim Wrist Zone)**: Dedicated MPU6050 IMU bay ($\approx 15 \times 20 \times 3\text{ mm}$) anchored directly over the dorsal wrist reference.
     - **Connecting Spine**: Flexible wiring bridge routing 4-conductor I2C harness without rigid components.
     - **Zone 2 (Forearm Bay)**: Main electronics housing ESP32-S3 Dev Board ($\approx 25 \times 50 \times 7\text{ mm}$), $1000\text{–}1100\text{ mAh}$ LiPo battery ($\approx 32 \times 52 \times 7\text{ mm}$), and TP4056 charge/protect module ($\approx 15 \times 17 \times 2\text{ mm}$).
  6. **Side Profile View (Panel 6)**: Tapered elevation showing ultra-slim wrist clearance and elevated electronics chamber.

---

## DI-03 — Canonical 270° C-Shell Enclosure (Merged ChatGPT + Gemini)

- **Status:** **Canonical Engineering Reference** — supersedes DI-01 and DI-02.
- **Date logged:** 2026-08-22
- **Primary asset:** [`dev_logs/design-assets/SPARK_270deg_C_Shell_Design_DI03.md`](file:///D:/Aaradhya-Dev-Tamrakar/SPARK/dev_logs/design-assets/SPARK_270deg_C_Shell_Design_DI03.md)
- **Render assets:**
  - [`enclosure_concept_v2_gemini_270deg.jpg`](file:///D:/Aaradhya-Dev-Tamrakar/SPARK/dev_logs/design-assets/enclosure_concept_v2_gemini_270deg.jpg) — Gemini exploded/assembly render
  - [`enclosure_concept_v2_chatgpt_270deg.jpg`](file:///D:/Aaradhya-Dev-Tamrakar/SPARK/dev_logs/design-assets/enclosure_concept_v2_chatgpt_270deg.jpg) — ChatGPT orthographic design sheet
- **Source:** Parallel ChatGPT + Gemini design explorations from the same engineering prompt, best elements merged and validated against Track 10 DFM research.

**Concept summary:**
270° C-shaped cross-section (NOT full wraparound bracer). Three-quarter forearm coverage with 90° open ventral gap bridged by a single wide Velcro strap. Three-part mechanical architecture: main C-shell + removable Zone 2 dorsal lid + replaceable proximal USB port insert.

**Key design decisions resolved:**
- **Zone 1 IMU mounting:** Friction-fit pocket with 0.2–0.4 mm interference ribs — no screws (too thin for bosses per Track 10).
- **Zone 2 component layout:** Lateral distribution using 270° arc width, not vertical stacking, to minimize profile height.
- **Screw bosses:** 4–6× M2.5 in Zone 2 only. 9 mm OD, 6–7 mm blind standoff. Heat-set insert contingency designed in.
- **USB panel:** Replaceable modular insert (two versions: dual USB-C or USB-C + Micro-USB) resolving TP4056 connector TBD.
- **LED visibility:** Locally thinned TPU (3.5 → 0.8 mm) as diffuser — no separate light pipe.
- **Print orientation:** Vertical (Z-axis along forearm axis), support-free design with 45° chamfers.

**Updated cost estimate (3.5 mm walls):** ~70–75 cm³, ~85–91 g, NPR 360–400 (8–11 hr print). Previous 18.5 cm³ / NPR 90 estimate invalidated.

**Open blockers before Fusion 360:**
1. ⚠ ESP32-S3 power input path (TP4056 outputs raw 3.0–4.2V, not regulated 5V).
2. TP4056 connector type confirmation.
3. Exact ESP32-S3 board caliper measurements.
4. TPU 95A screw test coupon.

---
