"""Builds the single consolidated data structure every report format
(PDF/HTML/CSV/JSON) is rendered from, following the standardized report
structure in Section 25.4."""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from backend.models import Investigation


def build_report_data(db: Session, investigation: Investigation) -> dict:
    sa = investigation.static_analysis
    risk = investigation.risk_score
    ai = investigation.ai_summary

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "cover": {
            "title": "Sentinel Investigation Report",
            "case_number": investigation.case.case_number if investigation.case else None,
            "investigator": investigation.case.investigator if investigation.case else None,
        },
        "case_information": {
            "case_id": investigation.case_id,
            "investigation_id": investigation.id,
            "status": investigation.status,
        },
        "file_information": {
            "filename": investigation.filename,
            "size": investigation.size,
            "mime": investigation.mime,
            "file_type": investigation.file_type,
            "uploaded_at": investigation.uploaded_at.isoformat() if investigation.uploaded_at else None,
        },
        "hashes": {
            "sha256": investigation.sha256,
            "sha1": investigation.sha1,
            "md5": investigation.md5,
        },
        "static_analysis": {
            "metadata": sa.metadata_json if sa else {},
            "sections": sa.sections_json if sa else [],
            "imports": sa.imports_json if sa else [],
            "permissions": sa.permissions_json if sa else [],
            "certificate": sa.certificate_json if sa else None,
            "security_findings": sa.security_findings_json if sa else [],
            "entropy": sa.entropy if sa else None,
            "is_packed": sa.is_packed if sa else False,
        } if sa else None,
        "iocs": [
            {"type": i.type, "value": i.value, "confidence": i.confidence, "source": i.source, "status": i.status}
            for i in investigation.iocs
        ],
        "threat_intelligence": [
            {
                "provider": t.provider, "status": t.status, "malware_family": t.malware_family,
                "detections": t.detections, "total_engines": t.total_engines, "tags": t.tags_json,
            }
            for t in investigation.threat_intel_results
        ],
        "risk_assessment": {
            "score": risk.score, "severity": risk.severity, "confidence": risk.confidence,
            "reasons": risk.reasons_json,
        } if risk else None,
        "mitre_attack": [
            {
                "technique_id": m.technique_id, "technique_name": m.technique_name, "tactic": m.tactic,
                "description": m.description, "evidence": m.evidence, "confidence": m.confidence,
            }
            for m in investigation.mitre_mappings
        ],
        "ai_summary": {
            "executive_summary": ai.executive_summary, "technical_summary": ai.technical_summary,
            "recommendations": ai.recommendations_json, "confidence": ai.confidence, "source": ai.source,
        } if ai else None,
        "timeline": [
            {"stage": e.stage, "status": e.status, "message": e.message,
             "timestamp": e.timestamp.isoformat() if e.timestamp else None}
            for e in investigation.timeline_events
        ],
    }
