"""Send command list."""

from telegram import Update
from telegram.ext import ContextTypes

HELP_TEXT = (
    "/ask <text> – Ask the LLM\n"
    "/clear – Clear chat memory\n"
    "/stats – Show stored turns\n"
    "/debug on|off – Show hidden <think> blocks"
)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text(HELP_TEXT)
