"""Single source of truth for the proposals.

Everything the team ALREADY wrote is marked `team` (with the section it comes from).
Everything NEW is a proposal and is labelled as such in the rendered documents.
Team money figures are in millions of ARS (M); every USD amount in the documents is derived from them
with ONE exchange-rate constant (FX_ARS_PER_USD). Durations are working days (wd).
"""
import datetime as dt

# ---------------------------------------------------------------- currency (single parametric constant)
# Clase 4 p7 lists "tipo de cambio" under the Economic factor of PESTEL: it is an explicit external factor.
FX_ARS_PER_USD = 1560.0
FX_DATE = dt.date(2026, 10, 9)
FX_SOURCE = ("Banco Nación, dólar oficial (venta), cotización publicada por El Cronista el 09/10/2026 "
             "(el mismo medio da el mayorista en 1.541,90); esa fuente repite cifras del día anterior: a confirmar con el cierre oficial")

SIM_START = dt.date(2026, 4, 1)          # first day of the Inicio phase (see 02-gantt/gantt.md)
ENTREGA = dt.date(2026, 10, 14)

# ---------------------------------------------------------------- the team's REAL Gantt (Excel annex to section 6)
# Source of truth for activities, durations, dates and gates: the team's own workbook, through the snapshot
# tools/team_gantt.json (a test proves the snapshot equals the Excel). Nothing here is an estimate of ours.
import team_gantt as _tg

TEAM = _tg.load()
# 'a-b' in the dependency column is read as the two endpoints {a, b}: that is what the team's own CPM sheet
# and its annex ('1, 3' for '1-3') do (see 02-gantt/gantt.md).
ACTIVITIES = [
    {"id": t["id"], "phase": _tg.PHASES.index(t["phase"]) + 1, "name": t["name"], "dur": t["dur"], "start": t["start"],
     "end": t["end"], "deps_raw": t["deps_raw"], "preds": _tg.parse_deps(t["deps_raw"], "endpoints"),
     "preds_range": _tg.parse_deps(t["deps_raw"], "range"), "entregable": t["entregable"]}
    for t in TEAM["activities"]
]
_HITO = {h["name"]: h["date"] for h in TEAM["hitos"]}
# id, Excel phase name, window declared in the summary document (F2 table), gate date declared there,
# gate date in the Excel (unchanged), hito name in the Excel
PHASES = [
    (1, "Inicio", "10/04–17/04", dt.date(2026, 4, 10), _HITO["Charter aprobado"], "Charter aprobado"),
    (2, "Análisis", "18/04–01/05", dt.date(2026, 5, 1), _HITO["Requerimientos aprobados"], "Requerimientos aprobados"),
    (3, "Diseño", "02/05–26/05", dt.date(2026, 5, 26), _HITO["Diseño aprobado"], "Diseño aprobado"),
    (4, "Desarrollo", "27/05–02/07", dt.date(2026, 7, 2), _HITO["Desarrollo completado"], "Desarrollo completado"),
    (5, "Integración", "03/07–21/07", dt.date(2026, 7, 21), _HITO["Integraciones validadas"], "Integraciones validadas"),
    (6, "Pruebas", "22/07–27/08", dt.date(2026, 8, 27), _HITO["Pruebas aprobadas"], "Pruebas aprobadas"),
    (7, "Implementación", "28/08–09/09", dt.date(2026, 9, 9), _HITO["Puesta en funcionamiento"], "Puesta en funcionamiento"),
    (8, "Cierre", "10/09–30/09", dt.date(2026, 9, 30), _HITO["Cierre del proyecto"], "Cierre del proyecto"),
]
GATES = {f"G{p[0]}": p[4] for p in PHASES}
GATES_DECLARED = {f"G{p[0]}": p[3] for p in PHASES}
# last activity of each phase that closes its gate (its stated end date is the gate date)
PHASE_LAST = {1: 4, 2: 10, 3: 17, 4: 23, 5: 26, 6: 32, 7: 35, 8: 40}
# phase 4 also finishes activity 21; the gate needs both (the later one, 23, closes it)
PHASE_GATE_ACTS = {1: [4], 2: [10], 3: [17], 4: [21, 23], 5: [26], 6: [32], 7: [35], 8: [40]}

