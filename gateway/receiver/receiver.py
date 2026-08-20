#!/usr/bin/env python3
"""
receiver.py

Gateway-side serial/BLE/replay receiver for SPARK's Layer 2 (laptop gateway),
per tracker SPARK_TRACKER.md sec:2.1 item 2 ("Receives JSON streams from wearable over BLE")
and sec:6.2 ("Gateway receives, logs, and reports correctly").

Provides:
  - `Receiver`: Abstract base defining connection lifecycle and dispatching via wire_format.
  - `NullReceiver`: No-op receiver for integration tests with manual injection.
  - `ReplayReceiver`: Replays recorded JSON events from files or lists for testing/demo.
  - `SerialReceiver`: Reads line-delimited JSON streams from a USB-Serial COM port.
  - `BLEReceiver`: Stub for BLE GATT notifications (hardware pairing scope).
"""

from __future__ import annotations

import abc
import json
import logging
import time
from collections.abc import Callable
from pathlib import Path

from gateway.receiver.wire_format import EventPayload, parse_event

logger = logging.getLogger("spark.gateway.receiver")

EventCallback = Callable[[EventPayload], None]


class Receiver(abc.ABC):
    """
    Transport-agnostic contract for anything that hands SPARK CONFIRMED_FALL
    events to the rest of the gateway pipeline.
    """

    def __init__(self, on_event: EventCallback):
        self._on_event = on_event
        self._connected = False

    @abc.abstractmethod
    def connect(self) -> None:
        """Establish the transport connection. Raises on failure."""

    @abc.abstractmethod
    def listen(self) -> None:
        """Block or loop, dispatching self._on_event(EventPayload) for each frame received."""

    @abc.abstractmethod
    def close(self) -> None:
        """Tear down the transport connection cleanly."""

    @property
    def connected(self) -> bool:
        return self._connected

    def _dispatch_raw(self, raw: bytes) -> None:
        """Shared helper: parse via wire_format, then dispatch."""
        event = parse_event(raw)
        logger.info("Received and parsed event %s", event.event_id)
        self._on_event(event)


class NullReceiver(Receiver):
    """
    No-op receiver. Connects instantly, never produces events on its own, closes cleanly.
    Allows manual event injection for deterministic testing.
    """

    def connect(self) -> None:
        self._connected = True
        logger.info("NullReceiver connected (mock/manual injection mode).")

    def listen(self) -> None:
        logger.info("NullReceiver listening -- waiting for injected events.")

    def close(self) -> None:
        self._connected = False
        logger.info("NullReceiver closed.")

    def inject_dummy_event(self, event: EventPayload) -> None:
        """Inject an already-parsed EventPayload directly."""
        logger.info("NullReceiver: injecting event %s", event.event_id)
        self._on_event(event)

    def inject_raw_payload(self, raw: bytes) -> None:
        """Inject raw JSON wire bytes through the parsing path."""
        self._dispatch_raw(raw)


class ReplayReceiver(Receiver):
    """
    Replay receiver that emits a sequence of recorded or simulated JSON events.
    Useful for automated verification, CI, and laptop demo sessions.
    """

    def __init__(
        self,
        on_event: EventCallback,
        events: list[dict | bytes | str] | None = None,
        file_path: Path | str | None = None,
        interval_s: float = 0.0,
    ):
        super().__init__(on_event)
        self.events: list[bytes] = []
        self.interval_s = interval_s

        if events:
            for e in events:
                if isinstance(e, bytes):
                    self.events.append(e)
                elif isinstance(e, str):
                    self.events.append(e.encode("utf-8"))
                elif isinstance(e, dict):
                    self.events.append(json.dumps(e).encode("utf-8"))

        if file_path:
            p = Path(file_path)
            if p.exists():
                text = p.read_text(encoding="utf-8")
                # Support either JSON array or line-delimited JSON
                text_strip = text.strip()
                if text_strip.startswith("[") and text_strip.endswith("]"):
                    items = json.loads(text_strip)
                    for item in items:
                        self.events.append(json.dumps(item).encode("utf-8"))
                else:
                    for line in text.splitlines():
                        if line.strip():
                            self.events.append(line.strip().encode("utf-8"))

    def connect(self) -> None:
        self._connected = True
        logger.info("ReplayReceiver connected (%d events queued).", len(self.events))

    def listen(self) -> None:
        if not self._connected:
            raise RuntimeError("Cannot listen on disconnected ReplayReceiver.")

        for i, raw in enumerate(self.events):
            logger.info("Replaying event %d/%d", i + 1, len(self.events))
            self._dispatch_raw(raw)
            if self.interval_s > 0 and i < len(self.events) - 1:
                time.sleep(self.interval_s)

    def close(self) -> None:
        self._connected = False
        logger.info("ReplayReceiver closed.")


class SerialReceiver(Receiver):
    """
    Serial port receiver for laptop-tethered development testing.
    Reads line-delimited JSON packets matching docs/WIRE_FORMAT_v1.md over USB Serial.
    """

    def __init__(self, on_event: EventCallback, port: str = "COM3", baud: int = 115200):
        super().__init__(on_event)
        self.port = port
        self.baud = baud
        self._serial = None

    def connect(self) -> None:
        try:
            import serial

            self._serial = serial.Serial(self.port, self.baud, timeout=1.0)
            self._connected = True
            logger.info("SerialReceiver connected on %s @ %d baud", self.port, self.baud)
        except ImportError as err:
            raise ImportError(
                "pyserial is required for SerialReceiver. Install via `pip install pyserial`."
            ) from err
        except Exception as e:
            self._connected = False
            raise ConnectionError(f"Failed to open serial port {self.port}: {e}") from e

    def listen(self) -> None:
        if not self._connected or not self._serial:
            raise RuntimeError("Cannot listen on disconnected SerialReceiver.")

        logger.info("SerialReceiver listening on %s...", self.port)
        while self._connected:
            line = self._serial.readline()
            if line:
                line_str = line.decode("utf-8", errors="replace").strip()
                if line_str.startswith("{") and line_str.endswith("}"):
                    try:
                        self._dispatch_raw(line_str.encode("utf-8"))
                    except Exception as e:
                        logger.warning("Error parsing serial frame: %s", e)

    def close(self) -> None:
        self._connected = False
        if self._serial and self._serial.is_open:
            self._serial.close()
        logger.info("SerialReceiver closed.")


class BLEReceiver(Receiver):
    """
    BLE GATT transport receiver stub.
    """

    def __init__(self, on_event: EventCallback, device_address: str | None = None):
        super().__init__(on_event)
        self.device_address = device_address

    def connect(self) -> None:
        raise NotImplementedError(
            "BLEReceiver.connect(): blocked on live BLE pairing hardware integration."
        )

    def listen(self) -> None:
        raise NotImplementedError("BLEReceiver.listen(): see connect().")

    def close(self) -> None:
        raise NotImplementedError("BLEReceiver.close(): see connect().")
