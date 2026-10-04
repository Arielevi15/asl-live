# asl-live

Real-time recognition of American Sign Language in the browser: fingerspelled
letters first, then a vocabulary of isolated signs. Training runs in Google
Colab; inference runs entirely client-side with MediaPipe Tasks JS and ONNX
Runtime Web, deployed as a static site on GitHub Pages.

**Status: work in progress.** Phase 1 of 6 (setup and end-to-end spike). There
is no live demo yet and no results to report. This README will carry the
results table and the demo link once they exist.

## What this is, and what it is not

This recognises **individual fingerspelled letters and individual isolated
signs**. It does not interpret sentences, grammar or meaning. ASL is a full
language with its own syntax, spatial grammar and non-manual markers; a
per-letter and per-sign classifier is a small building block, nothing more.

The goal of the project is not a high number on a public benchmark. It is:

1. an honest, **signer-independent** evaluation (train, validation and test
   never share a person),
2. a **measured gap** between accuracy on public data and accuracy on real
   webcam video from people the model never saw, and
3. a demo that works for those people.

Known limitations, stated up front:

- **J and Z are out of scope** for the letter model. Both need motion, and no
  dataset used here has them as clean per-letter clips.
- The test volunteers are mostly **not ASL signers**, so they are novice
  learners, and the person checking their signing during recording is not an
  ASL signer either. Subtle handshape errors can pass unnoticed.

## Privacy

Camera frames never leave the device: landmark extraction and inference both
run in the browser. For the recorded evaluation sessions, **no video is ever
captured or stored** - only numeric hand landmarks. Participants are
identified by pseudonymous IDs only, recorded with written consent, and nothing
of theirs is published without separate permission.

## How it works

1. MediaPipe Tasks Hand Landmarker gives 21 points per hand (plus two shoulder
   points from the Pose Landmarker, for signs, where location matters).
2. A single preprocessing contract turns those points into a feature vector:
   pixel units, wrist origin, palm-size scaling, handedness canonicalisation,
   explicit masks for missing hands. `src/asl/features.py` is the source of
   truth and `web/features.js` is a port of it, held to within `1e-5` of the
   Python output by golden-fixture tests.
3. A small model (MLP for letters; a conv plus sequence model for signs) is
   trained in Colab, exported to ONNX, and checked against PyTorch on the same
   fixtures before it is allowed into `web/`.
4. The browser runs the same features and the exported model, with temporal
   smoothing before a letter is committed.

## Repository layout

```
configs/      one YAML per experiment
docs/         decisions.md and one data card per dataset
src/asl/      all logic: schema, data, extraction, features, models, train, eval, export
notebooks/    thin Colab bootstrap only
web/          the static demo, the record page, and the exported model
tests/        Python tests, JS parity tests, golden fixtures
reports/runs/ one folder per training run: resolved config, commit, seed, metrics
```

## Development

```bash
pip install -e ".[dev]"          # install the package and dev tools
pre-commit install               # enable the commit guard rails
pytest -q                        # Python tests
node --test "tests/**/*.test.js"  # JS parity tests
python -m http.server -d web 8000  # local demo at http://localhost:8000
```

Requires Python >= 3.11 and Node >= 22. Camera access needs HTTPS or
`localhost`.

Datasets are never committed. Each one has a card in `docs/data_cards/` with
its license and the steps to download it yourself.

## License

MIT for the code in this repository. The datasets are **not** covered by it -
see each data card for the terms that apply to the data.
