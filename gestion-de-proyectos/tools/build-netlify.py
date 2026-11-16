#!/usr/bin/env python3
"""Build dist/suite-netlify/ (and dist/suite-netlify.zip): a self-contained copy of the study suite for Netlify Drop.

Included: hub, lessons, mock exam, glossary, diagrams and the class decks.
Left out on purpose (the site is public): raw/ (cátedra PDFs), tp/, entregable/, trabajo-grupal/, the team defense deck.
Links to anything left out become plain dimmed text, and the hub catalog is trimmed to what exists in the pack.
Run from anywhere: python3 tools/build-netlify.py
"""
import re, shutil, sys, zipfile
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "dist" / "suite-netlify"
COPY = ["index.html", "repaso.html", "assets", "clases", "reference", "diagramas",
        "slides/index.html", "slides/assets", "slides/08-agilidad", "slides/09-scrum", "slides/10-ceremonias",
        "slides/12-lean-xp-kanban", "slides/defensa-tp"]
SKIP_FILES = {"_template.html"}

# Appended to the pack's suite-data.js: drop what the pack does not ship. PACK_FILES is filled in below.
TRIM = """
// --- added by tools/build-netlify.py: this copy has no raw/, tp/ or team deck ---
(function () {
  var have = PACK_FILES;
  var ok = function (p) { return p && have.indexOf(p) >= 0; };
  window.SUITE.classes.forEach(function (c) { c.pdf = null; c.extraPdfs = []; if (c.slides && !ok(c.slides)) c.slides = null; });
  (window.SUITE.tpSections || []).forEach(function (s) { if (!ok(s.page)) s.page = null; });
  window.SUITE.extras = (window.SUITE.extras || []).filter(function (x) { return ok(x.path); });
})();
"""

# Appended to the pack's suite-index.js: the Slides page and the diagram index only list what ships.
TRIM_INDEX = """
// --- added by tools/build-netlify.py ---
(function () {
  var have = PACK_FILES;
  var I = window.SUITE_INDEX;
  I.decks = I.decks.filter(function (d) { return have.indexOf(d.path) >= 0; });
  I.diagrams.forEach(function (d) { d.pages = d.pages.filter(function (p) { return have.indexOf(p) >= 0; }); });
})();
"""

A_RE = re.compile(r'<a\b([^>]*?)href="([^"]+)"([^>]*)>(.*?)</a>', re.S)
REF_RE = re.compile(r'(?:href|src)="([^"]+)"')


def is_external(u):
    return u.startswith(("http:", "https:", "mailto:", "#", "data:", "javascript:"))


def target(page, url):
    path = unquote(url.split("#")[0].split("?")[0])
    if not path:
        return page
    t = (page.parent / path).resolve()
    return t / "index.html" if t.is_dir() else t


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    for item in COPY:
        src, dst = ROOT / item, OUT / item
        if src.is_dir():
            shutil.copytree(src, dst, ignore=lambda d, names: [n for n in names if n in SKIP_FILES])
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

    files = sorted(str(p.relative_to(OUT)) for p in OUT.rglob("*") if p.is_file())
    data = OUT / "assets" / "suite-data.js"
    data.write_text(data.read_text(encoding="utf-8") + TRIM.replace("PACK_FILES", repr(files).replace("'", '"')), encoding="utf-8")
    index = OUT / "assets" / "suite-index.js"
    index.write_text(index.read_text(encoding="utf-8") + TRIM_INDEX.replace("PACK_FILES", repr(files).replace("'", '"')), encoding="utf-8")

    unwrapped = 0
    for page in OUT.rglob("*.html"):
        html = page.read_text(encoding="utf-8")

        def fix(m):
            nonlocal unwrapped
            url = m.group(2)
            if is_external(url) or target(page, url).exists():
                return m.group(0)
            unwrapped += 1
            return '<span class="local-only" title="No incluido en la versión web">' + m.group(4) + "</span>"

        new = A_RE.sub(fix, html)
        if new != html:
            page.write_text(new, encoding="utf-8")

    # Ask search engines to stay out: it is a personal study site.
    (OUT / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")
    (OUT / "_headers").write_text("/*\n  X-Robots-Tag: noindex, nofollow\n", encoding="utf-8")

    broken = []
    for page in OUT.rglob("*.html"):
        for url in REF_RE.findall(page.read_text(encoding="utf-8")):
            if not is_external(url) and not target(page, url).exists():
                broken.append(f"{page.relative_to(OUT)} -> {url}")

    zpath = OUT.with_suffix(".zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(OUT.rglob("*")):
            if p.is_file():
                z.write(p, p.relative_to(OUT))

    size = sum(p.stat().st_size for p in OUT.rglob("*") if p.is_file()) / 1e6
    print(f"{OUT.relative_to(ROOT)}: {len(list(OUT.rglob('*.html')))} pages, {size:.1f} MB, {unwrapped} links to left-out files turned into text")
    print(f"{zpath.relative_to(ROOT)}: {zpath.stat().st_size / 1e6:.1f} MB")
    if broken:
        print("BROKEN LINKS:\n  " + "\n  ".join(broken))
        sys.exit(1)
    print("OK: no broken relative links in the pack")


if __name__ == "__main__":
    main()
