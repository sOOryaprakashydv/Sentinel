"""
File Identification Module (Section 17).

Identifies true file type from content (magic bytes) rather than trusting
the extension, then routes to the correct static analyzer. Uses
`python-magic` when available and falls back to a small built-in magic-byte
table so the pipeline still works in environments where libmagic isn't
installed.
"""
from __future__ import annotations

from pathlib import Path

_SIGNATURES: list[tuple[bytes, str, str]] = [
    (b"MZ", "pe", "application/x-dosexec"),
    (b"PK\x03\x04", "zip_based", "application/zip"),  # zip, apk, docx/xlsx/pptx all start this way
    (b"%PDF-", "pdf", "application/pdf"),
    (b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1", "ole", "application/x-ole-storage"),  # legacy .doc/.xls/.ppt
]

_SCRIPT_EXTENSIONS = {
    ".js": "javascript",
    ".ps1": "powershell",
    ".py": "python",
    ".bat": "batch",
}

_OFFICE_EXTENSIONS = {".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx"}


def identify_file(file_path: str | Path, original_filename: str) -> dict:
    """Returns {"category": ..., "mime": ..., "detail": ...}
    category is one of: pe, apk, pdf, office_ole, office_zip, zip, script, unknown
    """
    path = Path(file_path)
    ext = Path(original_filename).suffix.lower()
    header = path.read_bytes()[:16] if path.exists() else b""

    try:
        import magic  # python-magic, requires libmagic on the OS
        mime = magic.from_file(str(path), mime=True)
    except Exception:
        mime = _guess_mime(header, ext)

    if ext in _SCRIPT_EXTENSIONS:
        return {"category": "script", "mime": mime, "detail": _SCRIPT_EXTENSIONS[ext]}

    for sig, category, sig_mime in _SIGNATURES:
        if header.startswith(sig):
            mime = mime or sig_mime
            if category == "zip_based":
                return {"category": _resolve_zip_variant(path, ext), "mime": mime, "detail": None}
            if category == "ole":
                return {"category": "office_ole", "mime": mime, "detail": None}
            return {"category": category, "mime": mime, "detail": None}

    return {"category": "unknown", "mime": mime or "application/octet-stream", "detail": None}


def _resolve_zip_variant(path: Path, ext: str) -> str:
    if ext == ".apk":
        return "apk"
    if ext in _OFFICE_EXTENSIONS:
        return "office_zip"
    return "zip"


def _guess_mime(header: bytes, ext: str) -> str:
    import mimetypes
    guessed, _ = mimetypes.guess_type("f" + ext)
    if guessed:
        return guessed
    if header.startswith(b"MZ"):
        return "application/x-dosexec"
    if header.startswith(b"PK"):
        return "application/zip"
    if header.startswith(b"%PDF-"):
        return "application/pdf"
    return "application/octet-stream"
