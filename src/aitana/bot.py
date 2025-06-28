"""Minimal Telegram bot for AItana – Phase 2.

Run with:
    python -m aitana.bot
or simply:
    python src/aitana/bot.py
"""

from __future__ import annotations

import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    ContextTypes,
    MessageHandler,
    filters,
)

# --------------------------------------------------------------------------- #
# Logging                                                                      #
# --------------------------------------------------------------------------- #
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------- #
# Configuration                                                                #
# --------------------------------------------------------------------------- #
load_dotenv()  # Loads variables from .env into the environment (if .env exists)
TOKEN = os.getenv("AITANA_TOKEN")

if TOKEN is None:
    raise RuntimeError(
        "Environment variable AITANA_TOKEN is not set. "
        "Export it or create a .env file with AITANA_TOKEN=<your-token>."
    )

# --------------------------------------------------------------------------- #
# Handlers                                                                     #
# --------------------------------------------------------------------------- #
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Print every text message to stdout."""
    user = update.effective_user
    text = update.message.text if update.message else ""
    print(f"[{user.username or user.id}] {text}")


# --------------------------------------------------------------------------- #
# Entry point                                                                  #
# --------------------------------------------------------------------------- #
def main() -> None:
    """Start the bot (polling)."""
    application = Application.builder().token(TOKEN).build()

    # Register the handler for any plain text message (no commands)
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text)
    )

    logger.info("AItana bot started. Waiting for messages…")
    application.run_polling()


if __name__ == "__main__":
    main()
