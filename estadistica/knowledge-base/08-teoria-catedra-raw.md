# Teoría de la cátedra (extracción directa de `raw/`)

Fuente: 12 PDFs de la Prof. Elsa Diaz (FEP, UNICABA) en `raw/`. Extracción hecha leyendo el texto con `lit` y renderizando las diapositivas como imagen para recuperar las fórmulas (el texto de las fórmulas sale ilegible). Los números y fórmulas de abajo son los que figuran en las diapositivas; cuando el cálculo exacto difiere del que muestra la diapositiva, se marca como **[Nota]**.

Índice de archivos:
1. DISTRIBUCIONES DISCRETAS DE PROBABILIDAD pdf.pdf (17 págs.)
2. DISTRIBUCIÓN BINOMIAL Y POISSON.pdf (24)
3. DISTRIBUCIÓN MUESTRAL DE LA MEDIA.pdf (12)
4. distribución muestral de la proporción.pdf (8)
5. DISTRIBUCIÓN NORMAL.pdf (22)
6. Fórmulas 1°Parcial.pdf (1)
7. GLOSARIO PROBABILIDADES.pdf (1)
8. Intervalos de confianza PARA LA MEDIA.pdf (26)
9. Intervalos de confianza PARA LA PROPORCIÓN.pdf (16)
10. RESUMIEN REGRESIÓN-CORRELACIÓN.pdf (2)
11. SUMA DE VARIABLES.pdf (16)
12. TEORÍA DE LA PROBABILIDAD.pdf (29)

---

## 1. DISTRIBUCIONES DISCRETAS DE PROBABILIDAD (variables aleatorias discretas)

**Definiciones**
- Variable aleatoria discreta: entre dos valores cualesquiera de su dominio existe a lo sumo un número finito de valores posibles. También "variables de conteo".
- Distribución de probabilidad: muestra los posibles resultados y la probabilidad de cada uno. Dos propiedades: P(r) ≥ 0 para todo r, y la sumatoria de todas las probabilidades = 1.
- Función de probabilidad: la fórmula que da P(r). En el dado es la definición clásica; en experimentos más complejos se usan Binomial o Poisson.
- Función de distribución acumulada: probabilidades acumuladas a la izquierda (F) y a la derecha (G):
  - F(r₀) = P(r ≤ r₀) = Σ P(r), ∀ r ≤ r₀
  - G(r₀) = P(r ≥ r₀) = Σ P(r), ∀ r ≥ r₀
  - "Comparando con estadística descriptiva": son las frecuencias acumuladas relativas por izquierda y por derecha.
- Esperanza: μ = E(r) = Σ rᵢ·P(rᵢ). "Valor que se espera obtener tras infinitas observaciones". Difiere del promedio descriptivo porque trabaja sobre lo que se espera, no sobre lo ya ocurrido; ambos muestran el "centro de gravedad".
- Varianza: σ² = V(r) = Σ (rᵢ − E(r))²·P(rᵢ). Desvío: D.S.(x) = √Var(x).
- CV = desvío/promedio · 100% (aplicado también a la variable aleatoria).

**Ejemplo dado (tabla P, F, G)**: r = {1..6}, P(r)=1/6.

| r | P(r) | F(r) | G(r) |
|---|------|------|------|
| 1 | 1/6 | 1/6 | 1 |
| 2 | 1/6 | 2/6 | 5/6 |
| 3 | 1/6 | 3/6 | 4/6 |
| 4 | 1/6 | 4/6 | 3/6 |
| 5 | 1/6 | 5/6 | 2/6 |
| 6 | 1/6 | 1 | 1/6 |

Traducción a F/G que usa la cátedra:
- P(r=3)=1/6; P(r≤4)=F(4)=4/6; P(r≥2)=G(2)=5/6
- P(r<5)=P(r≤4)=F(4)=4/6; P(r>5)=P(r≥6)=G(6)=1/6
- P(3≤r≤6)=F(6)−F(2)=1−2/6=5/6

E(r)=21/6=3,5; V(r)=2,917 (suma de (r−3,5)²·1/6 = 1,042+0,375+0,0417+0,0417+0,375+1,042). Nota de la cátedra: "los valores hallados se podrán obtener con alguna herramienta tecnológica".

**Ejemplo (bolillas, con reposición)**: caja con 3 bolillas numeradas {1,2,3}, se sacan 2 con reposición. Variable: suma de los números. 9 combinaciones; dominio r={2,3,4,5,6}.

| r | P(r) | F(r) | G(r) |
|---|------|------|------|
| 2 | 1/9 | 1/9 | 9/9=1 |
| 3 | 2/9 | 3/9 | 8/9 |
| 4 | 3/9 | 6/9 | 6/9 |
| 5 | 2/9 | 8/9 | 3/9 |
| 6 | 1/9 | 9/9=1 | 1/9 |

E(r)=4 y V(r)=1,33; **CV = 28,83% "> 20%" ⇒ "alta variabilidad o incertidumbre"**. **[Nota]** con V=4/3 el CV exacto sería 1,1547/4 = 28,87%; la diapositiva escribe 28,83%. El criterio práctico que usa la cátedra: CV > 20% = alta variabilidad.

---

## 2. DISTRIBUCIÓN BINOMIAL Y POISSON

**Binomial** (nombre de la cátedra: "X ~ Bi(n; p)")
- Experimento dicotómico: espacio muestral con solo dos resultados mutuamente excluyentes que forman sistema exhaustivo. n repeticiones idénticas de un ensayo con resultados "éxito"/"fracaso"; p constante en las n pruebas; independencia.
- Variable: X = número de éxitos en n pruebas independientes. Dominio x = {0, 1, 2, 3, …, n}. Parámetros n (cantidad de repeticiones) y p (prob. de éxito); q = 1 − p.
- Función de probabilidad: **P(x=r) = nCr · pʳ · qⁿ⁻ʳ**, con nCr = (n sobre r), r ≤ n ("cantidad de subconjuntos de r elementos que se pueden armar a partir de n").
- Esperanza E(x) = n·p; Varianza Var(x) = n·p·q.
- Notación: X ~ Bi(n; p), "se comporta como una Binomial cuyos parámetros son n y p".
- Herramienta usada: app **Probability Distributions** (X~Bin(n,p); campos n, p, x; opciones P(X=x), P(X≤x), P(X≥x)). La app tiene "Moments" para E y Var.

