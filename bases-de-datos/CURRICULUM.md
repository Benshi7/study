# Plan de clases — Base de Datos (UCBA, 2026 1C)

Mapa completo del temario oficial a lecciones. **Este archivo es el contrato de cobertura**:
si un tema del programa no está acá, falta una lección.

Orden de lectura = orden de numeración. Se avanza de arriba hacia abajo.

**Leyenda:** ✅ escrita · ⏳ próxima · ⬜ pendiente · ⏸ diferida al 2do parcial

---

## Unidad 1 — Sistemas de Gestión de Base de Datos

> *Introducción a las Bases de Datos. Los DBMS: componentes. Estructura de datos relacional.
> Conceptos Básicos: atributos, tuplas, claves y relaciones. Dato e Información: concepto.
> Independencia de datos. Usuarios de la Base de Datos. Conceptos de Tablas.*

| # | Lección | Estado |
|---|---|---|
| 0001 | ¿Qué problema resuelve una base de datos? Dato, información y minimundo | ✅ |
| 0002 | El DBMS por dentro: qué hace, su catálogo, y quién lo usa | ✅ |
| 0003 | Los tres niveles y la independencia de datos | ✅ |
| 0004 | La estructura relacional: relación, tupla, atributo, dominio | ✅ |
| 0005 | Claves e integridad: candidata, primaria, foránea | ✅ |
| 0006 | El ciclo de vida de una base de datos: las cuatro etapas | ✅ |

## Unidad 2 — Modelos de Datos

> *Introducción. Modelo de Datos. Proceso de Diseño de una base de Datos. Diseño Conceptual.
> Modelo Entidad-Relación. Estructura de Datos Relacional: Relaciones, Integridad.*

| # | Lección | Estado |
|---|---|---|
| 0007 | Modelo de datos, proceso de diseño y qué califica como entidad | ⏳ |
| 0008 | Los cinco tipos de atributo: simple, compuesto, multivaluado, derivado, clave | ⬜ |
| 0009 | Relaciones y grado: unaria, binaria, ternaria | ⬜ |
| 0010 | **La razón de cardinalidad: dónde va el número** | ✅ |
| 0011 | Participación total vs parcial: la línea doble | ⬜ |
| 0012 | Entidad débil y relación identificativa | ⬜ |
| 0013 | Especialización: dos marcas y cuatro combinaciones | ✅ |
| 0014 | Contar registros del supertipo (total/parcial × exclusiva/solapada) | ✅ |
| 0015 | Relaciones N:N, atributos de relación y el patrón histórico | ⬜ |
| 0016 | Del DER al modelo relacional: las siete reglas de mapeo | ⬜ |
| 0017 | Integridad en el modelo relacional: de entidad y referencial | ⬜ |
| 0018 | **Integrador**: resolver el Ej. Clínica de punta a punta | ⬜ |

## Unidad 3 — Diseño de Base de Datos

> *Diseño Relacional. Concepto y finalidad de la Normalización. Formas Normales 1°, 2° y 3°.
> Independencia de los datos, redundancia e inconsistencia en la información.*

Base: **Clase 3 (Normalización)** + el ejercicio de clase del **10/09/2026** con su
respuesta, + el **Ejercicio 1 (Proveedores)** con su resolución oficial en ERDPlus.

| # | Lección | Estado |
|---|---|---|
| 0019 | Las anomalías: por qué se normaliza | ✅ |
| 0020 | Dependencia funcional: la única herramienta que vas a usar | ✅ |
| 0021 | Primera forma normal: el grupo repetitivo | ✅ |
| 0022 | Segunda forma normal: la dependencia parcial | ✅ |
| 0023 | Tercera forma normal: la dependencia transitiva | ✅ |
| 0024 | Dónde vive el precio: N:N, tabla asociativa e histórico | ✅ |
| 0025 | **Integrador A**: el ejercicio del 10/09, paso a paso | ✅ |
| 0026 | **Integrador B**: Ejercicio 1 (Proveedores) — del DER a 3FN | ✅ |

## Unidad 4 — Organización física e Índices

> *Tipos de Índices. Utilización y Manejo. Estructura física de Datos, organización y diseño.*

| # | Lección | Estado |
|---|---|---|
| 0027 | Almacenamiento, disco y el enfoque de archivos | ✅ |
| 0028 | **Índices: principal, agrupado y secundario** (+ denso/no denso) | ✅ |
| 0029 | Store procedures, funciones y disparadores | ✅ |

