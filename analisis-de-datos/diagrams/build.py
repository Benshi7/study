#!/usr/bin/env python3
"""Generate the course diagrams (diagram-design profile "adi-unicaba").

Each diagram is computed here, so geometry is reproducible. The script writes:
  diagrams/<slug>.html   standalone page per diagram
  diagrams/index.html    gallery
and injects each SVG into its lesson/reference between <!-- diagram:slug --> markers
(first run: replaces an anchor snippet or inserts after it).

Run:  python3 diagrams/build.py
"""
from __future__ import annotations

import html
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "diagrams"

# --------------------------------------------------------------------------- primitives


def r4(v: float) -> int:
    return int(round(v / 4.0) * 4)


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def mono_w(text: str, size: int = 8) -> float:
    return len(text) * (0.6 * size + 0.06 * size)


def markers(slug: str) -> str:
    out = []
    for name, cls in (("arrow", "m-muted"), ("arrow-accent", "m-accent"), ("arrow-soft", "m-soft")):
        out.append(
            f'<marker id="{slug}-{name}" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">'
            f'<polygon class="{cls}" points="0 0, 8 3, 0 6"/></marker>'
        )
    return "<defs>" + "".join(out) + "</defs>"


def ortho(points: list[tuple[float, float]], r: float = 8) -> str:
    """Orthogonal polyline with quarter-round corners of radius r."""
    d = f"M{points[0][0]:g},{points[0][1]:g}"
    for i in range(1, len(points) - 1):
        (x0, y0), (x1, y1), (x2, y2) = points[i - 1], points[i], points[i + 1]
        dx0, dy0 = x1 - x0, y1 - y0
        dx1, dy1 = x2 - x1, y2 - y1
        l0, l1 = math.hypot(dx0, dy0), math.hypot(dx1, dy1)
        rr = min(r, l0 / 2, l1 / 2)
        ax, ay = x1 - dx0 / l0 * rr, y1 - dy0 / l0 * rr
        bx, by = x1 + dx1 / l1 * rr, y1 + dy1 / l1 * rr
        d += f" L{ax:g},{ay:g} Q{x1:g},{y1:g} {bx:g},{by:g}"
    d += f" L{points[-1][0]:g},{points[-1][1]:g}"
    return d


def path(d: str, cls: str = "edge", marker: str | None = None, slug: str = "") -> str:
    m = f' marker-end="url(#{slug}-{marker})"' if marker else ""
    return f'<path class="{cls}" d="{d}"{m}/>'


def line(x1, y1, x2, y2, cls="edge", marker=None, slug=""):
    return path(f"M{x1:g},{y1:g} L{x2:g},{y2:g}", cls, marker, slug)


def label_above(cx: float, y_line: float, text: str, cls: str = "label") -> str:
    w = r4(mono_w(text) + 10)
    return (f'<rect class="mask" x="{cx - w / 2:g}" y="{y_line - 20:g}" width="{w}" height="12" rx="2"/>'
            f'<text class="{cls}" x="{cx:g}" y="{y_line - 11:g}" text-anchor="middle">{esc(text)}</text>')


def label_side(x_line: float, cy: float, text: str, cls: str = "label") -> str:
    w = r4(mono_w(text) + 10)
    x = x_line + 8
    return (f'<rect class="mask" x="{x:g}" y="{cy - 6:g}" width="{w}" height="12" rx="2"/>'
            f'<text class="{cls}" x="{x + w / 2:g}" y="{cy + 3:g}" text-anchor="middle">{esc(text)}</text>')


def box(x, y, w, h, name, sub=None, kind="node", rx=6, name_cls="name", sub_cls=None) -> str:
    cx = x + w / 2
    sub_cls = sub_cls or ("sub-accent" if kind == "focal" else "sub")
    out = [f'<rect class="mask" x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{rx}"/>',
           f'<rect class="{kind}" x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{rx}"/>']
    if sub:
        out.append(f'<text class="{name_cls}" x="{cx:g}" y="{y + h / 2 - 2:g}" text-anchor="middle">{esc(name)}</text>')
        out.append(f'<text class="{sub_cls}" x="{cx:g}" y="{y + h / 2 + 12:g}" text-anchor="middle">{esc(sub)}</text>')
    else:
        out.append(f'<text class="{name_cls}" x="{cx:g}" y="{y + h / 2 + 4:g}" text-anchor="middle">{esc(name)}</text>')
    return "".join(out)


def text(x, y, content, cls="sub", anchor="start") -> str:
    return f'<text class="{cls}" x="{x:g}" y="{y:g}" text-anchor="{anchor}">{esc(content)}</text>'


def legend(y: float, width: float, items: list[str]) -> str:
    """items: already-rendered SVG snippets placed left to right."""
    return (f'<line class="rule" x1="24" y1="{y:g}" x2="{width - 24:g}" y2="{y:g}"/>'
            + text(24, y + 24, "LEYENDA", "eyebrow") + "".join(items))


def svg_wrap(slug, w, h, title, desc, body) -> str:
    # max-width keeps each diagram at its natural scale instead of stretching narrow viewBoxes.
    return (f'<svg class="dg" viewBox="0 0 {w} {h}" style="max-width:{w}px;margin-inline:auto" role="img" aria-labelledby="{slug}-title {slug}-desc" '
            f'xmlns="http://www.w3.org/2000/svg">'
            f'<title id="{slug}-title">{esc(title)}</title><desc id="{slug}-desc">{esc(desc)}</desc>'
            f'{markers(slug)}<rect class="bg" width="100%" height="100%"/>{body}</svg>')


# --------------------------------------------------------------------------- diagrams

DIAGRAMS = []


def diagram(fn):
    DIAGRAMS.append(fn)
    return fn