**Poisson** (X ~ P(λ))
- Modela el número de eventos que ocurren aleatoriamente en un continuo (tiempo, longitud, superficie, peso, volumen). Ejemplos de la cátedra: llamadas a un conmutador, bacterias por volumen de fluido, llegadas a caja, descomposturas de una máquina por día, accidentes en un cruce, árboles de una especie por área.
- Condiciones: sucesos en un continuo; independientes entre sí; tasa media de ocurrencia constante en cualquier intervalo del continuo.
- Variable x = número de ocurrencias dentro de la extensión "t" del continuo. Dominio x = {0, 1, 2, 3, …}.
- Parámetro: **λ = b·t** ("cantidad media esperada de sucesos en la extensión t"); b = frecuencia media de ocurrencia por unidad del continuo; t = extensión del continuo.
- **P(x=r) = e^(−λ) · λʳ / r!**; E(x)=λ; Var(x)=λ.

**Ejemplos con resultados de la cátedra**
- TP N°2, ej. 15: P(aprobar Estadística I)=0,7; se eligen 4 alumnos; P(2 aprueben y los otros 2 no) = **0,2646**.
- Ejemplo 8 estudiantes, p(aprobar)=0,7: (a) P(3 no aprueben); (b) P(más de 4 aprueben). Solo se plantean; **las diapositivas no traen el resultado**. (a) equivale a X~Bi(8; 0,7), P(X=5) o Y~Bi(8; 0,3), P(Y=3); (b) P(X≥5).
- Encuesta de mercado, 60% aceptación, n=20 → ver §Ejercicios resueltos (E3).
- Autos por esquina → ver §Ejercicios resueltos (E4).

**Convención de la cátedra**: si piden "no compran", se redefine la variable con p del complemento (X = personas que NO compran ~ Bi(20; 0,4)); "más de 9" se transforma en "≥ 10" (variable discreta).

---

## 3. DISTRIBUCIÓN MUESTRAL DE LA MEDIA

- Estadístico vs parámetro (rec. del PDF de proporción): el estadístico varía de muestra a muestra; el parámetro es fijo.
- Distribución muestral de la media: distribución de probabilidades de todas las medias posibles de muestras de tamaño n de una población.
- Parámetros de x̄ (demostración con x̄ = (x₁+…+xₙ)/n): **μ_x̄ = μ_x**; **σ²_x̄ = σ²/n**, es decir **σ_x̄ = σ/√n** (error estándar).
- Estandarización: **Z = (x̄ − μ) / (σ/√n)**.
- Qué se puede asegurar de x̄:
  - Si x es normal ⇒ x̄ es normal (suma de normales).
  - Si x no es normal ⇒ x̄ normal "a medida que crece el tamaño de muestra (**mayor o igual a 30**)", por TCL.
- Ejemplo de construcción (caja con 3 bolillas {2,3,4}, n=2 con reposición): población μ=3, σ=0,8165 (desvío **poblacional**, n en el denominador). Las 9 medias muestrales: 2; 2,5; 3; 2,5; 3; 3,5; 3; 3,5; 4.

| x̄ | P(x̄) |
|----|------|
| 2 | 1/9 |
| 2,5 | 2/9 |
| 3 | 3/9 |
| 3,5 | 2/9 |
| 4 | 1/9 |

  Resulta μ_x̄ = 3 y σ_x̄ = 0,57735 ("con calculadora"). Relación: 0,8165 / 0,57735 = **√2** = √n.
- Ejemplo numérico → ver E5 (ganancias de empleados).

---

## 4. DISTRIBUCIÓN MUESTRAL DE LA PROPORCIÓN

- Parámetro poblacional **p**: único, fijo. Estimador puntual **p̂**: variable aleatoria (proporción de éxitos en una muestra). Ejemplo ilustrado: población con p=0,4 (juegan tenis); muestras de n=4 dan p̂ = 0,25; 1; 0,5.
- Modelo binomial: X = cantidad de éxitos en n pruebas independientes; E(x)=μ(x)=n·p; σ²(x)=n·p·q = n·p·(1−p).
- p̂ = x/n. Demostración: μ(p̂)=μ(x/n)=(1/n)·n·p = **p**; σ²(p̂)=σ²(x/n)=(1/n²)·n·p·q = p·q/n ⇒ **σ_p̂ = √(p·q/n)** (q = 1−p).
- Aproximación normal: "para n grande, la binomial es aproximadamente normal cuando el número esperado de éxitos y fracasos, **n·p y n·(1−p) (n·q), son ambos al menos 15**" (la diapositiva lo escribe "n·p > 15 y n·q > 15"). Explicación de la cátedra: "garantiza que no haya desequilibrio; más de 15 de cada uno".
- **Z = (p̂ − p) / √(p·q/n)**.
- Frase de la cátedra: "para una muestra aleatoria de tamaño n de una población con proporción p de resultados en una categoría, la distribución de muestreo de la proporción muestral tiene media p y desvío √(p·q/n)".
- **[Nota]** La diapositiva del TCL (§11) dice "binomial ≈ normal a partir de n=30"; la de proporciones exige n·p y n·q ≥ 15. Son criterios distintos en la misma cátedra.
- No hay ejemplo numérico de p̂ resuelto en este PDF.

---

## 5. DISTRIBUCIÓN NORMAL

- Función de densidad = "función de probabilidad de una variable aleatoria continua". Depende de μ y σ. Forma de campana centrada en la media; mayor σ ⇒ más aplastada.
- **IMPORTANTE**: P(x = a) = 0; P(x ≤ a) = P(x < a); P(x ≥ a) = P(x > a).
- Regla empírica 68–95–99,7: 68% a 1σ de la media, 95% a 2σ, 99,7% a 3σ.
- Estandarizar (tipificar): dado σ, μ y x, hallar el z que con μ=0, σ=1 encierra la misma región. Pregunta guía: "¿a cuántos desvíos está x del promedio?" **z = (x − μ)/σ**.
- [Anotación docente] En la diapositiva 7 (manuscrito sobre la imagen): dibuja N con μ=5, σ=3, P(x>11) y debajo la N(0,1) con "P(z > )", "z =" (para completar en clase; z = (11−5)/3 = 2).
- Normal estándar N(0;1). La estandarización "permite la comparación de valores puntuales de dos distribuciones normales diferentes".
- App usada: Probability Distributions con X~N(μ,σ); campo x, y selector de P(X<x), P(X>x), 2P(X>|x|). Para fractil se fija la probabilidad y la app devuelve x.

**Tipos de ejercicios (de la cátedra)**: "entre", "fractil", "parámetro μ o σ desconocido", "dos parámetros desconocidos". Ver E6 a E10.

---

## 6. FÓRMULAS 1°PARCIAL (hoja de fórmulas)

