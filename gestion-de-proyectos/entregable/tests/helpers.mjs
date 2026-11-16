// Shared helpers for the entregable tests: read a .docx without Word, parse the markdown sources.
import { createRequire } from "node:module";
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";
import { DOMParser } from "@xmldom/xmldom";
import AdmZip from "adm-zip";
import MarkdownIt from "markdown-it";

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
export const REPO = path.resolve(ROOT, "..");
export const DIST_DOCX = path.join(ROOT, "dist", "TP_Cascada_Grupo01.docx");
export const DIST_MD = path.join(ROOT, "dist", "TP_Cascada_Grupo01.md");
export const SRC_DIR = path.join(ROOT, "src");
export const ORIG_DIR = path.join(REPO, "trabajo-grupal");

export const md = new MarkdownIt({ html: false, linkify: false }).enable("table");

export function srcFiles() {
  return fs.readdirSync(SRC_DIR).filter((f) => f.endsWith(".md")).sort();
}

export function readSrc(f) {
  return fs.readFileSync(path.join(SRC_DIR, f), "utf8");
}

// ---------- tokens / words ----------
export function tokens(text) {
  return (text.toLowerCase().match(/[\p{L}\p{N}]+/gu) || []);
}

export function multiset(list) {
  const m = new Map();
  for (const t of list) m.set(t, (m.get(t) || 0) + 1);
  return m;
}

// tokens present in `a` and not (enough) in `b`
export function diffCount(a, b) {
  const mb = multiset(b);
  let missing = 0;
  const seen = new Map();
  for (const t of a) {
    const used = (seen.get(t) || 0) + 1;
    seen.set(t, used);
    if (used > (mb.get(t) || 0)) missing++;
  }
  return missing;
}

// ---------- markdown model ----------
// Flatten a markdown source into { headings, tables:[{rows, cols}], images:[{alt, src}], text }
export function mdModel(source) {
  const toks = md.parse(source, {});
  const headings = [];
  const tables = [];
  const images = [];
  const textParts = [];
  let curTable = null;
  let inTable = false;
  for (let i = 0; i < toks.length; i++) {
    const t = toks[i];
    if (t.type === "table_open") { curTable = { rows: 0, cols: 0, cells: [] }; inTable = true; }
    if (t.type === "tr_open" && curTable) { curTable.rows++; curTable._c = 0; }
    if (t.type === "th_open" || t.type === "td_open") { if (curTable) curTable._c++; }
    if (t.type === "tr_close" && curTable) curTable.cols = Math.max(curTable.cols, curTable._c);
    if (t.type === "table_close") { tables.push(curTable); curTable = null; inTable = false; }
    if (t.type === "heading_open") {
      const inline = toks[i + 1];
      headings.push({ level: Number(t.tag.slice(1)), text: inline.children.map((c) => c.content).join("") });
    }
    if (t.type === "inline") {
      for (const c of t.children || []) {
        if (c.type === "image") images.push({ alt: c.content, src: c.attrGet("src") });
      }
      const plain = (t.children || [])
        .filter((c) => c.type !== "image")
        .map((c) => (c.type === "softbreak" || c.type === "hardbreak" ? " " : c.content))
        .join("");
      if (plain.trim() !== "[[TOC]]" && !/^Tabla: /.test(plain)) textParts.push(plain); // 'Tabla: x' lines are captions
      if (curTable && inTable) curTable.cells.push(plain);
    }
  }
  return { headings, tables, images, text: textParts.join("\n") };
}

export function mdWords(source) {
  return tokens(mdModel(source).text);
}

// ---------- docx model ----------
const W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main";

export function parseXml(xml) {
  const errors = [];
  const doc = new DOMParser({
    onError: (level, msg) => { if (level !== "warning") errors.push(msg); },
  }).parseFromString(xml, "text/xml");
  return { doc, errors };
}

function kids(node, name) {
  const out = [];
  for (let c = node.firstChild; c; c = c.nextSibling) if (c.nodeType === 1 && c.nodeName === name) out.push(c);
  return out;
}
function all(node, name) {
  return Array.from(node.getElementsByTagName(name));
}
function textOf(node) {
  return all(node, "w:t").map((t) => t.textContent).join("");
}
function paraInfo(p) {
  const pPr = kids(p, "w:pPr")[0];
  const style = pPr && kids(pPr, "w:pStyle")[0] ? kids(pPr, "w:pStyle")[0].getAttribute("w:val") : "";
  const sect = pPr ? kids(pPr, "w:sectPr")[0] : null;
  const drawings = all(p, "w:drawing");
  const instr = all(p, "w:instrText").map((i) => i.textContent);
  return {
    type: "p",
    style,
    text: textOf(p),
    drawings: drawings.map((d) => {
      const docPr = d.getElementsByTagName("wp:docPr")[0];
      const ext = d.getElementsByTagName("wp:extent")[0];
      return { descr: docPr ? docPr.getAttribute("descr") : "", cx: ext ? Number(ext.getAttribute("cx")) : 0, cy: ext ? Number(ext.getAttribute("cy")) : 0 };
    }),
    instr,
    sectLandscape: sect ? (kids(sect, "w:pgSz")[0] || { getAttribute: () => "" }).getAttribute("w:orient") === "landscape" : null,
    hasSect: !!sect,
  };
}

