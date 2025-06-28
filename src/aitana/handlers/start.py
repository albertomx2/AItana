"""Send welcome + help."""

from telegram import Update
from telegram.ext import ContextTypes

from .help import help_command


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await help_command(update, context)
