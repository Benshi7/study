"""Inline SVG builders (themed with CSS variables so they work in light and dark)."""
import html

MONTHS_ES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
PHASE_COLORS = ["#2b7bb9", "#e07b1f", "#2e8b57", "#7b4fb0", "#9b5a42", "#6b7280", "#a3a31a", "#1aa3b8"]


def _esc(s):
    return html.escape(str(s), quote=True)


def gantt_full(acts, res, cal, phase_of, names, width=980, themed=True):
    """40-row Gantt: x = working-day index. Critical bars have a thick outline."""
    left, top, rowh = 300, 36, 17
    total = max(r["ef"] for r in res.values())
    plot_w = width - left - 20
    sx = plot_w / total
    h = top + rowh * len(acts) + 40
    ink = "var(--ink)" if themed else "#222"
    mute = "var(--mute)" if themed else "#777"
    grid = "var(--rule)" if themed else "#ddd"
    s = [f'<svg viewBox="0 0 {width} {h}" role="img" aria-label="Diagrama de Gantt de las 40 actividades" xmlns="http://www.w3.org/2000/svg" font-family="system-ui, sans-serif" font-size="11">']
    # month grid
    last_m = None
    for idx in range(total):
        d = cal.date_of(idx)
        if d.month != last_m:
            x = left + idx * sx
            s.append(f'<line x1="{x:.1f}" y1="{top - 10}" x2="{x:.1f}" y2="{h - 30}" stroke="{grid}" stroke-dasharray="3 3"/>')
            s.append(f'<text x="{x + 3:.1f}" y="{top - 14}" fill="{mute}">{MONTHS_ES[d.month - 1]} {d.year}</text>')
            last_m = d.month
    for k, a in enumerate(acts):
        y = top + k * rowh
        r = res[a["id"]]
        ph = phase_of[a["id"]]
        color = PHASE_COLORS[ph - 1]
        s.append(f'<text x="{left - 8}" y="{y + 11}" text-anchor="end" fill="{ink}">{a["id"]}. {_esc(names[a["id"]][:44])}</text>')
        w = max((r["ef"] - r["es"]) * sx, 3)
        stroke = f'stroke="{ink}" stroke-width="2"' if r["critical"] else 'stroke="none"'
        s.append(f'<rect x="{left + r["es"] * sx:.1f}" y="{y + 2}" width="{w:.1f}" height="{rowh - 5}" rx="2" fill="{color}" {stroke}><title>{a["id"]} · {_esc(names[a["id"]])} · holgura {r["slack"]} d.h.</title></rect>')
    s.append(f'<text x="{left}" y="{h - 10}" fill="{mute}">Borde grueso = actividad crítica (holgura 0). Una barra por actividad; color por fase.</text>')
    s.append("</svg>")
    return "\n".join(s)


def gantt_phases(phases, res, cal, gates, width=800):
    """Phase-level Gantt with gate diamonds. phases: [(id, name, es, ef)]."""
    left, top, rowh = 250, 30, 28
    total = max(p[3] for p in phases)
    plot_w = width - left - 34
    sx = plot_w / total
    h = top + rowh * len(phases) + 30
    s = [f'<svg viewBox="0 0 {width} {h}" role="img" aria-label="Gantt por fases con los 8 hitos de control" xmlns="http://www.w3.org/2000/svg" font-family="system-ui, sans-serif" font-size="12">']
    last_m = None
    for idx in range(total):
        d = cal.date_of(idx)
        if d.month != last_m:
            x = left + idx * sx
            s.append(f'<line x1="{x:.1f}" y1="{top - 8}" x2="{x:.1f}" y2="{h - 20}" stroke="var(--rule)" stroke-dasharray="3 3"/>')
            s.append(f'<text x="{x + 3:.1f}" y="{top - 12}" fill="var(--mute)">{MONTHS_ES[d.month - 1]}</text>')
            last_m = d.month
    for k, (pid, name, es, ef) in enumerate(phases):
        y = top + k * rowh
        s.append(f'<text x="{left - 8}" y="{y + 17}" text-anchor="end" fill="var(--ink)">{pid}. {_esc(name)}</text>')
        s.append(f'<rect x="{left + es * sx:.1f}" y="{y + 4}" width="{(ef - es) * sx:.1f}" height="18" rx="3" fill="{PHASE_COLORS[pid - 1]}"/>')
        gx = left + ef * sx
        s.append(f'<path d="M{gx:.1f} {y + 2} l7 11 l-7 11 l-7 -11 z" fill="var(--bg)" stroke="var(--ink)" stroke-width="2"><title>{_esc(gates[pid - 1])}</title></path>')
    s.append(f'<text x="{left}" y="{h - 4}" fill="var(--mute)">◇ = hito de control (gate) al final de cada fase</text>')
    s.append("</svg>")
    return "\n".join(s)


def s_curve(cum, labels, total, width=520, height=240):
    left, bottom, top = 54, height - 36, 16
    n = len(labels)
    xs = [left + i * (width - left - 20) / (n - 1) for i in range(n)]
    ys = [bottom - (cum[k] / total) * (bottom - top) for k in labels]
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
    s = [f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="Curva S del costo acumulado por mes" xmlns="http://www.w3.org/2000/svg" font-family="system-ui, sans-serif" font-size="11">']
    for frac in (0, 0.25, 0.5, 0.75, 1):
        y = bottom - frac * (bottom - top)
        s.append(f'<line x1="{left}" y1="{y:.1f}" x2="{width - 20}" y2="{y:.1f}" stroke="var(--rule)"/>')
        s.append(f'<text x="{left - 6}" y="{y + 4:.1f}" text-anchor="end" fill="var(--mute)">{frac * total:,.0f}</text>'.replace(",", "."))
    for x, k in zip(xs, labels):
        s.append(f'<text x="{x:.1f}" y="{bottom + 16}" text-anchor="middle" fill="var(--mute)">{k[-2:]}/{k[2:4]}</text>')
    s.append(f'<polyline points="{pts}" fill="none" stroke="var(--accent)" stroke-width="3"/>')
    for x, y in zip(xs, ys):
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="var(--accent)"/>')
    s.append("</svg>")
    return "\n".join(s)
