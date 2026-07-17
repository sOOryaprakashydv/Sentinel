from datetime import datetime

from pydantic import BaseModel, ConfigDict


class IOCOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    type: str
    value: str
    confidence: float
    source: str
    evidence: str | None
    status: str
    created_at: datetime


class IOCListOut(BaseModel):
    total: int
    items: list[IOCOut]
