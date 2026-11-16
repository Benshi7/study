# Calculadora Casio fx-991EX (ClassWiz) — guía para el final de FEP

Fuente: *fx-570EX / fx-991EX Guía del usuario* (manual oficial en español, RJA532433-001V01). Las citas "p. N" son las páginas **impresas** del manual (la página N del PDF es la N+1). Todo lo marcado **[manual]** está escrito o mostrado en el manual; lo marcado **[no está en el manual]** es convención habitual o inferencia y conviene confirmarlo en pantalla antes del examen.

Notación de teclas: `[=]` es la tecla igual, `[▼]`/`[▲]` son el cursor, `[1]`…`[9]` son las teclas numéricas usadas para elegir ítems de menú. `SHIFT` y `OPTN` se escriben tal cual.

---

## 0. Resumen de una pantalla

| Quiero… | Modo | Función |
|---|---|---|
| x̄, s, σ, n, Σx, cuartiles de datos (con o sin frecuencia) | `MENU 6` Statistics → `[1]` 1-Variable | `OPTN 3` (1-Variable Calc) |
| Recta y = a + bx, r, ŷ, x̂ | `MENU 6` Statistics → `[2]` y=a+bx | `OPTN 4` (Regression Calc) |
| P(a < X < b), P(X > a), P(X < b) con Normal | `MENU 7` Distribution → `[2]` Normal CD | Lower, Upper, σ, μ |
| Valor x tal que P(X ≤ x) = área (percentil, Z de un IC) | `MENU 7` → `[3]` Inverse Normal | Area, σ, μ |
| P(X = k) Binomial / Poisson | `MENU 7` → `[4]` Binomial PD / `[▼][2]` Poisson PD | x, N, p / x, λ |
| P(X ≤ k) Binomial / Poisson | `MENU 7` → `[▼][1]` Binomial CD / `[▼][3]` Poisson CD | x, N, p / x, λ |
| nCr, n! | `MENU 1` Calculate | `SHIFT ÷` (nCr), `SHIFT x⁻¹` (x!) |
| Fracción ↔ decimal | cualquier cálculo | `S⇔D` |
| Student t (probabilidad o valor crítico) | **no existe** | usar la tabla t |

---

## 1. Preparación y configuración

### 1.1 Menú principal (p. 5) [manual]
`MENU` muestra 8 íconos numerados por pantalla: **1** Calculate, **2** Complex, **3** Base-N, **4** Matrix, **5** Vector, **6** Statistics, **7** Distribution, **8** Spreadsheet; con `[▼]` aparecen **9** Table, **A** Equation/Func, **B** Inequality, **C** Ratio. Se elige con el número (o con el cursor y `[=]`).

### 1.2 SETUP (pp. 6-8) [manual]
`SHIFT MENU` (SETUP), luego `[▼]`/`[▲]` para recorrer y el número del ítem.

| Ajuste | Teclas | Para qué |
|---|---|---|
| Input/Output | `SETUP 1` → `1` MathI/MathO (por defecto) · `2` MathI/DecimalO · `3` LineI/LineO · `4` LineI/DecimalO | `MathI/DecimalO` hace que los resultados salgan directo en decimal. |
| Number Format | `SETUP 3` → `1` Fix (decimales, 0-9) · `2` Sci · `3` Norm | `Fix 4` = 4 decimales; es redondeo de **pantalla**. |
| **Statistics (columna Freq)** | `SETUP [▼] 3` (Statistics) → `1` On / `2` Off | **On** agrega la columna `Freq` en el editor. |

Importante (p. 22): **cambiar el ajuste Statistics, salir del modo Statistics o cambiar entre 1 variable y 2 variables borra todos los datos del editor.** Por eso hay que activar `Freq` **antes** de cargar los datos.

### 1.3 Memoria y reinicio (pp. 2, 13, 45) [manual]
- **Ans**: guarda el último resultado. Se usa con la tecla `Ans`. En modo Distribution, el resultado queda en Ans salvo que se haya elegido `List` (p. 33).
- **Variables A-F, M, x, y**: `SHIFT RCL` (STO) + tecla de la variable guarda el resultado visible (el manual lo muestra con `3+5` → STO A). Se recuperan con `ALPHA` + tecla de la variable, o con `RCL`.
- Ans, M y variables **se mantienen** al apretar `AC`, cambiar de modo o apagar (p. 13).
- Reinicio (`SHIFT 9` = RESET): `1` Setup Data (vuelve la configuración a los valores de fábrica, p. 45) · `2` Memory (borra Ans/M/variables, p. 13) · `3` Initialize All (borra todo, p. 2). Cada uno pide confirmar con `[=]` (Yes). El orden 2 y 3 de este menú **[no está en el manual]**; el manual solo escribe los nombres.
- Para volver a cálculos aritméticos desde Statistics: `MENU 1` (p. 45).

