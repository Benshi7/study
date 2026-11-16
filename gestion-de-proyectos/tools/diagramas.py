#!/usr/bin/env python3
"""Build the course diagrams (diagram-design, profile "unicaba-cursada") and embed them.

Usage (from the project root):
  python3 tools/diagramas.py            # write diagramas/*.html and embed into every page with markers
  python3 tools/diagramas.py --check    # exit 1 if any embedded copy is stale

Pages opt in with a marker pair inside a <figure class="diagram">:
  <!--diagram:agil-vs-cascada-->  ...replaced...  <!--/diagram:agil-vs-cascada-->

Colours and fonts live in assets/diagram.css (classes dg-*), so the same SVG works in
lessons (light/dark), slides and standalone pages. Every coordinate is a multiple of 4.
"""
import html
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "diagramas"


def r4(n):
    return int(-(-n // 4) * 4)


class Svg:
    def __init__(self, slug, w, h, title, desc):
        self.slug, self.w, self.h = slug, w, h
        self.title, self.desc = title, desc
        self.parts = []

    def add(self, s):
        self.parts.append(s)

    # -- primitives ---------------------------------------------------------
    def box(self, x, y, w, h, name, subs=(), cls="dg-box", tag=None, name_cls="dg-name"):
        cx = x + w / 2
        self.add(f'<rect class="dg-mask" x="{x}" y="{y}" width="{w}" height="{h}" rx="6"/>')
        self.add(f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="6"/>')
        if tag:
            self.add(f'<text class="dg-tag" x="{x + w - 12}" y="{y + 20}" text-anchor="end">{html.escape(tag)}</text>')
        n = len(subs)
        if n == 0:
            self.add(f'<text class="{name_cls}" x="{cx:g}" y="{y + h / 2 + 5:g}" text-anchor="middle">{html.escape(name)}</text>')
            return
        block = 20 + 18 * n
        top = y + (h - block) / 2
        self.add(f'<text class="{name_cls}" x="{cx:g}" y="{top + 15:g}" text-anchor="middle">{html.escape(name)}</text>')
        for i, s in enumerate(subs):
            self.add(f'<text class="dg-sub" x="{cx:g}" y="{top + 33 + 18 * i:g}" text-anchor="middle">{html.escape(s)}</text>')

    def path(self, d, cls="dg-line", marker="arrow"):
        m = f' marker-end="url(#{self.slug}-{marker})"' if marker else ""
        self.add(f'<path class="{cls}" d="{d}"{m}/>')

    def label(self, cx, line_y, text, cls="dg-lbl"):
        """Label centred on a horizontal connector, 8px above it, on an opaque mask."""
        w = r4(len(text) * 7.2 + 8)
        x = cx - w / 2
        self.add(f'<rect class="dg-mask" x="{x:g}" y="{line_y - 24}" width="{w}" height="16" rx="2"/>')
        self.add(f'<text class="{cls}" x="{cx:g}" y="{line_y - 12}" text-anchor="middle">{html.escape(text)}</text>')

    def text(self, x, y, text, cls="dg-note", anchor="start"):
        self.add(f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}">{html.escape(text)}</text>')

    def legend(self, items):
        """items: list of (kind, text). Horizontal strip in the bottom 60px."""
        y0 = self.h - 56
        self.add(f'<line class="dg-rule" x1="40" y1="{y0}" x2="{self.w - 40}" y2="{y0}"/>')
        self.text(40, y0 + 28, "LEYENDA", "dg-tag")
        x = 128
        for kind, label in items:
            cy = y0 + 24
            if kind == "focal":
                self.add(f'<rect class="dg-focal" x="{x}" y="{cy - 8}" width="20" height="16" rx="4"/>')
                x += 28
            elif kind == "box":
                self.add(f'<rect class="dg-box" x="{x}" y="{cy - 8}" width="20" height="16" rx="4"/>')
                x += 28
            elif kind == "ghost":
                self.add(f'<rect class="dg-ghost" x="{x}" y="{cy - 8}" width="20" height="16" rx="4"/>')
                x += 28
            elif kind == "arrow":
                self.path(f"M{x} {cy} H{x + 24}", "dg-line", "arrow")
                x += 32
            elif kind == "arrow-link":
                self.path(f"M{x} {cy} H{x + 24}", "dg-line-link", "arrow-link")
                x += 32
            elif kind == "arrow-accent":
                self.path(f"M{x} {cy} H{x + 24}", "dg-line-accent", "arrow-accent")
                x += 32
            elif kind == "dot-focal":
                self.add(f'<circle class="dg-dot-focal" cx="{x + 8}" cy="{cy}" r="8"/>')
                x += 24
            self.text(x, cy + 4, label, "dg-note")
            x += r4(len(label) * 6.6) + 32

    def render(self):
        s = self.slug
        head = (
            f'<svg viewBox="0 0 {self.w} {self.h}" xmlns="http://www.w3.org/2000/svg" role="img" '
            f'aria-labelledby="{s}-title {s}-desc">'
            f'<title id="{s}-title">{html.escape(self.title)}</title>'
            f'<desc id="{s}-desc">{html.escape(self.desc)}</desc>'
            "<defs>"
            f'<marker id="{s}-arrow" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon class="dg-ah" points="0 0, 8 3, 0 6"/></marker>'
            f'<marker id="{s}-arrow-accent" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon class="dg-ah-accent" points="0 0, 8 3, 0 6"/></marker>'
            f'<marker id="{s}-arrow-link" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon class="dg-ah-link" points="0 0, 8 3, 0 6"/></marker>'
            "</defs>"
            f'<rect class="dg-bg" width="100%" height="100%"/>'
        )
        return head + "\n".join(self.parts) + "</svg>"


# ---------------------------------------------------------------------------
# 1. Agil vs cascada: same time axis, when does the client see value?
# ---------------------------------------------------------------------------
def agil_vs_cascada():
    d = Svg("agil-vs-cascada", 960, 540,
            "Ágil versus cascada: cuándo llega el primer valor",
            "Dos filas sobre el mismo eje de tiempo: en cascada hay cinco fases secuenciales y el cliente recibe valor recién en la entrega final; en ágil hay cinco iteraciones y el primer valor llega al terminar la primera.")
    d.text(40, 48, "Cascada · planificar todo al inicio, entregar al final", "dg-row")
    xs = [(40, 128, "Requisitos"), (176, 128, "Diseño"), (312, 288, "Desarrollo"), (608, 160, "Pruebas")]
    for x, w, name in xs:
        d.box(x, 64, w, 64, name)
    d.box(776, 64, 136, 64, "Entrega", cls="dg-focal")
    d.text(844, 156, "valor recién acá", "dg-note", "middle")

    d.text(40, 244, "Ágil · planificar períodos cortos, entregar en cada iteración", "dg-row")
    # feedback arrows first so boxes sit above them
    for i in range(4):
        x1 = 40 + 152 + i * 180
        d.path(f"M{x1} 292 H{x1 + 28}", "dg-line-link", "arrow-link")
    for i in range(5):
        x = 40 + i * 180
        d.box(x, 260, 152, 64, f"Iteración {i + 1}", ["entrega valor"])
        cx = x + 76
        d.add(f'<circle class="{"dg-dot-focal" if i == 0 else "dg-dot"}" cx="{cx}" cy="352" r="8"/>')
    d.text(116, 384, "primer valor", "dg-note-accent", "middle")

    d.path("M40 428 H920", "dg-line", "arrow")
    d.text(40, 452, "inicio", "dg-lbl")
    d.text(480, 452, "misma duración total", "dg-note", "middle")
    d.text(912, 452, "fin", "dg-lbl", "end")
    d.legend([("dot-focal", "incremento con valor para el cliente"), ("arrow-link", "feedback y ajuste")])
    return d


# ---------------------------------------------------------------------------
# 2. Cynefin as the catedra shows it: domain -> method
# ---------------------------------------------------------------------------
def cynefin():
    d = Svg("cynefin", 960, 540,
            "Cynefin: qué metodología corresponde a cada dominio",
            "Cuatro dominios ordenados por incertidumbre creciente: simple usa buenas prácticas, complicado usa cascada, complejo y caótico usan ágil; el dominio desordenado exige accionar para llegar a alguno de los cuatro.")
    d.text(40, 40, "INCERTIDUMBRE CRECIENTE", "dg-tag")
    d.path("M40 56 H920", "dg-line", "arrow")
    cols = [(40, "Simple", ["Situaciones claras", "y conocidas"], "1", "dg-box"),
            (268, "Complicado", ["Requiere experiencia", "en la materia"], "2", "dg-focal"),
            (496, "Complejo", ["Sin experiencia en el", "tema o la tecnología"], "3", "dg-box"),
            (724, "Caótico", ["Sin experiencia en el", "tema ni la tecnología"], "4", "dg-box")]
    # connectors first (boxes are painted over them)
    for x in (138, 366, 594, 822):
        d.path(f"M{x} 184 V240")
    for x, name, subs, tag, cls in cols:
        d.box(x, 88, 196, 96, name, subs, cls, tag)
    d.box(40, 240, 196, 64, "Buenas prácticas")
    d.box(268, 240, 196, 64, "Cascada", cls="dg-focal")
    d.box(496, 240, 424, 64, "Ágil", cls="dg-viol")
    # dominio 5
    d.add('<rect class="dg-mask" x="40" y="368" width="880" height="80" rx="6"/>')
    d.add('<rect class="dg-ghost" x="40" y="368" width="880" height="80" rx="6"/>')
    d.add('<text class="dg-tag" x="908" y="388" text-anchor="end">5</text>')
    d.add('<text class="dg-name" x="480" y="404" text-anchor="middle">Desordenado</text>')
    d.add('<text class="dg-sub" x="480" y="428" text-anchor="middle">No aplica a ninguno de los anteriores: accionar para llegar a los 4 anteriores</text>')
    d.legend([("focal", "único dominio en cascada"), ("arrow", "se gestiona con"), ("ghost", "dominio sin clasificar")])
    return d


# ---------------------------------------------------------------------------
# 3. Scrum: who owns which artefact, and the two gates (DoR, DoD)
# ---------------------------------------------------------------------------
def scrum_artefactos():
    d = Svg("scrum-artefactos", 960, 560,
            "Scrum: roles, artefactos y los dos controles de calidad",
            "El Equipo Scrum reúne al Product Owner, al equipo de desarrollo y al Scrum Master. El Product Owner ordena el Product Backlog; el equipo lo lleva al Sprint Backlog si cumple la DoR y entrega un Incremento con las historias que cumplen la DoD.")
    d.add('<rect class="dg-zone" x="28" y="24" width="904" height="152" rx="8"/>')
    d.text(44, 48, "EQUIPO SCRUM", "dg-tag")
    # connectors first
    d.path("M160 160 V312")
    d.text(168, 244, "ordena", "dg-lbl")
    d.path("M480 160 V312")
    d.text(472, 244, "se compromete", "dg-lbl", "end")
    d.path("M540 160 V260 Q540 268 548 268 H792 Q800 268 800 276 V312")
    d.label(672, 268, "entrega")
    d.path("M680 112 H600")
    d.label(640, 112, "facilita")
    d.path("M280 360 H360")
    d.label(320, 360, "DoR")
    d.path("M600 360 H680", "dg-line-accent", "arrow-accent")
    d.label(640, 360, "DoD", "dg-lbl-accent")
    # roles
    d.box(40, 64, 240, 96, "Product Owner", ["Una sola persona", "Dueño del backlog"])
    d.box(360, 64, 240, 96, "Equipo de desarrollo", ["3 a 9 personas", "autoorganizado"])
    d.box(680, 64, 240, 96, "Scrum Master", ["Facilita Scrum", "No es un Project Manager"])
    # artefacts
    d.box(40, 312, 240, 96, "Product Backlog", ["Lista única ordenada", "por valor de negocio"], "dg-store")
    d.box(360, 312, 240, 96, "Sprint Backlog", ["Tareas del Sprint,", "acordadas con el PO"], "dg-store")
    d.box(680, 312, 240, 96, "Incremento", ["Historias que", "alcanzaron la DoD"], "dg-focal")
    d.text(40, 448, "DoR · Definition of Ready: la historia está lista para entrar al Sprint.", "dg-note")
    d.text(40, 472, "DoD · Definition of Done: la historia cumple el checklist y cuenta como terminada.", "dg-note")
    d.legend([("arrow", "relación"), ("arrow-accent", "control de calidad (DoD)"), ("focal", "lo que se entrega")])
    return d


# ---------------------------------------------------------------------------
# 4. The TP as a chain with the ties that make it one story
# ---------------------------------------------------------------------------
def tp_cadena():
    d = Svg("tp-cadena", 1040, 512,
            "Cómo se atan las ocho secciones técnicas del TP",
            "Las secciones 3 a 10 forman una cadena: Canvas, Design Thinking, Charter, Gantt, Stakeholders, Comunicación, Riesgos y Presupuesto. Además del orden, el Gantt aporta el camino crítico a Riesgos y las semanas al Presupuesto, y la matriz de riesgos aporta el EMV que define la reserva de contingencia.")
    cx = [130, 390, 650, 910]
    xs = [40, 300, 560, 820]
    row1, row2 = 40, 312
    # connectors first
    for i in range(3):
        d.path(f"M{xs[i] + 180} 88 H{xs[i + 1]}")
        d.path(f"M{xs[i] + 180} 360 H{xs[i + 1]}", "dg-line-accent" if i == 2 else "dg-line",
               "arrow-accent" if i == 2 else "arrow")
    d.label(260, 88, "hipótesis")
    d.label(520, 88, "problema")
    d.label(780, 88, "hitos")
    d.label(260, 360, "atención")
    d.label(520, 360, "R04 · R06")
    d.label(780, 360, "EMV", "dg-lbl-accent")
    # Gantt -> Stakeholders (chain), Gantt -> Riesgos and Gantt -> Presupuesto (data ties)
    d.path("M852 136 V192 Q852 200 844 200 H138 Q130 200 130 208 V312")
    d.label(500, 200, "actores")
    d.path("M900 136 V232 Q900 240 892 240 H658 Q650 240 650 248 V312", "dg-line-link", "arrow-link")
    d.label(780, 240, "camino crítico", "dg-lbl-link")
    d.path("M948 136 V312", "dg-line-link", "arrow-link")
    d.add('<rect class="dg-mask" x="860" y="264" width="80" height="16" rx="2"/>')
    d.add('<text class="dg-lbl-link" x="900" y="276" text-anchor="middle">semanas</text>')
    nodes = [
        (0, row1, "Canvas", ["¿Qué negocio y", "para quién?"], "03", "dg-box"),
        (1, row1, "Design Thinking", ["¿El problema", "es real?"], "04", "dg-box"),
        (2, row1, "Charter", ["¿Qué hacemos y", "con qué límites?"], "05", "dg-box"),
        (3, row1, "Gantt", ["¿Qué tareas, en qué", "orden y cuánto duran?"], "06", "dg-box"),
        (0, row2, "Stakeholders", ["¿A quién afecta y", "con cuánto poder?"], "07", "dg-box"),
        (1, row2, "Comunicación", ["¿Qué, a quién,", "cuándo y por dónde?"], "08", "dg-box"),
        (2, row2, "Riesgos", ["¿Qué puede pasar", "y qué hacemos?"], "09", "dg-box"),
        (3, row2, "Presupuesto", ["¿Cuánto cuesta?"], "10", "dg-focal"),
    ]
    for c, y, name, subs, tag, cls in nodes:
        d.box(xs[c], y, 180, 96, name, subs, cls, tag)
    d.legend([("arrow", "el relato: lo que una sección le pasa a la siguiente"),
              ("arrow-link", "dependencia de dato"), ("arrow-accent", "la que más preguntan")])
    return d


# ---------------------------------------------------------------------------
# 5. The Sprint and its four events (Scrum Guide 2020 timeboxes for a 1-month Sprint)
# ---------------------------------------------------------------------------
def sprint_ciclo():
    # Catedra version (Scrum parte 2, p7-p19): 2 weeks to 2 months, DoR gate, Sprint 0 and refinement outside.
    d = Svg("sprint-ciclo", 960, 560,
            "El Sprint y sus ceremonias según la cátedra",
            "Un Sprint es un time box fijo de 2 semanas a 2 meses con cuatro ceremonias y un objetivo: Sprint Planning, trabajo con Daily Scrum, Sprint Review y Sprint Retrospective. Las historias del Product Backlog entran si cumplen la DoR, el Incremento cumple la DoD y se muestra en la Review, y la retrospectiva deja un plan de acción para el Sprint siguiente. Sprint 0 y refinamiento quedan fuera de los cuatro eventos.")
    d.add('<rect class="dg-zone" x="28" y="24" width="904" height="200" rx="8"/>')
    d.text(44, 48, "SPRINT · TIME BOX FIJO DE 2 SEMANAS A 2 MESES · 4 CEREMONIAS, 1 OBJETIVO", "dg-tag")
    # connectors first
    for x in (236, 464, 692):
        d.path(f"M{x} 128 H{x + 32}")
    d.path("M138 272 V176")
    d.text(146, 252, "entra si cumple la DoR", "dg-lbl")
    d.path("M366 272 V176")
    d.text(374, 252, "guía el trabajo", "dg-lbl")
    d.path("M594 176 V272")
    d.text(602, 252, "se muestra", "dg-lbl")
    d.path("M822 176 V272")
    d.text(830, 252, "deja", "dg-lbl")
    # events
    d.box(40, 80, 196, 96, "Sprint Planning", ["1ª tarea: PO explica HU", "objetivo + tareas"], "dg-box")
    d.box(268, 80, 196, 96, "Trabajo + Daily", ["15 min · 3 preguntas", "impedimentos"], "dg-box")
    d.box(496, 80, 196, 96, "Sprint Review", ["PO + demo", "a stakeholders"], "dg-box")
    d.box(724, 80, 196, 96, "Retrospectiva", ["última tarea", "cómo mejorar"], "dg-box")
    # artefacts
    d.box(40, 272, 196, 88, "Product Backlog", ["ordenado por el PO"], "dg-store")
    d.box(268, 272, 196, 88, "Sprint Backlog", ["con el Sprint Goal"], "dg-store")
    d.box(496, 272, 196, 88, "Incremento", ["cumple la DoD"], "dg-focal")
    d.box(724, 272, 196, 88, "Plan de acción", ["fecha y responsable"], "dg-store")
    # outside the four ceremonies
    d.box(40, 392, 428, 72, "Sprint 0 · puesta a punto", ["no está en la Guía · máximo 2 Sprints"], "dg-ghost")
    d.box(492, 392, 428, 72, "Refinamiento · lo modera el PO", ["Scrum lo ve como parte de la Planning"], "dg-ghost")
    d.legend([("box", "ceremonia"), ("focal", "lo que se entrega"), ("ghost", "fuera de las 4 ceremonias")])
    return d


# ---------------------------------------------------------------------------
# 5b. The Sprint as a map: ceremonies on time, artefacts below, refinement as a
#     continuous band, where slicing and splitting happen, and the time boxes.
# ---------------------------------------------------------------------------
def sprint_mapa():
    d = Svg("sprint-mapa", 1096, 620,
            "El Sprint completo: ceremonias, artefactos, refinamiento y tiempos",
            "Dentro de un Sprint de 2 semanas a 2 meses van la Planning, el trabajo con Daily de 15 minutos, la Review y la Retrospectiva. La Planning toma del Product Backlog las historias que cumplen la DoR y en su paso 4 las parte en tareas (splitting) para el Sprint Backlog; el trabajo produce el Incremento que cumple la DoD y se muestra en la Review; la Retro deja un plan de acción. Debajo, el refinamiento corre durante todo el Sprint, lo modera el PO y parte épicas en historias (slicing) que el próximo Sprint toma en su Planning.")
    d.add('<rect class="dg-zone" x="28" y="24" width="856" height="456" rx="8"/>')
    d.text(44, 48, "UN SPRINT · TIME BOX FIJO DE 2 SEMANAS A 2 MESES · 4 CEREMONIAS, 1 OBJETIVO", "dg-tag")
    # connectors first
    d.path("M128 272 V224")
    d.text(136, 252, "DoR", "dg-lbl")
    d.path("M232 224 V240 Q232 248 240 248 H360 Q368 248 368 256 V272")
    d.path("M456 316 H568", "dg-line-accent", "arrow-accent")
    d.label(512, 316, "DoD", "dg-lbl-accent")
    d.path("M640 272 V224")
    d.text(648, 252, "se muestra", "dg-lbl")
    d.path("M800 224 V272")
    d.text(808, 252, "deja", "dg-lbl")
    d.path("M128 400 V360")
    d.text(136, 384, "slicing", "dg-lbl")
    d.path("M872 316 H912")
    d.path("M872 432 H912")
    # ceremonies, in time order
    d.add('<rect class="dg-mask" x="40" y="72" width="224" height="152" rx="6"/>')
    d.add('<rect class="dg-box" x="40" y="72" width="224" height="152" rx="6"/>')
    d.text(56, 100, "Sprint Planning", "dg-name")
    for i, step in enumerate(["1 · el PO explica las HU", "2 · cuánto entra", "3 · objetivo del Sprint"]):
        d.text(56, 128 + 20 * i, step, "dg-sub")
    d.add('<rect class="dg-focal" x="52" y="180" width="200" height="32" rx="4"/>')
    d.text(64, 200, "4 · splitting: HU → tareas", "dg-note-accent")
    d.box(280, 72, 272, 152, "Trabajo + Daily", ["Daily: 15 min, cada día", "tareas de hasta 8 h"])
    for i in range(10):
        d.add(f'<circle class="dg-dot" cx="{308 + 24 * i}" cy="204" r="4"/>')
    d.box(568, 72, 144, 152, "Sprint Review", ["demo a", "stakeholders"])
    d.box(728, 72, 144, 152, "Retrospectiva", ["última tarea:", "cómo mejorar"])
    # artefacts
    d.box(40, 272, 176, 88, "Product Backlog", ["lo ordena el PO"], "dg-store")
    d.box(280, 272, 176, 88, "Sprint Backlog", ["objetivo + tareas"], "dg-store")
    d.box(568, 272, 144, 88, "Incremento", ["cumple la DoD"], "dg-focal")
    d.box(728, 272, 144, 88, "Plan de acción", ["fecha y responsable"], "dg-store")
    # refinement: a band under the whole Sprint
    d.add('<rect class="dg-mask" x="40" y="400" width="832" height="64" rx="6"/>')
    d.add('<rect class="dg-ghost" x="40" y="400" width="832" height="64" rx="6"/>')
    d.text(56, 428, "Refinamiento · continuo, durante todo el Sprint", "dg-name")
    d.text(56, 448, "lo modera el PO · slicing: épicas → historias chicas que cumplan la DoR, para el próximo Sprint", "dg-sub")
    # next Sprint
    d.box(912, 272, 144, 192, "Próximo Sprint", ["su Planning toma", "las HU listas y", "el plan de acción"], "dg-ghost")
    d.text(40, 508, "Tiempos de la cátedra: Sprint de 2 semanas a 2 meses · Daily de 15 min · tareas de hasta 8 h · Sprint 0 de hasta 2 Sprints, antes del primero.", "dg-note")
    d.text(40, 532, "Guía Scrum 2020 (no la da la cátedra), para un Sprint de 1 mes: Planning hasta 8 h · Review hasta 4 h · Retro hasta 3 h.", "dg-note")
    d.text(40, 556, "El refinamiento no es una de las 4 ceremonias: la cátedra dice que «Scrum lo ve como parte de la Planning».", "dg-note")
    d.legend([("box", "ceremonia"), ("ghost", "fuera de las 4 ceremonias"), ("focal", "splitting e Incremento"),
              ("arrow-accent", "control DoD")])
    return d


# ---------------------------------------------------------------------------
# 7. Slicing vs splitting (Scrum parte 2, p13-p17)
# ---------------------------------------------------------------------------
def hu_slicing():
    d = Svg("hu-slicing", 960, 540,
            "Épica, historia de usuario y tarea: slicing y splitting",
            "Una épica se parte en historias de usuario con slicing durante el refinamiento (siete técnicas) y cada historia se parte en tareas con splitting durante la Sprint Planning (tres criterios).")
    d.path("M216 112 H376")
    d.path("M580 112 H740")
    d.box(40, 64, 176, 96, "Épica", ["demasiado grande", "para un Sprint"], "dg-ghost")
    d.box(380, 64, 200, 96, "Historia de usuario", ["Como… quiero…", "para…"], "dg-focal")
    d.box(744, 64, 176, 96, "Tarea", ["trabajo técnico", "de hasta 8 horas"])
    d.text(304, 188, "SLICING", "dg-tag", "middle")
    d.text(304, 208, "en el refinamiento", "dg-lbl", "middle")
    d.text(656, 188, "SPLITTING", "dg-tag", "middle")
    d.text(656, 208, "en la Sprint Planning", "dg-lbl", "middle")
    d.add('<rect class="dg-zone" x="40" y="236" width="424" height="236" rx="8"/>')
    d.text(56, 260, "SLICING · PARTIR HISTORIAS · 7 TÉCNICAS", "dg-tag")
    for i, line in enumerate(["Roles: comprador / vendedor",
                              "Pasos del flujo: buscar, carrito, envío, pagar",
                              "Principal / alternativo: tarjeta vencida",
                              "Regla de negocio: envío gratis desde $30.000",
                              "Datos de entrada: filtros de km y marca",
                              "Datos de salida: email o pantalla",
                              "Operaciones: publicar, modificar, dar de baja"]):
        d.text(56, 292 + i * 24, line)
    d.add('<rect class="dg-zone" x="496" y="236" width="424" height="236" rx="8"/>')
    d.text(512, 260, "SPLITTING · PARTIR EN TAREAS · 3 CRITERIOS", "dg-tag")
    for i, line in enumerate(["Tipo de actividad: diseño, desarrollo, pruebas",
                              "Componente técnico: front-end, back-end",
                              "Tecnología o herramienta: Postman, Selenium"]):
        d.text(512, 292 + i * 24, line)
    d.text(512, 388, "Ejemplo de la cátedra:", "dg-note-accent")
    d.text(512, 412, "«Como comprador, quiero recibir un email", "dg-note")
    d.text(512, 436, "con la confirmación de la compra…»", "dg-note")
    d.legend([("ghost", "demasiado grande"), ("focal", "unidad de valor para el usuario"), ("box", "unidad de trabajo")])
    return d


# ---------------------------------------------------------------------------
# 8. Retrospective: Starfish (Scrum parte 3, p11)
# ---------------------------------------------------------------------------
def retro_starfish():
    d = Svg("retro-starfish", 960, 560,
            "Retrospectiva Starfish: cinco brazos",
            "La estrella de mar tiene cinco brazos: comenzar a hacer, seguir haciendo, dejar de hacer, hacer más y hacer menos. Cada brazo clasifica una práctica según el valor que da hoy.")
    cx, cy = 480, 272
    arms = [(360, 24, "Seguir haciendo", ["da valor tal como está", "ej.: actividades del TP"]),
            (40, 168, "Comenzar a hacer", ["creemos que dará valor", "ej.: ejemplos prácticos"]),
            (680, 168, "Dejar de hacer", ["ya no aporta valor", "ej.: clases sin recreo"]),
            (136, 368, "Hacer más", ["da más valor del esperado", "ej.: repasos al inicio"]),
            (584, 368, "Hacer menos", ["antes valía, ahora poco", "ej.: menos evaluaciones"])]
    for x, y, *_ in arms:
        d.path(f"M{cx} {cy} L{x + 120} {y + 44}", "dg-line", None)
    d.add(f'<circle class="dg-mask" cx="{cx}" cy="{cy}" r="64"/>')
    d.add(f'<circle class="dg-focal" cx="{cx}" cy="{cy}" r="64"/>')
    d.text(cx, cy - 2, "Starfish", "dg-name", "middle")
    d.text(cx, cy + 18, "¿qué hacemos con", "dg-sub", "middle")
    d.text(cx, cy + 34, "cada práctica?", "dg-sub", "middle")
    for x, y, name, subs in arms:
        d.box(x, y, 240, 88, name, subs)
    d.legend([("box", "brazo: decisión sobre una práctica"), ("focal", "el equipo, en la retro")])
    return d


# ---------------------------------------------------------------------------
# 9. Retrospective: Sailing Boat, mapped to FODA (Scrum parte 3, p12; Clase 5)
# ---------------------------------------------------------------------------
def retro_velero():
    d = Svg("retro-velero", 960, 580,
            "Retrospectiva Sailing Boat y su equivalencia con FODA",
            "El barco es el equipo y la isla el objetivo. El viento son las fortalezas que impulsan, el ancla las debilidades que frenan, el sol las oportunidades y las rocas las amenazas o riesgos: son los cuatro cuadrantes del FODA.")
    # connectors first
    d.path("M380 260 H244", "dg-line-link", "arrow-link")
    d.label(312, 260, "rumbo")
    d.path("M680 84 L580 212", "dg-line-accent", "arrow-accent")
    d.path("M280 84 L380 212", "dg-line-accent", "arrow-accent")
    d.path("M440 304 L360 392", "dg-line", "arrow")
    d.path("M520 304 L600 392", "dg-line", "arrow")
    d.box(40, 40, 240, 88, "Sol · oportunidades", ["FODA: O (externo +)", "ej.: tenemos a los profes"], tag="O")
    d.box(680, 40, 240, 88, "Viento · fortalezas", ["FODA: F (interno +)", "ej.: buena química"], tag="F")
    d.box(40, 216, 200, 88, "Isla · objetivo", ["ej.: promocionar"], "dg-store")
    d.box(380, 216, 200, 88, "Barco · el equipo", ["nosotros"], "dg-focal")
    d.box(200, 396, 240, 88, "Ancla · debilidades", ["FODA: D (interno −)", "ej.: temas que no sabemos"], tag="D")
    d.box(520, 396, 240, 88, "Rocas · amenazas", ["FODA: A (externo −)", "ej.: problemas los miércoles"], tag="A")
    d.legend([("arrow-accent", "impulsa o ilumina"), ("arrow", "frena o pone en riesgo"), ("arrow-link", "hacia el objetivo")])
    return d


# ---------------------------------------------------------------------------
# 10. Push vs pull (cronograma clase 12: "Kanban, pull y push, cuellos de botella")
# ---------------------------------------------------------------------------
def push_pull():
    d = Svg("push-pull", 960, 460,
            "Push contra pull: dónde se esconde el cuello de botella",
            "En push cada etapa empuja trabajo a la siguiente sin mirar su capacidad y la cola se acumula frente a la etapa lenta. En pull cada etapa toma trabajo solo cuando tiene lugar bajo su límite de WIP, así que la etapa llena queda a la vista y frena a las anteriores.")
    d.text(40, 44, "Push · se empuja trabajo sin mirar la capacidad", "dg-row")
    for x in (280, 600):
        d.path(f"M{x} 96 H{x + 76}")
    d.box(40, 64, 240, 64, "Análisis", ["termina y empuja"])
    d.box(360, 64, 240, 64, "Desarrollo", ["termina y empuja"])
    d.box(680, 64, 240, 64, "Pruebas", ["cola: 9 ítems esperando"], "dg-focal")
    d.text(800, 156, "la cola crece y nadie la ve a tiempo", "dg-note-accent", "middle")

    d.text(40, 220, "Pull · cada etapa toma trabajo cuando tiene lugar (límite de WIP)", "dg-row")
    for x in (280, 600):
        d.path(f"M{x} 260 H{x + 76}")
        d.path(f"M{x + 76} 288 H{x + 4}", "dg-line-link", "arrow-link")
    d.box(40, 240, 240, 64, "Análisis", ["WIP 2 de 3 · toma si hay lugar"])
    d.box(360, 240, 240, 64, "Desarrollo", ["WIP 3 de 3 · espera la señal"])
    d.box(680, 240, 240, 64, "Pruebas", ["WIP 2 de 2 · llena, frena"], "dg-focal")
    d.text(480, 340, "La columna llena se ve en el tablero: ahí está el cuello de botella para atacar.", "dg-note", "middle")
    d.legend([("arrow", "trabajo"), ("arrow-link", "señal de capacidad (pull)"), ("focal", "cuello de botella")])
    return d


# ---------------------------------------------------------------------------
# 6. Kanban board: WIP limits, pull and where the bottleneck shows
# ---------------------------------------------------------------------------
def kanban_flujo():
    d = Svg("kanban-flujo", 960, 512,
            "Tablero Kanban: límites de WIP, pull y cuello de botella",
            "Cuatro columnas: Por hacer con cuatro tarjetas, En curso con tres de un límite de tres, Revisión con dos de un límite de dos y Hecho con tres. La columna Revisión llena es el cuello de botella: nada nuevo entra hasta que salga una tarjeta, y el trabajo se tira (pull) cuando hay capacidad.")
    cols = [(40, "Por hacer", "sin límite", "dg-ghost", ["Historia 7", "Historia 8", "Historia 9", "Historia 10"]),
            (260, "En curso", "WIP 3 / 3", "dg-box", ["Historia 4", "Historia 5", "Historia 6"]),
            (480, "Revisión", "WIP 2 / 2", "dg-focal", ["Historia 2", "Historia 3"]),
            (700, "Hecho", "terminadas", "dg-store", ["Historia 1"])]
    d.path("M800 348 H140", "dg-line", "arrow")
    d.label(470, 348, "pull: se toma trabajo solo cuando hay capacidad")
    for x, name, wip, cls, cards in cols:
        d.add(f'<rect class="dg-zone" x="{x}" y="24" width="204" height="288" rx="8"/>')
        d.text(x + 12, 48, name.upper(), "dg-tag")
        d.text(x + 192, 48, wip, "dg-tag", "end")
        for i, c in enumerate(cards):
            d.box(x + 20, 72 + i * 56, 164, 44, c, cls=cls)
    d.text(40, 396, "Cuello de botella: Revisión está llena, así que En curso no puede entregar y Por hacer no avanza.", "dg-note")
    d.text(40, 420, "El límite de WIP vuelve visible el problema el mismo día en que aparece.", "dg-note")
    d.legend([("focal", "cuello de botella"), ("arrow", "dirección del pull")])
    return d


# ---------------------------------------------------------------------------
# 11. The pitch in one picture: sources -> common layer -> accesses (TP 3 and 5.6)
# ---------------------------------------------------------------------------
def capa_comun():
    d = Svg("capa-comun", 1040, 480,
            "Una capa geográfica común entre las fuentes y los accesos",
            "Las áreas del GCBA, USIG e Innovación y los vecinos alimentan una única capa geográfica común, con control de calidad; esa capa se consulta desde el Mapa Web, Boti y BAX.")
    d.text(160, 32, "FUENTES", "dg-tag", "middle")
    d.text(520, 32, "PLATAFORMA", "dg-tag", "middle")
    d.text(880, 32, "ACCESOS", "dg-tag", "middle")
    # connectors first; three attach points per edge of the central box (170, 212, 254)
    d.path("M280 92 H332 Q340 92 340 100 V162 Q340 170 348 170 H400")
    d.path("M280 212 H400")
    d.path("M280 332 H332 Q340 332 340 324 V262 Q340 254 348 254 H400", "dg-line-link", "arrow-link")
    d.path("M640 170 H692 Q700 170 700 162 V100 Q700 92 708 92 H760", "dg-line-accent", "arrow-accent")
    d.path("M640 212 H760", "dg-line-accent", "arrow-accent")
    d.path("M640 254 H692 Q700 254 700 262 V324 Q700 332 708 332 H760", "dg-line-accent", "arrow-accent")
    d.box(40, 48, 240, 88, "Áreas del GCBA", ["Transporte, Cultura,", "Espacio Público"])
    d.box(40, 168, 240, 88, "USIG e Innovación", ["infraestructura", "y estándares"])
    d.box(40, 288, 240, 88, "Vecinos", ["reportan y validan"], cls="dg-viol")
    d.box(400, 128, 240, 168, "Capa geográfica común", ["un solo dato por lugar,", "con control de calidad"], cls="dg-focal")
    d.box(760, 48, 240, 88, "Mapa Web / Mobile", ["consultar, reportar, seguir"])
    d.box(760, 168, 240, 88, "Boti", ["WhatsApp"])
    d.box(760, 288, 240, 88, "BAX", ["canal digital de la Ciudad"])
    d.legend([("focal", "lo que construye el proyecto"), ("arrow", "dato oficial"),
              ("arrow-link", "aporte ciudadano"), ("arrow-accent", "la misma capa, en cada canal")])
    return d


# ---------------------------------------------------------------------------
# 12. The numbers chain: Gantt -> weekly cost -> risk impact -> reserve -> baseline
# ---------------------------------------------------------------------------
def cadena_cifras():
    d = Svg("cadena-cifras", 1080, 320,
            "La cadena de cifras: del Gantt a la línea base de costos",
            "El camino crítico de 126 días hábiles da 25,2 semanas; el costo de recursos humanos dividido por esas semanas da USD 4.833 por semana; con eso se valora el impacto de cada riesgo, la suma de los valores esperados residuales da la reserva de USD 41.206 y, sumada al base de USD 200.633, la línea base de USD 241.839.")
    d.text(40, 44, "Si el jurado tira de un hilo, sale toda la cadena", "dg-row")
    xs = [40, 248, 456, 664, 872]
    for i in range(4):
        last = i == 3
        d.path(f"M{xs[i] + 168} 144 H{xs[i + 1]}", "dg-line-accent" if last else "dg-line",
               "arrow-accent" if last else "arrow")
    nodes = [
        ("Gantt", ["126 días hábiles", "= 25,2 semanas"], "06", "dg-box"),
        ("Costo semanal", ["RRHH 121.790 ÷ 25,2", "= USD 4.833"], "10", "dg-box"),
        ("Impacto", ["semanas × 4.833", "+ gastos afectados"], "09", "dg-box"),
        ("Reserva", ["EMV = impacto × prob.", "Σ residual: 41.206"], "09", "dg-box"),
        ("Línea base", ["200.633 + 41.206", "= USD 241.839"], "10", "dg-focal"),
    ]
    for x, (name, subs, tag, cls) in zip(xs, nodes):
        d.box(x, 88, 168, 112, name, subs, cls, tag)
    d.legend([("box", "sección del TP (número arriba a la derecha)"), ("focal", "la cifra que se aprueba")])
    return d


DIAGRAMS = {
    "capa-comun": (capa_comun, "Una capa geográfica común", "Fuentes, plataforma y accesos del proyecto."),
    "cadena-cifras": (cadena_cifras, "La cadena de cifras", "Del camino crítico a la línea base de costos."),
    "sprint-ciclo": (sprint_ciclo, "El Sprint y sus eventos", "Planning, Daily, Review y Retrospectiva dentro de un Sprint."),
    "sprint-mapa": (sprint_mapa, "El Sprint completo", "Ceremonias, artefactos, refinamiento continuo, slicing, splitting y tiempos."),
    "kanban-flujo": (kanban_flujo, "Tablero Kanban", "WIP, pull y cuello de botella."),
    "hu-slicing": (hu_slicing, "Slicing y splitting", "De la épica a la historia de usuario y de la historia a las tareas."),
    "retro-starfish": (retro_starfish, "Retrospectiva Starfish", "Cinco brazos para decidir qué hacer con cada práctica."),
    "retro-velero": (retro_velero, "Retrospectiva Sailing Boat", "Velero, isla, viento, ancla, sol y rocas: el FODA del equipo."),
    "push-pull": (push_pull, "Push contra pull", "Dónde se esconde y dónde se ve el cuello de botella."),
    "agil-vs-cascada": (agil_vs_cascada, "Ágil versus cascada", "Un mismo proyecto, dos formas de entregar valor."),
    "cynefin": (cynefin, "Cynefin y metodologías", "Del dominio del problema a la metodología."),
    "scrum-artefactos": (scrum_artefactos, "Scrum: roles y artefactos", "Quién es dueño de qué y qué controles hay."),
    "tp-cadena": (tp_cadena, "La cadena del TP", "Cómo se atan las secciones 3 a 10."),
}

# Gallery (diagramas/index.html): groups in study order; the first slug of a group can be featured wide.
GALLERY = [
    ("agil", "Ruta ágil · para el parcial", ["sprint-mapa", "agil-vs-cascada", "cynefin", "scrum-artefactos", "sprint-ciclo",
                                            "hu-slicing", "retro-starfish", "retro-velero", "push-pull", "kanban-flujo"]),
    ("cascada", "Ruta cascada · TP y defensa", ["tp-cadena", "capa-comun", "cadena-cifras"]),
]
FEATURED = {"sprint-mapa"}

GALLERY_PAGE = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Diagramas</title>
<script src="../assets/theme.js"></script>
<script src="../assets/suite-nav.js" defer></script>
<link rel="stylesheet" href="../assets/course.css">
<link rel="stylesheet" href="../assets/diagram.css">
<link rel="stylesheet" href="../assets/suite.css">
</head>
<body>
<main class="wide">
<header class="hub-hero">
  <p class="kicker">Diagramas</p>
  <h1>Todos los diagramas, en orden de estudio</h1>
  <p>Un clic en un diagrama lo abre en grande. Debajo de cada uno, dónde aparece.</p>
</header>
{groups}
</main>
</body>
</html>
"""


def page_label(path):
    t = re.search(r"<title>(.*?)</title>", (ROOT / path).read_text(encoding="utf-8"), re.S)
    label = html.unescape(t.group(1)).split(" · ")[0].strip() if t else path
    if path.startswith("slides/"):
        label = "Slides · " + label + (" (web)" if "-web/" in path else "")
    return label


def gallery(svgs):
    where = {}
    for page in pages():
        for slug in MARK_OPEN.findall(page.read_text(encoding="utf-8")):
            where.setdefault(slug, []).append(str(page.relative_to(ROOT)))
    out = []
    listed = [s for _, _, slugs in GALLERY for s in slugs]
    missing = [s for s in DIAGRAMS if s not in listed]
    if missing:
        raise SystemExit(f"GALLERY: add {missing} to a group")
    for _, heading, slugs in GALLERY:
        out.append(f"<h2>{html.escape(heading)}</h2>\n<div class=\"figs\">")
        for s in slugs:
            _, title, sub = DIAGRAMS[s]
            links = " · ".join(f'<a href="../{p}">{html.escape(page_label(p))}</a>' for p in dict.fromkeys(where.get(s, [])))
            out.append(
                f'<article class="fig{" is-wide" if s in FEATURED else ""}">'
                f'<a class="pic" href="{s}.html" aria-label="Ver en grande: {html.escape(title)}">{svgs[s]}</a>'
                f'<div class="meta-row"><strong>{html.escape(title)}</strong><span>{html.escape(sub)}</span>'
                + (f"<span>Aparece en: {links}</span>" if links else "")
                + "</div></article>")
        out.append("</div>")
    (OUT / "index.html").write_text(GALLERY_PAGE.replace("{groups}", "\n".join(out)), encoding="utf-8")


PAGE = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<script src="../assets/theme.js"></script>
<script src="../assets/suite-nav.js" defer></script>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
{skin}
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: var(--d-paper); color: var(--d-ink); font-family: "Montserrat", system-ui, sans-serif; margin: 0; }}
  .frame {{ max-width: 1100px; margin: 0 auto; padding: 2rem 16px 3rem; }}
  .eyebrow {{ font: 500 .66rem "Geist Mono", ui-monospace, monospace; letter-spacing: .18em; text-transform: uppercase; color: var(--d-muted); margin-bottom: .5rem; }}
  h1 {{ font-size: clamp(1.4rem, 2vw + .8rem, 1.9rem); font-weight: 700; letter-spacing: -.01em; line-height: 1.2; margin-bottom: .4rem; }}
  .sub {{ color: var(--d-muted); font-size: .9rem; margin-bottom: 1.5rem; }}
  svg {{ display: block; width: 100%; height: auto; min-width: 640px; }}
  .scroll {{ overflow-x: auto; }}
</style>
</head>
<body>
<div class="frame">
  <p class="eyebrow">Diagrama · Taller de Gestión de Proyectos Digitales</p>
  <h1>{title}</h1>
  <p class="sub">{sub}</p>
  <div class="scroll">
{svg}
  </div>
</div>
</body>
</html>
"""

MARK = re.compile(r"(<!--diagram:([a-z0-9-]+)-->)(.*?)(<!--/diagram:\2-->)", re.S)
MARK_OPEN = re.compile(r"<!--diagram:([a-z0-9-]+)-->")


def skin_css():
    """assets/diagram.css inlined (standalone pages must not depend on other files)."""
    css = (ROOT / "assets" / "diagram.css").read_text(encoding="utf-8")
    return re.sub(r"@import url\([^)]*\);\s*", "", css)


def build():
    OUT.mkdir(exist_ok=True)
    svgs = {}
    for slug, (fn, title, sub) in DIAGRAMS.items():
        svg = fn().render()
        svgs[slug] = svg
        (OUT / f"{slug}.html").write_text(PAGE.format(title=html.escape(title), sub=html.escape(sub), svg=svg, skin=skin_css()), encoding="utf-8")
    return svgs


def pages():
    yield from sorted((ROOT / "clases").glob("*.html"))
    yield from sorted((ROOT / "slides").glob("*/index.html"))


def embed(svgs, check=False):
    stale = []
    for page in pages():
        text = page.read_text(encoding="utf-8")

        def sub(m):
            slug = m.group(2)
            if slug not in svgs:
                raise SystemExit(f"{page}: unknown diagram '{slug}'")
            return f"{m.group(1)}\n{svgs[slug]}\n{m.group(4)}"

        new = MARK.sub(sub, text)
        if new != text:
            stale.append(page)
            if not check:
                page.write_text(new, encoding="utf-8")
    return stale


if __name__ == "__main__":
    check = "--check" in sys.argv
    svgs = build()
    stale = embed(svgs, check)
    if not check:
        gallery(svgs)
    if check and stale:
        print("stale:", *[str(p.relative_to(ROOT)) for p in stale], sep="\n  ")
        sys.exit(1)
    print(f"{len(svgs)} diagramas; {'' if check else 'actualizadas '}{len(stale)} páginas")
