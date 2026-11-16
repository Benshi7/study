"""Renders the markdown deliverables from the computed numbers (single source of truth)."""
import pathlib

import budget as bud
import coherence as co
import cpm
import data as D
import risks as rk
import svg
import render_budget as rbud
from fmt import ars, n, pct, table, u, usd

ROOT = pathlib.Path(__file__).resolve().parent.parent


def write(rel, text):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text.strip() + "\n", encoding="utf-8")


def context(o, res, acts, cal):
    names = {a["id"]: a["name"] for a in D.ACTIVITIES}
    phase_of = {a["id"]: a["phase"] for a in D.ACTIVITIES}
    cp = o["critical_path"]
    crit_ids = sorted(i for i, r in res.items() if r["critical"])
    la, lb = o["ladder_a"], o["ladder_b"]
    sorted_risks = o["risks"]["sorted"]
    return dict(o=o, res=res, acts=acts, cal=cal, names=names, phase_of=phase_of, cp=cp, crit_ids=crit_ids, la=la, lb=lb, sr=sorted_risks)


def render_gantt(c):
    o, res, cal, names = c["o"], c["res"], c["cal"], c["names"]
    g, cal_o = o["gantt"], o["calendar"]
    sc = {s["key"]: s for s in g["scenarios"]}
    team = D.TEAM
    by = {a["id"]: a for a in D.ACTIVITIES}
    fmt_ids = lambda ids: ", ".join(map(str, ids))
    pub_crit = c["crit_ids"]
    fix_crit = g["critical_corrected"]
    added = sorted(set(fix_crit) - set(pub_crit))
    removed = sorted(set(pub_crit) - set(fix_crit))
    # --- tables
    scen_rows = []
    labels = {
        "escrito": "**Como está escrito, «a-b» = los dos extremos** (es lo que calcula la hoja del equipo)",
        "rango": "Como está escrito, «a-b» = todo el rango",
        "fechas_del_equipo": "Fechas escritas en las columnas Inicio/Fin",
        "corregida": "**Dependencias corregidas según las fechas** (opción A, recomendada)",
        "con_adelantos": "Dependencias como están + 7 adelantos + vínculo 26→27 (opción B)",
        "fs_estricto": "Fin-a-inicio estricto + vínculo 26→27, fechas recalculadas (opción C)",
    }
    for s in g["scenarios"]:
        crit = "—" if s["n_critical"] is None else s["n_critical"]
        scen_rows.append([labels[s["key"]], s["total"], s["end"], crit])
    why = {
        (2, 1): "Inicio-a-inicio +1 día: 2 y 3 arrancan el día siguiente a que arranca 1.",
        (3, 1): "Ídem.",
        (8, 7): "Las fechas esperan a 5 y 6 (terminan el 17/04), no a 7 (termina el 21/04).",
        (9, 7): "Ídem.",
        (14, 13): "14 arranca al día siguiente de que termina 11 (08/05); 13 termina el 12/05.",
        (15, 12): "15 arranca al día siguiente de que termina 11; 12 termina el 12/05.",
        (16, 14): "16 arranca al día siguiente de que termina 13 (12/05); 14 termina el 15/05.",
    }
    lead_rows = [[s, names[s], p, names[p], k, why[(s, p)]] for s, p, k in g["leads"]]
    cell_why = {
        8: "Arranca el 20/04, el día siguiente a que terminan 5 y 6 (17/04); 7 termina el 21/04.",
        9: "Ídem 8.",
        10: "Si 8 y 9 ya no esperan a 7, la actividad 7 queda sin sucesora: lo lógico es validar con 7 terminada (termina el 21/04; 10 arranca el 27/04).",
        14: "Arranca el 11/05, el día siguiente a que termina 11 (08/05); 13 termina el 12/05.",
        15: "Arranca el 11/05: espera a 10 y 11, no a 12 (termina el 12/05).",
        16: "Arranca el 13/05, el día siguiente a que terminan 12 y 13 (12/05); 14 termina el 15/05.",
        27: "Arranca el 22/07, el día siguiente a que termina 26; 18 a 23 terminan, como tarde, el 02/07.",
    }
    cells_rows = []
    for i in g["corrected_cells_range"]:
        cells_rows.append([i, names[i], by[i]["deps_raw"], g["corrected_text"][str(i)], cell_why[i]])
    explicit_rows = [[i, names[i], by[i]["deps_raw"], g["corrected_text"][str(i)]] for i in g["corrected_cells_endpoints"] if i not in g["corrected_cells_range"]]
    rng_rows = [[i, s_team, s_rng] for i, s_rng, s_team in g["range_slack_mismatches"]]
    hol_rows = [[h["id"], names[h["id"]], ", ".join(h["dates"])] for h in g["holiday_hits"]]
    pert_rows = []
    for r in g["pert_example"]:
        pert_rows.append([r["id"], names[r["id"]], r["o"], r["m"], r["p"], n(r["te"], 2), n(r["te"] - r["m"], 2)])
    act_rows = []
    for a in D.ACTIVITIES:
        i = a["id"]
        act_rows.append([i, a["name"], a["dur"], a["deps_raw"], g["corrected_text"][str(i)], a["start"].strftime("%d/%m"), a["end"].strftime("%d/%m"),
                         res[i]["slack"], "**Sí**" if i in fix_crit else "No", D.ACTIVITY_OWNER[i]])
    phase_rows = [[x["phase"], f"{x['declared_start']} – {x['declared_end']}", f"{x['team_start']} – {x['team_end']}"] for x in g["phase_diffs"]]
    gates = [[gg["gate"], gg["name"], gg["declared"], gg["proposed"], gg["computed"], "✓" if gg["ok"] else "✗"] for gg in o["gates"]]
    gap = g["gap"]
    txt = f"""
# Gantt: el Excel ya tiene lo que pide la cátedra; ajustes puntuales

> **Corrección importante.** Nuestro análisis anterior dijo que el Gantt «no tenía duraciones, dependencias ni camino crítico». Eso era cierto **solo para la imagen del documento Word**. El **Excel del equipo (Anexo del punto 6)** sí los trae: 40 actividades con duración en días hábiles, dependencias, holguras, camino crítico (CPM) y 8 hitos. Esta página **toma ese Excel como base** y ya no propone reemplazarlo: propone ajustes puntuales. Ningún original fue modificado. Archivo de datos: `schedule.csv`; diagrama: `gantt.svg`.

## Lo que ya está bien

- **40 actividades, 8 fases, 8 hitos** con fechas. Los 8 hitos del Excel son **idénticos** a los del Charter (§6.3) y a los gates del documento resumido: ninguna fecha de hito cambia.
- **Cada duración coincide con las fechas:** para las 40 actividades, el rango Inicio–Fin tiene exactamente esa cantidad de días hábiles (lunes a viernes).
- **El cálculo CPM de la hoja «Dependencias y Camino Crítico» es correcto** si «a-b» se lee como *los dos extremos*: recalculado por separado, da **{cal_o['cpm_wd']} días hábiles, {o['n_critical']} actividades críticas y las mismas holguras que la hoja, sin ninguna diferencia**. El propio Anexo lo confirma: escribe «1, 3» donde el cronograma dice «1-3».
- **La nota del Anexo sobre PERT es correcta** (CPM con una duración por actividad; no inventaron estimaciones de tres puntos). Ver el punto 7 por si preguntan.

## Qué ajustar (en orden de importancia)

### 1 · La notación «a-b» es ambigua y cambia el resultado

«1-3» puede leerse como {{1, 2, 3}} o como {{1, 3}}. La hoja del equipo usa la segunda; si alguien la lee como rango, el CPM da **{cal_o['range_wd']} días hábiles** (no {cal_o['cpm_wd']}), cambian **{len(g['range_slack_mismatches'])} holguras** y **{len(g['range_critical_mismatches'])} marcas de «crítica»** (actividades {fmt_ids(g['range_critical_mismatches'])}). Se afecta solo donde el guion cubre tres o más números: actividades {fmt_ids(g['ambiguous_ids'])}.

**Arreglo (sin cambiar fechas):** escribir listas explícitas («1, 2, 3») en todas las celdas, como ya hace el Anexo. La columna `Predecesoras propuestas (explícitas)` de `schedule.csv` trae el texto listo para pegar.

### 2 · Las fechas y la columna de dependencias no se cuentan la misma historia

Hay **7 actividades que empiezan antes de que termine una de sus predecesoras** y **una espera que la columna no explica**. Mirando las fechas, lo más probable es que la columna tenga errores de tipeo (hipótesis: **confirmar con quien armó el Excel**):

{table(['Sucesora', 'Nombre', 'Predecesora', 'Nombre', 'Adelanto (d.h.)', 'Qué muestran las fechas'], lead_rows)}

Además, la actividad **27 (Pruebas funcionales)** arranca el 22/07, el día siguiente a que termina **26**, pero su celda dice «18-23» (todas terminan, como tarde, el 02/07): **{g['idle_gaps'][0][2]} días hábiles de espera** que ninguna dependencia explica. Y entre **31 y 32** hay **un día hábil sin actividad** (21/08).

**Celdas a corregir (la lista escrita contradice las fechas, se lea el guion como se lea):**

{table(['ID', 'Actividad', 'Escrito', 'Propuesto', 'Por qué'], cells_rows)}

**Celdas que solo hay que escribir explícitas** (la lectura «extremos» pierde predecesoras que las fechas sí respetan):

{table(['ID', 'Actividad', 'Escrito', 'Explícito'], explicit_rows)}

Con esas correcciones **todas las fechas del equipo se reproducen exactamente** (hasta la actividad 31; desde la 32 el cálculo adelanta un día por el día sin actividad) y ya no queda ningún solape salvo 2 y 3, que se escriben como inicio-a-inicio (+1 día).

### 3 · Qué le hace cada lectura a la fecha de cierre

{table(['Lectura', 'Días hábiles', 'Fin', 'Actividades con holgura 0'], scen_rows)}

Cómo se llega de un número al otro: con las dependencias **como están** y fin-a-inicio estricto más el vínculo 26→27, el proyecto cerraría el **{cal_o['strict_end']}** ({cal_o['strict_wd']} d.h.); los **{gap['leads_saved']} días hábiles** de adelantos lo comprimen a {cal_o['dated_wd']}, y el día sin actividad entre 31 y 32 lo estira a {cal_o['span_wd']} (el cierre del 30/09 del equipo). **Conclusión:** la fecha del 30/09 se sostiene, pero solo con las dependencias corregidas (opción A) o declarando los adelantos (opción B).

### 4 · El camino crítico cambia con las correcciones

- **Publicado** (hoja del equipo): {len(pub_crit)} actividades sin holgura; cadena principal {fmt_ids(o['critical_path'])}.
- **Con dependencias corregidas:** {o['n_critical_corrected']} actividades sin holgura; cadena principal {fmt_ids(o['critical_path_corrected'])}.
- **Entran al camino crítico:** {fmt_ids(added)}. **Salen:** {fmt_ids(removed)}.
- Lectura de negocio: pasan a ser críticas la **integración con canales digitales (25)** y las **pruebas de intercambio (26)**, que antes tenían 32 días de holgura. Es coherente con el riesgo R12 (cambios en canales como Boti, BAX y miBA): conviene decirlo en la defensa.

### 5 · Calendario y feriados (opcional)

El Excel declara un «período operativo ficticio» y usa lunes a viernes **sin feriados**. Es una convención válida si se declara. Dentro del período hay **{g['holiday_weekdays_in_window']} feriados o días no laborables en día de semana**; si se contaran, las {cal_o['span_wd']} jornadas terminarían el **{g['real_calendar_end']}**, un día antes de la entrega (14/10). Actividades cuyas fechas incluyen alguno:

{table(['ID', 'Actividad', 'Fechas no laborables incluidas'], hol_rows)}

**Propuesta (mínimo esfuerzo):** no tocar fechas y agregar una línea: *«Las fechas del proyecto (01/04–30/09/2026) corresponden a una simulación académica; se cuentan los días de lunes a viernes, sin feriados.»* Fuentes de los feriados: [Canal 26](https://www.canal26.com/general/2025/11/02/confirman-los-feriados-del-2026-en-argentina-el-calendario-completo-con-fines-de-semana-largos/) y [Argentina.travel](https://www.argentina.travel/es/novedades/feriados-en-argentina-2026-calendario-para-planificar-tu-viaje); el traslado del 15/06 (Güemes) figura como **a confirmar**.

### 6 · Columna «Responsable» vacía

Propuesta: un **rol** por actividad, el mismo que usa el presupuesto (`Responsable propuesto (rol)` en la tabla de abajo y en `schedule.csv`). Cada rol trabaja dentro de su ventana del presupuesto, así que **mano de obra y Gantt cuentan lo mismo**.

### 7 · PERT: no hace falta, pero hay que saber contestarlo (complemento)

La Clase 3 enseña PERT `(O+4M+P)/6` para estimar duraciones. La hoja usa **CPM con una duración por actividad** y lo dice. Es aceptable. Si el profesor pregunta: *«no tenemos estimaciones de tres puntos; usamos CPM con duraciones únicas, y PERT es el paso siguiente para las actividades más inciertas».* A modo de **ilustración** (valores a acordar, **no son datos del equipo**; M es la duración del equipo):

{table(['ID', 'Actividad', 'O', 'M', 'P', 'Esperada', 'Diferencia vs. M'], pert_rows)}

### 8 · Otros documentos que no coinciden con el Excel

- **Documento resumido, tabla de fases:** {len(g['phase_diffs'])} de 8 ventanas difieren del Excel, y dos fases arrancan un **sábado** (18/04 y 02/05):

{table(['Fase', 'En el documento resumido', 'En el Excel'], phase_rows)}

- **Charter largo §6.5:** lista **7** puntos de control (junta «desarrollo e integraciones» en el Gate 4) frente a los **8** hitos del Excel y de §6.3. Propuesta: 8, uno por fase, con los nombres del Excel.
- La actividad 36 (**Monitoreo inicial**) es de la fase *Implementación* en el Excel; la tabla de fases del resumen la ubica en *Cierre*.

### Gates: Excel, Charter y resultado del cálculo

{table(['Gate', 'Hito (Excel)', 'Documento resumido', 'Excel', 'Calculado (fechas del equipo)', 'OK'], gates)}

## Las 40 actividades (como las escribió el equipo, con la propuesta al lado)

Inicio/Fin son las del equipo; «Holgura» y «Crítica» corresponden a la opción A.

{table(['ID', 'Actividad', 'Dur.', 'Dependencias (escrito)', 'Explícitas (propuesta)', 'Inicio', 'Fin', 'Holgura', 'Crítica', 'Responsable (rol)'], act_rows)}

## Opciones para decidir entre todos

| Opción | Qué se hace | Fechas | Fin | Esfuerzo |
|---|---|---|---|---|
| **A (recomendada)** | Corregir {len(g['corrected_cells_range'])} celdas, escribir explícitas las demás y marcar 2 y 3 como inicio-a-inicio | No cambian | {cal_o['corrected_end']} de cálculo; 30/09 con el día sin actividad | Bajo (editar ~12 celdas) |
| B | Dejar las dependencias y registrar 7 adelantos y el vínculo 26→27 | No cambian | {cal_o['dated_end']} | Bajo, pero conserva los errores de tipeo |
| C | Respetar fin-a-inicio con las dependencias actuales | Se corren | {cal_o['strict_end']} (pasa el 30/09) | Alto: rehacer fechas, hitos y presupuesto |
| Mínimo para entregar | Solo agregar una nota en el punto 6: «a-b = los dos extremos» y la línea de simulación | No cambian | 23/09 (CPM) / 30/09 (fechas) | Muy bajo |

## Línea base

La tabla de arriba, con las fechas del equipo, es la **línea base v1 del cronograma** (Clase 3); cualquier cambio de fecha de un gate pasa por el control de cambios del Charter.

## Qué no se pudo verificar

- Que las correcciones propuestas sean las que **quiso escribir** quien armó el Excel: son una deducción a partir de las fechas.
- Si la Clase 3 usa la notación de **adelantos y retrasos**: la cátedra enseña las relaciones FS, FF y SS (el cuarto tipo, SF, aparece solo como complemento); los adelantos son un recurso de este análisis.
- La imagen EMF incrustada en el documento Word no se pudo abrir; el Excel la reemplaza.
"""
    write("02-gantt/gantt.md", txt)
    write("02-gantt/gantt.svg", svg.gantt_full(c["acts"], res, cal, c["phase_of"], names, themed=False))


