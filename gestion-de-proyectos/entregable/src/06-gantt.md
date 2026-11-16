# 6. Gantt del proyecto completo

## 6.1 Criterios de planificación

Tomando como base el alcance, los entregables principales y los 8 hitos definidos en el Project Charter, estructuramos la planificación temporal y las dependencias en el diagrama de Gantt

El cronograma del proyecto se organiza bajo una metodología **Cascada (Waterfall)**, por lo que las principales fases se desarrollan de manera secuencial. Cada etapa cuenta con actividades, dependencias y entregables definidos, y su finalización permite avanzar hacia la siguiente fase.

Dentro de cada fase pueden desarrollarse actividades en paralelo cuando no existe una dependencia directa entre ellas. El cronograma contempla las siguientes etapas:

- Inicio

- Análisis

- Diseño

- Desarrollo

- Integración

- Pruebas

- Implementación

- Cierre

Se establece como período tentativo del proyecto **abril a septiembre de 2026** (del 01/04 al 30/09), es decir, unos seis meses.

Las fechas son una planificación académica estimativa y pueden ajustarse de acuerdo con la disponibilidad de los equipos, las validaciones de las áreas involucradas y las dependencias técnicas identificadas durante el proyecto.

## 6.2 Cronograma detallado

El diagrama muestra las 40 actividades agrupadas por fase, con el camino crítico resaltado y los 8 hitos del proyecto. Ninguna actividad comienza antes de que termine su predecesora; las que no están en el camino crítico tienen holgura y pueden desplazarse sin afectar el cierre.

![Diagrama de Gantt del proyecto: 40 actividades por fase, camino crítico e hitos](img/gantt.png)

**Anexo Cronograma Detallado de Trabajo y Diagrama de Gantt – Proyecto Modernización del Mapa Interactivo de la Ciudad**

> **Resumen del cronograma.** El detalle completo (cronograma de 40 actividades, dependencias, holguras, camino crítico e hitos) se encuentra en el **Anexo A**, adaptado del Excel del equipo. El proyecto se organiza en 8 fases (inicio, análisis, diseño, desarrollo, integración, pruebas, implementación, cierre) entre el 01/04/2026 y el 30/09/2026 (camino crítico de 126 días hábiles dentro de una ventana de 131 días hábiles, unas 25 semanas de trabajo; los 5 días restantes son holgura del cierre). La hoja de dependencias marca 23 actividades con holgura cero (camino crítico) y la planilla de hitos registra 8 hitos operativos.

## 6.3 Hitos principales

Los principales hitos del proyecto son:

| **Hito** | **Fecha estimada** | **Resultado** |
|---|---|---|
| Charter aprobado | 14/04/2026 | Project Charter formalizado y firmado |
| Requerimientos aprobados | 07/05/2026 | Requerimientos funcionales y no funcionales validados |
| Diseño aprobado | 08/06/2026 | Arquitectura, capa geográfica, integraciones y UX definidos |
| Desarrollo completado | 15/07/2026 | Componentes principales desarrollados |
| Integraciones validadas | 03/08/2026 | Fuentes y canales integrados |
| Pruebas aprobadas | 27/08/2026 | Solución validada |
| Puesta en funcionamiento | 09/09/2026 | Solución disponible en producción |
| Cierre del proyecto | 30/09/2026 | Transferencia y cierre formal |

La línea de tiempo ubica los ocho hitos sobre las fases del proyecto.

![Línea de tiempo de los 8 hitos del proyecto sobre las fases](img/hitos.png)

## 6.4 Relación entre fases

El flujo principal del proyecto es secuencial: cada fase se apoya en la aprobación de la anterior, con un solapamiento parcial entre Integración y Pruebas. El diagrama muestra las ocho fases con sus fechas y su hito, y detalla las actividades de Diseño que se desarrollan en paralelo.

![Relación entre las fases del proyecto: fechas, hitos y actividades de Diseño en paralelo](img/fases.png)

Dentro de cada etapa se permite el desarrollo paralelo de actividades que no presentan dependencias directas. Por ejemplo, durante Diseño pueden desarrollarse simultáneamente la arquitectura, la capa geográfica, el sistema de reportes y el diseño UX/UI.

## 6.5 Hitos de control

Para mantener el enfoque Waterfall, se establecen puntos de control antes de avanzar entre las principales etapas:

- **Gate 1 (Hito 1):** aprobación del Project Charter.

- **Gate 2 (Hito 2):** aprobación de requerimientos.

- **Gate 3 (Hito 3):** aprobación del diseño.

- **Gate 4 (Hito 4):** finalización del desarrollo.

- **Gate 5 (Hito 5):** validación de integraciones.

- **Gate 6 (Hito 6):** aprobación de pruebas.

- **Gate 7 (Hito 7):** autorización de puesta en producción.

- **Gate 8 (Hito 8):** cierre y transferencia operativa.

Estos puntos de control permiten verificar que los entregables de cada etapa cumplan con los criterios definidos antes de continuar con la siguiente fase.
