# Coherencia: qué se congela, cómo se fusiona y si el proyecto tiene sentido

> **Propuesta.** Ningún original fue modificado; esto es la guía para que, al unificar, todas las secciones digan lo mismo.

## 1. Mapa de fusión

| Sección | Fuente |
|---|---|
| Documento base | **«Proyect Charter y demas puntos»** (secciones 5 a 10 completas) |
| 1 Carátula | «TP Grupo 01» (única carátula; revisar logo y nómina) |
| 2 Índice | Se rehace al final con páginas reales |
| 3 Canvas · 4 Design Thinking | Documento resumido como punto de partida, reescritos con `05-canvas-dt-smart.md` |
| 5 Charter | Condensado de `01` + Anexo A con el texto largo |
| 6 Gantt | Imagen y hitos del largo + tabla de `02-gantt` |
| 7 · 8 | PDF «corregido» (reemplaza el cuerpo; agregar 2 filas en la matriz de comunicación) |
| 9 · 10 | Largo + EMV y escenarios de `04` y `03` |
| Storytelling | «Conexión narrativa» del resumen como idea; frases puente de abajo |

## 2. Datos a congelar (una sola fuente de verdad)

| Dato | Valor a usar |
|---|---|
| Nombre del proyecto | «Modernización del Mapa Interactivo de la Ciudad» (el resumen dice «…y Ampliación… de Buenos Aires») |
| Fechas | 01/04/2026 inicio de la Fase 1; Charter 10/04; cierre 30/09/2026; entrega 14/10/2026 |
| Gates | 8 gates (G1–G8) con las fechas del Excel (sin cambios); G2 = 01/05 (feriado real: ver `02-gantt`, punto 5) |
| Dependencias del Gantt | Listas explícitas («5, 6»), nunca «a-b»; actividades 2 y 3 como inicio-a-inicio +1 día (ver `02-gantt`) |
| Riesgos | IDs R01–R15 del documento largo (+R16–R19); una sola matriz |
| Moneda | **USD** en todo el documento; equivalente en pesos solo como referencia («ARS … M») |
| Tipo de cambio | ARS 1.560,00 por USD · 09/10/2026 · Banco Nación, dólar oficial (venta) · **a confirmar**; una sola constante recalcula todo |
| Segmento | **Hogares de la Ciudad** (cada hogar con su propia realidad); hogar con niños, adulto mayor y movilidad reducida son **personas** de Design Thinking, no segmentos |
| Perfil de hogar | **Básico** (dato mínimo declarado, opt-in) **incluido**; personalización avanzada o con datos sensibles no necesarios **excluida** del MVP (aclaración propuesta para §5.5.1/§5.5.2) |
| Presupuesto | Una sola cifra total en USD (escenario A USD 230.639 o B USD 266.868) citada igual en Charter, sección 10 y conclusión; reserva de contingencia USD 30.003; mantenimiento posterior USD 17.948 fuera de la línea base |
| Stakeholders | Los nombres del PDF §7.1 (15 filas); los 9 principales para el Charter |
| Sponsor | «Sponsor institucional de Modernización de CABA» (el resumen: «Autoridad Institucional de Modernización»; confirmar denominación vigente) |
| Fuentes priorizadas | Transporte y Cultura (las que nombran el resumen y el PDF); el documento largo solo dice «seleccionadas»: **completar** |
| Nómina del equipo | Una sola lista: la cantidad de nombres cambia según el archivo (8, 9 y 10) y hay un apellido sin completar |

## 3. Checklist de coherencia (7 puntos)

**Estado hoy** (según la revisión) y **resultado con las propuestas** (calculado por `tools/coherence.py` sobre los números propuestos):

