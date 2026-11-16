# 1er Parcial — mapa de estudio

**Jueves 24/09/2026, 18:30.** En papel, **una hora exacta**, dibujando a mano.
La hoja la dan ellos; no hace falta llevar computadora.

Fuentes de este mapa, en orden de autoridad:

1. `raw/PAUTAS_EXAMEN.md` — lo que el docente dijo en clase el 17/09. **Manda sobre todo lo demás.**
2. `raw/Clase Indices y Txn .pptx` — el deck de la última clase (se titula "Clase 4").
3. `raw/Material_Examen/unidad {1,2,3,4}*.pdf` — los mismos decks en PDF, reorganizados
   por unidad. La Unidad 4 viene **partida en dos**: `unidad 4 conceptos.pdf` (índices y
   transacciones, que coincide casi textual con el PPTX) y `unidad 4 DDL.pdf` (que **no
   tiene PPTX equivalente** y está diferido — ver abajo).
4. Los tres decks anteriores (Unidades 1, 2 y 3) y el cronograma.
5. `raw/Fundamentos-de-Sistemas-de-Bases-de-Datos.pdf` (Elmasri) — sólo como apoyo.

El contrato de cobertura de la materia completa sigue siendo [CURRICULUM.md](CURRICULUM.md).

---

## Lo primero, porque cambia la estrategia entera

**Teoría y práctica se aprueban por separado. No se promedian.**

El docente lo aclaró respondiendo a esa pregunta exacta. Sacar todo de una parte y nada de
la otra es desaprobado. El ejemplo que dio: 5 de teoría bien y 2 de práctica → **el examen
es un 2**.

| Si toma… | Hace falta… |
|---|---|
| 5 preguntas por parte | 3 de teoría **y** 3 de práctica, para un 4 |
| 3 preguntas por parte | 2 de teoría **y** 2 de práctica |

Cantidad no cerrada. Primero dijo "cuatro teóricas seguramente y tres o cuatro prácticas",
después "yo supongo que vamos a hacer tres y tres".

Y ahora **la frase más importante de toda la clase**:

> El caso típico es el que ya trabaja con bases de datos: resuelve la práctica fácil,
> no estudia la teoría, y desaprueba.

Ese es tu perfil de riesgo. La práctica la vas a sacar. **La teoría es donde se cae la gente
como vos.** Estudiá en ese orden.

El recuperatorio es del **examen completo**, no de la parte que fallaste.

---

## Corrección (24/09): los modelos SÍ sirven — pero sólo cuatro preguntas

**Revisión de lo que sigue abajo.** Descartamos `Examen1.webp` / `Examen2.webp` enteros
porque las preguntas 2 a 7 salen de `unidad 4 DDL.pdf`, que está diferido. Eso es correcto.
Pero **las otras cuatro preguntas están 100% en alcance y son el mejor predictor que
tenemos**:

| Pregunta | Qué es | Dónde practicarla |
|---|---|---|
| **1** · "Grafique y explique qué es Ciclo de Vida" | Unidad 1 | `0006` |
| **8** · "Normalizar en 3FN la siguiente tabla" | El ejemplo de facturación de la Clase 3, **con los derivados `Precio Total` y `Precio_R`** | `0025`, `reference/0002` |
| **9** · "Informar cuántos registros tiene la entidad Persona (**contemple todas las posibilidades**)" | Conteo sobre un ISA `Persona → Secretaria / Docente / Alumno`, 5 de cada uno | `0014` |
| **10** · "Convertir el Modelo Conceptual en un Modelo Relacional en 3FN" | **Es el TP3 textual** (PROVEEDOR / MATERIAL / PEDIDO / DEPARTAMENTO / UNIDAD MEDIDA) | `0026` |

**Dos conclusiones que cambian el plan de práctica:**

1. **Los TP se reusan como ejercicios de parcial.** La pregunta 10 es el TP3 sin cambiarle
   una coma. Resolver los TP no es "practicar parecido": es practicar lo mismo.