@diagram
def c_level():
    slug, W, H = "c-level", 800, 380
    b = []
    # Tree connectors first (drawn behind boxes).
    b.append(line(400, 80, 400, 104, "tree"))
    b.append(path(ortho([(112, 156), (112, 104), (688, 104), (688, 156)]), "tree"))
    b.append(line(304, 104, 304, 156, "tree"))
    b.append(line(496, 104, 496, 156, "tree"))
    zones = [("Tecnología", 24), ("Seguridad", 216), ("Negocio", 408), ("Datos", 600)]
    zone_svg = []
    for name, zx in zones:
        zone_svg.append(f'<rect class="zone" x="{zx}" y="128" width="176" height="188" rx="8"/>')
        zone_svg.append(text(zx + 12, 144, name.upper(), "eyebrow"))
    b = zone_svg + b  # zones are containers: paint them first
    b.append(line(112, 212, 112, 244, "edge edge-dashed"))
    b.append(line(304, 212, 304, 244, "edge edge-dashed"))
    b.append(label_side(112, 228, "NO CONFUNDIR"))
    b.append(label_side(304, 228, "NO CONFUNDIR"))
    b.append(box(320, 24, 160, 56, "CEO · Executive", "visión y estrategia"))
    b.append(box(32, 156, 160, 56, "CIO · Information", "opera sistemas de info"))
    b.append(box(32, 244, 160, 56, "CTO · Technology", "I+D · construye productos"))
    b.append(box(224, 156, 160, 56, "CSO · Security", "seguridad en general"))
    b.append(box(224, 244, 160, 56, "CISO · Info Security", "seguridad de la info"))
    b.append(box(416, 156, 160, 56, "CBDO · Business Dev.", "crecer con oportunidades"))
    b.append(box(608, 156, 160, 56, "CDO · Data", "estrategia de los datos", "focal"))
    b.append(text(496, 260, "no confundir con el CEO:", "sub", "middle"))
    b.append(text(496, 276, "el CEO fija la visión", "sub", "middle"))
    b.append(text(688, 260, "\"Director de Datos\":", "sub", "middle"))
    b.append(text(688, 276, "políticas transversales", "sub", "middle"))
    b.append(legend(332, W, [
        '<rect class="focal" x="104" y="348" width="16" height="12" rx="3"/>',
        text(128, 357, "foco de la materia (CDO)", "sub"),
        '<line class="edge edge-dashed" x1="304" y1="354" x2="336" y2="354"/>',
        text(344, 357, "pares que el choice suele invertir", "sub"),
    ]))
    return dict(
        slug=slug, w=W, h=H, svg=svg_wrap(slug, W, H, "Roles C-level de la organización data-driven",
            "Organigrama con el CEO arriba y los roles agrupados por área: CIO y CTO en tecnología, CSO y CISO en seguridad, CBDO en negocio y CDO en datos.", "".join(b)),
        eyebrow="Lección 0003 · roles", h1="Quién es quién en el C-level",
        subtitle="Slide 12: incorporación de nuevas áreas y perfiles. Los pares punteados son los que el choice invierte.",
        caption="Tres pares que se confunden y el CDO como foco.",
        targets=[("lessons/0003-roles-c-level.html", "replace", '<pre class="diagram">                    CEO')],
        lesson="lessons/0003-roles-c-level.html")


@diagram
def dikw():
    slug, W, H = "dikw", 800, 352
    cx, ys, ws = 272, [312, 248, 184, 120, 56], [480, 384, 288, 192, 96]
    layers = [
        ("Datos", "elementos discontinuos", ["Registrar hechos y eventos", "del mundo real"], False),
        ("Información", "datos procesados", ["Dar contexto y significado", "a los datos"], True),
        ("Conocimiento", "aplicar la información", ["Resolver problemas y", "generar valor"], False),
        ("Sabiduría", None, ["Juicio y comprensión profunda", "para decisiones estratégicas"], False),
    ]
    b = [line(16, 300, 16, 64, "edge", "arrow", slug), text(8, 48, "MÁS VALOR", "eyebrow"),
         text(560, 48, "PROPÓSITO DE CADA NIVEL", "eyebrow")]
    for i, (name, sub, purpose, focal) in enumerate(layers):
        yb, yt, wb, wt = ys[i], ys[i + 1], ws[i], ws[i + 1]
        pts = f"{cx - wb / 2:g},{yb} {cx + wb / 2:g},{yb} {cx + wt / 2:g},{yt} {cx - wt / 2:g},{yt}"
        b.append(f'<polygon class="{"layer-focal" if focal else "layer"}" points="{pts}"/>')
        mid = (yb + yt) / 2
        if sub:
            b.append(text(cx, mid - 2, name, "name", "middle"))
            b.append(text(cx, mid + 12, sub, "sub-accent" if focal else "sub", "middle"))
        else:
            b.append(text(cx, mid + 4, name, "name", "middle"))
        edge_x = cx + (wb + wt) / 4
        b.append(f'<line class="leader" x1="{edge_x + 8:g}" y1="{mid:g}" x2="548" y2="{mid:g}"/>')
        b.append(text(560, mid - 2, purpose[0], "name" if focal else "body"))
        b.append(text(560, mid + 14, purpose[1], "name" if focal else "body"))
    b.append(text(16, 340, "Fuente: Hey, «The Data, Information, Knowledge, Wisdom Chain», citado en los slides.", "sub"))
    return dict(
        slug=slug, w=W, h=H, svg=svg_wrap(slug, W, H, "Pirámide DIKW",
            "Pirámide de cuatro niveles, de datos en la base a sabiduría en la cima, con el propósito de cada nivel; información está destacada.", "".join(b)),
        eyebrow="Lección 0005 · del dato al insight", h1="¿Datos e información son lo mismo? No.",
        subtitle="La pirámide DIKW: cada nivel agrega valor sobre el anterior. Un insight es información de valor para decidir.",
        caption="DIKW: información son datos procesados, con contexto y significado.",
        targets=[("lessons/0005-del-dato-al-insight.html", "replace", '<pre class="diagram">          SABIDURÍA')],
        lesson="lessons/0005-del-dato-al-insight.html")


def _circle_rect_hits(cx, cy, R, x, y, w, h):
    hits = []
    for xe in (x, x + w):
        s = R * R - (xe - cx) ** 2
        if s >= 0:
            for sign in (-1, 1):
                yy = cy + sign * math.sqrt(s)
                if y - 1e-6 <= yy <= y + h + 1e-6:
                    hits.append((xe, yy))
    for ye in (y, y + h):
        s = R * R - (ye - cy) ** 2
        if s >= 0:
            for sign in (-1, 1):
                xx = cx + sign * math.sqrt(s)
                if x - 1e-6 <= xx <= x + w + 1e-6:
                    hits.append((xx, ye))
    return hits


