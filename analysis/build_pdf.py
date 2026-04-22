from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image,
    HRFlowable, PageBreak, Table, TableStyle
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import KeepTogether
import datetime, os

# ── Paths ────────────────────────────────────────────────────────────────────
OUT   = "outputs/gfbg_equity_research.pdf"
IMGS  = "outputs"
W, H  = A4

# ── Color palette ────────────────────────────────────────────────────────────
NAVY     = colors.HexColor("#1B3A6B")
GOLD     = colors.HexColor("#C8972B")
TEAL     = colors.HexColor("#2E7D9A")
DARK     = colors.HexColor("#1F2937")
GRAY     = colors.HexColor("#6B7280")
LGRAY    = colors.HexColor("#F3F4F6")
WHITE    = colors.white
RED_SOFT = colors.HexColor("#DC2626")

# ── Styles ───────────────────────────────────────────────────────────────────
def S(name, **kw):
    base = {
        "fontName":   kw.pop("font", "Helvetica"),
        "fontSize":   kw.pop("size", 10),
        "textColor":  kw.pop("color", DARK),
        "leading":    kw.pop("leading", 14),
        "spaceAfter": kw.pop("after", 0),
        "spaceBefore":kw.pop("before", 0),
        "alignment":  kw.pop("align", TA_LEFT),
    }
    base.update(kw)
    return ParagraphStyle(name, **base)

cover_tag   = S("ct", font="Helvetica",      size=10,  color=GOLD,  align=TA_LEFT, after=4)
cover_title = S("ch", font="Helvetica-Bold", size=28,  color=WHITE, align=TA_LEFT, leading=34, after=6)
cover_sub   = S("cs", font="Helvetica",      size=12,  color=colors.HexColor("#CBD5E1"), align=TA_LEFT, after=4)
cover_meta  = S("cm", font="Helvetica",      size=9,   color=colors.HexColor("#94A3B8"), align=TA_LEFT)

sec_label   = S("sl", font="Helvetica-Bold", size=7,   color=GOLD,   after=4,  spaceBefore=2, letterSpacing=1.5)
sec_title   = S("st", font="Helvetica-Bold", size=18,  color=NAVY,   after=6,  leading=22)
body        = S("b",  font="Helvetica",      size=10,  color=DARK,   leading=16, after=4)
bullet_head = S("bh", font="Helvetica-Bold", size=11,  color=NAVY,   leading=15, after=2, leftIndent=12)
bullet_body = S("bb", font="Helvetica",      size=9.5, color=GRAY,   leading=14, after=10, leftIndent=24)
caption     = S("cap",font="Helvetica-Oblique", size=8.5, color=GRAY, after=14, align=TA_CENTER)
rating_txt  = S("rt", font="Helvetica-Bold", size=22,  color=TEAL,   align=TA_CENTER, after=4)
concl_body  = S("cb", font="Helvetica",      size=10.5,color=DARK,   leading=17, after=6, align=TA_CENTER)
risk_head   = S("rh", font="Helvetica-Bold", size=10,  color=RED_SOFT, after=2, leftIndent=12)
risk_body   = S("rb", font="Helvetica",      size=9.5, color=GRAY,   leading=14, after=10, leftIndent=24)
footer_s    = S("ft", font="Helvetica",      size=7.5, color=GRAY,   align=TA_CENTER)

DATE = datetime.date.today().strftime("%B %d, %Y")

# ── Cover page builder ───────────────────────────────────────────────────────
def cover_background(canvas, doc):
    canvas.saveState()
    # Full navy background
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    # Gold accent bar (left edge)
    canvas.setFillColor(GOLD)
    canvas.rect(0, 0, 0.45*cm, H, fill=1, stroke=0)
    # Bottom strip
    canvas.setFillColor(colors.HexColor("#0F2347"))
    canvas.rect(0, 0, W, 3.2*cm, fill=1, stroke=0)
    canvas.restoreState()