# phase windows as written in the summary document (F2 table): they disagree with the Excel (see 02-gantt/gantt.md)
F2_PHASE_WINDOWS = {
    "Inicio": (dt.date(2026, 4, 10), dt.date(2026, 4, 17)), "Análisis": (dt.date(2026, 4, 18), dt.date(2026, 5, 1)),
    "Diseño": (dt.date(2026, 5, 2), dt.date(2026, 5, 26)), "Desarrollo": (dt.date(2026, 5, 27), dt.date(2026, 7, 2)),
    "Integración": (dt.date(2026, 7, 3), dt.date(2026, 7, 21)), "Pruebas": (dt.date(2026, 7, 22), dt.date(2026, 8, 27)),
    "Implementación": (dt.date(2026, 8, 28), dt.date(2026, 9, 9)), "Cierre": (dt.date(2026, 9, 10), dt.date(2026, 9, 30)),
}
# the 7 control points of the long document (section 6.5), merged differently from the 8 hitos
CHARTER_GATES_6_5 = [
    "Aprobación del Project Charter", "Aprobación de requerimientos", "Aprobación del diseño",
    "Finalización del desarrollo e integraciones", "Aprobación de pruebas", "Autorización de puesta en producción",
    "Cierre y transferencia operativa",
]

# Responsable column (empty in the team's sheet): PROPOSAL, one accountable ROLE per activity, always a role
# that works in that activity's window (see TEAM_ROLES below).
ACTIVITY_OWNER = {
    1: "Project Manager", 2: "Project Manager", 3: "Especialistas en datos y GIS", 4: "Project Manager",
    5: "Analistas funcionales", 6: "Analistas funcionales", 7: "Especialistas en datos y GIS",
    8: "Analistas funcionales", 9: "Analistas funcionales", 10: "Project Manager",
    11: "Desarrolladores", 12: "Especialistas en datos y GIS", 13: "Analistas funcionales", 14: "Analistas funcionales",
    15: "Desarrolladores", 16: "UX/UI", 17: "Project Manager",
    18: "Desarrolladores", 19: "Desarrolladores", 20: "Desarrolladores", 21: "Desarrolladores", 22: "Desarrolladores",
    23: "Desarrolladores", 24: "Especialistas en datos y GIS", 25: "Desarrolladores",
    26: "QA y testing", 27: "QA y testing", 28: "QA y testing", 29: "UX/UI", 30: "Seguridad informática",
    31: "Desarrolladores", 32: "QA y testing", 33: "Infraestructura/DevOps", 34: "Documentación y capacitación",
    35: "Infraestructura/DevOps", 36: "Infraestructura/DevOps", 37: "Project Manager",
    38: "Documentación y capacitación", 39: "Project Manager", 40: "Project Manager",
}

# Illustration ONLY (the team's annex says it has no three-point estimates and does not invent them): what PERT
# (O+4M+P)/6 would do on the most uncertain activities if the team agreed such ranges. M = the team's duration.
PERT_EXAMPLE = [
    {"id": 7, "o": 5, "m": 7, "p": 15}, {"id": 23, "o": 9, "m": 12, "p": 21}, {"id": 25, "o": 6, "m": 8, "p": 16},
    {"id": 27, "o": 6, "m": 8, "p": 10}, {"id": 30, "o": 6, "m": 7, "p": 10}, {"id": 31, "o": 5, "m": 7, "p": 16},
]

