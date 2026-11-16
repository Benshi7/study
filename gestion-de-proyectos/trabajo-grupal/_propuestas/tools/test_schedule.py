"""Tests for the CPM / PERT / working-day calendar helpers (written first)."""
import datetime as dt
import unittest

import cpm
import calendar_ar as car


class PertTests(unittest.TestCase):
    def test_symmetric(self):
        self.assertEqual(cpm.pert(2, 5, 8), 5)

    def test_skewed(self):
        # (1 + 4*2 + 9) / 6 = 3
        self.assertAlmostEqual(cpm.pert(1, 2, 9), 3.0)

    def test_right_skew_with_integer_expected(self):
        # chosen so that expected duration is an integer although M < te
        self.assertEqual(cpm.pert(4, 6, 14), 7)

    def test_rejects_unordered_triple(self):
        with self.assertRaises(ValueError):
            cpm.pert(5, 3, 8)

    def test_sigma(self):
        self.assertAlmostEqual(cpm.pert_sigma(2, 5, 8), 1.0)


class CpmTests(unittest.TestCase):
    # Hand-checked toy network:
    #   A(3) -> B(2) -> D(3)
    #   A(3) -> C(4) -> D(3)
    # Critical path A-C-D = 10; B has 2 days of slack.
    NET = [
        {"id": "A", "dur": 3, "preds": []},
        {"id": "B", "dur": 2, "preds": ["A"]},
        {"id": "C", "dur": 4, "preds": ["A"]},
        {"id": "D", "dur": 3, "preds": ["B", "C"]},
    ]

    def test_forward_backward(self):
        r = cpm.schedule(self.NET)
        self.assertEqual(r["A"]["es"], 0)
        self.assertEqual(r["A"]["ef"], 3)
        self.assertEqual(r["D"]["es"], 7)
        self.assertEqual(r["D"]["ef"], 10)
        self.assertEqual(r["B"]["ls"], 5)
        self.assertEqual(r["B"]["slack"], 2)
        self.assertEqual(r["C"]["slack"], 0)

    def test_critical_flags_and_duration(self):
        r = cpm.schedule(self.NET)
        self.assertEqual([k for k, v in r.items() if v["critical"]], ["A", "C", "D"])
        self.assertEqual(cpm.project_duration(r), 10)

    def test_critical_path_order(self):
        r = cpm.schedule(self.NET)
        self.assertEqual(cpm.critical_path(self.NET, r), ["A", "C", "D"])

    def test_zero_duration_milestone(self):
        net = self.NET + [{"id": "M", "dur": 0, "preds": ["D"]}]
        r = cpm.schedule(net)
        self.assertEqual(r["M"]["es"], 10)
        self.assertEqual(r["M"]["ef"], 10)
        self.assertTrue(r["M"]["critical"])

    def test_unknown_predecessor(self):
        with self.assertRaises(ValueError):
            cpm.schedule([{"id": "A", "dur": 1, "preds": ["Z"]}])

    def test_cycle_detected(self):
        net = [
            {"id": "A", "dur": 1, "preds": ["B"]},
            {"id": "B", "dur": 1, "preds": ["A"]},
        ]
        with self.assertRaises(ValueError):
            cpm.schedule(net)

    def test_duplicate_ids(self):
        with self.assertRaises(ValueError):
            cpm.schedule([{"id": "A", "dur": 1, "preds": []}, {"id": "A", "dur": 1, "preds": []}])


