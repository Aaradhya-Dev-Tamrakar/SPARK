import adsk.core, adsk.fusion

def run(_context: str):
    app = adsk.core.Application.get()
    product = app.activeDocument.products.itemByProductType("DesignProductType")
    design = adsk.fusion.Design.cast(product)
    root = design.rootComponent
    sk = root.sketches.add(root.xYConstructionPlane)
    lines = sk.sketchCurves.sketchLines

    L = 250.0
    W = 25.0
    thick = 1.5  # slightly thicker for diffusion

    # Cover: flat strip with snap tabs
    lines.addByTwoPoints(adsk.core.Point3D.create(0, -W/2, 0), adsk.core.Point3D.create(L, -W/2, 0))
    lines.addByTwoPoints(adsk.core.Point3D.create(L, -W/2, 0), adsk.core.Point3D.create(L, W/2, 0))
    lines.addByTwoPoints(adsk.core.Point3D.create(L, W/2, 0), adsk.core.Point3D.create(0, W/2, 0))
    lines.addByTwoPoints(adsk.core.Point3D.create(0, W/2, 0), adsk.core.Point3D.create(0, -W/2, 0))

    # Snap tabs (match Module D)
    for si in range(4):
        t = (si + 1) / 5.0
        x = t * L
        tw, td = 4.0, 2.0
        x1, x2 = x - td/2, x + td/2
        y1, y2 = -W/2 - tw, -W/2
        lines.addByTwoPoints(adsk.core.Point3D.create(x1, y1, 0), adsk.core.Point3D.create(x2, y1, 0))
        lines.addByTwoPoints(adsk.core.Point3D.create(x2, y1, 0), adsk.core.Point3D.create(x2, y2, 0))
        lines.addByTwoPoints(adsk.core.Point3D.create(x2, y2, 0), adsk.core.Point3D.create(x1, y2, 0))
        lines.addByTwoPoints(adsk.core.Point3D.create(x1, y2, 0), adsk.core.Point3D.create(x1, y1, 0))
        # Top
        lines.addByTwoPoints(adsk.core.Point3D.create(x1, W/2, 0), adsk.core.Point3D.create(x2, W/2, 0))
        lines.addByTwoPoints(adsk.core.Point3D.create(x2, W/2, 0), adsk.core.Point3D.create(x2, W/2 + tw, 0))
        lines.addByTwoPoints(adsk.core.Point3D.create(x2, W/2 + tw, 0), adsk.core.Point3D.create(x1, W/2 + tw, 0))
        lines.addByTwoPoints(adsk.core.Point3D.create(x1, W/2 + tw, 0), adsk.core.Point3D.create(x1, W/2, 0))

    prof = sk.profiles.item(0)
    ext = root.features.extrudeFeatures
    inp = ext.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    inp.setDistanceExtent(False, adsk.core.ValueInput.createByReal(thick))
    feat = ext.add(inp)

    print("Diffuser Cover created: " + feat.name)