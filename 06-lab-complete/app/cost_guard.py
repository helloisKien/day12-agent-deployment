from datetime import datetime

import redis
from fastapi import Header, HTTPException

from app.config import settings

redis_client = redis.from_url(settings.redis_url, decode_responses=True)


def check_budget(x_api_key: str = Header(default=None)) -> None:
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing X-API-Key header")

    # Mock cost estimate for each request in this lab.
    estimated_cost = 0.01
    month_key = datetime.utcnow().strftime("%Y-%m")
    key = f"budget:{x_api_key}:{month_key}"

    current = float(redis_client.get(key) or 0.0)
    if current + estimated_cost > settings.monthly_budget_usd:
        raise HTTPException(
            status_code=402,
            detail=f"Monthly budget exceeded (${settings.monthly_budget_usd})",
        )

    redis_client.incrbyfloat(key, estimated_cost)
    redis_client.expire(key, 32 * 24 * 3600)
