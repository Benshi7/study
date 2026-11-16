#!/usr/bin/env python3
"""One-time (re-runnable) extraction of the markdown sources from the team's originals.

Reads (read-only):
  trabajo-grupal/_analisis/convertidos/charter-y-demas.md   (converted from 'Proyect Charter y demas puntos.docx', "F1")
  trabajo-grupal/_analisis/convertidos/proyecto-integrador.md (converted from 'Proyecto Integrador ... .docx', "F2")
  trabajo-grupal/Gantt_y_Camino_Critico_Hitos_Anexo_Punto_6.xlsx
Writes entregable/src/{02b,03(part),05,06(part),09,10,11,12}-*.md and copies the Gantt image.

The converted markdown is only an intermediate: tests/docx.test.mjs checks the final docx against the ORIGINAL
.docx files, so a converter mistake cannot go unnoticed. Hand-written files (01, 02, 03 figure, 04, 07, 08)
are not touched by this script. Every deviation from the originals is logged in CAMBIOS-vs-ORIGINALES.md.
"""
import pathlib
import re
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REPO = ROOT.parent
CONV = REPO / "trabajo-grupal" / "_analisis" / "convertidos"
SRC = ROOT / "src"
IMG = ROOT / "img"
sys.path.insert(0, str(REPO / "trabajo-grupal" / "_propuestas" / "tools"))
from xlsx_reader import read_workbook  # noqa: E402  (read-only reuse)

H1_TITLES = {
    5: "5. Project Charter",
    6: "6. Gantt del proyecto completo",
    9: "9. Gestión de riesgos - Matriz de riesgos",
    10: "10. Gestión de costos - Presupuesto",
}

f1 = (CONV / "charter-y-demas.md").read_text(encoding="utf-8").split("\n")
f2 = (CONV / "proyecto-integrador.md").read_text(encoding="utf-8").split("\n")


def find(lines, pattern, start=0):
    rx = re.compile(pattern)
    for i in range(start, len(lines)):
        if rx.search(lines[i]):
            return i
    raise SystemExit(f"marker not found: {pattern}")


HEAD_RX = re.compile(r"^(?:#{1,6}\s+|\*\*)(\d+(?:\.\d+)*)\.?\s+(.*?)(?:\*\*)?\s*:?\s*$")


def normalize_headings(block):
    out = []
    for line in block:
        m = HEAD_RX.match(line.rstrip())
        if m and (line.startswith("#") or (line.startswith("**") and line.rstrip().endswith(("**", "**:")))):
            num, title = m.group(1), m.group(2).strip().rstrip(":").strip("*").strip()
            depth = num.count(".") + 1
            if depth == 1:
                if int(num) in H1_TITLES and not any(o.startswith("# ") for o in out):
                    out.append("# " + H1_TITLES[int(num)])
                    continue
                out.append(line)  # numbered bold item (e.g. an objective), not a heading
                continue
            out.append("#" * depth + " " + f"{num} {title}")
            continue
        out.append(line)
    return out


def tidy(block):
    text = "\n".join(block)
    text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"
    return text


# ---------------------------------------------------------------- F1 section 5 (Project Charter)
i5 = find(f1, r"^\*\*5\. PROJECT CHARTER\*\*")
i6 = find(f1, r"^\*\*6\. GANTT DEL PROYECTO COMPLETO\*\*")
i7 = find(f1, r"^## 7\. Matriz de Stakeholders")
i9 = find(f1, r"^\*\*9\. GESTI[OÓ]N DE RIESGOS")
i10 = find(f1, r"^\*\*10\. Gesti[oó]n de Costos")

sec5 = f1[i5:i6]
n0 = find(sec5, r"^\*NOTA: Para el TP")
n1 = find(sec5, r"^## 5\.5\. Alcance", n0)
removed_note = sec5[n0:n1]
sec5 = sec5[:n0] + sec5[n1:]
(SRC / "05-project-charter.md").write_text(tidy(normalize_headings(sec5)), encoding="utf-8")