> **La Unidad 4 de la cátedra viene partida en dos**, y sólo una mitad entra al 1er parcial.
> `raw/Material_Examen/unidad 4 conceptos.pdf` (almacenamiento, índices, transacciones) se
> dictó con deck y **entra**; `unidad 4 DDL.pdf` (CREATE, ALTER, DROP, restricciones, store
> procedures, triggers) **no tiene deck** y los docentes confirmaron que queda **diferido al
> 2do parcial**. Por eso la 0029 absorbe los procedimientos almacenados y disparadores que
> antes vivían en la 0040, y queda en pausa. Detalle en [PARCIAL.md](PARCIAL.md).

## Unidad 5 — Lenguaje de Consulta de Datos

> *Introducción al SQL. DDL, DML y SQL. Creación de BD y tablas. Consultas Simples y
> Multitablas. Consultas Sumarias. SubConsultas. Manipulación de Datos. Integridad de Datos:
> reglas de eliminación y actualización. Disparador e Integridad. Procedimientos almacenados. Vistas.*

| # | Lección | Estado |
|---|---|---|
| 0030 | SQL: las tres familias (DDL, DML, DCL) y para qué sirve cada una | ⬜ |
| 0031 | DDL: CREATE TABLE y las restricciones declaradas | ✅ |
| 0032 | SELECT: proyección, filtrado y orden | ✅ |
| 0033 | Condiciones de búsqueda a fondo (y la trampa de NULL) | ✅ |
| 0034 | Consultas multitabla: el JOIN y sus variantes | ✅ |
| 0035 | Consultas sumarias: GROUP BY, HAVING y las funciones de agregación | ✅ |
| 0036 | Subconsultas: escalares, de fila, correlacionadas, EXISTS | ✅ |
| 0037 | DML: INSERT, INSERT multifila, UPDATE, DELETE | ✅ |
| 0038 | Integridad referencial en acción: ON DELETE y ON UPDATE (+ ALTER y DROP) | ✅ |
| 0039 | Vistas: para qué sirven de verdad | ✅ |
| 0040 | **Integrador TP5 Clínica**: del DER de la cátedra a los scripts | ✅ |

> Los disparadores y procedimientos almacenados que antes eran la 0040 se movieron a la
> **0029**, porque la cátedra los dicta en el material de Unidad 4. La Unidad 5 queda en
> 10 lecciones.

> **2026-10-15 — llegó el material del 2do parcial.** Los decks `DDL, SP , Triggers .pptx` y
> `DML_Base de Datos.pptx` destrabaron la 0029 y las 0031–0039. El número 0040, que había
> quedado libre, pasó a ser el **integrador del TP5 Clínica** (DER de la cátedra → relacional
> → scripts). La 0030 (las tres familias) queda pendiente: su contenido es de la Clase 1 y
> la 0031 cubre la parte de DDL. ALTER y DROP, que no tenían lección propia, entraron en la
> 0038 junto con ON DELETE, porque el deck los da juntos y el Examen1 los pregunta.
> Todas las lecciones SQL tienen ejercicios con corrección automática (`assets/sqlbox.js`)
> sobre la base de la Clínica (`assets/seeds/clinica.js`).

## Unidad 6 — Administración de Transacciones

> *Definición. Procesamiento, errores y recuperación. Concurrencia. Concepto de bloqueo
> de datos. Deadlock; prevención y detención.*

| # | Lección | Estado |
|---|---|---|
| 0041 | **Qué es una transacción y qué promete ACID** | ✅ |
| 0042 | Problemas de concurrencia (pérdida de actualización, suma incorrecta, lectura sucia, no repetible, fantasma) | ✅ opcional |
| 0043 | Planificaciones, serialización, conflicto, bloqueos/2PL, deadlock y MVCC | ✅ opcional |
| 0044 | Tipos de fallos, estados de una transacción, log UNDO/REDO, recuperabilidad | ✅ opcional |

## Unidad 7 — Procesamiento y Optimización de Consultas

> *Procesamientos de Consultas. Etapas. Estrategias de procesamiento, recuperación y
> concurrencia. Análisis de un plan de ejecución de un Motor de Base de Datos Comercial.*

