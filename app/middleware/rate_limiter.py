from __future__ import annotations

import time
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limiter_acquire: Callable[[str, int, int], tuple[bool, int]]):
        super().__init__(app)
        self.limiter_acquire = limiter_acquire

    async def dispatch(self, request: Request, call_next):
        tenant = request.headers.get("x-tenant-id", "public")
        route = request.url.path
        key = f"rl:{tenant}:{route}"

        allowed, retry_ms = self.limiter_acquire(key, settings.rl_rate, settings.rl_burst_size)
        if not allowed:
            return Response("Too Many Requests", status_code=429, headers={"Retry-After": str(max(1, retry_ms // 1000))})

        response = await call_next(request)
        return response
