# Material de Exámenes Previos y TPs

Fuentes:
- `2026-05-13-Nota-18-07_anotado.pdf` (4 páginas)
- `2026-05-27-Nota-18-22_anotado.pdf` (4 páginas)
- `TPNº1 PPT ej 7 y 10.pdf` (13 páginas)
- `Trabajo Final.pptx` (19 diapositivas)

**Aclaración importante sobre los dos PDF "anotado"**: a pesar del nombre de archivo (que sugiere una nota/calificación, ej. "Nota-18-07"), el contenido de ambos PDF NO muestra una corrección docente con calificación numérica circulada, tachones en rojo del profesor, ni comentarios de "bien/mal" de un corrector externo. Lo que contienen es la **resolución manuscrita propia del usuario**, con autoanotaciones tipo recordatorio ("OJO", "Terminar", flechas de aclaración). El "18-07" y "18-22" del nombre de archivo parecen ser una marca de hora de exportación (18:07 hs y 18:22 hs), no una nota sobre 10 o sobre 20. Esto se aclara para no inventar una calificación que no está documentada en el archivo.

## Qué se evaluó en estos exámenes/TPs corregidos (temas, tipo de ejercicio)

### 2026-05-13-Nota-18-07_anotado.pdf — Distribución Normal
- **Ejercicio 3**: dosificación de latas de cerveza, X ~ N(750, 50). Cálculo de P(X≥800) por aproximación (uso de tabla/app), P(X<650), y cálculo de un valor `a` tal que P(X>a)=0,1 (percentil de la normal, "el 10% con mayor contenido").
- **Ejercicio 5**: estaturas X ~ N(1,68; σ), con σ desconocido a despejar a partir de un percentil dado (P(X<1,78)=0,95 ⇒ estandarizar y despejar σ). Luego calcular P(X>1,8) y el percentil 10 inferior.
- **Ejercicio 6**: peso de paquetes de harina X ~ N(950, 47). Incluye un ítem c) que combina Normal + **Binomial**: probabilidad de que, en una muestra de 5 paquetes, "alguno" pese menos de 900 g ⇒ se modela Y ~ Bi(5, p) con p = P(X<900) hallado por la Normal, y luego se pide P(Y≥1).
- **Ejercicio 8**: consumo de combustible X ~ N(18,5; 1,8). Incluye probabilidad de un intervalo, un percentil (95%), y dos ítems de **probabilidad condicional** con la Normal: P(X>18,5 | X>17,5) y P(X>18,3 | X<19).
- **Ejercicio 9**: peso de bolsas de café X ~ N(250, 20). Unión de dos eventos disjuntos (P(X<244,36) ∪ P(X>255,64)) y percentil superado por el 5%.

### 2026-05-27-Nota-18-22_anotado.pdf — Intervalos de Confianza para la media (y tamaño de muestra)
- Encabezado con las 3 fórmulas madre del tema: IC para μ con σ conocido (usa Z), IC para μ con σ desconocido (usa t de Student), e IC para proporción p (usa Z). También las fórmulas de tamaño de muestra n para cada caso.
- **Ejercicio 1**: σ conocido (10 hs), n=30, x̄=240 hs. IC al 90% y 95% usando Z (Z_0,1=1,645 y Z_0,05=1,96).
- **Ejercicio 3**: presión arterial diastólica, muestra de n=20, σ desconocido (se estima S con calculadora: x̄=50,35, S=8,5733). IC al 95% y 99% usando t con 19 grados de libertad (t_19,0,05=2,093; t_19,0,01=2,8609).
- **Ejercicio 4**: tiempos de compra online, n=10, σ desconocido. IC al 99% con t_9,0,01=3,2498.
- **Ejercicio 5**: velocidad de lectura, n=6, σ desconocido. a) IC al 95% con t_5,0,05=2,57. b) **Cálculo iterativo de tamaño de muestra** cuando σ es desconocido: como la fórmula n=(t·S/E)² depende de t, que a su vez depende de los grados de libertad (n−1), hay que iterar probando distintos n hasta que el resultado converja (se probó n=10→resultado 32; n=20→27; n=28→27; n=27→27, deteniéndose en n=27 alumnos).
- **Ejercicio 6**: tiempo de atención al cliente, σ CONOCIDO (4,215 min, dato dado). a) IC al 98% (nivel de riesgo 2%) usando Z. b) cuántos clientes más observar para reducir el error de muestreo en 1 minuto (usa E=4−1=3 minutos y recalcula n). c) **ejercicio inverso**: dado un intervalo ya construido (12,142 ; 15,858), despejar el nivel de confianza — se iguala el extremo inferior del IC a la fórmula, se despeja Z, se busca el área asociada en la tabla, y se obtiene α y luego 1−α (nivel de confianza = 72%).