| Control | Hoy | Con la propuesta |
|---|---|---|
| Hitos Charter = Gantt | Parcial: los 8 hitos del Excel = §6.3 = resumen, pero §5.12 no tiene fechas, §6.5 lista 7 puntos y la tabla de fases del resumen no coincide con el Excel | 8 gates con la fecha del Excel, iguales en Charter, Gantt y resumen |
| Presupuesto del Charter = total | No: el Charter §5.8 no da cifra | El Charter cita USD 266.868 (B) o USD 230.639 (A) |
| Riesgos Charter ⊂ matriz | Parcial: 12 vs 15; «comercios» no está en la matriz | Los 5 riesgos del Charter son un subconjunto con IDs |
| Contingencia = Σ EMV | No: 10 % plano | USD 30.003 = Σ EMV residual |
| Mano de obra = duraciones del Gantt | Parcial: 2 de 4 comparables no cierran | Cada rol usa los días hábiles de sus actividades |
| Stakeholders Charter ∈ matriz ∈ comunicación | No: dos actores sin fila de comunicación; roles del §5.11 distintos del PDF | Lista única de 9; +2 filas en la matriz de comunicación |
| Frase puente por sección | Mayormente sí desde la sección 6; faltan 3–5 | Frases puente propuestas para 3 a 10 |

Verificación automática (el script **lee los documentos generados** y los compara contra el cronograma recalculado desde sus fechas):

| Control | OK | Detalle |
|---|---|---|
| hitos Charter = Gantt | ✓ | ok |
| presupuesto Charter = total | ✓ | ok |
| riesgos Charter ⊂ matriz | ✓ | ok |
| contingencia = Σ EMV | ✓ | ok |
| mano de obra = duraciones del Gantt | ✓ | ok |
| stakeholders Charter ∈ matriz ∈ comunicación | ✓ | ok |
| frase puente por sección | ✓ | ok |

## 4. Frases puente propuestas (apertura de cada sección)

| Sección | Frase |
|---|---|
| 3 | Nuestro punto de partida es una pregunta concreta: ¿cómo hace un hogar de la Ciudad, con su propia realidad, para enterarse de lo que le corresponde y reportar lo que ve sin saber de antemano a qué organismo ni por qué canal acudir?; el Canvas muestra quién usa, quién paga y qué recibe cada lado. |
| 4 | Del Canvas surge una hipótesis de problema; Design Thinking, como investigación simulada con tres proto-personas, la convierte en un punto de vista y una pregunta de diseño y baja la idea a un prototipo de tres pantallas (consultar, reportar y seguir); la validación con hogares reales queda como actividad del proyecto. |
| 5 | Con el problema y el segmento definidos, el Charter formaliza qué vamos a construir, con qué límites y con qué metas medibles. |
| 6 | Para cumplir los objetivos del Charter ordenamos el trabajo en 40 actividades con duraciones y dependencias; su camino crítico fija la fecha de cierre. |
| 7 | Las actividades del Gantt dependen de personas y organismos con distinto poder e interés; la matriz indica cuánto esfuerzo dedicarle a cada uno. |
| 8 | La estrategia de la matriz de stakeholders se traduce en qué se comunica, a quién, con qué frecuencia y por qué canal. |
| 9 | Cada actividad del camino crítico y cada relación con un stakeholder puede fallar; la matriz de riesgos los prioriza y cuantifica su valor monetario esperado. |
| 10 | El presupuesto, expresado en USD con un tipo de cambio único, convierte el Gantt en dinero (personas × tarifa × duración) y los riesgos en una reserva de contingencia que sale de sus EMV. |

## 5. ¿Tiene más o menos sentido el proyecto?

**Veredicto: sí tiene sentido, con un recorte.** El problema es real y concreto, el modelo de dos lados (vecino y GCBA) explica quién usa y quién paga, y el cronograma y el presupuesto ya cierran entre sí. El riesgo no es la idea: es el **tamaño**.

