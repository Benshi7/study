"""
etl.py — Todo el flujo del TP en un solo comando, de los CSV originales a los CSV para Power BI.

    1. EXTRAER     datasets/*.csv -> raw_    (copia fiel, sin corregir)
    2. LIMPIAR     raw_  -> core_            (docs/04 y docs/05)
    3. MODELAR     core_ -> mart_ -> export/ (tabla plana por póliza + tablas del dashboard)

Después de cada etapa se controla que no se haya perdido ningún registro ni ningún euro.
Si un control falla, el flujo se detiene: mejor no exportar nada que exportar algo incoherente.
El registro queda en export/etl_log.txt.

Uso (desde la carpeta trabajo_practico/):
    python src/etl.py              # tope de siniestros grandes en el percentil 99
    python src/etl.py 0.995        # otro percentil
"""

import sys
import time
from datetime import datetime

import build_core
import build_mart
import load_raw
from db import BASE, DATASETS, DB_PATH, conectar

EXPORT = BASE / "export"
registro = []


class ControlFallido(Exception):
    pass


def log(texto=""):
    print(texto)
    registro.append(texto)


def controlar(conn, nombre, sql_esperado, sql_obtenido):
    esperado = conn.execute(sql_esperado).fetchone()[0]
    obtenido = conn.execute(sql_obtenido).fetchone()[0]
    ok = esperado == obtenido
    log(f"    [{'OK' if ok else 'FALLA'}] {nombre}: {esperado:,} -> {obtenido:,}")
    if not ok:
        raise ControlFallido(nombre)


def filas_csv(nombre):
    with open(DATASETS / nombre, encoding="utf-8") as f:
        return sum(1 for _ in f) - 1          # menos el encabezado


def extraer():
    log("\n=== 1. EXTRAER (datasets/*.csv -> raw_)")
    DB_PATH.unlink(missing_ok=True)           # se reconstruye todo desde los CSV
    load_raw.main()
    with conectar() as conn:
        controlar(conn, "filas freq", f"SELECT {filas_csv('freMTPL2freq.csv')}", "SELECT COUNT(*) FROM raw_freq")
        controlar(conn, "filas sev", f"SELECT {filas_csv('freMTPL2sev.csv')}", "SELECT COUNT(*) FROM raw_sev")


def limpiar():
    log("\n=== 2. LIMPIAR (raw_ -> core_)")
    build_core.main()
    with conectar() as conn:
        controlar(conn, "pólizas", "SELECT COUNT(*) FROM raw_freq", "SELECT COUNT(*) FROM core_poliza")
        controlar(conn, "siniestros (con póliza + huérfanos)", "SELECT COUNT(*) FROM raw_sev",
                  "SELECT (SELECT COUNT(*) FROM core_siniestro) + (SELECT COUNT(*) FROM core_siniestro_huerfano)")
        controlar(conn, "pólizas con conteo inconsistente", "SELECT 0", """
            SELECT COUNT(*) FROM core_poliza p
            WHERE p.claimnb <> (SELECT COUNT(*) FROM core_siniestro s WHERE s.idpol = p.idpol)""")
        rotas = len(conn.execute("PRAGMA foreign_key_check").fetchall())
        controlar(conn, "claves foráneas rotas", "SELECT 0", f"SELECT {rotas}")


def modelar(percentil):
    log(f"\n=== 3. MODELAR (core_ -> mart_ -> export/), tope en el percentil {percentil:g}")
    sys.argv = [sys.argv[0], str(percentil)]  # build_mart lee el percentil de la línea de comandos
    build_mart.main()
    with conectar() as conn:
        controlar(conn, "pólizas", "SELECT COUNT(*) FROM core_poliza", "SELECT COUNT(*) FROM mart_poliza_analitica")
        controlar(conn, "siniestros", "SELECT COUNT(*) FROM core_siniestro",
                  "SELECT SUM(siniestros) FROM mart_poliza_analitica")
        controlar(conn, "monto total en centavos", "SELECT CAST(ROUND(SUM(claimamount) * 100) AS INTEGER) FROM core_siniestro",
                  "SELECT CAST(ROUND(SUM(monto) * 100) AS INTEGER) FROM mart_poliza_analitica")


def main():
    percentil = float(sys.argv[1]) if len(sys.argv) > 1 else build_mart.TOPE_PERCENTIL
    inicio = time.time()
    log(f"ETL TP freMTPL2 — {datetime.now():%Y-%m-%d %H:%M}")
    try:
        extraer()
        limpiar()
        modelar(percentil)
        log(f"\nETL terminado OK en {time.time() - inicio:.0f} s. Archivos en export/:")
        for f in sorted(EXPORT.glob("*.csv")):
            log(f"    {f.name:<28} {f.stat().st_size / 1e6:8.2f} MB")
        estado = 0
    except ControlFallido as e:
        log(f"\n*** ETL DETENIDO: falló el control «{e}». No usar export/ hasta revisarlo.")
        estado = 1
    EXPORT.mkdir(exist_ok=True)
    (EXPORT / "etl_log.txt").write_text("\n".join(registro) + "\n", encoding="utf-8")
    sys.exit(estado)


if __name__ == "__main__":
    main()
