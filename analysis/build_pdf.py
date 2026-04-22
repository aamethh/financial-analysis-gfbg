from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image,
    HRFlowable, PageBreak, Table, TableStyle, KeepTogether
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
import datetime, os

# ── Paths ────────────────────────────────────────────────────────────────────
OUT  = "outputs/gfbg_equity_research_v2.pdf"
IMGS = "outputs"
W, H = A4

# ── Palette ──────────────────────────────────────────────────────────────────
NAVY      = colors.HexColor("#1B3A6B")
NAVY_DARK = colors.HexColor("#0F2347")
GOLD      = colors.HexColor("#C8972B")
GOLD_LIGHT= colors.HexColor("#FDF3E3")
TEAL      = colors.HexColor("#2E7D9A")
TEAL_LIGHT= colors.HexColor("#EBF6FA")
DARK      = colors.HexColor("#1F2937")
GRAY      = colors.HexColor("#6B7280")
LGRAY     = colors.HexColor("#F9FAFB")
MID_GRAY  = colors.HexColor("#E5E7EB")
RED       = colors.HexColor("#DC2626")
GREEN     = colors.HexColor("#16A34A")
WHITE     = colors.white

DATE = datetime.date.today().strftime("%B %d, %Y")

# ── Style factory ─────────────────────────────────────────────────────────────
def S(name, font="Helvetica", size=10, color=None, leading=None,
      after=0, before=0, align=TA_LEFT, left=0, **kw):
    return ParagraphStyle(
        name,
        fontName=font, fontSize=size,
        textColor=color or DARK,
        leading=leading or size * 1.4,
        spaceAfter=after, spaceBefore=before,
        alignment=align, leftIndent=left,
        **kw
    )

# Cover
cov_tag   = S("ct", size=9,  color=GOLD,  after=6)
cov_title = S("ch", font="Helvetica-Bold", size=30, color=WHITE, leading=36, after=8)
cov_sub   = S("cs", size=12, color=colors.HexColor("#CBD5E1"), after=6)
cov_meta  = S("cm", size=9,  color=colors.HexColor("#94A3B8"), after=3)

# Section headers
sec_lbl  = S("sl", font="Helvetica-Bold", size=7,  color=GOLD,  after=4, before=2)
sec_ttl  = S("st", font="Helvetica-Bold", size=17, color=NAVY,  after=4, leading=21)

# Body
body     = S("body", size=10, color=DARK, leading=16, after=4)
b_head   = S("bh", font="Helvetica-Bold", size=10.5, color=NAVY,  after=2, left=10)
b_body   = S("bb", size=9.5,  color=GRAY,  leading=15, after=9,  left=22)
caption  = S("cap", font="Helvetica-Oblique", size=8.5, color=GRAY, after=12, align=TA_CENTER)
risk_h   = S("rh", font="Helvetica-Bold", size=10,  color=RED,   after=2,  left=10)
risk_b   = S("rb", size=9.5,  color=GRAY,  leading=15, after=9,  left=22)
cat_h    = S("cah", font="Helvetica-Bold", size=10.5, color=TEAL, after=2, left=10)
cat_b    = S("cab", size=9.5, color=GRAY, leading=15, after=9, left=22)
val_cell = S("vc", font="Helvetica-Bold", size=10, color=NAVY, align=TA_CENTER, after=0)
val_sub  = S("vs", size=8.5, color=GRAY, align=TA_CENTER, after=0)
rating_s = S("rat", font="Helvetica-Bold", size=20, color=TEAL, align=TA_CENTER, after=4)
concl_s  = S("con", size=10.5, color=DARK, leading=17, after=6, align=TA_CENTER)
foot_s   = S("ft", size=7.5, color=GRAY, align=TA_CENTER)
snap_lbl = S("snl", size=8,  color=GRAY,  align=TA_CENTER, after=0)
snap_val = S("snv", font="Helvetica-Bold", size=13, color=NAVY, align=TA_CENTER, after=0)

# ── Page backgrounds ─────────────────────────────────────────────────────────
def cover_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    canvas.setFillColor(GOLD)
    canvas.rect(0, 0, 0.45*cm, H, fill=1, stroke=0)
    canvas.setFillColor(NAVY_DARK)
    canvas.rect(0, 0, W, 3*cm, fill=1, stroke=0)
    canvas.restoreState()

def inner_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(WHITE)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    canvas.setFillColor(GOLD)
    canvas.rect(0, 0, 0.35*cm, H, fill=1, stroke=0)
    canvas.setStrokeColor(MID_GRAY)
    canvas.setLineWidth(0.5)
    canvas.line(2*cm, 1.6*cm, W - 2*cm, 1.6*cm)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(GRAY)
    canvas.drawString(2*cm, 1.1*cm, "Grupo Financiero BG  —  Equity Research")
    canvas.drawRightString(W - 2*cm, 1.1*cm, f"Confidential  |  {DATE}")
    canvas.restoreState()

