#!/usr/bin/env python3
"""
main.py

Gateway skeleton entrypoint. Wires receiver -> SHAP stub -> PDF stub
-> JSON storage into one pipeline, using NullReceiver + a manually
injected dummy event since no real wire format or live BLE hardware
exists yet this session (see gateway/receiver/wire_format.py,
gateway/receiver/receiver.py).

This is the sec:6.2 integration-benchmark shape ("Gateway receives,
logs, and reports correctly") exercised end-to-end on dummy data only
-- not a claim that the real benchmark is met, which requires real
hardware, a real wire format, and a trained model (all explicitly
blocked/gated this session).

Usage:
    python -m gateway.main
"""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone

from gateway.receiver.receiver import NullReceiver
from gateway.receiver.wire_format import EventPayload
from gateway.report.pdf_report import ReportData, generate_report
from gateway.shap_pipeline.shap_stub import get_explainer
from gateway.storage.json_store import JsonEventStore

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s: %(message)s")
logger = logging.getLogger("spark.gateway.main")


def _build_dummy_event() -> EventPayload:
    return EventPayload(
        event_id=str(uuid.uuid4()),
        timestamp=datetime.now(timezone.utc).isoformat(),
        confidence=0.94,
        peak_features={
            "a_x": 0.4,
            "a_y": 0.6,
            "a_z": 3.1,
            "w_x": 0.8,
            "w_y": 0.5,
            "w_z": 0.6,
        },
        device_id="DUMMY-DEVICE",
    )


def handle_event(event: EventPayload, store: JsonEventStore) -> None:
    logger.info("Handling event %s", event.event_id)

    explainer = get_explainer()
    shap_result = explainer.explain(event)

    report_data = ReportData(
        event_id=event.event_id,
        timestamp_iso=event.timestamp,
        severity_score=event.confidence,  # placeholder mapping, scale TBD
        cnn_confidence=event.confidence,
        shap_top_feature=shap_result.top_feature,
        shap_values=shap_result.values,
        device_id=event.device_id or "UNSET",
    )
    report_path = f"data/gateway_events/{event.event_id}.pdf"
    generate_report(report_data, report_path)

    store.save_event(event.event_id, event, shap_result, report_path)
    logger.info("Event %s: logged + reported at %s", event.event_id, report_path)


def main() -> None:
    store = JsonEventStore()
    receiver = NullReceiver(on_event=lambda e: handle_event(e, store))
    receiver.connect()
    receiver.listen()  # no-op, logs only -- see NullReceiver

    dummy = _build_dummy_event()
    receiver.inject_dummy_event(dummy)

    receiver.close()


if __name__ == "__main__":
    main()
