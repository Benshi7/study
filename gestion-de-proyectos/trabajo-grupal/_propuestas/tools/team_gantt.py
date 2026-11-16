"""The team's REAL Gantt (Excel annex to section 6): loading, dependency readings and consistency checks.

The Excel is read-only input. `write_snapshot()` stores a JSON copy (team_gantt.json) so the pack does not
depend on the file being next to it; a test proves the snapshot equals the live workbook.
"""
import datetime as dt
import json
import pathlib
import re

import calendar_ar as car
import cpm
import xlsx_reader as xr

TOOLS = pathlib.Path(__file__).resolve().parent
TRABAJO = TOOLS.parent.parent
XLSX = TRABAJO / "Gantt_y_Camino_Critico_Hitos_Anexo_Punto_6.xlsx"
SNAPSHOT = TOOLS / "team_gantt.json"
PHASES = ["Inicio", "Análisis", "Diseño", "Desarrollo", "Integración", "Pruebas", "Implementación", "Cierre"]
_DATE2 = "%d/%m/%y"
_DATE4 = "%d/%m/%Y"


def _d(s, fmt):
    return dt.datetime.strptime(s, fmt).date()


def from_workbook(path=XLSX):
    sheets = dict(xr.read_workbook(path))
    s1 = sheets["Cronograma y Gantt"]
    acts = []
    for r in s1:
        if r and r[0].isdigit():
            r = r + [""] * (9 - len(r))
            acts.append({"id": int(r[0]), "phase": r[1], "name": r[2], "start": _d(r[3], _DATE2), "end": _d(r[4], _DATE2),
                         "dur": int(r[5]), "deps_raw": r[6], "responsable": r[7], "entregable": r[8]})
    sheet2 = {}
    for r in sheets["Dependencias y Camino Crítico"]:
        if r and r[0].isdigit():
            sheet2[int(r[0])] = {"phase": r[1], "name": r[2], "preds_raw": r[3], "dur": int(r[4]), "slack": int(r[5]),
                                 "critical": r[6].strip() == "SÍ"}
    hitos = []
    for r in sheets["Hitos Operativos y Académicos"]:
        if len(r) >= 4 and re.fullmatch(r"\d\d/\d\d/\d{4}", r[1] or ""):
            hitos.append({"name": r[0], "date": _d(r[1], _DATE4), "result": r[2], "scope": r[3]})
    anexo_rows = []
    for r in sheets["Anexo Punto 6"]:
        if len(r) >= 6 and r[0].isdigit() and r[4].strip() == "SÍ":
            anexo_rows.append({"id": int(r[0]), "name": r[1], "dur": int(r[2]), "slack": int(r[3]), "deps_raw": r[5]})
    return {"title": s1[0][0], "note": s1[1][0], "activities": acts, "sheet2": sheet2, "hitos": hitos,
            "anexo_rows": anexo_rows, "anexo_critical": [r["id"] for r in anexo_rows]}


def _to_json(o):
    if isinstance(o, dt.date):
        return {"__date__": o.isoformat()}
    raise TypeError(type(o))


def _from_json(o):
    if "__date__" in o:
        return dt.date.fromisoformat(o["__date__"])
    return o


def write_snapshot(path=SNAPSHOT, xlsx=XLSX):
    data = from_workbook(xlsx)
    pathlib.Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=1, default=_to_json), encoding="utf-8")
    return data


def load(path=SNAPSHOT):
    raw = json.loads(pathlib.Path(path).read_text(encoding="utf-8"), object_hook=_from_json)
    raw["sheet2"] = {int(k): v for k, v in raw["sheet2"].items()}
    return raw


# ---------------------------------------------------------------- dependency notation
def parse_deps(raw, mode):
    """'1-3' is read as {1,2,3} (mode 'range') or as {1,3} (mode 'endpoints'); commas always list explicit ids."""
    if mode not in ("range", "endpoints"):
        raise ValueError(f"unknown mode {mode!r}")
    raw = (raw or "").strip()
    if raw in ("", "-"):
        return []
    out = []
    for part in raw.split(","):
        part = part.strip()
        m = re.fullmatch(r"(\d+)\s*-\s*(\d+)", part)
        if m:
            a, b = int(m[1]), int(m[2])
            out += list(range(a, b + 1)) if mode == "range" else [a, b]
        else:
            out.append(int(part))
    return out


def is_ambiguous(raw):
    """True when a dash spans three or more numbers: only then do the two readings differ."""
    return any(int(m[2]) - int(m[1]) >= 2 for m in re.finditer(r"(\d+)\s*-\s*(\d+)", raw or ""))


