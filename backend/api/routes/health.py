from fastapi import APIRouter

from backend.config import get_settings
from backend.schemas import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health_check():
    settings = get_settings()
    return HealthResponse(
        status="healthy",
        version=settings.APP_VERSION,
        threat_intel_configured=settings.threat_intel_configured,
        ai_configured=settings.ai_configured,
    )
