# 9. Gestión de riesgos - Matriz de riesgos

A partir del análisis de las actividades del camino crítico del Gantt y de las interacciones con los stakeholders cuya gestión definimos en la matriz y en el plan de comunicación, identificamos y priorizamos los riesgos del proyecto. Una comunicación oportuna es también una respuesta a riesgos como la falta de coordinación entre áreas (R04) o la baja participación de los vecinos (R06).

La gestión de riesgos tiene como objetivo identificar, analizar y controlar aquellos eventos que podrían afectar el alcance, cronograma, costos, calidad o implementación del proyecto de modernización del Mapa Interactivo de la Ciudad.

La gestión se realizará durante todo el ciclo de vida del proyecto, con especial atención a las etapas de análisis, integración, desarrollo y pruebas. Los riesgos identificados serán revisados periódicamente y podrán incorporarse nuevos riesgos a medida que avance el proyecto.

## 9.1 Metodología de evaluación

Para evaluar los riesgos se utilizarán dos variables principales:

**Probabilidad:** representa la posibilidad de que ocurra el riesgo.

- 1 = Muy baja

- 2 = Baja

- 3 = Media

- 4 = Alta

- 5 = Muy alta

**Impacto:** representa el efecto que tendría el riesgo sobre los objetivos del proyecto.

- 1 = Muy bajo

- 2 = Bajo

- 3 = Medio

- 4 = Alto

- 5 = Muy alto

El nivel de riesgo se obtiene mediante la siguiente fórmula:

**Nivel de riesgo = Probabilidad × Impacto**

La clasificación utilizada será:

| **Puntaje** | **Nivel** |
|---|---|
| 1–4 | Bajo |
| 5–9 | Medio |
| 10–16 | Alto |
| 17–25 | Crítico |

Los riesgos de nivel alto y crítico tendrán prioridad de seguimiento y deberán contar con acciones preventivas y planes de contingencia definidos.

## 9.2 Matriz de riesgos

| **ID** | **Riesgo** | **Causa** | **Consecuencia** | **Prob.** | **Impacto** | **Nivel** | **Respuesta** | **Responsable** |
|---|---|---|---|---|---|---|---|---|
| R01 | Falta de disponibilidad de APIs o fuentes necesarias | Las fuentes seleccionadas no cuentan con mecanismos adecuados de integración o acceso | No se puede incorporar determinada información al mapa | 3 | 5 | 15 - Alto | Mitigar | Tecnología + Datos |
| R02 | Baja calidad o desactualización de los datos | Las fuentes no poseen controles suficientes de actualización | Los usuarios podrían recibir información incorrecta o desactualizada | 4 | 5 | 20 - Crítico | Mitigar | Datos + áreas responsables |
| R03 | Problemas de integración entre sistemas | Diferencias técnicas, formatos o arquitecturas entre sistemas | Retrasos, errores de intercambio o funcionalidades incompletas | 3 | 4 | 12 - Alto | Mitigar | Tecnología |
| R04 | Falta de coordinación entre áreas | Diferentes prioridades, tiempos o responsables institucionales | Retrasos en validaciones, información y decisiones | 4 | 4 | 16 - Alto | Mitigar | Responsable del proyecto |
| R05 | Crecimiento no controlado del alcance | Incorporación de nuevas funcionalidades durante el desarrollo | Aumento de costos y plazos y pérdida de foco del proyecto | 4 | 5 | 20 - Crítico | Evitar / Mitigar | PM + Sponsor |
| R06 | Baja participación de los vecinos | Poco conocimiento de la funcionalidad o baja adopción | Menor cantidad de reportes y validaciones colaborativas | 3 | 3 | 9 - Medio | Mitigar | UX + Comunicación |
| R07 | Reportes incorrectos o maliciosos | Errores de los usuarios o uso inadecuado del sistema | Información incorrecta o generación de alertas innecesarias | 3 | 4 | 12 - Alto | Mitigar | Tecnología + Datos |
| R08 | Problemas de rendimiento o disponibilidad | Carga elevada, errores de infraestructura o configuración insuficiente | Dificultad o imposibilidad de utilizar el servicio | 3 | 5 | 15 - Alto | Mitigar | Tecnología + Infraestructura |
| R09 | Restricciones presupuestarias | Presupuesto insuficiente o aumento de costos | Reducción del alcance, retrasos o necesidad de priorización | 3 | 4 | 12 - Alto | Mitigar | Sponsor + PM |
| R10 | Tratamiento inadecuado de datos de usuarios | Recolección de información innecesaria o controles insuficientes | Riesgos de privacidad, incumplimientos y pérdida de confianza | 2 | 5 | 10 - Alto | Evitar / Mitigar | Datos + Seguridad |
| R11 | Demoras en desarrollo o pruebas | Problemas técnicos, disponibilidad limitada del equipo o correcciones mayores | Retraso de hitos y de la puesta en funcionamiento | 3 | 4 | 12 - Alto | Mitigar | PM + Tecnología |
| R12 | Cambios en canales digitales existentes | Modificaciones en capacidades o condiciones de integración de los canales seleccionados | Necesidad de rediseñar integraciones o funcionalidades | 3 | 4 | 12 - Alto | Mitigar | Tecnología + responsables de canales |
| R13 | Falta de validación de las áreas responsables | Demoras o ausencia de participación de las áreas | Entregables incompletos o dificultades para implementar la solución | 3 | 4 | 12 - Alto | Mitigar | PM + áreas responsables |
| R14 | Fallas detectadas durante las pruebas finales | Errores no identificados en etapas anteriores | Retraso de la implementación y necesidad de retrabajo | 3 | 4 | 12 - Alto | Mitigar | QA + Tecnología |
| R15 | Confusión entre información oficial y contenidos comerciales futuros; baja adopción por parte de comercios | Incorporación de servicios patrocinados sin diferenciación suficiente, o escasa adhesión de los comercios al modelo comercial | Pérdida de claridad para los usuarios y menores ingresos por servicios patrocinados | 2 | 3 | 6 - Medio | Aceptar | PM + Comunicación |

