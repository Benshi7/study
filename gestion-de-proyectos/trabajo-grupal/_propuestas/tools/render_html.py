"""Renders the single self-contained HTML for the team (no references to private workspace/tooling)."""
import html
import pathlib

import costing as cs
import data as D
import render_format as rfmt
import svg
from fmt import ars, n, pct, u, usd, usd2
from render_budget import _old_display_errors

ROOT = pathlib.Path(__file__).resolve().parent.parent

CSS = """
:root{--bg:#fff;--ink:#2a1f2d;--mute:#6b5a70;--rule:#eadbe6;--accent:#b83a95;--accent2:#6b2fae;--soft:#f8e8f3;--card:#fff;--ok:#1f7a4d;--okbg:#e4f3ea;--warn:#8a5a00;--warnbg:#fff3d6;--hero-ink:#fff}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#1b1220;--ink:#f1e9f0;--mute:#b9a7bf;--rule:#3c2c43;--accent:#e17cc4;--accent2:#a98cf0;--soft:#2c1c33;--card:#241829;--ok:#6cc592;--okbg:#1f3328;--warn:#f0c36a;--warnbg:#3a2f12;--hero-ink:#1b1220}}
:root[data-theme="dark"]{--bg:#1b1220;--ink:#f1e9f0;--mute:#b9a7bf;--rule:#3c2c43;--accent:#e17cc4;--accent2:#a98cf0;--soft:#2c1c33;--card:#241829;--ok:#6cc592;--okbg:#1f3328;--warn:#f0c36a;--warnbg:#3a2f12;--hero-ink:#1b1220}
*{box-sizing:border-box}html{font-size:17px;scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font-family:"Source Serif 4",Georgia,serif;line-height:1.6}
.hero{background:var(--accent);color:var(--hero-ink);padding:2.2rem 16px 2rem;border-radius:0 0 0 64px;position:relative}
.hero-in{max-width:56rem;margin:0 auto}
.hero p{margin:.2rem 0;font-family:"Montserrat",system-ui,sans-serif;font-size:.85rem;opacity:.95}
.hero h1{font-family:"Montserrat",system-ui,sans-serif;font-size:1.7rem;line-height:1.2;margin:.3rem 0 .5rem}
main{max-width:56rem;margin:0 auto;padding:1rem 16px 4rem}
h2{font-family:"Montserrat",system-ui,sans-serif;font-size:1.3rem;margin:2.4rem 0 .6rem;padding-bottom:.25rem;border-bottom:2px solid var(--accent)}
h3{font-family:"Montserrat",system-ui,sans-serif;font-size:1.02rem;margin:1.4rem 0 .4rem;color:var(--accent2)}
a{color:var(--accent2)}
nav.toc{display:flex;flex-wrap:wrap;gap:.4rem;margin:1rem 0;font-family:system-ui,sans-serif;font-size:.8rem}
nav.toc a{background:var(--soft);padding:.25rem .65rem;border-radius:99px;text-decoration:none;color:var(--ink)}
.note{border-left:4px solid var(--accent);background:var(--soft);padding:.7rem 1rem;border-radius:0 8px 8px 0;margin:1rem 0;font-size:.95rem}
.warn{border-left-color:var(--warn);background:var(--warnbg)}
.chip{display:inline-block;font-family:system-ui,sans-serif;font-size:.7rem;padding:.1rem .5rem;border-radius:99px;background:var(--soft);color:var(--accent2);border:1px solid var(--rule);margin-right:.3rem}
.chip.prop{background:var(--warnbg);color:var(--warn)}
.wrap{overflow-x:auto;margin:.8rem 0;border:1px solid var(--rule);border-radius:8px}
table{border-collapse:collapse;width:100%;font-size:.84rem;min-width:30rem;background:var(--card)}
th,td{padding:.4rem .55rem;border-bottom:1px solid var(--rule);text-align:left;vertical-align:top}
th{font-family:system-ui,sans-serif;font-size:.7rem;text-transform:uppercase;letter-spacing:.04em;background:var(--accent);color:var(--hero-ink)}
td.num,th.num{text-align:right;white-space:nowrap}
tr.total td{font-weight:700;background:var(--soft)}
.cards{display:grid;gap:.9rem}
.card{border:1px solid var(--rule);background:var(--card);border-radius:10px;padding:.9rem 1rem}
.card h3{margin-top:0}
.card dl{margin:.4rem 0;display:grid;grid-template-columns:7.5rem 1fr;gap:.2rem .6rem;font-size:.9rem}
.card dt{font-family:system-ui,sans-serif;font-size:.7rem;text-transform:uppercase;color:var(--mute);padding-top:.25rem}
.card dd{margin:0}
.agree{display:flex;align-items:center;gap:.5rem;margin-top:.5rem;font-family:system-ui,sans-serif;font-size:.85rem}
.agree input{width:1.1rem;height:1.1rem;accent-color:var(--accent)}
.svgbox{overflow-x:auto;border:1px solid var(--rule);border-radius:8px;background:var(--card);padding:.5rem;margin:.8rem 0}
.svgbox svg{min-width:640px;width:100%;height:auto}
.cols{display:grid;gap:1rem}
@media(max-width:600px){.card dl{grid-template-columns:1fr}.card dt{padding-top:.5rem}}
@media(min-width:760px){.cols{grid-template-columns:1fr 1fr}.cards{grid-template-columns:1fr}}
button.theme{position:absolute;top:.6rem;right:.8rem;border:1px solid var(--hero-ink);background:transparent;color:var(--hero-ink);border-radius:8px;padding:.3rem .6rem;font:inherit;font-size:.8rem;cursor:pointer}
footer{color:var(--mute);font-size:.8rem;border-top:1px solid var(--rule);margin-top:3rem;padding-top:1rem;font-family:system-ui,sans-serif}
ul.tight{margin:.3rem 0;padding-left:1.2rem}
ul.check{list-style:none;padding-left:0;font-size:.92rem}ul.check li{margin:.3rem 0}ul.check input{accent-color:var(--accent);margin-right:.4rem}
@media print{button.theme,nav.toc{display:none}.hero{background:#fff;color:#000;border-bottom:3px solid #b83a95;border-radius:0}.card,.wrap,.svgbox{break-inside:avoid}.svgbox,.wrap{overflow:visible}:root{--bg:#fff;--ink:#000;--card:#fff}}
"""