2. **El gráfico se puede plantear de cuatro formas distintas**, y no son intercambiables:
   - **Forma 1** — enunciado en prosa → dibujar el DER (TP1, TP2).
   - **Forma 2** — DER dado → convertirlo a relacional 3FN (TP3, Examen2 Q10) → `0026`.
   - **Forma 3** — DER dado → responder algo sobre él, como el conteo (Examen1 Q9) → `0014`.
   - **Forma 4** — tabla plana → normalizar (Examen1 Q8, TP4) → `0025`.

   El triángulo del Examen1 Q9 dice **"ES"** en lugar de "ISA". Es lo mismo.

---

## Por qué igual descartamos el resto de esos modelos

### El examen del compañero salía ÍNTEGRO de `unidad 4 DDL.pdf`

`raw/Examen1.webp` y `raw/Examen2.webp` tienen triggers, stored procedures, `ALTER TABLE`
y lectura de código PL/SQL. **Nada de eso entra**, y ahora sabemos exactamente de dónde salió:

| Pregunta del modelo | Origen |
|---|---|
| 2 · Triggers | `unidad 4 DDL.pdf` pp. 9–11 |
| 3 · Tres restricciones | `unidad 4 DDL.pdf` pp. 2–5 (PK, Unique, Default, Not Null, Check, FK) |
| 5 · Stored procedure: qué, cuándo, `CALL` | `unidad 4 DDL.pdf` pp. 7–8 |
| 6 · Borrar `duración` de `Curso`, agregar campo | `unidad 4 DDL.pdf` p. 6, **textual**: `ALTER TABLE Curso drop duración` |
| 7 · Explicar el procedimiento dado | `unidad 4 DDL.pdf` p. 9, **textual**: `GET_LOAD_ID` |

Las cinco preguntas, del mismo PDF. Y los docentes ya confirmaron que **DDL, store
procedures y triggers quedan diferidos al 2do parcial**. Ese PDF, entero, está fuera.

### `bd parcial 1a.jpg` / `1b.jpg` tampoco es un 1er parcial

A pesar del nombre, son las dos caras de **un examen posterior**: piden graficar los
componentes de un **Datawarehouse** (Unidad 9), explicar `EXISTS`, generar vistas y
resolver consultas SQL con subconsultas y promedios (Unidad 5). Todo eso se dicta
**después** de este parcial.

Lo único que sobrevive de ese modelo: su pregunta 2, que vuelve a ser índices.

### Por qué descartamos el resto

Dos razones, las dos del docente:

- *"No hay examen modelo de años anteriores: no vamos a tomar nada que no hayamos dado."*
- El deck de la última clase **no tiene procedimientos almacenados ni funciones ni
  disparadores**. El cronograma prometía "Procedimientos almacenados. Funciones" en esa
  clase; el docente dio **índices y transacciones** en su lugar. Y `PAUTAS_EXAMEN.md`, que
  enumera lo que entra de teoría, no los menciona.

Lo que sigue en pie de ese examen de muestra: normalización y modelo conceptual, que son
justamente los dos ejercicios prácticos. El resto, descartado.

**A cambio entró algo que no estaba en el radar: transacciones y ACID** (Unidad 6).

---

## Qué entra de teoría

*"Todo lo visto desde la clase 1 hasta la de hoy, y sale de los PPT: si se leen todo eso y
lo estudian, prácticamente tienen aprobada la parte teórica."*

Preguntas **abiertas para desarrollar**, más "algún multiple choice por ahí". Son puntuales
y casi siempre piden justificar: *"¿por qué?"*, *"justifique"*.

