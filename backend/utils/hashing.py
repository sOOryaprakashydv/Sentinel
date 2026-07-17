"""File hashing utilities used by the Upload module (Section 16)."""
import hashlib
from pathlib import Path


def compute_hashes(file_path: str | Path, chunk_size: int = 1024 * 1024) -> dict[str, str]:
    """Stream a file in chunks and compute md5/sha1/sha256 simultaneously
    so large samples don't need to be loaded into memory at once."""
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:
        while chunk := f.read(chunk_size):
            md5.update(chunk)
            sha1.update(chunk)
            sha256.update(chunk)

    return {
        "md5": md5.hexdigest(),
        "sha1": sha1.hexdigest(),
        "sha256": sha256.hexdigest(),
    }
