"""Echo handler – replies with the same text received."""

from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes


async def echo_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reply to any text message with the same text."""
    text: str = update.message.text or ""
    await update.message.reply_text(text)
