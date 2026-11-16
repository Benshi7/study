# Probabilidad Básica

> Nota de alcance: este bloque cubre lo que aparece en el material de la cátedra (TEORÍA DE LA PROBABILIDAD, GLOSARIO PROBABILIDADES, RESUMEN PROBABILIDAD, probabilidades.pdf). No incluye combinatoria (permutaciones/combinaciones) porque no aparece en estos PDFs — si el final la toma, conviene armar un bloque aparte con esos apuntes.

## Conceptos clave

### Experimento determinístico vs. aleatorio
- **Experimento determinístico**: su resultado se puede predecir con certeza. Ej: congelar agua a 0°C.
- **Experimento aleatorio (o no determinístico)**: no se puede predecir el resultado con exactitud, aunque se conozcan todos los resultados posibles. Necesita al menos dos resultados posibles. Ej: tirar un dado.

### Espacio muestral (E)
Conjunto de **todos** los resultados posibles de un experimento aleatorio.
Ejemplo: tirar un dado → E = {1, 2, 3, 4, 5, 6}.

### Suceso o evento
Es un subconjunto del espacio muestral (un conjunto de puntos muestrales).
- **Suceso imposible**: nunca ocurre (∅).
- **Suceso seguro o cierto**: ocurre siempre (coincide con E).

Ejemplo: A = "sale un número par al tirar un dado" → A = {2, 4, 6}.

### Definiciones de probabilidad

**1. Definición clásica o de Laplace**

P(A) = (casos favorables a A) / (casos posibles)

Solo se puede usar si todos los resultados del espacio muestral son **igualmente posibles** (equiprobables).

Ejemplo: P(sacar un número par al tirar un dado) = 3/6 = 1/2.

**2. Definición frecuencial**

P(A) ≈ fr = (n° de éxitos) / (n° de ensayos), repitiendo el experimento *n* veces, con *n* lo más grande posible.

Es una aproximación empírica: cuantas más repeticiones, más se acerca la frecuencia relativa a la probabilidad real.

**3. Definición axiomática (Kolmogorov)**

P(A) es un número real que cumple:
1. P(A) ≥ 0
2. P(E) = 1
3. P(A ∪ B) = P(A) + P(B) si A y B son mutuamente excluyentes (A ∩ B = ∅)

Consecuencia: 0 ≤ P(A) ≤ 1.

### Complemento de un suceso
El complemento de A (Ā) es todo lo que **no** es A dentro de E.

P(Ā) = 1 − P(A) y por lo tanto P(A) + P(Ā) = 1.

### Clasificación de sucesos

- **Mutuamente excluyentes (o incompatibles)**: no pueden ocurrir al mismo tiempo. A ∩ B = ∅. Ej: sacar una carta que sea copa Y que sea oro (no puede ser las dos cosas a la vez).
- **No excluyentes (o compatibles)**: sí pueden ocurrir simultáneamente. A ∩ B ≠ ∅. Ej: sacar una carta que sea un 5 y que sea de oro (el 5 de oro cumple ambas).
- **Exhaustivos**: su unión es todo el espacio muestral. A ∪ B = E.
- **Complementarios**: son exhaustivos Y excluyentes al mismo tiempo (las dos condiciones juntas). Ej: A = "número par" y Ā = "número impar" al tirar un dado.
- **Independientes**: la probabilidad de uno no cambia por la ocurrencia del otro (típico: extracción **con** reposición).
- **Dependientes**: la probabilidad de uno sí se modifica según si el otro ocurrió o no (típico: extracción **sin** reposición).

### Probabilidad condicional
Es la probabilidad de que ocurra un suceso, sabiendo que otro ya ocurrió (reduce el espacio muestral).

P(B/A) = P(A ∩ B) / P(A), se lee "probabilidad de B habiendo ocurrido A" (o dado A).

Ejemplo con tabla de contingencia: de 150 personas, 70 son mujeres y de esas 30 están en contra. P(en contra / mujer) = 30/70 ≈ 0,4286.

