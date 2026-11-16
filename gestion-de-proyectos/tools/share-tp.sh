#!/usr/bin/env bash
# Packs tp/ into dist/tp-cascada.zip to share with the team.
# tp/ is self-contained: unzip anywhere and open tp-cascada/index.html.
set -eu
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
"$ROOT/tools/sync-assets.sh" >/dev/null
"$ROOT/tools/check-tp-standalone.sh" "$ROOT/tp" >/dev/null || { echo "tp/ is not standalone: run tools/check-tp-standalone.sh"; exit 1; }
mkdir -p "$ROOT/dist"
OUT="$ROOT/dist/tp-cascada.zip"
rm -f "$OUT"

# Stage under a top-level "tp-cascada/" folder and drop editor/Windows junk.
STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT
mkdir -p "$STAGE/tp-cascada"
cp -R "$ROOT/tp/." "$STAGE/tp-cascada/"
rm -f "$STAGE"/tp-cascada/*:Zone.Identifier "$STAGE"/tp-cascada/assets/*:Zone.Identifier
[ -f "$STAGE/tp-cascada/LEEME.txt" ] || { echo "LEEME.txt missing in tp/"; exit 1; }

if command -v zip >/dev/null 2>&1; then
  (cd "$STAGE" && zip -qr "$OUT" tp-cascada)
  TOOL="zip"
elif command -v python3 >/dev/null 2>&1; then
  python3 - "$STAGE" "$OUT" <<'PY'
import os, sys, zipfile
stage, out = sys.argv[1], sys.argv[2]
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for d, _, files in os.walk(stage):
        for f in files:
            full = os.path.join(d, f)
            z.write(full, os.path.relpath(full, stage))
PY
  TOOL="python3 zipfile"
else
  OUT="$ROOT/dist/tp-cascada.tar.gz"
  tar -czf "$OUT" -C "$STAGE" tp-cascada
  TOOL="tar"
fi
echo "created $OUT (using $TOOL)"
