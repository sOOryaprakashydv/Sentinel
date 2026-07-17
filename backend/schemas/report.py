from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ReportGenerateRequest(BaseModel):
    format: str  # "pdf" | "html" | "csv" | "json"


class ReportOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    investigation_id: int
    format: str
    status: str
    generated_at: datetime