### Teorema de la probabilidad total
Si A₁, A₂, ..., Aₙ son sucesos mutuamente excluyentes que forman un sistema exhaustivo (cubren todo E), y B es cualquier suceso con P(B) ≠ 0:

P(B) = Σ P(Aᵢ) · P(B/Aᵢ)

Se resuelve fácil con un **diagrama de árbol**: se consideran todas las ramas que llegan a B y se suman.

Ejemplo: un supermercado compra a 3 proveedores (A: 45%, B: 32%, C: 23%) y cada uno tiene distinto % de bolsas rotas (4%, 6%, 2,5%). La probabilidad de que llegue una bolsa rota es:
P(R) = 0,45·0,04 + 0,32·0,06 + 0,23·0,025 = 0,04295

### Teorema de Bayes (o de la probabilidad de las causas)
Permite "invertir" una probabilidad condicional: dado que ya ocurrió B, ¿cuál es la probabilidad de que la causa haya sido Aₖ?

P(Aₖ/B) = [P(Aₖ) · P(B/Aₖ)] / [Σ P(Aᵢ) · P(B/Aᵢ)]

El denominador es exactamente el teorema de la probabilidad total (P(B)).

Nota de la cátedra: a P(Aₖ/B) se la llama **probabilidad a posteriori**.

Ejemplo (continuación del anterior): si la bolsa llegó rota, ¿cuál es la probabilidad de que sea del proveedor A?
P(A/R) = 0,018 / 0,04295 = 0,4191

## Fórmulas de referencia rápida

| Fórmula | Nombre | Cuándo se usa |
|---|---|---|
| P(A) = casos favorables / casos posibles | Laplace | Espacio muestral equiprobable |
| P(A) = n° de éxitos / n° de ensayos | Frecuencial | Cuando no hay equiprobabilidad, se estima con muchas repeticiones |
| P(Ā) = 1 − P(A) | Complemento | Cuando es más fácil calcular "lo contrario" |
| P(A∪B) = P(A) + P(B) | Regla de la suma (mutuamente excluyentes) | Calcular P(A o B) cuando A y B no pueden pasar juntos |
| P(A∪B) = P(A) + P(B) − P(A∩B) | Regla de la suma (caso general) | Calcular P(A o B) cuando A y B sí pueden pasar juntos (evita contar dos veces la intersección) |
| P(A∩B) = P(A)·P(B) | Regla del producto (independientes) | Calcular P(A y B) cuando un suceso no afecta al otro (con reposición) |
| P(A∩B) = P(A)·P(B/A) | Regla del producto (dependientes) | Calcular P(A y B) cuando un suceso afecta al otro (sin reposición) |
| P(B/A) = P(A∩B) / P(A) | Probabilidad condicional | Calcular P(de B) sabiendo que ya ocurrió A |
| P(B) = Σ P(Aᵢ)·P(B/Aᵢ) | Probabilidad total | Cuando B puede ocurrir por distintas "causas" o caminos que cubren todo E |
| P(Aₖ/B) = P(Aₖ)·P(B/Aₖ) / Σ P(Aᵢ)·P(B/Aᵢ) | Teorema de Bayes | Cuando ya sabés que B ocurrió y querés la probabilidad de una causa puntual |
| Ā∪B̄ = (A∩B)‾ ; Ā∩B̄ = (A∪B)‾ | Leyes de De Morgan | Para pasar de "no (A y B)" a "no A o no B" y viceversa |

**Cómo probar que dos sucesos son independientes** (alcanza con probar UNA de estas tres igualdades):
- P(A∩B) = P(A)·P(B)
- P(A) = P(A/B)
- P(B) = P(B/A)

## Confusiones típicas / trampas de examen multiple choice

Esta es la parte más importante para repasar. Son los errores que más aparecen en los multiple choice.

