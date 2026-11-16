# Auditoría de lecciones — FEP (UNICABA)

Alcance: `lessons/0001–0014`, `lessons/index.html`, `reference/{machete-final,super-glosario,glosario-probabilidad-basica}.html`.
Verdad de referencia: `knowledge-base/01–07`, `NOTES.md`, y PDFs de `raw/` y `trabajos/` (releídos con `lit parse`: cronograma, Fórmulas 1°Parcial, muestral proporción, IC proporción, Binomial/Poisson, TP1/3/4/5/6 + respuestas).
Método: todo número de las lecciones recalculado con scipy; chequeo automático de coherencia opción↔feedback en los 61 quizzes; chequeo de links relativos; lectura completa de cada HTML. No se editó ningún archivo de lecciones.

Resumen ejecutivo:
- 1 bug funcional grave (quiz con feedback invertido) y 1 contradicción de convención (umbral CV).
- Aritmética: sin errores de fondo; solo redondeos (0005).
- El mayor problema NO es de errores sino de cobertura para el nuevo objetivo: **mecanizar**. Las lecciones están escritas para "la app calcula" y casi no hay un solo desarrollo numérico paso a paso. Varias cajas "Preguntame…" (0009, 0010, 0011, 0013) prometen justamente los ejemplos resueltos que faltan.
- Hoja de fórmulas del 1°Parcial (`raw/Fórmulas 1°Parcial.pdf`) trae SOLO: Pk, Mo, CV, condicional, unión, producto x2. No trae x̄/S² agrupados, binomial, Poisson, Z, IC. Conviene asumir que hay que saber de memoria todo lo demás (verificar la hoja del final).

---

## 1. Tabla priorizada

