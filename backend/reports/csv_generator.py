"""CSV export. Since a single CSV can't cleanly nest sections, the demo
produces a summary-rows CSV: header fields + one row per IOC, which is
also what Section 19's "IOC Export" calls for."""
import csv
from pathlib import Path


def generate_csv_report(data: dict, output_path: str | Path) -> str:
    path = Path(output_path)

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow(["Sentinel Investigation Report"])
        writer.writerow(["Filename", data["file_information"]["filename"]])
        writer.writerow(["SHA256", data["hashes"]["sha256"]])
        writer.writerow(["File Type", data["file_information"]["file_type"]])
        if data.get("risk_assessment"):
            writer.writerow(["Risk Score", data["risk_assessment"]["score"]])
            writer.writerow(["Severity", data["risk_assessment"]["severity"]])
        writer.writerow([])

        writer.writerow(["-- Indicators of Compromise --"])
        writer.writerow(["Type", "Value", "Confidence", "Source", "Status"])
        for ioc in data.get("iocs", []):
            writer.writerow([ioc["type"], ioc["value"], ioc["confidence"], ioc["source"], ioc["status"]])
        writer.writerow([])

        writer.writerow(["-- MITRE ATT&CK --"])
        writer.writerow(["Technique ID", "Name", "Tactic", "Confidence"])
        for m in data.get("mitre_attack", []):
            writer.writerow([m["technique_id"], m["technique_name"], m["tactic"], m["confidence"]])
        writer.writerow([])

        writer.writerow(["-- Threat Intelligence --"])
        writer.writerow(["Provider", "Status", "Malware Family", "Detections", "Total Engines"])
        for t in data.get("threat_intelligence", []):
            writer.writerow([t["provider"], t["status"], t["malware_family"], t["detections"], t["total_engines"]])

    return str(path)
