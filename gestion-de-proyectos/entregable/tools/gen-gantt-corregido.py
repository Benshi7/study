#!/usr/bin/env python3
"""Corrige el Gantt del equipo y genera:
   - data/gantt.json                       (fuente única para el Anexo A, el gráfico de Gantt y los tests)
   - dist/Gantt_corregido_TP_Cascada.xlsx  (copia del Excel del equipo con las correcciones; el original no se toca)

Correcciones (todas listadas en la hoja «Correcciones» del libro y en CAMBIOS-vs-ORIGINALES.md):
  1. Superposiciones: una actividad no puede empezar antes de que termine su predecesora (relación fin a inicio, sin
     desfase). Cada actividad empieza el día hábil siguiente al fin de su última predecesora, o en su fecha original si
     esa fecha ya es posterior. Las duraciones no cambian; el fin se recalcula con la duración.
  2. Dependencias con notación explícita: «1-3» pasa a «1, 3» (las actividades 1 y 3, como ya hacía la hoja del anexo).
  3. Responsable: un rol por actividad, tomado de los perfiles del presupuesto (más Sponsor para aprobaciones).
  4. Se quita la línea de hitos académicos de la hoja del anexo (el documento no hace referencia a fechas de entrega).
Requiere openpyxl:  PY_XL=/ruta/al/python/con/openpyxl python3 tools/gen-gantt-corregido.py
(si PY_XL no está definido se usa el intérprete actual). Calendario: lunes a viernes, sin feriados (igual que el original)."""
import datetime as dt
import json
import pathlib
import re
import sys

import openpyxl

ROOT = pathlib.Path(__file__).resolve().parents[1]
REPO = ROOT.parent
SRC = REPO / "trabajo-grupal" / "Gantt_y_Camino_Critico_Hitos_Anexo_Punto_6.xlsx"
OUT_XLSX = ROOT / "dist" / "Gantt_corregido_TP_Cascada.xlsx"
OUT_JSON = ROOT / "data" / "gantt.json"
PROJECT_END = dt.date(2026, 9, 30)

D = lambda s: dt.datetime.strptime(s, "%d/%m/%y").date()
fmt2 = lambda d: d.strftime("%d/%m/%y")
fmt4 = lambda d: d.strftime("%d/%m/%Y")

ROLE = {
    1: "Project Manager", 2: "Project Manager", 3: "Analistas funcionales", 4: "Sponsor",
    5: "Analistas funcionales", 6: "Analistas funcionales", 7: "Especialistas en datos y GIS",
    8: "Analistas funcionales", 9: "Analistas funcionales", 10: "Project Manager",
    11: "Desarrolladores", 12: "Especialistas en datos y GIS", 13: "Desarrolladores", 14: "Analistas funcionales",
    15: "Desarrolladores", 16: "UX/UI", 17: "Sponsor",
    18: "Desarrolladores", 19: "Desarrolladores", 20: "Desarrolladores", 21: "Desarrolladores", 22: "Desarrolladores",
    23: "Desarrolladores", 24: "Especialistas en datos y GIS", 25: "Desarrolladores", 26: "QA y testing",
    27: "QA y testing", 28: "QA y testing", 29: "UX/UI", 30: "Seguridad informática", 31: "Desarrolladores",
    32: "Sponsor", 33: "Infraestructura/DevOps", 34: "Documentación y capacitación", 35: "Infraestructura/DevOps",
    36: "Infraestructura/DevOps", 37: "Project Manager", 38: "Documentación y capacitación",
    39: "Project Manager", 40: "Sponsor",
}
HITO_ACT = [4, 10, 17, 23, 26, 32, 35, 40]  # actividad cuyo fin marca cada hito (1..8)


def isw(d):
    return d.weekday() < 5


def nextwd(d):
    d += dt.timedelta(1)
    while not isw(d):
        d += dt.timedelta(1)
    return d


def addwd(start, n):
    d = start
    for _ in range(n - 1):
        d = nextwd(d)
    return d


def bd(a, b):
    return sum(1 for k in range((b - a).days + 1) if isw(a + dt.timedelta(k)))


def parse_deps(s):
    """«a-b» se lee como las actividades a y b (así calcula el CPM del equipo); «a, b» y «a,b» son las listadas."""
    if s in ("-", None, ""):
        return []
    out = []
    for p in re.split(r"\s*,\s*", str(s).strip()):
        if re.fullmatch(r"\d+-\d+", p):
            a, b = p.split("-")
            out += [int(a), int(b)]
        elif p:
            out.append(int(p))
    return sorted(set(out))


def deps_text(lst):
    return ", ".join(str(x) for x in lst) if lst else "-"