La hoja de fórmulas oficial del primer parcial contiene **solo** estas 7 expresiones (notación textual):
1. P_k = L_I + [ (k·N/100) − F_a ] / f · i  (percentil; *kN/100* = posición, F_a = frecuencia acumulada anterior, f = frecuencia del intervalo, i = amplitud)
2. M_o = L_I + Δ₁/(Δ₁+Δ₂) · i
3. CV = desvío/promedio · 100%
4. P(A/B) = P(A ∩ B) / P(B)
5. P(A ∪ B) = P(A) + P(B) − P(A ∩ B)
6. P(A ∩ B) = P(A) · P(B/A)
7. P(A ∩ B) = P(A) · P(B)   (independientes)

No incluye Bayes, probabilidad total, ni fórmulas de distribuciones. Notación: **la cátedra escribe la condicional con barra: P(A/B)**.

---

## 7. GLOSARIO PROBABILIDADES (traducción de frases a desigualdades; n = 20)

| Frase | Expresión |
|-------|-----------|
| "como máximo 12" | P(x ≤ 12) |
| "como mínimo 12" | P(x ≥ 12) |
| "a lo sumo 12" | P(x ≤ 12) |
| "por lo menos 12" | P(x ≥ 12) |
| "más de la mitad" | P(x > n/2) = P(x > 20/2) = P(x > 10) = P(x ≥ 11) |
| "menos de la mitad" | P(x < 10) = P(x ≤ 9) |
| "más de la tercera parte" | P(x > n/3) = P(x > 20/3) = P(x > 6,67) = P(x ≥ 7) |
| "menos de la tercera parte" | P(x < 6,67) = P(x ≤ 6) |
| "entre 6 y 10" | P(6 ≤ x ≤ 10) = P(x ≤ 10) − P(x ≤ 5) = P(x ≥ 6) − P(x ≥ 11) |
| "entre 13 y 16" | P(13 ≤ x ≤ 16) = P(x ≤ 16) − P(x ≤ 12) = P(x ≥ 13) − P(x ≥ 17) |
| "ninguno" | P(x = 0) |
| "alguno" | P(x ≥ 1) |

Convención: "entre a y b" es **inclusivo** (a ≤ x ≤ b). Para variable discreta con fracciones (6,67) se redondea al entero siguiente hacia el lado correcto (>6,67 ⇒ ≥7; <6,67 ⇒ ≤6).

---

## 8. INTERVALOS DE CONFIANZA PARA LA MEDIA

**Definiciones previas**
- Estadístico: describe una muestra (x̄, s). Parámetro: describe una población (μ, σ).
- Inferencia: (1) estimación de parámetros (puntual: un número; por intervalos: rango que muy probablemente contiene el parámetro); (2) test de hipótesis.
- IC = estimador puntual ± margen de error E. Nivel de confianza (1−α); nivel de riesgo α (α/2 en cada cola).
- Interpretación: "un nivel de confianza de 95% implica que 95% de todas las muestras de tamaño n daría lugar a un intervalo que incluye el parámetro μ, y sólo 5% de las muestras producirá un intervalo erróneo" (gráfico de 7 medias muestrales: ICs 1 a 5 aciertan, 6 y 7 fallan).
- Efecto: mayor confianza ⇒ IC más ancho; mayor n ⇒ IC más angosto.

**σ conocido (Z)**
- Z = (x̄ − μ)/(σ/√n); despejando μ: μ = x̄ − Z·σ/√n.
- se (error estándar) = σ/√n; margen de error **E = Z·σ/√n**.
- **IC(μ) = x̄ ± Z · σ/√n**, con Z = z_{1−α/2}.
- Cómo hallar z (app): se ingresa el valor de z, se elige la opción **2P(X>|x|)** y el resultado es α. (Ejemplo de pantalla: z=2,8868 → α=0,0039.)
- Tamaño de muestra: de E = Z·σ/√n ⇒ **n = (Z·σ/E)²**. "El cálculo dará con decimales; el redondeo de este valor será **SIEMPRE hacia arriba**".

**σ desconocido (t de Student)**
- Se usa s y la distribución t con **ν = n − 1** (gl, v, df). Familia de distribuciones; media 0; forma de campana y simétrica; más dispersa (más plana en el centro, colas más pesadas) que la normal; al aumentar ν tiende a la normal. Supuesto: población normal o casi normal. "El valor de t en un nivel de confianza dado tiene una magnitud mayor que el valor z correspondiente".
- **IC(μ) = x̄ ± t_{(n−1; 1−α/2)} · s/√n**.
- Tamaño de muestra con σ desconocido: **n = ( t_{(n−1;1−α/2)} · s / E )²** ⇒ **MÉTODO ITERATIVO**: "se elige cualquier n para comenzar, debe ser mayor al n que teníamos antes (para disminuir el error)"; se ajusta n (gl) hasta que coincide el valor de entrada y el de salida ("cuando coincide el valor de n finaliza el proceso").

**Convención sobre s**: ver §Convenciones (s con n−1).

Ejemplos resueltos: E11 a E14.

---

## 9. INTERVALOS DE CONFIANZA PARA LA PROPORCIÓN

- Validez: n grande con **n·p > 15 y n·q > 15** (en el IC se verifica con p̂ y q̂). "Tamaño muestral requerido para la validez del IC de la proporción".
- Media μ_p̂ = p; desvío σ_p̂ = √(p·q/n). Como p es desconocido se reemplaza por su estimador p̂: **se = √(p̂·q̂/n)**, con q̂ = 1 − p̂. p̂ ~ Normal (TCL).
- Z = (p̂ − p)/√(p̂·q̂/n); margen de error **E = Z·√(p̂·q̂/n)**.
- **IC(p) = p̂ ± Z · √(p̂·q̂/n)**.
- Tamaño de muestra: de E = Z·√(p̂q̂/n) ⇒ **n = Z²·p̂·q̂ / E²**. "En el cálculo de tamaño de muestra si se tiene información previa sobre la proporción de éxitos, será el valor utilizado; caso contrario la proporción de éxitos se asume en **0,5**".
- Para hallar el nivel de confianza de un IC dado: amplitud = Ls − Li; E = amplitud/2; despejar Z de E; con la app (opción 2P(X>|x|)) obtener α; confianza = 1 − α.
- Siempre se identifica qué es "éxito" según lo que pregunta (ej. "fumadores").
- No hay corrección por población finita en el material (aunque el ejemplo da N=11.000, no se usa).

Ejemplos: E15 y E16.

---

## 10. REGRESIÓN-CORRELACIÓN (resumen de la cátedra)

