"""
Template-based fallback summary (Sections 23.10, 48: "the application
remains functional even if external APIs fail"). Produces the same JSON
shape Gemini would, built purely from Sentinel's own computed evidence,
so the Investigation screen never has an empty AI Summary card.
"""
from __future__ import annotations

_RECOMMENDATION_TEMPLATES = {
    "Critical": [
        "Isolate the affected system from the network immediately.",
        "Preserve the file, hashes, and this report as evidence.",
        "Block any malicious domains/IPs identified in the IOC list at the network perimeter.",
        "Scan other endpoints for the same file hash or matching indicators.",
    ],
    "High": [
        "Isolate or closely monitor the affected system.",
        "Preserve the file and this report as evidence.",
        "Review the extracted IOCs and block confirmed-malicious entries.",
    ],
    "Medium": [
        "Continue monitoring the affected system for further activity.",
        "Review the flagged findings and confirm whether the file was executed.",
    ],
    "Low": [
        "Retain the file for reference; no immediate containment action required.",
    ],
    "Informational": [
        "No significant malicious indicators were found; retain findings for the case file.",
    ],
}


def generate_fallback_summary(context: dict) -> dict:
    filename = context.get("filename", "the uploaded file")
    severity = context.get("severity", "Informational")
    score = context.get("risk_score", 0)
    family = context.get("malware_family")
    mitre = context.get("mitre") or []
    reasons = context.get("risk_reasons") or []
    ti = context.get("threat_intelligence") or []

    ti_hits = [r for r in ti if r.get("status") == "success" and r.get("reputation") == "malicious"]

    lines = [f"{filename} received a risk score of {score}/100 ({severity})."]
    if reasons:
        top_reasons = ", ".join(r.get("label", "") for r in reasons[:5])
        lines.append(f"This is based on: {top_reasons}.")
    if family:
        lines.append(f"External threat intelligence associates this sample with the '{family}' family.")
    elif ti_hits:
        lines.append("External threat intelligence flagged this sample as malicious.")
    if mitre:
        technique_names = ", ".join(f"{m.get('technique_id')} ({m.get('technique_name')})" for m in mitre[:4])
        lines.append(f"Observed behavior maps to MITRE ATT&CK techniques including {technique_names}.")
    if not reasons and not ti_hits and not mitre:
        lines.append("Available evidence is insufficient to determine additional malware behavior. "
                      "Further dynamic analysis is recommended.")

    executive_summary = " ".join(lines)[:900]

    technical_lines = ["The following evidence contributed to this assessment:"]
    for r in reasons:
        technical_lines.append(f"- {r.get('label')} (+{r.get('points')} points)")
    for r in ti_hits:
        technical_lines.append(f"- {r.get('provider')} reputation: malicious"
                                + (f", family: {r.get('malware_family')}" if r.get("malware_family") else ""))
    if not reasons and not ti_hits:
        technical_lines.append("- No rule-based indicators or threat intelligence matches were found.")
    technical_summary = "\n".join(technical_lines)

    capabilities = []
    tactic_set = {m.get("tactic") for m in mitre}
    if "Credential Access" in tactic_set:
        capabilities.append("Credential harvesting")
    if "Command and Control" in tactic_set:
        capabilities.append("Command and control communication")
    if "Persistence" in tactic_set:
        capabilities.append("Persistence across reboot")
    if "Defense Evasion" in tactic_set:
        capabilities.append("Evasion/obfuscation")
    if not capabilities:
        capabilities = ["Could not be determined from available evidence"]

    objective = "Could not be determined from available evidence"
    if "Credential Access" in tactic_set:
        objective = "Credential theft"
    elif "Command and Control" in tactic_set:
        objective = "Remote access / command and control"
    elif family:
        objective = f"Consistent with known '{family}' behavior"

    confidence_bucket = "High" if score >= 70 else "Medium" if score >= 40 else "Low"

    recommendations = _RECOMMENDATION_TEMPLATES.get(severity, _RECOMMENDATION_TEMPLATES["Informational"])

    return {
        "executive_summary": executive_summary,
        "technical_summary": technical_summary,
        "threat_assessment": {
            "potential_objective": objective,
            "capabilities": capabilities,
            "confidence": confidence_bucket,
        },
        "recommendations": recommendations,
        "confidence": context.get("risk_confidence", 0.5),
    }