---

## 2. Estadística de una variable (descriptiva)

### Cuándo la uso
Media, desvío, n, Σx, Σx², mínimo/máximo, cuartiles de una lista de datos, o de una **tabla de frecuencias** (valor + frecuencia). Para datos agrupados en intervalos, se carga la **marca de clase** como x y la frecuencia como Freq.

### Secuencia de teclas (pp. 21-23) [manual]
1. `SHIFT MENU [▼] 3` (Statistics) → `1` (On). *(Solo si hay tabla de frecuencias; para una lista simple se deja Off.)*
2. `MENU 6` (Statistics) → `[=]`.
3. En *Select Type*: `[1]` (1-Variable). Aparece el editor con columnas `x` y `Freq`.
4. Escribir cada valor de x con `[=]`; bajar con `[▼]`, pasar a la columna Freq con `[▶]` y escribir cada frecuencia con `[=]`. (El manual escribe la x de arriba hacia abajo y luego las frecuencias: `1=2=3=4=5=` `▼ ▶` `1=2=3=2=`).
5. `AC` → pantalla de cálculo estadístico. Para volver a editar los datos: `OPTN 3` (Data).
6. Ver todas las medidas: desde el editor `OPTN 3` (1-Variable Calc); desde la pantalla de cálculo `OPTN 2` (1-Variable Calc). Se recorre con `[▼]`.
7. Para usar un valor en una cuenta (p. ej. el CV): `AC`, `OPTN [▼] 2` (Variable) y la tecla del símbolo (en el manual, `x̄` es `OPTN [▼] 2` → `[1]`); `Σx`/`Σx²` están en `OPTN [▼] 1` (Summation, ítems 1-8); `min/máx/Q1/Med/Q3` en `OPTN [▼] 3` (Min/Max).

### Qué significa el resultado
La pantalla *1-Variable Calc* lista (el manual muestra las primeras seis líneas, p. 22): `x̄`, `Σx`, `Σx²`, `σ²x`, `σx`, `s²x`; y con `[▼]` siguen `sx`, `n`, `minX`, `Q1`, `Med`, `Q3`, `maxX` (orden de las últimas líneas **[no está en el manual]**; leer las etiquetas).

| Símbolo | Significado | Fórmula |
|---|---|---|
| `x̄` | media | Σ f·x / n |
| `σx` | desvío **poblacional** (divide por n) | √(Σ f(x−x̄)² / n) |
| `sx` | desvío **muestral** (divide por n−1) | √(Σ f(x−x̄)² / (n−1)) |
| `σ²x`, `s²x` | varianzas correspondientes | — |
| `n` | suma de las frecuencias (no la cantidad de filas) | Σ f |
| `Σx`, `Σx²` | suma de x y de x² ponderadas por Freq | — |
| `Q1`, `Med`, `Q3` | cuartiles de los datos tal como se cargaron | — |

### Trampas
- **σx vs sx**: la cátedra escribe **S** para el estadístico muestral y **σ** para el parámetro poblacional (`knowledge-base/02`, Red 2). En los materiales, el desvío "con calculadora" de una muestra se informa como S (p. ej. S = 8,5733 con n = 20 y t de 19 g.l.; S = 3,0101 en el TP1 con n = 200; no se pudo comprobar con los datos crudos cuál de las dos opciones de la calculadora produce cada valor). **Regla práctica:** los datos son una **muestra** (peso de paquetes, presión de pacientes, n elegidos) → `sx`. Solo si el enunciado dice que son **todos** los elementos de la población → `σx`. Esta regla es coherente con la convención de la cátedra, pero el criterio exacto no está escrito en `NOTES.md`; si un enunciado de múltiple opción da dos opciones que difieren solo en el 3.er decimal, mirar si dice "muestra" o "población".
- **Variable aleatoria discreta (tabla x, P(x))**: la calculadora no acepta probabilidades como frecuencias de forma documentada. Convertirlas a enteros (p. ej. P×100) y cargar eso como Freq; con la tabla completa de la distribución corresponde `σx` (es el desvío de **la variable**, E(X) = x̄). **[el uso de Freq decimal no está en el manual]**
- **Datos agrupados**: x̄ y σ salen **aproximados** (usan marcas de clase). `Q1/Med/Q3` de la calculadora **no** son los percentiles interpolados de la cátedra (Pk = LI + (kN/100 − Fa)/f · i) y la manera en que la calculadora define los cuartiles no figura en el manual. Para Me, Mo y percentiles de datos agrupados, usar la fórmula.
- **Freq olvidada**: sin la columna `Freq` hay que repetir los datos. Con `Freq` en On, olvidarse de escribir la frecuencia deja valores incompletos en la tabla.
- **CV**: `CV = (sx ÷ x̄) × 100`. Umbrales de la cátedra: ver `NOTES.md` (homogeneidad < 20 %).
- Se borra todo al salir del modo o al cambiar el tipo (p. 22).

