# TP Integrador · Análisis de Datos

**¿Quién cuesta más?** Costo esperado de siniestros por perfil de conductor y vehículo en un seguro
de autos de Francia (dataset freMTPL2).

Integrantes: Bruno, Juan Pablo, Uriel y Nicolás.

Nos ubicamos en el rol del equipo de pricing de una aseguradora y le presentamos a la dirección
técnica qué perfiles tienen mayor costo esperado de siniestros (prima pura) y cuánto se apartan del
promedio de la cartera.

Para una vista general del trabajo, abrir `documentacion.html`. Ahí está todo resumido en una página.

## Qué hay en cada carpeta

```
├── documentacion.html   documentación breve del proceso (resumen de todo)
├── docs/                un documento por etapa, en el orden de la consigna
├── datasets/            los dos CSV originales, sin modificar
├── sql/                 creación de tablas, consultas de exploración y calidad, limpieza y mart
├── src/                 scripts de Python del ETL (etl.py corre todo)
├── notebooks/           demo del ETL, comprensión de los datos, hipótesis y EDA
├── export/              dataset final que usan Power BI y los notebooks
├── powerbi/             dashboard (.pbix), consultas, medidas y guía
├── presentacion/        presentación de la exposición (index.html) y gráficos
└── requirements.txt     librerías de Python
```

## Dónde está cada etapa

| Etapa de la consigna | Documento | Evidencia |
|---|---|---|
| 1. Definición del caso | `docs/01_caso.md` | |
| 2. Recolección y comprensión de los datos | `docs/02_diccionario.md` | `notebooks/01_comprension.ipynb` |
| 3. Modelado y almacenamiento | `docs/03_modelo_datos.md` | `sql/01_raw_tables.sql`, `sql/02_core_tables.sql`, `src/db.py`, `src/load_raw.py` |
| 4. Consultas SQL | `docs/04_hallazgos_calidad.md` | `sql/10_exploracion.sql`, `sql/11_calidad.sql` |
| 5. Calidad, limpieza y normalización | `docs/05_limpieza.md` | `sql/20_limpieza_core.sql`, `sql/21_antes_despues.sql`, `src/build_core.py` |
| 6. ETL | `docs/06_etl.md` | `src/etl.py`, `notebooks/00_etl_demo.ipynb`, diagrama en `presentacion/img/etl_flujo.png` |
| 7. Análisis exploratorio con Python | `docs/07_eda.md` | `notebooks/02_historia.ipynb`, `notebooks/03_eda.ipynb` |
| 8. Dashboard en Power BI | `docs/08_dashboard.md` | `powerbi/TP_freMTPL2.pbix` |
| 9. Conclusiones, limitaciones y mejoras | `docs/09_conclusiones_limitaciones.md` | `presentacion/index.html` |

El dataset final que usa Power BI es `export/polizas.csv` (una fila por póliza), junto con las tablas
chicas del dashboard que están en la misma carpeta.

## Cómo correrlo

Hace falta Python 3.10 o más nuevo. SQLite viene incluido con Python.

```bash
python -m venv .venv
source .venv/bin/activate          # en Windows: .venv\Scripts\activate
pip install -r requirements.txt

python src/etl.py                  # CSV -> raw_ -> core_ -> mart_ -> export/  (unos 10 segundos)
```

El ETL arma la base `db/seguros.db` desde cero y deja el dataset final en `export/`, con un registro
de los controles en `export/etl_log.txt`. El tope de los siniestros grandes está en el percentil 99;
se puede cambiar, por ejemplo con `python src/etl.py 0.995`.

También se puede correr paso a paso:

```bash
python src/load_raw.py                      # carga los CSV a raw_
python src/run_sql.py 10_exploracion.sql    # consultas de exploración
python src/run_sql.py 11_calidad.sql        # consultas de calidad
python src/build_core.py                    # limpieza: raw_ -> core_
python src/run_sql.py 21_antes_despues.sql  # comparación antes y después
python src/build_mart.py                    # mart_ y export/
```

Los notebooks se abren con `jupyter notebook notebooks/`. Ya tienen los resultados guardados. El
`01_comprension` lee los CSV originales; los demás necesitan que antes se haya corrido el ETL.

Para ver la base desde DBeaver: nueva conexión SQLite y elegir el archivo `db/seguros.db`.

La presentación se abre con `presentacion/index.html` en el navegador. Se navega con las flechas.

## Criterios que seguimos

- Ningún número de la documentación está escrito a mano: todos salen de una consulta o de una celda.
- Las suposiciones están aclaradas como tales.
- La capa `raw_` nunca se corrige. Las correcciones se hacen en `core_` y se muestran como antes y
  después.
