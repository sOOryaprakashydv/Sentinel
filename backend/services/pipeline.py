"""
Investigation Pipeline Service (Section 11).

Runs the full workflow for one investigation: static analysis -> IOC
extraction -> threat intelligence -> risk scoring -> MITRE mapping -> AI
summary. Every stage is wrapped so a failure in one (e.g. VirusTotal being
down) doesn't stop the rest of the pipeline, matching Section 20.8 /
Section 48 ("remains functional even if external APIs fail").

This runs in-process via FastAPI BackgroundTasks — no distributed worker
queue, per the demo's explicit Out-of-Scope list (Section 7).
"""
from __future__ import annotations

from sqlalchemy.orm import Session

from backend.ai import build_ai_summary
from backend.database import session_scope
from backend.ioc import extract_iocs
from backend.mitre import map_to_mitre
from backend.models import (
    AISummary, IOC, Investigation, InvestigationStatus, MitreMapping,
    RiskScore, StaticAnalysis, ThreatIntelResult, TimelineEvent,
)
from backend.risk_engine import calculate_risk
from backend.static_analysis import run_static_analysis
from backend.threat_intel import query_all_providers
from backend.utils.logger import get_logger

logger = get_logger(__name__)


def _log_event(db: Session, investigation_id: int, stage: str, status: str, message: str | None = None) -> None:
    db.add(TimelineEvent(investigation_id=investigation_id, stage=stage, status=status, message=message))
    db.flush()


def run_pipeline(investigation_id: int) -> None:
    """Entry point called as a background task right after upload."""
    with session_scope() as db:
        investigation = db.get(Investigation, investigation_id)
        if not investigation:
            logger.error("Investigation %s not found, aborting pipeline.", investigation_id)
            return

        try:
            _log_event(db, investigation_id, "pipeline", "started")
            _run_static_analysis_stage(db, investigation)
            iocs = _run_ioc_stage(db, investigation)
            ti_results = _run_threat_intel_stage(db, investigation)
            risk = _run_risk_stage(db, investigation, iocs, ti_results)
            mitre = _run_mitre_stage(db, investigation, iocs)
            _run_ai_stage(db, investigation, risk, mitre, ti_results, iocs)

            investigation.status = InvestigationStatus.COMPLETE
            from sqlalchemy import func
            investigation.completed_at = func.now()
            _log_event(db, investigation_id, "pipeline", "completed")

        except Exception as exc:
            logger.exception("Pipeline failed for investigation %s", investigation_id)
            investigation.status = InvestigationStatus.FAILED
            investigation.error_message = str(exc)
            _log_event(db, investigation_id, "pipeline", "failed", str(exc))


def _run_static_analysis_stage(db: Session, investigation: Investigation) -> dict:
    investigation.status = InvestigationStatus.ANALYZING
    _log_event(db, investigation.id, "static_analysis", "started")
    try:
        result = run_static_analysis(investigation.stored_path, investigation.filename)
        investigation.file_type = result.get("file_type")
        investigation.mime = result.get("mime")

        db.add(StaticAnalysis(
            investigation_id=investigation.id,
            metadata_json=result.get("metadata", {}),
            sections_json=result.get("sections", []),
            imports_json=result.get("imports", []),
            exports_json=result.get("exports", []),
            resources_json=result.get("resources", []),
            permissions_json=result.get("permissions", []),
            certificate_json=result.get("certificate"),
            security_findings_json=result.get("security_findings", []),
            entropy=result.get("entropy"),
            compiler=result.get("compiler"),
            is_packed=result.get("is_packed", False),
        ))
        investigation.status = InvestigationStatus.STATIC_ANALYSIS_DONE
        _log_event(db, investigation.id, "static_analysis", "completed")
        return result
    except Exception as exc:
        _log_event(db, investigation.id, "static_analysis", "failed", str(exc))
        return {}


def _run_ioc_stage(db: Session, investigation: Investigation) -> list[dict]:
    _log_event(db, investigation.id, "ioc_extraction", "started")
    try:
        static_analysis = investigation.static_analysis
        sa_dict = {"imports": static_analysis.imports_json} if static_analysis else {}
        iocs = extract_iocs(investigation.stored_path, sa_dict)
        for ioc in iocs:
            db.add(IOC(investigation_id=investigation.id, **ioc))
        _log_event(db, investigation.id, "ioc_extraction", "completed", f"{len(iocs)} indicator(s) found")
        return iocs
    except Exception as exc:
        _log_event(db, investigation.id, "ioc_extraction", "failed", str(exc))
        return []


