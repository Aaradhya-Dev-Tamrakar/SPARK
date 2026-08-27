import adsk.core, adsk.fusion

def run(_context: str):
    app = adsk.core.Application.get()
    product = app.activeDocument.products.itemByProductType("DesignProductType")
    design = adsk.fusion.Design.cast(product)
    root = design.rootComponent
    sk = root.sketches.add(root.xYConstructionPlane)
    lines = sk.sketchCurves.sketchLines

    W = 124.0  # matches elbow half-width (~95% of forearm)
    H = 60.0
    thick = 1.2

    # Boundary
    lines.addByTwoPoints(adsk.core.Point3D.create(0, -W, 0), adsk.core.Point3D.create(H, -W*0.6, 0))
    lines.addByTwoPoints(adsk.core.Point3D.create(H, -W*0.6, 0), adsk.core.Point3D.create(H, W*0.6, 0))
    lines.addByTwoPoints(adsk.core.Point3D.create(H, W*0.6, 0), adsk.core.Point3D.create(0, W, 0))
    lines.addByTwoPoints(adsk.core.Point3D.create(0, W, 0), adsk.core.Point3D.create(0, -W, 0))

    # Waterbomb folds
    lines.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(H, 0, 0))
    lines.addByTwoPoints(adsk.core.Point3D.create(H/2, -W*0.3, 0), adsk.core.Point3D.create(H/2, W*0.3, 0))

    # Hook tabs (2)
    for side_y in [-W, W]:
        tab_x = H * 0.7
        tw, td = 6.0, 3.0
        x1, x2 = tab_x, tab_x + td
        y1, y2 = side_y - tw/2, side_y + tw/2
        lines.addByTwoPoints(adsk.core.Point3D.create(x1, y1, 0), adsk.core.Point3D.create(x2, y1, 0))
        lines.addByTwoPoints(adsk.core.Point3D.create(x2, y1, 0), adsk.core.Point3D.create(x2, y2, 0))
        lines.addByTwoPoints(adsk.core.Point3D.create(x2, y2, 0), adsk.core.Point3D.create(x1, y2, 0))
        lines.addByTwoPoints(adsk.core.Point3D.create(x1, y2, 0), adsk.core.Point3D.create(x1, y1, 0))

    # Strap anchor
    lines.addByTwoPoints(adsk.core.Point3D.create(H*0.2, -10, 0), adsk.core.Point3D.create(H*0.2, 10, 0))
    lines.addByTwoPoints(adsk.core.Point3D.create(H*0.2, 10, 0), adsk.core.Point3D.create(H*0.2+5, 10, 0))
    lines.addByTwoPoints(adsk.core.Point3D.create(H*0.2+5, 10, 0), adsk.core.Point3D.create(H*0.2+5, -10, 0))
    lines.addByTwoPoints(adsk.core.Point3D.create(H*0.2+5, -10, 0), adsk.core.Point3D.create(H*0.2, -10, 0))

    prof = sk.profiles.item(0)
    ext = root.features.extrudeFeatures
    inp = ext.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    inp.setDistanceExtent(False, adsk.core.ValueInput.createByReal(1.2))
    feat = ext.add(inp)

    print("Module C (Elbow Closure) created: " + feat.name)