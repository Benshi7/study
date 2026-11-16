"""Working-day calendar for the simulated project window (Argentina, 2026).

Holidays are NATIONAL ones. Sources and caveats are documented in 02-gantt/gantt.md:
- 2026 'dias no laborables con fines turisticos' (Res. 164/25): 23/03, 10/07, 07/12.
- Movable holidays: 15/06 (Guemes, moved from Wed 17/06) is an ASSUMPTION to confirm.
Weekend days are never working days. A 'month' is 21 working days by convention (see budget.py).
"""
import datetime as dt

HOLIDAYS_2026 = frozenset(
    {
        dt.date(2026, 1, 1),
        dt.date(2026, 2, 16),
        dt.date(2026, 2, 17),
        dt.date(2026, 3, 23),   # non-working day (tourism)
        dt.date(2026, 3, 24),
        dt.date(2026, 4, 2),
        dt.date(2026, 4, 3),
        dt.date(2026, 5, 1),
        dt.date(2026, 5, 25),
        dt.date(2026, 6, 15),   # Guemes moved from Wed 17/06 (to confirm)
        dt.date(2026, 7, 9),
        dt.date(2026, 7, 10),   # non-working day (tourism): treated as non-working (conservative)
        dt.date(2026, 8, 17),
        dt.date(2026, 10, 12),
        dt.date(2026, 11, 20),
        dt.date(2026, 12, 7),
        dt.date(2026, 12, 8),
        dt.date(2026, 12, 25),
    }
)


class Calendar:
    """Maps working-day indexes (0-based, day 0 = first working day on/after start) to dates."""

    def __init__(self, start, holidays=HOLIDAYS_2026, horizon=800):
        self.holidays = frozenset(holidays)
        self._dates = []
        d = start
        while len(self._dates) < horizon:
            if self.is_workday(d):
                self._dates.append(d)
            d += dt.timedelta(days=1)
        self._index = {d: i for i, d in enumerate(self._dates)}

    def is_workday(self, d):
        return d.weekday() < 5 and d not in self.holidays

    def next_workday(self, d):
        d += dt.timedelta(days=1)
        while not self.is_workday(d):
            d += dt.timedelta(days=1)
        return d

    def date_of(self, index):
        return self._dates[index]

    def index_of(self, d):
        if d not in self._index:
            raise ValueError(f"{d} is not a working day in this calendar")
        return self._index[d]

    def start_date(self, es):
        """Date on which an activity with early start `es` begins."""
        return self._dates[es]

    def finish_date(self, ef):
        """Date on which an activity with early finish `ef` (exclusive index) ends."""
        return self._dates[ef - 1]

    def workdays_between(self, d1, d2):
        return self.index_of(d2) - self.index_of(d1) + 1
