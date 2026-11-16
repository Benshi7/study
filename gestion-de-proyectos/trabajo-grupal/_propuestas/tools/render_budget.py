"""Renders 03-presupuesto/presupuesto.md (USD, itemised) from the computed numbers."""
import pathlib

import costing as cs
import data as D
from fmt import ars, n, pct, table, u, usd, usd2

ROOT = pathlib.Path(__file__).resolve().parent.parent


def write(rel, text):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text.strip() + "\n", encoding="utf-8")


def _short(l):
    return f"{l['comportamiento'][0]}/{l['asignacion'][0]}"          # F/D = Fijo/Directo, V/D = Variable/Directo


def _qty_x_unit(l):
    """The arithmetic exactly as a calculator reproduces it: unit price (with cents) x working days / 21 (x people)."""
    if l["unidad"] == "global":
        return f"1 global × {usd(l['unit_usd'])}"
    if l.get("role"):
        return f"{l['qty']} pers. × {usd2(l['unit_usd'])}/mes × {l['workdays']} ÷ 21"
    return f"1 servicio × {usd2(l['unit_usd'])}/mes × {l['workdays']} ÷ 21"


def _dur(l):
    return f"{l['workdays']} d.h. = {n(l['duracion_meses'], 2)} m" if l["duracion_meses"] is not None else "post-cierre"


