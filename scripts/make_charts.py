"""Erzeugt die statischen Grafiken (PNG) für den Bericht im Repo."""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RH, RD = ROOT / "results" / "hourly", ROOT / "results" / "daily"
OUT = ROOT / "results" / "charts"
OUT.mkdir(parents=True, exist_ok=True)

# Referenzpalette (validiert, siehe dataviz-Skill): feste Reihenfolge, nie zyklisch
C = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
INK, INK2, MUTED, GRID, BASE, SURF = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7", "#fcfcfb"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": BASE, "axes.labelcolor": INK2,
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6,
    "axes.spines.top": False, "axes.spines.right": False, "figure.facecolor": SURF, "axes.facecolor": SURF,
    "legend.frameon": False, "axes.titleweight": "bold", "axes.titlesize": 11, "axes.titlecolor": INK,
})


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / name, dpi=150)
    plt.close(fig)


# 1) Ereignisstudie
SER = [("NDX", "Nasdaq 100"), ("BTC", "Bitcoin"), ("UST", "US-Staatsanleihen 30J"), ("GOLD", "Gold"), ("CHF", "Schweizer Franken"), ("JPY", "Yen")]
fig, axes = plt.subplots(1, 2, figsize=(12, 4.4), sharey=False)
for ax, nm, title in [(axes[0], "riskoff", "Nach einem Risk-off-Signal"), (axes[1], "riskon", "Nach einem Risk-on-Signal")]:
    p = pd.read_csv(RH / f"event_path_{nm}.csv", index_col=0)
    for i, (k, lab) in enumerate(SER):
        if k in p:
            ax.plot(p.index, p[k], color=C[i], lw=2, label=lab)
    ax.axvline(0, color=INK2, lw=1, ls="--")
    ax.axhline(0, color=BASE, lw=1)
    ax.set_title(title)
    ax.set_xlabel("Stunden relativ zum Signal (Signal = 0)")
    ax.set_ylabel("kumulierte Überrendite ggü. Normal-Drift (bps)")
    ax.text(0.5, 0.02, "links: Bewegung VOR dem Signal · rechts: was danach noch kommt", transform=ax.transAxes,
            ha="center", color=MUTED, fontsize=8)
axes[0].legend(loc="upper left", fontsize=8, ncol=2)
save(fig, "01_ereignisstudie.png")

# 2) Equity-Kurven der Referenzstrategien (netto)
eq = pd.read_csv(RH / "equity_curves_daily_cum.csv", index_col=0, parse_dates=True)
pick = [c for c in ["Nutzer-Idee: Gold+Bonds long / BTC+NDX short", "RF Basis (long Ziel, 4h, z2.5, EOD)",
                    "RF + Short Quelle", "RF Risk-off nur US-Sitzung", "Gegenhalten (IS-Optimum)"] if c in eq]
fig, ax = plt.subplots(figsize=(12, 4.6))
for i, c in enumerate(pick):
    ax.plot(eq.index, eq[c] * 100, color=C[i], lw=1.6, label=c)
ax.axvline(pd.Timestamp("2023-01-01"), color=INK2, lw=1, ls="--")
ax.text(pd.Timestamp("2023-01-15"), ax.get_ylim()[1] * 0.92, "Out-of-Sample →", color=INK2, fontsize=9)
ax.axhline(0, color=BASE, lw=1)
ax.set_title("Intraday-Rotationsstrategien nach Kosten (kumulierte Rendite in %, je Bein 5 % Risikobudget)")
ax.set_ylabel("kumulierte Rendite (%)")
ax.legend(fontsize=8, loc="upper left")
save(fig, "02_equity_intraday.png")

# 3) Latenz & Kosten
lc = pd.read_csv(RH / "latency_cost_sensitivity.csv")
fig, ax = plt.subplots(figsize=(7, 4))
for i, (cm, lab) in enumerate([(0.0, "ohne Kosten"), (1.0, "realistische Kosten"), (2.0, "doppelte Kosten")]):
    x = lc[lc.cost_mult == cm]
    ax.plot(x.delay_h, x.Sharpe, marker="o", ms=6, color=C[i], lw=2, label=lab)
