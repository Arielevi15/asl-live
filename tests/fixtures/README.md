# Golden fixtures

Raw landmark inputs and the expected feature vectors they must produce.
Regenerated **only** by `python scripts/make_fixtures.py`, and only on purpose:
every changed number in a fixture diff has to be explained by the change that
caused it (rule 1, rule 10, and the `preprocessing-change` skill).

Fixtures prove that `web/features.js` matches `src/asl/features.py` within
`1e-5`. They do not prove either one is correct - a Python bug would be frozen
here just as happily. Correctness is the job of the hand-checked cases in
`tests/test_features.py`.

`smoke/` will hold a few dozen committed clips in the clip format, used by the
smoke training run in CI. They are synthetic or come from the author's own
recordings - never from a public dataset (rule 7) and never from a participant
(rule 8).