| # | Archivo | Problema | Sev. | Arreglo concreto |
|---|---|---|---|---|
| 1 | `0009-intervalos-de-confianza.html` (quiz 1) | **Feedback invertido.** Opción b ("El 95% de los datos caen entre 10 y 14", incorrecta) muestra panel verde "correcto" con la explicación de muestreo repetido; opción c (la correcta) muestra panel rojo "Eso describiría la dispersión de los datos". El alumno aprende lo contrario en LA trampa más importante de IC. Detectado por script: `q1b` flag=false/div=correct, `q1c` flag=true/div=wrong. | alta | Intercambiar los textos de `#q1b` y `#q1c` (o las clases correct/wrong). Revisar que el flag `true` coincida con la clase en los 61 quizzes (el resto está bien). |
| 2 | `super-glosario.html` §2 | Dice "CV < 5% → el promedio es representativo". Contradice machete, simulacro (Q2/Q4), NOTES.md y la clave del TP1 ("CV=27,17% >10%", "CV=42% >10%, promedio no representativo"). Origen: la red conceptual (`knowledge-base/02`) dice 5%; las respuestas del TP usan 10%. Un CV de 7% da respuestas opuestas según el umbral. | alta | Unificar en **10%** (clave de TPs) y anotar "(la red conceptual usa 5% como criterio más exigente; en TPs/parciales se usó 10%)". Aplicar igual en `knowledge-base/02` para no reintroducirlo. |
| 3 | (falta) Distribución muestral de la **proporción** | Es la clase 12 del cronograma (unidad 7) y no hay lección, ni sección en machete ni en super-glosario. Faltan: p̂ ~ N(p; √(pq/n)), μ_p̂=p, **condición de normalidad n·p ≥ 15 y n·q ≥ 15** (criterio de la cátedra, distinto de n≥30), y de dónde sale el IC de proporción. 0009 da el IC de proporción sin su justificación ni condición de validez. | alta | Nueva lección "Distribución muestral de la proporción + IC proporción" (ver §2). Agregar tarjeta al machete y sección al glosario. |
| 4 | (falta) Descriptiva con datos agrupados — **cuenta mecánica** | No hay ninguna lección con x̄, S², S, CV, Mo, Me, Pk en tabla de intervalos. 0011 solo tiene teoría de percentiles y termina con "¿Querés ver el cálculo… paso a paso?". Es el bloque más mecánico del final y el que la hoja de fórmulas NO resuelve (x̄ y S² no vienen). | alta | Lección nueva con TP1 Ej.7 resuelto (datos verificados abajo, §3.1): columnas f, F, Xm, Xm·f, (Xm−x̄)²·f; modo calculadora estadística (1-VAR con FREQ: cargar Xm y f; leer x̄, **s con n−1**, no σ con n; la clave de la cátedra usa n−1: S=3,0101). Cerrar con CV, Mo (Δ1, Δ2), Me, P20, P90 y "porcentaje bajo X" (Pk al revés). |
| 5 | (falta) Tabla Z / valores críticos — **cuenta mecánica** | 0008 no tiene ni un cálculo con Z (solo el ejemplo comparativo A vs B). No hay lectura de tabla, ni la regla de "P(Z<z)" con tabla acumulada, ni fractil inverso con número, ni valores críticos (1,645 / 1,96 / 2,576 / 2,326). Convención de la cátedra: Z_α y t_α se nombran por **α total (dos colas)**: Z_0,1=1,645 (90%), Z_0,05=1,96 (95%), t_19,0,05=2,093. Esto no está dicho en ningún lado. | alta | Ampliar 0008 (o nueva 0008b) con: (a) lectura de tabla Z paso a paso con 3 ejemplos (§3.2), (b) simetría: P(Z<−z)=1−P(Z<z), (c) fractil: de 0,90 → z=1,28 → x=μ+zσ, (d) mini-tabla de valores críticos con la convención α-total, (e) 95% ↔ ±1,96 (NO ±2: la regla empírica es aproximada). |
| 6 | (falta) Binomial y Poisson **por fórmula** | 0006 solo enseña a elegir distribución; no hay un solo P(X=k) calculado ni sumas acumuladas. Tampoco hay entrenamiento de las traducciones de tasa tipo TP3: "1 jugador cada 2,5 h → λ en 6 h = 2,4" (Ej.8), "1 boleto cada 6 s → λ en 15 s = 2,5" (Ej.18), "3 personas cada 5 min → 15 min λ=9" (Ej.15). 0006 solo cubre tasas "X por unidad" y 0014/0012 también. | alta | Agregar a 0006 (o lección nueva): C(n,r)·pʳ·q^(n−r) y e^−λ·λʳ/r! con calculadora, 2 ejemplos c/u (§3.3); regla "al menos uno = 1−P(0)" con Poisson; sumas cortas (≤3 términos) y cuándo conviene el complemento; tabla de conversión "cada X" → tasa b=1/X. |
| 7 | `0007-frecuencia-y-probabilidad.html` | La lección dice cubrir VA discreta pero no calcula E(X)=ΣxP, Var(X), σ, ni **CV<0,2 = baja fluctuación** (convención de la cátedra, TP3 Ej.2–4, aparece en machete sin desarrollo). Sin esto no se resuelven TP3 Ej.1–5 (tabla con incógnitas A,B,C; distribución de "facturas procesadas"; suma de 2 bolillas con/sin reposición). | alta | Sumar "Ejemplo resuelto": tabla errores 0–3 (E=1, V=1, σ=1, CV=1 → alta fluctuación) y tabla autos 0–4 (E=2,1; V=1,29; σ=1,136; CV=0,54, datos del TP3 Ej.2), con columnas x, P, x·P, (x−E)²·P. Calculadora modo 1-VAR con frecuencias=probabilidades. |
| 8 | `0010-regresion-y-correlacion.html` | El final tendrá la forma del TP6 (12 ítems MC) y la lección no cubre: (a) **leer diagramas de dispersión** (TP6 Ej.1,7,8: positiva/negativa, lineal, fuerte/moderada) — no hay ni un gráfico; (b) dado R²=87,1% **decidir el signo por contexto** (edad–precio → negativa; TP6 Ej.10) y r=±√R²; (c) predecir con la recta (Ej.3, 11: 159,62−0,10·800=79,62≈80); (d) obtener a, b, r con la calculadora en modo REG (Ej.12, y el TP final del grupo documenta las teclas); (e) residuos/linealidad (Ej.6). Cierra con "¿Querés el ejemplo helados…?". | alta | Agregar 4 SVG de dispersión (r≈+0,95, +0,7, −0,9, ≈0 curva) con quiz "clasificá"; tarjeta "R² no tiene signo: mirar el contexto"; ejemplo helados resuelto con pasos de calculadora (MODE→REG→A+BX→datos→SHIFT 1/2 → A, B, r); 3 ítems de predicción redondeada. Verificar datos del TP6 Ej.12 antes de publicar (A=0, B=3, r=0,941978 según el TP del grupo). |
| 9 | `0012-simulacro-final.html` | (a) Sesgo de posición: **16 de 22 correctas son "b"** (73%), 5 "a", 1 "c", nunca d/e; en todas las lecciones 45/61 son "b". El final es a–e y el simulacro solo tiene a–d: entrena "elegir b". (b) Ningún ítem exige calcular (todo es reconocer); contradice el objetivo actual. (c) Sin puntaje ni resultado final. | alta | Aleatorizar posición (incluir d y e), agregar 5.ª opción plausible. Añadir 10–12 ítems numéricos (Z con tabla, binomial/Poisson, IC con t, media agrupada, r/R²/predicción) con respuesta a 2–4 decimales y distractores por error típico (olvidar escalar λ, usar σ en vez de σ/√n, ≥ vs >, z de una cola). Contador de aciertos al pie. |
| 10 | `0005-normal-binomial-al-menos-uno.html` | Redondeo inconsistente: 0,855⁵ = **0,4569** (dice ≈0,458) → 1−0,4569 = **0,5431** (dice 0,542); P(Y>1)=0,1557 (dice 0,155). Los valores que muestra coinciden con p=0,1446 (z redondeado a −1,06 en tabla), no con "p≈0,145". Con z exacto (−1,0638) p=0,1437 → P(Y≥1)=0,5396. En MC la diferencia puede mover la opción. | media | Mostrar p=0,1446 (tabla, z=−1,06) y recalcular 0,458/0,542/0,155 con ese p; agregar nota: "app da 0,1437 → 0,540; elegí la opción más cercana". |
| 11 | `0003-bayes-vs-probabilidad-total.html` | Dice "se resuelve fácil con un diagrama de árbol" pero **no dibuja el árbol**. Los números son correctos (P(R)=0,04295; P(A/R)=0,4191; fuego/humo 9%). | media | SVG de árbol 3 ramas (0,45/0,32/0,23 → 0,04/0,06/0,025) con camino resaltado; botón "mostrar Bayes" que resalta solo la rama de A. Agregar mini-calculadora: el alumno cambia %. |
| 12 | `0008-normal-y-estandarizacion.html` | Faltan patrones que sí caen: **Normal condicional** P(X>18,3 | X<19)=0,2521 y P(X>μ | X>17,5)=0,7035 (TP4 Ej.8c/d; KB07 marca "Terminar" como punto débil); **búsqueda de parámetros** con dos percentiles (TP4 Ej.13: 10% sobre 65 y 10% bajo 55 → μ=60, σ=5/1,2816=3,90); combinación con constante (TP4 Ej.14c: +200 g). Regla empírica no aclara que 95% real es ±1,96σ. | media | Un ejemplo resuelto por patrón, con dibujo de campana sombreada (SVG) mostrando el área pedida y la resta/división. |
| 13 | `0009-intervalos-de-confianza.html` | (a) **No hay ni un IC calculado**; (b) no enseña el **método iterativo de n con t** (TP5 Ej.5b: 10→32, 20→27, 28→27, 27→27) aunque KB04 lo marca y es "dato de examen"; (c) omite **p=0,5 por defecto** cuando no hay estimación previa de p (IC proporción PDF); (d) omite que con n<30 y σ desconocido se asume población Normal; (e) omite condición n·p̂≥15, n·q̂≥15; (f) etiquetas: dice "Unidad 6 · Lección 1/3" pero IC es U7 (cronograma). | media | Agregar 3 ejemplos resueltos (todos verificados, §3.4): IC Z (TP5 Ej.1: 240±3,00 al 90% y ±3,58 al 95%), IC t (TP5 Ej.3: x̄=50,35, s=8,5733, t=2,093 → (46,34; 54,36)), IC proporción y n (140/500 → (0,247; 0,313); n=1364; 864 más; confianza inversa Z=0,996 → ≈68%). Corregir kicker a U7. |
| 14 | `0011-medidas-de-posicion-y-forma.html` | No incluye CV, Mo, ni la diferencia de posición datos sueltos (n+1)/2 vs tabla n/2 (que sí está en super-glosario y KB02 como punto "reforzado en clase"). Termina con "¿Querés ver el cálculo…?". Sin link de "Siguiente" (callejón sin salida). Kicker "Unidad 2 · Lección 3/3" dentro del bloque "Inferencia" del índice. | media | Cubrir con la lección nueva del ítem 4; agregar boxplot SVG interactivo (ver §4). Enlazar siguiente → 0013. |
| 15 | `0014-que-distribucion-uso.html` | (a) Cuadro "Tres casos" tiene **4 filas**; (b) suma/promedio no aclara independencia ni que, si x no es Normal, hace falta n≥30 (TCL); (c) no menciona Binomial→Normal (n≥30 por la cátedra, o n·p≥15 y n·q≥15 por la lámina de proporción: **dos criterios distintos en la cátedra**, hoy ninguno está en las lecciones); (d) sin ejemplo de suma resuelto. | media | Cambiar "Tres" por "Cuatro"; añadir fila TCL con condiciones; ejemplo TP4 Ej.14a (20 paquetes: μ=19000, σ=47√20=210,19, z=3,04 → P(>19640)=0,0012); aclarar en una caja los dos criterios de aproximación y cuál usar si el enunciado no dice. |
| 16 | `machete-final.html` | Faltan: dist. muestral de proporción y condición 15/15; p=0,5 por defecto; Binomial→Normal; valores críticos (1,645/1,96/2,576; convención α-total); fórmulas de x̄ y S² agrupados (la hoja no las trae); E, V, CV<0,2 en detalle; asimetría de la Binomial (p<0,5 positiva, TP3 Ej.12c); Mo con Δ; posición (n+1)/2 vs n/2; método iterativo con t. Sí está bien el umbral CV 10% y la convención Mo>x̄ negativa. | media | Agregar 3 tarjetas: "Fórmulas que la hoja NO trae", "Valores críticos y lectura de tabla", "Calculadora: pasos 1-VAR y REG". |
| 17 | `0012-simulacro-final.html` Q10 (opción d) | El feedback dice "ese caso límite justamente tiende a Poisson". La cátedra no enseña Poisson como límite de la Binomial (KB03: "no mencionada"); puede confundir. | baja | Reemplazar por "Sin p no hay Binomial". |
| 18 | `0001`–`0011` (JS) | `showFeedback` oculta TODOS los `.feedback` de la página; responder la pregunta 2 borra la explicación de la 1. El parámetro `correct` no se usa. 0012–0014 ya usan la versión por quiz. | media | Usar la versión de 0012 (limitada al `.quiz` padre) en las 11 lecciones; mejor, extraerla a `assets/quiz.js` y cargarla desde todas. Opcional: bloquear radios tras elegir y contar aciertos. |
| 19 | `0004-exhaustivos-y-traduccion-enunciados.html` | Falta el entrenamiento de **fracciones de n** ("a lo sumo la tercera parte", "menos de la tercera parte de 10": n/3=3,33 → X≤3; "al menos la tercera parte de 9" → X≥3; TP3 Ej.10b/16b) y de **redefinir éxito** en la misma frase ("recuperar" vs "irrecuperable", p=0,2 vs 0,8). 0006 menciona p'=1−p pero sin fracciones. | media | Tabla de 6 traducciones con n concreto, incluyendo n/3 no entero; 3 ítems de quiz que obligan a escribir (n, p, desigualdad) antes de ver opciones. |
| 20 | `0006` / `0014` / `0012` | Asimetría de la Binomial no cubierta (TP3 Ej.12c: p=0,15 → positiva; p>0,5 negativa; p=0,5 simétrica). | media | Una fila en 0006 con las 3 siluetas (ya existen SVG en 0014; reutilizar con p=0,15/0,5/0,85). |
| 21 | `0013-tablas-de-contingencia.html` | Correcta (tabla 0,12/0,18/0,60/0,10; P(A/Ū)=0,857; P(U∪A)=0,90). Falta: caso con **conteos** (clase 1-4-26: 8/10 tornillos, A/D=2/3 ≠ 4/9) y caso **sin reposición/con reposición** al lado (4/40·4/39 vs 4/40·4/40). | baja | Segundo ejemplo con conteos + el par con/sin reposición, ambos con tabla color-coded. |
| 22 | `lessons/index.html` | (a) Estilos propios: cuerpo en Fira Code (mono) — contradice la preferencia confirmada (sans Plus Jakarta; mono solo fórmulas); no usa `notebook.css`. (b) Subtítulo "8 días" desactualizado (re-rendir). (c) Agrupaciones con unidades erradas: "Unidad 6 · Inferencia" contiene regresión (cronograma: regresión = U8, IC = U7); Simulacro "★" al final pero numerado 12; 13/14 antes que 12. (d) Sin indicador de progreso. | baja | Importar `notebook.css` y limitar mono a `.n`; reordenar por syllabus real (U1-2, U4, U5, U6, U7, U8); renombrar subtítulo ("Re-rendir: repaso mecánico + conceptual"). |
| 23 | `assets/notebook.css` (`@media print`) | Solo pone `body{background:white;color:black}`: `h1/h2/strong/th` quedan en parchment/amarillo claro sobre blanco y las tablas conservan fondo oscuro con texto negro → **machete imprimido ilegible** (el machete trae reglas `@media print` propias para tarjetas, pero no arregla esto). | media | En `@media print` redefinir `--paper`, `--paper-raised`, `--ink`, `--ink-dim`, `--accent`, `--formula`, `--code-bg` a tonos claros/oscuros contrastados. |
| 24 | Todas las lecciones | Kickers de unidad inconsistentes con el cronograma: 0009 "Unidad 6", 0010 "Unidad 6", 0011 "Unidad 2 · 3/3", 0007 "Unidad 1-2 → 3", 0012 titula "Unidad 4 · Probabilidad" para Bayes etc. (U4 sí), "Unidad 5 · Normal" (U5 sí, pero Q15 suma = U6). | baja | Normalizar: U1-3 descriptiva, U4 probabilidad/VA/Bin/Poisson, U5 normal, U6 suma+TCL, U7 muestral+IC, U8 regresión. |
| 25 | `super-glosario.html` | Subtítulo "4 unidades cubiertas" (son 8); §5 sin IC de proporción, n para proporción ni confianza inversa; §4 sin combinación/suma de n iguales ni búsqueda de parámetros; trampas de `Var(x)=1` omite Var=0. | media | Alinear con machete: agregar IC proporción, n=Z²p̂q̂/E², amplitud=2E, suma de n, parámetros por 2 percentiles. |
| 26 | `glosario-probabilidad-basica.html` | Sin leyes de De Morgan ni complemento (están en KB01 y en machete parcialmente); sin link al machete/super-glosario. Resto correcto. | baja | Agregar 2 filas + nav-row. |
| 27 | `0004`, `super-glosario` (HTML) | `P(x < n/2)` con `<` sin escapar en `<td>`. Hoy el parser lo tolera (`<` + espacio es texto) pero es HTML inválido. | baja | Usar `&lt;`. |
| 28 | Varias lecciones (0001–0003, 0005, 0007–0009, 0011) | Enlaces externos a Math is Fun en inglés como "lectura recomendada"; sin mirror. Sin errores 404 internos: todos los `href`/`src` relativos resuelven. | baja | Opcional: reemplazar por referencia a los PDFs de `raw/` (más alineados con la cátedra). |
| 29 | `_site/` | Copia generada **idéntica** hoy a `lessons/`, `reference/`, `assets/`. Quedará desactualizada al editar. | baja | Regenerar `_site` tras aplicar los arreglos. |

