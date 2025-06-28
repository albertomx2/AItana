"""Async wrapper for Together AI chat completions (DeepSeek-Chat)."""

from __future__ import annotations

import os
from typing import Any, TypedDict

import httpx

API_URL = "https://api.together.xyz/v1/chat/completions"
MODEL_NAME = os.getenv("MODEL_NAME", "deepseek-chat")
MAX_TOKENS_OUT = int(os.getenv("MAX_TOKENS_OUT", "300"))


class Message(TypedDict):
    role: str
    content: str


async def generate(messages: list[Message]) -> str:
    """Call Together AI and return the assistant's reply."""
    api_key = os.getenv("TOGETHER_API_KEY")  # ← se lee en cada llamada
    print("DEBUG API_KEY:", os.getenv("TOGETHER_API_KEY")[:8], flush=True)

    if api_key is None:
        raise RuntimeError(
            "TOGETHER_API_KEY missing – add it to .env or export it to enable /ask."
        )

    payload: dict[str, Any] = {
        "model": MODEL_NAME,
        "messages": messages,
        "max_tokens": MAX_TOKENS_OUT,
        "temperature": 0.7,
    }
    headers = {"Authorization": f"Bearer {api_key}"}

    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(API_URL, json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"].strip()