@diagram
def flujo_da():
    slug, W, H = "flujo-da", 720, 616
    cx, cy, R, sw, sh, hw, hh = 360, 284, 200, 160, 56, 176, 88
    stations = [
        ("Problema o pregunta", "¿qué necesita el negocio?", True),
        ("Hipótesis", "suposición a validar", False),
        ("Exploración y consultas", "SQL · Python", False),
        ("Recopilar info de valor", "datos relevantes", False),
        ("Visualizaciones", "gráficos claros", False),
        ("Comunicar hallazgos", "storytelling", False),
    ]
    n = len(stations)
    rects = []
    for k in range(n):
        th = math.radians(-90 + k * 360 / n)
        px, py = cx + R * math.cos(th), cy + R * math.sin(th)
        rects.append((r4(px - sw / 2), r4(py - sh / 2), th))
    b = []
    # Ring arcs on the station circle, clockwise, exit(k) -> entry(k+1).
    def classify(k):
        x, y, th = rects[k]
        pts = _circle_rect_hits(cx, cy, R, x, y, sw, sh)
        def delta(p):
            a = math.atan2(p[1] - cy, p[0] - cx)
            return (a - th + math.pi) % (2 * math.pi) - math.pi
        entry = min(pts, key=delta)
        exit_ = max(pts, key=delta)
        return entry, exit_
    for k in range(n):
        j = (k + 1) % n
        _, ex = classify(k)
        en, _ = classify(j)
        phi = math.atan2(en[1] - cy, en[0] - cx) - 1.2 / R
        qx, qy = cx + R * math.cos(phi), cy + R * math.sin(phi)
        b.append(f'<path class="edge" d="M{ex[0]:.3f},{ex[1]:.3f} A{R},{R} 0 0 1 {qx:.3f},{qy:.3f}" marker-end="url(#{slug}-arrow)"/>')
    # Dashed write-back spokes from "Recopilar" (3) and "Comunicar" (5) into the hub.
    for k in (3, 5):
        x, y, _ = rects[k]
        pcx, pcy = x + sw / 2, y + sh / 2
        ux, uy = pcx - cx, pcy - cy
        L = math.hypot(ux, uy)
        ux, uy = ux / L, uy / L
        def bd(a, bb):
            ds = []
            if abs(ux) > 1e-9: ds.append(a / abs(ux))
            if abs(uy) > 1e-9: ds.append(bb / abs(uy))
            return min(ds)
        ds, dh = bd(sw / 2, sh / 2), bd(hw / 2, hh / 2)
        sx, sy = pcx - ds * ux, pcy - ds * uy
        exx, eyy = cx + (dh + 6) * ux, cy + (dh + 6) * uy
        b.append(f'<path class="edge-soft" d="M{sx:.3f},{sy:.3f} L{exx:.3f},{eyy:.3f}" marker-end="url(#{slug}-arrow-soft)"/>')
    # Label on the closing arc (outside the ring, clear of both stations).
    b.append('<rect class="mask" x="184" y="84" width="84" height="12" rx="2"/>')
    b.append(text(226, 93, "NUEVA PREGUNTA", "label", "middle"))
    for k, (name, sub, focal) in enumerate(stations):
        x, y, _ = rects[k]
        b.append(box(x, y, sw, sh, name, sub, "focal" if focal else "node"))
    b.append(f'<rect class="hub" x="{cx - hw / 2:g}" y="{cy - hh / 2:g}" width="{hw}" height="{hh}" rx="8"/>')
    b.append(text(cx, cy - 2, "Insights", "name-inverse", "middle"))
    b.append(text(cx, cy + 16, "información de valor", "sub-inverse", "middle"))
    b.append(legend(572, W, [
        '<line class="edge" x1="104" y1="592" x2="136" y2="592"/>',
        text(144, 595, "flujo de trabajo, iterativo", "sub"),
        '<line class="edge-soft" x1="344" y1="592" x2="376" y2="592"/>',
        text(384, 595, "lo que alimenta los insights", "sub"),
    ]))
    return dict(
        slug=slug, w=W, h=H, svg=svg_wrap(slug, W, H, "Flujo de trabajo del Data Analyst",
            "Ciclo de seis pasos, de la pregunta de negocio a comunicar hallazgos, que vuelve a empezar con una nueva pregunta y alimenta los insights del centro.", "".join(b)),
        eyebrow="Lección 0005 · Data Analyst", h1="El flujo del Data Analyst es un ciclo",
        subtitle="Las respuestas generan nuevas preguntas. Cada vuelta deja evidencia y hallazgos como insights.",
        caption="Pregunta → hipótesis → exploración → recopilar → visualizar → comunicar, y otra vez.",
        targets=[("lessons/0005-del-dato-al-insight.html", "replace", '<pre class="diagram">1 Problema / pregunta')],
        lesson="lessons/0005-del-dato-al-insight.html")


@diagram
def tipos_datos():
    slug, W, H = "tipos-datos", 800, 340
    b = [line(400, 72, 400, 92, "tree"),
         path(ortho([(248, 112), (248, 92), (628, 92), (628, 112)]), "tree"),
         line(248, 160, 248, 184, "tree"),
         path(ortho([(96, 208), (96, 184), (400, 184), (400, 208)]), "tree"),
         line(248, 184, 248, 208, "tree"),
         line(628, 160, 628, 184, "tree"),
         path(ortho([(552, 208), (552, 184), (704, 184), (704, 208)]), "tree")]
    b.append(box(320, 24, 160, 48, "Datos", "atributo de un hecho"))
    b.append(box(168, 112, 160, 48, "Cualitativos", "no cuantificables"))
    b.append(box(548, 112, 160, 48, "Cuantitativos", "cuantificables"))
    leaves = [("Nominales", "sin orden", "color de ojos", False),
              ("Ordinales", "el orden importa", "alto · medio · bajo", False),
              ("Binarias", "dos valores", "sí / no · frío / caliente", True),
              ("Discretos", "enteros, indivisibles", "cantidad de hijos", False),
              ("Continuos", "valor en un intervalo", "altura: 1.78 m", False)]
    for i, (name, sub, ex, focal) in enumerate(leaves):
        x = 28 + i * 152
        b.append(box(x, 208, 136, 52, name, sub, "focal" if focal else "node"))
        b.append(text(x + 68, 280, ex, "note", "middle"))
    b.append(legend(300, W, [
        '<rect class="focal" x="104" y="316" width="16" height="12" rx="3"/>',
        text(128, 325, "trampa: binarias va del lado CUALITATIVO (slide 24)", "sub"),
    ]))
    return dict(
        slug=slug, w=W, h=H, svg=svg_wrap(slug, W, H, "Tipos de datos según la cátedra",
            "Árbol que divide los datos en cualitativos (nominales, ordinales, binarias) y cuantitativos (discretos, continuos), con un ejemplo de cada uno.", "".join(b)),
        eyebrow="Bloque 1 · tipos de datos", h1="El árbol de tipos de datos",
        subtitle="Slide 24 de la introducción. Clasificá por los valores, no por el nombre de la columna.",
        caption="Tipos de datos (slide 24): binarias está del lado cualitativo.",
        targets=[("reference/datos-y-analisis.html", "replace", '<pre class="diagram">                         DATOS'),
                 ("lessons/0006-repaso-intercalado-bloque-1.html", "after",
                  '<span class="sidenote">Árbol de tipos de datos y tabla de tipos de análisis: <a href="../reference/datos-y-analisis.html">Referencia · Datos y análisis</a>.</span>')],
        lesson="lessons/0006-repaso-intercalado-bloque-1.html")


