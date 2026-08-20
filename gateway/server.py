#!/usr/bin/env python3
"""
server.py

SPARK Gateway Local REST & Dashboard Server.
Provides local network endpoints to serve incident records and clinical PDF
reports to the web/mobile display client (Layer 3), per SPARK_TRACKER.md §2.1.

Endpoints:
  - GET /                   : Embedded responsive web dashboard
  - GET /api/health         : Service health check
  - GET /api/events         : List recent fall event records (JSON)
  - GET /api/events/<id>    : Retrieve specific event details (JSON)
  - GET /api/reports/<id>   : Download/view clinical PDF report (PDF)
"""

from __future__ import annotations

import argparse
import json
import logging
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from gateway.storage.json_store import JsonEventStore

logger = logging.getLogger("spark.gateway.server")

DASHBOARD_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SPARK Fall Detection Gateway</title>
    <style>
        :root {
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --accent-red: #ef4444;
            --accent-green: #22c55e;
            --accent-blue: #3b82f6;
            --border-color: #334155;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-primary);
            margin: 0;
            padding: 24px;
        }
        .container {
            max-width: 960px;
            margin: 0 auto;
        }
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 16px;
            margin-bottom: 24px;
        }
        h1 { margin: 0; font-size: 24px; display: flex; align-items: center; gap: 8px; }
        .badge-live {
            background-color: rgba(34, 197, 94, 0.2);
            color: var(--accent-green);
            font-size: 12px;
            padding: 4px 8px;
            border-radius: 9999px;
            border: 1px solid var(--accent-green);
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }
        .stat-card {
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 16px;
        }
        .stat-label { color: var(--text-secondary); font-size: 13px; margin-bottom: 4px; }
        .stat-value { font-size: 24px; font-weight: bold; }
        .event-card {
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 18px;
            margin-bottom: 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .event-title { font-size: 16px; font-weight: bold; margin-bottom: 4px; }
        .event-meta { font-size: 13px; color: var(--text-secondary); }
        .btn-pdf {
            background-color: var(--accent-blue);
            color: white;
            padding: 8px 16px;
            border-radius: 6px;
            text-decoration: none;
            font-size: 13px;
            font-weight: 500;
        }
        .btn-pdf:hover { opacity: 0.9; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>⚡ SPARK Clinical Gateway <span class="badge-live">● SYSTEM ACTIVE</span></h1>
            <div>Layer 3 Local Display</div>
        </header>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Total Fall Incidents</div>
                <div class="stat-value" id="stat-total">--</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Latest Node Confirmed</div>
                <div class="stat-value" id="stat-latest-node">--</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Explainability Engine</div>
                <div class="stat-value" style="color: var(--accent-green)">Active (SHAP)</div>
            </div>
        </div>

        <h2>Recent Fall Incidents</h2>
        <div id="events-list">Loading telemetry stream...</div>
    </div>

    <script>
        async function fetchEvents() {
            try {
                const res = await fetch('/api/events');
                const data = await res.json();
                document.getElementById('stat-total').innerText = data.length;
                if (data.length > 0) {
                    document.getElementById('stat-latest-node').innerText = data[0].device_id || 'SPARK-NODE-01';
                }
                const container = document.getElementById('events-list');
                if (data.length === 0) {
                    container.innerHTML = '<p style="color: var(--text-secondary)">No fall incidents recorded yet.</p>';
                    return;
                }
                container.innerHTML = data.map(ev => `
                    <div class="event-card">
                        <div>
                            <div class="event-title">🚨 Confirmed Fall Event #${ev.event_id}</div>
                            <div class="event-meta">
                                Device: <strong>${ev.device_id}</strong> &nbsp;|&nbsp;
                                Confidence: <strong>${(ev.confidence * 100).toFixed(1)}%</strong> &nbsp;|&nbsp;
                                Primary Trigger: <strong>${ev.shap_top_feature || 'a_z'}</strong>
                            </div>
                        </div>
                        <a class="btn-pdf" href="/api/reports/${ev.event_id}" target="_blank">📄 View Clinical PDF</a>
                    </div>
                `).join('');
            } catch (err) {
                document.getElementById('events-list').innerText = 'Failed to connect to gateway API: ' + err;
            }
        }
        fetchEvents();
        setInterval(fetchEvents, 3000);
    </script>
</body>
</html>
"""


class GatewayRequestHandler(BaseHTTPRequestHandler):
    store: JsonEventStore
    store_dir: Path

    def _set_cors_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _send_json(self, status: int, data: Any) -> None:
        payload = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self._set_cors_headers()
        self.end_headers()
        self.wfile.write(payload)

    def do_OPTIONS(self) -> None:
        self.send_response(HTTPStatus.NO_CONTENT)
        self._set_cors_headers()
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        # 1. Web Dashboard Root
        if path == "" or path == "/":
            body = DASHBOARD_HTML_TEMPLATE.encode("utf-8")
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self._set_cors_headers()
            self.end_headers()
            self.wfile.write(body)
            return

        # 2. API Health
        if path == "/api/health":
            self._send_json(
                HTTPStatus.OK,
                {
                    "status": "healthy",
                    "service": "spark-gateway-api",
                    "version": "1.0.0",
                },
            )
            return

        # 3. API Events List
        if path == "/api/events":
            records = self.store.list_events()
            self._send_json(HTTPStatus.OK, records)
            return

        # 4. API Event Detail
        if path.startswith("/api/events/"):
            event_id = path.split("/api/events/")[1].strip()
            record = self.store.load_event(event_id)
            if record:
                self._send_json(HTTPStatus.OK, record)
            else:
                self._send_json(HTTPStatus.NOT_FOUND, {"error": f"Event {event_id} not found"})
            return

        # 5. API PDF Report Download
        if path.startswith("/api/reports/"):
            event_id = path.split("/api/reports/")[1].strip()
            # Check for PDF file matching pattern
            pdf_path = self.store_dir / f"SPARK_Report_{event_id}.pdf"
            if not pdf_path.is_file():
                # Fallback to direct event_id.pdf
                pdf_path = self.store_dir / f"{event_id}.pdf"

            if pdf_path.is_file():
                pdf_bytes = pdf_path.read_bytes()
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-Type", "application/pdf")
                self.send_header(
                    "Content-Disposition", f'inline; filename="SPARK_Report_{event_id}.pdf"'
                )
                self.send_header("Content-Length", str(len(pdf_bytes)))
                self._set_cors_headers()
                self.end_headers()
                self.wfile.write(pdf_bytes)
            else:
                self._send_json(
                    HTTPStatus.NOT_FOUND, {"error": f"Report PDF for event {event_id} not found"}
                )
            return

        # Not Found
        self._send_json(HTTPStatus.NOT_FOUND, {"error": f"Endpoint {path} not found"})

    def log_message(self, format: str, *args: Any) -> None:
        logger.debug(
            "%s - - [%s] %s", self.address_string(), self.log_date_time_string(), format % args
        )


def create_server(
    host: str = "0.0.0.0", port: int = 8000, store_dir: Path = Path("data/gateway_events")
) -> ThreadingHTTPServer:
    """Create a configured ThreadingHTTPServer instance for the SPARK gateway API."""
    store_dir.mkdir(parents=True, exist_ok=True)
    store = JsonEventStore(store_dir=store_dir)

    class CustomHandler(GatewayRequestHandler):
        pass

    CustomHandler.store = store
    CustomHandler.store_dir = store_dir

    server = ThreadingHTTPServer((host, port), CustomHandler)
    logger.info("SPARK Gateway Server configured at http://%s:%d", host, port)
    return server


def main() -> None:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    parser = argparse.ArgumentParser(description="SPARK Gateway REST API & Dashboard Server")
    parser.add_argument("--host", default="0.0.0.0", help="Binding host (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8000, help="Port number (default: 8000)")
    parser.add_argument(
        "--store-dir",
        type=Path,
        default=Path("data/gateway_events"),
        help="Incident storage directory",
    )
    args = parser.parse_args()

    server = create_server(host=args.host, port=args.port, store_dir=args.store_dir)
    print(f"🚀 SPARK Gateway API & Dashboard running at http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
