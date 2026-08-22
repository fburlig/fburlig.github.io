# fionaburlig.com

Quarto site, rendered by GitHub Actions on every push to `main` and published from the `gh-pages` branch. Nothing to install locally unless you want to preview (`quarto preview`).

## Editing
- **Papers:** edit `papers.yaml`, then run `python3 build.py` (needs `pip install pyyaml`). This regenerates `research.qmd` and `_featured.md` (the homepage list). Set `featured: true` to show a paper on the homepage; homepage order is `FEATURED_ORDER` in `build.py`.
- **Homepage text / teaching / nav / footer:** edit `index.qmd`, `teaching.qmd`, `teaching/*.qmd`, or `_quarto.yml` (navbar).
- **PDFs:** drop into `s/` (same path scheme as the old Squarespace site, so old links keep working).
- **CV:** replace `cv.pdf`.
- **Style:** `style.css`.

Commit and push; the site updates in under a minute.
