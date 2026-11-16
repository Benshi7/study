# Estadística — Final Multiple Choice — Resources

## Knowledge

- [Math is Fun: Mutually Exclusive Events](https://www.mathsisfun.com/data/probability-events-mutually-exclusive.html)
  Explicación clara y visual de sucesos mutuamente excluyentes, con la aclaración clave de que son en realidad *dependientes* (si ocurre uno, la probabilidad del otro cae a cero). Usar para: la trampa "independientes ≠ mutuamente excluyentes".
- [Math is Fun: Independent Events](https://www.mathsisfun.com/data/probability-events-independent.html)
  Definición de independencia, la falacia del jugador, y contraste con sucesos dependientes (ej. extracción sin reposición). Usar para: reforzar cuándo multiplicar probabilidades directamente vs. condicionalmente.
- [Math is Fun: Conditional Probability](https://www.mathsisfun.com/data/probability-events-conditional.html)
  Distingue con claridad probabilidad conjunta P(A y B) de probabilidad condicional P(B|A), con la fórmula que las conecta y el ejemplo del helado (chocolate/frutilla) para extraer una condicional a partir de datos conjuntos. Usar para: la trampa "condicional ≠ conjunta".
- [Math is Fun: Bayes' Theorem](https://www.mathsisfun.com/data/bayes-theorem.html)
  Explica el teorema de Bayes como una "inversión" de una condicional ya conocida, con el ejemplo intuitivo de fuego/humo (P(fuego) es raro, P(humo) es común, 90% de los fuegos generan humo → P(fuego/humo) da solo 9%, mostrando por qué vale la pena revisar igual). Usar para: distinguir Bayes (causa puntual) de probabilidad total (denominador que suma todos los caminos).
- [Math is Fun: The Complement Rule](https://www.mathsisfun.com/data/probability-complement.html)
  P(A) + P(A') = 1, con el ejemplo de "es más fácil calcular el complemento primero" cuando el suceso directo es complicado de contar. Usar para: la trampa de "al menos uno" ⇒ P(X≥1) = 1 − P(X=0).
- [Math is Fun: Random Variables](https://www.mathsisfun.com/data/random-variables.html)
  Muestra el puente entre frecuencia y probabilidad con el ejemplo de la suma de dos dados: "probabilidad = frecuencia del valor / total de resultados". Usar para: la transición conceptual de tabla de frecuencias (Estadística Descriptiva) a función de probabilidad (variable aleatoria).
- [Math is Fun: Standard Normal Distribution](https://www.mathsisfun.com/data/standard-normal-distribution.html)
  Explica la estandarización (Z) como "restar la media, dividir por el desvío", y por qué sirve: permite usar una sola tabla de referencia en vez de una por cada combinación de μ y σ. Incluye la regla empírica 68-95-99,7. Usar para: el concepto de por qué estandarizamos, no el cálculo manual.
- Material propio de la cátedra, ya resumido en `knowledge-base/*.md` (7 bloques, generados a partir de los PDFs originales de la materia: teoría, glosario, apuntes de clase, resúmenes, TPs y exámenes corregidos previos). Fuente primaria para todo el contenido — los recursos externos son solo para reforzar/citar, no para reemplazar la bajada de la cátedra (la cátedra tiene convenciones propias, ej. "sin especificar reposición → se asume sin reposición").

- [Math is Fun: Confidence Intervals](https://www.mathsisfun.com/data/confidence-interval.html)
  Explica el IC como x̄ ± margen de error y, sobre todo, la interpretación correcta del nivel de confianza (propiedad del método sobre muestreo repetido, no probabilidad del intervalo ya calculado). Usar para: Lección 9, la trampa "95% de confianza".
- [Math is Fun: Correlation](https://www.mathsisfun.com/data/correlation.html)
  r de −1 a 1, dirección y fuerza, y el recordatorio "correlation is not causation" con ejemplos. Usar para: Lección 10, correlación vs. causalidad y lectura del signo.
- [Math is Fun: Quartiles / Skewness](https://www.mathsisfun.com/data/quartiles.html)
  Cuartiles, RIC, boxplot y asimetría visual. Usar para: Lección 11, posición y forma. Ojo: para el signo de la asimetría prima la convención de la cátedra (Mo > x̄ ⇒ negativa), no la etiqueta de la web.

## Wisdom (Communities)
No se buscaron comunidades — la mission es repaso individual para un final en 8 días, no hay tiempo/necesidad de validación en comunidad. Si el usuario cambia de opinión, agregar acá.

## Gaps
- Falta recurso externo específico para Teorema de Bayes y distribuciones discretas (binomial/Poisson) — las lecciones 3, 5 y 6 se apoyan por ahora en la KB de la cátedra.
- Inferencia (IC), regresión/correlación y medidas de posición/forma ya cubiertas con recursos (ver arriba) y con lecciones 9, 10 y 11.
