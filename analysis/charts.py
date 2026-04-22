import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os

# ── Config ──────────────────────────────────────────────────────────────────
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

YEARS = ['2023', '2024', '2025']
BLUE  = "#1B3A6B"
GOLD  = "#C8972B"
TEAL  = "#2E7D9A"
GRAY  = "#6B7280"

FONT_TITLE  = {"fontsize": 14, "fontweight": "bold", "color": "#111827"}
FONT_LABEL  = {"fontsize": 10, "color": GRAY}
FONT_TICK   = {"labelsize": 9,  "labelcolor": GRAY}

def base_style(ax, title, ylabel):
    ax.set_title(title, pad=14, **FONT_TITLE)
    ax.set_ylabel(ylabel, **FONT_LABEL)
    ax.set_xticks(range(len(YEARS)))
    ax.set_xticklabels(YEARS)
    ax.tick_params(axis="both", **FONT_TICK)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#D1D5DB")
    ax.yaxis.grid(True, color="#F3F4F6", linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)

def add_value_labels(ax, rects, fmt="{:,.0f}"):
    for rect in rects:
        h = rect.get_height()
        ax.annotate(
            fmt.format(h),
            xy=(rect.get_x() + rect.get_width() / 2, h),
            xytext=(0, 6), textcoords="offset points",
            ha="center", va="bottom", fontsize=8.5, color="#374151"
        )

def save(fig, name):
    path = os.path.join(OUTPUT_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  saved -> {path}")

# ── Load data ────────────────────────────────────────────────────────────────
df = pd.read_excel("data/gfbg_dataset.xlsx")
df.columns = ['Metrica', '2023', '2024', '2025', 'YoY']

def row(keyword):
    return df.loc[df['Metrica'].str.contains(keyword, case=False, na=False), YEARS].values[0].tolist()

activos   = row('Activos')
prestamos = row('stamos')
depositos = row('sit')
patrimonio= row('atrimonio')
utilidad  = row('tilidad')
aum       = row('AUM')

roe = [round(u / p * 100, 2) for u, p in zip(utilidad, patrimonio)]
roa = [round(u / a * 100, 2) for u, a in zip(utilidad, activos)]

x = range(len(YEARS))

# ── 1. Total Assets ──────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 4.5), facecolor="white")
bars = ax.bar(x, activos, color=BLUE, width=0.5, zorder=3)
base_style(ax, "Total Assets (USD Millions)", "USD Millions")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
add_value_labels(ax, bars)
save(fig, "01_total_assets.png")

# ── 2. Gross Loans ───────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 4.5), facecolor="white")
bars = ax.bar(x, prestamos, color=TEAL, width=0.5, zorder=3)
base_style(ax, "Gross Loans (USD Millions)", "USD Millions")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
add_value_labels(ax, bars)
save(fig, "02_gross_loans.png")

# ── 3. Deposits ──────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 4.5), facecolor="white")
bars = ax.bar(x, depositos, color=GOLD, width=0.5, zorder=3)
base_style(ax, "Total Deposits (USD Millions)", "USD Millions")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
add_value_labels(ax, bars)
save(fig, "03_deposits.png")

# ── 4. AUM ───────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 4.5), facecolor="white")
bars = ax.bar(x, aum, color=BLUE, width=0.5, zorder=3)
base_style(ax, "Assets Under Management — AUM (USD Millions)", "USD Millions")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
add_value_labels(ax, bars)
save(fig, "04_aum.png")

# ── 5. ROE ───────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 4.5), facecolor="white")
bars = ax.bar(x, roe, color=TEAL, width=0.5, zorder=3)
ax.axhline(20, color="#E5E7EB", linewidth=1.2, linestyle="--", zorder=2)
ax.text(2.55, 20.3, "20% threshold", fontsize=8, color=GRAY)
base_style(ax, "Return on Equity — ROE (%)", "%")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:.1f}%"))
add_value_labels(ax, bars, fmt="{:.2f}%")
save(fig, "05_roe.png")

# ── 6. ROA ───────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 4.5), facecolor="white")
bars = ax.bar(x, roa, color=GOLD, width=0.5, zorder=3)
ax.axhline(1.5, color="#E5E7EB", linewidth=1.2, linestyle="--", zorder=2)
ax.text(2.55, 1.55, "Sector avg ~1.5%", fontsize=8, color=GRAY)
base_style(ax, "Return on Assets — ROA (%)", "%")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:.2f}%"))
add_value_labels(ax, bars, fmt="{:.2f}%")
save(fig, "06_roa.png")

# ── 7. Combined: AUM vs Loans vs Total Assets ────────────────────────────────
width = 0.25
fig, ax = plt.subplots(figsize=(9, 5.5), facecolor="white")

xi = [i - width for i in x]
xj = list(x)
xk = [i + width for i in x]

b1 = ax.bar(xi, activos,   width=width, color=BLUE,  label="Total Assets", zorder=3)
b2 = ax.bar(xj, aum,       width=width, color=GOLD,  label="AUM",          zorder=3)
b3 = ax.bar(xk, prestamos, width=width, color=TEAL,  label="Gross Loans",  zorder=3)

for bars in [b1, b2, b3]:
    add_value_labels(ax, bars)

base_style(ax, "AUM vs. Gross Loans vs. Total Assets (USD Millions)", "USD Millions")
ax.set_xticks(list(x))
ax.set_xticklabels(YEARS)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
ax.legend(frameon=False, fontsize=9)
save(fig, "07_aum_vs_loans_vs_assets.png")

print("\nAll charts generated successfully.")
