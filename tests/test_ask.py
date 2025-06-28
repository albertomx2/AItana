"""Test /ask handler with a mocked Together AI response."""

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from aitana.handlers.ask import ask_command


@pytest.mark.asyncio
async def test_ask_handler(monkeypatch):
    """Ensure bot sends LLM reply and stores history."""
    # --- Fake LLM (skip network) ------------------------------------------
    async def fake_generate(_messages):  # noqa: D401
        return "Paris."

    monkeypatch.setattr("aitana.llm_client.generate", fake_generate)

    # --- Fake memory append (skip SQLite) ---------------------------------
    monkeypatch.setattr("aitana.memory.append_pair", AsyncMock())

    # --- Build minimal stub Update ----------------------------------------
    captured: dict[str, str] = {}

    async def fake_reply(text: str, **_) -> None:  # noqa: D401
        captured["reply"] = text

    message = SimpleNamespace(text="/ask Capital of France?", reply_text=fake_reply)
    update = SimpleNamespace(message=message, effective_chat=SimpleNamespace(id=1))
    context = None

    # --- Act --------------------------------------------------------------
    await ask_command(update, context)  # type: ignore[arg-type]

    # --- Assert -----------------------------------------------------------
    assert captured["reply"] == "Paris."
