"""Centralised logging configuration for AItana."""

from __future__ import annotations

import logging
import sys

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


def setup(level: int = logging.INFO) -> None:
    """Configure root logger once."""
    logging.basicConfig(
        stream=sys.stdout,
        format=LOG_FORMAT,
        level=level,
    )
