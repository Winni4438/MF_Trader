"""Grafiken für den Folgebericht 'Überhitzung und relative Mean Reversion'."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / "results"
OUT = R / "charts_meanrev"
OUT.mkdir(parents=True, exist_ok=True)
C = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
INK, INK2, MUTED, GRID, BASE, SURF = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7", "#fcfcfb"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": BASE, "axes.labelcolor": INK2,
                     "xtick.color": MUTED, "ytick.color": MUTED, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6,
                     "axes.spines.top": False, "axes.spines.right": False, "figure.facecolor": SURF, "axes.facecolor": SURF,
                     "legend.frameon": False, "axes.titleweight": "bold", "axes.titlesize": 11, "axes.titlecolor": INK})
DIV = LinearSegmentedColormap.from_list("div", ["#e34948", "#f0efec", "#2a78d6"])


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / name, dpi=150)
    plt.close(fig)


# 1) Überblick je Familie: mittlere Netto-Sharpe IS vs OOS (Stunden 2019–2026)
fam_rows = []
ts = pd.read_csv(R / "meanrev_hourly" / "single_asset_grid.csv")
pp = pd.read_csv(R / "meanrev_hourly" / "pairs_grid.csv")
bk = pd.read_csv(R / "meanrev_hourly" / "baskets_xs_grid.csv")
fu = pd.read_csv(R / "meanrev_hourly" / "funding_grid.csv")
fam_rows.append(("Einzelasset (beide Seiten)", ts[ts.family == "Einzelasset"]))
fam_rows.append(("Einzelasset nur long", ts[ts.family == "Einzelasset nur long"]))
fam_rows.append(("Einzelasset nur short", ts[ts.family == "Einzelasset nur short"]))
fam_rows.append(("Paare, schnelle Signale", pp[~pp.indicator.isin(["RSI48", "RSI96"])]))
fam_rows.append(("Paare, RSI 48–96 h", pp[pp.indicator.isin(["RSI48", "RSI96"])]))
fam_rows.append(("Korb gegen Korb", bk[bk.family == "Korb gegen Korb"]))
fam_rows.append(("Querschnitt", bk[bk.family.str.startswith("Querschnitt")]))
fam_rows.append(("Krypto-Funding", fu))
labels = [f for f, _ in fam_rows]
is_ = [d.Sharpe_IS.mean() for _, d in fam_rows]
oos = [d.Sharpe_OOS.mean() for _, d in fam_rows]
y = np.arange(len(labels))
fig, ax = plt.subplots(figsize=(10, 4.8))
ax.barh(y - 0.2, is_, height=0.38, color=C[0], label="2019–2022 (Optimierung)")
ax.barh(y + 0.2, oos, height=0.38, color=C[1], label="2023–2026 (Test)")
ax.set_yticks(y, labels)
ax.invert_yaxis()
ax.axvline(0, color=INK2, lw=1)
ax.set_xlabel("mittlere Sharpe Ratio nach Kosten über alle Varianten der Familie")
ax.set_title("Überhitzungs-Strategien intraday (≤ 48 h): fast alle Familien verlieren nach Kosten")
ax.legend(loc="lower right", fontsize=8)
save(fig, "m01_familien_ueberblick.png")
pd.DataFrame({"Familie": labels, "Sharpe_IS_Mittel": is_, "Sharpe_OOS_Mittel": oos,
              "Varianten": [len(d) for _, d in fam_rows]}).to_csv(OUT / "m01_data.csv", index=False)

# 2) Klasse × Richtung (OOS)
cd = pd.read_csv(R / "meanrev_hourly" / "conditioning.csv")
y2 = cd[cd["class"].notna() & (cd.condition == "keine")]
pv = y2.pivot_table(index="class", columns="side", values="Sharpe_ALL", aggfunc="mean")[["nur long", "nur short", "beide"]]
fig, ax = plt.subplots(figsize=(7, 5.4))
lim = np.nanmax(np.abs(pv.values))
im = ax.imshow(pv.values, cmap=DIV, vmin=-lim, vmax=lim, aspect="auto")
ax.set_xticks(range(3), ["überverkauft kaufen", "überkauft shorten", "beides"])
ax.set_yticks(range(len(pv)), pv.index)
ax.grid(False)
for i in range(pv.shape[0]):
    for j in range(pv.shape[1]):
        ax.text(j, i, f"{pv.values[i, j]:+.2f}", ha="center", va="center", fontsize=8, color=INK)
fig.colorbar(im, ax=ax, shrink=0.8, label="Sharpe nach Kosten 2019–2026")
ax.set_title("Wo hilft Gegenhalten? Einzelasset je Klasse und Richtung")
save(fig, "m02_klasse_richtung.png")
pv.to_csv(OUT / "m02_data.csv")

# 3) IBS-Dip-Kauf US-Indizes (Futures, Stunden) vs. Buy & Hold
cv = pd.read_csv(R / "ibs_futures_hourly" / "curve.csv", index_col=0, parse_dates=True)
fig, ax = plt.subplots(figsize=(11, 4.2))
for i, c in enumerate(cv.columns):
    d = cv[c].diff().fillna(cv[c])
    sc = d * (0.10 / np.sqrt(252)) / d.std()
    ax.plot(cv.index, sc.cumsum() * 100, color=C[i], lw=1.8, label=c)
ax.axhline(0, color=BASE, lw=1)
ax.axvline(pd.Timestamp("2023-01-01"), color=INK2, lw=1, ls="--")
ax.set_ylabel("kumulierte Rendite in %\n(je Linie auf 10 % Vol. skaliert)")
ax.set_title("Dip-Kauf nach Kassaschluss nahe am Tagestief (IBS < 0,2), Index-Futures, nach Kosten")
ax.legend(fontsize=8, loc="upper left")
save(fig, "m03_ibs_futures.png")

# 4) IBS je Index
ib = pd.read_csv(R / "ibs_futures_hourly" / "ibs_futures_hourly.csv")
ib = ib[~ib.Index.str.startswith(("Korb", "Buy"))]
fig, ax = plt.subplots(figsize=(8, 4))
x = np.arange(len(ib))
ax.bar(x - 0.2, ib.Sharpe_bis2022, width=0.38, color=C[0], label="2019–2022")
ax.bar(x + 0.2, ib.Sharpe_ab2023, width=0.38, color=C[1], label="2023–2026")
ax.set_xticks(x, ib.Index)
ax.axhline(0, color=INK2, lw=1)
ax.set_ylabel("Sharpe nach Kosten")
ax.set_title("IBS-Dip-Kauf je Index: ein US-Phänomen")
ax.legend(fontsize=8)
save(fig, "m04_ibs_je_index.png")

# 5) Umgebung der relativen RSI-Paare (klassenübergreifend): Sharpe gesamt nach RSI-Fenster × Schwelle
ng = pd.read_csv(R / "pair_rsi_deepdive" / "neighbourhood_grid.csv")
ng = ng[ng.scope == "klassenübergreifend"]
for col, fn, title in [("Sharpe_IS", "m05a_paare_umgebung_is.png", "2019–2022"), ("Sharpe_OOS", "m05b_paare_umgebung_oos.png", "2023–2026")]:
    pv = ng.groupby(["rsi_h", "theta"])[col].mean().unstack()
    fig, ax = plt.subplots(figsize=(6.4, 4))
    lim = max(1.0, np.nanmax(np.abs(pv.values)))
    im = ax.imshow(pv.values, cmap=DIV, vmin=-lim, vmax=lim, aspect="auto")
    ax.set_xticks(range(pv.shape[1]), [f"{int(t * 50)} Pkt." for t in pv.columns])
    ax.set_yticks(range(pv.shape[0]), [f"RSI {r} h" for r in pv.index])
    ax.grid(False)
    for i in range(pv.shape[0]):
        for j in range(pv.shape[1]):
            v = pv.values[i, j]
            ax.text(j, i, "–" if not np.isfinite(v) else f"{v:+.2f}", ha="center", va="center", fontsize=8, color=INK)
    ax.set_xlabel("Mindestabstand der RSI-Werte (A überkauft vs. B überverkauft)")
    fig.colorbar(im, ax=ax, shrink=0.8, label="Sharpe nach Kosten")
    ax.set_title(f"Relative RSI-Paare, klassenübergreifend ({title})")
    save(fig, fn)

# 6) Kurve relative RSI-Paare + wörtliches Nutzer-Beispiel
cr = pd.read_csv(R / "pair_rsi_deepdive" / "curve.csv", index_col=0, parse_dates=True)
ur = pd.read_csv(R / "user_rsi_example" / "hourly_rsi14_7030_curve.csv", index_col=0, parse_dates=True)
fig, ax = plt.subplots(figsize=(11, 4.2))
series = [("Relative RSI-Paare (netto)", cr["Relative-RSI-Paare (netto)"]), ("dieselbe Strategie, 1 h später (netto)", cr["Verzögerung 1 h (netto)"]),
          ("Dein Beispiel: Tages-RSI(14) 70/30 (netto)", ur["netto"])]
for i, (lab, s) in enumerate(series):
    d = s.diff().fillna(s)
    sc = d * (0.10 / np.sqrt(252)) / d.std()
    ax.plot(s.index, sc.cumsum() * 100, color=C[i], lw=1.8, label=lab)
ax.axhline(0, color=BASE, lw=1)
ax.axvline(pd.Timestamp("2023-01-01"), color=INK2, lw=1, ls="--")
ax.set_ylabel("kumulierte Rendite in % (auf 10 % Vol. skaliert)")
ax.set_title("Paar-Handel mit relativer Überhitzung: Fenster und Reaktionszeit entscheiden")
ax.legend(fontsize=8, loc="upper left")
save(fig, "m06_paare_kurven.png")
print("Charts:", sorted(p.name for p in OUT.glob("*.png")))
