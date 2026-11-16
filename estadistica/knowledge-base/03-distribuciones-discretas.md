# Distribuciones Discretas de Probabilidad

## Resumen por distribución

### Variable aleatoria discreta (general)
- **Condición**: entre dos valores cualesquiera del dominio hay a lo sumo un número finito de valores posibles (variable de conteo).
- **Función de probabilidad** P(r): cumple P(r) ≥ 0 para todo r, y ΣP(r) = 1.
- **Función de distribución acumulada**:
  - Por izquierda: F(r₀) = P(r ≤ r₀) = Σ P(r), ∀ r ≤ r₀
  - Por derecha: G(r₀) = P(r ≥ r₀) = Σ P(r), ∀ r ≥ r₀
- **Esperanza**: μ = E(r) = Σ rᵢ·P(rᵢ)
- **Varianza**: σ² = V(r) = Σ (rᵢ − E(r))²·P(rᵢ)
- **Desvío estándar**: D.S.(r) = √Var(r)
- **Ejemplo mínimo**: dado equilibrado, r = número en la cara superior, r={1,...,6}, P(r)=1/6 c/u → E(r)=3,5, V(r)=2,917.

### Distribución Binomial
- **Condiciones de uso**: experimento dicotómico (éxito/fracaso), n repeticiones idénticas e independientes, p constante en todas las pruebas.
- **Parámetros**: n (cantidad de pruebas), p (prob. de éxito), q = 1 − p.
- **Variable**: X = número de éxitos en n pruebas. Dominio x = {0, 1, 2, ..., n}.
- **Función de probabilidad**: P(x=r) = nCr · pʳ · q^(n−r), con nCr = C(n,r).
- **Esperanza**: E(x) = n·p
- **Varianza**: Var(x) = n·p·q
- **Notación**: X ~ Bi(n; p)
- **Ejemplo mínimo**: probabilidad de aprobar Estadística I es 0,7. En 4 alumnos, P(exactamente 2 aprueben) = 0,2646 → Binomial(n=4, p=0,7).

### Distribución de Poisson
- **Condiciones de uso**: eventos que ocurren en un continuo (tiempo, longitud, superficie, volumen, etc.); sucesos independientes entre sí; tasa promedio de ocurrencia constante en cualquier intervalo del continuo.
- **Parámetro**: λ = b·t (cantidad media esperada de sucesos en la extensión t del continuo)
  - b: frecuencia media de ocurrencia por unidad del continuo
  - t: extensión del continuo considerada
- **Variable**: x = número de ocurrencias en la extensión t. Dominio x = {0, 1, 2, 3, ...}.
- **Función de probabilidad**: P(x=r) = e^(−λ)·λʳ / r!
- **Esperanza**: E(x) = λ
- **Varianza**: Var(x) = λ
- **Notación**: X ~ P(λ)
- **Ejemplo mínimo**: transitan 15 autos/min por una esquina. En 1 minuto (λ=15), P(x=11)=0,06629. En 3 minutos (λ=15·3=45), P(x>31)=0,982218. En 30 segundos (λ=15·0,5=7,5), P(x=7)=0,14648.
- **Trampa clave del parámetro**: λ SIEMPRE debe recalcularse según la unidad de tiempo/espacio pedida en la pregunta, no la unidad en que viene dado el promedio (b).

## Suma de variables aleatorias

### Propiedades del promedio (esperanza)
1. μ(x₁ ± x₂) = μ(x₁) ± μ(x₂)
2. μ(k) = k (constante)
3. μ(k·x₁) = k·μ(x₁)
4. μ(k ± x) = k ± μ(x)

### Propiedades de la varianza
1. σ²(x₁ ± x₂) = σ²(x₁) + σ²(x₂) — **el signo siempre es +**, aun si la variable se resta (trampa clásica)
2. σ²(k) = 0 (una constante no tiene varianza)
3. σ²(k·x₁) = k²·σ²(x₁)
4. σ²(k ± x) = σ²(x) — sumar/restar una constante no cambia la dispersión

### Combinación lineal general (base del Teorema Central del Límite)
Sea W = a₁·x₁ + a₂·x₂ + ... + aₙ·xₙ, con x₁,...,xₙ variables aleatorias independientes:
- μ_W = a₁·μ_x1 + a₂·μ_x2 + ... + aₙ·μ_xn
- σ_W = √(a₁²·σ²_x1 + a₂²·σ²_x2 + ... + aₙ²·σ²_xn)

