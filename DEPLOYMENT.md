# Deployment Information

## Public URL
https://day12-agent-deployment-production-4d78.up.railway.app

## Platform
Railway

## Test Commands

### Health Check
```bash
curl -i https://day12-agent-deployment-production-4d78.up.railway.app/health
```

Observed result:

- HTTP status: `200`
- Body:
  - `{"status":"ok","uptime_seconds":75.0,"timestamp":"2026-04-17T12:30:53.275073+00:00"}`

### API Test (with authentication)
```bash
curl -X POST https://day12-agent-deployment-production-4d78.up.railway.app/ask \
  -H "X-API-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test","question":"hello from railway"}'
```

Observed result:

- HTTP status: `200`
- Body:
  - `{"user_id":"test","question":"hello from railway","answer":"[Mock answer] You asked: hello from railway","history_items_before":0}`

## Environment Variables Set
- PORT
- REDIS_URL
- AGENT_API_KEY
- RATE_LIMIT_PER_MINUTE
- MONTHLY_BUDGET_USD
- LOG_LEVEL (optional)

## Screenshots
- [Deployment dashboard](screenshots/dashboard.png)
- [Service running](screenshots/running.png)
- [Test results](screenshots/test.png)