# ---------------------------------------------------------------- risks (IDs of the long document are the master IDs)
# team: id, short name, P, I, level (as written), response, owner  -> from F1 §9.2
# proposal: evento/problema/restriccion (Clase 5 p17 template), category (Clase 5 p25), residual P/I, response type
RISKS = [
    dict(id="R01", name="Falta de disponibilidad de APIs o fuentes necesarias", p=3, i=5, resp="Mitigar", owner="Tecnología + Datos",
         evento="las fuentes seleccionadas no ofrecen un mecanismo de integración o de acceso", problema="no se puede incorporar parte de la información al mapa",
         restr="alcance y calidad", cat="Técnico", pr=2, ir=4, hl=True),
    dict(id="R02", name="Baja calidad o desactualización de los datos", p=4, i=5, resp="Mitigar", owner="Datos + áreas responsables",
         evento="las fuentes no tienen controles suficientes de actualización", problema="los vecinos reciben información incorrecta o vencida",
         restr="calidad", cat="Técnico", pr=2, ir=4, hl=True),
    dict(id="R03", name="Problemas de integración entre sistemas", p=3, i=4, resp="Mitigar", owner="Tecnología",
         evento="los sistemas difieren en formatos o arquitectura", problema="errores de intercambio y funcionalidades incompletas",
         restr="tiempo y alcance", cat="Técnico", pr=2, ir=3, hl=False),
    dict(id="R04", name="Falta de coordinación entre áreas", p=4, i=4, resp="Mitigar", owner="Project Manager",
         evento="las áreas tienen prioridades, tiempos o responsables distintos", problema="demoras en validaciones, información y decisiones",
         restr="tiempo", cat="De la organización", pr=3, ir=3, hl=True),
    dict(id="R05", name="Crecimiento no controlado del alcance", p=4, i=5, resp="Evitar", owner="PM + Sponsor",
         evento="se agregan funcionalidades durante el desarrollo sin evaluar su impacto", problema="aumentan costos y plazos y se pierde el foco",
         restr="alcance, tiempo y costo", cat="De dirección de proyectos", pr=2, ir=4, hl=True),
    dict(id="R06", name="Baja participación de los vecinos", p=3, i=3, resp="Mitigar", owner="UX + Comunicación",
         evento="el vecino no conoce o no usa la función de reportes", problema="se generan pocos reportes y validaciones colaborativas",
         restr="alcance (valor entregado)", cat="Externo", pr=2, ir=3, hl=False),
    dict(id="R07", name="Reportes incorrectos o maliciosos", p=3, i=4, resp="Mitigar", owner="Tecnología + Datos",
         evento="los usuarios cargan reportes erróneos o con mala intención", problema="información poco confiable y alertas innecesarias",
         restr="calidad", cat="Técnico", pr=2, ir=3, hl=False),
    dict(id="R08", name="Problemas de rendimiento o disponibilidad", p=3, i=5, resp="Mitigar", owner="Tecnología + Infraestructura",
         evento="la carga supera lo previsto o la infraestructura está mal configurada", problema="el servicio no puede usarse con normalidad",
         restr="calidad", cat="Técnico", pr=2, ir=4, hl=False),
    dict(id="R09", name="Restricciones presupuestarias", p=3, i=4, resp="Mitigar", owner="Sponsor + PM",
         evento="el presupuesto resulta insuficiente o los costos aumentan", problema="se reduce el alcance o se posterga lo de menor prioridad",
         restr="costo y alcance", cat="De la organización", pr=2, ir=3, hl=False),
    dict(id="R10", name="Tratamiento inadecuado de datos personales y del perfil de hogar", p=3, i=5, resp="Evitar", owner="Datos + Seguridad", mod=True,
         evento="se recolectan datos innecesarios del hogar (incluido el perfil de hogar básico) o los controles de acceso son insuficientes", problema="riesgos de privacidad de los hogares, incumplimiento normativo y pérdida de confianza (marco legal a verificar: Ley 25.326)",
         restr="calidad y alcance", cat="Externo (regulatorio)", pr=2, ir=5, hl=False),
    dict(id="R11", name="Demoras en desarrollo o pruebas", p=3, i=4, resp="Mitigar", owner="PM + Tecnología",
         evento="hay problemas técnicos, poca disponibilidad del equipo o correcciones mayores", problema="se retrasan hitos y la puesta en funcionamiento",
         restr="tiempo", cat="De dirección de proyectos", pr=2, ir=3, hl=False),
    dict(id="R12", name="Cambios en canales digitales existentes (Boti, BAX, miBA)", p=3, i=4, resp="Mitigar", owner="Tecnología + responsables de canales",
         evento="los canales cambian sus capacidades o condiciones de integración", problema="hay que rediseñar integraciones o funcionalidades",
         restr="alcance y tiempo", cat="Externo", pr=2, ir=3, hl=True),
    dict(id="R13", name="Falta de validación de las áreas responsables", p=3, i=4, resp="Mitigar", owner="PM + áreas responsables",
         evento="las áreas demoran o no participan en las validaciones", problema="entregables incompletos o difíciles de implementar",
         restr="tiempo y alcance", cat="De la organización", pr=2, ir=3, hl=False),
    dict(id="R14", name="Fallas detectadas en las pruebas finales", p=3, i=4, resp="Mitigar", owner="QA + Tecnología",
         evento="quedan errores sin detectar en etapas anteriores", problema="se retrasa la implementación y hay retrabajo",
         restr="tiempo y calidad", cat="Técnico", pr=2, ir=3, hl=False),
    dict(id="R15", name="Confusión entre información oficial y contenido de socios", p=2, i=3, resp="Evitar", owner="PM + Comunicación", mod=True,
         evento="se incorpora contenido de socios sin diferenciarlo de lo oficial", problema="los usuarios pierden claridad sobre qué es oficial",
         restr="calidad", cat="Externo", pr=1, ir=3, hl=False),
    # --- NEW for Option B (proposal; no team rating exists, values are PROPOSED to be agreed)
    dict(id="R16", name="Las áreas no adoptan la capa común", p=3, i=4, resp="Mitigar", owner="Sponsor + PM", new=True,
         evento="las áreas siguen manteniendo su propio mapa en lugar de consumir la capa", problema="no se ven los costos evitados ni el uso de la capa",
         restr="alcance (valor entregado)", cat="De la organización", pr=2, ir=3, hl=False),
    dict(id="R17", name="Dependencia de socios y convenios (tercer lado, opcional)", p=2, i=2, resp="Aceptar", owner="Sponsor", new=True,
         evento="los convenios con socios (Banco Ciudad, Pase Cultural, etc.) no se concretan o se demoran", problema="la capa de beneficios no está disponible en el lanzamiento",
         restr="alcance (opcional)", cat="Externo", pr=2, ir=2, hl=False),
    dict(id="R18", name="Dependencia de miBA como identidad digital (supuesto a confirmar)", p=2, i=4, resp="Transferir", owner="Responsables de canales", new=True,
         evento="la integración con BAX/Boti exige miBA y el acceso no está disponible a tiempo (a confirmar con fuentes oficiales)", problema="se limita la disponibilidad multicanal",
         restr="alcance y tiempo", cat="Externo", pr=1, ir=4, hl=False),
    dict(id="R19", name="Variación del tipo de cambio ARS/USD (presupuesto expresado en USD)", p=4, i=3, resp="Mitigar", owner="Sponsor + PM", new=True,
         evento="el tipo de cambio ARS/USD se aleja del valor usado para convertir el presupuesto", problema="los costos en pesos medidos en USD se desvían del presupuesto aprobado",
         restr="costo", cat="Externo (económico, PESTEL)", pr=3, ir=3, hl=False),
]
# conversion of the team's ordinal scales to money (PROPOSAL, to agree): probability and absolute impact in M ARS
SCALE = {
    "prob": {1: 0.10, 2: 0.30, 3: 0.50, 4: 0.70, 5: 0.90},
    "impact_M": {1: 1.5, 2: 3.0, 3: 6.0, 4: 12.0, 5: 25.0},
}
# risks that go to the Charter's "riesgos de alto nivel" are the ones flagged hl=True (chosen in 04-riesgos.md)