@diagram
def try_except():
    slug, W, H = "try-except", 800, 488
    b = [line(320, 64, 320, 96, "edge", "arrow", slug),
         line(320, 144, 320, 168, "edge", "arrow", slug),
         line(432, 212, 520, 212, "edge-accent", "arrow-accent", slug),
         label_above(476, 212, "SÍ", "label-accent"),
         line(320, 256, 320, 296, "edge", "arrow", slug),
         label_side(320, 276, "NO"),
         line(320, 344, 320, 392, "edge"),
         path(ortho([(640, 236), (640, 396), (324, 396)]), "edge"),
         line(320, 400, 320, 424, "edge", "arrow", slug)]
    b.append(box(240, 24, 160, 40, "Entra al try", None, "node", rx=20))
    b.append(box(200, 96, 240, 48, "Ejecuta el try línea a línea", "print('2') → 10 / 0 → …"))
    b.append('<polygon class="mask" points="320,168 432,212 320,256 208,212"/>')
    b.append('<polygon class="node" points="320,168 432,212 320,256 208,212"/>')
    b.append(text(320, 216, "¿Alguna línea falla?", "name", "middle"))
    b.append(box(520, 188, 240, 48, "Salta al except", "el resto del try NO se ejecuta", "focal"))
    b.append(box(200, 296, 240, 48, "El try termina completo", "el except se saltea"))
    b.append('<circle class="dot" cx="320" cy="396" r="4"/>')
    b.append(box(200, 424, 240, 40, "Sigue después del try/except", None, "node", rx=20))
    b.append(text(472, 316, "Ejemplo del notebook:", "note"))
    b.append(text(472, 332, "imprime 1 · 2 · 4 · 5", "note"))
    return dict(
        slug=slug, w=W, h=H, svg=svg_wrap(slug, W, H, "Flujo de try / except",
            "Diagrama de flujo: si una línea del try falla, se salta al except sin ejecutar el resto del try; si no falla, el except se saltea; en ambos casos el programa sigue.", "".join(b)),
        eyebrow="Lección 0010 · manejo de errores", h1="Qué pasa cuando algo falla dentro del try",
        subtitle="El error corta el try en esa línea: las siguientes no corren. Después, el programa sigue igual.",
        caption="try/except: por qué el ejemplo del notebook imprime 1, 2, 4, 5.",
        targets=[("lessons/0010-errores-y-bucles.html", "replace", '<pre class="diagram">try:                       ← intenta este bloque')],
        lesson="lessons/0010-errores-y-bucles.html")


@diagram
def sql_orden():
    slug, W, H = "sql-orden", 800, 196
    names = ["FROM", "WHERE", "GROUP BY", "HAVING", "SELECT", "ORDER BY", "LIMIT"]
    subs = ["tabla(s)", "filtra FILAS", "agrupa", "filtra GRUPOS", "elige columnas", "ordena", "recorta"]
    focal = {1, 3}
    b = [text(20, 28, "ORDEN EN QUE EL MOTOR EVALÚA LA CONSULTA", "eyebrow")]
    for i in range(len(names) - 1):
        x = 20 + i * 112
        b.append(line(x + 88, 72, x + 112, 72, "edge", "arrow", slug))
    for i, (n, s) in enumerate(zip(names, subs)):
        x = 20 + i * 112
        kind = "focal" if i in focal else "node"
        b.append(f'<rect class="mask" x="{x}" y="48" width="88" height="48" rx="6"/>'
                 f'<rect class="{kind}" x="{x}" y="48" width="88" height="48" rx="6"/>')
        b.append(text(x + 8, 62, str(i + 1), "eyebrow"))
        b.append(text(x + 44, 80, n, "name-mono", "middle"))
        b.append(text(x + 44, 116, s, "sub-accent" if i in focal else "sub", "middle"))
    b.append(text(400, 152, "WHERE no ve agregados ni alias del SELECT: todavía no existen.", "note", "middle"))
    b.append(text(400, 176, "se escribe: SELECT … FROM … WHERE … GROUP BY … HAVING … ORDER BY … LIMIT", "sub", "middle"))
    return dict(
        slug=slug, w=W, h=H, svg=svg_wrap(slug, W, H, "Orden de evaluación de SQL",
            "Las siete cláusulas en el orden en que el motor las evalúa: FROM, WHERE, GROUP BY, HAVING, SELECT, ORDER BY y LIMIT; WHERE y HAVING destacadas.", "".join(b)),
        eyebrow="Lección 0014 · SELECT", h1="Se escribe en un orden, se evalúa en otro",
        subtitle="WHERE filtra filas antes de agrupar; HAVING filtra grupos después.",
        caption="WHERE (filas) vs HAVING (grupos), según el orden de evaluación.",
        targets=[("lessons/0014-sql-select-y-agregacion.html", "after", "FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT</pre>")],
        lesson="lessons/0014-sql-select-y-agregacion.html")


@diagram
def medallion():
    slug = "medallion"
    tier_w, tier_h, gap, pad = 172, 380, 16, 16
    tiers = [
        dict(name="Bronze", bucket="raw / ingesta", style="outer",
             f=["datos crudos, sin transformar", "landing zone · full load", "Data Engineer (ingesta)"],
             ex=["CSV tal como llegó", "histórico completo"]),
        dict(name="Silver", bucket="cleaned / conformed", style="focal",
             f=["limpiar, validar, estandarizar", "ODS · staging · normalizado", "Data Engineer (cleansing)"],
             ex=["sin duplicados", "tipos corregidos"]),
        dict(name="Gold", bucket="business / curated", style="default",
             f=["agregar y modelar para BI", "DWH · Data Mart · Power BI", "Data Analyst · BI (consume)"],
             ex=["fact_ventas · dim_cliente", "KPIs y métricas"]),
    ]
    promos = [("LIMPIEZA", True), ("MODELADO", False)]
    n = len(tiers)
    W = pad + n * tier_w + (n - 1) * gap + pad
    H = 80 + tier_h + 16
    tx = [pad + i * (tier_w + gap) for i in range(n)]
    tcx = [x + tier_w / 2 for x in tx]
    b = []
    for i, (lab, foc) in enumerate(promos):
        cls, mk = ("edge-accent", "arrow-accent") if foc else ("edge", "arrow")
        b.append(f'<path class="{cls}" d="M{tcx[i]:g},80 C{tcx[i]:g},0 {tcx[i + 1]:g},0 {tcx[i + 1]:g},80" marker-end="url(#{slug}-{mk})"/>')
        b.append(text((tcx[i] + tcx[i + 1]) / 2, 50, lab, "label-accent" if foc else "label", "middle"))
    field_labels = ["QUÉ PASA", "EN EL SLIDE", "QUIÉN"]
    for i, t in enumerate(tiers):
        x, cxx, st = tx[i], tcx[i], t["style"]
        card_cls = {"outer": "node-soft", "focal": "focal", "default": "node"}[st]
        band_cls = {"outer": "band-outer", "focal": "band-focal", "default": "band"}[st]
        b.append(f'<rect class="mask" x="{x}" y="80" width="{tier_w}" height="{tier_h}" rx="6"/>')
        b.append(f'<rect class="{card_cls}" x="{x}" y="80" width="{tier_w}" height="{tier_h}" rx="6"/>')
        b.append(f'<path class="{band_cls}" d="M{x},86 Q{x},80 {x + 6},80 H{x + tier_w - 6} Q{x + tier_w},80 {x + tier_w},86 V130 H{x} Z"/>')
        b.append(text(cxx, 106, t["name"], "name-lg", "middle"))
        b.append(text(cxx, 144, t["bucket"], "sub-accent" if st == "focal" else "sub", "middle"))
        for k, (lab, val) in enumerate(zip(field_labels, t["f"])):
            ly = 180 + 40 * k
            b.append(text(x + 16, ly, lab, "eyebrow"))
            b.append(f'<foreignObject x="{x + 16}" y="{ly + 6}" width="140" height="24">'
                     f'<div xmlns="http://www.w3.org/1999/xhtml" class="fo">{esc(val)}</div></foreignObject>')
        b.append(f'<line class="rule" x1="{x + 16}" y1="344" x2="{x + tier_w - 16}" y2="344"/>')
        b.append(text(x + 16, 360, "EJEMPLO", "eyebrow"))
        for k, e in enumerate(t["ex"]):
            b.append(text(x + 16, 374 + 14 * k, e, "sub-accent" if st == "focal" else "sub"))
    return dict(
        slug=slug, w=W, h=H, svg=svg_wrap(slug, W, H, "Arquitectura Medallion",
            "Tres capas de refinamiento: Bronze con datos crudos, Silver con datos limpios y validados (destacada) y Gold con datos modelados para BI.", "".join(b)),
        eyebrow="Lección 0013 · Data Warehouse", h1="Medallion: Bronze → Silver → Gold",
        subtitle="Capas de refinamiento progresivo. El paso a Silver es el data cleansing del bloque 1.",
        caption="Medallion: la limpieza (Bronze → Silver) conecta con el data cleansing del bloque 1.",
        targets=[("lessons/0013-data-warehouse-y-medallion.html", "before",
                  '<div class="box">\n  <span class="label">Conectá con el bloque 1</span>')],
        lesson="lessons/0013-data-warehouse-y-medallion.html")


