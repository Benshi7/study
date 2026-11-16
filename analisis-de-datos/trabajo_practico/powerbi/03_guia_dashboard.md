# Guía para armar el dashboard

Cuatro páginas que siguen el hilo de la presentación. Cada página responde **una pregunta**
y se conecta con una hipótesis del caso (`docs/01_caso.md`).

| Página | Pregunta | Hipótesis |
|---|---|---|
| 1 · Cartera | ¿Cómo es la cartera y cuánto pesan los siniestros grandes? | H3 |
| 2 · Perfiles | ¿Quién cuesta más, y cuánto se aparta del promedio? | H1, H2 |
| 3 · Mapa | ¿Dónde cuesta más? | H2 (zona) |
| 4 · Calidad | ¿Podemos confiar en los datos? | Acto 1 |

## 0. Preparación (15 min)

1. Correr `python src/etl.py`: deja en `export/` los 7 CSV que usa el dashboard.
2. Power BI Desktop → **Transformar datos** → crear el parámetro `RutaDatos` y las consultas de
   `01_power_query.m` (están tipadas: `franja_bm` y `franja_vehage` como texto, decimales en `en-US`).
3. Cerrar y aplicar. Pegar las medidas de `02_medidas.dax`.
4. Vista > Temas > Examinar temas > `tema_tp.json`.

### Modelo (vista Modelo)

| Relación | Tipo | Nota |
|---|---|---|
| `dim_region[region_2016]` → `polizas[region_2016]` | uno a muchos | Para el mapa (latitud/longitud) |
| `siniestros[idpol]` → `polizas[idpol]` | muchos a uno, filtro hacia siniestros | **Solo** si usan el tope dinámico opcional |
| `parametros`, `pareto`, `calidad_*` | sin relación | Tablas sueltas, se usan solo en tarjetas y gráficos propios |

### Ajustes de columnas (vista Datos)

- `polizas[vehbrand]` → **Ordenar por columna** → `vehbrand_orden`.
- `polizas[exposure]`, `monto`, `monto_topeado` → **Resumen: no resumir** (todo se calcula con medidas).
- Ocultar las columnas de flags y `claimnb_declarado` salvo en la página 4.

## 1. Página «Cartera» — ¿Cómo es la cartera?

```
┌──────────────────────────────────────────────────────────────┐
│ Título: "La cartera en una mirada"                            │
│ [Pólizas] [Exposición] [Frecuencia] [Severidad c/tope] [Prima pura c/tope] │
│ ┌───────────────────────────┐ ┌────────────────────────────┐ │
│ │ Pareto: % siniestros vs   │ │ Frecuencia (columnas) y    │ │
│ │ % monto acumulado         │ │ severidad c/tope (línea)   │ │
│ │ (línea, tabla `pareto`)   │ │ por Zona (area)            │ │
│ └───────────────────────────┘ └────────────────────────────┘ │
│ Texto: "El 1 % de los siniestros explica el 38 % del costo"  │
│ Segmentadores (arriba): Zona, Combustible, Antigüedad vehículo │
└──────────────────────────────────────────────────────────────┘
```

| Visual | Campos |
|---|---|
| 5 tarjetas | `[Pólizas]`, `[Exposición]`, `[Frecuencia]`, `[Severidad con tope]`, `[Prima pura con tope]` |
| Gráfico de líneas (Pareto) | Eje X `pareto[pct_siniestros]`, Y `pareto[pct_monto_acum]` (sin resumir). Agregar línea de referencia en X = 0,01 |
| Columnas y líneas | Eje `polizas[area]`; columnas `[Frecuencia]`; línea `[Severidad con tope]` |
| Tarjeta pequeña | `[% monto recortado]` con el texto «el tope p99 recorta el 30,7 % del monto» |

**Lectura (H2 y H3):** la frecuencia sube de la zona A a la E/F; la severidad no acompaña. El 1 % de los siniestros pesa el 38 %.

## 2. Página «Perfiles» — ¿Quién cuesta más?