---

## 2. Temas faltantes (por syllabus)

Cobertura contra el cronograma:

| Unidad (cronograma) | Estado en lecciones | Qué falta |
|---|---|---|
| U1–U3 Descriptiva (variables, tablas, gráficos, tendencia, variabilidad datos sueltos y agrupados, posición, asimetría) | Parcial: solo 0011 (teoría) y tarjetas del machete | **Lección mecánica completa** (ítem 4): x̄, S², S, CV, Mo, Me, Pk; datos sueltos vs agrupados; calculadora. Tipos de variable/muestreo/gráficos (bastones vs histograma) solo en machete. |
| U4 Probabilidad (clásica, conjunta, condicional, tablas, total, Bayes) | Buena (0001–0004, 0013) | Árbol visual (0003); conteos+con/sin reposición (0013); De Morgan/complemento. |
| U4 VA discreta (función de probabilidad, F, E, V) | Débil (0007 sin E/V) | E, V, σ, CV<0,2, distribuciones con incógnitas A,B,C, suma de 2 bolillas con/sin reposición (TP3 Ej.3–5). |
| U4 Binomial / Poisson | Elección sí (0006, 0014); **cálculo no** | Fórmula con calculadora, acumuladas, "cada X", asimetría Binomial, E/V/σ de cada una (σ ≠ Var). |
| U5 Normal / estandarizada / búsqueda de parámetros / combinación | Concepto sí (0008, 0014); **cálculo no** | Lectura de tabla Z, fractil numérico, condicional, parámetros por 2 percentiles, Normal→Binomial resuelto, bandas por percentiles (TP4 Ej.4: MB/B/M/S/I). |
| U6 Suma de variables y TCL | Tarjeta en 0014/machete | Propiedades de μ y σ² (signo +, k²), Y=kX, suma con constante, TCL n≥30 si no Normal, ejemplo resuelto (TP4 Ej.14/15/16/20). |
| U7 Distribución muestral de la media | Solo definición en 0009 | Ejemplo P(x̄ > a) con σ/√n; diferencia individuo vs promedio con números. |
| U7 **Distribución muestral de la proporción** | **Inexistente** | Lección nueva (ítem 3). |
| U7 IC media Z/t, IC proporción, tamaño de muestra | Concepto sí, **cero ejemplos numéricos** | Ver ítem 13: ejemplos resueltos + iteración con t + p=0,5 + confianza inversa + "cuántos más". |
| U8 Regresión / correlación | Concepto básico (0010) | Dispersión visual, signo por contexto, predicción, REG en calculadora, extrapolación con ejemplo. |

