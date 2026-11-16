# 4. Consultas SQL y diagnóstico de calidad

Las consultas están en dos archivos y cada bloque tiene un código, que es el que usamos acá:

- `sql/10_exploracion.sql` (códigos E): para conocer la cartera y calcular las primeras métricas.
- `sql/11_calidad.sql` (códigos C): para buscar problemas en los datos.

Las dos corren sobre la capa `raw_`, es decir, sobre los datos sin corregir. Se ejecutan con
`python src/run_sql.py <archivo>` o abriendo el archivo en DBeaver. En este documento está el
diagnóstico; lo que hicimos con cada problema está en el documento 5.

## Qué responde cada consulta

| Código | Pregunta | Por qué la necesitábamos |
|--------|----------|--------------------------|
| E1 | ¿Cuántas filas y pólizas distintas tiene cada tabla? | Para confirmar la granularidad de cada tabla. |
| E2 | ¿Cómo se distribuye la cantidad de siniestros declarada? | Para ver cuántas pólizas no tienen siniestros. |
| E3, E4 | ¿Cómo se reparte la cartera por zona y por región? | Para saber qué segmentos tienen poco peso. |
| E5, E5b | ¿Cómo son los montos y cuánto suman los más grandes? | Es la base de la hipótesis H3. |
| E6 | Frecuencia, severidad y prima pura de toda la cartera | Para tener las métricas de referencia (y ahí apareció la diferencia de la conciliación). |
| E7 | ¿Qué pasa si se hace el JOIN sin agrupar antes? | Para mostrar el error de fan-out. |
| C1, C2 | ¿Hay nulos? ¿Hay pólizas repetidas? | Controles básicos. |
| C3 | ¿Hay siniestros repetidos? | Para decidir si había duplicados que borrar. |
| C4, C4b | ¿Hay `IDpol` mal escritos? ¿Corregirlos choca con otra póliza? | Para poder convertir el ID a entero sin errores. |
| C5, C5b | ¿Hay siniestros sin póliza? | Impiden crear la clave foránea (ver documento 3). |
| C6, C7 | ¿Coincide `ClaimNb` con los siniestros de la otra tabla? | Es la conciliación entre las dos tablas. |
| C8, C8b | ¿Dónde se concentran las inconsistencias? | Para entender el origen del problema. |
| C9, C9b | ¿Hay exposiciones fuera de lo esperable? | La exposición es el denominador de todo. |
| C10 a C12b | ¿Hay valores extremos o fuera de rango? | Para decidir qué dejar y qué corregir. |
| C13, C13b | ¿`Area` y `Density` miden lo mismo? | Para detectar variables redundantes. |
| C14 | ¿Hay variantes de escritura en las categóricas? | Para normalizar las regiones. |

## Problemas encontrados

