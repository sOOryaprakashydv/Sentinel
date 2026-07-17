"""Dashboard stats aggregation (Section 15.4)."""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.models import Investigation, Report, RiskScore
from backend.threat_intel import any_provider_configured
from backend.config import get_settings


def get_dashboard_stats(db: Session) -> dict:
    settings = get_settings()
    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)

    total_investigations = db.scalar(select(func.count(Investigation.id))) or 0
    files_today = db.scalar(
        select(func.count(Investigation.id)).where(Investigation.uploaded_at >= today_start)
    ) or 0
    high_risk = db.scalar(
        select(func.count(RiskScore.id)).where(RiskScore.severity.in_(["High", "Critical"]))
    ) or 0
    critical = db.scalar(
        select(func.count(RiskScore.id)).where(RiskScore.severity == "Critical")
    ) or 0
    reports_generated = db.scalar(select(func.count(Report.id))) or 0

    recent = db.scalars(
        select(Investigation).order_by(Investigation.uploaded_at.desc()).limit(10)
    ).all()

    recent_out = []
    for inv in recent:
        recent_out.append({
            "id": inv.id, "filename": inv.filename, "file_type": inv.file_type, "size": inv.size,
            "sha256": inv.sha256, "status": inv.status, "uploaded_at": inv.uploaded_at,
            "risk_severity": inv.risk_score.severity if inv.risk_score else None,
            "risk_score": inv.risk_score.score if inv.risk_score else None,
        })

    return {
        "total_investigations": total_investigations,
        "files_uploaded_today": files_today,
        "high_risk_samples": high_risk,
        "critical_alerts": critical,
        "reports_generated": reports_generated,
        "threat_intelligence_online": any_provider_configured(),
        "ai_online": settings.ai_configured,
        "recent_uploads": recent_out,
    }