def render_risks(c):
    o, res = c["o"], c["res"]
    sr = c["sr"]
    scale_rows = [[k, pct(D.SCALE["prob"][k], 0), f"{u(D.SCALE['impact_M'][k])} (≈ {ars(D.SCALE['impact_M'][k])})"] for k in range(1, 6)]
    names = c["names"]
    reg = []
    fixc = set(o["gantt"]["critical_corrected"])
    for r in sr:
        acts_ = D.RISK_ACTS[r["id"]]
        if any(res[a]["critical"] for a in acts_):
            crit = "Sí"
        elif any(a in fixc for a in acts_):
            crit = "Solo con las dependencias corregidas"
        else:
            crit = "No"
        tag = " *(nuevo)*" if r["new"] else (" *(reformulado)*" if r["mod"] else "")
        reg.append([r["id"], r["name"] + tag, f"{r['p']}×{r['i']}={r['p'] * r['i']}", rk.level(r["p"] * r["i"]), usd(r["emv0_usd"]), r["resp"],
                    f"{r['pr']}×{r['ir']}", usd(r["emv_usd"]), ", ".join(map(str, acts_)) + f" ({crit})", r["owner"], "◆" if r["hl"] else ""])
    word = []
    full = {r["id"]: r for r in D.RISKS}
    for r in sr:
        f = full[r["id"]]
        word.append([r["id"], f"Ante {f['evento']}, podría ocasionar {f['problema']}, lo que impactaría en {f['restr']}.", f["cat"]])
    hl = [r for r in sr if r["hl"]]
    txt = f"""
# Riesgos: un solo registro, con EMV y respuestas

> **Propuesta.** Se parte de los 15 riesgos del documento largo (§9.2, **se conservan sus IDs R01–R15 y sus P e I**, salvo R10, reformulado por el perfil de hogar básico: P inicial de 2 a 3) y de los 4 del documento resumido (se mapean a esos mismos IDs). Se agregan 4 riesgos: tres propios de la Opción B (R16–R18) y **R19** por la moneda (el presupuesto ahora se expresa en USD). Se agregan también las columnas que la cátedra pide: **EMV** y **respuesta** (Clase 5). Importes en USD al tipo de cambio único de `03-presupuesto`. Ningún original fue modificado.

## Qué estaba mal y cómo se arregla

| Problema | Propuesta |
|---|---|
| 15 riesgos en un documento y 4 en otro, con IDs distintos (en uno R04 es adopción de vecinos; en el otro es coordinación entre áreas) | **IDs maestros = los del documento largo.** Equivalencias: resumen R01→R01, R02→R02, R03 (alcance)→**R05**, R04 (adopción)→**R06**. En el resumen conviene eliminar la lista de 4 y remitir a la matriz completa. |
| No hay EMV; la contingencia es un 10 % plano | EMV = probabilidad × impacto en dinero (Clase 5, p31). Ver escala y totales abajo. |
| Casi todo es «Mitigar» | Se proponen respuestas variadas: Evitar (R05, R10, R15), Transferir (R18), Aceptar (R17). |
| §9.4 destaca 8 riesgos y omite otros de nivel 12 | Criterio único: se ordena por **EMV residual**. |
| §9 cita «las actividades del camino crítico del Gantt» | Ese camino **sí existe** (Excel, hoja «Dependencias y Camino Crítico»). La columna «Actividades del Gantt» (abajo) marca qué riesgos tocan actividades críticas **según el Excel**; usar la misma lista en §6 y §9 (si se adoptan las dependencias corregidas, ver `02-gantt`). |
| Faltan riesgos de la Opción B y de la moneda | R16 (las áreas no adoptan la capa), R17 (convenios con socios), R18 (dependencia de miBA, **supuesto a confirmar**), **R19** (variación del tipo de cambio ARS/USD: factor Económico del PESTEL, Clase 4 p7). |
| Privacidad de los hogares | R10 se reformula: el **perfil de hogar básico (dato mínimo declarado, opt-in)** entra en el alcance, así que la probabilidad inicial sube de 2 a 3; el marco legal queda como **«Ley 25.326, a verificar»** (no se afirma qué dice). |

Texto sugerido para la apertura de §9: *«A partir de las actividades expuestas del Gantt (sección 6, con su camino crítico) y de las interacciones con los stakeholders, identificamos y priorizamos los riesgos del proyecto.»*

## Escala de conversión a dinero (propuesta, a acordar)

El equipo usa escalas ordinales de 1 a 5. Para calcular un EMV hay que pasarlas a porcentaje y a pesos:

{table(['Nivel', 'Probabilidad', 'Impacto (si ocurre)'], scale_rows)}

Los importes son **supuestos del grupo, no datos**: ARS 1,5 / 3 / 6 / 12 / 25 M, que son ≈ 0,5 %, 1 %, 2 %, 4 % y 8 % del presupuesto base del equipo (ARS 313 M), expresados en USD con el tipo de cambio único. El registro permite cambiarlos en un solo lugar (`tools/data.py`) y recalcular todo.

## Registro consolidado (ordenado por EMV residual)

Referencias: ◆ = va a «Riesgos de alto nivel» del Charter. P×I inicial es el del equipo; P×I residual es el esperado **después** de aplicar la respuesta (propuesta a validar). EMV en USD (tipo de cambio único de `03-presupuesto`).

{table(['ID', 'Riesgo', 'P×I inicial', 'Nivel', 'EMV inicial', 'Respuesta', 'P×I res.', 'EMV residual', 'Actividades del Gantt (¿críticas según el Excel?)', 'Dueño (rol)', '◆'], reg)}

**Totales:** EMV inicial {usd(o['risks']['emv_initial_usd'])} · **EMV residual (amenazas) {usd(o['risks']['emv_residual_usd'])}** → es la **reserva de contingencia** propuesta (Clase 5, p30–31: los riesgos residuales alimentan el plan de contingencia; Clase 4, p19 y p20: contingencia = probabilidad × impacto). De esa suma, {usd(o['risks']['emv_residual_team15_usd'])} vienen de los 15 riesgos del equipo.

**Riesgos que tocan actividades críticas** (según el Excel del equipo): {', '.join(r['id'] for r in sr if any(res[a]['critical'] for a in D.RISK_ACTS[r['id']]))}. Con las dependencias corregidas (`02-gantt`) se suman: {', '.join(r['id'] for r in sr if not any(res[a]['critical'] for a in D.RISK_ACTS[r['id']]) and any(a in set(o['gantt']['critical_corrected']) for a in D.RISK_ACTS[r['id']])) or 'ninguno'}. Los de este grupo conviene vigilarlos primero: un retraso en una actividad crítica corre la fecha de cierre.

**Decisión de método a declarar (Clase 5, p32):** la diapositiva resta las oportunidades a las amenazas. Esta propuesta **no cuantifica oportunidades** y reserva solo las amenazas (postura conservadora). Si el equipo identifica oportunidades, puede restarlas (modo «neto»).

## Redacción con la plantilla de la cátedra (Clase 5, p17)

{table(['ID', 'Riesgo (evento → problema → restricción afectada)', 'Categoría (Clase 5, p25)'], word)}

## Los {len(hl)} riesgos de alto nivel para el Charter

{table(['ID', 'Riesgo', 'EMV residual (USD)'], [[r['id'], r['name'], usd(r['emv_usd'])] for r in hl])}

Criterio: los de mayor nivel inicial o EMV que además son los que el propio equipo ya había destacado en §9.4 (R01, R02, R04, R05) más R12 (canales digitales, clave para la Opción B). Todos están en el registro.

## Para la defensa

- *«¿De dónde sale la contingencia?»* → de la suma de los EMV residuales: {usd(o['risks']['emv_residual_usd'])}.
- *«¿Y si los importes de impacto fueran otros?»* → ver la sensibilidad en `03-presupuesto`: con la escala a la mitad la contingencia sería {usd(o['sensitivity']['0.5']['contingency'])}; con la escala ×1,5, {usd(o['sensitivity']['1.5']['contingency'])}. Con el dólar ±20 % cambia el total en USD (cuadro de `03-presupuesto`), no los pesos.
- Los riesgos R16–R19 y el EMV de cada fila son **propuestas**: ninguno proviene de datos del proyecto.
"""
    write("04-riesgos.md", txt)


