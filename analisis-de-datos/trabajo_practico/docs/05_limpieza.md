# 5. Limpieza y normalización

En esta etapa cargamos la capa `core_` a partir de `raw_`, aplicando lo que decidimos en el
documento 4. La capa `raw_` no se toca: es el "antes" y `core_` es el "después".

- Estructura de las tablas: `sql/02_core_tables.sql`
- Correcciones: `sql/20_limpieza_core.sql` (cada paso indica qué problema resuelve)
- Comparación antes y después: `sql/21_antes_despues.sql` (códigos A)
- Se corre con `python src/build_core.py` y después `python src/run_sql.py 21_antes_despues.sql`

## Criterio: corregir, marcar o dejar

No todos los problemas se pueden arreglar. Para cada uno elegimos una de tres acciones:

| Acción | Cuándo la usamos | Ejemplo |
|--------|------------------|---------|
| Corregir | Cuando sabemos cuál es el valor correcto | `1.00E+05` pasa a 100000 |
| Marcar | Cuando el dato es sospechoso pero borrarlo también sesgaría el análisis | El lote de `IDpol` ≤ 24.500 |
| Dejar | Cuando el dato es raro pero real, o no tenemos forma de saber cuál sería el correcto | Siniestros repetidos, edades de más de 90 |

Las marcas son columnas `flag_` con 0 o 1. No borran nada, pero permiten filtrar o comparar después
en el EDA y en Power BI.

## Qué hicimos con cada problema

| # | Problema | Acción | Cómo | Registros (A4) |
|---|----------|--------|------|---------------:|
| Q1 y Q2 | `ClaimNb` no coincide con la tabla de siniestros | Corregir | `claimnb` pasa a ser la cantidad de siniestros con monto; el valor original queda en `claimnb_declarado` y se marca `flag_claimnb_corregido` | 9.117 |
| Q3 | Lote de `IDpol` ≤ 24.500 | Marcar | `flag_lote_idpol_bajo = 1` | 9.139 |
| Q4 | Siniestros sin póliza | Apartar | Van a `core_siniestro_huerfano` | 195 |
| Q5 | `IDpol` escrito como `1.00E+05` | Corregir | `CAST(CAST(idpol AS REAL) AS INTEGER)` | 1 |
| Q7 | Exposición mayor a un año | Corregir | Se recorta a 1 y se marca `flag_exposure_recortada` | 1.224 |
| Q14 | Regiones sin acentos | Normalizar | Tabla `core_dim_region` con el nombre oficial y la región de 2016 | 21 regiones |
| Q6 | Siniestros repetidos | Dejar | Pueden ser reales y no hay forma de distinguirlos | 496 filas |
| Q8 | Exposición muy chica | Dejar | Son pólizas cortas reales | 6.877 |
| Q9 | `ClaimNb` extremos | Se resuelve con Q1 | El conteo ahora sale de los montos | |
| Q10 | Vehículos con 99 o 100 años | Dejar | Suponemos que es un código de "desconocido"; al agrupar por franjas quedan en la última | 48 |
| Q11 | Conductores de más de 90 años | Dejar | Es posible; quedan en la franja más alta | 401 |
| Q12 | Montos muy grandes | Dejar | No es un error; se analiza en H3 | |
| Q13 | `Area` redundante con `Density` | Dejar | Usamos una u otra | |

### La decisión más discutible: el lote de IDpol ≤ 24.500

En ese rango las 9.139 pólizas declaran siniestros, pero solo 288 tienen montos. Teníamos tres
opciones:

| Opción | Problema |
|--------|----------|
| Usar `ClaimNb` como viene | Cuenta 9.657 siniestros sin monto: la frecuencia sube y deja de ser coherente con la prima pura. |
| Recalcular el conteo desde los montos (la que elegimos) | Esas pólizas quedan casi todas con 0 siniestros, aunque declaraban alguno. |
| Borrar el lote | Perdemos 9.139 pólizas y su exposición. |

Recalculamos el conteo y además marcamos el lote, para poder comprobar si cambiaba los resultados.
Como se ve en la tabla A2 de abajo, prácticamente no los cambia.

## Antes y después

### A1. Conciliación

| Momento | Pólizas con conteo inconsistente |
|---|---:|
| Antes (`raw_`) | 9.117 |
| Después (`core_`) | 0 |

### A2. Indicadores de toda la cartera

| Versión | Pólizas | Exposición | Siniestros | Frecuencia | Prima pura |
|---|---:|---:|---:|---:|---:|
| Antes: `ClaimNb` original y exposición sin recortar | 678.013 | 358.499,4 | 36.102 | 0,1007 | 167,11 |
| Después: `core_` completa | 678.013 | 358.360,1 | 26.444 | 0,0738 | 167,18 |
| Después: sin el lote de `IDpol` ≤ 24.500 | 668.874 | 353.720,6 | 26.142 | 0,0739 | 167,54 |

Lo que muestra esta tabla:

- La frecuencia baja un 27 % (de 0,1007 a 0,0738), porque dejamos de contar siniestros sin monto.
  Visto desde el otro lado, antes estaba inflada un 36 %.
- La prima pura casi no cambia, porque depende del monto, que es el mismo. Solo varía un poco la
  exposición por el recorte de Q7.
- Ahora los números cierran entre sí. Antes, frecuencia × severidad daba 0,1007 × 2.265,51 ≈ 228,
  que no coincide con la prima pura de 167,11. Después da 0,0738 × 2.265,51 ≈ 167, que sí coincide.
- Sacar el lote no mueve la frecuencia (0,0738 contra 0,0739). Restando las filas, el lote tiene
  302 siniestros en 4.639,5 años de exposición, una frecuencia de 0,065, parecida a la del resto.

### A3. Severidad

| Momento | Siniestros | Severidad media |
|---|---:|---:|
| Antes (todos los siniestros) | 26.639 | 2.278,54 |
| Después (`core_siniestro`) | 26.444 | 2.265,51 |
| Apartados (huérfanos) | 195 | 4.044,69 |

Los siniestros huérfanos son más caros que el promedio. Al apartarlos la severidad baja un poco. Es
un costo real que la aseguradora pagó pero que no podemos asignar a ningún perfil, así que lo
declaramos como limitación.

### A5. Tipo de IDpol

En `raw_freq` el `idpol` está guardado como texto en las 678.013 filas, y en `core_poliza` como
entero en las 678.013. La fila `1.00E+05` quedó como 100000 con el resto de sus datos intactos.

### A6. Regiones

Las 21 regiones quedan con su nombre oficial y agrupadas en las 13 regiones de 2016. Grand Est queda
incompleta: tiene Alsace y Champagne-Ardenne (5.226 pólizas), pero falta Lorraine. La correspondencia
entre regiones viejas y nuevas la sacamos de la ley de reforma territorial de 2016, no del dataset.

## Controles al terminar (`src/build_core.py`)

- Pólizas: 678.013 en `raw_freq` y 678.013 en `core_poliza`.
- Siniestros: los 26.639 de `raw_sev` son los 26.444 de `core_siniestro` más los 195 huérfanos.
- Claves foráneas rotas: 0.
- Todas las restricciones `CHECK` se cumplieron (si una fila no las cumpliera, la carga fallaría).
