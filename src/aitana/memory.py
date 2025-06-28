"""Tiny SQLite memory for chat history + flags (/stats, /clear, /debug)."""

from __future__ import annotations

import asyncio
import sqlite3
from pathlib import Path
from typing import Iterable

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "aitana.db"
DB_PATH.parent.mkdir(exist_ok=True)


def _init_db() -> None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript(
        """
        CREATE TABLE IF NOT EXISTS history (
            chat_id INTEGER,
            role     TEXT,
            text     TEXT,
            ts       DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS flags (
            chat_id INTEGER PRIMARY KEY,
            debug   INTEGER DEFAULT 0
        );
        """
    )
    conn.commit()
    conn.close()


_init_db()

# ---------- Internal sync helpers ------------------------------------------ #


def _run(query: str, params: tuple | list[tuple] = ()) -> Iterable[tuple]:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    if isinstance(params, list):
        cur.executemany(query, params)
    else:
        cur.execute(query, params)
    if query.strip().lower().startswith("select"):
        rows = cur.fetchall()
    else:
        rows = []
    conn.commit()
    conn.close()
    return rows


# ---------- Public async API ------------------------------------------------ #


async def append_pair(chat_id: int, user_text: str, bot_text: str) -> None:
    await _aio(lambda: _run(
        "INSERT INTO history(chat_id, role, text) VALUES(?,?,?)",
        [(chat_id, "user", user_text), (chat_id, "assistant", bot_text)],
    ))


async def get_last(chat_id: int, limit: int) -> list[tuple[str, str]]:
    rows = await _aio(lambda: _run(
        "SELECT role, text FROM history WHERE chat_id=? "
        "ORDER BY ts DESC LIMIT ?",
        (chat_id, limit),
    ))
    return list(rows)[::-1]   # oldest → newest


async def count_pairs(chat_id: int) -> int:
    rows = await _aio(lambda: _run(
        "SELECT COUNT(*) FROM history WHERE chat_id=?", (chat_id,),
    ))
    return int(rows[0][0])


async def clear_history(chat_id: int) -> None:
    await _aio(lambda: _run(
        "DELETE FROM history WHERE chat_id=?", (chat_id,),
    ))


async def set_debug(chat_id: int, value: bool) -> None:
    await _aio(lambda: _run(
        "INSERT INTO flags(chat_id, debug) VALUES(?, ?) "
        "ON CONFLICT(chat_id) DO UPDATE SET debug=excluded.debug",
        (chat_id, int(value)),
    ))


async def get_debug(chat_id: int) -> bool:
    rows = await _aio(lambda: _run(
        "SELECT debug FROM flags WHERE chat_id=?", (chat_id,),
    ))
    return bool(rows[0][0]) if rows else False


# ---------- util ------------------------------------------------------------ #


async def _aio(func):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, func)