## 9.3 Acciones preventivas y planes de contingencia

Para los principales riesgos identificados se establecen las siguientes acciones:

| **ID** | **Acción preventiva** | **Plan de contingencia** |
|---|---|---|
| R01 | Realizar el relevamiento de APIs y fuentes durante la etapa de Análisis y validar su factibilidad antes del desarrollo | Utilizar una fuente alternativa o limitar temporalmente la funcionalidad asociada |
| R02 | Definir responsables de cada fuente, frecuencia de actualización y controles de calidad | Identificar la fuente afectada, informar la limitación y suspender temporalmente la publicación de datos no confiables |
| R03 | Diseñar las integraciones previamente y realizar pruebas técnicas tempranas | Implementar la integración por etapas y priorizar las fuentes críticas |
| R04 | Establecer responsables y reuniones de seguimiento entre áreas | Elevar los bloqueos al PM y, cuando corresponda, al Sponsor para resolución |
| R05 | Aplicar control formal de cambios y evaluar impacto antes de aprobar nuevas funcionalidades | Postergar funcionalidades no críticas para una etapa posterior |
| R06 | Realizar comunicación clara sobre la utilidad del sistema y facilitar la participación | Ajustar mecanismos de participación y reforzar la comunicación a usuarios |
| R07 | Incorporar validaciones, criterios de consistencia y mecanismos para detectar reportes anómalos | Revisar, ocultar o invalidar reportes que no cumplan los criterios establecidos |
| R08 | Realizar pruebas de rendimiento, monitoreo y controles de infraestructura | Escalar recursos, limitar funcionalidades no críticas o activar procedimientos de recuperación |
| R09 | Realizar seguimiento periódico del presupuesto y priorización de funcionalidades | Reprogramar actividades o postergar funcionalidades de menor prioridad |
| R10 | Aplicar criterios de minimización de datos, controles de acceso y revisión de los datos recolectados | Restringir el tratamiento afectado, corregir la configuración y activar el procedimiento correspondiente |
| R11 | Establecer seguimiento semanal del desarrollo y pruebas | Repriorizar tareas, reasignar recursos o ajustar actividades no críticas |
| R12 | Validar las capacidades de los canales antes de desarrollar las integraciones | Adaptar la integración o utilizar otro canal previsto dentro del alcance |
| R13 | Definir responsables por área y fechas de validación | Escalar los bloqueos y reprogramar la actividad afectada |
| R14 | Ejecutar pruebas progresivas durante las etapas de desarrollo e integración | Corregir los defectos y repetir las pruebas antes de autorizar la implementación |
| R15 | Sin acción proactiva en esta etapa (estrategia Aceptar): se monitorea. Si se incorpora contenido comercial en una fase futura, se definen reglas claras para diferenciarlo del contenido oficial y se valida la aceptación del modelo comercial antes de incorporarlo | Suspender la publicación del contenido comercial que genere confusión |

## 9.4 Priorización de riesgos

Para priorizar se usa el mapa de calor de riesgos, que cruza la probabilidad y el impacto de cada riesgo de la matriz (9.2) y lo ubica en una de tres zonas: **aceptable**, **aceptable con atención** e **inaceptable**.

