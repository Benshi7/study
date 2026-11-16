# **Tp entregable**

| **Universidad de la Ciudad de Buenos Aires** <br> Taller de Gestión de Proyectos |
|---|

| **Proyecto Integrador de Gestión de Proyectos:   Modernización y Ampliación del Mapa Interactivo de la Ciudad de Buenos Aires** |
|---|

| **Contexto Institucional:** Gobierno de la Ciudad de Buenos Aires (GCBA) |
|---|

| **INTEGRANTES (GRUPO 01)** <br> [nómina omitida en la copia de análisis] |
|---|

| **Fecha:** 14 de Octubre de 2026 | **Año Lectivo:** 2026 |
|---|---|

# ÍNDICE

- Resumen Ejecutivo

- Canvas del Proyecto

- Aplicación de Design Thinking

- Project Charter (Acta de Constitución del Proyecto)

- Identificación del Proyecto

  - Propósito y Justificación

  - Objetivos del Proyecto

  - Alcance Incluido y Excluido

  - Entregables Principales

  - Gobernanza y Roles

- Cronograma y Gantt del Proyecto Completo

- Matriz de Stakeholders

- Plan de Comunicación

- Gestión de Riesgos - Matriz de Riesgos

- Gestión de Costos - Presupuesto Total

- Conclusión General

# Resumen Ejecutivo

## Storytelling del Proyecto

## El presente trabajo de gestión nace de una necesidad ciudadana concreta: la fragmentación de la información pública georreferenciada en la Ciudad Autónoma de Buenos Aires. Actualmente, los vecinos y visitantes deben navegar por múltiples aplicaciones y páginas para hallar datos cotidianos clave como puntos culturales, paradas de colectivos, estaciones de subte, obras en la vía pública o realizar reportes de incidencias urbanas.

## Para dar respuesta a este desafío con un enfoque metódico de project management, la narrativa de este proyecto sigue una secuencia lógica y estructurada donde cada herramienta metodológica cumple un propósito y utilidad específica:

- **Canvas del Proyecto:** Se elabora para conceptualizar de forma holística y en una sola vista el modelo estratégico del proyecto. Sirve para alinear a los actores clave, validar la propuesta de valor y asegurar la factibilidad inicial identificando socios, recursos, canales y la estructura básica de costos e ingresos.

- **Design Thinking:** Se aplica para empatizar profundamente con los ciudadanos y comprender sus verdaderos dolores en la interacción con el entorno urbano. Sirve para definir el problema real, idear soluciones innovadoras, prototipar y testear tempranamente la interfaz y el módulo colaborativo antes de comprometer recursos de desarrollo masivos.

- **Project Charter (Acta de Constitución):** Se redacta para formalizar institucionalmente el proyecto y autorizar el inicio del trabajo. Sirve para establecer el acuerdo marco entre la dirección y el equipo, fijando la visión, los objetivos alineados con los hallazgos del Design Thinking, el alcance permitido/excluido, la gobernanza y la autoridad del Project Manager.

- **Cronograma y Diagrama de Gantt (Waterfall):** Se planifica para ordenar temporalmente las 8 fases del proyecto y sus hitos de control (Gates). Sirve para prever dependencias técnicas, coordinar los plazos de las entregas intermitentes, controlar el progreso físico del trabajo y asegurar el cumplimiento de la fecha de cierre acordada en el Project Charter.

- **Matriz de Stakeholders:** Se construye para identificar y clasificar a todas las personas y organizaciones impactadas o con capacidad de influencia. Sirve para planificar estrategias de involucramiento según el nivel de poder e interés de cada grupo, garantizando el apoyo de los sponsors y la adopción activa por parte de los vecinos.

- **Plan de Comunicación:** Se diseña para estructurar el flujo de información de forma transparente y oportuna entre los involucrados. Sirve para definir frecuencias, canales y responsables de cada reporte o reunión, minimizando malos entendidos y alineando las expectativas operativas y comunitarias durante todo el ciclo de vida.

- **Gestión de Riesgos (Matriz de Riesgos):** Se ejecuta para identificar, evaluar y monitorear proactivamente las incertidumbres técnicas, operativas y de alcance. Sirve para definir acciones preventivas y planes de contingencia específicos, reduciendo el impacto de imprevistos sobre la calidad, el tiempo y el costo de la plataforma.

- **Presupuesto y Gestión de Costos:** Se cuantifica para estimar detalladamente la inversión requerida en capital humano, licencias, datos e infraestructura, incluyendo una reserva del 10%. Sirve para asegurar la viabilidad financiera, justificar la asignación de recursos públicos y controlar las desviaciones monetarias para garantizar el éxito institucional del proyecto.

