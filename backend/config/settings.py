"""
Central application configuration.

All configurable values (Section 44 of the PRD) are sourced from environment
variables / a .env file so the demo can run without code changes across
machines. Nothing here is hard-coded per-deployment.
"""
from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # project root


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- General ---
    APP_NAME: str = "Sentinel"
    APP_VERSION: str = "1.0.0-demo"
    ENV: str = "development"
    LOG_LEVEL: str = "INFO"

    # --- Server ---
    API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    # --- Database ---
    DATABASE_URL: str = f"sqlite:///{BASE_DIR / 'sentinel.db'}"

    # --- Storage ---
    UPLOAD_DIRECTORY: str = str(BASE_DIR / "uploads")
    REPORT_DIRECTORY: str = str(BASE_DIR / "reports")
    LOG_DIRECTORY: str = str(BASE_DIR / "logs")
    MAX_UPLOAD_SIZE_MB: int = 100

    # --- Threat Intelligence (optional; app degrades gracefully if absent) ---
    VT_API_KEY: Optional[str] = Field(default=None)
    MALWAREBAZAAR_API_KEY: Optional[str] = Field(default=None)
    TI_REQUEST_TIMEOUT_SECONDS: int = 15
    TI_CACHE_DURATION_MINUTES: int = 60

    # --- AI (optional; app degrades gracefully if absent) ---
    GEMINI_API_KEY: Optional[str] = Field(default=None)
    GEMINI_MODEL: str = "gemini-1.5-pro"

    # --- Supported file extensions (Section 6, Demo Scope) ---
    ALLOWED_EXTENSIONS: set[str] = {
        ".exe", ".dll", ".apk", ".pdf", ".doc", ".docx", ".xls", ".xlsx",
        ".ppt", ".pptx", ".zip", ".js", ".ps1", ".py", ".bat",
    }

    @property
    def max_upload_size_bytes(self) -> int:
        return self.MAX_UPLOAD_SIZE_MB * 1024 * 1024

    @property
    def threat_intel_configured(self) -> bool:
        return bool(self.VT_API_KEY or self.MALWAREBAZAAR_API_KEY)

    @property
    def ai_configured(self) -> bool:
        return bool(self.GEMINI_API_KEY)


@lru_cache
def get_settings() -> Settings:
    return Settings()


def ensure_runtime_directories() -> None:
    """Create upload/report/log directories on startup if missing."""
    settings = get_settings()
    for path in (settings.UPLOAD_DIRECTORY, settings.REPORT_DIRECTORY, settings.LOG_DIRECTORY):
        Path(path).mkdir(parents=True, exist_ok=True)
