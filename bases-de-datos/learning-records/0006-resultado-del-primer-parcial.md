# Primer parcial aprobado con 5, y lo que quedó flojo

Bruno rindió el 1er parcial el 2026-09-24 (en papel, una hora) y lo **aprobó con 5**
(la nota mínima para aprobar es 4). Sintió que podía haber sacado más: se puso nervioso y
se bloqueó con la clave primaria compuesta.

**Resultado por parte, comparado con la resolución oficial:**

- **Teoría (4 multiple choice):** P3 (N:M) y P4 (índice primario vs. secundario), bien.
  P1 mal: contestó Durabilidad, y la respuesta es **Atomicidad**. Asoció "error" con
  "la operación no se ejecutó". P2: contestó Dependencia Parcial. Como el enunciado marcaba
  `id_ciudad` como PK, la clave es compuesta y la respuesta parcial se puede defender
  (incumple 2FN antes que 3FN).
- **Normalización:** llegó a las 4 tablas correctas (ORDEN, CLIENTE, ARTICULO y la tabla
  de detalle), todas con PK y sin campos derivados. El error fue dejar `cant` en ORDEN y
  `precio` en ARTICULO. La solución oficial pone **los dos en ORDEN_DETALLE**.
- **DER a MER:** coincide con la solución oficial. Resolvió bien el multivaluado (TELEFONOS
  como tabla aparte) y la FK de la relación 1:N en PEDIDO.

**Qué reforzar para el 2do parcial:**

1. **En la tabla de detalle van la cantidad y el precio, siempre.** El precio se guarda en el
   renglón por historicidad: es el precio al momento de la venta. Es la convención de la
   cátedra (`RenglonFact` en `unidad 3.pdf`), aunque los datos del ejercicio permitan otra cosa.
2. **Cuando la PK compuesta traba, normalizar paso a paso.** Lo que queda en la "primera
   tabla" después de 2FN es la tabla de detalle, con su cantidad. Saltar directo a 3FN le
   hizo perder esa pista.
3. **Marcar las FK de forma explícita** como `(PK, FK)` o `(FK)`, igual que el docente. Un
   `#` suelto es ambiguo.
4. **ACID con precisión:** la atomicidad es todo o nada (rollback ante un error a mitad de la
   operación). La durabilidad solo aplica a lo que ya está confirmado.
5. **La cardinalidad se lee de las marcas del diagrama**, no se deduce del negocio.

**Evidencia:** fotos del examen, de sus respuestas y de la resolución del docente
compartidas en la sesión del 2026-10-01; nota del SIU: "1er examen Parcial — 5 (Cinco) — Aprobado".

Relacionado: [[0004-alcance-real-del-primer-parcial]], [[PARCIAL.md]]
