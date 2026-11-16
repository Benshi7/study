Acá va el panorama completo, ordenado por las etapas de la consigna.

## 1. Caso y pregunta

**Rol:** equipo de pricing de una aseguradora, que le presenta a la dirección técnica.

**Pregunta:** *¿Qué perfiles de conductor y vehículo tienen mayor costo esperado de siniestros (prima pura), y cuánto se apartan del promedio de la cartera?*

**Hipótesis para validar o refutar:**
- **H1:** los conductores jóvenes y los BonusMalus altos tienen mayor frecuencia de siniestros.
- **H2:** la densidad o la zona urbana sube la frecuencia, pero no necesariamente la severidad.
- **H3:** la severidad depende más de unos pocos siniestros grandes que del perfil del asegurado.

**Aclaración de alcance:** el dataset no trae la prima que cobra la compañía. Por eso "pricing" acá significa **prima pura técnica** (el costo esperado), no tarifa comercial ni siniestralidad real. Conviene decirlo desde la primera diapositiva.

## 2. Datos de partida

- **Frecuencia:** 678.013 filas y 12 columnas, una por póliza.
- **Severidad:** 26.639 filas y 2 columnas (IDpol y monto), una por siniestro.
- Es solo responsabilidad civil frente a terceros. El monto es la estimación más actualizada del costo de cada siniestro, es decir que incluye reservas y no solo pagos. Eso es material para la sección de limitaciones.

## 3. Enriquecimiento

La parte con más valor es **`dim_region`**. Los códigos de región parecen ser los códigos INSEE de las regiones francesas anteriores a 2016, por ejemplo 11 = Île-de-France, 82 = Rhône-Alpes y 93 = Provence-Alpes-Côte d'Azur. Hay que confirmarlo con el primer `head()`. Si se confirma, pueden:
- agregar los nombres de las regiones;
- armar una tabla de mapeo de las regiones viejas a las 13 regiones nuevas de 2016, que es una transformación SQL linda de mostrar;
- cruzar con indicadores externos por región, como población o PBI, y quizás siniestralidad vial de Eurostat a nivel NUTS2. No verifiqué la disponibilidad de esto último.

El riesgo es que no tengo documentado con precisión de qué año son los datos de freMTPL2. Elijan un año de referencia para los datos externos y declárenlo como limitación.

El resto del enriquecimiento:
- **`dim_area`:** las zonas A–F con los rangos de densidad que observen en los datos.
- **Tablas de binning:** franjas de edad, de antigüedad del vehículo y de BonusMalus.
- La marca **no** se puede enriquecer, porque viene anonimizada (B1–B14).

## 4. Modelado en Postgres

Tres capas, para que el ETL sea visible:

```
raw   → freq, sev                    (tal cual vienen, sin tocar)
core  → poliza, siniestro,           (limpias, con PK/FK)
        siniestro_huerfano,
        dim_region, dim_region_2016, dim_area, dim_franja_*
mart  → poliza_analitica             (1 fila por póliza + n_sin + costo + features)
        vw_segmento                  (agregados para Power BI)
```

- **`poliza`:** PK `idpol`.
- **`siniestro`:** PK generada por ustedes, FK `idpol`. Es la relación 1:N.
- **`siniestro_huerfano`:** guarda los siniestros sin póliza, para documentarlos en vez de perderlos.
- **`poliza_analitica`:** se construye agregando los siniestros primero y haciendo LEFT JOIN después, para evitar el fan-out que vimos antes.

## 5. Calidad y correcciones

Problemas **confirmados en fuentes**:

| Problema | Qué hacer |
|---|---|
| Las pólizas con IDpol ≤ 24500 tienen conteos de siniestros sin contraparte en severidad | Reconstruir el conteo desde `sev`, que es lo que hacen Wüthrich y Merz. Mostrar la frecuencia **antes y después**: es el momento fuerte del relato |
| Siniestros en `sev` sin póliza en `freq` | Encontrarlos con anti-join, moverlos a `siniestro_huerfano` y cuantificarlos |
| Conteos que no coinciden (una póliza con `ClaimNb = 2` y un solo siniestro) | Reportar todos los casos con una consulta de conciliación |
| `idpol` es DOUBLE en la tabla de frecuencia y BIGINT en la de severidad (en la versión de Kaggle) | Castear a entero y validar que no se pierda precisión |

