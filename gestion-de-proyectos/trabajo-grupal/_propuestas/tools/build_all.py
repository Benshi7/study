"""Computes schedule, risks and the USD budget from data.py.

`compute()` is pure (no file writes) so tests can run it with other exchange rates;
`build()` calls it and writes the CSVs and numbers.json used by render.py.
"""
import csv
import datetime as dt
import json
import math
import pathlib

import budget as bud
import calendar_ar as car
import costing as cs
import cpm
import data as D
import risks as rk
import team_gantt as tg

ROOT = pathlib.Path(__file__).resolve().parent.parent
FMT = "%d/%m/%Y"
MGMT_RESERVE_PCT = 0.10          # Clase 4 p21 example; proposal to agree
IMPACT_FACTORS = (0.5, 1.0, 1.5)  # sensitivity of the (assumed) impact scale
FX_FACTORS = (0.8, 1.0, 1.2)      # sensitivity of the exchange rate


def d(date):
    return date.strftime(FMT)


def compute(fx=None, with_sens=True):
    fx = float(D.FX_ARS_PER_USD if fx is None else fx)
    team = D.TEAM
    cal = tg.weekday_calendar(D.SIM_START)         # the team's convention: Monday to Friday, no holidays
    cal_real = car.Calendar(D.SIM_START)             # national holidays 2026 (only used to report the effect)
    # ------------------------------------------------ schedule (the team's real Gantt)
    acts = tg.acts_for_cpm(team, "endpoints")      # the reading that reproduces the team's own CPM sheet
    res_cpm = cpm.schedule(acts)
    total_wd = cpm.project_duration(res_cpm)
    path = cpm.critical_path(acts, res_cpm)
    idx = tg.stated_index(team, cal)               # stated dates -> working-day indexes
    res = {}
    for t_ in team["activities"]:
        i = t_["id"]
        es, ef = idx[i]
        s2 = team["sheet2"][i]
        # es/ef = the team's stated dates; slack and critical flag = the team's CPM sheet; ls/lf are relative to es/ef
        res[i] = {"es": es, "ef": ef, "ls": es + s2["slack"], "lf": ef + s2["slack"], "slack": s2["slack"], "critical": s2["critical"]}
    sc = tg.scenarios(team, cal)
    scd = {r["key"]: r for r in sc}
    dated_acts, dated_res = scd["con_adelantos"]["acts"], scd["con_adelantos"]["res"]
    path_dated = cpm.critical_path(dated_acts, dated_res)
    corr = scd["corregida"]
    path_corr = cpm.critical_path(corr["acts"], corr["res"])
    gate_rows, gate_ok = [], True
    for ph in D.PHASES:
        ef = max(res[a]["ef"] for a in D.PHASE_GATE_ACTS[ph[0]])
        got = cal.finish_date(ef)
        ok = got == ph[4]
        gate_ok &= ok
        gate_rows.append({"gate": f"G{ph[0]}", "name": ph[5], "declared": d(ph[3]), "proposed": d(ph[4]), "computed": d(got), "ok": ok})
    phase_wd = {}
    for ph in D.PHASES:
        ids = [a["id"] for a in D.ACTIVITIES if a["phase"] == ph[0]]
        phase_wd[ph[0]] = max(res[i]["ef"] for i in ids) - min(res[i]["es"] for i in ids)
    r_range = cpm.schedule(tg.acts_for_cpm(team, "range"))
    diff_range = tg.compare_to_team_sheet(r_range, team)
    holiday_hits = [{"id": i, "dates": [x.strftime("%d/%m") for x in hs]} for i, hs in tg.holiday_hits(team, car.HOLIDAYS_2026)]
    hol_window = [h for h in car.HOLIDAYS_2026 if D.SIM_START <= h <= dt.date(2026, 9, 30) and h.weekday() < 5]
    pert_rows = [{**r, "te": cpm.pert(r["o"], r["m"], r["p"]), "sigma": cpm.pert_sigma(r["o"], r["m"], r["p"])} for r in D.PERT_EXAMPLE]
    gantt_info = {
        "scenarios": [{k: (d(v) if isinstance(v, dt.date) else v) for k, v in r.items() if k not in ("res", "acts")} for r in sc],
        "leads": [list(x) for x in tg.overlap_leads(team, "endpoints", cal)],
        "critical_corrected": sorted(i for i, r in corr["res"].items() if r["critical"]),
        "critical_dated": sorted(i for i, r in dated_res.items() if r["critical"]),
        "critical_range": sorted(i for i, r in r_range.items() if r["critical"]),
        "corrected_cells_range": tg.corrected_cells(team, "range"),
        "corrected_cells_endpoints": tg.corrected_cells(team, "endpoints"),
        "corrected_text": {str(k): v for k, v in tg.explicit_deps_text(corr["acts"]).items()},
        "idle_gaps": [list(x) for x in tg.idle_gaps(team, "endpoints", cal)],
        "gap": tg.gap_explanation(team, cal),
        "ambiguous_ids": [a["id"] for a in team["activities"] if tg.is_ambiguous(a["deps_raw"])],
        "range_slack_mismatches": [list(x) for x in diff_range["slack"]],
        "range_critical_mismatches": diff_range["critical"],
        "phase_diffs": [{k: (d(v) if isinstance(v, dt.date) else v) for k, v in x.items()} for x in tg.phase_window_differences(team, D.F2_PHASE_WINDOWS)],
        "holiday_hits": holiday_hits, "holiday_weekdays_in_window": len(hol_window),
        "real_calendar_end": d(cal_real.finish_date(scd["fechas_del_equipo"]["total"])),
        "pert_example": pert_rows, "owners": {str(k): v for k, v in D.ACTIVITY_OWNER.items()},
        "annex_rows": len(team["anexo_rows"]),
    }

    # ------------------------------------------------ risks (ARS M scale -> USD with the single exchange rate)
    rrows = []
    for r in D.RISKS:
        rk.check_residual(r["p"], r["i"], r["pr"], r["ir"])
        s = rk.score(r["p"], r["i"])
        e0 = rk.emv(D.SCALE["prob"][r["p"]], D.SCALE["impact_M"][r["i"]])
        e1 = rk.emv(D.SCALE["prob"][r["pr"]], D.SCALE["impact_M"][r["ir"]])
        rrows.append({**r, "score": s, "level": rk.level(s), "score_res": rk.score(r["pr"], r["ir"]),
                      "level_res": rk.level(rk.score(r["pr"], r["ir"])), "emv0": e0, "emv": e1, "kind": "amenaza",
                      "emv0_usd": cs.round_half_up(cs.usd_of(e0, fx)), "emv_usd": cs.round_half_up(cs.usd_of(e1, fx)),
                      "new": r.get("new", False), "mod": r.get("mod", False)})
    rrows_sorted = rk.sort_by_emv(list(rrows))
    emv_res_usd = sum(r["emv_usd"] for r in rrows)
    emv_init_usd = sum(r["emv0_usd"] for r in rrows)
    team15 = [r for r in rrows if not r["new"]]

    # ------------------------------------------------ budget lines and ladders
    lines = cs.build_lines(res, cal, fx)
    cats = cs.categories(lines)
    costs_b = sum(c["b"] for k, c in cats.items() if k != "mant")
    maint_usd = cats["mant"]["b"]
    costs_a = sum(c["team"] for c in cats.values())            # the team's costs (incl. initial maintenance), converted
    ladder_a = cs.ladder_int(costs_a, emv_res_usd, 0.0)
    ladder_b = cs.ladder_int(costs_b, emv_res_usd, MGMT_RESERVE_PCT)
    team_cont_usd = cs.round_half_up(cs.usd_of(D.TEAM_CONTINGENCY, fx))
    team_usd = {"costs": costs_a, "contingency": team_cont_usd, "total": costs_a + team_cont_usd,
                "ars_total_m": D.TEAM_TOTAL}
    all_in_b = ladder_b["total"] + maint_usd

    lab_rows = []
    for l in (x for x in lines if x["role"]):
        key = l["role"]
        _, label, tm, tc, ids = next(r for r in D.TEAM_ROLES if r[0] == key)
        rate_ars = tc / tm
        qty_a = tc / (rate_ars * l["duracion_meses"])
        lab_rows.append({"key": key, "label": label, "team_months": tm, "team_cost_ars": tc, "rate_ars": rate_ars,
                         "rate_usd": l["unit_usd"], "wd": l["workdays"], "months": l["duracion_meses"], "qty_a": qty_a,
                         "cost_a": l["usd_team"], "qty_b": l["qty"], "cost_b": l["usd_b"]})
    lab_a = sum(r["cost_a"] for r in lab_rows)
    lab_b = sum(r["cost_b"] for r in lab_rows)
    other_total = costs_b - lab_b

    buf, day = 0, dt.date(2026, 9, 30)
    while day < D.ENTREGA:
        day += dt.timedelta(days=1)
        if cal_real.is_workday(day):
            buf += 1

    # ------------------------------------------------ cash curve (scenario B, USD, aligned with the Gantt)
    months_keys = ["2026-04", "2026-05", "2026-06", "2026-07", "2026-08", "2026-09"]
    cash_f = {k: 0.0 for k in months_keys}
    for l in lines:
        if l["cat"] == "mant":
            continue
        lo = min(res[i]["es"] for i in l["window"])
        hi = max(res[i]["ef"] for i in l["window"])
        for idx, v in bud.spread(l["usd_b"], lo, hi).items():
            cash_f[cal.date_of(idx).strftime("%Y-%m")] += v
    cash = cs.round_to_total(cash_f, costs_b)
    cum = bud.cumulative(cash)
    assert cum[months_keys[-1]] == costs_b, "cash curve must end at the project costs"

    base_curve = cs.baseline_curve(cash, ladder_b["contingency"])
    assert list(base_curve["cumulative"].values())[-1] == ladder_b["baseline"], "baseline curve must end at the baseline"
    out = {
        "fx": {"value": fx, "date": d(D.FX_DATE), "source": D.FX_SOURCE},
        "calendar": {"start": d(D.SIM_START), "total_wd": total_wd, "cpm_wd": total_wd, "end": d(cal.finish_date(total_wd)),
                     "range_wd": scd["rango"]["total"], "range_end": d(scd["rango"]["end"]),
                     "span_wd": scd["fechas_del_equipo"]["total"], "span_end": d(scd["fechas_del_equipo"]["end"]),
                     "dated_wd": scd["con_adelantos"]["total"], "dated_end": d(scd["con_adelantos"]["end"]),
                     "corrected_wd": corr["total"], "corrected_end": d(corr["end"]),
                     "strict_wd": scd["fs_estricto"]["total"], "strict_end": d(scd["fs_estricto"]["end"]),
                     "calendar_days_10_04_to_30_09": (dt.date(2026, 9, 30) - dt.date(2026, 4, 10)).days + 1},
        "phase_wd": phase_wd, "critical_path": path, "n_critical": sum(1 for r in res.values() if r["critical"]),
        "critical_path_dated": path_dated, "n_critical_dated": scd["con_adelantos"]["n_critical"],
        "critical_path_corrected": path_corr, "n_critical_corrected": corr["n_critical"],
        "gates": gate_rows, "gates_ok": gate_ok, "gantt": gantt_info,
        "risks": {"emv_initial": sum(r["emv0"] for r in rrows), "emv_residual": sum(r["emv"] for r in rrows),
                  "emv_initial_usd": emv_init_usd, "emv_residual_usd": emv_res_usd,
                  "emv_residual_team15_usd": sum(r["emv_usd"] for r in team15),
                  "n": len(rrows), "n_new": sum(1 for r in rrows if r["new"]),
                  "sorted": [{k: r[k] for k in ("id", "name", "p", "i", "score", "level", "emv0", "pr", "ir", "emv", "emv0_usd", "emv_usd", "resp", "owner", "hl", "new", "mod")} for r in rrows_sorted]},
        "lines": lines, "categories": cats, "labour": lab_rows, "labour_a": lab_a, "labour_b": lab_b,
        "other_total": other_total, "maint_usd": maint_usd, "ladder_a": ladder_a, "ladder_b": ladder_b, "team_usd": team_usd,
        "gap_a_vs_team": ladder_a["total"] - team_usd["total"], "all_in_b": all_in_b, "buffer_wd": buf, "cash": cash, "cum": cum,
        "mgmt_reserve_pct": MGMT_RESERVE_PCT,
        "pyramid": cs.pyramid(lines, ladder_b, cats),
        "bridge": cs.bridge(team_usd["total"], team_cont_usd, ladder_a, ladder_b, lab_a, lab_b, maint_usd, D.TEAM_TOTAL, fx),
        "cash_baseline": base_curve["monthly"], "cum_baseline": base_curve["cumulative"],
        "p17": cs.p17_groups(lines), "indirect": dict(D.INDIRECT),
    }
    if with_sens:
        sens = {}
        for f in IMPACT_FACTORS:
            tot = sum(cs.round_half_up(cs.usd_of(D.SCALE["prob"][r["pr"]] * D.SCALE["impact_M"][r["ir"]] * f, fx)) for r in D.RISKS)
            sens[str(f)] = {"contingency": tot, "pct_of_costs_b": tot / costs_b, "pct_of_costs_a": tot / costs_a}
        out["sensitivity"] = sens
        fxs = {}
        for f in FX_FACTORS:
            o2, *_ = compute(fx=fx * f, with_sens=False)
            fxs[str(f)] = {"fx": fx * f, "total_a": o2["ladder_a"]["total"], "total_b": o2["ladder_b"]["total"],
                           "contingency": o2["ladder_b"]["contingency"], "costs_b": o2["ladder_b"]["project_costs"]}
        out["fx_sens"] = fxs
    return out, res, acts, cal


