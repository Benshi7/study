# Gantt: el Excel ya tiene lo que pide la cátedra; ajustes puntuales

> **Corrección importante.** Nuestro análisis anterior dijo que el Gantt «no tenía duraciones, dependencias ni camino crítico». Eso era cierto **solo para la imagen del documento Word**. El **Excel del equipo (Anexo del punto 6)** sí los trae: 40 actividades con duración en días hábiles, dependencias, holguras, camino crítico (CPM) y 8 hitos. Esta página **toma ese Excel como base** y ya no propone reemplazarlo: propone ajustes puntuales. Ningún original fue modificado. Archivo de datos: `schedule.csv`; diagrama: `gantt.svg`.

## Lo que ya está bien

- **40 actividades, 8 fases, 8 hitos** con fechas. Los 8 hitos del Excel son **idénticos** a los del Charter (§6.3) y a los gates del documento resumido: ninguna fecha de hito cambia.
- **Cada duración coincide con las fechas:** para las 40 actividades, el rango Inicio–Fin tiene exactamente esa cantidad de días hábiles (lunes a viernes).
- **El cálculo CPM de la hoja «Dependencias y Camino Crítico» es correcto** si «a-b» se lee como *los dos extremos*: recalculado por separado, da **126 días hábiles, 23 actividades críticas y las mismas holguras que la hoja, sin ninguna diferencia**. El propio Anexo lo confirma: escribe «1, 3» donde el cronograma dice «1-3».
- **La nota del Anexo sobre PERT es correcta** (CPM con una duración por actividad; no inventaron estimaciones de tres puntos). Ver el punto 7 por si preguntan.

## Qué ajustar (en orden de importancia)

### 1 · La notación «a-b» es ambigua y cambia el resultado

«1-3» puede leerse como {1, 2, 3} o como {1, 3}. La hoja del equipo usa la segunda; si alguien la lee como rango, el CPM da **129 días hábiles** (no 126), cambian **17 holguras** y **5 marcas de «crítica»** (actividades 25, 26, 27, 28, 30). Se afecta solo donde el guion cubre tres o más números: actividades 4, 8, 9, 15, 16, 17, 27, 31, 39, 40.

**Arreglo (sin cambiar fechas):** escribir listas explícitas («1, 2, 3») en todas las celdas, como ya hace el Anexo. La columna `Predecesoras propuestas (explícitas)` de `schedule.csv` trae el texto listo para pegar.

### 2 · Las fechas y la columna de dependencias no se cuentan la misma historia

Hay **7 actividades que empiezan antes de que termine una de sus predecesoras** y **una espera que la columna no explica**. Mirando las fechas, lo más probable es que la columna tenga errores de tipeo (hipótesis: **confirmar con quien armó el Excel**):

| Sucesora | Nombre | Predecesora | Nombre | Adelanto (d.h.) | Qué muestran las fechas |
|---|---|---|---|---|---|
| 2 | Identificación inicial de stakeholders | 1 | Definición del proyecto y alcance | 2 | Inicio-a-inicio +1 día: 2 y 3 arrancan el día siguiente a que arranca 1. |
| 3 | Relevamiento preliminar de sistemas y fuentes | 1 | Definición del proyecto y alcance | 2 | Ídem. |
| 8 | Definición de requerimientos funcionales | 7 | Relevamiento de fuentes de datos y APIs | 2 | Las fechas esperan a 5 y 6 (terminan el 17/04), no a 7 (termina el 21/04). |
| 9 | Definición de requerimientos no funcionales | 7 | Relevamiento de fuentes de datos y APIs | 2 | Ídem. |
| 14 | Diseño de validación y seguimiento | 13 | Diseño del sistema de reportes | 2 | 14 arranca al día siguiente de que termina 11 (08/05); 13 termina el 12/05. |
| 15 | Diseño de integraciones y APIs | 12 | Diseño de la capa geográfica común | 2 | 15 arranca al día siguiente de que termina 11; 12 termina el 12/05. |
| 16 | Diseño UX/UI | 14 | Diseño de validación y seguimiento | 3 | 16 arranca al día siguiente de que termina 13 (12/05); 14 termina el 15/05. |

