from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, JSON, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.session import Base


class ThreatIntelResult(Base):
    """One row per provider queried (VirusTotal, MalwareBazaar, ...).
    Section 20.12 requires normalization across providers into a common shape."""

    __tablename__ = "threat_intel_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    investigation_id: Mapped[int] = mapped_column(ForeignKey("investigations.id"))

    provider: Mapped[str] = mapped_column(String(64))          # "virustotal" | "malwarebazaar"
    status: Mapped[str] = mapped_column(String(32), default="not_configured")
    # status: "success" | "not_found" | "error" | "not_configured" | "rate_limited"

    malware_family: Mapped[str | None] = mapped_column(String(128), nullable=True)
    detections: Mapped[int | None] = mapped_column(Integer, nullable=True)
    total_engines: Mapped[int | None] = mapped_column(Integer, nullable=True)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    tags_json: Mapped[list] = mapped_column(JSON, default=list)
    raw_json: Mapped[dict] = mapped_column(JSON, default=dict)
    error_message: Mapped[str | None] = mapped_column(String(1024), nullable=True)

    queried_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    investigation = relationship("Investigation", back_populates="threat_intel_results")