# ── Helpers ───────────────────────────────────────────────────────────────────
def chart(fname, w=15.5*cm, h=8.5*cm):
    return Image(os.path.join(IMGS, fname), width=w, height=h)

def divider():
    return HRFlowable(width="100%", thickness=0.5, color=MID_GRAY, spaceAfter=10, spaceBefore=4)

def gold_rule():
    return HRFlowable(width=2.5*cm, thickness=2, color=GOLD, spaceAfter=10, spaceBefore=2)

def section(label, title):
    return [
        Paragraph(label, sec_lbl),
        Paragraph(title, sec_ttl),
        gold_rule(),
        Spacer(1, 0.2*cm),
    ]

# ── Metrics snapshot box ──────────────────────────────────────────────────────
def metrics_snapshot():
    metrics = [
        ("ROE", ">20%",   "Return on equity"),
        ("ROA", "~4%",    "Return on assets"),
        ("AUM Growth", "+20.9%", "Year-over-year"),
        ("Capital Ratio", "27.2%", "Well above min."),
        ("Loan/Deposit", "91%",   "Down from 95%"),
    ]
    header = [[Paragraph("KEY METRICS SNAPSHOT", S("smh", font="Helvetica-Bold",
               size=8, color=GOLD, align=TA_CENTER))]]
    rows   = [[
        Table([[Paragraph(v, snap_val)], [Paragraph(lbl, snap_lbl)], [Paragraph(sub, val_sub)]],
              colWidths=[2.8*cm])
        for lbl, v, sub in metrics
    ]]

    inner = Table(header + rows, colWidths=[15.5*cm])
    inner.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), NAVY),
        ("TOPPADDING",   (0,0), (-1,0), 8),
        ("BOTTOMPADDING",(0,0), (-1,0), 8),
        ("BACKGROUND",   (0,1), (-1,-1), LGRAY),
        ("TOPPADDING",   (0,1), (-1,-1), 10),
        ("BOTTOMPADDING",(0,1), (-1,-1), 10),
        ("BOX",          (0,0), (-1,-1), 1, MID_GRAY),
        ("LINEBELOW",    (0,0), (-1,0), 0.5, GOLD),
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
    ]))
    return inner

# ── Valuation table ───────────────────────────────────────────────────────────
def valuation_table():
    headers = ["Metric", "GFBG (Est.)", "Regional Peers", "Read"]
    rows = [
        ["P/B  (Price / Book)", "~2.2x", "1.0x – 1.8x", "Premium — justified by ROE"],
        ["P/E  (Price / Earnings)", "~12x", "9x – 14x",  "Fairly valued to slight premium"],
        ["ROE", "20.8%", "8% – 14%",    "Best-in-class"],
        ["AUM Growth (YoY)", "+20.9%", "+5% – +12%",   "Significantly above peers"],
    ]

    col_w = [4.2*cm, 3.2*cm, 3.5*cm, 4.6*cm]
    data  = [headers] + rows
    t = Table(data, colWidths=col_w)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), NAVY),
        ("TEXTCOLOR",     (0,0), (-1,0), WHITE),
        ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,0), 9),
        ("TOPPADDING",    (0,0), (-1,0), 8),
        ("BOTTOMPADDING", (0,0), (-1,0), 8),
        ("ALIGN",         (0,0), (-1,0), "CENTER"),

        ("FONTNAME",      (0,1), (-1,-1), "Helvetica"),
        ("FONTSIZE",      (0,1), (-1,-1), 9),
        ("TEXTCOLOR",     (0,1), (0,-1), DARK),
        ("TEXTCOLOR",     (1,1), (-1,-1), GRAY),
        ("FONTNAME",      (1,1), (1,-1), "Helvetica-Bold"),
        ("TEXTCOLOR",     (1,1), (1,-1), TEAL),
        ("ALIGN",         (1,0), (-1,-1), "CENTER"),
        ("ALIGN",         (-1,1),(-1,-1), "LEFT"),

        ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, LGRAY]),
        ("TOPPADDING",    (0,1), (-1,-1), 7),
        ("BOTTOMPADDING", (0,1), (-1,-1), 7),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("BOX",           (0,0), (-1,-1), 0.8, MID_GRAY),
        ("LINEBELOW",     (0,0), (-1,0),  1,   GOLD),
        ("INNERGRID",     (0,1), (-1,-1), 0.3, MID_GRAY),
    ]))
    return t