# ---------------------------------------------------------------- budget (team figures)
TEAM_ROLES = [
    # key, label, team months, team cost M, monthly rate M (implied = cost / months), activity window (Gantt ids)
    ("pm", "Project Manager", 6, 48.0, list(range(1, 41))),
    ("af", "Analistas funcionales", 3, 18.0, [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]),
    ("dev", "Desarrolladores", 4, 40.0, [11, 12, 13, 14, 15, 18, 19, 20, 21, 22, 23, 24, 25, 31]),
    ("gis", "Especialistas en datos y GIS", 4, 32.0, [3, 7, 12, 15, 18, 23, 24, 25, 26]),
    ("ux", "UX/UI", 2, 12.0, [5, 16, 29]),
    ("qa", "QA y testing", 2, 12.0, [26, 27, 28, 29, 30, 31, 32]),
    ("sec", "Seguridad informática", 1, 8.0, [11, 30]),
    ("infra", "Infraestructura/DevOps", 2, 16.0, [11, 24, 25, 33, 35, 36]),
    ("doc", "Documentación y capacitación", 1, 4.0, [34, 38, 39]),
]
# Scenario B headcount (PROPOSAL): people (full time) during each role's window
B_QTY = {"pm": 1, "af": 2, "dev": 3, "gis": 2, "ux": 2, "qa": 2, "sec": 1, "infra": 1, "doc": 1}
OTHER_COSTS = [
    # key, label, team amount M, window (activity ids for the cash curve), items
    ("tec", "Desarrollo y tecnología", 35.0, list(range(11, 33))),
    ("dat", "Datos, GIS e integraciones", 18.0, list(range(5, 27))),
    ("inf", "Infraestructura y seguridad", 30.0, list(range(11, 41))),
    ("imp", "Implementación y capacitación", 12.0, [33, 34, 35]),
]
MAINT = ("mant", "Mantenimiento inicial (posterior a la puesta en funcionamiento)", 28.0)
TEAM_TOTAL = 344.3
TEAM_BASE = 313.0
TEAM_CONTINGENCY = 31.3

