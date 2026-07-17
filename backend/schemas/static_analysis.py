from datetime import datetime

from pydantic import BaseModel, ConfigDict


class StaticAnalysisOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    metadata_json: dict
    sections_json: list
    imports_json: list
    exports_json: list
    resources_json: list
    permissions_json: list
    certificate_json: dict | None
    security_findings_json: list
    entropy: float | None
    compiler: str | None
    is_packed: bool
    yara_matches_json: list
    created_at: datetime