### Teorema Central del Límite (TCL)
- Si x₁,...,xₙ son **Normales** → W ~ N(μ_W; σ_W) exactamente, sin importar n.
- Si x₁,...,xₙ **no son Normales** → W es **aproximadamente** Normal si n ≥ 30 (regla práctica del TCL).
- Caso particular: la distribución **Binomial se aproxima a Normal cuando n ≥ 30** (es un caso concreto del TCL, ya que Binomial = suma de n variables Bernoulli independientes).

### Suma de binomiales/Poisson que da otra distribución conocida
No aparece explícitamente en los PDFs una propiedad de "suma de binomiales = binomial" o "suma de Poisson = Poisson" con parámetros sumados; el material solo trabaja combinaciones lineales generales vía TCL. Si el examen la pregunta, la propiedad reproductiva estándar es: suma de n binomiales independientes con el mismo p da Binomial(Σnᵢ, p); suma de Poisson independientes da Poisson(Σλᵢ) — pero **verificar si el docente la tomó**, porque no está en el material provisto.

## Tabla comparativa

| Aspecto | Binomial | Poisson |
|---|---|---|
| Tipo de experimento | Dicotómico (éxito/fracaso), n pruebas fijas | Conteo de eventos en un continuo (tiempo, espacio, volumen) |
| Parámetros | n, p (2 parámetros) | λ = b·t (1 parámetro) |
| Dominio | x = {0, 1, ..., n} (acotado por n) | x = {0, 1, 2, ...} (no acotado) |
| Esperanza | n·p | λ |
| Varianza | n·p·q (siempre ≤ E(x), porque q<1) | λ (varianza = esperanza, propiedad distintiva) |
| Cuándo usar | Se conoce n (repeticiones) y p (prob. de éxito constante) | Se conoce una tasa promedio de ocurrencia (b) y una extensión (t); NO hay "n" de repeticiones fijas |
| Aproximación | Binomial → Normal si n ≥ 30 (vía TCL) | (no mencionada aproximación Poisson↔Binomial en el material) |

## Trampas de examen multiple choice

1. **Confundir cuándo usar Binomial vs Poisson**: si el problema da una tasa promedio por unidad de tiempo/espacio (ej. "15 autos por minuto", "3 llamadas por hora") sin un número fijo de "pruebas", es **Poisson**, no Binomial. Si hay un n de intentos y una p de éxito, es Binomial.
2. **No recalcular λ**: al cambiar la extensión del continuo (t) hay que recalcular λ = b·t. Usar el λ original dado en otra unidad de tiempo es el error más común (ej.: dan 15 autos/min y preguntan por 3 minutos → λ=45, no 15).
3. **Confundir varianza con desvío estándar**: Var(x) = n·p·q (Binomial) o λ (Poisson) NO es lo mismo que el desvío σ = √Var(x). Las opciones múltiple choice suelen poner el valor de varianza donde se pide desvío (o viceversa).
4. **Signo en σ²(x₁ ± x₂)**: aunque la variable sea una resta, la varianza de la suma/resta de independientes **siempre se suma** (nunca se resta). Este es el error de signo más común en la propiedad de varianzas.
5. **σ²(k) ≠ k**: una constante tiene varianza CERO, no la constante misma. Confundir μ(k)=k con σ²(k)=k es común.
6. **Mal identificar n y p en Binomial**: revisar bien qué es "éxito" en el enunciado — si preguntan por los que NO compran/NO aprueban, p cambia (p' = 1−p original) y hay que reconstruir la distribución con el nuevo p, no reusar el mismo p.
7. **Aplicar TCL con n < 30 sin verificar Normalidad previa**: si la variable original NO es Normal y n < 30, W no es aproximadamente Normal — no se puede aplicar TCL sin más justificación.
8. **P(x > k) vs P(x ≥ k)**: por ser variable discreta, P(X > k) = P(X ≥ k+1), no P(X ≥ k). Confundir estas desigualdades estrictas/no estrictas es un error típico de opción múltiple.
9. **Dominio acotado**: en Binomial, x no puede superar n (dominio finito); en Poisson, x no tiene cota superior (dominio infinito). Una opción con x > n en un problema Binomial es automáticamente incorrecta/imposible.

## Preguntas de autoevaluación

**1)** Un kiosco vende en promedio 8 golosinas por hora (proceso continuo, sin n de pruebas fijo). ¿Qué distribución modela mejor "cantidad de golosinas vendidas en 2 horas"?
a) Binomial(n=2, p=8)
b) Binomial(n=8, p=2)
c) **Poisson(λ=16)** ✓
d) Poisson(λ=8)

