# Diseño de la interfaz

Objetivo: una interfaz **sobria, clara y accesible**, inspirada en la **estructura** de un mapa institucional (barra superior con buscador, barra lateral de iconos, panel de contenido, mapa a pantalla completa, controles abajo a la derecha), **sin imitar la identidad oficial**: no usar escudo, logo, tipografía ni la paleta amarilla/gris del sitio oficial. La identidad visual es la de la universidad del trabajo: **blanco y rosa**, con modo claro y oscuro.

Referencias de estructura: `refs/mapa-oficial-ruta.png` (panel de ruta) y `refs/mapa-oficial-capas.png` (desglose de capas). Ver `refs/README.md`.

## 1. Estructura

```
┌───────────────────────────────────────────────────────────────────────────┐
│ Mapa de la Ciudad — prototipo │ [ Direcciones o lugares      🔍 ] │ ☾/☀ │  ← barra superior
├────┬───────────────┬──────────────────────────────────────────────────────┤
│ ⌖  │ Panel          │                                                      │
│ ☆  │  (pestaña      │                  MAPA                                │
│ ≡  │   activa)      │                                                      │
│ 📣 │                │                                  [capas][regla][⌖]   │  ← controles
│ 🏠 │                │                                                      │
│ ✦  │                │  Prototipo conceptual, datos ficticios               │  ← cartel fijo
└────┴───────────────┴──────────────────────────────────────────────────────┘
```

(Los iconos de la ilustración son orientativos: usar SVG propios, no emojis.)

- **Barra superior (altura 56 px):** título a la izquierda; buscador al centro (campo con botón de lupa, como el oficial); a la derecha, interruptor claro/oscuro. Fondo blanco (claro) o gris muy oscuro (oscuro), con una línea inferior rosa de 3 px.
- **Barra lateral (ancho 64 px):** iconos con etiqueta; el activo con fondo rosa suave y borde izquierdo rosa. Orden: Explorar, Favoritos, Capas, Reportes, Mi hogar, Asistente.
- **Panel (ancho 360 px en escritorio):** scroll interno; encabezado con el título de la pestaña; contenido en tarjetas.
- **Mapa:** ocupa el resto; atribución de OpenStreetMap abajo a la derecha (Leaflet la agrega; no ocultarla).
- **Controles del mapa (abajo a la derecha):** tres botones: **ver/ocultar capas** (abre el desglose), **regla** (opcional) y **mi ubicación**. El desglose se abre como un menú sobre el botón, con ítems de icono + nombre + interruptor, separador y «Favoritos», igual que en la captura de referencia.
- **Cartel fijo:** etiqueta pequeña abajo a la izquierda del mapa: «Prototipo conceptual, datos ficticios». En teléfono, también en la barra superior (abreviado: «Prototipo · datos ficticios»). No se puede cerrar.
- **Móvil (< 768 px):** el panel pasa a **hoja inferior** deslizable (alturas: 20 %, 50 %, 90 %); la barra lateral se convierte en barra inferior de 5 iconos; el buscador ocupa el ancho; el desglose de capas se abre como hoja.

## 2. Paleta

Basada en los tokens del documento del trabajo (azul de encabezados, grises, verde y rojo de estado) con el **rosa universitario** como acento. Valores **propuestos** (contraste verificado con la fórmula WCAG 2.1; revisar si se cambian).

### Modo claro

| Token | Valor | Uso | Contraste |
|---|---|---|---|
| `--bg` | `#FFFFFF` | fondo de barras y panel | — |
| `--bg-soft` | `#FDF1F7` | fondo de tarjetas/activos | — |
| `--text` | `#1F1F24` | texto | 16,4:1 sobre blanco |
| `--muted` | `#5F6670` | texto secundario | 5,8:1 sobre blanco |
| `--accent` | `#A3216E` | rosa de marca (botones, activos, enlaces) | 7,0:1 sobre blanco |
| `--accent-contrast` | `#FFFFFF` | texto sobre `--accent` | 7,0:1 |
| `--accent-soft` | `#FDF1F7` | fondo de selección | texto `--accent` 6,4:1 |
| `--rule` | `#E3D3DC` | bordes | decorativo |
| `--ok` | `#2E7D4F` | resuelto, habilitada | 5,1:1 sobre blanco |
| `--warn` | `#8A6100` | demoras, atención | 5,5:1 |
| `--danger` | `#B3402E` | cortes, urgente | 5,7:1 |
| `--info` | `#1F5FA8` | informativo, enlaces secundarios | 6,4:1 |

