# Revisión de la versión completa de la compañera (round 2)

Fecha de análisis: 12/10/2026 · Entrega: 14/10/2026 · Original sin modificar (sha256 idéntico antes y después).

## Veredicto

- Es un **documento único con los 10 puntos**, con storytelling explícito: esa es su mayor virtud y cumple la letra de la consigna.
- **No debería ser la base.** Tiene tres problemas de fondo: Design Thinking afirma investigación real, el Gantt es una imagen que contradice la tabla de hitos del mismo documento, y las secciones 7 y 8 no usan la versión corregida (opción B).
- El formato es el punto más flojo: no hay índice automático, los títulos mezclan niveles y negritas manuales, y se usan cuatro tipografías.
- **Recomendación:** mantener nuestro maestro como base y **tomar de esta versión los puentes narrativos** (6 «Conexión narrativa»), no el resto.
- No pude renderizar el `.docx` (no hay LibreOffice): todo juicio visual queda pendiente.

## Inventario

| Dato | Valor |
|---|---|
| Longitud | ≈ 17.000 palabras incl. tablas; 25 tablas; 2 imágenes (portada y Gantt); estimación 50–60 pp. |
| Estructura | Carátula, índice, resumen/storytelling, Canvas, DT, Charter (5.1–5.12), Gantt, Stakeholders, Comunicación, Riesgos, Presupuesto, Conclusión. Los 10 puntos están, en orden. |
| Reutilización (similitud léxica ≥ 80 %) | Resumen, Canvas y DT: ≈ 100 %/78 % de F2. Charter: ≈ 70 % de F1. Riesgos: ≈ 76 % de F1. Presupuesto: ≈ 42 % idéntico a F1 (el resto reescrito/ampliado). Gantt: casi todo reescrito. Estimación aproximada: los párrafos cortos no se miden. |
| Storytelling | 6 puentes «Conexión narrativa» (DT→Charter, Charter→Gantt, Gantt→Stakeholders, Comunicación→Riesgos, Riesgos→Presupuesto, Presupuesto→Conclusión). **Faltan:** Canvas→DT, Stakeholders→Comunicación, resumen→Canvas. |
| Anexos | Ninguno. No incluye el Excel del Gantt ni el análisis CPM. |

## Fortalezas

1. **Storytelling real:** el resumen explica el rol de cada herramienta y hay puentes entre secciones. Es lo que más cuesta lograr y la consigna lo exige.
2. **Documento autocontenido:** los 10 puntos y una conclusión en un solo archivo, con numeración de pie de página.
3. **Aritmética correcta:** presupuesto, mano de obra y riesgos cierran (ver tabla de números).

## Problemas

1. **Design Thinking presenta investigación como real:** «Se realizaron entrevistas y observaciones con vecinos y turistas» y «Se validaron los prototipos con usuarios representativos». Es un ejercicio simulado; además contradice el deck del propio equipo, que rotula el test como simulado. Es el riesgo académico más serio.
2. **Gantt incoherente.** La imagen de la sección 6.2 tiene 8 fases y ≈ 17 actividades (el Excel tiene 40), errores de rotulado visibles («Itnas», «Imas», «Baroa», «Banos», «Dama»; «4 hitos» usado como duración; «Arial» como responsable) y **7 de sus 8 hitos con fechas distintas de la tabla 6.3 del mismo documento**. Ejemplos: Charter 14/04 contra 10/04; Requerimientos 19/05 contra 01/05; Diseño 16/06 contra 26/05; Desarrollo 21/07 contra 02/07. Reemplaza el Gantt del documento base sin anexo.
3. **Secciones 7 y 8 sin la versión corregida:** la matriz de stakeholders tiene 14 filas de F1 (sin USIG/ASI, Hacienda ni socios con oferta geolocalizada). El PDF corregido tiene 15 y refleja la opción B.
4. **Formato (desde el XML):** sin campo de índice (índice tecleado con números de página fijos, no verificables); 6 títulos de nivel 1 en lugar de 10, con las secciones 5, 6, 9 y 10 en negrita manual y la 7 como título 2; 58 pseudo-títulos en negrita; 207 párrafos con estilo «Normal (Web)» (pegados de web); 4 familias tipográficas (Calibri, Times New Roman, Inter, Arial); sin saltos de página ni anexos horizontales.
5. **Defecto real en el resumen:** la palabra «estaciones» queda partida en dos párrafos con estilo Título 2 («…estac» / «iones de subte…»); además, párrafos de más de 300 caracteres con estilo de título aparecerán en el panel de navegación.
6. **Contingencia plana de 10 %:** igual que F1; no sale de los riesgos. Frente al pack (EMV ≈ USD 30.291 ≈ ARS 46,8 M al tipo de cambio de referencia) es menor que lo derivado (ARS 31,3 M). Supuesto del pack.
7. **Segmento y moneda:** no usa «hogares» (usa vecinos, turistas, usuarios del transporte); todo el presupuesto está en pesos sin tipo de cambio.

## Comparación con nuestro maestro

| Aspecto | Su versión | Maestro | Mejor |
|---|---|---|---|
| Orden/estructura 1–10 | Sí, pero niveles de título inconsistentes | 10 H1 en orden + anexos | Maestro |
| Índice | Manual, páginas tecleadas | Campo automático (páginas al actualizar en Word) | Maestro |
| Canvas | Lista de texto (F2) | Texto de F2 + figura opción B | Maestro |
| Design Thinking | Texto corto con afirmaciones de investigación real | Capítulo con figuras, investigación **simulada** rotulada | Maestro |
| Charter | F1 (largo) | F1 (largo) | Igual |
| Gantt | Imagen incoherente, sin anexo | Resumen + Anexo A con las 40 actividades del Excel | Maestro |
| Stakeholders / Comunicación | F1 | PDF corregido (opción B) | Maestro |
| Riesgos / Presupuesto | F1 con retoques | F1 tal cual | Igual |
| **Storytelling** | **6 puentes + resumen + conclusión** | Resumen y conclusión de F2; faltan transiciones 3→4 y 8→9 | **Su versión** |
| Pie de página | Número simple | «Página X de Y» | Maestro |
| Tipografía/estilos | 4 familias, estilos mezclados | Un archivo de tokens | Maestro |

