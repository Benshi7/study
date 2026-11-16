# Riesgos: un solo registro, con EMV y respuestas

> **Propuesta.** Se parte de los 15 riesgos del documento largo (§9.2, **se conservan sus IDs R01–R15 y sus P e I**, salvo R10, reformulado por el perfil de hogar básico: P inicial de 2 a 3) y de los 4 del documento resumido (se mapean a esos mismos IDs). Se agregan 4 riesgos: tres propios de la Opción B (R16–R18) y **R19** por la moneda (el presupuesto ahora se expresa en USD). Se agregan también las columnas que la cátedra pide: **EMV** y **respuesta** (Clase 5). Importes en USD al tipo de cambio único de `03-presupuesto`. Ningún original fue modificado.

## Qué estaba mal y cómo se arregla

| Problema | Propuesta |
|---|---|
| 15 riesgos en un documento y 4 en otro, con IDs distintos (en uno R04 es adopción de vecinos; en el otro es coordinación entre áreas) | **IDs maestros = los del documento largo.** Equivalencias: resumen R01→R01, R02→R02, R03 (alcance)→**R05**, R04 (adopción)→**R06**. En el resumen conviene eliminar la lista de 4 y remitir a la matriz completa. |
| No hay EMV; la contingencia es un 10 % plano | EMV = probabilidad × impacto en dinero (Clase 5, p31). Ver escala y totales abajo. |
| Casi todo es «Mitigar» | Se proponen respuestas variadas: Evitar (R05, R10, R15), Transferir (R18), Aceptar (R17). |
| §9.4 destaca 8 riesgos y omite otros de nivel 12 | Criterio único: se ordena por **EMV residual**. |
| §9 cita «las actividades del camino crítico del Gantt» | Ese camino **sí existe** (Excel, hoja «Dependencias y Camino Crítico»). La columna «Actividades del Gantt» (abajo) marca qué riesgos tocan actividades críticas **según el Excel**; usar la misma lista en §6 y §9 (si se adoptan las dependencias corregidas, ver `02-gantt`). |
| Faltan riesgos de la Opción B y de la moneda | R16 (las áreas no adoptan la capa), R17 (convenios con socios), R18 (dependencia de miBA, **supuesto a confirmar**), **R19** (variación del tipo de cambio ARS/USD: factor Económico del PESTEL, Clase 4 p7). |
| Privacidad de los hogares | R10 se reformula: el **perfil de hogar básico (dato mínimo declarado, opt-in)** entra en el alcance, así que la probabilidad inicial sube de 2 a 3; el marco legal queda como **«Ley 25.326, a verificar»** (no se afirma qué dice). |

Texto sugerido para la apertura de §9: *«A partir de las actividades expuestas del Gantt (sección 6, con su camino crítico) y de las interacciones con los stakeholders, identificamos y priorizamos los riesgos del proyecto.»*

## Escala de conversión a dinero (propuesta, a acordar)

El equipo usa escalas ordinales de 1 a 5. Para calcular un EMV hay que pasarlas a porcentaje y a pesos:

| Nivel | Probabilidad | Impacto (si ocurre) |
|---|---|---|
| 1 | 10 % | USD 962 (≈ ARS 1,5 M) |
| 2 | 30 % | USD 1.923 (≈ ARS 3,0 M) |
| 3 | 50 % | USD 3.846 (≈ ARS 6,0 M) |
| 4 | 70 % | USD 7.692 (≈ ARS 12,0 M) |
| 5 | 90 % | USD 16.026 (≈ ARS 25,0 M) |

Los importes son **supuestos del grupo, no datos**: ARS 1,5 / 3 / 6 / 12 / 25 M, que son ≈ 0,5 %, 1 %, 2 %, 4 % y 8 % del presupuesto base del equipo (ARS 313 M), expresados en USD con el tipo de cambio único. El registro permite cambiarlos en un solo lugar (`tools/data.py`) y recalcular todo.

