from __future__ import annotations

from typing import Dict

from .groq_client import GroqClient
from .interfaces import LLMClient


def get_providers() -> Dict[str, LLMClient]:
    return {
        "groq": GroqClient(),
    }


def select_provider(name: str) -> LLMClient:
    providers = get_providers()
    key = name.lower()
    if key not in providers:
        raise ValueError(f"Unknown provider: {name}")
    return providers[key]