def render(c):
    o, la, lb = c["o"], c["la"], c["lb"]
    fx = o["fx"]["value"]
    lab, lines, cats = o["labour"], o["lines"], o["categories"]
    costs_b, cont = lb["project_costs"], lb["contingency"]
    team = o["team_usd"]
    maint = o["maint_usd"]
    team_costs_no_maint = sum(c_["team"] for k, c_ in cats.items() if k != "mant")
    a_costs_no_maint = team_costs_no_maint

    # ---- desglose tables, one per category
    desglose = []
    for key, label in D.CATEGORIES:
        rows = []
        for l in (x for x in lines if x["cat"] == key):
            rows.append([l["id"], l["concepto"], l["wp"], _short(l), l["metodo"].split(" (")[0], _qty_x_unit(l), _dur(l), usd(l["usd_b"]), l["meses"], l["supuesto"]])
        sub = cats[key]["b"]
        note = " (fuera de la línea base)" if key == "mant" else ""
        rows.append(["", f"**Subtotal {label[0].lower() + label[1:]}{note}**", "", "", "", "", "", f"**{usd(sub)}**", "", ""])
        desglose.append(f"### {label}\n\n" + table(["ID", "Concepto", "Paquete de trabajo (Gantt)", "F/V · D/I", "Método", "Cantidad × costo unitario", "Duración", "Subtotal (USD)", "Meses", "Supuesto"], rows))

    # ---- labour table
    rows_lab = []
    for r in lab:
        rows_lab.append([r["label"], f"{r['team_months']} m", usd(r["cost_a"]), usd(r["rate_usd"]) + "/mes", f"{r['wd']} ({n(r['months'], 2)} m)",
                         n(r["qty_a"], 2), usd(r["cost_a"]), r["qty_b"], usd(r["cost_b"])])
    rows_lab.append(["**Total mano de obra**", "", f"**{usd(o['labour_a'])}**", "", "", "", f"**{usd(o['labour_a'])}**", "", f"**{usd(o['labour_b'])}**"])
    team_vs = [[r["label"], f"{r['team_months']}", n(r["months"], 2), "no" if abs(r["team_months"] - r["months"]) > 0.25 else "sí"] for r in lab]

    # ---- worked examples
    dev = next(x for x in lab if x["key"] == "dev")
    hosting = next(x for x in lines if x["id"] == "INF1")
    r01 = next(x for x in o["risks"]["sorted"] if x["id"] == "R01")
    prob = D.SCALE["prob"][r01["pr"]]
    imp_usd = cs.usd_of(D.SCALE["impact_M"][r01["ir"]], fx)
    top3 = o["risks"]["sorted"][:3]

    comp = [
        ["Costos del proyecto (sin reservas)", usd(team_costs_no_maint), usd(a_costs_no_maint), usd(costs_b)],
        ["Mantenimiento inicial posterior al cierre", usd(maint), usd(maint), "fuera de la línea base"],
        ["Reserva de contingencia", usd(team["contingency"]) + " (10 % plano)", usd(la["contingency"]) + " (Σ EMV)", usd(cont) + " (Σ EMV)"],
        ["Línea base de costos", "—", usd(la["baseline"]), usd(lb["baseline"])],
        ["Reserva de gestión", "no existe", "no definida", usd(lb["mgmt_reserve"]) + " (10 %)"],
        ["**Total**", f"**{usd(team['total'])}**", f"**{usd(la['total'])}**", f"**{usd(lb['total'])}**"],
        ["Total con mantenimiento posterior", usd(team["total"]), usd(la["total"]), usd(o["all_in_b"])],
        ["Equivalente en ARS (referencia, al tipo de cambio)", ars(D.TEAM_TOTAL), ars(la["total"] * fx / 1e6), ars(lb["total"] * fx / 1e6)],
    ]
    fx_rows = [[f"×{k.replace('.', ',')}", n(v["fx"], 2), usd(v["costs_b"]), usd(v["contingency"]), usd(v["total_a"]), usd(v["total_b"])] for k, v in o["fx_sens"].items()]
    sens_rows = [[f"×{k.replace('.', ',')}", usd(v["contingency"]), pct(v["pct_of_costs_b"]), pct(v["pct_of_costs_a"])] for k, v in o["sensitivity"].items()]
    cash_rows = [[k[-2:] + "/" + k[:4], usd(o["cash"][k]), usd(o["cum"][k])] for k in o["cash"]]
    cat_rows = [[cats[k]["label"], usd(cats[k]["b"]), pct(cats[k]["b"] / (costs_b + maint))] for k, _ in D.CATEGORIES]
    short = {"pm": "PM", "af": "analistas", "dev": "desarrolladores", "gis": "datos/GIS", "ux": "UX/UI", "qa": "QA", "sec": "seguridad", "infra": "infraestructura", "doc": "documentación"}
    people_b = ", ".join(f"{short[r['key']]} {r['qty_b']}" for r in lab)
    implied = [usd(r["rate_usd"]) for r in lab]

    br, pyr = o["bridge"], o["pyramid"]
    bridge_rows = [["Total del equipo, convertido (incluye el mantenimiento inicial)", "—", usd(team["total"])]]
    for s in br["steps"]:
        bridge_rows.append([s["name"], ("+" if s["delta"] >= 0 else "−") + usd(abs(s["delta"])), usd(s["running"])])
    bridge_rows.append(["**Escenario B con mantenimiento inicial**", "", f"**{usd(o['all_in_b'])}**"])
    bridge_reasons = "\n".join(f"{i}. **{s['name']}:** {s['reason']}" for i, s in enumerate(br["steps"], 1))
    pyr_rows = [
        ["**Presupuesto**", f"**{usd(pyr['total'])}**", "Línea base + reserva de gestión"],
        ["Reserva de gestión (10 %)", usd(pyr["mgmt_reserve"]), "Imprevistos no identificados; requiere aprobación de la dirección (p19)"],
        ["**Línea base de costos**", f"**{usd(pyr['baseline'])}**", "Proyecto + reserva de contingencia"],
        ["Reserva de contingencia", usd(pyr["contingency"]), "Suma de los EMV de los riesgos identificados"],
        ["**Proyecto**", f"**{usd(pyr['project'])}**", f"Suma de los {pyr['n_packages']} paquetes de trabajo (líneas del desglose)"],
    ] + [[f"↳ Centro contable: {c_['label']}", usd(c_["usd"]), "Suma de sus paquetes de trabajo"] for c_ in pyr["centers"]]
    pyr_rows.append([f"↳ Paquetes de trabajo ({pyr['n_packages']})", "—", "Cada uno referido a actividades del Gantt (columna «Paquete de trabajo» del desglose)"])
    total_p17 = costs_b + maint
    p17_rows = [[g["rubric"], ", ".join(g["ids"]) if g["ids"] else "—", usd(g["usd_b"]) if g["ids"] else "no previstos (no aplica)",
                 pct(g["usd_b"] / total_p17) if g["ids"] else "0,0 %"] for g in o["p17"]]
    cum_base = o["cum_baseline"]
    cash_base_rows = [[k[-2:] + "/" + k[:4], usd(o["cash_baseline"][k]), usd(cum_base[k])] for k in o["cash_baseline"]]
    ind = o["indirect"]

    txt = f"""
# Presupuesto: de los pesos del equipo a un presupuesto en USD que se puede seguir número por número

> **Propuesta.** Responde al pedido del profesor: *«dar más detalle de cómo construyen los números»*. Se conservan **los importes y las tarifas del equipo** (están en pesos, §10); lo nuevo es (1) la **moneda de presentación en USD con un único tipo de cambio**, (2) el **desglose en {len(lines)} líneas** que muestran paquete de trabajo, tipo de costo, método, cantidad × costo unitario × duración y mes de incurrencia, (3) la **duración sale de las fechas del Gantt del equipo (Excel, punto 6)**, (4) la **contingencia sale de los EMV** y (5) la **reserva de gestión** explícita. Ningún original fue modificado. Archivos: `desglose.csv` (las {len(lines)} líneas con todos los campos), `model.csv` (mano de obra), `tools/` (recalcula todo).

## Moneda y tipo de cambio

**Tipo de cambio:** ARS {n(fx, 2)} por USD · {o['fx']['source']} · fecha de referencia {o['fx']['date']} · **a confirmar**.

- Todos los importes del equipo están en pesos (ARS). Se convierten a USD con **una sola constante** (`FX_ARS_PER_USD` en `tools/data.py`): cambiarla recalcula **todas** las cifras de este documento y de los demás.
- El tipo de cambio es un factor **Económico** del PESTEL (Clase 4, p7): por eso se lo trata como supuesto explícito y como riesgo (**R19**).
- Cada línea se redondea a USD enteros y los totales son **sumas de líneas ya redondeadas**: todas las tablas cierran.
- Si el equipo prefiere otra referencia (por ejemplo, el cierre oficial del día de entrega), se cambia la constante y se regenera.

### Sensibilidad al tipo de cambio

{table(['Tipo de cambio', 'ARS por USD', 'Costos del proyecto (B)', 'Contingencia', 'Total A', 'Total B'], fx_rows)}

A menor valor del dólar, más USD cuestan los mismos pesos; el equipo puede mostrar este cuadro como evidencia de que **entiende el efecto de la moneda** en el presupuesto.

## Cómo se construye cada número

Se sigue el orden de la Clase 4 (p15: planificar, estimar, presupuestar, controlar):

1. **Qué estimar** (p17: mano de obra, materiales, subcontratistas y asesores, alquiler de equipo e instalaciones, viajes, reservas de contingencia y de gestión): ver la tabla «Rubros de la Clase 4» más abajo; cada línea del desglose cae en un rubro.
2. **Duración (p16: «parte de la estimación de recursos (tiempos)»):** sale del **Gantt del equipo (Excel)**: las fechas Inicio–Fin de cada actividad. Para cada rol, días hábiles = unión de las actividades donde interviene (lunes a viernes, sin feriados, como el Excel); **21 días hábiles = 1 mes**.
3. **Costo por paquete de trabajo (p16):** `cantidad × costo unitario × duración`. Cada línea del desglose indica a qué fase y actividades del Gantt corresponde.
4. **Técnica de estimación (p18):** **paramétrica** para la mano de obra (tarifa mensual × personas × meses) y **experta** para el resto (el equipo dio importes globales sin cotizaciones). **No se usa estimación análoga**: no hay datos de proyectos anteriores en los documentos.
5. **Clasificación (p13–14):** **fijo/variable** (¿cambia con la cantidad de trabajo?) y **directo/indirecto** (¿beneficia solo a este proyecto?). Todas las líneas son **directas**; los costos indirectos están **declarados en cero** (sección «Costos indirectos»).
6. **Presupuestación (p15, p23, p24):** se suma «hacia arriba»: paquetes de trabajo → centros contables → proyecto; el acumulado mensual es la **curva S**.
7. **Reservas (p19–21):** **contingencia** = suma de los EMV de los riesgos identificados; **reserva de gestión** = porcentaje decidido por la dirección (10 %, el ejemplo de la cátedra, p21).

### Tres ejemplos resueltos

**a) Desarrolladores** (mano de obra, paramétrica): tarifa del equipo = {ars(dev['team_cost_ars'])} ÷ {dev['team_months']} meses = {ars(dev['rate_ars'])}/mes = **{usd(dev['rate_usd'])}/mes**. En el Gantt intervienen {dev['wd']} días hábiles = {n(dev['months'], 2)} meses. Con **{dev['qty_b']} personas** (propuesta B): {dev['qty_b']} × {usd(dev['rate_usd'])} × {n(dev['months'], 2)} = **{usd(dev['cost_b'])}**. (El equipo tenía {ars(dev['team_cost_ars'])} ≈ {usd(dev['cost_a'])}, que con esas duraciones equivale a ≈ {n(dev['qty_a'], 1)} personas.)

**b) Infraestructura y hosting** (`{hosting['id']}`, experta, fija, directa): el equipo estimó {ars(hosting['ars_team_m'])} = **{usd(hosting['usd_b'])}** para todo el período. Ventana del Gantt: {hosting['wp']} = {n(hosting['duracion_meses'], 2)} meses → **{usd(hosting['unit_usd'])}/mes implícito**. Es un valor a reemplazar por una **cotización**.

**c) Contingencia** (riesgo {r01['id']}, fórmula de la Clase 4 p20: probabilidad × impacto): probabilidad residual {pct(prob, 0)} × impacto de nivel {r01['ir']} ({usd(imp_usd)}) = **{usd(r01['emv_usd'])}**. La contingencia total es la **suma de los EMV residuales de los {o['risks']['n']} riesgos = {usd(cont)}**; los tres mayores son {', '.join(f"{t['id']} ({usd(t['emv_usd'])})" for t in top3)}.

## Qué estaba mal en el presupuesto original

- **Mano de obra = «meses × costo»**, sin personas, y los meses no salen del Gantt. Comparación con los días hábiles reales de cada rol (1 mes = 21 d.h.):

{table(['Rol', 'Meses del equipo', 'Meses según Gantt (1 persona)', '¿Coinciden (±0,25)?'], team_vs)}

- **Contingencia del 10 % plano** ({usd(team['contingency'])}), que no deriva de los riesgos y se calcula incluso sobre el mantenimiento posterior al cierre. No hay reserva de gestión (Clase 4, p19–21).
- El Charter (§5.8) enumera categorías pero **no da una cifra**; el total solo aparece en §10. Todo en pesos y sin tipo de cambio declarado.

## Mano de obra: personas × tarifa × duración del Gantt

{table(['Rol', 'Meses (equipo)', 'Costo equipo (USD)', 'Tarifa (USD/mes)', 'Días hábiles en el Gantt', 'Personas A', 'Costo A (USD)', 'Personas B', 'Costo B (USD)'], rows_lab)}

- **Escenario A:** conservar el costo de cada rol del equipo (convertido a USD). «Personas A» muestra cuántas personas implican con las duraciones del Gantt (≈ {n(lab[2]['qty_a'], 1)} desarrolladores y ≈ {n(lab[3]['qty_a'], 1)} en datos/GIS): **equipo chico para 6 componentes en paralelo**, algo que un profesor puede cuestionar.
- **Escenario B:** dimensionamiento propuesto (personas a tiempo completo durante la ventana de cada rol): {people_b}. Criterio principal: la Fase 4 tiene **3 frentes de desarrollo en paralelo** (capa geográfica, reportes y vista de gestión), de ahí 3 desarrolladores. Es una **propuesta a acordar**.

## Desglose completo (escenario B)

F/V = fijo/variable, D/I = directo/indirecto (Clase 4, p13–14). Método según la Clase 4, p18. «Cantidad × costo unitario» y «Duración» salen del Gantt; los costos unitarios de las líneas con importe global son **implícitos** (importe ÷ meses): se reemplazan por cotizaciones cuando existan. La **fuente** de todas las líneas que no son mano de obra es *«equipo (importe global, sin cotización) · a confirmar con cotización»*; en la mano de obra, *tarifa: equipo · personas: propuesta*. Detalle de campos en `desglose.csv`.

{(chr(10) * 2).join(desglose)}

### Peso de cada categoría

{table(['Categoría', 'Importe (USD)', '% del total con mantenimiento'], cat_rows)}

## Suma ascendente: de los paquetes de trabajo al presupuesto (Clase 4, p24)

La diapositiva de la cátedra arma el presupuesto de abajo hacia arriba: actividad → paquete de trabajo → centro contable → proyecto; al proyecto se le suma la **reserva de contingencia** (da la **línea base de costos**) y a la línea base la **reserva de gerencia** (da el **presupuesto**). Así queda el escenario B:

{table(['Nivel (Clase 4, p24)', 'Importe (USD)', 'Cómo se obtiene'], pyr_rows)}

El mantenimiento inicial ({usd(maint)}) ocurre **después del cierre**: queda fuera de la línea base y se informa aparte.

## Rubros de la Clase 4 (p17: «qué debemos estimar»)

{table(['Rubro (p17)', 'Líneas del desglose', 'Importe (escenario B)', '% del total con mantenimiento'], p17_rows)}

*Clasificación propuesta:* el original no distingue entre trabajo propio y contratado, por eso hay un rubro «otras actividades». Las **reservas** (contingencia y gestión) se muestran en la suma ascendente.

## Costos indirectos (Clase 4, p14 y p16)

{ind['declared']} **Importe: {usd(ind['usd'])}.** {ind['decision']}

## Escalera de reservas y comparación

{table(['Concepto', 'Hoy (equipo, convertido)', 'Escenario A', 'Escenario B'], comp)}

- **A (mínimo esfuerzo):** mismos costos, contingencia derivada de los riesgos. **No se puede conservar el total del equipo ({usd(team['total'])}):** la contingencia calculada ({usd(la['contingency'])}) supera los {usd(team['contingency'])} que había, así que el total sube {usd(o['gap_a_vs_team'])} ({pct(o['gap_a_vs_team'] / team['total'])}) o habría que recortar costos.
- **B:** mano de obra desde el Gantt con equipo proporcionado al alcance y reserva de gestión explícita: **{usd(lb['total'])}** hasta el cierre y **{usd(o['all_in_b'])}** con el mantenimiento inicial posterior. **La comparación correcta es contra el total del equipo, que también incluye el mantenimiento: {usd(o['all_in_b'])} contra {usd(team['total'])}, es decir {pct(br['like_for_like_pct'])} más.** (Comparar {usd(lb['total'])} contra {usd(team['total'])} daría {pct(br['until_closing_pct'])} y mezcla alcances distintos.)
- Con la escala de impactos propuesta, la **contingencia es el {pct(cont / costs_b)} de los costos de B** (el equipo había puesto 10 %). Depende de esa escala (ver sensibilidad: de {pct(o['sensitivity']['0.5']['pct_of_costs_b'])} a {pct(o['sensitivity']['1.5']['pct_of_costs_b'])}): lo que faltaba era la **trazabilidad**, no una cifra exacta.

### Puente comparable: del total del equipo al escenario B

{table(['Paso', 'Variación', 'Acumulado'], bridge_rows)}

{bridge_reasons}

Diferencia de redondeo: el total del equipo convertido **línea por línea** es {usd(team['total'])}; convertido **de una sola vez** ({ars(D.TEAM_TOTAL)} ÷ {n(fx, 2)}) da USD {n(D.TEAM_TOTAL * 1e6 / fx, 2)}: {n(abs(br['rounding_diff']), 2)} USD de diferencia, por redondear cada línea a dólares enteros.

## Recomendación para la entrega del 14/10

**Presentar el escenario B.** Razones: (1) es el que **responde literalmente** al pedido del profesor, porque cada número tiene fórmula, fuente y supuesto; (2) la mano de obra **concuerda con el Gantt** que se presenta en la sección 6 (con A, la sección 6 y la 10 se contradicen: analistas 3 meses contra {n(lab[1]['months'], 1)}); (3) **ya está calculado**: al equipo le quedan dos decisiones (personas por rol y tarifas) y pegar las tablas. **Regla de corte:** si no hay acuerdo sobre las personas por rol el 13/10 al mediodía, entregar **A** (se cambian solo la moneda y la contingencia) y dejar B en la defensa como mejora. En ambos casos: declarar el tipo de cambio y que las cifras son estimativas con fin académico.

### Sensibilidad de la contingencia a la escala de impactos (supuesta)

{table(['Escala de impacto', 'Contingencia', '% de los costos de B', '% de los costos de A'], sens_rows)}

## Curva S (escenario B, costos del proyecto por mes, alineados con el Gantt)

{table(['Mes', 'Costo del mes', 'Acumulado'], cash_rows)}

### Curva S de la línea base (con contingencia)

En la Clase 4 la línea base incluye la reserva de contingencia (p24). Para mostrarla, la contingencia se reparte **en proporción al costo de cada mes**:

{table(['Mes', 'Costo del mes + contingencia', 'Acumulado (línea base)'], cash_base_rows)}

La curva termina en **{usd(lb['baseline'])}** (la línea base). La reserva de gestión ({usd(lb['mgmt_reserve'])}) no se distribuye: se asigna cuando la dirección la autoriza (p19).

Cada línea se reparte parejo entre el primer y el último día de las actividades de su ventana (`desglose.csv`, columna «Paquete de trabajo»). La curva termina en **{usd(costs_b)}** (los costos del proyecto, **sin** reservas); las reservas se asignan a la línea base cuando se las usa. El mantenimiento inicial ({usd(maint)}) es posterior al cierre y queda fuera.

## Chequeos de cordura

{table(['Chequeo', 'Resultado'], [
    ['Las sumas cierran (líneas → categorías → total)', 'Sí: costos + contingencia + reserva = total, en A y en B; los totales son sumas de líneas redondeadas'],
    ['La curva S termina en los costos del proyecto', f'Sí ({usd(costs_b)})'],
    ['Mano de obra sobre costos del proyecto', f"B {pct(o['labour_b'] / costs_b)} (equipo: {pct(o['labour_a'] / team_costs_no_maint)})"],
    ['Tarifa mensual por rol (USD/mes, convertida del equipo)', '; '.join(f"{short[r['key']]} {x.replace('USD ', '')}" for r, x in zip(lab, implied))],
    ['Contingencia / costos', f"A {pct(la['contingency'] / a_costs_no_maint)} · B {pct(cont / costs_b)}"],
    ['Efecto del tipo de cambio', f"±20 % en el dólar mueve el total B entre {usd(o['fx_sens']['1.2']['total_b'])} y {usd(o['fx_sens']['0.8']['total_b'])}"],
    ['Costos indirectos', 'No se imputan (a declarar); todas las líneas son directas'],
    ['Unidades', f"USD enteros; 1 mes = 21 días hábiles; tipo de cambio único ARS {n(fx, 2)}"],
])}

## Qué es verificado y qué es supuesto

- **Verificado:** que las sumas cierran, que cada línea sale de `cantidad × costo unitario` (o del importe del equipo ÷ tipo de cambio) y que la duración sale de las fechas del Gantt del equipo. `bash tools/run-all.sh` lo comprueba, incluso con otro tipo de cambio.
- **Supuesto (a acordar entre todos):** el **tipo de cambio** (a confirmar), las **tarifas** (son las del equipo; **no se contrastaron con datos de mercado**), las **personas por rol**, la **escala de impactos**, el 10 % de reserva de gestión y las ventanas de cada línea. Los importes globales no tienen cotización.
"""
    write("03-presupuesto/presupuesto.md", txt)
    write("03-presupuesto/model.py", MODEL_PY)
    render_extra(c)


