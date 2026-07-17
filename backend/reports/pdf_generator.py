"""PDF report generator (Section 25). Built with ReportLab per the PRD's
dependency list (Section 46) — no headless-browser/network step needed,
matching "generate reports without requiring internet access" (25.2)."""
from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
)

_SEVERITY_COLORS = {
    "Critical": colors.HexColor("#dc2626"),
    "High": colors.HexColor("#ea580c"),
    "Medium": colors.HexColor("#d97706"),
    "Low": colors.HexColor("#16a34a"),
    "Informational": colors.HexColor("#6b7280"),
}


def _styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle("SentinelTitle", parent=styles["Title"], textColor=colors.HexColor("#1d4ed8")))
    styles.add(ParagraphStyle("SentinelH2", parent=styles["Heading2"], textColor=colors.HexColor("#1d4ed8"),
                               spaceBefore=14, spaceAfter=6))
    styles.add(ParagraphStyle("Mono", parent=styles["Normal"], fontName="Courier", fontSize=9))
    return styles


def _kv_table(rows: list[tuple[str, str]]) -> Table:
    t = Table(rows, colWidths=[45 * mm, 120 * mm])
    t.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#6b7280")),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, colors.HexColor("#e5e7eb")),
    ]))
    return t


def _data_table(header: list[str], rows: list[list[str]]) -> Table:
    data = [header] + rows if rows else [header, ["—"] * len(header)]
    t = Table(data, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f3f4f6")),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#e5e7eb")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


def generate_pdf_report(data: dict, output_path: str | Path) -> str:
    styles = _styles()
    doc = SimpleDocTemplate(str(output_path), pagesize=A4,
                             topMargin=25 * mm, bottomMargin=20 * mm)
    story = []

    story.append(Paragraph("Sentinel Investigation Report", styles["SentinelTitle"]))
    story.append(Paragraph(
        f"Case {data['case_information'].get('case_id') or '—'} · "
        f"Investigation #{data['case_information']['investigation_id']} · Generated {data['generated_at']}",
        styles["Normal"],
    ))
    story.append(Spacer(1, 10 * mm))

    if data.get("ai_summary"):
        story.append(Paragraph("Executive Summary", styles["SentinelH2"]))
        story.append(Paragraph(data["ai_summary"]["executive_summary"], styles["Normal"]))

    story.append(Paragraph("File Identification &amp; Hashes", styles["SentinelH2"]))
    fi = data["file_information"]
    story.append(_kv_table([
        ("Filename", fi["filename"]),
        ("Size", f"{fi['size']} bytes"),
        ("Type", str(fi["file_type"])),
        ("SHA256", data["hashes"]["sha256"]),
        ("SHA1", data["hashes"]["sha1"]),
        ("MD5", data["hashes"]["md5"]),
    ]))

    if data.get("risk_assessment"):
        ra = data["risk_assessment"]
        story.append(Paragraph("Risk Assessment", styles["SentinelH2"]))
        color = _SEVERITY_COLORS.get(ra["severity"], colors.grey)
        story.append(Paragraph(
            f'<font size="28" color="{color.hexval()}"><b>{ra["score"]}</b></font> '
            f'&nbsp;&nbsp;<font color="{color.hexval()}"><b>{ra["severity"]}</b></font> '
            f'&nbsp;&nbsp;Confidence: {round(ra["confidence"] * 100)}%',
            styles["Normal"],
        ))
        story.append(Spacer(1, 3 * mm))
        for r in ra["reasons"]:
            story.append(Paragraph(f'&#10003; {r["label"]} (+{r["points"]})', styles["Normal"]))

    if data.get("static_analysis"):
        sa = data["static_analysis"]
        story.append(Paragraph("Static Analysis", styles["SentinelH2"]))
        story.append(Paragraph(f'Entropy: {sa["entropy"]} · Packed: {sa["is_packed"]}', styles["Normal"]))
        for f in sa["security_findings"]:
            story.append(Paragraph(f'<b>[{f["severity"].upper()}]</b> {f["title"]} — {f["detail"]}', styles["Normal"]))

    story.append(PageBreak())

    story.append(Paragraph("Indicators of Compromise", styles["SentinelH2"]))
    story.append(_data_table(
        ["Type", "Value", "Confidence", "Source", "Status"],
        [[i["type"], i["value"][:60], f'{round(i["confidence"]*100)}%', i["source"], i["status"]]
         for i in data.get("iocs", [])],
    ))

    story.append(Paragraph("Threat Intelligence", styles["SentinelH2"]))
    story.append(_data_table(
        ["Provider", "Status", "Family", "Detections"],
        [[t["provider"], t["status"], t["malware_family"] or "—",
          f'{t["detections"]}/{t["total_engines"]}' if t["detections"] is not None else "—"]
         for t in data.get("threat_intelligence", [])],
    ))

    story.append(Paragraph("MITRE ATT&amp;CK", styles["SentinelH2"]))
    story.append(_data_table(
        ["Technique", "Name", "Tactic", "Confidence"],
        [[m["technique_id"], m["technique_name"], m["tactic"], f'{round(m["confidence"]*100)}%']
         for m in data.get("mitre_attack", [])],
    ))

    if data.get("ai_summary"):
        story.append(Paragraph("AI Investigation Summary", styles["SentinelH2"]))
        story.append(Paragraph(data["ai_summary"]["technical_summary"].replace("\n", "<br/>"), styles["Normal"]))
        story.append(Paragraph("Recommendations", styles["SentinelH2"]))
        for r in data["ai_summary"]["recommendations"]:
            story.append(Paragraph(f"• {r}", styles["Normal"]))

    doc.build(story)
    return str(output_path)
