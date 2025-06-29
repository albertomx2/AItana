"""Main chat handler – any plain message goes to the LLM or registers an expense."""

from __future__ import annotations

import os
from typing import cast

from telegram import Update
from telegram.ext import ContextTypes

from aitana import llm_client, memory
from aitana.utils.expenses import add_expense, parse_expense  # 🆕 expense utils

MAX_HISTORY = int(os.getenv("MAX_HISTORY", "6"))


async def chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle normal text messages: detect expenses or reply with LLM."""
    if not (update.message and update.effective_chat):
        return

    chat_id = cast(int, update.effective_chat.id)
    text = (update.message.text or "").strip()
    if not text:
        return

    # 🔍 1) Try to parse as expense
    exp = parse_expense(text)
    if exp:
        add_expense(exp)
        await update.message.reply_text(
            f"✅ Gasto registrado: {exp['amount']:.2f} € en {exp['place']}."
        )
        return  # no LLM call

    # 🤖 2) Otherwise, build prompt for the LLM
    messages: list[llm_client.Message] = [
    {
        "role": "system",
        "content": (
            "You are AItana, a helpful assistant.\n"
            "If you include a <think> block, ALWAYS close it with </think>."
        ),
    },
]
    history = await memory.get_last(chat_id, MAX_HISTORY * 2)
    messages += [{"role": r, "content": t} for r, t in history]
    messages.append({"role": "user", "content": text})

    # 3) Call model
    try:
        raw = await llm_client.generate(messages)
    except Exception as exc:  # noqa: BLE001
        await update.message.reply_text(f"⚠️ LLM error: {exc}")
        return

    think, final = _split_think(raw)

    # 4) Send response(s)
    if await memory.get_debug(chat_id) and think:
        await update.message.reply_text(f"<think>\n{think}\n</think>")
    await update.message.reply_text(final)

    # 5) Persist
    await memory.append_pair(chat_id, text, final)


# ---------- helpers -------------------------------------------------------- #
def _split_think(text: str) -> tuple[str, str]:
    """Return (think, final) parts; think='' if absent."""
    if "<think>" in text and "</think>" in text:
        pre, rest = text.split("<think>", 1)
        think, post = rest.split("</think>", 1)
        combined = f"{pre.strip()} {post.strip()}".strip()
        return think.strip(), combined
    return "", text.strip()