def schedule_rows(team, cal):
    """schedule.csv: the team's 40 rows as written + what each reading of the dependency column computes."""
    sc = {r["key"]: r for r in tg.scenarios(team, cal)}
    e, rg, fx = sc["escrito"]["res"], sc["rango"]["res"], sc["corregida"]["res"]
    fixed_txt = tg.explicit_deps_text(sc["corregida"]["acts"])
    cells_range = set(tg.corrected_cells(team, "range"))
    cells_end = set(tg.corrected_cells(team, "endpoints"))
    rows = []
    for a in D.ACTIVITIES:
        i = a["id"]
        s2 = team["sheet2"][i]
        change = "Sí" if i in cells_range else ("Aclarar" if i in cells_end else "No")
        if i in (2, 3):
            change = "Inicio-a-inicio"
        rows.append({
            "ID": i, "Fase": a["phase"], "Fase (nombre)": tg.PHASES[a["phase"] - 1], "Actividad": a["name"], "Duración (d.h.)": a["dur"],
            "Dependencias (como las escribió el equipo)": a["deps_raw"], "Inicio (equipo)": d(a["start"]), "Fin (equipo)": d(a["end"]),
            "Predecesoras (lectura extremos)": ",".join(map(str, a["preds"])), "Predecesoras (lectura rango)": ",".join(map(str, a["preds_range"])),
            "Predecesoras propuestas (explícitas)": fixed_txt[i], "Cambia": change,
            "Inicio temprano (extremos)": d(cal.start_date(e[i]["es"])), "Fin temprano (extremos)": d(cal.finish_date(e[i]["ef"])),
            "Holgura hoja del equipo": s2["slack"], "Holgura (extremos)": e[i]["slack"], "Crítica (extremos)": "Sí" if e[i]["critical"] else "No",
            "Holgura (rango)": rg[i]["slack"], "Crítica (rango)": "Sí" if rg[i]["critical"] else "No",
            "Holgura (propuesta)": fx[i]["slack"], "Crítica (propuesta)": "Sí" if fx[i]["critical"] else "No",
            "Responsable propuesto (rol)": D.ACTIVITY_OWNER[i],
            "Hito": next((f"G{p[0]}" for p in D.PHASES if D.PHASE_LAST[p[0]] == i), ""),
        })
    return rows


