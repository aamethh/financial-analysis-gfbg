import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
import os

# ── Palette & config ─────────────────────────────────────────────────────────
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

YEARS  = ['2023', '2024', '2025']
XI     = list(range(len(YEARS)))

BLUE        = "#1B3A6B"
BLUE_LIGHT  = "#D6E4F0"
GOLD        = "#C8972B"
GOLD_LIGHT  = "#F5E6C8"
TEAL        = "#2E7D9A"
TEAL_LIGHT  = "#C9E8F0"
GRAY        = "#9CA3AF"
DARK        = "#1F2937"
SUBTITLE_C  = "#6B7280"

plt.rcParams.update({
    "font.family":      "sans-serif",
    "font.sans-serif":  ["Segoe UI", "Arial", "Helvetica", "DejaVu Sans"],
    "axes.facecolor":   "white",
    "figure.facecolor": "white",
})

# ── Load data ────────────────────────────────────────────────────────────────
df = pd.read_excel("data/gfbg_dataset.xlsx")
df.columns = ['Metrica', '2023', '2024', '2025', 'YoY']

def row(kw):
    return df.loc[df['Metrica'].str.contains(kw, case=False, na=False), YEARS].values[0].tolist()

activos    = row('Activos')
prestamos  = row('stamos')
depositos  = row('sit')
patrimonio = row('atrimonio')
utilidad   = row('tilidad')
aum        = row('AUM')

roe = [round(u / p * 100, 2) for u, p in zip(utilidad, patrimonio)]
roa = [round(u / a * 100, 2) for u, a in zip(utilidad, activos)]

# ── Helpers ──────────────────────────────────────────────────────────────────
def base_style(ax):
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.spines["bottom"].set_color("#E5E7EB")
    ax.yaxis.set_visible(False)
    ax.tick_params(axis="x", labelsize=13, labelcolor=GRAY, length=0)
    ax.set_xticks(XI)
    ax.set_xticklabels(YEARS)
    ax.set_xlim(-0.6, len(YEARS) - 0.4)

def add_header(fig, title, subtitle):
    fig.text(0.13, 0.97, title,    fontsize=16, fontweight="bold",   color=DARK,      va="top")
    fig.text(0.13, 0.90, subtitle, fontsize=11, fontweight="normal", color=SUBTITLE_C, va="top")

def label_bars(ax, vals, color=DARK, fmt="{:,.0f}", yoffset=0.015):
    ymax = max(vals)
    for i, v in enumerate(vals):
        ax.text(i, v + ymax * yoffset, fmt.format(v),
                ha="center", va="bottom", fontsize=13, fontweight="bold", color=color)

def label_line(ax, vals, color=DARK, fmt="{:.1f}%", yoffset=0.04):
    yspan = max(vals) - min(vals) if max(vals) != min(vals) else 1
    for i, v in enumerate(vals):
        ax.text(i, v + yspan * yoffset, fmt.format(v),
                ha="center", va="bottom", fontsize=13, fontweight="bold", color=color)

