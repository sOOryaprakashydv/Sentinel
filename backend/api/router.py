from fastapi import APIRouter

from backend.api.routes import cases, dashboard, health, investigations, reports, upload

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(upload.router)
api_router.include_router(investigations.router)
api_router.include_router(reports.router)
api_router.include_router(dashboard.router)
api_router.include_router(cases.router)
