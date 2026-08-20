#!/usr/bin/env python3
"""
test_gateway_server.py

Unit tests for SPARK Gateway REST & Dashboard Server (gateway/server.py).
"""

import json
import threading
import urllib.error
import urllib.request
from pathlib import Path

import pytest

from gateway.receiver.wire_format import EventPayload
from gateway.server import create_server
from gateway.shap_pipeline.explainer import ShapAttribution
from gateway.storage.json_store import JsonEventStore


@pytest.fixture
def server_fixture(tmp_path: Path):
    store_dir = tmp_path / "events"
    store_dir.mkdir(parents=True, exist_ok=True)
    store = JsonEventStore(store_dir=store_dir)

    # Seed one test event
    event = EventPayload(
        event_id="TEST001",
        device_id="SPARK-NODE-01",
        firmware_version="v1.0.0-s3",
        timestamp_ms=1700000000000,
        confidence=0.92,
        peak_features={"a_x": 0.4, "a_y": 0.6, "a_z": 3.8, "w_x": 0.8, "w_y": 1.4, "w_z": 0.7},
    )
    shap_res = ShapAttribution(
        values={"a_z": 0.48, "w_y": 0.22},
        top_feature="a_z",
        clinical_summary="High vertical impact detected.",
    )
    # Create dummy pdf
    pdf_path = store_dir / "SPARK_Report_TEST001.pdf"
    pdf_path.write_bytes(b"%PDF-1.4 dummy report content")

    store.save_event("TEST001", event, shap_res, str(pdf_path))

    # Start server on ephemeral port (127.0.0.1:0 lets OS assign port)
    server = create_server(host="127.0.0.1", port=0, store_dir=store_dir)
    port = server.server_address[1]

    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    base_url = f"http://127.0.0.1:{port}"
    yield base_url

    server.shutdown()
    server.server_close()


def test_server_dashboard_root(server_fixture: str):
    with urllib.request.urlopen(f"{server_fixture}/") as response:
        assert response.status == 200
        html = response.read().decode("utf-8")
        assert "SPARK Fall Detection Gateway" in html
        assert "Recent Fall Incidents" in html


def test_server_health_check(server_fixture: str):
    with urllib.request.urlopen(f"{server_fixture}/api/health") as response:
        assert response.status == 200
        data = json.loads(response.read().decode("utf-8"))
        assert data["status"] == "healthy"
        assert data["service"] == "spark-gateway-api"


def test_server_list_events(server_fixture: str):
    with urllib.request.urlopen(f"{server_fixture}/api/events") as response:
        assert response.status == 200
        events = json.loads(response.read().decode("utf-8"))
        assert len(events) == 1
        assert events[0]["event_id"] == "TEST001"
        assert events[0]["confidence"] == 0.92


def test_server_get_event_detail(server_fixture: str):
    with urllib.request.urlopen(f"{server_fixture}/api/events/TEST001") as response:
        assert response.status == 200
        data = json.loads(response.read().decode("utf-8"))
        assert data["event_id"] == "TEST001"
        assert data["shap"]["top_feature"] == "a_z"


def test_server_get_event_not_found(server_fixture: str):
    with pytest.raises(urllib.error.HTTPError) as exc_info:
        urllib.request.urlopen(f"{server_fixture}/api/events/NONEXISTENT")
    assert exc_info.value.code == 404


def test_server_get_pdf_report(server_fixture: str):
    with urllib.request.urlopen(f"{server_fixture}/api/reports/TEST001") as response:
        assert response.status == 200
        assert response.headers.get("Content-Type") == "application/pdf"
        body = response.read()
        assert body.startswith(b"%PDF-1.4")


def test_server_get_pdf_report_not_found(server_fixture: str):
    with pytest.raises(urllib.error.HTTPError) as exc_info:
        urllib.request.urlopen(f"{server_fixture}/api/reports/MISSING")
    assert exc_info.value.code == 404
