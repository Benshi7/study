# Especificaciones funcionales

Prototipo de un solo archivo (`mock/index.html`). Todo ocurre en el navegador; no hay servidor ni cuentas reales. Los datos salen de `seed-data.json` (incrustado en el HTML) y los cambios del usuario viven **solo en memoria** (opcionalmente en `localStorage` envuelto en `try/catch`).

## 1. Pantallas y estructura

Una sola página con cuatro zonas (ver `04-diseno-ui.md` para el detalle visual):

1. **Barra superior:** nombre «Mapa de la Ciudad — prototipo», buscador «Direcciones o lugares», botón de modo claro/oscuro y cartel permanente «Prototipo conceptual, datos ficticios».
2. **Barra lateral de iconos** (como en el mapa oficial): Explorar (zona), Favoritos, Capas, Reportes, Mi hogar, Asistente.
3. **Panel lateral:** contenido de la pestaña activa (listas, formularios, tarjetas).
4. **Mapa** (Leaflet, teselas OpenStreetMap) con marcadores, líneas y controles abajo a la derecha: ver/ocultar capas (desglose), regla (medir distancia, opcional) y «Mi ubicación» (ficticia: lleva a «Mi hogar»).

En pantallas angostas (< 768 px) el panel pasa a una **hoja inferior** (bottom sheet) sobre el mapa y la barra lateral se vuelve una barra inferior de iconos.

## 2. Pestañas del panel

### 2.1 Explorar (consultar la zona)
- Filtros rápidos tipo chips: **Todo · Cortes · Ciclovías · Subte · Eventos · Reportes**.
- Lista «Cerca de mí» ordenada por cercanía a «Mi hogar» (o al centro del mapa si no hay hogar), con icono, título, distancia aproximada y estado.
- Al tocar un ítem: el mapa se centra, se abre su ficha (popup + detalle en el panel).

### 2.2 Capas (desglose)
Lista de capas con interruptor, como el desglose del mapa oficial (ver `refs/mapa-oficial-capas.png`):

| Capa | Icono sugerido | Contenido | Activa por defecto |
|---|---|---|---|
| Cortes de tránsito | cono | líneas rojas + ficha | Sí |
| Red de ciclovías | bicicleta | líneas verdes/azules | Sí |
| Estado del subte (metro) | subte | estaciones línea D + estado | Sí |
| Favoritos | estrella | Casa, Escuela, Plaza | Sí |
| Reportes vecinales | megáfono | marcadores por estado | Sí |
| Eventos | calendario | marcadores con hora | Sí |

### 2.3 Reportes (reportar y seguir)
- **Botón principal «Reportar una incidencia»** (visible en el panel y como botón flotante en el mapa).
- **Flujo en 3 pasos** (RF-10 a RF-14): ¿Qué ocurre? → ¿Dónde? → Revisar y enviar. Sin datos personales.
- **«Mis reportes»:** lista con estado actual, línea de tiempo y próximo paso (RF-15 a RF-18).
- **Reportes cerca:** los de otras personas, con botón **«Sigue vigente»** y **«Ya no está»** (RF-20 a RF-23).

### 2.4 Mi hogar
Tarjeta de perfil del hogar (ficticio) con:
- Nombre del hogar, dirección ficticia, lugares frecuentes (escuela, plaza, subte).
- **Avisos del día** (de `avisos_hogar`): corte cerca de la escuela, ciclovía, subte, avance de su reporte, evento cercano; ordenados por prioridad.
- Botón «Ver recorrido a la escuela» (dibuja la línea casa→escuela y marca el corte que lo afecta).
- Botón «¿Qué tengo para hacer hoy?» (abre el asistente).

### 2.5 Asistente (simulado)
Ver `03-asistente-simulado.md`. Siempre con el cartel **«Asistente simulado: las respuestas son guionadas y no usan inteligencia artificial real»**.

### 2.6 Ruta (opcional)
Como el panel de ruta oficial (`refs/mapa-oficial-ruta.png`): selector de modo (a pie, bicicleta, transporte, auto), campos A y B, botón «Calcular». **No calcula rutas reales**: dibuja una línea guionada entre A y B (puntos de `hogar` y `lugares`) y muestra una duración ficticia según el modo, avisando si cruza un corte. Marcarlo como «estimación ficticia».

### 2.7 Del lado del área (opcional, «si hay tiempo»)

> **Opcional.** No bloquea el MVP ni los criterios del `README.md`: se implementa solo cuando todo lo anterior esté terminado y verificado. Si no se implementa, el mock sigue siendo válido.

