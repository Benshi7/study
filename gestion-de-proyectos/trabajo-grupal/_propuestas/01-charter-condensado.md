# Project Charter condensado (≈ 2 páginas) + camino medio

> **Formato recomendado: la plantilla de la cátedra.** El mismo contenido está **completo en la plantilla de 24 campos** (`raw/Project_Charter_Template5.docx`) en `01-charter/Project_Charter_completado.docx`, con su `README.md` (mapa de los 13 elementos de la Clase 3 a los 24 campos y qué va al Anexo A). Este texto queda como **versión en prosa** del mismo contenido; si hay que elegir, **la plantilla es la opción principal**.

> **Propuesta.** Es una versión **para colocar como sección 5** manteniendo, como **Anexo A – Charter ampliado**, el texto largo del equipo (§5.1–5.12): nadie pierde trabajo. Se condensan las palabras del propio documento; lo nuevo está marcado **(propuesta)**. Ningún original fue modificado.

## Por qué condensar (con evidencia)

- La cátedra define el Charter como un **acuerdo preliminar de alto nivel** con **13 elementos en 3 partes** (Clase 3, p12–16). Lo que se evalúa es que estén y que sean **coherentes con el resto**.
- La sección 5 del documento largo tiene ≈ **6.060 palabras (más de la mitad del archivo (≈ 53 %))**; sus apartados 5.8 (presupuesto), 5.9 (riesgos) y 5.12 (cronograma) **repiten con menos detalle** las secciones 10, 9 y 6.
- **Esa duplicación ya produjo las contradicciones:** 12 riesgos en el Charter vs 15 en la matriz (y uno del Charter no está en la matriz), 8 hitos vs 7 gates, presupuesto sin cifra en el Charter y con cifra en la sección 10.
- Una sola fuente por dato (el Charter **resume y remite**) elimina esa clase de error.

## Mapa de los 13 elementos

| Elemento (nombre de la cátedra) | Dónde está hoy | Estado | Qué cambia |
|---|---|---|---|
| 1 · Propósito o justificación | §5.2, §5.3 | Presente | Condensar |
| 2 · Descripción de alto nivel | §5.1 (descripción breve), §5.5.1 | Presente | Condensar |
| 3 · Objetivos | §5.4 | Parcial | Los 8 objetivos no tienen meta ni plazo (no SMART). Se reemplazan por 4 resultados SMART (ver `05`); los 8 quedan en el Anexo A. |
| 4 · Requisitos de alto nivel | No existe como tal (se deducen de §5.5–5.6) | **Falta** | Lista de 8 requisitos (propuesta, abajo) |
| 5 · Producto o resultados principales | §5.6 | Presente | Condensar los 8 entregables en una lista |
| 6 · Suposiciones y restricciones | §5.10 | Presente | Condensar + supuesto de simulación + supuestos a confirmar |
| 7 · Cronograma de alto nivel | §5.12 (8 hitos, sin fechas) | Parcial | Tabla de 8 gates con fechas (de 02-gantt) |
| 8 · Presupuesto de alto nivel | §5.8 (categorías, sin cifra ni moneda) | Parcial | Una cifra en USD y 4 líneas (de 03-presupuesto) |
| 9 · Riesgos de alto nivel | §5.9.1 (12 riesgos) | Parcial | 5 riesgos con los IDs de la matriz; uno de los 12 («comercios») no existe en la matriz |
| 10 · Criterios de éxito | §5.7.1 | Presente | Condensar y vincular a los objetivos SMART |
| 11 · Stakeholders principales | §5.11 (roles) y PDF §7.3 | Parcial | Lista única de 9, igual a la del PDF |
| 12 · Responsabilidades y autoridad del PM | §5.11.2 (responsabilidades) | Parcial | Falta la **autoridad**: se propone abajo |
| 13 · Requisitos de aprobación | §5.11.1 (qué aprueba el Sponsor), §5.7.3 | Parcial | Se explicitan quién aprueba qué (propuesta, abajo) |

---

# 5. Project Charter *(texto propuesto)*

**Proyecto:** Modernización del Mapa Interactivo de la Ciudad · **Metodología:** cascada · **Organización:** Gobierno de la Ciudad de Buenos Aires · **Período simulado:** 01/04/2026–30/09/2026.

## Parte I

