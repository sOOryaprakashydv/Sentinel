# Deploying Sentinel

The whole app — FastAPI backend + React frontend — ships as **one Docker image**: the
frontend is built and served directly by the backend, so there's one service to deploy,
no CORS setup, and no keeping two hosts in sync.

## Recommended: Render (free tier, easiest)

1. Push this project to a GitHub (or GitLab) repo.
2. Go to [render.com](https://render.com) → **New** → **Blueprint** → connect the repo.
   Render finds `render.yaml` in the repo root automatically and configures everything.
   (No Blueprint? Use **New → Web Service → Docker** instead, point it at the repo, and
   it'll pick up the `Dockerfile` — same result, just click-through instead of automatic.)
3. Click **Apply** / **Create Web Service**. Render builds the Docker image and deploys it —
   takes a few minutes the first time.
4. Once it's live, your app is at `https://<your-service-name>.onrender.com`.
5. Optional — add API keys: in the service's **Environment** tab, add `VT_API_KEY`,
   `MALWAREBAZAAR_API_KEY`, and/or `GEMINI_API_KEY`. Without them the app runs in
   degraded mode automatically (Settings page shows what's active).

**Free tier caveats** (worth knowing, not blockers for a demo):
- The service spins down after ~15 min idle and takes ~30-60s to wake up on the next request.
- The filesystem is ephemeral — uploaded files, generated reports, and the SQLite database
  reset on every deploy or restart. Fine for demoing the workflow; not for a persistent case
  archive. See the note at the bottom of `render.yaml` for how to add durable storage
  (a paid Disk, or swap SQLite for Render's free managed Postgres) when you're ready for that.

## Same Dockerfile also works on

- **Railway** — New Project → Deploy from GitHub repo → it auto-detects the `Dockerfile`.
- **Fly.io** — `fly launch` in the project root detects the `Dockerfile`; `fly deploy` ships it.
- **Any VPS** — see below.

## Your own VPS (Docker)

```bash
git clone <your-repo-url> sentinel && cd sentinel
cp .env.example .env          # fill in API keys if you have them — optional
docker build -t sentinel .
docker run -d --name sentinel \
  -p 80:8000 \
  --env-file .env \
  -v sentinel_uploads:/app/uploads \
  -v sentinel_reports:/app/reports \
  -v sentinel_db:/app/data \
  -e DATABASE_URL=sqlite:////app/data/sentinel.db \
  sentinel
```

The three `-v` volumes make uploads, reports, and the database persist across container
restarts (unlike the free-tier cloud path above). Put a reverse proxy (Caddy or nginx) in
front for HTTPS if this is reachable from the internet — Caddy is the least fuss:

```bash
# Caddyfile
your-domain.com {
    reverse_proxy localhost:80
}
```

## Building/running without Docker at all

Still works exactly as in the main README — `uvicorn backend.main:app` for the API,
`npm run dev` for the frontend with hot reload. The Docker path above is specifically
for turning it into one deployable production build; local development doesn't need it.

## Verifying a deploy

Hit `/api/v1/health` — it should return `{"status": "healthy", ...}` and tells you whether
threat intel / AI keys were picked up. The homepage should load the full dashboard, not a
bare JSON response (if you see JSON at `/`, the frontend build didn't get copied into the
image — check the Docker build logs for the `npm run build` step).
