"""
IOC Extraction Module (Section 19).

Pipeline: pull printable strings from the raw file -> run type-specific
regexes -> normalize -> de-duplicate -> attach a confidence level. Also
folds in a few IOCs that fall naturally out of static analysis (e.g. a
registry-key import, a suspicious URL already found in a PDF action).
"""
from __future__ import annotations

import re
from pathlib import Path

_MIN_STRING_LEN = 4

_STRINGS_RE = re.compile(rb"[\x20-\x7e]{%d,}" % _MIN_STRING_LEN)

_PATTERNS: dict[str, re.Pattern] = {
    "ipv4": re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b"),
    "ipv6": re.compile(r"\b(?:[A-Fa-f0-9]{1,4}:){7}[A-Fa-f0-9]{1,4}\b"),
    "url": re.compile(r"\b[a-zA-Z][a-zA-Z0-9+.\-]*://[^\s\"'<>]+"),
    "email": re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b"),
    "domain": re.compile(
        r"\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+"
        r"(?:com|net|org|info|biz|xyz|top|ru|cn|io|co|me|link|club|online|site|icu|shop)\b"
    ),
    "registry_key": re.compile(
        r"\b(?:HKEY_LOCAL_MACHINE|HKEY_CURRENT_USER|HKLM|HKCU|HKCR|HKU)\\[A-Za-z0-9_\\\s\.\-]+"
    ),
    "file_path": re.compile(
        r"\b[A-Za-z]:\\(?:[^\\\s\"'<>|*?]+\\)*[^\\\s\"'<>|*?]+\.\w{1,5}"
    ),
    "hash_md5": re.compile(r"\b[a-fA-F0-9]{32}\b"),
    "hash_sha1": re.compile(r"\b[a-fA-F0-9]{40}\b"),
    "hash_sha256": re.compile(r"\b[a-fA-F0-9]{64}\b"),
    "user_agent": re.compile(r"Mozilla/5\.0[^\r\n\"']{10,200}"),
    "cve": re.compile(r"CVE-\d{4}-\d{4,7}"),
    # BTC (legacy/segwit), ETH
    "crypto_wallet": re.compile(
        r"\b(?:bc1[a-z0-9]{25,39}|[13][a-km-zA-HJ-NP-Z1-9]{25,34}|0x[a-fA-F0-9]{40})\b"
    ),
}

# Extremely common false-positive domains/strings to suppress noise in the demo
_DOMAIN_ALLOWLIST = {
    "microsoft.com", "schemas.microsoft.com", "w3.org", "adobe.com",
    "openxmlformats.org", "sun.com", "apache.org", "python.org",
}


def _extract_strings(raw: bytes) -> list[str]:
    return [m.decode("ascii", errors="ignore") for m in _STRINGS_RE.findall(raw)]


def _confidence(ioc_type: str, value: str) -> float:
    """Simple heuristic confidence (Section 19, IOC Confidence)."""
    if ioc_type in ("hash_sha256", "hash_sha1", "hash_md5"):
        return 0.9
    if ioc_type in ("ipv4", "url", "registry_key"):
        return 0.75
    if ioc_type == "domain" and value.lower() not in _DOMAIN_ALLOWLIST:
        return 0.6
    if ioc_type == "cve":
        return 0.95
    return 0.5


def extract_iocs(file_path: str | Path, static_analysis: dict | None = None) -> list[dict]:
    path = Path(file_path)
    raw = path.read_bytes()
    strings = _extract_strings(raw)
    blob = "\n".join(strings)

    seen: set[tuple[str, str]] = set()
    iocs: list[dict] = []

    for ioc_type, pattern in _PATTERNS.items():
        for match in pattern.findall(blob):
            value = match.strip()
            if not value:
                continue
            if ioc_type == "domain" and value.lower() in _DOMAIN_ALLOWLIST:
                continue
            key = (ioc_type, value.lower())
            if key in seen:
                continue
            seen.add(key)
            iocs.append({
                "type": ioc_type,
                "value": value,
                "confidence": _confidence(ioc_type, value),
                "source": "string_scan",
                "evidence": f"Matched via string extraction ({ioc_type} pattern).",
                "status": "unknown",
            })

    # Fold in a couple of static-analysis-derived IOCs when available.
    if static_analysis:
        for imp in static_analysis.get("imports", []) or []:
            dll = imp.get("dll") if isinstance(imp, dict) else None
            if dll and dll.lower() in ("urlmon.dll", "wininet.dll", "winhttp.dll"):
                key = ("file_path", dll.lower())
                if key not in seen:
                    seen.add(key)
                    iocs.append({
                        "type": "file_path",
                        "value": dll,
                        "confidence": 0.55,
                        "source": "static_analysis",
                        "evidence": "Networking-capable DLL imported by the binary.",
                        "status": "unknown",
                    })

    return iocs
