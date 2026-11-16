# La notación de especialización de la cátedra: círculo y arco, no la d/o de Elmasri

El docente dijo que **especialización es clave** en el parcial del 24/09
("exclusiva o solapada, y la parte de exclusividad", `raw/PAUTAS_EXAMEN.md`), y que la
notación va **de memoria** porque no van a tener ERDPlus. Eso obligó a fijar exactamente
qué símbolos corrige la cátedra, leyendo las imágenes dentro del PPTX y no reconstruyendo
de memoria ni copiando de `Rta-TP-Farmacia.erdplus`, que tiene errores conocidos.

## Lo que se verificó

Fuente: **`raw/B Clase 2 Diseño Conceptual Udeci.pptx`**, imágenes extraídas del zip
(`ppt/media/image28–image32.png`) y leídas una por una.

1. **La notación es triángulo + círculo + arco.** El vínculo ISA es un triángulo apuntando
   hacia abajo. Sobre él se dibujan dos marcas independientes:
   - **Círculo** entre el supertipo y el triángulo → **total**. Sin círculo → **parcial**.
   - **Arco** cruzando las patas → **exclusiva**. Sin arco → **solapada**.

   Las reglas están escritas por el propio docente en los slides 25 y 26: *"Se grafica sin
   círculo"*, *"Se grafica con un círculo"*, *"se grafica con elipse"* (la "elipse" es el
   arco).

2. **El deck trae exactamente un ejemplo de cada una de las cuatro combinaciones**, lo cual
   es el mejor material didáctico posible:

   | Ejemplo | Combinación |
   |---|---|
   | Empleado_Restaurante → Camarero / Cocinero / Lava_platos | parcial + exclusiva |
   | Participantes_Película → Productor / Director / Actores | parcial + solapada |
   | Ficha → Ficha_autor / Ficha_tema | total + exclusiva |
   | Equipo_fútbol → Delantero / Defensa / Portero / Centrocampista | total + solapada |

3. **Vocabulario:** el docente dice **"exclusiva"**; Elmasri dice "disjunta". Es lo mismo.
   Usar la palabra del docente en la hoja.

4. **El patrón de justificación del docente**, que conviene imitar: total/parcial se
   argumenta hablando del **conjunto** ("sólo hay 2 tipos de fichas", "puede haber más
   empleados"); exclusiva/solapada se argumenta hablando de **un individuo** ("un empleado
   sólo realiza una tarea", "un jugador puede jugar de delantero y de defensor").

## La contradicción dentro del propio deck

El **slide 27** ("Simbología ISA · Total, Exclusiva") muestra Vehículo → Diesel / Nafta en
notación de **Elmasri**: línea doble para participación total, círculo con letra adentro y
símbolo de subconjunto (⊂) sobre cada pata. **No coincide con los slides 25 y 26.**

Decisión tomada: **dibujar la de los slides 25 y 26**. Razones: son los únicos slides con la
regla de dibujo escrita explícita, traen los cuatro casos completos, y es la notación con la
que está resuelto el TP1. La del slide 27 es una figura suelta del libro. Queda anotado en
la lección 0013 como advertencia, porque si el docente la usa en el enunciado hay que poder
leerla.

## La pregunta de conteo

Bruno reportó que el docente pide **contar registros del supertipo "contemplando todas las
posibilidades"**. Eso no aparece escrito en el deck; se dedujo de las restricciones y se
formalizó en la lección 0014:

|  | Exclusiva | Solapada |
|---|---|---|
| **Total** | `\|E\| = Σ nᵢ` | `máx(nᵢ) ≤ \|E\| ≤ Σ nᵢ` |
| **Parcial** | `\|E\| ≥ Σ nᵢ` | `\|E\| ≥ máx(nᵢ)` |

Regla mnemónica: **total da el máximo, exclusiva da el mínimo**. Sólo total + exclusiva
produce un número exacto. El error previsible es poner el mínimo en cero cuando es solapada:
el piso siempre es el subtipo más grande.

## Estado de ACID, de la misma sesión

Se le tomó ACID de memoria antes de empezar. Resultado: los cuatro nombres correctos,
aislamiento y consistencia bien definidos, y **un error de raíz repetido tres veces**:
definió atomicidad con la definición de *transacción* ("empieza y termina"), y por eso
invirtió atomicidad ↔ consistencia en dos casos de diagnóstico y atribuyó el ROLLBACK a la
consistencia. Después preguntó si `begin+rollback` "no es atómico" — se corrigió: el
rollback es la rama "nada" del todo-o-nada, o sea atomicidad **funcionando**. Lo que viola
la atomicidad es la tercera rama, la mitad aplicada que queda así.

Corregido en la sesión. La distinción operativa que le quedó: **atomicidad mira si la
transacción se completó; consistencia mira si el estado en que la dejó es válido.**

## Artefactos producidos

- `lessons/0013-especializacion-la-notacion-isa.html`
- `lessons/0014-contar-registros-del-supertipo.html`
- `reference/0004-notacion-der-a-mano.html` — hoja de símbolos imprimible
- `assets/diagrams/especializacion-cuatro-combinaciones.svg`
- `assets/diagrams/especializacion-conteo.svg`
- `assets/diagrams/notacion-der-simbolos.svg`

## Qué sigue

Quedan tres días y las prioridades que fijó Bruno: `0008` (atributo derivable, error nº1 del
docente — ya cubierto parcialmente en la referencia 0004), `0009` (unarias y binarias) y
`0016` (pasaje DER → relacional, que necesita para el ejercicio práctico). `0011`, `0012`,
`0015`, `0017` y `0018` probablemente no lleguen, y está bien: no son lo que el docente dijo
que toma.
