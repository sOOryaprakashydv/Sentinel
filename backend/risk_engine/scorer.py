"""
Risk Scoring Engine (Section 21).

Deterministic and evidence-driven: every point is traceable to a rule
match, capped at 100, with a confidence value and a plain-language reason
list. This module never calls the AI — per Section 21.1, AI only explains
scores, it never sets them.
"""
from __future__ import annotations

from backend.risk_engine.rules import (
    FILE_RULES, WINDOWS_RULES, ANDROID_RULES, OFFICE_RULES, PDF_RULES,
    THREAT_INTEL_RULES, IOC_RULES, severity_for_score,
)


def _match(reasons: list[dict], points: int, rule_key: str, label: str, score: int) -> tuple[int, int]:
    reasons.append({"rule": rule_key, "label": label, "points": points})
    return score + points, 1


def calculate_risk(
    static_analysis: dict | None,
    file_type: str | None,
    iocs: list[dict] | None,
    threat_intel_results: list[dict] | None,
) -> dict:
    static_analysis = static_analysis or {}
    iocs = iocs or []
    threat_intel_results = threat_intel_results or []

    score = 0
    reasons: list[dict] = []
    matched_count = 0

    findings_text = " ".join(
        f.get("title", "") for f in static_analysis.get("security_findings_json")
        or static_analysis.get("security_findings", []) or []
    ).lower()
    imports_flat = " ".join(
        fn for imp in (static_analysis.get("imports_json") or static_analysis.get("imports", []) or [])
        for fn in (imp.get("functions", []) if isinstance(imp, dict) else [])
    ).lower()
    permissions = set(static_analysis.get("permissions_json") or static_analysis.get("permissions", []) or [])
    is_packed = bool(static_analysis.get("is_packed"))
    entropy = static_analysis.get("entropy")

    # --- File Characteristics ---
    if is_packed:
        score, m = _match(reasons, FILE_RULES["packed_executable"][1], "packed_executable",
                           FILE_RULES["packed_executable"][0], score)
        matched_count += m
    if entropy is not None and entropy > 7.2 and not is_packed:
        score, m = _match(reasons, FILE_RULES["high_entropy"][1], "high_entropy",
                           FILE_RULES["high_entropy"][0], score)
        matched_count += m
    if "unsigned" in findings_text or "not signed" in findings_text:
        score, m = _match(reasons, FILE_RULES["unsigned_executable"][1], "unsigned_executable",
                           FILE_RULES["unsigned_executable"][0], score)
        matched_count += m
    if "executable content inside archive" in findings_text or "embedded exe" in findings_text:
        score, m = _match(reasons, FILE_RULES["embedded_executable"][1], "embedded_executable",
                           FILE_RULES["embedded_executable"][0], score)
        matched_count += m

    # --- Windows / PE static indicators ---
    if file_type == "pe":
        for keyword, rule_key in [
            ("createremotethread", "createremotethread_import"),
            ("writeprocessmemory", "writeprocessmemory_import"),
            ("virtualalloc", "virtualalloc_import"),
            ("winexec", "winexec_import"),
            ("urldownloadtofile", "urldownloadtofile_import"),
        ]:
            if keyword in imports_flat:
                label, pts = WINDOWS_RULES[rule_key]
                score, m = _match(reasons, pts, rule_key, label, score)
                matched_count += m

    # --- Android permissions ---
    if file_type == "apk":
        perm_map = {
            "android.permission.SEND_SMS": "send_sms_permission",
            "android.permission.READ_SMS": "read_sms_permission",
            "android.permission.RECEIVE_BOOT_COMPLETED": "receive_boot_completed",
            "android.permission.SYSTEM_ALERT_WINDOW": "system_alert_window",
            "android.permission.REQUEST_INSTALL_PACKAGES": "request_install_packages",
        }
        for perm, rule_key in perm_map.items():
            if perm in permissions:
                label, pts = ANDROID_RULES[rule_key]
                score, m = _match(reasons, pts, rule_key, label, score)
                matched_count += m

    # --- Office macros ---
    if file_type in ("office_ole", "office_zip"):
        if static_analysis.get("metadata_json", static_analysis.get("metadata", {})).get("has_macros") \
                or "macro" in findings_text:
            score, m = _match(reasons, OFFICE_RULES["vba_macro"][1], "vba_macro",
                               OFFICE_RULES["vba_macro"][0], score)
            matched_count += m
        if "autoexec" in findings_text or "autoopen" in findings_text:
            score, m = _match(reasons, OFFICE_RULES["autoopen_macro"][1], "autoopen_macro",
                               OFFICE_RULES["autoopen_macro"][0], score)
            matched_count += m
        if "powershell" in findings_text:
            score, m = _match(reasons, OFFICE_RULES["powershell_execution"][1], "powershell_execution",
                               OFFICE_RULES["powershell_execution"][0], score)
            matched_count += m

    # --- PDF indicators ---
    if file_type == "pdf":
        pdf_map = {
            "embedded javascript": "embedded_javascript",
            "launch action": "launch_action",
            "embedded file": "embedded_file",
            "auto-run action on open": "openaction",
        }
        for keyword, rule_key in pdf_map.items():
            if keyword in findings_text:
                label, pts = PDF_RULES[rule_key]
                score, m = _match(reasons, pts, rule_key, label, score)
                matched_count += m

    # --- Threat Intelligence ---
    for result in threat_intel_results:
        if result.get("status") != "success":
            continue
        detections = result.get("detections") or 0
        total = result.get("total_engines") or 0
        if result.get("provider") == "virustotal" and total:
            if detections > 50:
                score, m = _match(reasons, THREAT_INTEL_RULES["vt_over_50"][1], "vt_over_50",
                                   THREAT_INTEL_RULES["vt_over_50"][0], score)
                matched_count += m
            elif detections > 30:
                score, m = _match(reasons, THREAT_INTEL_RULES["vt_over_30"][1], "vt_over_30",
                                   THREAT_INTEL_RULES["vt_over_30"][0], score)
                matched_count += m
        if result.get("provider") == "malwarebazaar":
            score, m = _match(reasons, THREAT_INTEL_RULES["malwarebazaar_match"][1], "malwarebazaar_match",
                               THREAT_INTEL_RULES["malwarebazaar_match"][0], score)
            matched_count += m
        if result.get("malware_family"):
            score, m = _match(reasons, THREAT_INTEL_RULES["malware_family_identified"][1],
                               "malware_family_identified",
                               THREAT_INTEL_RULES["malware_family_identified"][0], score)
            matched_count += m

    # --- IOC reputation ---
    malicious_domains = [i for i in iocs if i.get("type") == "domain" and i.get("status") == "malicious"]
    malicious_ips = [i for i in iocs if i.get("type") == "ipv4" and i.get("status") == "malicious"]
    if malicious_domains:
        score, m = _match(reasons, IOC_RULES["malicious_domain"][1], "malicious_domain",
                           IOC_RULES["malicious_domain"][0], score)
        matched_count += m
    if malicious_ips:
        score, m = _match(reasons, IOC_RULES["malicious_ip"][1], "malicious_ip",
                           IOC_RULES["malicious_ip"][0], score)
        matched_count += m

    displayed_score = min(score, 100)
    severity = severity_for_score(displayed_score)

    # Confidence (Section 21.7): grows with corroborating evidence & data completeness.
    ti_attempted = len(threat_intel_results)
    ti_succeeded = len([r for r in threat_intel_results if r.get("status") == "success"])
    completeness = 0.5 if ti_attempted == 0 else (0.5 + 0.5 * (ti_succeeded / ti_attempted))
    evidence_factor = min(matched_count / 6, 1.0)
    confidence = round(min(0.4 + 0.35 * evidence_factor + 0.25 * completeness, 0.99), 2)

    return {
        "score": displayed_score,
        "raw_score": score,
        "severity": severity,
        "confidence": confidence,
        "reasons": reasons,
    }
