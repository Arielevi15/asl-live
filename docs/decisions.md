# Decisions

Every non-obvious decision, newest last. Each entry: date, decision, reason,
alternatives rejected. A decision that changes a versioned interface contract
(clip format, label file, model I/O, feature version) must also say which
version it moves and point at the updated fixtures.

---

## D-0001 - Project name `asl-live`

- **Date:** 2026-10-04
- **Decision:** The project and repository are named `asl-live`.
- **Reason:** Short, says what it is (ASL, live/real-time), and claims nothing
  about interpreting meaning.
- **Alternatives rejected:** Names containing "translator" or "interpreter".
  They overclaim: this is per-letter and per-sign recognition, not conversion
  between languages. Rule 9 forbids the word anywhere in the project.

## D-0002 - No fixed weekly hour budget

- **Date:** 2026-10-04
- **Decision:** No fixed weekly hour limit. The 12-week plan still assumes
  10-15 hours a week as its planning baseline.
- **Reason:** Extra hours can shorten the coding phases, but not the phases
  that wait on people: recording sessions, consent, volunteer scheduling.
- **Alternatives rejected:** Committing to a fixed weekly number, which would
  make the timeline look more precise than it is.

## D-0003 - J and Z are out of scope for the letter model

- **Date:** 2026-10-04
- **Decision:** The letter model covers the 24 static letters (A-Y without J
  and Z) plus a `no_sign` class. J and Z are excluded.
- **Reason:** Both letters are defined by motion, so a single-frame classifier
  cannot represent them. No dataset available here has them as clean
  per-letter clips: the Google ASL Fingerspelling set labels whole phrases,
  not individual letters.
- **Alternatives rejected:**
  - Training them from the fingerspelling set anyway - needs CTC over phrase
    labels, which is a different model and a later stretch goal.
  - Approximating them with a static handshape - dishonest about what the
    model can actually do.
- **Consequence:** Stated in the README limitations and in the final report.

## D-0004 - Sign model input: both hands plus two shoulder points, no face or lips

- **Date:** 2026-10-04
- **Decision:** For the signs stage the input is both hands (21 landmarks
  each) plus BlazePose indices 11 and 12 (the shoulders). The 468 face
  landmarks and all lip points are dropped on first load.
- **Reason:** Location relative to the body distinguishes many signs, and
  recovering it needs the shoulders (preprocessing step 5: origin at the
  shoulder midpoint, scaled by shoulder width). Translation to the wrist and
  palm-size scaling alone discard exactly that information. Lip points cost
  browser time in the live demo and have not been shown to be needed here.
- **Alternatives rejected:**
  - Keeping all 543 landmarks - 468 are face points, which dominate the input
    and cost memory and time for no demonstrated gain.
  - Keeping lips only - plausible for signs with mouth morphemes, but
    unjustified until there is evidence.
- **Revisit if:** the confusion matrix shows errors that are plausibly
  lip-dependent.

## D-0005 - Python floor 3.11, numpy pinned to the 2.4 line

- **Date:** 2026-10-04
- **Decision:** `requires-python = ">=3.11"`, ruff `target-version = "py311"`,
  `numpy==2.4.6`, `PyYAML==6.0.3`.
- **Reason:** numpy 2.4.6 is the newest release that still ships wheels for
  cp311 through cp314, so the same pin holds whether Colab is on 3.11, 3.12 or
  3.13. The current numpy 2.5 line requires Python >= 3.12, which would push
  the floor up before the Colab runtime has been checked.
- **Alternatives rejected:**
  - Floor `>=3.10` with `numpy==2.2.x` - keeps an old numpy for the sake of a
    Python version Colab has long since left behind.
  - Floor `>=3.12` with `numpy==2.5.3` - matches the author machine (3.12.10)
    but breaks if Colab is still on 3.11.
- **Open:** the real Colab Python version is unverified. Confirm it in issue #1
  and tighten the floor in a follow-up PR.

## D-0006 - LF line endings forced through `.gitattributes`

- **Date:** 2026-10-04
- **Decision:** `.gitattributes` sets `* text=auto eol=lf` plus explicit
  per-extension rules, and `mixed-line-ending --fix=lf` runs in pre-commit.
- **Reason:** The development machine has `core.autocrlf=true` set globally,
  which would otherwise store CRLF in the index. CI runs on Linux, and the
  Python/JS golden-fixture parity tests compare output across both platforms;
  a line-ending difference there is a silent and confusing failure.
- **Alternatives rejected:** Changing the global git config instead - fixes one
  machine, not the repository, and does nothing for a future contributor.

## D-0007 - No `jsonschema` dependency; `schema.py` validates in plain Python

- **Date:** 2026-10-04
- **Decision:** The clip-format validator in `src/asl/schema.py` will be
  hand-written Python that raises with a clear message naming the offending
  file and field.
- **Reason:** The format has about a dozen fields. A hand-written check keeps
  the Colab install thinner and gives better error messages than a generic
  validator, and it has to fail loudly with context anyway.
- **Alternatives rejected:** `jsonschema` or `pydantic` - more dependency
  surface and worse messages for a format this small.

## D-0008 - Test skeletons are explicitly skipped, never empty

- **Date:** 2026-10-04
- **Decision:** The scaffold ships `tests/test_features.py`,
  `tests/test_export.py` and `tests/features.test.js` as skeletons whose cases
  are skipped with a reason naming the issue that will implement them, not as
  empty files or `pass` bodies.
