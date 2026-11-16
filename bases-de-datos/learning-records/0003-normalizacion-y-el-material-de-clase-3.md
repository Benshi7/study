# La Unidad 3 se arma sobre dos ejercicios con resolución oficial

Llegó el material de la **Clase 3 (Normalización)** más dos ejercicios **con la respuesta
del docente al lado**: el del 10/09/2026 (órdenes, resuelto en planilla) y el Ejercicio 1
(proveedores, resuelto en ERDPlus). Es la primera vez en el curso que tenemos enunciado y
corrección oficial para practicar el procedimiento completo.

**Qué se descubrió al cruzar las fuentes (no está en ninguna slide suelta):**

1. **El modelo 3FN de la slide 11 no elimina la anomalía 7.** El profe lista siete
   anomalías; 1FN mata la 1 y la 2, 2FN la 5 y la 6, 3FN la 3 y la 4. La séptima —el mismo
   producto con dos precios unitarios— sigue viva en `RenglonFact(#NFact, #CProd, Canti,
   PUnit)`. No es un error: se resuelve en las slides 14–15 decidiendo **dónde vive el
   precio**, que es una pregunta de negocio y no de forma normal.
2. **Hay tres modelos válidos para el precio**, los tres en 3FN: en el renglón (A),
   en el producto (B, slide 14) o con tabla de histórico y la fecha en la clave (C, slide 15).
   El ejemplo de facturación termina en A; el ejercicio del 10/09 usa B.
3. **En la resolución del 10/09, `PRECIO` se muda a `ARTICULOS` en el paso de 3FN.**
   Por la definición estricta de Elmasri (10.3.5) es un arreglo de **2FN**: `PRECIO` depende
   sólo de `NUM_ART`, que es parte de la clave compuesta. El modelo final queda correcto;
   lo que difiere es en qué paso se clasifica el arreglo. **Vale preguntárselo al docente**,
   porque define cómo espera la entrega.
4. **Hay dos versiones oficiales del Ejercicio 1** (Clase 2 slide 35 y
   `Clase3_Ej1_Proveedores_RS.erdplus`) con **estructura idéntica y nombres distintos**
   (`ID_PROVEEDOR` vs `Cod_Proveedor`, `MATERIAL_PROVEEDOR` vs `PROVEE`). Los nombres no se
   evalúan; la consistencia interna sí.

**Implicaciones para las próximas sesiones:**

- La cátedra evalúa **dos caminos distintos** hacia 3FN: normalizar desde una tabla sucia
  (dependencias funcionales) y mapear desde un DER (reglas de mapeo). Hay que practicar
  los dos y no mezclarlos.
- Cuando aparezca un conflicto entre el libro y la resolución del docente, se señala la
  diferencia **como pregunta para él**, nunca como "la cátedra se equivocó".
  Ver [[0001-conocimiento-previo-y-mision]].
- Falta el **Ejercicio 2** del 10/09 (armar una base de datos). El enunciado del PDF está
  como imagen y no se pudo extraer. Queda planteado al final de la lección 0026 y se
  desarrollará cuando Bruno lo tenga.

Relacionado: [[CURRICULUM.md]], [[0002-temario-completo-y-correccion-de-alcance]]