def render_budget(c):
    rbud.render(c)


def render_charter(c):
    o, lb, res = c["o"], c["lb"], c["res"]
    gate_rows = [[g["gate"], g["name"], g["proposed"]] for g in o["gates"]]
    hl = [r for r in c["sr"] if r["hl"]]
    mapping = [
        ["1 · Propósito o justificación", "§5.2, §5.3", "Presente", "Condensar"],
        ["2 · Descripción de alto nivel", "§5.1 (descripción breve), §5.5.1", "Presente", "Condensar"],
        ["3 · Objetivos", "§5.4", "Parcial", "Los 8 objetivos no tienen meta ni plazo (no SMART). Se reemplazan por 4 resultados SMART (ver `05`); los 8 quedan en el Anexo A."],
        ["4 · Requisitos de alto nivel", "No existe como tal (se deducen de §5.5–5.6)", "**Falta**", "Lista de 8 requisitos (propuesta, abajo)"],
        ["5 · Producto o resultados principales", "§5.6", "Presente", "Condensar los 8 entregables en una lista"],
        ["6 · Suposiciones y restricciones", "§5.10", "Presente", "Condensar + supuesto de simulación + supuestos a confirmar"],
        ["7 · Cronograma de alto nivel", "§5.12 (8 hitos, sin fechas)", "Parcial", "Tabla de 8 gates con fechas (de 02-gantt)"],
        ["8 · Presupuesto de alto nivel", "§5.8 (categorías, sin cifra ni moneda)", "Parcial", "Una cifra en USD y 4 líneas (de 03-presupuesto)"],
        ["9 · Riesgos de alto nivel", "§5.9.1 (12 riesgos)", "Parcial", "5 riesgos con los IDs de la matriz; uno de los 12 («comercios») no existe en la matriz"],
        ["10 · Criterios de éxito", "§5.7.1", "Presente", "Condensar y vincular a los objetivos SMART"],
        ["11 · Stakeholders principales", "§5.11 (roles) y PDF §7.3", "Parcial", "Lista única de 9, igual a la del PDF"],
        ["12 · Responsabilidades y autoridad del PM", "§5.11.2 (responsabilidades)", "Parcial", "Falta la **autoridad**: se propone abajo"],
        ["13 · Requisitos de aprobación", "§5.11.1 (qué aprueba el Sponsor), §5.7.3", "Parcial", "Se explicitan quién aprueba qué (propuesta, abajo)"],
    ]
    txt = f"""
# Project Charter condensado (≈ 2 páginas) + camino medio

> **Formato recomendado: la plantilla de la cátedra.** El mismo contenido está **completo en la plantilla de 24 campos** (`raw/Project_Charter_Template5.docx`) en `01-charter/Project_Charter_completado.docx`, con su `README.md` (mapa de los 13 elementos de la Clase 3 a los 24 campos y qué va al Anexo A). Este texto queda como **versión en prosa** del mismo contenido; si hay que elegir, **la plantilla es la opción principal**.

> **Propuesta.** Es una versión **para colocar como sección 5** manteniendo, como **Anexo A – Charter ampliado**, el texto largo del equipo (§5.1–5.12): nadie pierde trabajo. Se condensan las palabras del propio documento; lo nuevo está marcado **(propuesta)**. Ningún original fue modificado.

## Por qué condensar (con evidencia)

- La cátedra define el Charter como un **acuerdo preliminar de alto nivel** con **13 elementos en 3 partes** (Clase 3, p12–16). Lo que se evalúa es que estén y que sean **coherentes con el resto**.
- La sección 5 del documento largo tiene ≈ **6.060 palabras (más de la mitad del archivo (≈ 53 %))**; sus apartados 5.8 (presupuesto), 5.9 (riesgos) y 5.12 (cronograma) **repiten con menos detalle** las secciones 10, 9 y 6.
- **Esa duplicación ya produjo las contradicciones:** 12 riesgos en el Charter vs 15 en la matriz (y uno del Charter no está en la matriz), 8 hitos vs 7 gates, presupuesto sin cifra en el Charter y con cifra en la sección 10.
- Una sola fuente por dato (el Charter **resume y remite**) elimina esa clase de error.

## Mapa de los 13 elementos

{table(['Elemento (nombre de la cátedra)', 'Dónde está hoy', 'Estado', 'Qué cambia'], mapping)}

---

# 5. Project Charter *(texto propuesto)*

**Proyecto:** Modernización del Mapa Interactivo de la Ciudad · **Metodología:** cascada · **Organización:** Gobierno de la Ciudad de Buenos Aires · **Período simulado:** 01/04/2026–30/09/2026.

## Parte I

**1. Propósito y justificación.** Modernizar el Mapa Interactivo para convertirlo en una **plataforma geográfica común** que integre información de distintas áreas, la ofrezca desde varios canales digitales y permita la participación de los vecinos. El problema identificado es la **dispersión de la información entre canales, áreas y sistemas**: cada hogar debe saber de antemano qué organismo y qué canal usar, y no ve qué ocurre con lo que reporta. *(Condensado de §5.2–5.3; la validación con personas se detalla en la sección 4.)*

**2. Descripción de alto nivel.** Una **capa geográfica común** reutilizable por el Mapa y otros canales (Boti y BAX, sujeto a validación técnica), más un **sistema de reportes ciudadanos georreferenciados** con validación colaborativa y seguimiento del estado hasta el cierre, un **perfil de hogar básico** (dato mínimo declarado por el propio hogar, opt-in) y una **vista de gestión** para las áreas responsables. La Opción B del Canvas lo expresa como plataforma de dos lados: el vecino que usa y el Gobierno que financia y gestiona.

**3. Objetivos del proyecto** *(propuesta: cuatro resultados SMART; el texto completo está en `05-canvas-dt-smart.md`)*.
- **O1 · Capa geográfica confiable:** al 26/05 (Gate 3) la arquitectura y el diseño de la capa están aprobados y, al 02/07 (Gate 4), la capa integra las fuentes priorizadas con responsable y frecuencia de actualización definidos para el 100 % de ellas.
- **O2 · Integración multicanal:** al 21/07 (Gate 5) el Mapa y al menos un canal conversacional consumen la capa mediante API.
- **O3 · Reportes y seguimiento:** al 27/08 (Gate 6) el 100 % de los casos de prueba del flujo reporte → validación → derivación → resolución → cierre están aprobados.
- **O4 · Gestión y experiencia:** al 09/09 (Gate 7) al menos 3 áreas operativas usan la vista de gestión.

**4. Requisitos de alto nivel** *(propuesta; derivados de §5.5–5.6)*: (a) integrar las fuentes oficiales priorizadas en una capa común; (b) consultar la capa desde el Mapa y desde canales digitales seleccionados; (c) reportar incidencias con ubicación, categoría, fecha y hora; (d) validación colaborativa por otros usuarios; (e) seguimiento de estados (Reportado → Validado → Derivado → En gestión → Resuelto → Cerrado); (f) vista de gestión con filtros por categoría y estado; (g) gobernanza y calidad de datos y protección de los datos personales, incluido el perfil de hogar básico, opt-in y con dato mínimo (marco legal: **Ley 25.326, a verificar**); (h) documentación y transferencia a los responsables operativos.

## Parte II

**5. Producto y resultados principales.** Capa geográfica común · integraciones con fuentes y canales · módulo de reportes · validación colaborativa · seguimiento de incidencias · vista de gestión · documentación técnica y funcional · plan de implementación y cierre (§5.6).

**6. Suposiciones y restricciones.** *Supuestos:* las áreas ponen a disposición sus fuentes y participan de las validaciones; las fuentes priorizadas tienen APIs viables; los canales elegidos siguen disponibles; el equipo está disponible en cada etapa; las fuentes pueden asociarse a una referencia geográfica común. *Restricciones:* alcance cerrado (§5.5), enfoque en cascada con gates, dependencia de sistemas externos, calidad de las fuentes, presupuesto y plazos aprobados, protección de datos. **Supuesto de simulación:** *las fechas corresponden a una simulación académica; el trabajo se entrega el 14/10/2026.* **A confirmar:** la integración con BAX requiere miBA; marco legal de datos personales.

**7. Cronograma de alto nivel** *(detalle en la sección 6)*.

{table(['Gate', 'Hito', 'Fecha'], gate_rows)}

Duración simulada: 01/04–30/09/2026 (**{o['calendar']['span_wd']} días hábiles**, lunes a viernes). Camino crítico y holguras: sección 6.

**8. Presupuesto de alto nivel** *(detalle en la sección 10; escenario B, a decidir entre todos)*.

{table(['Concepto', 'Monto (USD)'], [['Costos del proyecto (mano de obra {0} + otros rubros {1})'.format(usd(o['labour_b']), usd(o['other_total'])), usd(lb['project_costs'])], ['Reserva de contingencia (Σ EMV de la matriz de riesgos)', usd(lb['contingency'])], ['**Línea base de costos**', f"**{usd(lb['baseline'])}**"], ['Reserva de gestión (10 %)', usd(lb['mgmt_reserve'])], ['**Presupuesto total**', f"**{usd(lb['total'])}**"]])}

*Importes en USD al tipo de cambio de ARS {n(o['fx']['value'], 2)} por USD (referencia del {o['fx']['date']}, **a confirmar**); equivalente en pesos: {ars(lb['total'] * o['fx']['value'] / 1e6)}. Operación inicial posterior al cierre: {usd(o['maint_usd'])}, fuera de la línea base. Si el equipo elige el escenario A, el total es {usd(c['la']['total'])}.*

**9. Riesgos de alto nivel** *(detalle en la sección 9; mismos IDs)*: {'; '.join(f"**{r['id']}** {r['name'].lower()}" for r in hl)}.

## Parte III

**10. Criterios de éxito.** Los cuatro objetivos SMART anteriores, más: información de fuentes oficiales con responsable y actualización definidos; cada reporte con un estado identificable desde la creación hasta el cierre; acceso de las áreas a la vista de gestión; documentación suficiente para operar y mantener (§5.7.1).

**11. Stakeholders principales** *(detalle en las secciones 7 y 8; misma lista)*: {', '.join(D.CHARTER_STAKEHOLDERS_PROPOSED)}.

**12. Responsabilidades y autoridad del Project Manager** *(autoridad: propuesta)*. *Responsabilidades (§5.11.2):* elaborar y mantener el plan, coordinar las etapas, seguir cronograma, alcance, riesgos, recursos y costos, comunicar avances y desvíos y gestionar la aprobación de entregables. *Autoridad:* asignar y reasignar recursos dentro de la línea base aprobada; aprobar cambios **menores** (sin efecto en alcance, costo ni plazo de los gates); usar la **reserva de contingencia** con registro (§10.8); **escalar** al Sponsor todo cambio significativo y todo uso de la **reserva de gestión**, que requiere su aprobación.

**13. Requisitos de aprobación** *(propuesta; amplía §5.11.1 y §5.7.3)*. El **Sponsor institucional** aprueba el Charter, el alcance y los cambios significativos; **Hacienda / Presupuesto** aprueba la partida y la reserva de gestión; cada **gate** se aprueba por el Sponsor con las áreas dueñas del dato; la aceptación final exige: alcance cumplido, entregables y documentación completos, pruebas funcionales y de integración aprobadas, defectos críticos resueltos o aceptados formalmente.

---

## Anexo A – Charter ampliado

El texto actual del Charter (§5.1–5.12) pasa íntegro como anexo con la advertencia: *«En caso de diferencia, rigen los datos de las secciones 5 (resumen), 6, 9 y 10.»* Así se conserva todo el trabajo y los números **tienen una sola fuente**.

## Aclaración propuesta para §5.5.1 y §5.5.2 (perfil de hogar)

El Charter excluye *«funcionalidades de perfil personal avanzado o personalización basada en datos sensibles que no sean necesarias para los objetivos definidos»* (§5.5.2): la exclusión es **condicional**, no una contradicción con un perfil por hogar. Para que nadie la lea de otra manera, se propone agregar **una oración**:

> *«Quedan incluidos en el alcance el **perfil de hogar básico** (dato mínimo declarado por el propio hogar, opt-in) y la personalización que se derive de él; quedan **excluidos del MVP** la personalización avanzada y el uso de datos sensibles que no sean necesarios para los objetivos definidos.»*

## Qué limpiar antes de entregar (se vio en los originales)

- La **nota de chat** dentro de §5.4.2 («yo los mantendría…») y la sección «Resumen y borrador» del documento resumido.
- El título **«5.11.7 Res.ponsables»** (error de tipeo).
- Nombre del proyecto: dos versiones («Modernización del Mapa Interactivo de la Ciudad» vs «Modernización y Ampliación…»). Unificar.
"""
    write("01-charter-condensado.md", txt)


