#!/usr/bin/env python3
"""
main.py

SPARK Gateway Service Entrypoint.
Orchestrates the real-time event pipeline:
  [Event Receiver: BLE / Serial / Replay / Null]
       ↓
  [Wire Format Parser: parse_event()]
       ↓
  [SHAP Explainability Engine: get_explainer()]
       ↓
  [Clinical PDF Incident Report: generate_report()]
       ↓
  [Local JSON Storage: JsonEventStore]

Usage:
    # Run in mock/null mode with a dummy event
    python -m gateway.main --mode null

    # Replay simulated fall events
    python -m gateway.main --mode replay

    # Listen on USB Serial COM port
    python -m gateway.main --mode serial --port COM3
"""

from __future__ import annotations

import argparse
import json
import logging
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

from gateway.receiver.receiver import BleReceiver, NullReceiver, ReplayReceiver, SerialReceiver
from gateway.receiver.wire_format import EventPayload
from gateway.report.pdf_report import ReportData, generate_report
from gateway.shap_pipeline.explainer import ShapExplainer, get_explainer
from gateway.storage.json_store import JsonEventStore

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("spark.gateway")


def build_dummy_payload(device_id: str = "SPARK-NODE-01") -> bytes:
    """Build a realistic wire format JSON payload matching docs/WIRE_FORMAT_v1.md."""
    payload = {
        "event_id": str(uuid.uuid4())[:8].upper(),
        "device_id": device_id,
        "firmware_version": "v1.0.0-s3",
        "timestamp_ms": int(time.time() * 1000),
        "confidence": 0.94,
        "peak_features": {
            "a_x": 0.45,
            "a_y": 0.62,
            "a_z": 3.85,
            "w_x": 0.85,
            "w_y": 1.42,
            "w_z": 0.70,
        },
    }
    return json.dumps(payload).encode("utf-8")


def handle_event(
    event: EventPayload,
    store: JsonEventStore,
    explainer: ShapExplainer,
    out_dir: Path,
) -> Path:
    """Process a single fall event: compute SHAP, render PDF, and archive to JSON."""
    logger.info("Processing confirmed fall event: %s (Device: %s)", event.event_id, event.device_id)

    # 1. Compute feature attribution
    shap_result = explainer.explain(event)
    logger.info(
        "SHAP top feature: %s (Attribution: %.1f%%)",
        shap_result.top_feature,
        shap_result.values.get(shap_result.top_feature, 0.0) * 100,
    )

    # 2. Build report view model
    ts_str = datetime.fromtimestamp(event.timestamp_ms / 1000.0, tz=timezone.utc).strftime(
        "%Y-%m-%d %H:%M:%S UTC"
    )
    report_data = ReportData(
        event_id=event.event_id,
        timestamp_iso=ts_str,
        severity_score=min(max(event.confidence, 0.0), 1.0),
        cnn_confidence=event.confidence,
        shap_top_feature=shap_result.top_feature,
        shap_values=shap_result.values,
        device_id=event.device_id,
        firmware_version=event.firmware_version,
        clinical_summary=shap_result.clinical_summary,
        temporal_attributions=shap_result.temporal_attributions,
    )

    # 3. Generate clinical PDF report
    pdf_path = out_dir / f"SPARK_Report_{event.event_id}.pdf"
    generate_report(report_data, pdf_path)
    logger.info("Clinical PDF report written to: %s", pdf_path)

    # 4. Save to local JSON store
    store.save_event(event.event_id, event, shap_result, str(pdf_path))
    logger.info("Event record archived in JSON store.")

    return pdf_path


def main() -> None:
    ap = argparse.ArgumentParser(description="SPARK Gateway Incident Ingestion Service")
    ap.add_argument(
        "--mode",
        choices=["null", "replay", "serial", "ble"],
        default="null",
        help="Receiver transport mode (default: null)",
    )
    ap.add_argument(
        "--replay-file",
        type=Path,
        default=None,
        help="Path to JSON file containing recorded events for replay mode",
    )
    ap.add_argument("--port", default="COM3", help="Serial port for serial mode (default: COM3)")
    ap.add_argument("--baud", type=int, default=115200, help="Serial baud rate (default: 115200)")
    ap.add_argument(
        "--ble-addr",
        default=None,
        help="Target BLE device MAC/UUID address (optional, scans for SPARK-* by default)",
    )
    ap.add_argument(
        "--model",
        type=Path,
        default=Path("data/processed_sisfall/model/spark_cnn.keras"),
        help="Path to trained Keras model for SHAP attribution",
    )
    ap.add_argument(
        "--out-dir",
        type=Path,
        default=Path("data/gateway_events"),
        help="Directory to save generated PDF reports and records",
    )
    args = ap.parse_args()

    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    store = JsonEventStore(store_dir=out_dir)
    explainer = get_explainer(model_path=args.model)
    logger.info("Initialized %s", explainer.__class__.__name__)

    if args.mode == "null":
        null_rx = NullReceiver(on_event=lambda e: handle_event(e, store, explainer, out_dir))
        null_rx.connect()
        # Inject one dummy event to verify end-to-end flow
        raw = build_dummy_payload()
        null_rx.inject_raw_payload(raw)
        null_rx.close()

    elif args.mode == "replay":
        sample_events = [build_dummy_payload(f"SPARK-NODE-0{i + 1}") for i in range(3)]
        replay_rx = ReplayReceiver(
            on_event=lambda e: handle_event(e, store, explainer, out_dir),
            events=sample_events if not args.replay_file else None,
            file_path=args.replay_file,
            interval_s=0.5,
        )
        replay_rx.connect()
        replay_rx.listen()
        replay_rx.close()

    elif args.mode == "serial":
        serial_rx = SerialReceiver(
            on_event=lambda e: handle_event(e, store, explainer, out_dir),
            port=args.port,
            baud=args.baud,
        )
        try:
            serial_rx.connect()
            serial_rx.listen()
        except KeyboardInterrupt:
            logger.info("Interrupted by user.")
        finally:
            serial_rx.close()

    elif args.mode == "ble":
        ble_rx = BleReceiver(
            on_event=lambda e: handle_event(e, store, explainer, out_dir),
            device_address=args.ble_addr,
        )
        try:
            ble_rx.connect()
            ble_rx.listen()
        except KeyboardInterrupt:
            logger.info("BLE receiver interrupted by user.")
        finally:
            ble_rx.close()


if __name__ == "__main__":
    main()
