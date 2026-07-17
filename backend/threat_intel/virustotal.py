"""VirusTotal provider (Section 20.6-20.8). Public API v3.
Degrades to status='not_configured' with no crash when VT_API_KEY is unset,
and to status='error'/'rate_limited' on network failures, per Section 20.8:
"No other module shall fail because VirusTotal is unavailable." """
from __future__ import annotations

import requests

from backend.config import get_settings
from backend.threat_intel.base import ThreatIntelProvider, ThreatResult
from backend.utils.logger import get_logger

logger = get_logger(__name__)

_BASE_URL = "https://www.virustotal.com/api/v3"


class VirusTotalProvider(ThreatIntelProvider):
    name = "virustotal"

    def __init__(self):
        self.settings = get_settings()

    @property
    def is_configured(self) -> bool:
        return bool(self.settings.VT_API_KEY)

    def _headers(self) -> dict:
        return {"x-apikey": self.settings.VT_API_KEY}

    def lookup_hash(self, sha256: str) -> ThreatResult:
        if not self.is_configured:
            return self._not_configured(sha256, "sha256")

        try:
            resp = requests.get(
                f"{_BASE_URL}/files/{sha256}",
                headers=self._headers(),
                timeout=self.settings.TI_REQUEST_TIMEOUT_SECONDS,
            )
        except requests.RequestException as exc:
            logger.warning("VirusTotal request failed: %s", exc)
            return ThreatResult(
                provider=self.name, status="error", indicator=sha256, indicator_type="sha256",
                error_message=f"VirusTotal is unavailable: {exc}",
            )

        if resp.status_code == 404:
            return ThreatResult(provider=self.name, status="not_found", indicator=sha256, indicator_type="sha256")
        if resp.status_code == 429:
            return ThreatResult(
                provider=self.name, status="rate_limited", indicator=sha256, indicator_type="sha256",
                error_message="VirusTotal quota exceeded.",
            )
        if resp.status_code != 200:
            return ThreatResult(
                provider=self.name, status="error", indicator=sha256, indicator_type="sha256",
                error_message=f"VirusTotal returned HTTP {resp.status_code}.",
            )

        return self._normalize(resp.json(), sha256)

    def _normalize(self, payload: dict, sha256: str) -> ThreatResult:
        attrs = payload.get("data", {}).get("attributes", {})
        stats = attrs.get("last_analysis_stats", {})
        malicious = stats.get("malicious", 0)
        suspicious = stats.get("suspicious", 0)
        total = sum(stats.values()) if stats else 0

        reputation = "unknown"
        if malicious > 0:
            reputation = "malicious"
        elif suspicious > 0:
            reputation = "suspicious"
        elif total > 0:
            reputation = "harmless"

        popular_threat = attrs.get("popular_threat_classification", {}) or {}
        family = popular_threat.get("suggested_threat_label")

        results = attrs.get("last_analysis_results", {}) or {}
        labels = sorted({r.get("result") for r in results.values() if r.get("result")})[:10]

        confidence = round(malicious / total, 2) if total else None

        return ThreatResult(
            provider=self.name,
            status="success",
            indicator=sha256,
            indicator_type="sha256",
            reputation=reputation,
            confidence=confidence,
            malware_family=family,
            detections=malicious,
            total_engines=total,
            tags=(attrs.get("tags") or [])[:15] or labels,
            first_seen=str(attrs.get("first_submission_date", "")) or None,
            last_seen=str(attrs.get("last_analysis_date", "")) or None,
            raw=payload,
        )
