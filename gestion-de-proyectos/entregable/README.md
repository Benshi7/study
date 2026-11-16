# Entregable consolidado — TP Cascada (Grupo 01)

Un solo documento Word (`dist/TP_Cascada_Grupo01.docx`) generado desde archivos Markdown (`src/`). Consolida el contenido **original** del equipo: las propuestas de mejora todavía no están aplicadas.

## Estructura

```
src/            una fuente Markdown por punto de la consigna (+ resumen ejecutivo, conclusión y Anexo A)
img/            PNG usados por el documento (se generan desde img-src/; el Gantt, las fases, los hitos, el mapa de calor, el presupuesto y los stakeholders se generan desde los datos: data/gantt.json y las tablas de src/)
img-src/        figuras en HTML (Canvas, Design Thinking, logo) + theme.css (generado desde theme.json)
theme.json      ÚNICA fuente de colores, tipografías y tamaños (documento y figuras)
build/          build-docx.mjs (md → docx) y figures.mjs (HTML → PNG con Chrome headless)
build.sh        reconstruye todo (./build.sh) o sin figuras (./build.sh --fast)
tests/          25 pruebas (npm test): estructura, fidelidad contra los originales, tema, privacidad
tools/          gen-sources.py y gen-annex.py (extracción única/re-ejecutable), word-counts.mjs
dist/           TP_Cascada_Grupo01.docx y TP_Cascada_Grupo01.md (+ dist/img) para Notion
```

Documentos de seguimiento: `CAMBIOS-vs-ORIGINALES.md` (toda desviación respecto de los originales), `PENDIENTES.md` (decisiones y puntos abiertos) y `BASE-F1-agregar-quitar.md` (qué se agrega, reemplaza y quita respecto del archivo base).

## Ciclo editar → construir

1. Editar `src/NN-*.md` (en cualquier editor o en Notion; ver abajo).
2. `./build.sh --fast` (o `./build.sh` si cambiaron las figuras o `theme.json`).
3. `npm test` (corre las 25 pruebas; deben pasar).
4. Abrir `dist/TP_Cascada_Grupo01.docx` en Word. Al abrirlo Word pregunta si actualizar los campos: **aceptar** (genera el índice con números de página). Si no pregunta: clic derecho sobre el índice → *Actualizar campo* → *Actualizar toda la tabla*.

### Convenciones de las fuentes Markdown

- `# N. Título` = Título 1 (los 10 puntos de la consigna, numerados a mano como en los originales). Un `#` sin número (Resumen ejecutivo, Conclusión general, Anexo A) = título sin numeración que también entra en el índice.
- `## N.k` y `### N.k.j` = Título 2 y 3 (la numeración se escribe en el texto; una prueba verifica que no haya saltos ni duplicados).
- `Tabla: texto` en una línea justo antes de una tabla = leyenda de esa tabla. Sin esa línea, la leyenda se toma del título más cercano. Las leyendas «Tabla n» y «Figura n» se numeran solas.
- `![texto alternativo](img/archivo.png)` = figura; el texto alternativo es también la leyenda.
- `[[TOC]]` = índice automático.
- `> cita` = recuadro destacado.
- La carátula (`01-caratula.md`) se maqueta centrada: el primer párrafo solo en negrita es el subtítulo, el segundo es el título del proyecto.

## Notion

`dist/TP_Cascada_Grupo01.md` es una sola página en Markdown sin HTML (las leyendas pasan a cursiva y `[[TOC]]` es una lista simple). Para usarla: importar el `.md` en Notion y subir las imágenes de `dist/img/` si no se enlazan solas. **No verifiqué cómo Notion muestra tablas anchas ni imágenes**: conviene probar primero una importación chica. Cuando se quiera volver a Word, lo más seguro es copiar los cambios de vuelta a `src/` y reconstruir (el docx se arma desde `src/`, no desde Notion).

## Aplicar la estética blanca y rosa más adelante

1. Editar solo `theme.json` (colores `accent`, `heading`, `tableHeaderFill`, etc.; fuentes; tamaños).
2. `./build.sh` (regenera `img-src/theme.css`, vuelve a dibujar las figuras y reconstruye el docx).
3. Una prueba verifica que todo color y tipografía del XML salga de `theme.json`, así que no quedan colores sueltos.

## De dónde sale cada parte

| Punto | Fuente |
|---|---|
| 1 Carátula | cabecera y datos de `TP Grupo 01.docx`, `Proyecto Integrador…docx` y `Proyect Charter y demas puntos.docx`; logo recortado de este último |
| 2 Índice | campo de índice automático de Word |
| Resumen ejecutivo, Conclusión general | `Proyecto Integrador…docx` |
| 3 Canvas | texto de `Proyecto Integrador…docx` + figura del tablero de la Opción B (`tp/assets/canvas-data.js`) |
| 4 Design Thinking | deck `Design Thinking - Mapa Interactivo GCBA.pdf` reescrito como capítulo, con figuras en HTML |
| 5, 6, 9, 10 | `Proyect Charter y demas puntos.docx` (base) |
| 7, 8 | `Stakeholders_y_Plan_de_Comunicacion_CORREGIDO (1).pdf` (reemplaza 7 y 8 del base) |
| Anexo A | `Gantt_y_Camino_Critico_Hitos_Anexo_Punto_6.xlsx`, tablas idénticas al Excel |

## Verificación

- `npm test`: 25 pruebas. Comprueban, entre otras cosas, que ninguna palabra del texto de §5, 6, 9 y 10 se perdió respecto de los `.docx` originales (salvo la nota de chat registrada), que las tablas de §7–8 coinciden con el PDF, que el Anexo A coincide celda por celda con el Excel, y que los originales no cambiaron (`tests/originals.sha256`).
- **Layout visual: verificado con LibreOffice 24.2** (ver `PENDIENTES.md`); en Word real puede variar algún salto de página. Hay que abrir el `.docx` en Word y revisar saltos de página, anchos de tabla y el índice.
- Validación del paquete: el docx pasa el validador de esquema OOXML (XSD) de la skill docx (`validate.py`, 25 partes válidas, 0 errores). Se ejecutó con un entorno Python temporal; no es parte del flujo.
- Las figuras se revisaron como imágenes (Canvas, recorrido, ideas, prototipo y logo; el perfil y el punto de vista se generan con el mismo CSS).

## Herramientas instaladas

Solo dentro de `entregable/` (`npm`): `docx`, `markdown-it`, `adm-zip`, `@xmldom/xmldom`, `puppeteer-core` (usa el Chrome headless que ya existía en `~/.cache`; no descarga navegadores).

## Vista previa en PDF y números de página del índice

`./build.sh --fast --toc-pages` rellena los números de página del índice (render con LibreOffice + `build/fill_toc_pages.py`, requiere `soffice` y PyMuPDF: `PDF_PY=/ruta/a/python ./build.sh --fast --toc-pages`) y escribe `dist/TP_Cascada_Grupo01.pdf`. Word igualmente los recalcula al abrir. Sin ese flag el índice queda con entradas pero sin números hasta actualizar campos.
