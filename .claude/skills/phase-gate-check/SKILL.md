---
name: phase-gate-check
description: Use when work may satisfy the current phase gate, or when the user asks whether the phase is done. Checks each gate criterion against real evidence and never advances the phase on its own.
---

# Phase gate check

The gate definitions live in CLAUDE.md, section "Phase gates". The current phase is the "Current phase" line at the top. Do not hard-code criteria here; read them from CLAUDE.md each time so the two never drift.

## Steps
1. Read the "Current phase" line and the matching gate. Split the gate into individual criteria (separated by semicolons).
2. For each criterion, find evidence and classify it:
   - **Met**: evidence exists and you ran or opened it this session (test output, CI run URL, `reports/runs/<run_id>/metrics.json`, a file that passes `schema.py` validation, a working demo checked by the user).
   - **Not met**: evidence exists and shows the criterion fails.
   - **No evidence**: nothing you can check from here.
3. Criteria only the user can confirm (for example "runs in a fresh Colab", "demo works in the browser", "consent forms signed", "recordings done") are **No evidence** until the user gives a log, a link or an explicit confirmation. Do not infer them from code that merely exists.
4. Report a table: criterion, status, evidence (command, path or URL, commit), what is missing.
5. If every criterion is Met:
   - Ask the user to confirm the phase is done. Stop until they answer.
   - On confirmation: update the "Current phase" line in CLAUDE.md, add a dated entry to `docs/decisions.md` saying the gate was passed, and propose the tag for the gate (`v0.1-spike`, `v0.2-letters`, ...). Creating or pushing a tag needs the user's approval.
6. If anything is Not met or No evidence, list the next concrete step per item and do not change the phase.

## Hard rules
- Never advance the phase on your own.
- Never mark a criterion Met without evidence.
- Never start work from the next phase until the user has confirmed this gate.
- Test-set results (frozen test people) count only if they were produced by the protocol in CLAUDE.md and are logged; never run or look at the frozen test set to "check" a gate before Phase 3.
