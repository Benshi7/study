"""Tests for the budget audit additions (written first): Clase 4 p24 pyramid, like-for-like bridge,
baseline S-curve with contingency, p17 rubric mapping and the generated audit documents."""
import pathlib
import unittest

import build_all
import costing
import data as D
from fmt import pct, usd

ROOT = pathlib.Path(__file__).resolve().parent.parent


class PyramidTests(unittest.TestCase):
    """Clase 4 p24: activity -> work package -> accounting centre -> project (+contingency = baseline; +management reserve = budget)."""

    @classmethod
    def setUpClass(cls):
        cls.o, *_ = build_all.compute(with_sens=False)
        cls.p = cls.o["pyramid"]

    def test_levels_foot(self):
        p = self.p
        self.assertEqual(sum(c["usd"] for c in p["centers"]), p["project"])
        self.assertEqual(p["project"] + p["contingency"], p["baseline"])
        self.assertEqual(p["baseline"] + p["mgmt_reserve"], p["total"])

    def test_matches_the_scenario_b_ladder(self):
        lb = self.o["ladder_b"]
        self.assertEqual(self.p["total"], lb["total"])
        self.assertEqual(self.p["baseline"], lb["baseline"])
        self.assertEqual(self.p["project"], lb["project_costs"])

    def test_maintenance_is_not_an_accounting_centre_of_the_baseline(self):
        labels = [c["label"] for c in self.p["centers"]]
        self.assertNotIn("Mantenimiento inicial", labels)
        self.assertEqual(len(labels), 5)

    def test_work_packages_count(self):
        n = sum(1 for l in self.o["lines"] if l["cat"] != "mant")
        self.assertEqual(self.p["n_packages"], n)
        self.assertEqual(n, 28)


class BridgeTests(unittest.TestCase):
    """The comparison must be like-for-like: the team's total INCLUDES the initial maintenance."""

    @classmethod
    def setUpClass(cls):
        cls.o, *_ = build_all.compute(with_sens=False)
        cls.b = cls.o["bridge"]

    def test_bridge_foots_from_team_total_to_b_with_maintenance(self):
        run = self.o["team_usd"]["total"]
        for step in self.b["steps"]:
            run += step["delta"]
            self.assertEqual(run, step["running"], step["name"])
        self.assertEqual(run, self.o["all_in_b"])

    def test_three_steps_with_reasons(self):
        self.assertEqual(len(self.b["steps"]), 3)
        for s in self.b["steps"]:
            self.assertTrue(s["reason"])

    def test_scenario_a_is_the_first_stop(self):
        self.assertEqual(self.b["steps"][0]["running"], self.o["ladder_a"]["total"])

    def test_like_for_like_percent_uses_maintenance_on_both_sides(self):
        expected = self.o["all_in_b"] / self.o["team_usd"]["total"] - 1
        self.assertAlmostEqual(self.b["like_for_like_pct"], expected)
        self.assertGreater(self.b["like_for_like_pct"], self.o["ladder_b"]["total"] / self.o["team_usd"]["total"] - 1)

    def test_rounding_difference_vs_direct_conversion_is_small_and_reported(self):
        direct = D.TEAM_TOTAL * 1e6 / self.o["fx"]["value"]
        self.assertAlmostEqual(self.b["rounding_diff"], self.o["team_usd"]["total"] - direct, places=6)
        self.assertLess(abs(self.b["rounding_diff"]), 10)

    def test_bridge_scales_with_fx(self):
        o2, *_ = build_all.compute(fx=2 * self.o["fx"]["value"], with_sens=False)
        self.assertLessEqual(abs(self.o["bridge"]["steps"][-1]["running"] - 2 * o2["bridge"]["steps"][-1]["running"]), 40)


class BaselineCurveTests(unittest.TestCase):
    def test_curve_with_contingency_ends_at_the_baseline(self):
        o, *_ = build_all.compute(with_sens=False)
        last = list(o["cum_baseline"].values())[-1]
        self.assertEqual(last, o["ladder_b"]["baseline"])
        self.assertEqual(sum(o["cash_baseline"].values()), o["ladder_b"]["baseline"])

    def test_monthly_contingency_is_proportional_to_monthly_cost(self):
        cash = {"a": 10, "b": 30, "c": 60}
        out = costing.baseline_curve(cash, 10)
        self.assertEqual(sum(out["monthly"].values()), 110)
        self.assertEqual(out["monthly"], {"a": 11, "b": 33, "c": 66})
        self.assertEqual(list(out["cumulative"].values())[-1], 110)

    def test_zero_contingency_leaves_the_curve_unchanged(self):
        cash = {"a": 10, "b": 30}
        self.assertEqual(costing.baseline_curve(cash, 0)["monthly"], cash)


