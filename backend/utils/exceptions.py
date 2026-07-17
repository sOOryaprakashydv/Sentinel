"""Custom exceptions mapped to the standardized error envelope (Section 28)."""


class SentinelError(Exception):
    """Base class for all handled Sentinel errors."""
    code = "SENTINEL_ERROR"
    status_code = 500

    def __init__(self, message: str, code: str | None = None, status_code: int | None = None):
        super().__init__(message)
        self.message = message
        if code:
            self.code = code
        if status_code:
            self.status_code = status_code


class UnsupportedFileTypeError(SentinelError):
    code = "UNSUPPORTED_FILE_TYPE"
    status_code = 415


class FileTooLargeError(SentinelError):
    code = "FILE_TOO_LARGE"
    status_code = 413


class InvestigationNotFoundError(SentinelError):
    code = "INVESTIGATION_NOT_FOUND"
    status_code = 404


class AnalysisNotReadyError(SentinelError):
    code = "ANALYSIS_NOT_READY"
    status_code = 409


class ThreatIntelUnavailableError(SentinelError):
    code = "TI_UNAVAILABLE"
    status_code = 503


class ThreatIntelQuotaExceededError(SentinelError):
    code = "VT_QUOTA_EXCEEDED"
    status_code = 429


class AIUnavailableError(SentinelError):
    code = "AI_UNAVAILABLE"
    status_code = 503


class ReportGenerationError(SentinelError):
    code = "REPORT_GENERATION_FAILED"
    status_code = 500
