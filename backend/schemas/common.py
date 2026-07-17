from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Standardized error envelope (Section 28)."""
    success: bool = False
    error: str
    code: str


class HealthResponse(BaseModel):
    status: str
    version: str
    threat_intel_configured: bool
    ai_configured: bool
