#!/usr/bin/env bash
# Runs the tests for the shareable deliverable (compartir/).
# Usage: tools/test-compartir.sh
# Checks the canvas data, rebuilds the deliverable, and verifies privacy / self-containment.
set -euo pipefail
cd "$(dirname "$0")/.."
command -v node >/dev/null || { echo "node is required" >&2; exit 2; }
exec node tools/test-compartir.mjs
