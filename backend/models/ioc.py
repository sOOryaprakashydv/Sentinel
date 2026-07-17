from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.session import Base


class IOCType(str, enum.Enum):
    IPV4 = "ipv4"
    IPV6 = "ipv6"
    DOMAIN = "domain"
    URL = "url"
    EMAIL = "email"
    FILE_PATH = "file_path"
    REGISTRY_KEY = "registry_key"
    MUTEX = "mutex"
    HASH_MD5 = "hash_md5"
    HASH_SHA1 = "hash_sha1"
    HASH_SHA256 = "hash_sha256"
    USER_AGENT = "user_agent"
    CRYPTO_WALLET = "crypto_wallet"
    CVE = "cve"


class IOCStatus(str, enum.Enum):
    UNKNOWN = "unknown"
    BENIGN = "benign"
    SUSPICIOUS = "suspicious"
    MALICIOUS = "malicious"


class IOC(Base):
    __tablename__ = "iocs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    investigation_id: Mapped[int] = mapped_column(ForeignKey("investigations.id"))

    type: Mapped[str] = mapped_column(Enum(IOCType))
    value: Mapped[str] = mapped_column(String(2048))
    confidence: Mapped[float] = mapped_column(Float, default=0.5)   # 0.0 - 1.0
    source: Mapped[str] = mapped_column(String(64))                 # e.g. "static_analysis", "strings"
    evidence: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    status: Mapped[str] = mapped_column(Enum(IOCStatus), default=IOCStatus.UNKNOWN)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    investigation = relationship("Investigation", back_populates="iocs")