def render_canvas(c):
    o = c["o"]
    txt = f"""
# Canvas (Opción B), Design Thinking y objetivos SMART

> **Propuesta.** Lo que sigue concreta la **Opción B** (plataforma de dos lados) con el segmento que **definió el equipo**: **hogares de la Ciudad en general**, cada uno con su propia realidad. Todo texto nuevo está marcado **(propuesta)**; ninguno proviene de investigación hecha. Ningún original fue modificado.

## 0. Decisión de segmento (resuelta por el equipo)

Las propuestas anteriores comparaban un segmento de hogares con niños con otro centrado solo en quienes reportan incidencias. El equipo aclaró que **no es ni una cosa ni la otra**: el segmento son los **hogares de la Ciudad en general**, y **cada hogar tiene su realidad**. Eso es justamente lo que justifica un perfil por hogar. Los «tipos de hogar» (hogar con niños, adulto mayor, persona con movilidad reducida) pasan a ser **personas** para Design Thinking y para las demos, no segmentos distintos del Canvas.

**Coherencia con el Charter.** El Charter excluye *«perfil personal avanzado o personalización basada en datos sensibles que no sean necesarias para los objetivos definidos»* (§5.5.2). La exclusión es **condicional**: un **perfil de hogar básico** (dato mínimo declarado por el propio hogar, opt-in) **no está excluido**. Se propone una oración aclaratoria en `01-charter-condensado.md`: *perfil de hogar básico INCLUIDO; personalización avanzada y datos sensibles no necesarios EXCLUIDOS del MVP*.

## 1. Segmento (plantilla de la Clase 1: *[quiénes] que [situación] y hoy [dolor]*) *(propuesta)*

- **Lado hogar (externo):** **Hogares de la Ciudad** *[quiénes]* que **conviven con su propia mezcla de necesidades** —trámites, servicios, obras y reclamos de su entorno, movilidad— *[situación]* y hoy **deben saber de antemano qué preguntar, a qué organismo y por qué canal, y no ven qué pasó con lo que reportan** *[dolor]*. (Dolor tomado de la visión del equipo y del §5.3 del Charter.)
- **Lado áreas (interno):** *áreas de gobierno que gestionan incidencias y servicios y hoy reciben información dispersa, duplicada y sin una referencia geográfica común.* (§5.3.1.)
- **Tercer lado, opcional:** socios con oferta geolocalizada (Banco Ciudad, Pase Cultural, DisfrutemosBA); **fuera de la primera implementación** (§5.5.2, §10.1).

## 2. Personas: cada hogar tiene su realidad *(propuesta; son escenarios, no segmentos)*

Sirven para las proto-personas de Design Thinking (ver `05b-design-thinking-revisado.md`), para decidir qué muestra el perfil de hogar básico y, más adelante, para un mock. Salen de los textos del propio equipo.

| Persona (escenario de uso) | Situación del hogar | Qué necesita | Cómo se vería |
|---|---|---|---|
| **Hogar con niños en edad escolar** | Se entera tarde de la inscripción o la vacunación | Saber qué le corresponde y cuándo, sin buscar | Aviso proactivo sobre el mapa, según el perfil de hogar básico (opt-in) |
| **Persona con movilidad reducida** | No sabe qué veredas de su recorrido están en obra | Recorridos y obras de su cuadra | Capa de obras y cortes sobre el recorrido |
| **Adulto mayor** | No sabe qué trámites le corresponden | Un lugar donde ver y pedir lo que le toca | Vista del hogar con trámites y puntos cercanos |
| **Vecino que reporta** | Se cruza con una incidencia y no sabe a quién avisar | Reportar y ver qué pasó | Reporte con ubicación y estados hasta el cierre |

Las cuatro comparten el **mismo segmento** (hogares de la Ciudad) y la **misma plataforma**; cambia lo que cada hogar ve primero.

## 3. Mapa de valor del lado hogar *(propuesta; formato Clase 1, p8–9)*

| Perfil del cliente | Mapa de valor |
|---|---|
| **Tareas:** enterarse de lo que le corresponde al hogar; informar una incidencia de su entorno; saber si otro ya la informó; consultar qué pasa en su cuadra. | **Propuesta de valor:** un único lugar sobre el mapa donde cada hogar ve lo que le corresponde y reporta y sigue lo que ve, con estado visible de principio a fin. |
| **Frustraciones:** no saber qué organismo o canal corresponde; enterarse tarde; no ver qué pasó con el reporte; información duplicada o desactualizada. | **Aliviadores:** punto único con ubicación; perfil de hogar básico (dato mínimo, opt-in) para mostrar primero lo que importa; estados visibles (Reportado → … → Cerrado). |
| **Beneficios esperados:** que el reporte llegue a quien corresponde; enterarse del avance; confiar en que el dato es oficial y actual. | **Generadores de satisfacción:** disponible también desde canales ya usados (Boti, BAX, **sujeto a validación técnica**). |

## 4. Mapa de valor del lado GCBA (quien financia y decide) *(propuesta)*

| Perfil del cliente | Mapa de valor |
|---|---|
| **Tareas:** gestionar incidencias y servicios con el equipo que tiene; coordinar áreas; justificar el presupuesto. | **Propuesta de valor:** la **vista de gestión** (dónde se concentran las incidencias y en qué estado están) y una **capa geográfica reutilizable** por otros servicios. |
| **Frustraciones:** cada área mantiene su solución geográfica; no hay una vista única; se reconstruye la capa en cada iniciativa (§5.3.1). | **Aliviadores:** una referencia geográfica común; costos evitados por no duplicar soluciones; menos esfuerzo para derivar casos. |
| **Beneficios esperados:** ver y priorizar; mostrar resultados con datos. | **Generadores de satisfacción:** datos para decidir dónde intervenir; la capa la consumen canales existentes. |

Son **dos propuestas de valor** porque son **dos segmentos**: quien usa (el hogar) no es quien paga (GCBA). Esa es la característica de la plataforma multilateral.

## 5. Canales, relación con el cliente e ingresos *(consistente con §5.8.4 y §10; propuesta)*

| Bloque | Texto propuesto |
|---|---|
| **Canales** | Web del Mapa; Boti (WhatsApp de la Ciudad); BAX (sujeto a validación técnica y a miBA) |
| **Relación con el cliente** | Autoservicio con seguimiento del reporte; avisos proactivos solo con opt-in; vista de gestión para las áreas |
| **Ingreso principal** | Partida de modernización de servicios digitales del GCBA (Hacienda / Presupuesto), primera implementación |
| **Costos evitados** | Cada área que deja de mantener su propia solución: argumento para el sponsor, a medir |
| **Socios (fase futura)** | Convenios con socios (comisiones, canjes) y espacios patrocinados: fuera del presupuesto actual |
| **Hogares** | No pagan |

El presupuesto se expresa en **USD** (ver `03-presupuesto`): quién paga no cambia, cambia la moneda de presentación.

## 6. Objetivos SMART *(propuesta)*

Se parte de la nota del propio Charter: agrupar los 8 objetivos en **4 resultados**. Cada uno se escribe con las cinco letras de la Clase 1 (específico, medible, alcanzable, relevante, con plazo). Las **metas numéricas son propuestas** y las líneas base están **«a medir»**.

| Resultado | Objetivos del Charter | Meta SMART *(propuesta)* | Plazo | ¿Cómo se verifica? |
|---|---|---|---|---|
| **O1 · Capa geográfica confiable** | 1 + 7 | La capa integra las **fuentes priorizadas** [completar: Transporte y Cultura son las que nombra el equipo] y el 100 % tiene responsable y frecuencia de actualización definidos. | 02/07/2026 (Gate 4) | Registro de fuentes con responsable y frecuencia |
| **O2 · Integración multicanal** | 2 | El Mapa y **al menos 1 canal conversacional** consumen la capa por API (BAX sujeto a validación técnica y a miBA). | 21/07/2026 (Gate 5) | Pruebas de intercambio de datos aprobadas |
| **O3 · Reportes y seguimiento** | 3 + 4 + 5 | El 100 % de los casos de prueba del flujo completo (reporte, validación, derivación, resolución, cierre) aprobados; los 6 estados operativos. | 27/08/2026 (Gate 6) | Informe de pruebas (actividades 27–32) |
| **O4 · Gestión y experiencia del hogar** | 6 + 8 | **≥ 3 áreas operativas** acceden a la vista de gestión y actualizan estados, y el hogar ve la información relevante de su entorno con el **perfil de hogar básico (opt-in)**; línea base de consultas evitables: a medir. | 09/09/2026 (Gate 7) | Registro de accesos y capacitación (actividades 34–35); prueba del perfil básico |

*Metas de uso post-cierre* (cantidad de reportes validados, hogares con perfil activo, tiempo de resolución): línea base **«a medir»**; no se afirman cifras.

## 7. Design Thinking: investigación simulada, rotulada y coherente

**Decisión del grupo.** Las entrevistas del deck son inventadas y **no hace falta hacer entrevistas reales**. Lo honesto y más defendible es **rotular la investigación como simulada** (ejercicio académico): proto-personas e hipótesis apoyadas en fuentes públicas, sin citas ni conteos inventados. En la defensa, la pregunta *«¿a cuántas personas entrevistaron y qué encontraron?»* tiene una respuesta coherente: *«es una investigación simulada, declarada como tal; la validación con hogares es la actividad 5 del Gantt»*.

**Qué hay que cambiar en el deck** (texto exacto, slide por slide, en `05b-design-thinking-revisado.md`): la portada pasa a «Hogares de la Ciudad × áreas del GCBA»; la slide de Empatizar pasa a **Investigación simulada** con hipótesis H1–H3; las proto-personas pasan de una a tres; «Mi hogar» queda como **decisión del grupo**; se quita el texto suelto «→ Cambiarla». También están ahí la trazabilidad con el Canvas, el Charter, el Gantt y los riesgos, y el texto de la sección 4 del documento.

*Criterios de la Clase 7: a confirmar con el PDF de la cátedra, que todavía no está en la carpeta.*

**Para después:** un *mock* de una funcionalidad (por ejemplo, el seguimiento de un reporte o la vista del hogar con su perfil básico) para mostrar cómo se vería. Se hace al final, con el documento cerrado; no se construye ahora.
"""
    write("05-canvas-dt-smart.md", txt)


