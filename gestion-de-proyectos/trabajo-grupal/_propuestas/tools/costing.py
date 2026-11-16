"""USD cost model: one exchange rate, line items traceable to the Gantt (Clase 4 method).

The team's figures are in ARS (millions). Every USD amount is `ARS x 1e6 / fx`, rounded to whole
dollars AT LINE LEVEL, so every table foots exactly (totals are sums of the rounded lines).
"""
import math

import budget as bud
import data as D

MONTH_ES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
POST_CLOSING = "post-cierre (sin fecha)"


def usd_of(ars_m, fx):
    """Millions of ARS -> USD (float)."""
    return ars_m * 1e6 / fx


def round_half_up(x):
    return int(math.floor(x + 0.5))


def round_to_total(values, total):
    """Round a dict of floats to integers (largest remainder) so that the integers add up to `total`."""
    s = sum(values.values())
    if abs(s - total) > 1:
        raise ValueError(f"values add up to {s}, which is not close to {total}")
    floors = {k: math.floor(v) for k, v in values.items()}
    rem = total - sum(floors.values())
    if rem < 0 or rem > len(values):
        raise ValueError("cannot reach the total by rounding")
    out = dict(floors)
    for k in sorted(values, key=lambda k: values[k] - floors[k], reverse=True)[:rem]:
        out[k] += 1
    return out


def ladder_int(project_costs, contingency, mgmt_reserve_pct):
    """Clase 4: costs + contingency = baseline; baseline + management reserve = budget (whole USD)."""
    if min(project_costs, contingency, mgmt_reserve_pct) < 0:
        raise ValueError("inputs must be non-negative")
    baseline = project_costs + contingency
    reserve = round_half_up(baseline * mgmt_reserve_pct)
    return {"project_costs": project_costs, "contingency": contingency, "baseline": baseline,
            "mgmt_reserve": reserve, "total": baseline + reserve}


def wp_text(res_ids):
    """'Fases 2–3 · act. 5–17' from a list of Gantt activity ids."""
    phase_of = {a["id"]: a["phase"] for a in D.ACTIVITIES}
    phases = sorted({phase_of[i] for i in res_ids})
    ph = f"Fase {phases[0]}" if len(phases) == 1 else f"Fases {phases[0]}–{phases[-1]}"
    lo, hi = min(res_ids), max(res_ids)
    return f"{ph} · act. {lo}" if lo == hi else f"{ph} · act. {lo}–{hi}"


def months_label(cal, res, ids):
    lo = min(res[i]["es"] for i in ids)
    hi = max(res[i]["ef"] for i in ids)
    d0, d1 = cal.start_date(lo), cal.finish_date(hi)
    first, last = (d0.year, d0.month), (d1.year, d1.month)
    if first == last:
        return f"{MONTH_ES[d0.month - 1]} {d0.year}"
    return f"{MONTH_ES[d0.month - 1]}–{MONTH_ES[d1.month - 1]} {d1.year}"


def window_months_keys(cal, res, ids):
    lo = min(res[i]["es"] for i in ids)
    hi = max(res[i]["ef"] for i in ids)
    return sorted({cal.date_of(idx).strftime("%Y-%m") for idx in range(lo, hi)})


def build_lines(res, cal, fx):
    """The 32 budget lines: 9 labour roles + the team's 23 other line items."""
    cats = dict(D.CATEGORIES)
    lines = []
    for n_, (key, label, tm, tc, ids) in enumerate(D.TEAM_ROLES, 1):
        rate_ars = tc / tm
        unit = usd_of(rate_ars, fx)
        wd = bud.role_workdays(res, ids)
        months = bud.months(wd)
        qty = D.B_QTY[key]
        lines.append({
            "id": f"RH{n_}", "cat": "rh", "categoria": cats["rh"], "role": key, "concepto": label,
            "wp": wp_text(ids), "comportamiento": "Variable", "asignacion": "Directo", "metodo": "Paramétrica (tarifa mensual × personas × meses del Gantt)",
            "qty": qty, "unidad": "persona-mes (100 % dedicación)", "unit_usd": unit, "duracion_meses": months, "workdays": wd,
            "usd_team": round_half_up(usd_of(tc, fx)), "usd_b": round_half_up(qty * unit * months), "ars_team_m": tc,
            "supuesto": "Tarifa = costo del equipo ÷ meses de su tabla §10.2; personas a tiempo completo durante la ventana del rol.",
            "fuente": "tarifa: equipo (§10.2) · personas: propuesta (escenario B)", "meses": months_label(cal, res, ids), "window": ids,
        })
    for lid, cat, concept, ars_m, kind, window, comp, asig, metodo, supuesto in D.BUDGET_LINES:
        amount = round_half_up(usd_of(ars_m, fx))
        if window:
            wd_line = bud.role_workdays(res, window)
            months = bud.months(wd_line)
            wp, meses = wp_text(window), months_label(cal, res, window)
        else:
            wd_line, months, wp, meses = None, None, "Posterior al cierre (fuera del Gantt)", POST_CLOSING
        if kind == "mensual":
            qty, unidad, unit = months, "mes de servicio", amount / months
        else:
            qty, unidad, unit = 1, "global", float(amount)
        lines.append({
            "id": lid, "cat": cat, "categoria": cats[cat], "role": None, "concepto": concept, "wp": wp, "comportamiento": comp,
            "asignacion": asig, "metodo": metodo, "qty": qty, "unidad": unidad, "unit_usd": unit, "duracion_meses": months,
            "workdays": wd_line, "usd_team": amount, "usd_b": amount, "ars_team_m": ars_m, "supuesto": supuesto,
            "fuente": "equipo (importe global, sin cotización) · a confirmar con cotización", "meses": meses, "window": window,
        })
    return lines


