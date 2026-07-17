"""
Sentinel FastAPI application entry point.

Run with:  uvicorn backend.main:app --reload --port 8000

In production (see Dockerfile), this also serves the built React frontend
(frontend/dist) as static files, so the whole app — API + UI — is a single
deployable service with no separate frontend host and no cross-origin setup.
"""
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from backend.api import api_router
from backend.config import ensure_runtime_directories, get_settings
from backend.database import init_db
from backend.utils.exceptions import SentinelError
from backend.utils.logger import configure_logging, get_logger

settings = get_settings()
configure_logging()
logger = get_logger(__name__)

FRONTEND_DIST = Path(__file__).resolve().parent.parent / "frontend" / "dist"

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-assisted malware investigation platform for police cyber crime units.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(SentinelError)
async def sentinel_error_handler(request: Request, exc: SentinelError):
    # Standardized error envelope (Section 28) — never leak stack traces to the frontend.
    logger.warning("Handled error [%s]: %s", exc.code, exc.message)
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "error": exc.message, "code": exc.code},
    )


@app.on_event("startup")
def on_startup():
    ensure_runtime_directories()
    init_db()
    logger.info("Sentinel backend started (%s)", settings.APP_VERSION)
    if not settings.threat_intel_configured:
        logger.warning("No threat intelligence API keys configured — running in degraded mode.")
    if not settings.ai_configured:
        logger.warning("GEMINI_API_KEY not configured — AI summaries will use the rule-based fallback.")
    if FRONTEND_DIST.exists():
        logger.info("Serving built frontend from %s", FRONTEND_DIST)
    else:
        logger.info("No frontend build found at %s — API-only mode (run `npm run build` to enable it).", FRONTEND_DIST)


app.include_router(api_router, prefix=settings.API_V1_PREFIX)


if FRONTEND_DIST.exists():
    # Vite's hashed JS/CSS bundles live under /assets — served directly.
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST / "assets"), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        """SPA catch-all: any non-API, non-asset path returns index.html so
        client-side routing (React Router) works on hard refresh / deep links."""
        if full_path.startswith(settings.API_V1_PREFIX.lstrip("/")) or full_path in ("docs", "openapi.json", "redoc"):
            raise HTTPException(status_code=404)
        candidate = FRONTEND_DIST / full_path
        if full_path and candidate.is_file():
            return FileResponse(candidate)
        return FileResponse(FRONTEND_DIST / "index.html")

else:
    @app.get("/")
    def root():
        return {"application": settings.APP_NAME, "version": settings.APP_VERSION, "docs": "/docs"}

