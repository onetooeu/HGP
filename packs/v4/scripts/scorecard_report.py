"""Generate a PDF auto-report from HGP_Falsification_Scorecard.csv

Usage:
  python scorecard_report.py

Reads: ../docs/HGP_Falsification_Scorecard.csv
Writes: ../HGP_Scorecard_AutoReport_v4.pdf (in repo root)
"""
from pathlib import Path
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors

ROOT = Path(__file__).resolve().parents[1]
score = pd.read_csv(ROOT/'docs'/'HGP_Falsification_Scorecard.csv')

def gate_status_color(val):
    v = str(val).strip().lower()
    if v in ("pass","passed","yes","ok","✅"):
        return colors.HexColor("#d7f5d7")
    if v in ("fail","failed","no","❌"):
        return colors.HexColor("#f7d7d7")
    if v in ("partial","pending","tbd","?", "⚠️"):
        return colors.HexColor("#fff2cc")
    return colors.white

report_pdf = ROOT/"HGP_Scorecard_AutoReport_v4.pdf"
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="H1", parent=styles["Heading1"], fontSize=18, leading=22, spaceAfter=10))
styles.add(ParagraphStyle(name="H2", parent=styles["Heading2"], fontSize=13.5, leading=17, spaceAfter=8))
styles.add(ParagraphStyle(name="Body", parent=styles["BodyText"], fontSize=10.5, leading=14))
styles.add(ParagraphStyle(name="Small", parent=styles["BodyText"], fontSize=9, leading=12, textColor=colors.grey))

doc = SimpleDocTemplate(str(report_pdf), pagesize=A4, leftMargin=2.0*cm, rightMargin=2.0*cm, topMargin=1.7*cm, bottomMargin=1.6*cm)

story = []
story.append(Paragraph("HGP Falsification Scorecard — Auto Report (v4)", styles["Title"]))
story.append(Paragraph("Generated from /docs/HGP_Falsification_Scorecard.csv.", styles["Small"]))
story.append(Spacer(1, 10))

vals = score["PassFail"].fillna("").astype(str).str.strip().str.lower()
passed = vals.isin(["pass","passed","yes","ok","✅"]).sum()
failed = vals.isin(["fail","failed","no","❌"]).sum()
partial = vals.isin(["partial","pending","tbd","?","⚠️"]).sum()
unknown = len(score) - passed - failed - partial

story.append(Paragraph("<b>Status summary</b>", styles["H2"]))
story.append(Paragraph(f"Passed: {passed} • Failed: {failed} • Partial/Pending: {partial} • Unset: {unknown}", styles["Body"]))
story.append(Spacer(1, 8))

table_data = [list(score.columns)] + score.astype(str).values.tolist()
tbl = Table(table_data, colWidths=[1.2*cm, 8.4*cm, 1.7*cm, 2.7*cm, 2.0*cm])
ts = TableStyle([
    ("BACKGROUND",(0,0),(-1,0), colors.HexColor("#003366")),
    ("TEXTCOLOR",(0,0),(-1,0), colors.white),
    ("GRID",(0,0),(-1,-1), 0.25, colors.grey),
    ("FONTNAME",(0,0),(-1,0), "Helvetica-Bold"),
    ("FONTSIZE",(0,0),(-1,0), 9),
    ("FONTSIZE",(0,1),(-1,-1), 8.2),
    ("VALIGN",(0,0),(-1,-1), "TOP"),
])
for r in range(1, len(table_data)):
    bg = gate_status_color(table_data[r][2])
    ts.add("BACKGROUND", (0,r), (-1,r), bg)
tbl.setStyle(ts)
story.append(tbl)
story.append(PageBreak())

story.append(Paragraph("Guidance", styles["H1"]))
story.append(Paragraph("Fill EvidenceLink with immutable artifacts. Bayesian gates require prior sensitivity reporting.", styles["Body"]))

from reportlab.pdfgen import canvas
def footer(c, doc):
    c.saveState()
    c.setFont("Helvetica", 9)
    c.setFillColor(colors.grey)
    c.drawString(2.0*cm, 1.1*cm, "HGP Scorecard Auto Report v4")
    c.drawRightString(A4[0]-2.0*cm, 1.1*cm, f"Page {doc.page}")
    c.restoreState()

doc.build(story, onFirstPage=footer, onLaterPages=footer)
print("Wrote", report_pdf)
