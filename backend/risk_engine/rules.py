"""Deterministic rule tables (Section 21.5). Every rule is traceable
evidence — the AI module never touches the score, only explains it."""

FILE_RULES = {
    "packed_executable": ("Packed Executable", 12),
    "high_entropy": ("High Entropy", 8),
    "unsigned_executable": ("Unsigned Executable", 10),
    "embedded_executable": ("Embedded Executable", 15),
    "multiple_resources": ("Multiple Resources", 5),
}

WINDOWS_RULES = {
    "createremotethread_import": ("CreateRemoteThread Import", 12),
    "writeprocessmemory_import": ("WriteProcessMemory Import", 10),
    "virtualalloc_import": ("VirtualAlloc Import", 8),
    "winexec_import": ("WinExec Import", 6),
    "urldownloadtofile_import": ("URLDownloadToFile Import", 12),
}

ANDROID_RULES = {
    "send_sms_permission": ("SEND_SMS Permission", 12),
    "read_sms_permission": ("READ_SMS Permission", 10),
    "receive_boot_completed": ("RECEIVE_BOOT_COMPLETED", 8),
    "system_alert_window": ("SYSTEM_ALERT_WINDOW", 12),
    "request_install_packages": ("REQUEST_INSTALL_PACKAGES", 10),
}

OFFICE_RULES = {
    "vba_macro": ("VBA Macro", 20),
    "autoopen_macro": ("AutoOpen Macro", 18),
    "powershell_execution": ("PowerShell Execution", 15),
    "embedded_exe": ("Embedded EXE", 20),
}

PDF_RULES = {
    "embedded_javascript": ("Embedded JavaScript", 12),
    "launch_action": ("Launch Action", 18),
    "embedded_file": ("Embedded File", 10),
    "openaction": ("OpenAction", 8),
}

THREAT_INTEL_RULES = {
    "vt_over_30": ("VirusTotal > 30 detections", 20),
    "vt_over_50": ("VirusTotal > 50 detections", 25),
    "malwarebazaar_match": ("MalwareBazaar Match", 20),
    "malware_family_identified": ("Malware Family Identified", 15),
    "known_campaign": ("Known Malware Campaign", 15),
}

IOC_RULES = {
    "malicious_domain": ("Malicious Domain", 10),
    "malicious_ip": ("Malicious IP", 10),
    "known_c2": ("Known C2 Server", 15),
    "urlhaus_match": ("URLhaus Match", 15),
}

SEVERITY_BANDS = [
    (0, 20, "Informational"),
    (21, 40, "Low"),
    (41, 60, "Medium"),
    (61, 80, "High"),
    (81, 100, "Critical"),
]


def severity_for_score(score: int) -> str:
    for low, high, label in SEVERITY_BANDS:
        if low <= score <= high:
            return label
    return "Critical"
