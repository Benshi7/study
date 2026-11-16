"""Spanish number formatting and small markdown helpers (USD is the reporting currency)."""
import data as D


def n(x, nd=1):
    """1234.5 -> '1.234,5' (Spanish)."""
    s = f"{x:,.{nd}f}"
    return s.replace(",", "§").replace(".", ",").replace("§", ".")


def usd(v):
    """Whole US dollars: 261115 -> 'USD 261.115'."""
    return "USD " + n(int(v + 0.5) if v >= 0 else -int(-v + 0.5), 0)


def usd2(v):
    """Unit price with cents: 3883.495 -> 'USD 3.883,50' (so that unit x days / 21 reproduces the subtotal)."""
    return "USD " + n(v, 2)


def u(ars_m, fx=None):
    """Millions of ARS (the team's figures) -> 'USD x' at the single exchange rate."""
    fx = D.FX_ARS_PER_USD if fx is None else fx
    return usd(ars_m * 1e6 / fx)


def ars(x, nd=1):
    """Reference amount in ARS millions: 'ARS 344,3 M'."""
    return f"ARS {n(x, nd)} M"


def pct(x, nd=1):
    return f"{n(100 * x, nd)} %"


def table(headers, rows, align=None):
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c) for c in r) + " |")
    return "\n".join(out)
