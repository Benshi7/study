"""
build_core.py — Construye la capa CORE (datos limpios) a partir de RAW.

Pasos:
  1. Recrea las tablas core_ (sql/02_core_tables.sql). RAW no se toca.
  2. Ejecuta sql/20_limpieza_core.sql (carga y correcciones).
  3. Controla que no se haya perdido ningún registro en el camino.

Requisito: haber corrido antes  python src/load_raw.py
Uso (desde la carpeta trabajo_practico/):
    python src/build_core.py
"""

from db import conectar, ejecutar_script


def contar(conn, tabla):
    return conn.execute(f"SELECT COUNT(*) FROM {tabla}").fetchone()[0]


def main():
    conn = conectar()
    print("Ejecutando 02_core_tables.sql ...")
    ejecutar_script(conn, "02_core_tables.sql")
    print("Ejecutando 20_limpieza_core.sql ...")
    ejecutar_script(conn, "20_limpieza_core.sql")

    # Controles de "no perder nada": todo lo que entra a raw tiene que aparecer en core.
    raw_freq, raw_sev = contar(conn, "raw_freq"), contar(conn, "raw_sev")
    poliza = contar(conn, "core_poliza")
    siniestro, huerfano = contar(conn, "core_siniestro"), contar(conn, "core_siniestro_huerfano")

    print("\nControl de carga")
    print(f"  pólizas:    raw_freq {raw_freq:,} -> core_poliza {poliza:,}"
          f"  {'OK' if raw_freq == poliza else 'DIFERENCIA'}")
    print(f"  siniestros: raw_sev {raw_sev:,} -> core_siniestro {siniestro:,}"
          f" + huérfanos {huerfano:,} = {siniestro + huerfano:,}"
          f"  {'OK' if raw_sev == siniestro + huerfano else 'DIFERENCIA'}")

    # PRAGMA foreign_key_check devuelve filas solo si alguna FK está rota (debería estar vacío)
    rotas = conn.execute("PRAGMA foreign_key_check").fetchall()
    print(f"  claves foráneas rotas: {len(rotas)}  {'OK' if not rotas else 'REVISAR'}")
    conn.close()


if __name__ == "__main__":
    main()
