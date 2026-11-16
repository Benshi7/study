"""Renders 07-formato-entrega.md: one document, one style, a 2-day plan."""
import pathlib

import data as D
from fmt import ars, n, table, usd

ROOT = pathlib.Path(__file__).resolve().parent.parent

CONSIGNA = ["Carátula", "Índice", "Canvas del proyecto", "Aplicar Design Thinking", "Project Charter",
            "Gantt del proyecto completo", "Matriz de stakeholders", "Plan de comunicación",
            "Gestión de riesgos - Matriz de riesgos", "Gestión de costos - Presupuesto"]

CHECKLIST = [
    "Un solo archivo con los 10 puntos, en el orden de la consigna.",
    "Carátula única, con el nombre del proyecto unificado y una sola nómina del equipo.",
    "Índice automático actualizado (actualizar campos) justo antes de exportar.",
    "Títulos con los estilos del procesador de texto, no con negritas manuales; puntos numerados del 1 al 10.",
    "Misma fuente, tamaño e interlineado en todo el documento (venía de tres fuentes distintas).",
    "Todas las tablas con el mismo estilo, encabezado repetido y sin filas partidas entre páginas.",
    "Pie de tabla y pie de figura numerados por punto (Tabla 9.1, Figura 6.1) y citados en el texto.",
    "Cada punto abre con su frase puente; ninguna sección empieza «en seco».",
    "Una sola moneda (USD), con tipo de cambio, fecha y fuente declarados en las secciones 5 y 10.",
    "Fechas en formato dd/mm/aaaa y porcentajes con coma y espacio (12,1 %) en todo el documento.",
    "Mismos nombres de roles, stakeholders y áreas en todas las secciones.",
    "IDs únicos y coincidentes: G1–G8, R01–R19 y actividades 1–40 iguales en Charter, Gantt, riesgos y presupuesto.",
    "Los 7 controles de coherencia pasan (hitos, presupuesto, riesgos, contingencia, mano de obra, stakeholders, frases puente).",
    "El presupuesto total se cita igual en el Charter, en la sección 10 y en la conclusión.",
    "Sin restos internos: notas de chat, «Resumen y borrador», títulos con errores de tipeo.",
    "Sin texto de otro color, resaltados ni comentarios de revisión pendientes.",
    "Gantt legible (página apaisada, resolución suficiente, leyenda) con el camino crítico marcado.",
    "Supuestos declarados: simulación de fechas, tipo de cambio, Ley 25.326 y BAX/miBA «a confirmar».",
    "Numeración «Página X de Y», sin páginas en blanco ni títulos huérfanos al pie.",
    "Exportado a PDF y revisado página por página: se ven tablas e imágenes y abre bien en otro equipo.",
]

PAGES = [
    ["1 · Carátula", "1", "Única; nómina completa"],
    ["2 · Índice (+ apertura)", "1,5", "Índice automático + 5 líneas de apertura (frase puente de apertura)"],
    ["3 · Canvas del proyecto", "2–3", "Opción B, las dos propuestas de valor, segmento y personas"],
    ["4 · Aplicar Design Thinking", "2", "Solo lo hecho; hipótesis a validar si no hay evidencia"],
    ["5 · Project Charter", "2–3", "Charter condensado; el texto largo va como Anexo A"],
    ["6 · Gantt del proyecto completo", "3–4", "Tabla de actividades + diagrama apaisado + camino crítico"],
    ["7 · Matriz de stakeholders", "2", "Matriz poder/interés + lista única"],
    ["8 · Plan de comunicación", "2", "Matriz con una fila por stakeholder de la sección 7"],
    ["9 · Gestión de riesgos", "3–4", "Registro con P×I, EMV y respuestas"],
    ["10 · Gestión de costos", "4–5", "Desglose, reservas, curva S, cómo se construyen los números"],
    ["Cierre", "0,5", "Frase de cierre que vuelve a la pregunta inicial"],
    ["Anexos", "según contenido", "A Charter ampliado · B Gantt en Excel (referencia) · C desglose del presupuesto línea por línea"],
]


def write(rel, text):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text.strip() + "\n", encoding="utf-8")


