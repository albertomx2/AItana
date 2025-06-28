"""Handler for /ask command (Together AI – DeepSeek, with <think> filter)."""

from __future__ import annotations

import os
from typing import cast

from telegram import Update
from telegram.ext import ContextTypes

from aitana import llm_client, memory

MAX_HISTORY = int(os.getenv("MAX_HISTORY", "6"))


async def ask_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Answer user's question using LLM + short-term memory."""
    if not (update.message and update.effective_chat):
        return

    chat_id = cast(int, update.effective_chat.id)
    question = (update.message.text or "").partition(" ")[2].strip()
    if not question:
        await update.message.reply_text("Usage: /ask <your question>")
        return

    # 1. Build prompt: system + history + new user
    messages: list[llm_client.Message] = [
        {"role": "system", "content": "You are AItana, a helpful assistant."},
    ]
    hist = await memory.get_last(chat_id, MAX_HISTORY * 2)
    messages += [{"role": r, "content": t} for r, t in hist]
    messages.append({"role": "user", "content": question})

    # 2. Call the model
    try:
        raw_reply = await llm_client.generate(messages)
    except Exception as exc:  # noqa: BLE001
        await update.message.reply_text(f"⚠️ LLM error: {exc}")
        return

    # 3. Split <think> block if present
    think, final = _split_think(raw_reply)

    # 4. Send response(s) depending on debug flag
    if await memory.get_debug(chat_id) and think:
        await update.message.reply_text(f"<think>\n{think}\n</think>")
    await update.message.reply_text(final)

    # 5. Persist only visible part
    await memory.append_pair(chat_id, question, final)


# --------------------------------------------------------------------------- #
# Helpers                                                                     #
# --------------------------------------------------------------------------- #
def _split_think(text: str) -> tuple[str, str]:
    """Return (think, final) parts; think='' if not found."""
    if "<think>" in text and "</think>" in text:
        pre, rest = text.split("<think>", 1)
        think, post = rest.split("</think>", 1)
        combined = f"{pre.strip()} {post.strip()}".strip()
        return think.strip(), combined
    return "", text.strip()