- **Coeficiente de determinación (bondad de ajuste) r²**, 0 ≤ r² ≤ 1: "mide el porcentaje en que la variable y queda explicada por la recta de regresión ŷ". "Para que un modelo sea aceptable **r² > 0,5**". r²=1 ajuste perfecto (explica 100% de la variabilidad de y respecto de x); r²=0 el modelo no explica nada.
  - r² = (S_xy)²/(S_xx·S_yy) = (Σ(x−x̄)(y−ȳ))² / [Σ(x−x̄)(x−x̄)·Σ(y−ȳ)(y−ȳ)] = (Σx·y − n·x̄·ȳ)² / [(Σx² − n·x̄²)(Σy² − n·ȳ²)].
- **Coeficiente de correlación r**, −1 ≤ r ≤ 1: fuerza y dirección de la relación **lineal** entre dos variables cuantitativas.
  - r = S_xy / √(S_xx·S_yy) = (Σx·y − n·x̄·ȳ) / √[(Σx² − n·x̄²)(Σy² − n·ȳ²)].
  - r > 0 relación directa (positiva); r < 0 inversa (negativa).
  - **Si −0,7 < r < 0,7 relación débil; si r < −0,7 o r > 0,7 relación fuerte** (la cátedra usa 0,7 como corte). Hay imagen de dispersogramas con r = 1, −1, 0, 0,8, 0,4, −0,7.
- **Recta de regresión (de mínimos cuadrados, "recta muestral promedio")**: **ŷ = a + b·x**.
  - Características: (1) Σ(y − ŷ) = Σe = 0 (suma de residuos = 0); (2) Σe² = Σ(y − ŷ)² = mínima; (3) pasa por el punto (x̄; ȳ).
  - **b** = coeficiente de regresión o pendiente: variación esperada de y cuando x aumenta una unidad. **b = S_xy/S_xx = (Σxy − n·x̄·ȳ)/(Σx² − n·x̄²)**; también **b = r · (S_y/S_x)**.
  - **a** = constante de regresión u ordenada al origen: valor promedio de y cuando x=0. **a = ȳ − b·x̄**.
  - El signo de b coincide con el de r.
  - Cuidado con la **extrapolación** (predecir fuera del rango observado de x); el riesgo aumenta al alejarse.
- **[Nota]** En este resumen S_xx, S_xy, S_yy son **sumas de cuadrados/productos de desvíos** (sin dividir por n ni n−1), no varianzas. En b = r·S_y/S_x, S_y y S_x son desvíos (aquí la división por n−1 o n se cancela en el cociente).
- Sin ejemplos resueltos ni anotaciones manuscritas en este PDF.

---

## 11. SUMA DE VARIABLES ALEATORIAS y TEOREMA CENTRAL DEL LÍMITE

**Suma de normales**: variables independientes con distribución normal ⇒ la suma W = x₁ + x₂ + … + xₙ también es normal ("la suma de variables normales origina otra variable normal").

**Propiedades (notación de la cátedra)**
- Promedio: (1) μ(x₁ ± x₂) = μ(x₁) ± μ(x₂); (2) μ(k) = k; (3) μ(k·x₁) = k·μ(x₁); (4) μ(k ± x) = k ± μ(x).
- Varianza: (1) σ²(x₁ ± x₂) = σ²(x₁) ± σ²(x₂) **[como figura en la diapositiva]**; (2) σ²(k) = 0; (3) σ²(k·x₁) = k²·σ²(x₁); (4) σ²(k ± x) = σ²(x).
  - **[Nota]** En todos los ejemplos resueltos la cátedra **suma** las varianzas (σ_w = √(σ²₁ + σ²₂ + …)), aun cuando se restara; la "±" de la propiedad 1 del slide es una imprecisión. Para variables independientes la varianza de una diferencia es la SUMA.

**Teorema Central del Límite (enunciado de la cátedra)**
- Sean x₁,…,xₙ variables aleatorias independientes, no necesariamente normales, con medias μ_xᵢ y desvíos σ_xᵢ; W = a₁x₁ + a₂x₂ + … + aₙxₙ ⇒ W tiende a ser normal con n suficientemente grande, con
  - **μ_W = a₁μ₁ + a₂μ₂ + … + aₙμₙ**
  - **σ_W = √(a₁²σ₁² + a₂²σ₂² + … + aₙ²σₙ²)**.
- En resumen: si las xᵢ son normales ⇒ W ~ N(μ_W; σ_W); si no son normales ⇒ W es aproximadamente normal **si n ≥ 30**.
- Observación: "Un caso concreto del TCL es la distribución binomial. **A partir de n=30**, la binomial se comporta estadísticamente como una normal" (con gráficos Bin(5;0,4), Bin(30;0,4), Bin(50;0,4), Bin(500;0,4)).

**[Anotación docente]** Diapositiva 15 (manuscrita, "Para interpretar"): tres casos para identificar W y su distribución:
1. x = lluvia mensual, x~Normal, μ_x = …, σ_x = … → W = lluvia anual, **W ~ Normal** (suma de 12 normales).
2. x = lluvia diaria, x~Normal → W = lluvia anual, **W ~ Normal**.
3. x = lluvia bimestral, x~Normal → W = lluvia anual, **W ~ Normal**.
(En los tres, la clave señalada en color es que x es normal ⇒ W normal; la cantidad de sumandos cambia: 12, 365, 6.) Ejercicios con datos: E17 a E20.

---

## 12. TEORÍA DE LA PROBABILIDAD

**Conceptos**
- Experimento determinístico (resultado predecible; ej. congelamiento del agua, caída libre) vs aleatorio (no se puede predecir con exactitud aunque se conozcan los resultados posibles; debe haber 2 o más resultados).
- Espacio muestral **E**: conjunto de todos los resultados posibles. Suceso o evento: subconjunto de E; suceso imposible (nunca ocurre) y suceso seguro o cierto (ocurre siempre). Ej. A = número par = {2;4;6}.
- Definiciones de probabilidad:
  - Clásica o de Laplace: **P(A) = n° de casos favorables a A / n° de casos posibles**; solo si todos los resultados son igualmente posibles.
  - Frecuencial: realizar el experimento n veces (n lo más grande posible): **P(A) = n° de éxitos / n° de ensayos = f/n = f_r**.
  - Axiomática o de Kolmogorov: (1) P(A) ≥ 0; (2) **P(E) = 1**; (3) P(A ∪ B) = P(A) + P(B) si A y B son mutuamente excluyentes (A ∩ B = ∅). Consecuencia: 0 ≤ P(A) ≤ 1.
