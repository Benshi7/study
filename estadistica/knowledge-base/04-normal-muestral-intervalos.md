# Distribución Normal, Distribución Muestral e Intervalos de Confianza

## Distribución normal

**Función de densidad**: f(x) = (1/(σ√(2π))) · e^(−½·((x−μ)/σ)²), X ~ N(μ, σ)

**Propiedades**:
- Acampanada (campana de Gauss), simétrica, unimodal
- Me = Mo = μ
- Dos puntos de inflexión en x = μ ± σ
- Depende de dos parámetros: μ (posición) y σ (dispersión/forma)
- P(x=a) = 0 siempre (variable continua) → P(x≤a) = P(x<a) y P(x≥a) = P(x>a)
- Área bajo la curva = probabilidad; área total = 1

**Regla empírica (68-95-99,7)**:
- μ ± 1σ → 68% de los valores
- μ ± 2σ → 95% de los valores
- μ ± 3σ → 99,7% de los valores

**Estandarización (Z)**:
- Fórmula: Z = (x − μ) / σ
- Mide a cuántos desvíos estándar está x de la media
- Distribución normal estándar: N(0,1), con μ=0 y σ=1
- Permite comparar valores de distribuciones normales distintas (distinta μ y σ) llevándolas a la misma escala

**Casos típicos de cálculo con tabla Z / app**:
1. **Probabilidad simple**: P(X>a), P(X<a) → estandarizar y buscar en tabla Z
2. **Probabilidad "entre"**: P(a<X<b) = P(X<b) − P(X<a)
3. **Fractil** (dado un percentil, hallar el valor x): despejar de z = (x−μ)/σ → x = μ + z·σ
4. **Hallar un parámetro desconocido (μ o σ)**: se plantea la ecuación con el z correspondiente al percentil dado y se despeja
5. **Dos parámetros desconocidos**: se necesitan dos ecuaciones (dos percentiles dados) y se resuelve el sistema

## Teorema central del límite y distribución muestral de la media

**Distribución muestral de la media**: es la distribución de probabilidades de todos los posibles promedios (x̄) de las muestras de tamaño n extraídas de una población.

**Parámetros de x̄** (demostrables a partir de x̄ = (1/n)(x₁+...+xₙ)):
- μ_x̄ = μ (la media de las medias muestrales es igual a la media poblacional)
- σ_x̄ = σ/√n (error estándar de la media)

**Enunciado del TCL y condiciones**:
- Si la variable x original **es Normal** → x̄ es Normal exactamente, para cualquier n (porque es combinación lineal/suma de normales).
- Si la variable x original **NO es Normal** → x̄ tiende a Normal a medida que n crece; regla práctica: **n ≥ 30**.

**Estadístico Z para la media muestral**:
Z = (x̄ − μ) / (σ/√n)

## Intervalos de confianza para la media

**Definiciones previas**:
- Estadístico: describe una muestra (ej. x̄, s)
- Parámetro: describe una población (ej. μ, σ)
- Estimación puntual: un único número (mejor suposición del parámetro)
- Estimación por intervalos: rango numérico que probablemente contenga el parámetro

**Estructura general**: IC(μ) = x̄ ± E, donde E es el margen de error.

### Caso 1: desvío poblacional σ CONOCIDO → se usa Z, distribución normal
IC(μ) = x̄ ± Z · (σ/√n)

### Caso 2: desvío poblacional σ DESCONOCIDO → se usa t de Student
IC(μ) = x̄ ± t · (s/√n)
- Grados de libertad: ν = n − 1
- t se busca con ν y con el nivel de confianza (1−α)

**Cómo se elige el valor crítico (Z o t)**:
- Depende del nivel de confianza (1−α), que es un dato fijado de antemano (ej. 95%, 90%)
- α = nivel de riesgo; se reparte en las dos colas: α/2 en cada extremo
- Con Z: se busca z tal que 2·P(Z>|z|) = α
- Con t: además del nivel de confianza, se necesita ν = n−1

**Distribución t de Student — propiedades**:
- Familia de distribuciones (una para cada ν), no una sola distribución
- Continua, simétrica, en forma de campana, con media 0
- Más dispersa/achatada que la Z (colas más pesadas)
- A medida que ν aumenta (muestra más grande), t → Z (se parecen cada vez más)
- Para el mismo nivel de confianza, |t| > |z| siempre (el valor crítico t es más exigente/mayor)