**Para qué sirve.** El flujo del vecino (consultar, reportar, seguir) es la parte visible, pero el proyecto se apoya en la **integración de información de las áreas** en una capa geográfica común. Esta vista muestra, de forma simple, cómo llegan esos datos al mapa, para que el mock no se lea como un simple «reportador».

**Qué es y qué no es.** Es una **maqueta conceptual** con datos ficticios (`fuentes` en `seed-data.json`). **No es un panel real del Gobierno de la Ciudad**, no se conecta a ninguna fuente y no representa su funcionamiento interno. Debe rotularse así dentro de la propia vista.

**Contenido:**
- Un **enlace discreto «Ver cómo llegan los datos»** (al pie de la pestaña «Capas»; ver `04-diseno-ui.md`, §7) que abre la vista dentro del panel, con botón «Volver al mapa».
- Un **diagrama simple** *Fuentes → Capa común → Accesos*, con los accesos **Mapa** (este prototipo), **Boti** y **BAX**. Boti y BAX se rotulan «ilustrativo, sujeto a validación»: el mock no los integra.
- Una **tarjeta por fuente** (de `fuentes`) con: área (ficticia), capa que alimenta, cantidad de registros, calidad de datos (% de campos completos), estado de sincronización («Actualizado hace X min», «Con demora» o «Sin conexión») y la acción «Simular actualización».

```
 FUENTES (áreas, ficticias)      CAPA COMÚN                 ACCESOS
 Movilidad ......... cortes ─┐
 Transporte ........ subte ──┤   ┌──────────────────┐     ┌─ Mapa (este prototipo)
 Espacio Público ... ciclovías┼─▶│ Capa geográfica  │────▶┼─ Boti  (ilustrativo)
 Cultura ........... eventos ┤   │ común + control  │     └─ BAX   (ilustrativo)
 Participación vecinal ──────┘   │ de calidad       │
   reportes validados            └──────────────────┘
   (complemento colaborativo)
```

## 3. Estados de un reporte

Ver tabla de equivalencias en `00-contexto.md`. Los textos visibles son: **Recibido**, **Revisando que siga vigente**, **Enviado al área responsable**, **Resuelto**. **Nunca** mostrar «En validación».

Diagrama:

```
Recibido → Revisando que siga vigente → Enviado al área responsable → Resuelto
              ↑ (confirmaciones de la comunidad)
```

Reglas de la simulación:
- Un reporte nuevo nace en **Recibido**.
- A los 5 segundos (configurable) pasa a **Revisando que siga vigente** y aparece el mensaje con el próximo paso.
- Cuando alcanza **3 confirmaciones** («Sigue vigente»), pasa a **Enviado al área responsable** y muestra el área (ficticia) que lo toma.
- Botón de demo «Avanzar estado» (visible solo en un panel «Controles de demostración» plegable) lleva a **Resuelto**.
- Un reporte con **3 o más «Ya no está»** y 0 confirmaciones se rotula **«Sin confirmar»** y se atenúa en el mapa (caso del reporte `r14`).

## 4. Requisitos funcionales

### Mapa y capas
- **RF-01** Mostrar un mapa real centrado en Palermo (`zona.centro`, zoom 15) con atribución de OpenStreetMap visible.
- **RF-02** Mostrar el cartel «Prototipo conceptual, datos ficticios» de forma permanente (no cerrable).
- **RF-03** Dibujar las capas de `seed-data.json`: cortes (líneas), ciclovías (líneas), subte (estaciones), favoritos, reportes y eventos (marcadores).
- **RF-04** Permitir activar/desactivar cada capa desde el desglose y desde los chips; el estado se refleja en el mapa al instante.
- **RF-05** Mostrar un popup/ficha al tocar un elemento, con título, estado, hora relativa («hace 35 min», «en 2 h») y acciones disponibles.
- **RF-06** Buscador: filtra por texto los **datos locales** (reportes, eventos, lugares y favoritos) y centra el mapa; no usa servicios externos de geocodificación.
- **RF-07** Botones de zoom y «Mi ubicación» (lleva a «Mi hogar», sin geolocalización real).
- **RF-08** Chips de filtro que combinan con las capas.
- **RF-09** Tiempos relativos calculados con la hora del navegador al abrir (usar `hace_min` / `inicio_en_min`).