### 1. Independientes ≠ Mutuamente excluyentes (la trampa más común)
Son conceptos DISTINTOS que la gente confunde todo el tiempo:
- **Mutuamente excluyentes** habla de si A y B **pueden ocurrir juntos o no** (es sobre el espacio muestral, geometría de conjuntos).
- **Independientes** habla de si la ocurrencia de uno **cambia la probabilidad** del otro (es sobre cómo se relacionan las probabilidades).

Relación (memorizarla, aparece seguido en el final):
- Si A y B son **independientes** → **no** son mutuamente excluyentes (salvo casos triviales de probabilidad 0).
- Si A y B son **mutuamente excluyentes** → **no** son independientes.
- Si A y B **no son mutuamente excluyentes** → pueden ser independientes o no; hay que probarlo con la fórmula P(A∩B) = P(A)·P(B).

Ejemplo de la cátedra: A = "gano en el bingo", B = "día soleado". Son independientes (ganar el bingo no depende del clima), pero NO son mutuamente excluyentes (puede pasar que gane el bingo en un día soleado).

### 2. Probabilidad condicional vs. probabilidad conjunta
- P(A∩B) o P(A y B) = probabilidad de que pasen **las dos cosas** (probabilidad conjunta).
- P(B/A) = probabilidad de que pase B **sabiendo que A ya pasó** (probabilidad condicional, espacio muestral reducido).

Se relacionan por: P(A∩B) = P(A) · P(B/A). Si en el examen te dan la conjunta y la de un evento, podés despejar la condicional (y viceversa) — no las confundas ni las uses indistintamente.

### 3. "Y" en el enunciado no siempre es intersección; "o" no siempre es unión
En el lenguaje coloquial, cuando el enunciado pide una probabilidad conjunta usamos la palabra "y" (que matemáticamente es ∩) y cuando pide una probabilidad de que ocurra al menos uno de dos sucesos usamos "o" (que matemáticamente es ∪). Cuidado: esta correspondencia (y=∩, o=∪) es la convención que da la cátedra para traducir el enunciado a fórmula, no una regla lógica general.

### 4. Con reposición (independiente) vs. sin reposición (dependiente)
- **Con reposición**: la composición no cambia entre extracciones → sucesos **independientes** → se usa P(A∩B) = P(A)·P(B).
- **Sin reposición**: la composición cambia después de cada extracción → sucesos **dependientes** → se usa P(A∩B) = P(A)·P(B/A), y la segunda probabilidad se calcula sobre el espacio *reducido*.

**Convención de la cátedra (importante para el multiple choice):** si el ejercicio NO especifica si la extracción es con o sin reposición, se asume que es **sin reposición** (dependiente).

### 5. Regla de la suma: olvidarse de restar la intersección
Error clásico: aplicar P(A∪B) = P(A) + P(B) aunque A y B **no** sean mutuamente excluyentes. Ahí hay que restar la intersección: P(A∪B) = P(A) + P(B) − P(A∩B), porque si no, contás dos veces los casos que están en ambos.

Truco para detectar la trampa en el enunciado: si los dos sucesos pueden compartir elementos (por ejemplo "sacar un 3 o una carta de copa" — el 3 de copa cumple ambas), NO son excluyentes y hay que restar la intersección.

### 6. Sucesos exhaustivos vs. complementarios
- **Exhaustivos**: alcanza con que la unión sea E (pueden solaparse).
- **Complementarios**: exigen DOS condiciones a la vez: ser exhaustivos Y ser mutuamente excluyentes.

Todo par de complementarios (A, Ā) es automáticamente exhaustivo y excluyente, pero no todo par exhaustivo es complementario (podrían solaparse).

### 7. Teorema de Bayes vs. Teorema de la probabilidad total (se confunden porque comparten fórmula)
- **Probabilidad total** responde: "¿cuál es la probabilidad de B en total, considerando todos los caminos posibles?" → P(B) = Σ P(Aᵢ)·P(B/Aᵢ).
- **Bayes** responde: "ya sé que ocurrió B, ¿cuál es la probabilidad de que la causa haya sido Aₖ en particular?" → invierte la condicional.

