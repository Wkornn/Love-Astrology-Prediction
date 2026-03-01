# Keep Render Backend Alive (Free)

Render free tier spins down after 15 minutes of inactivity. Use these **free** services to keep it awake:

---

## Option 1: UptimeRobot (Recommended)
**Best for: Simple, reliable, no coding**

1. Go to https://uptimerobot.com
2. Sign up (free account = 50 monitors)
3. Click **"Add New Monitor"**
4. Configure:
   - **Monitor Type**: HTTP(s)
   - **Friendly Name**: Love Astrology Backend
   - **URL**: `https://your-backend.onrender.com/health`
   - **Monitoring Interval**: 5 minutes (free tier)
5. Save

✅ Your backend will be pinged every 5 minutes and stay awake!

---

## Option 2: Cron-job.org
**Best for: More frequent pings**

1. Go to https://cron-job.org
2. Sign up (free)
3. Create new cronjob:
   - **URL**: `https://your-backend.onrender.com/health`
   - **Schedule**: Every 10 minutes
4. Enable

---

## Option 3: GitHub Actions (Free)
**Best for: Full control, no external service**

Create `.github/workflows/keep-alive.yml`:

```yaml
name: Keep Backend Alive

on:
  schedule:
    - cron: '*/14 * * * *'  # Every 14 minutes
  workflow_dispatch:  # Manual trigger

jobs:
  ping:
    runs-on: ubuntu-latest
    steps:
      - name: Ping Backend
        run: |
          curl -f https://your-backend.onrender.com/health || exit 0
```

Commit and push. GitHub will ping your backend every 14 minutes for free.

---

## Option 4: Vercel Cron (Easiest)
**Best for: Already using Vercel**

Add to your frontend `vercel.json`:

```json
{
  "crons": [
    {
      "path": "/api/ping-backend",
      "schedule": "*/10 * * * *"
    }
  ]
}
```

Create `frontend/api/ping-backend.ts`:

```typescript
export default async function handler() {
  await fetch('https://your-backend.onrender.com/health');
  return new Response('OK', { status: 200 });
}
```

---

## Comparison

| Service | Interval | Setup | Reliability |
|---------|----------|-------|-------------|
| UptimeRobot | 5 min | 2 min | ⭐⭐⭐⭐⭐ |
| Cron-job.org | 1 min | 2 min | ⭐⭐⭐⭐ |
| GitHub Actions | 14 min | 5 min | ⭐⭐⭐⭐⭐ |
| Vercel Cron | 10 min | 5 min | ⭐⭐⭐⭐ |

---

## Recommendation

**Use UptimeRobot** - It's the simplest and most reliable. Takes 2 minutes to set up and you get email alerts if your backend goes down.

---

## Important Notes

- Render free tier has **750 hours/month** (31 days = 744 hours)
- Keeping it alive 24/7 uses all free hours
- If you run out, backend sleeps until next month
- Consider upgrading to Render paid ($7/month) for production use

---

## Alternative: Accept the Cold Start

If you don't want to use uptime monitors:

1. Add loading message to frontend:
   ```
   "Waking up backend... This may take 30 seconds on first request"
   ```

2. Increase frontend timeout:
   ```typescript
   axios.defaults.timeout = 60000; // 60 seconds
   ```

3. Show friendly message:
   ```
   "☕ Backend is waking up from sleep... Please wait"
   ```

This is the most honest approach and saves your free hours!
