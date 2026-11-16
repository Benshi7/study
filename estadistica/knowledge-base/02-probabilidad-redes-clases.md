# Probabilidad — Redes Conceptuales y Apuntes de Clase

> Nota de alcance: los PDFs de este bloque ("C1-RESUMEN-RED CONCEPTUAL", "cont red", "clase 25-3") son en realidad la red conceptual y los ejercicios de **Estadística Descriptiva** (Unidad 1 de la cátedra), no de probabilidad pura. Se incluyen igual porque son el mapa completo que usa la cátedra para ubicar a la Probabilidad dentro de la materia, y porque varios conceptos (frecuencia relativa, coeficiente de variación) son la base directa de ideas que después se usan en probabilidad y distribuciones. El único apunte que es 100% probabilidad es "clase 1-4-26 fep" (tablas de contingencia, condicional, independencia, regla de la multiplicación). Para la teoría dura de probabilidad (axiomas, Bayes, etc.) el bloque de referencia es `01-probabilidad-basica.md`.

## Mapa de conceptos

### Red 1 — De dónde sale la Probabilidad dentro de la materia (C1-RESUMEN)

```
ESTADÍSTICA (estudia fenómenos aleatorios)
├── DESCRIPTIVA (trabaja con la muestra m, describe lo que ya se observó)
│   └── N = Población → se le extrae una MUESTRA m
│       └── X = Variable (característica de interés)
│           ├── CUANTITATIVA (números)
│           │   ├── CONTINUA → admite decimales
│           │   └── DISCRETA → admite solo enteros
│           └── CUALITATIVA (atributos)
│               ├── ORDINAL → implica jerarquía/orden
│               └── NOMINAL → sin orden
│
│   Proceso de trabajo con datos (los 5 pasos, en orden — cada uno depende del anterior):
│   1) RECOPILAR ("juntar" datos: encuesta, observación directa)
│   2) ORGANIZAR ("ordenar")
│   3) PRESENTAR → tabular datos → arreglo de frecuencia (v. discreta) o
│      distribución de frecuencias por intervalos/clases (v. continua)
│   4) ANALIZAR → métodos gráficos (bastones/barras/histogramas) y métodos numéricos
│   5) INTERPRETAR
│
└── INFERENCIAL (generaliza de la muestra a la población; necesita PROBABILIDAD
    como base matemática para poder cuantificar la incertidumbre de esa generalización)
```

Puntos de la tabla de frecuencias (vocabulario que reaparece en probabilidad de variables discretas más adelante):
- f = frecuencia absoluta (cuántas veces se repite un valor)
- F = frecuencia acumulada
- fr = frecuencia relativa = f/n
- Fr = frecuencia acumulada relativa = F/n
- Marca de clase (Xm) = punto medio del intervalo; Amplitud (a) = ancho del intervalo; los intervalos se escriben cerrados a izquierda y abiertos a derecha [Li ; Ls).

### Red 2 — Métodos numéricos (cont red.pdf)

```
MÉTODOS NUMÉRICOS
├── MEDIDAS DE TENDENCIA CENTRAL
│   ├── Media aritmética ("promedio") — x̄ en muestra, μ en población
│   ├── Mediana (Me) — "el del medio"; requiere datos ordenados
│   └── Moda (Mo) — "el de mayor frecuencia, el que más se repite"
└── MEDIDAS DE VARIABILIDAD
    ├── Varianza — S² en muestra, σ² en población
    ├── Desvío = √Varianza — S en muestra, σ en población
    └── Coeficiente de Variación (CV) = (desvío/promedio) · 100%
        ├── CV < 20% → "los datos son homogéneos"
        └── CV < 5%  → "el promedio es representativo" (umbral más exigente)
            ⚠ Discrepancia: este apunte de clase dice 5%, pero la clave del TP1 y el resto
              del material usan 10%. Convención adoptada: 10% (la de los TPs corregidos).
              Si en el examen una opción dice 5% y otra 10%, priorizar 10%.
```

Distinción importante que remarca la cátedra en verde: **Parámetro** = valor calculado sobre la Población (μ, σ, σ²) vs. **Estadístico** = valor calculado sobre la Muestra (x̄, S, S²). Esta distinción es la misma que después se usa en Inferencial para estimar parámetros a partir de estadísticos.

### Red 3 — Probabilidad propiamente dicha (clase 1-4-26 fep.pdf)

```
Experimento aleatorio → se organiza en TABLA DE CONTINGENCIA (filas/columnas = eventos)
    ↓
Probabilidad simple: P(evento) = casos del evento / total (#E)
    ↓
Combinación de eventos:
    ├── Unión: P(A∪B) = P(A) + P(B) − P(A∩B)   (regla general, resta la intersección)
    └── Condicional: P(A/B) = P(A∩B) / P(B), con P(B) ≠ 0
            ↓
        Definición de independencia: A y B son independientes si P(A/B) = P(A)
            ↓
        Si son independientes → P(A∩B) = P(A)·P(B)  (caso particular de la regla del producto)
            ↓
        Regla de la multiplicación (caso general, para eventos secuenciales):
        P(A₁∩A₂) = P(A₂/A₁) · P(A₁)
            ├── CON reposición → A₁ y A₂ independientes → P(A₂/A₁) = P(A₂)
            └── SIN reposición → A₁ y A₂ dependientes → P(A₂/A₁) se calcula sobre
                el espacio muestral reducido (un caso menos en el numerador Y en el denominador)
```