def _entity(x, y, w, tag, name, fields, focal=False):
    h = 28 + 16 * len(fields) + 12
    cls = "focal" if focal else "node"
    out = [f'<rect class="mask" x="{x}" y="{y}" width="{w}" height="{h}" rx="6"/>',
           f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="6"/>',
           f'<rect class="mask" x="{x + 8}" y="{y + 8}" width="36" height="12" rx="2"/>',
           f'<rect class="{"focal" if focal else "node-soft"}" x="{x + 8}" y="{y + 8}" width="36" height="12" rx="2"/>',
           text(x + 26, y + 17, tag, "eyebrow", "middle"),
           text(x + 52, y + 19, name, "name"),
           f'<line class="rule" x1="{x}" y1="{y + 28}" x2="{x + w}" y2="{y + 28}"/>']
    for i, f in enumerate(fields):
        out.append(text(x + 12, y + 46 + 16 * i, f, "field"))
    return "".join(out), h


@diagram
def estrella():
    slug, W, H = "estrella", 800, 556
    b = [line(400, 196, 400, 120, "edge"), line(500, 264, 584, 264, "edge"),
         line(216, 264, 300, 264, "edge"), line(400, 332, 400, 408, "edge")]
    for x, y, t in [(408, 188, "N"), (408, 136, "1"), (508, 254, "N"), (568, 254, "1"),
                    (224, 254, "1"), (284, 254, "N"), (408, 348, "N"), (408, 400, "1")]:
        b.append(f'<rect class="mask" x="{x - 2}" y="{y - 8}" width="12" height="10" rx="2"/>')
        b.append(text(x + 4, y, t, "label", "middle"))
    fact, _ = _entity(300, 196, 200, "FACT", "fact_ventas",
                      ["→ fecha_id", "→ cliente_id", "→ producto_id", "→ tienda_id", "monto", "cantidad"], focal=True)
    b.append(fact)
    for (x, y, name, fields) in [
        (312, 32, "dim_fecha", ["# fecha_id", "año · mes · día", "trimestre"]),
        (584, 220, "dim_cliente", ["# cliente_id", "nombre", "segmento · ciudad"]),
        (40, 220, "dim_tienda", ["# tienda_id", "nombre", "ciudad · región"]),
        (312, 408, "dim_producto", ["# producto_id", "nombre", "categoría · precio"]),
    ]:
        b.append(_entity(x, y, 176, "DIM", name, fields)[0])
    b.append(legend(516, W, [
        text(104, 543, "# clave primaria (PK)", "sub"),
        text(264, 543, "→ clave foránea (FK)", "sub"),
        text(424, 543, "1 — N: una fila de la dim, muchas en la fact", "sub"),
    ]))
    return dict(
        slug=slug, w=W, h=H, svg=svg_wrap(slug, W, H, "Esquema estrella",
            "Modelo en estrella con la tabla de hechos fact_ventas en el centro y cuatro dimensiones alrededor (fecha, cliente, tienda, producto), unidas por relaciones uno a muchos.", "".join(b)),
        eyebrow="Lección 0013 · Data Warehouse", h1="El esquema estrella",
        subtitle="La fact guarda las métricas y las FK; cada dimensión aporta contexto con su PK.",
        caption="Estrella: las FK de la fact apuntan a la PK de cada dimensión.",
        targets=[("lessons/0013-data-warehouse-y-medallion.html", "replace", '<pre class="diagram">                 DIM_FECHA')],
        lesson="lessons/0013-data-warehouse-y-medallion.html")


@diagram
def vida_dato():
    slug, W, H = "vida-dato", 720, 412
    cols = [24, 256, 488]  # stage columns, 208 wide, 24 apart
    b = [line(232, 44, 256, 44, "edge", "arrow", slug), line(464, 44, 488, 44, "edge", "arrow", slug)]
    # Band for dimensions that can fail at any stage (container: painted before its cards).
    b.append('<rect class="zone" x="24" y="244" width="672" height="92" rx="8"/>')
    b.append(text(40, 262, "EN CUALQUIER ETAPA", "eyebrow"))
    for x, name, sub in [(cols[0], "Nace", "se genera o se carga"),
                         (cols[1], "Viaja / se guarda", "transferencia · almacenamiento"),
                         (cols[2], "Se usa", "reportes · decisiones")]:
        b.append(box(x, 24, 208, 40, name, None, "store"))
        b.append(text(x + 104, 80, sub, "sub", "middle"))
    b.append(box(cols[0], 96, 208, 56, "Configuración", "¿se generó del modo correcto?", "focal"))
    b.append(box(cols[1], 96, 208, 56, "Integridad", "¿llegó sin romperse?", "focal"))
    b.append(box(cols[2], 96, 208, 56, "Tempestividad", "¿está disponible a tiempo?"))
    b.append(box(cols[2], 168, 208, 56, "Consistencia", "¿dice lo mismo en todos lados?"))
    b.append(text(cols[0] + 104, 176, "nunca estuvo bien", "note", "middle"))
    b.append(text(cols[1] + 104, 176, "estuvo bien, se rompió después", "note", "middle"))
    for x, name, sub in [(40, "Completitud", "¿están los obligatorios?"),
                         (260, "Duplicados", "¿se repite sin necesidad?"),
                         (480, "Precisión", "¿refleja la realidad?")]:
        b.append(box(x, 272, 200, 48, name, sub))
    b.append(text(360, 364, "Configuración vs integridad: ¿estuvo bien alguna vez?", "note", "middle"))
    b.append(legend(380, W, [
        '<rect class="focal" x="104" y="396" width="16" height="12" rx="3"/>',
        text(128, 405, "el par que se confunde en el choice", "sub"),
    ]))
    return dict(
        slug=slug, w=W, h=H, svg=svg_wrap(slug, W, H, "La vida del dato y las dimensiones de calidad",
            "Tres etapas del dato (nace, viaja, se usa) con la dimensión de calidad que falla en cada una, y una banda con completitud, duplicados y precisión, que pueden fallar en cualquier etapa.", "".join(b)),
        eyebrow="Lección 0001 · calidad de datos", h1="La vida del dato",
        subtitle="Seguí al dato desde que nace hasta que se usa: en qué momento falló te dice qué dimensión es.",
        caption="Dimensiones de calidad según la etapa en que falla el dato.",
        targets=[("lessons/0001-dimensiones-de-calidad.html", "replace", '<pre class="diagram">  NACE'),
                 ("reference/calidad-y-gobierno.html", "after",
                  "→ tempestividad · <strong>contradice otra fuente</strong> → consistencia.</p>")],
        lesson="lessons/0001-dimensiones-de-calidad.html")


