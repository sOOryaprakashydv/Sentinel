from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.session import Base


class MitreMapping(Base):
    __tablename__ = "mitre_mappings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    investigation_id: Mapped[int] = mapped_column(ForeignKey("investigations.id"))

    technique_id: Mapped[str] = mapped_column(String(16))       # e.g. "T1027"
    technique_name: Mapped[str] = mapped_column(String(256))
    tactic: Mapped[str] = mapped_column(String(64))             # e.g. "Defense Evasion"
    description: Mapped[str] = mapped_column(String(1024))
    evidence: Mapped[str] = mapped_column(String(1024))
    confidence: Mapped[float] = mapped_column(Float)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    investigation = relationship("Investigation", back_populates="mitre_mappings")