Temas puntuales sin ninguna cobertura en lecciones (sí aparecen en TPs/parciales):
1. x̄ y S² para datos agrupados + calculadora (s con n−1).
2. E(X), Var(X), CV<0,2 de VA discreta con tabla.
3. P(X=k) binomial/Poisson por fórmula; "1 cada X" → tasa.
4. Lectura de Z/t y convención α total; valores críticos clave.
5. Normal condicional; parámetros por 2 percentiles; bandas por percentiles.
6. Distribución muestral de la proporción; criterio n·p, n·q ≥ 15; p=0,5.
7. Iteración de n con t; IC inverso (hallar nivel de confianza).
8. Asimetría de la Binomial por el valor de p.
9. Lectura de diagramas de dispersión (fuerte/moderada/negativa) y signo de r por contexto.
10. Binomial→Normal (dos criterios en la cátedra; decidir cuál enseñar).

---

## 3. Material verificado listo para usar en las lecciones nuevas

Todos los valores recalculados (scipy); coinciden con las claves de la cátedra salvo redondeo.

### 3.1 Datos agrupados (TP1 Ej.7 — peso de 200 paquetes)
Intervalos [30,32)…[42,44) amplitud 2; f = 28, 36, 43, 51, 27, 11, 4 (N=200); Xm = 31, 33, …, 43.
x̄ = 35,62; S (n−1) = 3,0101 (con n sería 3,0026: no usar); CV = 8,45% (<20% homogéneo, <10% media representativa); Mo = 36 + 8/(8+24)·2 = 36,5 (Δ1=8, Δ2=24); Me = 35,674; P20 = 32,667; P90 = 39,630. Asimetría: Mo 36,5 > x̄ 35,62 ⇒ negativa.