## Puntos reforzados en clase

Estas son aclaraciones que el profesor hizo en vivo y que no siempre quedan tan explícitas en un resumen:

1. **Por qué se puede "cancelar" S en una ecuación tipo S/x̄ = S** (Ejercicio 5, clase 25-3): el profesor aclara que se puede asumir S ≠ 0 porque "si fuera S = 0, todos los valores de la variable serían iguales" — y en el enunciado los valores son distintos. Es el tipo de justificación que un multiple choice puede pedir como "paso justificado".

2. **Posición de la mediana: NO es la misma fórmula para lista de datos crudos que para tabla de frecuencias.** Esto se remarca explícitamente como algo para recordar:
   - Lista de datos (datos sueltos, sin tabla): posición de la mediana = (n+1)/2, equivalente a 50/100·(n+1).
   - Tabla de frecuencias acumuladas: se usa n/2 (sin el +1) para ubicar la fila donde "vive" la mediana según F.
   Mismo criterio aplica para cuartiles y percentiles: con lista de datos se usa k/100·(n+1); con tabla de frecuencias se usa k/100·n.

3. **Cuidado al leer qué percentil te está preguntando el problema, sobre todo si hay que despejarlo "al revés".** En el ejercicio 7f (clase 25-3), pedían el porcentaje de paquetes con "al menos 34 gramos". Al despejar la incógnita k en la fórmula del percentil, el resultado da k = 32, PERO eso significa que el peso de 34 gr es el **percentil 32** (deja 32% por debajo), no el percentil 34. El profesor lo marca con un "¡ojo!" en el apunte porque es un error muy fácil de cometer: confundir el valor del dato con el número del percentil que le corresponde.

4. **Diferencia entre "independientes" y que un suceso "no afecte" al otro, mostrada con números concretos** (clase 1-4-26): usando la tabla de contingencia de máquinas A/B y torvillos defectuosos, se calcula P(A) = 4/9 y P(A/D) = 2/3. Como son distintos, el profesor concluye explícitamente: "como la ocurrencia de D modifica la P(A), resulta que A y D NO son independientes". Es la forma más concreta de mostrar que hay que comparar P(A) contra P(A/B) con números reales, no "a ojo".

5. **La independencia se puede romper aunque parezca simétrica.** En el ejemplo del mazo de 40 cartas, A="copa o espada" no es independiente de B="no copa", pero SÍ es independiente de C="copa u oro". El punto pedagógico es que no hay que asumir independencia por la forma del enunciado: hay que probarla siempre con la cuenta P(A∩B) =? P(A)·P(B).

6. **Comparación visual "con reposición" vs "sin reposición"** (regla de la multiplicación): en el mismo ejercicio (sacar as y luego rey de un mazo de 40) se resuelven las dos versiones una debajo de la otra: sin reposición da 4/40 · 4/39 (el denominador de la segunda extracción bajó a 39); con reposición da 4/40 · 4/40 (el denominador se mantiene en 40). Verlas juntas ayuda a fijar que la única diferencia es si el "universo" de la segunda extracción cambia o no.

## Ejemplos resueltos

### 1. Tabla de contingencia — probabilidad simple, unión y condicional (clase 1-4-26)

Enunciado: en una fábrica hay dos máquinas A y B. Un día, A fabrica 8 tornillos (2 defectuosos) y B fabrica 10 tornillos (1 defectuoso).

Tabla de contingencia:

| | D (defectuoso) | D̄ | Total |
|---|---|---|---|
| A | 2 | 6 | 8 |
| B | 1 | 9 | 10 |
| Total | 3 | 15 | 18 |

- a) P(D) = #D / #E = 3/18 = **1/6**
- b) P(A) = #A / #E = 8/18 = **4/9**
- c) P(D∪A) = P(D) + P(A) − P(D∩A) = 1/6 + 4/9 − 1/9 = 9/18 = **1/2** (P(D∩A) = 2/18 = 1/9, porque hay 2 tornillos que son de A Y defectuosos)
- d) P(A/D) = P(A∩D)/P(D) = (2/18)/(3/18) = 2/3. Como P(A) = 4/9 ≠ P(A/D) = 2/3, **A y D no son independientes**.

### 2. Verificación de independencia con mazo de cartas (clase 1-4-26)

