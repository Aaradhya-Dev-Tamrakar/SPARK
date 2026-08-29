import adsk.core
import adsk.fusion


def run(_context: str):
    app = adsk.core.Application.get()
    product = app.activeDocument.products.itemByProductType("DesignProductType")
    design = adsk.fusion.Design.cast(product)
    root = design.rootComponent
    sk = root.sketches.add(root.xYConstructionPlane)
    lines = sk.sketchCurves.sketchLines

    L = 80.0
    W = 50.0
    H = 15.0  # taller walls (was 12)

    # Base
    lines.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(L, 0, 0))
    lines.addByTwoPoints(adsk.core.Point3D.create(L, 0, 0), adsk.core.Point3D.create(L, W, 0))
    lines.addByTwoPoints(adsk.core.Point3D.create(L, W, 0), adsk.core.Point3D.create(0, W, 0))
    lines.addByTwoPoints(adsk.core.Point3D.create(0, W, 0), adsk.core.Point3D.create(0, 0, 0))

    # Wall flaps
    # Bottom wall
    lines.addByTwoPoints(adsk.core.Point3D.create(0, -H, 0), adsk.core.Point3D.create(L, -H, 0))
    lines.addByTwoPoints(adsk.core.Point3D.create(0, -H, 0), adsk.core.Point3D.create(0, 0, 0))
    lines.addByTwoPoints(adsk.core.Point3D.create(L, -H, 0), adsk.core.Point3D.create(L, 0, 0))
    # Top wall
    lines.addByTwoPoints(
        adsk.core.Point3D.create(0, W + H, 0), adsk.core.Point3D.create(L, W + H, 0)
    )
    lines.addByTwoPoints(adsk.core.Point3D.create(0, W + H, 0), adsk.core.Point3D.create(0, W, 0))
    lines.addByTwoPoints(adsk.core.Point3D.create(L, W + H, 0), adsk.core.Point3D.create(L, W, 0))
    # Left wall
    lines.addByTwoPoints(adsk.core.Point3D.create(-H, 0, 0), adsk.core.Point3D.create(-H, W, 0))
    lines.addByTwoPoints(adsk.core.Point3D.create(-H, 0, 0), adsk.core.Point3D.create(0, 0, 0))
    lines.addByTwoPoints(adsk.core.Point3D.create(-H, W, 0), adsk.core.Point3D.create(0, W, 0))
    # Right wall
    lines.addByTwoPoints(
        adsk.core.Point3D.create(L + H, 0, 0), adsk.core.Point3D.create(L + H, W, 0)
    )
    lines.addByTwoPoints(adsk.core.Point3D.create(L + H, 0, 0), adsk.core.Point3D.create(L, 0, 0))
    lines.addByTwoPoints(adsk.core.Point3D.create(L + H, W, 0), adsk.core.Point3D.create(L, W, 0))

    # Dovetail foot (widened to 12mm)
    dw, dh = 12.0, 4.5
    x0, x1 = L / 2 - dw / 2, L / 2 + dw / 2
    y0, y1 = -H, -H - dh
    lines.addByTwoPoints(adsk.core.Point3D.create(x0, y0, 0), adsk.core.Point3D.create(x1, y0, 0))
    lines.addByTwoPoints(adsk.core.Point3D.create(x1, y0, 0), adsk.core.Point3D.create(x1, y1, 0))
    lines.addByTwoPoints(adsk.core.Point3D.create(x1, y1, 0), adsk.core.Point3D.create(x0, y1, 0))
    lines.addByTwoPoints(adsk.core.Point3D.create(x0, y1, 0), adsk.core.Point3D.create(x0, y0, 0))

    # Battery/MCU pockets (enlarged for 303040 LiPo + XIAO)
    # Two battery pockets: 35x35mm for 303040 LiPo
    for px, py in [(15, 15), (L - 15, 15)]:
        pw, ph = 35.0, 35.0
        lines.addByTwoPoints(
            adsk.core.Point3D.create(px - pw / 2, py - ph / 2, 0),
            adsk.core.Point3D.create(px + pw / 2, py - ph / 2, 0),
        )
        lines.addByTwoPoints(
            adsk.core.Point3D.create(px + pw / 2, py - ph / 2, 0),
            adsk.core.Point3D.create(px + pw / 2, py + ph / 2, 0),
        )
        lines.addByTwoPoints(
            adsk.core.Point3D.create(px + pw / 2, py + ph / 2, 0),
            adsk.core.Point3D.create(px - pw / 2, py + ph / 2, 0),
        )
        lines.addByTwoPoints(
            adsk.core.Point3D.create(px - pw / 2, py + ph / 2, 0),
            adsk.core.Point3D.create(px - pw / 2, py - ph / 2, 0),
        )
    # Two MCU pockets: 25x20mm for XIAO/Qt Py
    for px, py in [(15, W - 15), (L - 15, W - 15)]:
        pw, ph = 25.0, 20.0
        lines.addByTwoPoints(
            adsk.core.Point3D.create(px - pw / 2, py - ph / 2, 0),
            adsk.core.Point3D.create(px + pw / 2, py - ph / 2, 0),
        )
        lines.addByTwoPoints(
            adsk.core.Point3D.create(px + pw / 2, py - ph / 2, 0),
            adsk.core.Point3D.create(px + pw / 2, py + ph / 2, 0),
        )
        lines.addByTwoPoints(
            adsk.core.Point3D.create(px + pw / 2, py + ph / 2, 0),
            adsk.core.Point3D.create(px - pw / 2, py + ph / 2, 0),
        )
        lines.addByTwoPoints(
            adsk.core.Point3D.create(px - pw / 2, py + ph / 2, 0),
            adsk.core.Point3D.create(px - pw / 2, py - ph / 2, 0),
        )

    prof = sk.profiles.item(0)
    ext = root.features.extrudeFeatures
    inp = ext.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    inp.setDistanceExtent(False, adsk.core.ValueInput.createByReal(1.2))
    feat = ext.add(inp)

    print(
        "Module E (Electronics Tray) created: "
        + feat.name
        + " | H=15mm, Battery=35x35mm, MCU=25x20mm"
    )
