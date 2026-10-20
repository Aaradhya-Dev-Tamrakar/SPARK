## Objective
Align SPARK resumption documents and project status reporting with the confirmed plan to begin component procurement next semester after the Dashain, Tihar, and Chhath holidays.

## Scope and boundaries
- Keep tracker, post-boards master plan, cohort execution plan, supervisor progress report, and README aligned on the dependency order.
- Use GitHub Milestones to group tracked work by delivery phase; leave due dates unset until ordering and delivery windows are confirmed.
- Keep protocol review and ethics preparation ahead of procurement; gate hardware bring-up on parts arrival and volunteer recording on logger validation and institutional approval.
- Planning documents are settled; the October 14 authorization extends this issue to independent mid-defense and final-defense LaTeX reports while preserving the proposal.
- Do not assign calendar dates until the next-semester ordering and delivery windows are known.

## Tasks
- [x] Update the SPARK tracker with the resumption timing and current dependency order.
- [x] Replace expired week-based targets in the post-boards and cohort plans with dependency gates.
- [x] Mark the dated supervisor-report schedule as historical and retain the current sequence separately.
- [x] Replace README percentage bars with factual workstream statuses and links to phase milestones.
- [x] Create phase milestones without due dates and assign open issues by delivery phase.
- [x] Review and update the thesis LaTeX schedule, chronology, and status claims after the planning documents are settled (independent reports prepared locally; proposal preserved).
- [ ] Set calendar dates with the team when the next-semester order and delivery window are confirmed.
- [x] Check documentation consistency and repository verification before closing.


## Thesis implementation — October 14, 2026

- [x] Create independently buildable `docs/SPARK_Mid_Defense/` and `docs/SPARK_Final_Defense/` with editable sources, figures, references, evidence snapshots, and PDFs.
- [x] Preserve KEC metadata and the proposal; leave signatures and defense dates unconfirmed.
- [x] Separate August and October results, reconcile report-level sampling to 100 Hz / 200 samples / 2 s, and expose threshold, hardware, cohort, power, and explanation limitations.
- [x] Add a documentation-reviewed, unexecuted forty-episode MuJoCo protocol with five held-out episodes per condition.
- [x] Complete bounded Fleet Scout → Reviewer → Writer → Formatter → Lead stages with isolated outputs and Antigravity inheritance disabled.
- [x] Compile and visually inspect both reports; verify references, source hashes, standalone inputs, and unchanged proposal.
- [x] Compare proposal chapters, figures, tables, appendices, and all 20 included manual references against both reports; record retain/adapt/defer/exclude decisions and the proposal-only Gantt rule.
- [x] Restore relevant literature, theory, algorithms, feasibility/BOM estimates, transfer-learning design, and stage-specific deliverables; correct verified bibliography records and flag unresolved sources.
- [x] Rebuild both standalone PDFs and inspect layout; resolve report citations/cross-references and verify no defense report contains a Gantt chart or obsolete calendar schedule.
- [ ] Resolve the pre-existing lint/format verification gate and publish the thesis changes using repository sync wrappers.

Local outputs: mid-defense PDF 41 pages; final-defense thesis draft 46 pages. Report index: `docs/THESIS_REPORTS.md`; proposal coverage and citation review: `docs/thesis_work/PROPOSAL_COVERAGE_AND_REFERENCE_AUDIT.md`. The final thesis still awaits hardware, approved cohort, and integrated evaluation. No simulation, training, or volunteer recording was executed for these reports.

Validation: this continuation compiled both reports independently and confirmed no undefined citation/reference or overfull-box warnings in the final LaTeX logs. Existing baseline evidence remains 65 Python tests passed (48 dependency warnings), four structural checks passed, and repository-wide Ruff has 23 pre-existing findings; four files need formatting. Changes remain local and uncommitted/unpushed. No sync preview was run: `sync.ps1` has no `WhatIf` parameter. This issue remains open for publication and later confirmed calendar dates.
