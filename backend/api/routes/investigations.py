from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.api.deps import get_investigation_or_404
from backend.database import get_db
from backend.models import Investigation
from backend.schemas import (
    AISummaryOut, InvestigationDetailOut, InvestigationSummaryOut,
    IOCListOut, MitreMappingListOut, RiskScoreOut, StaticAnalysisOut,
    ThreatIntelSummaryOut,
)
from backend.threat_intel import any_provider_configured
from backend.utils.exceptions import AnalysisNotReadyError

router = APIRouter(prefix="/investigations", tags=["investigations"])


@router.get("", response_model=list[InvestigationSummaryOut])
def list_investigations(db: Session = Depends(get_db)):
    investigations = db.scalars(select(Investigation).order_by(Investigation.uploaded_at.desc())).all()
    out = []
    for inv in investigations:
        out.append(InvestigationSummaryOut(
            id=inv.id, filename=inv.filename, file_type=inv.file_type, size=inv.size,
            sha256=inv.sha256, status=inv.status, uploaded_at=inv.uploaded_at,
            risk_severity=inv.risk_score.severity if inv.risk_score else None,
            risk_score=inv.risk_score.score if inv.risk_score else None,
        ))
    return out


@router.get("/{investigation_id}", response_model=InvestigationDetailOut)
def get_investigation(investigation: Investigation = Depends(get_investigation_or_404)):
    return investigation


@router.get("/{investigation_id}/static", response_model=StaticAnalysisOut)
def get_static_analysis(investigation: Investigation = Depends(get_investigation_or_404)):
    if not investigation.static_analysis:
        raise AnalysisNotReadyError("Static analysis has not completed yet.")
    return investigation.static_analysis


@router.get("/{investigation_id}/iocs", response_model=IOCListOut)
def get_iocs(investigation: Investigation = Depends(get_investigation_or_404)):
    return IOCListOut(total=len(investigation.iocs), items=investigation.iocs)


@router.get("/{investigation_id}/threat-intelligence", response_model=ThreatIntelSummaryOut)
def get_threat_intelligence(investigation: Investigation = Depends(get_investigation_or_404)):
    return ThreatIntelSummaryOut(results=investigation.threat_intel_results, online=any_provider_configured())


@router.get("/{investigation_id}/risk", response_model=RiskScoreOut)
def get_risk_score(investigation: Investigation = Depends(get_investigation_or_404)):
    if not investigation.risk_score:
        raise AnalysisNotReadyError("Risk score has not been calculated yet.")
    return investigation.risk_score


@router.get("/{investigation_id}/mitre", response_model=MitreMappingListOut)
def get_mitre_mappings(investigation: Investigation = Depends(get_investigation_or_404)):
    return MitreMappingListOut(total=len(investigation.mitre_mappings), items=investigation.mitre_mappings)


@router.get("/{investigation_id}/summary", response_model=AISummaryOut)
def get_ai_summary(investigation: Investigation = Depends(get_investigation_or_404)):
    if not investigation.ai_summary:
        raise AnalysisNotReadyError("AI summary has not been generated yet.")
    return investigation.ai_summary
