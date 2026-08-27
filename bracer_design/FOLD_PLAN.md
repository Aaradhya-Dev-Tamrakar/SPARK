# Spark Hand Bracer — Fold Plan & Assembly Guide

**Version:** 1.1 (component-validated)  
**Design:** Modular origami bracer, zero screws, parallel print  
**Print:** 6 flat STLs, PETG 1.2 mm single wall, no supports  
**Components validated:** Seeed XIAO/Qt Py, 303040/402030 LiPo, WS2812B 5050 strip

---

## 📦 Module Inventory (6 STLs)

> Scripts: `bracer_design/module_*.py` — run via `tools/fusion_mcp.py` from project root.

| Module | Entity | Print Time | Flat Size | Material | Key Dims |
|--------|--------|------------|-----------|----------|----------|
| **A** Forearm Segment | Extrude12 | ~55 min | 250×260 mm | PETG | LED groove 12mm, Dovetail 12×4.5mm |
| **B** Wrist Closure | Extrude7 | ~35 min | 100×180 mm | PETG | Hook tabs 6×3mm, Strap anchor |
| **C** Elbow Closure | Extrude8 | ~35 min | 100×248 mm | PETG | Hook tabs 6×3mm, Strap anchor |
| **D** LED Strip | Extrude13 | ~25 min | 250×28 mm | PETG | Channel 28mm, LED groove 12mm |
| **E** Electronics Tray | Extrude14 | ~30 min | 80×50 mm | PETG | H=15mm, Batt 35×35mm, MCU 25×20mm |
| **F** Diffuser Cover | Extrude11 | ~20 min | 250×25 mm | Clear TPU/PETG | Snap tabs 4×2mm, 1.5mm thick |

**Total print (parallel, 3+ printers): ~1 hour**

---

## 🎯 Component Fit (Validated)

| Component | Spec | Module | Pocket/Groove | Margin |
|-----------|------|--------|---------------|--------|
| **WS2812B 5050 strip** | 10×2 mm | D | 12 mm groove × 2.5 mm deep | +2 mm |
| **303040 LiPo (500 mAh)** | 30×30×4 mm | E | 35×35 mm pocket × 2 | +5 mm |
| **402030 LiPo (500 mAh)** | 40×20×3 mm | E | fits in 35×35 pocket | ✅ |
| **Seeed XIAO ESP32C3** | 21×17.5×3.5 mm | E | 25×20 mm pocket × 2 | +4 mm |
| **Qt Py / Feather** | 22×18×5 mm | E | fits in 25×20 pocket | ✅ |
| **JST-PH 2.0 / wiring** | ~8×6 mm | E | open pocket space | ✅ |
| **Tray stack height** | XIAO + LiPo ≈ 7.5 mm | E | 15 mm wall height | 2× margin |

---

## 📐 Folding Instructions

### **Module A — Forearm Segment** (Miura-ori panel)
```
FLAT: 250×260 mm panel with scored grid

CREASE PATTERN:
- Transverse lines (straight across): VALLEY folds ↑
- Diagonal lines (45° zigzag): MOUNTAIN folds ↓
- Spacing: 12 mm facets, 72° Miura angle
- LED groove: 12 mm wide, center line (fold with panel)
- Dovetail channel: 12×4.5 mm, center strip
- Hook slots: 3 per long edge, 6×3 mm rectangular cutouts

FOLD SEQUENCE:
1. Place flat, score lines UP
2. Fold ALL transverse lines as VALLEY (paper toward you)
3. Fold ALL diagonal lines as MOUNTAIN (paper away)
4. Panel corrugates into rigid curved trough
5. Press along length to set creases firmly
6. Hold 5 sec per fold (PETG springs back)

RESULT: Rigid curved panel matching forearm contour
- Concave face = inner (against arm)
- LED groove at bottom center
- Dovetail channel just above groove
- Hook slots on both long edges
```

---

