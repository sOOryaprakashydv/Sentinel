from fastapi import Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Investigation
from backend.utils.exceptions import InvestigationNotFoundError


def get_investigation_or_404(investigation_id: int, db: Session = Depends(get_db)) -> Investigation:
    investigation = db.get(Investigation, investigation_id)
    if not investigation:
        raise InvestigationNotFoundError(f"Investigation {investigation_id} was not found.")
    return investigation
