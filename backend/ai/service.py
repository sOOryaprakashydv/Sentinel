"""AI Investigation Engine orchestrator (Section 23). Tries Gemini first,
transparently falls back to the deterministic template summarizer, and
always tags the result with its true `source` so the UI can be honest
about how the summary was produced."""
from __future__ import annotations

from backend.ai.fallback import generate_fallback_summary
from backend.ai.gemini_client import GeminiUnavailable, generate_investigation_summary
from backend.config import get_settings
from backend.utils.logger import get_logger

logger = get_logger(__name__)


def build_ai_summary(context: dict) -> dict:
    settings = get_settings()

    if settings.ai_configured:
        try:
            result = generate_investigation_summary(context)
            result["source"] = "gemini"
            return result
        except GeminiUnavailable as exc:
            logger.info("Gemini unavailable (%s); using rule-based fallback.", exc)

    result = generate_fallback_summary(context)
    result["source"] = "rule_based_fallback"
    return result