# ---------------------------------------------------------------- F1 section 6 (Gantt)
sec6 = [l for l in f1[i6:i7] if "image1.emf" not in l]
sec6 = [l.replace("![imagen](media/charter-y-demas/image5.png)", "![Diagrama de Gantt del proyecto: cronograma detallado de las 40 actividades](img/gantt-f1.png)") for l in sec6]
shutil.copyfile(CONV / "media" / "charter-y-demas" / "image5.png", IMG / "gantt-f1.png")
sec6 = normalize_headings(sec6)
wb = dict(read_workbook(REPO / "trabajo-grupal" / "Gantt_y_Camino_Critico_Hitos_Anexo_Punto_6.xlsx"))
dep_rows = [r for r in wb["Dependencias y Camino Crítico"] if r and r[0].isdigit()]
critical = sum(1 for r in dep_rows if r[6].strip().upper() in ("SÍ", "SI"))
crono_rows = [r for r in wb["Cronograma y Gantt"] if r and r[0].isdigit()]
phases = []
for r in crono_rows:
    if r[1] not in phases:
        phases.append(r[1])
# summary box (facts read from the team's Excel; no new analysis)
box = [
    "",
    f"> **Resumen del cronograma.** El detalle completo (cronograma de {len(crono_rows)} actividades, dependencias, holguras, camino crítico e hitos) se encuentra en el **Anexo A**, tomado del Excel del equipo. "
    f"El proyecto se organiza en {len(phases)} fases ({', '.join(p.lower() for p in phases)}) entre el 01/04/2026 y el 30/09/2026. "
    f"La hoja de dependencias marca {critical} actividades con holgura cero (camino crítico) y la planilla de hitos registra 8 hitos operativos.",
    "",
]
# put the box right after the caption line of the detailed schedule image
out6 = []
for l in sec6:
    out6.append(l)
    if l.startswith("**Anexo Cronograma Detallado"):
        out6.extend(box)
(SRC / "06-gantt.md").write_text(tidy(out6), encoding="utf-8")

# ---------------------------------------------------------------- F1 sections 9 and 10
(SRC / "09-riesgos.md").write_text(tidy(normalize_headings(f1[i9:i10])), encoding="utf-8")
(SRC / "10-presupuesto.md").write_text(tidy(normalize_headings(f1[i10:])), encoding="utf-8")

# ---------------------------------------------------------------- F2 pieces (resumen ejecutivo, canvas text, conclusion)


def f2_block(start_rx, end_rx):
    a = find(f2, start_rx)
    b = find(f2, end_rx, a + 1)
    out = []
    for l in f2[a + 1:b]:
        if l.startswith("## ") and not re.match(r"^## \d", l):
            out.append(l[3:])  # F2 used '##' for plain paragraphs
        else:
            out.append(l)
    return out


resumen = f2_block(r"^# Resumen Ejecutivo", r"^# Canvas del Proyecto")
resumen = [l for l in resumen if not l.startswith("## Storytelling")]
(SRC / "02b-resumen-ejecutivo.md").write_text("# Resumen ejecutivo\n\n## Storytelling del proyecto\n\n" + tidy(resumen), encoding="utf-8")

canvas = f2_block(r"^# Canvas del Proyecto", r"^# Aplicaci[oó]n de Design Thinking")
(SRC / "_canvas-text-from-f2.md").write_text(tidy(canvas), encoding="utf-8")  # merged by hand into 03-canvas.md

concl = f2_block(r"^# Conclusi[oó]n General", r"^# \*\*Resumen y borrador\*\*")
(SRC / "11-conclusion.md").write_text("# Conclusión general\n\n" + tidy(concl), encoding="utf-8")

print("removed note words:", len(" ".join(removed_note).split()))
print("critical:", critical, "phases:", phases, "activities:", len(crono_rows))