# Canvas del Proyecto

## Como primer paso para estructurar estratégicamente la plataforma multilateral y articular a los actores clave, se desarrolla el Canvas del Proyecto:

- **Socios Clave:** Ministerio de Modernización, Secretaría de Transporte, Ministerio de Cultura, comunas de CABA, prestadores de transporte (Subte/Autobuses) y áreas de soporte de IA conversacional (Boti/BAX).

- **Actividades Clave:** Desarrollo de capa geográfica única (GIS), integración de APIs oficiales, desarrollo de módulo de reportes ciudadanos y validación colaborativa, pruebas de usabilidad y campañas de difusión.

- **Propuesta de Valor:** Plataforma geográfica común y centralizada que unifica en un solo mapa interactivo puntos de interés cultural, paradas de colectivos, estaciones de subte y un canal directo de reporte y seguimiento colaborativo de incidencias urbanas.

- **Relaciones con el Ciudadano:** Transparente, participativa, bidireccional y accesible a través de múltiples canales (Mapa Web, Boti, BAX).

- **Segmentos de Usuarios:** Vecinos de CABA, visitantes/turistas, usuarios del transporte público, actores culturales y áreas operativas de gestión de la Ciudad.

- **Recursos Clave:** Infraestructura de servidores y bases de datos GIS, equipo multidisciplinario de desarrollo y datos, APIs institucionales y canal conversacional Boti.

- **Canales:** Mapa Interactivo Web/Mobile, Boti (WhatsApp), BAX y portales de difusión institucional de CABA.

- **Estructura de Costos:** Honorarios del equipo (RRHH), licenciamiento y herramientas tecnológicas, infraestructura GIS y nube, capacitación, comunicación y reserva de contingencia (10%).

- **Fuentes de Valor e Ingresos:** Valor público de alto impacto, optimización del gasto en soluciones fragmentadas y factibilidad de visibilidad patrocinada para comercios locales en etapas futuras.

# Aplicación de Design Thinking

## Para asegurar que la solución responda verdaderamente a los dolores del ciudadano, aplicamos el marco de Design Thinking antes de formalizar la gestión técnica del proyecto:

- **Empatizar:** Se realizaron entrevistas y observaciones con vecinos y turistas en CABA. Se detectó la frustración de tener que consultar distintas apps para saber cuándo llega el colectivo, dónde hay un evento cultural cercano o cómo reportar un corte de calle.

- **Definir:** El problema central es: *La dispersión de datos geográficos y la falta de un canal unificado con validación ciudadana impiden acceder ágilmente a servicios urbanos (transporte, cultura) y reportar incidencias del entorno*.

- **Idear:** Se ideó transformar el mapa consultivo estático en una *Capa Geográfica Común* reutilizable, que alimente diversos canales (incluyendo Boti) e incorpore reporte ciudadano con validación en tiempo real.

- **Prototipar:** Se diseñaron wireframes y prototipos interactivos del mapa con capas seleccionables (Cultura, Subtes, Colectivos, Reportes).

- **Testear:** Se validaron los prototipos con usuarios representativos, confirmando la alta valoración de la navegación unificada y la simplicidad para confirmar/desestimar reportes de otros usuarios.

## *Conexión Narrativa:* Las conclusiones del Design Thinking sirven como base directa para la redacción del Project Charter y la definición formal del alcance del proyecto.

# Project Charter (Acta de Constitución del Proyecto)

# Identificación del Proyecto

- **Nombre:** Modernización y Ampliación del Mapa Interactivo de la Ciudad de Buenos Aires.

- **Tipo:** Proyecto de Transformación Digital del Servicio Público.

- **Metodología:** Cascada (Waterfall) estructurada.

- **Duración:** 6 meses (24 semanas) | **Fecha de Inicio:** 10 de Abril de 2026 | **Fecha de Cierre:** 30 de Septiembre de 2026.  
|---|

# Propósito y Justificación

Convertir el mapa en una plataforma geográfica transversal que unifique el acceso a la cultura, transporte (colectivos y subtes) e información pública, y otorgue a la ciudadanía un rol activo en el mantenimiento de la calidad de vida urbana a través de reportes y validaciones colaborativas.

# Objetivos del Proyecto

- **Objetivo General:** Modernizar el Mapa Interactivo de CABA mediante una capa geográfica común integrada con canales digitales existentes y un sistema de reportes ciudadanos geolocalizados.

- **Objetivos Específicos:**

  - Centralizar la información geográfica de transporte, cultura e incidencias.

  - Implementar integraciones multicanal (Mapa Web, Boti, BAX) mediante APIs.

  - Desarrollar un módulo de reporte ciudadano georreferenciado y seguimiento de estado (Reportado → Validado → Derivado → Resuelto → Cerrado).

  - Incorporar mecanismos de validación colaborativa comunitaria.

