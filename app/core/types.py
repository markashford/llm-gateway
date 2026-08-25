from typing import Optional
from pydantic import BaseModel


class LLMRequest(BaseModel):
    prompt: str
    max_tokens: int = 25
    temperature: float = 0.7
    provider: Optional[str] = None


class LLMResponse(BaseModel):
    text: str
    provider: str
