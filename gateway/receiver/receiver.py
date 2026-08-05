#!/usr/bin/env python3
"""
receiver.py

Gateway-side serial/BLE receiver skeleton for SPARK's Layer 2 (laptop
gateway), per tracker SPARK_TRACKER.md sec:2.1 item 2 ("Receives JSON
streams from wearable over BLE") and sec:6.2 ("Gateway receives, logs,
and reports correctly").

SCOPE OF THIS FILE: connection lifecycle and a transport-agnostic
callback interface only. Actual frame parsing is delegated to
gateway/receiver/wire_format.py, which is intentionally unimplemented
pending firmware-side wire-format confirmation (Action tied to this
session's scope note -- WAIT on exact format). This file must not be
extended to guess at BLE service/characteristic UUIDs or serial framing.

Explicitly NOT in scope here (repo-wide blocked list, this session):
  - Live BLE pairing/discovery against real hardware.
  - Real multi-client hotspot behavior (tracker Action #20).

What this skeleton provides:
  - A `Receiver` abstract base defining the connect/listen/on_event
    contract every transport (serial, BLE) will implement.
  - A `NullReceiver` that never receives anything -- lets the rest of
    the gateway pipeline (SHAP stub, PDF stub, storage) be exercised
    and integration-tested without live hardware.
  - Stub subclasses for the two transports named in tracker sec:2.1
    (BLE primary) and the proposal's now-superseded dev-mode serial
    fallback (kept as a stub only because it costs nothing and may be
    useful for laptop-tethered debugging; not a tracker commitment).
"""

from __future__ import annotations

import abc
import logging
from typing import Callable, Optional

from gateway.receiver.wire_format import EventPayload, parse_event

logger = logging.getLogger("spark.gateway.receiver")

EventCallback = Callable[[EventPayload], None]


class Receiver(abc.ABC):
    """
    Transport-agnostic contract for anything that can hand SPARK
    CONFIRMED_FALL events to the rest of the gateway pipeline.

    Concrete transports (BLE, serial) implement connect()/listen()/
    close(). None of them may implement frame parsing themselves --
    they must call wire_format.parse_event() so there is exactly one
    place the (currently unconfirmed) wire format is interpreted.
    """

    def __init__(self, on_event: EventCallback):
        self._on_event = on_event
        self._connected = False

    @abc.abstractmethod
    def connect(self) -> None:
        """Establish the transport connection. Raises on failure."""

    @abc.abstractmethod
    def listen(self) -> None:
        """
        Block, dispatching self._on_event(EventPayload) for each frame
        received. Concrete implementations must decode raw bytes via
        wire_format.parse_event(raw) -- never inline their own parsing.
        """

    @abc.abstractmethod
    def close(self) -> None:
        """Tear down the transport connection cleanly."""

    @property
    def connected(self) -> bool:
        return self._connected

    def _dispatch_raw(self, raw: bytes) -> None:
        """Shared helper: parse via wire_format, then dispatch."""
        event = parse_event(raw)  # raises WireFormatNotConfirmed today
        logger.info("Received event %s", getattr(event, "event_id", "?"))
        self._on_event(event)


class NullReceiver(Receiver):
    """
    No-op receiver. Connects instantly, never produces events, closes
    cleanly. Exists so gateway/main.py and integration tests can wire
    up the full pipeline (receiver -> SHAP stub -> report stub ->
    storage) end-to-end with dummy events injected manually, without
    needing live hardware or a confirmed wire format.
    """

    def connect(self) -> None:
        self._connected = True
        logger.info("NullReceiver connected (no-op, no hardware).")

    def listen(self) -> None:
        logger.info("NullReceiver listening (no-op) -- will never emit events.")

    def close(self) -> None:
        self._connected = False
        logger.info("NullReceiver closed.")

    def inject_dummy_event(self, event: EventPayload) -> None:
        """Test/dev-only: bypass wire_format entirely, dispatch directly."""
        logger.info("NullReceiver: injecting dummy event %s", event.event_id)
        self._on_event(event)


class BLEReceiver(Receiver):
    """
    BLE transport stub (primary transport per tracker sec:2.1).

    UNIMPLEMENTED. BLOCKED on:
      1. Firmware-side wire format confirmation (see wire_format.py).
      2. Live BLE pairing (repo-wide blocked item, this session).

    Candidate library (not yet chosen/vetted): `bleak` (cross-platform,
    works on the Acer Swift Go 16 laptop gateway per tracker sec:2.2).
    Not installed, not a commitment -- placeholder name only.
    """

    def __init__(self, on_event: EventCallback, device_address: Optional[str] = None):
        super().__init__(on_event)
        self.device_address = device_address

    def connect(self) -> None:
        raise NotImplementedError(
            "BLEReceiver.connect(): blocked on live BLE pairing "
            "(out of scope this session) and wire-format confirmation."
        )

    def listen(self) -> None:
        raise NotImplementedError("BLEReceiver.listen(): see connect().")

    def close(self) -> None:
        raise NotImplementedError("BLEReceiver.close(): see connect().")


class SerialReceiver(Receiver):
    """
    Serial transport stub. Not a tracker-committed transport (tracker
    sec:2.1 names BLE only) -- kept as an optional dev/debug stub for
    laptop-tethered testing, matching the proposal's now-superseded
    "USB Serial (development/debug fallback)" note. Confirm with team
    before relying on this; may be dropped if BLE-only is confirmed
    sufficient.

    UNIMPLEMENTED. Blocked on wire-format confirmation.
    """

    def __init__(self, on_event: EventCallback, port: Optional[str] = None, baud: int = 115200):
        super().__init__(on_event)
        self.port = port
        self.baud = baud

    def connect(self) -> None:
        raise NotImplementedError(
            "SerialReceiver.connect(): blocked on wire-format confirmation."
        )

    def listen(self) -> None:
        raise NotImplementedError("SerialReceiver.listen(): see connect().")

    def close(self) -> None:
        raise NotImplementedError("SerialReceiver.close(): see connect().")
