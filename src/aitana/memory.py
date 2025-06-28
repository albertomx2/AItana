"""Tiny SQLite memory for chat histories."""

from __future__ import annotations

import asyncio
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "aitana.db"
DB_PATH.parent.mkdir(exist_ok=True)


def _init_db() -> None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS history "
        "(chat_id INTEGER, role TEXT, text TEXT, ts DATETIME DEFAULT CURRENT_TIMESTAMP)"
    )
    conn.commit()
    conn.close()


_init_db()  # run at import


async def get_last(chat_id: int, limit: int) -> list[tuple[str, str]]:
    """Return [(role, text), …] (newest last)."""
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        None,
        _read_sync,
        chat_id,
        limit,
    )


def _read_sync(chat_id: int, limit: int):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT role, text FROM history "
        "WHERE chat_id=? ORDER BY ts DESC LIMIT ?",
        (chat_id, limit),
    )
    out = cur.fetchall()[::-1]  # reverse to oldest→newest
    conn.close()
    return out


async def append_pair(chat_id: int, user_text: str, bot_text: str) -> None:
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, _write_sync, chat_id, user_text, bot_text)


def _write_sync(chat_id: int, user_text: str, bot_text: str) -> None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executemany(
        "INSERT INTO history(chat_id, role, text) VALUES(?,?,?)",
        [
            (chat_id, "user", user_text),
            (chat_id, "assistant", bot_text),
        ],
    )
    conn.commit()
    conn.close()
