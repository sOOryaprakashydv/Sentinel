from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UploadResponse(BaseModel):
    investigation_id: int
    status: str
    filename: str


class TimelineEventOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    stage: str
    status: str
    message: str | None = None
    timestamp: datetime


class InvestigationSummaryOut(BaseModel):
    """Lightweight row for list views (Dashboard recent uploads, etc.)."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    filename: str
    file_type: str | None
    size: int
    sha256: str
    status: str
    uploaded_at: datetime
    risk_severity: str | None = None
    risk_score: int | None = None


class InvestigationDetailOut(BaseModel):
    """Full detail for the Investigation screen (Section 41.6-41.7)."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    case_id: int | None
    filename: str
    size: int
    mime: str | None
    file_type: str | None
    sha256: str
    sha1: str
    md5: str
    status: str
    error_message: str | None
    uploaded_at: datetime
    completed_at: datetime | None
    timeline_events: list[TimelineEventOut] = []
