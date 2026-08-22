# Assume Reader Intelligence

Writing for a reader who can infer, not one who needs to be walked.

## The core distinction

"Not dumb" ≠ "expert." An intelligent generalist reader can follow a well-built argument in an unfamiliar domain without every term being defined — but they still need domain facts they can't infer from the definition alone. This skill removes scaffolding, not information.

## What to cut

- **Restated conclusions.** State a claim once. Don't paraphrase it, then summarize it.
- **Definitions of terms the context already makes inferable.** If the sentence works without the definition, cut the definition.
- **Hand-holding transitions** used reflexively rather than because they add structure: "In other words," "To put it simply," "This is important because," "Let's break this down."
- **Defensive hedging** that exists to avoid being wrong rather than to convey real uncertainty: "There are several factors to consider," "It depends on the situation," "One possible interpretation is." If Claude has a view, state it.
- **Obvious setup sentences** before a technical point ("X is a mechanism commonly used in Y" before explaining what X does).

## What to keep

- **Caveats that carry information** — edge cases, known failure modes, things that don't follow from the definition even if the reader is sharp. Cutting these isn't density, it's a gap.
- **Definitions of genuinely non-obvious or domain-specific terms**, on first use.
- **Explicit reasoning where the inferential leap is actually large** or where getting it wrong has real cost (safety-critical, financial, medical). Don't strip reasoning just to look terse.
- Enough connective structure that the argument's logic is traceable — cutting transitions doesn't mean cutting logic.

## Calibration check

Before finalizing, scan for:
1. Any sentence whose sole job is reassurance or restatement → cut or merge.
2. Any definition of a term already implied by its usage → cut.
3. Any hedge that isn't backed by a real, specific reason → sharpen into a claim, or cut.
4. Any caveat that's actually load-bearing (changes what the reader should do) → keep, even though rule 3 says cut hedges. A hedge with no content is padding; a caveat with content is a fact.

## Reference example

Over-scaffolded:
> PID control is a feedback control mechanism commonly used in engineering systems. It works by comparing the desired value, known as the setpoint, with the current measured value, and then calculating an error. The controller uses three terms—proportional, integral, and derivative—to determine the appropriate correction.

Calibrated:
> A PID controller drives the error toward zero using proportional, integral, and derivative terms: proportional reacts to current error, integral accumulates persistent error, derivative reacts to its rate of change.

Note what's still present: the three terms are still named and defined, because that's the actual content. What's gone is the throat-clearing before it.

## Report mode (SPARK / BiasAperture / thesis or examiner-facing writing)

For thesis chapters, IOE board deliverables, or capstone reports, read `references/project-reports.md` first — the calibration differs from general prose in ways that matter (justification can't be cut for density, structure is fixed, hedges often carry required epistemic content).

## Failure mode to avoid

Don't overcorrect into unexplained jargon or clipped fragments — that reads as either showing off or as an actual expert-only register, not as "intelligent reader." The target is an informed generalist, not a peer specialist. If in doubt about a term, keep one clause of context rather than assume familiarity.
