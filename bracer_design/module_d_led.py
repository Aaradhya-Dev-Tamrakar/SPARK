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
    W = 28.0  # widened channel (was 25)

    # Base strip (flat) - widened for 12mm LED groove + walls
    lines.addByTwoPoints(
        adsk.core.Point3D.create(0, -W / 2, 0), adsk.core.Point3D.create(L, -W / 2, 0)
    )
    lines.addByTwoPoints(
        adsk.core.Point3D.create(L, -W / 2, 0), adsk.core.Point3D.create(L, W / 2, 0)
    )
    lines.addByTwoPoints(
        adsk.core.Point3D.create(L, W / 2, 0), adsk.core.Point3D.create(0, W / 2, 0)
    )
    lines.addByTwoPoints(
        adsk.core.Point3D.create(0, W / 2, 0), adsk.core.Point3D.create(0, -W / 2, 0)
    )

    # Fold lines for U-channel (two walls)
    lines.addByTwoPoints(
        adsk.core.Point3D.create(0, -W / 2, 0), adsk.core.Point3D.create(L, -W / 2, 0)
    )
    lines.addByTwoPoints(
        adsk.core.Point3D.create(0, W / 2, 0), adsk.core.Point3D.create(L, W / 2, 0)
    )

    # Snap tabs on edges (match Module A groove - 12mm)
    for si in range(4):
        t = (si + 1) / 5.0
        x = t * L
        tw, td = 4.0, 2.0
        y1, y2 = -W / 2 - tw, -W / 2
        x1, x2 = x - td / 2, x + td / 2
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
        # Top edge too
        lines.addByTwoPoints(
            adsk.core.Point3D.create(x1, W / 2, 0), adsk.core.Point3D.create(x2, W / 2, 0)
        )
        lines.addByTwoPoints(
            adsk.core.Point3D.create(x2, W / 2, 0), adsk.core.Point3D.create(x2, W / 2 + tw, 0)
        )
        lines.addByTwoPoints(
            adsk.core.Point3D.create(x2, W / 2 + tw, 0), adsk.core.Point3D.create(x1, W / 2 + tw, 0)
        )
        lines.addByTwoPoints(
            adsk.core.Point3D.create(x1, W / 2 + tw, 0), adsk.core.Point3D.create(x1, W / 2, 0)
        )

    # LED groove (widened to 12mm for 5050 strip)
    gw = 12.0
    lines.addByTwoPoints(
        adsk.core.Point3D.create(0, -gw / 2, 0), adsk.core.Point3D.create(L, -gw / 2, 0)
    )
    lines.addByTwoPoints(
        adsk.core.Point3D.create(L, -gw / 2, 0), adsk.core.Point3D.create(L, gw / 2, 0)
    )
    lines.addByTwoPoints(
        adsk.core.Point3D.create(L, gw / 2, 0), adsk.core.Point3D.create(0, gw / 2, 0)
    )
    lines.addByTwoPoints(
        adsk.core.Point3D.create(0, gw / 2, 0), adsk.core.Point3D.create(0, -gw / 2, 0)
    )

    prof = sk.profiles.item(0)
    ext = root.features.extrudeFeatures
    inp = ext.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    inp.setDistanceExtent(False, adsk.core.ValueInput.createByReal(1.2))
    feat = ext.add(inp)

    print("Module D (LED Strip) created: " + feat.name + " | Channel=28mm, LED groove=12mm")
