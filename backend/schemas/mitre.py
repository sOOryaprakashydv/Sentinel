from pydantic import BaseModel, ConfigDict


class MitreMappingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    technique_id: str
    technique_name: str
    tactic: str
    description: str
    evidence: str
    confidence: float


class MitreMappingListOut(BaseModel):
    total: int
    items: list[MitreMappingOut]
