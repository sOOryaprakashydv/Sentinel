from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, JSON, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.session import Base


class RiskScore(Base):
    __tablename__ = "risk_scores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    investigation_id: Mapped[int] = mapped_column(ForeignKey("investigations.id"), unique=True)

    score: Mapped[int] = mapped_column(Integer)                 # 0-100, Section 21.3
    severity: Mapped[str] = mapped_column(String(16))           # Low/Medium/High/Critical
    confidence: Mapped[float] = mapped_column(Float)            # 0.0-1.0, Section 21.7
    reasons_json: Mapped[list] = mapped_column(JSON, default=list)  # explainability, Section 21.8

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    investigation = relationship("Investigation", back_populates="risk_score")
