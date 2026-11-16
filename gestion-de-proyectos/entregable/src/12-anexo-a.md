# Anexo A. Cronograma, dependencias, camino crítico e hitos

Este anexo reproduce las hojas del Excel de planificación del equipo, adaptadas para que las fechas respeten las dependencias entre actividades (ninguna actividad empieza antes de que termine su predecesora), con las dependencias escritas de forma explícita («1, 3» indica las actividades 1 y 3) y con un rol responsable por actividad. Las duraciones, el camino crítico y las holguras son los del equipo.

## A.1 Cronograma de actividades

CRONOGRAMA DE ACTIVIDADES Y DIAGRAMA DE GANTT (01/04/2026 - 30/09/2026)

Período operativo ficticio del proyecto. Duración en días hábiles (lunes a viernes). «Responsable» indica el rol principal de cada actividad. Dependencias: «1, 3» significa las actividades 1 y 3; ninguna actividad empieza antes de que termine su predecesora.

Tabla: Cronograma de actividades del proyecto (adaptado del Excel del equipo)

| ID | Fase | Actividad | Inicio | Fin | Duración (días) | Dependencias | Responsable | Entregable |
|---|---|---|---|---|---|---|---|---|
| 1 | Inicio | Definición del proyecto y alcance | 01/04/26 | 03/04/26 | 3 | - | Project Manager | Project Charter |
| 2 | Inicio | Identificación inicial de stakeholders | 06/04/26 | 08/04/26 | 3 | 1 | Project Manager | Registro inicial |
| 3 | Inicio | Relevamiento preliminar de sistemas y fuentes | 06/04/26 | 09/04/26 | 4 | 1 | Analistas funcionales | Relevamiento inicial |
| 4 | Inicio | Aprobación del Charter | 10/04/26 | 14/04/26 | 3 | 1, 3 | Sponsor | Charter aprobado |
| 5 | Análisis | Relevamiento de necesidades de vecinos | 15/04/26 | 21/04/26 | 5 | 4 | Analistas funcionales | Requerimientos de usuario |
| 6 | Análisis | Relevamiento de necesidades de áreas de gobierno | 15/04/26 | 21/04/26 | 5 | 4 | Analistas funcionales | Requerimientos internos |
| 7 | Análisis | Relevamiento de fuentes de datos y APIs | 15/04/26 | 23/04/26 | 7 | 4 | Especialistas en datos y GIS | Inventario de fuentes |
| 8 | Análisis | Definición de requerimientos funcionales | 24/04/26 | 30/04/26 | 5 | 5, 7 | Analistas funcionales | Requerimientos funcionales |
| 9 | Análisis | Definición de requerimientos no funcionales | 24/04/26 | 30/04/26 | 5 | 5, 7 | Analistas funcionales | Requerimientos no funcionales |
| 10 | Análisis | Validación de requerimientos | 01/05/26 | 07/05/26 | 5 | 8, 9 | Project Manager | Requerimientos aprobados |
| 11 | Diseño | Diseño de arquitectura de la solución | 08/05/26 | 14/05/26 | 5 | 10 | Desarrolladores | Arquitectura |
| 12 | Diseño | Diseño de la capa geográfica común | 08/05/26 | 18/05/26 | 7 | 10 | Especialistas en datos y GIS | Diseño geográfico |
| 13 | Diseño | Diseño del sistema de reportes | 08/05/26 | 18/05/26 | 7 | 10 | Desarrolladores | Diseño de reportes |
| 14 | Diseño | Diseño de validación y seguimiento | 19/05/26 | 25/05/26 | 5 | 13 | Analistas funcionales | Flujo de incidencias |
| 15 | Diseño | Diseño de integraciones y APIs | 19/05/26 | 26/05/26 | 6 | 10, 12 | Desarrolladores | Diseño de integración |
| 16 | Diseño | Diseño UX/UI | 26/05/26 | 04/06/26 | 8 | 10, 14 | UX/UI | Prototipos |
| 17 | Diseño | Aprobación del diseño | 05/06/26 | 08/06/26 | 2 | 11, 16 | Sponsor | Diseño aprobado |
| 18 | Desarrollo | Desarrollo de la capa geográfica | 09/06/26 | 29/06/26 | 15 | 17 | Desarrolladores | Capa geográfica |
| 19 | Desarrollo | Desarrollo del módulo de reportes | 09/06/26 | 29/06/26 | 15 | 17 | Desarrolladores | Módulo de reportes |
| 20 | Desarrollo | Desarrollo de validación colaborativa | 30/06/26 | 06/07/26 | 5 | 19 | Desarrolladores | Validación |
| 21 | Desarrollo | Desarrollo del seguimiento de incidencias | 07/07/26 | 13/07/26 | 5 | 19, 20 | Desarrolladores | Seguimiento |
| 22 | Desarrollo | Desarrollo de vista de gestión | 09/06/26 | 29/06/26 | 15 | 17 | Desarrolladores | Panel de gestión |
| 23 | Desarrollo | Desarrollo de APIs e integraciones | 30/06/26 | 15/07/26 | 12 | 15, 18 | Desarrolladores | Integraciones |
| 24 | Integración | Integración con fuentes oficiales | 16/07/26 | 23/07/26 | 6 | 18, 23 | Especialistas en datos y GIS | Fuentes integradas |
| 25 | Integración | Integración con canales digitales | 16/07/26 | 27/07/26 | 8 | 23 | Desarrolladores | Canales integrados |
| 26 | Integración | Pruebas de intercambio de datos | 28/07/26 | 03/08/26 | 5 | 24, 25 | QA y testing | Integraciones validadas |
| 27 | Pruebas | Pruebas funcionales | 22/07/26 | 31/07/26 | 8 | 18, 23 | QA y testing | Resultados de testing |
| 28 | Pruebas | Pruebas de integración | 04/08/26 | 10/08/26 | 5 | 26, 27 | QA y testing | Integración validada |
| 29 | Pruebas | Pruebas de usabilidad | 03/08/26 | 11/08/26 | 7 | 16, 27 | UX/UI | Evaluación UX |
| 30 | Pruebas | Pruebas de rendimiento y seguridad | 03/08/26 | 11/08/26 | 7 | 27 | Seguridad informática | Evaluación técnica |
| 31 | Pruebas | Corrección de errores | 12/08/26 | 20/08/26 | 7 | 27, 30 | Desarrolladores | Versión corregida |
| 32 | Pruebas | Aprobación final de pruebas | 24/08/26 | 27/08/26 | 4 | 31 | Sponsor | Solución validada |
| 33 | Implementación | Preparación del entorno productivo | 28/08/26 | 02/09/26 | 4 | 32 | Infraestructura/DevOps | Entorno preparado |
| 34 | Implementación | Capacitación y documentación | 28/08/26 | 04/09/26 | 6 | 32 | Documentación y capacitación | Materiales y capacitación |
| 35 | Implementación | Puesta en funcionamiento | 07/09/26 | 09/09/26 | 3 | 33, 34 | Infraestructura/DevOps | Solución implementada |
| 36 | Implementación | Monitoreo inicial | 10/09/26 | 16/09/26 | 5 | 35 | Infraestructura/DevOps | Informe inicial |
| 37 | Cierre | Evaluación de resultados | 17/09/26 | 22/09/26 | 4 | 36 | Project Manager | Evaluación |
| 38 | Cierre | Documentación final | 17/09/26 | 24/09/26 | 6 | 36 | Documentación y capacitación | Documentación |
| 39 | Cierre | Transferencia a responsables operativos | 25/09/26 | 28/09/26 | 2 | 36, 38 | Project Manager | Transferencia |
| 40 | Cierre | Cierre formal del proyecto | 29/09/26 | 30/09/26 | 2 | 37, 39 | Sponsor | Acta de cierre |

