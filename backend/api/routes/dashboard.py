from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas import DashboardStatsOut
from backend.services import get_dashboard_stats

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/stats", response_model=DashboardStatsOut)
def dashboard_stats(db: Session = Depends(get_db)):
    return get_dashboard_stats(db)
