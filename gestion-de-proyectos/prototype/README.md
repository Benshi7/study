# Prototipo «Mapa de la Ciudad — prototipo»

Carpeta de especificaciones para construir **un mock HTML de un solo archivo** de una plataforma ficticia de mapa interactivo para la Ciudad Autónoma de Buenos Aires (CABA). Está pensada para que un agente o una persona **sin contexto previo** pueda construirlo leyendo solo esta carpeta.

> **Importante.** Es un prototipo conceptual de un trabajo práctico académico. Todos los datos son ficticios. No usa el escudo, el logo ni la identidad oficial del Gobierno de la Ciudad, y no debe presentarse como un sitio oficial.

## Qué hay que construir

Un único archivo `prototype/mock/index.html` (HTML + CSS + JavaScript vanilla) que muestre, sobre un **mapa real de Palermo** (Leaflet + teselas de OpenStreetMap), los casos de uso de la plataforma:

1. **Consultar** información de la zona (cortes de tránsito, ciclovías, estado del subte, eventos, reportes de otros vecinos).
2. **Reportar** una incidencia en pocos pasos (ubicación + categoría).
3. **Seguir** el estado del reporte con lenguaje claro y el próximo paso explicado.
4. **Confirmar** que un reporte de otra persona sigue vigente (validación colaborativa).
5. **Mi hogar**: avisos relevantes para un hogar (corte cerca de la escuela, ciclovía, subte).
6. **¿Qué tengo para hacer hoy?**: un asistente **simulado** (respuestas guionadas, sin IA real ni API) que resume lo relevante del día.
7. **Del lado del área** (*opcional, «si hay tiempo»*): una vista que muestra cómo llegan los datos de las áreas a la capa común (fuentes → capa común → accesos), con estado de sincronización y calidad.

> **El mock no es solo un «reportador».** Debe mostrar también las **capas oficiales integradas** (cortes, ciclovías, subte, eventos) como parte central; los reportes de vecinos son un complemento colaborativo. La pantalla opcional del punto 7 refuerza esa idea.

## Índice de archivos

| Archivo | Contenido |
|---|---|
| `README.md` | Este índice, cómo correrlo y criterios de aceptación |
| `00-contexto.md` | Qué es el TP, la persona Lucía, las 3 pantallas de baja fidelidad y las restricciones |
| `01-specs.md` | Pantallas, componentes, interacciones, estados y requisitos (RF/RNF); la vista opcional «Del lado del área» está en §2.7 (RF-41 a RF-49, CA-13 a CA-17) |
| `02-datos-ficticios.md` | Reglas y descripción de los datos ficticios |
| `seed-data.json` | Datos ficticios listos para usar (reportes, eventos, cortes, ciclovías, subte, avisos y, para la vista opcional, `fuentes`) |
| `03-asistente-simulado.md` | Lógica guionada de «¿Qué tengo para hacer hoy?» |
| `04-diseno-ui.md` | Estructura de la interfaz, paleta, tipografía y componentes |
| `05-tecnica-referencias.md` | Stack, Leaflet, OpenStreetMap, checklist de pruebas, qué no hacer |
| `06-guion-demo.md` | Guion de demostración de 3 a 5 minutos |
| `07-ideas-extra.md` | Backlog opcional priorizado |
| `PROMPT-nuevo-chat.md` | Prompt listo para pegar en un chat nuevo |
| `refs/` | Capturas de la interfaz oficial como referencia de estructura (ver `refs/README.md`) |
| `mock/` | Carpeta de salida (el HTML va en `mock/index.html`) |

## Cómo correrlo

- Abrir `mock/index.html` con doble clic en un navegador moderno.
- **Requiere conexión a internet**: Leaflet se carga desde unpkg y las teselas desde OpenStreetMap.
- Si se prefiere servirlo localmente: `python3 -m http.server 8000` dentro de `prototype/mock/` y abrir `http://localhost:8000`.
- No hay compilación, instalación ni dependencias locales.

## Estructura

```
prototype/
├── README.md … 07-ideas-extra.md, PROMPT-nuevo-chat.md
├── seed-data.json          (fuente de los datos; el HTML debe incrustarlos)
├── refs/                   (capturas de referencia)
└── mock/
    └── index.html          (entregable: UN solo archivo)
```

## Criterios de aceptación (resumen)

El mock está terminado cuando:

- [ ] Abre con doble clic y muestra un mapa real de Palermo con marcadores ficticios.
- [ ] Hay un cartel **permanente** visible: «Prototipo conceptual, datos ficticios».
- [ ] No aparece ningún escudo, logo ni marca oficial; el título es «Mapa de la Ciudad — prototipo».
- [ ] Las capas se activan y desactivan desde un desglose (cortes, ciclovías, subte, favoritos, reportes vecinales, eventos).
- [ ] Se puede crear un reporte (categoría + ubicación marcada en el mapa) y verlo en «Mis reportes» con estado «Recibido» y el próximo paso explicado.
- [ ] El estado avanza (simulado) y usa lenguaje claro: **no** se usa «En validación» como texto visible.
- [ ] Se puede confirmar «Sigue vigente» en un reporte ajeno y el contador sube.
- [ ] La tarjeta «Mi hogar» muestra al menos 3 avisos (corte cerca de la escuela, ciclovía, subte).
- [ ] El botón «¿Qué tengo para hacer hoy?» muestra una respuesta guionada coherente con los datos y el cartel «asistente simulado».
- [ ] Funciona en modo claro y oscuro, en escritorio y en teléfono (≥ 360 px de ancho), con foco visible y teclado.
- [ ] Se superan los puntos de la lista de verificación de `05-tecnica-referencias.md`.

**Opcional (solo si se implementa; no condiciona lo anterior):**

- [ ] La vista «Del lado del área» abre desde un enlace discreto en «Capas», lista las fuentes ficticias con su estado, registros y calidad, muestra el diagrama fuentes → capa común → accesos y se rotula como maqueta (CA-13 a CA-17).
- [ ] «Simular actualización» hace desaparecer la etiqueta de datos con demora o sin conexión en el mapa del vecino.

## Datos no verificados

Varias cosas están marcadas como **«a verificar por quien implemente»** (coordenadas exactas, estaciones de la línea D, nombres de calles, política de teselas). No inventar certezas: si no se puede verificar, dejarlo como dato ficticio y rotularlo así.