## Errores que el usuario cometió (según las anotaciones/correcciones)

No hay marcas explícitas de corrección docente (tachones, "mal", nota numérica) en ninguno de los dos PDF. Lo que sí hay son **autoanotaciones que delatan los puntos donde el usuario dudó o necesitó un recordatorio especial**, y que son las zonas de mayor riesgo de error en un examen real:

1. **Ejercicio 6.c del examen del 13/05 (harina)**: anotación en verde "OJO: acá la igualdad importa!" junto al cálculo de P(Y≥1) en una Binomial derivada de una Normal. Esto señala que el usuario identificó como punto crítico la diferencia entre P(Y≥1) y P(Y>1) — un error típico es usar el complemento mal (1 − P(Y=0) da P(Y≥1), pero si se confunde con P(Y>1) el resultado cambia). **Recomendación de repaso**: practicar la traducción de "al menos uno"/"alguno" a la desigualdad correcta antes de aplicar el complemento.

2. **Ejercicio 8.d del examen del 13/05 (combustible, probabilidad condicional)**: anotación roja "Terminar" (terminar/completar) al lado del resultado final, sugiriendo que el ítem quedó incompleto o se resolvió con premura contra el tiempo. Es un ítem de probabilidad condicional con la Normal (P(X>18,3 | X<19)), tema que combina dos herramientas (estandarización + fórmula de condicional) y es más lento de resolver — riesgo real en un multiple choice cronometrado.

3. **Ejercicio 5.b del examen del 27/05 (tamaño de muestra con t de Student)**: anotación "¡OJO! t se mueve con n" — es el gotcha central de calcular n cuando σ es desconocido: no se puede despejar n en un solo paso porque t depende de los grados de libertad (n−1). Requiere iteración (probar un n, recalcular t, recalcular n, repetir hasta estabilizar). El usuario iteró correctamente hasta converger en n=27, pero el proceso muestra que necesitó varios intentos (n=10, 20, 28, 27, 26) antes de encontrar el valor estable — es la parte del tema con más probabilidad de fallar por atajos ("despejar n directo sin iterar").

4. **Ejercicio 6.c del examen del 27/05 (IC inverso — hallar nivel de confianza)**: es un ejercicio "al revés" (dado el intervalo, hallar 1−α) que exige despejar Z de la fórmula y buscar el área correspondiente en la tabla en sentido inverso. No hay marca de error, pero es estructuralmed distinto a los demás (que van de datos → IC) y aparece marcado con signos de interrogación ("¿α?") mientras se resolvía, indicando que costó identificar el camino a seguir.

**Patrón general identificado**: los puntos de fricción no son errores de cálculo aritmético, sino de **identificar qué fórmula/enfoque usar cuando el ejercicio se plantea "al revés"** (dado el resultado, hallar el parámetro) o cuando se combinan dos distribuciones (Normal → Binomial) o dos herramientas (Normal + condicional). Esto es información valiosa para priorizar el repaso.

## Ejercicios del TPNº1 (enunciado y resolución)

