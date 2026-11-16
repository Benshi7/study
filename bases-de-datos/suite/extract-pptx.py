# Extracts the slide text of every .pptx in a folder to one Markdown file per deck.
# Usage:  python3 -I suite/extract-pptx.py raw /tmp/decks
# Read the output, then add concepts/edges/cards to suite/data/content.js (see README.md).
import zipfile,re,sys,pathlib
from xml.etree import ElementTree as ET
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
src=pathlib.Path(sys.argv[1]); out=pathlib.Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
for f in sorted(src.glob("*.pptx")):
    z=zipfile.ZipFile(f)
    slides=sorted([n for n in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml$',n)],key=lambda n:int(re.findall(r'\d+',n)[0]))
    lines=[]
    for i,n in enumerate(slides,1):
        root=ET.fromstring(z.read(n))
        paras=[]
        for p in root.iter('{%s}p'%ns['a']):
            t=''.join(x.text or '' for x in p.iter('{%s}t'%ns['a'])).strip()
            if t: paras.append(t)
        lines.append(f"## Slide {i}\n"+"\n".join(paras))
    name=re.sub(r'[^A-Za-z0-9]+','_',f.stem).strip('_')
    (out/f"{name}.md").write_text("\n\n".join(lines),encoding="utf-8")
    print(f.name,len(slides),"slides")
