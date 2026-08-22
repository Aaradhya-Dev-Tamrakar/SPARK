# SPARK — DI-03: Canonical 270° C-Shell Enclosure Design Reference

**Status:** Canonical Engineering Reference — supersedes DI-01/DI-02.
**Date:** 2026-08-22
**Source:** Merged from parallel ChatGPT + Gemini design explorations, validated against Track 10 DFM research and locked BOM.
**Render assets:**

- [`enclosure_concept_v2_gemini_270deg.jpg`](file:///D:/Aaradhya-Dev-Tamrakar/SPARK/dev_logs/design-assets/enclosure_concept_v2_gemini_270deg.jpg) — Gemini exploded/assembly render
- [`enclosure_concept_v2_chatgpt_270deg.jpg`](file:///D:/Aaradhya-Dev-Tamrakar/SPARK/dev_logs/design-assets/enclosure_concept_v2_chatgpt_270deg.jpg) — ChatGPT orthographic design sheet

---

## 1. Architecture Summary

A **single continuous 270° C-shaped TPU 95A shell** with a removable dorsal electronics lid and a replaceable proximal port insert. Two-zone internal layout connected by a flexible wiring spine.

```
            PROXIMAL / ELBOW
                  ↑
       ┌────────────────────────┐
       │     USB SERVICE PANEL  │  ← Replaceable port insert
       │    PROG   |   CHARGE  │
       ├────────────────────────┤
       │                        │
       │       ZONE 2           │  ← Electronics bay (ESP32, LiPo, TP4056)
       │    85 mm long          │     Removable dorsal lid, 4–6 M2.5 screws
       │                        │
       └──────────┬─────────────┘
                  │
            FLEXIBLE SPINE       ← 24 mm, 4-wire I2C channel
                  │
       ┌──────────┴─────────────┐
       │       ZONE 1           │  ← Sensor island (MPU6050 only)
       │    36 mm long          │     Friction-fit pocket, NO screws
       └────────────────────────┘
                  ↓
            DISTAL / HAND

              ╲            ╱
               ╲          ╱
                ╲________╱
                 90° GAP        ← Velcro strap bridges here
```

---

## 2. Envelope Dimensions

| Parameter | Value |
|---|---|
| **Overall axial length** | 145 mm |
| Zone 1 (wrist) | 36 mm |
| Flexible spine | 24 mm |
| Zone 2 (forearm) | 85 mm |
| **Reference forearm circumference** | 160 mm |
| Inner radius at reference section | 25.46 mm |
| **Shell coverage** | 270° |
| **Ventral opening** | 90° (~40 mm gap) |
| **Nominal shell wall** | 3.5 mm |
| Local structural wall (bosses, strap slots) | 4.0 mm |
| Minimum skin-contact edge radius | ≥2.0 mm |
| General external fillets | 2–4 mm |
| Strap width | 35–40 mm |

---

## 3. Three-Part Mechanical Architecture

### Part A — Main C-Shell (single print)

The continuous 270° forearm shell containing:

- Zone 1 sensor island (integral)
- Flexible spine with cable channel (integral)
- Zone 2 lower electronics tray (integral)
- Ventral strap slots (integral)
- Screw bosses around Zone 2 perimeter (integral)

### Part B — Dorsal Electronics Lid

A shallow curved lid covering only Zone 2. Contains:

- Screw recesses (counterbored, flush exterior)
- LED diffusion windows (locally thinned to 0.8 mm)
- Camera FPC connector keepout pocket
- Flush cosmetic surface

### Part C — Replaceable Port Insert

A small modular proximal panel for the dual USB-C interface. **Two versions can be printed** to resolve the TP4056 USB-C vs. Micro-USB TBD:

```
VERSION A                        VERSION B
┌──────────────────────┐         ┌──────────────────────┐
│ USB-C       USB-C    │         │ USB-C       MICRO-USB│
│ PROG        CHARGE   │         │ PROG        CHARGE   │
└──────────────────────┘         └──────────────────────┘
```

---

## 4. Zone 1 — IMU Sensor Island (No Screws)

Zone 1 is too thin for M2.5 screw bosses (DFM Track 10 confirmed). The MPU6050 is held by a **friction-fit pocket with TPU retention ribs**.

### Pocket Spec

| Feature | Dimension |
|---|---|
| PCB nominal | 15 × 20 × 3 mm |
| Pocket internal | 15.5 × 20.5 × 3.6 mm |
| Lateral clearance | 0.25 mm/side |
| Pocket floor (skin-facing wall) | 3.5–4.0 mm solid |
| Retention lip / rail preload | 0.2–0.4 mm compression |
| Sensor island width | ~27–30 mm |
| Sensor island length | ~31–34 mm |

### Retention Method

Two low-profile TPU retention rails along the long edges. The IMU slides in laterally and is held by interference fit. A snap-in TPU retention cap on the lid side applies gentle vertical compression.

```
TOP VIEW OF IMU POCKET

       20.5 mm
   ┌───────────────┐
   │ ┌───────────┐ │
   │ │           │ │
   │ │ MPU6050   │ │  ← 0.2–0.4 mm interference fit
   │ │           │ │
   │ └───────────┘ │
   │ ▲           ▲ │
   │ retention   │ │
   │ rails       │ │
   └───────────────┘
         15.5 mm
```

### Cross-Section A-A (Through Zone 1)

```
                 DORSAL / OUTSIDE
                       ↑
                 ┌───────────┐
                 │  3.5 mm   │  ← outer wall
           ╭─────┴───────────┴─────╮
          /    sensor island        \
         /   ┌──────────────┐        \
        │    │   MPU6050    │         │
        │    │ 15×20×3 mm   │         │     270° arc
        │    └──────────────┘         │     R_inner = 25.46 mm
        │      retention ribs         │
         \                           /
          \_________________________/
       [Slot]                   [Slot]  ← strap pass-through
       ──────                   ──────
       : : : : : : : : : : : : : : :   ← 90° ventral gap (~40 mm)

       Total Zone 1 Height: ~10.0 mm
       Arc Width: ~52 mm
```

> **Do not glue the IMU.** A mechanically constrained pocket gives serviceable access and avoids adhesive creep.

---

## 5. Connecting Spine

A flexible cable tunnel, not a miniature enclosure.

| Feature | Value |
|---|---|
| Spine axial length | 24 mm |
| Nominal wall | 3.0–3.5 mm |
| Cable channel width | 6–8 mm |
| Cable channel height | 2.0–2.5 mm |
| Minimum bend radius | ≥8 mm |
| Cable exit radius | ≥2 mm |
| Flex relief grooves | 3 slots, 1.0 mm radius (lateral) |

### Cross-Section B-B (Through Spine)

```
                 DORSAL / OUTSIDE
                       ↑
               ╭──────────────╮
             ╭─┤  3.0–3.5 mm  ├─╮
            /  │               │  \
           │   │ ┌───────────┐ │   │
           │   │ │ SDA SCL   │ │   │     I2C wireway: 6 × 2.5 mm
           │   │ │ VCC GND   │ │   │     30 AWG silicone stranded
           │   │ └───────────┘ │   │
            \  │               │  /
             ╰─┴───────────────┴─╯
                   OPEN GAP

           Overall: 58 mm W × ~7.5 mm H
```

Strain relief at each end: 1–2 mm TPU cable-retention bridge. 15 mm S-bend loop inside Zone 2 absorbs flex displacement.

---

## 6. Zone 2 — Electronics Bay

### Component Arrangement: Lateral, Not Stacked

Use the 270° arc width to distribute ESP32 and LiPo laterally, keeping Zone 2 thinner.

### Component Pockets

| Component | Pocket Dimensions | Notes |
|---|---|---|
| LiPo battery | 33.5 × 54 × 7.8 mm | 1.0–1.5 mm TPU perimeter buffer. Retained by edge lips, NOT clamped on faces. |
| ESP32-S3 board | 26.5 × 52 × 8 mm | Mounted on internal shelf. 2× M2.5 screws into standoffs. |
| TP4056 module | 16 × 18 × 3 mm | Proximal alignment slot near USB panel. |

### Camera FPC Keepout: 1.5–2.0 mm radial clearance with surrounding TPU shield.

### Thermal Isolation: 1.5 mm internal TPU separator between LiPo and TP4056.

### Cross-Section C-C (Through Zone 2)

```
                    DORSAL / OUTSIDE
                          ↑
                ┌──────────────────┐
                │  curved TPU lid  │  ← 2.5–3.0 mm
         ╭──────┴──────────────────┴──────╮
        /    ESP32-S3 (7 mm)     TP4056    \
       │                          (2 mm)    │
       │     ┌──────────────────────┐       │     270° arc
       │     │ 1100 mAh LiPo (7mm) │       │     R_inner = 27.5 mm
       │     └──────────────────────┘       │     Wall: 3.5–4.0 mm
        \   [thermal separator 1.5 mm]     /
         ╲________________________________╱
      [Slot]                          [Slot]
      : : : : : : : : : : : : : : : : : : :  ← 90° ventral gap

      Zone 2 Height: ~22.5 mm | Arc Width: ~62–68 mm
```

---

## 7. Shell Join — Screw Bosses (Zone 2 Only)

4–6 hidden M2.5 screws. None in Zone 1.

| Parameter | Value |
|---|---|
| Boss OD | 9.0 mm |
| Pilot hole | 2.1 mm |
| Thread engagement | 6–7 mm |
| Solid bottom | ≥1.0 mm |
| Boss-to-edge | ≥4.0 mm |
| Fillet | 1.5–2.0 mm |

**Heat-set insert contingency**: Ream to 3.2 mm, install M2.5 brass inserts at 210°C if self-tapping strips. Test coupon first.

---

## 8. Velcro Strap System

Two pairs of pass-through slots (42 × 4.5–5.0 mm, 2.0–2.5 mm end radius, 4.0 mm local wall) at ventral edges. One pair per zone. Single 35–40 mm hook-and-loop strap. One side permanently anchored, free end has 25–30 mm pull tab for elderly one-handed operation.

---

## 9. External USB Interface

Dual ports on proximal end cap. Port differentiation via three cues:

| Cue | PROG (ESP32) | CHARGE (TP4056) |
|---|---|---|
| Position | Upper / left | Lower / right |
| Label | Debossed "PROG" | Debossed "CHG" + battery icon |
| Dust flap tab | Small rectangular | Larger circular |

Integral TPU dust covers via 0.8–1.0 mm living hinge. Splash resistant only — do not claim waterproofing.

---

## 10. LED Visibility

Two ~3 × 5 mm windows on dorsal lid, locally thinned from 3.5 → 0.8 mm. Dark TPU at 0.8 mm transmits red/blue LED light effectively. No separate light pipe needed.

---

## 11. Fusion 360 Modeling Workflow

| Step | Operation | Key Value |
|---|---|---|
| 1 | Draw forearm circle | Ø50.93 mm |
| 2 | Create 270° arc | R_i = 25.46 mm |
| 3 | Offset outward | 3.5 mm → R_o = 28.96 mm |
| 4 | Extrude | 145 mm |
| 5 | Taper Zone 1→Spine | Gradual, no step |
| 6 | Zone 2 bulge | +5–8 mm outward |
| 7 | Shell / hollow | Interior cavities |
| 8 | Add features | Bosses, slots, pockets, ports |

---

## 12. Print Strategy

**Orientation**: Vertical (forearm axis along Z). Minimal support needed. 270° perimeter is self-supporting.

| Parameter | Value |
|---|---|
| Layer height | 0.20 mm |
| Nozzle temp | 230°C |
| Bed temp | 60°C |
| Speed | 25–30 mm/s |
| Perimeters | 7–9 |
| Infill | 10–15% Gyroid |
| Supports | Ideally 0% |
| Brim | 5–10 mm |

All internal ceilings chamfered ≥45°. Strap slots use teardrop profiles. Bosses print vertically.

---

## 13. Assembly Sequence

1. **Inspect** printed parts (warps, blocked ports, rough channels)
2. **Install MPU6050** into Zone 1 friction pocket — verify no rocking
3. **Route I2C cable** (pre-soldered 70 mm, 28–30 AWG silicone) through spine → Zone 2
4. **Seat LiPo** in perimeter pocket — route leads through dedicated channel
5. **Mount ESP32-S3** on shelf — align USB-C — 2× M2.5 screws into standoffs
6. **Slide TP4056** into end-cap alignment slot — align USB with port insert
7. **Connect harnesses** (I2C → ESP32 GPIOs; LiPo → TP4056; TP4056 OUT → ESP32 ⚠ verify voltage)
8. **Close lid** — star-pattern screw tightening (4–6× M2.5), max 0.15 Nm
9. **Install port insert** and dust covers
10. **Thread Velcro strap** through all four slots

---

## 14. Volume, Mass & Cost

| Wall | Volume | Mass | Cost (NPR 4/g) |
|---|---|---|---|
| 3.0 mm | ~55.3 cm³ | ~66.9 g | ~NPR 268 |
| **3.5 mm** | **~65.1 cm³** | **~78.8 g** | **~NPR 315** |
| 4.0 mm | ~75.1 cm³ | ~90.8 g | ~NPR 363 |

**Realistic prototype (3.5 mm + features)**: ~70–75 cm³, ~85–91 g, **NPR 360–400** incl. waste. Print time: **8–11 hours**.

> ⚠ The earlier 18.5 cm³ / NPR 90 estimate is invalidated. Update thesis BOM.

---

## 15. Open Design Decisions (Resolve Before Final CAD)

### ⚠ CRITICAL: ESP32-S3 Power Input Path

TP4056 outputs raw LiPo voltage (3.0–4.2V), not regulated 5V. Confirm the ESP32-S3 board's acceptable battery input pin before wiring. May need a boost converter.

### TP4056 Connector Type

Resolved by replaceable port insert. Confirm physical module before Fusion 360 parameter lock.

### Exact ESP32-S3 Board Dimensions

Measure with calipers: USB-C location, FPC height, mounting holes, antenna keepout, reset/boot buttons, underside clearance.

### Screw Test Coupon

Print test boss in actual TPU 95A stock. Torque-test M2.5 × 8 mm screw before committing CAD geometry.

---

## 16. Mechanical BOM (Enclosure-Specific)

| Part | Qty | Material | Purpose |
|---|---|---|---|
| Main C-shell | 1 | TPU 95A | Structural enclosure |
| Electronics lid | 1 | TPU 95A | Zone 2 cover |
| Port insert | 1 | TPU 95A | Replaceable USB panel |
| Velcro strap | 1 | Hook-and-loop, 35–40 mm | One-handed closure |
| M2.5 × 8 mm screws | 6–8 | Metal (from BOM) | Shell/lid attachment |

Integral features (no separate parts): IMU retention rails, cable strain reliefs, battery retainer lips, thermal separator, LED diffuser windows.

---

*Canonical reference for Action #17 CAD work. Cross-ref: Track 10 DFM in [`SPARK_research_board_merged.md`](file:///D:/Aaradhya-Dev-Tamrakar/SPARK/docs/SPARK_research_board_merged.md), BOM in [`SPARK_Component_Order_Form.xlsx`](file:///D:/Aaradhya-Dev-Tamrakar/SPARK/docs/SPARK_Component_Order_Form.xlsx).*
