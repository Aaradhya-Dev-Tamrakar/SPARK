"""
test_pdf_report.py

Unit tests for clinical PDF report generation in SPARK Gateway.
Tests verify:
    1. Report generation completes without error.
    2. Resulting file exists, is non-empty, and has valid PDF magic header (%PDF-).
    3. Handles custom metadata and varying confidence levels properly.
"""

from pathlib import Path

from gateway.report.pdf_report import DUMMY_EVENT, ReportData, generate_report


class TestPdfReport:
    def test_generate_default_dummy_report(self, tmp_path: Path):
        out_pdf = tmp_path / "test_report.pdf"
        res = generate_report(DUMMY_EVENT, out_pdf)

        assert Path(res).exists()
        assert out_pdf.stat().st_size > 1000  # Non-trivial PDF size

        content = out_pdf.read_bytes()
        assert content.startswith(b"%PDF-")

    def test_generate_custom_report_data(self, tmp_path: Path):
        data = ReportData(
            event_id="CUSTOM-EVT-99",
            timestamp_iso="2026-08-20 12:00:00 UTC",
            severity_score=0.95,
            cnn_confidence=0.98,
            shap_top_feature="w_y",
            shap_values={
                "a_x": 0.10,
                "a_y": 0.10,
                "a_z": 0.20,
                "w_x": 0.10,
                "w_y": 0.40,
                "w_z": 0.10,
            },
            device_id="SPARK-NODE-02",
            firmware_version="v1.1.0",
            clinical_summary="High pitch rotation detected preceding lateral impact.",
        )
        out_pdf = tmp_path / "custom_report.pdf"
        res = generate_report(data, out_pdf)

        assert Path(res).exists()
        assert out_pdf.read_bytes().startswith(b"%PDF-")