| Tema | Qué pide exactamente | Lección |
|---|---|---|
| **Índices** | Nombre de cada tipo, para qué sirve, qué beneficio tiene | ⬜ `0028` |
| **Transacciones** | Las definiciones de **ACID** | ⬜ `0041` |
| **Normalización** | Nombrar las tres formas normales y **cuál es el fin** de normalizar | ✅ `0019`–`0023` |
| **MER** | Relaciones unarias y binarias | ⬜ `0009` |
| **MER** | Atributo derivable: qué es **y para qué se usa** | ⬜ `0008` |
| **MER** | Historicidad | ✅ `0024` |
| **Especialización** | Exclusiva o solapada, y la parte de exclusividad | ✅ `0013`, `0014` |
| **Notación** | De memoria, sin la herramienta (ver abajo) | ✅ `reference/0004` |
| Almacenamiento | Está en el deck, no lo nombró — probabilidad baja, pero entra | ⬜ `0027` |

### La pregunta textual que dio

> **¿Cuál de todos los índices ordena físicamente los campos?**
> → **El agrupado.** Más el "justifique".

La dio como pregunta de parcial, literal. Ver la sección de índices más abajo, porque acá
hay una trampa fina.

**Índices es el único tema confirmado por tres fuentes independientes:**

1. El docente dio la pregunta textual en clase (`PAUTAS_EXAMEN.md`).
2. Las pautas lo listan: "nombre de los tipos y para qué sirve cada uno, qué beneficio tiene".
3. El modelo `bd parcial 1a.jpg`, pregunta 2: *"Explique cada tipo de Índices: Agrupados,
   Principal y Secundarios. **De un ejemplo**."* — nótese que pide ejemplo.

Si hay un tema que no se puede dejar sin estudiar, es éste.

---

## Qué entra de práctica

Dos ejercicios que *"van de cajón"*:

1. **Modelado (DER / MER).** Un enunciado corto del estilo de los que hicieron en clase con
   el otro profesor. Mencionó: **libros, autos, farmacia, celulares**. Hay que armar el
   diagrama entidad-relación **a mano**.
2. **Normalización.** Una tabla con campos, para descomponer en *n* tablas,
   **poniendo la clave primaria de cada una**.

También avisó que normalización **puede venir mezclada**: una pregunta teórica sobre las
formas normales y después el ejercicio.

> Material de práctica que ya tenés en `raw/`: `TP1_Base de Datos 2026 1er Cuatrimestre.pdf`
> (Farmacia), `Rta-TP-Farmacia.erdplus`, `Ej DER Clinica.pptx`,
> `Ejercicios para realizar en clase 2026-09-10.pdf` con su respuesta.
> "Farmacia" salió de la boca del docente como ejemplo. Resolvelo.

---

## Los tres errores que marcan siempre

Los nombró como los que ven en todos los exámenes. Son puntos regalados si no los cometés.

1. **Modelar los campos calculados.** Si la tabla trae el precio y un total que es la
   multiplicación, **ese campo derivado no va** en las tablas normalizadas.
   *"Si lo ponen, está mal."*
2. **No poner las claves primarias** de las tablas resultantes.
3. En teoría, **no acordarse para qué sirve cada tipo de índice**.

> **Conexión directa.** El ejercicio de normalización del examen de muestra tenía las
> columnas **Precio Total** y **Precio_R** agregadas sobre el ejercicio del 10/09. Esas dos
> columnas son exactamente la trampa del error nº 1. Si aparecen, se eliminan y se justifica
> por qué: son derivables de cantidad × precio.

---

## La respuesta canónica del ejercicio de normalización

`raw/Material_Examen/unidad 3.pdf` es el deck de normalización, y trae **el ejercicio
resuelto por la propia cátedra**. Es el ejemplo de facturación, el mismo que reaparece
en los parciales.

La página 4 resuelve el misterio de las columnas raras del modelo:

> "Vemos campos que surgen de multiplicaciones, sumas etc. (**Atributos Derivables**)
> **Pcio R = Cant x P Unit**"

`Precio_R` es **Precio Renglón**, y la cátedra lo rotula ella misma como atributo derivable.
Es exactamente el error nº 1 que marcan. **Se elimina.**

Y la página 11 da el modelo final en 3FN, que es la respuesta que esperan:

