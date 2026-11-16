# 2. Recolección y comprensión de los datos

Todos los números de este documento salen de `notebooks/01_comprension.ipynb`. En esta etapa no
modificamos ningún dato: solo miramos qué teníamos.

## Fuente y formato

El dataset es freMTPL2 (French Motor Third-Party Liability), una cartera de seguros de autos de
responsabilidad civil de una aseguradora francesa que no se identifica. Es un dataset público muy
usado en el ámbito actuarial: viene en el paquete `CASdatasets` de R, y nosotros usamos la copia
publicada en Kaggle.

Son dos archivos CSV separados por comas, con encabezado y sin valores nulos.

El dataset no trae fechas. Por cómo está armado (el 99,8 % de las pólizas tiene una exposición de
un año o menos) suponemos que corresponde a un solo período anual, pero el año no está documentado.
Lo único seguro es que es anterior a 2016, porque usa las regiones francesas de antes de la reforma
de ese año.

## Granularidad y relación entre las tablas

| Archivo | Cada fila es | Filas | Columnas | IDpol distintos |
|---------|--------------|------:|---------:|----------------:|
| `freMTPL2freq.csv` | una póliza | 678.013 | 12 | 678.013 |
| `freMTPL2sev.csv` | un siniestro | 26.639 | 2 | 24.950 |

Las dos tablas se relacionan por `IDpol`. Una póliza puede tener cero, uno o varios siniestros: en la
tabla de siniestros, 23.571 pólizas aparecen una sola vez y hay una que aparece 66 veces.

## Diccionario de `freMTPL2freq.csv`

| Columna | Tipo | Descripción | Valores observados | Comentarios |
|---------|------|-------------|--------------------|-------------|
| `IDpol` | float | Identificador de la póliza | 1 a 6.114.330 | Debería ser entero. Pandas lo lee como float por una sola fila escrita `1.00E+05`. |
| `ClaimNb` | entero | Cantidad de siniestros declarados | 0 a 16, mediana 0 | El 95 % de las pólizas no tiene siniestros. |
| `Exposure` | float | Tiempo de vigencia, en años | 0,0027 a 2,01, mediana 0,49 | Hay 1.224 pólizas con más de un año. |
| `VehPower` | entero | Potencia del vehículo, en categorías | 4 a 15 | |
| `VehAge` | entero | Antigüedad del vehículo, en años | 0 a 100, mediana 6 | 230 vehículos con más de 40 años. |
| `DrivAge` | entero | Edad del conductor | 18 a 100, mediana 44 | |
| `BonusMalus` | entero | Puntaje bonus-malus (50 es el mejor nivel, más de 100 es recargo) | 50 a 230, mediana 50 | |
| `VehBrand` | texto | Marca del vehículo, anonimizada | 11 valores: B1 a B6 y B10 a B14 | No existen B7, B8 ni B9. |
| `VehGas` | texto | Combustible | Regular 345.877, Diesel 332.136 | |
| `Area` | texto | Zona según densidad, de A (rural) a F (urbana) | A a F | |
| `Density` | entero | Habitantes por km² de la comuna del conductor | 1 a 27.000, mediana 393 | Muy asimétrica: la media es 1.792. |
| `Region` | texto | Región de Francia | 21 nombres | Vienen como nombres sin acentos, no como códigos. |

## Diccionario de `freMTPL2sev.csv`

| Columna | Tipo | Descripción | Valores observados | Comentarios |
|---------|------|-------------|--------------------|-------------|
| `IDpol` | entero | Póliza a la que pertenece el siniestro | 139 a 6.113.971 | Es la clave para unir con la tabla de pólizas. |
| `ClaimAmount` | float | Costo del siniestro | 1 a 4.075.400,56, mediana 1.172, media 2.278,54 | Suponemos que está en euros. La media es mucho más alta que la mediana, señal de que hay algunos montos enormes. |

## Region: nombres, no códigos

Pensábamos que `Region` iba a venir con códigos numéricos del INSEE, pero vienen los nombres de las
regiones de antes de 2016, sin acentos y con algunas variantes como `Provence-Alpes-Cotes-D'Azur`. No
hubo que decodificarlos, pero sí normalizarlos (ver documento 5).

Francia metropolitana tenía 22 regiones antes de 2016 y en los datos aparecen 21: falta Lorraine.
Además la cartera está muy concentrada: solo `Centre` tiene 160.601 pólizas, cerca del 24 %.

## Area y Density

| Area | Density mínima | Mediana | Máxima | Pólizas |
|------|-----:|-----:|-----:|-----:|
| A | 1 | 27 | 50 | 103.957 |
| B | 50 | 72 | 100 | 75.459 |
| C | 100 | 222 | 500 | 191.880 |
| D | 500 | 1.054 | 1.993 | 151.596 |
| E | 2.001 | 3.744 | 9.850 | 137.167 |
| F | 10.008 | 27.000 | 27.000 | 17.954 |

Las zonas siguen el orden de la densidad y casi no se pisan (solo comparten los valores de borde 50,
100 y 500). `Area` parece ser la densidad agrupada en tramos, así que en el análisis conviene usar una
de las dos y no ambas como si fueran independientes.

## Primeras sospechas

En esta etapa solo las contamos. Se confirman con SQL en el documento 4.

| # | Sospecha | Cantidad |
|---|----------|---------:|
| S1 | `IDpol` en formato científico (`1.00E+05`, que por las filas vecinas sería 100000) | 1 fila |
| S2 | Siniestros cuya póliza no está en la tabla de pólizas | 195 siniestros de 6 pólizas |
| S3 | Pólizas cuyo `ClaimNb` no coincide con la cantidad de siniestros en la otra tabla | 9.117 (8.851 con `IDpol` ≤ 24.500) |
| S4 | Exposición mayor a un año | 1.224 |
| S5 | Vehículos de más de 40 años | 230 |
| S6 | Montos de siniestro extremos (máximo 4.075.400 contra una mediana de 1.172) | a medir |

Varios de estos problemas ya los comentaban otros usuarios del dataset y los pudimos confirmar con
nuestros números. Encontramos dos matices: las pólizas inconsistentes se concentran en
`IDpol` ≤ 24.500, pero no todas (quedan 266 fuera de ese rango), y el problema de tipo de `IDpol` se
debe a una única fila mal escrita.