MODEL_PY = '''"""Thin runner: prints the USD budget model. All logic lives in ../tools (costing.py, build_all.py, data.py).

Usage: python3 model.py [ARS_PER_USD]   (default: the single constant in tools/data.py)
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "tools"))
import build_all  # noqa: E402

if __name__ == "__main__":
    fx = float(sys.argv[1]) if len(sys.argv) > 1 else None
    o, *_ = build_all.compute(fx=fx)
    print("Tipo de cambio ARS/USD:", o["fx"]["value"], "·", o["fx"]["date"])
    print("Escenario A:", o["ladder_a"])
    print("Escenario B:", o["ladder_b"])
    print("Contingencia (Σ EMV residual, USD):", o["risks"]["emv_residual_usd"])
'''


def _old_display_errors(lines):
    """How the first version displayed each line (people x unit rounded to whole USD x months with 1-2 decimals) vs its subtotal."""
    bad = []
    for l in lines:
        if l["unidad"] == "global":
            continue
        if l.get("role"):
            shown = l["qty"] * round(l["unit_usd"]) * round(l["duracion_meses"], 2)
        else:
            shown = round(l["qty"], 1) * round(l["unit_usd"])
        diff = abs(shown - l["usd_b"])
        if diff > 1:
            bad.append((l["id"], diff))
    return bad


