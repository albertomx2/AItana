"""Smoke-test for the echo handler (Phase 4) without real Telegram objects."""

from types import SimpleNamespace
from typing import Any

import pytest

from aitana.handlers.echo import echo_text


@pytest.mark.asyncio
async def test_echo_text():
    """echo_text should reply with exactly the same text."""
    captured: list[str] = []

    async def fake_reply(text: str, **_: Any) -> None:  # noqa: D401
        captured.append(text)

    message = SimpleNamespace(text="ping", reply_text=fake_reply)
    update = SimpleNamespace(message=message)
    context = None  # Not used by the handler

    await echo_text(update, context)  # type: ignore[arg-type]
    assert captured == ["ping"]
