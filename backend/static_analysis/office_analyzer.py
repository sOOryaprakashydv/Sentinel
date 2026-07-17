"""Microsoft Office Static Analyzer (Section 18). Covers both legacy OLE
(.doc/.xls/.ppt) and modern OOXML (.docx/.xlsx/.pptx) documents, primarily
hunting for VBA macros — the dominant Office-based infection vector."""
from __future__ import annotations

from pathlib import Path


def analyze_office(file_path: str | Path, variant: str) -> dict:
    """variant is 'office_ole' or 'office_zip'."""
    path = Path(file_path)

    result = {
        "metadata": {"variant": variant},
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

    try:
        from oletools.olevba import VBA_Parser
    except ImportError:
        result["security_findings"].append({
            "title": "Limited analysis",
            "severity": "info",
            "detail": "oletools is not installed; macro analysis was skipped. "
                      "Install oletools for VBA macro extraction.",
        })
        return result

    try:
        parser = VBA_Parser(str(path))
        if not parser.detect_vba_macros():
            result["metadata"]["has_macros"] = False
            return result

        result["metadata"]["has_macros"] = True
        macro_modules = []
        suspicious_keywords: set[str] = set()

        for (_, _, vba_filename, vba_code) in parser.extract_macros():
            macro_modules.append(vba_filename)
            analysis = parser.analyze_macros() if hasattr(parser, "analyze_macros") else []

        try:
            for kw_type, keyword, description in parser.analyze_macros():
                if kw_type in ("Suspicious", "IOC", "AutoExec"):
                    suspicious_keywords.add(keyword)
                    result["security_findings"].append({
                        "title": f"{kw_type}: {keyword}",
                        "severity": "high" if kw_type == "Suspicious" else "medium",
                        "detail": description,
                    })
        except Exception:
            pass

        result["sections"] = [{"name": m} for m in macro_modules]

        if not result["security_findings"]:
            result["security_findings"].append({
                "title": "Macros present but no known-bad patterns matched",
                "severity": "medium",
                "detail": "The document contains VBA macros; manual review is still recommended.",
            })

        parser.close()

    except Exception as exc:
        result["security_findings"].append({
            "title": "Office parsing error",
            "severity": "low",
            "detail": f"oletools failed to fully parse this document: {exc}",
        })

    return result
