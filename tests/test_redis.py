import pytest
from app.rate_limiter.redis_token_bucket import RedisTokenBucket
from redis import Redis

@pytest.fixture
def redis_client():
    return Redis.from_url("redis://localhost:6379/0", decode_responses=True)

def test_token_bucket_allows_initial(redis_client):
    bucket = RedisTokenBucket(redis_client)
    key = "test:bucket"
    allowed, retry_ms = bucket.acquire(key, rate_per_sec=5, burst=10)
    assert allowed is True
    assert retry_ms == 0

def test_token_bucket_blocks_when_exceeded(redis_client):
    bucket = RedisTokenBucket(redis_client)
    key = "test:bucket_block"
    # Exhaust the burst
    for _ in range(10):
        allowed, _ = bucket.acquire(key, rate_per_sec=1, burst=10)
        assert allowed is True
    allowed, retry_ms = bucket.acquire(key, rate_per_sec=1, burst=10)
    assert allowed is False
    assert retry_ms > 0