class RubricMappingTests(unittest.TestCase):
    """Clase 4 p17 lists what to estimate; every budget line must fall in exactly one rubric."""

    def test_every_line_is_mapped_once(self):
        o, *_ = build_all.compute(with_sens=False)
        ids = [l["id"] for l in o["lines"]]
        mapped = [i for g in o["p17"] for i in g["ids"]]
        self.assertEqual(sorted(ids), sorted(mapped))
        self.assertEqual(len(mapped), len(set(mapped)))

    def test_rubric_totals_foot_to_project_costs_plus_maintenance(self):
        o, *_ = build_all.compute(with_sens=False)
        self.assertEqual(sum(g["usd_b"] for g in o["p17"]), o["ladder_b"]["project_costs"] + o["maint_usd"])

    def test_p17_rubrics_are_the_slide_list(self):
        o, *_ = build_all.compute(with_sens=False)
        names = [g["rubric"] for g in o["p17"]]
        for needed in ("Mano de obra", "Materiales", "Subcontratistas y asesores", "Alquiler de equipo e instalaciones", "Viajes"):
            self.assertIn(needed, names)
        travel = next(g for g in o["p17"] if g["rubric"] == "Viajes")
        self.assertEqual(travel["ids"], [])
        self.assertEqual(travel["usd_b"], 0)


class IndirectCostsTests(unittest.TestCase):
    def test_indirect_costs_are_declared_explicitly(self):
        o, *_ = build_all.compute(with_sens=False)
        ind = o["indirect"]
        self.assertEqual(ind["usd"], 0)
        self.assertTrue(ind["declared"])
        self.assertTrue(ind["decision"])

    def test_all_lines_are_direct(self):
        o, *_ = build_all.compute(with_sens=False)
        self.assertTrue(all(l["asignacion"] == "Directo" for l in o["lines"]))


class AuditDocumentsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.o, *_ = build_all.compute()
        cls.md = (ROOT / "03-presupuesto" / "presupuesto.md").read_text(encoding="utf-8")
        cls.aud = (ROOT / "03-presupuesto" / "auditoria.md").read_text(encoding="utf-8")
        cls.mem = (ROOT / "03-presupuesto" / "memoria-de-calculo.md").read_text(encoding="utf-8")

    def test_budget_doc_shows_the_p24_pyramid_and_like_for_like_bridge(self):
        self.assertIn("Suma ascendente", self.md)
        self.assertIn(usd(self.o["pyramid"]["baseline"]), self.md)
        self.assertIn(pct(self.o["bridge"]["like_for_like_pct"]), self.md)

    def test_budget_doc_no_longer_compares_apples_to_oranges(self):
        wrong = pct(self.o["ladder_b"]["total"] / self.o["team_usd"]["total"] - 1) + " sobre el total del equipo"
        self.assertNotIn(wrong, self.md)

    def test_audit_cites_the_slides_it_verified(self):
        for needle in ("p24", "p20", "p21", "p17", "p18"):
            self.assertIn(needle, self.aud)

    def test_audit_states_verified_vs_assumed_vs_market_unverified(self):
        low = self.aud.lower()
        for needle in ("verificado", "supuesto", "sin contrastar con el mercado"):
            self.assertIn(needle, low)

    def test_audit_reports_rounding_difference(self):
        self.assertIn(str(abs(int(round(self.o["bridge"]["rounding_diff"])))), self.aud)

    def test_memoria_has_numbered_steps_and_one_example_per_cost_type(self):
        for n in range(1, 9):
            self.assertIn(f"\n{n}. ", self.mem, f"step {n}")
        for cost_type in ("Mano de obra", "Herramienta mensual", "Importe global", "Servicio mensual", "Mantenimiento", "Contingencia", "Reserva de gestión", "Curva S"):
            self.assertIn(cost_type, self.mem)

    def test_memoria_numbers_come_from_the_model(self):
        self.assertIn(usd(self.o["ladder_b"]["total"]), self.mem)
        self.assertIn(usd(self.o["ladder_b"]["contingency"]), self.mem)


if __name__ == "__main__":
    unittest.main()
