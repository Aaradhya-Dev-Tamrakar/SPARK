#!/usr/bin/env python3
"""
seed_gateway_events.py

Zero-dependency seed script for SPARK Gateway.
Uses Python standard library ONLY (no reportlab, no numpy, no bleak required).
Populates data/gateway_events with realistic simulated fall events (JSON)
and a dummy placeholder PDF so Sonia can run gateway.server immediately on fresh Windows 11.
"""

# Keep PDF cross-reference entry whitespace intact; it is part of the PDF byte format.
# ruff: noqa: W291

from __future__ import annotations

import json
import time
import uuid
from pathlib import Path

# Minimal valid single-page PDF bytes generated with zero dependencies
MINIMAL_PDF_BYTES = b"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>
endobj
4 0 obj
<< /Length 135 >>
stream
BT
/F1 20 Tf
50 720 Td
(SPARK CLINICAL INCIDENT REPORT) Tj
/F1 12 Tf
0 -30 Td
(Simulation Mode - Kathmandu Engineering College) Tj
ET
endstream
endobj
5 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj
xref
0 6
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000227 00000 n 
0000000414 00000 n 
trailer
<< /Size 6 /Root 1 0 R >>
startxref
485
%%EOF
"""

SAMPLE_SCENARIOS = [
    {
        "device_id": "SPARK-NODE-01 (Forward Trip)",
        "confidence": 0.96,
        "peak_features": {
            "a_x": 3.80,
            "a_y": 0.65,
            "a_z": 2.10,
            "w_x": 0.75,
            "w_y": 4.20,
            "w_z": 0.85,
        },
        "shap": {
            "top_feature": "w_y",
            "values": {
                "a_x": 0.28,
                "a_y": 0.05,
                "a_z": 0.16,
                "w_x": 0.06,
                "w_y": 0.38,
                "w_z": 0.07,
            },
            "clinical_summary": "Dominant pitch angular velocity (w_y) and forward surge acceleration (a_x) consistent with a forward trip mechanism.",
        },
    },
    {
        "device_id": "SPARK-NODE-02 (Lateral Slip)",
        "confidence": 0.92,
        "peak_features": {
            "a_x": 0.85,
            "a_y": 4.45,
            "a_z": 1.95,
            "w_x": 4.10,
            "w_y": 0.90,
            "w_z": 1.30,
        },
        "shap": {
            "top_feature": "a_y",
            "values": {
                "a_x": 0.08,
                "a_y": 0.44,
                "a_z": 0.12,
                "w_x": 0.25,
                "w_y": 0.05,
                "w_z": 0.06,
            },
            "clinical_summary": "Dominant lateral sway acceleration (a_y) and roll rate (w_x) indicating a side slip onto the lateral torso.",
        },
    },
    {
        "device_id": "SPARK-NODE-03 (Vertical Collapse / Syncope)",
        "confidence": 0.98,
        "peak_features": {
            "a_x": 0.35,
            "a_y": 0.40,
            "a_z": 5.75,
            "w_x": 0.45,
            "w_y": 0.60,
            "w_z": 0.30,
        },
        "shap": {
            "top_feature": "a_z",
            "values": {
                "a_x": 0.03,
                "a_y": 0.04,
                "a_z": 0.72,
                "w_x": 0.05,
                "w_y": 0.11,
                "w_z": 0.05,
            },
            "clinical_summary": "Dominant vertical impact spike (a_z) with minimal rotational velocity, characteristic of a syncope collapse.",
        },
    },
    {
        "device_id": "SPARK-NODE-04 (Rotational Twist Fall)",
        "confidence": 0.89,
        "peak_features": {
            "a_x": 1.80,
            "a_y": 2.30,
            "a_z": 2.85,
            "w_x": 2.20,
            "w_y": 1.60,
            "w_z": 4.90,
        },
        "shap": {
            "top_feature": "w_z",
            "values": {
                "a_x": 0.14,
                "a_y": 0.18,
                "a_z": 0.20,
                "w_x": 0.12,
                "w_y": 0.08,
                "w_z": 0.28,
            },
            "clinical_summary": "Dominant yaw rotation (w_z) with multi-axis acceleration indicating a rotational twist during movement.",
        },
    },
]


def seed_events(store_dir: Path = Path("data/gateway_events")) -> list[str]:
    store_dir.mkdir(parents=True, exist_ok=True)
    index_path = store_dir / "index.jsonl"
    created_ids: list[str] = []

    now_ms = int(time.time() * 1000)

    for i, scenario in enumerate(SAMPLE_SCENARIOS):
        event_id = str(uuid.uuid4())[:8].upper()
        created_ids.append(event_id)

        pdf_path = store_dir / f"SPARK_Report_{event_id}.pdf"
        if not pdf_path.exists():
            pdf_path.write_bytes(MINIMAL_PDF_BYTES)

        record = {
            "event_id": event_id,
            "payload": {
                "event_id": event_id,
                "device_id": scenario["device_id"],
                "firmware_version": "v1.0.0-s3",
                "timestamp_ms": now_ms - (len(SAMPLE_SCENARIOS) - i) * 60000,
                "confidence": scenario["confidence"],
                "peak_features": scenario["peak_features"],
            },
            "shap": scenario["shap"],
            "report_path": str(pdf_path),
        }

        event_file = store_dir / f"{event_id}.json"
        event_file.write_text(json.dumps(record, indent=2), encoding="utf-8")

        with index_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"event_id": event_id, "report_path": str(pdf_path)}) + "\n")

    print(f"[OK] Successfully seeded {len(created_ids)} simulated fall events into {store_dir}")
    print(f"     Event IDs: {', '.join(created_ids)}")
    return created_ids


if __name__ == "__main__":
    seed_events()
