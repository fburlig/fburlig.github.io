#!/usr/bin/env python3
"""Render index.html and research.html from papers.yaml. Run: python3 build.py"""
import yaml, html

D = yaml.safe_load(open("papers.yaml"))
FEATURED_ORDER = [  # homepage order
    "Paying for power",
    "Insurance and the demand for adaptation",
    "The value of clean water",
    "Groundwater and crop choice",
    "Beliefs, forecasts, and investments",
]

def page(title, here, body):
    nav = "".join(
        f'<a href="{h}"{" class=here" if k == here else ""}>{k}</a>'
        for k, h in [("home", "/"), ("research", "/research"), ("teaching", "/teaching"), ("cv", "/cv.pdf")]
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/style.css">
</head><body>
<nav>{nav}</nav>
{body}

</body></html>
"""

def with_(p):
    return f" · with {p['authors']}" if p.get("authors") else ""

def links(p):
    if not p.get("links"): return ""
    return '<div class="links">' + " ".join(f'<a href="{u}">{html.escape(k)}</a>' for k, u in p["links"].items()) + "</div>"

def title_link(p):
    t = html.escape(p["title"])
    return f'<a href="{p["pdf"]}">{t}</a>' if p.get("pdf") else t

# ---------- research.html ----------
def entry(p, tail):
    return f'<li>{title_link(p)}<div class="meta">{with_(p).lstrip(" ·")}{tail}</div>{links(p)}</li>'

wp = "".join(entry(p, f" · {p['date']}" + (f"<br>{p['status']}" if p.get("status") else "")) for p in D["working_papers"])
pub = "".join(entry(p, f" · {p['journal']} · {p['year']}") for p in D["publications"])
wip = "".join(entry(p, "") for p in D["work_in_progress"])
research = f"""<h1>Research</h1>
<p class="meta">Working papers, publications, and work in progress. NBER versions, appendices, replication packages, and coverage are linked under each paper.</p>
<h2>working papers</h2><ul class="papers">{wp}</ul>
<h2>publications</h2><ul class="papers">{pub}</ul>
<h2>work in progress</h2><ul class="papers">{wip}</ul>
"""
open("research.html", "w").write(page("Research — Fiona Burlig", "research", research))

# ---------- index.html ----------
allp = D["working_papers"] + D["publications"]
def find(prefix):
    return next(p for p in allp if p["title"].startswith(prefix))
feat = ""
for pre in FEATURED_ORDER:
    p = find(pre)
    st = p.get("status") or (f"{p['journal'].split(',')[0]}" if p.get("journal") else "")
    feat += f'<li>{title_link(p)}{with_(p)}{" · " + st if st else ""}</li>'

index = f"""<img class="headshot" src="/headshot.jpg" alt="Fiona Burlig">
<p class="lede">I am <strong>Fiona Burlig</strong>, an assistant professor at the Harris School of Public Policy at the University of Chicago, an NBER Faculty Research Fellow (EEE and DEV), an affiliate of J-PAL, BREAD, and the IGC, and Deputy Faculty Director of EPIC-India and the Odisha Data, Policy, and Innovation Centre. I am an applied microeconomist with research interests in and at the intersection of energy, environmental, and resource economics and development economics. Prior to joining Harris, I was a postdoc in the Department of Economics at the University of Chicago. I hold a PhD in agricultural and resource economics from the University of California, Berkeley, and a BA in economics, political science, and German from Williams College.</p>

<h2>research</h2>
<p>I'm an environmental and energy economist. I study how households, firms, and governments respond to environmental change and environmental policy, with a particular focus on energy, water, and climate adaptation in low- and middle-income countries.</p>
<p>Some current work…</p>
<ul class="arrow">{feat}</ul>
<p class="more"><a href="/research">all research →</a></p>

<h2>teaching</h2>
<ul class="arrow">
<li><a href="/teaching">Program evaluation</a> · PPHA 34600, Harris School, every spring</li>
</ul>

<h2>more</h2>
<p class="inline"><a href="/cv.pdf">CV</a><a href="https://scholar.google.com/citations?user=73OXPLsAAAAJ">Google Scholar</a><a href="https://github.com/fburlig">GitHub</a><a href="mailto:burlig@uchicago.edu">contact</a></p>
"""
open("index.html", "w").write(page("Fiona Burlig", "home", index))
print("built index.html, research.html")