def _run_threat_intel_stage(db: Session, investigation: Investigation) -> list[dict]:
    investigation.status = InvestigationStatus.ENRICHING
    _log_event(db, investigation.id, "threat_intelligence", "started")
    results_out: list[dict] = []
    try:
        results = query_all_providers(investigation.sha256)
        for r in results:
            db.add(ThreatIntelResult(
                investigation_id=investigation.id,
                provider=r.provider, status=r.status, malware_family=r.malware_family,
                detections=r.detections, total_engines=r.total_engines, confidence=r.confidence,
                tags_json=r.tags, raw_json=r.raw, error_message=r.error_message,
            ))
            results_out.append({
                "provider": r.provider, "status": r.status, "malware_family": r.malware_family,
                "detections": r.detections, "total_engines": r.total_engines, "reputation": r.reputation,
            })
        _log_event(db, investigation.id, "threat_intelligence", "completed")
    except Exception as exc:
        _log_event(db, investigation.id, "threat_intelligence", "failed", str(exc))
    return results_out


def _run_risk_stage(db: Session, investigation: Investigation, iocs: list[dict], ti_results: list[dict]) -> dict:
    investigation.status = InvestigationStatus.SCORING
    _log_event(db, investigation.id, "risk_scoring", "started")
    sa = investigation.static_analysis
    sa_dict = {
        "security_findings_json": sa.security_findings_json, "imports_json": sa.imports_json,
        "permissions_json": sa.permissions_json, "metadata_json": sa.metadata_json,
        "is_packed": sa.is_packed, "entropy": sa.entropy,
    } if sa else {}

    risk = calculate_risk(sa_dict, investigation.file_type, iocs, ti_results)
    db.add(RiskScore(
        investigation_id=investigation.id, score=risk["score"], severity=risk["severity"],
        confidence=risk["confidence"], reasons_json=risk["reasons"],
    ))
    _log_event(db, investigation.id, "risk_scoring", "completed", f'Score {risk["score"]} ({risk["severity"]})')
    return risk


def _run_mitre_stage(db: Session, investigation: Investigation, iocs: list[dict]) -> list[dict]:
    investigation.status = InvestigationStatus.MAPPING_MITRE
    _log_event(db, investigation.id, "mitre_mapping", "started")
    sa = investigation.static_analysis
    sa_dict = {
        "security_findings_json": sa.security_findings_json, "imports_json": sa.imports_json,
        "entropy": sa.entropy, "is_packed": sa.is_packed,
    } if sa else {}

    mappings = map_to_mitre(sa_dict, investigation.file_type, iocs)
    for m in mappings:
        db.add(MitreMapping(investigation_id=investigation.id, **m))
    _log_event(db, investigation.id, "mitre_mapping", "completed", f"{len(mappings)} technique(s) mapped")
    return mappings


def _run_ai_stage(
    db: Session, investigation: Investigation, risk: dict, mitre: list[dict],
    ti_results: list[dict], iocs: list[dict],
) -> None:
    investigation.status = InvestigationStatus.SUMMARIZING
    _log_event(db, investigation.id, "ai_summary", "started")

    family = next((r.get("malware_family") for r in ti_results if r.get("malware_family")), None)
    context = {
        "filename": investigation.filename,
        "sha256": investigation.sha256,
        "risk_score": risk["score"],
        "risk_confidence": risk["confidence"],
        "risk_reasons": risk["reasons"],
        "severity": risk["severity"],
        "malware_family": family,
        "threat_intelligence": ti_results,
        "iocs": iocs[:30],
        "mitre": mitre,
    }

    try:
        summary = build_ai_summary(context)
        db.add(AISummary(
            investigation_id=investigation.id,
            executive_summary=summary.get("executive_summary", ""),
            technical_summary=summary.get("technical_summary", ""),
            recommendations_json=summary.get("recommendations", []),
            confidence=summary.get("confidence", 0.5),
            source=summary.get("source", "unavailable"),
        ))
        _log_event(db, investigation.id, "ai_summary", "completed", f'source={summary.get("source")}')
    except Exception as exc:
        _log_event(db, investigation.id, "ai_summary", "failed", str(exc))