## Registro consolidado (ordenado por EMV residual)

Referencias: ◆ = va a «Riesgos de alto nivel» del Charter. P×I inicial es el del equipo; P×I residual es el esperado **después** de aplicar la respuesta (propuesta a validar). EMV en USD (tipo de cambio único de `03-presupuesto`).

| ID | Riesgo | P×I inicial | Nivel | EMV inicial | Respuesta | P×I res. | EMV residual | Actividades del Gantt (¿críticas según el Excel?) | Dueño (rol) | ◆ |
|---|---|---|---|---|---|---|---|---|---|---|
| R10 | Tratamiento inadecuado de datos personales y del perfil de hogar *(reformulado)* | 3×5=15 | Alto | USD 8.013 | Evitar | 2×5 | USD 4.808 | 12, 19 (Solo con las dependencias corregidas) | Datos + Seguridad |  |
| R01 | Falta de disponibilidad de APIs o fuentes necesarias | 3×5=15 | Alto | USD 8.013 | Mitigar | 2×4 | USD 2.308 | 7, 24 (Sí) | Tecnología + Datos | ◆ |
| R02 | Baja calidad o desactualización de los datos | 4×5=20 | Crítico | USD 11.218 | Mitigar | 2×4 | USD 2.308 | 7, 24, 36 (Sí) | Datos + áreas responsables | ◆ |
| R05 | Crecimiento no controlado del alcance | 4×5=20 | Crítico | USD 11.218 | Evitar | 2×4 | USD 2.308 | 4, 10, 17 (Sí) | PM + Sponsor | ◆ |
| R08 | Problemas de rendimiento o disponibilidad | 3×5=15 | Alto | USD 8.013 | Mitigar | 2×4 | USD 2.308 | 30 (Sí) | Tecnología + Infraestructura |  |
| R04 | Falta de coordinación entre áreas | 4×4=16 | Alto | USD 5.385 | Mitigar | 3×3 | USD 1.923 | 6, 10, 17 (Sí) | Project Manager | ◆ |
| R19 | Variación del tipo de cambio ARS/USD (presupuesto expresado en USD) *(nuevo)* | 4×3=12 | Alto | USD 2.692 | Mitigar | 3×3 | USD 1.923 | 4, 18, 33 (Sí) | Sponsor + PM |  |
| R03 | Problemas de integración entre sistemas | 3×4=12 | Alto | USD 3.846 | Mitigar | 2×3 | USD 1.154 | 15, 25, 26 (Solo con las dependencias corregidas) | Tecnología |  |
| R06 | Baja participación de los vecinos | 3×3=9 | Medio | USD 1.923 | Mitigar | 2×3 | USD 1.154 | 5, 36 (Sí) | UX + Comunicación |  |
| R07 | Reportes incorrectos o maliciosos | 3×4=12 | Alto | USD 3.846 | Mitigar | 2×3 | USD 1.154 | 19, 20 (No) | Tecnología + Datos |  |
| R09 | Restricciones presupuestarias | 3×4=12 | Alto | USD 3.846 | Mitigar | 2×3 | USD 1.154 | 4, 18 (Sí) | Sponsor + PM |  |
| R11 | Demoras en desarrollo o pruebas | 3×4=12 | Alto | USD 3.846 | Mitigar | 2×3 | USD 1.154 | 18, 19, 20, 21, 31 (Sí) | PM + Tecnología |  |
| R12 | Cambios en canales digitales existentes (Boti, BAX, miBA) | 3×4=12 | Alto | USD 3.846 | Mitigar | 2×3 | USD 1.154 | 15, 25 (Solo con las dependencias corregidas) | Tecnología + responsables de canales | ◆ |
| R13 | Falta de validación de las áreas responsables | 3×4=12 | Alto | USD 3.846 | Mitigar | 2×3 | USD 1.154 | 10, 17 (Sí) | PM + áreas responsables |  |
| R14 | Fallas detectadas en las pruebas finales | 3×4=12 | Alto | USD 3.846 | Mitigar | 2×3 | USD 1.154 | 27, 28, 29, 30, 31, 32 (Sí) | QA + Tecnología |  |
| R16 | Las áreas no adoptan la capa común *(nuevo)* | 3×4=12 | Alto | USD 3.846 | Mitigar | 2×3 | USD 1.154 | 22, 36 (Sí) | Sponsor + PM |  |
| R18 | Dependencia de miBA como identidad digital (supuesto a confirmar) *(nuevo)* | 2×4=8 | Medio | USD 2.308 | Transferir | 1×4 | USD 769 | 25 (Solo con las dependencias corregidas) | Responsables de canales |  |
| R17 | Dependencia de socios y convenios (tercer lado, opcional) *(nuevo)* | 2×2=4 | Bajo | USD 577 | Aceptar | 2×2 | USD 577 | 35 (Sí) | Sponsor |  |
| R15 | Confusión entre información oficial y contenido de socios *(reformulado)* | 2×3=6 | Medio | USD 1.154 | Evitar | 1×3 | USD 385 | 38 (Sí) | PM + Comunicación |  |

