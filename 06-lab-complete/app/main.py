import json
import logging
import signal
import time
from contextlib import asynccontextmanager
from datetime import datetime, timezone

import redis
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.auth import verify_api_key
from app.config import settings
from app.cost_guard import check_budget
from app.rate_limiter import check_rate_limit
from utils.mock_llm import ask as llm_ask

logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format='{"time":"%(asctime)s","level":"%(levelname)s","message":"%(message)s"}',
)
logger = logging.getLogger(__name__)

redis_client = redis.from_url(settings.redis_url, decode_responses=True)
start_time = time.time()
is_ready = False
in_flight_requests = 0


class AskRequest(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=100)
    question: str = Field(..., min_length=1, max_length=2000)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    global is_ready
    logger.info(json.dumps({"event": "startup", "env": settings.environment}))
    is_ready = True
    yield
    is_ready = False
    logger.info(json.dumps({"event": "shutdown"}))


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/docs" if settings.environment != "production" else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "X-API-Key"],
)


@app.middleware("http")
async def middleware(request: Request, call_next):
    global in_flight_requests
    in_flight_requests += 1
    started = time.time()
    try:
        response: Response = await call_next(request)
    finally:
        in_flight_requests -= 1
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    logger.info(
        json.dumps(
            {
                "event": "request",
                "method": request.method,
                "path": request.url.path,
                "status": response.status_code,
                "duration_ms": round((time.time() - started) * 1000, 1),
            }
        )
    )
    return response


@app.get("/")
def root():
    return {"app": settings.app_name, "version": settings.app_version}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "uptime_seconds": round(time.time() - start_time, 1),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/ready")
def ready():
    if not is_ready:
        raise HTTPException(status_code=503, detail="Service not ready")
    try:
        redis_client.ping()
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Redis unavailable: {exc}") from exc
    return {"status": "ready"}


@app.post("/ask")
def ask_agent(
    body: AskRequest,
    _user: str = Depends(verify_api_key),
    _rate_limit: None = Depends(check_rate_limit),
    _budget: None = Depends(check_budget),
):
    history_key = f"history:{body.user_id}"
    prior_history = redis_client.lrange(history_key, 0, -1)
    answer = llm_ask(body.question)

    redis_client.rpush(history_key, json.dumps({"role": "user", "content": body.question}))
    redis_client.rpush(history_key, json.dumps({"role": "assistant", "content": answer}))
    redis_client.ltrim(history_key, -20, -1)
    redis_client.expire(history_key, 7 * 24 * 3600)

    return {
        "user_id": body.user_id,
        "question": body.question,
        "answer": answer,
        "history_items_before": len(prior_history),
    }


def _handle_sigterm(signum, _frame):
    logger.info(json.dumps({"event": "signal", "signal": signum}))


signal.signal(signal.SIGTERM, _handle_sigterm)


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        timeout_graceful_shutdown=30,
    )
