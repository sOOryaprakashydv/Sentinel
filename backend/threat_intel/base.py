"""
Threat Intelligence provider interface (Section 20.11).

Every provider (VirusTotal, MalwareBazaar, and future ones like ThreatFox,
AlienVault OTX, URLhaus, AbuseIPDB) implements this same interface so the
orchestrator and normalization layer never depend on provider specifics.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ThreatResult:
    """Normalized shape every provider response is converted into
    (Section 20.12)."""
    provider: str
    status: str  # "success" | "not_found" | "error" | "not_configured" | "rate_limited"
    indicator: str
    indicator_type: str  # "sha256" | "domain" | "ip" | "url"
    reputation: str | None = None  # "malicious" | "suspicious" | "harmless" | "unknown"
    confidence: float | None = None
    malware_family: str | None = None
    detections: int | None = None
    total_engines: int | None = None
    tags: list[str] = field(default_factory=list)
    first_seen: str | None = None
    last_seen: str | None = None
    error_message: str | None = None
    raw: dict[str, Any] = field(default_factory=dict)


class ThreatIntelProvider(ABC):
    name: str

    @property
    @abstractmethod
    def is_configured(self) -> bool:
        ...

    @abstractmethod
    def lookup_hash(self, sha256: str) -> ThreatResult:
        ...

    def lookup_ip(self, ip: str) -> ThreatResult:
        return ThreatResult(provider=self.name, status="not_found", indicator=ip, indicator_type="ip")

    def lookup_domain(self, domain: str) -> ThreatResult:
        return ThreatResult(provider=self.name, status="not_found", indicator=domain, indicator_type="domain")

    def lookup_url(self, url: str) -> ThreatResult:
        return ThreatResult(provider=self.name, status="not_found", indicator=url, indicator_type="url")

    def _not_configured(self, indicator: str, indicator_type: str) -> ThreatResult:
        return ThreatResult(
            provider=self.name, status="not_configured", indicator=indicator, indicator_type=indicator_type,
            error_message=f"{self.name} API key is not configured.",
        )
