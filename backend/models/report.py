from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.session import Base


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    investigation_id: Mapped[int] = mapped_column(ForeignKey("investigations.id"))

    format: Mapped[str] = mapped_column(String(8))       # pdf | html | csv | json
    location: Mapped[str] = mapped_column(String(1024))  # path on disk
    status: Mapped[str] = mapped_column(String(16), default="generated")

    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    investigation = relationship("Investigation", back_populates="reports")