Además, la actividad **27 (Pruebas funcionales)** arranca el 22/07, el día siguiente a que termina **26**, pero su celda dice «18-23» (todas terminan, como tarde, el 02/07): **13 días hábiles de espera** que ninguna dependencia explica. Y entre **31 y 32** hay **un día hábil sin actividad** (21/08).

**Celdas a corregir (la lista escrita contradice las fechas, se lea el guion como se lea):**

| ID | Actividad | Escrito | Propuesto | Por qué |
|---|---|---|---|---|
| 8 | Definición de requerimientos funcionales | 5-7 | 5, 6 | Arranca el 20/04, el día siguiente a que terminan 5 y 6 (17/04); 7 termina el 21/04. |
| 9 | Definición de requerimientos no funcionales | 5-7 | 5, 6 | Ídem 8. |
| 10 | Validación de requerimientos | 8-9 | 7, 8, 9 | Si 8 y 9 ya no esperan a 7, la actividad 7 queda sin sucesora: lo lógico es validar con 7 terminada (termina el 21/04; 10 arranca el 27/04). |
| 14 | Diseño de validación y seguimiento | 13 | 11 | Arranca el 11/05, el día siguiente a que termina 11 (08/05); 13 termina el 12/05. |
| 15 | Diseño de integraciones y APIs | 10-12 | 10, 11 | Arranca el 11/05: espera a 10 y 11, no a 12 (termina el 12/05). |
| 16 | Diseño UX/UI | 10-14 | 12, 13 | Arranca el 13/05, el día siguiente a que terminan 12 y 13 (12/05); 14 termina el 15/05. |
| 27 | Pruebas funcionales | 18-23 | 26 | Arranca el 22/07, el día siguiente a que termina 26; 18 a 23 terminan, como tarde, el 02/07. |

**Celdas que solo hay que escribir explícitas** (la lectura «extremos» pierde predecesoras que las fechas sí respetan):

| ID | Actividad | Escrito | Explícito |
|---|---|---|---|
| 4 | Aprobación del Charter | 1-3 | 1, 2, 3 |
| 17 | Aprobación del diseño | 11-16 | 11, 12, 13, 14, 15, 16 |
| 31 | Corrección de errores | 27-30 | 27, 28, 29, 30 |
| 39 | Transferencia a responsables operativos | 36-38 | 36, 37, 38 |
| 40 | Cierre formal del proyecto | 37-39 | 37, 38, 39 |

Con esas correcciones **todas las fechas del equipo se reproducen exactamente** (hasta la actividad 31; desde la 32 el cálculo adelanta un día por el día sin actividad) y ya no queda ningún solape salvo 2 y 3, que se escriben como inicio-a-inicio (+1 día).

### 3 · Qué le hace cada lectura a la fecha de cierre

| Lectura | Días hábiles | Fin | Actividades con holgura 0 |
|---|---|---|---|
| **Como está escrito, «a-b» = los dos extremos** (es lo que calcula la hoja del equipo) | 126 | 23/09/2026 | 23 |
| Como está escrito, «a-b» = todo el rango | 129 | 28/09/2026 | 24 |
| Fechas escritas en las columnas Inicio/Fin | 131 | 30/09/2026 | — |
| **Dependencias corregidas según las fechas** (opción A, recomendada) | 130 | 29/09/2026 | 27 |
| Dependencias como están + 7 adelantos + vínculo 26→27 (opción B) | 130 | 29/09/2026 | 26 |
| Fin-a-inicio estricto + vínculo 26→27, fechas recalculadas (opción C) | 139 | 12/10/2026 | 25 |