def render(c):
    o = c["o"]
    fx = o["fx"]
    lb = c["lb"]
    order = "\n".join(f"{i}. {t}" for i, t in enumerate(CONSIGNA, 1))
    bridges = [[("Apertura" if k == "apertura" else "Cierre" if k == "cierre" else k), v] for k, v in D.BRIDGES.items()]
    roles = ", ".join(r[1] for r in D.TEAM_ROLES)
    glossary = [
        ["Nombre del proyecto", "«Modernización del Mapa Interactivo de la Ciudad»", "«…y Ampliación…», «Mapa v4.1» como nombre"],
        ["Segmento", "«Hogares de la Ciudad»", "«vecinos», «ciudadanos» como sinónimos del segmento"],
        ["Perfil de hogar", "«perfil de hogar básico» (dato mínimo, opt-in)", "«perfil personal», «perfil avanzado» sin aclarar"],
        ["Gates", "G1–G8 (uno por fase)", "«hito 4», «gate 4» con otro significado"],
        ["Riesgos", "R01–R19 (IDs del documento largo + nuevos)", "R01–R04 del resumen con otro significado"],
        ["Actividades", "1–40 (numeración del Gantt)", "Nombres distintos para la misma actividad"],
        ["Roles", roles, "«devs», «analistas» sin el nombre completo"],
        ["Stakeholders", "Los 15 nombres de la matriz de stakeholders", "Roles sueltos del Charter que no están en la matriz"],
        ["Escenario de presupuesto", "«Escenario B (recomendado)» o «Escenario A»", "Cifras de los dos escenarios mezcladas"],
        ["Moneda", f"USD; «ARS … M» solo como referencia", "«$» sin moneda"],
    ]
    txt = f"""
# Formato y entrega: un solo documento, con el mismo estilo de punta a punta

> **Propuesta.** Responde a la devolución del Prof. Armando (*«mejorar el orden de los puntos, el formato, prolijidad»*) y a la pregunta de una compañera sobre si el trabajo va junto o por separado. **La entrega final es el 14/10/2026: quedan 2 días** (hoy 12/10). Ningún original fue modificado; no se genera todavía el archivo Word (se puede hacer después).

## Respuesta a la pregunta: ¿Word o PDF, junto o por separado?

La consigna dice textualmente: *«Documento conteniendo los siguientes puntos: 1. Carátula … 10. Gestión de costos - Presupuesto»* y agrega: *«no deben ser puntos sueltos, el documento debe contener un storytelling dando continuidad y conexión entre los puntos»*. Por lo tanto:

- **Va un solo documento** con los 10 puntos, en ese orden, y con una historia que los conecte. Los archivos separados fueron la entrega parcial y los profesores respondieron sobre ellos, pero **no cumplen lo que pide la consigna para la entrega final**.
- **Formato de archivo:** la consigna **no lo especifica** (no dice Word ni PDF). Recomendación: armarlo en Word (o Google Docs) y entregar el **PDF** como versión final, porque conserva el formato; tener el `.docx` a mano por si lo piden. Si el equipo quiere **certeza**, conviene **confirmar por mail** con los profesores (hay un texto listo más abajo).
- **El Gantt en Excel:** el cronograma tiene que aparecer **dentro del documento** (punto 6, como tabla o imagen). El Excel va como **anexo o adjunto de apoyo**, no como reemplazo.
- **El Charter largo:** como **Anexo A** al final del mismo documento (no como archivo aparte). La consigna no dice nada sobre anexos: es una sugerencia, no un requisito.

## Orden del documento

Los puntos, tal como los enumera la consigna:

{order}

## Mapa de fusión (qué sale de cada fuente)

{table(['Punto', 'Fuente', 'Qué se corta o se condensa', 'Qué se agrega'], [
    ['Base del documento', '«Proyect Charter y demas puntos»', 'Se reemplaza la sección 5 por el Charter condensado; el texto largo pasa a Anexo A', 'Estilos unificados, índice automático, frases puente'],
    ['1 Carátula', '«TP Grupo 01»', 'Una sola carátula (revisar logo y nómina)', 'Versión y fecha 14/10/2026'],
    ['2 Índice', 'Se rehace', 'Se descarta el índice de cada archivo', 'Índice automático al final del armado'],
    ['3 Canvas · 4 Design Thinking', 'Documento resumido como punto de partida', 'Se descartan las afirmaciones sin evidencia', 'Texto de `05-canvas-dt-smart.md` (segmento hogares, personas, dos propuestas de valor)'],
    ['5 Charter', '`01-charter-condensado.md`', '≈ 6.000 palabras → ≈ 2 páginas', 'Aclaración del perfil de hogar básico; Anexo A'],
    ['6 Gantt', 'Imagen y hitos del largo (§6)', 'Tabla de fases del resumen (no coincide con el Excel: ver `02-gantt`)', 'Tabla de actividades del **Excel** (con las dependencias explícitas) + camino crítico + 8 hitos; el Excel completo va de anexo'],
    ['7 · 8', 'PDF «corregido» de stakeholders y comunicación', 'Se reemplaza el cuerpo de esas secciones', '2 filas en la matriz de comunicación (prestadores de transporte y proveedores)'],
    ['9 Riesgos · 10 Presupuesto', 'Largo + `04-riesgos.md` y `03-presupuesto`', 'Contingencia del 10 % plano; cifras en pesos', 'EMV, USD, desglose, reservas, curva S'],
    ['Storytelling', 'La «conexión narrativa» del resumen', '—', '10 frases puente (abajo)'],
])}

## Guía de estilo

### Estructura

- **Un título de nivel 1 por punto**, numerado «1.» a «10.» con los nombres exactos de la consigna. **Nivel 2** numerado dentro del punto (5.1, 5.2…); **nivel 3** sin numerar. No más de tres niveles.
- **Carátula:** nombre del proyecto (único), materia (Taller de Gestión de Proyectos Digitales), carrera y universidad, profesores, grupo, **una sola nómina**, fecha de entrega (14/10/2026) y versión.
- **Índice automático** (Referencias → Tabla de contenido, 3 niveles); se actualiza antes de exportar.
- **Apertura** de media página bajo el índice (frase puente de apertura) y **cierre** corto después de la sección 10.

### Tipografía y formato

- Fuente única (Calibri o Arial) **11 pt** en el cuerpo; títulos de 16, 14 y 12 pt en negrita; interlineado 1,15; márgenes de 2,5 cm; A4 vertical (la sección 6 puede ir **apaisada**).
- Color solo en títulos y encabezados de tabla (magenta institucional `#B83A95`); el resto en negro. Sin resaltados.
- **Tablas:** encabezado en negrita con fondo, bordes finos, texto de 9 a 10 pt, **fila de encabezado repetida**, filas que no se parten entre páginas, números alineados a la derecha.
- **Pie de figura y de tabla** numerados por punto («Tabla 10.2 — Desglose de mano de obra»; «Figura 6.1 — Gantt»): las tablas llevan el pie arriba y las figuras abajo; todas se citan en el texto.
- **Encabezado:** nombre del proyecto. **Pie:** «Página X de Y», versión y fecha.
- **Imágenes:** ancho de columna, buena resolución, con leyenda; el Gantt se entrega apaisado.

### Unidades, moneda y fechas

- **Moneda:** **USD** con punto de miles («USD {n(lb['total'], 0)}»); equivalente en pesos solo como referencia («{ars(lb['total'] * fx['value'] / 1e6)}»). El **tipo de cambio** (ARS {n(fx['value'], 2)} por USD, {fx['date']}, Banco Nación, **a confirmar**) se declara en las secciones 5 y 10.
- **Fechas** en formato dd/mm/aaaa; **porcentajes** con coma y espacio (12,1 %); duraciones en **días hábiles** (d.h.); 1 mes = 21 d.h.
- **Siglas** con su significado la primera vez: PERT, EMV, EDT, OKR, SMART.

### Glosario de términos e IDs (una sola forma)

{table(['Concepto', 'Forma única', 'Evitar'], glossary)}

### Presupuesto de páginas (que se lea como una historia, no como tres documentos pegados)

{table(['Punto', 'Páginas aprox.', 'Contenido'], PAGES)}

## Frases puente

Plantilla: **[qué entregó el punto anterior] → [qué pregunta abre este punto] → [qué le entrega al siguiente]**. Propuestas con el contenido real del proyecto (las de los puntos 3 a 10 son las que verifica el script de coherencia):

{table(['Punto', 'Frase'], bridges)}

## Líneas para pegar (supuesto de simulación y moneda)

- *«Las fechas del proyecto (01/04/2026–30/09/2026) corresponden a una simulación académica; el trabajo se entrega el 14/10/2026.»* (en el Charter y en el Gantt)
- *«Los importes están expresados en USD al tipo de cambio de ARS {n(fx['value'], 2)} por USD ({fx['date']}); son estimaciones con fin académico y deberán ajustarse con cotizaciones.»* (en el Charter y en el presupuesto)

## Checklist de prolijidad

{chr(10).join('- [ ] ' + x for x in CHECKLIST)}

## Plan de 2 días

Ordenado por prioridad: **Bloqueantes** (sin esto no se cumple la consigna) → **Mejoran la nota** → **Defensa**. Se trabaja en paralelo por rol (sin nombres); el esfuerzo es S (≤ 1 h), M (2–4 h) o L (más de 4 h).

### Hoy lunes 12/10

| Prioridad | Tarea | Rol | Esfuerzo |
|---|---|---|---|
| **Bloqueantes** | Acordar en el grupo las decisiones 1 a 4 de `00-resumen.md` (escenario de presupuesto, USD y tipo de cambio, segmento «hogares», perfil de hogar básico) | Todos | S |
| **Bloqueantes** | Crear el documento base con los estilos de la guía (títulos 1–10, índice, encabezado y pie) y la carátula única | Formato | M |
| **Bloqueantes** | Presupuesto: copiar las tablas de `03-presupuesto` (escenario elegido) y la memoria de cálculo a la sección 10, y la cifra a la sección 5 | Presupuesto | M |
| **Mejoran la nota** | Gantt: pasar la tabla de 40 actividades del Excel a la sección 6, corregir las celdas de dependencias (opción A de `02-gantt`) y escribir la línea de simulación | Gantt | S–M |
| **Defensa** | Anotar quién defiende cada punto (cada integrante «defiende» una sección ante el resto) | Coordinador | S |

### Martes 13/10

| Prioridad | Tarea | Rol | Esfuerzo |
|---|---|---|---|
| **Bloqueantes** | Ensamblar los 10 puntos en el documento base y pegar las 10 frases puente | Formato + Coordinador | M |
| **Bloqueantes** | Charter en la plantilla de la cátedra (`01-charter/Project_Charter_completado.docx`, revisado y con los saltos de página ajustados en Word) en la sección 5 + Anexo A; stakeholders y comunicación (PDF «corregido» + 2 filas) | Charter / Stakeholders | M |
| **Bloqueantes** | Riesgos: registro único R01–R19 con EMV y respuestas | Riesgos | M |
| **Mejoran la nota** | Design Thinking: rotular la investigación como simulada y pegar la copia revisada de las slides (`05b`) | Canvas / DT | L |
| **Mejoran la nota** | Objetivos SMART del Charter y personas del Canvas | Canvas / DT | S |
| **Mejoran la nota** | Pegar el resumen ejecutivo y verificar la tabla de consistencia del guion (`08-guion-narrativo.md`): los mismos valores en todas las secciones | Formato + Coordinador | S |
| **Defensa** | Preparar respuestas a las 8 preguntas de `06-coherencia.md` | Todos | S |

### Miércoles 14/10 (entrega)

| Prioridad | Tarea | Rol | Esfuerzo |
|---|---|---|---|
| **Bloqueantes** | Pasar el checklist de prolijidad (20 puntos) y los 7 controles de coherencia; revisión cruzada: cada integrante lee una sección que no escribió | Todos | M |
| **Bloqueantes** | Actualizar índice, exportar a PDF, abrir el PDF en otro equipo y enviar | Formato | S |
| **Defensa** | Ensayo corto de la defensa del 18/11: cada uno explica en una frase qué pregunta responde su sección | Todos | S |

**Para después:** un *mock* de una funcionalidad (seguimiento de un reporte o vista del hogar) para mostrar cómo se vería; se hace con el documento cerrado.

## Respuesta lista para pegar

Para la compañera:

> Sobre el formato: la consigna pide *un documento* con los 10 puntos juntos y en orden (carátula, índice, canvas, design thinking, charter, gantt, stakeholders, comunicación, riesgos y presupuesto), con una historia que los conecte; no puntos sueltos.
> Entonces la entrega final va en **un solo archivo** (armado en Word y exportado a PDF). El Gantt en Excel lo adjuntamos como anexo, pero el cronograma también va dentro del documento, en el punto 6. Si queremos tener certeza del formato de archivo, mandamos un mail corto a los profes para confirmarlo.

Mail corto a los profesores (opcional):

> Estimados profesores: para la entrega final del 14/10, ¿confirman que el trabajo va en un único documento (Word o PDF) con los 10 puntos de la consigna, y que el Gantt en Excel puede acompañarlo como anexo? Muchas gracias.
"""
    write("07-formato-entrega.md", txt)
