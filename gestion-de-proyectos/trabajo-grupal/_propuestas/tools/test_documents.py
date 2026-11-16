"""Checks that read the GENERATED documents (not the model) so they cannot be tautological.

Written before verify_documents.py; includes mutation tests proving each check can fail.
"""
import csv
import io
import pathlib
import re
import unittest

import verify_documents as vd

ROOT = pathlib.Path(__file__).resolve().parent.parent


class DocumentChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.docs = vd.load(ROOT)

    def test_all_checks_pass_on_generated_docs(self):
        for chk in vd.run(self.docs):
            self.assertTrue(chk.ok, f"{chk.name}: {chk.detail}")

    def test_seven_checks_exist(self):
        self.assertEqual(len(vd.run(self.docs)), 7)

    def test_gate_dates_mutation_detected(self):
        bad = dict(self.docs)
        bad["01"] = re.sub(r"\| G2 \|([^|]*)\| 01/05/2026 \|", r"| G2 |\1| 30/04/2026 |", self.docs["01"])
        self.assertNotEqual(bad["01"], self.docs["01"])
        res = {c.name: c for c in vd.run(bad)}
        self.assertFalse(res["hitos Charter = Gantt"].ok)

    def test_gate_mutation_in_the_gantt_csv_is_detected_too(self):
        bad = dict(self.docs)
        # move the end date of activity 35 (closes G7) in the schedule: the Charter and the Gantt then disagree
        bad["schedule"] = self.docs["schedule"].replace("09/09/2026", "10/09/2026")
        self.assertNotEqual(bad["schedule"], self.docs["schedule"])
        res = {c.name: c for c in vd.run(bad)}
        self.assertFalse(res["hitos Charter = Gantt"].ok)

    def test_budget_total_mutation_detected(self):
        bad = dict(self.docs)
        m = re.search(r"\*\*Presupuesto total\*\* \| \*\*(USD [\d.]+)\*\*", self.docs["01"])
        self.assertIsNotNone(m)
        bad["01"] = self.docs["01"].replace(m.group(1), "USD 1")
        res = {c.name: c for c in vd.run(bad)}
        self.assertFalse(res["presupuesto Charter = total"].ok)

    def test_charter_risk_not_in_matrix_detected(self):
        bad = dict(self.docs)
        bad["01"] = self.docs["01"].replace("**R01**", "**R99**", 1)
        res = {c.name: c for c in vd.run(bad)}
        self.assertFalse(res["riesgos Charter ⊂ matriz"].ok)

    def test_contingency_mutation_detected(self):
        bad = dict(self.docs)
        m = re.search(r"Reserva de contingencia \(Σ EMV de la matriz de riesgos\) \| (USD [\d.]+)", self.docs["01"])
        self.assertIsNotNone(m)
        bad["01"] = self.docs["01"].replace(m.group(1), "USD 1", 1)
        res = {c.name: c for c in vd.run(bad)}
        self.assertFalse(res["contingencia = Σ EMV"].ok)

    def test_labour_months_mutation_detected(self):
        rows = list(csv.reader(io.StringIO(self.docs["model"])))
        col = rows[0].index("Meses según Gantt")
        rows[1][col] = str(float(rows[1][col]) + 1.0)
        out = io.StringIO()
        csv.writer(out).writerows(rows)
        bad = dict(self.docs)
        bad["model"] = out.getvalue()
        res = {c.name: c for c in vd.run(bad)}
        self.assertFalse(res["mano de obra = duraciones del Gantt"].ok)

    def test_stakeholder_mutation_detected(self):
        bad = dict(self.docs)
        bad["01"] = self.docs["01"].replace("Vecinos y usuarios", "Los vecinos", 1)
        res = {c.name: c for c in vd.run(bad)}
        self.assertFalse(res["stakeholders Charter ∈ matriz ∈ comunicación"].ok)

    def test_bridge_missing_detected(self):
        bad = dict(self.docs)
        bad["06"] = re.sub(r"\| 8 \|[^\n]*\n", "", self.docs["06"])
        res = {c.name: c for c in vd.run(bad)}
        self.assertFalse(res["frase puente por sección"].ok)


if __name__ == "__main__":
    unittest.main()