# Alcance Incluido y Excluido

- **Incluido:** Desarrollo de capa GIS única, integración de paradas de colectivos, estaciones de subte y centros culturales, módulo de reporte e interacción colaborativa, vista de gestión para áreas operativas de CABA.

- **Excluido:** Reemplazo de Boti o sistemas internos preexistentes, desarrollo de navegador tipo Waze, ejecución física de obras de reparación.

# Entregables Principales

- Capa geográfica centralizada (GIS).

- APIs e integraciones de datos (Transporte, Cultura, Canales).

- Módulo de reportes y validación colaborativa.

- Vista de gestión para organismos del Gobierno.

- Documentación técnica, funcional y plan de capacitación.

# Gobernanza y Roles

- **Sponsor:** Autoridad Institucional de Modernización de CABA.

- **Project Manager:** [integrante nombrado en el original].

- **Equipos:** Tecnología, Datos y GIS, UX/UI, Calidad (QA), Comunicación y Representantes Comunitarios/Comunas.

# Cronograma y Gantt del Proyecto Completo

## La ejecución se articula secuencialmente bajo metodología Waterfall con 8 fases y sus respectivos Hitos de Control (Gates):

| Fase | Período de Ejecución | Hito de Control (Gate) | Fecha de Aprobación |
|---|---|---|---|
| **Fase 1: Inicio** | 10/04/2026 - 17/04/2026 | Gate 1: Charter Aprobado | 10/04/2026 |
| **Fase 2: Análisis y Requerimientos** | 18/04/2026 - 01/05/2026 | Gate 2: Requerimientos Aprobados | 01/05/2026 |
| **Fase 3: Diseño Funcional y Técnico** | 02/05/2026 - 26/05/2026 | Gate 3: Diseño Aprobado | 26/05/2026 |
| **Fase 4: Desarrollo de Componentes** | 27/05/2026 - 02/07/2026 | Gate 4: Desarrollo Completado | 02/07/2026 |
| **Fase 5: Integración de Fuentes y Canales** | 03/07/2026 - 21/07/2026 | Gate 5: Integraciones Validadas | 21/07/2026 |
| **Fase 6: Pruebas y QA** | 22/07/2026 - 27/08/2026 | Gate 6: Pruebas Aprobadas | 27/08/2026 |
| **Fase 7: Implementación y Despliegue** | 28/08/2026 - 09/09/2026 | Gate 7: Puesta en Funcionamiento | 09/09/2026 |
| **Fase 8: Cierre del Proyecto** | 10/09/2026 - 30/09/2026 | Gate 8: Cierre Formal Aprobado | 30/09/2026 |

*Conexión Narrativa:* Para cumplir con este cronograma, se requiere la articulación fluida con los involucrados analizados en la Matriz de Stakeholders.

# Matriz de Stakeholders

## Se realiza la clasificación estratégica según el level de Poder / Influencia e Interés:

- **Alto Poder / Alto Interés (Gestionar de Cerca):** Sponsor Institucional, Project Manager, Equipo Técnico y de Datos, Secretaría de Transporte, Ministerio de Cultura, Líderes de Boti/BAX.

- **Alto Poder / Bajo Interés (Mantener Satisfechos):** Autoridades de Auditoría y Comisiones Fiscalizadoras.

- **Bajo Poder / Alto Interés (Mantener Involucrados e Informados):** Vecinos de CABA, usuarios de transporte, organizaciones culturales, equipo UX/UI.

- **Bajo Poder / Bajo Interés (Monitorear):** Comercios locales y potenciales anunciantes futuros.

*Stakeholders Críticos:* Sponsor (respaldo presupuestario), Equipo GIS/Datos (disponibilidad de APIs) y Vecinos (adopción del módulo colaborativo).

# Plan de Comunicación

## Para mantener informados y coordinados a los stakeholders, se define la siguiente matriz de comunicación:

| Información / Comunicación | Destinatarios | Responsable | Frecuencia | Canal | Objetivo |
|---|---|---|---|---|---|
| **Avance General del Proyecto** | Sponsor, PM, Directores | PM | Quincenal | Informe / Reunión | Informar estado y desvíos |
| **Seguimiento Técnico y Tareas** | Equipo Técnico | Líder Técnico | Semanal | Tablero / Reunión | Controlar desarrollo |
| **Validación de Integraciones** | Áreas Operativas | Analista Funcional | Bisemanal | Mesas de trabajo | Validar APIs y fuentes |
| **Lanzamiento y Novedades** | Vecinos y Comunidad | Comunicación CABA | Pre-despliegue | Redes / Canales oficiales | Difundir uso |
| **Gestión de Cambios y Crisis** | Sponsor, PM, Afectados | PM | Inmediata | Reunión extraordinaria | Resolver eventos críticos |

