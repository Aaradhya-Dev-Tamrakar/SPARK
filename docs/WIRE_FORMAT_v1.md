# SPARK Wire Format v1 — LOCKED

Resolves the firmware (`comms/output.h`) ↔ gateway (`receiver/wire_format.py`)
schema gap found reconciling `firmware-skeleton` and `gateway-skeleton`.

## Transport
BLE, JSON payload. Serial is the dev/debug fallback (same JSON schema, no
BLE framing). GATT UUIDs and BLE chunking/MTU handling: still open, not
blocked by this doc — device is single-producer, one event at a time, so
chunking only matters if a payload exceeds one BLE packet (see §Size below).

## Payload (JSON, one object per CONFIRMED_FALL event)

```json
{
  "event_id": "string, device-generated (e.g. UUID or seq counter)",
  "device_id": "string, e.g. MAC or provisioned ID",
  "firmware_version": "string, e.g. semver",
  "timestamp_ms": "uint32, device clock at trigger — firmware's FallEvent.timestamp_ms, unchanged",
  "confidence": "float, 0.0-1.0 — resolves to class_probs[1] (P(FALL)) from InferenceOutput",
  "peak_features": {
    "a_x": "float (g)", "a_y": "float (g)", "a_z": "float (g)",
    "w_x": "float (dps)", "w_y": "float (dps)", "w_z": "float (dps)"
  }
}
```

### Resolution #1 — `confidence` vs `class_probs[2]`
Firmware keeps `InferenceOutput.class_probs[2]` internally (unchanged —
that's the TFLite contract, not touched). At the transport boundary
(`OutputTransport::SendFallEvent`), firmware sends only
`class_probs[1]` as `confidence`. `class_probs[0]` (P(NON_FALL)) is
redundant (softmax sums to 1) and dropped from the wire.

### Resolution #2 — `raw_window` dropped from v1
Gateway's `EventPayload.raw_window` (200×6 full window) is **not** part
of v1. Checked against `shap_stub.py`: the stub only consumes
`peak_features` (6 scalars), not the full window. Real SHAP (Kernel/
Gradient explainer against the loaded model) will eventually need the
full window as explainer input — that's a v2 addition once WP 2.0 lands
a trained model, not a v1 blocker. `peak_features` = one peak value per
channel over the gate-triggered window (max magnitude sample per axis;
computed firmware-side from the same window fed to `TfliteModel::Invoke`).

### Size note
6 floats + 2 strings + timestamp + confidence, JSON-encoded, is well
under a single BLE packet (~20 bytes ATT default, but SPARK should
negotiate a larger MTU — even so, this payload is ~250-350 bytes typical,
fits in 2-3 packets at MTU 185+). No chunking protocol needed for v1;
revisit only if `raw_window` (v2) is added, since 200×6 floats ≈ 4.8KB
would need real chunking.

## Action items this resolves/opens
- Firmware: `output.cpp` `SendFallEvent` — encode `FallEvent` → this JSON
  shape. Needs `peak_features` computed from the trigger window (new,
  wasn't buffered before — gate.cpp tracks magnitude but not per-axis
  peaks; add peak-tracking to `ThresholdGate` or compute in app_main
  from the window already passed to `TfliteModel::Invoke`).
- Gateway: `wire_format.py` `parse_event` — implement against this shape,
  drop `raw_window`/`extra` from `EventPayload` or keep `raw_window` as
  `Optional[None]` reserved for v2.
- Both: replace "wire format not confirmed" blocking comments with a
  reference to this doc.
