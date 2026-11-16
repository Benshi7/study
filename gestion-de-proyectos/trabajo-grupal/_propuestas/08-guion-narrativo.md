# Guion narrativo: el hilo de las 10 secciones

> La consigna pide que el documento tenga un **storytelling** «dando continuidad y conexión entre los puntos». Este guion fija **qué cuenta cada sección**, **qué recibe de la anterior**, **qué hechos deben repetirse idénticos** (con un valor único que sale del modelo) y **cómo se pasa de una a otra**. Es la columna vertebral para el documento único (ver `07-formato-entrega.md`). Todo número sale de `tools/`; si algo cambia (por ejemplo, el tipo de cambio), se regenera y una prueba compara los valores contra el resto del pack.

## 1. El papel de cada sección

| # | Sección (consigna) | Qué responde | Qué recibe | Qué entrega |
|---|---|---|---|---|
| 1 | Carátula | Presentar el trabajo. | — | El nombre del proyecto: Modernización del Mapa Interactivo de la Ciudad. |
| 2 | Índice | Guiar la lectura de una sola historia. | Los 10 puntos de la consigna | Los 10 puntos en orden, con sus páginas. |
| 3 | Canvas del proyecto | ¿Qué negocio y para quién? | La pregunta de un hogar que no sabe a qué área acudir | El segmento hogares de la Ciudad y dos propuestas de valor (hogar y GCBA). |
| 4 | Aplicar Design Thinking | ¿El problema es real y qué solución lo resuelve? (investigación simulada) | El segmento y las propuestas de valor | Punto de vista, pregunta de diseño y un prototipo de tres pantallas: consultar, reportar y seguir. |
| 5 | Project Charter | ¿Qué hacemos, con qué límites y con qué metas? | El problema y el prototipo | Objetivo general, cuatro resultados, 8 hitos, presupuesto y riesgos de alto nivel, y los stakeholders principales. |
| 6 | Gantt del proyecto completo | ¿Qué tareas, en qué orden y cuánto duran? | Los cuatro resultados y los entregables | 40 actividades, 126 días hábiles de camino crítico y los 8 hitos con fecha. |
| 7 | Matriz de stakeholders | ¿A quién afecta y con cuánto poder e interés? | Las actividades del Gantt y los stakeholders del Charter | 15 stakeholders clasificados y una estrategia para cada uno. |
| 8 | Plan de comunicación | ¿Qué se comunica, a quién, cuándo y por qué canal? | La estrategia de la matriz de stakeholders | Una matriz de comunicación con responsable, frecuencia y canal por destinatario. |
| 9 | Gestión de riesgos - Matriz de riesgos | ¿Qué puede fallar y qué hacemos? | El camino crítico y los stakeholders | 19 riesgos con valor monetario esperado; su suma (USD 30.003) es la reserva de contingencia. |
| 10 | Gestión de costos - Presupuesto | ¿Cuánto cuesta? | Las duraciones del Gantt y la suma de los EMV | Presupuesto de USD 266.868 en USD (línea base USD 242.607 más reserva de gestión USD 24.261). |

## 2. Objetos del hilo (deben repetirse idénticos)

Son los hechos que un profesor puede cruzar entre secciones. Cada uno tiene **un valor canónico**; si una sección lo cita, cita este.