Tabla: Mapa de calor de riesgos (zona según probabilidad e impacto)

| **Probabilidad \ Impacto** | **1 - Muy bajo** | **2 - Bajo** | **3 - Medio** | **4 - Alto** | **5 - Muy alto** |
|---|---|---|---|---|---|
| **5 - Muy alta** | Aceptable | Con atención | Inaceptable | Inaceptable | Inaceptable |
| **4 - Alta** | Aceptable | Con atención | Con atención | Inaceptable | Inaceptable |
| **3 - Media** | Aceptable | Aceptable | Con atención | Con atención | Inaceptable |
| **2 - Baja** | Aceptable | Aceptable | Aceptable | Con atención | Inaceptable |
| **1 - Muy baja** | Aceptable | Aceptable | Aceptable | Con atención | Con atención |

Aplicado a los 15 riesgos de la matriz, el resultado es el siguiente:

![Mapa de calor de riesgos: ubicación de R01 a R15 según probabilidad e impacto](img/mapa-calor.png)

- **Zona inaceptable (6 riesgos).** Requieren una respuesta activa y seguimiento en cada reunión de control, durante los hitos de aprobación (punto 9.5).
  - **R02 - Baja calidad o desactualización de los datos:** probabilidad 4, impacto 5 (nivel crítico).
  - **R05 - Crecimiento no controlado del alcance:** probabilidad 4, impacto 5 (nivel crítico).
  - **R04 - Falta de coordinación entre áreas:** probabilidad 4, impacto 4 (nivel alto).
  - **R01 - Falta de disponibilidad de APIs o fuentes necesarias:** probabilidad 3, impacto 5 (nivel alto).
  - **R08 - Problemas de rendimiento o disponibilidad:** probabilidad 3, impacto 5 (nivel alto).
  - **R10 - Tratamiento inadecuado de datos de usuarios:** probabilidad 2, impacto 5 (nivel alto). Aunque su probabilidad es baja, su impacto es muy alto.

- **Zona aceptable con atención (8 riesgos).** Se mitigan con las acciones preventivas del punto 9.3 y tienen un seguimiento periódico de la matriz.
  - **R03 - Problemas de integración entre sistemas.**
  - **R06 - Baja participación de los vecinos.**
  - **R07 - Reportes incorrectos o maliciosos.**
  - **R09 - Restricciones presupuestarias.**
  - **R11 - Demoras en desarrollo o pruebas.**
  - **R12 - Cambios en canales digitales existentes.**
  - **R13 - Falta de validación de las áreas responsables.**
  - **R14 - Fallas detectadas durante las pruebas finales.**

- **Zona aceptable (1 riesgo).** Su probabilidad y su impacto son bajos, por lo que el costo de mitigarlo no se justifica en esta etapa. Se adopta la estrategia **Aceptar**, con monitoreo.
  - **R15 - Confusión entre información oficial y contenidos comerciales futuros; baja adopción por parte de comercios:** probabilidad 2, impacto 3 (nivel medio). Mantiene su plan de contingencia: suspender la publicación del contenido comercial que genere confusión.

Los riesgos de la zona inaceptable deberán recibir seguimiento prioritario durante las reuniones de control del proyecto.

## 9.5 Seguimiento y actualización de la matriz

La matriz de riesgos será revisada periódicamente por el responsable del proyecto y actualizada cuando se identifiquen nuevos riesgos, cambie la probabilidad o el impacto de un riesgo existente o se modifique el contexto del proyecto.

El seguimiento se realizará principalmente durante los hitos de aprobación definidos en el cronograma:

- aprobación del Project Charter;

- aprobación de requerimientos;

- aprobación del diseño;

- finalización del desarrollo;

- validación de integraciones;

- aprobación de pruebas;

- puesta en funcionamiento;

- cierre del proyecto.

Cuando un riesgo se materialice, dejará de ser tratado únicamente como riesgo y pasará a gestionarse como un problema o incidente del proyecto, registrando las acciones realizadas y su impacto.

## 9.6 Criterios de control

La gestión de riesgos deberá mantenerse alineada con el alcance, cronograma, presupuesto y criterios de aceptación definidos en el Project Charter.

Cualquier riesgo que pueda producir un cambio significativo en alguno de estos elementos deberá ser comunicado al responsable del proyecto y, cuando corresponda, al Sponsor para evaluar las acciones necesarias.

La matriz constituye un instrumento de seguimiento durante todo el proyecto y no un documento estático. Su finalidad es anticipar situaciones que puedan afectar los objetivos y establecer respuestas antes de que los riesgos se materialicen.

