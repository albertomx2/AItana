"""AItana – Phase 3: echo bot with modular handlers."""

from __future__ import annotations

import os

from dotenv import load_dotenv
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

from .handlers import echo_text, start_command
from .utils import logging as log_utils

# --------------------------------------------------------------------------- #
# Logging & config                                                            #
# --------------------------------------------------------------------------- #
log_utils.setup()

load_dotenv()
TOKEN = os.getenv("AITANA_TOKEN")
if TOKEN is None:
    raise RuntimeError(
        "Environment variable AITANA_TOKEN is not set. "
        "Define it or create a .env file with AITANA_TOKEN=<token>."
    )

# --------------------------------------------------------------------------- #
# Application setup                                                           #
# --------------------------------------------------------------------------- #
def build_app() -> Application:
    """Create and return a configured Application instance."""
    app = Application.builder().token(TOKEN).build()

    # Register handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_text))

    return app


def main() -> None:
    """Run the bot with polling."""
    app = build_app()
    app.run_polling()


if __name__ == "__main__":
    main()
