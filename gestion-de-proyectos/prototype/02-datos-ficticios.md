# Datos ficticios

Todos los datos están en `seed-data.json` (en esta carpeta). El HTML debe **incrustarlos** (pegar el JSON dentro de un `<script type="application/json" id="seed">`), de modo que el mock siga siendo un solo archivo.

> **Aviso.** Nada de esto representa incidencias, eventos, marcas, personas ni direcciones reales. Las coordenadas son **aproximadas** (±300 m) y **deben verificarse por quien implemente** mirando el mapa real: ajustar los puntos para que caigan sobre calles o plazas plausibles de Palermo. Los nombres de calles reales no se usan en los textos; los lugares se llaman «ficticios».

## Convenciones

- **Tiempo relativo:** `hace_min` (minutos desde el momento de crear el reporte hasta ahora), `inicio_en_min` (minutos hasta el inicio de un evento; negativo = ya empezó), `fin_en_min`, `actualizado_hace_min`. El cliente calcula `ahora - hace_min` al abrir. **No usar fechas absolutas.**
- **Coordenadas:** `[latitud, longitud]` (orden de Leaflet).
- **Seudónimos:** `vecina_12`, `vecino_08`, etc. Son genéricos; no corresponden a personas reales.
- **Estados** (id → texto visible): `recibido` → Recibido; `revisando` → Revisando que siga vigente; `derivado` → Enviado al área responsable; `resuelto` → Resuelto. Ver tabla en `00-contexto.md`.

## Estructura del JSON

| Clave | Contenido |
|---|---|
| `zona` | Nombre, centro `[-34.5865, -58.4235]`, zoom 15, límites aproximados y puntos de referencia (Plaza Italia, plaza de Palermo Soho, Bosques) |
| `persona` | Lucía F. (ficticia) |
| `hogar` | Dirección ficticia, coordenadas, lugares (escuela, plaza, subte) y `recorrido_escuela` (polilínea) |
| `favoritos` | Casa, Escuela, Plaza |
| `categorias_reporte` | 10 categorías con id y nombre |
| `estados_reporte` | 4 estados con texto visible y `proximo_paso` |
| `areas_ficticias` | Áreas que reciben reportes (nombres genéricos) |
| `reportes` | 14 reportes de vecinos (ver tabla) |
| `eventos` | 7 eventos con marcas ficticias |
| `cortes_transito` | 3 cortes (polilíneas) |
| `ciclovias` | 3 tramos (polilíneas) |
| `subte` | Línea D, 3 estaciones, estado y mensaje |
| `avisos_hogar` | 5 avisos para «Mi hogar» con prioridad y referencia a otros elementos |
| `fuentes` | **Opcional.** 5 fuentes ficticias de datos para la vista «Del lado del área» (ver sección más abajo) |
| `cartel_permanente` | Texto del cartel fijo |

## Reportes de ejemplo (14)

| Id | Categoría | Estado | Confirmaciones | Observación |
|---|---|---|---|---|
| r01 | Obstrucción en la vía | Enviado al área responsable | 7 | **Es el reporte propio de Lucía** (`mio: true`), frente a la escuela; sirve para mostrar el seguimiento |
| r02 | Bache | Enviado | 12 | |
| r03 | Luminaria apagada | Revisando | 2 | Con 1 confirmación más pasa a «Enviado al área responsable» |
| r04 | Árbol o ramas caídas | Recibido | 1 | Ideal para probar el umbral de 3 confirmaciones (regla: los reportes en Recibido o Revisando tienen menos de 3) |
| r05 | Semáforo | Enviado | 9 | |
| r06 | Residuos | Revisando | 2 | |
| r07 | Vereda rota | Enviado | 15 | |
| r08 | Pérdida de agua | Resuelto | 11 | Para mostrar un caso cerrado |
| r09 | Ciclovía obstruida | Recibido | 0 | Coincide con la ciclovía `b03` |
| r10 | Señalización | Enviado | 6 | |
| r11 | Bache | Revisando | 2 | |
| r12 | Luminaria | Resuelto | 5 | |
| r13 | Obstrucción | Recibido | 1 | |
| r14 | Obstrucción (dudoso) | Revisando | 0 + 3 «ya no está» | **Caso de reporte incorrecto o malicioso**; se muestra «Sin confirmar» (ver RF-23) |

## Eventos de ejemplo (7)