# ---------------------------------------------------------------- budget line items (the team's own section 10, §10.3-10.7)
CATEGORIES = [
    ("rh", "Recursos humanos"), ("tec", "Desarrollo y tecnología"), ("dat", "Datos, GIS e integraciones"),
    ("inf", "Infraestructura y seguridad"), ("imp", "Implementación y capacitación"), ("mant", "Mantenimiento inicial"),
]


def _r(a, b):
    return list(range(a, b + 1))


M_PARAM = "Paramétrica (tarifa mensual × personas × meses del Gantt)"
M_EXP_G = "Experta (importe global del equipo)"
M_EXP_M = "Experta (importe global del equipo, prorrateado por mes de uso)"
# id, category, concept, team amount (ARS M), kind ('mensual' = prorated over the months of its window; 'global' = one amount),
# window (Gantt activity ids; None = after the closing), behaviour (Clase 4 p13), assignment (Clase 4 p14), method (Clase 4 p18), assumption
BUDGET_LINES = [
    ("TEC1", "tec", "Herramientas y ambientes de desarrollo", 8.0, "mensual", _r(11, 32), "Fijo", "Directo", M_EXP_M, "Cuota por período de uso durante diseño, desarrollo y pruebas (§10.3)."),
    ("TEC2", "tec", "Licencias y herramientas de testing", 5.0, "mensual", _r(27, 32), "Fijo", "Directo", M_EXP_M, "Solo durante la fase de pruebas (§10.3)."),
    ("TEC3", "tec", "Herramientas de monitoreo y gestión", 5.0, "mensual", _r(1, 40), "Fijo", "Directo", M_EXP_M, "Se usan durante todo el proyecto (§10.3)."),
    ("TEC4", "tec", "Servicios tecnológicos complementarios", 7.0, "global", _r(11, 32), "Variable", "Directo", M_EXP_G, "Servicios contratados según necesidad del desarrollo (§10.3)."),
    ("TEC5", "tec", "Herramientas de soporte y documentación", 5.0, "mensual", _r(11, 40), "Fijo", "Directo", M_EXP_M, "Desde el diseño hasta el cierre (§10.3)."),
    ("TEC6", "tec", "Otros servicios técnicos", 5.0, "global", _r(11, 32), "Variable", "Directo", M_EXP_G, "Importe global sin detalle en el original (§10.3)."),
    ("DAT1", "dat", "Preparación y normalización de datos", 5.0, "global", _r(7, 12), "Variable", "Directo", M_EXP_G, "Depende de la cantidad y calidad de las fuentes (§10.4)."),
    ("DAT2", "dat", "Desarrollo y configuración de APIs", 6.0, "global", [23], "Variable", "Directo", M_EXP_G, "Coincide con la actividad 23 del Gantt (§10.4)."),
    ("DAT3", "dat", "Servicios de geocodificación y mapas", 4.0, "mensual", _r(18, 32), "Variable", "Directo", M_EXP_M, "Consumo durante desarrollo e integración; el original no da volumen (§10.4)."),
    ("DAT4", "dat", "Integración con fuentes oficiales", 3.0, "global", [24], "Variable", "Directo", M_EXP_G, "Coincide con la actividad 24 del Gantt (§10.4)."),
    ("INF1", "inf", "Infraestructura y hosting", 10.0, "mensual", _r(11, 40), "Fijo", "Directo", M_EXP_M, "Se asume infraestructura dedicada; si se comparte con otros proyectos pasa a Indirecto (§10.5)."),
    ("INF2", "inf", "Base de datos y almacenamiento", 5.0, "mensual", _r(11, 40), "Variable", "Directo", M_EXP_M, "Crece con el volumen de datos y reportes (§10.5)."),
    ("INF3", "inf", "Monitoreo y disponibilidad", 4.0, "mensual", _r(24, 40), "Fijo", "Directo", M_EXP_M, "Desde las integraciones hasta el cierre (§10.5)."),
    ("INF4", "inf", "Seguridad y controles de acceso", 6.0, "global", _r(11, 30), "Fijo", "Directo", M_EXP_G, "Se diseña en la arquitectura y se prueba en la actividad 30 (§10.5)."),
    ("INF5", "inf", "Backup y recuperación", 5.0, "mensual", _r(33, 40), "Fijo", "Directo", M_EXP_M, "Desde la puesta en producción hasta el cierre (§10.5)."),
    ("IMP1", "imp", "Preparación del entorno productivo", 4.0, "global", [33], "Fijo", "Directo", M_EXP_G, "Coincide con la actividad 33 del Gantt (§10.6)."),
    ("IMP2", "imp", "Capacitación de equipos internos", 3.0, "global", [34], "Variable", "Directo", M_EXP_G, "Depende de la cantidad de personas a capacitar (§10.6)."),
    ("IMP3", "imp", "Materiales y documentación operativa", 2.0, "global", [34], "Variable", "Directo", M_EXP_G, "Coincide con la actividad 34 del Gantt (§10.6)."),
    ("IMP4", "imp", "Soporte durante la puesta en funcionamiento", 3.0, "global", [35], "Variable", "Directo", M_EXP_G, "Coincide con la actividad 35 del Gantt (§10.6)."),
    ("MAN1", "mant", "Corrección de errores iniciales", 10.0, "global", None, "Variable", "Directo", M_EXP_G, "Posterior al cierre; sin duración definida en el original (§10.7)."),
    ("MAN2", "mant", "Soporte técnico", 7.0, "global", None, "Variable", "Directo", M_EXP_G, "Posterior al cierre; sin duración definida en el original (§10.7)."),
    ("MAN3", "mant", "Ajustes menores y optimización", 6.0, "global", None, "Variable", "Directo", M_EXP_G, "Posterior al cierre; sin duración definida en el original (§10.7)."),
    ("MAN4", "mant", "Monitoreo y mantenimiento", 5.0, "global", None, "Variable", "Directo", M_EXP_G, "Posterior al cierre; sin duración definida en el original (§10.7)."),
]
# the team's section 10 does not impute indirect costs (shared offices, utilities, overhead): to be declared in the document

