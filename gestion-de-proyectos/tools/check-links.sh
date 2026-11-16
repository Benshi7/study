#!/usr/bin/env bash
# Verifies that every relative link in the suite resolves to a real file.
#  - HTML: href/src on <a>, <link>, <script>, <img> (+ #fragment must exist as an id in the target HTML)
#  - CSS/HTML: @import url(...) with a relative path
#  - Catalog: lesson/page paths in assets/suite-data.js whose status says the page exists
# Ignored: http(s), mailto, data:, javascript:, pure #anchors, and <a class="local-only"> links
# (those only work in the full copy that has raw/).
# Also ignored: <a class="pending"> links, i.e. links to a lesson that is planned but not written yet.
# Convention: write them as class="local-only pending" (subdued style + skipped). When the target file
# exists, delete BOTH classes ("local-only" also skips the check; it is meant for raw/ PDFs only)
# so the checker starts verifying the link.
# Exit code 1 when something is broken.
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || exit 2

python3 - "$ROOT" <<'PY'
import os, re, sys
from html.parser import HTMLParser
from urllib.parse import unquote

root = sys.argv[1]
SKIP_DIRS = {"raw", ".atl", "dist", "node_modules", ".git"}
SKIP_PREFIX = ("http://", "https://", "mailto:", "data:", "javascript:", "tel:", "//")
failures, checked = [], 0
ids_cache = {}

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids = [], set()
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if a.get("name"):
            self.ids.add(a["name"])
        cls = (a.get("class") or "").split()
        for key in ("href", "src"):
            if key in a and a[key] is not None and "local-only" not in cls and "pending" not in cls:
                self.links.append(a[key])

def parse(path):
    if path not in ids_cache:
        p = Page()
        with open(path, encoding="utf-8") as f:
            p.feed(f.read())
        ids_cache[path] = p
    return ids_cache[path]

def check(source, target):
    global checked
    target = target.strip()
    if not target or target.startswith("#") or target.startswith(SKIP_PREFIX):
        return
    checked += 1
    path, _, frag = target.partition("#")
    path = unquote(path.split("?")[0])
    resolved = os.path.normpath(os.path.join(os.path.dirname(source), path)) if path else source
    rel = os.path.relpath(source, root)
    if not os.path.exists(resolved):
        failures.append(f"{rel}: missing file -> {target}")
    elif frag and resolved.endswith(".html") and frag not in parse(resolved).ids:
        failures.append(f"{rel}: missing anchor #{frag} in {os.path.relpath(resolved, root)}")

for dirpath, dirnames, filenames in os.walk(root):
    dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
    for name in filenames:
        full = os.path.join(dirpath, name)
        if name.endswith(".html"):
            for link in parse(full).links:
                check(full, link)
        if name.endswith((".html", ".css")):
            with open(full, encoding="utf-8") as f:
                text = f.read()
            for m in re.finditer(r"@import\s+(?:url\()?['\"]?([^'\")\s;]+)", text):
                check(full, m.group(1))

print(f"HTML/CSS links checked: {checked}")
if failures:
    print("BROKEN LINKS:")
    for line in failures:
        print("  " + line)
    sys.exit(1)
print("OK: no broken relative links")
PY
html_status=$?

# Catalog check: pages the catalog claims exist must exist.
node - <<'JS'
const fs = require("fs"), path = require("path"), vm = require("vm");
const ctx = { window: {} };
vm.runInNewContext(fs.readFileSync("assets/suite-data.js", "utf8"), ctx);
const S = ctx.window.SUITE;
const bad = [];
const need = (p, why) => { if (p && !fs.existsSync(p)) bad.push(`${why}: ${p}`); };
for (const c of S.classes) {
  if (c.status === "listo") { need(c.lesson, `class ${c.number} lesson`); (c.lessonMore || []).forEach(p => need(p, `class ${c.number} lessonMore`)); }
  if (c.pdf && fs.existsSync("raw")) need(path.join("raw", c.pdf), `class ${c.number} pdf`);
}
for (const x of S.extras) if (x.status === "listo") need(x.path, `extra ${x.id}`);
for (const t of S.tpSections) need(t.page, `tp section ${t.number} page`);
// tp/assets/tp-data.js (shared folder) must agree with this catalog: same section pages and statuses.
const tctx = { window: {} };
vm.runInNewContext(fs.readFileSync("tp/assets/tp-data.js", "utf8"), tctx);
const T = tctx.window.TP;
for (const n of T.nav) need(path.join("tp", n.href), `tp-data nav ${n.label}`);
for (const s of T.sections) {
  if (s.page) need(path.join("tp", s.page), `tp-data section ${s.n}`);
  const root = S.tpSections.find(x => x.number === s.n);
  if (!root) { bad.push(`tp-data section ${s.n} missing in suite-data.js`); continue; }
  const expected = root.page ? root.page.replace(/^tp\//, "") : null;
  if (expected !== s.page) bad.push(`section ${s.n}: page differs (suite-data: ${expected}, tp-data: ${s.page})`);
  if (root.status !== s.status) bad.push(`section ${s.n}: status differs (suite-data: ${root.status}, tp-data: ${s.status})`);
}
if (bad.length) { console.log("CATALOG PROBLEMS:"); bad.forEach(b => console.log("  " + b)); process.exit(1); }
console.log("OK: catalog paths match files");
JS
catalog_status=$?

[ "$html_status" -eq 0 ] && [ "$catalog_status" -eq 0 ]