### Modo oscuro

| Token | Valor | Uso | Contraste |
|---|---|---|---|
| `--bg` | `#17161B` | fondo | — |
| `--bg-soft` | `#22202A` | tarjetas | — |
| `--text` | `#ECECF1` | texto | 15,3:1 |
| `--muted` | `#A9A9B5` | secundario | 7,7:1 |
| `--accent` | `#FF8CC6` | rosa de marca | 8,4:1 sobre `--bg` |
| `--accent-contrast` | `#17161B` | texto sobre `--accent` | 8,4:1 |
| `--rule` | `#3A3745` | bordes | decorativo |
| `--ok`/`--warn`/`--danger`/`--info` | tonos más claros de los de modo claro (**a verificar**: ≥ 4,5:1 sobre `--bg`) | estados | |

Implementar con variables CSS en `:root`, `@media (prefers-color-scheme: dark)` y el atributo `[data-theme]` para el interruptor manual. El mapa en modo oscuro: aplicar un filtro CSS suave a las teselas (`filter: invert(0.92) hue-rotate(180deg) brightness(0.9) contrast(0.9)`) **solo a la capa de teselas**, no a los marcadores; **a verificar** visualmente.

Nota sobre los tokens del documento del trabajo (para referencia): texto `#222222`, secundario `#5F6670`, azul de encabezados `#1F3A5F`, verde `#2E7D4F`, rojo `#B3402E`. El rosa final de la universidad puede ajustarse; mantener **un solo token** (`--accent`) para cambiarlo fácilmente.

## 3. Tipografía

- Pila de sistema: `system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif` (sin fuentes externas, para mantener un solo archivo y funcionar sin conexión de fuentes).
- Tamaños: base 16 px; títulos de panel 20 px/600; subtítulos 16 px/600; texto secundario 14 px; etiquetas 12 px (mínimo).
- Interlineado 1,45; ancho de línea ≤ 70 caracteres en tarjetas de texto.

## 4. Componentes

| Componente | Descripción |
|---|---|
| **Botón primario** | Fondo `--accent`, texto `--accent-contrast`, radio 8 px, alto ≥ 44 px, foco con anillo de 3 px |
| **Botón secundario** | Borde `--accent`, texto `--accent`, fondo transparente |
| **Chip de filtro** | Píldora con borde; activo con fondo `--accent-soft` y borde `--accent` |
| **Tarjeta** | Fondo `--bg-soft`, borde `--rule`, radio 12 px, sombra mínima |
| **Marcador de reporte** | Círculo de 28 px con icono de categoría; **color por estado** (Recibido: gris; Revisando: ámbar; Enviado: azul; Resuelto: verde); «Sin confirmar»: gris atenuado con borde punteado. **No depender solo del color**: usar además forma o icono interno |
| **Marcador de evento** | Rombo con icono de calendario y hora relativa |
| **Línea de corte** | Trazo rojo grueso discontinuo; etiqueta con icono de cono |
| **Ciclovía** | Trazo continuo verde azulado; con obstrucción: trazo punteado ámbar |
| **Estación de subte** | Círculo con letra «D» y estado |
| **Línea de estados** | 4 pasos horizontales con círculos conectados; el actual resaltado y los cumplidos con tilde; texto del próximo paso debajo |
| **Toast** | Aviso breve (4 s) abajo al centro, con `role="status"` |
| **Hoja inferior** | Handle visible, `aria-expanded`, cierra con arrastre o botón |
| **Cartel fijo** | Píldora con borde, texto 12–13 px, siempre sobre el mapa |

Iconos: SVG en línea, trazo de 1,75 px, esquinas redondeadas, consistentes. **No usar emojis como iconos** en la versión final.

## 5. Accesibilidad

- Estructura semántica: `header`, `nav`, `main`, `aside`; pestañas con `role="tablist"`/`tab`/`tabpanel` y teclas de flecha.
- Foco visible siempre; orden de tabulación lógico; atajo «Saltar al mapa».
- Todos los controles del mapa son botones reales con `aria-label`.
- Los marcadores tienen alternativa en lista (el panel «Cerca de mí» expone la misma información).
- Contraste ≥ 4,5:1 (texto) y ≥ 3:1 (iconos y bordes de controles).
- Toasts y respuestas del asistente con `aria-live="polite"`.
- Respeta `prefers-reduced-motion` (sin animaciones de desplazamiento ni «escribiendo…» animado) y `prefers-color-scheme`.
- Idioma `lang="es-AR"`.

## 6. Qué evitar