## A.2 Dependencias, holguras y camino crítico

ANÁLISIS DE DEPENDENCIAS, HOLGURAS Y CAMINO CRÍTICO

Cálculo CPM basado exclusivamente en las dependencias y duraciones del cronograma. Holgura 0 = actividad crítica. La duración de la red es de 126 días hábiles dentro de una ventana de 131 días hábiles (01/04 al 30/09/2026).

Tabla: Dependencias, holguras y camino crítico (adaptado del Excel del equipo)

| ID | Fase | Actividad | Predecesoras | Duración (días) | Holgura (días) | Camino Crítico |
|---|---|---|---|---|---|---|
| 1 | Inicio | Definición del proyecto y alcance | - | 3 | 0 | SÍ |
| 2 | Inicio | Identificación inicial de stakeholders | 1 | 3 | 120 | NO |
| 3 | Inicio | Relevamiento preliminar de sistemas y fuentes | 1 | 4 | 0 | SÍ |
| 4 | Inicio | Aprobación del Charter | 1, 3 | 3 | 0 | SÍ |
| 5 | Análisis | Relevamiento de necesidades de vecinos | 4 | 5 | 2 | NO |
| 6 | Análisis | Relevamiento de necesidades de áreas de gobierno | 4 | 5 | 111 | NO |
| 7 | Análisis | Relevamiento de fuentes de datos y APIs | 4 | 7 | 0 | SÍ |
| 8 | Análisis | Definición de requerimientos funcionales | 5, 7 | 5 | 0 | SÍ |
| 9 | Análisis | Definición de requerimientos no funcionales | 5, 7 | 5 | 0 | SÍ |
| 10 | Análisis | Validación de requerimientos | 8, 9 | 5 | 0 | SÍ |
| 11 | Diseño | Diseño de arquitectura de la solución | 10 | 5 | 15 | NO |
| 12 | Diseño | Diseño de la capa geográfica común | 10 | 7 | 24 | NO |
| 13 | Diseño | Diseño del sistema de reportes | 10 | 7 | 0 | SÍ |
| 14 | Diseño | Diseño de validación y seguimiento | 13 | 5 | 0 | SÍ |
| 15 | Diseño | Diseño de integraciones y APIs | 10, 12 | 6 | 24 | NO |
| 16 | Diseño | Diseño UX/UI | 10, 14 | 8 | 0 | SÍ |
| 17 | Diseño | Aprobación del diseño | 11, 16 | 2 | 0 | SÍ |
| 18 | Desarrollo | Desarrollo de la capa geográfica | 17 | 15 | 0 | SÍ |
| 19 | Desarrollo | Desarrollo del módulo de reportes | 17 | 15 | 52 | NO |
| 20 | Desarrollo | Desarrollo de validación colaborativa | 19 | 5 | 52 | NO |
| 21 | Desarrollo | Desarrollo del seguimiento de incidencias | 19, 20 | 5 | 52 | NO |
| 22 | Desarrollo | Desarrollo de vista de gestión | 17 | 15 | 62 | NO |
| 23 | Desarrollo | Desarrollo de APIs e integraciones | 15, 18 | 12 | 0 | SÍ |
| 24 | Integración | Integración con fuentes oficiales | 18, 23 | 6 | 34 | NO |
| 25 | Integración | Integración con canales digitales | 23 | 8 | 32 | NO |
| 26 | Integración | Pruebas de intercambio de datos | 24, 25 | 5 | 32 | NO |
| 27 | Pruebas | Pruebas funcionales | 18, 23 | 8 | 0 | SÍ |
| 28 | Pruebas | Pruebas de integración | 26, 27 | 5 | 32 | NO |
| 29 | Pruebas | Pruebas de usabilidad | 16, 27 | 7 | 35 | NO |
| 30 | Pruebas | Pruebas de rendimiento y seguridad | 27 | 7 | 0 | SÍ |
| 31 | Pruebas | Corrección de errores | 27, 30 | 7 | 0 | SÍ |
| 32 | Pruebas | Aprobación final de pruebas | 31 | 4 | 0 | SÍ |
| 33 | Implementación | Preparación del entorno productivo | 32 | 4 | 2 | NO |
| 34 | Implementación | Capacitación y documentación | 32 | 6 | 0 | SÍ |
| 35 | Implementación | Puesta en funcionamiento | 33, 34 | 3 | 0 | SÍ |
| 36 | Implementación | Monitoreo inicial | 35 | 5 | 0 | SÍ |
| 37 | Cierre | Evaluación de resultados | 36 | 4 | 4 | NO |
| 38 | Cierre | Documentación final | 36 | 6 | 0 | SÍ |
| 39 | Cierre | Transferencia a responsables operativos | 36, 38 | 2 | 0 | SÍ |
| 40 | Cierre | Cierre formal del proyecto | 37, 39 | 2 | 0 | SÍ |