Ambos usan el mismo denominador (la suma de probabilidad total), pero Bayes agrega el numerador P(Aₖ)·P(B/Aₖ) para aislar una causa puntual. Si el enunciado pregunta "¿cuál es la probabilidad de que llegue rota?" es probabilidad total; si pregunta "si llegó rota, ¿cuál es la probabilidad de que sea del proveedor X?" es Bayes.

### 8. Traducción de enunciados a notación (glosario de la cátedra)
Si n es el total de casos:
- "como máximo k" / "a lo sumo k" → P(x ≤ k)
- "como mínimo k" / "por lo menos k" → P(x ≥ k)
- "más de la mitad" → P(x > n/2)
- "menos de la mitad" → P(x < n/2)
- "ninguno" → P(x = 0)
- "alguno" → P(x ≥ 1)
- "entre a y b" → P(a ≤ x ≤ b) = P(x ≤ b) − P(x ≤ a−1)

Trampa típica: confundir "más de la mitad" (estricto, >) con "por lo menos la mitad" (≥). Leer bien el enunciado.

## Preguntas de autoevaluación

**1.** Se sabe que A y B son sucesos independientes. ¿Cuál de las siguientes afirmaciones es correcta?
a) A y B son necesariamente mutuamente excluyentes
b) A y B no pueden ser mutuamente excluyentes
c) A y B son complementarios
d) No se puede determinar nada sobre su exclusión mutua

**Correcta: b.** Si dos sucesos son independientes, no son mutuamente excluyentes (salvo casos triviales de probabilidad cero). Independencia y exclusión mutua son conceptos distintos: uno habla de si se afectan las probabilidades, el otro de si pueden ocurrir juntos.

---

**2.** De una urna con 8 bolillas rojas y 4 azules se extraen dos bolillas SIN reposición. ¿Qué fórmula corresponde para calcular P(ambas rojas)?
a) P(R₁)·P(R₂) con P(R₂) = 8/12
b) P(R₁)·P(R₂/R₁) con P(R₂/R₁) = 7/11
c) P(R₁) + P(R₂)
d) P(R₁∪R₂)

**Correcta: b.** Sin reposición, los sucesos son dependientes: la segunda extracción se hace sobre un espacio reducido (11 bolillas, de las cuales quedaron 7 rojas si la primera salió roja). Se usa la regla del producto para dependientes.

---

**3.** Un enunciado dice: "calcular la probabilidad de que salga un 3 o una carta de oro" en un mazo de 40 cartas. ¿Qué regla hay que aplicar?
a) P(3) + P(oro), porque son mutuamente excluyentes
b) P(3) + P(oro) − P(3 y oro), porque no son mutuamente excluyentes
c) P(3) · P(oro)
d) P(3/oro)

**Correcta: b.** El 3 de oro pertenece a ambos sucesos, por lo tanto no son mutuamente excluyentes y hay que restar la intersección para no contar dos veces ese caso.

---

**4.** ¿Cuál es la diferencia principal entre P(A∩B) y P(B/A)?
a) Son la misma cosa, solo cambia la notación
b) P(A∩B) es la probabilidad de que ocurran ambos sucesos; P(B/A) es la probabilidad de B asumiendo que A ya ocurrió
c) P(A∩B) siempre es mayor que P(B/A)
d) P(B/A) solo se usa cuando los sucesos son independientes

**Correcta: b.** P(A∩B) es la probabilidad conjunta (ambos ocurren); P(B/A) es la probabilidad condicional (B, dado que A ya pasó, sobre un espacio muestral reducido). Se relacionan por P(A∩B) = P(A)·P(B/A).

---

**5.** Un ejercicio no aclara si la extracción de dos cartas de un mazo es con o sin reposición. Según la convención de la cátedra, ¿cómo hay que resolverlo?
a) Se asume con reposición (independiente)
b) Se asume sin reposición (dependiente)
c) No se puede resolver sin esa información
d) Depende del número de cartas del mazo

