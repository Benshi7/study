# Suite de estudio y TP — Taller de Gestión de Proyectos Digitales

Abrir `index.html` en el navegador (doble clic; no necesita servidor).

| Carpeta | Para qué |
| --- | --- |
| `clases/` | Lecciones de concepto, una por clase de la cátedra. |
| `tp/` | TP Cascada del equipo. **Autocontenida: es la que se comparte.** |
| `raw/` | PDFs de la cátedra. |
| `assets/` | Estilos, scripts y catálogo (`suite-data.js`). Fuente única. |
| `tools/` | Utilidades: `sync-assets.sh`, `check-links.sh`, `check-tp-standalone.sh`, `share-tp.sh`. |

## Sumar una clase nueva
1. Copiar el PDF a `raw/`.
2. Ajustar la entrada de la clase en `assets/suite-data.js`.
3. Crear la lección en `clases/` desde `clases/_template.html` y poner `status: "listo"`.
4. `tools/sync-assets.sh` (si tocó `assets/`) y `tools/check-links.sh`.

## Compartir el TP con el equipo
1. `tools/share-tp.sh` sincroniza los assets, comprueba que `tp/` sea autocontenida (`tools/check-tp-standalone.sh`) y genera `dist/tp-cascada.zip`.
2. Mandar el zip al grupo. Cada integrante lo descomprime y abre `tp-cascada/index.html` (doble clic, sin servidor ni cuentas). `LEEME.txt` explica todo en una página.
3. **Votar:** `decisiones.html`. Cada persona vota en su navegador, copia su código (`TPV1.…`) al grupo, y cualquiera pega los códigos en *Recuento* para ver el resultado y exportar las decisiones cerradas.
4. **Avance:** `avance.html`. El estado se pasa por código (`TPS1.…`) y se integra por sección (gana la edición más reciente).
5. Los links atenuados (`class="local-only"`) apuntan a `raw/` o `clases/` y solo funcionan en la copia completa.

Para agregar una decisión nueva: editar el bloque `EDIT HERE` de `tp/decisiones.html` (sin cambiar los `id` de las ya votadas) y volver a compartir la carpeta.

Archivos propios de `tp/assets/` que no se sincronizan desde `assets/`: `logic.js` (votos y avance, sin DOM), `tp-data.js`, `tp-common.js`, `tp.css`, `tp-nav.css`. Si cambian páginas o estados de las secciones, actualizar `tp/assets/tp-data.js` y `assets/suite-data.js` (`tools/check-links.sh` avisa si difieren).

## Mantener el entregable (`compartir/`)

`compartir/tp-cascada-canvas-y-partes.html` es un único HTML, sin referencias a estas carpetas, para mandar a los compañeros. **No se edita a mano**: se genera.

- **Contenido de las 4 opciones de Canvas** (bloques, comparador, mapa de valor, qué cambia en cada sección): editar `tp/assets/canvas-data.js`. Es la fuente única: la usan el taller (`tp/canvas-taller.html`) y el entregable, así que un cambio se edita una sola vez.
- **Texto, estilos y comportamiento de la página**: editar `compartir/src/tp-cascada.template.html` (y `compartir/src/render.js` si cambia cómo se dibuja el Canvas).
- Después de editar: `tools/build-compartir.sh` regenera el HTML y `tools/test-compartir.sh` verifica que las 4 opciones sigan completas (9 bloques cada una), que no haya referencias internas ni recursos locales, y que los scripts compilen.
- Al cambiar `tp/assets/canvas-data.js` también hay que volver a armar el zip del equipo con `tools/share-tp.sh`, porque el taller lo carga.