### 3.2 Tabla Z / fractil
P(Z<1,28)=0,8997; P(Z<−1,06)=0,1446 (z exacto −1,0638 → 0,1437); z(0,90)=1,2816; z(0,95)=1,6449; z(0,975)=1,9600; z(0,99)=2,3263; z(0,995)=2,5758. Regla empírica exacta: 68,27% / 95,45% / 99,73%.
Latas N(750,50): P(X≥800)=0,1587; P(X<650)=0,0228; contenido mínimo del 10% superior = 750+1,2816·50 = 814,08.

### 3.3 Binomial y Poisson
Bi(8; 0,7): P(X=5)=C(8,5)·0,7⁵·0,3³=56·0,16807·0,027=0,2541. Bi(4; 0,7): P(X=2)=0,2646. Bi(20; 0,6): P(10)=0,11714; P(≤12)=0,58411. Bi(20; 0,4): P(>9)=P(≥10)=0,24466.
Poisson λ=3: P(2)=e⁻³·9/2=0,2240; P(≥1)=0,9502. Autos 15/min: P(11)=0,06629 (λ=15); P(>31 en 3 min, λ=45)=0,98222; P(7 en 30 s, λ=7,5)=0,14648. Bingo "1 cada 2,5 h", 6 h: λ=2,4; P(≥3)=0,43029.