# ════════════════════════════════════════════════════════════════════════════
# BUILD
# ════════════════════════════════════════════════════════════════════════════
doc = SimpleDocTemplate(
    OUT, pagesize=A4,
    leftMargin=2.5*cm, rightMargin=2*cm,
    topMargin=0, bottomMargin=3.5*cm,
)

story = []

# ── PAGE 1: COVER ─────────────────────────────────────────────────────────────
story += [
    Spacer(1, 3.6*cm),
    Paragraph("EQUITY RESEARCH  /  FINANCIAL INSTITUTIONS", cov_tag),
    Spacer(1, 0.3*cm),
    Paragraph("Grupo Financiero BG", cov_title),
    Paragraph("Panama  |  Banking &amp; Asset Management", cov_sub),
    Spacer(1, 1.6*cm),
    HRFlowable(width="55%", thickness=0.8, color=GOLD, spaceAfter=14),
    Spacer(1, 0.2*cm),
    metrics_snapshot(),
    Spacer(1, 1.4*cm),
    HRFlowable(width="55%", thickness=0.5, color=colors.HexColor("#2D4E7A"), spaceAfter=12),
    Paragraph("Prepared by:  Ameth Espinosa  —  Financial Analyst Jr.", cov_meta),
    Paragraph(f"Date:  {DATE}", cov_meta),
    Paragraph("Classification:  Confidential  |  For Institutional Use Only", cov_meta),
    PageBreak(),
]

# ── PAGE 2: THESIS + HERO CHART ───────────────────────────────────────────────
story += section("01  /  INVESTMENT THESIS", "Why GFBG stands out")

thesis = [
    ("A bank becoming an asset manager",
     "AUM grew +37% in two years and is nearly the size of the entire balance sheet. "
     "This shift brings higher margins, less credit risk, and more predictable revenue — "
     "a business model closer to a wealth manager than a traditional bank."),
    ("Profitability that holds — year after year",
     "ROE above 20% for three straight years. A cost-to-income ratio of 28.1% is among "
     "the best in the region. This is not a one-time result — it is structural."),
    ("Strong capital with room to grow",
     "Capital ratio of 27.2% — well above what regulators require. "
     "The bank can grow, acquire, or return capital to shareholders without strain."),
]
for h, b in thesis:
    story += [Paragraph(f"‣  {h}", b_head), Paragraph(b, b_body)]

story += [
    Spacer(1, 0.3*cm), divider(),
    *section("02  /  KEY CHARTS", "The story in numbers"),
    chart("07_aum_vs_loans_vs_assets.png", w=15.5*cm, h=8.8*cm),
    Paragraph(
        "Managed money (AUM) is growing 3x faster than loans. "
        "By 2025, AUM nearly equals the bank's total assets — a structural shift in the business.",
        caption),
    PageBreak(),
]

# ── PAGE 3: ROE / ROA / AUM CHARTS ───────────────────────────────────────────
story += [
    Spacer(1, 0.5*cm),
    *section("02  /  KEY CHARTS (cont.)", ""),
]

roe_img = chart("05_roe.png",  w=7.6*cm, h=5.2*cm)
roa_img = chart("06_roa.png",  w=7.6*cm, h=5.2*cm)
side = Table([[roe_img, roa_img]], colWidths=[8*cm, 8*cm])
side.setStyle(TableStyle([("VALIGN", (0,0), (-1,-1), "TOP")]))
story.append(side)

cap = Table(
    [[Paragraph("ROE above 20% — held for three consecutive years.", caption),
      Paragraph("ROA at 4% — nearly 3x the regional banking average.", caption)]],
    colWidths=[8*cm, 8*cm])
story.append(cap)

story += [
    Spacer(1, 0.3*cm),
    chart("04_aum.png", w=15.5*cm, h=6.8*cm),
    Paragraph(
        "AUM grew from $14.4B to $19.9B in two years — the fastest-growing segment in the business.",
        caption),
    Spacer(1, 0.3*cm),
    divider(),
    PageBreak(),
]

# ── PAGE 4: INSIGHTS + VALUATION ─────────────────────────────────────────────
story += section("03  /  KEY INSIGHTS", "What the numbers tell us")

insights = [
    ("AUM is approaching the size of the whole bank",
     "At $19.9B, managed assets are now 94% of total assets. "
     "In 2023 that number was 76%. The shift is fast and consistent."),
    ("ROE above 20% — three years in a row",
     "Most banks globally earn 10-12% ROE. GFBG earns double. "
     "That gap reflects a better business mix and tighter cost control."),
    ("The bank is lending less relative to deposits",
     "Loan-to-deposit ratio fell from 95% to 91%. "
     "Less reliance on credit means lower risk and more room for fee income."),
    ("Capital buffer is very strong",
     "At 27.2%, the capital ratio gives the bank flexibility to invest, "
     "expand, or absorb shocks — without needing to raise money from investors."),
]
for h, b in insights:
    story += [Paragraph(f"‣  {h}", b_head), Paragraph(b, b_body)]