- **Alcance vs. tiempo:** 8 objetivos, 8 entregables y 4 canales (Mapa, Boti, BAX, miBA) en 131 días hábiles (01/04–30/09). La **Fase 4 (desarrollo) dura 27 días hábiles**; con 3 desarrolladores son ≈ **81 días-persona para 6 componentes** (≈ 14 por componente). Un profesor puede decir que es optimista.
- **Datos personales:** el reporte lleva ubicación y el perfil de hogar básico agrega datos del hogar; el marco legal (**Ley 25.326**) está **sin verificar** en los documentos. Debe aparecer en supuestos, riesgo R10 y requisitos (dato mínimo, opt-in).
- **Dependencias externas:** Boti, BAX y miBA no están bajo control del proyecto (R12, R18).
- **Participación ciudadana:** el valor depende de que los vecinos reporten y validen (R06); sin esa masa crítica el módulo pierde sentido.

### Qué desafiaría un profesor *(y qué responder)*

| Pregunta | Respuesta propuesta |
|---|---|
| ¿Por qué el proyecto «empezó» en abril? | Simulación declarada en una línea (supuesto de simulación). |
| ¿Cuál es el camino crítico? | Según el CPM del Excel: 126 d.h. y 23 actividades sin holgura (cadena 1, 3, 4, 7, 8, 10, 13, 14, 16, 17, 18, 23, 27, 30, 31, 32, 34, 35, 36, 38, 39, 40); con las dependencias corregidas cambia (ver `02-gantt`). |
| ¿Cómo calcularon la contingencia? | Σ EMV residual = USD 30.003; sensibilidad en `03`. |
| ¿Con cuánta gente se desarrolla todo eso en 27 días? | Escenario B con 3 desarrolladores + MVP recortado (abajo). |
| ¿Quién paga y qué recibe cada lado? | GCBA paga y recibe la vista de gestión; el vecino no paga y recibe seguimiento de su reporte. |
| ¿Hay evidencia de usuarios? | No: la investigación está rotulada como **simulada** (hipótesis); no se afirman entrevistas (`05b`). |
| ¿Qué pasa si BAX/Boti/miBA cambian? | R12 y R18; BAX queda sujeto a validación técnica. |
| ¿Cómo tratan los datos personales? | Minimización, controles de acceso, R10; **Ley 25.326, a verificar**. |

### MVP recortado (propuesta, coherente con la Opción B)

| Entra en la primera implementación | Fase futura |
|---|---|
| Capa geográfica con **2 fuentes priorizadas** (Transporte y Cultura) | Más fuentes y áreas |
| Reportes con **pocas categorías** (calle cortada, vehículo detenido, obstáculo) | Nuevas categorías |
| Validación colaborativa simple (confirmar / ya no está) | Reputación y moderación avanzada |
| Estados Reportado → Validado → Derivado → Resuelto → Cerrado (**5**; «En gestión» queda opcional) | Estados por área |
| Integración con **Mapa + Boti** | **BAX** y miBA (sujetos a validación) |
| Vista de gestión **básica** (listar y filtrar) | Tableros analíticos |
| **Perfil de hogar básico** (dato mínimo declarado, opt-in) | Personalización avanzada y uso de datos sensibles |
| — | Socios, beneficios, publicidad |

Esto es **consistente con §5.5.2**: la exclusión alcanza solo a la personalización avanzada o con datos sensibles *no necesarios*. Baja el riesgo de R05 (alcance).

## 6. Orden de magnitud del total

- **Verificado:** que las sumas cierran, que la duración de la mano de obra sale del Gantt y que la contingencia sale de los EMV.
- **Supuesto:** las **tarifas** (las del equipo; no contrastadas con datos de mercado), las personas por rol, la escala de impactos y el tipo de cambio (a confirmar). Con la escala a la mitad o ×1,5 la contingencia queda entre USD 15.002 y USD 45.005; con el dólar ±20 %, el total B queda entre USD 222.399 y USD 333.583.
- El total depende sobre todo de **tarifas × personas**: son las dos cosas que el grupo debe acordar y poder defender.
