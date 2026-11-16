"""
db.py — Funciones compartidas para trabajar con la base SQLite del TP.

La base es un único archivo: db/seguros.db (se crea solo la primera vez).
"""

import re
import sqlite3
from pathlib import Path

import pandas as pd

# Rutas del proyecto (relativas a este archivo, así funciona desde cualquier carpeta)
BASE = Path(__file__).resolve().parent.parent
DB_PATH = BASE / "db" / "seguros.db"
SQL_DIR = BASE / "sql"
DATASETS = BASE / "datasets"


def conectar():
    """Abre la base y activa las claves foráneas.

    En SQLite las FK vienen DESACTIVADAS por defecto: sin este PRAGMA, la base aceptaría
    un siniestro de una póliza inexistente sin quejarse.
    """
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def ejecutar_script(conn, nombre_archivo):
    """Ejecuta un .sql de estructura (CREATE/DROP) completo, sin mostrar resultados."""
    conn.executescript((SQL_DIR / nombre_archivo).read_text(encoding="utf-8"))
    conn.commit()


def separar_sentencias(texto):
    """Corta el texto de un .sql en sentencias. Cada una conserva sus comentarios de arriba.

    sqlite3.complete_statement() dice si lo acumulado ya forma una sentencia completa
    (termina en ';' fuera de comentarios y textos).
    """
    sentencias, actual = [], ""
    for linea in texto.splitlines(keepends=True):
        actual += linea
        if sqlite3.complete_statement(actual):
            sentencias.append(actual.strip())
            actual = ""
    return sentencias


def titulo_de(sentencia):
    """Devuelve el comentario-título de una consulta (ej. '-- E1. ¿Cuántas filas...').

    Un título es un comentario que empieza con una letra mayúscula, un número y un punto:
    E1., C5b., A2., etc.
    """
    for linea in sentencia.splitlines():
        if re.match(r"--\s*[A-Z]\d+\w*\.", linea):
            return linea.lstrip("- ").strip()
    return None


def correr_consultas(conn, nombre_archivo):
    """Ejecuta un .sql de consultas y muestra el resultado de cada SELECT como tabla."""
    texto = (SQL_DIR / nombre_archivo).read_text(encoding="utf-8")
    for sentencia in separar_sentencias(texto):
        cursor = conn.execute(sentencia)
        if cursor.description is None:          # no devuelve filas (ej. CREATE TEMP VIEW)
            continue
        columnas = [c[0] for c in cursor.description]
        df = pd.DataFrame(cursor.fetchall(), columns=columnas)
        titulo = titulo_de(sentencia)
        if titulo:
            print(f"\n=== {titulo}")
        print(df.to_string(index=False) if len(df) else "(sin filas)")
