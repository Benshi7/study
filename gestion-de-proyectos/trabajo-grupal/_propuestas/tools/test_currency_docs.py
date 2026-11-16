"""Checks over the GENERATED documents for the USD / households / format-of-delivery revision.

They read the files written by render.py (not the model), so they cannot be tautological.
"""
import csv
import io
import pathlib
import re
import unittest

import data as D
from fmt import n

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONSIGNA = ["Carátula", "Índice", "Canvas del proyecto", "Aplicar Design Thinking", "Project Charter",
            "Gantt del proyecto completo", "Matriz de stakeholders", "Plan de comunicación",
            "Gestión de riesgos - Matriz de riesgos", "Gestión de costos - Presupuesto"]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def section(text, heading):
    """Text between a '## <heading>' line and the next '## ' line."""
    m = re.search(rf"^## {re.escape(heading)}[^\n]*\n(.*?)(?=^## |\Z)", text, flags=re.M | re.S)
    return m.group(1) if m else ""


class CurrencyTests(unittest.TestCase):
    DOCS = ["00-resumen.md", "01-charter-condensado.md", "03-presupuesto/presupuesto.md", "04-riesgos.md",
            "05-canvas-dt-smart.md", "06-coherencia.md", "07-formato-entrega.md"]

    def test_no_leftover_ars_million_notation(self):
        for rel in self.DOCS:
            self.assertIsNone(re.search(r"\$\s?[\d.,]+ M\b", read(rel)), f"{rel} still has '$… M' amounts")

    def test_budget_doc_declares_the_single_exchange_rate(self):
        t = read("03-presupuesto/presupuesto.md")
        self.assertIn("Tipo de cambio", t)
        self.assertIn(n(D.FX_ARS_PER_USD, 2), t)
        self.assertIn(D.FX_DATE.strftime("%d/%m/%Y"), t)
        self.assertIn("Banco Nación", t)
        self.assertIn("a confirmar", t.split("Tipo de cambio", 1)[1][:600])

    def test_budget_doc_has_fx_sensitivity_and_how_numbers_are_built(self):
        t = read("03-presupuesto/presupuesto.md")
        self.assertIn("Cómo se construye cada número", t)
        self.assertIn("Sensibilidad al tipo de cambio", t)
        self.assertIn("Clase 4", t)


class DesgloseTests(unittest.TestCase):
    COLS = ["ID", "Concepto", "Categoría", "Paquete de trabajo", "Comportamiento", "Asignación",
            "Método de estimación (Clase 4)", "Cantidad", "Unidad", "Costo unitario (USD)",
            "Duración (meses según Gantt)", "Subtotal equipo (USD)", "Subtotal escenario B (USD)",
            "Equivalente equipo (ARS M)", "Supuesto", "Fuente", "Meses en que se incurre", "Días hábiles (Gantt)"]

    def setUp(self):
        self.rows = list(csv.DictReader(io.StringIO(read("03-presupuesto/desglose.csv"))))

    def test_columns_and_row_count(self):
        self.assertEqual(list(self.rows[0].keys()), self.COLS)
        self.assertEqual(len(self.rows), 32)

    def test_no_empty_cells(self):
        for r in self.rows:
            for c in self.COLS:
                self.assertNotEqual(r[c].strip(), "", f"{r['ID']} / {c}")

    def test_costs_of_the_project_match_the_budget_doc(self):
        project = sum(int(r["Subtotal escenario B (USD)"]) for r in self.rows if r["Categoría"] != "Mantenimiento inicial")
        m = re.search(r"\| Costos del proyecto \(sin reservas\) \| [^|]*\| [^|]*\| USD ([\d.]+) \|", read("03-presupuesto/presupuesto.md"))
        self.assertIsNotNone(m)
        self.assertEqual(int(m.group(1).replace(".", "")), project)

    def test_model_csv_is_in_usd(self):
        header = next(csv.reader(io.StringIO(read("03-presupuesto/model.csv"))))
        self.assertTrue(any("USD" in h for h in header), header)
        self.assertFalse(any("(M)" in h for h in header), header)


