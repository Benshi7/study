"""Fills the cátedra's Project Charter template (raw/Project_Charter_Template5.docx) with its 24 fields.

The template is never modified: a COPY is written to 01-charter/Project_Charter_completado.docx. Only the
word/document.xml part changes (text runs in the empty value cells, row heights that were 'exact' become 'atLeast' so
the text is not clipped, and a few cloned rows for the stakeholder and milestone lists). Every other part of the
package is copied byte for byte. Numbers come from build_all.compute(), the pack's single source of truth.
"""
import copy
import io
import pathlib
import re
import xml.etree.ElementTree as ET
import zipfile

import data as D
from fmt import n, usd

HERE = pathlib.Path(__file__).resolve().parent
PACK = HERE.parent
TEMPLATE = PACK.parent.parent / "raw" / "Project_Charter_Template5.docx"
OUT = PACK / "01-charter" / "Project_Charter_completado.docx"

WNS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W = "{%s}" % WNS
XML_SPACE = "{http://www.w3.org/XML/1998/namespace}space"
DRAFT_NOTE = "Borrador del equipo, sin firmar ni aprobar. Proyecto simulado con fines académicos; cifras en USD estimativas, a confirmar."
FONT_SZ = "18"                                   # 9 pt for the values (the labels use 8-10 pt)
ZIP_DATE = (2026, 10, 12, 0, 0, 0)               # fixed so that the build is byte-for-byte deterministic


def bullets(items):
    return [f"• {x}" for x in items]


