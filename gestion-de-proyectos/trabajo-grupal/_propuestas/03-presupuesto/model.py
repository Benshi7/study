"""Thin runner: prints the USD budget model. All logic lives in ../tools (costing.py, build_all.py, data.py).

Usage: python3 model.py [ARS_PER_USD]   (default: the single constant in tools/data.py)
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "tools"))
import build_all  # noqa: E402

if __name__ == "__main__":
    fx = float(sys.argv[1]) if len(sys.argv) > 1 else None
    o, *_ = build_all.compute(fx=fx)
    print("Tipo de cambio ARS/USD:", o["fx"]["value"], "·", o["fx"]["date"])
    print("Escenario A:", o["ladder_a"])
    print("Escenario B:", o["ladder_b"])
    print("Contingencia (Σ EMV residual, USD):", o["risks"]["emv_residual_usd"])