Archivo: `TPNº1 PPT ej 7 y 10.pdf` — Trabajo Práctico Nº1 "Fundamentos de Estadística y Probabilidad", ejercicios 7 y 10 (estadística descriptiva con datos agrupados en intervalos).

### Ejercicio 7 — Peso de 200 paquetes de pastillas (tabla de intervalos)
Tabla de frecuencias: intervalos de peso [30-32) a [42-44), f y F acumulada, N=200.

- **a)** Variable: peso (gramos) de los paquetes → cuantitativa continua.
- **b)** Modo y mediana:
  - Mo = 36,5 gramos (intervalo modal [36,38), usando Δ1=8, Δ2=24).
  - Me = 35,67 gramos (intervalo mediano [34,36), con F_a=64, f=43).
- **c)** Homogeneidad (coeficiente de variación): x̄=35,62 g, S=3,0101 g ⇒ CV=8,45% < 20% ⇒ **datos homogéneos**.
- **d)** Percentil 20 (peso no superado por el 20% de los paquetes): P20 = 32,67 g (intervalo [32,34)).
- **e)** Percentil 90 (peso superado solo por el 10%): P90 = 39,63 g (intervalo [38,40)).
- **f)** Porcentajes con distintos umbrales:
  1. Hasta 40 g: 92,5% (interpolando con Pk).
  2. Al menos 34 g: 68% (sumando frecuencias de los intervalos desde 34 en adelante: 43+51+27+11+4=136 sobre 200).
  3. Como máximo 38,15 g: 80,01% (despejando k de la fórmula de Pk).
  4. Como mínimo 33,50 g: 72,5% (complemento de 27,5%, usando la fórmula 100−k).
- **Adicional (forma de la distribución)**: comparando Mo=36,5 y x̄=35,62 (Mo > x̄) ⇒ **asimetría negativa**. Coherente con la regla del archivo 06.

### Ejercicio 10 — Tiempo de atletas en una prueba olímpica (tabla de intervalos)
Tabla: intervalos de tiempo [10-15) a [30-35), n=50 atletas.

- **a)** Homogeneidad y asimetría: CV = 28,65% > 20% ⇒ **datos NO homogéneos**. Comparando Mo=17,71 min y x̄=20,3 min (Mo < x̄) ⇒ **asimetría positiva**.
- **b)** Tiempo del competidor más rápido del 15% más lento: se interpreta como P85 = 27,5 min (intervalo [25,30)).
- **c)** Tiempo máximo para recibir una de las 10 medallas (10 de 50 = 20% más rápidos): P20 = 15,48 min (intervalo [15,20)). Nota manuscrita clave: "el subíndice siempre es % del total acumulado a IZQUIERDA" — recordatorio de que el percentil se define siempre respecto al porcentaje que queda POR DEBAJO, incluso cuando el enunciado habla de "los más rápidos" o "los más lentos" (hay que traducir correctamente a qué lado corresponde el percentil).

## Resumen del Trabajo Final

Archivo: `Trabajo Final.pptx` (19 diapositivas). Tema: **Regresión y Correlación**, aplicado a un caso real de Argentina. Integrantes: Dario F. Jerez, Mirkala Parra, Fari, D. Rodrigo Ruiz.

- **Diapositivas 2-5 (marco teórico)**: diferencias entre correlación y regresión (la regresión predice y modela causa-efecto con una ecuación; la correlación solo cuantifica fuerza/dirección con un número, r). Tabla comparativa (objetivo, simetría/asimetría, dependencia, instrumento). Fórmula e interpretación del coeficiente de correlación de Pearson (r entre -1 y 1: -1 correlación lineal perfecta negativa, 0 sin correlación lineal, 1 perfecta positiva).

