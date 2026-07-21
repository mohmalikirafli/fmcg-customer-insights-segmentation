"""Build concise PDF report and executive summary from generated results."""
from pathlib import Path
import json
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "04_Output" / "figures"
TAB = ROOT / "04_Output" / "tables"
metrics = json.loads((TAB / "key_metrics.json").read_text())
segments = pd.read_csv(TAB / "segment_sizes.csv")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="TitleBlue", parent=styles["Title"], fontSize=22, leading=27, textColor=colors.HexColor("#0067B1")))
styles.add(ParagraphStyle(name="H1Blue", parent=styles["Heading1"], fontSize=16, textColor=colors.HexColor("#0067B1")))
styles.add(ParagraphStyle(name="BodyClean", parent=styles["BodyText"], fontSize=9.5, leading=14))

report_path = ROOT / "01_Report" / "FMCG_Customer_Insights_Report.pdf"
report_path.parent.mkdir(parents=True, exist_ok=True)
doc = SimpleDocTemplate(str(report_path), pagesize=A4, rightMargin=1.7*cm, leftMargin=1.7*cm, topMargin=1.5*cm, bottomMargin=1.5*cm)
story = [
    Paragraph("FMCG Customer Insights:<br/>Consumer Segmentation and Purchase Drivers", styles["TitleBlue"]),
    Paragraph("<b>Author:</b> Mohammad Maliki Rafli<br/><b>Program:</b> Master of Public Health - Biostatistics and Health Data Science, Universitas Airlangga", styles["BodyClean"]),
    Paragraph("<b>Disclosure:</b> Fully synthetic data; results are portfolio demonstrations, not market estimates.", styles["BodyClean"]),
    Spacer(1, 10),
    Paragraph("Executive Summary", styles["H1Blue"]),
    Paragraph(f"The analysis used {metrics['n_respondents']} synthetic FMCG consumer profiles, identified four actionable segments, and modeled high new-product intention. The four-cluster silhouette score was {metrics['silhouette_score_k4']:.3f}; holdout ROC-AUC was {metrics['test_roc_auc']:.3f} and accuracy was {metrics['test_accuracy']:.3f}.", styles["BodyClean"]),
]
metric_rows = [["Metric", "Result"], ["Consumers", f"{metrics['n_respondents']:,}"], ["Segments", "4"], ["Cronbach alpha", f"{metrics['minimum_cronbach_alpha']:.3f}-{metrics['maximum_cronbach_alpha']:.3f}"], ["ROC-AUC", f"{metrics['test_roc_auc']:.3f}"], ["Accuracy", f"{metrics['test_accuracy']:.3f}"], ["Median spend", f"IDR {metrics['median_monthly_spend_idr']:,}"]]
table = Table(metric_rows, colWidths=[9*cm, 6*cm])
table.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), colors.HexColor("#0067B1")), ("TEXTCOLOR", (0,0), (-1,0), colors.white), ("GRID", (0,0), (-1,-1), 0.4, colors.grey), ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"), ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#F2F7FC")])]))
story += [table, PageBreak(), Paragraph("Consumer Segments", styles["H1Blue"])]
segment_rows = [["Segment", "Share"]] + [[row.segment, f"{row.share_pct:.1f}%"] for row in segments.itertuples()]
segment_table = Table(segment_rows, colWidths=[11*cm, 4*cm])
segment_table.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), colors.HexColor("#0067B1")), ("TEXTCOLOR", (0,0), (-1,0), colors.white), ("GRID", (0,0), (-1,-1), 0.4, colors.grey), ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold")]))
story += [segment_table, Spacer(1, 12), Image(str(FIG / "02_segment_profile_heatmap.png"), width=16*cm, height=8*cm), PageBreak(), Paragraph("Channel and Purchase-Intention Evidence", styles["H1Blue"]), Image(str(FIG / "03_channel_by_segment.png"), width=16*cm, height=8.5*cm), Spacer(1, 8), Image(str(FIG / "07_purchase_intention_roc_curve.png"), width=10*cm, height=8*cm), Paragraph("Model coefficients are adjusted associations and must not be interpreted causally.", styles["BodyClean"])]
doc.build(story)

presentation_path = ROOT / "05_Presentation" / "FMCG_Customer_Insights_Executive_Summary.pdf"
presentation_path.parent.mkdir(parents=True, exist_ok=True)
W, H = landscape(A4)
c = canvas.Canvas(str(presentation_path), pagesize=(W, H))
blue = colors.HexColor("#0067B1")
light = colors.HexColor("#EAF4FC")
dark = colors.HexColor("#263238")

def page(title, subtitle=""):
    c.setFillColor(light); c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColor(blue); c.setFont("Helvetica-Bold", 25); c.drawString(42, H-58, title)
    c.setFillColor(dark); c.setFont("Helvetica", 12); c.drawString(44, H-82, subtitle)

def bullets(items, x=55, y=None):
    y = y or H-125
    c.setFillColor(dark); c.setFont("Helvetica", 13)
    for item in items:
        c.drawString(x, y, "• " + item); y -= 28

page("FMCG Customer Insights", "Consumer Segmentation and Purchase Drivers")
bullets(["800 synthetic consumer profiles", "Four actionable segments", "Holdout ROC-AUC 0.849", "Recommendations for innovation, retention, premium growth, and value strategy"], y=H-145)
c.showPage()
page("Four Actionable Consumer Segments", "Balanced segment shares with distinct motivations")
c.drawImage(str(FIG / "02_segment_profile_heatmap.png"), 45, 65, width=520, height=280, preserveAspectRatio=True)
bullets(["Value Seekers: bundles and visible value", "Convenience Loyalists: availability and easy repurchase", "Digital Trend Explorers: social discovery and trials", "Quality & Wellness Enthusiasts: credible premium benefits"], x=590, y=H-135)
c.showPage()
page("Channel Behavior", "Shopping channels differ meaningfully across segments")
c.drawImage(str(FIG / "03_channel_by_segment.png"), 45, 65, width=560, height=300, preserveAspectRatio=True)
bullets(["55.7% of Digital Trend Explorers use e-commerce", "49.0% of Convenience Loyalists use minimarkets", "Value Seekers have the strongest traditional-market presence"], x=620, y=H-145)
c.showPage()
page("Purchase-Intention Model", f"Holdout ROC-AUC {metrics['test_roc_auc']:.3f} | Accuracy {metrics['test_accuracy']:.3f}")
c.drawImage(str(FIG / "05_purchase_intention_drivers.png"), 40, 65, width=480, height=300, preserveAspectRatio=True)
c.drawImage(str(FIG / "07_purchase_intention_roc_curve.png"), 545, 80, width=250, height=230, preserveAspectRatio=True)
c.showPage()
page("Recommended Activation", "Translate segments into measurable commercial actions")
bullets(["Digital Trend Explorers: creator seeding, reviews, social commerce", "Quality & Wellness Enthusiasts: evidence-led benefits and transparency", "Convenience Loyalists: availability, trust, frictionless repurchase", "Value Seekers: pack-price architecture, bundles, targeted promotions", "Validate all hypotheses using observed market data"], y=H-135)
c.save()
print(report_path)
print(presentation_path)
