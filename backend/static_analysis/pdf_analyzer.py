"""PDF Static Analyzer (Section 18). Looks for JavaScript, embedded files,
launch actions and auto-open actions — the classic malicious-PDF signals."""
from __future__ import annotations

import re
from pathlib import Path

SUSPICIOUS_KEYWORDS = {
    b"/JavaScript": ("Embedded JavaScript", "high"),
    b"/JS": ("Embedded JavaScript", "high"),
    b"/OpenAction": ("Auto-run action on open", "medium"),
    b"/Launch": ("Launch action (can execute external programs)", "high"),
    b"/EmbeddedFile": ("Embedded file object", "medium"),
    b"/AA": ("Additional actions (auto-triggered)", "medium"),
    b"/RichMedia": ("Embedded Flash/rich media", "medium"),
    b"/AcroForm": ("Form fields present", "low"),
}


def analyze_pdf(file_path: str | Path) -> dict:
    path = Path(file_path)
    raw = path.read_bytes()

    result = {
        "metadata": {},
        "sections": [],
        "imports": [],
        "exports": [],
        "resources": [],
        "certificate": None,
        "security_findings": [],
        "entropy": None,
        "compiler": None,
        "is_packed": False,
        "yara_matches": [],
    }

    findings = []
    for keyword, (title, severity) in SUSPICIOUS_KEYWORDS.items():
        count = raw.count(keyword)
        if count:
            findings.append({
                "title": title,
                "severity": severity,
                "detail": f"Found {count} occurrence(s) of {keyword.decode()} in the PDF object structure.",
            })
    result["security_findings"] = findings

    obj_count = len(re.findall(rb"\d+\s+\d+\s+obj", raw))
    result["metadata"]["object_count"] = obj_count

    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(str(path))
        info = reader.metadata or {}
        result["metadata"].update({
            "page_count": len(reader.pages),
            "author": str(info.get("/Author", "")) if info else "",
            "producer": str(info.get("/Producer", "")) if info else "",
            "creator": str(info.get("/Creator", "")) if info else "",
        })
        if reader.is_encrypted:
            result["security_findings"].append({
                "title": "Encrypted PDF",
                "severity": "medium",
                "detail": "The PDF is encrypted/password-protected, which can hinder detection engines.",
            })
    except ImportError:
        result["security_findings"].append({
            "title": "Limited analysis",
            "severity": "info",
            "detail": "PyPDF2 is not installed; only raw object-stream keyword scanning was performed.",
        })
    except Exception as exc:
        result["security_findings"].append({
            "title": "PDF parsing error",
            "severity": "low",
            "detail": f"PyPDF2 failed to fully parse this PDF: {exc}",
        })

    return result
