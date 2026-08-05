#!/usr/bin/env python3
"""
wire_format.py

Defines SPARK's gateway-side event schema and parses the wire format
the ESP32-S3 wearable node uses to transmit a CONFIRMED_FALL event
over BLE/serial, per docs/WIRE_FORMAT_v1.md (LOCKED).

STATUS: unblocked. docs/WIRE_FORMAT_v1.md resolves the firmware
(comms/output.h) <-> gateway schema gap. Transport is BLE, JSON
payload (serial is the same JSON schema, no BLE framing -- dev/debug
fallback only). GATT UUIDs and BLE chunking/MTU are explicitly left
open by that doc (not needed for v1 -- payload fits in 2-3 packets at
MTU 185+, see doc's Size note) and are NOT handled here; this module
parses an already-reassembled JSON payload, it does not do BLE framing.

Schema (WIRE_FORMAT_v1.md):
    event_id: str
    device_id: str
    firmware_version: str
    timestamp_ms: uint32 (device clock at trigger)
    confidence: float, 0.0-1.0 (== firmware's class_probs[1]; the
        class_probs[0]/P(NON_FALL) value never crosses the wire --
        it's redundant since softmax sums to 1, and stays internal
        to firmware's InferenceOutput per the doc's Resolution #1)
    peak_features: {a_x, a_y, a_z, w_x, w_y, w_z} -> float

v1 explicitly excludes raw_window (full 200x6 window) -- reserved for
v2 once WP 2.0 lands a trained model and real SHAP needs it as
explainer input (doc's Resolution #2). Do not implement parsing for
it here; EventPayload.raw_window stays Optional[None].
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Optional


# Placeholder channel ordering, matching MPU6050's 6-axis output as
# used elsewhere in the repo (training/data_prep/prepare_sisfall.py):
# a_x, a_y, a_z, w_x, w_y, w_z. Not confirmed as the wire order --
# just the axis set the gateway pipeline needs a name for.
IMU_CHANNELS = ("a_x", "a_y", "a_z", "w_x", "w_y", "w_z")


@dataclass
class EventPayload:
    """
    Gateway-side representation of one CONFIRMED_FALL event, per
    docs/WIRE_FORMAT_v1.md.

    timestamp_ms replaces the earlier draft's ISO-string `timestamp`
    field -- the locked doc specifies device clock ms (uint32), not a
    gateway-assigned ISO timestamp. Any caller previously reading
    `.timestamp` needs updating (see gateway/main.py).
    """

    event_id: str
    device_id: str
    firmware_version: str
    timestamp_ms: int  # device clock at trigger, per WIRE_FORMAT_v1.md
    confidence: float  # == firmware class_probs[1], P(FALL), 0.0-1.0
    peak_features: dict  # {channel_name: peak_value}, keys from IMU_CHANNELS
    raw_window: Optional[list] = None  # NOT parsed in v1 -- reserved for v2
    extra: dict = field(default_factory=dict)  # unrecognized fields, preserved


class WireFormatNotConfirmed(NotImplementedError):
    """
    Retained for backward compatibility with any code still importing
    it (e.g. older test fixtures). No longer raised by parse_event --
    the format is locked as of docs/WIRE_FORMAT_v1.md.
    """


class WireFormatError(ValueError):
    """Raised when a raw payload doesn't match docs/WIRE_FORMAT_v1.md."""


_REQUIRED_FIELDS = (
    "event_id",
    "device_id",
    "firmware_version",
    "timestamp_ms",
    "confidence",
    "peak_features",
)


def parse_event(raw: bytes) -> EventPayload:
    """
    Parse a raw BLE/serial JSON payload into an EventPayload, per
    docs/WIRE_FORMAT_v1.md. Transport framing (BLE packet reassembly,
    MTU/chunking) happens upstream in receiver.py -- this function
    takes an already-reassembled, complete JSON payload as bytes.

    raw_window is never populated here (v1 doesn't send it, per the
    doc's Resolution #2) -- always None on the returned EventPayload.
    Any fields in the payload beyond the locked schema are preserved
    in .extra rather than silently dropped or raising.
    """
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as e:
        raise WireFormatError(f"payload is not valid UTF-8: {e}") from e

    try:
        obj = json.loads(text)
    except json.JSONDecodeError as e:
        raise WireFormatError(f"payload is not valid JSON: {e}") from e

    if not isinstance(obj, dict):
        raise WireFormatError(f"payload must be a JSON object, got {type(obj).__name__}")

    missing = [f for f in _REQUIRED_FIELDS if f not in obj]
    if missing:
        raise WireFormatError(f"payload missing required field(s): {missing}")

    peak_features = obj["peak_features"]
    if not isinstance(peak_features, dict):
        raise WireFormatError("peak_features must be a JSON object")
    missing_channels = [ch for ch in IMU_CHANNELS if ch not in peak_features]
    if missing_channels:
        raise WireFormatError(f"peak_features missing channel(s): {missing_channels}")

    known = set(_REQUIRED_FIELDS) | {"raw_window"}
    extra = {k: v for k, v in obj.items() if k not in known}

    return EventPayload(
        event_id=str(obj["event_id"]),
        device_id=str(obj["device_id"]),
        firmware_version=str(obj["firmware_version"]),
        timestamp_ms=int(obj["timestamp_ms"]),
        confidence=float(obj["confidence"]),
        peak_features={ch: float(peak_features[ch]) for ch in IMU_CHANNELS},
        raw_window=None,  # v1 never sends this; not parsed even if present
        extra=extra,
    )
