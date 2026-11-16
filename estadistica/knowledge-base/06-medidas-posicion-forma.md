# Medidas de Posición y de Forma

Fuente: "Medidas de posición y de forma ( con anotaciones ).pdf" (14 páginas, presentación de la Prof. Elsa Diaz, con anotaciones manuscritas del usuario). El manuscrito es legible en su totalidad; no hay páginas ilegibles.

## Conceptos clave (percentiles, cuartiles, deciles, rango intercuartílico)

- **Medidas de posición (o de concentración)**: permiten establecer el porcentaje de datos concentrados dentro de un intervalo determinado. Cuartiles y percentiles son las medidas de posición trabajadas en el material (no aparecen deciles explícitamente en este PDF, pero son análogos: dividen la distribución en 10 partes iguales, D_k = P_(10k)).

- **Cuartiles (Q, 3 en total)**: dividen la distribución en 4 partes iguales de 25% cada una.
  - Q1: deja a la izquierda el 25% de las observaciones (y el 75% a la derecha).
  - Q2: es la mediana (50%/50%).
  - Q3: deja a la izquierda el 75% (y el 25% a la derecha, los "mayores").
  - Equivalencia con percentiles: Q1 = P25, Q2 = P50 = Mediana, Q3 = P75.

- **Percentiles (P, 99 en total)**: dividen la distribución en 100 partes iguales. El percentil P_k es el valor que supera al k% de los datos y es superado por el (100−k)%.
  - Ejemplo del material: "el 75% de los jubilados cobra menos de $9000" ⇒ P75 = 9000.
  - Ejemplo: "el 30% de los alumnos obtiene calificaciones mayores que 7" ⇒ ojo, esto NO es P30 = 7 directamente en el sentido ingenuo — hay que fijarse qué lado del porcentaje se da. Si el 30% obtiene MÁS que 7, entonces el 70% obtiene MENOS o igual que 7, por lo tanto P70 = 7 (el material lo marca explícitamente así: "P70 = 7"). Esta es una trampa clásica de lectura del enunciado.

- **Fórmula para variable continua (datos agrupados en intervalos)**, idéntica en estructura a la de la mediana pero generalizada a la posición k:
  
  P_k = L_I + [ (k·N/100 − F_a) / f ] · i

  Donde:
  - L_I: límite inferior del intervalo que contiene a P_k
  - N (o n): total de observaciones
  - F_a: frecuencia acumulada anterior al intervalo que contiene a P_k
  - f: frecuencia absoluta del intervalo que contiene a P_k
  - i: amplitud del intervalo

  **Pasos** (tal como los resalta el material):
  1. Determinar la posición: Pos = n·k/100
  2. Buscar el intervalo: es el que corresponde a la primera F (frecuencia acumulada) que iguale o supere la posición calculada.
  3. Aplicar la fórmula.

  Caso particular mediana (k=50): Me = L_I + [ (N/2 − F_a) / f ] · i

- **Rango intercuartílico (RIC)**: RIC = Q3 − Q1. Es una medida de dispersión robusta (no afectada por outliers), preferida sobre el desvío estándar cuando la distribución tiene fuerte asimetría. Se usa junto con la mediana (en lugar de media + desvío) para describir distribuciones muy asimétricas.

- **Diagrama de caja (boxplot)**: representa el 50% central de los datos como una caja (entre Q1 y Q3), con la mediana marcada dentro, y "bigotes" que representan el 25% inferior y el 25% superior restantes. Si un lado de la caja (o un bigote) tiene mayor longitud/área, indica que los datos en ese tramo están más dispersos.

## Medidas de forma (asimetría/skewness, curtosis) — fórmulas e interpretación de signo

El material NO trabaja curtosis (no aparece en las 14 páginas); solo cubre **asimetría**, basada en la comparación entre la Moda (Mo) y la Media (x̄):