Todos con anfitriones **ficticios** (marcas inventadas: «Café Brisa Norte», «Librería Tinta Fresca», «Estudio Vuelo», «Manzana Verde», «Rueda Libre Bicicletería», «Cine Club Medianoche», «Raíz Cercana»). Si se agregan más, **verificar que el nombre no coincida con un comercio real conocido** y rotular «ficticio». Costos: «Gratis» o «Con inscripción». El evento `e04` (feria) ya empezó y está relacionado con el corte `c02`; el evento `e01` empieza en 150 minutos y es el protagonista de la respuesta del asistente.

## Cortes, ciclovías, subte y avisos

- **Cortes:** `c01` (obra, cerca de la escuela, impacto alto, con alternativa), `c02` (evento en la calle), `c03` (un carril por bacheo).
- **Ciclovías:** `b01` troncal, `b02` parque, `b03` transversal con obstrucción.
- **Subte:** línea D con estado «demoras» y un mensaje. **A verificar:** nombres y orden de estaciones, y que la línea D efectivamente pase por esa zona; si no se puede confirmar, rotular la línea como «línea de ejemplo».
- **Avisos del hogar:** `a01` corte cerca de la escuela (prioridad 1), `a03` subte (2), `a04` avance del reporte propio (2), `a02` ciclovía (3), `a05` evento (4).

## Fuentes de datos (opcional: vista «Del lado del área»)

La clave `fuentes` alimenta la pantalla opcional descrita en `01-specs.md` (§2.7, RF-41 a RF-49). **No se usa en el resto del mock**: si la pantalla no se implementa, se puede ignorar sin afectar nada.

Cada fuente representa a un área que «entrega» datos a la capa común. Son 5, todas ficticias:

| Id | Área (ficticia) | Tipo | Capa que alimenta | Registros | Última sincronización | Estado | Calidad |
|---|---|---|---|---|---|---|---|
| f01 | Área de Movilidad | oficial | Cortes de tránsito (`cortes_transito`) | 42 | hace 4 min | Actualizado | 94 % |
| f02 | Área de Transporte | oficial | Estado del subte (`subte`) | 16 | hace 8 min | Actualizado | 97 % |
| f03 | Área de Espacio Público | oficial | Red de ciclovías (`ciclovias`) | 57 | hace 190 min | **Con demora** | 82 % |
| f04 | Área de Cultura | oficial | Eventos (`eventos`) | 31 | hace 1500 min | **Sin conexión** | 71 % |
| f05 | Participación vecinal | colaborativa | Reportes vecinales (`reportes`) | 14 | hace 1 min | Actualizado | 89 % |

Campos de cada fuente: `id`, `area`, `tipo` (`oficial` o `colaborativa`), `capa` (clave de la capa en este mismo JSON), `capa_nombre`, `registros` (total ficticio de la fuente), `registros_en_zona` (los que realmente dibuja el mock en Palermo; coincide con la cantidad de elementos del JSON), `ultima_sync_hace_min` (misma convención de tiempo relativo), `estado`, `calidad` y `efecto_demo` (qué debe cambiar en el mapa del vecino al pulsar «Simular actualización»).

Reglas:

- **Estado** (id → texto visible): `actualizado` → «Actualizado hace X min»; `con_demora` → «Con demora»; `sin_conexion` → «Sin conexión». Regla orientativa para que el estado sea coherente con el tiempo: hasta 60 min = actualizado; más de 60 min con la fuente respondiendo = con demora; sin respuesta = sin conexión.
- **Calidad** = porcentaje ficticio de **campos completos** en los registros de la fuente (0–100). Es solo una cifra ilustrativa; en el proyecto real el control de calidad se definiría con cada área.
- Los nombres de área son **genéricos y rotulados como ficticios**; no representan a ningún organismo real ni sus cifras. No sustituyen a `areas_ficticias` (que son las que reciben reportes).
- Los reportes vecinales (`f05`) figuran como fuente **colaborativa** para mostrar que complementan, y no reemplazan, a las fuentes oficiales.
- Las cifras (registros, minutos, porcentajes) son inventadas; **no** presentarlas como mediciones.

## Reglas para ampliar los datos

1. Mantener los textos cortos (≤ 140 caracteres) y neutrales; sin acusaciones ni datos de personas.
2. No incluir fotos de personas, patentes ni números de teléfono.
3. Cada reporte necesita: `id`, `categoria`, `titulo`, `coord`, `estado`, `hace_min`, `confirmaciones`, `usuario`.
4. No mencionar organismos reales como responsables de resolver; usar `areas_ficticias`.
5. Si se agregan marcas o comercios, deben ser inventados y rotulados como ficticios.
