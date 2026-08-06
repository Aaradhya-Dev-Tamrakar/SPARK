# SPARK — CAD Practice Part Walkthrough

First hands-on Fusion 360 exercise before modeling DI-01's real two-zone enclosure geometry. Companion to `CAD_SOFTWARE_GUIDE.md` §3 — same toolset (sketch → extrude → shell → fillet → export), applied to a throwaway shape so mistakes here don't cost real enclosure time.

---

## Goal

A simple hollow box with rounded edges, exported as STL. Not a real part — a rehearsal of the four commands the actual enclosure needs.

## Steps

1. **New sketch on a plane** — New Design → expand Origin in browser tree → click XY plane → Sketch → Create Sketch.
2. **Draw a rectangle** — Rectangle tool (R), click one corner, drag, click opposite corner. Exact size doesn't matter yet.
3. **Add dimensions** — Sketch Dimension tool (D), click an edge, type a value. Try 60mm × 40mm. This is what makes it parametric — change these numbers later and the shape updates.
4. **Finish sketch and extrude** — Finish Sketch → select the rectangle face → Create → Extrude → try 30mm → OK. Solid block exists.
5. **Shell it out** — Modify → Shell → click the top face (face to remove) → wall thickness 2mm (matches enclosure spec) → OK. Same command the real enclosure wall uses.
6. **Fillet the edges** — Modify → Fillet → select outer edges (box-select for several at once) → radius 3mm → OK. Same technique as the enclosure's rounded ergonomic edges.
7. **Export as STL** — right-click body in browser tree → Save As Mesh, or File → Export → STL format → save.

## After this

Move to DI-01's actual Zone 1 (wrist, IMU-only, slim) / Zone 2 (forearm, ESP32+battery+charge-circuit, wide) geometry per the two-zone spec already logged in `DESIGN_IDEAS.md`, using the same four commands. Fillet radius, shell thickness, and dimensions will be re-derived from the locked spec (Action #8), not carried over from this practice part.

---

**Status:** Practice part exercise defined, not yet completed in-app (no `.f3d`/`.stl` file exists in the repo yet).
