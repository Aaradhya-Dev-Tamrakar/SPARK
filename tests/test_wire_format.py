"""
Unit tests for gateway wire format parsing (WIRE_FORMAT_v1.md specification).
"""

import json

import pytest

from gateway.receiver.wire_format import (
    IMU_CHANNELS,
    EventPayload,
    WireFormatError,
    parse_event,
)


def test_parse_valid_event():
    raw_payload = {
        "event_id": "evt_001",
        "device_id": "spark_wearable_01",
        "firmware_version": "v1.0.0",
        "timestamp_ms": 123456,
        "confidence": 0.94,
        "peak_features": {
            "a_x": 2.8,
            "a_y": 1.2,
            "a_z": 3.1,
            "w_x": 150.0,
            "w_y": 210.5,
            "w_z": 45.0,
        },
    }
    payload_bytes = json.dumps(raw_payload).encode("utf-8")
    event = parse_event(payload_bytes)

    assert isinstance(event, EventPayload)
    assert event.event_id == "evt_001"
    assert event.device_id == "spark_wearable_01"
    assert event.firmware_version == "v1.0.0"
    assert event.timestamp_ms == 123456
    assert event.confidence == pytest.approx(0.94)
    assert len(event.peak_features) == 6
    assert event.peak_features["a_x"] == pytest.approx(2.8)
    assert event.raw_window is None


def test_parse_invalid_json():
    with pytest.raises(WireFormatError, match="not valid JSON"):
        parse_event(b"{invalid json")


def test_parse_missing_required_field():
    raw_payload = {
        "event_id": "evt_002",
        "device_id": "spark_wearable_01",
        # firmware_version missing
        "timestamp_ms": 123456,
        "confidence": 0.94,
        "peak_features": dict.fromkeys(IMU_CHANNELS, 1.0),
    }
    with pytest.raises(WireFormatError, match="missing required field"):
        parse_event(json.dumps(raw_payload).encode("utf-8"))


def test_parse_missing_imu_channel():
    raw_payload = {
        "event_id": "evt_003",
        "device_id": "spark_wearable_01",
        "firmware_version": "v1.0.0",
        "timestamp_ms": 123456,
        "confidence": 0.88,
        "peak_features": {
            "a_x": 2.8,
            "a_y": 1.2,
            # a_z missing
            "w_x": 150.0,
            "w_y": 210.5,
            "w_z": 45.0,
        },
    }
    with pytest.raises(WireFormatError, match="peak_features missing channel"):
        parse_event(json.dumps(raw_payload).encode("utf-8"))
