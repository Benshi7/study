# Para llevar al equipo: propuestas de mejora

> Los archivos originales de `trabajo-grupal/` **no se tocaron**. Esto es lo que proponemos, listo para discutir. Todo número nuevo es **propuesta**; lo desconocido está marcado **a confirmar**. Las fechas simuladas (01/04–30/09/2026, entrega 14/10) **se mantienen**: se agrega una línea que lo declara. **Quedan 2 días** (12/10 → 14/10): el plan está en `07-formato-entrega.md`.

## Qué dijeron los profesores y qué cambia

| Devolución | Qué hacemos |
|---|---|
| **Prof. Armando:** *«mejorar el orden de los puntos, el formato, prolijidad»* | Un solo documento con el orden de la consigna y una guía de estilo (problema 6). |
| **Prof. Pacheco:** *«se ven bien, todavía faltan varios puntos»; «en el presupuesto, dar más detalle de cómo construyen los números»* | Revisar contra los 10 puntos de la consigna (problema 6) y presupuesto desglosado en USD (problema 7). |

## Los 8 puntos y qué proponemos

| Problema | Propuesta | Leer | Esfuerzo | Decide |
|---|---|---|---|---|
| 1 · Gantt: ya tiene duraciones, dependencias y camino crítico; mejoras puntuales | **Corrección de nuestro análisis anterior:** el Excel ya trae todo eso (CPM de 126 d.h., 23 críticas, 8 hitos). Ajustes: la notación «a-b» es ambigua (126 vs 129 d.h.), 7 celdas de dependencias contradicen las fechas, la columna Responsable está vacía y el camino crítico cambia al corregirlas | `02-gantt/` | S | Quien armó el Gantt |
| 2 · Presupuesto sin trazabilidad | Mano de obra = personas × tarifa × duración del Gantt; contingencia = Σ EMV (USD 30.003, 14,1 % de costos, vs 10 % plano); reserva de gestión. En USD: escenario A USD 230.639 / B USD 266.868 | `03-presupuesto/`, `04-riesgos.md` | M–L | Todo el grupo (tarifas y personas) |
| 3 · Versiones que se contradicen | IDs maestros R01–R15 (+R16–R19); 8 gates; una nómina; eliminar la nota de chat y «Resumen y borrador» | `04-riesgos.md`, `06-coherencia.md` | S | Coordinador |
| 4 · Canvas, Design Thinking y SMART débiles | Opción B con segmento **«Hogares de la Ciudad»** (cada hogar con su realidad; los tipos de hogar son personas), dos propuestas de valor, 4 objetivos SMART y Design Thinking como **investigación simulada** rotulada, con tres proto-personas y copia revisada de las slides (`05b`) | `05-canvas-dt-smart.md` | M | Grupo (+ consulta a los profesores) |
| 5 · Charter muy largo (≈ 6.000 palabras) | **Charter en la plantilla de la cátedra** (24 campos en 3 partes), completo y conciso, con la aclaración del perfil de hogar básico; mapa de los 13 elementos de la Clase 3 a los 24 campos; el texto actual pasa a Anexo A | `01-charter/Project_Charter_completado.docx`, `01-charter/README.md`, `01-charter-condensado.md` | S–M | Grupo |
| 6 · Formato y prolijidad (pedido del Prof. Armando) | **Un solo documento** con los 10 puntos en el orden de la consigna, una guía de estilo única, índice automático, 10 frases puente y checklist de 20 puntos; plan de 2 días | `07-formato-entrega.md` | M | Coordinador + una persona de formato |
| 7 · Presupuesto: cómo se construyen los números (pedido del Prof. Pacheco) | Presupuesto en **USD** con un único tipo de cambio (ARS 1.560,00, 09/10/2026), desglosado en 32 líneas con paquete de trabajo, tipo de costo, método (Clase 4), cantidad × costo unitario × duración y mes; explicación con 3 ejemplos; **auditoría contra la Clase 4** (corrige una comparación que mezclaba alcances) y memoria de cálculo de una página | `03-presupuesto/presupuesto.md`, `auditoria.md`, `memoria-de-calculo.md`, `desglose.csv` | M | Todo el grupo |
| 8 · Guion narrativo (el hilo entre secciones) | Papel de cada sección, objetos del hilo con valor único (segmento, hitos, duración, USD, tipo de cambio, riesgos), 10 frases puente con el contenido final, resumen ejecutivo y tabla de consistencia | `08-guion-narrativo.md` | S | Coordinador |

## ¿Tiene más o menos sentido el proyecto?

**Sí**: el problema es real y el modelo de dos lados cierra. El riesgo es el **tamaño**: 27 días hábiles de desarrollo para 6 componentes y 4 canales. Propuesta: **MVP recortado** (Mapa + Boti; 2 fuentes; BAX y miBA a fase futura; **perfil de hogar básico sí, personalización avanzada no**). Los números **cierran entre sí**, aunque las tarifas, las personas por rol y el tipo de cambio son supuestos a acordar. Detalle en `06-coherencia.md`.

## Decisiones que hay que tomar entre todos

1. **Presupuesto:** escenario **B** (USD 266.868, mano de obra desde el Gantt; **recomendado**) o **A** (USD 230.639, mínimo esfuerzo). Regla de corte en `03-presupuesto`.
2. **Moneda y tipo de cambio:** USD, con ARS 1.560,00 por USD (09/10/2026, **a confirmar**) como constante única.
3. **Segmento:** **hogares de la Ciudad en general**; hogar con niños, adulto mayor y persona con movilidad reducida son **personas** de Design Thinking.
4. **Perfil de hogar básico** (dato mínimo, opt-in) **incluido**; personalización avanzada excluida del MVP: oración aclaratoria para §5.5.
5. **Gantt:** opción A (corregir 7 celdas de dependencias y escribirlas explícitas), B (registrar adelantos) o solo la nota mínima; los 8 gates **no cambian de fecha** (Gate 2 sigue el 01/05; simulación lunes a viernes sin feriados, declarada en una línea).
6. **Tarifas y personas por rol** (supuestos del grupo).
7. **Charter condensado** con Anexo A, o dejarlo largo.
8. **Formato de entrega:** un solo documento (Word → PDF) con el Excel del Gantt como anexo.
9. **Design Thinking:** decidido que la investigación es **simulada** y se rotula como tal (sin entrevistas reales); falta elegir si «Mi hogar» entra al prototipo (opción A) o queda fuera del MVP (opción B), ver `05b`.

## Para después

Un **mock** de alguna funcionalidad (por ejemplo, el seguimiento de un reporte o la vista del hogar con su perfil básico) para mostrar cómo se vería: se hace **al final**, con el documento cerrado. No se construye ahora.

## Verificación

- 7 controles de coherencia propuestos: 7 en verde.
- Los gates, el CPM del Excel (lecturas, escenarios y camino crítico) y los totales se calculan con `tools/` a partir del Excel del equipo (todo recalcula con `bash tools/run-all.sh`; el presupuesto también con otro tipo de cambio: `python3 03-presupuesto/model.py 1800`).
- **Sin verificar:** denominaciones vigentes de áreas, el texto de la Ley 25.326, el traslado del feriado del 15/06, el tipo de cambio contra el cierre oficial, las tarifas contra datos de mercado y que las correcciones del Gantt sean las que quiso escribir quien armó el Excel (se deducen de las fechas).
