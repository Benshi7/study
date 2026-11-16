"""Risk scoring (team scale 1-5 x 1-5) and expected monetary value (Clase 5, p31)."""

LEVELS = ((4, "Bajo"), (9, "Medio"), (16, "Alto"), (25, "Crítico"))


def score(p, i):
    if not (1 <= p <= 5 and 1 <= i <= 5):
        raise ValueError("probability and impact must be in 1..5")
    return p * i


def level(s):
    for upper, name in LEVELS:
        if s <= upper:
            return name
    raise ValueError(f"score out of range: {s}")


def emv(prob, impact_money):
    return prob * impact_money


def emv_from_levels(p, i, base, scale):
    """EMV in the same unit as `base`, converting ordinal levels with an explicit scale."""
    return emv(scale["prob"][p], scale["impact_pct_of_base"][i] * base)


def total_emv(rows, mode="threats_only"):
    if mode not in ("threats_only", "net"):
        raise ValueError("mode must be 'threats_only' or 'net'")
    threats = sum(r["emv"] for r in rows if r["kind"] == "amenaza")
    opps = sum(r["emv"] for r in rows if r["kind"] == "oportunidad")
    return threats if mode == "threats_only" else threats - opps


def sort_by_emv(rows):
    return sorted(rows, key=lambda r: (-r["emv"], r["id"]))


def check_residual(p0, i0, p1, i1):
    """A response may not make the residual risk worse than the initial one."""
    if p1 > p0 or i1 > i0:
        raise ValueError("residual probability/impact must not exceed the initial ones")