| Objeto | Valor canónico | Secciones donde aparece | Dónde se verificó |
|---|---|---|---|
| Nombre del proyecto | Modernización del Mapa Interactivo de la Ciudad | 1, 2, 3, 5 | Charter condensado y en plantilla |
| Segmento | Hogares de la Ciudad (cada hogar con su realidad) | 3, 4, 5, 7 | `05`, `05b`, Charter en plantilla |
| Funcionalidades núcleo | Consultar · Reportar · Seguir (las tres pantallas del prototipo); la vista de gestión es el lado del GCBA de «Seguir»; «Mi hogar» es opcional (decisión del grupo) | 4, 5, 6 | `05b` (prototipo), Charter §5.6 |
| Hitos | Charter aprobado 10/04/2026; Requerimientos aprobados 01/05/2026; Diseño aprobado 26/05/2026; Desarrollo completado 02/07/2026; Integraciones validadas 21/07/2026; Pruebas aprobadas 27/08/2026; Puesta en funcionamiento 09/09/2026; Cierre del proyecto 30/09/2026 | 5, 6 | `02-gantt`, Charter condensado y en plantilla |
| Duración | 126 días hábiles (CPM del Excel del equipo); 130 con las dependencias corregidas (opción A recomendada); las fechas son simuladas | 5, 6, 9 | `02-gantt`, `06`, Charter en plantilla |
| Presupuesto | USD 266.868 = línea base USD 242.607 (costos USD 212.604 + contingencia USD 30.003) + reserva de gestión USD 24.261; mantenimiento inicial posterior al cierre USD 17.948 | 5 (campo 12), 10 | `03-presupuesto`, memoria de cálculo, Charter en plantilla |
| Tipo de cambio | ARS 1.560,00 por USD (09/10/2026; a confirmar) | 5, 10 | `03-presupuesto`, Charter en plantilla |
| Riesgos principales | R10 (USD 4.808), R01 (USD 2.308), R02 (USD 2.308) | 5, 9, 10 | `04-riesgos`, `03-presupuesto` |
| Resultados del Charter | O1 Capa geográfica confiable; O2 Integración multicanal; O3 Reportes y seguimiento; O4 Gestión y experiencia del hogar | 3, 4, 5, 6 | `05`, Charter en plantilla |
| Simulación | Proyecto simulado con fines académicos: fechas ficticias (01/04/2026 a 30/09/2026), investigación de Design Thinking simulada y cifras estimativas | 1, 4, 5, 6, 10 | `05b`, Charter en plantilla |

## 3. Frases puente

Son las del pack (`07-formato-entrega.md`), con el contenido final: segmento hogares, investigación simulada, cuatro resultados, camino crítico del Excel y presupuesto en USD.

- **Apertura.** Este documento cuenta una sola historia: de la pregunta de un hogar que no sabe a qué organismo acudir, al proyecto, el cronograma, los riesgos y el presupuesto necesarios para resolverla.
- **2 → 3.** Nuestro punto de partida es una pregunta concreta: ¿cómo hace un hogar de la Ciudad, con su propia realidad, para enterarse de lo que le corresponde y reportar lo que ve sin saber de antemano a qué organismo ni por qué canal acudir?; el Canvas muestra quién usa, quién paga y qué recibe cada lado.
- **3 → 4.** Del Canvas surge una hipótesis de problema; Design Thinking, como investigación simulada con tres proto-personas, la convierte en un punto de vista y una pregunta de diseño y baja la idea a un prototipo de tres pantallas (consultar, reportar y seguir); la validación con hogares reales queda como actividad del proyecto.
- **4 → 5.** Con el problema y el segmento definidos, el Charter formaliza qué vamos a construir, con qué límites y con qué metas medibles.
- **5 → 6.** Para cumplir los objetivos del Charter ordenamos el trabajo en 40 actividades con duraciones y dependencias; su camino crítico fija la fecha de cierre.
- **6 → 7.** Las actividades del Gantt dependen de personas y organismos con distinto poder e interés; la matriz indica cuánto esfuerzo dedicarle a cada uno.
- **7 → 8.** La estrategia de la matriz de stakeholders se traduce en qué se comunica, a quién, con qué frecuencia y por qué canal.
- **8 → 9.** Cada actividad del camino crítico y cada relación con un stakeholder puede fallar; la matriz de riesgos los prioriza y cuantifica su valor monetario esperado.
- **9 → 10.** El presupuesto, expresado en USD con un tipo de cambio único, convierte el Gantt en dinero (personas × tarifa × duración) y los riesgos en una reserva de contingencia que sale de sus EMV.
- **Cierre.** Con los costos, las reservas y la línea base cerrados, volvemos a la pregunta inicial: cuánto cuesta, y en cuánto tiempo, que un hogar de la Ciudad deje de buscar a quién preguntar.

## 4. Resumen ejecutivo (borrador)

Hoy un hogar de la Ciudad que quiere saber qué ocurre en su cuadra, o reportar algo que vio, debe saber de antemano qué área responde y por qué canal; y después de reportar no ve qué pasó. Este proyecto, Modernización del Mapa Interactivo de la Ciudad, propone convertir el Mapa en una plataforma geográfica común: una capa que integra información oficial, la ofrece al Mapa y a canales como Boti, y permite consultar, reportar y seguir incidencias, mientras las áreas ven y gestionan lo que les corresponde.

