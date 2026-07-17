"""Script Static Analyzer (Section 18) for JavaScript, PowerShell, Python
and Batch files — pure pattern-based inspection since these are plain text,
no third-party parser required."""
from __future__ import annotations

import re
from pathlib import Path

from backend.static_analysis.entropy import shannon_entropy

# (pattern, title, severity) per script language family
_COMMON_PATTERNS = [
    (r"(?i)invoke-expression|iex\s*\(", "Dynamic code execution (Invoke-Expression)", "high"),
    (r"(?i)downloadstring|downloadfile|net\.webclient", "Remote download capability", "high"),
    (r"(?i)-enc(odedcommand)?\s+[A-Za-z0-9+/=]{20,}", "Base64-encoded PowerShell payload", "high"),
    (r"(?i)frombase64string|atob\(|base64\.b64decode", "Base64 decoding routine", "medium"),
    (r"(?i)eval\s*\(", "Use of eval()", "high"),
    (r"(?i)createobject\(|activexobject\(", "COM/ActiveX object instantiation", "medium"),
    (r"(?i)wscript\.shell|shell\.application", "Windows Shell automation", "medium"),
    (r"(?i)-windowstyle\s+hidden|-w\s+hidden", "Hidden execution window", "high"),
    (r"(?i)bypass\s+-executionpolicy|-ep\s+bypass", "Execution policy bypass", "high"),
    (r"(?i)certutil.*-decode|certutil.*-urlcache", "certutil abused for download/decode", "high"),
    (r"(?i)os\.system\(|subprocess\.(call|popen|run)", "Shell command execution", "medium"),
    (r"(?i)socket\.socket\(|reverse.?shell", "Networking/reverse-shell primitives", "high"),
]


def analyze_script(file_path: str | Path) -> dict:
    path = Path(file_path)
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        text = raw.decode("latin-1", errors="ignore")

    findings = []
    for pattern, title, severity in _COMMON_PATTERNS:
        if re.search(pattern, text):
            findings.append({"title": title, "severity": severity, "detail": f"Pattern matched: {pattern}"})

    long_lines = [ln for ln in text.splitlines() if len(ln) > 500]
    if long_lines:
        findings.append({
            "title": "Abnormally long line(s)",
            "severity": "low",
            "detail": f"{len(long_lines)} line(s) over 500 characters — often indicates obfuscation "
                      f"or a minified/packed payload.",
        })

    return {
        "metadata": {"line_count": text.count("\n") + 1, "char_count": len(text)},
        "sections": [],
        "imports": [],
        "exports": [],
        "resources": [],
        "certificate": None,
        "security_findings": findings,
        "entropy": round(shannon_entropy(raw), 3),
        "compiler": None,
        "is_packed": False,
        "yara_matches": [],
    }
