"""Report generation dispatcher (Section 25.3: PDF / HTML / CSV / JSON)."""
from pathlib import Path

from backend.reports.csv_generator import generate_csv_report
from backend.reports.data_builder import build_report_data
from backend.reports.html_generator import generate_html_report
from backend.reports.json_generator import generate_json_report
from backend.reports.pdf_generator import generate_pdf_report
from backend.utils.exceptions import ReportGenerationError

_GENERATORS = {
    "pdf": (generate_pdf_report, "pdf"),
    "html": (generate_html_report, "html"),
    "csv": (generate_csv_report, "csv"),
    "json": (generate_json_report, "json"),
}


def generate_report(data: dict, output_dir: str | Path, investigation_id: int, fmt: str) -> str:
    fmt = fmt.lower()
    if fmt not in _GENERATORS:
        raise ReportGenerationError(f"Unsupported report format: {fmt}")

    generator_fn, ext = _GENERATORS[fmt]
    output_path = Path(output_dir) / f"investigation_{investigation_id}_report.{ext}"

    try:
        return generator_fn(data, output_path)
    except Exception as exc:
        raise ReportGenerationError(f"Failed to generate {fmt.upper()} report: {exc}") from exc


__all__ = ["generate_report", "build_report_data"]