- **Diapositivas 6-13 (caso práctico)**: aplicación con datos de INDEC, Argentina, período enero 2024 - diciembre 2025 (24 observaciones mensuales). Variables: inflación mensual (X, independiente) vs. variación salarial (Y, dependiente). Incluye diagrama de dispersión (tendencia ascendente, relación positiva), modelo de regresión lineal y = a + bx, resultado obtenido: **y = 1,6246 + 0,8021x** (por cada 1% de inflación, el salario sube ≈0,80%). Predicción con x=2,9% de inflación esperada ⇒ y≈3,95% de variación salarial estimada. Error estándar de la estimación: s=1,3667. Coeficiente de determinación R² explicado como el cuadrado de r, interpretado como % de variabilidad de Y explicada por X, con la regla práctica de que R² > 0,5 indica un ajuste aceptable.

- **Diapositiva 15**: instructivo paso a paso para usar la calculadora científica en modo REG/A+BX para obtener a, b y r (MODE → REG → A+BX → ingresar pares con la tecla M+ → SHIFT+2 para ver S-VAR → leer A, B, r).

- **Diapositivas 16-18 (resolución de ejercicios adicionales del TP de Regresión)**: Ejercicio 5 (longitudes óseas, correlación lineal positiva justificada por proporcionalidad antropométrica) y Ejercicio 12 resuelto por dos métodos con calculadora científica en modo REG (resultado: A=0, B=3, recta Y=3X, r=0,941978).

**Integración de temas**: el Trabajo Final es la aplicación práctica end-to-end del bloque de Regresión y Correlación (que no forma parte de las medidas de posición/forma, pero sí es material de examen relevante) — muestra el uso real de la calculadora científica en modo estadístico, que es la misma herramienta (S-VAR, modo SD/REG) usada en otros temas de la materia para hallar x̄ y S rápidamente (como se ve en las anotaciones "de la muestra con la calculadora" en los dos exámenes anotados).

## Recomendaciones de repaso basadas en los errores identificados

1. **Practicar la traducción de enunciados a desigualdades correctas** ("al menos", "como máximo", "más de", "no menos de") antes de aplicar fórmulas — es el punto de fricción más repetido en los 3 documentos analizados (harina ítem c, TP1 ejercicio 10 ítem c).

2. **Automatizar el algoritmo de cálculo de tamaño de muestra n cuando σ es desconocido (usa t)**: armar una tabla mental de iteración rápida (probar n, mirar t en la tabla de t-Student, recalcular n, repetir) para no perder tiempo en el examen. Si σ es conocido (usa Z), n se despeja en un solo paso — diferenciar bien ambos casos ANTES de empezar a calcular.

3. **Repasar ejercicios "inversos"** (dado el IC o el percentil, hallar el nivel de confianza o el parámetro desconocido): son menos frecuentes en la práctica pero aparecieron en ambos exámenes anotados (ítem 8.c "harina" tipo inverso implícito, e ítem 6.c "atención al cliente" totalmente inverso) — practicar despejar Z o k de las fórmulas estándar.

4. **Repasar combinación Normal + Binomial** (probabilidad de éxito p obtenida de una Normal, usada luego como parámetro de una Binomial): aparece en el ejercicio de la harina y es un patrón de multiple choice típico (dos distribuciones encadenadas en un mismo ítem).

5. **Reforzar el signo de la asimetría con la regla Mo vs. x̄** (ver archivo 06): se aplicó correctamente en TODOS los casos verificados en TP1, así que la regla está bien internalizada — mantenerla así, sin necesidad de repaso adicional en este punto puntual.

6. **Practicar tiempos**: la anotación "Terminar" en el ejercicio de combustible sugiere presión de tiempo en ítems de probabilidad condicional con Normal — practicar resolver ese tipo de ítem en menos de 2-3 minutos para no comprometer el resto del examen.

## Verificación de claves

Recalculado con Python (scipy) contra enunciados y claves de la cátedra.