# ---------------------------------------------------------------- stakeholders (F4 §7.1 and §8.1; canonical names)
STAKEHOLDERS_F4 = [
    "Sponsor institucional", "Project Manager", "Equipo de Tecnología y Desarrollo", "Equipo de Datos y GIS",
    "USIG e Innovación/ASI", "Áreas dueñas del dato (Transporte y Cultura)", "Responsables de canales (Boti, BAX, miBA)",
    "Hacienda / Presupuesto", "Comunas y áreas operativas", "Equipo UX/UI", "Comunicación institucional",
    "Vecinos y usuarios", "Prestadores de transporte público", "Proveedores tecnológicos", "Socios con oferta geolocalizada",
]
# who appears as recipient / owner in the F4 communication matrix §8.1 (normalised to the names above)
COMMS_F4 = [
    "Sponsor institucional", "Hacienda / Presupuesto", "Comunas y áreas operativas", "Project Manager",
    "Equipo de Tecnología y Desarrollo", "Equipo de Datos y GIS", "Equipo UX/UI", "Áreas dueñas del dato (Transporte y Cultura)",
    "USIG e Innovación/ASI", "Responsables de canales (Boti, BAX, miBA)", "Comunicación institucional", "Vecinos y usuarios",
    "Socios con oferta geolocalizada",
]
# proposal: two added rows in §8.1 cover the two missing stakeholders
COMMS_PROPOSED = COMMS_F4 + ["Prestadores de transporte público", "Proveedores tecnológicos"]
CHARTER_STAKEHOLDERS_PROPOSED = [
    "Sponsor institucional", "Hacienda / Presupuesto", "Project Manager", "Equipo de Tecnología y Desarrollo",
    "Equipo de Datos y GIS", "USIG e Innovación/ASI", "Áreas dueñas del dato (Transporte y Cultura)",
    "Responsables de canales (Boti, BAX, miBA)", "Vecinos y usuarios",
]

