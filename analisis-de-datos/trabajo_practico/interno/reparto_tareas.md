# Reparto de tareas — TP freMTPL2 (presentación 9/11)

## Lo que ya está hecho

| Pieza | Archivo | Para qué sirve |
|---|---|---|
| Caso, pregunta, hipótesis H1–H3 | `docs/01_caso.md` | El marco de todo |
| Comprensión de los datos | `notebooks/01_comprension.ipynb`, `docs/02_diccionario.md` | Diccionario y sospechas |
| Base SQLite (`raw_` → `core_`) | `sql/`, `src/`, `docs/03_modelo_datos.md` | Datos cargados y limpios |
| Calidad y limpieza (14 problemas, antes/después) | `docs/04_hallazgos_calidad.md`, `docs/05_limpieza.md` | Acto 1 de la historia |
| Borrador de historia con gráficos | `notebooks/02_historia.ipynb` | Primeros resultados de H1–H3 |
| Borrador de presentación (19 slides) | `presentacion/index.html` | Estructura del relato |

## La pieza que destraba todo: un dataset general

✅ **Hecho.** Se arma con `python src/build_mart.py` y deja tres CSV en `export/`:

| Archivo | Filas | Contenido |
|---|---:|---|
| `polizas.csv` | 678.013 | Una fila por póliza (ver abajo) |
| `siniestros.csv` | 26.444 | Una fila por siniestro: `idpol`, `monto`, `monto_topeado`, `es_grande` |
| `parametros.csv` | 2 | Con qué tope se armó (percentil y valor) |

`polizas.csv` es la **tabla plana `mart_poliza_analitica`**: una fila por póliza con
exposición, cantidad de siniestros, costo total, costo con tope, franjas (edad, BonusMalus,
antigüedad del vehículo), región con nombre oficial y región 2016, y las marcas de calidad.

Con ese CSV, cada tarea de abajo se puede hacer **sin tocar la base ni el SQL**.

## Tareas pendientes

| # | Tarea | Necesita | Bloquea a | ¿Independiente? |
|---|---|---|---|---|
| 0 | ~~Armar `mart_poliza_analitica` + CSV~~ | — | — | ✅ Hecho |
| 1 | ~~Tope de siniestros grandes~~ | — | — | ✅ Configurable: `python src/build_mart.py 0.995`. Por defecto p99 = 16.451,22 (recorta el 30,7 % del monto). Con `siniestros.csv` se puede probar otro tope sin correr nada |
| 2 | ~~ETL en un solo script + diagrama del flujo~~ | — | — | ✅ Hecho: `python src/etl.py`, `docs/06_etl.md`, `presentacion/img/etl_flujo.png` |
| 3 | ~~EDA completo en Python~~ | — | 7 | ✅ Hecho: `notebooks/03_eda.ipynb` + gráficos `presentacion/img/eda_*.png` |
| 4 | Dashboard Power BI (4 páginas: cartera, perfiles, mapa, calidad) | 0 (CSV) | 7 | 🟡 Casi: `powerbi/TP_freMTPL2.pbix` ya tiene mapa y Pareto. Faltan 3 ajustes (ver `powerbi/README.md`) |
| 5 | ~~Limitaciones y fuentes externas~~ | — | 7 | ✅ Hecho: `docs/07_limitaciones.md` (fuentes, 13 limitaciones de datos, 7 del análisis, mejoras futuras y versión corta para la slide) |
| 6 | *Opcional:* GLM Poisson para comparar con las relatividades simples | 0 | 7 | Sí |
| 7 | ~~Presentación final + guion~~ | — | — | ✅ Hecho: `presentacion/index.html` (13 slides, una por pauta, ≈ 15 min, tecla S = notas) + `docs/08_guion.md`. **Falta:** ensayar |

## Cómo se relaciona

```
mart + CSV (hecho) ──┬──► 2. ETL + diagrama
                     ├──► 3. EDA Python ────┐
                     ├──► 4. Power BI ──────┼──► 7. Presentación
                     └──► 6. GLM (opc.) ────┘
5. limitaciones / fuentes ──────────────────────► 7
```