class SegmentTests(unittest.TestCase):
    def test_segment_is_households_in_general(self):
        t = read("05-canvas-dt-smart.md")
        self.assertIn("Hogares de la Ciudad", t)
        self.assertIn("cada hogar", t.lower())
        self.assertIn("opt-in", t)

    def test_household_types_are_personas_not_segments(self):
        t = read("05-canvas-dt-smart.md")
        self.assertIn("Personas", t)
        for w in ("hogar con niños", "adulto mayor", "movilidad reducida"):
            self.assertIn(w, t)

    def test_old_segment_decision_is_gone(self):
        for rel in ("00-resumen.md", "05-canvas-dt-smart.md", "06-coherencia.md"):
            t = read(rel)
            self.assertNotIn("vecinos que reportan", t, rel)
            self.assertNotIn("en lugar de hogares con chicos", t, rel)

    def test_charter_clarification_is_conditional_not_a_contradiction(self):
        t = read("05-canvas-dt-smart.md")
        self.assertIn("perfil de hogar básico", t)
        self.assertIn("que no sean necesarias", t)
        self.assertNotIn("**excluye** el", t)
        self.assertIn("perfil de hogar básico", read("01-charter-condensado.md"))

    def test_freeze_list_has_currency_fx_and_segment(self):
        t = read("06-coherencia.md")
        self.assertRegex(t, r"\| Moneda \| [^\n]*USD")
        self.assertIn(n(D.FX_ARS_PER_USD, 2), t)
        self.assertRegex(t, r"\| Segmento \| [^\n]*Hogares de la Ciudad")

    def test_risk_register_has_fx_and_household_data(self):
        t = read("04-riesgos.md")
        self.assertIn("R19", t)
        self.assertIn("tipo de cambio", t.lower())
        self.assertIn("hogar", t.lower())


class FormatDeliveryTests(unittest.TestCase):
    def setUp(self):
        self.t = read("07-formato-entrega.md")

    def test_answers_the_teammate_with_one_document(self):
        self.assertIn("un solo documento", self.t)
        self.assertIn("Word", self.t)
        self.assertIn("PDF", self.t)
        self.assertIn("Anexo", self.t)

    def test_lists_the_ten_points_of_the_consigna_in_order(self):
        sec = section(self.t, "Orden del documento")
        titles = re.findall(r"^(?:\d+)\. (.+)$", sec, flags=re.M)
        self.assertEqual(titles, CONSIGNA)

    def test_twenty_item_tidiness_checklist(self):
        sec = section(self.t, "Checklist de prolijidad")
        self.assertEqual(len(re.findall(r"^- \[ \] ", sec, flags=re.M)), 20)

    def test_ten_bridge_sentences(self):
        sec = section(self.t, "Frases puente")
        rows = re.findall(r"^\| (Apertura|\d+|Cierre) \| (.+) \|$", sec, flags=re.M)
        self.assertEqual(len(rows), 10)
        for key, phrase in rows:
            self.assertGreaterEqual(len(phrase.split()), 8, key)

    def test_has_simulation_line_and_style_spec_pieces(self):
        for w in ("supuesto de simulación", "dd/mm/aaaa", "USD", "R01", "G1", "Índice automático", "Pie de figura"):
            self.assertIn(w, self.t, w)

    def test_two_day_plan_with_three_dates(self):
        sec = section(self.t, "Plan de 2 días")
        for d in ("12/10", "13/10", "14/10"):
            self.assertIn(d, sec)
        for w in ("Bloqueantes", "Mejoran la nota", "Defensa"):
            self.assertIn(w, sec)

    def test_ready_to_paste_reply(self):
        sec = section(self.t, "Respuesta lista para pegar")
        self.assertGreaterEqual(len(re.findall(r"^> ", sec, flags=re.M)), 2)

    def test_merge_map_present(self):
        self.assertIn("Mapa de fusión", self.t)

    def test_no_names_or_phone_numbers(self):
        self.assertIsNone(re.search(r"\+?54\s?9?\s?11[\s-]?\d{4}[\s-]?\d{4}", self.t))
        self.assertIsNone(re.search(r"\b\d{4}[\s-]\d{4}\b", self.t))


class SummaryTests(unittest.TestCase):
    def test_new_problems_6_and_7_and_mock_later(self):
        t = read("00-resumen.md")
        self.assertRegex(t, r"\| 6 · [^\n]*[Ff]ormato")
        self.assertRegex(t, r"\| 7 · [^\n]*[Pp]resupuesto[^\n]*números")
        self.assertIn("Para después", t)
        self.assertIn("mock", t.lower())
        self.assertIn("hogares", t.lower())
        self.assertIn("USD", t)


if __name__ == "__main__":
    unittest.main()
