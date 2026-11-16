# Catálogo de Trabajos Prácticos — Base de Datos (UCiudad, 2026)

Fuente: enunciados oficiales de la cátedra (Milich / Crispino) + entregas del Grupo 3. Las consignas son verbatim; las soluciones se citan solo como resolución plausible.

---

## TP1 — Cadena de farmacias

**Dominio:** farmacia (cadena con sucursales en varias ciudades).

**Consigna (verbatim):**
> "Desarrollar el Modelo Conceptual, definiendo las entidades, los atributos de cada una de ellas y la cardinalidad de las relaciones."
> "**Requerimientos:** Usted ha sido contratado con el motivo de diseñar una base de datos para una cadena de farmacias. De las entrevistas mantenidas con el personal de la empresa durante la etapa de relevamiento se obtuvieron los siguientes puntos a ser considerados: […]"
> "Con el modelo desarrollado usted debería poder responder las siguientes consultas: […]"

Fórmulas en los bullets: "Todo empleado se identifica con un código, guardando además…", "hay que poder conocer…", "Por cada ciudad hay un único…", "es decir, si… entonces…", "Cada medicamento puede venir en muchas… pero es producido por un único…".

**Entregable:** Modelo Conceptual (DER).

**Features forzadas:** ISA (Empleado → Personal propio / Farmacéutico); multivaluado (teléfono/s); compuesto (dirección = calle + número); derivado (antigüedad); relación ternaria con atributo (Stock: Farmacia × Medicamento × Presentación → cantidad); 1:N (Ciudad–Farmacia, Farmacia–Empleado); N:N (Medicamento–Presentación).

**Trampas:** "antigüedad" es **derivado** de la fecha de ingreso; el farmacéutico parece colgar de la farmacia ("un solo farmacéutico a cargo de la misma") pero un bullet posterior lo **reubica en Ciudad**; el "código postal" aparece **solo en la lista de consultas**, que funciona como requerimiento encubierto.

**Tamaño:** ~7 entidades conceptuales / ~10 tablas relacionales.

---

## TP2 — Clínica

**Dominio:** clínica médica (torres, habitaciones, consultorios, pacientes, profesionales).

**Consigna (verbatim):** misma cabecera que TP1 —
> "Desarrollar el Modelo Conceptual, definiendo las entidades, los atributos de cada una de ellas y la cardinalidad de las relaciones"
> "**Requerimientos:** La clínica cuenta con una estructura física de tres torres, de las cuales dos son para hospitalización y cirugías y una para consulta. […]"

Fórmulas: "Por cada habitación o consultorio **es importante conocer**…", "también **se necesita conocer** qué comodidades posee, **a saber:**", "Respecto de los pacientes…", "De cada profesional se guarda…", "**Una característica importante es que** un doctor puede dirigir un área específica…".

**Entregable:** Modelo Conceptual.

**Features forzadas:** ISA triple (Torre → Hospitalización/Cirugías/Consulta; Departamento → Habitación/Consultorio; Personal → Profesional/No profesional); compuestos (ubicación = torre+piso+número; longitud = ancho+largo; dirección = calle+número+piso+depto); multivaluado (teléfono/s); derivado (edad); 1:1 con identificador compartido (Paciente–Historia Clínica); historicidad (ocupación: desde cuándo y por cuánto tiempo); **unaria** (jefe de área → personal a cargo); N:N (Consulta–Servicio–Profesional).

**Trampas:** "edad" junto a "fecha de nacimiento" → **derivado**; la historia clínica parece entidad independiente pero es **1:1 identificada por el paciente**; las comodidades (baños, clóset, camas, ventana) aplican **solo a habitación**, no a consultorio, lo que obliga a la especialización; "jefe de área" introduce una relación **recursiva** sin nombrarla.

**Tamaño:** ~10-12 entidades / ~14 tablas.

---

## TP3 — Pedidos de materiales a proveedores

**Dominio:** compras / abastecimiento (departamentos que piden materiales a proveedores).

**Consigna (verbatim):**
> "Convertir el Modelo Conceptual presentado a continuación en un Modelo Relacional expresado en 3FN:"

La cátedra entrega el DER ya resuelto (PROVEEDOR, MATERIAL, UNIDAD MEDIDA, PEDIDO, DEPARTAMENTO; relaciones PROVEE, AFECTADO, POSEE, REALIZA, EXPRESA).

**Entregable:** Modelo Relacional en 3FN (pasaje DER → tablas con PK y FK). Sin SQL.