**1. Propósito y justificación.** Modernizar el Mapa Interactivo para convertirlo en una **plataforma geográfica común** que integre información de distintas áreas, la ofrezca desde varios canales digitales y permita la participación de los vecinos. El problema identificado es la **dispersión de la información entre canales, áreas y sistemas**: cada hogar debe saber de antemano qué organismo y qué canal usar, y no ve qué ocurre con lo que reporta. *(Condensado de §5.2–5.3; la validación con personas se detalla en la sección 4.)*

**2. Descripción de alto nivel.** Una **capa geográfica común** reutilizable por el Mapa y otros canales (Boti y BAX, sujeto a validación técnica), más un **sistema de reportes ciudadanos georreferenciados** con validación colaborativa y seguimiento del estado hasta el cierre, un **perfil de hogar básico** (dato mínimo declarado por el propio hogar, opt-in) y una **vista de gestión** para las áreas responsables. La Opción B del Canvas lo expresa como plataforma de dos lados: el vecino que usa y el Gobierno que financia y gestiona.

**3. Objetivos del proyecto** *(propuesta: cuatro resultados SMART; el texto completo está en `05-canvas-dt-smart.md`)*.
- **O1 · Capa geográfica confiable:** al 26/05 (Gate 3) la arquitectura y el diseño de la capa están aprobados y, al 02/07 (Gate 4), la capa integra las fuentes priorizadas con responsable y frecuencia de actualización definidos para el 100 % de ellas.
- **O2 · Integración multicanal:** al 21/07 (Gate 5) el Mapa y al menos un canal conversacional consumen la capa mediante API.
- **O3 · Reportes y seguimiento:** al 27/08 (Gate 6) el 100 % de los casos de prueba del flujo reporte → validación → derivación → resolución → cierre están aprobados.
- **O4 · Gestión y experiencia:** al 09/09 (Gate 7) al menos 3 áreas operativas usan la vista de gestión.

**4. Requisitos de alto nivel** *(propuesta; derivados de §5.5–5.6)*: (a) integrar las fuentes oficiales priorizadas en una capa común; (b) consultar la capa desde el Mapa y desde canales digitales seleccionados; (c) reportar incidencias con ubicación, categoría, fecha y hora; (d) validación colaborativa por otros usuarios; (e) seguimiento de estados (Reportado → Validado → Derivado → En gestión → Resuelto → Cerrado); (f) vista de gestión con filtros por categoría y estado; (g) gobernanza y calidad de datos y protección de los datos personales, incluido el perfil de hogar básico, opt-in y con dato mínimo (marco legal: **Ley 25.326, a verificar**); (h) documentación y transferencia a los responsables operativos.

## Parte II

**5. Producto y resultados principales.** Capa geográfica común · integraciones con fuentes y canales · módulo de reportes · validación colaborativa · seguimiento de incidencias · vista de gestión · documentación técnica y funcional · plan de implementación y cierre (§5.6).

**6. Suposiciones y restricciones.** *Supuestos:* las áreas ponen a disposición sus fuentes y participan de las validaciones; las fuentes priorizadas tienen APIs viables; los canales elegidos siguen disponibles; el equipo está disponible en cada etapa; las fuentes pueden asociarse a una referencia geográfica común. *Restricciones:* alcance cerrado (§5.5), enfoque en cascada con gates, dependencia de sistemas externos, calidad de las fuentes, presupuesto y plazos aprobados, protección de datos. **Supuesto de simulación:** *las fechas corresponden a una simulación académica; el trabajo se entrega el 14/10/2026.* **A confirmar:** la integración con BAX requiere miBA; marco legal de datos personales.

**7. Cronograma de alto nivel** *(detalle en la sección 6)*.

| Gate | Hito | Fecha |
|---|---|---|
| G1 | Charter aprobado | 10/04/2026 |
| G2 | Requerimientos aprobados | 01/05/2026 |
| G3 | Diseño aprobado | 26/05/2026 |
| G4 | Desarrollo completado | 02/07/2026 |
| G5 | Integraciones validadas | 21/07/2026 |
| G6 | Pruebas aprobadas | 27/08/2026 |
| G7 | Puesta en funcionamiento | 09/09/2026 |
| G8 | Cierre del proyecto | 30/09/2026 |

Duración simulada: 01/04–30/09/2026 (**131 días hábiles**, lunes a viernes). Camino crítico y holguras: sección 6.

**8. Presupuesto de alto nivel** *(detalle en la sección 10; escenario B, a decidir entre todos)*.

