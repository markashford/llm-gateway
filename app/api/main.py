from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional

from redis import Redis

from app.middleware.rate_limiter import RateLimitMiddleware
from app.rate_limiter.redis_token_bucket import RedisTokenBucket
from app.core.config import settings

from app.providers.interfaces import ChatMessage, ChatRequest
from app.providers.router import select_provider

app = FastAPI(title="LLM Gateway")


# Rate limiter
redis = Redis.from_url(settings.redis_url, decode_responses=True)
bucket = RedisTokenBucket(redis)
app.add_middleware(RateLimitMiddleware, limiter_acquire=bucket.acquire)


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/providers")
def list_providers() -> Dict[str, List[str]]:
    from app.providers.router import get_providers

    return {"providers": sorted(get_providers().keys())}


class LlmModel(BaseModel):
    role: str
    content: str


class LlmBody(BaseModel):
    provider: str = Field("groq", description="Provider key: groq, openai, anthropic, google")
    model: str = Field("llama-3.1-8b-instant", description="Model name")
    messages: List[LlmModel]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 25


@app.post("/chat")
async def chat(body: LlmBody) -> Dict[str, Any]:
    try:
        client = select_provider(body.provider)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    req = ChatRequest(
        model=body.model,
        messages=[ChatMessage(role=m.role, content=m.content) for m in body.messages],
        temperature=body.temperature,
        max_tokens=body.max_tokens,
    )
    resp = await client.chat(req)
    return {"content": resp.content, "model": resp.model, "usage": resp.usage}
