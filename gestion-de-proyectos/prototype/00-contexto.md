# Contexto del prototipo

## 1. De dónde sale

El mock forma parte de un **trabajo práctico académico** («Modernización del Mapa Interactivo de la Ciudad»), de un taller universitario de gestión de proyectos digitales. El trabajo plantea, con metodología en cascada, el proyecto de modernizar el mapa interactivo que ofrece el Gobierno de la Ciudad Autónoma de Buenos Aires (GCBA). Es un **ejercicio de simulación**: el proyecto, las entrevistas, los datos y las cifras son parte del caso académico, no información real.

El mock sirve para **mostrar posibles funciones y casos de uso** de la propuesta. No es el producto: es una demostración navegable.

## 2. Idea de la propuesta

Hoy la información sobre la Ciudad (obras, cortes, transporte, cultura, reclamos) está repartida en canales distintos, y quien quiere reportar algo debe saber de antemano qué área del Gobierno lo gestiona. La propuesta es una **plataforma multilateral** con una capa geográfica común:

- **Hogares de la Ciudad** (segmento principal): consultan información oficial cercana, reportan incidencias y siguen el estado de sus reportes.
- **Áreas del GCBA** (lado institucional): mantienen sus datos en la capa común y ven dónde se concentran los reclamos (vista de gestión).
- **Visitantes y turistas** (beneficiarios secundarios): consultan el mismo mapa sin necesidad de reportar.
- **Socios con oferta geolocalizada** (tercer lado, opcional y futuro): comercios o marcas que muestran eventos u ofertas dentro de un canal oficial. Esto es **evolución futura**; en el mock aparece solo como «Eventos» con marcas **ficticias**.

Canales previstos (ficticios en el mock): mapa web, asistente conversacional, aplicación personal del vecino y notificaciones.

## 3. Hallazgo de Design Thinking que debe reflejar el mock

En el test del prototipo de baja fidelidad, una persona dudó ante el estado **«En validación»**: preguntó «¿Quién confirma que el reporte sigue vigente?». Por eso el mock **no debe mostrar «En validación»**. Debe usar lenguaje claro y explicar el próximo paso. Equivalencias:

| Estado interno (conceptual) | Texto visible en el mock | Próximo paso que se muestra |
|---|---|---|
| Recibido | **Recibido** | «Lo estamos revisando. Te avisamos cuando alguien más confirme que sigue vigente.» |
| En validación | **Revisando que siga vigente** | «Otras personas de tu zona pueden confirmar si el problema sigue ahí.» |
| Derivado | **Enviado al área responsable** | «El área responsable ya tiene tu reporte. Te avisamos cuando lo tome.» |
| Resuelto | **Resuelto** | «El área marcó el problema como resuelto. Si sigue ahí, podés reabrirlo.» |

## 4. La persona: Lucía

- **Lucía F.**, 36 años, cuidadora. Responsable de un hogar de la Ciudad con **dos chicos en edad escolar**. Vive en CABA. (Persona ficticia.)
- **Lo que busca:** organizar recorridos y encontrar información confiable de su zona.
- **Lo que le cuesta:** canales separados; no sabe quién responde ni qué pasó con el reclamo.
- **Necesidad priorizada:** consultar información oficial cercana y seguir un reporte sin conocer de antemano qué área lo gestiona.
- **Historia de usuario:** «Como persona adulta responsable de un hogar de la Ciudad, quiero ver información oficial de mi zona y seguir mis reportes para organizar el día con mayor previsibilidad.»
- **Pregunta de diseño:** ¿Cómo podríamos facilitar que las personas consulten, reporten y sigan situaciones de su entorno sin necesitar conocer qué área del Gobierno las gestiona?

**Escenario original (una mañana con información fragmentada):** 07:30 organiza el recorrido a la escuela con sus dos hijos → 07:40 busca información de obras y cortes repartida entre canales → 07:50 encuentra un obstáculo y no sabe qué área lo gestiona ni dónde reportarlo → después envía el reclamo y no puede saber si sigue vigente ni quién lo tomó.

El mock debe mostrar **cómo sería esa mañana con la plataforma**.

## 5. Las 3 pantallas del prototipo de baja fidelidad

El prototipo conceptual del trabajo tiene tres pantallas con un mismo recorrido; el mock las implementa y las amplía:

1. **Consultar:** información oficial cercana, actualizada; acceso a «Reportar una incidencia».
2. **Reportar:** «¿Qué ocurre?» (categoría, p. ej. «Obstrucción en la vía»), ubicación (punto marcado en el mapa), botón «Enviar reporte». Nota del prototipo: **sin datos personales para reportar**.
3. **Seguir:** línea de estados de un reporte, desde el envío hasta el cierre: Recibido → (revisión) → Derivado → Resuelto.

Ideas del brainstorming que pasan al prototipo: **mapa común + reportar + validar + seguir el estado**. Otras ideas: «Cerca de mí» (filtros por zona), «Confirmar» (la comunidad indica si sigue vigente), «Gestionar» (vista para áreas, fuera del alcance del mock salvo una pantalla opcional, ver `07-ideas-extra.md`).

## 6. Restricciones

- **Todo es ficticio:** reportes, eventos, marcas, cortes, avisos y fechas. Rotularlo en pantalla.
- **No inventar datos reales sensibles:** nada de nombres de personas reales, teléfonos, correos ni direcciones domiciliarias reales. Los nombres de usuarios son seudónimos genéricos.
- **No imitar la identidad oficial:** sin escudo, logo, colores ni tipografía institucionales presentados como oficiales. El nombre es «Mapa de la Ciudad — prototipo».
- **Marcas y comercios ficticios:** no usar marcas reales en los eventos.
- **Fechas relativas:** los datos usan desfases relativos a «ahora» calculados en el navegador; no fijar fechas absolutas.
- **Sin datos personales:** el flujo de reporte no pide nombre, teléfono ni correo.
- **Sin IA real:** el asistente es un guion con reglas; no llama a ninguna API.
- **Zona:** Palermo (CABA), con foco en Plaza Italia, Palermo Soho y Bosques de Palermo. Coordenadas **aproximadas**, a verificar sobre el mapa.
- **Idioma:** español rioplatense neutro en la interfaz (se puede usar «vos» con moderación; ser consistente).
