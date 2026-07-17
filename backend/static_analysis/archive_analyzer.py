"""ZIP Archive Static Analyzer (Section 18). Lists contents and flags
common abuse patterns: nested executables, double extensions, encrypted
archives, and zip-bomb-style extreme compression ratios."""
from __future__ import annotations

import zipfile
from pathlib import Path

EXECUTABLE_EXTENSIONS = {".exe", ".dll", ".scr", ".bat", ".ps1", ".js", ".vbs", ".jar", ".msi"}


def analyze_zip(file_path: str | Path) -> dict:
    path = Path(file_path)
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

    try:
        with zipfile.ZipFile(path) as z:
            infos = z.infolist()
            result["metadata"]["entry_count"] = len(infos)
            result["sections"] = [
                {"name": i.filename, "compressed_size": i.compress_size, "raw_size": i.file_size}
                for i in infos[:200]  # cap for sanity on huge archives
            ]

            embedded_exec = [i.filename for i in infos if Path(i.filename).suffix.lower() in EXECUTABLE_EXTENSIONS]
            if embedded_exec:
                result["security_findings"].append({
                    "title": "Executable content inside archive",
                    "severity": "high",
                    "detail": f"Contains executable-type entries: {', '.join(embedded_exec[:10])}",
                })

            double_ext = [i.filename for i in infos if i.filename.lower().count(".") >= 2
                          and Path(i.filename).suffix.lower() in {".exe", ".scr", ".bat"}]
            if double_ext:
                result["security_findings"].append({
                    "title": "Double file extension detected",
                    "severity": "high",
                    "detail": f"Files disguised with a trailing executable extension: {', '.join(double_ext[:10])}",
                })

            encrypted = any(i.flag_bits & 0x1 for i in infos)
            if encrypted:
                result["security_findings"].append({
                    "title": "Password-protected entries",
                    "severity": "medium",
                    "detail": "The archive contains encrypted entries, often used to evade AV scanning.",
                })

            total_compressed = sum(i.compress_size for i in infos) or 1
            total_raw = sum(i.file_size for i in infos)
            ratio = total_raw / total_compressed
            if ratio > 100:
                result["security_findings"].append({
                    "title": "Extreme compression ratio",
                    "severity": "medium",
                    "detail": f"Compression ratio of {ratio:.0f}:1 is consistent with a zip-bomb pattern.",
                })

    except zipfile.BadZipFile:
        result["security_findings"].append({
            "title": "Corrupted or invalid ZIP",
            "severity": "medium",
            "detail": "The file could not be opened as a valid ZIP archive.",
        })

    return result