## A.3 Hitos del proyecto

HITOS DEL PROYECTO

**1. Hitos Operativos del Proyecto**

Tabla: Hitos operativos del proyecto (adaptado del Excel del equipo)

| Hito Operativo | Fecha de Cumplimiento | Entregable / Resultado Asociado | Ámbito |
|---|---|---|---|
| Charter aprobado | 14/04/2026 | Project Charter formalizado y firmado | Proyecto Operativo |
| Requerimientos aprobados | 07/05/2026 | Especificación de Requerimientos Funcionales y No Funcionales | Proyecto Operativo |
| Diseño aprobado | 08/06/2026 | Documento de Arquitectura, Prototipos UI/UX y Modelo de Integración | Proyecto Operativo |
| Desarrollo completado | 15/07/2026 | Módulos de software, capa geográfica y APIs codificadas | Proyecto Operativo |
| Integraciones validadas | 03/08/2026 | Plataforma conectada con fuentes y canales digitales | Proyecto Operativo |
| Pruebas aprobadas | 27/08/2026 | Informe final de QA y aceptación de la solución | Proyecto Operativo |
| Puesta en funcionamiento | 09/09/2026 | Sistema desplegado en producción y capacitación efectuada | Proyecto Operativo |
| Cierre del proyecto | 30/09/2026 | Acta de Cierre, Lecciones Aprendidas y Transferencia | Proyecto Operativo |