- **Reason:** CLAUDE.md requires the test before any preprocessing or export
  change. A file of empty test functions reports green and is
  indistinguishable from real coverage; a skipped test with a reason shows up
  in every pytest and CI summary and names what is still missing.
- **Alternatives rejected:**
  - No test files until the code exists - loses the test-first discipline and
    the record of which cases the contract requires.
  - `xfail` - wrong semantics. The code does not exist, so nothing is failing.

## D-0009 - `pages.yml` and the smoke-run CI step are deferred

- **Date:** 2026-10-04
- **Decision:** The scaffold ships `ci.yml` only (ruff, pytest, node tests).
  `pages.yml` lands with the browser demo (issue #3). The smoke training run
  lands with `src/asl/train.py`, `configs/smoke.yaml` and
  `tests/fixtures/smoke/`; it is left in `ci.yml` as a commented TODO.
- **Reason:** `pages.yml` would deploy a `web/` directory that does not exist,
  and the smoke step would invoke a module that does not exist. Both would
  either fail or pass vacuously.
- **Consequence:** Issue #2 ("CI green") is **not** closable until the smoke
  run actually executes in CI. A green scaffold CI is not that gate criterion.

## D-0010 - Dependencies are added only when a module imports them

- **Date:** 2026-10-04
- **Decision:** The scaffold pins `numpy` and `PyYAML` (runtime) and `pytest`,
  `ruff`, `pre-commit` (dev), and nothing else. `torch`, `onnx`,
  `onnxruntime`, `mediapipe`, `scikit-learn` and any tracking library are added
  by the PR that introduces the module needing them. Node has no dependencies
  at all: `node --test` is built in and `web/features.js` is a pure ES module.
- **Reason:** The heavy pins must be verified against a live Colab runtime and,
  for MediaPipe, matched to the exact `.task` file the browser loads and
  checked by SHA-256 (rule 4). Pinning them blind now would record versions
  nobody has run.
- **Alternatives rejected:** A full upfront lock file - records unverified
  versions and slows every CI run for packages the code does not yet import.

## D-0011 - GitHub milestones, labels and gate issues

- **Date:** 2026-10-04
- **Decision:** Six milestones, one per phase, titled with an ASCII hyphen
  (`Phase 1 - Setup + spike`) and carrying the gate text plus the tag to apply
  on pass. Labels `phase-1`..`phase-6`, `bug`, `experiment`, `data`, `web`,
  `docs`, `blocked`. One issue per Phase 1 gate criterion (#1-#7) plus the
  scaffold (#8), each with a "Done when" checklist and an "Evidence to attach"
  section.
- **Reason:** The repo and GitHub are the whole project memory between
  sessions. The evidence section exists so a later phase-gate check reads real
  logs and links instead of inferring progress from code that merely exists.
  The ASCII hyphen keeps `gh issue list --milestone "..."` typable on Windows.
- **Alternatives rejected:**
  - Em dashes in milestone titles, matching the CLAUDE.md prose - awkward to
    quote in the Windows shell.
  - Milestone due dates - the phase weeks have no absolute start date yet.

## D-0012 - JS tests are run by glob, plus an explicit `package.json`

- **Date:** 2026-10-04
- **Decision:** The JS test command is `node --test "tests/**/*.test.js"`, not
  `node --test tests/`. A dependency-free root `package.json` sets
  `"type": "module"` and names the command once under `scripts.test`.
- **Reason:** Two separate problems, found by running the commands.
  1. From Node 22 on, a positional argument to `--test` is a glob pattern, not
     a directory to scan. `node --test tests/` tries to execute `tests` as a
     module and dies with `MODULE_NOT_FOUND` on Node 24.14.0. The glob form
     works and exits 0.
  2. `tests/features.test.js` uses `import`. Node 24 happens to accept that in
     a `.js` file through syntax detection, but that is an implicit fallback.
     `"type": "module"` states it, and keeps `web/features.js` importable as
     the pure ES module rule 1 requires.
- **Alternatives rejected:**
  - Bare `node --test` with no path - works, but scans the whole repository
    and would pick up stray test files outside `tests/`.
  - Renaming to `.mjs` - diverges from the filename CLAUDE.md specifies.
  - Relying on Node syntax detection - works today on Node 24, undefined on
    older runners.
- **Consequence:** The broken form appeared in four places. The user approved
  the edit on 2026-10-04 and it was applied to the CLAUDE.md "Commands" block
  and its per-commit rule, to the verify step of the `preprocessing-change`
  skill, and to the PR template. `docs/decisions.md` still quotes the broken
  form on purpose, to explain what was wrong.

---

## Still open, must close by the end of Phase 1

Tracked here so they cannot be forgotten. Each gets a numbered entry above
when it closes.

- Which public letter image sets to combine (a data card each, first).
- The 30-50 sign subset of ISLR - issue #6.
- Whether ASL Citizen is usable: license, vocabulary overlap, extraction cost.
- Volunteers and recording dates, and whether a Deaf ASL signer can join one
  recording session live by video call.
- The exact pinned versions of the MediaPipe Python package and
  `@mediapipe/tasks-vision`, and the SHA-256 of the shared
  `hand_landmarker.task` used by both (rule 4) - issue #3.
- The real Colab Python version, to tighten D-0005 - issue #1.
