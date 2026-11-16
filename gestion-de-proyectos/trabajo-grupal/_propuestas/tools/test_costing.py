"""Tests for the USD cost model (written first).

Everything is checked against `build_all.compute`, a pure function (no file writes), so the
tests can run it with several exchange rates.
"""
import unittest

import budget as bud
import build_all
import costing
import data as D

REQUIRED = ("id", "concepto", "categoria", "wp", "comportamiento", "asignacion", "metodo", "qty",
            "unidad", "unit_usd", "usd_b", "supuesto", "fuente", "meses")


class ConversionTests(unittest.TestCase):
    def test_usd_of(self):
        self.assertAlmostEqual(costing.usd_of(1.545, 1545.0), 1000.0)

    def test_round_half_up(self):
        self.assertEqual(costing.round_half_up(2.5), 3)
        self.assertEqual(costing.round_half_up(0.5), 1)
        self.assertEqual(costing.round_half_up(1.49), 1)

    def test_round_to_total_preserves_total(self):
        out = costing.round_to_total({"a": 1.4, "b": 1.4, "c": 1.2}, 4)
        self.assertEqual(sum(out.values()), 4)
        for k, v in {"a": 1.4, "b": 1.4, "c": 1.2}.items():
            self.assertLessEqual(abs(out[k] - v), 1)

    def test_round_to_total_rejects_incoherent_total(self):
        with self.assertRaises(ValueError):
            costing.round_to_total({"a": 1.4, "b": 1.4}, 10)


class FxParametricTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.o1, *_ = build_all.compute(fx=1500.0, with_sens=False)
        cls.o2, *_ = build_all.compute(fx=3000.0, with_sens=False)

    def test_fx_is_recorded(self):
        self.assertEqual(self.o1["fx"]["value"], 1500.0)

    def test_default_fx_comes_from_the_single_constant(self):
        o, *_ = build_all.compute(with_sens=False)
        self.assertEqual(o["fx"]["value"], D.FX_ARS_PER_USD)
        self.assertTrue(o["fx"]["source"])
        self.assertTrue(o["fx"]["date"])

    def test_every_line_scales_with_fx(self):
        self.assertEqual(len(self.o1["lines"]), len(self.o2["lines"]))
        for a, b in zip(self.o1["lines"], self.o2["lines"]):
            self.assertGreater(a["usd_team"], 0)
            self.assertLessEqual(abs(a["usd_team"] - 2 * b["usd_team"]), 2, a["id"])
            self.assertLessEqual(abs(a["usd_b"] - 2 * b["usd_b"]), 2, a["id"])

    def test_every_emv_scales_with_fx(self):
        for a, b in zip(self.o1["risks"]["sorted"], self.o2["risks"]["sorted"]):
            self.assertEqual(a["id"], b["id"])
            self.assertLessEqual(abs(a["emv_usd"] - 2 * b["emv_usd"]), 2, a["id"])

    def test_totals_scale_with_fx(self):
        t1, t2 = self.o1["ladder_b"]["total"], self.o2["ladder_b"]["total"]
        self.assertLess(abs(t1 - 2 * t2), 60)

    def test_lower_fx_means_higher_usd(self):
        o, *_ = build_all.compute(with_sens=True)
        s = o["fx_sens"]
        self.assertGreater(s["0.8"]["total_b"], s["1.0"]["total_b"])
        self.assertGreater(s["1.0"]["total_b"], s["1.2"]["total_b"])
        self.assertEqual(s["1.0"]["total_b"], o["ladder_b"]["total"])


class LineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.o, cls.res, cls.acts, cls.cal = build_all.compute(with_sens=False)
        cls.lines = cls.o["lines"]

    def test_expected_number_of_lines(self):
        # 9 labour roles + 6 tec + 4 dat + 5 inf + 4 imp + 4 mant (the team's own line items)
        self.assertEqual(len(self.lines), 9 + 6 + 4 + 5 + 4 + 4)

    def test_ids_are_unique(self):
        ids = [l["id"] for l in self.lines]
        self.assertEqual(len(ids), len(set(ids)))

    def test_required_fields_are_present_and_not_empty(self):
        for l in self.lines:
            for k in REQUIRED:
                self.assertIn(k, l, f"{l['id']} lacks {k}")
                self.assertNotEqual(str(l[k]).strip(), "", f"{l['id']}.{k} is empty")

    def test_closed_vocabularies(self):
        for l in self.lines:
            self.assertIn(l["comportamiento"], ("Fijo", "Variable"))
            self.assertIn(l["asignacion"], ("Directo", "Indirecto"))
            self.assertTrue(l["metodo"].startswith(("Paramétrica", "Experta", "Análoga")), l["metodo"])
            self.assertTrue(any(w in l["fuente"] for w in ("equipo", "propuesta", "a confirmar")), l["fuente"])

    def test_labour_is_people_x_rate_x_gantt_months(self):
        labour = [l for l in self.lines if l.get("role")]
        self.assertEqual(len(labour), 9)
        for l in labour:
            ids = next(r[4] for r in D.TEAM_ROLES if r[0] == l["role"])
            months = bud.months(bud.role_workdays(self.res, ids))
            self.assertAlmostEqual(l["duracion_meses"], months, places=9)
            self.assertLessEqual(abs(l["qty"] * l["unit_usd"] * months - l["usd_b"]), 1.0, l["id"])

    def test_labour_rate_is_the_teams_implied_rate_converted(self):
        fx = self.o["fx"]["value"]
        for l in (x for x in self.lines if x.get("role")):
            _, _, tm, tc, _ = next(r for r in D.TEAM_ROLES if r[0] == l["role"])
            self.assertAlmostEqual(l["unit_usd"], (tc / tm) * 1e6 / fx, places=6)

    def test_other_lines_qty_x_unit_equals_amount(self):
        for l in (x for x in self.lines if not x.get("role")):
            self.assertLessEqual(abs(l["qty"] * l["unit_usd"] - l["usd_b"]), 1.0, l["id"])
            if l["unidad"] == "global":
                self.assertEqual(l["qty"], 1)

    def test_team_amounts_come_from_the_team_ars_figures(self):
        fx = self.o["fx"]["value"]
        for l in self.lines:
            self.assertLessEqual(abs(l["usd_team"] - l["ars_team_m"] * 1e6 / fx), 0.5 + 1e-9, l["id"])

    def test_lines_foot_to_categories_and_to_project_costs(self):
        cats = self.o["categories"]
        for key, c in cats.items():
            self.assertEqual(sum(l["usd_b"] for l in self.lines if l["cat"] == key), c["b"], key)
            self.assertEqual(sum(l["usd_team"] for l in self.lines if l["cat"] == key), c["team"], key)
        project = sum(c["b"] for k, c in cats.items() if k != "mant")
        self.assertEqual(project, self.o["ladder_b"]["project_costs"])
        self.assertEqual(sum(c["team"] for c in cats.values()), self.o["ladder_a"]["project_costs"])

    def test_maintenance_is_outside_the_baseline(self):
        self.assertEqual(self.o["maint_usd"], self.o["categories"]["mant"]["b"])
        self.assertEqual(self.o["all_in_b"], self.o["ladder_b"]["total"] + self.o["maint_usd"])


class ReservesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.o, *_ = build_all.compute(with_sens=False)

    def test_emv_usd_follows_probability_times_impact(self):
        fx = self.o["fx"]["value"]
        for r in self.o["risks"]["sorted"]:
            exp = costing.round_half_up(D.SCALE["prob"][r["pr"]] * D.SCALE["impact_M"][r["ir"]] * 1e6 / fx)
            self.assertEqual(r["emv_usd"], exp, r["id"])

    def test_contingency_is_the_sum_of_residual_emv(self):
        total = sum(r["emv_usd"] for r in self.o["risks"]["sorted"])
        self.assertEqual(self.o["ladder_b"]["contingency"], total)
        self.assertEqual(self.o["ladder_a"]["contingency"], total)
        self.assertEqual(self.o["risks"]["emv_residual_usd"], total)

    def test_ladder_b_follows_clase_4(self):
        lb = self.o["ladder_b"]
        self.assertEqual(lb["baseline"], lb["project_costs"] + lb["contingency"])
        self.assertEqual(lb["mgmt_reserve"], costing.round_half_up(0.10 * lb["baseline"]))
        self.assertEqual(lb["total"], lb["baseline"] + lb["mgmt_reserve"])

    def test_scenario_a_has_no_management_reserve(self):
        la = self.o["ladder_a"]
        self.assertEqual(la["mgmt_reserve"], 0)
        self.assertEqual(la["total"], la["project_costs"] + la["contingency"])

    def test_the_new_exchange_rate_risk_exists_and_is_not_worse_after_response(self):
        r = next(x for x in self.o["risks"]["sorted"] if x["id"] == "R19")
        self.assertTrue(r["new"])
        self.assertLessEqual(r["pr"], r["p"])
        self.assertLessEqual(r["ir"], r["i"])

    def test_privacy_risk_covers_the_basic_household_profile(self):
        r = next(x for x in D.RISKS if x["id"] == "R10")
        self.assertIn("hogar", (r["evento"] + r["problema"]).lower())
        self.assertIn("25.326", r["problema"])


class CashCurveTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.o, *_ = build_all.compute(with_sens=False)

    def test_s_curve_ends_at_the_project_costs(self):
        cum = list(self.o["cum"].values())
        self.assertEqual(cum[-1], self.o["ladder_b"]["project_costs"])
        self.assertEqual(sum(self.o["cash"].values()), self.o["ladder_b"]["project_costs"])

    def test_s_curve_is_monotonic_and_has_six_months(self):
        cum = list(self.o["cum"].values())
        self.assertEqual(len(cum), 6)
        self.assertEqual(cum, sorted(cum))

    def test_cash_values_are_whole_dollars(self):
        for v in self.o["cash"].values():
            self.assertEqual(v, int(v))


if __name__ == "__main__":
    unittest.main()