def build():
    out, res, acts, cal = compute()
    fx = out["fx"]["value"]
    rows = schedule_rows(D.TEAM, cal)
    with open(ROOT / "02-gantt" / "schedule.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    with open(ROOT / "04-riesgos.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["ID", "Riesgo", "Nuevo", "P", "I", "Puntaje", "Nivel", "EMV inicial (USD)", "Respuesta", "P res.", "I res.", "EMV residual (USD)", "Dueño", "Alto nivel Charter"])
        for r in out["risks"]["sorted"]:
            w.writerow([r["id"], r["name"], "sí" if r["new"] else "no", r["p"], r["i"], r["p"] * r["i"], rk.level(r["p"] * r["i"]),
                        r["emv0_usd"], r["resp"], r["pr"], r["ir"], r["emv_usd"], r["owner"], "sí" if r["hl"] else "no"])
    (ROOT / "tools" / "numbers.json").write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    with open(ROOT / "03-presupuesto" / "model.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Rol", "Meses del equipo", "Costo del equipo (ARS M)", "Tarifa implícita (ARS M/mes)", "Tarifa implícita (USD/mes)",
                    "Días hábiles en el Gantt", "Meses según Gantt", "Personas A (para conservar su costo)", "Costo A (USD)",
                    "Personas B (propuesta)", "Costo B (USD)"])
        for r in out["labour"]:
            w.writerow([r["label"], r["team_months"], f"{r['team_cost_ars']:.1f}", f"{r['rate_ars']:.2f}", f"{r['rate_usd']:.2f}", r["wd"],
                        f"{r['months']:.2f}", f"{r['qty_a']:.2f}", r["cost_a"], r["qty_b"], r["cost_b"]])
    with open(ROOT / "03-presupuesto" / "desglose.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["ID", "Concepto", "Categoría", "Paquete de trabajo", "Comportamiento", "Asignación", "Método de estimación (Clase 4)",
                    "Cantidad", "Unidad", "Costo unitario (USD)", "Duración (meses según Gantt)", "Subtotal equipo (USD)",
                    "Subtotal escenario B (USD)", "Equivalente equipo (ARS M)", "Supuesto", "Fuente", "Meses en que se incurre",
                    "Días hábiles (Gantt)"])
        for l in out["lines"]:
            dur = f"{l['duracion_meses']:.2f}" if l["duracion_meses"] is not None else "posterior al cierre"
            qty = f"{l['qty']:.2f}" if isinstance(l["qty"], float) else str(l["qty"])
            w.writerow([l["id"], l["concepto"], l["categoria"], l["wp"], l["comportamiento"], l["asignacion"], l["metodo"], qty, l["unidad"],
                        f"{l['unit_usd']:.2f}", dur, l["usd_team"], l["usd_b"], f"{l['ars_team_m']:.1f}", l["supuesto"], l["fuente"], l["meses"],
                        l["workdays"] if l["workdays"] is not None else "posterior al cierre"])
    return out, res, acts, cal


if __name__ == "__main__":
    o, *_ = build()
    print("FX", o["fx"]["value"], o["fx"]["date"])
    print("A", o["ladder_a"], "| team", o["team_usd"], "| gap", o["gap_a_vs_team"])
    print("B", o["ladder_b"], "| all-in", o["all_in_b"])
    print("EMV residual USD", o["risks"]["emv_residual_usd"], "initial", o["risks"]["emv_initial_usd"], "n", o["risks"]["n"])
    print("labour A/B", o["labour_a"], o["labour_b"], "other", o["other_total"], "maint", o["maint_usd"])
    print("sens", {k: v["contingency"] for k, v in o["sensitivity"].items()}, {k: (round(v["fx"], 1), v["total_b"]) for k, v in o["fx_sens"].items()})
    print("cash", o["cash"])
