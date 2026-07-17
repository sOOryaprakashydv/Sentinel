from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RiskScoreOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    score: int
    severity: str
    confidence: float
    reasons_json: list
    created_at: datetime