JS = """
(function(){
  var root=document.documentElement,btn=document.getElementById('theme');
  function get(k){try{return localStorage.getItem(k)}catch(e){return null}}
  function set(k,v){try{localStorage.setItem(k,v)}catch(e){}}
  var saved=get('theme'); if(saved){root.setAttribute('data-theme',saved)}
  function cur(){return root.getAttribute('data-theme')||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light')}
  function paint(){btn.textContent=cur()==='dark'?'☀ Claro':'☾ Oscuro';btn.setAttribute('aria-pressed',cur()==='dark')}
  btn.addEventListener('click',function(){var n=cur()==='dark'?'light':'dark';root.setAttribute('data-theme',n);set('theme',n);paint()});paint();
  document.querySelectorAll('input[data-agree],input[data-check]').forEach(function(cb){
    var k=cb.hasAttribute('data-agree')?'agree-'+cb.getAttribute('data-agree'):'check-'+cb.getAttribute('data-check'); cb.checked=get(k)==='1';
    cb.addEventListener('change',function(){set(k,cb.checked?'1':'0')});
  });
})();
"""


def e(s):
    return html.escape(str(s))


def tbl(headers, rows, num_cols=(), total_rows=()):
    h = "".join(f'<th class="{"num" if i in num_cols else ""}">{e(x)}</th>' for i, x in enumerate(headers))
    body = []
    for ri, r in enumerate(rows):
        cls = ' class="total"' if ri in total_rows else ""
        body.append(f"<tr{cls}>" + "".join(f'<td class="{"num" if i in num_cols else ""}">{c}</td>' for i, c in enumerate(r)) + "</tr>")
    return f'<div class="wrap"><table><thead><tr>{h}</tr></thead><tbody>{"".join(body)}</tbody></table></div>'


def card(key, title, diag, fix, effort, who):
    return f"""<article class="card" id="p-{key}"><h3>{e(title)}</h3>
<dl><dt>Diagnóstico</dt><dd>{diag}</dd><dt>Qué cambiaría</dt><dd>{fix}</dd><dt>Cuánto cuesta</dt><dd>{e(effort)}</dd><dt>Quién decide</dt><dd>{e(who)}</dd></dl>
<label class="agree"><input type="checkbox" data-agree="{key}"> Acordado por el grupo</label></article>"""