```
CabeceraFact (#NFact, Fecha, CodCli)
RenglonFact  (#NFact, #CProd, Canti, Punit)
Prod         (#CProd, Descri)
Cli          (#CodCli, NomCli)
```

Cuatro tablas, cada una con su clave primaria marcada con `#`. Las definiciones textuales
de las tres formas normales están en la página 12 de ese mismo PDF — **memorizá esa
redacción**, que es la que corrige el docente.

---

## Índices: la taxonomía del docente, que NO es la de Elmasri

Del deck "Clase 4", slides 9 a 16. **Esto es lo que hay que contestar.**

| Tipo | Definición del docente | Beneficios / costos |
|---|---|---|
| **Principal o primario** | Se crea sobre la/s columna/s de la **clave primaria**. Sólo puede haber **uno** por tabla, porque la PK es única | Unicidad · Búsqueda eficiente · Base para las restricciones de integridad referencial |
| **Agrupado** | Las filas de la tabla **se ordenan en el mismo orden que el índice**: los valores parecidos quedan físicamente juntos en disco | **Ordenamiento físico (+)** · Búsqueda eficiente (+) · Ahorro de espacio (+) · Limitaciones en la modificación de datos (−) |
| **Secundario** | Se crea sobre columnas que **no** son la PK. No afecta el ordenamiento físico: crea una estructura de índice **separada** | No afecta el orden físico (+) · Búsqueda eficiente (+) · Mayor espacio (−) · Mayor flexibilidad (+) · Uso excesivo degrada el rendimiento (−) |

Y aparte, la clasificación por densidad (slide 13, copiada textual de Elmasri p. 431):

- **Índice denso**: una entrada por cada valor de la clave de búsqueda, y por tanto por cada registro.
- **Índice no denso** (escaso): sólo tiene entradas para algunos de los valores de búsqueda.
- El **principal es no denso**, porque incluye una entrada por cada **bloque de disco**, no por cada registro.

### ⚠️ La trampa, y es importante

El deck **se contradice consigo mismo**, y si razonás de más te equivocás.

- Slides 10 y 11 definen el **principal** como "el índice de la clave primaria" y le dan la
  unicidad. El **ordenamiento físico** se lo adjudican al **agrupado**.
- Slide 13, en cambio, está copiado de Elmasri, donde el índice principal **sí** implica que
  el archivo está ordenado por esa clave — de ahí que tenga "una entrada por bloque".

Son dos marcos distintos pegados en el mismo deck. `MISSION.md` ya fija el desempate:
**cuando Elmasri y la cátedra difieren, gana la cátedra.**

> A "¿cuál ordena físicamente?" la respuesta es **el agrupado**. No razonar desde el
> slide de denso/no denso. No corregir al docente en la hoja.

### Otra divergencia, menor pero anotada

La captura que mandaste del slide de Índice Secundario tiene un primer bullet —
*"Por defecto se crea en KP pero no es obligatorio"* — que **no aparece en el PPTX subido**
(busqué "KP" en los 19 slides: cero resultados). El resto del slide coincide palabra por
palabra. O sea que circulan **dos versiones del deck**. Vale la pena chequear cuál es la
vigente, porque ese bullet afirma algo sustantivo.

---

## Transacciones y ACID

Slides 18 y 19. Es lo único de Unidad 6 que entra, y el docente dijo que **en algún parcial
tomó las definiciones de ACID**.

- Una transacción incluye **una o más operaciones** de acceso a la base: inserción,
  eliminación, modificación o recuperación.
- Sus límites se marcan explícitamente con `begin transaction` y `end transaction`.
- Si sólo recupera datos y no actualiza, es una transacción de **sólo lectura**.

Las cuatro propiedades, con la redacción del deck:

| Propiedad | Definición |
|---|---|
| **Atomicidad** | Unidad atómica de procesamiento: o se ejecuta en su totalidad, o no se ejecuta en absoluto |
| **Conservación de la consistencia** | Su ejecución completa lleva la base de un estado consistente a otro |
| **Aislamiento** | Debe aparecer como si se ejecutara aislada: no interfiere con otras transacciones simultáneas |
| **Durabilidad** | Los cambios de una transacción confirmada **persisten**, y no se pierden por un fallo |

