"""
MITRE ATT&CK Mapping Module (Section 22).

Entirely rule-based: observed static-analysis behaviors are matched to
ATT&CK techniques (Section 22.4). Confidence mirrors how strong/specific
the matched evidence is.
"""
from __future__ import annotations

TECHNIQUES = {
    "T1055": ("Process Injection", "Defense Evasion",
              "The sample uses APIs commonly associated with injecting code into another process."),
    "T1059.001": ("Command and Scripting Interpreter: PowerShell", "Execution",
                  "The sample executes or embeds PowerShell commands."),
    "T1059.003": ("Command and Scripting Interpreter: Windows Command Shell", "Execution",
                  "The sample invokes the Windows command shell to run commands."),
    "T1547": ("Boot or Logon Autostart Execution: Registry Run Keys", "Persistence",
              "The sample references registry Run/RunOnce keys used to survive reboot."),
    "T1053": ("Scheduled Task/Job", "Persistence",
              "The sample references scheduled task creation for persistence."),
    "T1574": ("Hijack Execution Flow: DLL Side-Loading", "Defense Evasion",
              "The sample's structure is consistent with DLL side-loading."),
    "T1003": ("OS Credential Dumping", "Credential Access",
              "The sample imports APIs commonly used to access credential material."),
    "T1036": ("Masquerading", "Defense Evasion",
              "The sample disguises its true nature (e.g. double extension, mismatched icon/type)."),
    "T1027": ("Obfuscated Files or Information", "Defense Evasion",
              "The sample uses packing, high entropy, or encoding to hinder analysis."),
    "T1071": ("Application Layer Protocol", "Command and Control",
              "The sample contains network indicators consistent with C2 communication."),
    "T1204": ("User Execution", "Execution",
              "The sample relies on a user opening/running it (e.g. a macro-laden document)."),
    "T1105": ("Ingress Tool Transfer", "Command and Control",
              "The sample can download and execute additional payloads."),
}


def _findings_text(static_analysis: dict) -> str:
    findings = static_analysis.get("security_findings_json") or static_analysis.get("security_findings") or []
    return " ".join(f.get("title", "") + " " + f.get("detail", "") for f in findings).lower()


def _imports_text(static_analysis: dict) -> str:
    imports = static_analysis.get("imports_json") or static_analysis.get("imports") or []
    return " ".join(
        fn for imp in imports for fn in (imp.get("functions", []) if isinstance(imp, dict) else [])
    ).lower()


def map_to_mitre(static_analysis: dict | None, file_type: str | None, iocs: list[dict] | None) -> list[dict]:
    static_analysis = static_analysis or {}
    iocs = iocs or []
    findings = _findings_text(static_analysis)
    imports = _imports_text(static_analysis)

    mappings: list[dict] = []

    def add(technique_id: str, evidence: str, confidence: float):
        name, tactic, description = TECHNIQUES[technique_id]
        mappings.append({
            "technique_id": technique_id,
            "technique_name": name,
            "tactic": tactic,
            "description": description,
            "evidence": evidence,
            "confidence": round(confidence, 2),
        })

    if any(k in imports for k in ("createremotethread", "writeprocessmemory", "virtualallocex")):
        add("T1055", "Process injection APIs found in imports (CreateRemoteThread/WriteProcessMemory).", 0.9)

    if "powershell" in findings:
        add("T1059.001", "PowerShell execution pattern detected in script/macro content.", 0.85)

    if "cmd.exe" in findings or "command shell" in findings or "wscript.shell" in findings:
        add("T1059.003", "Command shell / WScript.Shell automation detected.", 0.75)

    if "registry" in findings and ("run" in findings or "hkcu\\software\\microsoft\\windows\\currentversion\\run" in findings):
        add("T1547", "Registry Run-key references found in extracted strings.", 0.7)

    if "scheduled task" in findings or "schtasks" in findings:
        add("T1053", "Scheduled task creation reference detected.", 0.7)

    if "credential" in findings or "lsass" in findings:
        add("T1003", "References to credential material access detected.", 0.75)

    if any(i.get("type") in ("url", "ipv4") for i in iocs) and ("download" in findings or "urldownloadtofile" in imports):
        add("T1105", "Sample can retrieve remote content and has embedded network indicators.", 0.7)

    if any(i.get("type") in ("url", "domain", "ipv4") for i in iocs):
        add("T1071", "Network-related IOCs (URL/domain/IP) extracted from the sample.", 0.6)

    entropy = static_analysis.get("entropy")
    is_packed = bool(static_analysis.get("is_packed"))
    if is_packed or (entropy is not None and entropy > 7.2):
        evidence = "High entropy" + (" and packed executable structure" if is_packed else "") + "."
        add("T1027", evidence, 0.9 if is_packed else 0.75)

    if file_type in ("office_ole", "office_zip") and ("macro" in findings):
        add("T1204", "Execution depends on a user opening a macro-enabled document.", 0.7)

    # De-duplicate by technique_id, keeping the highest-confidence entry.
    best: dict[str, dict] = {}
    for m in mappings:
        existing = best.get(m["technique_id"])
        if not existing or m["confidence"] > existing["confidence"]:
            best[m["technique_id"]] = m

    return sorted(best.values(), key=lambda m: m["confidence"], reverse=True)
