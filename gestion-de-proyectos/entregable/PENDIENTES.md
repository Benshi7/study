# Pendientes y decisiones abiertas

## Verificación
- [x] **Layout (verificado con LibreOffice 24.2, 12/10)**: el PDF de vista previa sale en `dist/TP_Cascada_Grupo01.pdf` (58 páginas). Verificado visualmente: carátula con logo, índice con números de página, figuras a ancho completo, tablas de riesgos y presupuesto sin cortes de palabra, Anexo A en hoja horizontal con encabezado repetido, encabezado/pie con 'Página X de Y'. Defectos encontrados y corregidos: (1) las figuras se recortaban a una línea por falta de `lineRule` explícito en el interlineado; (2) el índice no mostraba números de página; (3) columnas estrechas partían palabras (Impacto, Respuesta, Responsable). Solo falta confirmar en Word real (otras fuentes/saltos): abrir, aceptar la actualización de campos y revisar rápido.
- [ ] **Importación a Notion**: probar con una página chica antes de migrar todo (tablas anchas, imágenes, recuadros).
- [ ] Pegar la nómina real en `src/01-caratula.md` (línea «Integrantes del equipo») o directamente en Word.

## Transiciones
- Agregadas las frases puente 3 a 4, 7 a 8 y 8 a 9 (CAMBIOS sección E). Queda sin frase de enlace la carátula/índice con el resumen ejecutivo.

## Decisiones del grupo
- **Reserva de gestión**: concepto de la cátedra (Clase 4) que no está en el total. Decidir si se incluye y con qué criterio (referencia de la cátedra: 10 % del presupuesto; sobre la línea base serían USD 24.184).
- **Supuestos de la contingencia (punto 9.7)**: validar la conversión de probabilidad (10/30/50/70/90 %), las bandas de impacto, el costo semanal del equipo (USD 4.833) y los cálculos de impacto de cada riesgo; cambian directamente la contingencia (hoy USD 41.206, 20,5 % de los costos). También el criterio de probabilidad residual (Mitigar baja un nivel; Evitar / Mitigar, dos).
- **Segmento**: aplicado (hogares de la Ciudad como principal; visitantes y turistas como beneficiarios secundarios).
- **Canvas**: la figura de la Opción B es la referencia del punto 3; el listado de texto quedó alineado con ella (segmentos y socios clave).
- **Hitos y gates**: unificados en 8 (el punto 6.5 tiene 8 gates, uno por hito).
- **Fechas de los hitos 1 a 5 (nuevas)**: corregir las 7 superposiciones del Gantt obligó a mover los hitos 1 a 5 (14/04, 07/05, 08/06, 15/07, 03/08); los hitos 6 a 8 no cambian. Confirmar con el grupo. Alternativa: conservar las fechas del equipo y declarar los solapamientos como adelantos (con lo cual cambia el camino crítico de 126 días).
- **Roles del Gantt (columna Responsable)**: propuesta de un rol por actividad; el grupo debe revisarla.
- **Meses de dedicación del presupuesto vs. ventanas de los roles en el Gantt**: con un rol principal por actividad, las actividades de los analistas abarcan unas 1,6 mensualidades (presupuesto: 3), las de datos y GIS unas 3,3 (4), QA 0,6 (2) e infraestructura 0,6 (2). El presupuesto habla de dedicaciones parciales; conviene que el grupo confirme cómo se leen esos meses.
- **Tamaño del texto del Canvas (figura del punto 3)**: a ancho de página el texto queda en unos 4 pt. Evaluar una página apaisada para esa figura.
- **Rótulo «1. Carátula»**: aparece chico y centrado arriba de la portada para que el índice la liste; se puede quitar si prefieren portada sin rótulo.
- **Logo**: la imagen original traía debajo el nombre de un ciclo y licenciatura; se recortó. Confirmar que el logo y los datos de la portada son los que quieren.

## Observaciones sobre el contenido original (sin corregir)
Ver `CAMBIOS-vs-ORIGINALES.md` sección D y las propuestas de mejora en `trabajo-grupal/_propuestas/`.