**Correcta: b.** La convención de la cátedra indica que si no se especifica, se asume que la extracción es sin reposición (dependiente).

---

**6.** Sean A y B sucesos tales que A ∪ B = E y A ∩ B = ∅. ¿Cómo se llama esta relación entre A y B?
a) Independientes
b) Mutuamente excluyentes solamente
c) Complementarios
d) Compatibles

**Correcta: c.** Complementarios exige las dos condiciones simultáneamente: ser exhaustivos (A∪B = E) y ser mutuamente excluyentes (A∩B = ∅).

---

**7.** En una encuesta a 150 personas, 70 son mujeres y de esas 30 están en contra de una medida. ¿Qué representa el cálculo 30/70?
a) P(mujer y en contra)
b) P(en contra / mujer)
c) P(mujer / en contra)
d) P(mujer) + P(en contra)

**Correcta: b.** Es una probabilidad condicional: sobre el total de mujeres (70, el espacio reducido), cuántas están en contra (30). Se lee "probabilidad de estar en contra, dado que es mujer".

---

**8.** Un supermercado compra a tres proveedores con distintos porcentajes de compra y distintos porcentajes de productos defectuosos en cada uno. Te preguntan: "si llegó un producto defectuoso, ¿cuál es la probabilidad de que sea del proveedor B?". ¿Qué herramienta hay que usar?
a) Teorema de la probabilidad total
b) Regla de la suma
c) Teorema de Bayes
d) Regla del producto para independientes

**Correcta: c.** Es Bayes porque ya se sabe que ocurrió el efecto (producto defectuoso) y se pregunta por la probabilidad de una causa puntual (proveedor B). La probabilidad total se usaría si preguntaran "¿cuál es la probabilidad de que llegue un producto defectuoso en general?" (sin condicionar a una causa particular).

---

**9.** Si P(A) = 0,4 y P(A/B) = 0,4, ¿qué se puede concluir sobre A y B?
a) A y B son mutuamente excluyentes
b) A y B son independientes
c) A y B son complementarios
d) No se puede concluir nada

**Correcta: b.** Una de las formas de probar independencia es que P(A) = P(A/B) (que el hecho de que ocurra B no cambie la probabilidad de A).

---

**10.** El enunciado dice "la probabilidad de aprobar como mínimo 3 materias de las 5 que rindió" (n=5). ¿Cómo se traduce a notación?
a) P(x ≤ 3)
b) P(x < 3)
c) P(x ≥ 3)
d) P(x = 3)

**Correcta: c.** "Como mínimo" o "por lo menos" se traduce como P(x ≥ k), es decir, esa cantidad o más.

---

**11.** Se sabe que A y B son mutuamente excluyentes. ¿Cuál de las siguientes afirmaciones es correcta?
a) A y B son independientes
b) A y B no pueden ser independientes (salvo casos triviales)
c) P(A∩B) = P(A)·P(B) necesariamente
d) A y B son complementarios

**Correcta: b.** Si A y B son mutuamente excluyentes, P(A∩B) = 0. Para que sean independientes debería cumplirse P(A∩B) = P(A)·P(B), lo cual solo pasaría si P(A) = 0 o P(B) = 0 (caso trivial). En general, mutuamente excluyentes implica NO independientes.

---

**12.** ¿Qué axioma de Kolmogorov garantiza que 0 ≤ P(A) ≤ 1 para cualquier suceso A?
a) Es una consecuencia de los tres axiomas combinados (P(A)≥0, P(E)=1, y la aditividad para excluyentes), no un axioma en sí mismo
b) Es el segundo axioma directamente
c) Es el primer axioma directamente
d) No se puede garantizar, hay que probarlo caso por caso

**Correcta: a.** Los tres axiomas son: P(A)≥0, P(E)=1, y P(A∪B)=P(A)+P(B) si son excluyentes. La propiedad 0≤P(A)≤1 es una consecuencia que se deriva de estos tres, no un axioma independiente.