def fields(o):
    """Spanish content of the 24 fields. Keys are the field numbers; values are lists of paragraphs (or row lists)."""
    lb, fx, cal = o["ladder_b"], o["fx"], o["calendar"]
    maint, cont = o["maint_usd"], lb["contingency"]
    hl = [r for r in o["risks"]["sorted"] if r["hl"]]
    qty = ", ".join(f"{label.lower() if i else label} {D.B_QTY[key]}" for i, (key, label, *_rest) in enumerate(D.TEAM_ROLES))
    f = {}
    f[1] = ["Modernización del Mapa Interactivo de la Ciudad", "Gobierno de la Ciudad de Buenos Aires · metodología en cascada"]
    f[2] = [
        "Modernizar el Mapa Interactivo de la Ciudad para convertirlo en una plataforma geográfica común: una capa que integre información "
        "oficial de distintas áreas, la ponga a disposición del Mapa y de canales como Boti y BAX (sujeto a validación técnica) y permita que "
        "los hogares reporten, validen y sigan incidencias georreferenciadas.",
        "Duración simulada: 6 meses. Actividades desde el 01/04/2026; Charter aprobado el 10/04/2026; cierre el 30/09/2026.",
    ]
    f["pm"] = [["Director/a del proyecto (Project Manager). Rol a designar."]]
    f["auth"] = [["Planifica y coordina el proyecto; gestiona alcance, cronograma, riesgos, recursos y costos dentro de lo aprobado. "
                  "Los cambios significativos de alcance, presupuesto o cronograma requieren la aprobación del Sponsor."]]
    f["sponsor"] = [["Sponsor institucional del Gobierno de la Ciudad (a designar). Financia: Hacienda / Presupuesto."]]
    f["stype"] = [["Interno, institucional (sector público)."]]
    f[6] = bullets([
        "Capa geográfica común.",
        "Integraciones con fuentes oficiales y canales digitales (Mapa, Boti, BAX; sujeto a validación técnica).",
        "Módulo de reportes ciudadanos georreferenciados.",
        "Sistema de validación colaborativa.",
        "Sistema de seguimiento de incidencias.",
        "Vista de gestión para las áreas responsables.",
        "Documentación técnica y funcional.",
        "Plan de implementación y cierre.",
    ]) + [
        "Destinatarios: los hogares de la Ciudad. Perfil de hogar básico (dato mínimo, con consentimiento) incluido; personalización avanzada "
        "o datos sensibles que no sean necesarios, excluidos del MVP (aclaración propuesta al alcance excluido).",
        "Fuera de alcance: reemplazo de Boti/BAX, aplicación de navegación tipo Waze, resolución física de incidencias, funciones comerciales.",
    ]
    f[7] = [
        "Objetivo general: modernizar el Mapa Interactivo mediante una capa geográfica común que integre información oficial, facilite su acceso "
        "desde distintos canales y permita a los hogares reportar, validar y consultar incidencias geolocalizadas.",
        "Cuatro resultados (agrupan los 8 objetivos del Charter ampliado). Metas: propuesta; la línea base está «a medir».",
        "• Capa geográfica confiable (objetivos 1 y 7): fuentes priorizadas integradas; 100 % con responsable y frecuencia de actualización. Gate 4 · 02/07/2026.",
        "• Integración multicanal (objetivo 2): el Mapa y al menos un canal conversacional consumen la capa por API. Gate 5 · 21/07/2026.",
        "• Reportes y seguimiento (objetivos 3, 4 y 5): 100 % de los casos de prueba del flujo completo aprobados. Gate 6 · 27/08/2026.",
        "• Gestión y experiencia del hogar (objetivos 6 y 8): al menos 3 áreas operativas con acceso a la vista de gestión; perfil de hogar básico (opt-in) disponible. Gate 7 · 09/09/2026.",
    ]
    f[8] = ["A confirmar: el Charter del equipo no define sede de trabajo. Ámbito institucional: Gobierno de la Ciudad de Buenos Aires."]
    f[9] = [
        "No hay personas pre-asignadas (roles a designar).",
        f"Dotación propuesta, a acordar: {qty}.",
        "Se suman representantes de las áreas dueñas del dato y de los canales (Boti, BAX, miBA).",
    ]
    f["stakeholders"] = [
        ["Sponsor institucional", "Patrocinador: aprueba objetivos, alcance y cambios significativos (gestionar de cerca)", "Gobierno de la Ciudad de Buenos Aires"],
        ["Hacienda / Presupuesto", "Financia la partida; se le informan costos y desvíos (mantener satisfechos)", "Gobierno de la Ciudad de Buenos Aires"],
        ["Project Manager", "Coordina cronograma, cambios, riesgos y equipos (gestionar de cerca)", "Equipo de proyecto"],
        ["Equipo de Tecnología y Desarrollo; USIG e Innovación/ASI", "Construyen la plataforma, el geocodificador y las integraciones (gestionar de cerca)", "Equipo de proyecto; Gobierno de la Ciudad de Buenos Aires"],
        ["Equipo de Datos y GIS", "Capa geográfica común y calidad de los datos (gestionar de cerca)", "Equipo de proyecto"],
        ["Áreas dueñas del dato: Secretaría de Transporte (Movilidad) y Ministerio de Cultura", "Aportan y validan la información priorizada (gestionar de cerca)", "Gobierno de la Ciudad de Buenos Aires"],
        ["Responsables de canales (Boti, BAX, miBA)", "Definen la factibilidad de integrar los canales (gestionar de cerca)", "Gobierno de la Ciudad de Buenos Aires"],
        ["Vecinos y usuarios (hogares)", "Destinatarios; reportan y validan (mantener informados)", "Externo: ciudadanía"],
        ["Comunas y áreas operativas", "Gestionan los reportes de su ámbito (mantener informados)", "Gobierno de la Ciudad de Buenos Aires"],
    ]
    f["milestones"] = [[f"{h['name']}: {h['result']}", h["date"].strftime("%d/%m/%Y")] for h in D.TEAM["hitos"]]
    f[12] = [
        f"Presupuesto del proyecto (escenario B, recomendado): {usd(lb['total'])} = línea base {usd(lb['baseline'])} "
        f"(costos {usd(lb['project_costs'])} + contingencia {usd(cont)}, suma de los EMV) + reserva de gestión {usd(lb['mgmt_reserve'])} (10 %).",
        f"Mantenimiento inicial posterior al cierre: {usd(maint)}, fuera de la línea base. Total con mantenimiento: {usd(o['all_in_b'])}.",
        f"Moneda: USD. Tipo de cambio único: ARS {n(fx['value'], 2)} por USD ({fx['source'].split(',')[0]}; {fx['date']}; a confirmar). "
        "Estimación académica con las tarifas del equipo, sin cotizaciones.",
        "Detalle en la sección 10 (desglose en 32 líneas).",
    ]
    f["assumptions"] = bullets([
        "Proyecto simulado con fines académicos: fechas ficticias (01/04/2026 a 30/09/2026) y cifras estimativas.",
        "Las áreas seleccionadas ponen a disposición sus fuentes y APIs (disponibilidad a validar en el análisis).",
        "Los canales (Boti, BAX, miBA) pueden vincularse con la solución, sujeto a validación técnica.",
        "El equipo y las áreas participan en el análisis, la validación y las pruebas.",
        f"El presupuesto está en USD con un tipo de cambio único de ARS {n(fx['value'], 2)} (a confirmar).",
        "Las fuentes pueden asociarse a una referencia geográfica común.",
    ])
    f["constraints"] = bullets([
        "Alcance definido; todo cambio pasa por el control formal de cambios.",
        "Metodología en cascada: etapas, entregables y aprobaciones definidos de antemano.",
        "Dependencia de sistemas externos (fuentes, APIs y canales existentes).",
        f"Presupuesto y plazos aprobados (cronograma calculado: {cal['cpm_wd']} días hábiles).",
        "Protección de datos de los hogares: datos mínimos y con consentimiento (Ley 25.326: a verificar).",
    ])
    f[14] = [f"• {r['id']} · {r['name']} (EMV residual {usd(r['emv_usd'])}). Respuesta: {r['resp'].lower()}." for r in hl] + [
        f"Registro completo: {o['risks']['n']} riesgos en la sección 9; contingencia = suma de los EMV = {usd(cont)}."]
    f[15] = ["No aplica: es un proyecto interno del Gobierno de la Ciudad y el Charter del equipo no define contratos externos. "
             "A confirmar si se contratan proveedores tecnológicos o se firman convenios con socios (fase futura)."]
    f[16] = [
        "Problema: la información y los reportes sobre el entorno de cada hogar están repartidos entre áreas, sistemas y canales; el vecino debe saber de antemano "
        "qué área responde y por qué canal.",
        "Valor: una capa geográfica común y reutilizable; consulta y reportes con seguimiento visible para los hogares; vista de gestión para las áreas; "
        "menos soluciones geográficas duplicadas por área.",
        "Financiamiento: la partida de Hacienda / Presupuesto; el hogar no paga. Los ingresos de socios son una fase futura, fuera del presupuesto actual.",
        "Beneficios cuantitativos: a medir (no hay línea base).",
    ]
    f[17] = [
        "Expectativas inferidas de la matriz de stakeholders (sección 7); a validar con cada interesado.",
        "• Sponsor y Hacienda: decisiones informadas, costos y plazos bajo control.",
        "• Áreas dueñas del dato: que su información se use con criterios claros de calidad y actualización.",
        "• Responsables de canales: integración técnicamente viable, sin reemplazar sus canales.",
        "• Hogares: encontrar información cercana y seguir sus reportes sin conocer qué área responde.",
    ]
    f[18] = [
        "Según la matriz de stakeholders (sección 7) y el plan de comunicación (sección 8):",
        "• Gestionar de cerca: Sponsor, Project Manager, Tecnología, Datos y GIS, USIG/ASI, Transporte y Cultura, responsables de canales.",
        "• Mantener satisfechos: Hacienda / Presupuesto. Mantener informados: comunas y áreas operativas, UX/UI, comunicación institucional, hogares, prestadores y proveedores.",
        "• Monitorear: socios con oferta geolocalizada. Canales: informes quincenales, reuniones de seguimiento y solicitud formal ante cambios.",
    ]
    f[19] = bullets([
        "Hogares: consultar información oficial cercana, reportar con ubicación y categoría, y ver el estado de cada reporte.",
        "Áreas responsables: una vista de gestión para consultar y dar seguimiento a los reportes de su ámbito.",
        "Canales: acceso a la capa geográfica por API (Boti, BAX y miBA, sujeto a validación técnica).",
        "Fuentes de datos: responsable y frecuencia de actualización definidos.",
        "Sponsor y Hacienda: informes de avance, costos y cambios.",
    ])
    f[20] = bullets([
        "Información de fuentes oficiales integrada sobre una estructura geográfica común.",
        "Información y funciones disponibles en el Mapa y en los canales seleccionados.",
        "Reportes con ubicación y categoría, validación colaborativa y estados trazables hasta el cierre.",
        "Las áreas responsables consultan y siguen los reportes de su ámbito.",
        "Responsables, criterios de actualización y control de calidad definidos para cada fuente.",
        "Documentación técnica y funcional entregada; aceptación mediante pruebas funcionales y de integración.",
    ])
    f[21] = ["No aplica a este Charter: el equipo no definió un plan de mejora de procesos organizacionales. Lo más cercano es el objetivo 7 "
             "(criterios de calidad y gobernanza de los datos). A confirmar con los profesores si debe completarse."]
    f[22] = ["Metodología en cascada con etapas, hitos y aprobaciones (secciones 5 y 6) y control de cambios con evaluación de impacto "
             "(Charter ampliado, §5.9.2). Procesos internos del Gobierno de la Ciudad: a confirmar."]
    f[23] = ["No se aplican lecciones aprendidas de proyectos anteriores: los documentos del equipo no relevan la historia del Mapa Interactivo actual. A confirmar."]
    f[24] = ["Plantilla de Project Charter de la cátedra; Excel (Gantt, camino crítico e hitos); Word (documento del TP); matrices de riesgos y de "
             "comunicación del equipo; modelo de presupuesto en USD."]
    return f