### Ejemplo con salida
**Manual (p. 23):** x = {1, 2, 3, 4, 5}, Freq = {1, 2, 3, 2, 1} (es decir, los datos 1, 2, 2, 3, 3, 3, 4, 4, 5). `x̄ = 3` [manual].
Resto (verificado con Python): `n = 9`, `Σx = 27`, `Σx² = 93`, `σx = 1.154700538`, `sx = 1.224744871`, `σ²x = 1.3333…`, `s²x = 1.5`, `minX = 1`, `maxX = 5`.

**Tabla agrupada:** marcas de clase 31, 33, 35, 37, 39 con frecuencias 10, 30, 80, 60, 20.
`n = 200`, `Σx = 7100`, `Σx² = 252840`, `x̄ = 35.5`, `σx = 1.987460691`, `sx = 1.992448054`.
CV con sx: 1.992448 ÷ 35.5 × 100 = **5.61 %** (< 20 % → homogéneo).

**Variable aleatoria discreta:** X = 0, 1, 2, 3 con P = 0.1, 0.3, 0.4, 0.2. Cargar Freq = 10, 30, 40, 20: `n = 100`, `x̄ = 1.7` (= E(X)), `σx = 0.9` (= desvío de X, **no** `sx = 0.9045…`).

---

## 3. Regresión lineal y correlación

### Cuándo la uso
Cuando hay pares (x, y) y piden recta de regresión y = a + bx, correlación r, R² = r², o una predicción.

### Secuencia de teclas (pp. 21-24) [manual]
1. (Si quedó Freq en On: `SHIFT MENU [▼] 3` → `2` Off, para no tener columna de frecuencias.)
2. `MENU 6` (Statistics) → `[=]` → `[2]` (y = a + bx). El editor muestra `x` e `y`.
3. Cargar todos los x (cada uno con `[=]`), `[▼]` + `[▶]` para ir a la columna y, y cargar los y.
4. Desde el editor, `OPTN 4` (Regression Calc) muestra la recta con `a`, `b`, `r`.
5. Para leer un coeficiente en una cuenta: `AC`, `OPTN [▼] 4` (Regression), luego `[1]` a, `[2]` b, `[3]` r, `[4]` x̂, `[5]` ŷ, y `[=]`.
6. **Predicción de ŷ**: `AC`, escribir el valor de x, `OPTN [▼] 4` → `[5]` (ŷ), `[=]` (manual Ej. 4).
7. **Estimación de x̂**: `AC`, escribir el valor de y, `OPTN [▼] 4` → `[4]` (x̂), `[=]`.
8. Medias, desvíos y sumas de ambas variables: `OPTN 3` (2-Variable Calc) desde el editor; `Σxy`, `Σy`, `Σy²` están en `OPTN [▼] 1` (Summation).

### Qué significa el resultado
- `b` (pendiente): variación media de y por cada unidad que aumenta x.
- `a` (ordenada): valor estimado de y cuando x = 0 (solo tiene sentido si x = 0 está dentro del rango).
- `r`: correlación lineal, −1 ≤ r ≤ 1; el signo de r es el signo de b. `r² = R²` = proporción de la variación de y explicada por la recta.
- `ŷ`: valor estimado de y para el x dado.

### Trampas
- **x̂ no es la regresión de x sobre y.** La calculadora resuelve y = a + bx para x (el manual lo describe así, p. 23). Si el ejercicio pide "regresión de x sobre y", hay que intercambiar las columnas.
- Extrapolar fuera del rango de x no tiene respaldo, aunque la calculadora devuelva un número.
- `r` alto no prueba causalidad.
- Cambiar entre 1 variable y 2 variables **borra** los datos (p. 22). Cambiar entre tipos de regresión de 2 variables con `OPTN 1` (Select Type) no está descrito en el manual como operación que borre; **verificar en pantalla** antes de confiar en que los datos siguen.
- Elegir bien el tipo: `[2]` es lineal; `[4]` es logarítmica (mismo menú, p. 21). Una `r` rara y `a`, `b` raros suelen indicar tipo equivocado.

### Ejemplo con salida
Datos: x = 20, 22, 24, 27, 30, 33 (temperatura); y = 48, 53, 57, 66, 71, 80 (ventas).

| Resultado | Pantalla (aprox.) |
|---|---|
| `a` | −0.5819672131 |
| `b` | 2.426229508 |
| `r` | 0.9976854256 |
| `r²` (R²) | 0.9953762 (99,54 % explicado) |
| `ŷ` para x = 25 | 60.07377049 |
| `x̂` para y = 60 | 24.96959459 |

