"""
run_sql.py — Ejecuta un archivo de consultas y muestra cada resultado como tabla.

Uso (desde la carpeta trabajo_practico/):
    python src/run_sql.py 10_exploracion.sql
    python src/run_sql.py 11_calidad.sql
"""

import sys

from db import conectar, correr_consultas

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Uso: python src/run_sql.py <archivo.sql dentro de sql/>")
    conn = conectar()
    correr_consultas(conn, sys.argv[1])
    conn.close()