Cómo se llega de un número al otro: con las dependencias **como están** y fin-a-inicio estricto más el vínculo 26→27, el proyecto cerraría el **12/10/2026** (139 d.h.); los **9 días hábiles** de adelantos lo comprimen a 130, y el día sin actividad entre 31 y 32 lo estira a 131 (el cierre del 30/09 del equipo). **Conclusión:** la fecha del 30/09 se sostiene, pero solo con las dependencias corregidas (opción A) o declarando los adelantos (opción B).

### 4 · El camino crítico cambia con las correcciones

- **Publicado** (hoja del equipo): 23 actividades sin holgura; cadena principal 1, 3, 4, 7, 8, 10, 13, 14, 16, 17, 18, 23, 27, 30, 31, 32, 34, 35, 36, 38, 39, 40.
- **Con dependencias corregidas:** 27 actividades sin holgura; cadena principal 1, 3, 4, 5, 8, 10, 12, 16, 17, 18, 23, 25, 26, 27, 29, 31, 32, 34, 35, 36, 38, 39, 40.
- **Entran al camino crítico:** 5, 6, 12, 25, 26, 29. **Salen:** 7, 14.
- Lectura de negocio: pasan a ser críticas la **integración con canales digitales (25)** y las **pruebas de intercambio (26)**, que antes tenían 32 días de holgura. Es coherente con el riesgo R12 (cambios en canales como Boti, BAX y miBA): conviene decirlo en la defensa.

### 5 · Calendario y feriados (opcional)

El Excel declara un «período operativo ficticio» y usa lunes a viernes **sin feriados**. Es una convención válida si se declara. Dentro del período hay **8 feriados o días no laborables en día de semana**; si se contaran, las 131 jornadas terminarían el **13/10/2026**, un día antes de la entrega (14/10). Actividades cuyas fechas incluyen alguno:

| ID | Actividad | Fechas no laborables incluidas |
|---|---|---|
| 1 | Definición del proyecto y alcance | 02/04, 03/04 |
| 2 | Identificación inicial de stakeholders | 02/04, 03/04 |
| 3 | Relevamiento preliminar de sistemas y fuentes | 02/04, 03/04 |
| 10 | Validación de requerimientos | 01/05 |
| 17 | Aprobación del diseño | 25/05 |
| 18 | Desarrollo de la capa geográfica | 15/06 |
| 19 | Desarrollo del módulo de reportes | 15/06 |
| 22 | Desarrollo de vista de gestión | 15/06 |
| 24 | Integración con fuentes oficiales | 09/07, 10/07 |
| 25 | Integración con canales digitales | 09/07, 10/07 |
| 31 | Corrección de errores | 17/08 |