| Concepto | Monto (USD) |
|---|---|
| Costos del proyecto (mano de obra USD 151.709 + otros rubros USD 60.895) | USD 212.604 |
| Reserva de contingencia (Σ EMV de la matriz de riesgos) | USD 30.003 |
| **Línea base de costos** | **USD 242.607** |
| Reserva de gestión (10 %) | USD 24.261 |
| **Presupuesto total** | **USD 266.868** |

*Importes en USD al tipo de cambio de ARS 1.560,00 por USD (referencia del 09/10/2026, **a confirmar**); equivalente en pesos: ARS 416,3 M. Operación inicial posterior al cierre: USD 17.948, fuera de la línea base. Si el equipo elige el escenario A, el total es USD 230.639.*

**9. Riesgos de alto nivel** *(detalle en la sección 9; mismos IDs)*: **R01** falta de disponibilidad de apis o fuentes necesarias; **R02** baja calidad o desactualización de los datos; **R05** crecimiento no controlado del alcance; **R04** falta de coordinación entre áreas; **R12** cambios en canales digitales existentes (boti, bax, miba).

## Parte III

**10. Criterios de éxito.** Los cuatro objetivos SMART anteriores, más: información de fuentes oficiales con responsable y actualización definidos; cada reporte con un estado identificable desde la creación hasta el cierre; acceso de las áreas a la vista de gestión; documentación suficiente para operar y mantener (§5.7.1).

**11. Stakeholders principales** *(detalle en las secciones 7 y 8; misma lista)*: Sponsor institucional, Hacienda / Presupuesto, Project Manager, Equipo de Tecnología y Desarrollo, Equipo de Datos y GIS, USIG e Innovación/ASI, Áreas dueñas del dato (Transporte y Cultura), Responsables de canales (Boti, BAX, miBA), Vecinos y usuarios.

**12. Responsabilidades y autoridad del Project Manager** *(autoridad: propuesta)*. *Responsabilidades (§5.11.2):* elaborar y mantener el plan, coordinar las etapas, seguir cronograma, alcance, riesgos, recursos y costos, comunicar avances y desvíos y gestionar la aprobación de entregables. *Autoridad:* asignar y reasignar recursos dentro de la línea base aprobada; aprobar cambios **menores** (sin efecto en alcance, costo ni plazo de los gates); usar la **reserva de contingencia** con registro (§10.8); **escalar** al Sponsor todo cambio significativo y todo uso de la **reserva de gestión**, que requiere su aprobación.

**13. Requisitos de aprobación** *(propuesta; amplía §5.11.1 y §5.7.3)*. El **Sponsor institucional** aprueba el Charter, el alcance y los cambios significativos; **Hacienda / Presupuesto** aprueba la partida y la reserva de gestión; cada **gate** se aprueba por el Sponsor con las áreas dueñas del dato; la aceptación final exige: alcance cumplido, entregables y documentación completos, pruebas funcionales y de integración aprobadas, defectos críticos resueltos o aceptados formalmente.

---

## Anexo A – Charter ampliado

El texto actual del Charter (§5.1–5.12) pasa íntegro como anexo con la advertencia: *«En caso de diferencia, rigen los datos de las secciones 5 (resumen), 6, 9 y 10.»* Así se conserva todo el trabajo y los números **tienen una sola fuente**.

## Aclaración propuesta para §5.5.1 y §5.5.2 (perfil de hogar)

El Charter excluye *«funcionalidades de perfil personal avanzado o personalización basada en datos sensibles que no sean necesarias para los objetivos definidos»* (§5.5.2): la exclusión es **condicional**, no una contradicción con un perfil por hogar. Para que nadie la lea de otra manera, se propone agregar **una oración**:

> *«Quedan incluidos en el alcance el **perfil de hogar básico** (dato mínimo declarado por el propio hogar, opt-in) y la personalización que se derive de él; quedan **excluidos del MVP** la personalización avanzada y el uso de datos sensibles que no sean necesarios para los objetivos definidos.»*

## Qué limpiar antes de entregar (se vio en los originales)

- La **nota de chat** dentro de §5.4.2 («yo los mantendría…») y la sección «Resumen y borrador» del documento resumido.
- El título **«5.11.7 Res.ponsables»** (error de tipeo).
- Nombre del proyecto: dos versiones («Modernización del Mapa Interactivo de la Ciudad» vs «Modernización y Ampliación…»). Unificar.
