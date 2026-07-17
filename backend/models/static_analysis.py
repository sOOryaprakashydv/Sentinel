from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, JSON, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.session import Base


class StaticAnalysis(Base):
    """Static analysis findings (Section 18 & 26.5).

    JSON columns hold structured sub-sections so the analyzer modules
    (pefile / androguard / oletools / PyPDF2 / LIEF output) can be stored
    as-is without a rigid relational schema per file type.
    """

    __tablename__ = "static_analysis"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    investigation_id: Mapped[int] = mapped_column(ForeignKey("investigations.id"), unique=True)

    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)      # compiler, timestamps, arch, etc.
    sections_json: Mapped[list] = mapped_column(JSON, default=list)      # PE/ELF sections
    imports_json: Mapped[list] = mapped_column(JSON, default=list)       # imported functions/libraries
    exports_json: Mapped[list] = mapped_column(JSON, default=list)
    resources_json: Mapped[list] = mapped_column(JSON, default=list)
    permissions_json: Mapped[list] = mapped_column(JSON, default=list)   # APK permissions
    certificate_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    security_findings_json: Mapped[list] = mapped_column(JSON, default=list)  # each with a severity

    entropy: Mapped[float | None] = mapped_column(Float, nullable=True)
    compiler: Mapped[str | None] = mapped_column(String(128), nullable=True)
    is_packed: Mapped[bool] = mapped_column(default=False)

    yara_matches_json: Mapped[list] = mapped_column(JSON, default=list)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    investigation = relationship("Investigation", back_populates="static_analysis")
