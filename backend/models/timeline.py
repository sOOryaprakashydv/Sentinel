from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.session import Base


class TimelineEvent(Base):
    """Chronological pipeline events shown on the Investigation Timeline
    card (Section 24) and used as the audit trail (Section 43)."""

    __tablename__ = "timeline_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    investigation_id: Mapped[int] = mapped_column(ForeignKey("investigations.id"))

    stage: Mapped[str] = mapped_column(String(64))        # e.g. "static_analysis"
    status: Mapped[str] = mapped_column(String(16))       # "started" | "completed" | "failed" | "skipped"
    message: Mapped[str | None] = mapped_column(String(1024), nullable=True)

    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    investigation = relationship("Investigation", back_populates="timeline_events")
