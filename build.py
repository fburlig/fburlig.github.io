#!/usr/bin/env python3
"""Render research.qmd and _featured.md from papers.yaml. Run: python3 build.py, commit, push (GitHub Actions renders)."""
import yaml

D = yaml.safe_load(open("papers.yaml"))
CURRENT = [  # homepage "current research", in order; title prefixes from papers.yaml
    "Groundwater and crop choice",
    "Beliefs, forecasts, and investments",
    "Insurance and the demand for adaptation",
    "Paying for power",
]
SELECTED_PUBS = [
    "The value of clean water",
    "Out of the darkness",
]
LINK_ORDER = ["journal", "handbook", "nber", "appendix", "data/code", "software", "rct registry", "summary"]

import re
def slug(p):
    return re.sub(r"[^a-z0-9]+", "-", p["title"].lower()).strip("-")[:40]

def authors(p):
    a = f"with {p['authors']}" if p.get("authors") else ""
    if p.get("note"): a += "<sup>†</sup>"
    return a

def links(p, pdf_label="paper"):
    L = []
    if p.get("pdf"): L.append(f'<a href="{p["pdf"]}">{pdf_label}</a>')
    for k in LINK_ORDER:
        if k in (p.get("links") or {}): L.append(f'<a href="{p["links"][k]}">{k}</a>')
    if p.get("coverage"): L.append(f'<a href="coverage.html#{slug(p)}">coverage</a>')
    return f'<div class="links">{" · ".join(L)}</div>' if L else ""

def entry(p, tail, pdf_label="paper"):
    meta = " · ".join(x for x in [authors(p), tail] if x)
    return f'<div class="paper">\n<span class="ptitle">{p["title"]}</span><br>\n<span class="meta">{meta}</span>\n{links(p, pdf_label)}\n</div>\n'

out = ['---\ntitle: "research"\ntoc: false\n---\n', "## working papers\n"]
for p in D["working_papers"]:
    out.append(entry(p, p["date"] + (f"<br>{p['status']}" if p.get("status") else ""), pdf_label="draft"))
out.append("## publications\n")
for p in D["publications"]:
    out.append(entry(p, f"{p['journal']} · {p['year']}"))
out.append("## selected work in progress\n")
for p in D["work_in_progress"]:
    out.append(entry(p, ""))
notes = [p["note"] for s in D for p in D[s] if p.get("note")]
if notes: out.append('<p class="meta footnote">† ' + "; ".join(sorted(set(notes))) + "</p>\n")
open("research.qmd", "w").write("\n".join(out))

# ---------- coverage.qmd ----------
cov = ['---\ntitle: "coverage"\ntoc: false\n---\n',
       '<p class="meta">Press, podcasts, and blog coverage, by paper. Links to papers and summaries are on the <a href="research.html">research page</a>.</p>\n']
for sec in ("working_papers", "publications"):
    for p in D[sec]:
        if not p.get("coverage"): continue
        items = " · ".join(f'<a href="{list(c.values())[0]}">{list(c.keys())[0]}</a>' for c in p["coverage"])
        cov.append(f'<div class="paper" id="{slug(p)}">\n<span class="ptitle">{p["title"]}</span><br>\n<span class="links">{items}</span>\n</div>\n')
open("coverage.qmd", "w").write("\n".join(cov))

allp = D["working_papers"] + D["publications"]
def feat(pre):
    p = next(p for p in allp if p["title"].startswith(pre))
    st = p.get("status") or (f"{p['journal']}" if p.get("journal") else "")
    lab = "paper" if p.get("journal") else "draft"
    t = f'<a href="{p["pdf"]}">{p["title"]}</a>' if p.get("pdf") else p["title"]
    rows = [f'<span class="ftitle">{t}</span>']
    if p.get("authors"): rows.append(f'<span class="meta">{authors(p)}</span>')
    if st: rows.append(f'<span class="meta">{st}</span>')
    return '<div class="feat">\n' + "<br>\n".join(rows) + "\n</div>"
open("_featured.md", "w").write("\n".join(feat(x) for x in CURRENT) + "\n")
open("_selected.md", "w").write("\n".join(feat(x) for x in SELECTED_PUBS) + "\n")
print("built research.qmd, coverage.qmd, _featured.md, _selected.md")