- Operaciones: A ∩ B = {x / x ∈ A ∧ x ∈ B}; A ∪ B = {x / x ∈ A ∨ x ∈ B}; complemento Ā = {x / x ∈ E ∧ x ∉ A}. "Lo que coloquialmente decimos 'y' es una **intersección ∩**, 'o' es una **unión ∪**". Leyes de De Morgan: (A∪B)‾ = Ā ∩ B̄ ; (A∩B)‾ = Ā ∪ B̄.

**Clasificación de sucesos**
- Exhaustivos: su unión es E (A ∪ B = E). Ej. A = número mayor a 1 y B = número impar al lanzar un dado.
- Complementarios: exhaustivos y excluyentes a la vez. **P(Ā) = 1 − P(A)**. Ej. par/impar.
- Mutuamente excluyentes (incompatibles): no pueden ocurrir simultáneamente; A ∩ B = ∅. Ej. carta copa y carta oro.
- No excluyentes (compatibles): pueden ocurrir juntos. Ej. carta 5 y carta oro.
- Independientes: la probabilidad no se modifica por la ocurrencia previa del otro (ej. "con reposición"). Dependientes: se modifica (ej. "sin reposición").

**Reglas**
- Suma: excluyentes P(A∪B)=P(A)+P(B); no excluyentes **P(A∪B)=P(A)+P(B)−P(A∩B)**.
- Producto: independientes **P(A∩B)=P(A)·P(B)**; dependientes **P(A∩B)=P(A)·P(B/A)** ("probabilidad de que ocurra B habiendo ocurrido A"). Como A∩B = B∩A, también P(A∩B)=P(B)·P(A/B).
- Condicional: **P(A/B) = P(A∩B)/P(B)** ("probabilidad de la intersección dividida por la probabilidad de la condición").
- **Independencia**: se prueba con una de tres igualdades: P(A∩B)=P(A)·P(B); P(A)=P(A/B); P(B)=P(B/A).
- Relaciones: independientes ⇒ no mutuamente excluyentes; mutuamente excluyentes ⇒ no independientes; no excluyentes ⇒ pueden ser independientes o no (se prueba). Ejemplo cátedra: A = "gano en el bingo", B = "día soleado": independientes y no excluyentes.
- **Probabilidad total**: A₁,…,Aₙ mutuamente excluyentes y sistema exhaustivo (A₁∪…∪Aₙ=E), P(B) ≠ 0 ⇒ **P(B) = Σ P(Aᵢ)·P(B/Aᵢ)** (se suman todas las ramas del árbol que llegan a B). Incluye demostración (B = (A₁∩B) ∪ … ∪ (Aₙ∩B), disjuntos).
- **Bayes** ("teorema de la probabilidad de las causas"): **P(A_k/B) = P(A_k ∩ B)/P(B) = P(A_k)·P(B/A_k) / Σ P(Aᵢ)·P(B/Aᵢ)**. "P(A_k/B) se denomina **probabilidad a posteriori**".
- Herramientas: **diagrama de árbol** y **tabla de contingencia** (con probabilidades conjuntas dentro de la tabla y marginales en los márgenes).

Ejemplos: E21 a E26.

---

## Convenciones y notación de la cátedra

- **Idioma/símbolos**: probabilidad condicional con barra, **P(A/B)** (no P(A|B)). "y" = ∩, "o" = ∪. Complemento con barra superior Ā. Binomial "X ~ Bi(n; p)" (en las diapositivas de proporción y TCL aparece "Bin(n,p)" de la app); Poisson "X ~ P(λ)"; normal "N(μ; σ)" (con punto y coma). q = 1 − p. Poisson: λ = b·t. Variable aleatoria discreta genérica se llama **r** (también x); dominio con llaves.
- **Desvío**: **σ (n)** cuando se trabaja con la población o con una distribución de probabilidad completa; **s (n−1)** cuando se trabaja con datos de una muestra. Evidencias: (a) PDF "IC media", ej. consultas médicas: 20 datos, x̄=15,25 y **s=7,38**; recalculado, la desviación muestral con n−1 es 7,376 (→7,38), mientras que con n sería 7,189; (b) mismo PDF: "si σ es desconocido deberemos construir los intervalos usando s", t con ν = n−1; (c) PDF "Dist. muestral de la media": caja {2,3,4} población ⇒ σ = 0,8165 es el desvío **poblacional** (con n: 0,8165; con n−1 sería 1); σ_x̄ = 0,57735 es el desvío de las 9 medias tratadas como población completa; (d) la notación usa σ para parámetros y s para estadístico en IC; en regresión S_x, S_y aparecen sin especificar divisor (se cancela en b = r·S_y/S_x). Para datos agrupados/muestras la cátedra implica "sx" de calculadora (n−1); para una población completa o una distribución de probabilidad, "σx" (n). Los PDFs de raw/ no contienen un ejemplo con datos agrupados de desvío.
- **Cuándo Z y cuándo t**: Z con σ poblacional conocido (también para proporciones, siempre Z); t con s y ν = n−1 cuando σ es desconocido (suponiendo población normal o casi). El IC de la proporción siempre usa Z (con p̂, q̂).
- **Notación de valores críticos**: z_{1−α/2}, t_{(n−1; 1−α/2)}. Se obtienen con la **app Probability Distributions** (opción 2P(X>|x|) para ICs): se ingresa x y la app da α, o se fija α. Valores usados: z₀,₉₅=1,96; z₀,₉₀=1,64485 (≈1,645); z(98%)=2,05 (percentil 98; "z=2.05"); z(P>0,10)=1,282; z(P<0,05)=−1,645; t(19; 90%)=1,7291. La cátedra no trabaja con tabla impresa: usa la app, con 5–6 decimales.
- **Redondeos**: tamaño de muestra **SIEMPRE hacia arriba** (150,06→151; 1363,58→1364; iterativo 75,21→76; 74,21→75). Probabilidades con 4–6 decimales (0,056907; 0,983051; 0,28888...). Intervalos con 2–3 decimales; el margen de error se informa como "±". Puntaje de Mensa: x=132,8 se redondea a 133 ("al menos 133").
- **Corrección por población finita**: **no aparece** en ningún PDF (ej. N=11.000 con n=500 se resuelve sin factor).
- **TCL / normalidad**: n ≥ 30 para suma o media de variables no normales; binomial→normal "a partir de n=30" (PDF suma de variables) pero para p̂ se exige **n·p y n·q ≥ 15 (>15)**.
- **Condición de proporción**: ≥15 (no ≥5 ni ≥10).
- **Umbrales**: r: ±0,7 (débil/fuerte); r² > 0,5 = modelo aceptable; CV > 20% = alta variabilidad (PDF discretas).
- **Sin información previa de p**: p = 0,5 para tamaño de muestra.
- **Interpretación de IC**: "con X% de seguridad/confianza podemos afirmar que el parámetro está entre …"; relación con el nivel de riesgo α. Plausibilidad: un valor fuera del IC no es plausible (ej. μ=2 fuera de (2,49; 2,62)).
- **Variables discretas**: "más de 9" ⇒ ≥10; "más de 31" ⇒ ≥32. Para continuas P(X=a)=0.
- **Cómo pide "cuántos más"**: n_requerido − n_actual (864 = 1364 − 500; 55 = 75 − 20).
- **Fractil / "no superada por el 5%"**: se plantea P(W < w₀) = 0,05 y se busca w₀ en la app (72903,5).

