"""Coherence checks that READ the generated documents (text), not the model that produced them."""
import csv
import datetime as dt
import io
import pathlib
import re

import budget as bud
import calendar_ar as car
import coherence as co
import data as D
import team_gantt as tg

FILES = {
    "00": "00-resumen.md", "01": "01-charter-condensado.md", "03": "03-presupuesto/presupuesto.md",
    "04": "04-riesgos.md", "05": "05-canvas-dt-smart.md", "06": "06-coherencia.md", "gantt": "02-gantt/gantt.md",
    "schedule": "02-gantt/schedule.csv", "model": "03-presupuesto/model.csv", "risks_csv": "04-riesgos.csv",
    "07": "07-formato-entrega.md", "desglose": "03-presupuesto/desglose.csv",
}


def load(root):
    root = pathlib.Path(root)
    return {k: (root / v).read_text(encoding="utf-8") for k, v in FILES.items()}


def _date(s):
    d, m_, y = s.split("/")
    return dt.date(int(y), int(m_), int(d))


def _money(s):
    """'USD 261.115' -> 261115"""
    return float(re.search(r"USD\s*([\d.]+)", s).group(1).replace(".", ""))


def check_gates(docs):
    charter = {m.group(1): m.group(2) for m in re.finditer(r"\| (G\d) \|[^|]*\| (\d\d/\d\d/\d{4}) \|", docs["01"])}
    sched = list(csv.DictReader(io.StringIO(docs["schedule"])))
    gantt = {}
    for r in sched:
        if r["Hito"]:                       # the activity that closes each gate (e.g. 35 closes G7, not 36)
            gantt[r["Hito"]] = _date(r["Fin (equipo)"]).strftime("%d/%m/%Y")
    return co.check_milestones(charter, gantt)


def check_budget(docs):
    m1 = re.search(r"\*\*Presupuesto total\*\* \| \*\*(USD [\d.]+)\*\*", docs["01"])
    m2 = re.search(r"\| \*\*Total\*\* \| [^|]*\| [^|]*\| \*\*(USD [\d.]+)\*\* \|", docs["03"])
    if not (m1 and m2):
        return co.Check("presupuesto Charter = total", False, "total not found in Charter or in presupuesto.md")
    return co.check_budget_total(_money(m1.group(1)), _money(m2.group(1)))


def check_risks_subset(docs):
    m_ = re.search(r"\*\*9\. Riesgos de alto nivel\*\*[^\n]*", docs["01"])
    ids = re.findall(r"\*\*(R\d\d)\*\*", m_.group(0)) if m_ else []
    rows = list(csv.DictReader(io.StringIO(docs["risks_csv"])))
    matrix = [r["ID"] for r in rows]
    hl = {r["ID"] for r in rows if r["Alto nivel Charter"] == "sí"}
    sub = co.check_subset("riesgos", ids, matrix)
    if sub.ok and set(ids) != hl:
        return co.Check(sub.name, False, f"Charter lists {sorted(ids)} but matrix flags {sorted(hl)}")
    return sub if ids else co.Check(sub.name, False, "no risk ids found in the Charter")


def check_contingency(docs):
    m_ = re.search(r"Reserva de contingencia \(Σ EMV de la matriz de riesgos\) \| (USD [\d.]+)", docs["01"])
    rows = list(csv.DictReader(io.StringIO(docs["risks_csv"])))
    total = sum(float(r["EMV residual (USD)"]) for r in rows)
    if not m_:
        return co.Check("contingencia = Σ EMV", False, "contingency not found in Charter")
    val = _money(m_.group(1))
    ok = abs(val - total) <= 1
    return co.Check("contingencia = Σ EMV", ok, "ok" if ok else f"Charter {val:.0f} vs Σ EMV {total:.0f}")


def check_labour(docs):
    """Re-derives working days per role from the DATES in schedule.csv (independent of the CPM run)."""
    sched = {int(r["ID"]): r for r in csv.DictReader(io.StringIO(docs["schedule"]))}
    cal = tg.weekday_calendar(D.SIM_START)
    spans = {}
    for i, r in sched.items():
        spans[i] = {"es": cal.index_of(_date(r["Inicio (equipo)"])), "ef": cal.index_of(_date(r["Fin (equipo)"])) + 1}
    model = {r["Rol"]: r for r in csv.DictReader(io.StringIO(docs["model"]))}
    declared, derived, wd_bad = {}, {}, []
    for key, label, tm, tc, ids in D.TEAM_ROLES:
        if label not in model:
            return co.Check("mano de obra = duraciones del Gantt", False, f"role {label!r} missing in model.csv")
        wd = bud.role_workdays(spans, ids)
        if int(model[label]["Días hábiles en el Gantt"]) != wd:
            wd_bad.append((label, model[label]["Días hábiles en el Gantt"], wd))
        declared[key] = float(model[label]["Meses según Gantt"])
        derived[key] = bud.months(wd)
    res = co.check_labour_months(declared, derived, tol=0.006)
    if wd_bad:
        return co.Check(res.name, False, f"working days differ from schedule.csv: {wd_bad}")
    return res


def check_stakeholders(docs):
    m_ = re.search(r"\*\*11\. Stakeholders principales\*\*[^\n]*", docs["01"])
    line = m_.group(0) if m_ else ""
    missing_in_doc = [s for s in D.CHARTER_STAKEHOLDERS_PROPOSED if s not in line]
    base = co.check_stakeholders(D.CHARTER_STAKEHOLDERS_PROPOSED, D.STAKEHOLDERS_F4, D.COMMS_PROPOSED)
    if missing_in_doc:
        return co.Check(base.name, False, f"not in the Charter text: {missing_in_doc}")
    return base


def check_bridges(docs):
    found = {m.group(1): m.group(2).strip() for m in re.finditer(r"^\| (\d+) \| (.{40,}) \|$", docs["06"], flags=re.M)}
    sections = [str(i) for i in range(3, 11)]
    bridges = {k: (v if len(v.split()) >= 8 else "") for k, v in found.items()}
    return co.check_bridges(bridges, sections)


def run(docs):
    return [check_gates(docs), check_budget(docs), check_risks_subset(docs), check_contingency(docs),
            check_labour(docs), check_stakeholders(docs), check_bridges(docs)]


if __name__ == "__main__":
    for c in run(load(pathlib.Path(__file__).resolve().parent.parent)):
        print(("OK " if c.ok else "FAIL"), c.name, "-", c.detail)
