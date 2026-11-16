# Regresión y Correlación

## Correlación

El **coeficiente de correlación de Pearson (r)** mide la **fuerza** y la **dirección** de la relación **lineal** entre dos variables cuantitativas.

**Fórmula:**

```
r = Sxy / √(Sxx · Syy) = (Σx·y − n·x̄·ȳ) / √[(Σx² − n·x̄²) · (Σy² − n·ȳ²)]
```

También puede escribirse como:

```
r = Σ(xᵢ − x̄)(yᵢ − ȳ) / √[Σ(xᵢ − x̄)² · Σ(yᵢ − ȳ)²]
```

**Rango:** −1 ≤ r ≤ 1

**Interpretación del signo:**
- r > 0 → relación **directa** (o positiva): cuando una variable aumenta, la otra también aumenta.
- r < 0 → relación **inversa** (o negativa): cuando una variable aumenta, la otra disminuye.
- r = 0 → no hay relación **lineal** (pueden existir relaciones no lineales/curvilíneas que r no detecta).

**Interpretación de la magnitud (según la cátedra, criterio usado en clase):**
- −0,7 < r < 0,7 → relación **débil** (cuanto más cerca de 0, más débil)
- r ≤ −0,7 o r ≥ 0,7 → relación **fuerte** (cuanto más cerca de ±1, más fuerte)

Nota: existe también una escala más granular usada en algunos materiales (0,0–0,1 sin correlación; 0,1–0,3 baja; 0,3–0,5 media; 0,5–0,7 alta; 0,7–1,0 muy alta). Para el examen, priorizar el criterio dado por la cátedra (umbral en 0,7) salvo que el enunciado indique otra escala.

**Correlación ≠ Causalidad:** un r alto solo indica asociación estadística, NO que una variable cause la otra. Ejemplo clásico: talla de zapato e inteligencia en una muestra que incluye niños y adultos — ambas aumentan con la edad (variable de confusión), pero no hay relación causal directa entre ellas.

**Diagrama de dispersión:** paso previo obligatorio antes de calcular r. Permite ver si la relación es lineal, curvilínea, si hay outliers, y si tiene sentido calcular Pearson (que solo mide relación lineal).

## Regresión lineal simple

**Modelo (recta de mínimos cuadrados / recta muestral):**

```
ŷ = a + b·x
```

- **ŷ**: valor predicho (estimado) de la variable dependiente.
- **x**: variable independiente o predictora.
- **b**: pendiente o coeficiente de regresión.
- **a**: ordenada al origen o constante de regresión.

**Método de mínimos cuadrados:** busca la recta que minimiza la suma de los cuadrados de los residuos (errores).

Propiedades de la recta de mínimos cuadrados:
1. La suma de los residuos es cero: Σ(y − ŷ) = Σe = 0
2. La suma de los cuadrados de los residuos es mínima: Σe² = Σ(y − ŷ)² = mínima
3. La recta pasa siempre por el punto (x̄, ȳ)

**Fórmulas de los coeficientes:**

```
b = Sxy / Sxx = (Σx·y − n·x̄·ȳ) / (Σx² − n·x̄²) = (n·Σxy − Σx·Σy) / (n·Σx² − (Σx)²)
```

También: `b = r · (Sy / Sx)` — relaciona directamente la pendiente con el coeficiente de correlación.

```
a = ȳ − b·x̄
```

**Interpretación en contexto:**
- **b (pendiente):** mide la variación promedio esperada de Y cuando X aumenta en una unidad. Ejemplo: si b = 2,15 (USD por °C), significa que por cada 1°C que sube la temperatura, las ganancias por ventas de helado aumentan en promedio 2,15 USD.
- **a (ordenada al origen):** mide el valor promedio esperado de Y cuando X = 0. Ejemplo: si a = 4,40, significa que cuando la temperatura es 0°C, el modelo predice ganancias promedio de 4,40 USD. Cuidado: esta interpretación solo tiene sentido si X = 0 está dentro (o cerca) del rango de datos observado.

**Observaciones importantes:**
- El signo de **b** siempre coincide con el signo de **r** (misma dirección de la relación).
- **Extrapolación:** usar la recta para predecir Y con valores de X fuera del rango observado es riesgoso. El riesgo aumenta cuanto más nos alejamos del rango de datos.

## Coeficiente de determinación (R²)

**Fórmula:**

```
r² = R² = (Sxy)² / (Sxx · Syy) = (Σx·y − n·x̄·ȳ)² / [(Σx² − n·x̄²) · (Σy² − n·ȳ²)]
```

