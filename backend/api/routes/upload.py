from fastapi import APIRouter, BackgroundTasks, Depends, File, UploadFile
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas import UploadResponse
from backend.services import run_pipeline, save_and_register_upload

router = APIRouter(tags=["upload"])


@router.post("/upload", response_model=UploadResponse)
def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    case_id: int | None = None,
    db: Session = Depends(get_db),
):
    investigation = save_and_register_upload(db, file, case_id=case_id)
    background_tasks.add_task(run_pipeline, investigation.id)
    return UploadResponse(investigation_id=investigation.id, status=investigation.status, filename=investigation.filename)
