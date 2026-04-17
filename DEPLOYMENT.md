# Deployment Information

## Public URL
[TO_FILL_PUBLIC_URL]

## Platform
Railway / Render

## Test Commands

### Health Check
```bash
curl https://your-agent-domain/health
```

Expected: status 200 with JSON status payload.

### API Test (with authentication)
```bash
curl -X POST https://your-agent-domain/ask \
  -H "X-API-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test","question":"Hello"}'
```

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
