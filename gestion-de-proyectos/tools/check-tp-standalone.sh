#!/usr/bin/env bash
# Proves that the tp/ folder works detached from the rest of the workspace (teammates open it from a zip, file://).
# Usage: tools/check-tp-standalone.sh [path/to/tp]      (default: <repo>/tp)
# Fails (exit 1) when any tp/*.html:
#   - references a file outside the folder without class="local-only" (../clases, ../raw, ../assets, ...)
#   - references a file that does not exist inside the folder
#   - loads a remote resource (<script>, <link>, <img>, <iframe>, <source>, CSS url()/@import) other than the Google Fonts stylesheet
#   - does not load its own assets/theme.js (light/dark toggle)
# Also fails when a script in the folder uses fetch()/XMLHttpRequest (blocked on file://).
# Plain <a href="https://..."> navigation links are fine: they are not resources of the page.
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="${1:-$ROOT/tp}"
[ -d "$TARGET" ] || { echo "not a directory: $TARGET"; exit 2; }

python3 - "$TARGET" <<'PY'
import os, re, sys
from html.parser import HTMLParser
from urllib.parse import unquote

root = os.path.realpath(sys.argv[1])
failures, pages = [], 0
REMOTE = ("http://", "https://", "//")
FONTS_OK = ("https://fonts.googleapis.com/", "https://fonts.gstatic.com/")

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []   # (tag, attr, value, classes)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = (a.get("class") or "").split()
        for key in ("href", "src", "data", "poster", "action"):
            if a.get(key):
                self.refs.append((tag, key, a[key], cls))

def is_font(url):
    return url.startswith(FONTS_OK)

def check_ref(source, tag, value, cls, is_resource):
    rel = os.path.relpath(source, root)
    value = value.strip()
    if not value or value.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
        return
    if value.startswith(REMOTE):
        if is_resource and not is_font(value):
            failures.append(f"{rel}: remote resource <{tag}> -> {value}")
        return
    if "local-only" in cls:
        return
    path = unquote(value.split("#")[0].split("?")[0])
    if not path:
        return
    resolved = os.path.realpath(os.path.join(os.path.dirname(source), path))
    if not (resolved == root or resolved.startswith(root + os.sep)):
        failures.append(f"{rel}: escapes the folder without class=\"local-only\" -> {value}")
    elif not os.path.exists(resolved):
        failures.append(f"{rel}: missing file -> {value}")

def check_css(source, text):
    rel = os.path.relpath(source, root)
    for m in re.finditer(r"@import\s+(?:url\()?['\"]?([^'\")\s;]+)", text):
        check_ref(source, "@import", m.group(1), [], True)
    for m in re.finditer(r"url\(\s*['\"]?([^'\")]+)", text):
        v = m.group(1)
        if v.startswith(REMOTE) and not is_font(v):
            failures.append(f"{rel}: remote url() -> {v}")

for dirpath, _, files in os.walk(root):
    for name in sorted(files):
        full = os.path.join(dirpath, name)
        if name.endswith(".html"):
            pages += 1
            with open(full, encoding="utf-8") as f:
                text = f.read()
            p = Page()
            p.feed(text)
            has_theme = False
            for tag, key, value, cls in p.refs:
                resource = tag != "a" and not (tag == "form")
                check_ref(full, tag, value, cls, resource)
                if tag == "script" and value.endswith("assets/theme.js"):
                    has_theme = True
            if not has_theme:
                failures.append(f"{os.path.relpath(full, root)}: does not load assets/theme.js")
            for m in re.finditer(r"<style[^>]*>([\s\S]*?)</style>", text):
                check_css(full, m.group(1))
            for m in re.finditer(r"<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)</script>", text):
                if re.search(r"\bfetch\s*\(|XMLHttpRequest", m.group(1)):
                    failures.append(f"{os.path.relpath(full, root)}: inline script uses fetch/XMLHttpRequest (blocked on file://)")
        elif name.endswith(".css"):
            with open(full, encoding="utf-8") as f:
                check_css(full, f.read())
        elif name.endswith(".js"):
            with open(full, encoding="utf-8") as f:
                if re.search(r"\bfetch\s*\(|XMLHttpRequest", f.read()):
                    failures.append(f"{os.path.relpath(full, root)}: uses fetch/XMLHttpRequest (blocked on file://)")

for required in ("index.html", "LEEME.txt", "assets/logic.js", "assets/theme.js", "assets/course.css"):
    if not os.path.exists(os.path.join(root, required)):
        failures.append(f"missing required file: {required}")

print(f"standalone check: {pages} pages in {root}")
if failures:
    print("STANDALONE FAILURES:")
    for line in failures:
        print("  " + line)
    sys.exit(1)
print("OK: tp/ is self-contained")
PY
