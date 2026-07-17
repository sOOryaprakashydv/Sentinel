from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ThreatIntelResultOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    provider: str
    status: str
    malware_family: str | None
    detections: int | None
    total_engines: int | None
    confidence: float | None
    tags_json: list
    error_message: str | None
    queried_at: datetime


class ThreatIntelSummaryOut(BaseModel):
    results: list[ThreatIntelResultOut]
    online: bool  # whether any provider is configured/reachable
