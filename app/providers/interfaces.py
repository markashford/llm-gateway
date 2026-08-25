from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class ChatMessage:
    role: str
    content: str


@dataclass
class ChatRequest:
    model: str
    messages: List[ChatMessage]
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None


@dataclass
class ChatResponse:
    content: str
    model: str
    usage: Dict[str, Any] | None = None


class LLMClient:
    async def chat(self, req: ChatRequest) -> ChatResponse:  # pragma: no cover - interface
        raise NotImplementedError