---

## Notación a mano — no hay ERDPlus en el parcial

Lo dijo explícitamente: *"notación de memoria, porque no van a tener la herramienta que
dibuja sola"*. Lo que hay que saber dibujar sin pensar:

- **Atributo multivaluado** → doble elipse
- **Atributo derivado** → elipse punteada (y saber cuándo va punteada y cuándo no)
- **Cardinalidades** uno a uno y uno a muchos
- **Dónde va la pata de gallo**

Esto no es teoría: es motricidad. Se practica dibujando, no leyendo.

### La notación de especialización de la cátedra NO es la de Elmasri

Fuente: **`raw/B Clase 2 Diseño Conceptual Udeci.pptx`, slides 25, 26 y 27** — el deck de
la clase, verificado dentro del PPTX. Las mismas slides salen en `unidad 2.pdf` pp. 11–12.
**Nada de una letra `d` u `o` adentro de un círculo**, que es lo que enseña el libro.
La cátedra lo escribe así, textual:

> "**Parcial**: puede haber más empleados. **Se grafica sin círculo**."
> "**Total**: sólo hay 2 tipos de fichas. **Se grafica con un círculo**."
> "**Exclusiva**: un empleado sólo realiza una tarea. **Se grafica con elipse**."

Traducido a reglas de dibujo:

| Eje | Cómo se marca |
|---|---|
| **Total** | círculo sobre la línea entre el supertipo y el triángulo |
| **Parcial** | sin círculo |
| **Exclusiva** (disjunta) | arco que cruza las patas de los subtipos |
| **Solapada** | sin arco |

Los cuatro ejemplos del deck, uno por cuadrante:

| | Exclusiva | Solapada |
|---|---|---|
| **Total** | Ficha → Ficha_autor / Ficha_tema | Equipo_futbol → Delantero / Defensa / Portero / Centrocampistas |
| **Parcial** | Empleado_Restaurante → Camarero / Cocinero / Lava_platos | Participantes_Pelicula → Productor / Director / Actores |

El triángulo lleva **`ES`** adentro, no `ISA`.

> **Táctica de examen.** El deck mezcla más de una notación entre slides, así que el
> símbolo solo es discutible. En la slide "Simbología ISA" la propia cátedra dibuja el
> diagrama **y escribe al lado, en palabras, "Total, Exclusiva"**. Copiá eso: símbolo
> más rótulo escrito. Cuatro palabras que blindan la pregunta.

### CUIDADO con `raw/ejercicios.pdf`: no es material de cátedra

Es un **apunte de alumno**. Sirve como práctica, pero **no es fuente de verdad** y no hay
que citarlo como "la respuesta". Su página 3 trae un esquema relacional de Farmacia que
**no coincide con la resolución oficial** en dos puntos (ver abajo).

### Lo único oficial de Farmacia es el DER, y no incluye tablas

`raw/Rta-TP-Farmacia.erdplus` declara `diagramType: 1`: es **sólo el modelo conceptual**.
**No existe un esquema relacional oficial de este TP.** Cualquier tabla que uses es una
derivación tuya, defendible pero no canónica.

Lo que el DER oficial sí marca, y sirve de evidencia:

| Atributo | Marca en el archivo |
|---|---|
| `Telefono` (de Empleado) | `Multivalued: true` |
| `Direccion` (de Empleado) | `Composite: true`, con `Calle` y `Nro` |
| `Antoguedad` (de Propio) | `Derived: true` ← el error nº1, dibujado y marcado |
| Empleado → Farmaceutico / Propio | `totalSpecialization: true`, `supertypeDefinition: "Disjointed"` |

**Las dos divergencias con el apunte:**