# ------------------------------------------------------------------------------------------------ XML helpers
def _register(root_tag):
    for prefix, uri in re.findall(r'xmlns:([A-Za-z0-9]+)="([^"]+)"', root_tag):
        ET.register_namespace(prefix, uri)


def _make_p(ppr, text):
    p = ET.Element(W + "p")
    if ppr is not None:
        pp = copy.deepcopy(ppr)
        sp = pp.find(W + "spacing")
        if sp is not None:                                   # exact line heights would clip multi-line text
            for k in (W + "line", W + "lineRule"):
                sp.attrib.pop(k, None)
            sp.set(W + "line", "240")
            sp.set(W + "lineRule", "auto")
            sp.set(W + "before", "20")
            sp.set(W + "after", "20")
        ind = pp.find(W + "ind")
        if ind is not None:
            ind.attrib.pop(W + "right", None)
        p.append(pp)
    r = ET.SubElement(p, W + "r")
    rpr = ET.SubElement(r, W + "rPr")
    ET.SubElement(rpr, W + "rFonts", {W + a: "Calibri" for a in ("ascii", "eastAsia", "hAnsi", "cs")})
    ET.SubElement(rpr, W + "sz", {W + "val": FONT_SZ})
    ET.SubElement(rpr, W + "szCs", {W + "val": FONT_SZ})
    t = ET.SubElement(r, W + "t")
    t.set(XML_SPACE, "preserve")
    t.text = text
    return p