De un mazo de 40 cartas españolas se elige una al azar. A = "copa o espada" (#A=20), B = "no copa" (#B=30), C = "copa u oro" (#C=20).

- i) ¿A y B independientes? P(A) = 1/2, P(B) = 3/4, P(A∩B) = 10/40 = 1/4. Como P(A)·P(B) = 1/2·3/4 = 3/8 ≠ 1/4, **no son independientes**.
- ii) ¿A y C independientes? P(A) = 1/2, P(C) = 1/2, P(A∩C) = 10/40 = 1/4 (las cartas de copa). Como P(A)·P(C) = 1/2·1/2 = 1/4 = P(A∩C), **sí son independientes**.

### 3. Regla de la multiplicación, con y sin reposición (clase 1-4-26)

Se sacan 2 cartas de un mazo de 40, una tras otra. Hallar P(1ª sea as ∩ 2ª sea rey).

- Sin reposición: P(A₁∩A₂) = P(A₂/A₁)·P(A₁) = (4/39)·(4/40)
- Con reposición: P(A₁∩A₂) = P(A₂/A₁)·P(A₁) = (4/40)·(4/40)

La única diferencia es el denominador de la segunda probabilidad (39 si no hay reposición, porque ya se sacó una carta; 40 si hay reposición, porque el mazo vuelve a estar completo).

### 4. Cuartiles y percentiles con datos agrupados en intervalos (clase 25-3, Ejercicio 7)

Distribución de pesos (gramos) de 200 paquetes, en 7 intervalos de amplitud 2 (de [30,32) a [42,44)), con f y F ya calculados.

- Para hallar la mediana: se busca la posición n/2 = 100. Como F=100 no aparece exactamente, se toma el primer F que la supera (F=107, intervalo [34,36)) y se aplica:
  Me = LI + [(n/2 − Fa)/f]·a = 34 + [(100−64)/43]·2 = **35,67 gramos**
- Para un percentil Pk (ej. P20): se busca k·n/100 (=40 para P20), se ubica el intervalo donde "cae" ese acumulado, y se aplica la misma lógica con la fórmula:
  Pk = LI + [(k·n/100 − Fa)/f]·a → P20 = 32 + [(40−28)/36]·2 = **32,66 gramos**

Esta es la misma lógica que la mediana (que es, de hecho, el percentil 50) y que los cuartiles (percentiles 25, 50 y 75).

### 5. "Truco algebraico" con el Coeficiente de Variación (clase 25-3, Ejercicio 5)

Distribución discreta de 6 valores: -10, 3, a, 10, 1, 0. Se sabe que la desviación típica (S) es igual al coeficiente de variación de Pearson (CV = S/x̄).

- Planteo: CV = S → S/x̄ = S. Como S ≠ 0 (si lo fuera, todos los valores serían iguales, y no lo son), se puede dividir ambos lados por S: **x̄ = 1**.
- Con x̄ = 1 conocido, se despeja el valor desconocido a partir de la fórmula de la media:
  x̄ = (−10+3+a+10+1+0)/6 = 1 → a+4 = 6 → **a = 2**

Es un ejemplo típico de multiple choice: no hace falta calcular S explícitamente, alcanza con manipular la ecuación CV = S para despejar x̄ directamente.

## Conexión con distribuciones

Estos son los puentes que conectan lo visto en este bloque con Variables Aleatorias y Distribuciones (unidad posterior):

- **Frecuencia relativa (fr = f/n) → probabilidad puntual.** La tabla (x, f) de una variable discreta —vista en la Red 1 como "arreglo de frecuencia"— es exactamente el mismo objeto que después se llama función de probabilidad P(X=x) de una variable aleatoria discreta: en vez de "cuántas veces se repite x en la muestra", se pregunta "con qué probabilidad ocurre x". La Binomial y la Poisson (vistas más adelante) son casos particulares de esta idea con fórmulas cerradas para P(X=x).
- **Distribución de frecuencias por intervalos → densidad de probabilidad continua.** El histograma de la Red 1 (v. continua, con marca de clase, límites de intervalo y amplitud) es el antecedente directo de la función de densidad de la Distribución Normal: ahí el "área de cada barra" (frecuencia relativa) se transforma en "área bajo la curva" (probabilidad).
- **Media (x̄) y Varianza (S²) → Esperanza E(X) y Varianza Var(X).** Las mismas fórmulas de tendencia central y variabilidad de la Red 2 reaparecen sin cambiar de nombre cuando se trabaja con variables aleatorias: E(X) es la "media teórica" y Var(X) la "varianza teórica" de la distribución, calculadas con las probabilidades en lugar de las frecuencias relativas.
- **Independencia de eventos (Red 3) → independencia de variables aleatorias.** El mismo criterio P(A∩B)=P(A)·P(B) que se usa acá para dos eventos es la base de "variables aleatorias independientes" que se necesita más adelante para trabajar con la Suma de Variables (ver `SUMA DE VARIABLES.pdf`) y con la Distribución Muestral de la Media.
- **Probabilidad condicional y tabla de contingencia → tablas de doble entrada en variables aleatorias conjuntas** (si la cátedra las toma en el final, suelen aparecer con esta misma estructura de fila/columna que ya se practicó acá).
