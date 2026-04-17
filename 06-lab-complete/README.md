# Day 12 - Lab Complete

Base implementation for Day 12 final submission.

## Implemented Requirements

- Multi-stage Dockerfile
- API key authentication
- Rate limiting (default `10 req/min`)
- Cost guard (default `$10/month` per API key)
- Health (`/health`) and readiness (`/ready`) endpoints
- Graceful shutdown signal handling
- Stateless conversation history with Redis
- Config from environment variables

## Project Structure

```text
06-lab-complete/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── auth.py
│   ├── rate_limiter.py
│   └── cost_guard.py
├── utils/
│   └── mock_llm.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .dockerignore
├── railway.toml
└── render.yaml
```

## Run Locally (PowerShell)

```powershell
Copy-Item .env.example .env
docker compose up --build
```

In another terminal:

```powershell
curl http://localhost:8000/health
curl http://localhost:8000/ready
curl -X POST http://localhost:8000/ask `
  -H "X-API-Key: dev-key-change-me-in-production" `
  -H "Content-Type: application/json" `
  -d '{"user_id":"test","question":"Hello"}'
```

## Deploy

- Railway: use `railway.toml`
- Render: use `render.yaml`

Set these env vars on cloud:

- `PORT`
- `REDIS_URL`
- `AGENT_API_KEY`
- `RATE_LIMIT_PER_MINUTE`
- `MONTHLY_BUDGET_USD`
- `LOG_LEVEL` (optional)

## Validation

```powershell
python .\check_production_ready.py
```