def render_extra(c):
    """03-presupuesto/memoria-de-calculo.md (one page a professor can follow) and 03-presupuesto/auditoria.md."""
    o, la, lb, cal, res = c["o"], c["la"], c["lb"], c["cal"], c["res"]
    fx = o["fx"]["value"]
    lines = {l["id"]: l for l in o["lines"]}
    lab = {r["key"]: r for r in o["labour"]}
    br, pyr = o["bridge"], o["pyramid"]
    team = o["team_usd"]
    costs_b, cont, maint = lb["project_costs"], lb["contingency"], o["maint_usd"]
    r01 = next(x for x in o["risks"]["sorted"] if x["id"] == "R01")
    prob = D.SCALE["prob"][r01["pr"]]
    imp_usd = cs.usd_of(D.SCALE["impact_M"][r01["ir"]], fx)
    dev, tec1, inf1, tec4, man1, tec3 = lab["dev"], lines["TEC1"], lines["INF1"], lines["TEC4"], lines["MAN1"], lines["TEC3"]
    rh3 = lines["RH3"]

    # spread example: TEC3 (all the project), July
    lo = min(res[i]["es"] for i in tec3["window"])
    hi = max(res[i]["ef"] for i in tec3["window"])
    per_day = tec3["usd_b"] / (hi - lo)
    july = sum(1 for idx in range(lo, hi) if cal.date_of(idx).month == 7)

    # ---------------------------------------------------------------- memoria de calculo
    ex_rows = [
        ["Mano de obra (paramétrica)", f"RH3 Desarrolladores", f"{rh3['qty']} pers. × {usd2(rh3['unit_usd'])}/mes × {rh3['workdays']} ÷ 21", usd(rh3["usd_b"])],
        ["Herramienta mensual (experta, fija)", f"TEC1 {tec1['concepto']}", f"1 servicio × {usd2(tec1['unit_usd'])}/mes × {tec1['workdays']} ÷ 21", usd(tec1["usd_b"])],
        ["Importe global (experta, variable)", f"TEC4 {tec4['concepto']}", f"1 global × {usd(tec4['unit_usd'])}", usd(tec4["usd_b"])],
        ["Servicio mensual (experta, fijo)", f"INF1 {inf1['concepto']}", f"1 servicio × {usd2(inf1['unit_usd'])}/mes × {inf1['workdays']} ÷ 21", usd(inf1["usd_b"])],
        ["Mantenimiento (posterior al cierre)", f"MAN1 {man1['concepto']}", f"1 global × {usd(man1['unit_usd'])}; **fuera de la línea base**", usd(man1["usd_b"])],
        ["Contingencia (un riesgo)", f"{r01['id']} {r01['name']}", f"P {pct(prob, 0)} × impacto {usd(imp_usd)} (nivel {r01['ir']})", usd(r01["emv_usd"])],
        ["Contingencia (total)", f"Σ EMV de los {o['risks']['n']} riesgos", "suma de los EMV residuales", usd(cont)],
        ["Reserva de gestión", "10 % de la línea base", f"{usd(lb['baseline'])} × 10 %", usd(lb["mgmt_reserve"])],
        ["Curva S (un mes de una línea)", f"TEC3 {tec3['concepto']}", f"{usd2(per_day)} por día hábil × {july} d.h. de julio", usd(per_day * july)],
    ]
    mem = f"""
# Memoria de cálculo del presupuesto (una página)

> Moneda: **USD**, con **un único tipo de cambio: ARS {n(fx, 2)} por USD** ({o['fx']['source']}; fecha {o['fx']['date']}; a confirmar). Cambiar ese valor en `tools/data.py` recalcula todo. Cada importe se redondea a dólares enteros **por línea** y los totales suman líneas.

## Los 8 pasos (en el orden de la Clase 4, p15)

1. **Fijar la moneda y el tipo de cambio.** Los importes del equipo están en pesos; se convierten a USD con una sola constante. El tipo de cambio es un factor Económico del PESTEL (Clase 4, p7) y está tratado como riesgo (R19).
2. **Tomar la duración del Gantt.** Para cada rol o servicio, *días hábiles* = unión de las actividades donde interviene (fechas Inicio–Fin del Excel del equipo, lunes a viernes). **21 días hábiles = 1 mes.** (Clase 4, p16: la estimación parte de la estimación de recursos y tiempos).
3. **Estimar cada paquete de trabajo.** `cantidad × costo unitario × duración` (p16), considerando costos directos e indirectos. Técnica (p18): *paramétrica simple* para la mano de obra (tarifa × personas × tiempo) y *experta* para el resto; no hay datos para *análoga*.
4. **Clasificar** cada línea (p13–14): fijo/variable y directo/indirecto. Todas son directas; los indirectos están declarados en {usd(o['indirect']['usd'])}.
5. **Sumar hacia arriba** (p24): paquetes de trabajo → centros contables → **proyecto = {usd(costs_b)}**.
6. **Calcular la contingencia** (p19–20; Clase 5 p31: *EMV = P × I, con este valor generamos la reserva de contingencia*): suma de los EMV de los riesgos identificados = **{usd(cont)}**. Proyecto + contingencia = **línea base {usd(lb['baseline'])}**.
7. **Agregar la reserva de gestión** (p19, p21, p24): 10 % de la línea base = **{usd(lb['mgmt_reserve'])}** → **presupuesto {usd(lb['total'])}**. El mantenimiento inicial ({usd(maint)}) es posterior al cierre: se informa aparte (total con mantenimiento: **{usd(o['all_in_b'])}**).
8. **Presentar la curva S** (p23): cada línea se reparte parejo entre el primer y el último día de su ventana; el acumulado mensual termina en el costo del proyecto, y con la contingencia termina en la línea base.

## Un ejemplo por tipo de costo (se reproducen con una calculadora)

{table(['Tipo', 'Línea', 'Fórmula con números', 'Resultado'], ex_rows)}

## Los totales, como los muestra la cátedra (p24)

{table(['Nivel', 'Importe'], [
    ['Presupuesto', usd(pyr['total'])], ['Reserva de gestión (10 %)', usd(pyr['mgmt_reserve'])],
    ['Línea base de costos', usd(pyr['baseline'])], ['Reserva de contingencia (Σ EMV)', usd(pyr['contingency'])],
    ['Proyecto (Σ de {0} paquetes de trabajo)'.format(pyr['n_packages']), usd(pyr['project'])]])}

**Qué es supuesto:** el tipo de cambio, las tarifas (las del equipo, convertidas), las personas por rol, los importes globales sin cotización y la escala de impactos de los riesgos. **Qué se verifica solo:** que las sumas cierran y que cada línea sale de su fórmula (`bash tools/run-all.sh`).
"""
    write("03-presupuesto/memoria-de-calculo.md", mem)

    # ---------------------------------------------------------------- auditoria
    bad = _old_display_errors(o["lines"])
    max_bad = max((d_ for _, d_ in bad), default=0)
    team_labour_share = o["labour_a"] / sum(c_["team"] for k, c_ in o["categories"].items() if k != "mant")
    pm_total = sum(r["qty_b"] * r["months"] for r in o["labour"])
    avg_pm = o["labour_b"] / pm_total
    base = lb["baseline"]
    alt_total = round(base / 0.9)
    alt_reserve = alt_total - base
    infra_share = o["categories"]["inf"]["b"] / costs_b
    maint_share = maint / costs_b
    rates = "; ".join(f"{r['label']} {usd(r['rate_usd'])}" for r in o["labour"])
    aud_rows = [
        ["1", "La comparación «+" + pct(br["until_closing_pct"]) + " sobre el total del equipo» mezclaba alcances: B sin mantenimiento contra el equipo con mantenimiento.", "Alta (un profesor la detecta)", f"**Corregido:** comparación homogénea, {usd(o['all_in_b'])} contra {usd(team['total'])} = **+{pct(br['like_for_like_pct'])}**, con puente de tres pasos."],
        ["2", f"La aritmética mostrada no se reproducía con calculadora: en {len(bad)} líneas «cantidad × costo mostrado» difería del subtotal (hasta {usd(max_bad)}) por mostrar la tarifa sin centavos y los meses redondeados.", "Media (es justo lo que pidió el profesor)", "**Corregido:** se muestra «tarifa con centavos × días hábiles ÷ 21 (× personas)»; un test independiente la recalcula desde los CSV."],
        ["3", "No estaba la presentación «suma ascendente» de la Clase 4 (p24).", "Media", "**Agregado:** pirámide paquetes → centros contables → proyecto → línea base → presupuesto."],
        ["4", "La curva S no incluía la contingencia, pero la línea base de la cátedra sí (p24).", "Media", "**Agregado:** segunda curva que termina en la línea base."],
        ["5", "Los costos indirectos solo se mencionaban («conviene declararlo»), sin una fila; la p16 pide considerar directos e indirectos.", "Baja", "**Agregado:** fila declarada en USD 0 con decisión del grupo."],
        ["6", "Los rubros de «qué estimar» (p17) no estaban mapeados.", "Baja", "**Agregado:** tabla de rubros (clasificación propuesta)."],
        ["7", f"Redondeo: el total del equipo convertido línea por línea ({usd(team['total'])}) difiere {n(abs(br['rounding_diff']), 2)} USD de convertirlo de una vez.", "Informativa", "Declarado en el puente; no cambia ninguna conclusión."],
        ["8", "Se usa un único tipo de cambio de octubre de 2026 para un proyecto simulado de abril a septiembre de 2026; la fuente es secundaria.", "Informativa", "Declarado; sensibilidad ±20 % en el documento; **a confirmar con el cierre oficial**."],
        ["9", f"La base del 10 % de reserva de gestión es ambigua en la cátedra: p21 («10 % del presupuesto total, $100.000»), p24 (ejemplo $60 sobre una línea base de $240). Si fuera 10 % del total final, la reserva sería {usd(alt_reserve)} y el presupuesto {usd(alt_total)}.", "Media (decisión)", f"Se mantiene 10 % **de la línea base** ({usd(lb['mgmt_reserve'])}) y se declara; alternativa a decidir."],
    ]
    verified = [
        ["Escalera de reservas: proyecto + contingencia = línea base; + reserva de gerencia = presupuesto", "p24 (imagen)", "Coincide con el pack"],
        ["Contingencia = probabilidad × impacto (ejemplo: acero $500.000, 30 % de que suba 10 % → $15.000)", "p20", "Coincide: el pack usa P × I por riesgo"],
        ["EMV = P × I y «con este valor generamos la reserva de contingencia»", "Clase 5 p31", "Coincide: contingencia = Σ EMV"],
        ["Reserva de gestión: 10 % del presupuesto total, sin riesgos específicos", "p19, p21", "Coincide; la base del % es ambigua (hallazgo 9)"],
        ["Qué estimar: mano de obra, materiales, subcontratistas, alquiler de equipo e instalaciones, viajes, reservas", "p17", "Mapeado (tabla de rubros)"],
        ["Técnicas: análoga, paramétrica, experta", "p18", "Se usan paramétrica y experta; análoga no (sin datos previos)"],
        ["Costo por paquete de trabajo, directos e indirectos; parte de la estimación de recursos y tiempos", "p16", "Coincide (indirectos declarados en 0)"],
        ["Clasificación fijo/variable y directo/indirecto", "p13–14", "Coincide"],
        ["Curva S como línea base de desempeño; flujo de caja esperado", "p23 (imagen)", "Coincide; el pack muestra una curva por escenario B y la de línea base"],
        ["Valor tiempo del dinero con tasa de descuento (ejemplo de inversión)", "p29 (imagen)", "No aplica: es un proyecto público sin flujo de ingresos modelado; si se agregara, la lógica es la de esa tabla"],
    ]
    judg = [
        ["Mano de obra sobre costos del proyecto", f"B {pct(o['labour_b'] / costs_b)} · equipo {pct(team_labour_share)}", "Es la categoría dominante; **sin contrastar con el mercado**"],
        ["Costo promedio por persona-mes (B)", f"{usd(avg_pm)} ({n(pm_total, 1)} persona-mes)", "Sale de las tarifas del equipo convertidas; **sin contrastar con el mercado**"],
        ["Tarifas mensuales convertidas", rates, "Son las del equipo (pesos ÷ meses de su tabla §10.2); **sin contrastar con el mercado**"],
        ["Contingencia sobre costos del proyecto", f"{pct(cont / costs_b)} (rango {pct(o['sensitivity']['0.5']['pct_of_costs_b'])}–{pct(o['sensitivity']['1.5']['pct_of_costs_b'])} según la escala de impactos)", "Depende de una escala de impactos **supuesta**; lo que se verifica es la trazabilidad, no la cifra"],
        ["Infraestructura y seguridad sobre costos del proyecto", pct(infra_share), "Importes globales del equipo, **sin cotización**"],
        ["Mantenimiento inicial sobre costos del proyecto", pct(maint_share), "Importe global del equipo; sin duración definida"],
        ["Efecto del tipo de cambio", f"±20 % mueve el total B entre {usd(o['fx_sens']['1.2']['total_b'])} y {usd(o['fx_sens']['0.8']['total_b'])}", "Es el supuesto más sensible: conviene explicitarlo en el documento"],
    ]
    sev = lambda s: sum(1 for r in aud_rows if r[2].startswith(s))
    aud = f"""
# Auditoría del presupuesto contra el material de la cátedra

> **Veredicto.** Los números **cierran** y la estructura **coincide** con la Clase 4 en lo esencial (escalera de reservas, P × I, clasificación, técnicas). Se registraron **{len(aud_rows)} hallazgos** ({sev('Alta')} alto, {sev('Media')} medios, {sev('Baja')} bajos, {sev('Informativa')} informativos; el más importante: una comparación que mezclaba alcances); los de contenido están resueltos en `presupuesto.md` y quedan **dos decisiones** del grupo (base de la reserva e indirectos). Lo que **no** se puede verificar desde el material: las tarifas, los importes globales y el tipo de cambio contra el mercado.

## Qué se miró

- **Clase 4 (Gestión de costos):** texto de las p12–24 y p26–29 y **las imágenes de p23 (curva S), p24 (suma ascendente) y p29 (valor tiempo del dinero)**. Clase 5 p31 (EMV).
- **Ejemplo Clase:** es un Canvas de un negocio de insumos médicos; su único contenido de costos es el bloque «Estructura de costos» (p13). **No trae un presupuesto de proyecto**: el modelo a imitar es el de la Clase 4.
- **Pack:** `presupuesto.md`, `desglose.csv` (32 líneas), `model.csv`, `04-riesgos.csv`, `02-gantt/schedule.csv`.

## Lo verificado contra las diapositivas

{table(['Qué dice la cátedra', 'Dónde', 'Resultado'], verified)}

## Hallazgos

{table(['#', 'Hallazgo', 'Gravedad', 'Estado'], aud_rows)}

## Recálculo independiente

Un test (`tools/test_audit_independent.py`) recalcula **sin usar el modelo**: los totales desde `desglose.csv` y `04-riesgos.csv` (costos + Σ EMV + reserva = {usd(lb['total'])}; con mantenimiento, {usd(o['all_in_b'])}), los días hábiles de cada rol desde las fechas escritas del Excel, y cada línea con su fórmula mostrada (tarifa con centavos × días hábiles ÷ 21). Las sumas de la curva S también se recalculan. Resultado: **sin diferencias** (más allá del redondeo a dólares enteros).

## Razonabilidad: qué es verificado, supuesto y sin contrastar

{table(['Indicador', 'Valor', 'Lectura'], judg)}

**Verificado:** coherencia aritmética, correspondencia con la Clase 4/5, duraciones desde las fechas del Excel. **Supuesto:** tipo de cambio, personas por rol, escala de impactos, 10 % de reserva. **Sin contrastar con el mercado:** tarifas, importes globales, infraestructura. Este paquete no cita referencias de mercado porque no se consultaron fuentes verificables; si el equipo quiere defender las tarifas, necesita una cotización o una fuente.

## Puente con el total del equipo y con el campo (12) del Charter

{table(['Paso', 'Variación', 'Acumulado'], [['Total del equipo (§10), convertido', '—', usd(team['total'])]] + [[s['name'], ('+' if s['delta'] >= 0 else '−') + usd(abs(s['delta'])), usd(s['running'])] for s in br['steps']])}

El campo **(12) Summary Budget** del Charter en plantilla debe mostrar **{usd(lb['total'])}** (línea base {usd(lb['baseline'])} + reserva de gestión {usd(lb['mgmt_reserve'])}) **más** el mantenimiento inicial posterior al cierre de {usd(maint)}; ambos números salen de este puente y un test los compara.

## Decisiones para el grupo

1. **Base de la reserva de gestión:** 10 % de la línea base (propuesto) o 10 % del total final (hallazgo 9).
2. **Costos indirectos:** dejarlos en cero declarado (propuesto) o sumar un porcentaje justificado.
3. **Escenario A o B** y la regla de corte del 13/10 (ver `presupuesto.md`).
4. **Tipo de cambio de referencia:** confirmar con el cierre oficial.
"""
    write("03-presupuesto/auditoria.md", aud)
