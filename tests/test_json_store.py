"""
Unit tests for JSON event persistence.
"""

from gateway.receiver.wire_format import IMU_CHANNELS, EventPayload
from gateway.storage.json_store import JsonEventStore


def test_json_store_save_and_load(tmp_path):
    store = JsonEventStore(store_dir=tmp_path)

    payload = EventPayload(
        event_id="evt_test_001",
        device_id="dev_001",
        firmware_version="v1.0.0",
        timestamp_ms=5000,
        confidence=0.92,
        peak_features=dict.fromkeys(IMU_CHANNELS, 1.5),
    )

    path = store.save_event(event_id="evt_test_001", payload=payload)
    assert path.exists()

    loaded = store.load_event("evt_test_001")
    assert loaded["event_id"] == "evt_test_001"
    assert loaded["payload"]["confidence"] == 0.92
