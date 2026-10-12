"""Baut die Artefakt-Seite aus dem Markdown-Bericht + Template + Diagrammdaten."""
import json
import re
import sys
from pathlib import Path

import markdown

HERE = Path(__file__).resolve().parent
REPORT = Path(sys.argv[1])
OUT = HERE / "ueberhitzte_maerkte.html"

md = REPORT.read_text(encoding="utf-8")
# H1 des Berichts entfällt (Seite hat eigenen Kopf)
md = re.sub(r"^# .*\n", "", md, count=1)
# Verweise auf den ersten Bericht -> dessen veröffentlichte Seite
md = md.replace("](../reports/Kapitalrotation%20und%20Money%20Flow%20Trading.md)", "](https://claude.ai/artifact/2oFLQamUdStv2yT1rdrHK9)")
# Relative Repo-Links -> GitHub (Branch)
GH = "https://github.com/Winni4438/MF_Trader/blob/claude/blissful-gates-12gd63/"
md = re.sub(r"\]\(\.\./(?![^)]*\.png\))", "](" + GH, md)
html = markdown.markdown(md, extensions=["tables", "fenced_code", "sane_lists", "toc"],
                         extension_configs={"toc": {"permalink": False}})

FIG = {
    "m01_familien_ueberblick": """<figure class="chart"><figcaption><b>Welche Strategiefamilie trägt?</b>
<span>Mittlere Sharpe Ratio nach Kosten über alle Varianten je Familie, Stundendaten, Haltedauer höchstens 48 Stunden.</span></figcaption>
<div class="chartbox tall"><canvas id="c-families" role="img" aria-label="Balkendiagramm: Sharpe je Strategiefamilie"></canvas></div>
<details class="data"><summary>Daten als Tabelle</summary><div class="tablewrap" id="t-families"></div></details></figure>""",
    "m02_klasse_richtung": """<figure class="chart"><figcaption><b>Wo hilft Gegenhalten?</b>
<span>Einzelasset-Signale je Klasse und Richtung, Sharpe nach Kosten 2019–2026. Feld berühren oder überfahren für den Wert.</span></figcaption>
<div class="legend-div">verliert <i></i> gewinnt</div>
<div class="tablewrap" id="h-classdir"></div></figure>""",
    "m03_ibs_futures": """<figure class="chart"><figcaption><b>Dip-Kauf nach Kassaschluss nahe am Tagestief</b>
<span>IBS &lt; 0,2, nur long, höchstens 2 Sitzungen, Index-Futures, nach Kosten; jede Linie auf 10 % Jahresvolatilität skaliert.</span></figcaption>
<div class="chartbox tall"><canvas id="c-ibs" role="img" aria-label="Linienchart: kumulierte Rendite Dip-Kauf und Buy and Hold"></canvas></div>
<details class="data"><summary>Daten als Tabelle</summary><div class="tablewrap" id="t-ibs"></div></details></figure>""",
    "m04_ibs_je_index": """<figure class="chart"><figcaption><b>Dip-Kauf je Index: ein US-Phänomen</b>
<span>Sharpe nach Kosten in beiden Teilzeiträumen, Einstieg in der Stunde nach dem jeweiligen Kassaschluss.</span></figcaption>
<div class="chartbox"><canvas id="c-ibs-index" role="img" aria-label="Balkendiagramm: Sharpe je Index"></canvas></div>
<details class="data"><summary>Daten als Tabelle</summary><div class="tablewrap" id="t-ibs-index"></div></details></figure>""",
    "m05": """<figure class="chart"><figcaption><b>Relative RSI-Paare: wo die Zone liegt</b>
<span>Klassenübergreifende Paare, Sharpe nach Kosten nach RSI-Fenster und Mindestabstand der RSI-Werte. – = zu wenige Signale.</span></figcaption>
<div class="seg" id="seg-grid" role="group" aria-label="Zeitraum"><button type="button" data-mode="Sharpe_IS" aria-pressed="false">2019–2022</button><button type="button" data-mode="Sharpe_OOS" aria-pressed="true">2023–2026</button></div>
<div class="legend-div">verliert <i></i> gewinnt</div>
<div class="tablewrap" id="h-grid"></div></figure>""",
    "m06_paare_kurven": """<figure class="chart"><figcaption><b>Paar-Handel mit relativer Überhitzung</b>
<span>Bereinigter Kandidat (RSI 96 h, 30 Punkte Abstand, höchstens 24 h) gegen deine wörtliche Idee; jede Linie auf 10 % Volatilität skaliert, nach Kosten.</span></figcaption>
<div class="chartbox tall"><canvas id="c-pairs" role="img" aria-label="Linienchart: kumulierte Rendite Paar-Strategien"></canvas></div>
<details class="data"><summary>Daten als Tabelle</summary><div class="tablewrap" id="t-pairs"></div></details></figure>""",
}


def repl(m):
    src = m.group(0)
    for key, snippet in FIG.items():
        if key in src:
            return snippet
    return src


html = re.sub(r"<p>\s*<img[^>]*>\s*</p>", repl, html)
html = re.sub(r"<img[^>]*results/charts_meanrev/[^>]*>", repl, html)
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