**Propuesta (mínimo esfuerzo):** no tocar fechas y agregar una línea: *«Las fechas del proyecto (01/04–30/09/2026) corresponden a una simulación académica; se cuentan los días de lunes a viernes, sin feriados.»* Fuentes de los feriados: [Canal 26](https://www.canal26.com/general/2025/11/02/confirman-los-feriados-del-2026-en-argentina-el-calendario-completo-con-fines-de-semana-largos/) y [Argentina.travel](https://www.argentina.travel/es/novedades/feriados-en-argentina-2026-calendario-para-planificar-tu-viaje); el traslado del 15/06 (Güemes) figura como **a confirmar**.

### 6 · Columna «Responsable» vacía

Propuesta: un **rol** por actividad, el mismo que usa el presupuesto (`Responsable propuesto (rol)` en la tabla de abajo y en `schedule.csv`). Cada rol trabaja dentro de su ventana del presupuesto, así que **mano de obra y Gantt cuentan lo mismo**.

### 7 · PERT: no hace falta, pero hay que saber contestarlo (complemento)

La Clase 3 enseña PERT `(O+4M+P)/6` para estimar duraciones. La hoja usa **CPM con una duración por actividad** y lo dice. Es aceptable. Si el profesor pregunta: *«no tenemos estimaciones de tres puntos; usamos CPM con duraciones únicas, y PERT es el paso siguiente para las actividades más inciertas».* A modo de **ilustración** (valores a acordar, **no son datos del equipo**; M es la duración del equipo):

| ID | Actividad | O | M | P | Esperada | Diferencia vs. M |
|---|---|---|---|---|---|---|
| 7 | Relevamiento de fuentes de datos y APIs | 5 | 7 | 15 | 8,00 | 1,00 |
| 23 | Desarrollo de APIs e integraciones | 9 | 12 | 21 | 13,00 | 1,00 |
| 25 | Integración con canales digitales | 6 | 8 | 16 | 9,00 | 1,00 |
| 27 | Pruebas funcionales | 6 | 8 | 10 | 8,00 | 0,00 |
| 30 | Pruebas de rendimiento y seguridad | 6 | 7 | 10 | 7,33 | 0,33 |
| 31 | Corrección de errores | 5 | 7 | 16 | 8,17 | 1,17 |

### 8 · Otros documentos que no coinciden con el Excel

- **Documento resumido, tabla de fases:** 5 de 8 ventanas difieren del Excel, y dos fases arrancan un **sábado** (18/04 y 02/05):

| Fase | En el documento resumido | En el Excel |
|---|---|---|
| Inicio | 10/04/2026 – 17/04/2026 | 01/04/2026 – 10/04/2026 |
| Análisis | 18/04/2026 – 01/05/2026 | 13/04/2026 – 01/05/2026 |
| Diseño | 02/05/2026 – 26/05/2026 | 04/05/2026 – 26/05/2026 |
| Implementación | 28/08/2026 – 09/09/2026 | 28/08/2026 – 16/09/2026 |
| Cierre | 10/09/2026 – 30/09/2026 | 17/09/2026 – 30/09/2026 |

- **Charter largo §6.5:** lista **7** puntos de control (junta «desarrollo e integraciones» en el Gate 4) frente a los **8** hitos del Excel y de §6.3. Propuesta: 8, uno por fase, con los nombres del Excel.
- La actividad 36 (**Monitoreo inicial**) es de la fase *Implementación* en el Excel; la tabla de fases del resumen la ubica en *Cierre*.

### Gates: Excel, Charter y resultado del cálculo

| Gate | Hito (Excel) | Documento resumido | Excel | Calculado (fechas del equipo) | OK |
|---|---|---|---|---|---|
| G1 | Charter aprobado | 10/04/2026 | 10/04/2026 | 10/04/2026 | ✓ |
| G2 | Requerimientos aprobados | 01/05/2026 | 01/05/2026 | 01/05/2026 | ✓ |
| G3 | Diseño aprobado | 26/05/2026 | 26/05/2026 | 26/05/2026 | ✓ |
| G4 | Desarrollo completado | 02/07/2026 | 02/07/2026 | 02/07/2026 | ✓ |
| G5 | Integraciones validadas | 21/07/2026 | 21/07/2026 | 21/07/2026 | ✓ |
| G6 | Pruebas aprobadas | 27/08/2026 | 27/08/2026 | 27/08/2026 | ✓ |
| G7 | Puesta en funcionamiento | 09/09/2026 | 09/09/2026 | 09/09/2026 | ✓ |
| G8 | Cierre del proyecto | 30/09/2026 | 30/09/2026 | 30/09/2026 | ✓ |

## Las 40 actividades (como las escribió el equipo, con la propuesta al lado)

Inicio/Fin son las del equipo; «Holgura» y «Crítica» corresponden a la opción A.

| ID | Actividad | Dur. | Dependencias (escrito) | Explícitas (propuesta) | Inicio | Fin | Holgura | Crítica | Responsable (rol) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Definición del proyecto y alcance | 3 | - | - | 01/04 | 03/04 | 0 | **Sí** | Project Manager |
| 2 | Identificación inicial de stakeholders | 3 | 1 | 1 (inicio-a-inicio +1 día) | 02/04 | 06/04 | 120 | No | Project Manager |
| 3 | Relevamiento preliminar de sistemas y fuentes | 4 | 1 | 1 (inicio-a-inicio +1 día) | 02/04 | 07/04 | 0 | **Sí** | Especialistas en datos y GIS |
| 4 | Aprobación del Charter | 3 | 1-3 | 1, 2, 3 | 08/04 | 10/04 | 0 | **Sí** | Project Manager |
| 5 | Relevamiento de necesidades de vecinos | 5 | 4 | 4 | 13/04 | 17/04 | 2 | **Sí** | Analistas funcionales |
| 6 | Relevamiento de necesidades de áreas de gobierno | 5 | 4 | 4 | 13/04 | 17/04 | 111 | **Sí** | Analistas funcionales |
| 7 | Relevamiento de fuentes de datos y APIs | 7 | 4 | 4 | 13/04 | 21/04 | 0 | No | Especialistas en datos y GIS |
| 8 | Definición de requerimientos funcionales | 5 | 5-7 | 5, 6 | 20/04 | 24/04 | 0 | **Sí** | Analistas funcionales |
| 9 | Definición de requerimientos no funcionales | 5 | 5-7 | 5, 6 | 20/04 | 24/04 | 0 | **Sí** | Analistas funcionales |
| 10 | Validación de requerimientos | 5 | 8-9 | 7, 8, 9 | 27/04 | 01/05 | 0 | **Sí** | Project Manager |
| 11 | Diseño de arquitectura de la solución | 5 | 10 | 10 | 04/05 | 08/05 | 15 | No | Desarrolladores |
| 12 | Diseño de la capa geográfica común | 7 | 10 | 10 | 04/05 | 12/05 | 24 | **Sí** | Especialistas en datos y GIS |
| 13 | Diseño del sistema de reportes | 7 | 10 | 10 | 04/05 | 12/05 | 0 | **Sí** | Analistas funcionales |
| 14 | Diseño de validación y seguimiento | 5 | 13 | 11 | 11/05 | 15/05 | 0 | No | Analistas funcionales |
| 15 | Diseño de integraciones y APIs | 6 | 10-12 | 10, 11 | 11/05 | 18/05 | 24 | No | Desarrolladores |
| 16 | Diseño UX/UI | 8 | 10-14 | 12, 13 | 13/05 | 22/05 | 0 | **Sí** | UX/UI |
| 17 | Aprobación del diseño | 2 | 11-16 | 11, 12, 13, 14, 15, 16 | 25/05 | 26/05 | 0 | **Sí** | Project Manager |
| 18 | Desarrollo de la capa geográfica | 15 | 17 | 17 | 27/05 | 16/06 | 0 | **Sí** | Desarrolladores |
| 19 | Desarrollo del módulo de reportes | 15 | 17 | 17 | 27/05 | 16/06 | 52 | No | Desarrolladores |
| 20 | Desarrollo de validación colaborativa | 5 | 19 | 19 | 17/06 | 23/06 | 52 | No | Desarrolladores |
| 21 | Desarrollo del seguimiento de incidencias | 5 | 19-20 | 19, 20 | 24/06 | 30/06 | 52 | No | Desarrolladores |
| 22 | Desarrollo de vista de gestión | 15 | 17 | 17 | 27/05 | 16/06 | 62 | No | Desarrolladores |
| 23 | Desarrollo de APIs e integraciones | 12 | 15,18 | 15, 18 | 17/06 | 02/07 | 0 | **Sí** | Desarrolladores |
| 24 | Integración con fuentes oficiales | 6 | 18,23 | 18, 23 | 03/07 | 10/07 | 34 | No | Especialistas en datos y GIS |
| 25 | Integración con canales digitales | 8 | 23 | 23 | 03/07 | 14/07 | 32 | **Sí** | Desarrolladores |
| 26 | Pruebas de intercambio de datos | 5 | 24-25 | 24, 25 | 15/07 | 21/07 | 32 | **Sí** | QA y testing |
| 27 | Pruebas funcionales | 8 | 18-23 | 26 | 22/07 | 31/07 | 0 | **Sí** | QA y testing |
| 28 | Pruebas de integración | 5 | 26-27 | 26, 27 | 03/08 | 07/08 | 32 | No | QA y testing |
| 29 | Pruebas de usabilidad | 7 | 16,27 | 16, 27 | 03/08 | 11/08 | 35 | **Sí** | UX/UI |
| 30 | Pruebas de rendimiento y seguridad | 7 | 27 | 27 | 03/08 | 11/08 | 0 | **Sí** | Seguridad informática |
| 31 | Corrección de errores | 7 | 27-30 | 27, 28, 29, 30 | 12/08 | 20/08 | 0 | **Sí** | Desarrolladores |
| 32 | Aprobación final de pruebas | 4 | 31 | 31 | 24/08 | 27/08 | 0 | **Sí** | QA y testing |
| 33 | Preparación del entorno productivo | 4 | 32 | 32 | 28/08 | 02/09 | 2 | No | Infraestructura/DevOps |
| 34 | Capacitación y documentación | 6 | 32 | 32 | 28/08 | 04/09 | 0 | **Sí** | Documentación y capacitación |
| 35 | Puesta en funcionamiento | 3 | 33-34 | 33, 34 | 07/09 | 09/09 | 0 | **Sí** | Infraestructura/DevOps |
| 36 | Monitoreo inicial | 5 | 35 | 35 | 10/09 | 16/09 | 0 | **Sí** | Infraestructura/DevOps |
| 37 | Evaluación de resultados | 4 | 36 | 36 | 17/09 | 22/09 | 4 | No | Project Manager |
| 38 | Documentación final | 6 | 36 | 36 | 17/09 | 24/09 | 0 | **Sí** | Documentación y capacitación |
| 39 | Transferencia a responsables operativos | 2 | 36-38 | 36, 37, 38 | 25/09 | 28/09 | 0 | **Sí** | Project Manager |
| 40 | Cierre formal del proyecto | 2 | 37-39 | 37, 38, 39 | 29/09 | 30/09 | 0 | **Sí** | Project Manager |

## Opciones para decidir entre todos

| Opción | Qué se hace | Fechas | Fin | Esfuerzo |
|---|---|---|---|---|
| **A (recomendada)** | Corregir 7 celdas, escribir explícitas las demás y marcar 2 y 3 como inicio-a-inicio | No cambian | 29/09/2026 de cálculo; 30/09 con el día sin actividad | Bajo (editar ~12 celdas) |
| B | Dejar las dependencias y registrar 7 adelantos y el vínculo 26→27 | No cambian | 29/09/2026 | Bajo, pero conserva los errores de tipeo |
| C | Respetar fin-a-inicio con las dependencias actuales | Se corren | 12/10/2026 (pasa el 30/09) | Alto: rehacer fechas, hitos y presupuesto |
| Mínimo para entregar | Solo agregar una nota en el punto 6: «a-b = los dos extremos» y la línea de simulación | No cambian | 23/09 (CPM) / 30/09 (fechas) | Muy bajo |

## Línea base

La tabla de arriba, con las fechas del equipo, es la **línea base v1 del cronograma** (Clase 3); cualquier cambio de fecha de un gate pasa por el control de cambios del Charter.

## Qué no se pudo verificar

- Que las correcciones propuestas sean las que **quiso escribir** quien armó el Excel: son una deducción a partir de las fechas.
- Si la Clase 3 usa la notación de **adelantos y retrasos**: la cátedra enseña las relaciones FS, FF y SS (el cuarto tipo, SF, aparece solo como complemento); los adelantos son un recurso de este análisis.
- La imagen EMF incrustada en el documento Word no se pudo abrir; el Excel la reemplaza.
