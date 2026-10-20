# Hardware & CAD Engineer Task Briefing

**Assignee:** Sankalpa Lamsal (Roll 79039 / BEI)  
**Subsystem:** Mechanical Enclosure, 3D Parametric CAD, Power Architecture & DFM  
**Primary Directory:** [`dev_logs/design-assets/`](file:///f:/Aaradhya-Dev-Tamrakar/SPARK/dev_logs/design-assets/)  
**Last Updated:** October 20, 2026  
**Goal:** Deliver complete, sliced, 3D-printed, and assembled TPU 95A dorsal bracer enclosures housing physical SPARK hardware across simulation and real fabrication phases.

> [!NOTE]
> This guide was originally created during the Pre-Hardware / Software-in-the-Loop (SIL) phase (September 24, 2026).
> **§1–§3** cover CAD modeling, clearances, and slicing setup.
> **§4–§6** cover post-hardware physical fabrication, brass heat-set insert installation, harness integration, and drop-impact validation added October 20, 2026.

---

## 1. Why CAD Design Began in the SIL Phase
Standard electronic modules have precise manufacturer mechanical drawings and free 3D CAD models on **GrabCAD** and **3D ContentCentral**. Modeling the entire wearable housing in Fusion 360 ahead of time verified internal clearances and G-code toolpaths before physical silicon arrival.

---

## 2. Sankalpa's CAD & Slicing Action Checklist

### Task 1: Download Standard 3D CAD Component Models (STEP Files)
Download the exact 3D models for all BOM components to assemble inside your CAD environment:
1. **ESP32-S3 WROOM-1 DevKit**: Search GrabCAD for *"ESP32-S3 DevKitC-1"* ($25 \times 50 \times 7\text{ mm}$).
2. **TP4056 Type-C Charging Module**: Search GrabCAD for *"TP4056 USB-C"* ($15 \times 17 \times 2\text{ mm}$).
3. **MPU-6050 Breakout (GY-521)**: Search GrabCAD for *"GY-521 MPU6050"* ($20 \times 15 \times 3\text{ mm}$).
4. **1100 mAh LiPo Battery**: Model a rectangular pouch block ($32 \times 52 \times 7\text{ mm}$).

---

### Task 2: Parametric Modeling of the Two-Zone Dorsal Bracer
* **Reference Specifications:** [`dev_logs/design-assets/SPARK_270deg_C_Shell_Design_DI03.md`](file:///f:/Aaradhya-Dev-Tamrakar/SPARK/dev_logs/design-assets/SPARK_270deg_C_Shell_Design_DI03.md) and [`dev_logs/design-assets/enclosure_concept_v1_two_zone_bracer.png`](file:///f:/Aaradhya-Dev-Tamrakar/SPARK/dev_logs/design-assets/enclosure_concept_v1_two_zone_bracer.png).
* **Architecture Specifications:**
  * **Zone A (Wrist Hub, 36 mm length)**: Compact, low-profile housing directly over the dorsal wrist holding the MPU6050 flat against the wrist plane (minimizing motion artifact and lever-arm rotational whip). Friction-fit pocket with no metal screws.
  * **Spine Bridge (24 mm length)**: Flexible connecting channel carrying 4 silicone ribbon wires ($3.3\text{V}$, GND, SDA, SCL) from wrist to forearm.
  * **Zone B (Forearm Bay, 85 mm length)**: Wider housing mounted on the distal forearm holding the heavy components (ESP32-S3, 1100 mAh LiPo battery, and TP4056 charge board). Removable dorsal lid with screw fastening.
  * **Wrap Geometry**: 270° semi-rigid C-clamp profile ($75\%$ circumference wrap, 160 mm reference forearm) closed with a Velcro strap over a compression base-layer sleeve.
* **Wall Thickness & Fillets**:
  * Nominal shell wall: $3.5\text{ mm}$ (solid wall guaranteeing tear resistance in TPU 95A).
  * Local structural wall at screw bosses: $4.0\text{ mm}$.
  * Generous interior radii ($R \ge 1.5\text{ mm}$) to eliminate stress concentrations and delamination.

---

### Task 3: Design for Manufacture (DFM) & Fastener Fastening
* **Threaded Brass Heat-Set Inserts**:
  * 3D-printed TPU is flexible; standard self-tapping screws will strip the threads after 2–3 maintenance openings.
  * Model cylindrical mounting bosses designed for **M2.5 brass heat-set inserts**.
  * Boss outer diameter must be at least $2\times$ the insert outer diameter ($>4.5\text{ mm}$) with a $0.5\text{ mm}$ lead-in chamfer.
* **Dual USB-C Port Access (Off-Body Only)**:
  * Model dual cutouts: Port 1 for ESP32-S3 firmware flashing, Port 2 for TP4056 charging.
  * Recess ports by $1.5\text{ mm}$ with a protective snap-fit gasket to keep out sweat and dust.

---

### Task 4: Slicing Configuration in PrusaSlicer / Cura (TPU 95A)
* **Material:** Polymaker PolyFlex TPU 95A or KEC Makerspace TPU 95A.
* **Slicer Setup Parameters:**
  * Nozzle Diameter: $0.4\text{ mm}$
  * Layer Height: $0.20\text{ mm}$
  * Print Speed: $20\text{--}25\text{ mm/s}$ (slow speed is critical for flexible filament to prevent extruder jamming)
  * Infill: $25\%$ Gyroid (provides multidirectional flexibility without delamination)
  * Retraction: Disabled or limited to $\le 1.0\text{ mm}$ at $20\text{ mm/s}$ (prevents flexible filament wrapping around feeder gears)
* **Validation:** Slice the model and record:
  * Total print time (estimated $4.5\text{--}6.5\text{ hours}$).
  * Total filament mass (must verify within $20\text{--}25\text{ grams}$, matching the $\sim\text{NPR }90$ BOM estimate).

---

## 3. SIL-Phase Defense Questions (Pre-Hardware)

> These Q&As cover the CAD modeling rationale. See **§6** for the full defense questions including fabrication and physical validation.

---

## 4. Post-Hardware Physical Fabrication & Assembly (Phase 2)

> **Context:** Physical ESP32-S3 boards, MPU6050 breakouts, TP4056 modules, LiPo cells, and KEC Makerspace TPU filament are available.

### Task 5: 3D Print at KEC Makerspace & Mass Verification
* **Objective:** Print the final `.stl` file using KEC Makerspace TPU 95A (Black).
* **Execution:**
  1. Transfer sliced `.gcode` to the Makerspace 3D printer (e.g., Creality Ender-3 S1 with direct-drive extruder or Prusa i3 MK3S+).
  2. Inspect first-layer adhesion (bed at 50–60°C, nozzle at 220–230°C).
  3. Weigh the completed shell on a precision lab balance.
* **Acceptance Criteria:** 
  - Complete print with zero layer separation, stringing cleaned, and flexible hinge functioning.
  - Measured weight is within $20\text{--}25\text{ grams}$ ($\le\text{NPR }100$ material cost).

---

### Task 6: Brass Heat-Set Insert Installation
* **Objective:** Install 4–6 M2.5 threaded brass inserts into the forearm bay bosses.
* **Tools:** Temperature-controlled soldering iron set to $210\text{--}220^\circ\text{C}$ (slightly below TPU melting point to prevent burning).
* **Execution:**
  1. Place M2.5 insert squarely on the boss lead-in chamfer.
  2. Apply gentle vertical pressure with the soldering iron tip until the top of the insert sits flush with the boss surface.
  3. Allow 2 minutes cooling before threading screws.
* **Acceptance Criteria:** Screws thread smoothly with zero wobble; inserts withstand $1.5\text{ Nm}$ torque without spinning in the TPU.

---

### Task 7: Physical Component Dry-Fit & Wiring Harness Assembly
* **Objective:** Fit all 4 physical modules and wire the internal harness.
* **Assembly Steps:**
  1. Press MPU6050 into Zone 1 (dorsal wrist pocket). Verify it sits dead-flat without tilting.
  2. Route 4-wire flexible silicone ribbon cable ($30\text{ AWG}$) through the 24 mm spine bridge to Zone 2.
  3. Mount ESP32-S3 WROOM-1, 1100 mAh LiPo battery, and TP4056 board in Zone 2.
  4. Solder power leads: LiPo $\to$ TP4056 `BAT+`/`BAT-`, TP4056 `OUT+`/`OUT-` $\to$ ESP32-S3 `5V`/`GND`.
  5. Fasten removable dorsal lid with M2.5 button-head screws.
* **Acceptance Criteria:** All boards securely seated; USB-C ports accessible from outside; lid closes flush without pinching wires.

---

### Task 8: Mechanical Drop-Impact & Wearability Test
* **Objective:** Validate impact resilience and ergonomic comfort before clinical trials.
* **Execution:**
  1. Fasten the assembled unit to a mannequin arm or volunteer wrist with the Velcro strap over a compression sleeve.
  2. Perform 5 drop tests from $1.5\text{ meters}$ onto high-density gym crash mats (simulating fall impacts).
  3. Inspect for enclosure cracks, shifted internal boards, or loose solder joints.
* **Acceptance Criteria:** Zero structural failure, MPU6050 maintains rigid orientation reference, electronics remain fully operational.

---

## 5. Cohort Data Collection Support (Phase 3)

### Task 9: Enclosure Maintenance & Spare Straps for KEC Trials
* **Objective:** Support on-site cohort trials (12–20 subjects) with clean, sanitized, and adjustable wearable hardware.
* **Checklist:**
  - [ ] 2 sets of Velcro wrist straps (RR-papers, NPR 500) washed and ready.
  - [ ] 2 compression arm sleeves for hygiene isolation between participants.
  - [ ] Alcohol wipes for surface sanitization of the TPU shell between trials.
  - [ ] Allen key / screwdriver on hand for rapid battery inspection.
* **Acceptance Criteria:** Smooth subject turnaround during the 34-activity crash-mat trials without hardware downtime.

---

## 6. Defense Questions Sankalpa Must Be Prepared to Answer (Updated)

**Q1: "Why split the wearable into two zones instead of putting everything in a single wrist watch enclosure?"**  
* **Answer:** *"Placing the heavy 1100 mAh LiPo battery (~25g) and ESP32-S3 on the wrist creates significant rotational inertia and wrist fatigue for elderly users, causing severe false-positive impact spikes when the arm swings. Moving the battery and MCU to the forearm zone leaves only the lightweight MPU6050 (<2g) on the dorsal wrist, optimizing biomechanical stability."*

**Q2: "Why choose TPU 95A filament over standard PLA or ABS?"**  
* **Answer:** *"PLA is brittle and cracks upon ground impact during a fall. ABS requires a high-temperature heated chamber and emits toxic styrene fumes. TPU 95A is a thermoplastic polyurethane with high impact energy absorption, Shore 95A flexibility for comfortable anatomical wrist fit, and extreme fatigue resistance for repeated daily flexing."*

**Q3: "How do you ensure user electrical safety during battery charging?"**  
* **Answer:** *"We enforce an architectural off-body charging constraint. The enclosure uses dual single-purpose USB-C ports recessed behind an access hatch. The device is physically detached from the arm before plugging into mains power, eliminating any mains leakage path to the user."*

**Q4: "Why did you use brass heat-set inserts instead of tapping screws directly into the 3D-printed plastic?"**  
* **Answer:** *"TPU has low shear modulus and high elasticity. Self-tapping screws in TPU either strip threads immediately or relax over time due to viscoelastic creep, causing internal electronics to rattle loose. M2.5 brass heat-set inserts melt into the boss walls to form permanent, rigid mechanical threads capable of dozens of battery inspection cycles."*

**Q5: "How does the flexible spine accommodate wrist flexion and extension without breaking the wiring?"**  
* **Answer:** *"The spine bridge is a 24 mm long, 2 mm thick single-curvature TPU hinge with generous 1.5 mm strain-relief fillets. Inside, we run ultra-flexible 30 AWG stranded silicone-jacketed wires with an intentional 5 mm S-curve expansion loop. This accommodates the full 70° dorsal wrist extension during a forward slip without placing tensile strain on solder pads."*
