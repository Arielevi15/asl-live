"""Real guard tests for the repository rules that can be checked statically.

Unlike the other files in tests/, nothing here is skipped: these all run today
and must stay green.
"""

from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]

# Rule 9 forbids the overclaiming word in code, UI, README and commits. These
# are the trees that carry code, UI and the README. docs/ and tests/ are
# excluded on purpose: docs/decisions.md has to be able to record *why* the
# word is banned, and this file has to contain the needle it searches for.
RULE_9_ROOTS = ("README.md", "src", "web")
RULE_9_SUFFIXES = {".py", ".js", ".html", ".css", ".json", ".md", ".yaml", ".yml"}
BANNED_SUBSTRING = "translat"


def _rule_9_files() -> list[Path]:
    files: list[Path] = []
    for name in RULE_9_ROOTS:
        root = REPO / name
        if not root.exists():
            continue
        if root.is_file():
            files.append(root)
            continue
        files.extend(
            path for path in root.rglob("*") if path.is_file() and path.suffix in RULE_9_SUFFIXES
        )
    return files


def test_package_is_importable_and_versioned():
    import asl

    assert isinstance(asl.__version__, str)
    assert asl.__version__


def test_no_overclaiming_language_in_code_ui_or_readme():
    """Rule 9: this recognises letters and signs; it does not convert languages."""
    offenders = [
        str(path.relative_to(REPO))
        for path in _rule_9_files()
        if BANNED_SUBSTRING in path.read_text(encoding="utf-8").lower()
    ]
    assert not offenders, (
        f"Rule 9 violation: overclaiming wording found in {offenders}. "
        "This project does recognition of letters and isolated signs."
    )


def test_gitattributes_forces_lf():
    """docs/decisions.md D-0006: the index must hold LF regardless of autocrlf."""
    text = (REPO / ".gitattributes").read_text(encoding="utf-8")
    assert "* text=auto eol=lf" in text


@pytest.mark.parametrize(
    "entry",
    [
        "data/",
        "checkpoints/",
        "*.pt",
        "*.pth",
        "*.npy",
        "*.parquet",
        "kaggle.json",
        ".env",
        "__pycache__/",
        ".ipynb_checkpoints/",
        "wandb/",
        "recordings/",
    ],
)
def test_gitignore_covers_required_entry(entry):
    """CLAUDE.md lists the minimum set that .gitignore must cover."""
    lines = {
        line.strip() for line in (REPO / ".gitignore").read_text(encoding="utf-8").splitlines()
    }
    assert entry in lines


def test_requirements_are_exactly_pinned():
    """CLAUDE.md: pin every dependency. requirements.txt is the Colab lock file."""
    unpinned = []
    for line in (REPO / "requirements.txt").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "==" not in line:
            unpinned.append(line)
    assert not unpinned, f"requirements.txt has unpinned entries: {unpinned}"


def test_onnx_is_ignored_except_under_web_model():
    """The small shipped model must survive the blanket *.onnx ignore rule."""
    text = (REPO / ".gitignore").read_text(encoding="utf-8")
    assert "*.onnx" in text
    assert "!web/model/*.onnx" in text