Chequeos **a medir** (sospechas razonables, no hallazgos confirmados):
- `Exposure` mayor a 1 o muy cercana a 0.
- `ClaimNb` extremos.
- `ClaimAmount` en cero o negativo, y la cola pesada (definir un umbral de siniestro grande).
- Rangos: BonusMalus entre 50 y 350, DrivAge ≥ 18, VehAge con valores implausibles.
- **Consistencia Area ↔ Density:** las zonas deberían ordenarse por densidad. Si se solapan, es un hallazgo.
- Duplicados de `idpol`.

Cada problema va documentado con tres cosas: qué encontraron, cómo lo detectaron (la consulta) y qué decidieron.

## 6. ETL

1. **Extracción (Python):** bajar los CSV y cargarlos a `raw` con pandas y SQLAlchemy.
2. **Transformación (SQL):** de `raw` a `core` (casteos, conciliación, dimensiones) y de `core` a `mart`.
3. **Carga:** Power BI se conecta directo a `mart`.

Todo corre con un solo script reproducible. El diagrama del flujo es un entregable que pide la consigna, así que conviene armarlo desde el principio.

## 7. EDA en Python

- **Análisis univariado:** frecuencia ponderada por exposición, severidad media y prima pura por cada variable. Siempre mostrar la exposición al lado, porque un segmento chico con frecuencia alta puede ser ruido.
- **Relatividades:** cada segmento dividido por el promedio de la cartera. Es lo que hace que suene a tarifa.
- **Distribución de severidad** en escala log, y qué porcentaje del costo total explican los siniestros grandes (para H3).
- **Cruce edad × BonusMalus**, para mostrar la confusión entre variables.
- **Mapa regional.**
- **Plus opcional:** un GLM Poisson con offset de exposición, comparando sus relatividades con las univariadas. Si cambian, muestra concretamente por qué el análisis de una variable por vez engaña.

## 8. Dashboard en Power BI

Cuatro páginas:
1. **Cartera:** KPIs de pólizas, exposición, frecuencia, severidad media y prima pura.
2. **Perfiles de riesgo:** relatividades con segmentadores por región, edad, combustible y zona.
3. **Mapa regional.**
4. **Calidad de datos:** antes y después de las correcciones. Conecta el trabajo técnico con la visualización, que es justo lo que pide la consigna.

## 9. Arco de la exposición

1. ¿Podemos confiar en los datos? No del todo, y así lo detectamos y corregimos.
2. ¿Quién es más riesgoso?
3. ¿Cuánto debería costar cada perfil?
4. ¿Qué no podemos afirmar?

## 10. Limitaciones para declarar

- No hay fechas ni serie temporal, y el año de los datos no está documentado con precisión.
- Solo cubre RC.
- La marca está anonimizada.
- No hay prima comercial, así que no hay siniestralidad real.
- BonusMalus es endógeno: refleja siniestros pasados.
- Los montos incluyen reservas que todavía pueden desarrollarse.
- Los resultados muestran asociación, no causalidad.

## 11. Reparto sugerido

| Rol | Etapas |
|---|---|
| Datos y SQL | Modelado, DDL y consultas de conciliación |
| Calidad y ETL | Chequeos, correcciones y script del pipeline |
| Enriquecimiento | Dimensión regional y fuentes externas |
| EDA | Notebook y gráficos de relatividades |
| Power BI y relato | Dashboard y guion de la exposición |

Ajústenlo según cuántos sean. Todos tienen que poder explicar la conciliación de las dos tablas, porque es lo más probable que el docente pregunte.

¿Lo paso a un documento para compartir con el equipo? También puedo arrancar directamente con el DDL y las consultas de conciliación.