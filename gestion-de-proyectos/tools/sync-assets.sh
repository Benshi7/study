#!/usr/bin/env bash
# Copies the shared assets into tp/assets/ so tp/ stays self-contained.
# Single source of truth: assets/. Never edit the synced files in tp/assets/ by hand.
# tp/assets/ also holds tp-only files that are NOT synced and live only there:
#   logic.js, tp-data.js, tp-common.js, tp.css, tp-nav.css
set -eu
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mkdir -p "$ROOT/tp/assets"
for f in course.css theme.js quiz.js; do
  cp "$ROOT/assets/$f" "$ROOT/tp/assets/$f"
  echo "synced tp/assets/$f"
done