# ---------------------------------------------------------------- bridges (frases puente, PROPOSAL)
BRIDGES = {
    "apertura": "Este documento cuenta una sola historia: de la pregunta de un hogar que no sabe a qué organismo acudir, al proyecto, el cronograma, los riesgos y el presupuesto necesarios para resolverla.",
    "3": "Nuestro punto de partida es una pregunta concreta: ¿cómo hace un hogar de la Ciudad, con su propia realidad, para enterarse de lo que le corresponde y reportar lo que ve sin saber de antemano a qué organismo ni por qué canal acudir?; el Canvas muestra quién usa, quién paga y qué recibe cada lado.",
    "4": "Del Canvas surge una hipótesis de problema; Design Thinking, como investigación simulada con tres proto-personas, la convierte en un punto de vista y una pregunta de diseño y baja la idea a un prototipo de tres pantallas (consultar, reportar y seguir); la validación con hogares reales queda como actividad del proyecto.",
    "5": "Con el problema y el segmento definidos, el Charter formaliza qué vamos a construir, con qué límites y con qué metas medibles.",
    "6": "Para cumplir los objetivos del Charter ordenamos el trabajo en 40 actividades con duraciones y dependencias; su camino crítico fija la fecha de cierre.",
    "7": "Las actividades del Gantt dependen de personas y organismos con distinto poder e interés; la matriz indica cuánto esfuerzo dedicarle a cada uno.",
    "8": "La estrategia de la matriz de stakeholders se traduce en qué se comunica, a quién, con qué frecuencia y por qué canal.",
    "9": "Cada actividad del camino crítico y cada relación con un stakeholder puede fallar; la matriz de riesgos los prioriza y cuantifica su valor monetario esperado.",
    "10": "El presupuesto, expresado en USD con un tipo de cambio único, convierte el Gantt en dinero (personas × tarifa × duración) y los riesgos en una reserva de contingencia que sale de sus EMV.",
    "cierre": "Con los costos, las reservas y la línea base cerrados, volvemos a la pregunta inicial: cuánto cuesta, y en cuánto tiempo, que un hogar de la Ciudad deje de buscar a quién preguntar.",
}

# ---------------------------------------------------------------- risk -> Gantt activities exposed (PROPOSAL)
RISK_ACTS = {
    "R01": [7, 24], "R02": [7, 24, 36], "R03": [15, 25, 26], "R04": [6, 10, 17], "R05": [4, 10, 17],
    "R06": [5, 36], "R07": [19, 20], "R08": [30], "R09": [4, 18], "R10": [12, 19], "R11": [18, 19, 20, 21, 31],
    "R12": [15, 25], "R13": [10, 17], "R14": [27, 28, 29, 30, 31, 32], "R15": [38], "R16": [22, 36], "R17": [35],
    "R18": [25], "R19": [4, 18, 33],
}
# F2's four risks mapped to the master IDs of the long document
F2_TO_MASTER = {"R01": "R01", "R02": "R02", "R03 (scope creep)": "R05", "R04 (adopción de vecinos)": "R06"}


# ---------------------------------------------------------------- audit: Clase 4 p17 rubrics and indirect costs
# Proposed classification of the 32 budget lines in the rubrics of Clase 4 p17 ('qué debemos estimar').
P17_RUBRICS = [
    ("Mano de obra", [f"RH{i}" for i in range(1, 10)]),
    ("Materiales", ["IMP3"]),
    ("Subcontratistas y asesores", ["TEC4", "TEC6", "DAT3"]),
    ("Alquiler de equipo e instalaciones", ["TEC1", "TEC2", "TEC3", "TEC5", "INF1", "INF2", "INF3", "INF4", "INF5"]),
    ("Viajes", []),
    ("Otras actividades del proyecto (el original no distingue entre trabajo propio y contratado)",
     ["DAT1", "DAT2", "DAT4", "IMP1", "IMP2", "IMP4", "MAN1", "MAN2", "MAN3", "MAN4"]),
]
INDIRECT = {
    "usd": 0,
    "declared": ("Costos indirectos (seguros, impuestos, espacio de trabajo y servicios compartidos del GCBA; Clase 4, p14): "
                 "no se estiman en este presupuesto; se asume que los absorbe la organización."),
    "decision": ("Decisión del grupo: declararlo así (recomendado, es lo que dice el original) o sumar un porcentaje "
                 "sobre la mano de obra con una justificación escrita."),
}