def _set_cell(tc, paragraphs):
    ps = tc.findall(W + "p")
    ppr = ps[0].find(W + "pPr") if ps else None
    for p in ps:
        tc.remove(p)
    for text in paragraphs:
        tc.append(_make_p(ppr, text))


def _grow(tr):
    h = tr.find(W + "trPr/" + W + "trHeight")
    if h is not None and h.get(W + "hRule") == "exact":
        h.set(W + "hRule", "atLeast")


def _cells(tr):
    return tr.findall(W + "tc")


def _clone_after(tbl, ref_row, count):
    rows, idx = [], list(tbl).index(ref_row)
    for k in range(count):
        c = copy.deepcopy(ref_row)
        tbl.insert(idx + 1 + k, c)
        rows.append(c)
    return rows


def fill_document_xml(xml, o):
    m = re.match(r"(?:<\?xml[^>]*\?>\s*)?(<w:document[^>]*>)", xml)
    root_tag = m.group(1)
    _register(root_tag)
    root = ET.fromstring(xml.encode("utf-8"))
    body = root.find(W + "body")
    t0, t1 = body.findall(W + "tbl")[:2]
    r0, r1 = t0.findall(W + "tr"), t1.findall(W + "tr")
    f = fields(o)

    def single(tr, key, idx=1):
        _set_cell(_cells(tr)[idx], f[key])
        _grow(tr)

    # ---- Part I
    single(r0[1], 1)
    single(r0[2], 2)
    c4 = _cells(r0[4])
    for cell, key in zip(c4, ("pm", "auth", "sponsor", "stype")):
        _set_cell(cell, f[key][0])
    _grow(r0[4])
    for row, key in ((5, 6), (6, 7), (7, 8), (8, 9), (21, 12), (24, 14)):
        single(r0[row], key)
    # stakeholders list (4 rows in the template, 9 needed) and milestones (4 rows, 8 needed)
    st_rows = [r0[11], r0[12], r0[13], r0[14]]
    st_rows += _clone_after(t0, r0[14], len(f["stakeholders"]) - 4)
    for tr, vals in zip(st_rows, f["stakeholders"]):
        for cell, text in zip(_cells(tr), vals):
            _set_cell(cell, [text])
        _grow(tr)
    ms_rows = [r0[17], r0[18], r0[19], r0[20]]
    ms_rows += _clone_after(t0, r0[20], len(f["milestones"]) - 4)
    for tr, vals in zip(ms_rows, f["milestones"]):
        for cell, text in zip(_cells(tr), vals):
            _set_cell(cell, [text])
        _grow(tr)
    a, c = _cells(r0[23])
    _set_cell(a, f["assumptions"])
    _set_cell(c, f["constraints"])
    _grow(r0[23])
    # ---- Parts II and III
    for row, key in ((1, 15), (2, 16), (3, 17), (4, 18), (5, 19), (6, 20), (8, 21), (9, 22), (10, 23), (11, 24)):
        single(r1[row], key)
    # ---- draft note after the signature block (labels stay blank)
    ps = body.findall(W + "p")
    last = ps[-1]
    note = _make_p(last.find(W + "pPr"), DRAFT_NOTE)
    idx = list(body).index(last)
    body.insert(idx + 1, note)

    out = ET.tostring(root, encoding="unicode")
    out = re.sub(r"^<w:document[^>]*>", lambda _: root_tag, out, count=1)
    return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + out


