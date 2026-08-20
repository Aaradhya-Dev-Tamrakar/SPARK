"""
test_gateway_pipeline.py

Integration tests for the complete SPARK Gateway pipeline.
Tests verify:
    1. ReplayReceiver ingests multiple simulated events.
    2. handle_event triggers SHAP explanation, generates clinical PDF, and logs to JSON store.
    3. JSON store accurately retrieves saved events and reports.
"""

import json
from pathlib import Path

from gateway.main import build_dummy_payload, handle_event
from gateway.receiver.receiver import ReplayReceiver
from gateway.shap_pipeline.explainer import PeakFeatureExplainer
from gateway.storage.json_store import JsonEventStore


class TestGatewayPipeline:
    def test_end_to_end_event_handling(self, tmp_path: Path):
        store = JsonEventStore(store_dir=tmp_path)
        explainer = PeakFeatureExplainer()

        processed_events = []

        def on_event(event):
            pdf_path = handle_event(event, store, explainer, tmp_path)
            processed_events.append((event, pdf_path))

        # Generate 2 simulated payloads
        raw_payloads = [build_dummy_payload(f"TEST-DEV-{i}") for i in range(2)]

        receiver = ReplayReceiver(on_event=on_event, events=raw_payloads)
        receiver.connect()
        receiver.listen()
        receiver.close()

        assert len(processed_events) == 2

        for event, pdf_path in processed_events:
            assert Path(pdf_path).exists()
            assert Path(pdf_path).read_bytes().startswith(b"%PDF-")

            # Check JSON store record
            stored = store.load_event(event.event_id)
            assert stored is not None
            assert stored["event_id"] == event.event_id
            assert stored["payload"]["device_id"] == event.device_id
            assert "shap" in stored
            assert stored["shap"]["top_feature"] == "a_z"

        # Verify index.jsonl on disk
        index_file = tmp_path / "index.jsonl"
        assert index_file.exists()
        assert len(store.recent_event_ids()) == 2
