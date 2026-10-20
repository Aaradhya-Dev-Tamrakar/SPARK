# SPARK thesis preparation audit — 2026-10-14

Knowledge links: [[SPARK]] → [[Human fall detection]] → [[Thesis evidence register]]. [[Robot fall monitoring]] remains an exploratory hypothesis with separate validation gates.

Two independent KEC report folders contain editable chapters, local formatting/figures/references, copied evidence records, and compiled PDFs. The proposal is preserved. The report index is `docs/THESIS_REPORTS.md`.

## Evidence conclusions

- **EMPIRICALLY_VERIFIED inspection:** local arrays have shape `(38426,200,6)` float32 and metadata covers 38 subject IDs and 34 activity codes. This is inventory, not an evaluation denominator.
- **EMPIRICALLY_VERIFIED inspection:** decoded firmware header is 18,912 bytes and matches `spark_cnn_int8_upgraded.tflite`; SHA256 is `dd0e8e3d6b201acba2b524a1f911958f70bf15a52bc6592eb5cec97e78d5a2ea`. It differs from the August 18,904-byte model. Identity is not on-device execution.
- **Archived measured results:** August report sensitivity .8781/AUC .9185 and INT8 sensitivity .8743/AUC .8717 belong to the 6,712-window archived evaluation. October log has a different 3,707-window test partition and safety-column sensitivity .8981/AUC .9272. Neither reaches the 90% sensitivity goal. No new model evaluation was executed.
- **Unresolved provenance:** October log threshold .4236 disagrees with config/header .4065. The old quantization report cannot certify the newer export's performance.
- **Source-level contract:** 100 Hz × 200 samples = 2 s for existing preprocessing. 200 Hz is a planned logger rate. Unit conversion, anti-aliasing, trained input scaling, real buffering and device timing remain integration gates.
- **Implementation boundary:** sensor/I2C, TFLite Micro invocation, and transport writes remain stubbed. Gate code uses magnitude >=2.5 g held >300 ms, differing from older short-spike prose. Waveform gradient attribution is not exact SHAP; v1 lacks raw windows and supports peak-feature fallback.
- **HEURISTIC_HYPOTHESIS/planned:** battery endurance, completed enclosure, Nepal cohort, physical BLE/device timing, robot monitoring and mitigation. No clinical, robot, power, or firmware-emulator result is asserted.

## Fleet execution

Fleet was inspected before dispatch. The standard Commander path discarded target/tier fields and its queue teardown auto-committed; it was bypassed in favor of bounded direct Fleet adapters with SPARK as read-only input and disjoint task outputs. Antigravity context and automatic Git mutations were disabled. Two concurrent workers were selected against approximately 2.67 GiB free RAM, despite authorization for higher concurrency.

Seven bounded tasks completed: two balance Scouts, intelligence initial review, frozen-input delta review, identity correction, balance Writer, and efficiency Formatter. Total reported consumption was 19.61 credits. Frozen evidence preceded approved drafting. A filename miss in the initial review/draft was superseded by the independent byte-identity correction. Lead integrated only corrected evidence.

The final source-review agent returned preliminary confirmation of numerical provenance and flagged layout overflows, then hit its usage limit before writing its final review file. Lead completed the remaining evidence, dependency, compilation, and PDF layout checks; no completed agent review is claimed.

## Verification and publication state

- `uv run pytest -q`: 65 passed, 48 dependency warnings, 57.11 s.
- `uv run python scripts/verify.py`: 4 checks passed, 0 errors.
- Both thesis skill audits passed: zero banned hype, broken references, or missing citation keys; explicit scope and uncertainty/sample limitations present.
- Both local `build.bat` entrypoints compiled independently using latexmk/BibTeX. No sibling/proposal input appears in their LaTeX dependency records.
- PDF pages were rendered and inspected, including covers, unsigned approval form, tables, architecture/gate figures, references, evidence register, and robotics appendix. Overfull path boxes, duplicate page anchors, cover spillover, and short orphan continuations were corrected.
- `git diff --check` passed; no proposal diff exists.
- Repository-wide Ruff remains a baseline failure: 23 findings in existing `scripts/sync_drive.py`, `scripts/verify.py`, and `training/train_cnn.py`; four existing files fail formatting, additionally including `tests/test_train_cnn.py`. No unrelated source fixes were made.
- No sync, commit, push, or merge was performed. `sync.ps1` has no `WhatIf` parameter and is not a safe preview.

Robotics feasibility is documentation-reviewed, not runtime-tested. The planned forty-episode protocol includes five held-out episodes per condition; stable-controller, substep logging, calibrated units/preprocessing, independent annotations, event sensitivity, non-fall exposure alarms, timing, and replay interoperability are explicit prerequisites. No simulation was executed.
