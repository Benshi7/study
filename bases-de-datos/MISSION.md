# Mission: Bases de Datos — Universidad de la Ciudad de Buenos Aires (2026, 1er cuatrimestre)

## Why
Bruno cursa Base de Datos en la Licenciatura Complementaria en Ciencias de Datos y necesita
aprobar TPs, parciales y final. La materia recorre **nueve unidades**, desde qué es un dato
hasta datawarehouse, y se evalúa con la notación y los criterios concretos de la cátedra.
El objetivo es cubrir el temario completo, sin agujeros, y poder defender cada respuesta.

## Success looks like
- **Cobertura completa del temario.** Las nueve unidades, en orden, sin saltear.
  El mapa vive en [CURRICULUM.md](CURRICULUM.md) y es el contrato de esta misión.
- Explicar los fundamentos con precisión: dato vs información, qué hace un DBMS,
  los tres niveles de abstracción, independencia lógica y física.
- Dado un enunciado en prosa (tipo TP1 Farmacia, Ej. Clínica), producir el modelo conceptual
  completo — entidades, atributos, cardinalidades, participación, jerarquías ISA —
  y justificar cada decisión contra el texto.
- Convertir un modelo conceptual a relacional y normalizarlo hasta 3FN, explicando qué
  anomalía elimina cada paso.
- Escribir SQL: DDL, consultas multitabla, sumarias y subconsultas, DML, vistas,
  disparadores y procedimientos almacenados.
- Razonar sobre transacciones, concurrencia, bloqueos y deadlock.
- Leer un plan de ejecución y explicar por qué el motor eligió esa estrategia.
- Explicar índices, control de acceso, y los conceptos de datawarehouse, ETL y BI.
- Producir los diagramas en ERDPlus, que es la herramienta que exige la cátedra.

## Constraints
- **Clases incrementales y cortas.** Una lección = una idea + una práctica. Pero el
  recorrido arranca desde cero y avanza en orden de temario: nada se da por sabido
  sin haberlo cubierto antes.
- Bruno tiene conocimientos previos: el tono es de refuerzo y precisión, no de curso
  para alguien que nunca vio el tema. Se cubre todo, pero sin explicar de más.
- El material de la cátedra manda. `raw/` es la fuente de verdad sobre qué se evalúa
  y cómo. Cuando Elmasri y la cátedra difieran, gana la cátedra — y la diferencia
  se señala explícitamente.
- Los temas siguen avanzando durante el cuatrimestre. El plan se actualiza con lo que
  vaya dictando el docente.

## Out of scope
- Motores y dialectos concretos más allá de lo que pida la cátedra. SQL estándar primero;
  particularidades de un motor sólo si la materia lo exige.
- NoSQL, bases de grafos y almacenamiento distribuido: no están en el temario.
- Administración en producción real (replicación, alta disponibilidad, backups operativos).
  La Unidad 8 cubre seguridad y contingencia **a nivel conceptual**, que es lo evaluado.

> **Nota de corrección (2026-08-30).** La primera versión de este archivo declaraba fuera
> de alcance los índices, la optimización de consultas y el datawarehouse. Estaba mal:
> son las Unidades 4, 7 y 9 del programa. Corregido tras recibir el temario oficial.
