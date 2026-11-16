"""
load_raw.py — Crea la base SQLite y carga los CSV originales a la capa RAW.

Pasos:
  1. Ejecuta sql/01_raw_tables.sql (crea las tablas raw_).
  2. Lee cada CSV con pandas SIN transformar los datos y lo inserta en raw_<tabla>.
  3. Imprime un conteo de filas: CSV vs tabla, para comprobar que no se perdió nada.

Uso (desde la carpeta trabajo_practico/):
    python src/load_raw.py
"""

import pandas as pd

from db import DATASETS, conectar, ejecutar_script

# CSV -> tabla destino
ARCHIVOS = {
    "freMTPL2freq.csv": "raw_freq",
    "freMTPL2sev.csv": "raw_sev",
}

# Scripts de estructura, en orden
DDL = ["01_raw_tables.sql"]   # las tablas core_ las crea build_core.py


def cargar_csv(conn, archivo, tabla):
    """Lee un CSV y lo inserta en la tabla. Devuelve la cantidad de filas del CSV."""
    # dtype=str en IDpol de freq: así "1.00E+05" llega como texto, igual que en el archivo.
    tipos = {"IDpol": str} if tabla == "raw_freq" else None
    df = pd.read_csv(DATASETS / archivo, dtype=tipos)

    # Único cambio: nombres de columna en minúscula (coinciden con el DDL)
    df.columns = [c.lower() for c in df.columns]

    # if_exists="append": la tabla ya la creó 01_raw_tables.sql con los tipos que elegimos
    df.to_sql(tabla, conn, if_exists="append", index=False)
    return len(df)


def main():
    conn = conectar()
    for nombre in DDL:
        print(f"Ejecutando {nombre} ...")
        ejecutar_script(conn, nombre)

    filas_csv = {}
    for archivo, tabla in ARCHIVOS.items():
        print(f"Cargando {archivo} -> {tabla} ...")
        filas_csv[tabla] = cargar_csv(conn, archivo, tabla)
    conn.commit()

    # Control: ¿la base tiene la misma cantidad de filas que los CSV?
    print("\nControl de carga")
    print(f"{'tabla':<10}{'filas CSV':>12}{'filas DB':>12}  estado")
    for tabla, n_csv in filas_csv.items():
        n_db = conn.execute(f"SELECT COUNT(*) FROM {tabla}").fetchone()[0]
        estado = "OK" if n_db == n_csv else "DIFERENCIA"
        print(f"{tabla:<10}{n_csv:>12,}{n_db:>12,}  {estado}")
    conn.close()


if __name__ == "__main__":
    main()