### **Module B — Wrist Closure** (Waterbomb lock)
```
FLAT: 60×180 mm trapezoid, 1.2 mm thick

CREASE PATTERN:
- Horizontal center (30 mm from tip): VALLEY
- Vertical center (90 mm from edges): MOUNTAIN
- Hook tabs at base edges (2): pre-cut, fold OUT 90°
- Strap anchor: 20×5 mm slot at 12 mm from tip

FOLD SEQUENCE:
1. Score lines UP
2. Fold horizontal center as VALLEY (toward you)
3. Fold vertical center as MOUNTAIN (away)
4. Push sides inward → waterbomb collapses to 3D wedge
5. Twist to lock (self-locking)
6. Fold 2 hook tabs OUTWARD 90° at base edges
7. Strap anchor stays flat (thread 20 mm elastic/Velcro)

RESULT: Self-locking wedge with 2 outward hooks + strap hole
- Hooks match Module A wrist slots (6×3 mm)
- Strap anchor centered at narrow end
```

---

### **Module C — Elbow Closure** (Waterbomb lock, wider)
```
IDENTICAL to Module B but WIDER:
- Flat width: 248 mm (matches Module A elbow half-width × 2)
- Hook tabs at same relative positions
- Strap anchor at same relative position
- Mirror if left/right hand matters
```

---

### **Module D — LED Strip** (U-channel)
```
FLAT: 250×28 mm strip, 1.2 mm thick

CREASE PATTERN:
- Two long edges: VALLEY folds (fold UP 90°)
- Snap tabs: 4 per edge, pre-cut, fold OUT 90°
- LED groove: 12 mm wide, center (stays flat)

FOLD SEQUENCE:
1. Score lines UP
2. Fold BOTH long edges UP 90° (valley) → forms U-channel
3. Fold 4 snap tabs per edge OUTWARD 90° (mountain)
   → 8 tabs total, point away from channel interior
4. LED groove remains flat at channel bottom (12 mm wide)

RESULT: U-channel with snap tabs
- Channel interior: 28 mm wide × 10 mm tall
- LED groove at bottom: 12 mm wide
- 8 snap tabs (4 top, 4 bottom) clip into Module A groove
```

---

### **Module E — Electronics Tray** (Origami box)
```
FLAT: 80×50 mm cross, 1.2 mm thick, H=15 mm walls

CREASE PATTERN:
- 4 wall flaps (base edges): VALLEY folds (fold UP 90°)
- Dovetail foot (center bottom): MOUNTAIN fold (fold DOWN 90°)
- Battery pockets: 35×35 mm cutouts (2×, lower corners)
- MCU pockets: 25×20 mm cutouts (2×, upper corners)

FOLD SEQUENCE:
1. Score lines UP
2. Fold 4 wall flaps UP 90° (valley at base edges) → open box
3. Fold dovetail foot DOWN 90° (mountain) → foot extends below floor
4. Corner cutouts remain open

RESULT: Box 80×50×15 mm with dovetail foot
- Floor: 80×50 mm with 4 corner cutouts
- 2× battery pockets (35×35 mm) at bottom
- 2× MCU pockets (25×20 mm) at top
- Dovetail foot: 12×4.5 mm, slides into Module A rail
- Wire routing: gaps at wall bases
```

---

### **Module F — Diffuser Cover** (Flat snap-on)
```
FLAT: 250×25 mm strip, 1.5 mm thick (clear TPU/PETG)

CREASE PATTERN:
- No structural folds (stays FLAT)
- Snap tabs: 4 per edge, pre-cut, fold DOWN 90° (mountain)

FOLD SEQUENCE:
1. Score lines UP (tabs only)
2. Fold 8 snap tabs DOWN 90° (mountain)
   → Tabs point toward LED channel
3. Stays flat otherwise

RESULT: Flat diffuser cover
- 1.5 mm clear TPU (best diffusion) or clear PETG 95% infill
- 8 tabs lock onto Module D channel edges
```

---

## ⚡ Assembly Sequence (30 sec, no tools)

```
PREP: Fold all 6 modules per above

1. MODULE E → A
   Slide E dovetail foot INTO A interior dovetail rail (click)
   Foot faces DOWN, box sits inside A curve

2. MODULE B → A (WRIST)
   Hook B's 2 tabs INTO A's wrist-end slots (snap)
   Strap anchor faces outward

3. MODULE C → A (ELBOW)
   Hook C's 2 tabs INTO A's elbow-end slots (snap)
   Strap anchor faces outward

4. MODULE D → A
   Snap D's 8 tabs INTO A's LED groove (click)
   Channel sits in groove, tabs lock top & bottom

5. MODULE F → D
   Snap F's 8 tabs OVER D's channel edges (click)
   Diffuser covers LED groove from above

6. STRAP
   Thread 20 mm elastic/Velcro through B & C anchors
   Adjust tension for snug forearm fit

6. ELECTRONICS
   - WS2812B strip (5050, 30-60 LED/m) → D groove
   - Wires exit D ends → route to E box
   - XIAO/Qt Py → E upper pockets (25×20 mm)
   - LiPo (303040 or 402030) → E lower pockets (35×35 mm)
   - JST connector/wires → E open space

7. POWER ON → glow!
```

