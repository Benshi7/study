# Técnica y referencias

## 1. Stack

- **HTML + CSS + JavaScript vanilla**, todo en **un solo archivo**: `mock/index.html`.
- **Leaflet 1.9.4** (mapa), cargado desde unpkg con versión fijada:
  - CSS: `https://unpkg.com/leaflet@1.9.4/dist/leaflet.css`
  - JS: `https://unpkg.com/leaflet@1.9.4/dist/leaflet.js`
  - Se recomienda agregar los atributos `integrity` y `crossorigin=""` que figuran en la documentación oficial de Leaflet para esa versión (**a verificar por quien implemente** en https://leafletjs.com/download.html).
- **Teselas de OpenStreetMap:** `https://tile.openstreetmap.org/{z}/{x}/{y}.png`.
- **Atribución obligatoria:** `© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors` (Leaflet la muestra desde la opción `attribution` de la capa; no ocultarla).
- **Sin build, sin npm, sin frameworks.** Los iconos son SVG en línea.
- **Datos:** el contenido de `seed-data.json` incrustado en `<script type="application/json" id="seed">…</script>` y leído con `JSON.parse`.

## 2. Aviso sobre las teselas de OpenStreetMap

Las teselas del servidor público de OpenStreetMap tienen una **política de uso** (Tile Usage Policy): sirven para demostraciones de bajo tráfico, requieren atribución y no deben usarse para tráfico intensivo ni para descargas masivas. Este mock es una demostración académica, pero **si se publicara en internet o se usara con mucho tráfico habría que cambiar de proveedor** (un servicio de teselas con licencia o un servidor propio). **A verificar por quien implemente:** los términos vigentes en https://operations.osmfoundation.org/policies/tiles/ antes de compartirlo públicamente.

Requiere **conexión a internet** para ver el mapa. Si las teselas no cargan, el resto de la interfaz debe seguir funcionando y mostrar un mensaje claro (RNF-06).

## 3. Mapa

- Centro: `[-34.5865, -58.4235]`, zoom inicial 15; zoom mínimo 13 y máximo 18; `maxBounds` ampliado alrededor de Palermo (ver `zona.limites_aprox`) con cierta holgura, para que el mapa no se vaya de CABA.
- **Coordenadas aproximadas:** las del `seed-data.json` pueden caer en lugares poco plausibles. **A verificar por quien implemente:** abrir el mapa, comprobar que cada marcador cae sobre una calle o plaza razonable y corregir. Una forma rápida: habilitar un modo de depuración que muestre en consola las coordenadas del clic (`map.on('click', e => console.log(e.latlng))`) y reajustar.
- **Capas:** un `L.layerGroup` por capa (cortes, ciclovías, subte, favoritos, reportes, eventos). Alternar con `map.addLayer` / `map.removeLayer`.
- **Marcadores:** `L.marker` con `L.divIcon` (HTML/SVG propio) para evitar depender de las imágenes por defecto de Leaflet. Líneas con `L.polyline`.
- **Estaciones y línea D:** el trazado exacto y los nombres **deben verificarse** (ver `02-datos-ficticios.md`). Si no se confirma, rotular «línea de ejemplo».
- **Geocodificación:** **solo con datos locales.** El buscador filtra por texto reportes, eventos, lugares y favoritos; no consume Nominatim ni ningún servicio externo (evita problemas de política de uso, de privacidad y de latencia).
- **Ruta (opcional):** línea guionada entre dos puntos locales y tiempo ficticio; no usar servicios de ruteo reales.

## 4. Estado y persistencia

- Estado en memoria en un objeto único `state` (reportes propios, votos, capas activas, pestaña, tema, estado del asistente).
- `localStorage` es opcional y solo para conveniencias (tema, capas visibles). **Envolver cada lectura y escritura en `try/catch`** y hacer que la página funcione sin él (puede fallar en ventanas privadas o con almacenamiento bloqueado).
- Los reportes creados por la persona que usa el mock **no se envían a ningún lado**.

## 5. Tiempo

- Calcular `ahora = Date.now()` al cargar; derivar `creadoEn = ahora - hace_min * 60000`.
- Formato relativo en español: «hace 12 min», «hace 3 h», «ayer», «en 2 h», «mañana».
- Para probar el asistente a distintas horas, permitir un parámetro de URL `?hora=08:00` (solo para pruebas) que desplace `ahora`.

## 6. Pruebas manuales (checklist)

**Carga**
- [ ] Abre con doble clic; sin errores en la consola.
- [ ] El mapa aparece centrado en Palermo con atribución OSM.
- [ ] El cartel «Prototipo conceptual, datos ficticios» se ve en escritorio y en teléfono.
- [ ] Sin conexión a internet: mensaje claro y resto de la interfaz utilizable.

**Capas y consulta**
- [ ] Cada capa se activa y desactiva desde el desglose y desde los chips.
- [ ] Cada marcador abre una ficha con título, estado y tiempo relativo.
- [ ] El buscador encuentra «escuela», «feria» y «bache» y centra el mapa.

**Reportar y seguir**
- [ ] Reporte completo en ≤ 4 pasos; sin pedir datos personales.
- [ ] «Enviar» deshabilitado hasta tener categoría y ubicación.
- [ ] Aparece en «Mis reportes» como «Recibido» y avanza con mensaje de próximo paso.
- [ ] **No aparece nunca el texto «En validación»** (buscar con Ctrl+F).

**Validación colaborativa**
- [ ] En `r04`, votar «Sigue vigente» y usar «Simular confirmación de otra persona» (RF-24 en `01-specs.md`) hasta llegar a 3 lo pasa a «Enviado al área responsable».
- [ ] No se puede votar dos veces en el mismo reporte.
- [ ] `r14` se ve «Sin confirmar» y atenuado.

**Mi hogar y asistente**
- [ ] ≥ 3 avisos ordenados por prioridad.
- [ ] «Ver recorrido a la escuela» resalta el corte `c01`.
- [ ] El asistente responde en ≤ 1 s, con cartel «Asistente simulado»; las respuestas rápidas son coherentes con los datos.

**Accesibilidad y adaptación**
- [ ] Todo operable con teclado; foco visible.
- [ ] Modo claro/oscuro con buen contraste; respeta `prefers-color-scheme`.
- [ ] 360 px de ancho: sin desbordes horizontales; hoja inferior funcional.
- [ ] `prefers-reduced-motion`: sin animaciones.

## 7. Qué NO hacer

- No usar escudo, logo, nombre ni colores oficiales del Gobierno; no escribir «oficial» en la interfaz.
- No consumir APIs reales (ni de IA, ni de ruteo, ni de geocodificación, ni de datos del Gobierno).
- No usar marcas ni comercios reales en los eventos.
- No pedir ni almacenar datos personales.
- No mostrar «En validación».
- No ocultar ni acortar la atribución de OpenStreetMap.
- No agregar dependencias que obliguen a un paso de compilación.
- No tratar como ciertos los datos marcados «a verificar».

## 8. Referencias

- Leaflet: https://leafletjs.com/ (documentación y descarga de la versión 1.9.4).
- Política de teselas de OpenStreetMap: https://operations.osmfoundation.org/policies/tiles/
- Derechos de autor y atribución de OpenStreetMap: https://www.openstreetmap.org/copyright
- Pautas de accesibilidad WCAG 2.1 (contraste, foco, teclado): https://www.w3.org/TR/WCAG21/
- Patrón de pestañas accesibles (WAI-ARIA Authoring Practices): https://www.w3.org/WAI/ARIA/apg/patterns/tabs/
- Capturas de la interfaz oficial como referencia de estructura: `refs/`.

> **Nota sobre las URLs:** son referencias habituales y **deben verificarse** al implementar, porque pueden cambiar.