Lectura: por cada 1 °C más, las ventas suben ≈ 2,43 unidades; correlación lineal positiva muy fuerte.
En 2-Variable Calc: `n = 6`, `x̄ = 26`, `ȳ = 62.5`, `sx = 4.939635614`, `sy = 12.0124935`, `σx = 4.50924975`, `σy = 10.9658561`, `Σx = 156`, `Σx² = 4178`, `Σy = 375`, `Σy² = 24159`, `Σxy = 10046`.

**Control con el manual (p. 23-24):** regresión logarítmica (20, 3150), (110, 7310), (200, 8800), (290, 9310) con Fix 3 → `r = 0.998`, `a = −3857.984`, `b = 2357.532`; `ŷ(160) = 8106.898`. Verificado con Python.

---

## 4. Distribución Normal: Normal PD y Normal CD

### Cuándo la uso
- **Normal CD**: probabilidades de intervalos o colas, P(a < X < b), P(X > a), P(X < b). Es lo que reemplaza la tabla Z.
- **Normal PD**: altura de la curva f(x). Casi nunca se pide en el final (la probabilidad de un punto es 0 en una variable continua).

### Secuencia de teclas (pp. 32-34) [manual]
1. `MENU 7` (Distribution) → `[=]`.
2. `[2]` (Normal CD).
3. Pantalla de variables (el manual muestra, para Normal PD, los valores por defecto `x:0, σ:1, μ:0`): para **Normal CD** los campos son **Lower, Upper, σ, μ**. Escribir cada valor con `[=]`.
4. Un `[=]` final calcula (en el manual, tras `36 = 2 = 35 =` se aprieta `[=]` para ver el resultado).
5. De la pantalla de resultado, `[=]` o `AC` vuelven a la pantalla de variables. Para cambiar de tipo de distribución: `OPTN 1` (Select Type).
6. El resultado queda en `Ans` (p. 33).

### Qué significa el resultado
Normal CD devuelve P(Lower < X < Upper) = área bajo la curva entre los dos límites (etiqueta `p=`; la calculadora puede mostrar también los límites estandarizados `z:Low`/`z:Up` **[no está en el manual]**). Normal PD devuelve la densidad en x (etiqueta `p=`; manual: 0.1760326634 para x=36, σ=2, μ=35).

### Trampas
- **Colas infinitas**: para P(X > a) escribir `Lower = a`, `Upper = 1E99` (tecla `×10ˣ`: `1 [×10ˣ] 99`). Para P(X < b), `Lower = −1E99` (`(−) 1 [×10ˣ] 99`), `Upper = b`. El uso de ±1E99 es la convención habitual **[no está en el manual]**; alternativa segura: usar μ ± 10σ como límite.
- **Los campos recuerdan lo último que se usó** (el manual lo indica para N y p en Binomial, p. 34): antes de calcular, revisar los **cuatro** campos. El error típico es dejar σ o μ de un ejercicio anterior.
- **Orden de campos**: σ va **antes** que μ (Normal PD: x, σ, μ; Normal CD: Lower, Upper, σ, μ, p. 33). Invertirlos es un error frecuente.
- Se ingresa el **desvío σ**, no la varianza σ².
- Para la **distribución muestral** hay que ingresar el **error estándar**: σ/√n, no σ (ver sección 6).
- Se puede ingresar μ = 0 y σ = 1 (valores por defecto) para trabajar directamente con Z.
- Precisión: "hasta seis dígitos significativos" (p. 33), aunque se muestren más dígitos. No comparar la 7.ª cifra con las opciones.
- `P(X = a)` en continua es 0; Normal PD **no** es una probabilidad.

### Ejemplo con salida
X ~ N(μ = 100, σ = 15).

| Pregunta | Campos | Resultado |
|---|---|---|
| P(85 < X < 120) | Lower = 85, Upper = 120, σ = 15, μ = 100 | `p = 0.750134` |
| P(X > 120) | Lower = 120, Upper = 1E99 | `p = 0.0912112` |
| P(X < 85) | Lower = −1E99, Upper = 85 | `p = 0.158655` |
| f(105) (Normal PD) | x = 105, σ = 15, μ = 100 | `p = 0.0251589` |

Con Z directamente (σ = 1, μ = 0): P(−0.5 < Z < 1.2) → `0.576393`.

---

## 5. Normal inversa (percentiles y Z de intervalos)

### Cuándo la uso
- Dado un área (probabilidad) hallar el valor: percentiles, "el 10 % superior", Z crítico para IC (1,96; 1,645; 2,576).
- Búsqueda de parámetros (dos percentiles → μ y σ): una consulta por cada percentil.

