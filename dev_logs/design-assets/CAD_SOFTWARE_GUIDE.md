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

**Two modes: chat-only (no connector) and live via the Fusion MCP connector (Claude Desktop only).**

### 4a. Chat-only (claude.ai / no connector) — always available

Claude cannot open, edit, or export `.f3d`/`.step`/`.stl` files in this mode. What it can do:

| Use Claude for | Don't use Claude for |
|---|---|
| Explaining what a Fusion command does before you click it ("what does Shell actually do") | Generating the enclosure file itself |
| Converting your dimensional spec (two-zone layout, wall thickness, seam %) into an ordered step-by-step modeling plan you follow inside Fusion | Verifying real-world fit/tolerance — that only a physical test print can confirm |
| Debugging *why* a specific step isn't working ("I extruded but the shell command is greyed out" → usually means the body isn't a single closed solid yet) | Structural/thermal simulation of the real TPU part — Fusion has basic simulation tools built in for this, use those directly |
| Turning your design decisions into repo documentation (`DESIGN_IDEAS.md`, tracker entries) — already doing this for DI-01 | Making the actual go/no-go call on your printer's compatibility — check your specific machine's TPU support first |
| Reviewing a description of your model ("here's my current dimensions/features list") and flagging inconsistencies against the locked spec (Action #8, DI-01) | — |

### 4b. Live via Fusion MCP connector (Claude Desktop) — since April 28, 2026

Autodesk and Anthropic shipped an official MCP connector: Claude Desktop can connect directly to a running Fusion session and create/modify/query geometry from natural language — not just advice, actual live model edits (demonstrated: "round all the edges of this box" → Fusion applies fillets to all 24 edges automatically).

**Setup (~1 minute, confirmed steps):**
1. In Fusion: **Preferences → General → API** (Preferences for Scripting and Programming panel) → enable **Fusion MCP Server** checkbox → note the port (default `27182`).
2. In **Claude Desktop** (not claude.ai web): **Customize → Connectors tab → + → search "Fusion"** → click **+ → Install** on Autodesk Fusion.
3. Toggle the connector **Enabled**, click **Configure**, confirm the port matches Fusion's.
4. Fusion must stay open with a project active — the connector acts on your live session, not a saved file.

**What it's actually good at (per Autodesk's own guidance):**
- Bulk edits/renames — renaming components, swapping materials, bumping every fillet under a radius to a new value.
- Parametric parts from a spec — describe a bracket, mounting plate, or **simple enclosure** and Claude scripts it; works best with well-defined geometry (extrusions, holes, fillets, shells, patterns) — this matches the enclosure's toolset from §3.
- Export pipelines — batch-export components as STL/STEP/F3D with consistent naming.
- API discovery — pulls current Fusion Help docs for programmatic questions, useful even if you finish the step yourself in the UI.

**Caveats specific to your case:**
- Requires **Claude Desktop**, not the claude.ai browser/mobile chat this repo work has been happening in — separate app, separate setup.
- Community feedback is mixed on non-trivial custom geometry ("a little clunky," per one Autodesk forum user) — reliable for the bulk/parametric/export tasks above, less proven for one-off organic shapes like the bracer silhouette itself.
- Claude reads the live session via screenshots/state, not omniscient X-ray access — for TPU-specific concerns (wall thickness, print tolerance) you still need to state material/process explicitly in the prompt, same as any other request.
- Still verify output the same way as everything else in this repo: don't trust a connector-driven edit blind — check dimensions against DI-01/Action #8 spec before committing.

**How much to lean on it:** for the *first* pass of your two-zone geometry (sketch → extrude → shell → fillet), do it manually in Fusion per §3 so you actually learn the tool. Once the base geometry exists, the connector is well-suited for the repetitive part — bulk fillet/shell tweaks, renaming bodies to match Zone 1/Zone 2 naming, batch STL export for iterative print tests.

---

## 5. TPU-specific print notes (once modeling is done)

Flagged here for later — not modeling-software concerns, but relevant to the same enclosure:
- TPU is flexible filament — needs a printer with a direct-drive extruder or well-tuned Bowden setup; stringing/retraction settings differ significantly from PLA (which your `Action #2`/`#8` history already locked for a *different*, non-flexible print — confirm current printer's TPU capability before committing to TPU for this part).
- Wall thickness in the model (Fusion Shell command) should match the ~2 mm spec already logged in DI-01 — don't rely on slicer infill to compensate for thin walls in the model.
- Cross-reference with KEC Makerspace equipment (already the fabrication venue per Action #2) — confirm TPU compatibility with their specific printer(s) before finalizing wall thickness/tolerances in Fusion, since flexible filament print settings are less forgiving than PLA.

---

## Status
**In progress.** No Fusion 360 file exists in this repo yet. Current step: practice part exercise (see `CAD_PRACTICE_PART_WALKTHROUGH.md`) — box → shell → fillet → STL export, rehearsing the four core commands before modeling DI-01's real two-zone geometry.
