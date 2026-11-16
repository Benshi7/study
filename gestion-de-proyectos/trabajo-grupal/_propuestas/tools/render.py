"""Orchestrates all renderers. Usage: python3 render.py  (run build_all.py first or use run-all.sh)."""
import build_all
import charter_template as ct
import render_docs as rd
import render_dt
import render_story
import render_format as rf
import verify_documents as vd


def main():
    o, res, acts, cal = build_all.build()
    c = rd.context(o, res, acts, cal)
    rd.render_gantt(c)
    rd.render_risks(c)
    rd.render_budget(c)
    rd.render_charter(c)
    ct.write(o)
    ct.write_readme(o)
    rd.render_canvas(c)
    render_dt.render(c)
    render_story.render(c)
    rf.render(c)
    rd.render_coherence(c, [])           # first pass: 06 must exist before it can be verified
    ck = vd.run(vd.load(rd.ROOT))
    rd.render_coherence(c, ck)           # second pass: embeds the results
    ck = vd.run(vd.load(rd.ROOT))
    rd.render_summary(c, ck)
    import render_html
    render_html.render(c, ck)
    print("rendered: ok; coherence checks:", [(k.name, k.ok) for k in ck])


if __name__ == "__main__":
    main()