def render(c, ck):
    o, la, lb, res, cal = c["o"], c["la"], c["lb"], c["res"], c["cal"]
    names, cp = c["names"], c["cp"]
    fx = o["fx"]
    cats, lines, lab = o["categories"], o["lines"], o["labour"]
    costs_b, cont, maint = lb["project_costs"], lb["contingency"], o["maint_usd"]
    team = o["team_usd"]
    phases = []
    for ph in D.PHASES:
        ids = [a["id"] for a in D.ACTIVITIES if a["phase"] == ph[0]]
        phases.append((ph[0], ph[1], min(res[i]["es"] for i in ids), max(res[i]["ef"] for i in ids)))
    gate_labels = [f"G{p[0]} {p[5]} · {p[4].strftime('%d/%m/%Y')}" for p in D.PHASES]
    gantt_svg = svg.gantt_phases(phases, res, cal, gate_labels)
    labels = list(o["cash"].keys())
    scurve = svg.s_curve(o["cum"], labels, o["cum"][labels[-1]])
    gates_tbl = tbl(["Gate", "Hito (Excel)", "Resumen", "Excel", "Calculado"], [[g["gate"], e(g["name"]), g["declared"], g["proposed"], g["computed"] + (" ✓" if g["ok"] else " ✗")] for g in o["gates"]])
    cp_list = " → ".join(f"{i}" for i in cp)
    g, gc = o["gantt"], o["calendar"]
    by = {a["id"]: a for a in D.ACTIVITIES}
    scen_labels = {
        "escrito": "Como está escrito: «a-b» = los dos extremos (lo que calcula la hoja del equipo)",
        "rango": "Como está escrito: «a-b» = todo el rango",
        "fechas_del_equipo": "Fechas escritas en Inicio/Fin",
        "corregida": "<strong>Dependencias corregidas según las fechas (opción A)</strong>",
        "con_adelantos": "Dependencias como están + 7 adelantos + vínculo 26→27 (opción B)",
        "fs_estricto": "Fin-a-inicio estricto + vínculo 26→27 (opción C)",
    }
    scen_tbl = tbl(["Lectura", "Días hábiles", "Fin", "Actividades sin holgura"],
                   [[scen_labels[s["key"]], s["total"], s["end"], "—" if s["n_critical"] is None else s["n_critical"]] for s in g["scenarios"]])
    cells_tbl = tbl(["ID", "Actividad", "Escrito en el Excel", "Propuesto"],
                    [[i, e(names[i]), e(by[i]["deps_raw"]), e(g["corrected_text"][str(i)])] for i in g["corrected_cells_range"]])
    crit_pub, crit_fix = c["crit_ids"], g["critical_corrected"]
    crit_in, crit_out = sorted(set(crit_fix) - set(crit_pub)), sorted(set(crit_pub) - set(crit_fix))
    ids_txt = lambda xs: ", ".join(map(str, xs))
    opts_tbl = tbl(["Opción", "Qué se hace", "Fechas", "Fin", "Esfuerzo"], [
        ["<strong>A (recomendada)</strong>", f"Corregir {len(g['corrected_cells_range'])} celdas, escribir explícitas las demás y marcar 2 y 3 como inicio-a-inicio", "No cambian", f"{gc['corrected_end']} de cálculo; 30/09 con el día sin actividad", "Bajo: editar unas 12 celdas"],
        ["B", "Dejar las dependencias y registrar 7 adelantos y el vínculo 26→27", "No cambian", gc["dated_end"], "Bajo, conserva los errores de tipeo"],
        ["C", "Respetar fin-a-inicio con las dependencias actuales", "Se corren", f"{gc['strict_end']} (pasa el 30/09)", "Alto: rehacer fechas, hitos y presupuesto"],
        ["Mínimo", "Solo una nota en el punto 6: «a-b = los dos extremos» y la línea de simulación", "No cambian", f"{gc['end']} (CPM) / 30/09 (fechas)", "Muy bajo"],
    ])
    dev = next(x for x in lab if x["key"] == "dev")
    cards = "".join([
        card("gantt", "1 · Gantt: ya tiene lo que pide la cátedra; ajustes puntuales",
             f"<strong>Corrección de nuestro análisis anterior:</strong> el Excel del equipo ya trae duraciones, dependencias, holguras, camino crítico (CPM de {gc['cpm_wd']} días hábiles, {o['n_critical']} actividades críticas) y 8 hitos. Lo que falla: la notación «a-b» es ambigua ({gc['cpm_wd']} contra {gc['range_wd']} días hábiles según cómo se lea), {len(g['corrected_cells_range'])} celdas de dependencias contradicen las fechas y la columna Responsable está vacía.",
             f"Escribir las dependencias como listas explícitas y corregir {len(g['corrected_cells_range'])} celdas (hay texto listo), declarar la convención lunes a viernes sin feriados y asignar un rol por actividad. Con eso el camino crítico pasa a incluir la integración con canales (25) y las pruebas de intercambio (26).",
             "Bajo: editar unas 12 celdas del Excel; el texto está listo en la tabla de actividades.", "Quien armó el Gantt"),
        card("presupuesto", "2 · El presupuesto no tiene trazabilidad", "La contingencia es un 10 % fijo que no sale de los riesgos; la mano de obra es «meses × costo» y los meses no coinciden con el Gantt (analistas 3 vs 1,4; QA 2 vs 1,4). No hay reserva de gestión.",
             f"Mano de obra = personas × tarifa × duración del Gantt; contingencia = suma de los EMV ({usd(cont)}); reserva de gestión explícita. En USD: escenario A {usd(la['total'])}; escenario B {usd(lb['total'])}.", "Mediano a alto: acordar tarifas y personas por rol; recalcular la sección 10.", "Todo el grupo"),
        card("versiones", "3 · Versiones que se contradicen", "15 riesgos en un documento y 4 en otro, con IDs distintos; 8 hitos vs 7 gates; la nómina cambia según el archivo; quedó una nota de chat dentro del Charter.",
             "Un solo registro de riesgos (IDs R01–R15 más R16–R19), 8 gates, una sola nómina y una lista de datos «congelados» para todo el documento.", "Bajo: es una tarea de unificación.", "Coordinador del grupo"),
        card("canvas", "4 · Canvas, Design Thinking y objetivos", "Una sola propuesta de valor, segmentos muy amplios, objetivos sin meta ni plazo y Design Thinking que afirma 10 entrevistas inventadas como si fueran reales.",
             "Opción B con el segmento <strong>Hogares de la Ciudad</strong> (cada hogar con su realidad; hogar con niños, adulto mayor y persona con movilidad reducida son personas), dos propuestas de valor, 4 objetivos SMART y Design Thinking rotulado como <strong>investigación simulada</strong> (tres proto-personas, hipótesis y copia revisada de las slides).", "Mediano: es texto, no hace falta trabajo de campo.", "Grupo, con consulta a los profesores"),
        card("charter", "5 · Charter muy largo", "La sección 5 ronda las 6.000 palabras (más de la mitad del archivo) y repite con menos detalle los datos de las secciones 6, 9 y 10, de ahí las contradicciones.",
             "Charter de unas 2 páginas con los 13 elementos de la cátedra, que remite a las otras secciones y aclara que el perfil de hogar básico está incluido; el texto actual pasa íntegro a un anexo.", "Bajo a mediano.", "Grupo"),
        card("formato", "6 · Formato y prolijidad (devolución del Prof. Armando)", "Los archivos se entregaron por separado y con estilos distintos; la consigna pide un documento con los 10 puntos en orden y una historia que los conecte.",
             "Un solo documento (Word y PDF final), guía de estilo única, índice automático, 10 frases puente y checklist de 20 puntos, con el Gantt en Excel como anexo.", "Mediano: 2 días, con una persona de formato.", "Coordinador del grupo"),
        card("numeros", "7 · Presupuesto: cómo se construyen los números (devolución del Prof. Pacheco)", "Los importes están en pesos, sin tipo de cambio ni desglose de cómo se llegó a cada cifra.",
             f"Presupuesto en <strong>USD</strong> con un único tipo de cambio (ARS {n(fx['value'], 2)}), {len(lines)} líneas con paquete de trabajo, tipo de costo, método de la Clase 4, cantidad × costo unitario × duración y mes, y una explicación con tres ejemplos.", "Mediano: acordar personas por rol y pegar las tablas.", "Todo el grupo"),
        card("plantilla", "8 · Charter en la plantilla de la cátedra", "La cátedra entrega una plantilla de Project Charter de 24 campos en 3 partes y el Charter del equipo no la usa.",
             "Se completó la plantilla de forma concisa, con un mapa de los 13 elementos de la Clase 3 a los 24 campos; sede, contratos, mejora de procesos y experiencia previa dicen «a confirmar» o «no aplica» con su razón, y el texto largo pasa íntegro como anexo. Falta abrirla en Word y ajustar los saltos de página.", "Bajo: revisar en Word.", "Grupo"),
        card("auditoria", "9 · Auditoría del presupuesto contra la Clase 4", f"Se revisó el presupuesto contra las diapositivas: escalera de reservas, probabilidad × impacto, rubros, técnicas y curva S. Una comparación mezclaba alcances (el escenario B sin mantenimiento contra el total del equipo, que lo incluye): la comparable es <strong>{pct(o['bridge']['like_for_like_pct'])} más</strong>. Además, la aritmética mostrada no se reproducía con calculadora en {len(_old_display_errors(lines))} líneas.",
             "Suma ascendente como la de la cátedra, rubros de la Clase 4, costos indirectos declarados, curva S con contingencia, memoria de cálculo de una página y puente comparable con el total del equipo; cada línea se reproduce ahora con tarifa con centavos × días hábiles ÷ 21. Quedan dos decisiones: la base de la reserva de gestión y los costos indirectos.", "Bajo: ya está calculado; pegar las tablas.", "Todo el grupo"),
        card("guion", "10 · Guion narrativo: el hilo entre secciones", "La consigna exige un storytelling; hoy los puntos se leen como documentos distintos y hay valores que deben coincidir entre secciones.",
             "Papel de cada sección, objetos del hilo con un valor único (segmento, hitos, duración, USD, tipo de cambio, riesgos principales), diez frases puente con el contenido final, un resumen ejecutivo de unas 250 palabras y una tabla de consistencia.", "Bajo: pegar frases y resumen y verificar la tabla.", "Coordinador del grupo"),
    ])
    sens = o["sensitivity"]
    lab_rows = [[e(r["label"]), f"{r['team_months']}", usd(r["cost_a"]), usd(r["rate_usd"]), f"{r['wd']} ({n(r['months'], 2)})", n(r["qty_a"], 2), str(r["qty_b"]), usd(r["cost_b"])] for r in lab]
    lab_rows.append(["<strong>Total</strong>", "", usd(o["labour_a"]), "", "", "", "", usd(o["labour_b"])])
    lab_tbl = tbl(["Rol", "Meses (equipo)", "Costo equipo (USD)", "Tarifa (USD/mes)", "Días hábiles en el Gantt (meses)", "Personas A", "Personas B", "Costo B (USD)"], lab_rows, num_cols=(1, 2, 3, 4, 5, 6, 7), total_rows=(len(lab_rows) - 1,))
    team_costs_no_maint = sum(c_["team"] for k, c_ in cats.items() if k != "mant")
    comp = [
        ["Costos del proyecto (sin reservas)", usd(team_costs_no_maint), usd(team_costs_no_maint), usd(costs_b)],
        ["Mantenimiento posterior al cierre", usd(maint), usd(maint), "fuera de la línea base"],
        ["Reserva de contingencia", usd(team["contingency"]) + " (10 % plano)", usd(la["contingency"]) + " (suma de EMV)", usd(cont) + " (suma de EMV)"],
        ["Línea base de costos", "—", usd(la["baseline"]), usd(lb["baseline"])],
        ["Reserva de gestión", "no existe", "no definida", usd(lb["mgmt_reserve"]) + " (10 %)"],
        ["Total", usd(team["total"]), usd(la["total"]), usd(lb["total"])],
        ["Total con mantenimiento posterior", usd(team["total"]), usd(la["total"]), usd(o["all_in_b"])],
        ["Equivalente en ARS (referencia)", ars(D.TEAM_TOTAL), ars(la["total"] * fx["value"] / 1e6), ars(lb["total"] * fx["value"] / 1e6)],
    ]
    comp_tbl = tbl(["Concepto", "Hoy (equipo, convertido)", "Escenario A", "Escenario B"], comp, num_cols=(1, 2, 3), total_rows=(5,))
    sens_tbl = tbl(["Escala de impactos (supuesta)", "Contingencia", "% de los costos de B"], [[f"×{k.replace('.', ',')}", usd(v["contingency"]), pct(v["pct_of_costs_b"])] for k, v in sens.items()], num_cols=(1, 2))
    fx_tbl = tbl(["Tipo de cambio", "ARS por USD", "Costos de B", "Contingencia", "Total A", "Total B"],
                 [[f"×{k.replace('.', ',')}", n(v["fx"], 2), usd(v["costs_b"]), usd(v["contingency"]), usd(v["total_a"]), usd(v["total_b"])] for k, v in o["fx_sens"].items()], num_cols=(1, 2, 3, 4, 5))
    # itemised budget (compact; the full field list is in the CSV that accompanies the proposals)
    des_rows, total_rows_idx = [], []
    for key, label in D.CATEGORIES:
        for l in (x for x in lines if x["cat"] == key):
            if l["unidad"] == "global":
                qxu = f"1 global × {usd(l['unit_usd'])}"
            elif l.get("role"):
                qxu = f"{l['qty']} pers. × {usd2(l['unit_usd'])}/mes × {l['workdays']} ÷ 21"
            else:
                qxu = f"1 servicio × {usd2(l['unit_usd'])}/mes × {l['workdays']} ÷ 21"
            des_rows.append([l["id"], e(l["concepto"]), e(l["wp"]), f"{l['comportamiento'][0]}/{l['asignacion'][0]}", e(l["metodo"].split(" (")[0]), e(qxu), usd(l["usd_b"]), e(l["meses"])])
        total_rows_idx.append(len(des_rows))
        des_rows.append(["", f"<strong>Subtotal {e(label[0].lower() + label[1:])}</strong>", "", "", "", "", usd(cats[key]["b"]), "fuera de la línea base" if key == "mant" else ""])
    des_tbl = tbl(["ID", "Concepto", "Paquete de trabajo (Gantt)", "F/V · D/I", "Método (Clase 4)", "Cantidad × costo unitario × duración", "Subtotal (USD)", "Meses"], des_rows, num_cols=(6,), total_rows=tuple(total_rows_idx))
    hosting = next(x for x in lines if x["id"] == "INF1")
    r01 = next(x for x in o["risks"]["sorted"] if x["id"] == "R01")
    prob = D.SCALE["prob"][r01["pr"]]
    imp_usd = cs.usd_of(D.SCALE["impact_M"][r01["ir"]], fx["value"])
    rrows = []
    for r in c["sr"]:
        tag = ' <span class="chip prop">nuevo</span>' if r["new"] else (' <span class="chip">reformulado</span>' if r["mod"] else "")
        rrows.append([r["id"], e(r["name"]) + tag, f"{r['p']}×{r['i']}", usd(r["emv0_usd"]), e(r["resp"]), f"{r['pr']}×{r['ir']}", usd(r["emv_usd"]), "◆" if r["hl"] else ""])
    risk_tbl = tbl(["ID", "Riesgo", "P×I", "EMV inicial (USD)", "Respuesta", "P×I residual", "EMV residual (USD)", "Alto nivel"], rrows, num_cols=(2, 3, 5, 6))
    charter_map = tbl(["Elemento del Charter (cátedra)", "Estado hoy", "Qué cambia"], [
        ["1 · Propósito o justificación", "Presente", "Condensar"], ["2 · Descripción de alto nivel", "Presente", "Condensar; incluir el perfil de hogar básico"],
        ["3 · Objetivos", "Parcial: sin meta ni plazo", "4 resultados SMART; los 8 objetivos pasan al anexo"],
        ["4 · Requisitos de alto nivel", "<strong>Falta</strong>", "Lista de 8 requisitos (propuesta)"], ["5 · Producto o resultados", "Presente", "Lista de 8 entregables"],
        ["6 · Suposiciones y restricciones", "Presente", "Condensar + supuesto de simulación + tipo de cambio"], ["7 · Cronograma de alto nivel", "Parcial: sin fechas", "Tabla de 8 gates con fecha"],
        ["8 · Presupuesto de alto nivel", "Parcial: sin cifra ni moneda", "Una cifra en USD y 4 líneas"], ["9 · Riesgos de alto nivel", "Parcial: 12 vs 15", "5 riesgos con los IDs de la matriz"],
        ["10 · Criterios de éxito", "Presente", "Vincular a los objetivos SMART"], ["11 · Stakeholders principales", "Parcial", "Lista única de 9"],
        ["12 · Responsabilidades y autoridad del PM", "Parcial: falta la autoridad", "Agregar autoridad (propuesta)"], ["13 · Requisitos de aprobación", "Parcial", "Explicitar quién aprueba qué"],
    ])
    smart = tbl(["Resultado", "Meta SMART (propuesta)", "Plazo"], [
        ["O1 · Capa geográfica confiable (obj. 1 + 7)", "La capa integra las fuentes priorizadas y el 100 % tiene responsable y frecuencia de actualización definidos.", "02/07/2026 (G4)"],
        ["O2 · Integración multicanal (obj. 2)", "El Mapa y al menos 1 canal conversacional consumen la capa por API (BAX sujeto a validación técnica y a miBA).", "21/07/2026 (G5)"],
        ["O3 · Reportes y seguimiento (obj. 3 + 4 + 5)", "El 100 % de los casos de prueba del flujo completo aprobados; los 6 estados operativos.", "27/08/2026 (G6)"],
        ["O4 · Gestión y experiencia del hogar (obj. 6 + 8)", "Al menos 3 áreas operativas usan la vista de gestión y el hogar ve la información relevante de su entorno con el perfil de hogar básico (opt-in).", "09/09/2026 (G7)"],
    ])
    checks_tbl = tbl(["Control de coherencia (propuesta)", "OK"], [[e(k.name), "✓" if k.ok else "✗"] for k in ck])
    personas = tbl(["Persona (escenario de uso)", "Situación del hogar", "Qué necesita"], [
        ["Hogar con niños en edad escolar", "Se entera tarde de la inscripción o la vacunación", "Saber qué le corresponde y cuándo, sin buscar"],
        ["Persona con movilidad reducida", "No sabe qué veredas de su recorrido están en obra", "Recorridos y obras de su cuadra"],
        ["Adulto mayor", "No sabe qué trámites le corresponden", "Un lugar donde ver y pedir lo que le toca"],
        ["Vecino que reporta", "Se cruza con una incidencia y no sabe a quién avisar", "Reportar y ver qué pasó"],
    ])
    value = tbl(["", "Lado hogar (usa)", "Lado GCBA (financia y decide)"], [
        ["Tareas", "Enterarse de lo que le corresponde al hogar; informar una incidencia; consultar lo que pasa en su cuadra.", "Gestionar incidencias y servicios con el equipo que tiene; coordinar áreas; justificar el presupuesto."],
        ["Frustraciones", "No saber qué organismo o canal corresponde; enterarse tarde; no ver qué pasó con su reporte.", "Cada área mantiene su solución geográfica; no hay una vista única."],
        ["Propuesta de valor", "Un único lugar sobre el mapa donde cada hogar ve lo que le corresponde y reporta y sigue lo que ve, con estado visible.", "Vista de gestión y una capa geográfica reutilizable."],
    ])
    order_list = "".join(f"<li>{e(t)}</li>" for t in rfmt.CONSIGNA)
    bridge_rows = [[("Apertura" if k == "apertura" else "Cierre" if k == "cierre" else k), e(v)] for k, v in D.BRIDGES.items()]
    bridges_tbl = tbl(["Punto", "Frase puente propuesta"], bridge_rows)
    check_items = "".join(f'<li><label><input type="checkbox" data-check="{i}"> {e(x)}</label></li>' for i, x in enumerate(rfmt.CHECKLIST, 1))
    plan_tbl = tbl(["Día", "Prioridad", "Tarea", "Esfuerzo"], [
        ["Lun 12/10", "Bloqueantes", "Acordar en el grupo las decisiones 1 a 4 (presupuesto, USD y tipo de cambio, segmento «hogares», perfil de hogar básico)", "S"],
        ["Lun 12/10", "Bloqueantes", "Crear el documento base con los estilos de la guía y la carátula única", "M"],
        ["Lun 12/10", "Bloqueantes", "Pegar las tablas de presupuesto (escenario elegido) en las secciones 5 y 10", "M"],
        ["Lun 12/10", "Mejoran la nota", "Pasar la tabla del Gantt a la sección 6 y validarla con quien lo armó", "M"],
        ["Mar 13/10", "Bloqueantes", "Ensamblar los 10 puntos y pegar las 10 frases puente", "M"],
        ["Mar 13/10", "Bloqueantes", "Charter condensado + Anexo A; stakeholders y comunicación; registro único de riesgos", "M"],
        ["Mar 13/10", "Mejoran la nota", "Design Thinking: rotular la investigación como simulada y pegar la copia revisada de las slides; objetivos SMART y personas", "L"],
        ["Mar 13/10", "Defensa", "Preparar respuestas a las preguntas de coherencia y repartir quién defiende cada punto", "S"],
        ["Mié 14/10", "Bloqueantes", "Checklist de 20 puntos, 7 controles de coherencia, revisión cruzada, índice, PDF y envío", "M"],
        ["Mié 14/10", "Defensa", "Ensayo corto: cada uno dice en una frase qué pregunta responde su sección", "S"],
    ])
    page = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Propuestas de mejora del TP</title>