def _grid(x, y, cols, header, rows, focal_rows=(), kind="node"):
    """Small result table: header row + data rows; 'NULL' cells render in accent."""
    w = sum(cols)
    h = 20 + 18 * len(rows) + 6
    out = [f'<rect class="mask" x="{x}" y="{y}" width="{w}" height="{h}" rx="4"/>',
           f'<rect class="{kind}" x="{x}" y="{y}" width="{w}" height="{h}" rx="4"/>']
    xs = [x + sum(cols[:i]) for i in range(len(cols))]
    for cx, head in zip(xs, header):
        out.append(text(cx + 8, y + 14, head, "eyebrow"))
    out.append(f'<line class="rule" x1="{x}" y1="{y + 20}" x2="{x + w}" y2="{y + 20}"/>')
    for r, row in enumerate(rows):
        ry = y + 20 + 18 * r
        if r in focal_rows:
            out.append(f'<rect class="focal" x="{x + 3}" y="{ry + 3}" width="{w - 6}" height="16" rx="3"/>')
        for cx, cell in zip(xs, row):
            out.append(text(cx + 8, ry + 15, cell, "sub-accent" if cell == "NULL" else "field"))
    return "".join(out), h


@diagram
def joins():
    slug, W, H = "joins", 800, 452
    b = []
    # Join condition between the two source tables, then a tree down to the three results.
    b.append(line(296, 94, 448, 94, "edge-soft"))
    b.append(label_above(372, 94, "c.id = f.cliente_id"))
    b.append(line(400, 152, 400, 172, "tree"))
    b.append(line(140, 172, 660, 172, "tree"))
    for cx in (140, 400, 660):
        b.append(line(cx, 172, cx, 196, "edge", "arrow", slug))
    b.append(text(176, 40, "clientes (c)", "name"))
    b.append(_grid(176, 48, [40, 80], ["id", "nombre"],
                   [["1", "Ana"], ["2", "Beto"], ["3", "Caro"], ["4", "Dani"]])[0])
    b.append(text(456, 40, "facturas (f)", "name"))
    b.append(_grid(456, 48, [40, 80, 56], ["id", "cliente_id", "total"],
                   [["10", "1", "100"], ["11", "1", "50"], ["12", "2", "80"], ["13", "3", "20"]])[0])
    inner = [["Ana", "10", "100"], ["Ana", "11", "50"], ["Beto", "12", "80"], ["Caro", "13", "20"]]
    panels = [
        ("INNER JOIN", "solo las que coinciden", inner, (), "node", "4 filas", "Dani no aparece"),
        ("LEFT JOIN", "toda la izquierda + NULL", inner + [["Dani", "NULL", "NULL"]], (4,), "node",
         "5 filas", "Dani entra con NULL"),
        ("LEFT JOIN + IS NULL", "WHERE f.id IS NULL", [["Dani", "NULL", "NULL"]], (0,), "focal",
         "1 fila", "clientes SIN facturas"),
    ]
    for i, (title, snip, rows, frows, kind, count, why) in enumerate(panels):
        px = 24 + i * 260
        b.append(f'<rect class="mask" x="{px}" y="196" width="232" height="208" rx="6"/>'
                 f'<rect class="{kind}" x="{px}" y="196" width="232" height="208" rx="6"/>')
        b.append(text(px + 16, 218, title, "name-mono"))
        b.append(text(px + 16, 234, snip, "sub-accent" if kind == "focal" else "sub"))
        b.append(_grid(px + 16, 246, [72, 64, 64], ["nombre", "f.id", "total"], rows, frows,
                       "node" if kind == "focal" else "node-soft")[0])
        b.append(text(px + 16, 384, count, "name"))
        b.append(text(px + 216, 384, why, "sub", "end"))
    b.append(text(400, 436, "LEFT JOIN conserva toda la tabla de la izquierda; donde no hay pareja, completa con NULL.",
                  "note", "middle"))
    return dict(
        slug=slug, w=W, h=H, svg=svg_wrap(slug, W, H, "INNER JOIN y LEFT JOIN fila por fila",
            "Clientes (Ana, Beto, Caro, Dani) y facturas (Ana 2, Beto 1, Caro 1). INNER JOIN devuelve 4 filas sin Dani; "
            "LEFT JOIN devuelve 5, con Dani y NULL en las columnas de facturas; LEFT JOIN con WHERE f.id IS NULL deja solo a Dani.",
            "".join(b)),
        eyebrow="Lección 0015 · JOINs", h1="INNER vs LEFT, fila por fila",
        subtitle="Contá filas: INNER descarta a quien no tiene pareja; LEFT lo conserva con NULL; IS NULL lo aísla.",
        caption="Cuántas filas devuelve cada JOIN con las tablas de ejemplo.",
        targets=[("lessons/0015-taller-sql-chinook.html", "after",
                  'Truco: LEFT JOIN + WHERE derecha.id IS NULL = "clientes SIN facturas"</pre>')],
        lesson="lessons/0015-taller-sql-chinook.html")


