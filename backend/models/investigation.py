"""
Case & Investigation models.

The PRD's ERD (Section 26.2) lists separate `Cases` and `Evidence` tables,
with every other table (StaticAnalysis, IOCs, ThreatIntel, ...) hanging off
`Evidence`. Since the REST API (Section 27) addresses everything via
`/investigations/{id}`, this scaffold merges `Evidence` into a single
`Investigation` entity that a `Case` can have many of. This keeps the API
and DB vocabulary aligned without losing any field from the PRD tables.
"""
from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.session import Base


class InvestigationStatus(str, enum.Enum):
    UPLOADED = "uploaded"
    ANALYZING = "analyzing"
    STATIC_ANALYSIS_DONE = "static_analysis_done"
    ENRICHING = "enriching"
    SCORING = "scoring"
    MAPPING_MITRE = "mapping_mitre"
    SUMMARIZING = "summarizing"
    COMPLETE = "complete"
    FAILED = "failed"


class Case(Base):
    __tablename__ = "cases"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    case_number: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    investigator: Mapped[str | None] = mapped_column(String(128), nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="open")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    investigations: Mapped[list["Investigation"]] = relationship(
        back_populates="case", cascade="all, delete-orphan"
    )


class Investigation(Base):
    """Represents one uploaded file and everything discovered about it.
    Combines the PRD's `Evidence` table with top-level investigation state."""

    __tablename__ = "investigations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    case_id: Mapped[int | None] = mapped_column(ForeignKey("cases.id"), nullable=True)

    filename: Mapped[str] = mapped_column(String(512))
    stored_path: Mapped[str] = mapped_column(String(1024))
    size: Mapped[int] = mapped_column(Integer)
    mime: Mapped[str | None] = mapped_column(String(128), nullable=True)
    file_type: Mapped[str | None] = mapped_column(String(64), nullable=True)  # e.g. PE32, APK, PDF

    sha256: Mapped[str] = mapped_column(String(64), index=True)
    sha1: Mapped[str] = mapped_column(String(40))
    md5: Mapped[str] = mapped_column(String(32))

    status: Mapped[str] = mapped_column(
        Enum(InvestigationStatus), default=InvestigationStatus.UPLOADED
    )
    error_message: Mapped[str | None] = mapped_column(String(2048), nullable=True)

    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    case: Mapped["Case | None"] = relationship(back_populates="investigations")
    static_analysis: Mapped["StaticAnalysis | None"] = relationship(
        back_populates="investigation", uselist=False, cascade="all, delete-orphan"
    )
    iocs: Mapped[list["IOC"]] = relationship(back_populates="investigation", cascade="all, delete-orphan")
    threat_intel_results: Mapped[list["ThreatIntelResult"]] = relationship(
        back_populates="investigation", cascade="all, delete-orphan"
    )
    risk_score: Mapped["RiskScore | None"] = relationship(
        back_populates="investigation", uselist=False, cascade="all, delete-orphan"
    )
    mitre_mappings: Mapped[list["MitreMapping"]] = relationship(
        back_populates="investigation", cascade="all, delete-orphan"
    )
    ai_summary: Mapped["AISummary | None"] = relationship(
        back_populates="investigation", uselist=False, cascade="all, delete-orphan"
    )
    reports: Mapped[list["Report"]] = relationship(back_populates="investigation", cascade="all, delete-orphan")
    timeline_events: Mapped[list["TimelineEvent"]] = relationship(
        back_populates="investigation", cascade="all, delete-orphan", order_by="TimelineEvent.timestamp"
    )


# Imported at the bottom to avoid circular imports while keeping relationship() string refs valid.
from backend.models.static_analysis import StaticAnalysis  # noqa: E402
from backend.models.ioc import IOC  # noqa: E402
from backend.models.threat_intel import ThreatIntelResult  # noqa: E402
from backend.models.risk import RiskScore  # noqa: E402
from backend.models.mitre import MitreMapping  # noqa: E402
from backend.models.ai_summary import AISummary  # noqa: E402
from backend.models.report import Report  # noqa: E402
from backend.models.timeline import TimelineEvent  # noqa: E402