**Rango:** 0 ≤ R² ≤ 1 (se expresa habitualmente como porcentaje, 0% a 100%)

**Interpretación:** mide el porcentaje de la variabilidad de Y que queda explicado por la recta de regresión (por la variable X).

- R² = 1 (100%) → ajuste perfecto, el modelo explica toda la variabilidad de Y.
- R² = 0 (0%) → el modelo no explica nada de la variabilidad; no hay relación en el modelo.
- Regla práctica de la cátedra: **R² > 0,5** indica un modelo con **buen ajuste** (aceptable). Aunque el umbral exacto puede variar según la disciplina.

**Relación con r:** R² es simplemente **r elevado al cuadrado** (r² = R²). Por eso R² siempre es positivo (no tiene signo, a diferencia de r que sí indica dirección).

## Ejemplo resuelto

**Caso: Ventas de helados y temperatura** (TP grupal - Equipo 1)

- **Variable independiente (X):** Temperatura ambiental (°C)
- **Variable dependiente (Y):** Ganancias por ventas de helado (USD)

**Pasos aplicados:**
1. Diagrama de dispersión → se observa una tendencia creciente clara y fuerte.
2. Ecuación de regresión obtenida: **Ganancias = 4,40 + 2,15 × Temperatura (°C)**
3. Coeficiente de correlación: **r ≈ 0,9884** → asociación lineal positiva y muy fuerte.
4. Coeficiente de determinación: **R² ≈ 0,9769 (97,70%)** → el 97,70% de la variación en las ganancias se explica por la variación de la temperatura; el 2,30% restante depende de otras variables (promociones, día de semana, etc.).

**Interpretación de los coeficientes:**
- Pendiente (2,15): por cada 1°C que aumenta la temperatura, las ganancias aumentan en promedio 2,15 USD.
- Ordenada (4,40): ganancia promedio estimada cuando la temperatura es 0°C.

Verificación de consistencia: r² = 0,9884² ≈ 0,9770, que coincide con el R² informado — confirma la relación r² = R².

## Trampas de examen multiple choice

1. **Confundir correlación con causalidad:** un r alto (incluso r = 1) NUNCA prueba causalidad, solo asociación. Buscar en el enunciado si hay una variable de confusión o si simplemente se afirma "por lo tanto X causa Y" — eso suele ser la opción incorrecta.
2. **Confundir r con R² (o r²):** son conceptos relacionados pero distintos. r mide fuerza y dirección (rango −1 a 1, tiene signo); R² mide el % de variabilidad explicada (rango 0 a 1, siempre positivo). Si preguntan por "bondad de ajuste", es R², no r.
3. **Mal interpretar el signo de la pendiente:** b negativo significa relación inversa (Y disminuye cuando X aumenta), NO que "no hay relación". Recordar que el signo de b siempre coincide con el signo de r.
4. **Confundir a y b:** a es el valor de Y cuando X = 0 (ordenada); b es el cambio promedio en Y por cada unidad de cambio en X (pendiente). Las opciones suelen intercambiar estas definiciones.
5. **Extrapolar sin advertencia:** usar la recta para predecir fuera del rango de X observado es un error metodológico, aunque matemáticamente se pueda calcular. Si el enunciado pide predecir con un X muy alejado de los datos, la respuesta correcta suele señalar el riesgo de extrapolación.
6. **Asumir que r = 0 implica "sin relación alguna":** r = 0 solo indica ausencia de relación LINEAL; podría existir una relación curvilínea fuerte que Pearson no detecta (por eso el diagrama de dispersión es el primer paso).
7. **Redondeo y contexto de la variable dependiente:** en variables discretas (ej. cantidad de victorias, personas, unidades), el resultado de la predicción debe interpretarse/redondearse según el sentido práctico de la variable, no solo matemáticamente.
8. **Umbral de "relación fuerte":** distintas fuentes usan distintos puntos de corte para |r| (0,5 vs 0,7). Verificar cuál usó la cátedra al resolver un ejercicio de clasificación de fuerza.

## Preguntas de autoevaluación

**1.** El coeficiente de correlación de Pearson (r) puede tomar valores en el rango:
a) 0 a 100
b) 0 a 1
c) −1 a 1
d) −∞ a +∞

**Correcta: c)** El coeficiente r está siempre acotado entre −1 y 1, sin excepción, independientemente de la escala de las variables originales.

**2.** Si al calcular la recta de regresión se obtiene b = −3,5, ¿qué se puede afirmar sobre el coeficiente de correlación r?
a) r será positivo
b) r será negativo
c) r será igual a cero
d) No se puede determinar el signo de r sin más datos

