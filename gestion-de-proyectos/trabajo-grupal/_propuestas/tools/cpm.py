"""PERT estimates and critical-path method (finish-to-start, optional lead/lag), integer working days."""


def pert(o, m, p):
    """Expected duration (O + 4M + P) / 6, as taught in Clase 3."""
    if not (o <= m <= p):
        raise ValueError(f"expected O <= M <= P, got {(o, m, p)}")
    return (o + 4 * m + p) / 6


def pert_sigma(o, m, p):
    """Standard deviation (P - O) / 6. Complement: not in the cátedra slides."""
    if not (o <= m <= p):
        raise ValueError(f"expected O <= M <= P, got {(o, m, p)}")
    return (p - o) / 6


def links(a):
    """[(predecessor id, lag)] for an activity; a predecessor is `id` or `(id, lag)` (lag < 0 = lead)."""
    return [p if isinstance(p, tuple) else (p, 0) for p in a["preds"]]


def _topological(acts):
    ids = [a["id"] for a in acts]
    if len(set(ids)) != len(ids):
        raise ValueError("duplicate activity ids")
    by_id = {a["id"]: a for a in acts}
    for a in acts:
        for p, _ in links(a):
            if p not in by_id:
                raise ValueError(f"unknown predecessor {p!r} for {a['id']!r}")
    order, seen, temp = [], set(), set()

    def visit(i):
        if i in seen:
            return
        if i in temp:
            raise ValueError(f"cycle detected at {i!r}")
        temp.add(i)
        for p, _ in links(by_id[i]):
            visit(p)
        temp.discard(i)
        seen.add(i)
        order.append(i)

    for i in ids:
        visit(i)
    return order, by_id


def schedule(acts):
    """Forward and backward pass. Returns {id: {es, ef, ls, lf, slack, critical}}."""
    order, by_id = _topological(acts)
    res = {}
    for i in order:
        a = by_id[i]
        es = max((res[p]["ef"] + lag for p, lag in links(a)), default=0)
        res[i] = {"es": es, "ef": es + a["dur"]}
    end = max(r["ef"] for r in res.values()) if res else 0
    succ = {i: [] for i in by_id}
    for a in acts:
        for p, lag in links(a):
            succ[p].append((a["id"], lag))
    for i in reversed(order):
        a = by_id[i]
        lf = min((res[s]["ls"] - lag for s, lag in succ[i]), default=end)
        res[i]["lf"] = lf
        res[i]["ls"] = lf - a["dur"]
        res[i]["slack"] = res[i]["ls"] - res[i]["es"]
        res[i]["critical"] = res[i]["slack"] == 0
    # keep input order for readable reports
    return {a["id"]: res[a["id"]] for a in acts}


def project_duration(res):
    return max(r["ef"] for r in res.values())


def critical_path(acts, res):
    """One critical path (ids in order), following zero-slack predecessors back from the last finisher."""
    by_id = {a["id"]: a for a in acts}
    last = max((i for i in res if res[i]["critical"]), key=lambda i: (res[i]["ef"], -len(by_id[i]["preds"])))
    path = [last]
    while True:
        cur = by_id[path[-1]]
        cands = [p for p, lag in links(cur) if res[p]["critical"] and res[p]["ef"] + lag == res[path[-1]]["es"]]
        if not cands:
            break
        path.append(sorted(cands)[0] if len(cands) == 1 else sorted(cands, key=lambda p: -res[p]["ef"] + res[p]["es"])[0])
    return list(reversed(path))