**Interpretación correcta de "confianza" (trampa clásica)**:
- El nivel de confianza (1−α) es la probabilidad de que el **método** (el proceso de construir el intervalo) produzca un intervalo que contenga al parámetro — evaluado sobre la repetición del muestreo.
- **NO es la probabilidad de que el parámetro esté dentro de ESE intervalo particular ya calculado**. Una vez que el intervalo numérico está calculado, μ está o no está dentro — no hay azar de por medio (μ es una constante, no una variable aleatoria).
- Interpretación correcta: "con un 95% de confianza, el intervalo [a,b] contiene a μ" significa que si repitiéramos el muestreo muchas veces, el 95% de los intervalos construidos con este método contendrían al verdadero μ (y el 5% restante no).

**Tamaño de muestra necesario (despejando n del margen de error)**:
- Con σ conocido: n = (Z·σ/E)²
- Con σ desconocido: n = (t·s/E)² → requiere **método iterativo** porque t depende de ν = n−1, que es justamente la incógnita. Se propone un n inicial, se calcula el nuevo n, y se repite hasta que el n de entrada coincide con el n de salida (redondeado hacia arriba).
- El redondeo del tamaño de muestra **siempre es hacia arriba** (entero superior), nunca al más cercano.

**Efecto del tamaño muestral y del nivel de confianza sobre el error E**:
- Mayor nivel de confianza → E más grande (intervalo más ancho)
- Mayor tamaño de muestra n → E más chico (intervalo más angosto)
- Para reducir el error hay dos vías: aumentar n, o disminuir el nivel de confianza.

## Tabla de decisión rápida

| Situación | Qué usar |
|---|---|
| σ (desvío poblacional) conocido | Z |
| σ desconocido, se usa s (desvío muestral) | t de Student, con ν = n−1 |
| Variable original x ya es Normal | Trabajar directo con distribución normal de x (cualquier n) |
| Variable original x NO es Normal, n ≥ 30 | Usar distribución muestral de x̄ (aprox. Normal por TCL) |
| Variable original x NO es Normal, n < 30 | TCL no garantiza normalidad de x̄ (no se puede aplicar sin más supuestos) |
| Pregunta sobre un valor individual (x) | Z = (x−μ)/σ |
| Pregunta sobre un promedio de muestra (x̄) | Z = (x̄−μ)/(σ/√n) |
| Calcular tamaño de muestra con σ conocido | Fórmula directa n=(Zσ/E)² |
| Calcular tamaño de muestra con σ desconocido | Método iterativo (t depende de n) |

## Trampas de examen multiple choice

1. **Interpretar el IC como probabilidad del parámetro**: decir "hay 95% de probabilidad de que μ esté en este intervalo" es incorrecto una vez que el intervalo ya fue calculado con datos concretos. La probabilidad (1−α) es del **método**, no del intervalo particular ya obtenido.
2. **Confundir σ (desvío poblacional) con σ_x̄ (error estándar)**: σ_x̄ = σ/√n es SIEMPRE menor o igual a σ. Usar σ directamente en la fórmula de Z de la media (en lugar de σ/√n) es un error frecuente.
3. **Usar Z cuando corresponde t**: si el enunciado dice "se desconoce el desvío poblacional" o da un desvío calculado a partir de LA MUESTRA (s), corresponde t, no Z — aunque n sea grande. (Con n grande, t≈Z, pero conceptualmente sigue siendo t.)
4. **Olvidar los grados de libertad correctos**: ν = n−1, no n.
5. **Redondear el tamaño de muestra al entero más cercano** en vez de siempre hacia arriba (si sale n=150,06, la respuesta correcta es 151, no 150).
6. **No recalcular el error nuevo al pedir "reducir el error a la mitad" o similar**: hay que recalcular E y luego resolver n o el nivel de confianza correspondiente, no reusar el n original.
7. **Confundir el z/t de "una cola" con el de "dos colas"**: para IC se reparte α/2 en cada cola (valor 1−α/2), no se usa α completo de un solo lado.
8. **Aplicar TCL con n<30 sin que la población sea Normal**: la distribución muestral de x̄ no está garantizada como Normal en ese caso.
9. **Confundir "el promedio se distribuye Normal" con "los datos individuales se distribuyen Normal"**: aunque la variable original tenga una distribución asimétrica, x̄ puede ser aproximadamente Normal (por TCL) sin que eso implique que los datos individuales lo sean.