### Secuencia de teclas (p. 32-33) [manual]
`MENU 7` → `[=]` → `[3]` (Inverse Normal) → escribir **Area**, **σ**, **μ** (cada uno con `[=]`) → `[=]`.
El resultado es el valor x tal que **P(X ≤ x) = Area**. El manual indica: **"ajuste de cola siempre a la izquierda"** (p. 33): no se puede elegir cola derecha ni central.

### Qué significa el resultado
Es un valor de la variable (x, o Z si σ = 1 y μ = 0). Rango de Area: 0 ≤ Area ≤ 1 (p. 33).

### Trampas
- **Siempre cola izquierda.** Para "el 10 % superior" hay que ingresar `Area = 0.90`, no 0.10. Para P(X > x) = 0.05 → `Area = 0.95`.
- **Z de un IC al nivel (1−α)**: usar `Area = 1 − α/2` (95 % → 0.975; 90 % → 0.95; 99 % → 0.995), con σ = 1, μ = 0. Si se ingresa 0.95 para un IC al 95 % se obtiene 1.645 (el valor del 90 %).
- Con σ y μ de la variable, el resultado ya viene en unidades originales (no hace falta des-estandarizar).
- Es una función inversa: no devuelve probabilidades.

### Ejemplo con salida
| Pedido | Campos | Resultado |
|---|---|---|
| Z para IC al 95 % | Area = 0.975, σ = 1, μ = 0 | `1.95996` (exacto 1.959963985) |
| Z para IC al 90 % | Area = 0.95 | `1.64485` |
| Z para IC al 99 % | Area = 0.995 | `2.57583` |
| Corte del 10 % superior de N(100, 15) | Area = 0.90, σ = 15, μ = 100 | `119.223` |
| Primer cuartil de N(100, 15) | Area = 0.25 | `89.8827` |

---

## 6. Distribución muestral de la media y de la suma

### Cuándo la uso
Preguntas sobre un **promedio de muestra** x̄ (distribución muestral, TCL) o sobre una **suma** W de n variables. Se usa Normal CD con los parámetros de x̄ o de W.

### Secuencia de teclas
1. Calcular los parámetros con la calculadora en `MENU 1`: error estándar σ/√n (promedio) o σ√n (suma). Guardarlo con `SHIFT RCL` (STO) + variable, o escribirlo directamente.
2. `MENU 7` → `[2]` Normal CD.
3. **Promedio**: σ = σ/√n, μ = μ. **Suma**: μ = nμ, σ = σ√n.

### Qué significa el resultado
Probabilidad sobre el **promedio** (o la suma), no sobre una observación individual.

### Trampas
- Ingresar σ (el de la variable) en vez de σ/√n: error clásico. Se detecta porque da una probabilidad demasiado cercana a la de un individuo.
- Suma: μ_W = nμ y σ_W = √n·σ (**no** σ/√n); promedio: μ y σ/√n.
- El TCL requiere n ≥ 30 si la población no es normal (convención de la cátedra, `knowledge-base/04`).

### Ejemplo con salida
**Promedio:** μ = 50, σ = 12, n = 36 → σ_x̄ = 12/√36 = 2.
P(x̄ > 52): Lower = 52, Upper = 1E99, σ = 2, μ = 50 → `p = 0.158655`.
*(Con el error σ = 12 se obtendría 0.433816: otro número, otra opción de múltiple opción.)*

**Suma:** 50 días, μ = 5, σ = 2 por día → μ_W = 250, σ_W = 2√50 = 14.1421.
P(W > 260): Lower = 260, Upper = 1E99, σ = 14.1421, μ = 250 → `p = 0.239750`.

---

## 7. Intervalo de confianza para la media (Z y t)

### Cuándo la uso
La calculadora **no tiene un modo de intervalos de confianza**. Se usa para: obtener x̄ y sx de los datos (sección 2), obtener Z (sección 5), y hacer la aritmética de x̄ ± E con E = Z·σ/√n o E = t·s/√n.

### Secuencia de teclas
**σ conocido (Z):**
1. `MENU 7` → `[3]` Inverse Normal: Area = 1 − α/2, σ = 1, μ = 0 → resultado (queda en Ans).
2. `MENU 1`: `Ans × σ ÷ √n` (`√` es la tecla `√▪`; cerrar paréntesis si hace falta) → E. Luego x̄ − E y x̄ + E.

**σ desconocido (t):**
1. Obtener x̄ y **sx** de los datos (`MENU 6`, sección 2), y n.
2. **Buscar t en la tabla** con ν = n − 1 y α/2 (la calculadora no lo calcula, ver abajo).
3. `MENU 1`: E = t × sx ÷ √n; luego x̄ ± E.

