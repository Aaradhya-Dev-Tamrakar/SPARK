#!/usr/bin/env python3
"""
json_store.py

Local JSON logging/storage stub for SPARK's gateway, per tracker
SPARK_TRACKER.md sec:0 item 4 ("Output: local JSON + clinical PDF +
SHAP explainability") and sec:6.2 integration-benchmark verification
target ("Gateway receives, logs, and reports correctly").

No database. The proposal's PostgreSQL `fall_events` table (main.md
sec:gateway_impl) is part of the superseded MQTT/FastAPI/RPi design
and is NOT the current tracker architecture -- current design is
"local JSON" only (tracker sec:0/sec:2.1), so this stub writes flat
JSON files, not a DB-backed store. Do not add a DB dependency here
without a tracker update confirming that decision reversed.

One JSON file per event, plus an append-only index for "recent events"
listing (mirrors the proposal's dashboard "most recent 50 events" idea,
main.md ~line 1067, minus the Streamlit dashboard itself -- out of
scope, no dashboard requested this session).
"""

from __future__ import annotations

import json
import logging
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger("spark.gateway.storage")

DEFAULT_STORE_DIR = Path("data/gateway_events")  # under repo data/, gitignored


def _to_jsonable(obj: Any) -> Any:
    """Dataclasses (EventPayload, ShapAttribution, ReportData) -> dict."""
    if is_dataclass(obj) and not isinstance(obj, type):
        return asdict(obj)
    return obj


class JsonEventStore:
    """
    Flat-file JSON store: one file per event under store_dir, named
    <event_id>.json, plus an append-only index.jsonl for fast recent-
    events listing without re-reading every event file.

    Not thread-safe / not concurrency-tested -- single-gateway-process
    assumption matches tracker sec:2.1 ("laptop as sole gateway").
    """

    def __init__(self, store_dir: Optional[Path] = None):
        self.store_dir = Path(store_dir) if store_dir else DEFAULT_STORE_DIR
        self.store_dir.mkdir(parents=True, exist_ok=True)
        self.index_path = self.store_dir / "index.jsonl"

    def save_event(
        self,
        event_id: str,
        payload: Any,
        shap: Any = None,
        report_path: Optional[str] = None,
    ) -> Path:
        """
        Persists one event's full record (raw payload + SHAP result +
        path to its generated PDF, if any) as <event_id>.json, and
        appends a summary line to index.jsonl.
        """
        record: Dict[str, Any] = {
            "event_id": event_id,
            "payload": _to_jsonable(payload),
            "shap": _to_jsonable(shap) if shap is not None else None,
            "report_path": report_path,
        }

        event_path = self.store_dir / f"{event_id}.json"
        event_path.write_text(json.dumps(record, indent=2, default=str))
        logger.info("Saved event record to %s", event_path)

        with self.index_path.open("a") as f:
            f.write(json.dumps({"event_id": event_id, "report_path": report_path}) + "\n")

        return event_path

    def load_event(self, event_id: str) -> Dict[str, Any]:
        event_path = self.store_dir / f"{event_id}.json"
        return json.loads(event_path.read_text())

    def recent_event_ids(self, limit: int = 50) -> list[str]:
        """Mirrors proposal's 'most recent 50 events' framing, no dashboard."""
        if not self.index_path.exists():
            return []
        lines = self.index_path.read_text().splitlines()
        ids = [json.loads(line)["event_id"] for line in lines if line.strip()]
        return ids[-limit:][::-1]