**Correcta: b)** El signo de b siempre coincide con el signo de r; si b es negativo, r también lo es (relación inversa).

**3.** Un estudio encuentra r = 0,85 entre el número de bomberos enviados a un incendio y el monto de los daños materiales. ¿Qué conclusión es correcta?
a) Enviar más bomberos causa mayores daños
b) Existe una fuerte asociación lineal positiva, pero no se puede concluir causalidad (probablemente ambas variables dependen del tamaño del incendio)
c) Se debería enviar menos bomberos para reducir daños
d) r = 0,85 indica una relación débil

**Correcta: b)** Es el ejemplo clásico de variable de confusión: el tamaño del incendio determina tanto la cantidad de bomberos enviados como los daños. Correlación no implica causalidad.

**4.** Si R² = 0,64, ¿cuál es el valor aproximado de r (asumiendo relación positiva)?
a) 0,64
b) 0,8
c) 0,41
d) 1,28

**Correcta: b)** R² es r al cuadrado, entonces r = √0,64 = 0,8 (tomando el signo positivo dado que la relación es directa).

**5.** En la ecuación ŷ = 12 + 4,5x que predice el gasto mensual (ŷ, en miles de pesos) en función de los años de antigüedad laboral (x), ¿qué representa el valor 12?
a) El gasto promedio cuando la antigüedad es de 12 años
b) El gasto promedio estimado cuando la antigüedad es 0 (recién ingresado)
c) La correlación entre las variables
d) El cambio en el gasto por cada año adicional de antigüedad

**Correcta: b)** 12 es la ordenada al origen (a): el valor esperado de Y cuando X = 0.

**6.** ¿Cuál de las siguientes afirmaciones sobre la recta de mínimos cuadrados es INCORRECTA?
a) La suma de los residuos (Σe) es igual a 0
b) La recta pasa siempre por el punto (x̄, ȳ)
c) Minimiza la suma de los residuos sin elevarlos al cuadrado
d) Minimiza la suma de los cuadrados de los residuos

**Correcta: c)** El método se llama "mínimos cuadrados" precisamente porque minimiza Σe² (la suma de los residuos al cuadrado), no la suma simple de los residuos (que siempre es 0 por construcción, sin necesidad de minimizarla).

**7.** Un modelo de regresión obtiene R² = 0,30. ¿Qué se puede afirmar?
a) Es un modelo excelente porque explica el 30% de algo
b) El modelo tiene un ajuste pobre: solo el 30% de la variabilidad de Y es explicada por X, quedando 70% sin explicar
c) r debe ser negativo
d) La correlación es perfecta

**Correcta: b)** Con el criterio de la cátedra (R² > 0,5 para ajuste aceptable), R² = 0,30 indica un ajuste débil/pobre; el 70% de la variación de Y depende de otros factores no incluidos en el modelo.

**8.** Se calculó la recta de regresión con datos de temperatura entre 5°C y 35°C. ¿Cuál es el principal riesgo de usar esa ecuación para predecir Y cuando X = 80°C?
a) Ninguno, la fórmula matemática sigue siendo válida igual
b) Extrapolación: se está prediciendo fuera del rango de datos observado, lo cual no garantiza que la relación lineal se mantenga
c) El valor de r cambiará automáticamente
d) Habría que recalcular a y b antes de predecir

**Correcta: b)** Extrapolar (predecir fuera del rango observado de X) es riesgoso porque no hay evidencia de que la relación lineal se sostenga fuera de ese rango; el riesgo crece cuanto más lejos se predice.

**9.** ¿Cuál de los siguientes pares de variables es más probable que tenga r ≈ 0 (sin correlación lineal)?
a) Horas de estudio y calificación en un examen
b) Temperatura ambiental y ventas de helado
c) Altura de una persona adulta y su talla de zapato
d) Mes de nacimiento y altura de una persona adulta

**Correcta: d)** No existe relación lógica ni estadística esperable entre el mes de nacimiento y la altura adulta; las otras opciones muestran relaciones lineales plausibles (positivas).

**10.** ¿Qué diferencia fundamental existe entre correlación y regresión?
a) Son exactamente lo mismo, solo cambia el nombre
b) La correlación mide la relación de forma simétrica y no direccional; la regresión modela una relación direccional (X predice Y) y permite hacer predicciones
c) La regresión solo se usa con variables cualitativas
d) La correlación siempre requiere calcular antes la recta de regresión

**Correcta: b)** La correlación es simétrica (no distingue variable independiente/dependiente) y solo mide fuerza/dirección; la regresión es asimétrica (X → Y) y construye un modelo predictivo.
