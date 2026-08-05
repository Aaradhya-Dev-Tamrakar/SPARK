#!/usr/bin/env python3
"""
pdf_report.py

Clinical PDF incident report skeleton for SPARK's gateway (Layer 2),
per tracker SPARK_TRACKER.md sec:2.3 Claim 5 ("Auto-generated clinical
PDF reports") and sec:3 WP3 ("Clinical PDF report design + feedback
iteration" -- Sonia Thapa's item).

SCOPE: this session builds layout/fields only, populated with dummy
data (per this session's scope note: "layout/fields aren't gated by
real data -- build with dummy data"). Actual patient PDF content is
explicitly out of scope/blocked this session. Do not wire this to a
real EventPayload/ShapAttribution pipeline output expecting patient-
identifying content -- swap DUMMY_EVENT for real data only once that
gate is lifted, and route the field/layout *design* decisions through
Sonia (owner, tracker sec:3) first, not just the data source.

Reference content (proposal main.md sec:pdf_report, superseded
transport/DB details aside -- the *field list* is the only documented
spec and is reused here): timestamp, fall severity score, Layer 2 CNN
confidence score, SHAP top-contributing feature, full SHAP vector bar
chart, signature block for care-staff acknowledgement. One page.

Uses `reportlab` (already the repo's documented gateway dependency,
proposal main.md line ~1075: "ReportLab generates a one-page PDF...");
confirmed installed in this environment this session.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

from gateway.receiver.wire_format import IMU_CHANNELS


@dataclass
class ReportData:
    """
    Flat view-model for the PDF template. Deliberately decoupled from
    EventPayload/ShapAttribution (gateway/receiver, gateway/shap_pipeline)
    so template/layout changes (Sonia's ongoing design iteration) don't
    ripple into pipeline code, and so DUMMY_EVENT below can exist
    without importing real pipeline types.
    """

    event_id: str
    timestamp_iso: str
    severity_score: float  # 0.0-1.0, placeholder scale -- not yet defined
    cnn_confidence: float  # Layer 2 P(FALL), 0.0-1.0
    shap_top_feature: str
    shap_values: Dict[str, float]  # channel_name -> attribution
    device_id: str = "UNSET"


# Dummy data only -- no real patient content (blocked this session).
DUMMY_EVENT = ReportData(
    event_id="DUMMY-EVT-0001",
    timestamp_iso=datetime.now(timezone.utc).isoformat(),
    severity_score=0.72,
    cnn_confidence=0.94,
    shap_top_feature="a_z",
    shap_values={
        "a_x": 0.05,
        "a_y": 0.10,
        "a_z": 0.55,
        "w_x": 0.08,
        "w_y": 0.12,
        "w_z": 0.10,
    },
    device_id="DUMMY-DEVICE",
)


PAGE_W, PAGE_H = A4
MARGIN = 20 * mm


def _draw_header(c: canvas.Canvas, data: ReportData) -> float:
    """Draws title block. Returns the y-coordinate to continue below."""
    y = PAGE_H - MARGIN

    c.setFont("Helvetica-Bold", 16)
    c.drawString(MARGIN, y, "SPARK Fall Incident Report")
    y -= 8 * mm

    c.setFont("Helvetica", 9)
    c.setFillColor(colors.grey)
    c.drawString(
        MARGIN,
        y,
        "DRAFT LAYOUT -- dummy data, not a real patient record",
    )
    c.setFillColor(colors.black)
    y -= 10 * mm

    c.setFont("Helvetica", 10)
    c.drawString(MARGIN, y, f"Event ID: {data.event_id}")
    y -= 5 * mm
    c.drawString(MARGIN, y, f"Timestamp: {data.timestamp_iso}")
    y -= 5 * mm
    c.drawString(MARGIN, y, f"Device: {data.device_id}")
    y -= 10 * mm

    return y


def _draw_scores(c: canvas.Canvas, data: ReportData, y: float) -> float:
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN, y, "Detection Summary")
    y -= 7 * mm

    c.setFont("Helvetica", 10)
    c.drawString(MARGIN, y, f"Layer 2 CNN confidence: {data.cnn_confidence:.0%}")
    y -= 5 * mm
    c.drawString(MARGIN, y, f"Severity score: {data.severity_score:.2f} (scale TBD)")
    y -= 5 * mm
    c.drawString(MARGIN, y, f"SHAP top-contributing feature: {data.shap_top_feature}")
    y -= 10 * mm

    return y


def _draw_shap_chart(c: canvas.Canvas, data: ReportData, y: float) -> float:
    """
    Simple horizontal bar chart of SHAP attribution values, drawn with
    raw reportlab primitives (no matplotlib dependency -- keeps this
    module's dependency footprint to reportlab only, matching the
    single documented library in proposal main.md).
    """
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN, y, "SHAP Feature Attribution (dummy values)")
    y -= 8 * mm

    chart_left = MARGIN + 25 * mm
    chart_width = PAGE_W - MARGIN - chart_left - 20 * mm
    bar_height = 5 * mm
    max_abs = max((abs(v) for v in data.shap_values.values()), default=1.0) or 1.0

    c.setFont("Helvetica", 8)
    for ch in IMU_CHANNELS:
        val = data.shap_values.get(ch, 0.0)
        bar_w = (abs(val) / max_abs) * chart_width
        c.drawRightString(chart_left - 2 * mm, y + 1 * mm, ch)
        color = colors.HexColor("#c0392b") if val >= 0 else colors.HexColor("#2980b9")
        c.setFillColor(color)
        c.rect(chart_left, y, bar_w, bar_height, fill=1, stroke=0)
        c.setFillColor(colors.black)
        c.drawString(chart_left + bar_w + 2 * mm, y + 1 * mm, f"{val:+.2f}")
        y -= bar_height + 2 * mm

    y -= 8 * mm
    return y


def _draw_signature_block(c: canvas.Canvas, y: float) -> None:
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN, y, "Care Staff Acknowledgement")
    y -= 10 * mm

    c.setFont("Helvetica", 9)
    c.drawString(MARGIN, y, "Name: ______________________________")
    c.drawString(MARGIN + 90 * mm, y, "Date: ____________________")
    y -= 10 * mm
    c.drawString(MARGIN, y, "Signature: _________________________")


def generate_report(data: ReportData, output_path: str) -> str:
    """
    Renders a one-page PDF report to output_path. Returns output_path.

    Layout is a first-pass skeleton per this session's scope (fields/
    layout only, no real data) -- expect iteration once Sonia reviews
    (tracker sec:3, WP3, "Clinical PDF report design + feedback
    iteration" is explicitly her owned item, not finalized here).
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    c = canvas.Canvas(output_path, pagesize=A4)
    y = _draw_header(c, data)
    y = _draw_scores(c, data, y)
    y = _draw_shap_chart(c, data, y)
    _draw_signature_block(c, y)

    c.showPage()
    c.save()
    return output_path


if __name__ == "__main__":
    out = generate_report(DUMMY_EVENT, "/tmp/spark_dummy_report.pdf")
    print(f"Dummy report written to {out}")
