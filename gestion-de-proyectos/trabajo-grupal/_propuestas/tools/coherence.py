"""Cross-section coherence checks used by the proposals (and reusable for the final document)."""
from collections import namedtuple

Check = namedtuple("Check", "name ok detail")


def check_milestones(charter, gantt):
    miss = sorted(set(charter) ^ set(gantt))
    diff = sorted(k for k in set(charter) & set(gantt) if charter[k] != gantt[k])
    ok = not miss and not diff
    detail = "ok" if ok else f"missing in one side: {miss}; different dates: {diff}"
    return Check("hitos Charter = Gantt", ok, detail)


def check_budget_total(charter_total, budget_total, tol=1e-9):
    ok = abs(charter_total - budget_total) <= tol
    return Check("presupuesto Charter = total", ok, "ok" if ok else f"{charter_total} vs {budget_total}")


def check_subset(label, small, big):
    extra = sorted(set(small) - set(big))
    return Check(f"{label} Charter ⊂ matriz", not extra, "ok" if not extra else f"not in matrix: {extra}")


def check_contingency(contingency, emv_total, tol=1e-6):
    ok = abs(contingency - emv_total) <= tol
    return Check("contingencia = Σ EMV", ok, "ok" if ok else f"{contingency} vs {emv_total}")


def check_labour_months(declared, from_gantt, tol=0.25):
    bad = {k: (declared[k], from_gantt.get(k)) for k in declared if abs(declared[k] - from_gantt.get(k, 1e9)) > tol}
    return Check("mano de obra = duraciones del Gantt", not bad, "ok" if not bad else f"{bad}")


def check_stakeholders(charter, matrix, comms):
    miss_matrix = sorted(set(charter) - set(matrix))
    miss_comms = sorted(set(matrix) - set(comms))
    ok = not miss_matrix and not miss_comms
    detail = "ok" if ok else f"Charter not in matrix: {miss_matrix}; matrix not in comms: {miss_comms}"
    return Check("stakeholders Charter ∈ matriz ∈ comunicación", ok, detail)


def check_bridges(bridges, sections):
    empty = [s for s in sections if not bridges.get(s, "").strip()]
    return Check("frase puente por sección", not empty, "ok" if not empty else f"missing: {empty}")