| # | Problema | Consulta | Registros | Qué propusimos |
|---|----------|----------|----------:|----------------|
| Q1 | Pólizas que declaran siniestros (`ClaimNb` > 0) pero no tienen ninguno en la tabla de siniestros | C6, C7 | 9.116 pólizas (9.657 siniestros sin monto) | Contar los siniestros desde la tabla de siniestros y guardar el valor original. |
| Q2 | Póliza con `ClaimNb` mayor que sus siniestros, teniendo alguno | C7 | 1 | Lo mismo que Q1. |
| Q3 | Las inconsistencias se concentran en `IDpol` ≤ 24.500 | C8, C8b | 8.851 de 9.117 | Tratarlo como un problema de origen de un lote de datos. |
| Q4 | Siniestros sin póliza | C5, C5b | 195 siniestros de 6 pólizas (788.714,18 de monto) | Pasarlos a una tabla aparte. |
| Q5 | `IDpol` escrito como `1.00E+05` | C4, C4b | 1 | Convertirlo a 100000 (C4b confirma que no choca con otra póliza). |
| Q6 | Siniestros repetidos (misma póliza y mismo monto) | C3 | 241 grupos, 496 filas | No borrarlos: pueden ser siniestros reales del mismo valor. |
| Q7 | Exposición mayor a un año | C9, C9b | 1.224 (máximo 2,01) | Recortarla a 1 y marcarlo. |
| Q8 | Exposición muy chica (menos de 0,01 años, umbral nuestro) | C9 | 6.877 (mínimo 0,0027, un día) | Dejarlas: son pólizas cortas reales. |
| Q9 | `ClaimNb` extremos (5 o más en una póliza) | C10 | 9 (máximo 16) | Se resuelve con Q1. |
| Q10 | Vehículos de más de 40 años | C12, C12b | 230, de los cuales 48 tienen 99 o 100 | Suponemos que 99 y 100 significan "desconocido". Se agrupan en la franja más alta. |
| Q11 | Conductores de más de 90 años | C12 | 401 | Es posible. Se dejan en la franja más alta. |
| Q12 | Montos con cola muy pesada | E5, E5b, C11 | Máximo 4.075.400,56 contra una media de 2.278,54. Los siniestros de más de 10 veces la media son 192 (0,72 %) y suman el 35,55 % del monto. | No es un error: es lo que analiza H3. |
| Q13 | `Area` es casi `Density` en tramos | C13, C13b | Solo se solapan en los bordes (4.012 pólizas) | Usar una u otra en el análisis. |
| Q14 | Regiones con nombres sin acentos | C14 | 21 valores | Normalizarlas en una tabla de regiones. |

También hubo controles que dieron bien: no hay nulos (C1), no hay pólizas repetidas (C2), no hay
montos menores o iguales a cero (C11), no hay conductores menores de 18 ni BonusMalus fuera del rango
50 a 350 (C12) y no hay espacios de más en las categóricas (C14).

## El problema principal: las dos tablas no cierran

La frecuencia depende de contar bien los siniestros, y según qué tabla usáramos daba distinto:

| Métrica de toda la cartera (E6) | Con `ClaimNb` | Con la tabla de siniestros |
|---|---:|---:|
| Frecuencia (siniestros por año asegurado) | 0,1007 | 0,0738 |

Con `ClaimNb` la frecuencia es un 36 % más alta, porque incluye 9.657 siniestros que no tienen monto.
La prima pura (167,11) y la severidad (2.265,51) se calculan con los montos, así que no cambian.

Para entender de dónde venía la diferencia, miramos en qué rango de `IDpol` estaban las pólizas
inconsistentes (C8):

| Rango de IDpol | Pólizas | Inconsistentes | % |
|---|---:|---:|---:|
| Hasta 24.500 | 9.139 | 8.851 | 96,85 % |
| 24.501 a 1.000.000 | 77.891 | 248 | 0,32 % |
| Más de 1.000.000 | 590.983 | 18 | 0,00 % |

Dentro del primer rango (C8b), las 9.139 pólizas declaran al menos un siniestro, pero solo 288 tienen
montos. Parece un lote que se cargó distinto: solo pólizas con siniestros y sin sus montos.
Suponemos que es un problema del origen de los datos y no algo propio de esos asegurados.

Algo que notamos pero no pudimos confirmar: las 6 pólizas huérfanas tienen `IDpol` entre 2.220.367 y
2.286.775, y varias de las pólizas con `ClaimNb` extremo caen en ese mismo rango (por ejemplo la
2.241.683, con 16). Podría haber una relación, pero con estos datos no lo podemos afirmar.

## El error del fan-out (E7)

| Forma de unir | Filas | Exposición sumada |
|---|---:|---:|
| JOIN directo entre pólizas y siniestros | 679.513 | 359.515,2 |
| Agrupar los siniestros por póliza y después LEFT JOIN | 678.013 | 358.499,4 |

Con el JOIN directo aparecen 1.500 filas de más (una por cada siniestro adicional de una póliza) y se
suman 1.015,8 años de exposición que no existen. Sobre toda la cartera es poco (0,3 %), pero se
concentra en las pólizas con varios siniestros: en un análisis por segmento infla la exposición de
los perfiles más riesgosos y les baja la frecuencia. Por eso siempre agrupamos primero el lado de los
siniestros y después unimos.
