"""
Threat Intelligence orchestrator (Section 20.4-20.5, 20.8).

Queries every configured provider by SHA256 (the Query Order in 20.5 starts
here; IOC-based domain/IP/URL lookups are a natural Section 20.11 extension
point once a provider that supports them is wired in). Every provider
failure is isolated — one provider being down never blocks the others or
the rest of the investigation pipeline (Section 20.8).
"""
from __future__ import annotations

from backend.config import get_settings
from backend.threat_intel.base import ThreatIntelProvider, ThreatResult
from backend.threat_intel.cache import TTLCache
from backend.threat_intel.malwarebazaar import MalwareBazaarProvider
from backend.threat_intel.virustotal import VirusTotalProvider
from backend.utils.logger import get_logger

logger = get_logger(__name__)

_settings = get_settings()
_cache = TTLCache(ttl_minutes=_settings.TI_CACHE_DURATION_MINUTES)


def _providers() -> list[ThreatIntelProvider]:
    return [VirusTotalProvider(), MalwareBazaarProvider()]


def query_all_providers(sha256: str) -> list[ThreatResult]:
    """Query every provider for a given SHA256, using the cache when possible."""
    results: list[ThreatResult] = []

    for provider in _providers():
        cache_key = f"{provider.name}:{sha256}"
        cached = _cache.get(cache_key)
        if cached is not None:
            results.append(cached)
            continue

        try:
            result = provider.lookup_hash(sha256)
        except Exception as exc:  # a provider must never take the pipeline down with it
            logger.exception("Unexpected error querying %s", provider.name)
            result = ThreatResult(
                provider=provider.name, status="error", indicator=sha256, indicator_type="sha256",
                error_message=str(exc),
            )

        if result.status == "success":
            _cache.set(cache_key, result)
        results.append(result)

    return results


def any_provider_configured() -> bool:
    return any(p.is_configured for p in _providers())