export function docxModel(file) {
  const zip = new AdmZip(file);
  const entries = zip.getEntries().map((e) => e.entryName);
  const parts = {};
  for (const n of entries) if (/\.(xml|rels)$/.test(n)) parts[n] = zip.readAsText(n);
  const { doc } = parseXml(parts["word/document.xml"]);
  const body = doc.getElementsByTagName("w:body")[0];
  const blocks = [];
  const walk = (parent) => {
    for (let c = parent.firstChild; c; c = c.nextSibling) {
      if (c.nodeType !== 1) continue;
      if (c.nodeName === "w:sdt") { const content = kids(c, "w:sdtContent")[0]; if (content) walk(content); }
      else if (c.nodeName === "w:p") blocks.push(paraInfo(c));
      else if (c.nodeName === "w:tbl") {
        const rows = kids(c, "w:tr").map((tr) => kids(tr, "w:tc").map((tc) => all(tc, "w:p").map(textOf).join(" ").trim()));
        const hdr = kids(c, "w:tr")[0];
        const repeatsHeader = !!(hdr && all(hdr, "w:tblHeader").length);
        blocks.push({ type: "tbl", rows, repeatsHeader });
      } else if (c.nodeName === "w:sectPr") {
        const pg = kids(c, "w:pgSz")[0];
        blocks.push({ type: "sect", landscape: pg && pg.getAttribute("w:orient") === "landscape" });
      }
    }
  };
  walk(body);
  return { zip, entries, parts, blocks };
}

export function isHeading(b) {
  return b.type === "p" && ["Heading1", "UnnumberedHeading"].includes(b.style);
}

// Split docx blocks into segments starting at each Heading1 / UnnumberedHeading
export function segments(model) {
  const segs = [];
  let cur = null;
  for (const b of model.blocks) {
    if (isHeading(b)) { cur = { heading: b, blocks: [] }; segs.push(cur); }
    else if (cur) cur.blocks.push(b);
  }
  return segs;
}

const SKIP_STYLES = new Set(["Caption", "TOCHeading"]);
const skipStyle = (s) => SKIP_STYLES.has(s) || /^TOC\d?$/i.test(s) || /^Contents/i.test(s);
export function segmentWords(seg) {
  const parts = [seg.heading.text];
  for (const b of seg.blocks) {
    if (b.type === "p" && !skipStyle(b.style)) parts.push(b.text);
    if (b.type === "tbl") for (const r of b.rows) parts.push(r.join(" "));
  }
  return tokens(parts.join("\n"));
}

// ---------- original docx text (to check the converter did not lose content) ----------
export function originalBlocks(fileName) {
  return docxModel(path.join(ORIG_DIR, fileName)).blocks;
}

export function sha256(file) {
  return crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
}

// ---------- minimal xlsx reader (inline strings + shared strings), read-only ----------
function colIndex(ref) {
  const letters = /^[A-Z]+/.exec(ref)[0];
  let n = 0;
  for (const ch of letters) n = n * 26 + (ch.charCodeAt(0) - 64);
  return n - 1;
}
export function readXlsx(file) {
  const zip = new AdmZip(file);
  const shared = [];
  if (zip.getEntry("xl/sharedStrings.xml")) {
    const { doc } = parseXml(zip.readAsText("xl/sharedStrings.xml"));
    for (const si of Array.from(doc.getElementsByTagName("si"))) shared.push(Array.from(si.getElementsByTagName("t")).map((t) => t.textContent).join(""));
  }
  const wb = parseXml(zip.readAsText("xl/workbook.xml")).doc;
  const rels = {};
  for (const r of Array.from(parseXml(zip.readAsText("xl/_rels/workbook.xml.rels")).doc.getElementsByTagName("Relationship"))) rels[r.getAttribute("Id")] = r.getAttribute("Target");
  const out = [];
  for (const s of Array.from(wb.getElementsByTagName("sheet"))) {
    const target = rels[s.getAttribute("r:id")];
    const member = target.startsWith("/") ? target.slice(1) : "xl/" + target;
    const sheet = parseXml(zip.readAsText(member)).doc;
    const rows = [];
    for (const row of Array.from(sheet.getElementsByTagName("row"))) {
      const cells = [];
      for (const c of Array.from(row.getElementsByTagName("c"))) {
        const t = c.getAttribute("t");
        let v = "";
        if (t === "inlineStr") v = Array.from(c.getElementsByTagName("t")).map((x) => x.textContent).join("");
        else {
          const ve = c.getElementsByTagName("v")[0];
          v = ve ? ve.textContent : "";
          if (t === "s") v = shared[Number(v)];
        }
        cells[colIndex(c.getAttribute("r"))] = v;
      }
      rows.push(Array.from(cells, (x) => x ?? ""));
    }
    out.push({ name: s.getAttribute("name"), rows });
  }
  return out;
}