def categories(lines):
    out = {}
    for key, label in D.CATEGORIES:
        out[key] = {"label": label,
                    "team": sum(l["usd_team"] for l in lines if l["cat"] == key),
                    "b": sum(l["usd_b"] for l in lines if l["cat"] == key)}
    return out


# ------------------------------------------------------------------ audit helpers (Clase 4 p24 pyramid, bridge, baseline curve)
def pyramid(lines, ladder, cats):
    """Clase 4 p24, 'suma ascendente': work packages -> accounting centres -> project; + contingency = baseline; + reserve = budget.

    The initial maintenance happens after the closing, so it is not a centre of the baseline.
    """
    centers = [{"label": cats[k]["label"], "usd": cats[k]["b"]} for k, _ in D.CATEGORIES if k != "mant"]
    return {"total": ladder["total"], "mgmt_reserve": ladder["mgmt_reserve"], "baseline": ladder["baseline"],
            "contingency": ladder["contingency"], "project": ladder["project_costs"], "centers": centers,
            "n_packages": sum(1 for l in lines if l["cat"] != "mant")}


def bridge(team_total, team_contingency, ladder_a, ladder_b, labour_a, labour_b, maint, team_total_ars_m, fx):
    """Like-for-like bridge: the team's total includes the initial maintenance, so scenario B is compared WITH it.

    team (flat 10 %) -> A (contingency = sum of EMV) -> + labour from the Gantt -> + management reserve = B with maintenance.
    """
    s1 = ladder_a["contingency"] - team_contingency
    s2 = labour_b - labour_a
    s3 = ladder_b["mgmt_reserve"]
    steps, run = [], team_total
    for name, delta, reason in (
        ("Contingencia: 10 % plano → suma de los EMV", s1, "Contingencia calculada desde los riesgos identificados (Clase 4 p19–20), no un porcentaje plano."),
        ("Mano de obra: meses del equipo → personas × duración del Gantt", s2, "La duración sale de las fechas del Gantt del equipo y se explicitan las personas por rol (Clase 4 p16)."),
        ("Reserva de gestión (10 % de la línea base)", s3, "Reserva explícita para imprevistos no identificados (Clase 4 p19, p21, p24); no existía."),
    ):
        run += delta
        steps.append({"name": name, "delta": delta, "running": run, "reason": reason})
    all_in_b = ladder_b["total"] + maint
    assert run == all_in_b, f"bridge does not close: {run} != {all_in_b}"
    return {"steps": steps, "like_for_like_pct": all_in_b / team_total - 1, "until_closing_pct": ladder_b["total"] / team_total - 1,
            "rounding_diff": team_total - usd_of(team_total_ars_m, fx)}


def baseline_curve(cash, contingency):
    """Spread the contingency over the months in proportion to the monthly cost (baseline = costs + contingency, Clase 4 p24)."""
    total = sum(cash.values())
    if contingency == 0 or total == 0:
        monthly = dict(cash)
    else:
        share = round_to_total({k: contingency * v / total for k, v in cash.items()}, contingency)
        monthly = {k: cash[k] + share[k] for k in cash}
    run, cum = 0, {}
    for k, v in monthly.items():
        run += v
        cum[k] = run
    return {"monthly": monthly, "cumulative": cum}


def p17_groups(lines):
    """Clase 4 p17 'qué debemos estimar': each budget line falls in exactly one rubric (proposed classification)."""
    by_id = {l["id"]: l for l in lines}
    out, seen = [], set()
    for rubric, ids in D.P17_RUBRICS:
        for i in ids:
            if i not in by_id or i in seen:
                raise ValueError(f"bad rubric mapping for {i}")
            seen.add(i)
        out.append({"rubric": rubric, "ids": list(ids), "usd_b": sum(by_id[i]["usd_b"] for i in ids), "usd_team": sum(by_id[i]["usd_team"] for i in ids)})
    missing = set(by_id) - seen
    if missing:
        raise ValueError(f"lines without rubric: {sorted(missing)}")
    return out
