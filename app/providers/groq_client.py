from __future__ import annotations

import httpx
from typing import List

from app.core.config import settings
from .interfaces import ChatRequest, ChatResponse, LLMClient


class GroqClient(LLMClient):
    def __init__(self, base_url: str = "https://api.groq.com/openai/v1", api_key: str | None = None):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key or settings.groq_api_key or ""
        self._client = httpx.AsyncClient(base_url=self.base_url, headers={
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }, timeout=30.0)

    async def chat(self, req: ChatRequest) -> ChatResponse:
        payload = {
            "model": req.model,
            "messages": [{"role": m.role, "content": m.content} for m in req.messages],
            "temperature": req.temperature,
            "max_tokens": req.max_tokens,
            "stream": False,
        }
        resp = await self._client.post("/chat/completions", json=payload)
        resp.raise_for_status()
        data = resp.json()
        choice = data["choices"][0]
        content = choice["message"]["content"]
        return ChatResponse(content=content, model=data.get("model", req.model), usage=data.get("usage"))
