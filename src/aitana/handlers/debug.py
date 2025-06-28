"""Toggle showing <think> blocks."""

from telegram import Update
from telegram.ext import ContextTypes

from aitana import memory


async def debug_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not (update.message and update.effective_chat):
        return

    text = update.message.text or ""
    arg = text.split(maxsplit=1)[1] if len(text.split(maxsplit=1)) > 1 else ""
    arg = arg.lower().strip()
    if arg not in {"on", "off"}:
        await update.message.reply_text("Usage: /debug on|off")
        return

    await memory.set_debug(update.effective_chat.id, arg == "on")
    await update.message.reply_text(f"Debug mode set to {arg.upper()}")
