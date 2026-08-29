import adsk.core
import adsk.fusion


def run(_context: str):
    app = adsk.core.Application.get()
    product = app.activeDocument.products.itemByProductType("DesignProductType")
    design = adsk.fusion.Design.cast(product)
    root = design.rootComponent
    sk = root.sketches.add(root.xYConstructionPlane)
    lines = sk.sketchCurves.sketchLines

    L = 250.0
    W0 = 90.0
    W1 = 130.0

    # Boundary
    lines.addByTwoPoints(adsk.core.Point3D.create(0, -W0, 0), adsk.core.Point3D.create(L, -W1, 0))
    lines.addByTwoPoints(adsk.core.Point3D.create(L, -W1, 0), adsk.core.Point3D.create(L, W1, 0))
    lines.addByTwoPoints(adsk.core.Point3D.create(L, W1, 0), adsk.core.Point3D.create(0, W0, 0))
    lines.addByTwoPoints(adsk.core.Point3D.create(0, W0, 0), adsk.core.Point3D.create(0, -W0, 0))

    # Fold lines
    n = int(L / 12)
    for i in range(1, n):
        x = i * (L / n)
        w = W0 + (W1 - W0) * (i / n)
        lines.addByTwoPoints(adsk.core.Point3D.create(x, -w, 0), adsk.core.Point3D.create(x, w, 0))

    # Hook-tab slots (3 per edge)
    for edge_x in [0, L]:
        for si in range(3):
            t = (si + 1) / 4.0
            x = edge_x + (t * L / n if edge_x == 0 else -t * L / n)
            w = W0 if edge_x == 0 else W1
            sw, sd = 6.0, 3.0
            y1, y2 = -sw / 2, sw / 2
            x1, x2 = x, x + (sd if edge_x == 0 else -sd)
            lines.addByTwoPoints(
                adsk.core.Point3D.create(x1, y1, 0), adsk.core.Point3D.create(x2, y1, 0)
            )
            lines.addByTwoPoints(
                adsk.core.Point3D.create(x2, y1, 0), adsk.core.Point3D.create(x2, y2, 0)
            )
            lines.addByTwoPoints(
                adsk.core.Point3D.create(x2, y2, 0), adsk.core.Point3D.create(x1, y2, 0)
            )
            lines.addByTwoPoints(
                adsk.core.Point3D.create(x1, y2, 0), adsk.core.Point3D.create(x1, y1, 0)
            )

    # LED groove (widened to 12mm for 5050 strip)
    gw = 12.0
    for i in range(n):
        x0 = i * (L / n)
        x1 = (i + 1) * (L / n)
        lines.addByTwoPoints(
            adsk.core.Point3D.create(x0, -gw / 2, 0), adsk.core.Point3D.create(x1, -gw / 2, 0)
        )
        lines.addByTwoPoints(
            adsk.core.Point3D.create(x1, -gw / 2, 0), adsk.core.Point3D.create(x1, gw / 2, 0)
        )
        lines.addByTwoPoints(
            adsk.core.Point3D.create(x1, gw / 2, 0), adsk.core.Point3D.create(x0, gw / 2, 0)
        )
        lines.addByTwoPoints(
            adsk.core.Point3D.create(x0, gw / 2, 0), adsk.core.Point3D.create(x0, -gw / 2, 0)
        )

    # Dovetail channel (widened to 12mm)
    dw, dh = 12.0, 4.5
    for i in range(n):
        x0 = i * (L / n)
        x1 = (i + 1) * (L / n)
        yc = 0
        lines.addByTwoPoints(
            adsk.core.Point3D.create(x0, yc - dw / 2, 0),
            adsk.core.Point3D.create(x1, yc - dw / 2, 0),
        )
        lines.addByTwoPoints(
            adsk.core.Point3D.create(x1, yc - dw / 2, 0),
            adsk.core.Point3D.create(x1, yc - dw / 2 + dh, 0),
        )
        lines.addByTwoPoints(
            adsk.core.Point3D.create(x1, yc - dw / 2 + dh, 0),
            adsk.core.Point3D.create(x0, yc - dw / 2 + dh, 0),
        )
        lines.addByTwoPoints(
            adsk.core.Point3D.create(x0, yc - dw / 2 + dh, 0),
            adsk.core.Point3D.create(x0, yc - dw / 2, 0),
        )

    # Extrude
    prof = sk.profiles.item(0)
    ext = root.features.extrudeFeatures
    inp = ext.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    inp.setDistanceExtent(False, adsk.core.ValueInput.createByReal(1.2))
    feat = ext.add(inp)

    print(
        "Module A (Forearm Segment) created: " + feat.name + " | LED groove=12mm, Dovetail=12x4.5mm"
    )