## Números recalculados

| Control | Resultado |
|---|---|
| Presupuesto base 190 + 35 + 18 + 30 + 12 + 28 | $313.000.000 ✓ |
| Contingencia 10 % y total | $31.300.000 y $344.300.000 ✓ (idéntico a F1) |
| Subtotales de cada sub-tabla (10.3–10.7) | Todos cierran con su línea total ✓ |
| Mano de obra: meses × costo mensual (9 filas) y total | Todas correctas; suma $190.000.000 ✓ |
| Riesgos: probabilidad × impacto (15 filas) | 15/15 coinciden; niveles según umbrales (Alto 10–16, Crítico 17–25) ✓ |
| Hitos de la tabla 6.3 contra el Excel | 8/8 coinciden ✓ |
| Hitos de la imagen del Gantt contra la tabla 6.3 | **7/8 distintos** ✗ (ver problema 2) |
| Camino crítico | Se nombra en el texto de riesgos pero el documento no lo calcula ni lo muestra |

Duraciones de mano de obra contra Gantt (3 meses de analistas, 2 de QA): igual desajuste que F1; no es un error nuevo.

## Mapa de fusión

- **Base:** maestro (`entregable/dist/TP_Cascada_Grupo01.docx`).
- **Tomar de esta versión:**
  - Los 6 puentes «Conexión narrativa», adaptados al orden final del maestro (las secciones 7 y 8 son las del PDF corregido, así que el puente 7→8 y 8→9 hay que redactarlos).
  - Contrastar su «Conclusión General» (≈ 140 palabras) con la de F2 y quedarse con la mejor.
- **Descartar:** la imagen del Gantt, los párrafos de DT con investigación real, las secciones 7 y 8 de F1, los estilos «Normal (Web)» y las tipografías mezcladas.

## Plan de 2 días (12 → 14/10)

**Bloqueantes**
1. Acordar la base (maestro) con quien armó esta versión, mostrando los hitos contradictorios del Gantt y la sección de DT.
2. Pegar la nómina y abrir el `.docx` en Word: actualizar el índice (campos), revisar saltos de página y anchos de tabla.
3. Confirmar que DT sigue rotulado como simulado en todo el documento.

**Nota**
4. Incorporar los puentes de ella y redactar 3→4 y 8→9.
5. Decidir la reserva de contingencia (plana o desde los EMV) y declararlo en el texto.
6. Alinear segmento («hogares de la Ciudad») y moneda con lo decidido.

**Defensa**
7. Preparar respuestas para: por qué 10 % plano, qué es el camino crítico y por qué da 126 días hábiles, por qué DT es simulado, por qué opción B.

## No pude juzgar (sin render)

Distribución real de páginas y su cantidad exacta, aspecto de las fuentes incrustadas (Inter) y del estilo «Normal (Web)», espaciados, cortes de tabla entre páginas, calidad de impresión de las 2 imágenes y si los números de página del índice tecleado son correctos.

## Nota de método

Los saltos de línea dentro de las entradas del índice parecían «pegados» en la conversión a texto, pero el XML tiene saltos explícitos (`<w:br>`): es un artefacto de la extracción, no un defecto, y no cuenta en este informe.

## Revisión visual (con LibreOffice)

Convertida a PDF con LibreOffice 24.2 (copia en `render/`): **66 páginas** (nuestro maestro: 58). Miré 6 páginas (carátula, índice, hitos, Gantt, matriz de comunicación y la 13 por texto). Los saltos de página dependen de las fuentes; en Word real pueden variar.

- **Carátula:** la más cuidada de las dos (banner, foto de la ciudad, recuadros). El título es distinto del que usan los demás documentos («Proyecto Integrador de Gestión de Proyectos: Modernización y Ampliación del Mapa…») y la nómina figura completa en la portada.
- **Índice:** es tipeado, no un campo. Los números no coinciden con la paginación real: Charter «pág. 5» (real: 7), Gantt «pág. 26» (real: 38), Stakeholders «pág. 29» (real: 43), Comunicación «pág. 32» (real: 47), Riesgos «pág. 35» (real: 52). Los subapartados no llevan número. Puede diferir en Word, pero no por 10 a 17 páginas.
- **Títulos y fuentes:** el PDF usa Calibri, una sustituta de Arial y DejaVu Sans: al menos tres familias. Los apartados 5, 6, 9 y 10 siguen con negrita manual, como detectó la revisión XML.
- **Gantt:** es una captura de baja resolución; las etiquetas son diminutas a ancho de página y se leen los errores de rotulado («Itnas», «Baroa», «Arial» como responsable).
- **Tablas:** la matriz de comunicación parte palabras («funcionamient/o», «Capacitacione/s») y se corta entre páginas con encabezado repetido.
- **Resto de edición:** en 5.4 sigue el párrafo «hay una diferencia importante respecto de lo que tenían originalmente…», una nota dirigida al equipo. Nuestro maestro la quitó.

**Veredicto de prolijidad frente al maestro:** el maestro tiene índice automático con números correctos, un solo juego de estilos, figuras a ancho completo, anexo horizontal y tablas sin cortes de palabra. La versión de la compañera gana solo en la carátula y en las frases puente. Para la entrega conviene la carátula de ella dentro de nuestro maestro.