| # | Lección | Estado |
|---|---|---|
| 0045 | Las etapas del procesamiento de una consulta | ⬜ |
| 0046 | Leer un plan de ejecución sin adivinar | ⬜ |

## Unidad 8 — Seguridad e Integridad de las Bases de Datos

> *Tipos de Seguridad. Tipos de Fallas. Planes de Contingencia. Técnicas de Control de
> acceso. Privilegios, autorizaciones y Vistas.*

| # | Lección | Estado |
|---|---|---|
| 0047 | Control de acceso: privilegios, GRANT/REVOKE y vistas como mecanismo de seguridad | ✅ opcional |
| 0048 | Planes de contingencia (los tipos de falla quedaron en la 0044) | ⬜ |

## Unidad 9 — Datawarehouse

> *Historicidad de los datos: Slow change dimension, diseño, mantención y utilización.
> Concepto de Datawarehouse e Inteligencia de Negocios. ETL. Herramientas de visualización.*

| # | Lección | Estado |
|---|---|---|
| 0049 | OLTP, OLAP y qué es un Data Warehouse (+ BI, cubo, MOLAP/ROLAP/HOLAP) | ✅ |
| 0050 | Los componentes de un DW: ETL, staging, ODS, MDM, DQ, DW vs Data Mart | ✅ |
| 0051 | Modelo estrella, copo de nieve, Inmon y Kimball | ✅ |
| 0052 | **Slow Change Dimension**: una fila por foto, estado a una fecha, estado actual e historia contra foto | ✅ |
| 0053 | Repaso de la Unidad 9: definiciones y diferencias, estilo choice (15 preguntas) | ✅ |
| 0054 | **Conjuntos en SQL**: diagrama de Venn → SQL con JOIN + WHERE (y UNION/EXCEPT), 8 ejercicios corregibles | ✅ |
| 0055 | **La clase del parcial**: 7 bloques de 10 min (SCD actual, indicador, a una fecha, anteúltima, SUMINISTROS, conjuntos, DDL + teoría), 10 ejercicios corregibles y mini-simulacro | ✅ |

> **2026-10-23 — llegaron los decks de la Unidad 9.** `Intro Datawarehouse` y `Slow Change
> Dimension` (más el TP SCD) se convirtieron en las lecciones 0049–0052. El plan original tenía
> "ETL e inteligencia de negocios" como lección aparte: el deck no les da más que una lámina
> (ETL = extracción, transformación y carga), así que el ETL entró en la 0050 y el BI en la
> 0049. SCD pasó a tener lección propia (la 0052) porque el docente dijo que toma sus dos
> consultas en la práctica del 2do parcial. Visualización de datos sigue sin deck.

---

## Notas sobre el plan

- **Dónde estamos según la cátedra.** Al 2026-09-10 el docente dictó Clase 1 (Unidad 1),
  Clase 2 (Unidad 2, diseño conceptual hasta ISA y N:N) y Clase 3 (Normalización, que es
  el corazón de la Unidad 3). Las lecciones 0001 a 0026 cubren terreno ya visto en clase;
  de 0027 en adelante vamos por delante del curso.
- **La 0010 se escribió antes que el resto.** Fue la primera lección del workspace, cuando
  todavía no tenía el temario. Quedó renumerada a su lugar correcto en la Unidad 2.
- **La Unidad 3 creció de 6 a 8 lecciones** cuando llegó el material de la Clase 3.
  Justificaron el aumento dos cosas que el temario no anticipaba: el tema "dónde vive el
  precio" (histórico, slides 14–15) y el hecho de que hay **dos caminos distintos** para
  llegar a 3FN, y la cátedra evalúa los dos. Las Unidades 4 a 9 se corrieron dos lugares.
- **Los integradores son el termómetro real.** Cubrir un tema no es saberlo; resolver un
  enunciado completo sí. Los de la Unidad 3 (0025 y 0026) tienen resolución oficial del
  docente al lado, así que se corrigen solos. El Ej. Clínica (0018) no la tiene: ahí se
  practica sin red.
- **Falta el Ejercicio 2 del 10/09** (armar una base de datos). Bruno todavía no lo tiene
  resuelto; queda planteado al final de la 0026 y se desarrollará cuando lo encare.
- **El plan se ajusta.** Si el docente agrega, adelanta o profundiza algo, esta tabla
  se actualiza. Es un mapa, no una promesa rígida.
