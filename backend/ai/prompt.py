"""Prompt construction for the Gemini-based AI Investigation Engine
(Section 23.11). The AI only ever receives Sentinel's structured findings —
never the raw uploaded file (Section 23.3)."""
import json

SYSTEM_PROMPT = """You are a malware investigation assistant helping police investigators.

Rules you must always follow:
- Only explain the supplied evidence. Never fabricate information.
- Never invent malware names, capabilities, or IOCs that are not in the input.
- Never override the calculated risk score or modify the MITRE mappings — you only explain them.
- If evidence is unavailable or insufficient, explicitly say so rather than speculating.
- Write in clear language suitable for investigators without deep malware-analysis training.
- Respond ONLY with a single JSON object, no markdown fences, matching this exact shape:
{
  "executive_summary": "max 150 words, for senior officers: overall conclusion, risk level, recommended action",
  "technical_summary": "explains why the score/severity was assigned, referencing only supplied evidence",
  "threat_assessment": {"potential_objective": "...", "capabilities": ["..."], "confidence": "Low|Medium|High"},
  "recommendations": ["short actionable next steps, drawn only from what the evidence supports"],
  "confidence": 0.0
}"""


def build_investigation_payload(context: dict) -> str:
    """context should already be the trimmed, structured investigation data
    (Section 23.3) — filename, hashes, risk score, TI results, IOCs, MITRE."""
    return json.dumps(context, indent=2, default=str)


def build_user_prompt(context: dict) -> str:
    payload = build_investigation_payload(context)
    return (
        "Generate an investigation report using the following JSON evidence.\n"
        "Explain findings, summarize evidence, describe overall risk, and recommend next "
        "investigation steps. Avoid speculation beyond what the evidence supports.\n\n"
        f"EVIDENCE:\n{payload}"
    )