- Escudo, logo, tipografías o colores institucionales presentados como oficiales.
- Textos que insinúen que es un servicio real del Gobierno.
- Emojis decorativos, degradados llamativos, animaciones largas.
- Dependencias de fuentes o íconos externos (todo inline).

## 7. Vista opcional «Del lado del área» (si hay tiempo)

Pantalla opcional descrita en `01-specs.md` (§2.7, RF-41 a RF-49). **No agrega un ícono a la barra lateral** (se mantienen los 6 ítems / 5 en móvil) para no competir con el flujo del vecino.

**Acceso.** Enlace discreto, de texto secundario (`--muted`, subrayado al pasar el cursor, 14 px), **al pie de la pestaña «Capas»**: «Ver cómo llegan los datos». Debe ser un enlace real alcanzable con Tab. La vista se abre **dentro del panel** (en móvil, en la hoja inferior a 90 %), con encabezado «Del lado del área» y botón «← Volver al mapa» (foco inicial en el encabezado).

**Estructura (escritorio, panel de 360 px):**

```
┌─ Del lado del área ─────────────── [← Volver al mapa] ┐
│ Maqueta conceptual con datos ficticios: no es un      │
│ panel real del Gobierno de la Ciudad.                 │
│                                                       │
│  Fuentes  ──▶  Capa común  ──▶  Mapa                  │
│  (áreas)       (con control     Boti (ilustrativo)    │
│                 de calidad)     BAX  (ilustrativo)    │
│                                                       │
│ ┌ Área de Espacio Público (ficticia) ───────────────┐ │
│ │ Capa: Red de ciclovías · 57 registros             │ │
│ │ ⏱ Con demora · última actualización hace 3 h      │ │
│ │ Calidad ▓▓▓▓▓▓▓▓░░ 82 % de campos completos       │ │
│ │ [Ver capa en el mapa]   [Simular actualización]   │ │
│ └───────────────────────────────────────────────────┘ │
│ ┌ Área de Transporte (ficticia) ────────────────────┐ │
│ │ Capa: Estado del subte · 16 registros             │ │
│ │ ✓ Actualizado hace 8 min                          │ │
│ │ Calidad ▓▓▓▓▓▓▓▓▓░ 97 % de campos completos       │ │
│ └───────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────┘
```

(Iconos orientativos: usar SVG propios.)

**Componentes:**
- **Tarjeta de fuente:** misma tarjeta que el resto del panel (`--bg-soft`, borde `--rule`, radio 12 px). Título = área ficticia; etiqueta pequeña «Oficial» o «Colaborativa».
- **Estado de sincronización:** píldora con **icono + texto** (no solo color): tilde y `--ok` para «Actualizado hace X min»; reloj y `--warn` para «Con demora»; cruz o desconexión y `--danger` para «Sin conexión». Los textos se leen con `aria-live="polite"` cuando cambian.
- **Barra de calidad:** barra fina con el porcentaje escrito al lado («82 %»), `role="img"` con `aria-label` («Calidad de datos: 82 % de campos completos»).
- **Diagrama:** SVG inline o bloque de texto con tres columnas; con `<title>`/`aria-label` que lo describa. Los accesos Boti y BAX con borde punteado y el rótulo «ilustrativo».
- **«Simular actualización»:** botón secundario; debe verse como herramienta de demostración (rotulado «Demo» o con el mismo estilo que el panel «Controles de demostración»).

**Estados de la vista:**

| Estado | Qué se ve |
|---|---|
| Normal | Tarjetas con los estados iniciales de `fuentes` (dos «Actualizado» al menos, una «Con demora» y una «Sin conexión») |
| Tras «Simular actualización» | La tarjeta pasa a «Actualizado hace 0 min» y toast «Se actualizó: <capa>»; en el mapa del vecino desaparece la etiqueta «Datos con demora» o «Sin conexión con la fuente» |
| Reinicio de la demostración | Vuelven los estados iniciales |
| Sin `fuentes` en el JSON | No se muestra el enlace «Ver cómo llegan los datos» (la vista es opcional) |

**Reflejo en el mapa del vecino:** etiqueta pequeña («Datos con demora» en `--warn`, «Sin conexión con la fuente» en `--danger`) junto al nombre de la capa en el desglose y dentro de los popups de sus elementos. No se colorean los marcadores: se evita saturar el mapa.

**Móvil (360 px):** una tarjeta por fila, botones apilados de ≥ 44 px, diagrama en vertical (Fuentes ↓ Capa común ↓ Accesos).
