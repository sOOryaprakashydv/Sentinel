"""Upload validation (Section 16): extension allow-list + size limit.
MIME/type sniffing itself lives in static_analysis/file_identifier.py
(Section 17) since it needs to inspect file *content*, not just the name."""
from pathlib import Path

from backend.config import get_settings
from backend.utils.exceptions import FileTooLargeError, UnsupportedFileTypeError


def validate_upload(filename: str, size_bytes: int) -> None:
    settings = get_settings()

    ext = Path(filename).suffix.lower()
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise UnsupportedFileTypeError(
            f"File type '{ext or 'unknown'}' is not supported by the demo scope."
        )

    if size_bytes > settings.max_upload_size_bytes:
        raise FileTooLargeError(
            f"File exceeds the {settings.MAX_UPLOAD_SIZE_MB}MB upload limit."
        )
