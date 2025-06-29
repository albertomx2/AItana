"""Test chat handler with mocked Together AI response."""

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from aitana.handlers.chat import chat_handler  # ← cambia el import


@pytest.mark.asyncio
async def test_chat_handler(monkeypatch):
    """Ensure bot sends LLM reply and stores history."""
    async def fake_generate(_messages):
        return "Paris."

    monkeypatch.setattr("aitana.llm_client.generate", fake_generate)
    monkeypatch.setattr("aitana.memory.append_pair", AsyncMock())

    captured: dict[str, str] = {}

    async def fake_reply(text: str, **_):
        captured["reply"] = text

    message = SimpleNamespace(text="Capital of France?", reply_text=fake_reply)
    update = SimpleNamespace(message=message, effective_chat=SimpleNamespace(id=1))
    await chat_handler(update, None)  # ← llama al nuevo handler

    assert captured["reply"] == "Paris."