### Reportar y seguir
- **RF-10** Paso 1: elegir categoría entre `categorias_reporte` (botones grandes, máximo 10).
- **RF-11** Paso 2: marcar la ubicación en el mapa (clic/tap) con un marcador arrastrable; ofrecer «Usar mi hogar» y «Usar el centro del mapa».
- **RF-12** Paso 3: resumen y botón «Enviar reporte»; campo opcional de descripción (máx. 140 caracteres); texto visible: «No pedimos datos personales para reportar».
- **RF-13** Al enviar: confirmar con un mensaje claro y mostrar el reporte en «Mis reportes» con estado **Recibido**.
- **RF-14** Validar que haya categoría y ubicación antes de habilitar «Enviar reporte»; mensajes de error junto al campo.
- **RF-15** «Mis reportes»: lista con estado, antigüedad y área (cuando exista).
- **RF-16** Detalle del reporte con **línea de estados** (4 etapas) y el **próximo paso** del estado actual.
- **RF-17** Simulación del avance de estados (ver §3) con notificación en pantalla (toast) «Tu reporte pasó a: …».
- **RF-18** Estado vacío de «Mis reportes» con invitación a reportar.

### Validación colaborativa
- **RF-20** En reportes ajenos mostrar contador de confirmaciones y botones **«Sigue vigente»** y **«Ya no está»**.
- **RF-21** Cada persona vota una sola vez por reporte (se deshabilitan los botones y se muestra «Gracias, ya registramos tu respuesta»).
- **RF-22** Al llegar a 3 confirmaciones, el reporte pasa a «Enviado al área responsable».
- **RF-24** Panel plegable «Controles de demostración» con: «Simular confirmación de otra persona» (suma 1 confirmación al reporte seleccionado, para poder llegar al umbral de 3 sin que una misma persona vote varias veces), «Avanzar estado» y «Reiniciar demostración». Estos controles deben verse como herramientas de la demo, no como funciones del producto.
- **RF-23** Un reporte con ≥ 3 «Ya no está» se muestra como **«Sin confirmar»** y atenuado (ver `r14`). Explicar en la ficha: «Este reporte todavía no tiene confirmaciones de otras personas».

### Mi hogar y asistente
- **RF-30** Tarjeta «Mi hogar» con los avisos de `avisos_hogar` ordenados por `prioridad`.
- **RF-31** «Ver recorrido a la escuela» dibuja `hogar.recorrido_escuela` y resalta el corte `c01` si lo intersecta.
- **RF-32** Botón «¿Qué tengo para hacer hoy?» que muestra la respuesta guionada del asistente (ver `03-asistente-simulado.md`) con efecto de «escribiendo…» de 1 s como máximo.
- **RF-33** El asistente siempre muestra el cartel «Asistente simulado».
- **RF-34** Botones de respuesta rápida: «¿Hay cortes en mi recorrido?», «¿Qué eventos hay cerca?», «¿Cómo está el subte?».

### Ruta (opcional)
- **RF-40** Panel A/B con modo de transporte; línea guionada y tiempo ficticio con aviso de «estimación ficticia».

### Del lado del área (opcional, ver §2.7)
- **RF-41** Enlace discreto «Ver cómo llegan los datos» que abre la vista dentro del panel; botón «Volver al mapa» que restituye la pestaña anterior sin perder el estado (reportes, capas activas, mapa).
- **RF-42** Rótulo visible dentro de la vista: «Maqueta conceptual con datos ficticios: no es un panel real del Gobierno de la Ciudad». El cartel permanente (RF-02) sigue visible.
- **RF-43** Listar una tarjeta por cada elemento de `fuentes` con: área (ficticia), tipo (oficial o colaborativa), **capa que alimenta** y cantidad de **registros**.
- **RF-44** Mostrar la **calidad de datos** como porcentaje de campos completos (número + barra); el valor es ficticio y debe leerse sin depender del color.
- **RF-45** Mostrar el **estado de sincronización** con texto e icono (no solo color): «Actualizado hace X min», «Con demora (última actualización hace X)» o «Sin conexión (última conexión hace X)». El tiempo se calcula con `ultima_sync_hace_min` (RF-09).
- **RF-46** Mostrar el diagrama simple *Fuentes → Capa común → Accesos* (Mapa, Boti, BAX), con Boti y BAX rotulados «ilustrativo, sujeto a validación». Debe ser texto/SVG inline accesible (alternativa textual para lectores de pantalla).
- **RF-47** Botón **«Simular actualización»** por fuente (en la tarjeta; se considera herramienta de demostración): pone la fuente en «Actualizado hace 0 min» y aplica su `efecto_demo`. «Reiniciar demostración» (RF-24) restaura el estado inicial de las fuentes.
- **RF-48** **Reflejo en el mapa del vecino:** mientras una fuente esté «Con demora» o «Sin conexión», su capa muestra una etiqueta («Datos con demora» / «Sin conexión con la fuente») en el desglose de capas y en los popups de sus elementos; al simular la actualización, la etiqueta desaparece al instante sin recargar.
- **RF-49** Botón/enlace «Ver capa en el mapa» en cada tarjeta: activa la capa (si estaba apagada), vuelve al mapa y lo centra en la zona.