@diagram
def group_vs_over():
    slug, W, H = "group-vs-over", 800, 388
    src = [["Ana", "100"], ["Ana", "50"], ["Beto", "80"], ["Caro", "20"]]
    b = [path(ortho([(160, 173), (252, 173), (252, 98), (344, 98)]), "edge", "arrow", slug),
         path(ortho([(160, 205), (252, 205), (252, 279), (344, 279)]), "edge-accent", "arrow-accent", slug)]
    b.append(label_above(298, 98, "agrupa"))
    b.append(label_above(298, 279, "ventana", "label-accent"))
    b.append(text(40, 128, "ENTRADA: 4 FILAS", "eyebrow"))
    b.append(_grid(40, 140, [64, 56], ["cliente", "total"], src)[0])
    b.append(text(100, 262, "la misma entrada", "note", "middle"))
    b.append(text(100, 278, "para las dos consultas", "note", "middle"))
    # GROUP BY result
    b.append('<rect class="mask" x="344" y="24" width="416" height="148" rx="6"/>'
             '<rect class="node" x="344" y="24" width="416" height="148" rx="6"/>')
    b.append(text(360, 46, "SUM(total) … GROUP BY cliente", "name-mono"))
    b.append(text(360, 62, "una fila por grupo: el detalle se pierde", "sub"))
    b.append(_grid(360, 76, [72, 96], ["cliente", "sum(total)"],
                   [["Ana", "150"], ["Beto", "80"], ["Caro", "20"]], (), "node-soft")[0])
    b.append(text(560, 110, "3 filas", "name-lg"))
    b.append(text(560, 126, "colapsa", "sub"))
    # Window result
    b.append('<rect class="mask" x="344" y="196" width="416" height="168" rx="6"/>'
             '<rect class="focal" x="344" y="196" width="416" height="168" rx="6"/>')
    b.append(text(360, 218, "SUM(total) OVER (PARTITION BY cliente)", "name-mono"))
    b.append(text(360, 234, "cada fila conserva su detalle y suma el total del grupo", "sub-accent"))
    b.append(_grid(360, 248, [64, 56, 96], ["cliente", "total", "total_cliente"],
                   [["Ana", "100", "150"], ["Ana", "50", "150"], ["Beto", "80", "80"], ["Caro", "20", "20"]])[0])
    b.append(text(600, 290, "4 filas", "name-lg"))
    b.append(text(600, 306, "no colapsa", "sub-accent"))
    return dict(
        slug=slug, w=W, h=H, svg=svg_wrap(slug, W, H, "GROUP BY vs función ventana",
            "Cuatro facturas de entrada. GROUP BY cliente devuelve 3 filas con la suma por cliente; "
            "SUM OVER PARTITION BY cliente devuelve las 4 filas originales con el total del cliente agregado en cada una.",
            "".join(b)),
        eyebrow="Lección 0015 · funciones ventana", h1="GROUP BY colapsa, OVER no",
        subtitle="Las dos calculan la suma por cliente; la diferencia es cuántas filas salen.",
        caption="GROUP BY devuelve una fila por grupo; la ventana conserva todas las filas.",
        targets=[("lessons/0015-taller-sql-chinook.html", "after",
                  "<code>ORDER BY</code> define la secuencia.</p>")],
        lesson="lessons/0015-taller-sql-chinook.html")


@diagram
def graficos():
    slug, W, H = "graficos", 800, 400
    cw, y0, ch = 176, 24, 308
    cards = [
        dict(name="Líneas", fn="plt.plot()", kind="node",
             clues=["evolución", "tendencia", "en el tiempo", "día por día / por mes"],
             ex="Mostrar la evolución de las ventas día por día."),
        dict(name="Barras", fn="plt.bar()", kind="node",
             clues=["comparar", "por categoría", "cuál es mayor / menor", "por producto"],
             ex="Comparar el total vendido por producto."),
        dict(name="Histograma", fn="plt.hist()", kind="focal",
             clues=["cómo se distribuye", "concentración", "forma", "intervalos (bins)"],
             ex="Ver cómo se distribuyen las edades de los alumnos."),
        dict(name="Dispersión", fn="plt.scatter()", kind="node",
             clues=["se asocia / relación", "dos variables", "correlación", "¿más X, más Y?"],
             ex="¿Más horas de estudio se asocian con mejores notas?"),
    ]
    b = []
    for i, c in enumerate(cards):
        x = 24 + i * (cw + 16)
        foc = c["kind"] == "focal"
        b.append(f'<rect class="mask" x="{x}" y="{y0}" width="{cw}" height="{ch}" rx="6"/>'
                 f'<rect class="{c["kind"]}" x="{x}" y="{y0}" width="{cw}" height="{ch}" rx="6"/>')
        b.append(text(x + 16, y0 + 22, c["name"], "name"))
        b.append(text(x + 16, y0 + 38, c["fn"], "sub-accent" if foc else "sub"))
        # Mini chart: plot area x+20..x+160, baseline y0+136, top y0+56.
        ax, base, top, pw = x + 20, y0 + 136, y0 + 56, 140
        b.append(path(f"M{ax},{top} L{ax},{base} L{ax + pw},{base}", "axis"))
        mark = "mark-accent" if foc else "mark"
        if i == 0:
            vals = [0.25, 0.4, 0.33, 0.55, 0.5, 0.7, 0.74, 0.92]
            pts = [(ax + 10 + k * 17, base - v * (base - top)) for k, v in enumerate(vals)]
            b.append('<polyline class="series" points="' + " ".join(f"{px:g},{py:g}" for px, py in pts) + '"/>')
            b.extend(f'<circle class="mark" cx="{px:g}" cy="{py:g}" r="2.2"/>' for px, py in pts)
            b.append(text(ax + pw, base + 11, "tiempo →", "label", "end"))
        elif i == 1:
            for k, v in enumerate([0.6, 0.92, 0.4, 0.75]):
                bx, bh = ax + 12 + k * 32, v * (base - top)
                b.append(f'<rect class="{mark}" x="{bx}" y="{base - bh:g}" width="20" height="{bh:g}"/>')
                b.append(text(bx + 10, base + 11, "ABCD"[k], "label", "middle"))
        elif i == 2:
            for k, v in enumerate([0.12, 0.3, 0.58, 0.9, 1.0, 0.68, 0.36, 0.14]):
                bx, bh = ax + 6 + k * 16, v * (base - top)
                b.append(f'<rect class="{mark}" x="{bx}" y="{base - bh:g}" width="16" height="{bh:g}" '
                         f'style="stroke: var(--dg-paper); stroke-width: 1"/>')
            b.append(text(ax + pw, base + 11, "edad (intervalos) →", "label", "end"))
        else:
            pts = [(0.08, 0.2), (0.15, 0.12), (0.2, 0.3), (0.28, 0.26), (0.35, 0.42), (0.42, 0.34), (0.5, 0.5),
                   (0.56, 0.6), (0.63, 0.52), (0.7, 0.7), (0.78, 0.66), (0.85, 0.84), (0.92, 0.78)]
            for fx, fy in pts:
                b.append(f'<circle class="{mark}" cx="{ax + fx * pw:g}" cy="{base - fy * (base - top):g}" r="2.6"/>')
            b.append(text(ax + pw, base + 11, "horas →", "label", "end"))
            b.append(text(ax + 4, top + 4, "notas", "label"))
        b.append(text(x + 16, y0 + 166, "PALABRAS PISTA", "eyebrow"))
        for k, cl in enumerate(c["clues"]):
            b.append(text(x + 16, y0 + 182 + 14 * k, cl, "sub-accent" if foc and k == 0 else "field"))
        b.append(f'<line class="rule" x1="{x + 16}" y1="{y0 + 244}" x2="{x + cw - 16}" y2="{y0 + 244}"/>')
        b.append(text(x + 16, y0 + 260, "PREGUNTA TIPO", "eyebrow"))
        b.append(f'<foreignObject x="{x + 16}" y="{y0 + 266}" width="{cw - 32}" height="56">'
                 f'<div xmlns="http://www.w3.org/1999/xhtml" class="fo">{esc(c["ex"])}</div></foreignObject>')
    b.append(text(400, 360, "Barras = categorías separadas · histograma = intervalos numéricos pegados.", "note", "middle"))
    b.append(text(400, 380, "Trampa: “dispersión” de UNA variable (qué tan desparramada está) es histograma; dos variables es scatter.",
                  "note", "middle"))
    return dict(
        slug=slug, w=W, h=H, svg=svg_wrap(slug, W, H, "Qué gráfico para qué pregunta",
            "Cuatro tarjetas con un mini gráfico de ejemplo: líneas para evolución en el tiempo, barras para comparar categorías, "
            "histograma (destacado) para ver cómo se distribuye una variable, y dispersión para ver si dos variables se asocian; "
            "cada una con sus palabras pista y una pregunta tipo.", "".join(b)),
        eyebrow="Lección 0011 · Matplotlib", h1="La palabra del enunciado elige el gráfico",
        subtitle="Buscá la palabra pista: evolución → líneas, comparar → barras, distribuye → histograma, se asocia → dispersión.",
        caption="Cada gráfico con su palabra pista y una pregunta tipo del parcial.",
        targets=[("lessons/0011-pandas-y-matplotlib.html", "after",
                  "<td>Relaciones entre dos variables</td></tr>\n</table>\n</div>")],
        lesson="lessons/0011-pandas-y-matplotlib.html")


