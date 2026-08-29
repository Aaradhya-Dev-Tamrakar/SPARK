"""Reusable client for the Autodesk Fusion 360 MCP server (port 27182).

Handles the JSON-RPC handshake once, caches the session id, and exposes
execute_script() so Fusion work skips manual initialization each time.
"""

import json
import os
import urllib.error
import urllib.request

BASE = "http://127.0.0.1:27182/mcp"
SESSION_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".fusion_session")


def _post(payload, session=None):
    headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
    if session:
        headers["Mcp-Session-Id"] = session
    req = urllib.request.Request(BASE, data=json.dumps(payload).encode(), headers=headers)
    try:
        resp = urllib.request.urlopen(req, timeout=120)
        return resp.headers.get("Mcp-Session-Id"), resp.read().decode(), None
    except urllib.error.HTTPError as e:
        return e.headers.get("Mcp-Session-Id"), e.read().decode(), e.code


def connect(force=False):
    if not force and os.path.exists(SESSION_FILE):
        with open(SESSION_FILE) as f:
            sid = f.read().strip()
        if sid:
            return sid
    sid, _, _ = _post(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "opencode", "version": "1.0"},
            },
        }
    )
    _post({"jsonrpc": "2.0", "method": "notifications/initialized"}, session=sid)
    with open(SESSION_FILE, "w") as f:
        f.write(sid)
    return sid


def execute_script(script, sid=None):
    if sid is None:
        sid = connect()
    payload = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "fusion_mcp_execute",
            "arguments": {"featureType": "script", "object": {"script": script}},
        },
    }
    _, body, code = _post(payload, session=sid)
    if code in (400, 404):
        sid = connect(force=True)
        _, body, _ = _post(payload, session=sid)
    return json.loads(body)


def create_sphere(radius, x=0.0, y=0.0, z=0.0):
    script = (
        "import adsk.core, adsk.fusion\n"
        "import math\n"
        "def run(_context: str):\n"
        "    app = adsk.core.Application.get()\n"
        "    product = app.activeDocument.products.itemByProductType('DesignProductType')\n"
        "    design = adsk.fusion.Design.cast(product)\n"
        "    root = design.rootComponent\n"
        "    sk = root.sketches.add(root.xYConstructionPlane)\n"
        "    arc = sk.sketchCurves.sketchArcs.addByCenterStartSweep(\n"
        f"        adsk.core.Point3D.create({x}, {y}, {z}), adsk.core.Point3D.create({x + radius}, {y}, {z}), math.pi)\n"
        "    sk.sketchCurves.sketchLines.addByTwoPoints(\n"
        f"        adsk.core.Point3D.create({x - radius}, {y}, {z}), adsk.core.Point3D.create({x + radius}, {y}, {z}))\n"
        "    profile = sk.profiles.item(0)\n"
        "    ax = root.xConstructionAxis\n"
        "    rev = root.features.revolveFeatures\n"
        "    inp = rev.createInput(profile, ax, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)\n"
        "    inp.setAngleExtent(False, adsk.core.ValueInput.createByReal(2 * math.pi))\n"
        "    feat = rev.add(inp)\n"
        f"    print('Sphere created: radius={radius} cm at ({x},{y},{z}), entity=' + feat.name)\n"
    )
    return execute_script(script)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "sphere":
        r = float(sys.argv[2]) if len(sys.argv) > 2 else 5.0
        print(json.dumps(create_sphere(r), indent=2))
    elif len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            print(json.dumps(execute_script(f.read()), indent=2))
    else:
        print(json.dumps(connect() and {"status": "connected"}, indent=2))