## 9.7 Cuantificación de los riesgos y reserva de contingencia

La matriz del punto 9.2 califica cada riesgo con escalas ordinales. Para dimensionar la reserva de contingencia del presupuesto (punto 10.8) se convierten esas escalas a valores monetarios y se calcula el **valor monetario esperado (EMV)** de cada riesgo: **EMV = probabilidad × impacto**, con el impacto expresado en USD. La suma de los EMV residuales es la reserva de contingencia. Es el mismo criterio del ejemplo de la cátedra: probabilidad de ocurrencia × aumento de costo × gasto afectado.

### 9.7.1 Conversión de las escalas

Tabla: Conversión de la escala 1–5 a probabilidad e impacto en USD

| **Nivel** | **Probabilidad** | **Impacto si ocurre (USD)** |
|---|---|---|
| 1 - Muy bajo | 10 % | hasta 1.000 |
| 2 - Bajo | 30 % | de 1.000 a 3.000 |
| 3 - Medio | 50 % | de 3.000 a 6.000 |
| 4 - Alto | 70 % | de 6.000 a 10.000 |
| 5 - Muy alto | 90 % | más de 10.000 |

Los porcentajes de probabilidad y las bandas de impacto son supuestos de planificación del equipo, a validar. Las bandas equivalen aproximadamente al 0,5 %, 1,5 %, 3 % y 5 % del presupuesto base de costos (USD 200.633).

### 9.7.2 Impacto en USD de cada riesgo

El impacto de cada riesgo se calcula con los rubros del presupuesto del punto 10 y con dos referencias comunes. La primera es el **costo semanal del equipo**, USD 4.833: los recursos humanos (USD 121.790) divididos en 25,2 semanas, equivalentes a los 126 días hábiles del camino crítico; se usa para valorar los retrasos. La segunda son los costos mensuales por perfil del punto 10.2. Son importes de planificación: no incluyen sanciones, daño reputacional ni lucro cesante.

Tabla: Impacto en USD de cada riesgo si se materializa

| **Riesgo** | **Nivel de impacto** | **Qué ocurre si se materializa** | **Cálculo** | **Monto (USD)** |
|---|---|---|---|---|
| R01 | 5 | Una fuente no está disponible: se busca una fuente alternativa y se retrasa la integración | 2 semanas × USD 4.833 + 30 % del rubro Datos, GIS e integraciones (USD 11.538) | USD 13.127 |
| R02 | 5 | Se detectan datos erróneos tarde: se reprocesan y se revalidan con las áreas | 2 semanas × USD 4.833 + 100 % de preparación y normalización de datos (USD 3.205) | USD 12.871 |
| R03 | 4 | Los sistemas son incompatibles: se ajusta la integración por etapas | 1 semana × USD 4.833 + 20 % del rubro Datos, GIS e integraciones (USD 11.538) | USD 7.141 |
| R04 | 4 | Las áreas demoran decisiones y validaciones | 1,5 semanas × USD 4.833 | USD 7.250 |
| R05 | 5 | Crece el alcance: se agrega trabajo de desarrollo, datos y UX/UI | 20 % de los costos de desarrolladores, datos y GIS, y UX/UI (USD 25.640 + 20.512 + 7.692) | USD 10.769 |
| R06 | 3 | Baja participación: se rediseña la experiencia y se refuerzan los materiales | 1 mes de UX/UI (USD 3.846) + 100 % de materiales y documentación operativa (USD 1.282) | USD 5.128 |
| R07 | 4 | Reportes maliciosos: se refuerzan las validaciones y la moderación | 25 % del costo de desarrolladores (USD 25.640) | USD 6.410 |
| R08 | 5 | Problemas de rendimiento: se escala y reconfigura la infraestructura | 50 % del rubro Infraestructura y seguridad (USD 19.230) + 1 mes de infraestructura/DevOps (USD 5.128) | USD 14.743 |
| R09 | 4 | Aumentan los costos tecnológicos, por ejemplo por el tipo de cambio | 15 % de Desarrollo y tecnología más Infraestructura y seguridad (USD 22.435 + 19.230) | USD 6.250 |
| R10 | 5 | Datos de usuarios mal tratados: se corrigen controles y se retrasa el avance | 1 mes de seguridad informática (USD 5.128) + 2 semanas × USD 4.833 | USD 14.794 |
| R11 | 4 | Demoras en desarrollo o pruebas retrasan los hitos | 1,5 semanas × USD 4.833 | USD 7.250 |
| R12 | 4 | Un canal cambia sus condiciones: se rediseñan las integraciones | 1 semana × USD 4.833 + 30 % del rubro Datos, GIS e integraciones (USD 11.538) | USD 8.294 |
| R13 | 4 | Las áreas no validan a tiempo: se reprograman entregables | 1,5 semanas × USD 4.833 | USD 7.250 |
| R14 | 4 | Fallas en las pruebas finales: retrabajo y retraso | 15 % del costo de desarrolladores (USD 25.640) + 1 semana × USD 4.833 | USD 8.679 |
| R15 | 3 | Contenido comercial confuso: se rediseña la diferenciación con lo oficial | 1 mes de UX/UI (USD 3.846) | USD 3.846 |