# Gestión de Riesgos - Matriz de Riesgos

## Se evalúan los riesgos clave bajo la matriz de Probabilidad (1 a 5) × Impacto (1 a 5):

- **R01: Falta de disponibilidad de APIs de transporte/cultura (PxI: 3x5 = 15 - Alto)**.  
*Prevención:* Relevamiento técnico exhaustivo en fase de Análisis. *Contingencia:* Usar fuentes de respaldo o lotes de datos estáticos temporales.

- **R02: Baja calidad o desactualización de datos públicos (PxI: 4x5 = 20 - Crítico)**.  
*Prevención:* Controles automáticos de validación de esquema. *Contingencia:* Marcar datos no verificados o suspender temporalmente capas inconsistentes.

- **R03: Crecimiento no controlado del alcance (Scope Creep) (PxI: 4x5 = 20 - Crítico)**.  
*Prevención:* Proceso formal de Control de Cambios. *Contingencia:* Postergar requerimientos no esenciales para fases posteriores.

- **R04: Baja adopción del sistema de reportes por los vecinos (PxI: 3x3 = 9 - Medio)**.  
*Prevención:* Diseño enfocado en simplicidad y difusión clara. *Contingencia:* Ajustar incentivos de uso y retroalimentación interactiva.

*Conexión Narrativa:* La mitigación de estos riesgos se respalda económicamente a través de la reserva de contingencia prevista en el presupuesto.

# Gestión de Costos - Presupuesto Total

## El costo del proyecto se calcula estimando la dedicación de recursos, infraestructura y una reserva de contingencia del 10%:

| Rubro / Concepto de Gasto | Monto Estimado (ARS) |
|---|---|
| **1. Recursos Humanos** (PM, Analistas, Devs, GIS, UX, QA, Infra, Seguridad) | $190.000.000 ARS |
| **2. Desarrollo y Tecnología** (Herramientas, Licencias, Testing) | $35.000.000 ARS |
| **3. Datos, GIS e Integraciones** | $18.000.000 ARS |
| **4. Infraestructura, Nube y Seguridad** | $30.000.000 ARS |
| **5. Implementación y Capacitación** | $12.000.000 ARS |
| **6. Mantenimiento Inicial Post-Lanzamiento** | $28.000.000 ARS |
| **SUBTOTAL PRESUPUESTO BASE** | **$313.000.000 ARS** |
| **Reserva de Contingencia (10%)** | **$31.300.000 ARS** |
| **PRESUPUESTO TOTAL ESTIMADO** | **$344.300.000 ARS** |

# Conclusión General

## La implementación de este proyecto no sólo resolverá de forma eficiente la integración de información de interés público (puntos culturales, colectivos, subtes e incidencias), sino que sentará un precedente metodológico en el Gobierno de la Ciudad de Buenos Aires respecto a cómo encarar la transformación digital con metodologías sólidas de Gestión de Proyectos, garantizando la entrega dentro del tiempo, alcance y presupuesto previstos.

# **Resumen y borrador**

- **Proyecto:** Modernización del Mapa Interactivo de la Ciudad de Buenos Aires bajo metodología en cascada, con una duración estimada de 6 meses (abril a septiembre de 2026).

- **Propósito:** Transformar el mapa en una infraestructura geográfica común para centralizar información oficial, integrarse con canales digitales (como Boti y BAX) y habilitar la participación ciudadana.

- **Sistema de Reportes:** Incorpora un módulo para que los vecinos informen, validen y realicen un seguimiento de incidencias georreferenciadas en la vía pública (desde el reporte hasta su resolución).

- **Fases y Cronograma:** Se estructura en 8 etapas secuenciales (inicio, análisis, diseño, desarrollo, integración, pruebas, implementación y cierre) respaldadas por puntos de control o *gates*.

- **Gestión de Stakeholders:** Identifica actores clave —como el sponsor, el equipo de tecnología, áreas de gobierno y vecinos— estableciendo estrategias de gestión y planes de comunicación específicos.

- **Gestión de Riesgos:** Analiza 15 riesgos potenciales (destacando la calidad de datos y el control del alcance) y define acciones preventivas y planes de contingencia.

- **Presupuesto:** Estima un costo total de $344.300.000 ARS, que incluye recursos humanos, tecnología, infraestructura, mantenimiento inicial y una reserva de contingencia del 10%.