### Qué significa el resultado
E es el margen de error; el IC es (x̄ − E; x̄ + E). Amplitud del IC = 2E. Con una confianza del 95 %, el **procedimiento** captura a μ en el 95 % de las muestras (no es "el 95 % de los datos").

### Trampas
- **No existe la distribución t en la fx-991EX** (ver sección 12). No hay forma de calcular t crítico ni P(T < t) con la calculadora.
- Usar `sx` (no `σx`) para el desvío cuando σ es desconocido.
- ν = n − 1 (no n) para entrar a la tabla t.
- Si el enunciado da σ poblacional → Z; si da un desvío calculado de la muestra → t, aunque n sea grande (convención de la cátedra, `knowledge-base/04`).
- Usar `Area = 0.95` en vez de `0.975` para un IC bilateral al 95 %.

### Ejemplo con salida
**Z:** x̄ = 82.4, σ = 9, n = 36, confianza 95 %.
Inverse Normal (Area = 0.975) → `1.95996`. Luego `Ans × 9 ÷ √36` → `E = 2.93994`. IC = (79.46; 85.34).

**t (valor de tabla):** x̄ = 50.35, s = 8.5733, n = 20 (examen de la cátedra), t₁₉;₀,₀₂₅ = 2.093 (tabla).
`E = 2.093 × 8.5733 ÷ √20 = 4.01238` → IC = (46.34; 54.36).

---

## 8. Proporción y tamaño de muestra

### Cuándo la uso
- IC para la proporción: p̂ ± Z·√(p̂q̂/n).
- Tamaño de muestra: n = (Z·σ/E)² (media, σ conocido) o n = Z²·p̂q̂/E² (proporción).
Son **cuentas aritméticas** con Z de Inverse Normal.

### Secuencia de teclas
1. Z con Inverse Normal (Area = 1 − α/2).
2. En `MENU 1`: IC proporción: `Z × √(p̂ × (1 − p̂) ÷ n)`. Tamaño de muestra: `(Z × σ ÷ E)` y elevar al cuadrado con `x²`.
3. **Redondear n siempre hacia arriba.**

### Qué significa el resultado
E = margen de error. n = cantidad **mínima** de observaciones para lograr el margen E con la confianza dada.

### Trampas
- **n se redondea siempre hacia arriba** (138,29 → 139; 150,06 → 151), nunca al más cercano.
- Sin estimación previa de p, usar p̂ = 0.5 (peor caso).
- Con σ desconocido el tamaño de muestra requiere iteración con t (la calculadora no ayuda con t).
- E es el **semi-ancho** del intervalo, no el ancho total.

### Ejemplo con salida
**Proporción:** p̂ = 0.30, n = 200, 95 %: `E = 1.95996 × √(0.3 × 0.7 ÷ 200) = 0.0635101`; IC = (0.2365; 0.3635).
**Tamaño de muestra (media):** σ = 12, E = 2, 95 %: `(1.95996 × 12 ÷ 2)² = 138.2925` → **n = 139**.
**Tamaño de muestra (proporción, peor caso):** E = 0.03, p̂ = 0.5: `1.95996² × 0.25 ÷ 0.03² = 1067.07` → **n = 1068**.

---

## 9. Binomial (Binomial PD y Binomial CD)

### Cuándo la uso
X = número de éxitos en n ensayos independientes con probabilidad p constante.
- **Binomial PD** → P(X = k).
- **Binomial CD** → P(X ≤ k) (acumulada; el manual la llama "distribución acumulada binomial" y no explicita el sentido, p. 32; el sentido "hasta k inclusive" es la convención habitual **[no está en el manual]**: control rápido, `CD(x = N)` debe dar 1).

### Secuencia de teclas (pp. 32-34) [manual]
1. `MENU 7` → `[=]`.
2. Elegir tipo: `[4]` Binomial PD, o `[▼][1]` Binomial CD.
3. Elegir método: `[1]` List (varios x a la vez) o `[2]` Variable (un solo x).
4. **Variable**: ingresar `x`, `N`, `p` (cada uno con `[=]`), luego `[=]`.
5. **List**: escribir los x de la lista (cada uno con `[=]`), `[=]`, luego `N` y `p`, `[=]`. Devuelve la columna P con un resultado por cada x (hasta 45 valores, p. 33).
6. Con Variable, el resultado queda en `Ans` → permite `1 − Ans`.
7. Para cambiar de tipo: `OPTN 1` (Select Type).

### Qué significa el resultado
`p=` es la probabilidad pedida (PD: exacta en k; CD: acumulada hasta k).

### Trampas
- **Traducir el enunciado a acumuladas** (CD = P(X ≤ k)):

