# Asistente simulado: «¿Qué tengo para hacer hoy?»

Un botón (en «Mi hogar» y en el panel del asistente) que **finge** una inteligencia artificial. Es un **guion con reglas** sobre los datos ficticios: no llama a ninguna API, no usa modelos de lenguaje y no aprende. Debe verse creíble pero **declararse simulado**.

## Cartel obligatorio

Visible siempre en el panel del asistente y repetido bajo cada respuesta, en letra pequeña pero legible:

> **Asistente simulado.** Las respuestas son guionadas a partir de datos ficticios y no usan inteligencia artificial real.

## Entradas

- **Botón principal:** «¿Qué tengo para hacer hoy?».
- **Respuestas rápidas** (chips): «¿Hay cortes en mi recorrido?», «¿Qué eventos hay cerca?», «¿Cómo está el subte?», «¿Cómo va mi reporte?».
- **Campo de texto libre (opcional):** se interpreta por palabras clave (ver reglas). Si no entiende, responde con el mensaje de límites (ver abajo).

## Comportamiento

1. Al pulsar, mostrar «Armando tu resumen…» durante **≤ 1 segundo** (con `aria-live="polite"`; sin animaciones fuertes; respetar `prefers-reduced-motion`).
2. Mostrar la respuesta como una **tarjeta** con secciones breves y, cuando corresponda, botones «Ver en el mapa» que centran el mapa y abren la ficha del elemento.
3. Mantener un historial corto de la conversación dentro de la página (sin guardar nada fuera del navegador).

## Reglas del resumen diario

El resumen se arma tomando, en este orden, los elementos de `avisos_hogar` (por `prioridad`) y completando con datos de otras capas. Cada bloque se incluye **solo si existe** el dato:

| Orden | Bloque | Fuente | Condición |
|---|---|---|---|
| 1 | **Antes de salir** | `cortes_transito` con `cerca_de = "escuela"` | Hay un corte activo (`inicio_hace_min > 0` y `fin_en_min > 0`) |
| 2 | **Transporte** | `subte.estado` | Estado distinto de «normal» |
| 3 | **Tu reporte** | reporte con `mio = true` | Cambió de estado respecto de la última vez |
| 4 | **Cerca de casa** | `eventos` con `inicio_en_min < 480` y distancia < 1 km a «Mi hogar» | Hay al menos uno |
| 5 | **Para después** | `eventos` con `inicio_en_min` entre 480 y 1500 | Opcional |
| 6 | **Ciclovías** | `ciclovias` con `estado` distinto de «habilitada» | Hay alguna |

## Ejemplo de respuesta completa (con los datos de `seed-data.json`)

> **Tu día en la zona** *(resumen guionado)*
>
> **Antes de salir.** Hay un corte parcial por obra cerca de la escuela. Podés salir 5 minutos antes o usar la calle paralela. [Ver en el mapa]
>
> **Transporte.** La línea D tiene demoras; la frecuencia estimada es de 9 minutos. Si tenés apuro, considerá otro medio.
>
> **Tu reporte.** El contenedor frente a la escuela ya fue enviado al área responsable. Te avisamos cuando lo tome. [Ver reporte]
>
> **Cerca de casa.** La feria de diseño de autor está en marcha, a pocas cuadras. Más tarde, a las 12:30 aprox., hay una presentación en un café del barrio *(el horario se calcula con la hora del navegador)*.
>
> **Ciclovías.** El tramo transversal está obstruido por un auto estacionado; si vas en bici, sumá unos minutos.
>
> *Asistente simulado. Las respuestas son guionadas a partir de datos ficticios y no usan inteligencia artificial real.*

## Ejemplos de respuestas rápidas

**«¿Hay cortes en mi recorrido?»**
> Sí: un corte parcial por obra afecta el tramo cerca de la escuela. Alternativa: usar la calle paralela (suma unos 5 minutos). Hay otro corte por una feria que no cruza tu recorrido. [Ver recorrido]

**«¿Qué eventos hay cerca?»**
> Ahora: feria de diseño de autor (ya empezó). En unas 2 horas y media: presentación de un nuevo blend en un café del barrio. Más tarde: firma de libros infantiles. Mañana: clase abierta en la plaza. *(Todos ficticios.)*

**«¿Cómo está el subte?»**
> La línea D tiene demoras por revisión técnica (dato ficticio). Frecuencia estimada: 9 minutos. Actualizado hace unos 8 minutos.

**«¿Cómo va mi reporte?»**
> «Contenedor en medio de la vereda» está **enviado al área responsable**. Próximo paso: te avisamos cuando el área lo tome. Siete personas confirmaron que sigue vigente.

## Reglas para el texto libre

Detectar por palabras clave (sin distinguir mayúsculas ni tildes):

| Palabras | Respuesta |
|---|---|
| «corte», «obra», «tránsito», «calle» | Respuesta de cortes |
| «evento», «hacer», «plan», «feria» | Respuesta de eventos |
| «subte», «línea d», «metro» | Respuesta de subte |
| «reporte», «reclamo», «estado» | Respuesta de «Mi reporte» |
| «bici», «ciclovía» | Respuesta de ciclovías |
| «hoy», «día», «resumen» | Resumen diario |

Si no coincide ninguna: «No tengo una respuesta para eso. Soy un asistente simulado y solo conozco los datos de ejemplo de esta demostración. Probá con: cortes, eventos, subte o tu reporte.»

## Tono y límites

- **Tono:** claro, cálido y sobrio. Frases cortas. Tuteo rioplatense moderado, coherente con el resto de la interfaz (puede ser «vos» o neutro, pero consistente).
- **Sin promesas:** no asegurar horarios exactos de organismos ni prometer soluciones; usar «estimado», «aproximado» y «dato ficticio» donde corresponda.
- **Sin datos personales:** no pedir nombre, teléfono ni dirección.
- **Sin consejos médicos, legales ni de seguridad personal.**
- **Sin publicidad:** los eventos de marcas aparecen como información de la zona, rotulados como ficticios; no se «recomiendan» marcas.
- **Transparencia:** el cartel «Asistente simulado» no puede cerrarse ni ocultarse.

## Implementación sugerida

- Una función `generarResumen(datos, ahora, hogar)` que devuelva una lista de bloques `{titulo, texto, acciones[]}`.
- Una función `responder(pregunta)` que clasifique por palabras clave y llame a la anterior o a respuestas específicas.
- Todo en JavaScript local, determinista a partir de los datos y la hora del navegador. Probar con 3 horas simuladas (mañana, mediodía, noche) para ver que los bloques cambian de forma coherente.
