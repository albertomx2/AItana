"""Wrapper que lanza `ruff check --fix src tests`."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> None:  # noqa: D401
    """Run Ruff with auto-fix on src/ and tests/."""
    root = Path(__file__).resolve().parents[3]  # …/AItana/
    src_dir = root / "src"
    tests_dir = root / "tests"
    sys.exit(subprocess.call(["ruff", "check", "--fix", str(src_dir), str(tests_dir)]))
