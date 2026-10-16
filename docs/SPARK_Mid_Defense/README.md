# SPARK mid-defense progress report

Build this folder independently with `build.bat`, or run `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` from this directory. Output: `main.pdf`. TeX Live with latexmk and BibTeX is required. There are no inputs from the proposal or final-defense folder.

Edit `FrontPages/`, `Chapters/`, `Figures/`, and `BackPages/references.bib`. Figures are local editable LaTeX sources; `LoGoKEC.png` preserves the institutional logo. `utils.tex` and `kecreport.sty` retain the proposal formatting assets; the master uses `utils.tex`, matching the proposal's active setup.

Evidence is frozen to October 14, 2026. `evidence/` contains archived reports, a sanitized October Colab excerpt, metadata, and source hashes. August and October generations are deliberately separate. No training, clinical collection, or robot simulation was executed to create this report.

Human fall detection is the completion goal. Hardware, battery, physical transport, cohort, and integrated evaluation remain pending. Robot monitoring is a planned appendix. Use the result labels and pending sections when presenting progress; do not turn historical measurements or estimates into deployed-system claims.
