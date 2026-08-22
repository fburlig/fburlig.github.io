# fionaburlig.com

Plain HTML, hosted on GitHub Pages. No build system beyond one script.

## Editing
- **Papers:** edit `papers.yaml`, then run `python3 build.py` (needs `pip install pyyaml`). This regenerates `index.html` and `research.html`. Set `featured: true` to show a paper on the homepage; homepage order is `FEATURED_ORDER` in `build.py`.
- **Homepage text / teaching / nav / footer:** edit `build.py` (index template), `teaching.html`, or `teaching/*.html` directly.
- **PDFs:** drop into `s/` (same path scheme as the old Squarespace site, so old links keep working).
- **CV:** replace `cv.pdf`.
- **Style:** `style.css`.

Commit and push; the site updates in under a minute.