<script>try{{var t=localStorage.getItem('theme');if(t)document.documentElement.setAttribute('data-theme',t)}}catch(e){{}}</script>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@400;600&family=Montserrat:wght@600;700&display=swap">
<style>{CSS}</style></head><body>
<header class="hero"><button class="theme" id="theme" type="button" aria-pressed="false" aria-label="Cambiar entre modo claro y oscuro">☾ Oscuro</button><div class="hero-in">
<p>Taller de Gestión de Proyectos Digitales · TP Cascada</p>
<h1>Propuestas de mejora: presupuesto en USD, formato, Gantt, riesgos y coherencia</h1>
<p>Borrador para discutir entre todos · entrega 14/10/2026 · quedan 2 días</p></div></header>
<main>
<div class="note"><strong>Cómo leer esto.</strong> Los documentos de trabajo no se modificaron: esto es una <strong>propuesta aparte</strong>. Lo marcado <span class="chip prop">propuesta</span> es nuevo y hay que acordarlo; lo que no se pudo confirmar dice <strong>a confirmar</strong>. Las fechas simuladas (01/04 al 30/09/2026) se mantienen: solo se agrega una línea que lo declara. Importes en <strong>USD</strong>, con el equivalente en pesos solo como referencia.</div>
<div class="note"><strong>Tipo de cambio:</strong> ARS {n(fx['value'], 2)} por USD · {e(fx['source'])} · fecha de referencia {fx['date']} · <strong>a confirmar</strong>. Es una sola constante: si cambia, todas las cifras se recalculan.</div>
<nav class="toc" aria-label="Secciones"><a href="#resumen">Resumen</a><a href="#profes">Devolución</a><a href="#sentido">¿Tiene sentido?</a><a href="#gantt">Gantt</a><a href="#presupuesto">Presupuesto</a><a href="#riesgos">Riesgos</a><a href="#charter">Charter</a><a href="#canvas">Canvas y objetivos</a><a href="#formato">Formato y entrega</a><a href="#coherencia">Coherencia</a></nav>

