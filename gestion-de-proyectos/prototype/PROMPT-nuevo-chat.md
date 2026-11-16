# Prompt para pegar en un chat nuevo

Copiar desde la línea de abajo y pegar en el chat nuevo (con la carpeta `prototype/` disponible para el agente).

---

Quiero que construyas un mock web de un solo archivo a partir de las especificaciones que están en la carpeta `prototype/` (en el directorio de trabajo). **No tenés contexto previo: leé primero la carpeta completa.**

**Qué leer, en este orden:** `prototype/README.md`, `00-contexto.md`, `01-specs.md`, `02-datos-ficticios.md` junto con `seed-data.json`, `03-asistente-simulado.md`, `04-diseno-ui.md`, `05-tecnica-referencias.md`, `06-guion-demo.md`, `07-ideas-extra.md` y las capturas de `prototype/refs/` (con `refs/README.md`).

**Qué construir:** un único archivo `prototype/mock/index.html` (HTML + CSS + JavaScript vanilla), con un mapa real de Palermo (Leaflet 1.9.4 desde unpkg y teselas de OpenStreetMap con atribución). Es un prototipo conceptual de un trabajo práctico académico con **datos ficticios**: reportes de vecinos, eventos de marcas ficticias, capas (cortes de tránsito, ciclovías, subte, favoritos, reportes vecinales y eventos), el flujo reportar → seguir (con estados en lenguaje claro: nunca «En validación»), validación colaborativa («Sigue vigente»), tarjeta «Mi hogar» y un botón «¿Qué tengo para hacer hoy?» que **simula** un asistente de IA con respuestas guionadas (sin API real).

**Enfoque importante:** el proyecto no es solo un «reportador de incidencias». Su base es una **capa geográfica común que integra información de las áreas del Gobierno** (cortes, ciclovías, subte, eventos); los reportes y la validación de vecinos son un complemento. Por eso el mock debe mostrar **también las capas oficiales integradas** de forma protagonista, no solo reportes. Hay además una **pantalla opcional «Del lado del área»** (`01-specs.md` §2.7, RF-41 a RF-49, CA-13 a CA-17; datos en la clave `fuentes` de `seed-data.json`): constrúyela **solo después** de cumplir todos los criterios de aceptación del MVP y si hay tiempo. Es una maqueta conceptual, no un panel real.

**Reglas innegociables:**
1. Cartel permanente «Prototipo conceptual, datos ficticios». Nombre visible: «Mapa de la Ciudad — prototipo».
2. No usar escudo, logo, colores ni identidad oficial del Gobierno de la Ciudad; no presentarlo como oficial.
3. Marcas y comercios inventados; sin datos personales; sin llamadas a APIs de IA, ruteo ni geocodificación.
4. Incrustar `seed-data.json` en el HTML; tiempos relativos calculados en el navegador.
5. Estilo sobrio blanco y rosa, modo claro y oscuro, accesible (teclado, foco, contraste ≥ 4,5:1, `aria-live`), responsive desde 360 px.
6. Todo lo marcado «a verificar» (coordenadas, línea D del subte, URLs, `integrity` de Leaflet, política de teselas) debe verificarse o dejarse rotulado como ficticio; no inventes certezas.

**Cómo trabajar:**
1. Antes de escribir código, devolveme un **plan breve** (≤ 15 líneas): estructura del archivo, orden de construcción y qué verificarás.
2. Construí en pasos pequeños y verificá cada uno en el navegador (abrí el archivo, revisá la consola, probá el flujo completo y el modo oscuro, y un ancho de 360 px).
3. Recorré la lista de pruebas de `05-tecnica-referencias.md` y los criterios de aceptación del `README.md`; informá cuáles pasan y cuáles no, **con evidencia** (capturas o salida de la consola).
4. Si algo de las specs es ambiguo, tomá la decisión más simple y anotala en un comentario al inicio del HTML; no me hagas más de una pregunta a la vez.
5. Entregá: la ruta del archivo, cómo abrirlo, qué ideas extra (si agregaste alguna) y qué quedó pendiente.

No agregues funciones fuera de las specs hasta cumplir los criterios de aceptación. La pantalla opcional «Del lado del área» sí está dentro de las specs, pero va después del MVP y debe informarse por separado (qué criterios CA-13 a CA-17 pasan).

---