**Features forzadas:** N:N con atributo (POSEE: Pedido–Material con CANTIDAD); N:N sin atributo (PROVEE); multivaluado (TELÉFONO); compuesto (DIRECCIÓN = calle + nro); 1:N (Departamento–Pedido, Proveedor–Pedido); N:1 (Material–Unidad de Medida).

**Trampas:** el multivaluado se convierte en tabla propia; el compuesto se aplana en columnas; las dos N:N generan tablas intermedias, una con atributo propio. Es mecánica de pasaje, no interpretación.

**Tamaño:** 5 entidades → 7 tablas.

---

## TP4 — Biblioteca (normalización)

**Dominio:** biblioteca (préstamos de libros a socios).

**Consigna (verbatim):**
> "Generar una BD en 3° Forma Normal para el siguiente caso:"
> "Una biblioteca guarda, para cada uno de sus préstamos, los siguientes datos: número, nombre, apellido, dirección y teléfono del socio - ISBN del libro - Título del libro - […] - Fecha real de devolución."
> "**Condiciones:** 1) Cada socio tiene un número único que lo identifica. 2) Se registra un solo domicilio y un solo teléfono por cada socio. […] 7) Para cada libro, se decide por cuántos días se prestará. Esta cantidad de días no depende del socio, sino del libro. 8) Un mismo lector puede llevarse varias veces el mismo libro."
> "**Si surgen dudas respecto a otras condiciones, consultar con el docente y registrar por escrito.**"
> "**Se pide:** Diagrama Entidad-Relación / Modelo Entidad-Relación / Definir en qué forma normal se encuentra cada tabla"

**Entregable:** DER + modelo relacional + justificación de la forma normal de cada tabla.

**Features forzadas:** N:N con atributo propio (Libro–Autor con tipo de autor); entidad asociativa con identidad propia (Préstamo); 1:N (Socio–Préstamo); derivado (fecha esperada de devolución = fecha préstamo + días); dependencias funcionales explicitadas en las condiciones.

**Trampas:**
- Se parte de una **única relación universal plana** (atributos separados por guiones): hay que descomponerla, no diseñar desde cero.
- "Tipo de autor" parece atributo de Autor, pero la nota (\*) lo **reasigna al par libro-autor**.
- La condición 7 dicta la DF: días de préstamo **pertenece a Libro** (la entrega del grupo lo ubicó en Préstamo).
- La condición 8 impide usar (socio, libro) como PK del préstamo.
- "Fecha esperada de devolución" es **calculada**.
- La condición 6 ("solo de a uno por vez") es regla de negocio no representable en el modelo.

**Tamaño:** 6 tablas (Socio, Libro, Autor, Libro_Autor, Tipo_Autor, Préstamo).

---

## PATRÓN DE CONSIGNA

- **Encabezado imperativo breve y fijo**, en infinitivo, que define el entregable antes del caso: "Desarrollar el Modelo Conceptual, definiendo las entidades, los atributos de cada una de ellas y la cardinalidad de las relaciones", "Convertir el Modelo Conceptual… en un Modelo Relacional expresado en 3FN", "Generar una BD en 3° Forma Normal para el siguiente caso".
- **Ficción de relevamiento en segunda persona formal:** "Usted ha sido contratado con el motivo de diseñar una base de datos para…", "De las entrevistas mantenidas con el personal de la empresa durante la etapa de relevamiento se obtuvieron los siguientes puntos a ser considerados".
- **Cuerpo en viñetas cortas**, una regla de negocio por viñeta, redactadas desde la necesidad de información y no desde la estructura: "hay que poder conocer…", "es importante conocer…", "se guarda…", "los datos guardados son…". Nunca se usa vocabulario técnico de entidades, atributos ni cardinalidades.
- **Cardinalidad expresada en prosa**, con la fórmula "un único / un solo / muchos … pero", y a menudo reforzada con una aclaración explicativa: "es decir, si en una misma ciudad existe más de una farmacia, entonces…".
- **Trampa deliberada de atributo derivado** en casi todos los enunciados (antigüedad, edad, fecha esperada de devolución), siempre mencionada al lado del dato del que deriva.
- **Trampa de ubicación de atributo o relación:** un dato se presenta pegado a una entidad y una viñeta posterior (o una nota al pie con asterisco) lo reasigna a otra entidad o a la relación.
- **Cierre con la prueba de validación del modelo:** o una lista de consultas ("Con el modelo desarrollado usted debería poder responder las siguientes consultas"), o un bloque numerado de "Condiciones", o un "Se pide" con los entregables enumerados.
- **Cláusula de escape explícita ante ambigüedad:** "Si surgen dudas respecto a otras condiciones, consultar con el docente y registrar por escrito" — el enunciado admite que es incompleto a propósito.
