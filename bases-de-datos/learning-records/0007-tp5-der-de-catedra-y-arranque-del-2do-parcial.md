# TP5: el DER lo da la cátedra, y el 2do parcial arranca por SQL

El 2026-10-15 los docentes aclararon que el TP5 Clínica se resuelve sobre **su** DER
(`raw/TP5/TP DDL-DML  Clinica con DER.pptx`, slide 8), no sobre uno modelado por el grupo.
El foco del TP pasa a ser los scripts: DDL Desa/Prod, insert-values, insert-select, vistas y
las seis consultas. Hay una semana más para la entrega, y Bruno tiene que dominarlo para el
2do parcial, dentro de un mes (mediados de noviembre).

**Evidence:** el grupo ya escribió y corrió en DBeaver (SQLite) un script DDL/DML completo,
con FK compuestas y los insert-select de Desa a Prod (`raw/TP5/TP5_Grupo3_Scrips.sql`). Bruno
leyó el script de vistas y consultas con criterio: pidió comentarios que citen la consigna en
lugar de explicar de más. La parte práctica de SQL es terreno conocido. Su único tropiezo con
la herramienta fue esperar que DBeaver mostrara las vistas sin refrescar el árbol.

**Implications:**
- Igual que en el 1er parcial (LR [[0006-resultado-del-primer-parcial]]), el riesgo está en la
  **teoría escrita**: las definiciones de SP y triggers, "nombre y explique 3 restricciones",
  "explique EXISTS". Los modelos de examen (`Examen1` Q2, 3, 5, 6, 7 y `bd parcial 1a/1b`) salen
  textuales de los decks. La 0029 y el `reference/0006` llevan respuestas modelo por eso.
- En SQL, su zona de desarrollo próximo no es la sintaxis básica. Son los casos que no se
  ven a simple vista: NULL en CHECK y WHERE, "no es jefe" contra "tiene jefe" (`NOT EXISTS`),
  "ambos T1 y T2" (dos `IN`), el orden del DROP con FK y el INSERT … SELECT que empareja
  por posición.
- Camino propuesto para el TP: el paso 1 es el mapeo del DER de la cátedra (lección 0040).
  Siguen los escalones de `practica/tp5-clinica.html` y, al final, la reescritura del script
  del grupo. El mapeo tiene dos decisiones discutibles para llevar al docente: el triángulo
  de TORRE se mapea como 1:N y la F.HASTA punteada se guarda como `F_Hasta_Prevista`.
