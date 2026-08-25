from __future__ import annotations

import time
from typing import Tuple

from redis import Redis


TOKEN_BUCKET_LUA = """
-- KEYS[1] = bucket key
-- ARGV[1] = now_ms
-- ARGV[2] = refill_rate_per_sec
-- ARGV[3] = burst_capacity

local key = KEYS[1]
local now_ms = tonumber(ARGV[1])
local rate = tonumber(ARGV[2])
local burst = tonumber(ARGV[3])

local bucket = redis.call('HMGET', key, 'tokens', 'ts')
local tokens = tonumber(bucket[1])
local ts = tonumber(bucket[2])

if tokens == nil then
  tokens = burst
  ts = now_ms
else
  local elapsed_ms = math.max(0, now_ms - ts)
  local refill = (elapsed_ms / 1000.0) * rate
  tokens = math.min(burst, tokens + refill)
  ts = now_ms
end

local allowed = 0
local retry_after_ms = 0
if tokens >= 1.0 then
  tokens = tokens - 1.0
  allowed = 1
else
  local need = 1.0 - tokens
  retry_after_ms = math.ceil((need / rate) * 1000.0)
end

redis.call('HMSET', key, 'tokens', tokens, 'ts', ts)
redis.call('PEXPIRE', key, math.ceil((burst / rate) * 2000))

return {allowed, retry_after_ms}
"""


class RedisTokenBucket:
    def __init__(self, redis: Redis):
        self.redis = redis
        self._sha = self.redis.script_load(TOKEN_BUCKET_LUA)

    def acquire(self, key: str, rate_per_sec: int, burst: int) -> Tuple[bool, int]:
        now_ms = int(time.time() * 1000)
        try:
            allowed, retry_ms = self.redis.evalsha(self._sha, 1, key, now_ms, rate_per_sec, burst)
            return bool(allowed == 1), int(retry_ms)
        except Exception:
            res = self.redis.eval(TOKEN_BUCKET_LUA, 1, key, now_ms, rate_per_sec, burst)
            allowed, retry_ms = res[1], res[2]
            return bool(allowed == 1), int(retry_ms)
