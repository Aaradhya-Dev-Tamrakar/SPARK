#!/usr/bin/env python3
"""
test_ble_receiver.py

Unit tests for BleReceiver in gateway/receiver/receiver.py.
"""

import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from gateway.receiver.receiver import BLEReceiver, BleReceiver
from gateway.receiver.wire_format import EventPayload


@pytest.fixture
def sample_payload_bytes() -> bytes:
    payload = {
        "event_id": "BLE001",
        "device_id": "SPARK-NODE-01",
        "firmware_version": "v1.0.0-s3",
        "timestamp_ms": 1700000000000,
        "confidence": 0.96,
        "peak_features": {
            "a_x": 0.35,
            "a_y": 0.55,
            "a_z": 3.90,
            "w_x": 0.80,
            "w_y": 1.25,
            "w_z": 0.65,
        },
    }
    return json.dumps(payload).encode("utf-8")


def test_ble_receiver_init():
    callback = MagicMock()
    rx = BleReceiver(on_event=callback, device_address="AA:BB:CC:DD:EE:FF")
    assert rx.device_address == "AA:BB:CC:DD:EE:FF"
    assert not rx.connected
    assert rx.service_uuid == BleReceiver.DEFAULT_SERVICE_UUID
    assert rx.char_uuid == BleReceiver.DEFAULT_CHAR_UUID


def test_ble_receiver_backward_compat_alias():
    callback = MagicMock()
    rx = BLEReceiver(on_event=callback)
    assert isinstance(rx, BleReceiver)


def test_ble_notification_handler(sample_payload_bytes):
    received_events = []
    rx = BleReceiver(on_event=lambda e: received_events.append(e))

    # Simulate incoming GATT notification bytearray
    rx._notification_handler(0, bytearray(sample_payload_bytes))

    assert len(received_events) == 1
    event = received_events[0]
    assert isinstance(event, EventPayload)
    assert event.event_id == "BLE001"
    assert event.confidence == 0.96
    assert event.peak_features["a_z"] == 3.90


def test_ble_connect_with_mocked_bleak():
    callback = MagicMock()
    rx = BleReceiver(on_event=callback, device_address="AA:BB:CC:DD:EE:FF")

    mock_client = MagicMock()
    mock_client.address = "AA:BB:CC:DD:EE:FF"
    mock_client.is_connected = True
    mock_client.connect = AsyncMock()
    mock_client.disconnect = AsyncMock()

    with patch("bleak.BleakClient", return_value=mock_client):
        rx.connect(timeout=1.0)
        assert rx.connected
        assert rx._client is not None

        rx.close()
        assert not rx.connected
        assert rx._client is None


def test_ble_connect_failure_raises_connection_error():
    callback = MagicMock()
    rx = BleReceiver(on_event=callback, device_address="INVALID:ADDR")

    mock_client = MagicMock()
    mock_client.connect = AsyncMock(side_effect=RuntimeError("GATT connection failed"))

    with patch("bleak.BleakClient", return_value=mock_client):
        with pytest.raises(ConnectionError, match="Failed to connect to BLE device"):
            rx.connect(timeout=1.0)
        assert not rx.connected