- **Si Mo > x̄ (equivalente poblacional: Mo > μ)** ⇒ **Asimetría Negativa**. A los mayores valores de la variable les corresponden las mayores frecuencias (la "cola" larga queda a la izquierda).
- **Si Mo < x̄ (Mo < μ)** ⇒ **Asimetría Positiva**. A los menores valores de la variable les corresponden las mayores frecuencias (la "cola" larga queda a la derecha).
- **Si Mo = x̄ (Mo = μ)** ⇒ **Simetría**.

Regla mnemotécnica implícita en el material: pensar en la posición relativa de Mo respecto a x̄ en la recta numérica — si la Moda "se corrió" hacia la derecha (Mo > x̄), la cola larga (la asimetría) queda del lado izquierdo → negativa. Si la Moda quedó a la izquierda de la media (Mo < x̄), la cola larga queda a la derecha → positiva.

**Nota importante de coherencia con el TP1 (ver archivo 07)**: en el TPNº1 ejercicio 7, el usuario anotó "Mo > x̄ ⇒ Asimétrica Negativa" con Mo=36,5 y x̄=35,62 (Mo > x̄, correcto: negativa). Y en el ejercicio 10, con Mo=17,71 y x̄=20,3 (Mo < x̄), anotó correctamente "Asimétrica positiva". Ambos casos están bien aplicados según la regla del material.

## Qué remarcan las anotaciones manuscritas

Las anotaciones manuscritas de la profesora/usuario en este PDF son legibles y se concentran en:

1. **Diferenciar percentil de cuartil como "el mismo procedimiento con distinta posición"**: la anotación clave dice "Esto significa que para el cálculo de los cuartiles y percentiles se procederá de igual manera que con la mediana Me, pero ahora tendremos en cuenta la posición del cuartil o percentil buscado." Esto es la idea más importante para no confundir fórmulas: es UNA sola fórmula (la de Pk) que sirve para mediana, cuartiles y percentiles, cambiando solo el valor de k.

2. **Aclaración sobre el paso 2 (elegir el intervalo)**: se remarca "busco la F que iguale o supere a la posición" — error común es buscar el intervalo por el valor de f (frecuencia simple) en vez de F (acumulada), o quedarse con el intervalo anterior cuando la posición cae justo en el borde.

3. **Ejercicio resuelto completo (alturas de alumnos)**: sirve de plantilla numérica end-to-end: tabla de alturas con n=42, cálculo de P25 (posición=10,5 → intervalo [160,170) → P25=164,58 cm) y del porcentaje de alumnos que miden menos de 183 cm (se resuelve la fórmula de Pk "al revés", despejando k cuando el dato conocido es el valor de la variable y no el percentil — quedó k=82,62%).

4. **Distinción bigotes/caja en el boxplot**: anotación "1 cajones" (dos cajones: 25%+25% en el centro) y aclaración de que los "bigotes" son los 25% extremos de cada lado.

## Trampas de examen multiple choice

1. **Confundir "el k% obtiene MÁS que X" con "Pk = X"**: si el 30% obtiene calificaciones MAYORES que 7, el percentil de 7 es P70 (no P30), porque el percentil se define por lo que queda POR DEBAJO. Leer con cuidado de qué lado está el porcentaje dado.

2. **Usar f en lugar de F al buscar el intervalo**: la búsqueda del intervalo que contiene a Pk se hace con la frecuencia ACUMULADA (F), no con la frecuencia simple (f).

3. **Confundir Q2 con "el cuartil del medio en valor" en vez de "en posición de datos"**: Q2 es la MEDIANA (posición central de los datos ordenados), no el promedio de Q1 y Q3.

4. **Signo de la asimetría al revés**: memorizar mecánicamente "Mo > x̄ → positiva" es un error común; según este material (y la convención de Pearson clásica) es Mo > x̄ → NEGATIVA. Verificar siempre con el dibujo (cola larga = signo de la asimetría).

5. **Aplicar la fórmula de percentil a variable discreta cuando el enunciado da datos agrupados en intervalos de variable continua, o viceversa**: la fórmula con L_I e i (amplitud) es para intervalos (variable continua o discretizada en intervalos); para tablas de variable discreta sin intervalos el procedimiento cambia (se usa la F acumulada directamente sin fórmula de interpolación).