def inner_background(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(WHITE)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    # Left gold accent
    canvas.setFillColor(GOLD)
    canvas.rect(0, 0, 0.35*cm, H, fill=1, stroke=0)
    # Footer line
    canvas.setStrokeColor(colors.HexColor("#E5E7EB"))
    canvas.setLineWidth(0.5)
    canvas.line(2*cm, 1.6*cm, W - 2*cm, 1.6*cm)
    # Footer text
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(GRAY)
    canvas.drawString(2*cm, 1.1*cm, "Grupo Financiero BG — Equity Research")
    canvas.drawRightString(W - 2*cm, 1.1*cm, f"Confidential  |  {DATE}")
    canvas.restoreState()

# ── Image helper ─────────────────────────────────────────────────────────────
def chart(filename, width=15*cm, height=8.5*cm):
    path = os.path.join(IMGS, filename)
    return Image(path, width=width, height=height)

# ── Divider ──────────────────────────────────────────────────────────────────
def divider():
    return HRFlowable(width="100%", thickness=0.5,
                      color=colors.HexColor("#E5E7EB"), spaceAfter=12, spaceBefore=4)

def gold_rule():
    return HRFlowable(width=3*cm, thickness=2, color=GOLD, spaceAfter=10, spaceBefore=2)

# ── Build ─────────────────────────────────────────────────────────────────────
story = []

# ════════════════════════════════════════════════════════════════════════════
# PAGE 1 — COVER
# ════════════════════════════════════════════════════════════════════════════
doc = SimpleDocTemplate(
    OUT,
    pagesize=A4,
    leftMargin=2.5*cm, rightMargin=2*cm,
    topMargin=0, bottomMargin=3.5*cm,
)

story += [
    Spacer(1, 3.8*cm),
    Paragraph("EQUITY RESEARCH  /  FINANCIAL INSTITUTIONS", cover_tag),
    Spacer(1, 0.4*cm),
    Paragraph("Grupo Financiero BG", cover_title),
    Paragraph("Panama  |  Banking &amp; Asset Management", cover_sub),
    Spacer(1, 2.2*cm),
    HRFlowable(width="60%", thickness=0.8, color=GOLD, spaceAfter=16),
    Paragraph("Prepared by:  Ameth Espinosa — Financial Analyst Jr.", cover_meta),
    Paragraph(f"Date:  {DATE}", cover_meta),
    Paragraph("Classification:  Confidential", cover_meta),
    PageBreak(),
]

# ════════════════════════════════════════════════════════════════════════════
# PAGE 2 — INVESTMENT THESIS
# ════════════════════════════════════════════════════════════════════════════
story += [
    Spacer(1, 0.6*cm),
    Paragraph("01  /  INVESTMENT THESIS", sec_label),
    Paragraph("Why GFBG is a compelling investment", sec_title),
    gold_rule(),
    Spacer(1, 0.3*cm),

    Paragraph("1.  A bank transforming into an asset manager", bullet_head),
    Paragraph(
        "AUM grew +37% over two years and is approaching the total size of the bank's balance sheet. "
        "This structural shift unlocks higher-margin, capital-light revenue — a profile typical of "
        "top-tier wealth management firms, not traditional banks.",
        bullet_body),

    Paragraph("2.  Best-in-class profitability — sustained, not cyclical", bullet_head),
    Paragraph(
        "GFBG has delivered ROE above 20% for three consecutive years with a cost-to-income ratio "
        "of 28.1% — among the lowest in the region. This is not a one-time result. It reflects "
        "disciplined capital allocation and operating leverage built over time.",
        bullet_body),

    Paragraph("3.  Strong capital position with room to deploy", bullet_head),
    Paragraph(
        "A capital ratio of 27.2% — well above regulatory minimums — gives GFBG significant "
        "flexibility to grow organically or pursue strategic acquisitions without diluting shareholders.",
        bullet_body),

    Spacer(1, 0.6*cm),
    divider(),

    Paragraph("02  /  KEY CHARTS", sec_label),
    Paragraph("The story in four charts", sec_title),
    gold_rule(),
]

# Chart 1 — AUM vs Loans vs Assets (the hero chart)
story += [
    Spacer(1, 0.3*cm),
    chart("07_aum_vs_loans_vs_assets.png", width=16*cm, height=9*cm),
    Paragraph(
        "AUM is growing 3x faster than loans. By 2025, managed assets nearly equal the bank's entire balance sheet.",
        caption),
]

story.append(PageBreak())

# ════════════════════════════════════════════════════════════════════════════
# PAGE 3 — CHARTS (ROE + ROA)
# ════════════════════════════════════════════════════════════════════════════
story += [
    Spacer(1, 0.6*cm),
    Paragraph("02  /  KEY CHARTS (cont.)", sec_label),
    Spacer(1, 0.2*cm),
]

# ROE + ROA side by side via table
roe_img = chart("05_roe.png", width=7.8*cm, height=5.2*cm)
roa_img = chart("06_roa.png", width=7.8*cm, height=5.2*cm)

chart_table = Table(
    [[roe_img, roa_img]],
    colWidths=[8.1*cm, 8.1*cm],
)
chart_table.setStyle(TableStyle([("VALIGN", (0,0), (-1,-1), "TOP")]))
story.append(chart_table)

cap_table = Table(
    [[Paragraph("ROE held above 20% — three years in a row.", caption),
      Paragraph("ROA nearly 3x the sector average, consistently.", caption)]],
    colWidths=[8.1*cm, 8.1*cm],
)
story.append(cap_table)

story += [
    Spacer(1, 0.5*cm),
    chart("04_aum.png", width=16*cm, height=7*cm),
    Paragraph("AUM compound growth of +20.9% year-over-year — the fastest-growing segment in the business.", caption),
    Spacer(1, 0.4*cm),
    divider(),
]

# ════════════════════════════════════════════════════════════════════════════
# PAGE 4 — KEY INSIGHTS + RISKS + CONCLUSION
# ════════════════════════════════════════════════════════════════════════════
story.append(PageBreak())

story += [
    Spacer(1, 0.6*cm),
    Paragraph("03  /  KEY INSIGHTS", sec_label),
    Paragraph("What the numbers tell us", sec_title),
    gold_rule(),
    Spacer(1, 0.2*cm),
]

insights = [
    ("AUM dominance",
     "Managed assets reached $19.9B in 2025 — 94% of total balance sheet. "
     "GFBG is functionally converging with an asset manager."),
    ("ROE above 20% — three years straight",
     "Sustained profitability at this level is rare globally. "
     "It signals structural advantage, not a cyclical event."),
    ("Loan-to-Deposit ratio declining",
     "Down from 95% to 91%. The bank is becoming less reliant on credit "
     "and more focused on fee-based income — lower risk, more scalable."),
    ("Capital ratio of 27.2%",
     "Well above Basel III minimums. Strong buffer against credit losses "
     "and capacity to fund future growth without dilution."),
]

for head, detail in insights:
    story.append(Paragraph(f"‣  {head}", bullet_head))
    story.append(Paragraph(detail, bullet_body))

story += [
    Spacer(1, 0.4*cm),
    divider(),
    Spacer(1, 0.2*cm),
    Paragraph("04  /  RISK FACTORS", sec_label),
    Paragraph("What to watch", sec_title),
    gold_rule(),
    Spacer(1, 0.2*cm),
]

risks = [
    ("NPL coverage declining  (152.6% → 124.3%)",
     "Not critical at current levels, but the trend warrants monitoring. "
     "A sustained drop below 100% would signal asset quality deterioration."),
    ("AUM growth sustainability",
     "A +20.9% YoY AUM growth rate is exceptional — and hard to maintain. "
     "Slowing AUM growth would compress fee revenue and re-rate the stock."),
    ("Panama macro concentration",
     "The business is geographically concentrated. Any Panama-specific "
     "shock — fiscal, regulatory, or political — flows directly into results."),
]

for head, detail in risks:
    story.append(Paragraph(f"⚠  {head}", risk_head))
    story.append(Paragraph(detail, risk_body))

story += [
    divider(),
    Spacer(1, 0.3*cm),
    Paragraph("05  /  CONCLUSION", sec_label),
    Spacer(1, 0.5*cm),
]

# Rating box
rating_data = [[Paragraph("OUTPERFORM", rating_txt)]]
rating_box  = Table(rating_data, colWidths=[16*cm])
rating_box.setStyle(TableStyle([
    ("BACKGROUND",  (0,0), (-1,-1), colors.HexColor("#F0F9FF")),
    ("ROUNDEDCORNERS", [6]),
    ("BOX",         (0,0), (-1,-1), 1.5, TEAL),
    ("TOPPADDING",  (0,0), (-1,-1), 16),
    ("BOTTOMPADDING",(0,0),(-1,-1), 16),
]))
story.append(rating_box)
story += [
    Spacer(1, 0.5*cm),
    Paragraph(
        "GFBG is a rare combination: a highly profitable bank actively transitioning "
        "into an asset management platform. With ROE above 20%, AUM growing at nearly "
        "21% per year, and a capital ratio that provides ample runway — the risk/reward "
        "profile favors long-term investors with a 2-3 year horizon.",
        concl_body),
    Spacer(1, 1.2*cm),
    HRFlowable(width="40%", thickness=0.8, color=GOLD, spaceAfter=8),
    Paragraph("Ameth Espinosa  —  Financial Analyst Jr.", footer_s),
    Paragraph(f"Grupo Financiero BG Equity Research  |  {DATE}", footer_s),
]

# ── Render ───────────────────────────────────────────────────────────────────
page_fns = [cover_background, inner_background, inner_background, inner_background]

def on_page(canvas, doc):
    n = doc.page
    fn = page_fns[n - 1] if n <= len(page_fns) else inner_background
    fn(canvas, doc)

doc.build(story, onFirstPage=cover_background, onLaterPages=inner_background)
print(f"PDF generated -> {OUT}")
