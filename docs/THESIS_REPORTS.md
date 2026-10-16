# SPARK thesis reports

The proposal is preserved in [SPARK_Proposal](SPARK_Proposal/ThesisReports/thesis_report.tex). Two independent KEC report folders record the evidence snapshot of October 14, 2026:

| Report | Editable source | PDF | Purpose |
|---|---|---|---|
| Mid-defense | [main.tex](SPARK_Mid_Defense/main.tex) | [Progress report](SPARK_Mid_Defense/main.pdf), 40 pages | Completed software work, available results, limitations, and remaining tasks |
| Final-defense | [main.tex](SPARK_Final_Defense/main.tex) | [Thesis draft](SPARK_Final_Defense/main.pdf), 46 pages | Full draft with hardware, cohort, and integrated evaluation explicitly pending |

Each folder contains local KEC formatting, front pages, chapter sources, figures, BibTeX references, source-hash manifests, and archived result excerpts. Neither report reads files from the proposal or its sibling at build time. Run `build.bat` inside the selected folder with TeX Live and latexmk available. The PDF is generated as `main.pdf`; LaTeX intermediate files are ignored.

Human fall detection is the primary completion objective. The proposal's comparative literature, hardware/software theory, feasibility/BOM estimates, algorithms, transfer-learning design, deliverables, and relevant context have been restored with stage-appropriate status in the two reports. See the [coverage and twenty-reference audit](thesis_work/PROPOSAL_COVERAGE_AND_REFERENCE_AUDIT.md). Unmatched or mismatched proposal citations are explicitly identified there; unsupported performance comparisons and novelty claims were removed. Robotics is a proposed MuJoCo appendix requiring separate data, adaptation, and validation. No robot simulation was executed. Approval forms are unsigned and defense dates are unconfirmed. The Gantt chart remains only in the proposal; the reports use dependency gates without a calendar schedule.

The current reporting convention is **100 Hz, 200 samples, six channels, two seconds for the existing model pipeline**, with a separate planned **200 Hz logger**. Existing training values remain sensor-count based; calibrated physical-unit mapping and firmware timing are unresolved integration gates. A 200 Hz three-second model would require 600 samples and fresh training/evaluation. Proposal BOM prices are retained only as dated planning estimates and require re-quotation before procurement.

Do not combine August results with October model metadata. The October Colab log reports safety threshold 0.4236 while the configuration records 0.4065. Gradient-times-input attribution is not exact SHAP, and v1 event packets do not carry the waveform. Historical laptop benchmark claims are not MCU latency or measured battery evidence.

The work sequence is preparation → procurement next semester after Dashain, Tihar, and Chhath → parts receipt → logger validation → approved cohort collection → integrated evaluation. Institutional approval is a separate prerequisite for volunteer collection; logger validation alone does not authorize recording.
