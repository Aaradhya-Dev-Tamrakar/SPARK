# SPARK — CAD Software Guide (TPU Enclosure Design)

Decision record + working guide for designing the fall-detection enclosure (Action #8, two-zone electronics layout, DI-01 concept). Written for zero prior CAD experience across the team.

---

## 1. Decision: Fusion 360

**Use Fusion 360.** Not FreeCAD, not Tinkercad, not Blender.

| Option | Verdict | Why not |
|---|---|---|
| **Fusion 360** | **Chosen** | Parametric (edit dimensions after the fact — essential for a two-zone enclosure you'll revise against real PCB/battery fit), free for students, gentlest learning curve of the parametric tools, huge tutorial base, direct STL export for 3D printing. |
| FreeCAD | Rejected | Equally capable long-term, but rougher UI/UX and more crashes reported for beginners — steeper early curve for no real benefit at your scale of project. |
| Tinkercad | Rejected | Too limited — block-based, no real parametric control, can't do the precision wall-thickness/internal-cavity work an electronics enclosure needs. Fine for a first afternoon, not for this. |
| Blender | Rejected | Sculpting/organic-mesh tool, not dimension-driven. Wrong category for a part that must fit a PCB and battery to the millimeter. |
| SolidWorks | Rejected | Steeper curve, no comparable free/student path as smooth as Fusion's, industry-standard but overkill here. |
| OpenSCAD | Rejected | Code-based CAD — precise and version-control-friendly (interesting for a repo-driven team), but "not extreme learning curve" was a stated constraint and OpenSCAD's text-only workflow is a harder entry point than Fusion's visual sketch-and-extrude. Worth revisiting later if the team wants scriptable, git-diffable design files.

**Why parametric matters specifically for this part:** the enclosure has a locked two-zone internal layout (IMU/wrist zone, ESP32+battery+charge-circuit/forearm zone, connecting spine) that will keep changing as BOM dimensions get vendor-confirmed. A parametric model lets you change one dimension (e.g., battery thickness) and have the whole shell update, instead of remodeling from scratch. Sculpting tools (Blender) and block-based tools (Tinkercad) can't do this.

---

## 2. Licensing — what to sign up for

**Fusion 360 Personal Use license** (free, non-commercial, thesis/hobbyist projects qualify):
- Sign up at autodesk.com with any email — no `.edu` required.
- Valid 3 years, renewable.
- Restriction: no commercial use (selling the design/product). A university thesis is not commercial use — this is fine.
- Some advanced features gated (large assemblies, some simulation/generative-design tools) — none of these are needed for a single-part enclosure.

**Try Fusion 360 Education license first if KEC issues student emails** — same core software, fewer feature restrictions, same free cost, same non-commercial terms. If KEC doesn't have a recognized institutional domain or verification fails, fall back to Personal Use — functionally near-identical for this project either way.

Team: **each person creates their own free account** — don't share logins. Files can be shared via Fusion's own cloud project sharing (invite by email) once the account exists.

---

## 3. Learning path — realistic time budget

Target: functional competence for **one enclosure part**, not general CAD mastery.

| Stage | Time | What to learn | Where |
|---|---|---|---|
| 1. Interface + first shape | 1–2 hrs | Sketch a 2D profile, extrude to 3D, rotate/pan/zoom view | Autodesk's own "Fusion 360 for beginners" tutorial (in-app on first launch) |
| 2. Sketch constraints | 1–2 hrs | Dimensions, fillets, symmetry — this is what makes it *parametric* instead of freehand | Same tutorial track, "Sketching" module |
| 3. Solid modeling basics | 2–3 hrs | Extrude, revolve, shell (hollow out a solid — directly relevant, this *is* how you make an enclosure wall), fillet/chamfer edges | YouTube: search "Fusion 360 shell command tutorial" and "Fusion 360 enclosure design tutorial" |
| 4. Assemblies (optional, later) | 1–2 hrs | Only needed if you want to check IMU/ESP32/battery placement inside the shell as separate bodies before committing to final geometry | Autodesk's "Joints and assemblies" tutorial |
| 5. Export for printing | 30 min | STL export settings, mesh resolution | Fusion 360 docs: "Export as STL" |

**Total to first printable part: roughly 6–10 hours spread over a week**, not a single sitting. This matches "not extreme learning curve" — you will not be fluent, but you'll be able to build and iterate the enclosure.

**Don't try to learn everything Fusion can do.** You need: sketch → extrude → shell → fillet → export. That's the entire toolset this part requires.

---

## 4. Where Claude fits into this workflow

Claude does **not** replace Fusion 360 and cannot open, edit, or export `.f3d`/`.step`/`.stl` files directly — there's no CAD engine behind this chat. What Claude *can* do:

| Use Claude for | Don't use Claude for |
|---|---|
| Explaining what a Fusion command does before you click it ("what does Shell actually do") | Generating the enclosure file itself |
| Converting your dimensional spec (two-zone layout, wall thickness, seam %) into an ordered step-by-step modeling plan you follow inside Fusion | Verifying real-world fit/tolerance — that only a physical test print can confirm |
| Debugging *why* a specific step isn't working ("I extruded but the shell command is greyed out" → usually means the body isn't a single closed solid yet) | Anything requiring you to screen-share or upload the live `.f3d` file — Claude can't inspect it |
| Turning your design decisions into repo documentation (`DESIGN_IDEAS.md`, tracker entries) — already doing this for DI-01 | Structural/thermal simulation of the real TPU part — Fusion has basic simulation tools built in for this, use those directly |
| Drafting print settings guidance (TPU-specific slicer settings: temp, speed, retraction) once geometry is finalized | Making the actual go/no-go call on your printer's compatibility — check your specific machine's TPU support first |
| Reviewing a description of your model ("here's my current dimensions/features list") and flagging inconsistencies against the locked spec (Action #8, DI-01) | — |

**How much to lean on it:** treat Claude as a tutor/rubber-duck for the modeling steps and a documentation partner for the repo — not as the design tool itself. The actual 3D modeling work happens in Fusion 360, by hand, by you.

**When to bring a Fusion question to Claude:** any time you're stuck on *why* a command isn't behaving as expected, or need the CAD steps translated from the two-zone spec (§ above) into an ordered build sequence. Paste the specific error/behavior — Claude reasons about it from Fusion's documented behavior, same as searching a forum, but faster and contextualized to your enclosure spec already logged in this repo.

---

## 5. TPU-specific print notes (once modeling is done)

Flagged here for later — not modeling-software concerns, but relevant to the same enclosure:
- TPU is flexible filament — needs a printer with a direct-drive extruder or well-tuned Bowden setup; stringing/retraction settings differ significantly from PLA (which your `Action #2`/`#8` history already locked for a *different*, non-flexible print — confirm current printer's TPU capability before committing to TPU for this part).
- Wall thickness in the model (Fusion Shell command) should match the ~2 mm spec already logged in DI-01 — don't rely on slicer infill to compensate for thin walls in the model.
- Cross-reference with KEC Makerspace equipment (already the fabrication venue per Action #2) — confirm TPU compatibility with their specific printer(s) before finalizing wall thickness/tolerances in Fusion, since flexible filament print settings are less forgiving than PLA.

---

## Status
**Not yet started.** No Fusion 360 file exists in this repo. Next step: team signup (Personal Use license), Stage 1–2 tutorials, then model DI-01's two-zone geometry.