def acts_for_cpm(data, mode, extra_links=()):
    """Activities in the shape cpm.schedule expects. `extra_links` = [(pred, succ)] FS links to add."""
    acts = {a["id"]: {"id": a["id"], "dur": a["dur"], "preds": parse_deps(a["deps_raw"], mode)} for a in data["activities"]}
    for p, s in extra_links:
        acts[s]["preds"] = sorted(set(acts[s]["preds"] + [p]))
    return [acts[i] for i in sorted(acts)]


def compare_to_team_sheet(res, data):
    """Differences between a CPM run and the slack / critical flags written in the team's sheet."""
    slack, crit = [], []
    for i, s in data["sheet2"].items():
        if res[i]["slack"] != s["slack"]:
            slack.append((i, res[i]["slack"], s["slack"]))
        if res[i]["critical"] != s["critical"]:
            crit.append(i)
    return {"slack": sorted(slack), "critical": sorted(crit)}


# ---------------------------------------------------------------- calendar and stated dates
def weekday_calendar(start=dt.date(2026, 4, 1)):
    """The team's convention: every Monday-to-Friday is a working day (no holidays)."""
    return car.Calendar(start, holidays=frozenset())


def stated_index(data, cal):
    """{id: (es, ef)} working-day indexes (ef exclusive) read from the team's stated dates."""
    return {a["id"]: (cal.index_of(a["start"]), cal.index_of(a["end"]) + 1) for a in data["activities"]}


def overlap_pairs(data, mode):
    """(successor, predecessor) where the successor's stated start is on/before the predecessor's stated end."""
    end = {a["id"]: a["end"] for a in data["activities"]}
    out = []
    for a in data["activities"]:
        for p in parse_deps(a["deps_raw"], mode):
            if a["start"] <= end[p]:
                out.append((a["id"], p))
    return sorted(out, key=lambda t: (t[0], t[1]))


def overlap_leads(data, mode, cal):
    """(successor, predecessor, working days the successor starts BEFORE a finish-to-start would allow)."""
    idx = stated_index(data, cal)
    out = []
    for s, p in overlap_pairs(data, mode):
        out.append((s, p, idx[p][1] - idx[s][0]))
    return out


def _ancestors(acts):
    by = {a["id"]: a for a in acts}
    memo = {}

    def anc(i):
        if i not in memo:
            s = set()
            for p in by[i]["preds"]:
                s |= {p} | anc(p)
            memo[i] = s
        return memo[i]

    return {i: anc(i) for i in by}


def adjacent_unlisted_links(data, mode, cal):
    """(j, i) pairs where i starts the working day after j ends but j is not a (transitive) predecessor of i.

    These are places where the dates imply a dependency that the dependency column does not list.
    """
    idx = stated_index(data, cal)
    anc = _ancestors(acts_for_cpm(data, mode))
    out = []
    for i, (es, _) in idx.items():
        for j, (_, ef) in idx.items():
            if j != i and ef == es and j not in anc[i] and i not in anc[j]:
                out.append((j, i))
    return sorted(out)


def idle_gaps(data, mode, cal):
    """(pred, succ, idle working days) where a successor starts later than its latest predecessor requires."""
    idx = stated_index(data, cal)
    out = []
    for a in data["activities"]:
        preds = parse_deps(a["deps_raw"], mode)
        if not preds:
            continue
        latest = max(preds, key=lambda p: idx[p][1])
        gap = idx[a["id"]][0] - idx[latest][1]
        if gap > 0:
            out.append((latest, a["id"], gap))
    return sorted(out)


def holiday_hits(data, holidays):
    """[(id, [holiday dates inside the activity's stated range])] for weekday holidays."""
    out = []
    for a in data["activities"]:
        days = [a["start"] + dt.timedelta(k) for k in range((a["end"] - a["start"]).days + 1)]
        hit = [x for x in days if x in holidays and x.weekday() < 5]
        if hit:
            out.append((a["id"], hit))
    return out


def phase_windows(data):
    out = {}
    for p in PHASES:
        rows = [a for a in data["activities"] if a["phase"] == p]
        out[p] = (min(a["start"] for a in rows), max(a["end"] for a in rows))
    return out


def phase_window_differences(data, declared):
    """Phases whose window in another document differs from the Excel's (start or end)."""
    team = phase_windows(data)
    out = []
    for name, (ds, de) in declared.items():
        ts, te = team[name]
        if (ds, de) != (ts, te):
            out.append({"phase": name, "declared_start": ds, "declared_end": de, "team_start": ts, "team_end": te})
    return out


MISSING_LINKS = [(26, 27)]   # dates say 27 (Pruebas funcionales) starts right after 26 ends; the dependency column omits it


def dated_network(data, mode, cal, extra_links=tuple(MISSING_LINKS)):
    """The network that reproduces the team's stated dates: leads for the overlaps plus the missing links."""
    acts = {a["id"]: {"id": a["id"], "dur": a["dur"], "preds": list(parse_deps(a["deps_raw"], mode))} for a in data["activities"]}
    for s, p, k in overlap_leads(data, mode, cal):
        acts[s]["preds"] = [(x, -k) if x == p else x for x in acts[s]["preds"]]
    for p, s in extra_links:
        acts[s]["preds"] = acts[s]["preds"] + [p]
    return [acts[i] for i in sorted(acts)]


