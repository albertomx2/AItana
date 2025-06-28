"""Handler for /ask command (DeepSeek via Together AI)."""

from __future__ import annotations

import os

from telegram import Update
from telegram.ext import ContextTypes

from aitana import llm_client, memory

MAX_HISTORY = int(os.getenv("MAX_HISTORY", "6"))


async def ask_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Answer user's question using LLM + short-term memory."""
    # Aseguramos que existen message y chat; si no, salimos
    if not (update.message and update.effective_chat):
        return

    question = (update.message.text or "").partition(" ")[2].strip()

    if not question:
        await update.message.reply_text("Usage: /ask <your question>")
        return

    # 1. Construir mensajes: system + history + nuevo user
    messages: list[llm_client.Message] = [
        {"role": "system", "content": "You are AItana, a helpful assistant."},
    ]
    hist = await memory.get_last(update.effective_chat.id, MAX_HISTORY * 2)
    messages += [{"role": r, "content": t} for r, t in hist]
    messages.append({"role": "user", "content": question})

    # 2. Llamar al modelo
    try:
        reply = await llm_client.generate(messages)
    except Exception as exc:  # noqa: BLE001
        await update.message.reply_text(f"⚠️ LLM error: {exc}")
        return

    # 3. Responder y guardar
    await update.message.reply_text(reply)
    await memory.append_pair(update.effective_chat.id, question, reply)
