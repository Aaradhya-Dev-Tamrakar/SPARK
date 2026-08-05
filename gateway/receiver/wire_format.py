#!/usr/bin/env python3
"""
wire_format.py

Defines SPARK's gateway-side event schema and the (as-yet unconfirmed)
wire format the ESP32-S3 wearable node uses to transmit a
CONFIRMED_FALL event over BLE/serial.

STATUS: BLOCKED. The exact byte-level/serial wire format has not been
confirmed with the firmware side (tracker Action #24, MPU6050 firmware
reuse-vs-rewrite, still open; no firmware code exists in firmware/ as
of this session). Per this session's scope note, the format is
pending confirmation and must not be assumed.

What IS locked (tracker SPARK_TRACKER.md v26 sec:2.1, sec:2.4):
  - Transport: BLE (not WiFi/MQTT -- that was the v35/main.md proposal
    design, superseded; RPi 4B dropped, no PostgreSQL/FastAPI/Mosquitto
    in the current architecture).
  - Payload content: JSON (tracker sec:0, item 4: "local JSON + clinical
    PDF + SHAP explainability").
  - Direction: wearable node -> gateway, on-device Layer 1+2 decision
    already made; gateway does not re-run classification.

What is NOT locked and must not be assumed here:
  - Exact JSON field names/types beyond what's structurally necessary
    for the rest of the gateway pipeline to have something to import
    against (see EventPayload below -- shaped from proposal main.md's
    superseded MQTT payload as a *reference starting point only*,
    fields: event_id, timestamp, confidence, SHAP-relevant peak
    features -- not confirmed for the current BLE design).
  - BLE service/characteristic UUIDs, MTU/chunking strategy for
    payloads that exceed a single BLE packet, framing/delimiters,
    encoding (raw JSON text vs. CBOR/msgpack vs. length-prefixed).
  - Serial fallback format, if any (proposal's dev-mode note about a
    "USB Serial (development/debug fallback)" path -- not carried
    into the current tracker, unconfirmed whether it still applies).

DO NOT extend this file to add parsing logic until the format is
confirmed. This file exists only so downstream gateway modules
(logging, SHAP stub, PDF stub) have a stable Python type to import
against without themselves guessing wire details.
"""

from __future__ import annotations

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
    Gateway-side representation of one CONFIRMED_FALL event.

    Field set is a reference draft only (see module docstring) --
    shaped from proposal main.md's now-superseded MQTT JSON payload
    description (event_id, timestamp, confidence score) plus the six
    peak IMU features SHAP attribution needs (main.md sec:shap /
    tracker sec:2.4 Stage 4). NOT confirmed against an actual firmware
    wire format. Rename/restructure freely once that format lands.
    """

    event_id: str
    timestamp: str  # ISO 8601, gateway-assigned or device-assigned -- TBD
    confidence: float  # Layer 2 CNN P(FALL), 0.0-1.0
    peak_features: dict  # {channel_name: peak_value}, keys from IMU_CHANNELS
    raw_window: Optional[list] = None  # optional full 200x6 window, if sent
    device_id: Optional[str] = None
    firmware_version: Optional[str] = None
    extra: dict = field(default_factory=dict)  # unrecognized fields, preserved


class WireFormatNotConfirmed(NotImplementedError):
    """Raised by any parse function until the real format is confirmed."""


def parse_event(raw: bytes) -> EventPayload:
    """
    Parse a raw BLE/serial frame into an EventPayload.

    Intentionally unimplemented. Do not stub this with a guessed
    format -- raise loudly so a skipped confirmation step is obvious
    at integration time rather than silently parsing garbage.
    """
    raise WireFormatNotConfirmed(
        "gateway/receiver: wire format not yet confirmed (blocked on "
        "firmware-side confirmation, see module docstring). "
        "parse_event() must not be implemented against a guessed format."
    )