---

## Gaps vs knowledge-base existente

Referencias: 01 = `01-probabilidad-basica.md`, 03 = `03-distribuciones-discretas.md`, 04 = `04-normal-muestral-intervalos.md`, 05 = `05-regresion-correlacion.md`, 06 = `06-medidas-posicion-forma.md`.

**Faltantes (no aparecen en 01–06)**
1. **Distribución muestral de la proporción**: μ_p̂ = p, σ_p̂ = √(pq/n), Z = (p̂−p)/√(pq/n), condición n·p y n·q ≥ 15, deducción desde la binomial. No hay ni una mención de p̂ en 04 (la sección "Distribución muestral" cubre solo la media).
2. **Intervalos de confianza para la proporción**: IC = p̂ ± Z√(p̂q̂/n), se = √(p̂q̂/n), E, n = Z²p̂q̂/E², uso de p=0,5 sin información previa, "hallar nivel de confianza" a partir de un IC dado (E = amplitud/2 → z → α → 1−α). Falta en 04 (que solo trata IC para la media).
3. **Ejemplo de IC para la proporción** (universidad, 500 alumnos, 140 fumadores) y del estándar/margen de error (EEUU, 398/1545).
4. **Valores z y fractiles concretos** (1,96; 1,645/1,64485; 2,05; 1,282; −1,645) y ejemplos de fractil/parámetros de la normal (Mensa, estaturas): 04 solo describe los tipos de ejercicio sin números ni ejemplos (ver "Casos típicos de cálculo" en 04).
5. **Ejemplos resueltos del TCL**: venta de golosinas (anual/bimestral), pantalones defectuosos (50 días), cereal (suma de 10 paquetes y caja de 300 g con constante), ganancias de 32 empleados (x̄). 03 trae las propiedades pero no estos ejemplos numéricos.
6. **Ejemplo completo del IC para la media con t y método iterativo** (consultas médicas, 20 citas, iteración 50→76→75): 04 describe el método pero no tiene el cálculo. Tampoco el ejemplo de Bariloche (error, n, y "reducir el confianza → 89%") ni el ejercicio adicional (590 mujeres).
7. **Ejemplo de distribución muestral por enumeración** (caja {2,3,4}, n=2, 9 medias, σ_x̄=0,57735 = σ/√2) no está en 04.
8. **Ejemplo de variable aleatoria discreta con suma de dos bolillas** (E(r)=4, V(r)=1,33, **CV=28,83% > 20% = alta variabilidad**) y la regla "CV>20% ⇒ alta variabilidad": ausentes en 03 y 06 (06 solo menciona CV en una pregunta).
9. **Hoja oficial de fórmulas del 1° parcial** (§6): P_k ya está en 06 (línea ~21), pero **falta la fórmula de la moda con Δ: Mo = L_I + Δ₁/(Δ₁+Δ₂)·i** (06 solo usa Mo para asimetría), y falta registrar que esa hoja es el conjunto oficial de fórmulas (solo 7 expresiones, sin Bayes/total ni distribuciones).
10. **Ejemplos de probabilidad**: mazo de 40 cartas (4 o 7 = 0,2; 3 o copa = 0,325), bolas con/sin reposición (0,1111 / 0,0952), encuesta comedor escolar (hombres/mujeres), encuesta trabajo/título (independencia), jabón en polvo (árbol y tabla; P(R)=0,04295; Bayes 0,4191), dos cajas de monedas (solo enunciado). Revisar contra 01; 01 trae teoría y glosario pero la KB debería contener estos ejemplos numéricos.
11. **Glosario**: "alguno/ninguno/mitad" ya está en 01 (líneas ~163-166); **falta** el caso "más/menos de la tercera parte" (20/3=6,67 ⇒ ≥7 / ≤6) y los dos equivalentes de "entre a y b" (con ≤ o con ≥).

**Contradicciones o matices**
- **Binomial→normal**: 03 (líneas de TCL) dice "n ≥ 30" para la binomial; el PDF de proporción exige **n·p > 15 y n·q > 15**. Hay que dejar ambos criterios y aclarar cuándo aplica cada uno (n≥30 para TCL de sumas/medias; ≥15 para p̂ y IC de proporción).
- **Varianza de ±**: 03 corrige el signo ("siempre +"). El slide original (§11) escribe "σ²(x₁ ± x₂) = σ²(x₁) ± σ²(x₂)"; la KB tiene razón en el fondo, pero conviene avisar que el material oficial trae el error tipográfico por si aparece en un enunciado.
- **Notación de la Binomial**: 03 usa "Bi(n; p)" y el material la escribe "X~Bi(n;p)" en teoría pero "Bin(n,p)" en las capturas de la app: sin conflicto de fondo.
- **Umbral de fuerte (r)**: 05 ya prioriza 0,7 (coincide con el PDF). OK.
- **CV exacto vs slide**: el slide da 28,83%; el cálculo exacto da 28,87%. Si una pregunta de examen usa 28,83% el distractor puede ser 28,87%.
- **IC de 590 mujeres**: slide dice (2,49; 2,62); con el cálculo exacto 2,56 ± 1,96·0,0346 da (2,492; 2,628). La diapositiva trunca el límite superior (debería ser 2,63).
- **IC proporción, ej. 2**: se usa p̂=0,26 y se=0,011 redondeados (E=1,96·0,011=0,02156); sin redondeo da E≈0,0215 y p̂=0,2576.
- **Dato "55 citas más" / "864 más"** reflejan "n requerido − n actual", no el n requerido: puede ser trampa de examen.

**Datos de convención no recogidos en KB**
- Método de obtención de z/t: la cátedra usa la **app Probability Distributions** (2P(X>|x|)); 04 menciona "tabla Z / app" pero no explica el procedimiento para IC (ingresar z → α; o α → z).
- El texto de 04 interpreta que s se usa "cuando se calcula de LA MUESTRA": coherente con la evidencia (s=7,38 con n−1).

