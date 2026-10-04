## What

<!-- One or two sentences. What changed. -->

## Why

<!-- The reason, not a restatement of the diff. -->

## How it was tested

<!-- Commands actually run, with their real output. Never a remembered result. -->

```
pytest -q
node --test "tests/**/*.test.js"
```

## Results

<!-- Numbers only if a run produced them. Each number needs its config file,
     run folder (reports/runs/<run_id>/) and commit hash. Delete this section
     if the change produces no numbers. -->

| Metric | Value | Config | Run | Commit |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Checklist

- [ ] Tests pass locally (`pytest -q`, `node --test "tests/**/*.test.js"`)
- [ ] Conventional Commit messages, one logical change per commit
- [ ] No dataset files, checkpoints, secrets, participant recordings or notebook outputs committed
- [ ] Non-obvious decisions recorded in `docs/decisions.md`
- [ ] New dependencies were approved and are pinned
- [ ] CLAUDE.md updated (or an edit proposed) if this change makes it wrong

### If this touches preprocessing, splits, export or evaluation

- [ ] `FEATURE_VERSION` bumped in **both** `features.py` and `features.js`
- [ ] Golden fixtures regenerated on purpose, and the reason stated here
- [ ] Every changed fixture number is explained by this change
- [ ] Python/JS parity green within `1e-5`
- [ ] Hand-checked cases in `tests/test_features.py` still hold
- [ ] Any already exported model is flagged as stale and must be re-exported

Closes #
