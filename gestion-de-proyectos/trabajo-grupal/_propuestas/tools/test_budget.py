"""Tests for the cost model (written first)."""
import unittest

import budget


class LabourTests(unittest.TestCase):
    def test_person_months(self):
        # 21 working days = 1 month by convention
        self.assertAlmostEqual(budget.months(21), 1.0)
        self.assertAlmostEqual(budget.months(42), 2.0)

    def test_labour_cost(self):
        # 2 people x 6 M/month x 21 wd (1 month) x 100 %
        self.assertAlmostEqual(budget.labour_cost(qty=2, rate_month=6.0, workdays=21, dedication=1.0), 12.0)

    def test_dedication_scales_cost(self):
        self.assertAlmostEqual(budget.labour_cost(qty=1, rate_month=10.0, workdays=21, dedication=0.5), 5.0)

    def test_invalid_dedication(self):
        with self.assertRaises(ValueError):
            budget.labour_cost(qty=1, rate_month=1.0, workdays=21, dedication=1.5)

    def test_union_of_intervals(self):
        # intervals [0,3) and [2,6) overlap; [10,12) disjoint -> 6 + 2 = 8 days
        self.assertEqual(budget.union_days([(0, 3), (2, 6), (10, 12)]), 8)

    def test_role_workdays_from_schedule(self):
        sched = {"X": {"es": 0, "ef": 3}, "Y": {"es": 2, "ef": 6}, "Z": {"es": 10, "ef": 12}}
        self.assertEqual(budget.role_workdays(sched, ["X", "Y", "Z"]), 8)

    def test_role_workdays_unknown_activity(self):
        with self.assertRaises(KeyError):
            budget.role_workdays({"X": {"es": 0, "ef": 1}}, ["nope"])


class LadderTests(unittest.TestCase):
    def test_ladder_follows_class_4(self):
        r = budget.ladder(project_costs=3000.0, contingency=210.0, mgmt_reserve_pct=0.10)
        self.assertAlmostEqual(r["baseline"], 3210.0)
        self.assertAlmostEqual(r["mgmt_reserve"], 321.0)
        self.assertAlmostEqual(r["total"], 3531.0)

    def test_negative_inputs_rejected(self):
        with self.assertRaises(ValueError):
            budget.ladder(project_costs=-1, contingency=0, mgmt_reserve_pct=0.1)


class FootingTests(unittest.TestCase):
    def test_feet_ok(self):
        budget.check_foots({"a": 1.0, "b": 2.5}, 3.5)

    def test_feet_mismatch(self):
        with self.assertRaises(AssertionError):
            budget.check_foots({"a": 1.0, "b": 2.5}, 4.0)


class CashCurveTests(unittest.TestCase):
    def test_spread_evenly_over_workday_window(self):
        # 100 spread over indexes 0..3 (4 days) -> 25 per day
        d = budget.spread(100.0, 0, 4)
        self.assertEqual(len(d), 4)
        self.assertAlmostEqual(sum(d.values()), 100.0)
        self.assertAlmostEqual(d[2], 25.0)

    def test_cumulative_is_monotonic_and_ends_at_total(self):
        monthly = {"2026-04": 10.0, "2026-05": 20.0, "2026-06": 0.0, "2026-07": 5.0}
        cum = budget.cumulative(monthly)
        self.assertEqual(list(cum.values()), [10.0, 30.0, 30.0, 35.0])


if __name__ == "__main__":
    unittest.main()
