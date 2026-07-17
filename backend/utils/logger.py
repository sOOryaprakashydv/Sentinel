"""
Structured application logging (Sections 29 & 43).

Produces both a console stream (for `uvicorn` dev output) and a rotating
file handler under LOG_DIRECTORY, in the Timestamp / Level / Module /
Action / Details shape the PRD describes.
"""
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from backend.config import get_settings

_CONFIGURED = False


def configure_logging() -> None:
    global _CONFIGURED
    if _CONFIGURED:
        return

    settings = get_settings()
    log_dir = Path(settings.LOG_DIRECTORY)
    log_dir.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    root = logging.getLogger()
    root.setLevel(settings.LOG_LEVEL)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root.addHandler(console_handler)

    file_handler = RotatingFileHandler(
        log_dir / "sentinel.log", maxBytes=5 * 1024 * 1024, backupCount=5
    )
    file_handler.setFormatter(formatter)
    root.addHandler(file_handler)

    _CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    configure_logging()
    return logging.getLogger(name)
