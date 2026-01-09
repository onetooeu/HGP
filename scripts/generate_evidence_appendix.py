"""Generate an Evidence Appendix PDF from the scorecard CSV.

- Reads: docs/HGP_Falsification_Scorecard.csv (from a selected pack)
- Collects: any local file paths in EvidenceLink (if they exist) and lists them
- Writes: out/HGP_Evidence_Appendix.pdf

Note: This does not embed images automatically (safe + robust); it produces a structured appendix with links/paths.
"""
from pathlib import Path
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib import colors

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "out"
OUT.mkdir(exist_ok=True)

# user selects which pack's scorecard to use
score_path = ROOT / "packs" / "v4" / "docs" / "HGP_Falsification_Scorecard.csv"
if not score_path.exists():
    score_path = ROOT / "packs" / "v3" / "docs" / "HGP_Falsification_Scorecard.csv"

score = pd.read_csv(score_path).fillna("")

styles = getSampleStyleSheet()
doc = SimpleDocTemplate(str(OUT / "HGP_Evidence_Appendix.pdf"), pagesize=A4,
                        leftMargin=2.0*cm, rightMargin=2.0*cm, topMargin=1.7*cm, bottomMargin=1.6*cm)

story = []
story.append(Paragraph("HGP Evidence Appendix (auto-generated)", styles["Title"]))
story.append(Paragraph(f"Source scorecard: {score_path}", styles["BodyText"]))
story.append(Spacer(1, 10))

rows = [["Gate","PassFail","EvidenceLink","Exists?","Notes"]]
for _, r in score.iterrows():
    link = str(r.get("EvidenceLink","")).strip()
    exists = ""
    if link:
        p = (ROOT / link).resolve() if not Path(link).is_absolute() else Path(link)
        exists = "yes" if p.exists() else "no"
    rows.append([str(r.get("Gate","")), str(r.get("PassFail","")), link, exists, str(r.get("Notes",""))[:180]])

tbl = Table(rows, colWidths=[1.2*cm, 1.6*cm, 7.8*cm, 1.3*cm, 3.1*cm])
tbl.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0), colors.HexColor("#003366")),
    ("TEXTCOLOR",(0,0),(-1,0), colors.white),
    ("GRID",(0,0),(-1,-1), 0.25, colors.grey),
    ("FONTNAME",(0,0),(-1,0), "Helvetica-Bold"),
    ("FONTSIZE",(0,0),(-1,0), 9),
    ("FONTSIZE",(0,1),(-1,-1), 8),
    ("VALIGN",(0,0),(-1,-1), "TOP"),
]))
story.append(tbl)
doc.build(story)
print("Wrote", OUT/"HGP_Evidence_Appendix.pdf")
