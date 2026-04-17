# Day 12 Lab - Mission Answers

## Part 1: Localhost vs Production

### Exercise 1.1: Anti-patterns found
1. Hardcoded secrets in source code.
2. Fixed host/port values instead of environment variables.
3. Debug/reload mode enabled by default.
4. Missing health/readiness probes.
5. No graceful shutdown handling.

### Exercise 1.3: Comparison table
| Feature | Develop | Production | Why Important? |
|---------|---------|------------|----------------|
| Config | Hardcoded | Environment variables | Works across local/cloud and avoids code changes per env |
| Secrets | In code | In env / platform secret store | Prevents key leakage in git history |
| Health check | Missing | `/health` + `/ready` | Lets platform monitor and restart safely |
| Logging | print | Structured logs | Easier troubleshooting in deployment logs |
| Shutdown | Abrupt stop | Graceful SIGTERM handling | Reduces dropped requests during deploy/restart |

## Part 2: Docker

### Exercise 2.1: Dockerfile questions
1. Base image: `python:3.11-slim`.
2. Working directory: `/app` (runtime stage).
3. Copy `requirements.txt` first: to maximize Docker layer cache.
4. `CMD` vs `ENTRYPOINT`: `CMD` provides default command and can be overridden more easily.

### Exercise 2.3: Image size comparison
- Develop: [PENDING_MEASURE]
- Production: [PENDING_MEASURE]
- Difference: [PENDING_MEASURE]

## Part 3: Cloud Deployment

### Exercise 3.1: Railway deployment
- URL: [TO_FILL_PUBLIC_URL]
- Screenshot: [TO_FILL_SCREENSHOT_PATH]

## Part 4: API Security

### Exercise 4.1-4.3: Test results
- Without API key:
  - `POST /ask` returned `401` with detail `Missing X-API-Key header`.
- With valid API key:
  - `POST /ask` returned `200` with response:
    - `{"user_id":"test","question":"hello","answer":"[Mock answer] You asked: hello","history_items_before":0}`
- Rate limiting:
  - Sent 15 requests in a burst with same API key.
  - First 10 requests returned `200`.
  - Next 5 requests returned `429`.

### Exercise 4.4: Cost guard implementation
Implemented monthly budget check in Redis by API key and month key (`budget:<api_key>:YYYY-MM`).
Request is blocked with HTTP 402 when projected spending exceeds configured monthly budget.

## Part 5: Scaling & Reliability

### Exercise 5.1-5.5: Implementation notes
- Added `/health` (liveness) and `/ready` (readiness + Redis ping).
- Added signal handler for graceful shutdown behavior.
- Kept conversation history in Redis (`history:<user_id>`) to stay stateless across instances.
- Added Redis-backed rate limiting and monthly budget cost guard.
- Validated Dockerized runtime with app + Redis compose stack.
