from pathlib import Path

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from backend.api.deps import get_investigation_or_404
from backend.config import get_settings
from backend.database import get_db
from backend.models import Investigation, Report
from backend.reports import build_report_data, generate_report
from backend.schemas import ReportGenerateRequest, ReportOut
from backend.utils.exceptions import InvestigationNotFoundError

router = APIRouter(prefix="/reports", tags=["reports"])

_MEDIA_TYPES = {
    "pdf": "application/pdf",
    "html": "text/html",
    "csv": "text/csv",
    "json": "application/json",
}


@router.post("/{investigation_id}/generate", response_model=ReportOut)
def generate_investigation_report(
    request: ReportGenerateRequest,
    investigation: Investigation = Depends(get_investigation_or_404),
    db: Session = Depends(get_db),
):
    settings = get_settings()
    data = build_report_data(db, investigation)
    path = generate_report(data, settings.REPORT_DIRECTORY, investigation.id, request.format)

    report = Report(investigation_id=investigation.id, format=request.format.lower(), location=path, status="generated")
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


@router.get("/{investigation_id}/download")
def download_latest_report(
    fmt: str = "pdf",
    investigation: Investigation = Depends(get_investigation_or_404),
    db: Session = Depends(get_db),
):
    matching = [r for r in investigation.reports if r.format == fmt.lower()]
    if not matching:
        raise InvestigationNotFoundError(f"No {fmt.upper()} report has been generated for this investigation yet.")

    latest = sorted(matching, key=lambda r: r.generated_at, reverse=True)[0]
    path = Path(latest.location)
    return FileResponse(
        path=path,
        media_type=_MEDIA_TYPES.get(fmt.lower(), "application/octet-stream"),
        filename=path.name,
    )


@router.get("", response_model=list[ReportOut])
def list_reports(db: Session = Depends(get_db)):
    return db.query(Report).order_by(Report.generated_at.desc()).all()
