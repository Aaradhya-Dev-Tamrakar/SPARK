# Orchestrator board — master plan (2026-08-22)

Planning only, nothing claimed/created/executed below. 8 open items across 3 projects + 1 personal-org task.

---

## TIER 0 — needs your decision before anything can move

| # | Task | Decision needed |
|---|---|---|
| 1 | `task_2026-08-15_001` BiasAperture WP2/WP3 kickoff | Who owns WP2/Stream A vs WP3/Stream B — you, Tisha, or split by lane? Spec explicitly refuses to assume this; parent can't decompose into child tasks without it. |
| 2 | `task_2026-08-13_002` Cross-account `/topics` consolidation | "Every account running this task" — which accounts count? Full roster from `team-context.md` (IEEE/personal/gaming/family/project), or a specific subset? Unscoped as written. |
| 3 | `task_2026-08-10_001` BOM reconciliation, Velcro line | Locked design says Velcro is part of the enclosure (no separate purchase); BOM still carries a separate NPR 1,000 line. Real design call, not something I should infer. |

---

## TIER 1 — ready now, no blockers

| # | Task | What it takes |
|---|---|---|
| 4 | **SPARK synthesis follow-up** (new task, off `task_2026-08-21_001`) | Draft narrowed Claim 1/3 wording, completed `DATA_COLLECTION_PROTOCOL.md` rows (F09–F15/D15–D19), updated Ch.6 future-work draft — synthesized from the 19 merged checkpoints already delivered (`SPARK_research_board_merged.md`). Largest single item on the board; feeds thesis finalization directly. |
| 5 | **Portfolio site fix-pass** — two-step: `merge_results(task_2026-08-14_001)` [mechanical, 8/8 subtasks already `merged`] → unlocks `task_2026-08-14_010` (real code fixes: missing `import re` in `site_mcp.py`, wrong resume email, two XSS spots, unguarded haptic-feedback call, several others). `task_2026-08-14_010` is `kind: code`, repo `Aaradhya-Dev-Tamrakar/Aaradhya-Dev-Tamrakar.github.io` — sync.ps1-governed per the task's own spec. | Repo link needed at execution time (portfolio repo, not yet given this session). |

---

## TIER 2 — re-verify against live state first, likely partly/fully superseded

| # | Task | Why it needs re-checking, not blind execution |
|---|---|---|
| 6 | `task_2026-08-10_001` BOM reconciliation — 4 stated items | Item 3 (R-05 battery math) is **already closed** — `task_2026-08-12_001` done 2026-08-22, and tracker v54 confirms 110–140mA/~8–10hr is internally consistent (per team-context + Track 12's research). Item 1 (Velcro) is TIER-0 above. Items 2 (enclosure cost — still no CAD model per Track 10's just-delivered TPU boss-thickness research) and 4 (confirmed order placement) — unknown current state, need a tracker v54 + BOM xlsx re-read before treating as open work. |
| 7 | `task_2026-08-12_003` Notebook cleanup (delete 19 sources from main SPARK notebook `2c00f5a4`) | Team-memory only confirms cleanup happened on the **secondary** notebook (`3b67fc33`, 41→0 methodology sources). No confirmation either way for the main notebook's 19. Check current source count via nlm before deleting anything. |

---

## TIER 3 — blocked outside this environment, nothing to plan

| # | Task | Status |
|---|---|---|
| 8 | `task_2026-08-11_004` fuseAiF Week 14 fellowship notebook | `blocked` — local commit `f9b0ee8` made, not pushed (no authenticated git-write access here). Needs `git push` from your own machine. Nothing actionable from this session until that happens. |

---

## Suggested order once Tier 0 answers land

1. **#4 SPARK synthesis** — biggest, most consequential, thesis-timeline-adjacent.
2. **#5 Portfolio merge + fix-pass** — mechanical merge is free; fix-pass is scoped and self-contained.
3. **#6 / #7 Tier-2 closeouts** — cheap, mostly verification, may turn out already done.
4. **#1 BiasAperture decomposition** — once owner split is answered.
5. **#2 Cross-account topics** — lowest external urgency, personal-org task.

Say the word (and answer Tier 0) and I'll start wherever you want.
