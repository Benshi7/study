# Base F1: qué se conserva, agrega, reemplaza y quita

Documento base: `Proyect Charter y demas puntos.docx` («F1», ≈ 10.270 palabras). Solo describe la diferencia con F1; no contiene propuestas de mejora. Conteos de palabras aproximados (se cuentan títulos y tablas; las leyendas, el encabezado y el pie no cuentan). Generados con `node tools/word-counts.mjs`.

## Por sección

| Parte | Estado | Palabras F1 → consolidado | Detalle y motivo |
|---|---|---|---|
| Cabecera e índice manual de F1 | **Quitado / reemplazado** | 224 → 62 (carátula) + índice automático | El índice manual tenía páginas inventadas y un renglón cortado; la cabecera eran imágenes con la nómina. Ahora: carátula de texto + índice de Word |
| 1 Carátula | **Agregado** | — → 62 | Datos de F1, F2 y F3; nómina como `[Integrantes del grupo]` |
| 2 Índice | **Agregado** | — → automático | Campo de Word (niveles 1–3) |
| Resumen ejecutivo | **Agregado** (de F2) | — → 504 | Es el storytelling que F2 ya tenía; la consigna pide continuidad entre los puntos |
| 3 Canvas | **Agregado** | — → 244 + figura | Texto de F2 + tablero de la Opción B. F1 no tiene este punto |
| 4 Design Thinking | **Agregado** | — → 673 + 5 figuras | Reescritura del deck como capítulo; presentado como investigación simulada. F1 no tiene este punto |
| 5 Project Charter | **Conservado** | 5.716 → 5.604 | Texto íntegro. Se quitó la nota de chat de §5.4 (132 palabras) y se normalizó la forma de los títulos (misma redacción) |
| 6 Gantt | **Conservado + agregado** | 430 → 503 | Se mantienen 6.1 a 6.5 y la imagen del Gantt. Se agrega el recuadro de resumen (≈ 70 palabras) con referencia al Anexo A y se quita el objeto `.emf` que no se podía incluir |
| 7 Stakeholders | **Reemplazado** (por el PDF «corregido») | 607 → 585 | Contenido del PDF de 4 páginas, tablas reconstruidas fila por fila |
| 8 Comunicación | **Reemplazado** (por el PDF «corregido») | 684 → 642 | Ídem |
| 9 Riesgos | **Conservado** | 1.366 → 1.366 | Sin cambios de texto (15 riesgos R01–R15) |
| 10 Presupuesto | **Conservado** | 1.241 → 1.241 | Sin cambios (en pesos, total $344.300.000) |
| Conclusión general | **Agregado** (de F2) | — → 65 | Cierre del documento |
| Anexo A (hoja horizontal) | **Agregado** | — → 1.897 | Cuatro hojas del Excel de Gantt, camino crítico e hitos; valores sin cambios |
| Anexo A. «Gantt completo en Excel» (renglón de F1) | **Reemplazado** | — | Ese renglón apuntaba a un anexo que no estaba en el documento; ahora el anexo existe |

## Totales

- F1 original: ≈ 10.270 palabras.
- Quitado de F1: ≈ 132 (nota de chat) + 224 (cabecera e índice manual) + 1.291 (F1 §7 y §8, reemplazadas por el PDF).
- Agregado: ≈ 62 + 504 + 244 + 673 + 65 + 1.897 + 70 (resumen del Gantt) + 1.227 (§7 y §8 del PDF) = ≈ 4.742.
- Consolidado: ≈ 13.390 palabras (≈ 11.490 sin el Anexo A), 23 tablas, 7 figuras + logo.

## Figuras y formato agregados

Business Model Canvas (Opción B), recorrido de Lucía, punto de vista y pregunta de diseño, perfil de usuario, mapa de ideas y prototipo de tres pantallas; leyendas «Tabla n»/«Figura n»; encabezado y pie «Página X de Y»; estilo neutro editable desde `theme.json`.