def build_bytes(o):
    src = zipfile.ZipFile(TEMPLATE)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for info in src.infolist():
            data = src.read(info.filename)
            if info.filename == "word/document.xml":
                data = fill_document_xml(data.decode("utf-8"), o).encode("utf-8")
            zi = zipfile.ZipInfo(info.filename, ZIP_DATE)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = info.external_attr
            z.writestr(zi, data)
    return buf.getvalue()


def write(o):
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(build_bytes(o))
    return OUT


README = PACK / "01-charter" / "README.md"


def readme_text(o):
    lb = o["ladder_b"]
    elements = [
        ("1 · Propósito o Justificación del Proyecto", "(16) Business Case; (2) Project Scope Abstract", "§5.2, §5.3", "Condensado"),
        ("2 · Descripción de Alto Nivel del Proyecto", "(2) Project Scope Abstract", "§5.1 (descripción breve), §5.5.1", "Condensado"),
        ("3 · Objetivos del Proyecto", "(7) Project Objectives", "§5.4", "Los 8 objetivos pasan a 4 resultados con metas SMART (propuesta); los 8 quedan en el Anexo A"),
        ("4 · Requisitos de Alto Nivel", "(19) Stakeholders Requirements; (6)", "No existe como tal (se deducen de §5.5–5.6)", "Redactado a partir de §5.5–5.7"),
        ("5 · Descripción del Producto o Resultados Principales", "(6) Product Description / Deliverables", "§5.6", "Los 8 entregables en una lista; aclaración del perfil de hogar"),
        ("6 · Suposiciones y Restricciones", "(13) Assumptions / Constraints", "§5.10", "Condensado + supuesto de simulación y de tipo de cambio"),
        ("7 · Cronograma de Alto Nivel", "(11) Summary Milestone Schedule", "§5.12 (sin fechas)", "Los 8 hitos con las fechas del Excel del equipo"),
        ("8 · Presupuesto de Alto Nivel", "(12) Summary Budget", "§5.8 (categorías, sin cifra)", "Cifras en USD de `03-presupuesto` (ver campo 12)"),
        ("9 · Riesgos de Alto Nivel", "(14) High Level Project Risks", "§5.9.1 (12 riesgos)", "Los 5 marcados como de alto nivel en la matriz de riesgos"),
        ("10 · Criterios de Éxito", "(20) Success Criteria", "§5.7.1", "Condensado en 6 criterios; la aceptación detallada queda en el Anexo A"),
        ("11 · Stakeholders Principales", "(10) Stakeholders List; (17), (18)", "§5.11 y matriz de stakeholders (sección 7)", "Los 9 stakeholders críticos"),
        ("12 · Responsabilidades y Autoridad del Gerente de Proyecto", "(3) Project Manager y Level of Authority", "§5.11.2 (responsabilidades); la autoridad no estaba explícita", "Autoridad redactada como propuesta"),
        ("13 · Requisitos de Aprobación del Proyecto", "(4) Sponsor, (5) Type of Sponsor y Signature(s)/Dates", "No existía como tal", "Quién aprueba: el Sponsor; las firmas quedan en blanco"),
    ]
    fields_ = [
        ("(1) Project Title", "§5.1", "Nombre del proyecto"),
        ("(2) Project Scope Abstract", "§5.1, §5.5.1", "Resumen de alcance en 2 párrafos"),
        ("(3) Project Manager · Level of Authority", "§5.11.2", "Rol a designar; autoridad propuesta"),
        ("(4) Project Sponsor(s)", "§5.11.1", "Sponsor institucional a designar"),
        ("(5) Type of Project Sponsor", "§5.11.1", "Interno, institucional (sector público)"),
        ("(6) Product Description / Deliverables", "§5.5, §5.6", "8 entregables y aclaración de alcance"),
        ("(7) Project Objectives", "§5.4", "Objetivo general y 4 resultados"),
        ("(8) Work Site", "No estaba en el Charter", "**A confirmar** (no se inventó una sede)"),
        ("(9) Pre-assigned Resources", "§5.8.1, §10.2", "Sin personas; dotación propuesta"),
        ("(10) Stakeholders List", "Sección 7", "9 filas (Name / Title / Organization)"),
        ("(11) Summary Milestone Schedule", "§5.12, Excel", "8 hitos con fecha"),
        ("(12) Summary Budget", "§10, `03-presupuesto`", f"{usd(lb['total'])} + mantenimiento {usd(o['maint_usd'])}"),
        ("(13) Assumptions · Constraints", "§5.10", "6 supuestos y 5 restricciones"),
        ("(14) High Level Project Risks", "§5.9.1, sección 9", "5 riesgos de alto nivel"),
        ("(15) Main Contract Terms & Conditions", "—", "**No aplica / a confirmar** (proyecto interno)"),
        ("(16) Business Case", "§5.2, §5.3", "Problema, valor, financiamiento"),
        ("(17) Stakeholders Main Expectations", "Sección 7", "Inferidas; a validar"),
        ("(18) Stakeholders Engagement", "Secciones 7 y 8", "Estrategia por grupo"),
        ("(19) Stakeholders Requirements", "§5.5–5.7", "5 requisitos de alto nivel"),
        ("(20) Success Criteria", "§5.7.1", "6 criterios"),
        ("(21) High Level Process Improvement Plan", "—", "**No aplica / a confirmar**"),
        ("(22) Organizational Process Definition", "§5.9.2, §5.12", "Cascada y control de cambios; procesos del GCBA a confirmar"),
        ("(23) Main Lessons Learned Applied", "—", "**A confirmar** (sin datos)"),
        ("(24) Tools & Templates", "—", "Herramientas efectivamente usadas"),
    ]
    big = lambda rows, heads: "\n".join(["| " + " | ".join(heads) + " |", "|" + "|".join("---" for _ in heads) + "|"] + ["| " + " | ".join(r) + " |" for r in rows])
    return f"""# Project Charter en la plantilla de la cátedra

> **Qué es.** `Project_Charter_completado.docx` es una **copia** de `raw/Project_Charter_Template5.docx` (la plantilla de la cátedra: 3 partes y 24 campos) con los campos completos de forma **concisa**, a partir del Charter del equipo y del pack de propuestas. La plantilla original **no se modificó** (hay una prueba que lo comprueba). El Charter largo del equipo pasa a ser el **Anexo A – Charter ampliado**: nadie pierde trabajo.

## Por qué este formato

- La Clase 3 (p14–16, diapositivas de texto) pide un Charter de **13 elementos de alto nivel en 3 partes**. La plantilla trae esos mismos elementos como campos con una caja de tamaño limitado: obliga a la concisión.
- El Charter largo (≈ 6.000 palabras) repetía en detalle lo que ya está en las secciones 6, 9 y 10; esa repetición fue la fuente de las contradicciones entre versiones.

## Los 13 elementos de la Clase 3 (p14–16) y dónde quedaron

{big([[a, b, c, d] for a, b, c, d in elements], ["Elemento (Clase 3, p14–16)", "Campo de la plantilla", "Dónde estaba en el Charter del equipo", "Qué se hizo"])}

## Los 24 campos de la plantilla

{big([[a, b, c] for a, b, c in fields_], ["Campo", "Fuente", "Contenido"])}

## Qué va al «Anexo A – Charter ampliado»

§5.3.1 (consecuencias del problema), §5.4.2 (los 8 objetivos con su texto completo), §5.5.2–5.5.3 (alcance excluido y criterio de alcance), §5.6 (los 8 entregables con detalle), §5.7.2–5.7.3 (aceptación), §5.9.2–5.9.3 (gestión y control de cambios) y §5.11 (roles). La **nota de chat** que quedó dentro del §5.4 («Para el TP, yo los mantendría…») debe borrarse antes de entregar.

## Cosas que conviene saber

- **Filas de altura fija:** la plantilla viene de un PDF y sus filas tienen altura *exacta*; en la copia pasan a *al menos* esa altura, para que el texto no se corte. Por eso el documento ocupa más de una página.
- **No se pudo renderizar:** en este entorno no hay Word ni LibreOffice. La estructura se verificó por programa (paquete válido, XML bien formado, etiquetas intactas); **abrirlo en Word y ajustar saltos de página** es parte de la prolijidad final.
- **Campos honestos:** (8) sede, (15) contratos, (21) mejora de procesos y (23) lecciones aprendidas dicen *«a confirmar»* o *«no aplica»* con su razón; **no se inventó contenido**. Las firmas quedan en blanco y se agregó una nota de borrador al pie.
- **Aclaración de alcance propuesta (campo 6):** perfil de hogar **básico** (dato mínimo, con consentimiento) **incluido**; personalización avanzada o datos sensibles innecesarios **excluidos del MVP**. La exclusión original (§5.5.2) es condicional («que no sean necesarias»), no una contradicción.
- **Se regenera** con `python3 tools/render.py` (las cifras salen del modelo; una prueba compara los campos 11 y 12 con el pack).
"""


def write_readme(o):
    README.parent.mkdir(parents=True, exist_ok=True)
    README.write_text(readme_text(o).strip() + "\n", encoding="utf-8")
    return README
