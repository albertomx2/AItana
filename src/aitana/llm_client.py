"""Async wrapper for Together AI chat completions."""

from __future__ import annotations

import os
from typing import Any, TypedDict, cast

import httpx

API_URL = "https://api.together.xyz/v1/chat/completions"
_MODEL = os.getenv("MODEL_NAME", "deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free")
MODEL_NAME: str = cast(str, _MODEL)
MAX_TOKENS_OUT = int(os.getenv("MAX_TOKENS_OUT", "600"))


class Message(TypedDict):
    role: str
    content: str


async def generate(messages: list[Message]) -> str:
    """Call Together AI and return the assistant's reply."""
    api_key = os.getenv("TOGETHER_API_KEY")
    if api_key is None:
        raise RuntimeError(
            "TOGETHER_API_KEY missing – add it to .env or export it."
        )

    payload: dict[str, Any] = {
        "model": MODEL_NAME,
        "messages": messages,
        "max_tokens": MAX_TOKENS_OUT,
        "temperature": 0.7,
    }
    headers = {"Authorization": f"Bearer {api_key}"}

    async with httpx.AsyncClient(timeout=120) as client:
        resp = await client.post(API_URL, json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"].strip()
