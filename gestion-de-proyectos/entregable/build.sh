#!/usr/bin/env bash
# Rebuilds everything: theme.css + figures (HTML -> PNG), then the .docx and the Notion-friendly .md in dist/.
#   ./build.sh            full build
#   ./build.sh --fast     skip figure rendering (images in img/ are reused)
#   ./build.sh --toc-pages  (also) fill the cached TOC page numbers + write dist/TP_Cascada_Grupo01.pdf (needs soffice + PyMuPDF; set PDF_PY)
set -euo pipefail
cd "$(dirname "$0")"
FAST=0; TOC=0
# Corrected Gantt (dist/Gantt_corregido_TP_Cascada.xlsx, data/gantt.json) and annex A: needs openpyxl, e.g. PY_XL=/path/to/venv/bin/python ./build.sh
if [ -n "${PY_XL:-}" ]; then "$PY_XL" tools/gen-gantt-corregido.py && python3 tools/gen-annex.py; fi
for a in "$@"; do case "$a" in --fast) FAST=1;; --toc-pages) TOC=1;; esac; done
if [ "$FAST" = 0 ]; then node build/figures.mjs; fi
node build/build-docx.mjs
if [ "$TOC" = 1 ]; then
  "${PDF_PY:-python3}" build/fill_toc_pages.py dist/TP_Cascada_Grupo01.docx
  soffice -env:UserInstallation=file:///tmp/lo-profile-toc --headless --convert-to pdf --outdir dist dist/TP_Cascada_Grupo01.docx >/dev/null 2>&1
  echo "PDF preview: dist/TP_Cascada_Grupo01.pdf"
fi