## Preguntas de autoevaluación

**1.** Una variable X se distribuye N(50, 8). ¿Cuál es la probabilidad de que un valor individual sea mayor a 50?
a) 0
b) 0,25
c) 0,50 ✅
d) 1
*Justificación: la distribución es simétrica respecto de μ, por lo que P(X>μ) = 0,5.*

**2.** Al estandarizar un valor x de una N(μ,σ), la variable Z resultante:
a) Tiene media μ y desvío σ
b) Tiene media 0 y desvío 1 ✅
c) Depende de tabla t
d) Solo aplica si σ es desconocido
*Justificación: la estandarización siempre lleva a N(0,1), independientemente de los parámetros originales.*

**3.** Si x̄ es el promedio de una muestra de tamaño n=36 tomada de una población NO normal con σ=12, la distribución muestral de x̄:
a) No puede determinarse nunca
b) Es exactamente Normal solo si σ es conocido
c) Es aproximadamente Normal porque n≥30 (TCL) ✅
d) Es Normal solo si la población también lo es
*Justificación: con n≥30 el TCL garantiza normalidad aproximada de x̄ aun si la población original no es Normal.*

**4.** El error estándar de la media (σ_x̄) se calcula como:
a) σ
b) σ/n
c) σ/√n ✅
d) σ²/n
*Justificación: σ_x̄ = σ/√n, se deriva de las propiedades de la varianza de una suma de variables independientes dividida por n.*

**5.** Un IC para μ tiene σ desconocido y n=15. El valor crítico correspondiente debe obtenerse de:
a) La distribución Z, con α completo
b) La distribución t, con ν=14 ✅
c) La distribución t, con ν=15
d) La distribución Z, con ν=14
*Justificación: σ desconocido implica usar t de Student, con grados de libertad ν=n−1=14.*

**6.** "El intervalo de confianza del 95% para μ es (10; 14)". La interpretación correcta es:
a) Hay 95% de probabilidad de que μ esté entre 10 y 14
b) El 95% de los datos de la muestra están entre 10 y 14
c) Si repitiéramos el muestreo muchas veces, el 95% de los intervalos construidos así contendrían a μ ✅
d) μ vale con certeza 12 (punto medio del intervalo)
*Justificación: la confianza del 95% es una propiedad del procedimiento de muestreo repetido, no una probabilidad sobre el intervalo particular ya calculado.*

**7.** Al aumentar el nivel de confianza de 90% a 99%, manteniendo n constante, el intervalo de confianza:
a) Se vuelve más angosto
b) Se vuelve más ancho ✅
c) No cambia
d) Se vuelve más angosto solo si σ es conocido
*Justificación: mayor confianza requiere un valor crítico (Z o t) mayor, lo que aumenta el margen de error E y ensancha el intervalo.*

**8.** Al calcular el tamaño de muestra necesario con σ desconocido, se necesita un método iterativo porque:
a) La fórmula no tiene solución analítica
b) t depende de ν=n−1, que es la incógnita que se busca ✅
c) s siempre es indeterminado
d) El nivel de confianza cambia en cada iteración
*Justificación: como t varía según los grados de libertad (que dependen de n), hay que iterar hasta que el n propuesto y el n resultante coincidan.*

**9.** Si el cálculo de tamaño de muestra da n=88,3, la muestra a tomar debe ser:
a) 88
b) 89 ✅
c) 88,3 (sin redondear)
d) 90 (redondeado a la decena)
*Justificación: el tamaño de muestra siempre se redondea hacia el entero superior, nunca al más cercano ni hacia abajo.*

**10.** Si aumenta el tamaño de muestra n (manteniendo el mismo nivel de confianza), el margen de error E:
a) Aumenta
b) Disminuye ✅
c) No cambia
d) Depende únicamente de σ
*Justificación: E = Z·σ/√n (o t·s/√n); al crecer n, el denominador crece y E disminuye.*