**Totales:** EMV inicial USD 91.282 · **EMV residual (amenazas) USD 30.003** → es la **reserva de contingencia** propuesta (Clase 5, p30–31: los riesgos residuales alimentan el plan de contingencia; Clase 4, p19 y p20: contingencia = probabilidad × impacto). De esa suma, USD 25.580 vienen de los 15 riesgos del equipo.

**Riesgos que tocan actividades críticas** (según el Excel del equipo): R01, R02, R05, R08, R04, R19, R06, R09, R11, R13, R14, R16, R17, R15. Con las dependencias corregidas (`02-gantt`) se suman: R10, R03, R12, R18. Los de este grupo conviene vigilarlos primero: un retraso en una actividad crítica corre la fecha de cierre.

**Decisión de método a declarar (Clase 5, p32):** la diapositiva resta las oportunidades a las amenazas. Esta propuesta **no cuantifica oportunidades** y reserva solo las amenazas (postura conservadora). Si el equipo identifica oportunidades, puede restarlas (modo «neto»).

## Redacción con la plantilla de la cátedra (Clase 5, p17)

| ID | Riesgo (evento → problema → restricción afectada) | Categoría (Clase 5, p25) |
|---|---|---|
| R10 | Ante se recolectan datos innecesarios del hogar (incluido el perfil de hogar básico) o los controles de acceso son insuficientes, podría ocasionar riesgos de privacidad de los hogares, incumplimiento normativo y pérdida de confianza (marco legal a verificar: Ley 25.326), lo que impactaría en calidad y alcance. | Externo (regulatorio) |
| R01 | Ante las fuentes seleccionadas no ofrecen un mecanismo de integración o de acceso, podría ocasionar no se puede incorporar parte de la información al mapa, lo que impactaría en alcance y calidad. | Técnico |
| R02 | Ante las fuentes no tienen controles suficientes de actualización, podría ocasionar los vecinos reciben información incorrecta o vencida, lo que impactaría en calidad. | Técnico |
| R05 | Ante se agregan funcionalidades durante el desarrollo sin evaluar su impacto, podría ocasionar aumentan costos y plazos y se pierde el foco, lo que impactaría en alcance, tiempo y costo. | De dirección de proyectos |
| R08 | Ante la carga supera lo previsto o la infraestructura está mal configurada, podría ocasionar el servicio no puede usarse con normalidad, lo que impactaría en calidad. | Técnico |
| R04 | Ante las áreas tienen prioridades, tiempos o responsables distintos, podría ocasionar demoras en validaciones, información y decisiones, lo que impactaría en tiempo. | De la organización |
| R19 | Ante el tipo de cambio ARS/USD se aleja del valor usado para convertir el presupuesto, podría ocasionar los costos en pesos medidos en USD se desvían del presupuesto aprobado, lo que impactaría en costo. | Externo (económico, PESTEL) |
| R03 | Ante los sistemas difieren en formatos o arquitectura, podría ocasionar errores de intercambio y funcionalidades incompletas, lo que impactaría en tiempo y alcance. | Técnico |
| R06 | Ante el vecino no conoce o no usa la función de reportes, podría ocasionar se generan pocos reportes y validaciones colaborativas, lo que impactaría en alcance (valor entregado). | Externo |
| R07 | Ante los usuarios cargan reportes erróneos o con mala intención, podría ocasionar información poco confiable y alertas innecesarias, lo que impactaría en calidad. | Técnico |
| R09 | Ante el presupuesto resulta insuficiente o los costos aumentan, podría ocasionar se reduce el alcance o se posterga lo de menor prioridad, lo que impactaría en costo y alcance. | De la organización |
| R11 | Ante hay problemas técnicos, poca disponibilidad del equipo o correcciones mayores, podría ocasionar se retrasan hitos y la puesta en funcionamiento, lo que impactaría en tiempo. | De dirección de proyectos |
| R12 | Ante los canales cambian sus capacidades o condiciones de integración, podría ocasionar hay que rediseñar integraciones o funcionalidades, lo que impactaría en alcance y tiempo. | Externo |
| R13 | Ante las áreas demoran o no participan en las validaciones, podría ocasionar entregables incompletos o difíciles de implementar, lo que impactaría en tiempo y alcance. | De la organización |
| R14 | Ante quedan errores sin detectar en etapas anteriores, podría ocasionar se retrasa la implementación y hay retrabajo, lo que impactaría en tiempo y calidad. | Técnico |
| R16 | Ante las áreas siguen manteniendo su propio mapa en lugar de consumir la capa, podría ocasionar no se ven los costos evitados ni el uso de la capa, lo que impactaría en alcance (valor entregado). | De la organización |
| R18 | Ante la integración con BAX/Boti exige miBA y el acceso no está disponible a tiempo (a confirmar con fuentes oficiales), podría ocasionar se limita la disponibilidad multicanal, lo que impactaría en alcance y tiempo. | Externo |
| R17 | Ante los convenios con socios (Banco Ciudad, Pase Cultural, etc.) no se concretan o se demoran, podría ocasionar la capa de beneficios no está disponible en el lanzamiento, lo que impactaría en alcance (opcional). | Externo |
| R15 | Ante se incorpora contenido de socios sin diferenciarlo de lo oficial, podría ocasionar los usuarios pierden claridad sobre qué es oficial, lo que impactaría en calidad. | Externo |