```
┌──────────────────────────────────────────────────────────────┐
│ Segmentadores: Zona · Combustible · Antigüedad · Potencia    │
│ ┌──────────────────────┐ ┌───────────────────────────────┐  │
│ │ Rel. prima pura (tope)│ │ Rel. prima pura (tope)       │  │
│ │ por franja_edad (barras)│ │ por franja_bm (barras)     │  │
│ └──────────────────────┘ └───────────────────────────────┘  │
│ ┌───────────────────────────────────────────────────────┐   │
│ │ Matriz edad × BonusMalus, valor [Frecuencia], escala  │   │
│ │ de color (la ventaja de edad se achica a igual BM)    │   │
│ └───────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

| Visual | Campos |
|---|---|
| Barras por edad | Eje `franja_edad`; valor `[Rel. prima pura (tope)]`; tooltip `[% exposición]`, `[Aviso muestra]`; color por regla = campo `[Color relatividad]` |
| Barras por BonusMalus | Igual, con `franja_bm` |
| Matriz | Filas `franja_edad`, columnas `franja_bm`, valores `[Frecuencia]`, formato condicional de fondo (escala) |
| Línea de referencia | En cada gráfico de barras, línea constante en **1,0** («promedio de la cartera») |
| Opcional | Una tercera tarjeta con el segmentador «Tope» (ver tope dinámico) |

**Lectura (H1):** 18–21 años ≈ 3,6×, recargo (101+) ≈ 4,9×. Con el mismo BonusMalus la ventaja de edad se achica: edad y BonusMalus se mezclan.
**Ojo:** 18–21 es el 1,2 % de la exposición y 101+ el 1,0 %; la medida `[Aviso muestra]` lo muestra en el tooltip.

## 3. Página «Mapa» — ¿Dónde cuesta más?

> Si el mapa aparece bloqueado al abrir el `.pbix`, ver `LEEME_MAPA.txt` (es una opción de Power BI Desktop en cada computadora).

| Visual | Campos |
|---|---|
| Mapa de burbujas (Azure Maps o Mapa) | Latitud `dim_region[latitud]`, longitud `dim_region[longitud]`, ubicación/leyenda `dim_region[region_2016]`, tamaño `[Exposición]`, color `[Rel. prima pura (tope)]` |
| Barras ordenadas | Eje `polizas[region_2016]`, valor `[Rel. prima pura (tope)]`, ordenado de mayor a menor |
| Tabla | `region_2016`, `[% exposición]`, `[Frecuencia]`, `[Prima pura con tope]` |

- Se usan **latitud/longitud** y no los nombres: Power BI a veces geocodifica mal las regiones francesas.
  Las coordenadas de `dim_region.csv` son **centros aproximados** de cada región, sirven para burbujas y no para fronteras.
- **Avisos que tienen que ir escritos en la página:**
  - *Grand Est* está incompleta (falta Lorraine; ver A6 en `docs/05_limpieza.md`).
  - *Centre-Val de Loire* tiene ≈ 29 % de la exposición: la cartera no es representativa de toda Francia.
  - El mapa de regiones 2016 es un **dato externo** (reforma territorial de 2016).

## 4. Página «Calidad» — ¿Podemos confiar en los datos?

| Visual | Campos |
|---|---|
| Tarjetas | `[Pólizas con conteo corregido]` (9.117), `[Pólizas del lote bajo]` (9.139), `[Pólizas con exposición recortada]` (1.224) |
| Columnas agrupadas | `calidad_antes_despues[version]` × `frecuencia_version` (0,1007 → 0,0738 → 0,0739) |
| Tarjeta | `[Variación frecuencia]` (≈ −27 %) |
| Tabla | `calidad_hallazgos`: `codigo`, `problema`, `accion`, `registros`; formato condicional por `accion` |
| Texto | «195 siniestros sin póliza (más caros que el promedio): no se pueden asignar a un perfil» |

**Lectura:** de 14 problemas, 5 se corrigieron o normalizaron (Q1, Q2, Q5, Q7, Q14), 2 se marcaron o apartaron (Q3, Q4), 1 se resolvió con otra corrección (Q9) y 6 se dejaron y se declaran como límite.

## 5. Opcional: tope dinámico

El tope fijo (p99) ya viene en la columna `monto_topeado`. Si quieren que la dirección lo cambie en vivo:
parámetro numérico «Tope» + relación `siniestros → polizas` + medida `[Prima pura (tope elegido)]` (al final de `02_medidas.dax`).
Es un plus para la exposición, no un requisito.

## 6. Cómo comprobar que quedó bien

`valores_esperados.csv` tiene, calculado en pandas desde los mismos CSV, el valor correcto de cada medida por segmento. Chequeos rápidos:

| Medida (sin segmentadores) | Esperado |
|---|---:|
| `[Pólizas]` | 678.013 |
| `[Exposición]` | 358.360,1 |
| `[Total siniestros]` | 26.444 |
| `[Frecuencia]` | 0,0738 |
| `[Severidad]` | 2.265,51 |
| `[Prima pura]` | 167,18 |
| `[Prima pura con tope]` | 115,79 |
| `[% monto recortado]` | 30,7 % |

Y por segmento: `Rel. prima pura (tope)` de `18-21` = 3,56; de `101+` = 4,92; zona `E` = 1,36; zona `A` = 0,72.
Si da otra cosa, lo más probable es que los decimales se hayan leído mal (falta la cultura `en-US`) o que una columna esté en «Promedio» y no en «Suma».

## 7. Para la exposición oral

Mostrar el dashboard **en vivo**, no capturas: elegir un segmentador (ej. Combustible = Diesel) y ver cómo cambian las relatividades.
Decir en cada página qué pregunta responde y qué hipótesis confirma. Cerrar la página 4 con los límites que ya están en la slide 17.
