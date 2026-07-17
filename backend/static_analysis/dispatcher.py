"""Static Analysis dispatcher (Section 18 overview).
Single entry point the pipeline service calls after file identification."""
from __future__ import annotations

from pathlib import Path

from backend.static_analysis.file_identifier import identify_file
from backend.static_analysis.pe_analyzer import analyze_pe
from backend.static_analysis.apk_analyzer import analyze_apk
from backend.static_analysis.pdf_analyzer import analyze_pdf
from backend.static_analysis.office_analyzer import analyze_office
from backend.static_analysis.script_analyzer import analyze_script
from backend.static_analysis.archive_analyzer import analyze_zip

_DEFAULT_RESULT_KEYS = (
    "metadata", "sections", "imports", "exports", "resources", "permissions",
    "certificate", "security_findings", "entropy", "compiler", "is_packed", "yara_matches",
)


def run_static_analysis(file_path: str | Path, original_filename: str) -> dict:
    identity = identify_file(file_path, original_filename)
    category = identity["category"]

    if category == "pe":
        analysis = analyze_pe(file_path)
    elif category == "apk":
        analysis = analyze_apk(file_path)
    elif category == "pdf":
        analysis = analyze_pdf(file_path)
    elif category in ("office_ole", "office_zip"):
        analysis = analyze_office(file_path, category)
    elif category == "script":
        analysis = analyze_script(file_path)
    elif category == "zip":
        analysis = analyze_zip(file_path)
    else:
        analysis = {k: ([] if k not in ("entropy", "compiler", "is_packed", "certificate") else None)
                    for k in _DEFAULT_RESULT_KEYS}
        analysis["is_packed"] = False
        analysis["security_findings"] = [{
            "title": "Unrecognized file type",
            "severity": "info",
            "detail": "No specialized analyzer matched this file's signature; only hashing/identification "
                      "was performed.",
        }]

    analysis.setdefault("permissions", [])
    analysis["file_type"] = category
    analysis["mime"] = identity["mime"]
    return analysis