def render_coherence(c, ck):
    o, lb, la, res = c["o"], c["lb"], c["la"], c["res"]
    rows_now = [
        ["Hitos Charter = Gantt", "Parcial: los 8 hitos del Excel = §6.3 = resumen, pero §5.12 no tiene fechas, §6.5 lista 7 puntos y la tabla de fases del resumen no coincide con el Excel", "8 gates con la fecha del Excel, iguales en Charter, Gantt y resumen"],
        ["Presupuesto del Charter = total", "No: el Charter §5.8 no da cifra", f"El Charter cita {usd(lb['total'])} (B) o {usd(la['total'])} (A)"],
        ["Riesgos Charter ⊂ matriz", "Parcial: 12 vs 15; «comercios» no está en la matriz", "Los 5 riesgos del Charter son un subconjunto con IDs"],
        ["Contingencia = Σ EMV", "No: 10 % plano", f"{usd(lb['contingency'])} = Σ EMV residual"],
        ["Mano de obra = duraciones del Gantt", "Parcial: 2 de 4 comparables no cierran", "Cada rol usa los días hábiles de sus actividades"],
        ["Stakeholders Charter ∈ matriz ∈ comunicación", "No: dos actores sin fila de comunicación; roles del §5.11 distintos del PDF", "Lista única de 9; +2 filas en la matriz de comunicación"],
        ["Frase puente por sección", "Mayormente sí desde la sección 6; faltan 3–5", "Frases puente propuestas para 3 a 10"],
    ]
    rows_new = [[k.name, "✓" if k.ok else "✗", k.detail] for k in ck]
    bridges = [[k, v] for k, v in D.BRIDGES.items() if k.isdigit()]
    freeze = [
        ["Nombre del proyecto", "«Modernización del Mapa Interactivo de la Ciudad» (el resumen dice «…y Ampliación… de Buenos Aires»)"],
        ["Fechas", "01/04/2026 inicio de la Fase 1; Charter 10/04; cierre 30/09/2026; entrega 14/10/2026"],
        ["Gates", "8 gates (G1–G8) con las fechas del Excel (sin cambios); G2 = 01/05 (feriado real: ver `02-gantt`, punto 5)"],
        ["Dependencias del Gantt", "Listas explícitas («5, 6»), nunca «a-b»; actividades 2 y 3 como inicio-a-inicio +1 día (ver `02-gantt`)"],
        ["Riesgos", "IDs R01–R15 del documento largo (+R16–R19); una sola matriz"],
        ["Moneda", f"**USD** en todo el documento; equivalente en pesos solo como referencia («ARS … M»)"],
        ["Tipo de cambio", f"ARS {n(o['fx']['value'], 2)} por USD · {o['fx']['date']} · Banco Nación, dólar oficial (venta) · **a confirmar**; una sola constante recalcula todo"],
        ["Segmento", "**Hogares de la Ciudad** (cada hogar con su propia realidad); hogar con niños, adulto mayor y movilidad reducida son **personas** de Design Thinking, no segmentos"],
        ["Perfil de hogar", "**Básico** (dato mínimo declarado, opt-in) **incluido**; personalización avanzada o con datos sensibles no necesarios **excluida** del MVP (aclaración propuesta para §5.5.1/§5.5.2)"],
        ["Presupuesto", f"Una sola cifra total en USD (escenario A {usd(la['total'])} o B {usd(lb['total'])}) citada igual en Charter, sección 10 y conclusión; reserva de contingencia {usd(lb['contingency'])}; mantenimiento posterior {usd(o['maint_usd'])} fuera de la línea base"],
        ["Stakeholders", "Los nombres del PDF §7.1 (15 filas); los 9 principales para el Charter"],
        ["Sponsor", "«Sponsor institucional de Modernización de CABA» (el resumen: «Autoridad Institucional de Modernización»; confirmar denominación vigente)"],
        ["Fuentes priorizadas", "Transporte y Cultura (las que nombran el resumen y el PDF); el documento largo solo dice «seleccionadas»: **completar**"],
        ["Nómina del equipo", "Una sola lista: la cantidad de nombres cambia según el archivo (8, 9 y 10) y hay un apellido sin completar"],
    ]
    merge = [
        ["Documento base", "**«Proyect Charter y demas puntos»** (secciones 5 a 10 completas)"],
        ["1 Carátula", "«TP Grupo 01» (única carátula; revisar logo y nómina)"],
        ["2 Índice", "Se rehace al final con páginas reales"],
        ["3 Canvas · 4 Design Thinking", "Documento resumido como punto de partida, reescritos con `05-canvas-dt-smart.md`"],
        ["5 Charter", "Condensado de `01` + Anexo A con el texto largo"],
        ["6 Gantt", "Imagen y hitos del largo + tabla de `02-gantt`"],
        ["7 · 8", "PDF «corregido» (reemplaza el cuerpo; agregar 2 filas en la matriz de comunicación)"],
        ["9 · 10", "Largo + EMV y escenarios de `04` y `03`"],
        ["Storytelling", "«Conexión narrativa» del resumen como idea; frases puente de abajo"],
    ]
    dev = 3
    dev_days = res[18]["ef"] - res[18]["es"]
    phase4 = o["phase_wd"][4]
    txt = f"""
# Coherencia: qué se congela, cómo se fusiona y si el proyecto tiene sentido

> **Propuesta.** Ningún original fue modificado; esto es la guía para que, al unificar, todas las secciones digan lo mismo.

## 1. Mapa de fusión

{table(['Sección', 'Fuente'], merge)}

## 2. Datos a congelar (una sola fuente de verdad)

{table(['Dato', 'Valor a usar'], freeze)}

## 3. Checklist de coherencia (7 puntos)

**Estado hoy** (según la revisión) y **resultado con las propuestas** (calculado por `tools/coherence.py` sobre los números propuestos):

{table(['Control', 'Hoy', 'Con la propuesta'], rows_now)}

Verificación automática (el script **lee los documentos generados** y los compara contra el cronograma recalculado desde sus fechas):

{table(['Control', 'OK', 'Detalle'], rows_new)}

## 4. Frases puente propuestas (apertura de cada sección)

{table(['Sección', 'Frase'], bridges)}

## 5. ¿Tiene más o menos sentido el proyecto?

**Veredicto: sí tiene sentido, con un recorte.** El problema es real y concreto, el modelo de dos lados (vecino y GCBA) explica quién usa y quién paga, y el cronograma y el presupuesto ya cierran entre sí. El riesgo no es la idea: es el **tamaño**.

- **Alcance vs. tiempo:** 8 objetivos, 8 entregables y 4 canales (Mapa, Boti, BAX, miBA) en {o['calendar']['span_wd']} días hábiles (01/04–30/09). La **Fase 4 (desarrollo) dura {phase4} días hábiles**; con 3 desarrolladores son ≈ **{3 * phase4} días-persona para 6 componentes** (≈ {n(3 * phase4 / 6, 0)} por componente). Un profesor puede decir que es optimista.
- **Datos personales:** el reporte lleva ubicación y el perfil de hogar básico agrega datos del hogar; el marco legal (**Ley 25.326**) está **sin verificar** en los documentos. Debe aparecer en supuestos, riesgo R10 y requisitos (dato mínimo, opt-in).
- **Dependencias externas:** Boti, BAX y miBA no están bajo control del proyecto (R12, R18).
- **Participación ciudadana:** el valor depende de que los vecinos reporten y validen (R06); sin esa masa crítica el módulo pierde sentido.

### Qué desafiaría un profesor *(y qué responder)*

| Pregunta | Respuesta propuesta |
|---|---|
| ¿Por qué el proyecto «empezó» en abril? | Simulación declarada en una línea (supuesto de simulación). |
| ¿Cuál es el camino crítico? | Según el CPM del Excel: {o['calendar']['cpm_wd']} d.h. y {o['n_critical']} actividades sin holgura (cadena {', '.join(map(str, o['critical_path']))}); con las dependencias corregidas cambia (ver `02-gantt`). |
| ¿Cómo calcularon la contingencia? | Σ EMV residual = {usd(lb['contingency'])}; sensibilidad en `03`. |
| ¿Con cuánta gente se desarrolla todo eso en {phase4} días? | Escenario B con 3 desarrolladores + MVP recortado (abajo). |
| ¿Quién paga y qué recibe cada lado? | GCBA paga y recibe la vista de gestión; el vecino no paga y recibe seguimiento de su reporte. |
| ¿Hay evidencia de usuarios? | No: la investigación está rotulada como **simulada** (hipótesis); no se afirman entrevistas (`05b`). |
| ¿Qué pasa si BAX/Boti/miBA cambian? | R12 y R18; BAX queda sujeto a validación técnica. |
| ¿Cómo tratan los datos personales? | Minimización, controles de acceso, R10; **Ley 25.326, a verificar**. |

### MVP recortado (propuesta, coherente con la Opción B)

| Entra en la primera implementación | Fase futura |
|---|---|
| Capa geográfica con **2 fuentes priorizadas** (Transporte y Cultura) | Más fuentes y áreas |
| Reportes con **pocas categorías** (calle cortada, vehículo detenido, obstáculo) | Nuevas categorías |
| Validación colaborativa simple (confirmar / ya no está) | Reputación y moderación avanzada |
| Estados Reportado → Validado → Derivado → Resuelto → Cerrado (**5**; «En gestión» queda opcional) | Estados por área |
| Integración con **Mapa + Boti** | **BAX** y miBA (sujetos a validación) |
| Vista de gestión **básica** (listar y filtrar) | Tableros analíticos |
| **Perfil de hogar básico** (dato mínimo declarado, opt-in) | Personalización avanzada y uso de datos sensibles |
| — | Socios, beneficios, publicidad |

Esto es **consistente con §5.5.2**: la exclusión alcanza solo a la personalización avanzada o con datos sensibles *no necesarios*. Baja el riesgo de R05 (alcance).

## 6. Orden de magnitud del total

- **Verificado:** que las sumas cierran, que la duración de la mano de obra sale del Gantt y que la contingencia sale de los EMV.
- **Supuesto:** las **tarifas** (las del equipo; no contrastadas con datos de mercado), las personas por rol, la escala de impactos y el tipo de cambio (a confirmar). Con la escala a la mitad o ×1,5 la contingencia queda entre {usd(o['sensitivity']['0.5']['contingency'])} y {usd(o['sensitivity']['1.5']['contingency'])}; con el dólar ±20 %, el total B queda entre {usd(o['fx_sens']['1.2']['total_b'])} y {usd(o['fx_sens']['0.8']['total_b'])}.
- El total depende sobre todo de **tarifas × personas**: son las dos cosas que el grupo debe acordar y poder defender.
"""
    write("06-coherencia.md", txt)