# Dependencies re-derived from the team's STATED DATES (hypothesis, to confirm with whoever built the Excel).
# (id, -k) = finish-to-start with a lead of k days; 2 and 3 start the day after 1 starts (start-to-start + 1).
CORRECTED_DEPS = {
    1: [], 2: [(1, -2)], 3: [(1, -2)], 4: [1, 2, 3], 5: [4], 6: [4], 7: [4], 8: [5, 6], 9: [5, 6], 10: [7, 8, 9],
    11: [10], 12: [10], 13: [10], 14: [11], 15: [10, 11], 16: [12, 13], 17: [11, 12, 13, 14, 15, 16],
    18: [17], 19: [17], 20: [19], 21: [19, 20], 22: [17], 23: [15, 18], 24: [18, 23], 25: [23], 26: [24, 25],
    27: [26], 28: [26, 27], 29: [16, 27], 30: [27], 31: [27, 28, 29, 30], 32: [31], 33: [32], 34: [32],
    35: [33, 34], 36: [35], 37: [36], 38: [36], 39: [36, 37, 38], 40: [37, 38, 39],
}


def corrected_network(data):
    dur = {a["id"]: a["dur"] for a in data["activities"]}
    return [{"id": i, "dur": dur[i], "preds": list(CORRECTED_DEPS[i])} for i in sorted(CORRECTED_DEPS)]


def corrected_cells(data, mode):
    """Activities whose written dependency list (read as `mode`) differs from the corrected one."""
    out = []
    for a in data["activities"]:
        written = set(parse_deps(a["deps_raw"], mode))
        fixed = {p[0] if isinstance(p, tuple) else p for p in CORRECTED_DEPS[a["id"]]}
        if written != fixed:
            out.append(a["id"])
    return out


def explicit_deps_text(net):
    """Spreadsheet-ready dependency text per activity: '5, 6', '-', or '1 (inicio-a-inicio +1 día)'."""
    dur = {a["id"]: a["dur"] for a in net}
    out = {}
    for a in net:
        parts = []
        for p, lag in cpm.links(a):
            if lag < 0:
                n = dur[p] + lag
                parts.append(f"{p} (inicio-a-inicio +{n} día{'s' if n != 1 else ''})")
            else:
                parts.append(str(p))
        out[a["id"]] = ", ".join(parts) if parts else "-"
    return out


def _summary(key, label, acts, cal):
    res = cpm.schedule(acts)
    total = cpm.project_duration(res)
    return {"key": key, "label": label, "total": total, "end": cal.finish_date(total),
            "n_critical": sum(1 for r in res.values() if r["critical"]), "res": res, "acts": acts}


def scenarios(data, cal):
    """Five readings of the same Gantt, in a fixed order, each with its total (working days) and end date."""
    out = [
        _summary("escrito", "Como está escrito, «a-b» = los dos extremos (lo que calcula la hoja del equipo)", acts_for_cpm(data, "endpoints"), cal),
        _summary("rango", "Como está escrito, «a-b» = todo el rango", acts_for_cpm(data, "range"), cal),
    ]
    idx = stated_index(data, cal)
    total = max(e for _, e in idx.values())
    out.append({"key": "fechas_del_equipo", "label": "Fechas escritas por el equipo (columnas Inicio/Fin)", "total": total,
                "end": cal.finish_date(total), "n_critical": None, "res": None, "acts": None})
    out.append(_summary("corregida", "Dependencias corregidas según las fechas (7 celdas y 2 inicio-a-inicio)",
                        corrected_network(data), cal))
    out.append(_summary("con_adelantos", "Dependencias completas: 7 adelantos y el vínculo 26→27 (reproduce las fechas)",
                        dated_network(data, "endpoints", cal), cal))
    out.append(_summary("fs_estricto", "Fin-a-inicio estricto, sin adelantos, más el vínculo 26→27",
                        acts_for_cpm(data, "endpoints", MISSING_LINKS), cal))
    return out


def gap_explanation(data, cal):
    sc = {r["key"]: r for r in scenarios(data, cal)}
    stated = sc["fechas_del_equipo"]["total"]
    strict = sc["fs_estricto"]["total"]
    dated = sc["con_adelantos"]["total"]
    return {"stated_total": stated, "as_written_total": sc["escrito"]["total"], "with_link_strict_total": strict,
            "leads_saved": strict - dated, "idle_days": stated - dated}


if __name__ == "__main__":
    d = write_snapshot()
    print("snapshot written:", SNAPSHOT.name, "|", len(d["activities"]), "activities,", len(d["hitos"]), "hitos")
