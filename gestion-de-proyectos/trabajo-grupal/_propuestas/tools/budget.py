"""Cost model: labour = people x monthly rate x months (from the Gantt) x dedication; Clase 4 ladder."""

WORKDAYS_PER_MONTH = 21  # convention used throughout the proposals


def months(workdays):
    return workdays / WORKDAYS_PER_MONTH


def labour_cost(qty, rate_month, workdays, dedication=1.0):
    if not (0 < dedication <= 1):
        raise ValueError("dedication must be in (0, 1]")
    return qty * rate_month * months(workdays) * dedication


def union_days(intervals):
    """Total length of the union of half-open [start, end) intervals."""
    total, cur_s, cur_e = 0, None, None
    for s, e in sorted(intervals):
        if cur_e is None or s > cur_e:
            if cur_e is not None:
                total += cur_e - cur_s
            cur_s, cur_e = s, e
        else:
            cur_e = max(cur_e, e)
    if cur_e is not None:
        total += cur_e - cur_s
    return total


def role_workdays(sched, activity_ids):
    return union_days([(sched[a]["es"], sched[a]["ef"]) for a in activity_ids])


def ladder(project_costs, contingency, mgmt_reserve_pct):
    """Clase 4 p24: costs + contingency = baseline; baseline + management reserve = budget."""
    if min(project_costs, contingency, mgmt_reserve_pct) < 0:
        raise ValueError("inputs must be non-negative")
    baseline = project_costs + contingency
    reserve = baseline * mgmt_reserve_pct
    return {"project_costs": project_costs, "contingency": contingency, "baseline": baseline,
            "mgmt_reserve": reserve, "total": baseline + reserve}


def check_foots(parts, total, tol=1e-6):
    s = sum(parts.values())
    assert abs(s - total) <= tol, f"parts sum to {s}, expected {total}"


def spread(amount, start_index, end_index):
    """Spread `amount` evenly over working-day indexes [start_index, end_index)."""
    n = end_index - start_index
    if n <= 0:
        raise ValueError("empty window")
    return {i: amount / n for i in range(start_index, end_index)}


def cumulative(monthly):
    out, run = {}, 0.0
    for k, v in monthly.items():
        run += v
        out[k] = run
    return out