class CpmLagTests(unittest.TestCase):
    """Finish-to-start with a lead (negative lag) or a lag, hand-checked."""

    def test_lead_lets_the_successor_start_before_the_predecessor_finishes(self):
        net = [{"id": "A", "dur": 3, "preds": []}, {"id": "B", "dur": 2, "preds": [("A", -1)]}]
        r = cpm.schedule(net)
        self.assertEqual((r["B"]["es"], r["B"]["ef"]), (2, 4))
        self.assertEqual(cpm.project_duration(r), 4)

    def test_positive_lag_waits(self):
        net = [{"id": "A", "dur": 3, "preds": []}, {"id": "B", "dur": 2, "preds": [("A", 2)]}]
        r = cpm.schedule(net)
        self.assertEqual((r["B"]["es"], r["B"]["ef"]), (5, 7))

    def test_backward_pass_uses_the_lag(self):
        # A(3) -> B(2) with lead 1; A -> C(4) plain; C is the longer chain => B has slack
        net = [{"id": "A", "dur": 3, "preds": []}, {"id": "B", "dur": 2, "preds": [("A", -1)]},
               {"id": "C", "dur": 4, "preds": ["A"]}]
        r = cpm.schedule(net)
        self.assertEqual(cpm.project_duration(r), 7)
        self.assertEqual(r["B"]["slack"], 3)
        self.assertTrue(r["A"]["critical"] and r["C"]["critical"] and not r["B"]["critical"])

    def test_critical_path_follows_the_lag(self):
        net = [{"id": "A", "dur": 3, "preds": []}, {"id": "B", "dur": 2, "preds": [("A", -1)]}]
        r = cpm.schedule(net)
        self.assertEqual(cpm.critical_path(net, r), ["A", "B"])

    def test_plain_ids_and_pairs_can_be_mixed(self):
        net = [{"id": "A", "dur": 1, "preds": []}, {"id": "B", "dur": 1, "preds": []},
               {"id": "C", "dur": 1, "preds": ["A", ("B", 1)]}]
        r = cpm.schedule(net)
        self.assertEqual(r["C"]["es"], 2)

    def test_cycle_with_lags_is_still_detected(self):
        net = [{"id": "A", "dur": 1, "preds": [("B", -5)]}, {"id": "B", "dur": 1, "preds": ["A"]}]
        with self.assertRaises(ValueError):
            cpm.schedule(net)


class CalendarTests(unittest.TestCase):
    def setUp(self):
        self.cal = car.Calendar(start=dt.date(2026, 4, 1), holidays=car.HOLIDAYS_2026)

    def test_weekend_skipped(self):
        # Fri 10/04/2026 +1 working day -> Mon 13/04/2026
        self.assertEqual(self.cal.next_workday(dt.date(2026, 4, 10)), dt.date(2026, 4, 13))

    def test_holiday_skipped(self):
        # Thu 30/04 -> next working day skips Fri 01/05 (holiday) and the weekend
        self.assertEqual(self.cal.next_workday(dt.date(2026, 4, 30)), dt.date(2026, 5, 4))

    def test_is_workday(self):
        self.assertFalse(self.cal.is_workday(dt.date(2026, 5, 1)))
        self.assertFalse(self.cal.is_workday(dt.date(2026, 4, 18)))  # Saturday
        self.assertTrue(self.cal.is_workday(dt.date(2026, 4, 13)))

    def test_index_to_date_and_back(self):
        # day 0 is 01/04; 02/04 and 03/04 are holidays -> index 1 is 06/04
        self.assertEqual(self.cal.date_of(0), dt.date(2026, 4, 1))
        self.assertEqual(self.cal.date_of(1), dt.date(2026, 4, 6))
        self.assertEqual(self.cal.index_of(dt.date(2026, 4, 6)), 1)

    def test_end_date_of_activity(self):
        # an activity with es=1, ef=3 occupies indexes 1 and 2 -> ends on index 2 = 07/04
        self.assertEqual(self.cal.finish_date(3), dt.date(2026, 4, 7))
        self.assertEqual(self.cal.start_date(1), dt.date(2026, 4, 6))

    def test_workdays_between_inclusive(self):
        self.assertEqual(self.cal.workdays_between(dt.date(2026, 4, 13), dt.date(2026, 4, 30)), 14)

    def test_index_of_non_workday_raises(self):
        with self.assertRaises(ValueError):
            self.cal.index_of(dt.date(2026, 5, 1))


if __name__ == "__main__":
    unittest.main()
