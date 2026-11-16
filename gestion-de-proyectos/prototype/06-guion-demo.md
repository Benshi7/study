# Guion de demostración (3 a 5 minutos)

Pensado para presentar el mock en la defensa del trabajo, alineado con el hilo del documento: **Canvas → Design Thinking → Charter → … → Riesgos**. El mock no reemplaza el documento: lo **ilustra**.

> Decir al inicio: «Es un prototipo conceptual con datos ficticios, hecho para mostrar posibles casos de uso».

## Preparación (antes de empezar)

- Abrir `mock/index.html` con internet; modo claro; ventana en pantalla completa.
- Comprobar que el mapa carga y que el cartel «Prototipo conceptual, datos ficticios» se ve.
- Tener a mano la pestaña «Mi hogar».

## Guion

| Min | Qué se muestra | Qué se dice | Conexión con el trabajo |
|---|---|---|---|
| 0:00 | Pantalla inicial: mapa de Palermo con capas | «Este es el mapa común: una sola capa geográfica con la información de varias áreas y un lugar para que los vecinos participen.» | **Canvas:** plataforma multilateral (hogares + áreas + socios) |
| 0:30 | Desglose de capas: activar/desactivar cortes, ciclovías, subte | «El vecino ve en un solo lugar lo que hoy está repartido entre canales.» | Propuesta de valor: capa común |
| 1:00 | Pestaña «Mi hogar»: tarjeta con avisos (corte cerca de la escuela, subte, ciclovía) | «Lucía, la persona del Design Thinking, tiene dos chicos en edad escolar. Esta mañana no tiene que buscar en cinco canales.» | **Design Thinking:** persona Lucía y el escenario de la mañana con información fragmentada |
| 1:30 | «Ver recorrido a la escuela» → resalta el corte | «El mapa le dice qué corte afecta su camino y qué alternativa tiene.» | Hallazgo: «información oficial cercana» |
| 2:00 | «Reportar una incidencia»: categoría → ubicación → enviar | «Reportar lleva tres pasos y no pide datos personales.» | Idea que pasa a prototipo: reportar |
| 2:30 | «Mis reportes»: estado «Recibido» → «Revisando que siga vigente» con próximo paso | «El test mostró que ‘En validación’ confundía: ahora el estado se explica con lenguaje claro y dice qué pasa después.» | **Test de Design Thinking:** ajuste propuesto en el estado «seguir» |
| 3:00 | Reporte ajeno: «Sigue vigente» y, desde «Controles de demostración», simular otras dos confirmaciones → «Enviado al área responsable» | «La comunidad confirma que el problema sigue ahí; con tres confirmaciones el reporte avanza.» | **Riesgos:** R07, reportes incorrectos o maliciosos → validación colaborativa |
| 3:30 | `r14` «Sin confirmar» | «Un reporte dudoso, sin confirmaciones, queda marcado y no desplaza a los reales.» | Riesgos R07 (reportes incorrectos o maliciosos) y R02 (baja calidad o desactualización de los datos) |
| 4:00 | «¿Qué tengo para hacer hoy?» | «Un asistente que resume el día. Acá es simulado: muestra qué podría hacer la plataforma con la capa común y los canales.» | Canales: asistente conversacional (integración sujeta a validación) |
| 4:30 | Eventos de marcas ficticias en el mapa | «Los socios con oferta geolocalizada serían una evolución futura; hoy están solo como ejemplo.» | **Canvas:** tercer lado opcional; fuera del alcance de esta versión |
| 5:00 | Cierre con el cartel fijo | «Todo esto es ficticio, pero responde a la pregunta de diseño: consultar, reportar y seguir sin necesitar saber qué área lo gestiona.» | Cierre: pregunta de diseño |

## Paso opcional (30 a 45 s): «Del lado del área»

Solo si la pantalla opcional está implementada (ver `01-specs.md`, §2.7) y hay tiempo. Se intercala **después de la validación colaborativa y de `r14` (3:30)** y antes del asistente; suma unos 45 segundos al guion (si hace falta compensar, omitir la fila de los eventos de marcas ficticias de las 4:30).

| Qué se muestra | Qué se dice | Conexión con el trabajo |
|---|---|---|
| «Capas» → enlace «Ver cómo llegan los datos»; se ve el diagrama *Fuentes → Capa común → Accesos* | «Lo que vio el vecino es la parte visible. Lo que sostiene el proyecto es la integración de las fuentes de cada área en una capa común. Los reportes la complementan, no la reemplazan.» | **Charter:** objetivo de integrar información de diferentes áreas y fuentes oficiales; **Canvas:** actividad clave «capa geográfica única» |
| Tarjeta de ciclovías «Con demora» → **Simular actualización** → volver al mapa: desaparece la etiqueta «Datos con demora» | «Cada área entrega sus datos con su propio ritmo y calidad. Si una fuente se atrasa, el vecino lo ve y no confía a ciegas.» | **Riesgos:** R01 (disponibilidad de APIs), R02 (calidad de datos) y R04 (coordinación entre áreas) |

Cierre sugerido del paso: «Esta pantalla es una maqueta: no es un panel real. Sirve para mostrar que el valor está en integrar, no solo en reportar».

## Si hay poco tiempo (3 minutos)

Mostrar solo: capas (0:30) → «Mi hogar» con corte (1:00) → reportar + seguimiento (1:00) → validación colaborativa (0:30).

## Posibles preguntas y respuestas

- **¿Es un sitio oficial?** No. Es un prototipo conceptual con datos ficticios; por eso no usa escudo ni identidad oficial.
- **¿El asistente usa IA?** No. Es un guion para mostrar el caso de uso; una versión real requeriría un diseño y validación propios (privacidad, calidad de respuestas).
- **¿El proyecto es solo un sistema para reportar?** No. Los reportes y la validación son un complemento colaborativo; la base es la capa geográfica común que integra información de las áreas y fuentes oficiales, y que luego se muestra en el mapa y en canales como Boti y BAX (integración sujeta a validación). La pantalla opcional «Del lado del área» lo ilustra.
- **¿De dónde salen los datos?** Son inventados. En el proyecto real provendrían de las áreas dueñas del dato mediante la capa común.
- **¿Qué pasa con los reportes falsos?** Se mitigan con validación colaborativa y moderación (ver matriz de riesgos).
- **¿Y si el mapa no carga?** Requiere internet; tener una captura de respaldo (ver `refs/` o guardar una propia).

## Plan B

Tener 3 capturas de pantalla del mock (mapa con capas, «Mi hogar», seguimiento de reporte) para mostrar si falla la conexión durante la defensa.