<h2 id="resumen">Los 10 puntos y qué proponemos</h2>
<div class="cards">{cards}</div>

<h2 id="profes">Qué dijeron los profesores y qué cambia</h2>
{tbl(["Devolución", "Qué hacemos"], [["<strong>Prof. Armando:</strong> «mejorar el orden de los puntos, el formato, prolijidad»", "Un solo documento con el orden de la consigna y una guía de estilo única (problema 6)."], ["<strong>Prof. Pacheco:</strong> «se ven bien, todavía faltan varios puntos»; «en el presupuesto, dar más detalle de cómo construyen los números»", "Revisar contra los 10 puntos de la consigna (problema 6) y presupuesto desglosado en USD (problema 7)."]])}

<h2 id="sentido">¿Tiene más o menos sentido el proyecto?</h2>
<p><strong>Sí.</strong> El problema es real y concreto, el modelo de dos lados (el hogar usa y el Gobierno paga) explica quién recibe qué, y con las propuestas el cronograma, los riesgos y el presupuesto cierran entre sí. El riesgo no es la idea, es el <strong>tamaño</strong>: el desarrollo dura {o['phase_wd'][4]} días hábiles para 6 componentes (con 3 desarrolladores, unos {3 * o['phase_wd'][4]} días-persona, cerca de {round(3 * o['phase_wd'][4] / 6)} por componente) y hay 4 canales por integrar.</p>
<div class="cols"><div><h3>Entra en la primera implementación <span class="chip prop">propuesta</span></h3><ul class="tight"><li>Capa geográfica con 2 fuentes priorizadas (Transporte y Cultura)</li><li>Reportes con pocas categorías</li><li>Validación colaborativa simple</li><li>5 estados de seguimiento</li><li>Integración con el Mapa y Boti</li><li>Vista de gestión básica</li><li><strong>Perfil de hogar básico</strong> (dato mínimo declarado, opt-in)</li></ul></div>
<div><h3>Fase futura</h3><ul class="tight"><li>Más fuentes y áreas</li><li>BAX y miBA (sujetos a validación)</li><li>Tableros analíticos</li><li>Socios, beneficios y publicidad</li><li>Personalización avanzada y uso de datos sensibles</li></ul></div></div>
<p class="note warn"><strong>A confirmar:</strong> el tipo de cambio contra el cierre oficial, el texto de la Ley 25.326 (datos personales), la denominación vigente de algunas áreas, el traslado del feriado del 15/06, que BAX requiera miBA, y las tarifas contra datos de mercado.</p>

