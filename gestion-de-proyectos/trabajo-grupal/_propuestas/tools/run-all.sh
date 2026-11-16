#!/usr/bin/env bash
# Rebuilds every artifact from the single source of truth (tools/data.py) and runs all tests.
# Usage: bash run-all.sh [--tests-only]
# Inputs: the team's Excel is read through tools/team_gantt.json (snapshot). If the team edits the Excel, run
#   python3 team_gantt.py   (rewrites the snapshot; a test fails until you do) and then this script.
# A test also guards the five originals in trabajo-grupal/ (tools/originals.sha256).
set -euo pipefail
cd "$(dirname "$0")"
if [[ "${1:-}" != "--tests-only" ]]; then
  python3 build_all.py
  python3 render.py
fi
python3 -m unittest discover -s . -p 'test_*.py' -v 2>&1 | tail -n 60
