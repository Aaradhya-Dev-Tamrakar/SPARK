#!/usr/bin/env python3
"""
pdf_report.py

Clinical PDF incident report generator for SPARK's Gateway (Layer 2),
per proposal claim 5 ("Auto-generated clinical PDF reports") and WBS WP3.

Generates a structured, professional one-page medical incident summary
including kinematics, CNN confidence, SHAP attribution chart, and care staff
acknowledgement blocks.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

from gateway.receiver.wire_format import IMU_CHANNELS


@dataclass
class ReportData:
    """Flat view-model for the clinical PDF report."""

    event_id: str
    timestamp_iso: str
    severity_score: float  # 0.0 - 1.0
    cnn_confidence: float  # Layer 2 P(FALL), 0.0 - 1.0
    shap_top_feature: str
    shap_values: dict[str, float]  # channel_name -> attribution
    device_id: str = "SPARK-DEV-01"
    firmware_version: str = "v1.0.0"
    clinical_summary: str = ""
    temporal_attributions: dict[str, float] = field(default_factory=dict)


# Default dummy data for testing layout
DUMMY_EVENT = ReportData(
    event_id="EVT-20260820-001",
    timestamp_iso=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
    severity_score=0.88,
    cnn_confidence=0.94,
    shap_top_feature="a_z",
    shap_values={
        "a_x": 0.08,
        "a_y": 0.12,
        "a_z": 0.52,
        "w_x": 0.06,
        "w_y": 0.14,
        "w_z": 0.08,
    },
    device_id="SPARK-NODE-01",
    firmware_version="v1.0.0-s3",
    clinical_summary="High-impact fall detected with dominant vertical acceleration spike (a_z) during impact phase.",
    temporal_attributions={"pre_impact": 0.15, "impact_spike": 0.70, "post_impact": 0.15},
)


PAGE_W, PAGE_H = A4
MARGIN = 18 * mm


def _draw_header(c: canvas.Canvas, data: ReportData) -> float:
    """Draws title banner and metadata header."""
    y = PAGE_H - MARGIN

    # Top brand bar
    c.setFillColor(colors.HexColor("#1a365d"))
    c.rect(MARGIN, y - 10 * mm, PAGE_W - 2 * MARGIN, 12 * mm, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(MARGIN + 5 * mm, y - 4 * mm, "SPARK Clinical Fall Incident Report")
    c.setFont("Helvetica", 9)
    c.drawRightString(
        PAGE_W - MARGIN - 5 * mm, y - 4 * mm, "Signal Pattern Analysis & Real-time Kinetics"
    )

    y -= 18 * mm
    c.setFillColor(colors.black)

    # Metadata grid
    c.setFont("Helvetica-Bold", 9)
    c.drawString(MARGIN, y, "INCIDENT METADATA")
    c.setStrokeColor(colors.HexColor("#cbd5e1"))
    c.setLineWidth(0.5)
    c.line(MARGIN, y - 2 * mm, PAGE_W - MARGIN, y - 2 * mm)
    y -= 6 * mm

    c.setFont("Helvetica", 9)
    col1_x = MARGIN
    col2_x = MARGIN + 60 * mm
    col3_x = MARGIN + 120 * mm

    c.drawString(col1_x, y, f"Event ID: {data.event_id}")
    c.drawString(col2_x, y, f"Timestamp: {data.timestamp_iso}")
    c.drawString(col3_x, y, f"Device ID: {data.device_id}")
    y -= 5 * mm

    c.drawString(col1_x, y, f"Firmware: {data.firmware_version}")
    c.drawString(col2_x, y, "Protocol: WIRE_FORMAT_v1 (BLE/Serial)")
    c.drawString(col3_x, y, "Location: Wrist Wearable Node")
    y -= 10 * mm

    return y


def _draw_detection_summary(c: canvas.Canvas, data: ReportData, y: float) -> float:
    """Draws detection severity, confidence cards, and clinical summary."""
    c.setFont("Helvetica-Bold", 9)
    c.drawString(MARGIN, y, "DETECTION & RISK CLASSIFICATION")
    c.line(MARGIN, y - 2 * mm, PAGE_W - MARGIN, y - 2 * mm)
    y -= 7 * mm

    box_w = (PAGE_W - 2 * MARGIN - 8 * mm) / 3
    box_h = 16 * mm

    # Box 1: Classification
    c.setFillColor(colors.HexColor("#fee2e2"))
    c.rect(MARGIN, y - box_h, box_w, box_h, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#991b1b"))
    c.setFont("Helvetica-Bold", 8)
    c.drawString(MARGIN + 3 * mm, y - 4 * mm, "STATUS")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN + 3 * mm, y - 11 * mm, "CONFIRMED FALL")

    # Box 2: CNN Confidence
    x2 = MARGIN + box_w + 4 * mm
    c.setFillColor(colors.HexColor("#f1f5f9"))
    c.rect(x2, y - box_h, box_w, box_h, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#334155"))
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x2 + 3 * mm, y - 4 * mm, "LAYER-2 CONFIDENCE")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x2 + 3 * mm, y - 11 * mm, f"{data.cnn_confidence:.1%}")

    # Box 3: Severity
    x3 = x2 + box_w + 4 * mm
    c.setFillColor(colors.HexColor("#f1f5f9"))
    c.rect(x3, y - box_h, box_w, box_h, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#334155"))
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x3 + 3 * mm, y - 4 * mm, "IMPACT SEVERITY")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x3 + 3 * mm, y - 11 * mm, f"{data.severity_score:.2f} / 1.00")

    y -= box_h + 8 * mm

    # Narrative Summary
    if data.clinical_summary:
        c.setFillColor(colors.HexColor("#f8fafc"))
        c.setStrokeColor(colors.HexColor("#e2e8f0"))
        c.rect(MARGIN, y - 10 * mm, PAGE_W - 2 * MARGIN, 12 * mm, fill=1, stroke=1)
        c.setFillColor(colors.HexColor("#1e293b"))
        c.setFont("Helvetica-Oblique", 8.5)
        c.drawString(MARGIN + 3 * mm, y - 4 * mm, f"Analysis: {data.clinical_summary}")
        y -= 16 * mm

    return y


def _draw_shap_chart(c: canvas.Canvas, data: ReportData, y: float) -> float:
    """Draws horizontal SHAP feature attribution bar chart."""
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(MARGIN, y, "SHAP EXPLAINABILITY ATTRIBUTION (IMU KINEMATICS)")
    c.line(MARGIN, y - 2 * mm, PAGE_W - MARGIN, y - 2 * mm)
    y -= 8 * mm

    axis_labels = {
        "a_x": "Lateral Acceleration (a_x)",
        "a_y": "Longitudinal Acceleration (a_y)",
        "a_z": "Vertical Impact Acceleration (a_z)",
        "w_x": "Roll Angular Velocity (w_x)",
        "w_y": "Pitch Angular Velocity (w_y)",
        "w_z": "Yaw Angular Velocity (w_z)",
    }

    chart_left = MARGIN + 55 * mm
    chart_width = PAGE_W - MARGIN - chart_left - 25 * mm
    bar_height = 5 * mm
    max_val = max(data.shap_values.values(), default=1.0) or 1.0

    c.setFont("Helvetica", 8)
    for ch in IMU_CHANNELS:
        val = data.shap_values.get(ch, 0.0)
        label = axis_labels.get(ch, ch)
        bar_w = (abs(val) / max_val) * chart_width

        c.setFillColor(colors.HexColor("#334155"))
        c.drawRightString(chart_left - 3 * mm, y + 1 * mm, label)

        # Highlight top feature
        if ch == data.shap_top_feature:
            bar_color = colors.HexColor("#dc2626")  # Primary red
        else:
            bar_color = colors.HexColor("#3b82f6")  # Secondary blue

        c.setFillColor(bar_color)
        c.rect(chart_left, y, max(bar_w, 1.0), bar_height, fill=1, stroke=0)

        c.setFillColor(colors.black)
        c.drawString(chart_left + bar_w + 2 * mm, y + 1 * mm, f"{val * 100:.1f}%")
        y -= bar_height + 2.5 * mm

    y -= 8 * mm
    return y


def _draw_signature_block(c: canvas.Canvas, y: float) -> None:
    """Draws care staff acknowledgement and signoff block."""
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(MARGIN, y, "CLINICAL / CAREGIVER ACKNOWLEDGEMENT")
    c.line(MARGIN, y - 2 * mm, PAGE_W - MARGIN, y - 2 * mm)
    y -= 10 * mm

    c.setFont("Helvetica", 8.5)
    c.drawString(
        MARGIN, y, "Reviewing Clinician / Caregiver Name: ________________________________"
    )
    c.drawString(MARGIN + 105 * mm, y, "Review Date: ___________________")
    y -= 8 * mm
    c.drawString(
        MARGIN,
        y,
        "Triage Action: [  ] Assistance Provided   [  ] False Alarm   [  ] Hospital Escalation",
    )
    y -= 8 * mm
    c.drawString(MARGIN, y, "Clinician Signature: _________________________________")


def generate_report(data: ReportData, output_path: str | Path) -> str:
    """
    Renders a clinical one-page PDF report to output_path.
    Returns the resolved output path as a string.
    """
    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    c = canvas.Canvas(str(out_file), pagesize=A4)
    y = _draw_header(c, data)
    y = _draw_detection_summary(c, data, y)
    y = _draw_shap_chart(c, data, y)
    _draw_signature_block(c, y)

    c.showPage()
    c.save()
    return str(out_file)


if __name__ == "__main__":
    out = generate_report(DUMMY_EVENT, "data/gateway_events/sample_report.pdf")
    print(f"Sample report generated at {out}")