<h2 id="gantt">Gantt: el Excel ya está bien encaminado</h2>
<p class="note warn"><strong>Corrección.</strong> Nuestro análisis anterior dijo que el Gantt «no tenía duraciones, dependencias ni camino crítico». Eso valía solo para la imagen del documento Word: el <strong>Excel del equipo (anexo del punto 6)</strong> sí los trae. Esta propuesta toma el Excel como base y sugiere ajustes puntuales.</p>
<h3>Lo que ya está bien</h3>
<ul class="tight"><li><strong>40 actividades, 8 fases y 8 hitos</strong> con fecha; los hitos coinciden con los del Charter (§6.3) y con el documento resumido.</li><li>Cada duración coincide exactamente con las fechas (lunes a viernes).</li><li>El CPM de la hoja es correcto si «a-b» se lee como <em>los dos extremos</em>: da <strong>{gc['cpm_wd']} días hábiles</strong> y {o['n_critical']} actividades críticas, sin diferencias en las holguras. El propio anexo lo escribe así («1, 3» donde el cronograma dice «1-3»).</li><li>La nota del anexo sobre PERT es correcta: usan CPM con una duración por actividad y no inventan estimaciones de tres puntos.</li></ul>
<h3>Qué ajustar</h3>
<ol class="tight"><li><strong>La notación «a-b» es ambigua.</strong> Leída como rango da {gc['range_wd']} días hábiles, cambian {len(g['range_slack_mismatches'])} holguras y {len(g['range_critical_mismatches'])} marcas de crítica. Se escribe «1, 2, 3» o «1, 3», nunca «1-3».</li><li><strong>Las fechas y las dependencias no cuentan lo mismo.</strong> Siete actividades empiezan antes de que termine una predecesora; la actividad 27 espera {g['idle_gaps'][0][2]} días hábiles que ninguna dependencia explica, y hay un día sin actividad entre la 31 y la 32. Lo más probable son errores de tipeo en las celdas de dependencias (hipótesis: confirmar con quien armó el Excel).</li><li><strong>Responsable vacío:</strong> un rol por actividad, el mismo del presupuesto.</li><li><strong>Calendario:</strong> el Excel cuenta lunes a viernes sin feriados; hay {g['holiday_weekdays_in_window']} en el período. Basta con declararlo en una línea.</li></ol>
{cells_tbl}
<p>Con esas correcciones todas las fechas del equipo se reproducen exactamente (hasta la actividad 31) y el camino crítico cambia: entran {ids_txt(crit_in)} y salen {ids_txt(crit_out)}. La <strong>integración con canales digitales (25)</strong> y las <strong>pruebas de intercambio (26)</strong> pasan a ser críticas, coherente con el riesgo R12.</p>
<h3>Qué le hace cada lectura a la fecha de cierre</h3>
{scen_tbl}
<p>Con las dependencias como están y fin-a-inicio estricto más el vínculo 26→27, el cierre sería el {gc['strict_end']}; los adelantos lo comprimen y el día sin actividad entre 31 y 32 lo deja en el 30/09 del equipo. La fecha se sostiene solo con las dependencias corregidas (opción A) o declarando los adelantos (opción B).</p>
<div class="svgbox">{gantt_svg}</div>
{gates_tbl}
<h3>Opciones para decidir</h3>
{opts_tbl}
<div class="note"><strong>Supuesto de simulación (una línea para el documento):</strong> <em>«Las fechas del proyecto (01/04 a 30/09/2026) corresponden a una simulación académica; se cuentan los días de lunes a viernes, sin feriados; el trabajo se entrega el 14/10/2026.»</em><br>Si se contaran los feriados, las {gc['span_wd']} jornadas terminarían el {g['real_calendar_end']}, un día antes de la entrega. El feriado del 15/06 figura como <strong>a confirmar</strong>.</div>
<p class="note"><strong>PERT, por si preguntan:</strong> la Clase 3 enseña <code>(O+4M+P)/6</code>; el Excel usa CPM con duraciones únicas y lo declara. Respuesta posible: «no tenemos estimaciones de tres puntos; PERT es el paso siguiente para las actividades más inciertas».</p>