| Enunciado | Cuenta |
|---|---|
| P(X = k) | PD(k) |
| P(X ≤ k), "como máximo k" | CD(k) |
| P(X < k) | CD(k − 1) |
| P(X ≥ k), "al menos k" | 1 − CD(k − 1) |
| P(X > k), "más de k" | 1 − CD(k) |
| P(a ≤ X ≤ b) | CD(b) − CD(a − 1) |

- "Al menos uno": 1 − PD(0) (equivale a 1 − CD(0)).
- **Pantalla de lista**: muestra 4 decimales y, en el ejemplo del manual (p. 34), los muestra **truncados, no redondeados** (0.12677… aparece como 0.1267; 0.06338… como 0.0633). Para una respuesta precisa usar el modo Variable.
- Los campos N y p se **conservan** del cálculo anterior (p. 34): reingresarlos siempre.
- Variable → x debe ser entero 0 ≤ x ≤ N; fuera de rango da `ERROR` (p. 34).
- Verificar que sea Binomial: n fijo, ensayos independientes, p constante. Si hay muestreo sin reposición de población chica, no lo es.
- Esperanza y varianza: np y npq (cuenta aparte, no las da el modo Distribution).

### Ejemplo con salida
X ~ Bin(N = 10, p = 0.3).

| Pregunta | Función | Campos | Resultado |
|---|---|---|---|
| P(X = 3) | Binomial PD | x = 3, N = 10, p = 0.3 | `p = 0.266828` |
| P(X ≤ 3) | Binomial CD | x = 3 | `p = 0.649611` |
| P(X ≥ 4) | `1 − CD(3)` | `1 − Ans` | `0.350389` |
| P(X < 3) | `CD(2)` | x = 2 | `0.382783` |
| P(2 ≤ X ≤ 5) | `CD(5) − CD(1)` | dos corridas | `0.803343` |
| P(al menos 1) | `1 − PD(0)` | x = 0 | `0.971752` |

Tabla List de PD para x = 0, 1, 2, 3: columna P ≈ 0.0282, 0.1211, 0.2335, 0.2668 (se verá con 4 decimales).
**Control del manual (p. 34):** N = 15, p = 0.6, x = {10, 11, 12, 13} → P = 0.1859, 0.1267, 0.0633, 0.0219.

**Combo Normal → Binomial:** si p = P(X > 120) = 0.0912112 (Normal CD, guardar con STO A) y se toman 5 elementos, P(al menos uno supera 120) = `1 − PD(x = 0, N = 5, p = A)` = `0.380110`.

---

## 10. Poisson (Poisson PD y Poisson CD)

### Cuándo la uso
X = número de eventos en un intervalo (tiempo, área, longitud) con tasa media constante λ.

### Secuencia de teclas (pp. 32-34) [manual]
1. `MENU 7` → `[=]`.
2. `[▼][2]` Poisson PD, o `[▼][3]` Poisson CD.
3. Método: `[1]` List o `[2]` Variable.
4. Campos: **x**, **λ** (solo dos). Cada uno con `[=]`, luego `[=]`.

### Qué significa el resultado
PD: P(X = k). CD: P(X ≤ k) (mismo criterio que en binomial **[sentido no explicitado en el manual]**).

### Trampas
- **Escalar λ al intervalo pedido**: si la tasa es 3 por hora y piden 2 horas, λ = 3 × 2 = 6 (convención de la cátedra, `NOTES.md`). Si cambia la ventana de tiempo, cambia λ.
- Mismas conversiones que en binomial: P(X ≥ k) = 1 − CD(k − 1); P(X < k) = CD(k − 1); P(X > k) = 1 − CD(k).
- Para Poisson, E(X) = Var(X) = λ.
- No hay campo N ni p; si el problema los tiene, es binomial.

### Ejemplo con salida
Tasa 3 por hora, ventana 2 h → λ = 6.

| Pregunta | Función | Campos | Resultado |
|---|---|---|---|
| P(X = 4) | Poisson PD | x = 4, λ = 6 | `p = 0.133853` |
| P(X ≤ 4) | Poisson CD | x = 4, λ = 6 | `p = 0.285057` |
| P(X ≥ 5) | `1 − CD(4)` | `1 − Ans` | `0.714943` |
| P(X = 0) | Poisson PD | x = 0, λ = 6 | `0.00247875` |

---

## 11. Herramientas auxiliares

### Combinaciones, permutaciones y factorial (p. 17) [manual]
- nCr: `10 SHIFT ÷ (nCr) 4 [=]` → `210`.
- nPr: `10 SHIFT × (nPr) 4 [=]` → `5040`.
- n!: `5 SHIFT x⁻¹ (x!) [=]` → `120` (manual: `(5+3)!` → `40320`).

