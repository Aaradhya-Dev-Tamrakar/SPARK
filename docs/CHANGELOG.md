# CHANGELOG

All notable changes and repository sync events for the **SPARK** project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- Standard repository tooling and config: `pyproject.toml` (PEP 517/621), `.pre-commit-config.yaml` (Ruff & formatting hooks).
- Comprehensive AI guidelines: `AGENT.md`, `CLAUDE.md`, `ANTIGRAVITY.md`.
- Contributor templates: `.github/pull_request_template.md`.
- Data architecture guide: `data/README.md`.
- Licensing: `LICENSE` (MIT).

---

## [v48] - 2026-08-11
### Sourcing & Hardware
- Action #39: Fasteners confirmed and selected via local Daraz kit (M2/M2.5/M3 machine screw assortment).
- Enclosure TPU 95A 1kg filament roll priced (NPR 4,000). Total BOM updated to ~NPR 13,877 in `SPARK_Component_Order_Form.xlsx`.

---

## [v37] - 2026-08-10
### Proposal & Tooling
- Proposal made VS Code / LaTeX Workshop compile-ready with `ThesisReports/.latexmkrc`.
- Removed stale BOM duplicate; `docs/SPARK_Component_Order_Form.xlsx` locked as sole canonical BOM.
- Added LaTeX build ignore patterns in `.gitignore`.

---

## [v27] - 2026-08-06
### Firmware & Gateway
- Merged initial `firmware-skeleton` (Layer 1 gate with 21/21 passing host tests) and `gateway-skeleton`.
- Locked communication protocol in `docs/WIRE_FORMAT_v1.md`.

---

## [v23] - 2026-07-23
### Training
- Added `training/data_prep/prepare_sisfall.py` (SisFall 200 Hz window generator).
- Proposal defence successfully defended on July 9, 2026.
