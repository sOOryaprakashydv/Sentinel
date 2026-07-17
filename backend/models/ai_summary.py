from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, JSON, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.session import Base


class AISummary(Base):
    __tablename__ = "ai_summaries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    investigation_id: Mapped[int] = mapped_column(ForeignKey("investigations.id"), unique=True)

    executive_summary: Mapped[str] = mapped_column(String(4096))
    technical_summary: Mapped[str] = mapped_column(String(8192))
    recommendations_json: Mapped[list] = mapped_column(JSON, default=list)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)

    source: Mapped[str] = mapped_column(String(32), default="unavailable")
    # source: "gemini" | "rule_based_fallback" | "unavailable"

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    investigation = relationship("Investigation", back_populates="ai_summary")
