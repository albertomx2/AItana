"""Smoke-tests for /help and /stats."""

from types import SimpleNamespace

import pytest

from aitana import memory
from aitana.handlers.help import help_command
from aitana.handlers.stats import stats_command


@pytest.mark.asyncio
async def test_help(monkeypatch):
    out = {}
    async def fake_reply(text, **_): out["t"] = text
    msg = SimpleNamespace(text="/help", reply_text=fake_reply)
    update = SimpleNamespace(message=msg)
    await help_command(update, None)
    assert "/ask" in out["t"]

@pytest.mark.asyncio
async def test_stats(monkeypatch):
    chat_id = 42
    await memory.clear_history(chat_id)
    msg = SimpleNamespace(text="/stats", reply_text=lambda *a, **k: None)
    update = SimpleNamespace(message=msg, effective_chat=SimpleNamespace(id=chat_id))
    out = {}
    async def fake_reply(text, **_): out["r"]=text
    monkeypatch.setattr(msg, "reply_text", fake_reply)
    await stats_command(update, None)
    assert "0 message pairs" in out["r"]
