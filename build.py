#!/usr/bin/env python3
"""Render research.qmd and _featured.md from papers.yaml. Run: python3 build.py  (then commit; GitHub Actions renders the site)"""
import yaml

D = yaml.safe_load(open("papers.yaml"))
FEATURED_ORDER = [  # homepage order
    "Paying for power",
    "Insurance and the demand for adaptation",
    "The value of clean water",
    "Groundwater and crop choice",
    "Beliefs, forecasts, and investments",
]

def title_link(p):
    return f'[{p["title"]}]({p["pdf"]})' if p.get("pdf") else p["title"]

def links(p):
    if not p.get("links"): return ""
    return '<div class="links">' + " ".join(f'[<a href="{u}">{k}</a>]' for k, u in p["links"].items()) + "</div>"

def entry(p, tail):
    auth = f"with {p['authors']}" if p.get("authors") else ""
    meta = " · ".join(x for x in [auth, tail] if x)
    return f'<div class="paper">\n<span class="ptitle">{title_link(p)}</span><br>\n<span class="meta">{meta}</span>\n{links(p)}\n</div>\n'

# ---------- research.qmd ----------
out = ['---\ntitle: "research"\ntoc: false\n---\n', "## publications\n"]
for p in D["publications"]:
    out.append(entry(p, f"{p['journal']} · {p['year']}"))
out.append("## working papers\n")
for p in D["working_papers"]:
    tail = p["date"] + (f"<br>{p['status']}" if p.get("status") else "")
    out.append(entry(p, tail))
out.append("## selected work in progress\n")
for p in D["work_in_progress"]:
    out.append(entry(p, ""))
open("research.qmd", "w").write("\n".join(out))

# ---------- _featured.md (homepage) ----------
allp = D["working_papers"] + D["publications"]
lines = []
for pre in FEATURED_ORDER:
    p = next(p for p in allp if p["title"].startswith(pre))
    st = p.get("status") or (p["journal"].split(",")[0] if p.get("journal") else "")
    bits = [title_link(p)]
    if p.get("authors"): bits.append(f"with {p['authors']}")
    if st: bits.append(st)
    lines.append("↳ " + " · ".join(bits))
open("_featured.md", "w").write("<br>\n".join(lines) + "\n")
print("built research.qmd, _featured.md")