6. **Rango intercuartílico vs. rango total**: RIC = Q3 − Q1 (dispersión del 50% central), NO es lo mismo que el rango (máximo − mínimo).

## Preguntas de autoevaluación

**1.** Un percentil P_k para una variable continua agrupada en intervalos se calcula con la fórmula:
a) P_k = L_I + [(k·N/100 − F_a)/f] · i
b) P_k = L_S − [(k·N/100 − F_a)/f] · i
c) P_k = L_I + [(k·N/100 − f_a)/F] · i
d) P_k = (L_I + L_S)/2

**Correcta: a.** Es la fórmula general de interpolación en el intervalo; usa el límite inferior (L_I), la frecuencia acumulada anterior (F_a) y la frecuencia absoluta del intervalo (f), no al revés.

---

**2.** Si el 40% de los empleados de una empresa gana más de $500.000, ¿qué percentil corresponde a $500.000?
a) P40
b) P50
c) P60
d) P100

**Correcta: c.** Si el 40% gana MÁS, entonces el 60% gana MENOS o igual, por lo que $500.000 es el percentil 60 (P60).

---

**3.** En un diagrama de caja, ¿qué representa la longitud (o ancho) de la caja central?
a) El rango total de los datos
b) El 50% central de los datos (entre Q1 y Q3)
c) La desviación estándar
d) La moda

**Correcta: b.** La caja va de Q1 a Q3, conteniendo el 50% central de las observaciones; los bigotes representan el 25% inferior y el 25% superior.

---

**4.** Una distribución tiene Mo = 42 y x̄ = 38. ¿Qué tipo de asimetría presenta?
a) Asimetría positiva
b) Asimetría negativa
c) Simetría perfecta
d) No se puede determinar con esos datos

**Correcta: b.** Como Mo (42) > x̄ (38), la distribución es de asimetría negativa según la regla Mo > x̄ ⇒ asimetría negativa.

---

**5.** El rango intercuartílico (RIC) se calcula como:
a) Q3 + Q1
b) Q3 − Q1
c) (Q3 − Q1)/2
d) Máximo − Mínimo

**Correcta: b.** RIC = Q3 − Q1; mide la dispersión del 50% central de los datos, siendo robusto ante valores extremos.

---

**6.** Para hallar el intervalo donde se ubica un percentil P_k, se debe:
a) Buscar el intervalo cuya frecuencia simple f sea la mayor de la tabla
b) Buscar el primer intervalo cuya F (frecuencia acumulada) iguale o supere la posición calculada (n·k/100)
c) Buscar el intervalo central de la tabla
d) Promediar todos los límites de los intervalos

**Correcta: b.** El procedimiento de 3 pasos del material indica: calcular la posición (n·k/100), buscar el intervalo por la F acumulada que iguale o supere esa posición, y luego aplicar la fórmula de interpolación.

---

**7.** ¿Cuál de las siguientes afirmaciones sobre cuartiles es correcta?
a) Q1 = P75
b) Q2 = P50 = Mediana
c) Los cuartiles dividen la distribución en 3 partes iguales
d) Q3 deja a la izquierda el 25% de las observaciones

**Correcta: b.** Q2 coincide siempre con la mediana y con el percentil 50. Los cuartiles son 3 valores que dividen en 4 partes (no 3); Q1 = P25 y Q3 = P75.

---

**8.** En una distribución con fuerte asimetría, ¿qué par de medidas es más apropiado usar para describir tendencia central y dispersión?
a) Media aritmética y desvío estándar
b) Mediana y rango intercuartílico
c) Moda y varianza
d) Media geométrica y coeficiente de variación

**Correcta: b.** El material señala explícitamente: en distribuciones con gran asimetría es más apropiado medir tendencia central y dispersión mediante la mediana y el rango intercuartílico respectivamente, en vez de la media aritmética y la desviación típica (que son sensibles a outliers y a la asimetría).
