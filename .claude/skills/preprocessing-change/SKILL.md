---
name: preprocessing-change
description: Use before and during any change to src/asl/features.py, web/features.js, the golden fixtures, or the exported model I/O. Enforces the test-first, version-bump, fixtures and decisions.md checklist from CLAUDE.md.
---

# Preprocessing change checklist

Applies to any change that alters feature output: `src/asl/features.py`, `web/features.js`, `tests/fixtures/`, `scripts/make_fixtures.py`, the clip format, label file or ONNX I/O. CLAUDE.md rules 1, 5 and 10 are the authority; this skill only sequences them.

## 0. Stop and plan (mandatory)
Do not edit anything yet. Write the plan and wait for the user's approval:
- Which preprocessing step (1-9 in the contract) changes, and why.
- Files that will change, and the expected effect on output shapes and values.
- Tests that will be added or changed.
- Whether an already exported model becomes stale (see step 7).

## 1. Test first
- Add or update a hand-checked case in `tests/test_features.py`. The expected value must be worked out by hand from the contract, never copied from the current output of `features.py`.
- Run `pytest -q` and confirm the new test fails for the right reason.

## 2. Change `features.py`
- Smallest change that makes the new test pass.
- If the output of `features.py` changes in any way, bump `FEATURE_VERSION`.

## 3. Port to `web/features.js`
- Same change, same order of operations. `features.js` stays a pure ES module: no DOM, no camera, no globals.
- Bump `FEATURE_VERSION` in `features.js` to the same value. A test asserts both are equal.

## 4. Fixtures
- Regenerate only with `python scripts/make_fixtures.py`, and only because this change requires it.
- Review the fixture diff: every changed number must be explained by the change. Unexplained diffs mean a bug, not a new fixture.
- Hand-checked cases in `test_features.py` must not change unless the contract itself changed on purpose.

## 5. Verify
```bash
pytest -q
node --test tests/
```
Both green, parity within `1e-5`. Quote the actual output, never a remembered result.

## 6. Record
- Add an entry to `docs/decisions.md`: date, decision, reason, alternatives rejected, old and new `FEATURE_VERSION`.
- If the contract text in CLAUDE.md is now wrong, propose an edit to CLAUDE.md. Do not edit it silently.

## 7. Downstream impact
- The old `web/model/*.onnx` has the old `feature_version`; `app.js` will refuse to run it. State in the PR that the model must be retrained and re-exported, and that export parity (rule 5) must pass before `web/model/` is updated.
- Nothing trained on the old features may be reported as if it used the new ones.

## 8. Commits and PR
- Separate commits: test, `features.py`, `features.js`, fixtures, docs. Conventional Commits, scope `features`.
- PR body says why the fixtures changed and shows green parity tests. Never merge; report CI status and wait.