---

## Ejercicios resueltos encontrados

Formato: enunciado, datos, planteo, resultado.

**E1. Dado equilibrado (E/V)** (PDF 1)
- Enunciado: distribución, F, G, esperanza y varianza de r = cara superior de un dado; calcular P(r=3), P(r≤4), P(r≥2), P(r<5), P(r>5), P(3≤r≤6).
- Planteo: tabla P/F/G con 1/6.
- Resultado: 1/6; 4/6; 5/6; 4/6; 1/6; F(6)−F(2)=5/6. E(r)=3,5; V(r)=2,917.

**E2. Caja con 3 bolillas, 2 extracciones con reposición, suma** (PDF 1)
- Enunciado: construir distribución de la suma, funciones de distribución, E(r), V(r).
- Datos: bolillas {1,2,3}; 9 casos equiprobables.
- Resultado: dominio {2,3,4,5,6}; P=(1/9, 2/9, 3/9, 2/9, 1/9); F=(1/9, 3/9, 6/9, 8/9, 1); G=(1, 8/9, 6/9, 3/9, 1/9); E=4; V=1,33; CV=28,83% (>20% alta variabilidad).

**E3. Encuesta de mercado (Binomial)** (PDF 2)
- Enunciado: aceptación 60%; muestra 20 personas. (a) exactamente 10 compren; (b) a lo sumo 12 compren; (c) más de 9 NO compren; (d) cuántas se espera que no compren.
- Planteo: (a) X~Bi(20; 0,6), P(X=10); (b) P(X≤12); (c) Y = no compran ~ Bi(20; 0,4), P(Y>9)=P(Y≥10); (d) E = n·p = 20·0,4.
- Resultado: (a) 0,11714; (b) 0,58411; (c) 0,24466; (d) 8 personas.

**E4. Autos por esquina (Poisson)** (PDF 2)
- Enunciado: en promedio 15 autos/min. P(exactamente 11 en 1 min); P(más de 31 en 3 min); P(7 en 30 s).
- Planteo: (a) λ=15·1=15; (b) λ=15·3=45, P(x>31)=P(x≥32); (c) λ=15·0,5=7,5.
- Resultado: (a) 0,06629; (b) 0,982218; (c) 0,14648.

**E5. Ganancias de empleados (x̄, TCL)** (PDF 3)
- Enunciado: ganancias anuales con distribución asimétrica negativa, μ=15000, σ=2000, muestra n=32. P(x̄ < 15750).
- Planteo: por TCL x̄ ~ N(μ=15000; σ_x̄=2000/√32=353,56).
- Resultado: P(x̄<15750)=0,983051.

**E6. Comparar candidatos a beca (estandarización)** (PDF 5)
- Datos: A=8 en N(6;1); B=180 en N(160;15).
- Planteo: z_A=(8−6)/1=2; z_B=(180−160)/15=1,33.
- Resultado: A mejor candidato (z mayor).

**E7. Estaturas de varones argentinos, "entre"** (PDF 5)
- Datos: X~N(1,73; 0,08). P(1,65<X<1,80)?
- Planteo: P(X<1,8)−P(X<1,65).
- Resultado: 0,80921 − 0,15866 = 0,65055.

**E8. Mensa (fractil)** (PDF 5)
- Datos: puntaje IQ ~ N(100; 16); admite desde el percentil 98.
- Planteo: z=2,05 para acumulada 0,98; x = 100 + 2,05·16.
- Resultado: x=132,8 ⇒ puntaje de al menos 133.

**E9. Fractil: 10% de los varones más altos** (PDF 5)
- Datos: X~N(1,73; 0,08), P(X>x₁)=0,10.
- Resultado: x₁ = 1,83 m (con la app).

**E10. Parámetros desconocidos** (PDF 5)
- (a) Niños de 5 años, μ=1,10; 10% más altos superan 1,29: P(Z>Z₁)=0,10 ⇒ Z₁=1,282; σ=(1,29−1,10)/1,282 = **0,148 m**.
- (b) 10% superan 1,29 y 5% no superan 0,86: Z₁=1,282, Z₂=−1,645; sistema μ=0,86+1,645σ; μ=1,29−1,282σ ⇒ **σ=0,147 m; μ=1,10 m**.

**E11. IC media, σ conocido (Bariloche)** (PDF 8)
- Datos: n=100, x̄=$3400, σ=$1250.
- (a) IC 95%: 3400 ± 1,96·1250/√100 = 3400 ± 245 = (3155; 3645). "Con 95% de seguridad el ingreso promedio está entre $3155 y $3645".
- (b) Error de muestreo: 245 pesos.
- (c) Reducir el error a 200: (i) aumentar n: 200=1,96·1250/√n ⇒ n=(1,96·1250/200)²=(12,25)²=150,06 ⇒ **151 personas**; (ii) disminuir confianza: z=200·10/1250=1,6; 2P(z>1,6)=0,109599=α; 1−α=0,8904 ⇒ **≈89%**.

**E12. IC media, σ desconocido (consultas médicas)** (PDF 8)
- Datos: n=20 duraciones: 15 5 18 32 28 10 14 19 25 7 12 8 16 12 9 13 20 5 17 20.
- (a) x̄=15,25; s=7,38. (b) IC 90%: t(19; 0,95)=1,7291 ⇒ 15,25 ± 1,7291·7,38/√20 = 15,25 ± 2,8534 = (12,39; 18,10).
- (c) Reducir el error a la mitad: E_nuevo=2,8534/2=1,4267; n=(t·7,38/1,4267)²; n=50 (t=1,67655)⇒75,21→76; n=76 (t=1,6654)⇒74,21→75; n=75 (t=1,6657)⇒74,24→75 (coincide, fin). Respuesta: 75−20 = **55 citas más**.

**E13. Ideal de hijos (EE.UU., 2012)** (PDF 8)
- Datos: n=590, mediana 2, media 2,56, s=0,84.
- (a) estimador puntual 2,56; (b) se=0,84/√590=0,035; (c) IC 95%: (2,49; 2,62) [exacto 2,49–2,63]; (d) μ=2 no es plausible porque cae fuera del IC.

**E14. Interpretación de nivel de confianza** (PDF 8): gráfico con 7 medias y sus ICs; 95% de las muestras dan IC que contiene a μ; 5% no.