ax.axhline(0, color=BASE, lw=1)
ax.set_xlabel("Verzögerung des Einstiegs (Stunden nach Signal)")
ax.set_ylabel("Sharpe Ratio")
ax.set_title("Rotation-Follower: Wirkung von Reaktionszeit und Kosten")
ax.legend(fontsize=8)
save(fig, "03_latenz_kosten.png")

# 4) Paar-Matrix (stündlich, 8h)
pm = pd.read_csv(RH / "pair_matrix.csv")
pm = pm[(pm.window == 8)]
keys = ["SPX", "NDX", "DAX", "NKY", "BTC", "ETH", "AUDJPY", "MXN", "COPPER", "OIL", "SILVER", "GOLD", "UST", "BUND", "JPY", "CHF", "USD"]
keys = [k for k in keys if k in set(pm.A) | set(pm.B)]
M = pd.DataFrame(np.nan, index=keys, columns=keys)
for _, r in pm.iterrows():
    if r.A in M.index and r.B in M.columns:
        M.loc[r.A, r.B] = r.Sharpe_netto
        M.loc[r.B, r.A] = r.Sharpe_netto
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402
cmap = LinearSegmentedColormap.from_list("div", ["#e34948", "#f0efec", "#2a78d6"])
fig, ax = plt.subplots(figsize=(9, 7.5))
lim = np.nanmax(np.abs(M.values))
im = ax.imshow(M.values, cmap=cmap, vmin=-lim, vmax=lim)
ax.set_xticks(range(len(keys)), keys, rotation=60)
ax.set_yticks(range(len(keys)), keys)
ax.grid(False)
for i in range(len(keys)):
    for j in range(len(keys)):
        v = M.values[i, j]
        if np.isfinite(v):
            ax.text(j, i, f"{v:.1f}", ha="center", va="center", fontsize=6.5, color=INK)
fig.colorbar(im, ax=ax, shrink=0.8, label="Sharpe netto (Folgen des Paar-Flows, 8h)")
ax.set_title("Welche Paar-Rotation lohnt sich intraday? (blau = Folgen profitabel, rot = Gegenhalten wäre besser)")
save(fig, "04_paar_matrix_intraday.png")

# 5) Muster-Häufigkeit pro Jahr (Tagesdaten)
fq = pd.read_csv(RD / "pattern_frequency_by_year.csv", index_col=0)
sel = [c for c in fq.columns if c.startswith(("Klassisches", "Zins", "Liquidation", "Sell America", "Liquiditätsrally"))]
fig, ax = plt.subplots(figsize=(12, 4.2))
for i, c in enumerate(sel):
    ax.plot(fq.index, fq[c], marker="o", ms=5, lw=2, color=C[i], label=c)
ax.set_title("Wie oft kommt welche Rotation vor? (Tage pro Jahr, Tagesdaten 2007–2026*)")
ax.set_ylabel("Tage pro Jahr")
ax.legend(fontsize=8, ncol=2)
ax.text(1.0, -0.12, "*2026 bis 9. Oktober", transform=ax.transAxes, ha="right", color=MUTED, fontsize=8)
save(fig, "05_muster_haeufigkeit.png")

# 6) Folgetag nach Mustern
ft = pd.read_csv(RD / "pattern_followthrough.csv")
ft = ft[ft.h_days == 1]
pv = ft.pivot(index="pattern", columns="asset", values="mean_pct")[["SPY", "QQQ", "TLT", "GLD", "JPY", "CHF", "USD", "OIL", "BTC"]]
fig, ax = plt.subplots(figsize=(10, 5.2))
lim = np.nanmax(np.abs(pv.values))
im = ax.imshow(pv.values, cmap=cmap, vmin=-lim, vmax=lim, aspect="auto")
ax.set_xticks(range(pv.shape[1]), pv.columns)
ax.set_yticks(range(pv.shape[0]), [s[:52] for s in pv.index], fontsize=8)
ax.grid(False)
for i in range(pv.shape[0]):
    for j in range(pv.shape[1]):
        ax.text(j, i, f"{pv.values[i, j]:+.2f}", ha="center", va="center", fontsize=7, color=INK)
fig.colorbar(im, ax=ax, shrink=0.8, label="mittlere Rendite am Folgetag (%)")
ax.set_title("Was passiert am Tag nach einer Rotation? (2007–2026)")
save(fig, "06_folgetag_muster.png")
print("Charts:", sorted(p.name for p in OUT.glob("*.png")))
