"""Handler for the /start command."""

from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a simple greeting when the user issues /start."""
    await update.message.reply_text("Hello! I’m AItana 🤖")
