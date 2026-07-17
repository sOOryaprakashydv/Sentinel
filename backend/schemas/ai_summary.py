from pydantic import BaseModel, ConfigDict


class AISummaryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    executive_summary: str
    technical_summary: str
    recommendations_json: list
    confidence: float
    source: str
