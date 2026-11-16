"""Tests for the Charter filled in the cátedra's 24-field template (written first).

The .docx is built from the pack's single source of truth (build_all.compute) by tools/charter_template.py.
"""
import hashlib
import io
import pathlib
import re
import unittest
import xml.etree.ElementTree as ET
import zipfile

import build_all
import charter_template as ct
import data as D
from fmt import usd

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
TOOLS = pathlib.Path(__file__).resolve().parent
PACK = TOOLS.parent
RAW_TEMPLATE = PACK.parent.parent / "raw" / "Project_Charter_Template5.docx"
OUT = PACK / "01-charter" / "Project_Charter_completado.docx"


def _txt(e):
    return "".join(t.text or "" for t in e.iter(W + "t"))


def _rows(docx_bytes):
    z = zipfile.ZipFile(io.BytesIO(docx_bytes))
    root = ET.fromstring(z.read("word/document.xml"))
    out = []
    for tbl in root.iter(W + "tbl"):
        for tr in tbl.iter(W + "tr"):
            out.append(tr)
    return root, out


def field_text(docx_bytes, n):
    """Text of every cell in the row(s) that follow the label '(n)': value cells only."""
    _, rows = _rows(docx_bytes)
    for i, tr in enumerate(rows):
        cells = [_txt(tc).strip() for tc in tr.findall(W + "tc")]
        if cells and cells[0].replace(" ", "").startswith(f"({n})"):
            if n in (3,):
                return " | ".join(_txt(tc) for tc in rows[i + 1].findall(W + "tc"))
            if n == 13:
                return " | ".join(_txt(tc) for tc in rows[i + 1].findall(W + "tc"))
            if n in (10, 11):
                j, parts = i + 1, []
                while j < len(rows):
                    cs = [_txt(tc).strip() for tc in rows[j].findall(W + "tc")]
                    if cs and cs[0].replace(" ", "").startswith("(") and cs[0][1:3].replace(")", "").isdigit():
                        break
                    parts.append(" | ".join(cs))
                    j += 1
                return "\n".join(parts)
            return " | ".join(cells[1:])
    raise AssertionError(f"field ({n}) not found")


class TemplateIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.o, *_ = build_all.compute(with_sens=False)
        cls.data = ct.build_bytes(cls.o)
        cls.tpl = RAW_TEMPLATE.read_bytes()

    def test_valid_docx_zip_with_the_same_members(self):
        z = zipfile.ZipFile(io.BytesIO(self.data))
        self.assertIsNone(z.testzip())
        self.assertEqual(sorted(z.namelist()), sorted(zipfile.ZipFile(io.BytesIO(self.tpl)).namelist()))
        ET.fromstring(z.read("word/document.xml"))                       # well formed

    def test_root_declares_every_namespace_listed_in_ignorable(self):
        xml = zipfile.ZipFile(io.BytesIO(self.data)).read("word/document.xml").decode("utf-8")
        root_tag = xml[: xml.index(">", xml.index("<w:document")) + 1]
        ignorable = re.search(r'mc:Ignorable="([^"]+)"', root_tag).group(1).split()
        for prefix in ignorable:
            self.assertIn(f"xmlns:{prefix}=", root_tag, prefix)

    def test_other_parts_are_byte_identical(self):
        a, b = zipfile.ZipFile(io.BytesIO(self.data)), zipfile.ZipFile(io.BytesIO(self.tpl))
        for name in b.namelist():
            if name != "word/document.xml":
                self.assertEqual(a.read(name), b.read(name), name)

    def test_all_24_labels_survive(self):
        full = "".join(_txt(r) for r in _rows(self.data)[1])
        full = full.replace(" ", "")
        for n in range(1, 25):
            self.assertIn(f"({n})", full, n)

    def test_template_label_cells_are_unchanged(self):
        _, tpl_rows = _rows(self.tpl)
        _, out_rows = _rows(self.data)
        tpl_labels = [_txt(tc).strip() for tr in tpl_rows for tc in tr.findall(W + "tc") if _txt(tc).strip()]
        out_labels = [_txt(tc).strip() for tr in out_rows for tc in tr.findall(W + "tc") if _txt(tc).strip()]
        it = iter(out_labels)
        for label in tpl_labels:
            self.assertTrue(any(label == x for x in it), f"label lost or reordered: {label!r}")

    def test_template_in_raw_is_untouched(self):
        recorded = {}
        for line in (TOOLS / "inputs.sha256").read_text(encoding="utf-8").splitlines():
            h, _, name = line.partition("  ")
            recorded[name.strip()] = h
        self.assertIn("raw/Project_Charter_Template5.docx", recorded)
        self.assertEqual(hashlib.sha256(self.tpl).hexdigest(), recorded["raw/Project_Charter_Template5.docx"])

    def test_filled_rows_can_grow(self):
        _, rows = _rows(self.data)
        for tr in rows:
            if len(_txt(tr)) > 150:
                h = tr.find(W + "trPr/" + W + "trHeight")
                if h is not None:
                    self.assertNotEqual(h.get(W + "hRule"), "exact", _txt(tr)[:50])

    def test_build_is_deterministic(self):
        self.assertEqual(ct.build_bytes(self.o), self.data)

    def test_signature_block_stays_blank(self):
        root, _ = _rows(self.data)
        text = "".join(_txt(p) for p in root.iter(W + "p"))
        tail = text[text.index("Signature(s)/Dates"):]
        base = "".join(_txt(p) for p in ET.fromstring(zipfile.ZipFile(io.BytesIO(self.tpl)).read("word/document.xml")).iter(W + "p"))
        base_tail = base[base.index("Signature(s)/Dates"):]
        self.assertEqual(tail, base_tail + ct.DRAFT_NOTE)
        for word in ("firmado por", "aprobado por"):
            self.assertNotIn(word, tail.lower())


class ContentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.o, *_ = build_all.compute(with_sens=False)
        cls.data = ct.build_bytes(cls.o)
        cls.lb = cls.o["ladder_b"]

    def test_field_1_title(self):
        self.assertIn("Modernización del Mapa Interactivo de la Ciudad", field_text(self.data, 1))

    def test_summary_budget_matches_the_pack(self):
        t = field_text(self.data, 12)
        for v in (self.lb["total"], self.lb["baseline"], self.lb["mgmt_reserve"], self.o["maint_usd"]):
            self.assertIn(usd(v), t)
        self.assertIn("ARS", t)                                          # the exchange rate is declared
        self.assertIn("a confirmar", t.lower())

    def test_budget_field_tracks_the_exchange_rate(self):
        o2, *_ = build_all.compute(fx=2 * self.o["fx"]["value"], with_sens=False)
        t2 = field_text(ct.build_bytes(o2), 12)
        self.assertIn(usd(o2["ladder_b"]["total"]), t2)
        self.assertNotIn(usd(self.lb["total"]), t2)

    def test_milestones_are_the_eight_gates_with_dates(self):
        t = field_text(self.data, 11)
        for h in D.TEAM["hitos"]:
            self.assertIn(h["name"], t)
            self.assertIn(h["date"].strftime("%d/%m/%Y"), t)
        self.assertEqual(len(D.TEAM["hitos"]), 8)

    def test_high_level_risks_are_the_flagged_ones(self):
        t = field_text(self.data, 14)
        hl = [r for r in self.o["risks"]["sorted"] if r["hl"]]
        self.assertGreaterEqual(len(hl), 5)
        for r in hl:
            self.assertIn(r["name"], t)
            self.assertIn(r["id"], t)

    def test_stakeholders_list_has_the_critical_ones(self):
        t = field_text(self.data, 10)
        for needle in ("Sponsor institucional", "Hacienda", "Project Manager", "USIG", "Transporte", "Cultura", "canales", "Vecinos"):
            self.assertIn(needle, t)
        self.assertGreaterEqual(len([ln for ln in t.splitlines() if "|" in ln]), 9)

    def test_assumptions_and_constraints_declare_simulation_and_fx(self):
        t = field_text(self.data, 13).lower()
        self.assertIn("simulad", t)
        self.assertIn("tipo de cambio", t)

    def test_segment_is_households(self):
        t = (field_text(self.data, 2) + field_text(self.data, 16) + field_text(self.data, 7)).lower()
        self.assertIn("hogares", t)

    def test_objectives_have_the_four_results(self):
        t = field_text(self.data, 7)
        for needle in ("Capa geográfica confiable", "Integración multicanal", "Reportes y seguimiento", "propuesta"):
            self.assertIn(needle, t)

    def test_honest_minimal_fields(self):
        for n in (15, 21, 23):
            t = field_text(self.data, n).lower()
            self.assertTrue("no aplica" in t or "a confirmar" in t, n)
        self.assertIn("a confirmar", field_text(self.data, 23).lower())

    def test_work_site_is_not_invented(self):
        t = field_text(self.data, 8).lower()
        self.assertIn("a confirmar", t)

    def test_no_phone_numbers_or_personal_names(self):
        root, _ = _rows(self.data)
        text = " ".join(_txt(p) for p in root.iter(W + "p"))
        self.assertIsNone(re.search(r"\+?\d[\d\s-]{9,}\d", text))

    def test_in_the_conditional_scope_clarification(self):
        t = field_text(self.data, 6) + field_text(self.data, 13)
        self.assertIn("perfil de hogar básico", t.lower())


class FileAndReadmeTests(unittest.TestCase):
    def test_written_file_equals_the_build(self):
        o, *_ = build_all.compute(with_sens=False)
        self.assertTrue(OUT.exists(), "run tools/render.py")
        self.assertEqual(OUT.read_bytes(), ct.build_bytes(o))

    def test_readme_maps_the_24_fields_and_the_13_elements(self):
        t = (PACK / "01-charter" / "README.md").read_text(encoding="utf-8")
        for n in range(1, 25):
            self.assertRegex(t, rf"\|\s*\({n}\)", n)
        for el in ("Propósito o Justificación", "Descripción de Alto Nivel", "Objetivos del Proyecto", "Requisitos de Alto Nivel",
                   "Descripción del Producto", "Suposiciones y Restricciones", "Cronograma de Alto Nivel", "Presupuesto de Alto Nivel",
                   "Riesgos de Alto Nivel", "Criterios de Éxito", "Stakeholders Principales", "Responsabilidades y Autoridad",
                   "Requisitos de Aprobación"):
            self.assertIn(el, t)
        self.assertIn("Anexo A", t)
        self.assertIn("Clase 3", t)

    def test_condensed_charter_points_to_the_template_format(self):
        t = (PACK / "01-charter-condensado.md").read_text(encoding="utf-8")
        self.assertIn("Project_Charter_completado.docx", t)
        self.assertIn("plantilla", t.lower())


if __name__ == "__main__":
    unittest.main()