<h2 id="presupuesto">Presupuesto en USD: cómo se construye cada número</h2>
<p>Se conservan <strong>los importes y las tarifas del equipo</strong> (están en pesos); cada cifra se convierte con el tipo de cambio único y se redondea por línea, así que todas las tablas cierran. Lo nuevo: la duración sale de las fechas del Gantt del equipo, la contingencia sale de los riesgos y aparece la reserva de gestión (línea base = costos + contingencia; presupuesto = línea base + reserva de gestión).</p>
<h3>Efecto del tipo de cambio</h3>
{fx_tbl}
<p>El tipo de cambio es un factor Económico del PESTEL (Clase 4): se declara como supuesto y se trata como riesgo (R19).</p>
<h3>El método, en siete pasos (Clase 4)</h3>
<ol class="tight"><li><strong>Qué estimar:</strong> mano de obra, herramientas y servicios, infraestructura y las dos reservas.</li><li><strong>Duración:</strong> sale de las fechas del Gantt del equipo (días hábiles de cada rol; 21 días hábiles = 1 mes).</li><li><strong>Costo por paquete de trabajo:</strong> cantidad × costo unitario × duración.</li><li><strong>Técnica:</strong> paramétrica para la mano de obra y experta para el resto (importes globales del equipo, sin cotización); no se usa estimación análoga.</li><li><strong>Clasificación:</strong> fijo o variable; directo o indirecto. Todas las líneas son directas y no se imputan costos indirectos (a declarar).</li><li><strong>Presupuestación:</strong> suma por categoría y por mes; el acumulado es la curva S.</li><li><strong>Reservas:</strong> contingencia = suma de los EMV; reserva de gestión = 10 %.</li></ol>
<h3>Tres ejemplos resueltos</h3>
<ul class="tight"><li><strong>Desarrolladores:</strong> tarifa del equipo {ars(dev['team_cost_ars'])} ÷ {dev['team_months']} meses = {ars(dev['rate_ars'])}/mes = {usd(dev['rate_usd'])}/mes; {dev['wd']} días hábiles en el Gantt = {n(dev['months'], 2)} meses; con {dev['qty_b']} personas: {dev['qty_b']} × {usd(dev['rate_usd'])} × {n(dev['months'], 2)} = <strong>{usd(dev['cost_b'])}</strong>.</li><li><strong>Infraestructura y hosting:</strong> el equipo estimó {ars(hosting['ars_team_m'])} = {usd(hosting['usd_b'])}; la ventana del Gantt dura {n(hosting['duracion_meses'], 2)} meses, o sea {usd(hosting['unit_usd'])}/mes implícito (a reemplazar por una cotización).</li><li><strong>Contingencia (riesgo {r01['id']}):</strong> probabilidad residual {pct(prob, 0)} × impacto {usd(imp_usd)} = <strong>{usd(r01['emv_usd'])}</strong>; la contingencia total es la suma de los {o['risks']['n']} EMV residuales = {usd(cont)}.</li></ul>
<h3>Mano de obra: personas × tarifa × duración del Gantt</h3>
{lab_tbl}
<p>«Personas A» es cuántas personas implican los costos actuales con las duraciones del Gantt (≈ {n(lab[2]['qty_a'], 1)} desarrolladores): equipo chico para tres frentes en paralelo. «Personas B» es el dimensionamiento propuesto.</p>
<h3>Desglose completo (escenario B)</h3>
<p>F/V = fijo o variable; D/I = directo o indirecto. Las líneas con importe global tienen un costo unitario implícito (importe ÷ meses) que se reemplaza por una cotización cuando exista; su fuente es «equipo, a confirmar con cotización».</p>
{des_tbl}
<h3>Escalera de reservas y comparación</h3>
{comp_tbl}
<ul class="tight"><li><strong>A (mínimo esfuerzo):</strong> no se puede conservar el total actual: la contingencia calculada ({usd(la['contingency'])}) ya supera los {usd(team['contingency'])} que había.</li><li><strong>B (recomendado):</strong> mano de obra desde el Gantt y reserva de gestión explícita; {usd(lb['total'])}, {pct(lb['total'] / team['total'] - 1)} sobre el total del equipo.</li><li>La contingencia es el {pct(cont / costs_b)} de los costos de B: el 10 % del equipo cae dentro del rango; lo que faltaba era la trazabilidad.</li></ul>
<p class="note"><strong>Recomendación para el 14/10:</strong> presentar el escenario B, porque responde literalmente al pedido del profesor (cada número tiene fórmula, fuente y supuesto) y concuerda con el Gantt de la sección 6. <strong>Regla de corte:</strong> si no hay acuerdo sobre las personas por rol el 13/10 al mediodía, entregar A (se cambian solo la moneda y la contingencia) y dejar B para la defensa.</p>
{sens_tbl}
<h3>Curva S (escenario B, costo acumulado de los costos del proyecto, USD)</h3>
<div class="svgbox">{scurve}</div>
<p class="note warn"><strong>Supuestos a acordar:</strong> el tipo de cambio (a confirmar), las tarifas (no se contrastaron con datos de mercado), las personas por rol, la escala de impactos, el 10 % de reserva de gestión y que el mantenimiento posterior al cierre ({usd(maint)}) quede fuera de la línea base. Sí está verificado que las sumas cierran.</p>