def save(fig, name):
    path = os.path.join(OUTPUT_DIR, name)
    fig.savefig(path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  saved -> {path}")

# ── 1. Total Assets ──────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 5), facecolor="white")
fig.subplots_adjust(top=0.80)
add_header(fig,
    "The bank is growing steadily",
    "Total assets increased from $18.9B to $21.1B in two years  (+11%)")

bars = ax.bar(XI, activos, color=[BLUE_LIGHT, BLUE_LIGHT, BLUE], width=0.5, zorder=3)
label_bars(ax, activos, color=BLUE, fmt="${:,.0f}M")
base_style(ax)
save(fig, "01_total_assets.png")

# ── 2. Gross Loans ───────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 5), facecolor="white")
fig.subplots_adjust(top=0.80)
add_header(fig,
    "Loan portfolio grows at a moderate pace",
    "Gross loans rose from $12.0B to $13.3B  (+10.9% cumulative)")

bars = ax.bar(XI, prestamos, color=[TEAL_LIGHT, TEAL_LIGHT, TEAL], width=0.5, zorder=3)
label_bars(ax, prestamos, color=TEAL, fmt="${:,.0f}M")
base_style(ax)
save(fig, "02_gross_loans.png")

# ── 3. Deposits ──────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 5), facecolor="white")
fig.subplots_adjust(top=0.80)
add_header(fig,
    "Customer deposits keep increasing",
    "Deposits grew from $12.6B to $14.6B  (+15.8% cumulative)")

bars = ax.bar(XI, depositos, color=[GOLD_LIGHT, GOLD_LIGHT, GOLD], width=0.5, zorder=3)
label_bars(ax, depositos, color=GOLD, fmt="${:,.0f}M")
base_style(ax)
save(fig, "03_deposits.png")

# ── 4. AUM ───────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 5), facecolor="white")
fig.subplots_adjust(top=0.80)
add_header(fig,
    "Managed assets are growing very fast",
    "AUM grew +37% in two years — this is the bank's fastest-growing segment")

bars = ax.bar(XI, aum, color=[GOLD_LIGHT, GOLD_LIGHT, GOLD], width=0.5, zorder=3)
label_bars(ax, aum, color=GOLD, fmt="${:,.0f}M")
base_style(ax)
save(fig, "04_aum.png")

# ── 5. ROE ───────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 5), facecolor="white")
fig.subplots_adjust(top=0.80)
add_header(fig,
    "The bank earns over 20% return for its shareholders — every year",
    "ROE above 20% is considered excellent. Most banks average 10-12%.")

ax.fill_between(XI, roe, alpha=0.12, color=TEAL, zorder=2)
ax.plot(XI, roe, color=TEAL, linewidth=3, marker="o", markersize=10,
        markerfacecolor="white", markeredgewidth=2.5, zorder=3)
ax.axhline(20, color="#E5E7EB", linewidth=1.5, linestyle="--", zorder=1)
ax.text(len(YEARS) - 0.55, 20.4, "World-class threshold: 20%",
        fontsize=9, color=GRAY, ha="right")

label_line(ax, roe, color=TEAL, fmt="{:.1f}%")

base_style(ax)
ax.set_ylim(min(roe) - 4, max(roe) + 4)
save(fig, "05_roe.png")

# ── 6. ROA ───────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 5), facecolor="white")
fig.subplots_adjust(top=0.80)
add_header(fig,
    "For every $100 in assets, the bank generates $4 in profit",
    "ROA above 1.5% is exceptional. This bank earns nearly 3x the sector average.")

ax.fill_between(XI, roa, alpha=0.12, color=GOLD, zorder=2)
ax.plot(XI, roa, color=GOLD, linewidth=3, marker="o", markersize=10,
        markerfacecolor="white", markeredgewidth=2.5, zorder=3)
ax.axhline(1.5, color="#E5E7EB", linewidth=1.5, linestyle="--", zorder=1)
ax.text(len(YEARS) - 0.55, 1.62, "Sector average: ~1.5%",
        fontsize=9, color=GRAY, ha="right")

label_line(ax, roa, color=GOLD, fmt="{:.2f}%")

base_style(ax)
ax.set_ylim(min(roa) - 1.5, max(roa) + 1.5)
save(fig, "06_roa.png")

# ── 7. Combined: AUM vs Loans vs Total Assets ────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 6), facecolor="white")
fig.subplots_adjust(top=0.80)
add_header(fig,
    "Managed money (AUM) is catching up to the bank's total size",
    "AUM grew 3x faster than loans — the business model is shifting toward asset management")

ax.plot(XI, activos,   color=BLUE, linewidth=3, marker="o", markersize=11,
        markerfacecolor="white", markeredgewidth=2.5, zorder=3, label="Total Assets")
ax.plot(XI, aum,       color=GOLD, linewidth=3.5, marker="o", markersize=11,
        markerfacecolor="white", markeredgewidth=2.5, zorder=3, label="AUM (managed money)")
ax.plot(XI, prestamos, color=TEAL, linewidth=2.5, marker="o", markersize=9,
        markerfacecolor="white", markeredgewidth=2.5, zorder=3, linestyle="--", label="Gross Loans")

ax.fill_between(XI, aum, prestamos, alpha=0.07, color=GOLD)

for i, (a, m, l) in enumerate(zip(activos, aum, prestamos)):
    offset = 500
    ax.text(i, a + offset, f"${a:,.0f}M", ha="center", va="bottom",
            fontsize=10, fontweight="bold", color=BLUE)
    ax.text(i, m + offset, f"${m:,.0f}M", ha="center", va="bottom",
            fontsize=10, fontweight="bold", color=GOLD)
    ax.text(i, l - offset * 3.5, f"${l:,.0f}M", ha="center", va="top",
            fontsize=10, fontweight="bold", color=TEAL)

p1 = mpatches.Patch(color=BLUE, label="Total Assets")
p2 = mpatches.Patch(color=GOLD, label="AUM  (managed money)")
p3 = mpatches.Patch(color=TEAL, label="Gross Loans")
ax.legend(handles=[p1, p2, p3], frameon=False, fontsize=10.5,
          loc="upper left", labelcolor=DARK)

ax.text(1.85, (aum[2] + activos[2]) / 2,
        "AUM nearly\nequals total assets",
        fontsize=8.5, color=GRAY, ha="center", style="italic")

base_style(ax)
ax.set_xlim(-0.5, len(YEARS) - 0.5)
ax.set_ylim(8000, 24000)
save(fig, "07_aum_vs_loans_vs_assets.png")

print("\nAll charts generated successfully.")