*Justificación*: no hay n de repeticiones ni p de éxito constante — es una tasa de ocurrencia en un continuo (tiempo). λ = b·t = 8·2 = 16.

**2)** En una distribución Binomial(n=20, p=0,4), ¿cuál es el desvío estándar de X?
a) Var(x) = 4,8
b) **σ(x) = √4,8 ≈ 2,19** ✓
c) σ(x) = n·p = 8
d) σ(x) = n·p·q = 4,8

*Justificación*: Var(x)=n·p·q=20·0,4·0,6=4,8; el desvío es la raíz de la varianza, no la varianza misma.

**3)** Si σ²(x₁)=9 y σ²(x₂)=16, siendo x₁ y x₂ independientes, ¿cuánto vale σ²(x₁ − x₂)?
a) 7
b) **25** ✓
c) -7
d) √25

*Justificación*: σ²(x₁ ± x₂) = σ²(x₁) + σ²(x₂) siempre suma, independientemente del signo entre las variables → 9+16=25.

**4)** Un taller produce en promedio 5 pantalones defectuosos por día (distribución desconocida, asimétrica), con desvío 2. Sobre 50 días, ¿por qué se puede usar la distribución Normal para W = suma de 50 días?
a) Porque X ya es Normal
b) **Porque n=50 ≥ 30, aplica el Teorema Central del Límite** ✓
c) Porque la varianza es constante
d) No se puede usar Normal en este caso

*Justificación*: X no es Normal, pero al sumar n≥30 variables independientes, W tiende a Normal por TCL.

**5)** Si W = 3x₁ + 6x₂ (x₁, x₂ independientes), ¿cuál es la fórmula correcta de σ²_W?
a) σ²_W = 3σ²(x₁) + 6σ²(x₂)
b) **σ²_W = 3²·σ²(x₁) + 6²·σ²(x₂)** ✓
c) σ²_W = (3+6)²·σ²(x₁+x₂)
d) σ²_W = 3·σ(x₁) + 6·σ(x₂)

*Justificación*: en combinación lineal, cada coeficiente afecta la varianza al cuadrado: σ²(k·x)=k²·σ²(x).

**6)** Para una Binomial(n=20, p=0,4), P(X>9) equivale a:
a) P(X≥9)
b) **P(X≥10)** ✓
c) P(X≤9)
d) P(X≤10)

*Justificación*: en variable discreta, "mayor que 9" excluye el 9, por lo que P(X>9)=P(X≥10).

**7)** ¿Cuál de las siguientes NO es una condición necesaria para modelar con Poisson?
a) Los sucesos ocurren de forma independiente entre sí
b) La tasa promedio de ocurrencia es constante en el continuo
c) **El experimento debe tener un número fijo n de repeticiones** ✓ (es la condición de Binomial, no de Poisson)
d) Los sucesos se producen dentro de un continuo (tiempo, longitud, superficie, etc.)

*Justificación*: Poisson no requiere un n fijo de pruebas; eso es característico de Binomial.

**8)** En Binomial, si "éxito" se redefine como "NO comprar el producto" en vez de "comprar", y originalmente p(comprar)=0,6, ¿qué valor de p corresponde usar para la nueva variable?
a) p = 0,6 (no cambia)
b) **p = 0,4** ✓ (q original = 1−0,6)
c) p = 1
d) Depende de n

*Justificación*: al invertir qué se considera éxito, el nuevo p es el complemento del p original (q=1-p).

**9)** La varianza de una constante k es:
a) k
b) k²
c) **0** ✓
d) 1

*Justificación*: σ²(k)=0 — una constante no tiene dispersión, no confundir con μ(k)=k.

**10)** Un proceso Poisson tiene b = 12 eventos/hora. Se pregunta por la probabilidad de 3 eventos en 15 minutos. ¿Cuál es el λ correcto a usar?
a) λ = 12
b) λ = 3
c) **λ = 3** (b·t = 12·(15/60) = 12·0,25 = 3) ✓
d) λ = 12·15 = 180

*Justificación*: siempre convertir t a la misma unidad que b antes de multiplicar; 15 minutos = 0,25 horas.
