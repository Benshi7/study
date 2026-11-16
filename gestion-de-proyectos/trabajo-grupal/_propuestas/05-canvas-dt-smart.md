# Canvas (Opción B), Design Thinking y objetivos SMART

> **Propuesta.** Lo que sigue concreta la **Opción B** (plataforma de dos lados) con el segmento que **definió el equipo**: **hogares de la Ciudad en general**, cada uno con su propia realidad. Todo texto nuevo está marcado **(propuesta)**; ninguno proviene de investigación hecha. Ningún original fue modificado.

## 0. Decisión de segmento (resuelta por el equipo)

Las propuestas anteriores comparaban un segmento de hogares con niños con otro centrado solo en quienes reportan incidencias. El equipo aclaró que **no es ni una cosa ni la otra**: el segmento son los **hogares de la Ciudad en general**, y **cada hogar tiene su realidad**. Eso es justamente lo que justifica un perfil por hogar. Los «tipos de hogar» (hogar con niños, adulto mayor, persona con movilidad reducida) pasan a ser **personas** para Design Thinking y para las demos, no segmentos distintos del Canvas.

**Coherencia con el Charter.** El Charter excluye *«perfil personal avanzado o personalización basada en datos sensibles que no sean necesarias para los objetivos definidos»* (§5.5.2). La exclusión es **condicional**: un **perfil de hogar básico** (dato mínimo declarado por el propio hogar, opt-in) **no está excluido**. Se propone una oración aclaratoria en `01-charter-condensado.md`: *perfil de hogar básico INCLUIDO; personalización avanzada y datos sensibles no necesarios EXCLUIDOS del MVP*.

## 1. Segmento (plantilla de la Clase 1: *[quiénes] que [situación] y hoy [dolor]*) *(propuesta)*

- **Lado hogar (externo):** **Hogares de la Ciudad** *[quiénes]* que **conviven con su propia mezcla de necesidades** —trámites, servicios, obras y reclamos de su entorno, movilidad— *[situación]* y hoy **deben saber de antemano qué preguntar, a qué organismo y por qué canal, y no ven qué pasó con lo que reportan** *[dolor]*. (Dolor tomado de la visión del equipo y del §5.3 del Charter.)
- **Lado áreas (interno):** *áreas de gobierno que gestionan incidencias y servicios y hoy reciben información dispersa, duplicada y sin una referencia geográfica común.* (§5.3.1.)
- **Tercer lado, opcional:** socios con oferta geolocalizada (Banco Ciudad, Pase Cultural, DisfrutemosBA); **fuera de la primera implementación** (§5.5.2, §10.1).

## 2. Personas: cada hogar tiene su realidad *(propuesta; son escenarios, no segmentos)*

Sirven para las proto-personas de Design Thinking (ver `05b-design-thinking-revisado.md`), para decidir qué muestra el perfil de hogar básico y, más adelante, para un mock. Salen de los textos del propio equipo.

| Persona (escenario de uso) | Situación del hogar | Qué necesita | Cómo se vería |
|---|---|---|---|
| **Hogar con niños en edad escolar** | Se entera tarde de la inscripción o la vacunación | Saber qué le corresponde y cuándo, sin buscar | Aviso proactivo sobre el mapa, según el perfil de hogar básico (opt-in) |
| **Persona con movilidad reducida** | No sabe qué veredas de su recorrido están en obra | Recorridos y obras de su cuadra | Capa de obras y cortes sobre el recorrido |
| **Adulto mayor** | No sabe qué trámites le corresponden | Un lugar donde ver y pedir lo que le toca | Vista del hogar con trámites y puntos cercanos |
| **Vecino que reporta** | Se cruza con una incidencia y no sabe a quién avisar | Reportar y ver qué pasó | Reporte con ubicación y estados hasta el cierre |

Las cuatro comparten el **mismo segmento** (hogares de la Ciudad) y la **misma plataforma**; cambia lo que cada hogar ve primero.

## 3. Mapa de valor del lado hogar *(propuesta; formato Clase 1, p8–9)*

| Perfil del cliente | Mapa de valor |
|---|---|
| **Tareas:** enterarse de lo que le corresponde al hogar; informar una incidencia de su entorno; saber si otro ya la informó; consultar qué pasa en su cuadra. | **Propuesta de valor:** un único lugar sobre el mapa donde cada hogar ve lo que le corresponde y reporta y sigue lo que ve, con estado visible de principio a fin. |
| **Frustraciones:** no saber qué organismo o canal corresponde; enterarse tarde; no ver qué pasó con el reporte; información duplicada o desactualizada. | **Aliviadores:** punto único con ubicación; perfil de hogar básico (dato mínimo, opt-in) para mostrar primero lo que importa; estados visibles (Reportado → … → Cerrado). |
| **Beneficios esperados:** que el reporte llegue a quien corresponde; enterarse del avance; confiar en que el dato es oficial y actual. | **Generadores de satisfacción:** disponible también desde canales ya usados (Boti, BAX, **sujeto a validación técnica**). |

## 4. Mapa de valor del lado GCBA (quien financia y decide) *(propuesta)*

