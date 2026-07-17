import json
from pathlib import Path


def generate_json_report(data: dict, output_path: str | Path) -> str:
    path = Path(output_path)
    path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
    return str(path)
