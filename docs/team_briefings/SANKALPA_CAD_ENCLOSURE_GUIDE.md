# Hardware & CAD Engineer Task Briefing (Pre-Hardware Phase)

**Assignee:** Sankalpa Lamsal (Roll 79039 / BEI)  
**Subsystem:** Mechanical Enclosure, 3D Parametric CAD, Power Architecture & DFM  
**Primary Directory:** [`dev_logs/design-assets/`](file:///f:/Aaradhya-Dev-Tamrakar/SPARK/dev_logs/design-assets/)  
**Goal:** Deliver complete, sliced, and fabrication-ready 3D CAD models of the TPU 95A dorsal bracer before physical components arrive.

---

## 1. Why You Don't Need Physical Components Yet
Standard electronic modules have precise manufacturer mechanical drawings and free 3D CAD models on **GrabCAD** and **3D ContentCentral**. You can model the entire wearable housing, verify component clearances, and slice the G-code toolpaths right now.

---

## 2. Sankalpa's Action Checklist

### Task 1: Download Standard 3D CAD Component Models (STEP Files)
Download the exact 3D models for all BOM components to assemble inside your CAD environment:
1. **ESP32-S3 WROOM-1 DevKit**: Search GrabCAD for *"ESP32-S3 DevKitC-1"* ($25 \times 50 \times 7\text{ mm}$).
2. **TP4056 Type-C Charging Module**: Search GrabCAD for *"TP4056 USB-C"* ($15 \times 17 \times 2\text{ mm}$).
3. **MPU-6050 Breakout (GY-521)**: Search GrabCAD for *"GY-521 MPU6050"* ($20 \times 15 \times 3\text{ mm}$).
4. **1100 mAh LiPo Battery**: Model a rectangular pouch block ($32 \times 52 \times 7\text{ mm}$).

---

### Task 2: Parametric Modeling of the Two-Zone Dorsal Bracer
* **Reference Concept:** [`docs/SPARK_Proposal/Figures/enclosure_concept_v1_two_zone_bracer.png`](file:///f:/Aaradhya-Dev-Tamrakar/SPARK/docs/SPARK_Proposal/Figures/enclosure_concept_v1_two_zone_bracer.png)
* **Architecture Specifications:**
  * **Zone A (Wrist Hub)**: Compact, low-profile housing directly over the dorsal wrist holding the MPU6050 flat against the wrist plane (minimizing motion artifact and lever-arm rotational whip).
  * **Spine Bridge**: Flexible connecting channel carrying 4 silicone ribbon wires ($3.3\text{V}$, GND, SDA, SCL) from wrist to forearm.
  * **Zone B (Forearm Bay)**: Wider housing mounted on the distal forearm holding the heavy components (ESP32-S3, 1100 mAh LiPo battery, and TP4056 charge board).
  * **Wrap Geometry**: 270° semi-rigid C-clamp profile ($75\%$ circumference wrap) closed with a Velcro strap over a compression base-layer sleeve.
* **Wall Thickness & Fillets**:
  * Minimum shell wall: $2.0\text{ mm}$ (guarantees tear resistance in TPU 95A).
  * Generous interior radii ($R \ge 1.5\text{ mm}$) to eliminate stress concentrations.

---

### Task 3: Design for Manufacture (DFM) & Fastener Fastening
* **Threaded Brass Heat-Set Inserts**:
  * 3D-printed TPU is flexible; standard self-tapping screws will strip the threads after 2–3 maintenance openings.
  * Model cylindrical mounting bosses designed for **M2 / M2.5 brass heat-set inserts**.
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

## 3. Defense Questions Sankalpa Must Be Prepared to Answer

**Q1: "Why split the wearable into two zones instead of putting everything in a single wrist watch enclosure?"**  
* **Answer:** *"Placing the heavy 1100 mAh LiPo battery ($~25\text{g}$) and ESP32-S3 on the wrist creates significant rotational inertia and wrist fatigue for elderly users, causing severe false-positive impact spikes when the arm swings. Moving the battery and MCU to the forearm zone leaves only the lightweight MPU6050 ($<2\text{g}$) on the dorsal wrist, optimizing biomechanical stability."*

**Q2: "Why choose TPU 95A filament over standard PLA or ABS?"**  
* **Answer:** *"PLA is brittle and cracks upon ground impact during a fall. ABS requires a high-temperature heated chamber and emits toxic styrene fumes. TPU 95A is a thermoplastic polyurethane with high impact energy absorption, Shore 95A flexibility for comfortable anatomical wrist fit, and extreme fatigue resistance for repeated daily flexing."*

**Q3: "How do you ensure user electrical safety during battery charging?"**  
* **Answer:** *"We enforce an architectural off-body charging constraint. The enclosure uses dual single-purpose USB-C ports recessed behind an access hatch. The device is physically detached from the arm before plugging into mains power, eliminating any mains leakage path to the user."*