## A.4 Análisis del camino crítico e hitos (anexo al punto 6)

ANEXO AL PUNTO 6 - CAMINO CRÍTICO Y HITOS

Este anexo complementa el Gantt del proyecto. Se utiliza el método de Camino Crítico (CPM) para identificar las actividades cuya holgura es cero y que, por lo tanto, condicionan la duración total del cronograma.

**6.4 Análisis del camino crítico**

Según las dependencias y duraciones definidas, la red de actividades presenta una duración de 126 días hábiles, dentro de una ventana de 131 días hábiles. Las actividades con holgura cero integran el camino crítico. Como existen actividades paralelas que luego convergen, el camino crítico se interpreta como una red de actividades críticas y no necesariamente como una única secuencia lineal.

Tabla: Actividades de la red con holgura y condición de críticas (adaptado del Excel del equipo)

| ID | Actividad | Duración | Holgura | Crítica | Dependencias |
|---|---|---|---|---|---|
| 1 | Definición del proyecto y alcance | 3 | 0 | SÍ | - |
| 3 | Relevamiento preliminar de sistemas y fuentes | 4 | 0 | SÍ | 1 |
| 4 | Aprobación del Charter | 3 | 0 | SÍ | 1, 3 |
| 7 | Relevamiento de fuentes de datos y APIs | 7 | 0 | SÍ | 4 |
| 8 | Definición de requerimientos funcionales | 5 | 0 | SÍ | 5, 7 |
| 9 | Definición de requerimientos no funcionales | 5 | 0 | SÍ | 5, 7 |
| 10 | Validación de requerimientos | 5 | 0 | SÍ | 8, 9 |
| 13 | Diseño del sistema de reportes | 7 | 0 | SÍ | 10 |
| 14 | Diseño de validación y seguimiento | 5 | 0 | SÍ | 13 |
| 16 | Diseño UX/UI | 8 | 0 | SÍ | 10, 14 |
| 17 | Aprobación del diseño | 2 | 0 | SÍ | 11, 16 |
| 18 | Desarrollo de la capa geográfica | 15 | 0 | SÍ | 17 |
| 23 | Desarrollo de APIs e integraciones | 12 | 0 | SÍ | 15, 18 |
| 27 | Pruebas funcionales | 8 | 0 | SÍ | 18, 23 |
| 30 | Pruebas de rendimiento y seguridad | 7 | 0 | SÍ | 27 |
| 31 | Corrección de errores | 7 | 0 | SÍ | 27, 30 |
| 32 | Aprobación final de pruebas | 4 | 0 | SÍ | 31 |
| 34 | Capacitación y documentación | 6 | 0 | SÍ | 32 |
| 35 | Puesta en funcionamiento | 3 | 0 | SÍ | 33, 34 |
| 36 | Monitoreo inicial | 5 | 0 | SÍ | 35 |
| 38 | Documentación final | 6 | 0 | SÍ | 36 |
| 39 | Transferencia a responsables operativos | 2 | 0 | SÍ | 36, 38 |
| 40 | Cierre formal del proyecto | 2 | 0 | SÍ | 37, 39 |

**Nota metodológica sobre PERT**

El análisis incluido corresponde a CPM (Critical Path Method). Para aplicar PERT en sentido estricto se necesitan tres estimaciones por actividad: optimista, más probable y pesimista. Esas estimaciones no están definidas en el cronograma actual, por lo que no se agregan valores estimados que no surgen del proyecto.

**6.5 Hitos del proyecto**

Tabla: Hitos del proyecto según el anexo al punto 6 (adaptado del Excel del equipo)

| Hito | Fecha | Resultado asociado | Ámbito |
|---|---|---|---|
| Charter aprobado | 14/04/2026 | Project Charter formalizado y firmado | Proyecto Operativo |
| Requerimientos aprobados | 07/05/2026 | Especificación de Requerimientos Funcionales y No Funcionales | Proyecto Operativo |
| Diseño aprobado | 08/06/2026 | Documento de Arquitectura, Prototipos UI/UX y Modelo de Integración | Proyecto Operativo |
| Desarrollo completado | 15/07/2026 | Módulos de software, capa geográfica y APIs codificadas | Proyecto Operativo |
| Integraciones validadas | 03/08/2026 | Plataforma conectada con fuentes y canales digitales | Proyecto Operativo |
| Pruebas aprobadas | 27/08/2026 | Informe final de QA y aceptación de la solución | Proyecto Operativo |
| Puesta en funcionamiento | 09/09/2026 | Sistema desplegado en producción y capacitación efectuada | Proyecto Operativo |
| Cierre del proyecto | 30/09/2026 | Acta de Cierre, Lecciones Aprendidas y Transferencia | Proyecto Operativo |
