"""Hand-checked tests for the preprocessing contract.

These are deliberately NOT generated from the output of `features.py`. Golden
fixtures only prove that the JS port matches the Python original; they would
happily freeze a Python bug. Every expected value below must be worked out by
hand from the contract in CLAUDE.md before the test is unskipped.

Skeleton only: `src/asl/features.py` does not exist yet. The cases are skipped
with a reason rather than left empty, so that pytest and CI keep reporting what
is still missing (see docs/decisions.md D-0008).
"""

import pytest

SKIP_REASON = "src/asl/features.py not implemented yet - see issue #3"

pytestmark = pytest.mark.skip(reason=SKIP_REASON)


def test_coordinates_are_converted_to_pixels_before_anything_else():
    """Contract step 2: x *= frame_width, y *= frame_height.

    A normalised point (0.5, 0.25) in a 1280x720 frame must become
    (640.0, 180.0) before translation or scaling touch it. Running the same
    hand through 1280x720 and 640x480 must give the same final features, which
    is the whole reason the conversion happens first.
    """
    raise NotImplementedError(SKIP_REASON)


def test_translate_puts_wrist_at_origin():
    """Contract step 3: landmark 0 (wrist) becomes exactly (0, 0).

    Hand-checked: feed a hand whose wrist sits at (100, 200) and assert the
    wrist component of the output is 0 and every other point moved by the same
    offset.
    """
    raise NotImplementedError(SKIP_REASON)


def test_scale_makes_palm_size_one():
    """Contract step 4: divide by palm size (wrist to middle-finger MCP).

    Hand-checked: a hand with wrist at the origin and middle-finger MCP at
    (0, 50) must come out with that distance equal to 1.0. The same hand scaled
    by any factor must produce identical features.
    """
    raise NotImplementedError(SKIP_REASON)


def test_left_hand_is_mirrored_to_right():
    """Contract step 6, letters: mirror left hands onto the right-hand frame.

    Hand-checked: a left hand and its exact mirror image as a right hand must
    produce the same feature vector. Note MediaPipe handedness labels assume a
    mirrored selfie image, so this must also be verified against a real left
    hand, not only synthetic points.
    """
    raise NotImplementedError(SKIP_REASON)


def test_signs_mirror_the_whole_frame_never_one_hand():
    """Contract step 6, signs: dominance is decided per clip.

    Mirroring must apply to every landmark including the shoulders. Mirroring
    the hands independently would scramble two-handed signs, so assert that a
    left-dominant clip and its mirrored twin agree, and that no code path
    mirrors a single hand.
    """
    raise NotImplementedError(SKIP_REASON)


def test_body_frame_uses_shoulder_midpoint_and_shoulder_width():
    """Contract step 5, signs only.

    Hand-checked: shoulders at (100, 300) and (300, 300) give a midpoint of
    (200, 300) and a width of 200. A hand at (300, 300) must land at
    (0.5, 0.0) in the body frame.
    """
    raise NotImplementedError(SKIP_REASON)


def test_missing_hand_gives_zeros_and_mask():
    """Contract step 7: a missing hand is zeros plus a mask flag.

    Hand-checked: a frame storing `null` for a hand must produce an all-zero
    block for that hand and a mask entry marking it absent - not dropped
    columns, not a sentinel value.
    """
    raise NotImplementedError(SKIP_REASON)


def test_nan_never_reaches_the_model():
    """Contract step 7: NaN must never leave `features.py`.

    Feed NaN coordinates, a zero-length palm (wrist and MCP at the same point,
    which would divide by zero) and an empty frame. Every output must be
    finite.
    """
    raise NotImplementedError(SKIP_REASON)


def test_feature_version_matches_features_js():
    """Rule 1: the two implementations declare the same FEATURE_VERSION.

    Reads the integer constant from src/asl/features.py and parses it out of
    web/features.js, then asserts equality. This is the cheap tripwire for a
    Python change that was never ported.
    """
    raise NotImplementedError(SKIP_REASON)


def test_golden_fixtures_match_within_tolerance():
    """Rule 1: JS output matches Python output within 1e-5 on every fixture.

    The Python half lives here; the JS half lives in tests/features.test.js.
    Both read the same files from tests/fixtures/.
    """
    raise NotImplementedError(SKIP_REASON)
