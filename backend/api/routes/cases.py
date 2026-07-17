from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Case

router = APIRouter(prefix="/cases", tags=["cases"])


class CaseCreate(BaseModel):
    case_number: str
    investigator: str | None = None


class CaseOut(BaseModel):
    id: int
    case_number: str
    investigator: str | None
    status: str

    class Config:
        from_attributes = True


@router.post("", response_model=CaseOut)
def create_case(payload: CaseCreate, db: Session = Depends(get_db)):
    case = Case(case_number=payload.case_number, investigator=payload.investigator)
    db.add(case)
    db.commit()
    db.refresh(case)
    return case


@router.get("", response_model=list[CaseOut])
def list_cases(db: Session = Depends(get_db)):
    return db.scalars(select(Case).order_by(Case.created_at.desc())).all()