### 3.4 Inferencia
IC Z: σ=10, n=30, x̄=240: 90% → ±3,003 (z=1,6449); 95% → ±3,578 (z=1,96).
IC t: n=20, x̄=50,35, s=8,5733, t₁₉=2,093 → (46,34; 54,36); t₁₉(0,01)=2,8609; t₉(0,01)=3,2498; t₅(0,05)=2,5706.
IC proporción: 140/500=0,28; z90=1,6449 → E=0,0330 → (0,247; 0,313). n para E=0,02: 1363,59 → 1364; "cuántos más" 864. Confianza inversa del (0,26; 0,30): E=0,02 → Z=0,996 → confianza ≈ 68,1%.
Suma: 20 paquetes N(950;47): total ~ N(19000; 210,19); P(>19640)=0,0012.

---

## 4. Propuestas de interactividad (máx. 10, cada una atada a un tema)

1. **Calculadora de tabla Z con campana sombreada** (U5, 0008). Slider de z o de x con μ,σ editables; muestra el área sombreada, la lectura "P(Z<z)" como en la tabla, y botón "al revés" (dada la probabilidad, devuelve z). El alumno primero escribe su respuesta y luego se contrasta.
2. **Tabla de frecuencias editable para datos agrupados** (U1–3, ítem 4). Alumno completa columnas Xm, Xm·f, (Xm−x̄)²·f con validación celda por celda (verde/rojo) y botón "mostrar pasos de calculadora (1-VAR)". Dataset precargado: TP1 Ej.7 y Ej.10.
3. **Binomial interactivo con bastones** (U4). Sliders n, p; resalta P(X=k), P(X≤k), P(X>k), muestra E, σ y la asimetría (p<0,5 positiva / p>0,5 negativa). Entrada "frase del enunciado" → desigualdad correcta ("más de la mitad" con n=9 → X≥5).
4. **Poisson con escalado de tasa** (U4). Dos controles: "tasa: X cada Y [unidad]" y "ventana: Z [unidad]"; muestra λ calculado paso a paso y barras; ejercicios "1 cada 2,5 h en 6 h".
5. **Árbol de probabilidad total/Bayes** (0003). Árbol SVG con porcentajes editables; el alumno elige "total" o "Bayes" y se resalta qué ramas suman (numerador) y cuáles forman el denominador.
6. **Simulador de cobertura de IC** (U7, 0009). Genera 100 muestras de una población dada y dibuja los intervalos como segmentos; cuenta cuántos contienen μ (≈95%). Es la prueba empírica de "la confianza es del método" (anula el error del ítem 1) y permite cambiar n y nivel para ver el ancho.
7. **Selector Z / t / proporción con iteración de n** (U7). Mini-asistente de decisión (¿σ conocido? ¿dato es fracción?) + tabla de iteración de n con t: el alumno ingresa un n inicial, ve ν, t, n resultante y repite hasta converger (TP5 Ej.5b: 10→32→20→27→28→27).
8. **Dispersión y r** (U8, 0010). Arrastrar puntos o elegir un patrón; muestra r, R², recta y predicción en vivo; alumno debe clasificar "positiva/negativa, lineal, fuerte/moderada" antes de ver r. Incluye caso "R²=87,1% edad–precio → decidir signo por contexto" y botón "extrapolar".
9. **Boxplot + asimetría arrastrable** (U2–3, 0011). Mover moda y media sobre un histograma; el cartel dice asimétrica positiva/negativa según la convención de la cátedra (Mo>x̄ ⇒ negativa); caja Q1–Q3 con RIC y bigotes del 25%.
10. **Simulacro cronometrado con repaso espaciado** (0012). Preguntas con posición aleatoria (a–e), puntaje, tiempo por ítem (objetivo ≈2 min), y registro en `localStorage` de qué tema falló para rearmar un mini-simulacro con los temas débiles (reutiliza `practice/data`).

