# Report Mode: SPARK / BiasAperture / Thesis Writing

The base skill's calibration ("cut scaffolding, keep load-bearing content") still applies, but the reader profile and evaluation criteria differ from general technical prose. Three changes from base mode:

## 1. The reader is a domain expert, not a generalist — cut definitions harder

Examiners and supervisors (Er. Dipen Manandhar for SPARK; Shreejan Kisee for BiasAperture; IOE board examiners) already know the field. Never define: CNN, TFLite Micro, IMU, sensor fusion, PID, SHAP, fairness metrics, AIF360/Fairlearn, ROC-AUC, precision/recall, EU AI Act, NIST AI RMF. Defining these reads as padding to an examiner, not helpfulness.

Do define, on first use: project-specific terms and codenames that only exist inside this project — SPARK's own module names, a custom metric BiasAperture introduces, an abbreviation coined for this report. Standard academic convention (define acronym at first use, use thereafter), not a concession to reader ability.

## 2. Justification cannot be cut for density — this overrides the base skill's "let the reader infer" rule

The base skill treats inferable reasoning as safe to cut. In a report being evaluated, reasoning is often the deliverable, not the conclusion. An examiner needs to see *why* Sensitivity/Specificity ≥90% was the chosen threshold, *why* FairFace over UTKFace, *why* this fairness metric over another — even if a sharp reader could guess. Guessable ≠ gradable. Do not compress methodology or design-choice justification the way you would compress an aside in a blog post.

Rule of thumb: cut scaffolding around a claim (restatement, hand-holding transitions, hedge padding). Do not cut the evidentiary chain behind a claim (why this method, why this threshold, why this dataset, what the data showed).

## 3. Hedges are often required content, not defensive padding

Base-skill rule 4 (keep load-bearing caveats) is the default here, not the exception. Standard report hedges are epistemic, not defensive, and must stay:
- Scope limits: "under lab conditions," "on this dataset only," "within the tested distribution"
- Known threats to validity: dataset size, simulated vs. real falls, demographic coverage of FairFace/UTKFace
- Stated assumptions the results depend on

Cut only hedges with no specific referent — "it depends on several factors" with no factors named. Keep every hedge that names a real constraint.

## Structure and register — fixed, not compressible for density

- Keep standard sections intact: Abstract, Methodology, Results, Limitations, Discussion (or the KEC/IOE-mandated chapter structure). Don't collapse sections to save words.
- Formal register: no contractions, no conversational confidence markers ("the real problem is," "that approach fails because") — reframe as precise technical claims ("the primary limitation is," "this approach underperforms because").
- State benchmark numbers exactly (e.g., "Sensitivity/Specificity ≥ 90%," "ROC-AUC 0.841"), never as vague qualifiers ("performed well").
- Regulatory/standards references (EU AI Act Annex IV, NIST AI RMF) cited to the specific article/clause, not generally.

## LaTeX conventions (apply on top of the above — see repo-conventions skill for full rules)

- Keyword lists alphabetical A–Z.
- Dimension values: space before unit (`10 mm`, not `10mm`).
- Check the specific template/class file for existing local conventions before assuming these are exhaustive.

## Failure mode specific to report mode

In general prose, over-explaining reads as weak or AI-ish. In an examiner-facing report, under-justifying reads as unsubstantiated — which is worse, because it's gradable. When genuinely unsure whether to cut a piece of reasoning, keep it. The cost of an extra justified sentence is lower than the cost of an examiner flagging an unsupported design choice.