1. **`Cantidad`.** El DER oficial la cuelga de `Tiene` (Medicamento × Presentación, N:N), y
   deja `Stock` (Farmacia × Medicamento) **sin atributos**. El apunte arma un `Stock`
   ternario con las tres. El enunciado dice *"la cantidad en existencia (stock) del mismo
   **en cada farmacia**"*, así que el apunte parece más fiel — pero **no está confirmado**.
   Es la pregunta a hacerle al docente antes del jueves.
2. **`Farmaceutico`.** El oficial tiene `Id_Farmaceutico` + `Fecha Graduacion`; el apunte
   tiene `Matricula` + `Id_Ciudad`, sin fecha de graduación. El enunciado pide
   **las dos cosas**: ninguna de las dos versiones está completa.

Regla de pasaje que sí es de cátedra — `unidad 2.pdf` p. 13, textual: *"en el modelo
normalizado las relaciones muchos a muchos **NO existen**... se transforman en una nueva
tabla que se conoce con el nombre de **tabla asociativa o relacional**"*.

Todo esto está practicable en [`practica/der-mer-interactivo.html`](practica/der-mer-interactivo.html).

---

## Estado de cobertura y numeración

Sin renombrar ningún archivo escrito. El número es orden de lectura, no de escritura
— precedente: la `0010` se escribió primera.

**Ya escrito y en el parcial:**

- `0019`–`0023` — las tres formas normales y el fin de la normalización ✅
- `0024` — historicidad ✅
- `0025`, `0026` — los dos integradores de normalización ✅
- `0002` — el DBMS (por si cae algo de Unidad 1) ✅
- `0006` — ciclo de vida de una BD (pregunta 1 del parcial tomado) ✅

**Falta, y entra:**

| Lección | Tema | Prioridad |
|---|---|---|
| `0027` | Almacenamiento: primario/secundario/terciario, caché, cinta vs disco | baja |
| `0028` | Índices: los tres tipos del docente + denso/no denso | **alta** |
| `0041` | Transacciones y ACID | **alta** |
| `0013`, `0014` | Especialización: exclusiva vs solapada, exclusividad | **alta** |
| `0008` | Los cinco tipos de atributo (con derivable a fondo) | **alta** |
| `0009` | Relaciones y grado: unaria, binaria | media |
| `0018` | **Integrador**: MER desde un enunciado, a mano | **alta** |

**Hecho (2026-09-21).** `0006` es ahora el ciclo de vida, en Unidad 1; los dos primeros
temas de Unidad 2, ambos sin escribir, quedaron fusionados en `0007`.
`0010` y todo lo de Unidad 3 no se tocan.

**DIFERIDO al 2do parcial** — confirmado por los docentes, no entra acá:

| Lección | Tema | Fuente |
|---|---|---|
| `0029` | Store procedures, funciones y disparadores | `unidad 4 DDL.pdf` pp. 7–11 |
| `0031` | DDL: `CREATE`, `ALTER`, `DROP` y las restricciones | `unidad 4 DDL.pdf` pp. 1–7 |

El material ya lo tenemos entero y es bueno, así que estas dos lecciones se pueden escribir
igual — pero **después** del 24/09. Nada de gastar la semana ahí.

---

## Orden de ataque

Dos carreras separadas, porque son dos gates separados.

**Práctica** — la que "vas a sacar", pero no la regales:

1. `0018` — modelar un MER desde un enunciado, **a mano**, contra reloj. Empezá por Farmacia,
   que el docente nombró. Es lo único práctico sin cubrir.
2. Repaso de `0025` y `0026` en una hora de reloj, drilleando los dos errores: **fuera los
   campos calculados**, y **PK en cada tabla resultante**.

**Teoría** — tu punto débil real, por lo que dijo el docente:

3. `0028` índices — tiene pregunta textual confirmada.
4. `0041` transacciones y ACID.
5. `0013`, `0014` especialización exclusiva/solapada.
6. `0008` atributo derivable (qué es **y para qué se usa**) y `0009` unarias/binarias.
7. Notación a mano: doble elipse, punteada, cardinalidades, pata de gallo.
8. `0027` almacenamiento, si sobra tiempo.
