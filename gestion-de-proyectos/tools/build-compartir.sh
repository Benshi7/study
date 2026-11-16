#!/usr/bin/env bash
# Builds the shareable deliverable: compartir/tp-cascada-canvas-y-partes.html
#
#   compartir/src/tp-cascada.template.html   page text, CSS and behaviour (edit this for prose)
#   compartir/src/render.js                  renders the Canvas section from the data
#   tp/assets/canvas-data.js                 SINGLE SOURCE OF TRUTH for the 4 Canvas options
#                                            (also loaded by tp/canvas-taller.html)
#
# Usage: tools/build-compartir.sh      then: tools/test-compartir.sh
# Needs node. The output is one self-contained file: the data is inlined and the
# Canvas section is pre-rendered, so all four options show even without JavaScript.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
command -v node >/dev/null || { echo "node is required" >&2; exit 2; }

node - "$ROOT" <<'NODE'
const fs = require('fs');
const path = require('path');
const root = process.argv[2];
const dataPath = path.join(root, 'tp/assets/canvas-data.js');
const tplPath = path.join(root, 'compartir/src/tp-cascada.template.html');
const outPath = path.join(root, 'compartir/tp-cascada-canvas-y-partes.html');
const fail = (m) => { console.error('build-compartir: ' + m); process.exit(1); };

const tpl = fs.readFileSync(tplPath, 'utf8');
const dataSrc = fs.readFileSync(dataPath, 'utf8');
const data = require(dataPath);
const render = require(path.join(root, 'compartir/src/render.js'));

const once = (s, m) => s.split(m).length === 2;
if (!once(tpl, '<!--CANVAS_SECTION-->')) fail('template must contain <!--CANVAS_SECTION--> exactly once');
if (!once(tpl, '<!--CANVAS_DATA-->')) fail('template must contain <!--CANVAS_DATA--> exactly once');
if (/<\/script/i.test(dataSrc)) fail('canvas-data.js must not contain "</script"');

// The data file starts with a maintainer banner that mentions workspace paths: do not ship it.
const shipped = dataSrc.replace(/^\s*\/\*[\s\S]*?\*\/\s*/, '');

const out = tpl
  .replace('<!--CANVAS_SECTION-->', () => render.renderCanvasSection(data))
  .replace('<!--CANVAS_DATA-->', () => '<script>\n' + shipped.trimEnd() + '\n</script>');

fs.writeFileSync(outPath, out);
console.log('built ' + path.relative(root, outPath) + ' (' + Buffer.byteLength(out) + ' bytes)');
NODE