| Perfil del cliente | Mapa de valor |
|---|---|
| **Tareas:** gestionar incidencias y servicios con el equipo que tiene; coordinar áreas; justificar el presupuesto. | **Propuesta de valor:** la **vista de gestión** (dónde se concentran las incidencias y en qué estado están) y una **capa geográfica reutilizable** por otros servicios. |
| **Frustraciones:** cada área mantiene su solución geográfica; no hay una vista única; se reconstruye la capa en cada iniciativa (§5.3.1). | **Aliviadores:** una referencia geográfica común; costos evitados por no duplicar soluciones; menos esfuerzo para derivar casos. |
| **Beneficios esperados:** ver y priorizar; mostrar resultados con datos. | **Generadores de satisfacción:** datos para decidir dónde intervenir; la capa la consumen canales existentes. |

Son **dos propuestas de valor** porque son **dos segmentos**: quien usa (el hogar) no es quien paga (GCBA). Esa es la característica de la plataforma multilateral.

## 5. Canales, relación con el cliente e ingresos *(consistente con §5.8.4 y §10; propuesta)*

| Bloque | Texto propuesto |
|---|---|
| **Canales** | Web del Mapa; Boti (WhatsApp de la Ciudad); BAX (sujeto a validación técnica y a miBA) |
| **Relación con el cliente** | Autoservicio con seguimiento del reporte; avisos proactivos solo con opt-in; vista de gestión para las áreas |
| **Ingreso principal** | Partida de modernización de servicios digitales del GCBA (Hacienda / Presupuesto), primera implementación |
| **Costos evitados** | Cada área que deja de mantener su propia solución: argumento para el sponsor, a medir |
| **Socios (fase futura)** | Convenios con socios (comisiones, canjes) y espacios patrocinados: fuera del presupuesto actual |
| **Hogares** | No pagan |

El presupuesto se expresa en **USD** (ver `03-presupuesto`): quién paga no cambia, cambia la moneda de presentación.

## 6. Objetivos SMART *(propuesta)*

Se parte de la nota del propio Charter: agrupar los 8 objetivos en **4 resultados**. Cada uno se escribe con las cinco letras de la Clase 1 (específico, medible, alcanzable, relevante, con plazo). Las **metas numéricas son propuestas** y las líneas base están **«a medir»**.

| Resultado | Objetivos del Charter | Meta SMART *(propuesta)* | Plazo | ¿Cómo se verifica? |
|---|---|---|---|---|
| **O1 · Capa geográfica confiable** | 1 + 7 | La capa integra las **fuentes priorizadas** [completar: Transporte y Cultura son las que nombra el equipo] y el 100 % tiene responsable y frecuencia de actualización definidos. | 02/07/2026 (Gate 4) | Registro de fuentes con responsable y frecuencia |
| **O2 · Integración multicanal** | 2 | El Mapa y **al menos 1 canal conversacional** consumen la capa por API (BAX sujeto a validación técnica y a miBA). | 21/07/2026 (Gate 5) | Pruebas de intercambio de datos aprobadas |
| **O3 · Reportes y seguimiento** | 3 + 4 + 5 | El 100 % de los casos de prueba del flujo completo (reporte, validación, derivación, resolución, cierre) aprobados; los 6 estados operativos. | 27/08/2026 (Gate 6) | Informe de pruebas (actividades 27–32) |
| **O4 · Gestión y experiencia del hogar** | 6 + 8 | **≥ 3 áreas operativas** acceden a la vista de gestión y actualizan estados, y el hogar ve la información relevante de su entorno con el **perfil de hogar básico (opt-in)**; línea base de consultas evitables: a medir. | 09/09/2026 (Gate 7) | Registro de accesos y capacitación (actividades 34–35); prueba del perfil básico |

*Metas de uso post-cierre* (cantidad de reportes validados, hogares con perfil activo, tiempo de resolución): línea base **«a medir»**; no se afirman cifras.

## 7. Design Thinking: investigación simulada, rotulada y coherente

**Decisión del grupo.** Las entrevistas del deck son inventadas y **no hace falta hacer entrevistas reales**. Lo honesto y más defendible es **rotular la investigación como simulada** (ejercicio académico): proto-personas e hipótesis apoyadas en fuentes públicas, sin citas ni conteos inventados. En la defensa, la pregunta *«¿a cuántas personas entrevistaron y qué encontraron?»* tiene una respuesta coherente: *«es una investigación simulada, declarada como tal; la validación con hogares es la actividad 5 del Gantt»*.

**Qué hay que cambiar en el deck** (texto exacto, slide por slide, en `05b-design-thinking-revisado.md`): la portada pasa a «Hogares de la Ciudad × áreas del GCBA»; la slide de Empatizar pasa a **Investigación simulada** con hipótesis H1–H3; las proto-personas pasan de una a tres; «Mi hogar» queda como **decisión del grupo**; se quita el texto suelto «→ Cambiarla». También están ahí la trazabilidad con el Canvas, el Charter, el Gantt y los riesgos, y el texto de la sección 4 del documento.

*Criterios de la Clase 7: a confirmar con el PDF de la cátedra, que todavía no está en la carpeta.*

**Para después:** un *mock* de una funcionalidad (por ejemplo, el seguimiento de un reporte o la vista del hogar con su perfil básico) para mostrar cómo se vería. Se hace al final, con el documento cerrado; no se construye ahora.