## 5. Requisitos no funcionales

- **RNF-01 Un solo archivo:** HTML + CSS + JS vanilla en `mock/index.html`; únicas dependencias externas: Leaflet 1.9.4 (unpkg) y teselas de OpenStreetMap.
- **RNF-02 Sin datos personales reales** ni credenciales; ninguna llamada a APIs de IA.
- **RNF-03 Accesibilidad:** contraste ≥ 4,5:1 en texto, foco visible, navegación por teclado, roles/aria en pestañas y botones, `aria-live="polite"` para toasts y respuestas del asistente, tamaño táctil ≥ 44 px, soporte de `prefers-reduced-motion` y `prefers-color-scheme`.
- **RNF-04 Responsive:** de 360 px de ancho a escritorio.
- **RNF-05 Rendimiento:** carga inicial < 2 s con conexión normal; ≤ 100 marcadores; sin librerías pesadas.
- **RNF-06 Robustez:** si las teselas no cargan, mostrar mensaje «No se pudo cargar el mapa. Revisá tu conexión» sin romper el resto.
- **RNF-07 Sobriedad:** estética seria (ver `04-diseno-ui.md`); sin emojis decorativos ni animaciones llamativas.
- **RNF-08 Idioma:** español, con tono claro y sin tecnicismos.

## 6. Criterios de aceptación detallados

| ID | Criterio | Cómo se prueba |
|---|---|---|
| CA-01 | El mapa carga centrado en Palermo y muestra atribución OSM | Abrir el archivo con internet |
| CA-02 | El cartel «Prototipo conceptual, datos ficticios» siempre visible, también en teléfono | Redimensionar la ventana |
| CA-03 | Crear un reporte en ≤ 4 clics/toques desde «Reportar» | Seguir el flujo |
| CA-04 | El reporte nuevo aparece como «Recibido» y luego avanza con mensaje de próximo paso | Esperar 5 s |
| CA-05 | Nunca aparece el texto «En validación» | Buscar en la página (Ctrl+F) |
| CA-06 | Votar «Sigue vigente» y sumar confirmaciones simuladas (RF-24) hasta 3 pasa el reporte ajeno a «Enviado al área responsable» | Probar con `r04` |
| CA-07 | `r14` aparece como «Sin confirmar» y atenuado | Ver el mapa y la ficha |
| CA-08 | «Mi hogar» muestra ≥ 3 avisos y el recorrido a la escuela resalta el corte `c01` | Abrir la pestaña |
| CA-09 | El asistente responde en ≤ 1 s con datos coherentes y el cartel «Asistente simulado» | Pulsar el botón |
| CA-10 | Modo claro y oscuro con contraste correcto | Alternar y revisar |
| CA-11 | Todo se puede usar con teclado | Navegar con Tab |
| CA-12 | Sin errores en la consola | Abrir DevTools |

Criterios de la vista opcional «Del lado del área» (**solo si se implementa**; no condicionan el cumplimiento de CA-01 a CA-12):

| ID | Criterio | Cómo se prueba |
|---|---|---|
| CA-13 | Desde «Capas» el enlace «Ver cómo llegan los datos» abre la vista y «Volver al mapa» regresa sin perder reportes ni capas activas | Crear un reporte, abrir la vista, volver y revisar «Mis reportes» |
| CA-14 | La vista muestra 5 fuentes con los tres textos de estado («Actualizado hace X min», «Con demora», «Sin conexión»), registros, calidad (%) y capa que alimenta | Abrir la vista y comparar con `fuentes` |
| CA-15 | «Simular actualización» sobre la fuente de ciclovías (`f03`) o de eventos (`f04`) cambia su estado a «Actualizado hace 0 min» y **desaparece la etiqueta** correspondiente en el mapa del vecino | Pulsar el botón y mirar el desglose de capas y un popup de ciclovía o evento |
| CA-16 | El diagrama *Fuentes → Capa común → Accesos* se ve completo, con Boti y BAX rotulados «ilustrativo, sujeto a validación» | Revisar la vista |
| CA-17 | La vista muestra el rótulo «maqueta conceptual… no es un panel real» y el cartel permanente sigue visible; funciona con teclado, en modo claro y oscuro y en 360 px | Probar los tres casos |