---

## 5. Lo que está bien (no tocar)

- Aritmética de 0001–0004, 0007, 0008, 0012, 0013: verificada (0,04295; 0,4191; 9%; 20/36; 0,90; 0,5329; 166,31; tabla contingencia).
- Convenciones de la cátedra correctamente aplicadas en lecciones, simulacro y machete: Mo>x̄ ⇒ negativa, CV 20% homogeneidad, CV 10% representatividad de la media, R²>0,5, |r|≥0,7, σ_W=√n·σ, σ/√n, σ²(x₁±x₂) suma siempre, IC proporción con Z, E=amplitud/2, redondeo de n hacia arriba, extracción sin reposición por defecto (glosario).
- Links internos: sin rotos. Estilo: todas las lecciones usan `notebook.css` y sus clases existen (`.box/.example/.warn/.ask/.quiz/.feedback/.term/.formula/.nav-row/.two-col`); únicas excepciones: `index.html` (CSS propio) y los `<style>` locales de 0013/0014/super-glosario/machete (coherentes con los tokens).


---

## Estado de correcciones

Leyenda: **fixed** = corregido · **partial** = corregida la parte de corrección, el resto es contenido nuevo (pendiente) · **skipped** = no se tocó (motivo).

| # | Estado | Detalle |
|---|---|---|
| 1 | fixed | 0009 quiz 1: la correcta es la lectura de muestreo repetido; "95% de los datos caen entre…" ahora es incorrecta y explica que confunde el IC de μ con el rango de los datos. |
| 2 | fixed | `super-glosario` §2: CV<10% = media representativa (CV<20% homogeneidad), con nota de que la red conceptual usa 5%. Machete, simulacro y lecciones ya usaban 10%. `knowledge-base/02` NO se tocó (fuera de alcance): hay que alinearlo aparte. |
| 3 | skipped | Lección nueva (dist. muestral de la proporción); se hace después. En 0009 se agregó solo la condición n·p̂≥15 y n·q̂≥15. |
| 4 | skipped | Lección nueva (descriptiva agrupada). |
| 5 | skipped | Tema nuevo (tabla Z / valores críticos). Solo se aclaró en 0008, machete y glosario que el 95% exacto es ±1,96σ. |
| 6 | skipped | Tema nuevo (Binomial/Poisson por fórmula, tasas "cada X"). |
| 7 | skipped | Tema nuevo (E, Var, CV<0,2 con tablas). |
| 8 | skipped | Tema nuevo (dispersión, REG, predicción). |
| 9 | partial | 0012: 5.ª opción plausible en las 22 preguntas, opciones reordenadas; correctas ahora a5/b5/c4/d4/e4 (antes 16 de 22 eran "b"). Skipped: ítems numéricos nuevos y contador de aciertos (contenido nuevo). Feedback sin referencias a letras. |
| 10 | fixed | 0005: p=0,1446 (tabla, z=−1,06); 0,8554⁵≈0,458 → 0,542; P(Y>1)=0,155; nota de que con z exacto p=0,1437 y P(Y≥1)=0,540. Verificado con scipy. |
| 11 | partial | 0003: árbol SVG inline (paleta Kanagawa) con la rama de A resaltada y suma 0,04295. Skipped: botón "mostrar Bayes" y mini-calculadora (interactividad nueva). |
| 12 | partial | 0008: nota 68,27/95,45/99,73 y ±1,96σ. Skipped: ejemplos condicional / parámetros por 2 percentiles / combinación (contenido nuevo). |
| 13 | partial | 0009: kicker → Unidad 7; nota de población Normal con n<30; condiciones n·p̂, n·q̂ ≥ 15; p̂=0,5 por defecto. Skipped: ejemplos resueltos de IC, iteración de n con t, confianza inversa numérica (contenido nuevo). |
| 14 | partial | 0011: kicker "Unidades 1–3", sin "3/3", link "Siguiente → 0013". Skipped: CV/Mo/posición (n+1)/2 vs n/2 y boxplot (lección nueva). |
| 15 | fixed | 0014: "Cuatro casos"; caja de independencia y TCL (n≥30 si x no es Normal); ejemplo resuelto TP4 Ej.14a (σ=210,19; z=3,04; P≈0,0012, verificado); caja con los dos criterios Binomial→Normal. La indicación de cuál usar ante la duda es mía: confirmar con la cátedra. |
| 16 | partial | Machete: regla 1,96, condición 15/15, p̂=0,5 y supuesto de Normalidad en la tarjeta de IC. Skipped: tarjetas nuevas (fórmulas que la hoja no trae, valores críticos, calculadora). |
| 17 | fixed | 0012 Q10: feedback ahora "Sin p no hay Binomial: la Binomial necesita n y p conocidos." |
| 18 | fixed | `showFeedback` limitado al `.quiz` padre en 0001–0011 (igual que 0012–0014), inline en cada lección. Skipped: extraerlo a `assets/quiz.js` (fuera de alcance). |
| 19 | partial | 0004: tabla de 6 traducciones con fracciones de n (incluye 10/3 no entero) y caja n/p/desigualdad. Skipped: 3 ítems de quiz nuevos. |
| 20 | skipped | Asimetría de la Binomial (contenido nuevo). |
| 21 | skipped | 0013 ya es correcta; los casos con conteos y con/sin reposición son contenido nuevo. |
| 22 | skipped | `lessons/index.html` fuera de alcance. |
| 23 | partial | Machete: bloque `@media print` propio con paleta clara (fondo blanco, texto/acentos oscuros, `.ask` oculto). `assets/notebook.css` NO se tocó (fuera de alcance): el `@media print` global sigue igual para lecciones y super-glosario. |
| 24 | fixed | Kickers: 0001–0004 "Unidad 4", 0005 "Unidades 4–5", 0006 "Unidad 4", 0007 "Unidades 1-3 → Unidad 4", 0009 "Unidad 7", 0010 "Unidad 8", 0011 "Unidades 1–3". Encabezados del simulacro: "Unidades 1–3", "Unidades 5–6 (normal y suma)", "Unidad 7". |
| 25 | partial | Super-glosario: subtítulo "8 unidades"; IC proporción, n para proporción (p̂=0,5), E y amplitud=2E, confianza inversa, suma de n iguales, parámetros por 2 percentiles; "salvo Var=0 o Var=1" (también en 0006). |
| 26 | fixed | Glosario de probabilidad básica: filas Complemento y De Morgan + link a machete y super-glosario. |
| 27 | fixed | `&lt;` en `P(x < n/2)` (0004, super-glosario) y `Mo < x̄` (super-glosario); `&gt;` en `P(x > n/2)`. |
| 28 | skipped | Opcional: enlaces a Math is Fun sin cambios. |
| 29 | skipped | `_site/` fuera de alcance; hay que regenerarlo. |

Cambio extra: en las 14 lecciones, las respuestas correctas quedaron repartidas en posiciones (los 61 quizzes: a15/b15/c14/d13/e4; antes 45 de 61 eran "b"). Se reordenaron opciones y feedback juntos; ids `qNx` regenerados por posición.

Validación: parseo html5lib sin errores (solo se escaparon los `&` de la URL de Google Fonts), balance de etiquetas OK, links relativos sin rotos, y para los 61 quizzes: una sola opción correcta, flag `true` ⇔ panel `correct`, ids únicos y sin referencias huérfanas.
