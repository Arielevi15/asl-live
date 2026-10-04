"""Export parity and interface-contract tests.

Skeleton only: `src/asl/export.py` does not exist yet. Rule 5 says an exported
ONNX model must match PyTorch on the golden fixtures before it is allowed into
`web/`, and the interface contracts say the labels file, the class order in the
training config and the ONNX metadata must all agree. These are the tests that
enforce that, and they are skipped with a reason until the code exists
(docs/decisions.md D-0008).
"""

import pytest

SKIP_REASON = "src/asl/export.py not implemented yet - see issue #3"

pytestmark = pytest.mark.skip(reason=SKIP_REASON)


def test_onnx_matches_pytorch_on_golden_fixtures():
    """Rule 5: same inputs, same logits, within tolerance.

    Run the PyTorch checkpoint and the exported ONNX model on every golden
    fixture and compare logits. A mismatch means the export is wrong, not that
    the tolerance needs loosening.
    """
    raise NotImplementedError(SKIP_REASON)


def test_model_io_names_and_shapes():
    """Interface contract, model I/O.

    Letters: input `features` float32 [N, F], output `logits` float32 [N, C].
    Signs: inputs `features` float32 [N, T, F] and `mask` bool [N, T], output
    `logits` float32 [N, C]. N must be a dynamic batch dimension, and softmax
    must NOT be baked into the graph - it is applied in JS.
    """
    raise NotImplementedError(SKIP_REASON)


def test_labels_file_order_equals_training_config_order():
    """Interface contract, label file.

    Class order is defined once, in the training config. Assert the order in
    `web/model/<model_id>.labels.json` is identical, not merely the same set.
    A reordering here silently relabels every prediction in the browser.
    """
    raise NotImplementedError(SKIP_REASON)


def test_onnx_metadata_matches_labels_file():
    """Interface contract: `model_id`, `feature_version`, `classes_sha256`.

    The ONNX metadata properties must match the labels file exactly, so that
    `app.js` can refuse to run a model that was built against different
    features or a different class list.
    """
    raise NotImplementedError(SKIP_REASON)


def test_exported_model_is_under_the_size_budget():
    """Target table: model size < 5 MB.

    GitHub Pages serves the model from the repo and Git LFS is not an option
    there, so the budget is also the pre-commit large-file limit.
    """
    raise NotImplementedError(SKIP_REASON)