**Discrepancias analizadas (TP4)**
- **TP4 ej 6c (harina, 5 paquetes, clave 0,52957)**: σ = 47 es el desvío de UN paquete y el enunciado es "alguno de 5 < 900 g" (Normal → Binomial, no suma ni media de 5). p = P(X < 900) = 0,1437 y P(Y ≥ 1) = 1 − (1 − 0,1437)⁵ = **0,5396**. La clave 0,52957 reproduce exactamente 1 − 0,86⁵, es decir que **redondeó p a 0,14**. Veredicto: la clave está redondeada; vale 0,5396 (con z de tabla −1,06 daría 0,5413). El banco (p2-015) conserva 0,5396.
- **TP4 ej 1b (clave 6,69%)**: 1 − Φ(1,5) = 0,066807 = **6,68%** (la clave lo expresa como "alrededor del 7%"; 6,69% sale de redondear la tabla). Banco: 6,68%, sin ninguna opción cercana a 6,69%.
- **TP4 ej 4b (clave 65,45)**: exacto 72 + z(0,30)·12,5 = 65,44499 (la calculadora muestra 65,44), pero con z de tabla = −0,524 da 72 − 6,55 = **65,45**. Convención de la cátedra: z de tabla ⇒ 65,45. Banco (p2-006) corregido a 65,45 (la tabla del enunciado ya trae z = −0,524) y paso con la calculadora aclara 65,445.
- Otros hallazgos menores: ej 8a de la clave dice (15,5 < X < 22,42) pero el enunciado es 15,15 (0,95393 corresponde a 15,15; con 15,5 daría 0,9375); ej 8d clave 0,2515 vs exacto 0,2521; ej 5b clave 0,02458 sale de σ redondeado 0,061 (exacto 0,0242).

**Otras claves con error de tipeo/no reproducibles**
- TP1 ej 11d: clave 6451,54; correcto **6461,54** (6000 + 3/13·2000). TP1 ej 11e: clave "65000"; correcto **6500**.
- TP5 ej 10b: clave 32 facturas; con t(0,05; 9) fijo da 36,4 ⇒ 37 y con Z da 29,3 ⇒ 30; 32 sólo se reproduce **iterando t(n−1)** (n = 32 es punto fijo). Por eso no se incluyó en el banco.
- TP6 ej 12: las opciones b y e del enunciado son idénticas (y = 0,15 + 3x); la correcta es d (y = 3x, a = 0 exacto).

**Convenciones vistas en las resoluciones manuscritas (Práctica 2do parcial y Práctica adicional)**
- Variables y distribución siempre explicitadas (X = ..., X ~ Normal(μ; σ)); se usan **6 decimales** de la calculadora (0,261118; 0,331111; 0,747507), sin tabla.
- Condicional: P(A|B) = P(A∩B)/P(B) con dibujo de la recta; "más de la mitad de 12" = P(Y ≥ 7); "más de la mitad de 10" = P(Y ≥ 6); p de la Binomial = 0,2525 (4 decimales).
- Suma de n variables: W = X₁ + … + Xₙ, μ_W = nμ, σ_W = σ√n (σ² = nσ²).
- IC: **Z(90%) = 1,64** (no 1,645; aunque la clave de TP5 usa 1,645), Z(95%) = 1,96; error en 2-3 decimales (E = 5681,13; 0,068); **σ conocido ⇒ Z; σ desconocido y n chico ⇒ t** (t(0,025; 4) = 2,776) con s de n − 1.
- Reducir el error en 60%: E' = 0,4·E, n = (Z·σ/E')² = 75,00004 y **se redondea siempre hacia arriba** ⇒ 76, "64 meses más" (el cociente exacto daría 75, pero la cátedra publica 64). Para proporciones: E = 0,068 → E/2 = 0,034 ⇒ n = 797,56 ⇒ **798 en total**.
- Nivel de confianza dado un intervalo: z = E√n/σ, confianza = 99,6% (z = 2,887) y 99,95% (z = 3,4641).
- No se escribe interpretación textual extensa: se encuadra el resultado y se aclara "min", "meses más", "personas".
