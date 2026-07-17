"""Upload Service (Section 16). Validates, saves to disk, hashes, and
creates the initial Investigation row. The heavy pipeline work is kicked
off separately as a background task."""
from __future__ import annotations

import uuid
from pathlib import Path

from fastapi import UploadFile
from sqlalchemy.orm import Session

from backend.config import get_settings
from backend.models import Investigation, InvestigationStatus, TimelineEvent
from backend.utils.file_validator import validate_upload
from backend.utils.hashing import compute_hashes


def save_and_register_upload(db: Session, file: UploadFile, case_id: int | None = None) -> Investigation:
    settings = get_settings()

    raw = file.file.read()
    validate_upload(file.filename or "unknown", len(raw))

    stored_name = f"{uuid.uuid4().hex}_{Path(file.filename).name}"
    stored_path = Path(settings.UPLOAD_DIRECTORY) / stored_name
    stored_path.parent.mkdir(parents=True, exist_ok=True)
    stored_path.write_bytes(raw)

    hashes = compute_hashes(stored_path)

    investigation = Investigation(
        case_id=case_id,
        filename=file.filename or "unknown",
        stored_path=str(stored_path),
        size=len(raw),
        mime=file.content_type,
        sha256=hashes["sha256"],
        sha1=hashes["sha1"],
        md5=hashes["md5"],
        status=InvestigationStatus.UPLOADED,
    )
    db.add(investigation)
    db.flush()

    db.add(TimelineEvent(investigation_id=investigation.id, stage="upload", status="completed",
                          message=f"{investigation.filename} ({investigation.size} bytes)"))
    db.commit()
    db.refresh(investigation)
    return investigation