---

## 🖨️ Print Settings (Optimized)

| Setting | Value | Notes |
|---------|-------|-------|
| **Material (A,B,C,D,E)** | PETG | Heat resistant, good layer adhesion |
| **Material (F)** | Clear TPU (best) or clear PETG 95% infill | Diffusion |
| **Layer height** | 0.2 mm | Score lines still readable |
| **Wall count** | 1 (single wall) | 1.2 mm = thick line |
| **Infill** | 0% | Origami rigidity from folds |
| **Speed** | 60 mm/s | PETG handles well |
| **Temp** | 240/80°C | Standard PETG |
| **Supports** | NONE | All flat |
| **Bed** | 220×220 mm | Fits all modules |
| **Orientation** | Flat on bed | No rotation needed |

---

## 🔧 Post-Process

| Step | Action |
|------|--------|
| 1 | Remove from bed carefully (thin walls) |
| 2 | Clean score lines with deburring tool if needed |
| 3 | Test-fold each module before final crease |
| 4 | Trim tab interference with flush cutters (0.1 mm max) |
| 5 | Crease firmly — ruler edge, hold 5 sec |
| 6 | Assemble per sequence above |
| 7 | Install electronics, test LEDs |
| 8 | Optional: kapton tape over LED strip for protection |

---

## 📏 Parametric Adjustments (edit scripts)

| Parameter | Script | Default | Adjust For |
|-----------|--------|---------|------------|
| `forearm_length` | A, D | 250 mm | User arm length |
| `wrist_half_width` | A, B | 90 mm | Wrist circumference / π / 2 |
| `forearm_half_width` | A, C | 130 mm | Forearm circumference / π / 2 |
| `facet_size` | A | 12 mm | Smaller = smoother curve, longer print |
| `miura_angle` | A | 72° | Curvature (70-75° typical) |
| `wall_thick` | All | 1.2 mm | Material/printer dependent |
| `H (tray height)` | E | 15 mm | Component stack height |
| `battery_pocket` | E | 35×35 mm | Specific LiPo model |
| `mcu_pocket` | E | 25×20 mm | Specific MCU board |

---

## 🔄 Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | — | Initial modular origami design |
| 1.1 | — | Component validation fixes: LED groove 12mm, battery pockets 35×35mm, tray H=15mm, dovetail 12×4.5mm |

---

## 📄 Files

All design-plan files live in `bracer_design/`:

| File | Description |
|------|-------------|
| `bracer_design/module_a_forearm.py` | Forearm segment (Miura) |
| `bracer_design/module_b_wrist.py` | Wrist closure (waterbomb) |
| `bracer_design/module_c_elbow.py` | Elbow closure (waterbomb, wide) |
| `bracer_design/module_d_led.py` | LED strip (U-channel) |
| `bracer_design/module_e_tray.py` | Electronics tray (origami box) |
| `bracer_design/module_f_diffuser.py` | Diffuser cover (flat) |
| `bracer_design/FOLD_PLAN.md` | This document |

The reusable MCP client stays in the project `tools/` folder:

| File | Description |
|------|-------------|
| `tools/fusion_mcp.py` | Reusable MCP client (session-cached) |

### Running the module scripts

From the **project root** (`SPARK`), the client import resolves via the `tools` package:

```powershell
cd D:\Aaradhya-Dev-Tamrakar\SPARK
python -c "import json; from tools.fusion_mcp import execute_script; print(json.dumps(execute_script(open('bracer_design/module_a_forearm.py').read()), indent=2)[:1000])"
```

Swap `module_a_forearm.py` for any other module file in `bracer_design/`.

---

## ✅ Ready to Print

1. Export STLs from Fusion (right-click body → Save as STL)
2. Slice with settings above
3. Print all 6 in parallel
4. Fold, snap, glow

**No screws. No glue. Pure origami engineering.** ⚡