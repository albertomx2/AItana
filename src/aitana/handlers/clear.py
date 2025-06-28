"""Clear chat memory."""

from telegram import Update
from telegram.ext import ContextTypes

from aitana import memory


async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not (update.message and update.effective_chat):
        return
    await memory.clear_history(update.effective_chat.id)
    await update.message.reply_text("Conversation memory cleared ✅")