def render_summary(c, ck):
    o, lb, la = c["o"], c["lb"], c["la"]
    fx = o["fx"]
    rows = [
        ["1 · Gantt: ya tiene duraciones, dependencias y camino crítico; mejoras puntuales", f"**Corrección de nuestro análisis anterior:** el Excel ya trae todo eso (CPM de {o['calendar']['cpm_wd']} d.h., {o['n_critical']} críticas, 8 hitos). Ajustes: la notación «a-b» es ambigua ({o['calendar']['cpm_wd']} vs {o['calendar']['range_wd']} d.h.), {len(o['gantt']['corrected_cells_range'])} celdas de dependencias contradicen las fechas, la columna Responsable está vacía y el camino crítico cambia al corregirlas", "`02-gantt/`", "S", "Quien armó el Gantt"],
        ["2 · Presupuesto sin trazabilidad", f"Mano de obra = personas × tarifa × duración del Gantt; contingencia = Σ EMV ({usd(lb['contingency'])}, {pct(lb['contingency'] / lb['project_costs'])} de costos, vs 10 % plano); reserva de gestión. En USD: escenario A {usd(la['total'])} / B {usd(lb['total'])}", "`03-presupuesto/`, `04-riesgos.md`", "M–L", "Todo el grupo (tarifas y personas)"],
        ["3 · Versiones que se contradicen", "IDs maestros R01–R15 (+R16–R19); 8 gates; una nómina; eliminar la nota de chat y «Resumen y borrador»", "`04-riesgos.md`, `06-coherencia.md`", "S", "Coordinador"],
        ["4 · Canvas, Design Thinking y SMART débiles", "Opción B con segmento **«Hogares de la Ciudad»** (cada hogar con su realidad; los tipos de hogar son personas), dos propuestas de valor, 4 objetivos SMART y Design Thinking como **investigación simulada** rotulada, con tres proto-personas y copia revisada de las slides (`05b`)", "`05-canvas-dt-smart.md`", "M", "Grupo (+ consulta a los profesores)"],
        ["5 · Charter muy largo (≈ 6.000 palabras)", "**Charter en la plantilla de la cátedra** (24 campos en 3 partes), completo y conciso, con la aclaración del perfil de hogar básico; mapa de los 13 elementos de la Clase 3 a los 24 campos; el texto actual pasa a Anexo A", "`01-charter/Project_Charter_completado.docx`, `01-charter/README.md`, `01-charter-condensado.md`", "S–M", "Grupo"],
        ["6 · Formato y prolijidad (pedido del Prof. Armando)", "**Un solo documento** con los 10 puntos en el orden de la consigna, una guía de estilo única, índice automático, 10 frases puente y checklist de 20 puntos; plan de 2 días", "`07-formato-entrega.md`", "M", "Coordinador + una persona de formato"],
        ["7 · Presupuesto: cómo se construyen los números (pedido del Prof. Pacheco)", f"Presupuesto en **USD** con un único tipo de cambio (ARS {n(fx['value'], 2)}, {fx['date']}), desglosado en {len(o['lines'])} líneas con paquete de trabajo, tipo de costo, método (Clase 4), cantidad × costo unitario × duración y mes; explicación con 3 ejemplos; **auditoría contra la Clase 4** (corrige una comparación que mezclaba alcances) y memoria de cálculo de una página", "`03-presupuesto/presupuesto.md`, `auditoria.md`, `memoria-de-calculo.md`, `desglose.csv`", "M", "Todo el grupo"],
        ["8 · Guion narrativo (el hilo entre secciones)", "Papel de cada sección, objetos del hilo con valor único (segmento, hitos, duración, USD, tipo de cambio, riesgos), 10 frases puente con el contenido final, resumen ejecutivo y tabla de consistencia", "`08-guion-narrativo.md`", "S", "Coordinador"],
    ]
    txt = f"""
# Para llevar al equipo: propuestas de mejora

> Los archivos originales de `trabajo-grupal/` **no se tocaron**. Esto es lo que proponemos, listo para discutir. Todo número nuevo es **propuesta**; lo desconocido está marcado **a confirmar**. Las fechas simuladas (01/04–30/09/2026, entrega 14/10) **se mantienen**: se agrega una línea que lo declara. **Quedan 2 días** (12/10 → 14/10): el plan está en `07-formato-entrega.md`.

## Qué dijeron los profesores y qué cambia

| Devolución | Qué hacemos |
|---|---|
| **Prof. Armando:** *«mejorar el orden de los puntos, el formato, prolijidad»* | Un solo documento con el orden de la consigna y una guía de estilo (problema 6). |
| **Prof. Pacheco:** *«se ven bien, todavía faltan varios puntos»; «en el presupuesto, dar más detalle de cómo construyen los números»* | Revisar contra los 10 puntos de la consigna (problema 6) y presupuesto desglosado en USD (problema 7). |

## Los 8 puntos y qué proponemos

{table(['Problema', 'Propuesta', 'Leer', 'Esfuerzo', 'Decide'], rows)}

## ¿Tiene más o menos sentido el proyecto?

**Sí**: el problema es real y el modelo de dos lados cierra. El riesgo es el **tamaño**: {o['phase_wd'][4]} días hábiles de desarrollo para 6 componentes y 4 canales. Propuesta: **MVP recortado** (Mapa + Boti; 2 fuentes; BAX y miBA a fase futura; **perfil de hogar básico sí, personalización avanzada no**). Los números **cierran entre sí**, aunque las tarifas, las personas por rol y el tipo de cambio son supuestos a acordar. Detalle en `06-coherencia.md`.

## Decisiones que hay que tomar entre todos

1. **Presupuesto:** escenario **B** ({usd(lb['total'])}, mano de obra desde el Gantt; **recomendado**) o **A** ({usd(la['total'])}, mínimo esfuerzo). Regla de corte en `03-presupuesto`.
2. **Moneda y tipo de cambio:** USD, con ARS {n(fx['value'], 2)} por USD ({fx['date']}, **a confirmar**) como constante única.
3. **Segmento:** **hogares de la Ciudad en general**; hogar con niños, adulto mayor y persona con movilidad reducida son **personas** de Design Thinking.
4. **Perfil de hogar básico** (dato mínimo, opt-in) **incluido**; personalización avanzada excluida del MVP: oración aclaratoria para §5.5.
5. **Gantt:** opción A (corregir {len(o['gantt']['corrected_cells_range'])} celdas de dependencias y escribirlas explícitas), B (registrar adelantos) o solo la nota mínima; los 8 gates **no cambian de fecha** (Gate 2 sigue el 01/05; simulación lunes a viernes sin feriados, declarada en una línea).
6. **Tarifas y personas por rol** (supuestos del grupo).
7. **Charter condensado** con Anexo A, o dejarlo largo.
8. **Formato de entrega:** un solo documento (Word → PDF) con el Excel del Gantt como anexo.
9. **Design Thinking:** decidido que la investigación es **simulada** y se rotula como tal (sin entrevistas reales); falta elegir si «Mi hogar» entra al prototipo (opción A) o queda fuera del MVP (opción B), ver `05b`.

## Para después

Un **mock** de alguna funcionalidad (por ejemplo, el seguimiento de un reporte o la vista del hogar con su perfil básico) para mostrar cómo se vería: se hace **al final**, con el documento cerrado. No se construye ahora.

## Verificación

- {len(ck)} controles de coherencia propuestos: {sum(1 for k in ck if k.ok)} en verde.
- Los gates, el CPM del Excel (lecturas, escenarios y camino crítico) y los totales se calculan con `tools/` a partir del Excel del equipo (todo recalcula con `bash tools/run-all.sh`; el presupuesto también con otro tipo de cambio: `python3 03-presupuesto/model.py 1800`).
- **Sin verificar:** denominaciones vigentes de áreas, el texto de la Ley 25.326, el traslado del feriado del 15/06, el tipo de cambio contra el cierre oficial, las tarifas contra datos de mercado y que las correcciones del Gantt sean las que quiso escribir quien armó el Excel (se deducen de las fechas).
"""
    write("00-resumen.md", txt)
