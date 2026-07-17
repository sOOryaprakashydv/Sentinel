from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

_TEMPLATE_DIR = Path(__file__).parent / "templates"
_env = Environment(
    loader=FileSystemLoader(str(_TEMPLATE_DIR)),
    autoescape=select_autoescape(["html"]),
)


def generate_html_report(data: dict, output_path: str | Path) -> str:
    template = _env.get_template("report.html.j2")
    rendered = template.render(data=data)
    path = Path(output_path)
    path.write_text(rendered, encoding="utf-8")
    return str(path)
