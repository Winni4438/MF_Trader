"""Baut die Artefakt-Seite aus dem Markdown-Bericht + Template + Diagrammdaten."""
import json
import re
import sys
from pathlib import Path

import markdown

HERE = Path(__file__).resolve().parent
REPORT = Path(sys.argv[1])
OUT = HERE / "money_flow_trading.html"

md = REPORT.read_text(encoding="utf-8")
# H1 des Berichts entfällt (Seite hat eigenen Kopf)
md = re.sub(r"^# .*\n", "", md, count=1)
# Relative Repo-Links -> GitHub (Branch)
GH = "https://github.com/Winni4438/MF_Trader/blob/claude/blissful-gates-12gd63/"
md = re.sub(r"\]\(\.\./(?!results/charts/)", "](" + GH, md)
html = markdown.markdown(md, extensions=["tables", "fenced_code", "sane_lists", "toc"],
                         extension_configs={"toc": {"permalink": False}})

FIG = {
    "01_ereignisstudie": """<figure class="chart"><figcaption><b>Was nach dem Signal noch übrig ist</b>
<span>Durchschnittlicher Kursverlauf um 528 Risk-off- bzw. 382 Risk-on-Signale (4-Stunden-Flow, z ≥ 2,5), 2019–2026. Links vom Signal die Bewegung, die zur Erkennung führte; rechts die Überrendite gegenüber der normalen Drift.</span></figcaption>
<div class="seg" id="seg-event" role="group" aria-label="Signalrichtung"><button type="button" data-mode="riskoff" aria-pressed="true">Risk-off</button><button type="button" data-mode="riskon" aria-pressed="false">Risk-on</button></div>
<div class="chartbox tall"><canvas id="c-event" role="img" aria-label="Linienchart: Kursverlauf relativ zum Signalzeitpunkt"></canvas></div>
<details class="data"><summary>Daten als Tabelle (bps)</summary><p>Risk-off</p><div class="tablewrap" id="t-event-riskoff"></div><p>Risk-on</p><div class="tablewrap" id="t-event-riskon"></div></details></figure>""",
    "02_equity_intraday": """<figure class="chart"><figcaption><b>Intraday-Strategien nach Kosten</b>
<span>Kumulierte Rendite bei 5 % Risikobudget je Positionsbein, Stundendaten Juli 2019 bis September 2026. Ab 2023 Out-of-Sample.</span></figcaption>
<div class="chartbox tall"><canvas id="c-equity" role="img" aria-label="Linienchart: kumulierte Rendite der Strategien"></canvas></div>
<details class="data"><summary>Daten als Tabelle</summary><div class="tablewrap" id="t-equity"></div></details></figure>""",
    "03_latenz_kosten": """<figure class="chart"><figcaption><b>Reaktionszeit und Kosten</b>
<span>Sharpe Ratio des Rotation-Followers (Basisvariante) bei verzögertem Einstieg und unterschiedlichen Kostenannahmen.</span></figcaption>
<div class="chartbox"><canvas id="c-latency" role="img" aria-label="Linienchart: Sharpe Ratio je Verzögerung"></canvas></div>
<details class="data"><summary>Daten als Tabelle</summary><div class="tablewrap" id="t-latency"></div></details></figure>""",
    "04_paar_matrix_intraday": """<figure class="chart"><figcaption><b>Paar-Rotationen intraday: Sharpe nach Kosten</b>
<span>„Folge dem Flow von B nach A“ mit 8-Stunden-Fenster und 8 Stunden Haltedauer, 136 Paare. Feld berühren oder überfahren für Brutto- und Out-of-Sample-Werte.</span></figcaption>
<div class="legend-div">Folgen verliert <i></i> Folgen lohnt</div>
<div class="tablewrap" id="h-pairs"></div></figure>""",
    "05_muster_haeufigkeit": """<figure class="chart"><figcaption><b>Wie oft kommt welche Rotation vor?</b>
<span>Tage pro Jahr je Muster, klassifiziert aus Tagesrenditen von S&amp;P 500, Treasuries, Gold, US-Dollar und Yen (ETF-Daten 2007 bis 9. Oktober 2026).</span></figcaption>
<div class="chartbox"><canvas id="c-patterns" role="img" aria-label="Linienchart: Häufigkeit der Rotationsmuster pro Jahr"></canvas></div>
<details class="data"><summary>Daten als Tabelle</summary><div class="tablewrap" id="t-patterns"></div></details></figure>""",
    "06_folgetag_muster": """<figure class="chart"><figcaption><b>Was passiert am Tag nach einer Rotation?</b>
<span>Mittlere Rendite am Folgetag in %, 2007–2026. * = statistisch signifikant (|t| ≥ 1,96). Feld berühren oder überfahren für den t-Wert.</span></figcaption>
<div class="legend-div">negativ <i></i> positiv</div>
<div class="tablewrap" id="h-follow"></div></figure>""",
}


def repl(m):
    src = m.group(0)
    for key, snippet in FIG.items():
        if key in src:
            return snippet
    return src


html = re.sub(r"<p>\s*<img[^>]*>\s*</p>", repl, html)
html = re.sub(r"<img[^>]*results/charts/[^>]*>", repl, html)
html = html.replace("<p>", '<p class="lead">', 1)
html = html.replace("<table>", '<div class="tablewrap"><table>').replace("</table>", "</table></div>")
toc = "".join(f'<li><a href="#{i}">{re.sub("<[^>]+>", "", t)}</a></li>'
              for i, t in re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', html))
data = (HERE / "data.json").read_text(encoding="utf-8").replace("</", "<\\/")
page = (HERE / "template.html").read_text(encoding="utf-8")
page = page.replace("%%TOC%%", toc).replace("%%BODY%%", html).replace("%%DATA%%", data)
OUT.write_text(page, encoding="utf-8")
missing = [k for k in FIG if FIG[k][:60] not in page]
print("geschrieben:", OUT, len(page), "Bytes; nicht eingebunden:", missing)