### Fracciones y decimales (pp. 5-6, 10-11, 45) [manual]
- Con la configuración por defecto (MathI/MathO), los cocientes salen como fracción. Para pasar a decimal: tecla `S⇔D` mientras se muestra el resultado (FAQ, p. 45).
- Para que salgan siempre en decimal: `SHIFT MENU 1` (Input/Output) → `2` (MathI/DecimalO).
- Para pasar a Fix de N decimales: `SHIFT MENU 3` (Number Format) → `1` (Fix) → N.
- Fracción impropia ↔ mixta: el manual la menciona en p. 11 pero la tecla no se lee en el texto extraído; ver el manual impreso o la leyenda sobre la tecla `S⇔D`.

### Memoria y Ans
Ver sección 1.3. Uso típico: `Binomial CD` → `1 − Ans`; Inverse Normal → `Ans × σ ÷ √n`; guardar λ, σ_x̄ o p en una variable con `SHIFT RCL` (STO) y reutilizarla con `ALPHA` + variable.

### Modo Table (pp. 28-29) [manual]
`MENU 9` (Table): genera una tabla f(x) (y opcionalmente g(x)) para un rango Start / End / Step. Para una binomial completa: `f(x) = 10 nCr x × 0.3^x × 0.7^(10−x)` con Start 0, End 10, Step 1; devuelve P(X = 0)…P(X = 10) (0.0282, 0.1211, 0.2335, 0.2668, 0.2001, 0.1029, 0.0368, 0.0090, 0.0014, 0.0001, 0.0000). **[el armado de f(x) con nCr no está en el manual; control: valores de la tabla de Binomial PD]**. Útil para ver toda la distribución de golpe; no es necesario para el examen.

### Normal dentro de Statistics (p. 24)
En 1-Variable, `OPTN [▼] 4` (Norm Dist) ofrece `P(t)`, `Q(t)`, `R(t)` y `▸t`. **`▸t` estandariza usando x̄ y σx (poblacional)** de los datos cargados: es x̄ y σ **calculados**, no los del enunciado. Mejor usar Distribution con los parámetros del enunciado.

---

## 12. Qué NO hace la calculadora

- **No tiene distribución t de Student.** El modo Distribution ofrece **exactamente siete tipos**: Normal PD, Normal CD, Inverse Normal, Binomial PD, Binomial CD, Poisson PD, Poisson CD (manual, p. 32-33, "siete tipos distintos de cálculos de distribución"). No hay t, χ² ni F. Los valores críticos t y los p de pruebas con t salen de la **tabla t** (con ν = n − 1).
- No elige la distribución: decidir Binomial vs. Poisson vs. Normal, y Z vs. t, es parte del ejercicio.
- No decide si usar σ/√n, ni escala λ, ni traduce "al menos / más de / a lo sumo" a la acumulada correcta.
- No calcula IC, tamaño de muestra ni R²: son cuentas con los resultados de otras funciones.
- No interpreta r, b, E ni el IC.
- No calcula percentiles interpolados de datos agrupados (Pk) ni Mo/Me de una tabla de intervalos; para eso es la fórmula de la cátedra. Los cuartiles de la calculadora son sobre los datos cargados.
- No avisa si los datos no son lineales (r alto no implica linealidad).
- No da cola derecha en Inverse Normal (siempre izquierda).
- Normal PD, Binomial PD y Poisson PD no acumulan: hay que sumar o usar CD.

---

## 13. Control rápido de plausibilidad (antes de marcar)

1. ¿Una probabilidad entre 0 y 1? Si da > 1, revisar si se cargó λ, p o σ mal.
2. Normal CD sobre un promedio: ¿σ/√n? El resultado de una cola debe ser **menor** que el del individuo.
3. Inverse Normal: ¿el Z de IC al 95 % da 1.96? Si da 1.645, se usó 0.95 en vez de 0.975.
4. Binomial: `CD(N)` = 1.
5. Estadística: ¿`sx` > `σx`? Siempre es mayor (factor √(n/(n−1))).
6. ¿Sigue la columna Freq en On cuando se carga una lista simple (o a la inversa)?
7. Recordar que `Ans` solo se actualiza con un cálculo nuevo; si se editó un dato sin recalcular, el `Ans` es viejo.

---

## 14. Índice de páginas del manual citadas

| Tema | Página impresa (PDF = +1) |
|---|---|
| Inicializar / Initialize All | 2 |
| Menú de modos | 5 |
| SETUP (Input/Output, Number Format, Statistics) | 6-8 |
| Fracciones, S⇔D | 10-11 |
| Ans, variables, memoria, borrado | 13 |
| nCr, nPr, x! | 17 |
| Cálculos estadísticos (editor, Freq, 1-Variable, regresión, ŷ, x̂) | 21-24 |
| Table | 28-29 |
| Distribución (7 tipos, campos, lista, ejemplos) | 32-34 |
| FAQ (S⇔D, RESET Setup Data, Ans) | 45 |