def main():
    wb = openpyxl.load_workbook(SRC)
    ws1, ws2, ws3, ws4 = wb.worksheets
    T = {}
    for r in range(5, ws1.max_row + 1):
        if ws1.cell(r, 1).value is None:
            continue
        i = int(ws1.cell(r, 1).value)
        T[i] = dict(id=i, row=r, fase=ws1.cell(r, 2).value, act=ws1.cell(r, 3).value, s0=D(ws1.cell(r, 4).value),
                    e0=D(ws1.cell(r, 5).value), dur=int(ws1.cell(r, 6).value), dep0=str(ws1.cell(r, 7).value),
                    ent=ws1.cell(r, 9).value)
        T[i]["deps"] = parse_deps(T[i]["dep0"])
    assert len(T) == 40
    for t in T.values():
        assert bd(t["s0"], t["e0"]) == t["dur"], f"duración incoherente en la actividad {t['id']}"

    # 1) fechas corregidas
    for i in sorted(T):
        t = T[i]
        s = t["s0"]
        for p in t["deps"]:
            s = max(s, nextwd(T[p]["e"]))
        t["s"], t["e"] = s, addwd(s, t["dur"])
    changes = []
    for i in sorted(T):
        t = T[i]
        if (t["s"], t["e"]) != (t["s0"], t["e0"]):
            over = [p for p in t["deps"] if t["s0"] <= T[p]["e0"]]
            motivo = ("Empezaba antes de que terminara su predecesora (" + ", ".join(str(p) for p in over) + ")") if over else \
                "Se desplaza porque una predecesora corrigió su fecha de fin"
            changes.append(dict(id=i, campo="Inicio / Fin", antes=f"{fmt2(t['s0'])} – {fmt2(t['e0'])}",
                                despues=f"{fmt2(t['s'])} – {fmt2(t['e'])}", motivo=motivo))
        if t["dep0"] != deps_text(t["deps"]):
            changes.append(dict(id=i, campo="Dependencias", antes=t["dep0"], despues=deps_text(t["deps"]),
                                motivo="Notación explícita: se listan las actividades predecesoras"))
    overlaps0 = sorted(i for i, t in T.items() if any(t["s0"] <= T[p]["e0"] for p in t["deps"]))

    # 2) CPM (solo duraciones y dependencias; fin a inicio sin desfase)
    es, ef = {}, {}
    for i in sorted(T):
        es[i] = max([ef[p] for p in T[i]["deps"]], default=0)
        ef[i] = es[i] + T[i]["dur"]
    L = max(ef.values())
    succ = {i: [j for j in T if i in T[j]["deps"]] for i in T}
    lf, ls = {}, {}
    for i in sorted(T, reverse=True):
        lf[i] = min([ls[j] for j in succ[i]], default=L)
        ls[i] = lf[i] - T[i]["dur"]
    for i, t in T.items():
        t["slack"] = ls[i] - es[i]
        t["critical"] = t["slack"] == 0
    # contra la hoja del equipo
    for r in range(5, ws2.max_row + 1):
        if ws2.cell(r, 1).value is None:
            continue
        i = int(ws2.cell(r, 1).value)
        assert int(ws2.cell(r, 6).value) == T[i]["slack"], f"holgura distinta en {i}"
        assert (ws2.cell(r, 7).value == "SÍ") == T[i]["critical"], f"crítica distinta en {i}"
    crit = [i for i in T if T[i]["critical"]]
    assert L == 126 and len(crit) == 23, (L, len(crit))

    # 3) controles de la planificación corregida
    for i, t in T.items():
        for p in t["deps"]:
            assert t["s"] > T[p]["e"], f"superposición {i} con {p}"
    end = max(t["e"] for t in T.values())
    assert end <= PROJECT_END, end
    window = bd(dt.date(2026, 4, 1), PROJECT_END)
    hitos = []
    names = [(ws3.cell(r, 1).value, ws3.cell(r, 3).value, ws3.cell(r, 4).value) for r in range(6, 14)]
    for n, aid in enumerate(HITO_ACT, 1):
        hitos.append(dict(n=n, name=names[n - 1][0], result=names[n - 1][1], scope=names[n - 1][2], activity=aid,
                          date=fmt4(T[aid]["e"]), date_original=ws3.cell(5 + n, 2).value))

    # 4) escribir el libro corregido (sobre una copia del original)
    for i, t in T.items():
        r = t["row"]
        ws1.cell(r, 4).value = fmt2(t["s"])
        ws1.cell(r, 5).value = fmt2(t["e"])
        ws1.cell(r, 7).value = deps_text(t["deps"])
        ws1.cell(r, 8).value = ROLE[i]
    ws1["A2"].value = ("Período operativo ficticio del proyecto. Duración en días hábiles (lunes a viernes). "
                       "«Responsable» indica el rol principal de cada actividad. Dependencias: «1, 3» significa las actividades 1 y 3; "
                       "ninguna actividad empieza antes de que termine su predecesora.")
    for r in range(5, ws2.max_row + 1):
        if ws2.cell(r, 1).value is None:
            continue
        i = int(ws2.cell(r, 1).value)
        ws2.cell(r, 4).value = deps_text(T[i]["deps"])
    ws2["A2"].value = ("Cálculo CPM basado exclusivamente en las dependencias y duraciones del cronograma. Holgura 0 = actividad crítica. "
                       "La duración de la red es de 126 días hábiles dentro de una ventana de 131 días hábiles (01/04 al 30/09/2026).")
    for n, h in enumerate(hitos):
        ws3.cell(6 + n, 2).value = h["date"]
    for r in range(44, 52):  # hitos del anexo (hoja 4)
        n = r - 43
        ws4.cell(r, 2).value = hitos[n - 1]["date"]
    # tabla de actividades críticas del anexo: dependencias explícitas ya estaban; se verifica
    for r in range(13, 36):
        v = ws4.cell(r, 1).value
        if v is not None and str(v).isdigit():
            i = int(v)
            assert i in crit, f"actividad {i} del anexo no es crítica"
            if ws4.cell(r, 6).value not in (None, "-"):
                ws4.cell(r, 6).value = deps_text(T[i]["deps"])
    ws4["A8"].value = ws4["A8"].value.replace("126 unidades de trabajo", "126 días hábiles, dentro de una ventana de 131 días hábiles")
    ws4["A53"].value = None
    # hoja de correcciones
    wsc = wb.create_sheet("Correcciones")
    wsc["A1"].value = "CORRECCIONES RESPECTO DEL EXCEL ORIGINAL DEL EQUIPO"
    wsc["A2"].value = ("Las duraciones, el camino crítico (126 días hábiles, 23 actividades con holgura 0) y las holguras no cambian. "
                       "Se corrigen fechas, notación de dependencias y se completa «Responsable».")
    hdr = ["ID", "Actividad", "Campo", "Original", "Corregido", "Motivo"]
    for c, h in enumerate(hdr, 1):
        wsc.cell(4, c).value = h
    row = 5
    for ch in changes:
        wsc.cell(row, 1).value = ch["id"]
        wsc.cell(row, 2).value = T[ch["id"]]["act"]
        wsc.cell(row, 3).value = ch["campo"]
        wsc.cell(row, 4).value = ch["antes"]
        wsc.cell(row, 5).value = ch["despues"]
        wsc.cell(row, 6).value = ch["motivo"]
        row += 1
    for h in hitos:
        if h["date"] != h["date_original"]:
            wsc.cell(row, 1).value = f"Hito {h['n']}"
            wsc.cell(row, 2).value = h["name"]
            wsc.cell(row, 3).value = "Fecha"
            wsc.cell(row, 4).value = h["date_original"]
            wsc.cell(row, 5).value = h["date"]
            wsc.cell(row, 6).value = f"Fin de la actividad {h['activity']} en el cronograma corregido"
            row += 1
    # estilo de la hoja nueva, copiado de las cabeceras de la primera hoja
    for c in range(1, 7):
        src = ws1.cell(4, c)
        dst = wsc.cell(4, c)
        dst.font, dst.fill, dst.border, dst.alignment = src.font.copy(), src.fill.copy(), src.border.copy(), src.alignment.copy()
    wsc["A1"].font = ws1["A1"].font.copy()
    for col, w in zip("ABCDEF", (10, 40, 16, 22, 22, 70)):
        wsc.column_dimensions[col].width = w
    ws1.column_dimensions["H"].width = 30
    OUT_XLSX.parent.mkdir(exist_ok=True)
    wb.save(OUT_XLSX)

    gaps = window - L
    data = dict(
        generated_by="tools/gen-gantt-corregido.py",
        calendar="lunes a viernes, sin feriados",
        project_start="01/04/2026", project_end="30/09/2026",
        cp_days=L, window_days=window, idle_days=gaps, critical_count=len(crit),
        overlaps_original=overlaps0,
        phases=["Inicio", "Análisis", "Diseño", "Desarrollo", "Integración", "Pruebas", "Implementación", "Cierre"],
        tasks=[dict(id=i, fase=t["fase"], act=t["act"], start=fmt2(t["s"]), end=fmt2(t["e"]), start_original=fmt2(t["s0"]),
                    end_original=fmt2(t["e0"]), dur=t["dur"], deps=t["deps"], deps_text=deps_text(t["deps"]),
                    resp=ROLE[i], ent=t["ent"], slack=t["slack"], critical=t["critical"]) for i, t in sorted(T.items())],
        hitos=hitos,
        changes=changes,
    )
    OUT_JSON.parent.mkdir(exist_ok=True)
    OUT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"superposiciones originales: {overlaps0}")
    print(f"actividades con fecha cambiada: {sum(1 for c in changes if c['campo'] == 'Inicio / Fin')}; red {L} d.h., ventana {window}, ociosos {gaps}")
    print("hitos:", [(h['n'], h['date_original'], '->', h['date']) for h in hitos])


if __name__ == "__main__":
    sys.exit(main())
