"""AItana – main entry-point (Phase 7)."""

from __future__ import annotations

import asyncio
import os
from typing import cast

from dotenv import load_dotenv
from telegram import BotCommand
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

from .handlers import (
    chat_handler,
    clear_command,
    debug_command,
    help_command,
    start_command,
    stats_command,
)
from .utils import logging as log_utils

# --------------------------------------------------------------------------- #
# Logging & config                                                            #
# --------------------------------------------------------------------------- #
log_utils.setup()
load_dotenv()

_raw_token = os.getenv("AITANA_TOKEN")
if _raw_token is None:
    raise RuntimeError(
        "Environment variable AITANA_TOKEN is not set. "
        "Define it or create a .env file with AITANA_TOKEN=<token>."
    )

TOKEN: str = cast(str, _raw_token)

# --------------------------------------------------------------------------- #
# Application setup                                                           #
# --------------------------------------------------------------------------- #
COMMAND_LIST = [
    ("help",  "Show help"),
    ("clear", "Clear chat memory"),
    ("stats", "Show message count"),
    ("debug", "Toggle think blocks"),
]


def build_app() -> Application:
    """Create and return a configured Application instance."""
    app = Application.builder().token(TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("clear", clear_command))
    app.add_handler(CommandHandler("debug", debug_command))

    # All other text → LLM
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_handler))

    # Log handlers for debug
    log_utils.logging.getLogger(__name__).info("Handlers registered: %s", app.handlers)
    return app


async def _set_commands(app: Application) -> None:
    """Expose commands to Telegram client autocomplete."""
    await app.bot.set_my_commands([BotCommand(cmd, desc) for cmd, desc in COMMAND_LIST])


def main() -> None:
    """Run the bot with polling."""
    app = build_app()
    # register commands on startup
    asyncio.get_event_loop().run_until_complete(_set_commands(app))
    app.run_polling()


if __name__ == "__main__":
    main()