## Los 5 riesgos de alto nivel para el Charter

| ID | Riesgo | EMV residual (USD) |
|---|---|---|
| R01 | Falta de disponibilidad de APIs o fuentes necesarias | USD 2.308 |
| R02 | Baja calidad o desactualización de los datos | USD 2.308 |
| R05 | Crecimiento no controlado del alcance | USD 2.308 |
| R04 | Falta de coordinación entre áreas | USD 1.923 |
| R12 | Cambios en canales digitales existentes (Boti, BAX, miBA) | USD 1.154 |

Criterio: los de mayor nivel inicial o EMV que además son los que el propio equipo ya había destacado en §9.4 (R01, R02, R04, R05) más R12 (canales digitales, clave para la Opción B). Todos están en el registro.

## Para la defensa

- *«¿De dónde sale la contingencia?»* → de la suma de los EMV residuales: USD 30.003.
- *«¿Y si los importes de impacto fueran otros?»* → ver la sensibilidad en `03-presupuesto`: con la escala a la mitad la contingencia sería USD 15.002; con la escala ×1,5, USD 45.005. Con el dólar ±20 % cambia el total en USD (cuadro de `03-presupuesto`), no los pesos.
- Los riesgos R16–R19 y el EMV de cada fila son **propuestas**: ninguno proviene de datos del proyecto.
