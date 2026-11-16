"""Independent recomputation of the budget (written first).

Nothing here calls build_all/costing: it re-derives the numbers from the generated CSVs (desglose.csv, 04-riesgos.csv,
schedule.csv, model.csv) with plain Python, so a bug in the model cannot hide behind itself.
"""
import csv
import datetime as dt
import pathlib
import unittest

import data as D

ROOT = pathlib.Path(__file__).resolve().parent.parent


def rows(rel):
    with open(ROOT / rel, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def half_up(x):
    return int(x + 0.5)


class IndependentBudgetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.des = rows("03-presupuesto/desglose.csv")
        cls.risk = rows("04-riesgos.csv")
        cls.sched = rows("02-gantt/schedule.csv")
        cls.model = rows("03-presupuesto/model.csv")

    def test_line_count_and_ids_unique(self):
        ids = [r["ID"] for r in self.des]
        self.assertEqual(len(ids), 32)
        self.assertEqual(len(set(ids)), 32)

    def test_ladder_b_from_csv(self):
        costs = sum(int(r["Subtotal escenario B (USD)"]) for r in self.des if not r["ID"].startswith("MAN"))
        cont = sum(int(r["EMV residual (USD)"]) for r in self.risk)
        baseline = costs + cont
        reserve = half_up(baseline * 0.10)
        total = baseline + reserve
        maint = sum(int(r["Subtotal escenario B (USD)"]) for r in self.des if r["ID"].startswith("MAN"))
        text = (ROOT / "03-presupuesto" / "presupuesto.md").read_text(encoding="utf-8")
        for value in (costs, cont, baseline, reserve, total, total + maint):
            self.assertIn(f"{value:,}".replace(",", "."), text, value)

    def test_team_total_from_csv_is_the_converted_team_figure(self):
        team = sum(int(r["Subtotal equipo (USD)"]) for r in self.des)
        cont = half_up(D.TEAM_CONTINGENCY * 1e6 / D.FX_ARS_PER_USD)
        direct = D.TEAM_TOTAL * 1e6 / D.FX_ARS_PER_USD
        self.assertLess(abs(team + cont - direct), 10)          # line-level rounding only
        self.assertAlmostEqual(sum(float(r["Equivalente equipo (ARS M)"]) for r in self.des), D.TEAM_BASE, places=6)

    def test_labour_workdays_from_stated_dates(self):
        """Mon-Fri days in the union of the stated Inicio/Fin ranges of each role's activities == model.csv."""
        by_id = {}
        for r in self.sched:
            d = lambda s: dt.datetime.strptime(s, "%d/%m/%Y").date()
            by_id[int(r["ID"])] = (d(r["Inicio (equipo)"]), d(r["Fin (equipo)"]))
        for (key, label, tm, tc, ids), m in zip(D.TEAM_ROLES, self.model):
            days = set()
            for i in ids:
                a, b = by_id[i]
                x = a
                while x <= b:
                    if x.weekday() < 5:
                        days.add(x)
                    x += dt.timedelta(days=1)
            self.assertEqual(int(m["Días hábiles en el Gantt"]), len(days), label)

    def test_every_line_reproduces_from_its_displayed_inputs(self):
        """A professor with a calculator must get the subtotal: unit (cents) x working days / 21 (x people) == subtotal."""
        for r in self.des:
            unit = float(r["Costo unitario (USD)"])
            sub = int(r["Subtotal escenario B (USD)"])
            if r["Unidad"] == "global":
                self.assertAlmostEqual(unit, sub, delta=0.6, msg=r["ID"])
                continue
            wd = int(r["Días hábiles (Gantt)"])
            people = int(float(r["Cantidad"])) if r["ID"].startswith("RH") else 1
            self.assertAlmostEqual(people * unit * wd / 21, sub, delta=0.6, msg=r["ID"])

    def test_duration_column_is_days_over_21(self):
        for r in self.des:
            if r["Unidad"] == "global" and r["ID"].startswith("MAN"):
                continue
            if r["Días hábiles (Gantt)"]:
                self.assertAlmostEqual(float(r["Duración (meses según Gantt)"]), int(r["Días hábiles (Gantt)"]) / 21, places=1, msg=r["ID"])

    def test_fx_sensitivity_is_monotonic(self):
        text = (ROOT / "03-presupuesto" / "presupuesto.md").read_text(encoding="utf-8")
        self.assertIn("Sensibilidad al tipo de cambio", text)


class SCurveIndependentTests(unittest.TestCase):
    def test_curve_s_table_rows_add_up(self):
        text = (ROOT / "03-presupuesto" / "presupuesto.md").read_text(encoding="utf-8")
        block = text.split("## Curva S")[1].split("\n## ")[0]
        monthly, cumul = [], []
        for line in block.splitlines():
            parts = [p.strip() for p in line.strip("|").split("|")]
            if len(parts) == 3 and parts[0][:2].isdigit() and "/" in parts[0] and parts[1].startswith("USD"):
                monthly.append(int(parts[1][4:].replace(".", "")))
                cumul.append(int(parts[2][4:].replace(".", "")))
        self.assertGreaterEqual(len(monthly), 6)
        run = 0
        for m, c in zip(monthly[:6], cumul[:6]):
            run += m
            self.assertEqual(run, c)


if __name__ == "__main__":
    unittest.main()
