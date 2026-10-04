// JS half of the Python/JS parity check (rule 1).
//
// web/features.js is a pure ES module - no DOM, no camera, no globals - which
// is exactly what lets this file import it under `node --test` and compare its
// output with the vectors produced by src/asl/features.py.
//
// Skeleton only: web/features.js does not exist yet. The cases are skipped
// with a reason rather than left empty, so the node --test summary keeps
// reporting what is missing (see docs/decisions.md D-0008).

import test from "node:test";

const SKIP_REASON = "web/features.js not implemented yet - see issue #3";

// Golden fixtures: raw landmark inputs plus the expected feature vectors
// written by scripts/make_fixtures.py. Tolerance is 1e-5, per rule 1.
test("features.js matches the golden fixtures within 1e-5", { skip: SKIP_REASON }, () => {
  throw new Error(SKIP_REASON);
});

test("FEATURE_VERSION equals the value in features.py", { skip: SKIP_REASON }, () => {
  throw new Error(SKIP_REASON);
});

test("a missing hand yields zeros plus a mask flag", { skip: SKIP_REASON }, () => {
  throw new Error(SKIP_REASON);
});

test("no NaN or Infinity is ever returned", { skip: SKIP_REASON }, () => {
  throw new Error(SKIP_REASON);
});

test("the module imports with no DOM, camera or globals present", { skip: SKIP_REASON }, () => {
  throw new Error(SKIP_REASON);
});