story += [
    Spacer(1, 0.2*cm), divider(),
    *section("04  /  VALUATION", "Is the stock cheap or expensive?"),
    Paragraph(
        "Based on publicly available data and regional comparables, GFBG trades at a modest premium to peers. "
        "Given its superior ROE and AUM growth, that premium is justified.",
        S("vb", size=9.5, color=GRAY, leading=15, after=10)),
    valuation_table(),
    Spacer(1, 0.3*cm),
    Paragraph(
        "A P/B of ~2.2x is above the regional average, but GFBG's ROE is also nearly double the peer median. "
        "High-ROE banks historically command a premium. At current levels, the valuation reflects quality — "
        "not speculation.",
        S("vi", font="Helvetica-Oblique", size=9, color=GRAY, leading=14, after=0, left=8)),
    Spacer(1, 0.3*cm),
    divider(),
    PageBreak(),
]

# ── PAGE 5: CATALYSTS + RISKS + CONCLUSION ───────────────────────────────────
story += section("05  /  CATALYSTS", "What could drive the stock higher")

catalysts = [
    ("AUM growth accelerates fee income",
     "Each dollar of new AUM generates management fees with no credit risk attached. "
     "As AUM approaches and exceeds the loan book, fee income becomes the dominant revenue driver."),
    ("Business mix shift improves margins",
     "Moving from interest income (spread-dependent) to fee income (volume-dependent) "
     "structurally improves net margins and reduces sensitivity to interest rate cycles."),
    ("Expansion of wealth management services",
     "GFBG has the client base and brand to deepen penetration in private banking and "
     "family office services — both high-margin segments with strong regional demand."),
    ("Capital deployment: M&A or regional expansion",
     "With a 27.2% capital ratio, the bank has dry powder. A strategic acquisition or "
     "geographic expansion into neighboring markets would accelerate growth without dilution."),
]
for h, b in catalysts:
    story += [Paragraph(f"+ {h}", cat_h), Paragraph(b, cat_b)]

story += [
    divider(),
    *section("06  /  RISKS", "What could go wrong"),
]

risks = [
    ("NPL coverage is declining  (152.6% -> 124.3%)",
     "The bank is setting aside less money to cover potential loan losses. "
     "Not a problem today, but worth monitoring. A drop below 100% would be a red flag."),
    ("AUM growth may slow",
     "Growing AUM at +20.9% per year is hard to sustain indefinitely. "
     "If growth slows significantly, fee revenue projections come down and the stock re-rates."),
    ("Panama concentration risk",
     "Almost all revenue comes from Panama. A local recession, political instability, "
     "or regulatory change would hit the bank directly with no geographic buffer."),
]
for h, b in risks:
    story += [Paragraph(f"! {h}", risk_h), Paragraph(b, risk_b)]

story += [
    divider(),
    *section("07  /  CONCLUSION", "Our view"),
]

# Rating box
r_box = Table([[Paragraph("OUTPERFORM", rating_s)]], colWidths=[15.5*cm])
r_box.setStyle(TableStyle([
    ("BACKGROUND",   (0,0), (-1,-1), TEAL_LIGHT),
    ("BOX",          (0,0), (-1,-1), 1.5, TEAL),
    ("TOPPADDING",   (0,0), (-1,-1), 14),
    ("BOTTOMPADDING",(0,0), (-1,-1), 14),
]))
story.append(r_box)
story += [
    Spacer(1, 0.5*cm),
    Paragraph(
        "GFBG is one of the most profitable banks in the region — and it is actively transforming "
        "into something more valuable: an asset management platform with a banking license. "
        "With ROE above 20%, AUM growing at nearly 21% per year, and a capital ratio that provides "
        "real strategic flexibility, the risk/reward profile is compelling. "
        "We see the primary drivers over a 2-3 year horizon as continued AUM expansion, "
        "margin improvement from the fee/spread revenue mix shift, and disciplined capital deployment. "
        "Maintain OUTPERFORM.",
        concl_s),
    Spacer(1, 1*cm),
    HRFlowable(width="35%", thickness=0.8, color=GOLD, spaceAfter=8),
    Paragraph("Ameth Espinosa  —  Financial Analyst Jr.", foot_s),
    Paragraph(f"Grupo Financiero BG  |  Equity Research  |  {DATE}", foot_s),
    Paragraph("This report is for informational purposes only and does not constitute investment advice.", foot_s),
]

# ── Render ────────────────────────────────────────────────────────────────────
doc.build(story, onFirstPage=cover_bg, onLaterPages=inner_bg)
print(f"PDF generated -> {OUT}")