<h2 id="riesgos">Riesgos: un solo registro con EMV</h2>
<p>Se conservan los IDs R01–R15 y las probabilidades e impactos del equipo (salvo R10, reformulado por el perfil de hogar básico); el resumen mapea R03 a <strong>R05</strong> y R04 a <strong>R06</strong>. Se agregan R16 a R18 (Opción B) y <strong>R19</strong> (variación del tipo de cambio). Los importes por nivel son una <strong>propuesta a acordar</strong>: probabilidad 10, 30, 50, 70 y 90 %; impacto {', '.join(u(D.SCALE['impact_M'][k]) for k in range(1, 6))}.</p>
{risk_tbl}
<p>EMV inicial total: {usd(o['risks']['emv_initial_usd'])}. <strong>EMV residual (amenazas): {usd(o['risks']['emv_residual_usd'])}</strong>, que es la reserva de contingencia. ◆ = va a «Riesgos de alto nivel» del Charter. No se cuantifican oportunidades (decisión conservadora, a declarar en el documento).</p>

<h2 id="charter">Project Charter: de ≈ 6.000 palabras a ≈ 2 páginas</h2>
<p>La cátedra lo define como un acuerdo preliminar de alto nivel con 13 elementos. Resumir y remitir a las otras secciones evita que el mismo dato aparezca dos veces con valores distintos (así nacieron 12 vs 15 riesgos y 8 vs 7 hitos). El texto actual pasaría íntegro a un anexo.</p>
{charter_map}
<p class="note"><strong>Aclaración propuesta para el alcance (§5.5.1 y §5.5.2):</strong> el Charter excluye el perfil personal avanzado o la personalización con datos sensibles <em>que no sean necesarios</em>; la exclusión es condicional. Se propone agregar: <em>«Quedan incluidos el perfil de hogar básico (dato mínimo declarado por el propio hogar, opt-in) y la personalización que se derive de él; quedan excluidos del MVP la personalización avanzada y el uso de datos sensibles que no sean necesarios.»</em></p>

<h2 id="canvas">Canvas (Opción B), Design Thinking y objetivos SMART</h2>
<p><strong>Segmento (propuesta):</strong> <em>Hogares de la Ciudad que conviven con su propia mezcla de necesidades (trámites, servicios, obras y reclamos de su entorno, movilidad) y hoy deben saber de antemano qué preguntar, a qué organismo y por qué canal, y no ven qué pasó con lo que reportan.</em> Cada hogar tiene su realidad; por eso hay un perfil de hogar básico.</p>
<h3>Personas (escenarios de uso, no segmentos)</h3>
{personas}
{value}
<p>Son dos propuestas de valor porque son dos segmentos: quien usa (el hogar) no es quien paga (el GCBA).</p>
<h3>Objetivos SMART <span class="chip prop">propuesta</span></h3>
{smart}
<p>Las metas numéricas son propuestas y las líneas base están «a medir».</p>
<h3>Design Thinking</h3>
<p>El deck afirma diez entrevistas con vecinos que no se hicieron. Decisión del grupo: <strong>no hacen falta entrevistas reales</strong>; se rotula la investigación como una <strong>simulación académica</strong> (proto-personas e hipótesis apoyadas en fuentes públicas, sin citas ni conteos inventados) y la validación con hogares queda como la actividad 5 del Gantt. Falta decidir si «Mi hogar» (perfil de hogar básico, opcional) entra al prototipo. Criterios de la clase 7: <strong>a confirmar</strong>.</p>

<h2 id="formato">Formato y entrega: un solo documento</h2>
<p><strong>¿Word o PDF, junto o por separado?</strong> La consigna pide un <em>«documento conteniendo los siguientes puntos»</em> y aclara que <em>«no deben ser puntos sueltos»</em>: va <strong>un solo documento</strong> con los 10 puntos, en este orden y con una historia que los conecte. La consigna no especifica el formato de archivo: se recomienda armarlo en Word y entregar el <strong>PDF</strong>; el Gantt en Excel va como anexo, pero el cronograma también va dentro del documento (punto 6); el Charter ampliado, como Anexo A. Si el equipo quiere certeza, puede confirmarlo por mail con los profesores.</p>
<ol class="tight">{order_list}</ol>
<h3>Guía de estilo (resumen)</h3>
<ul class="tight"><li>Un título de nivel 1 por punto, numerado del 1 al 10; carátula única con una sola nómina; índice automático actualizado antes de exportar.</li><li>Una fuente única de 11 pt, títulos de 16, 14 y 12 pt, interlineado 1,15, márgenes de 2,5 cm; el Gantt apaisado.</li><li>Tablas con el mismo estilo, encabezado repetido y filas que no se parten; pie de tabla y de figura numerados por punto.</li><li>USD con punto de miles, tipo de cambio declarado; fechas dd/mm/aaaa; porcentajes con coma (12,1 %).</li><li>IDs únicos: G1–G8, R01–R19, actividades 1–40; mismos nombres de roles y stakeholders en todo el documento.</li></ul>
<h3>Frases puente (apertura, puntos 3 a 10 y cierre)</h3>
{bridges_tbl}
<h3>Checklist de prolijidad (20 puntos)</h3>
<ul class="check">{check_items}</ul>
<h3>Plan de 2 días (12/10 al 14/10)</h3>
{plan_tbl}
<p class="note"><strong>Para después:</strong> un <em>mock</em> de una funcionalidad (por ejemplo, el seguimiento de un reporte o la vista del hogar con su perfil básico) para mostrar cómo se vería; se hace con el documento cerrado.</p>

<h2 id="coherencia">Coherencia entre secciones</h2>
<p>Siete controles que revisan que las secciones digan lo mismo (hitos, presupuesto, riesgos, contingencia, mano de obra, stakeholders y frases puente). Con las propuestas, todos pasan:</p>
{checks_tbl}
<h3>Para congelar antes de unificar</h3>
<ul class="tight"><li>Nombre del proyecto: «Modernización del Mapa Interactivo de la Ciudad».</li><li>Moneda: USD; tipo de cambio ARS {n(fx['value'], 2)} por USD ({fx['date']}, a confirmar).</li><li>Segmento: Hogares de la Ciudad; perfil de hogar básico incluido, personalización avanzada excluida del MVP.</li><li>Fechas: inicio 01/04, Charter 10/04, cierre 30/09, entrega 14/10/2026.</li><li>8 gates con las fechas de la tabla; una sola nómina; una sola cifra de presupuesto citada igual en todas las secciones.</li><li>Fuentes priorizadas: Transporte y Cultura (completar si hay otras).</li></ul>

<footer>Borrador de trabajo: revisar y corregir entre todos. Los importes nuevos y las metas son propuestas, no datos.</footer>
</main><script>{JS}</script></body></html>
"""
    (ROOT / "propuestas-de-mejora.html").write_text(page, encoding="utf-8")
