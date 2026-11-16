"""Minimal read-only .xlsx reader (standard library only: no openpyxl or LibreOffice needed).

Returns plain strings per cell. Supports inline strings, shared strings and numbers; formulas are
read as their cached value. It never writes: the team's Excel is an original and stays untouched.
"""
import pathlib
import re
import xml.etree.ElementTree as ET
import zipfile

_M = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
_R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
_PKG = "{http://schemas.openxmlformats.org/package/2006/relationships}"


def _col_index(ref):
    """'C5' -> 2 (zero-based column)."""
    letters = re.match(r"[A-Z]+", ref).group(0)
    n = 0
    for ch in letters:
        n = n * 26 + (ord(ch) - 64)
    return n - 1


def _shared_strings(z):
    if "xl/sharedStrings.xml" not in z.namelist():
        return []
    root = ET.fromstring(z.read("xl/sharedStrings.xml"))
    return ["".join(t.text or "" for t in si.iter(_M + "t")) for si in root.findall(_M + "si")]


def _cell_text(c, shared):
    t = c.get("t")
    if t == "inlineStr":
        return "".join(x.text or "" for x in c.find(_M + "is").iter(_M + "t"))
    v = c.find(_M + "v")
    if v is None or v.text is None:
        return ""
    if t == "s":
        return shared[int(v.text)]
    return v.text


def read_workbook(path):
    """Return [(sheet_name, rows)] in workbook order; rows are lists of strings aligned by column."""
    path = pathlib.Path(path)
    if not path.exists():
        raise FileNotFoundError(path)
    with zipfile.ZipFile(path) as z:
        shared = _shared_strings(z)
        rels = {r.get("Id"): r.get("Target") for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels")).iter(_PKG + "Relationship")}
        out = []
        for s in ET.fromstring(z.read("xl/workbook.xml")).find(_M + "sheets"):
            target = rels[s.get(_R + "id")]
            member = target.lstrip("/") if target.startswith("/") else "xl/" + target
            rows = []
            for row in ET.fromstring(z.read(member)).iter(_M + "row"):
                cells = {}
                for c in row.findall(_M + "c"):
                    cells[_col_index(c.get("r"))] = _cell_text(c, shared)
                width = max(cells) + 1 if cells else 0
                rows.append([cells.get(i, "") for i in range(width)])
            out.append((s.get("name"), rows))
        return out
