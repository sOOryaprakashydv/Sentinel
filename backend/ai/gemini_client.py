"""Gemini client wrapper (Section 23). Isolated so the rest of the app
never imports google.generativeai directly, and so a missing key/package/
network failure degrades cleanly instead of crashing the pipeline."""
from __future__ import annotations

import json

from backend.ai.prompt import SYSTEM_PROMPT, build_user_prompt
from backend.config import get_settings
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class GeminiUnavailable(Exception):
    pass


def generate_investigation_summary(context: dict) -> dict:
    """Returns the parsed JSON dict described in prompt.SYSTEM_PROMPT.
    Raises GeminiUnavailable on any failure so the caller can fall back."""
    settings = get_settings()
    if not settings.GEMINI_API_KEY:
        raise GeminiUnavailable("GEMINI_API_KEY is not configured.")

    try:
        import google.generativeai as genai
    except ImportError as exc:
        raise GeminiUnavailable(f"google-generativeai package not installed: {exc}") from exc

    try:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel(
            model_name=settings.GEMINI_MODEL,
            system_instruction=SYSTEM_PROMPT,
        )
        response = model.generate_content(build_user_prompt(context))
        text = (response.text or "").strip()
        text = text.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        return json.loads(text)
    except Exception as exc:
        logger.warning("Gemini request failed, falling back to rule-based summary: %s", exc)
        raise GeminiUnavailable(str(exc)) from exc