# --------------------------------------------------------------------------- output

PAGE = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="../assets/diagrams.css">
<style>
  body {{ margin: 0; background: var(--dg-paper); color: var(--dg-ink); font-family: var(--dg-sans); }}
  main {{ max-width: 960px; margin: 0 auto; padding-block: 40px 56px; padding-inline: 16px; }}
  .eyebrow {{ font-family: var(--dg-mono); font-size: 0.72rem; letter-spacing: 0.16em; text-transform: uppercase; color: var(--dg-soft); }}
  h1 {{ font-family: var(--dg-display); font-size: clamp(1.6rem, 3.4vw, 2.3rem); letter-spacing: -0.02em; margin: 6px 0 8px; text-wrap: balance; }}
  .subtitle {{ color: var(--dg-muted); max-width: 64ch; margin: 0 0 28px; }}
  .frame {{ overflow-x: auto; }}
  .frame svg.dg {{ min-width: 560px; }}
  footer {{ margin-top: 32px; padding-top: 12px; border-top: 1px solid var(--dg-rule); font-family: var(--dg-mono); font-size: 0.75rem; color: var(--dg-soft); display: flex; gap: 16px; flex-wrap: wrap; }}
  a {{ color: var(--dg-accent); }}
</style>
</head>
<body>
<main>
{body}
</main>
</body>
</html>
"""


def standalone(d) -> str:
    body = (f'<p class="eyebrow">{esc(d["eyebrow"])}</p><h1>{esc(d["h1"])}</h1>'
            f'<p class="subtitle">{esc(d["subtitle"])}</p><div class="frame">{d["svg"]}</div>'
            f'<footer><a href="../{d["lesson"]}">Ir a la lección</a><a href="index.html">Todos los diagramas</a>'
            f'<a href="../suite/index.html">Suite de estudio</a><span>Análisis de Datos I · UNICABA 2026</span></footer>')
    return PAGE.format(title=esc(d["h1"]), body=body)


def gallery(ds) -> str:
    items = "".join(
        f'<section style="margin-block: 40px;"><p class="eyebrow">{esc(d["eyebrow"])}</p>'
        f'<h2 style="font-family: var(--dg-display); margin: 4px 0 12px;"><a href="{d["slug"]}.html" style="color: inherit; text-decoration: none;">{esc(d["h1"])}</a></h2>'
        f'<div class="frame">{d["svg"]}</div></section>' for d in ds)
    body = ('<p class="eyebrow">Análisis de Datos I · Primer Parcial</p><h1>Diagramas</h1>'
            '<p class="subtitle">Los mismos diagramas que están dentro de las lecciones, reunidos. Siguen el tema claro u oscuro de tu sistema.</p>'
            + items + '<footer><a href="../suite/index.html">Suite de estudio</a><a href="../index.html">Índice de lecciones</a></footer>')
    return PAGE.format(title="Diagramas ADI", body=body)


def figure(d, rel_prefix: str) -> str:
    return (f'<!-- diagram:{d["slug"]} -->\n<figure class="dg-figure"><div class="dg-scroll">{d["svg"]}</div>'
            f'<figcaption>{esc(d["caption"])} <a href="{rel_prefix}diagrams/{d["slug"]}.html">Ver en grande</a></figcaption></figure>\n'
            f'<!-- /diagram:{d["slug"]} -->')


def inject(d):
    for rel, mode, anchor in d["targets"]:
        p = ROOT / rel
        s = p.read_text()
        fig = figure(d, "../")
        start, end = f"<!-- diagram:{d['slug']} -->", f"<!-- /diagram:{d['slug']} -->"
        if start in s:
            s = re.sub(re.escape(start) + r".*?" + re.escape(end), lambda _: fig, s, flags=re.S)
        elif mode == "replace":
            i = s.find(anchor)
            if i < 0:
                raise SystemExit(f"anchor not found in {rel}: {anchor[:40]}")
            j = s.find("</pre>", i) + len("</pre>")
            s = s[:i] + fig + s[j:]
        elif mode == "after":
            i = s.find(anchor)
            if i < 0:
                raise SystemExit(f"anchor not found in {rel}: {anchor[:40]}")
            s = s[:i + len(anchor)] + "\n" + fig + s[i + len(anchor):]
        elif mode == "before":
            i = s.find(anchor)
            if i < 0:
                raise SystemExit(f"anchor not found in {rel}: {anchor[:40]}")
            s = s[:i] + fig + "\n" + s[i:]
        link = '<link rel="stylesheet" href="../assets/diagrams.css">'
        if link not in s:
            s = s.replace('<link rel="stylesheet" href="../assets/course.css">',
                          '<link rel="stylesheet" href="../assets/course.css">\n' + link, 1)
        p.write_text(s)


def main():
    OUT.mkdir(exist_ok=True)
    built = [fn() for fn in DIAGRAMS]
    for d in built:
        (OUT / f"{d['slug']}.html").write_text(standalone(d))
        inject(d)
        print(f"{d['slug']:<12} {d['w']}x{d['h']}  -> {', '.join(t[0] for t in d['targets'])}")
    (OUT / "index.html").write_text(gallery(built))
    print(f"gallery: {len(built)} diagrams")


if __name__ == "__main__":
    main()
