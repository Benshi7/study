"""Renders 08-guion-narrativo.md: the narrative spine of the 10 sections, with the thread objects taken from the single source of truth."""
import pathlib

import data as D
from fmt import n, table, usd

ROOT = pathlib.Path(__file__).resolve().parent.parent

SECTIONS = [  # number, consigna name, question, receives, delivers (the values are filled in render())
    (1, "Carátula"), (2, "Índice"), (3, "Canvas del proyecto"), (4, "Aplicar Design Thinking"), (5, "Project Charter"),
    (6, "Gantt del proyecto completo"), (7, "Matriz de stakeholders"), (8, "Plan de comunicación"),
    (9, "Gestión de riesgos - Matriz de riesgos"), (10, "Gestión de costos - Presupuesto"),
]


def render(c):
    o, lb = c["o"], c["lb"]
    fx = o["fx"]
    cal = o["calendar"]
    name = "Modernización del Mapa Interactivo de la Ciudad"
    hitos = [(h["name"], h["date"].strftime("%d/%m/%Y")) for h in D.TEAM["hitos"]]
    top3 = o["risks"]["sorted"][:3]
    top3_txt = ", ".join(f"{r['id']} ({usd(r['emv_usd'])})" for r in top3)
    n_st = len(D.STAKEHOLDERS_F4)
    results = ["Capa geográfica confiable", "Integración multicanal", "Reportes y seguimiento", "Gestión y experiencia del hogar"]
    spine = {
        1: ("Presentar el trabajo.", "—", f"El nombre del proyecto: {name}."),
        2: ("Guiar la lectura de una sola historia.", "Los 10 puntos de la consigna", "Los 10 puntos en orden, con sus páginas."),
        3: ("¿Qué negocio y para quién?", "La pregunta de un hogar que no sabe a qué área acudir", "El segmento hogares de la Ciudad y dos propuestas de valor (hogar y GCBA)."),
        4: ("¿El problema es real y qué solución lo resuelve? (investigación simulada)", "El segmento y las propuestas de valor", "Punto de vista, pregunta de diseño y un prototipo de tres pantallas: consultar, reportar y seguir."),
        5: ("¿Qué hacemos, con qué límites y con qué metas?", "El problema y el prototipo", f"Objetivo general, cuatro resultados, {len(hitos)} hitos, presupuesto y riesgos de alto nivel, y los stakeholders principales."),
        6: ("¿Qué tareas, en qué orden y cuánto duran?", "Los cuatro resultados y los entregables", f"40 actividades, {cal['cpm_wd']} días hábiles de camino crítico y los {len(hitos)} hitos con fecha."),
        7: ("¿A quién afecta y con cuánto poder e interés?", "Las actividades del Gantt y los stakeholders del Charter", f"{n_st} stakeholders clasificados y una estrategia para cada uno."),
        8: ("¿Qué se comunica, a quién, cuándo y por qué canal?", "La estrategia de la matriz de stakeholders", "Una matriz de comunicación con responsable, frecuencia y canal por destinatario."),
        9: ("¿Qué puede fallar y qué hacemos?", "El camino crítico y los stakeholders", f"{o['risks']['n']} riesgos con valor monetario esperado; su suma ({usd(lb['contingency'])}) es la reserva de contingencia."),
        10: ("¿Cuánto cuesta?", "Las duraciones del Gantt y la suma de los EMV", f"Presupuesto de {usd(lb['total'])} en USD (línea base {usd(lb['baseline'])} más reserva de gestión {usd(lb['mgmt_reserve'])})."),
    }
    spine_rows = [[str(i), nm, *spine[i]] for i, nm in SECTIONS]

    thread_rows = [
        ["Nombre del proyecto", name, "1, 2, 3, 5", "Charter condensado y en plantilla"],
        ["Segmento", "Hogares de la Ciudad (cada hogar con su realidad)", "3, 4, 5, 7", "`05`, `05b`, Charter en plantilla"],
        ["Funcionalidades núcleo", "Consultar · Reportar · Seguir (las tres pantallas del prototipo); la vista de gestión es el lado del GCBA de «Seguir»; «Mi hogar» es opcional (decisión del grupo)", "4, 5, 6", "`05b` (prototipo), Charter §5.6"],
        ["Hitos", "; ".join(f"{a} {b}" for a, b in hitos), "5, 6", "`02-gantt`, Charter condensado y en plantilla"],
        ["Duración", f"{cal['cpm_wd']} días hábiles (CPM del Excel del equipo); {cal['corrected_wd']} con las dependencias corregidas (opción A recomendada); las fechas son simuladas", "5, 6, 9", "`02-gantt`, `06`, Charter en plantilla"],
        ["Presupuesto", f"{usd(lb['total'])} = línea base {usd(lb['baseline'])} (costos {usd(lb['project_costs'])} + contingencia {usd(lb['contingency'])}) + reserva de gestión {usd(lb['mgmt_reserve'])}; mantenimiento inicial posterior al cierre {usd(o['maint_usd'])}", "5 (campo 12), 10", "`03-presupuesto`, memoria de cálculo, Charter en plantilla"],
        ["Tipo de cambio", f"ARS {n(fx['value'], 2)} por USD ({fx['date']}; a confirmar)", "5, 10", "`03-presupuesto`, Charter en plantilla"],
        ["Riesgos principales", top3_txt, "5, 9, 10", "`04-riesgos`, `03-presupuesto`"],
        ["Resultados del Charter", "; ".join(f"O{i} {r}" for i, r in enumerate(results, 1)), "3, 4, 5, 6", "`05`, Charter en plantilla"],
        ["Simulación", "Proyecto simulado con fines académicos: fechas ficticias (01/04/2026 a 30/09/2026), investigación de Design Thinking simulada y cifras estimativas", "1, 4, 5, 6, 10", "`05b`, Charter en plantilla"],
    ]
    # the consistency table (section 5) adds the number of the section where each value has to match
    consist_rows = [[r[0], r[1], r[2], r[3]] for r in thread_rows]

    bridge_rows = [["Apertura", D.BRIDGES["apertura"]]] + [[f"{int(k) - 1} → {k}", D.BRIDGES[k]] for k in ("3", "4", "5", "6", "7", "8", "9", "10")] + [["Cierre", D.BRIDGES["cierre"]]]
    bridge_lines = "\n".join(f"- **{lbl}.** {txt}" for lbl, txt in bridge_rows)

    summary = (
        f"Hoy un hogar de la Ciudad que quiere saber qué ocurre en su cuadra, o reportar algo que vio, debe saber de antemano qué área responde y por qué canal; "
        f"y después de reportar no ve qué pasó. Este proyecto, {name}, propone convertir el Mapa en una plataforma geográfica común: una capa que integra información oficial, "
        f"la ofrece al Mapa y a canales como Boti, y permite consultar, reportar y seguir incidencias, mientras las áreas ven y gestionan lo que les corresponde.\n\n"
        f"El Canvas plantea una plataforma de dos lados: el hogar usa y no paga; el GCBA financia y recibe una vista de gestión y una capa reutilizable. "
        f"Design Thinking, una investigación simulada con tres proto-personas, bajó la idea a un prototipo de tres pantallas: consultar, reportar y seguir. "
        f"El Charter fija el alcance, cuatro resultados y {len(hitos)} hitos, desde el Charter aprobado ({hitos[0][1]}) hasta el cierre ({hitos[-1][1]}).\n\n"
        f"El Gantt ordena 40 actividades y su camino crítico es de {cal['cpm_wd']} días hábiles. La matriz de stakeholders y el plan de comunicación definen a quién se informa, cuándo y por qué canal. "
        f"La matriz de riesgos reúne {o['risks']['n']} riesgos y la suma de sus valores esperados ({usd(lb['contingency'])}) es la reserva de contingencia. "
        f"El presupuesto, en USD con un tipo de cambio único de ARS {n(fx['value'], 2)}, suma {usd(lb['total'])} (línea base {usd(lb['baseline'])} más reserva de gestión de {usd(lb['mgmt_reserve'])}), "
        f"más {usd(o['maint_usd'])} de mantenimiento inicial posterior al cierre. Es una simulación académica: las fechas y las cifras son estimativas."
    )

    txt = f"""
# Guion narrativo: el hilo de las 10 secciones

> La consigna pide que el documento tenga un **storytelling** «dando continuidad y conexión entre los puntos». Este guion fija **qué cuenta cada sección**, **qué recibe de la anterior**, **qué hechos deben repetirse idénticos** (con un valor único que sale del modelo) y **cómo se pasa de una a otra**. Es la columna vertebral para el documento único (ver `07-formato-entrega.md`). Todo número sale de `tools/`; si algo cambia (por ejemplo, el tipo de cambio), se regenera y una prueba compara los valores contra el resto del pack.

## 1. El papel de cada sección

{table(['#', 'Sección (consigna)', 'Qué responde', 'Qué recibe', 'Qué entrega'], spine_rows)}

## 2. Objetos del hilo (deben repetirse idénticos)

Son los hechos que un profesor puede cruzar entre secciones. Cada uno tiene **un valor canónico**; si una sección lo cita, cita este.

{table(['Objeto', 'Valor canónico', 'Secciones donde aparece', 'Dónde se verificó'], thread_rows)}

## 3. Frases puente

Son las del pack (`07-formato-entrega.md`), con el contenido final: segmento hogares, investigación simulada, cuatro resultados, camino crítico del Excel y presupuesto en USD.

{bridge_lines}

## 4. Resumen ejecutivo (borrador)

{summary}

## 5. Tabla de consistencia

Antes de entregar, buscar cada valor en cada sección de la lista y comprobar que coincide palabra por palabra. Las pruebas de `tools/` ya lo verifican contra los documentos del pack (Charter, Gantt, presupuesto, riesgos, Design Thinking); en el documento final hay que repetir la verificación a mano.

{table(['Objeto', 'Valor canónico', 'Debe aparecer en las secciones', 'Verificado en'], consist_rows)}

**Cómo usarla:** al terminar de armar el documento, abrir la búsqueda de Word (Ctrl+F) y buscar «{usd(lb['total'])}», «ARS {n(fx['value'], 2)}», «{cal['cpm_wd']} días hábiles», «Hogares de la Ciudad» y las fechas de los hitos: cada una debe aparecer solo con el valor de esta tabla.
"""
    (ROOT / "08-guion-narrativo.md").write_text(txt.strip() + "\n", encoding="utf-8")
