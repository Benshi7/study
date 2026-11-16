"""
build_mart.py — Arma la capa MART (tablas listas para analizar) y la exporta a CSV.

    1. Calcula el tope de siniestros grandes y lo guarda en mart_parametro.
    2. Corre sql/30_mart.sql (pólizas y siniestros) y sql/31_mart_powerbi.sql (tablas del dashboard).
    3. Exporta todo a export/.

Requisito: haber corrido antes  python src/build_core.py   (o directamente  python src/etl.py)
Uso (desde la carpeta trabajo_practico/):
    python src/build_mart.py              # tope en el percentil 99
    python src/build_mart.py 0.995        # otro percentil, sin tocar el código
"""

import sys

import numpy as np
import pandas as pd

from db import BASE, conectar, ejecutar_script

# Un siniestro es "grande" si supera este percentil de los montos; por encima, se recorta al tope (H3).
TOPE_PERCENTIL = 0.99

EXPORT = BASE / "export"

TABLAS_A_EXPORTAR = {
    "mart_poliza_analitica": "polizas.csv",
    "mart_siniestro": "siniestros.csv",
    "mart_parametro": "parametros.csv",
    "mart_calidad_hallazgos": "calidad_hallazgos.csv",
    "mart_calidad_antes_despues": "calidad_antes_despues.csv",
    "mart_pareto": "pareto.csv",
    "mart_dim_region_mapa": "dim_region.csv",
}


def guardar_tope(conn, percentil):
    # SQLite no calcula percentiles: se hace con numpy (mismo método que notebooks/02_historia).
    montos = pd.read_sql("SELECT claimamount FROM core_siniestro", conn)["claimamount"]
    tope = float(np.percentile(montos, percentil * 100))
    conn.executescript("""
        DROP TABLE IF EXISTS mart_parametro;
        CREATE TABLE mart_parametro (nombre TEXT PRIMARY KEY, valor REAL NOT NULL);
    """)
    conn.executemany("INSERT INTO mart_parametro VALUES (?, ?)",
                     [("tope_percentil", percentil), ("tope_siniestro", tope)])
    conn.commit()
    return tope


def exportar(conn):
    EXPORT.mkdir(exist_ok=True)
    for tabla, archivo in TABLAS_A_EXPORTAR.items():
        df = pd.read_sql(f"SELECT * FROM {tabla}", conn)
        df.to_csv(EXPORT / archivo, index=False)
        print(f"  export/{archivo}: {len(df):,} filas")


def main():
    percentil = float(sys.argv[1]) if len(sys.argv) > 1 else TOPE_PERCENTIL
    conn = conectar()

    tope = guardar_tope(conn, percentil)
    ejecutar_script(conn, "30_mart.sql")
    ejecutar_script(conn, "31_mart_powerbi.sql")

    grandes, recorte = conn.execute(
        "SELECT SUM(es_grande), 1 - SUM(monto_topeado) / SUM(monto) FROM mart_siniestro").fetchone()
    print(f"Tope: percentil {percentil:g} = {tope:,.2f}. "
          f"{grandes:,} siniestros lo superan; el tope recorta el {100 * recorte:.1f} % del monto.")

    exportar(conn)
    conn.close()


if __name__ == "__main__":
    main()
