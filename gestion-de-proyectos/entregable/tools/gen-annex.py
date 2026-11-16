#!/usr/bin/env python3
"""Generates src/12-anexo-a.md from dist/Gantt_corregido_TP_Cascada.xlsx (the team's Gantt with the corrections made by
tools/gen-gantt-corregido.py). Values are reproduced exactly as in that workbook. Order: gen-gantt-corregido.py, then this."""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REPO = ROOT.parent
sys.path.insert(0, str(REPO / "trabajo-grupal" / "_propuestas" / "tools"))
from xlsx_reader import read_workbook  # noqa: E402

wb = dict(read_workbook(ROOT / "dist" / "Gantt_corregido_TP_Cascada.xlsx"))


def cell(v):
    return str(v).replace("|", "\\|").replace("\n", " ").strip()


def table(header, rows):
    out = ["| " + " | ".join(cell(h) for h in header) + " |", "|" + "---|" * len(header)]
    for r in rows:
        r = list(r) + [""] * (len(header) - len(r))
        out.append("| " + " | ".join(cell(x) for x in r[: len(header)]) + " |")
    return "\n".join(out)


def text_rows(rows):
    return [r for r in rows if any(c.strip() for c in r)]


def id_rows(rows, ncols):
    return [r[:ncols] for r in rows if r and r[0].isdigit()]


s1 = wb["Cronograma y Gantt"]
s2 = wb["Dependencias y Camino Crítico"]
s3 = wb["Hitos Operativos y Académicos"]
s4 = wb["Anexo Punto 6"]

parts = ["# Anexo A. Cronograma, dependencias, camino crítico e hitos", ""]
parts += ["Este anexo reproduce las hojas del Excel de planificación del equipo, adaptadas para que las fechas respeten las dependencias entre actividades (ninguna actividad empieza antes de que termine su predecesora), con las dependencias escritas de forma explícita («1, 3» indica las actividades 1 y 3) y con un rol responsable por actividad. Las duraciones, el camino crítico y las holguras son los del equipo.", ""]

# A.1
parts += ["## A.1 Cronograma de actividades", "", s1[0][0], "", s1[1][0], ""]
parts += ["Tabla: Cronograma de actividades del proyecto (adaptado del Excel del equipo)", "", table(s1[2][:9], id_rows(s1, 9)), ""]
# A.2
parts += ["## A.2 Dependencias, holguras y camino crítico", "", s2[0][0], "", s2[1][0], ""]
parts += ["Tabla: Dependencias, holguras y camino crítico (adaptado del Excel del equipo)", "", table(s2[2][:7], id_rows(s2, 7)), ""]
# A.3
hdr3 = next(r for r in s3 if r and r[0] == "Hito Operativo")
rows3 = [r[:4] for r in s3 if r and len(r) > 1 and r[1][:2].isdigit() and r[0] != "Hito Operativo"]
parts += ["## A.3 Hitos del proyecto", "", s3[0][0].strip(), "", "**" + s3[2][0] + "**", ""]
parts += ["Tabla: Hitos operativos del proyecto (adaptado del Excel del equipo)", "", table(hdr3[:4], rows3), ""]
# A.4 (sheet 'Anexo Punto 6', numbered 6.4 / 6.5 in the workbook)
t4 = text_rows(s4)
title4, intro4 = t4[0][0], t4[1][0]
sec64, para64 = t4[2][0], t4[3][0]
hdr4 = next(r for r in s4 if r and r[0] == "ID")
rows4 = id_rows(s4, 6)
pert_t = next(r[0] for r in s4 if r and r[0].startswith("Nota metodológica"))
pert_p = next(r[0] for i, r in enumerate(s4) if r and r[0].startswith("El análisis incluido"))
sec65 = next(r[0] for r in s4 if r and r[0].startswith("6.5"))
hdr65 = next(r for r in s4 if r and r[0] == "Hito")
rows65 = [r[:4] for r in s4 if r and len(r) > 1 and r[1][:2].isdigit() and r[0] != "Hito" and "/" in r[1] and len(r[1]) == 10]
parts += ["## A.4 Análisis del camino crítico e hitos (anexo al punto 6)", "", title4, "", intro4, "", "**" + sec64 + "**", "", para64, ""]
parts += ["Tabla: Actividades de la red con holgura y condición de críticas (adaptado del Excel del equipo)", "", table(hdr4[:6], rows4), ""]
parts += ["**" + pert_t + "**", "", pert_p, "", "**" + sec65 + "**", ""]
parts += ["Tabla: Hitos del proyecto según el anexo al punto 6 (adaptado del Excel del equipo)", "", table(hdr65[:4], rows65), ""]

(ROOT / "src" / "12-anexo-a.md").write_text("\n".join(parts), encoding="utf-8")
print("annex rows:", len(id_rows(s1, 9)), len(id_rows(s2, 7)), len(rows3), len(rows4), len(rows65))
