import time

import redis
from fastapi import Header, HTTPException

from app.config import settings

redis_client = redis.from_url(settings.redis_url, decode_responses=True)


def check_rate_limit(x_api_key: str = Header(default=None)) -> None:
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing X-API-Key header")

    key = f"rate:{x_api_key}"
    now = time.time()
    window_seconds = 60

    redis_client.zremrangebyscore(key, 0, now - window_seconds)
    current = redis_client.zcard(key)
    if current >= settings.rate_limit_per_minute:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded ({settings.rate_limit_per_minute} req/min)",
        )

    request_member = f"{now}:{current}"
    redis_client.zadd(key, {request_member: now})
    redis_client.expire(key, window_seconds)
