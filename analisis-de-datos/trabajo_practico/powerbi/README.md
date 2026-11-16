# Dashboard Power BI

## Cómo abrirlo

1. Correr `python src/etl.py` desde la carpeta principal del trabajo. Deja los 7 CSV que usa el
   dashboard en `export/`. (En la entrega la carpeta `export/` ya viene armada, así que este paso se
   puede saltear.)
2. Abrir `TP_freMTPL2.pbix`.
3. Si Power BI no encuentra los datos: ir a Inicio, Transformar datos, Editar parámetros, y poner en
   `RutaDatos` la ruta completa de la carpeta `export\`, terminada en `\`. Después, Actualizar.
4. Si el mapa aparece bloqueado, ver `LEEME_MAPA.txt`.

## Archivos

| Archivo | Qué es |
|---|---|
| `TP_freMTPL2.pbix` | El dashboard, con 4 páginas: Cartera, Perfiles, Mapa y Calidad |
| `01_power_query.m` | Las consultas de carga, en texto |
| `02_medidas.dax` | Las medidas, en texto |
| `03_guia_dashboard.md` | Cómo armamos cada página y qué valores tiene que dar |
| `tema_tp.json` | El tema de colores |
| `valores_esperados.csv` | Relatividades calculadas en Python, para comprobar que el dashboard da lo mismo |

La tabla `siniestros` está cargada pero sin relación con las demás: solo se usaría para el tope
dinámico opcional que se describe en la sección 5 de la guía.

Las decisiones de diseño del dashboard están explicadas en `docs/08_dashboard.md`.
