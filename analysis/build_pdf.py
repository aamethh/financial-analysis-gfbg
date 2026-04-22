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
OUT  = "outputs/gfbg_equity_research_v3.pdf"
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
    ("A bank transitioning into an asset manager",
     "AUM grew +37% over two years and now represents 94% of the balance sheet. "
     "The revenue mix is shifting toward capital-light fee income — "
     "structurally higher margins, lower credit risk, more predictable earnings."),
    ("Best-in-class profitability — structural, not cyclical",
     "ROE above 20% for three consecutive years, driven by a 28.1% cost-to-income ratio. "
     "That efficiency level is elite by any regional benchmark. "
     "It reflects operating leverage built into the model — not a one-year event."),
    ("Excess capital. Real optionality.",
     "Capital ratio of 27.2% — well above regulatory requirements. "
     "Management can grow organically, pursue acquisitions, or return capital. "
     "Each is accretive to shareholders at current valuations."),
]
for h, b in thesis:
    story += [Paragraph(f"‣  {h}", b_head), Paragraph(b, b_body)]

story += [
    Spacer(1, 0.3*cm), divider(),
    *section("02  /  KEY CHARTS", "The story in numbers"),
    chart("07_aum_vs_loans_vs_assets.png", w=15.5*cm, h=8.8*cm),
    Paragraph(
        "AUM grows 3x faster than loans. By 2025, managed assets nearly equal the entire balance sheet. "
        "The business model has fundamentally shifted.",
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
    ("AUM now equals 94% of the balance sheet",
     "Up from 76% in 2023. The pace of shift is accelerating — "
     "driven by higher-margin fee income replacing spread-dependent lending revenue."),
    ("ROE above 20% — three consecutive years",
     "Global banking peers average 10-12%. GFBG earns double. "
     "The gap is structural: elite cost control and a capital-light revenue mix."),
    ("Loan-to-Deposit ratio declining: 95% to 91%",
     "Less reliance on credit. More room for fee-based income. "
     "This shift lowers earnings volatility and improves the quality of revenue."),
    ("Capital ratio of 27.2% — real strategic flexibility",
     "No need to raise equity to fund growth. "
     "The bank can invest, acquire, or return capital — from existing resources."),
]
for h, b in insights:
    story += [Paragraph(f"‣  {h}", b_head), Paragraph(b, b_body)]

story += [
    Spacer(1, 0.2*cm), divider(),
    *section("04  /  VALUATION", "Is the stock cheap or expensive?"),
    Paragraph(
        "GFBG trades at a premium to regional peers. That premium is justified "
        "by structurally higher ROE and fee-based growth. Based on regional comparables:",
        S("vb", size=9.5, color=GRAY, leading=15, after=10)),
    valuation_table(),
    Spacer(1, 0.3*cm),
    Paragraph(
        "A P/B of ~2.2x sits above the peer range — but GFBG's ROE is nearly double the median. "
        "High-ROE franchises historically command a durable premium. "
        "If ROE remains above 20%, current multiples are sustainable. "
        "Downside risk is limited to a structural deterioration in AUM growth or margins.",
        S("vi", font="Helvetica-Oblique", size=9, color=GRAY, leading=14, after=0, left=8)),
    Spacer(1, 0.3*cm),
    divider(),
    PageBreak(),
]

# ── PAGE 5: CATALYSTS + RISKS + CONCLUSION ───────────────────────────────────
story += section("05  /  CATALYSTS", "What could drive the stock higher")

catalysts = [
    ("Continued AUM growth expands fee income",
     "Reducing earnings volatility and supporting multiple expansion. "
     "As fee income displaces interest income, the revenue profile becomes more predictable "
     "and deserves a higher valuation multiple."),
    ("Revenue mix shift structurally lifts margins",
     "Fee income carries no credit risk and scales with AUM — not with balance sheet size. "
     "Each percentage point shift in the mix improves ROE without additional capital deployment."),
    ("Wealth management penetration — underpenetrated market",
     "Private banking and family office services remain underpenetrated in Panama. "
     "GFBG's existing client base and regional brand create a low-cost path to capturing that demand."),
    ("Capital deployment: M&amp;A or geographic expansion",
     "A 27.2% capital ratio implies meaningful excess capital. "
     "A targeted acquisition or regional expansion would accelerate earnings growth "
     "without equity dilution at current valuations."),
]
for h, b in catalysts:
    story += [Paragraph(f"+ {h}", cat_h), Paragraph(b, cat_b)]

story += [
    divider(),
    *section("06  /  RISKS", "What could go wrong"),
]

risks = [
    ("NPL coverage declining: 152.6% to 124.3%",
     "Reserve levels are falling relative to non-performing loans. "
     "Not yet a concern — but a drop below 100% would signal a material deterioration in asset quality."),
    ("Sustained 20%+ AUM growth is unlikely long-term",
     "Slowing AUM growth compresses fee revenue and removes the primary re-rating catalyst. "
     "A normalization to 10-12% growth would pressure multiples."),
    ("Single-country exposure: Panama",
     "No geographic diversification. Fiscal deterioration, sovereign downgrade, "
     "or regulatory tightening flows directly into earnings with no external buffer."),
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
        "GFBG combines top-tier profitability with a structural shift toward asset management — "
        "a rare combination in regional banking. "
        "ROE above 20% is sustained. AUM is growing at nearly 21% per year. "
        "Capital is abundant. The business is becoming less capital-intensive and more profitable over time. "
        "Over a 2-3 year horizon, the primary return drivers are AUM expansion, "
        "margin improvement from the fee/spread mix shift, and disciplined capital deployment. "
        "Risk/reward is asymmetric to the upside. "
        "We maintain OUTPERFORM.",
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
