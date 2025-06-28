"""Return number of stored message pairs."""

from telegram import Update
from telegram.ext import ContextTypes

from aitana import memory


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not (update.message and update.effective_chat):
        return
    n = await memory.count_pairs(update.effective_chat.id)
    await update.message.reply_text(f"You have {n} message pairs stored.")