El Canvas plantea una plataforma de dos lados: el hogar usa y no paga; el GCBA financia y recibe una vista de gestión y una capa reutilizable. Design Thinking, una investigación simulada con tres proto-personas, bajó la idea a un prototipo de tres pantallas: consultar, reportar y seguir. El Charter fija el alcance, cuatro resultados y 8 hitos, desde el Charter aprobado (10/04/2026) hasta el cierre (30/09/2026).

El Gantt ordena 40 actividades y su camino crítico es de 126 días hábiles. La matriz de stakeholders y el plan de comunicación definen a quién se informa, cuándo y por qué canal. La matriz de riesgos reúne 19 riesgos y la suma de sus valores esperados (USD 30.003) es la reserva de contingencia. El presupuesto, en USD con un tipo de cambio único de ARS 1.560,00, suma USD 266.868 (línea base USD 242.607 más reserva de gestión de USD 24.261), más USD 17.948 de mantenimiento inicial posterior al cierre. Es una simulación académica: las fechas y las cifras son estimativas.

## 5. Tabla de consistencia

Antes de entregar, buscar cada valor en cada sección de la lista y comprobar que coincide palabra por palabra. Las pruebas de `tools/` ya lo verifican contra los documentos del pack (Charter, Gantt, presupuesto, riesgos, Design Thinking); en el documento final hay que repetir la verificación a mano.

| Objeto | Valor canónico | Debe aparecer en las secciones | Verificado en |
|---|---|---|---|
| Nombre del proyecto | Modernización del Mapa Interactivo de la Ciudad | 1, 2, 3, 5 | Charter condensado y en plantilla |
| Segmento | Hogares de la Ciudad (cada hogar con su realidad) | 3, 4, 5, 7 | `05`, `05b`, Charter en plantilla |
| Funcionalidades núcleo | Consultar · Reportar · Seguir (las tres pantallas del prototipo); la vista de gestión es el lado del GCBA de «Seguir»; «Mi hogar» es opcional (decisión del grupo) | 4, 5, 6 | `05b` (prototipo), Charter §5.6 |
| Hitos | Charter aprobado 10/04/2026; Requerimientos aprobados 01/05/2026; Diseño aprobado 26/05/2026; Desarrollo completado 02/07/2026; Integraciones validadas 21/07/2026; Pruebas aprobadas 27/08/2026; Puesta en funcionamiento 09/09/2026; Cierre del proyecto 30/09/2026 | 5, 6 | `02-gantt`, Charter condensado y en plantilla |
| Duración | 126 días hábiles (CPM del Excel del equipo); 130 con las dependencias corregidas (opción A recomendada); las fechas son simuladas | 5, 6, 9 | `02-gantt`, `06`, Charter en plantilla |
| Presupuesto | USD 266.868 = línea base USD 242.607 (costos USD 212.604 + contingencia USD 30.003) + reserva de gestión USD 24.261; mantenimiento inicial posterior al cierre USD 17.948 | 5 (campo 12), 10 | `03-presupuesto`, memoria de cálculo, Charter en plantilla |
| Tipo de cambio | ARS 1.560,00 por USD (09/10/2026; a confirmar) | 5, 10 | `03-presupuesto`, Charter en plantilla |
| Riesgos principales | R10 (USD 4.808), R01 (USD 2.308), R02 (USD 2.308) | 5, 9, 10 | `04-riesgos`, `03-presupuesto` |
| Resultados del Charter | O1 Capa geográfica confiable; O2 Integración multicanal; O3 Reportes y seguimiento; O4 Gestión y experiencia del hogar | 3, 4, 5, 6 | `05`, Charter en plantilla |
| Simulación | Proyecto simulado con fines académicos: fechas ficticias (01/04/2026 a 30/09/2026), investigación de Design Thinking simulada y cifras estimativas | 1, 4, 5, 6, 10 | `05b`, Charter en plantilla |

**Cómo usarla:** al terminar de armar el documento, abrir la búsqueda de Word (Ctrl+F) y buscar «USD 266.868», «ARS 1.560,00», «126 días hábiles», «Hogares de la Ciudad» y las fechas de los hitos: cada una debe aparecer solo con el valor de esta tabla.