**E15. Tabaquismo en universidad privada (proporción)** (PDF 9)
- Datos: N=11.000, n=500, 140 fumadores (360 no).
- (a) Variable: condición del alumno (fumador/no fumador); población: 11.000 alumnos; muestra: 500.
- (b) IC 90%: p̂=0,28; q̂=0,72; 0,28 ± 1,64485·√(0,28·0,72/500) = 0,28 ± 0,033 = (0,247; 0,313) ⇒ entre 24,7% y 31,3%.
- (c) E=0,02, 90%: n=1,64485²·0,28·0,72/0,02² = 1363,58 ⇒ 1364; "cuántos más" = 1364 − 500 = **864**.
- (d) Otro investigador: IC (26%; 30%): amplitud 0,04; E=0,02; 0,02 = Z·√(0,28·0,72/500) ⇒ Z=0,9960; α=0,31926 (app, 2P); 1−α=0,68074 ⇒ **68,07%**.

**E16. Cuestionario de Percepción Social 2018 (EE.UU.)** (PDF 9)
- Datos: 398 de 1545 de acuerdo; p̂=398/1545=0,26.
- (a) se=√(0,26·0,74/1545)=0,011 (cuánto se espera que p̂ varíe de muestra en muestra).
- (b) E 95% = 1,96·0,011 = 0,02156 ⇒ ±0,022 (±2,2 puntos porcentuales alrededor de 26%).

**E17. Cereal: peso de 10 paquetes en packaging de peso despreciable** (PDF 11)
- Datos: x~N(250; 20); W=x₁+…+x₁₀.
- μ_W=10·250=2500 g; σ_W=√(10·20²)=63,24 g.
- P(W>2600) = **0,056907**.

**E18. Cereal: caja de cartón de 300 g** (PDF 11)
- W=x₁+…+x₁₀+300. μ_W=10·250+300=**2800 g**; σ_W=√(10·20²+0)=**63,24 g** (la constante no suma varianza).

**E19. Venta de golosinas (TCL)** (PDF 11)
- Datos: venta diaria con distribución desconocida, μ=1300, σ=400.
- (a) W = venta anual = x₁+…+x₃₆₅: μ_W=365·1300=474500; σ_W=√(365·400²)=7642; P(W<460000)=**0,028887**.
- (b) W = venta bimestral (60 días): μ=60·1300=78000; σ=√(60·400²)=3098,4; P(W<w₀)=0,05 ⇒ **w₀ = 72903,5 $**.

**E20. Pantalones defectuosos (TCL)** (PDF 11)
- Datos: diaria asimétrica, μ=5, σ=2; 50 días.
- W~N(μ=5·50=250; σ²=2²·50=200 ⇒ σ=14,14). P(230≤W≤240) = P(W≤240) − P(W≤230) = 0,23972 − 0,078618 = **0,161102**.

**E21. Cartas (mazo de 40)** (PDF 12)
- (a) P(4 o 7)=P(4)+P(7)=4/40+4/40=1/5=**0,2** (excluyentes).
- (b) P(3 o copa)=P(3)+P(copa)−P(3 y copa)=4/40+10/40−1/40=13/40=**0,325**.

**E22. Pelotas (10 blancas, 5 negras), dos extracciones sucesivas** (PDF 12)
- (a) Con reemplazo: P(N₁∩N₂)=5/15·5/15=1/9=**0,1111**.
- (b) Sin reemplazo: P(N₁∩N₂)=P(N₁)·P(N₂/N₁)=5/15·4/14=2/21=**0,0952**.

**E23. Encuesta comedor escolar (condicional)** (PDF 12)
- Tabla: Hombres 60 a favor / 20 en contra / 80; Mujeres 40 / 30 / 70; Total 100 / 50 / 150.
- A) P(no a favor / mujer) = 30/70 ≈ 0,4286. B) P(hombre / a favor) = 60/100 = 0,60. (El slide plantea las preguntas; los resultados se deducen directamente de la tabla.)

**E24. Independencia trabajo/título universitario** (PDF 12)
- Tabla: T sí: U sí 75, U no 175, total 250; T no: 225, 525, 750; totales 300, 700, 1000.
- Planteo: P(T∩U)=75/1000=0,075; P(T)·P(U)=0,25·0,30=0,075 ⇒ **independientes** (también P(T/U)=75/300=0,25=P(T)). (Slide plantea el ejercicio; resultado deducido.)

**E25. Jabón en polvo (probabilidad total y Bayes)** (PDF 12)
- Datos: proveedores A 45%, B 32%, C 23% (resto); bolsas rotas: 4% (A), 6% (B), 2,5% (C).
- P(R) = 0,45·0,04 + 0,32·0,06 + 0,23·0,025 = 0,018 + 0,0192 + 0,00575 = **0,04295** (árbol y tabla de contingencia; la tabla da R̄ = 0,432; 0,3008; 0,22425; total 0,95705).
- Bayes: P(A/R) = P(A∩R)/P(R) = 0,018/0,04295 = **0,4191**.

**E26. Dos cajas de monedas (solo enunciado)** (PDF 12)
- Caja 1: 10 monedas de 10¢ y 5 de 50¢; caja 2: 15 de 10¢ y 12 de 25¢; se elige una caja y una moneda al azar. (a) P(10¢) ; (b) P(caja 1 / 10¢). El slide no trae resolución. Planteo (si las cajas son equiprobables): P(10¢)=½·10/15+½·15/27 = 0,6111; P(caja1/10¢)=(½·10/15)/0,6111 ≈ 0,5455. (Cálculo propio, no figura en el PDF.)

**E27. Ejemplo con Poisson/Binomial para práctica (sin resultado)**: 8 estudiantes, p=0,7: P(3 no aprueben); P(más de 4 aprueben) (sin solución en el slide).

---

## Respuesta puntual: ¿S con n−1 o σ con n?

Para datos de **muestra** (incluyendo los ejemplos de IC) la cátedra usa **s con n−1** (en la "calculadora" sx): PDF "Intervalos de confianza PARA LA MEDIA", ejemplo de 20 consultas: x̄=15,25, s=7,38 (comprobado: la desviación muestral n−1 de esos 20 datos da 7,376; con n daría 7,189), con t y ν=n−1. Para una **población completa o una distribución de probabilidad** usa **σ con n**: PDF "DISTRIBUCIÓN MUESTRAL DE LA MEDIA", caja {2,3,4}: σ=0,8165 (con n; con n−1 sería 1) y σ_x̄=0,57735 (las 9 medias como población); PDF discretas: V(r)=Σ(r−E)²P(r). El PDF de regresión usa S_xx, S_xy como sumas de desvíos (sin divisor). No hay en `raw/` un ejemplo con datos agrupados; para eso la regla de la cátedra (por su vínculo con el IC) sería S (n−1) si son datos de muestra.