Los importes son coherentes con la escala de impacto de la matriz: todos caen en la banda de su nivel (nivel 3, entre USD 3.000 y 6.000; nivel 4, entre USD 6.000 y 10.000; nivel 5, más de USD 10.000), de modo que ningún riesgo de impacto 5 tiene un importe menor que uno de impacto 4.

### 9.7.3 Efecto de la respuesta y EMV

La reserva de contingencia cubre el **riesgo residual**, es decir, el que queda después de aplicar la respuesta planificada. Las acciones preventivas del punto 9.3 (relevamiento de fuentes, pruebas progresivas, monitoreo, control formal de cambios) ya están financiadas en las dedicaciones del presupuesto base. Como criterio de planificación, una respuesta **Mitigar** reduce la probabilidad en un nivel y una respuesta **Evitar / Mitigar** la reduce en dos niveles, con un mínimo de nivel 1. Una respuesta **Aceptar** no reduce la probabilidad: el riesgo se asume con su probabilidad inicial. El impacto no cambia.

Tabla: EMV inicial y residual de cada riesgo

| **Riesgo** | **Respuesta** | **Prob. inicial** | **Prob. residual** | **Impacto (USD)** | **EMV inicial (USD)** | **EMV residual (USD)** |
|---|---|---|---|---|---|---|
| R01 | Mitigar | 50 % | 30 % | USD 13.127 | USD 6.564 | USD 3.938 |
| R02 | Mitigar | 70 % | 50 % | USD 12.871 | USD 9.010 | USD 6.436 |
| R03 | Mitigar | 50 % | 30 % | USD 7.141 | USD 3.571 | USD 2.142 |
| R04 | Mitigar | 70 % | 50 % | USD 7.250 | USD 5.075 | USD 3.625 |
| R05 | Evitar / Mitigar | 70 % | 30 % | USD 10.769 | USD 7.538 | USD 3.231 |
| R06 | Mitigar | 50 % | 30 % | USD 5.128 | USD 2.564 | USD 1.538 |
| R07 | Mitigar | 50 % | 30 % | USD 6.410 | USD 3.205 | USD 1.923 |
| R08 | Mitigar | 50 % | 30 % | USD 14.743 | USD 7.372 | USD 4.423 |
| R09 | Mitigar | 50 % | 30 % | USD 6.250 | USD 3.125 | USD 1.875 |
| R10 | Evitar / Mitigar | 30 % | 10 % | USD 14.794 | USD 4.438 | USD 1.479 |
| R11 | Mitigar | 50 % | 30 % | USD 7.250 | USD 3.625 | USD 2.175 |
| R12 | Mitigar | 50 % | 30 % | USD 8.294 | USD 4.147 | USD 2.488 |
| R13 | Mitigar | 50 % | 30 % | USD 7.250 | USD 3.625 | USD 2.175 |
| R14 | Mitigar | 50 % | 30 % | USD 8.679 | USD 4.340 | USD 2.604 |
| R15 | Aceptar | 30 % | 30 % | USD 3.846 | USD 1.154 | USD 1.154 |
| **Total** |  |  |  |  | **USD 69.353** | **USD 41.206** |

La suma de los EMV residuales, **USD 41.206**, es la reserva de contingencia del proyecto (punto 10.8). Representa el 20,5 % del presupuesto base de costos: es un resultado del cálculo, no una regla. Sin considerar el efecto de las respuestas, el EMV inicial sería de USD 69.353. Los riesgos con mayor EMV residual son R02 (USD 6.436), R08 (USD 4.423), R01 (USD 3.938), R04 (USD 3.625) y R05 (USD 3.231).

La reserva cubre solamente los riesgos identificados en esta matriz y suma sus EMV como si fueran independientes. Los eventos no identificados corresponden a la reserva de gestión (punto 10.8). Los EMV se recalculan cuando se actualicen la probabilidad o el impacto de un riesgo, durante los hitos de control (punto 9.5).
