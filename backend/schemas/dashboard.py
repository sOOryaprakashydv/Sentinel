from backend.schemas.investigation import InvestigationSummaryOut
from pydantic import BaseModel


class DashboardStatsOut(BaseModel):
    total_investigations: int
    files_uploaded_today: int
    high_risk_samples: int
    critical_alerts: int
    reports_generated: int
    threat_intelligence_online: bool
    ai_online: bool
    recent_uploads: list[InvestigationSummaryOut]
