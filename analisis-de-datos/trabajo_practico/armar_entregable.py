"""Arma la carpeta entregable/ y el zip a partir del repo.

Copia solo lo que va en la entrega (deja afuera interno/, la base SQLite, el entorno virtual y los
archivos temporales). Se puede correr las veces que haga falta: borra la carpeta anterior y la
vuelve a armar.

    python armar_entregable.py
"""
import shutil
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
DESTINO = RAIZ / "entregable"
ZIP = RAIZ / "TP_freMTPL2_entregable"

# (origen, patrón): todo lo que coincide con el patrón dentro del origen, manteniendo las carpetas
QUE_VA = [
    (".", "README.md"),
    (".", "documentacion.html"),
    (".", "requirements.txt"),
    ("docs", "*.md"),
    ("datasets", "*.csv"),
    ("sql", "*.sql"),
    ("src", "*.py"),
    ("notebooks", "*.ipynb"),
    ("export", "*"),
    ("powerbi", "*"),
    ("presentacion", "index.html"),
    ("presentacion", "relatividades.csv"),
    ("presentacion/assets", "**/*"),
    ("presentacion/img", "*.png"),
    ("presentacion/diagramas", "*.html"),
]
NO_VA = ("Zone.Identifier", "__pycache__", ".ipynb_checkpoints")


def main():
    if not (RAIZ / "export" / "polizas.csv").exists():
        raise SystemExit("Falta export/polizas.csv: correr antes  python src/etl.py")

    if DESTINO.exists():
        shutil.rmtree(DESTINO)

    copiados = 0
    for carpeta, patron in QUE_VA:
        for origen in sorted((RAIZ / carpeta).glob(patron)):
            if not origen.is_file() or any(x in str(origen) for x in NO_VA):
                continue
            destino = DESTINO / origen.relative_to(RAIZ)
            destino.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(origen, destino)
            copiados += 1

    zip_final = shutil.make_archive(str(ZIP), "zip", root_dir=RAIZ, base_dir=DESTINO.name)
    tam = Path(zip_final).stat().st_size / 1e6
    print(f"{copiados} archivos copiados a {DESTINO.name}/")
    print(f"Zip: {Path(zip_final).name} ({tam:.1f} MB)")


if __name__ == "__main__":
    main()
