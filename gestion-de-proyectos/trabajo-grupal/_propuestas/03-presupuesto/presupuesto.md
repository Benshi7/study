# Presupuesto: de los pesos del equipo a un presupuesto en USD que se puede seguir número por número

> **Propuesta.** Responde al pedido del profesor: *«dar más detalle de cómo construyen los números»*. Se conservan **los importes y las tarifas del equipo** (están en pesos, §10); lo nuevo es (1) la **moneda de presentación en USD con un único tipo de cambio**, (2) el **desglose en 32 líneas** que muestran paquete de trabajo, tipo de costo, método, cantidad × costo unitario × duración y mes de incurrencia, (3) la **duración sale de las fechas del Gantt del equipo (Excel, punto 6)**, (4) la **contingencia sale de los EMV** y (5) la **reserva de gestión** explícita. Ningún original fue modificado. Archivos: `desglose.csv` (las 32 líneas con todos los campos), `model.csv` (mano de obra), `tools/` (recalcula todo).

## Moneda y tipo de cambio

**Tipo de cambio:** ARS 1.560,00 por USD · Banco Nación, dólar oficial (venta), cotización publicada por El Cronista el 09/10/2026 (el mismo medio da el mayorista en 1.541,90); esa fuente repite cifras del día anterior: a confirmar con el cierre oficial · fecha de referencia 09/10/2026 · **a confirmar**.

- Todos los importes del equipo están en pesos (ARS). Se convierten a USD con **una sola constante** (`FX_ARS_PER_USD` en `tools/data.py`): cambiarla recalcula **todas** las cifras de este documento y de los demás.
- El tipo de cambio es un factor **Económico** del PESTEL (Clase 4, p7): por eso se lo trata como supuesto explícito y como riesgo (**R19**).
- Cada línea se redondea a USD enteros y los totales son **sumas de líneas ya redondeadas**: todas las tablas cierran.
- Si el equipo prefiere otra referencia (por ejemplo, el cierre oficial del día de entrega), se cambia la constante y se regenera.

### Sensibilidad al tipo de cambio

| Tipo de cambio | ARS por USD | Costos del proyecto (B) | Contingencia | Total A | Total B |
|---|---|---|---|---|---|
| ×0,8 | 1.248,00 | USD 265.757 | USD 37.500 | USD 288.299 | USD 333.583 |
| ×1,0 | 1.560,00 | USD 212.604 | USD 30.003 | USD 230.639 | USD 266.868 |
| ×1,2 | 1.872,00 | USD 177.176 | USD 25.005 | USD 192.208 | USD 222.399 |

A menor valor del dólar, más USD cuestan los mismos pesos; el equipo puede mostrar este cuadro como evidencia de que **entiende el efecto de la moneda** en el presupuesto.

## Cómo se construye cada número

Se sigue el orden de la Clase 4 (p15: planificar, estimar, presupuestar, controlar):

1. **Qué estimar** (p17: mano de obra, materiales, subcontratistas y asesores, alquiler de equipo e instalaciones, viajes, reservas de contingencia y de gestión): ver la tabla «Rubros de la Clase 4» más abajo; cada línea del desglose cae en un rubro.
2. **Duración (p16: «parte de la estimación de recursos (tiempos)»):** sale del **Gantt del equipo (Excel)**: las fechas Inicio–Fin de cada actividad. Para cada rol, días hábiles = unión de las actividades donde interviene (lunes a viernes, sin feriados, como el Excel); **21 días hábiles = 1 mes**.
3. **Costo por paquete de trabajo (p16):** `cantidad × costo unitario × duración`. Cada línea del desglose indica a qué fase y actividades del Gantt corresponde.
4. **Técnica de estimación (p18):** **paramétrica** para la mano de obra (tarifa mensual × personas × meses) y **experta** para el resto (el equipo dio importes globales sin cotizaciones). **No se usa estimación análoga**: no hay datos de proyectos anteriores en los documentos.
5. **Clasificación (p13–14):** **fijo/variable** (¿cambia con la cantidad de trabajo?) y **directo/indirecto** (¿beneficia solo a este proyecto?). Todas las líneas son **directas**; los costos indirectos están **declarados en cero** (sección «Costos indirectos»).
6. **Presupuestación (p15, p23, p24):** se suma «hacia arriba»: paquetes de trabajo → centros contables → proyecto; el acumulado mensual es la **curva S**.
7. **Reservas (p19–21):** **contingencia** = suma de los EMV de los riesgos identificados; **reserva de gestión** = porcentaje decidido por la dirección (10 %, el ejemplo de la cátedra, p21).

### Tres ejemplos resueltos

**a) Desarrolladores** (mano de obra, paramétrica): tarifa del equipo = ARS 40,0 M ÷ 4 meses = ARS 10,0 M/mes = **USD 6.410/mes**. En el Gantt intervienen 53 días hábiles = 2,52 meses. Con **3 personas** (propuesta B): 3 × USD 6.410 × 2,52 = **USD 48.535**. (El equipo tenía ARS 40,0 M ≈ USD 25.641, que con esas duraciones equivale a ≈ 1,6 personas.)

**b) Infraestructura y hosting** (`INF1`, experta, fija, directa): el equipo estimó ARS 10,0 M = **USD 6.410** para todo el período. Ventana del Gantt: Fases 3–8 · act. 11–40 = 5,10 meses → **USD 1.258/mes implícito**. Es un valor a reemplazar por una **cotización**.

**c) Contingencia** (riesgo R01, fórmula de la Clase 4 p20: probabilidad × impacto): probabilidad residual 30 % × impacto de nivel 4 (USD 7.692) = **USD 2.308**. La contingencia total es la **suma de los EMV residuales de los 19 riesgos = USD 30.003**; los tres mayores son R10 (USD 4.808), R01 (USD 2.308), R02 (USD 2.308).

## Qué estaba mal en el presupuesto original

- **Mano de obra = «meses × costo»**, sin personas, y los meses no salen del Gantt. Comparación con los días hábiles reales de cada rol (1 mes = 21 d.h.):

| Rol | Meses del equipo | Meses según Gantt (1 persona) | ¿Coinciden (±0,25)? |
|---|---|---|---|
| Project Manager | 6 | 6,19 | sí |
| Analistas funcionales | 3 | 1,52 | no |
| Desarrolladores | 4 | 2,52 | no |
| Especialistas en datos y GIS | 4 | 2,95 | no |
| UX/UI | 2 | 0,95 | no |
| QA y testing | 2 | 1,48 | no |
| Seguridad informática | 1 | 0,57 | no |
| Infraestructura/DevOps | 2 | 1,19 | no |
| Documentación y capacitación | 1 | 0,67 | no |

- **Contingencia del 10 % plano** (USD 20.064), que no deriva de los riesgos y se calcula incluso sobre el mantenimiento posterior al cierre. No hay reserva de gestión (Clase 4, p19–21).
- El Charter (§5.8) enumera categorías pero **no da una cifra**; el total solo aparece en §10. Todo en pesos y sin tipo de cambio declarado.

## Mano de obra: personas × tarifa × duración del Gantt

| Rol | Meses (equipo) | Costo equipo (USD) | Tarifa (USD/mes) | Días hábiles en el Gantt | Personas A | Costo A (USD) | Personas B | Costo B (USD) |
|---|---|---|---|---|---|---|---|---|
| Project Manager | 6 m | USD 30.769 | USD 5.128/mes | 130 (6,19 m) | 0,97 | USD 30.769 | 1 | USD 31.746 |
| Analistas funcionales | 3 m | USD 11.538 | USD 3.846/mes | 32 (1,52 m) | 1,97 | USD 11.538 | 2 | USD 11.722 |
| Desarrolladores | 4 m | USD 25.641 | USD 6.410/mes | 53 (2,52 m) | 1,58 | USD 25.641 | 3 | USD 48.535 |
| Especialistas en datos y GIS | 4 m | USD 20.513 | USD 5.128/mes | 62 (2,95 m) | 1,35 | USD 20.513 | 2 | USD 30.281 |
| UX/UI | 2 m | USD 7.692 | USD 3.846/mes | 20 (0,95 m) | 2,10 | USD 7.692 | 2 | USD 7.326 |
| QA y testing | 2 m | USD 7.692 | USD 3.846/mes | 31 (1,48 m) | 1,35 | USD 7.692 | 2 | USD 11.355 |
| Seguridad informática | 1 m | USD 5.128 | USD 5.128/mes | 12 (0,57 m) | 1,75 | USD 5.128 | 1 | USD 2.930 |
| Infraestructura/DevOps | 2 m | USD 10.256 | USD 5.128/mes | 25 (1,19 m) | 1,68 | USD 10.256 | 1 | USD 6.105 |
| Documentación y capacitación | 1 m | USD 2.564 | USD 2.564/mes | 14 (0,67 m) | 1,50 | USD 2.564 | 1 | USD 1.709 |
| **Total mano de obra** |  | **USD 121.793** |  |  |  | **USD 121.793** |  | **USD 151.709** |

- **Escenario A:** conservar el costo de cada rol del equipo (convertido a USD). «Personas A» muestra cuántas personas implican con las duraciones del Gantt (≈ 1,6 desarrolladores y ≈ 1,4 en datos/GIS): **equipo chico para 6 componentes en paralelo**, algo que un profesor puede cuestionar.
- **Escenario B:** dimensionamiento propuesto (personas a tiempo completo durante la ventana de cada rol): PM 1, analistas 2, desarrolladores 3, datos/GIS 2, UX/UI 2, QA 2, seguridad 1, infraestructura 1, documentación 1. Criterio principal: la Fase 4 tiene **3 frentes de desarrollo en paralelo** (capa geográfica, reportes y vista de gestión), de ahí 3 desarrolladores. Es una **propuesta a acordar**.

## Desglose completo (escenario B)

F/V = fijo/variable, D/I = directo/indirecto (Clase 4, p13–14). Método según la Clase 4, p18. «Cantidad × costo unitario» y «Duración» salen del Gantt; los costos unitarios de las líneas con importe global son **implícitos** (importe ÷ meses): se reemplazan por cotizaciones cuando existan. La **fuente** de todas las líneas que no son mano de obra es *«equipo (importe global, sin cotización) · a confirmar con cotización»*; en la mano de obra, *tarifa: equipo · personas: propuesta*. Detalle de campos en `desglose.csv`.

### Recursos humanos

| ID | Concepto | Paquete de trabajo (Gantt) | F/V · D/I | Método | Cantidad × costo unitario | Duración | Subtotal (USD) | Meses | Supuesto |
|---|---|---|---|---|---|---|---|---|---|
| RH1 | Project Manager | Fases 1–8 · act. 1–40 | V/D | Paramétrica | 1 pers. × USD 5.128,21/mes × 130 ÷ 21 | 130 d.h. = 6,19 m | USD 31.746 | abr–sep 2026 | Tarifa = costo del equipo ÷ meses de su tabla §10.2; personas a tiempo completo durante la ventana del rol. |
| RH2 | Analistas funcionales | Fases 2–3 · act. 5–17 | V/D | Paramétrica | 2 pers. × USD 3.846,15/mes × 32 ÷ 21 | 32 d.h. = 1,52 m | USD 11.722 | abr–may 2026 | Tarifa = costo del equipo ÷ meses de su tabla §10.2; personas a tiempo completo durante la ventana del rol. |
| RH3 | Desarrolladores | Fases 3–6 · act. 11–31 | V/D | Paramétrica | 3 pers. × USD 6.410,26/mes × 53 ÷ 21 | 53 d.h. = 2,52 m | USD 48.535 | may–ago 2026 | Tarifa = costo del equipo ÷ meses de su tabla §10.2; personas a tiempo completo durante la ventana del rol. |
| RH4 | Especialistas en datos y GIS | Fases 1–5 · act. 3–26 | V/D | Paramétrica | 2 pers. × USD 5.128,21/mes × 62 ÷ 21 | 62 d.h. = 2,95 m | USD 30.281 | abr–jul 2026 | Tarifa = costo del equipo ÷ meses de su tabla §10.2; personas a tiempo completo durante la ventana del rol. |
| RH5 | UX/UI | Fases 2–6 · act. 5–29 | V/D | Paramétrica | 2 pers. × USD 3.846,15/mes × 20 ÷ 21 | 20 d.h. = 0,95 m | USD 7.326 | abr–ago 2026 | Tarifa = costo del equipo ÷ meses de su tabla §10.2; personas a tiempo completo durante la ventana del rol. |
| RH6 | QA y testing | Fases 5–6 · act. 26–32 | V/D | Paramétrica | 2 pers. × USD 3.846,15/mes × 31 ÷ 21 | 31 d.h. = 1,48 m | USD 11.355 | jul–ago 2026 | Tarifa = costo del equipo ÷ meses de su tabla §10.2; personas a tiempo completo durante la ventana del rol. |
| RH7 | Seguridad informática | Fases 3–6 · act. 11–30 | V/D | Paramétrica | 1 pers. × USD 5.128,21/mes × 12 ÷ 21 | 12 d.h. = 0,57 m | USD 2.930 | may–ago 2026 | Tarifa = costo del equipo ÷ meses de su tabla §10.2; personas a tiempo completo durante la ventana del rol. |
| RH8 | Infraestructura/DevOps | Fases 3–7 · act. 11–36 | V/D | Paramétrica | 1 pers. × USD 5.128,21/mes × 25 ÷ 21 | 25 d.h. = 1,19 m | USD 6.105 | may–sep 2026 | Tarifa = costo del equipo ÷ meses de su tabla §10.2; personas a tiempo completo durante la ventana del rol. |
| RH9 | Documentación y capacitación | Fases 7–8 · act. 34–39 | V/D | Paramétrica | 1 pers. × USD 2.564,10/mes × 14 ÷ 21 | 14 d.h. = 0,67 m | USD 1.709 | ago–sep 2026 | Tarifa = costo del equipo ÷ meses de su tabla §10.2; personas a tiempo completo durante la ventana del rol. |
|  | **Subtotal recursos humanos** |  |  |  |  |  | **USD 151.709** |  |  |

### Desarrollo y tecnología

| ID | Concepto | Paquete de trabajo (Gantt) | F/V · D/I | Método | Cantidad × costo unitario | Duración | Subtotal (USD) | Meses | Supuesto |
|---|---|---|---|---|---|---|---|---|---|
| TEC1 | Herramientas y ambientes de desarrollo | Fases 3–6 · act. 11–32 | F/D | Experta | 1 servicio × USD 1.297,45/mes × 83 ÷ 21 | 83 d.h. = 3,95 m | USD 5.128 | may–ago 2026 | Cuota por período de uso durante diseño, desarrollo y pruebas (§10.3). |
| TEC2 | Licencias y herramientas de testing | Fase 6 · act. 27–32 | F/D | Experta | 1 servicio × USD 2.588,65/mes × 26 ÷ 21 | 26 d.h. = 1,24 m | USD 3.205 | jul–ago 2026 | Solo durante la fase de pruebas (§10.3). |
| TEC3 | Herramientas de monitoreo y gestión | Fases 1–8 · act. 1–40 | F/D | Experta | 1 servicio × USD 517,73/mes × 130 ÷ 21 | 130 d.h. = 6,19 m | USD 3.205 | abr–sep 2026 | Se usan durante todo el proyecto (§10.3). |
| TEC4 | Servicios tecnológicos complementarios | Fases 3–6 · act. 11–32 | V/D | Experta | 1 global × USD 4.487 | 83 d.h. = 3,95 m | USD 4.487 | may–ago 2026 | Servicios contratados según necesidad del desarrollo (§10.3). |
| TEC5 | Herramientas de soporte y documentación | Fases 3–8 · act. 11–40 | F/D | Experta | 1 servicio × USD 629,02/mes × 107 ÷ 21 | 107 d.h. = 5,10 m | USD 3.205 | may–sep 2026 | Desde el diseño hasta el cierre (§10.3). |
| TEC6 | Otros servicios técnicos | Fases 3–6 · act. 11–32 | V/D | Experta | 1 global × USD 3.205 | 83 d.h. = 3,95 m | USD 3.205 | may–ago 2026 | Importe global sin detalle en el original (§10.3). |
|  | **Subtotal desarrollo y tecnología** |  |  |  |  |  | **USD 22.435** |  |  |

### Datos, GIS e integraciones

| ID | Concepto | Paquete de trabajo (Gantt) | F/V · D/I | Método | Cantidad × costo unitario | Duración | Subtotal (USD) | Meses | Supuesto |
|---|---|---|---|---|---|---|---|---|---|
| DAT1 | Preparación y normalización de datos | Fases 2–3 · act. 7–12 | V/D | Experta | 1 global × USD 3.205 | 22 d.h. = 1,05 m | USD 3.205 | abr–may 2026 | Depende de la cantidad y calidad de las fuentes (§10.4). |
| DAT2 | Desarrollo y configuración de APIs | Fase 4 · act. 23 | V/D | Experta | 1 global × USD 3.846 | 12 d.h. = 0,57 m | USD 3.846 | jun–jul 2026 | Coincide con la actividad 23 del Gantt (§10.4). |
| DAT3 | Servicios de geocodificación y mapas | Fases 4–6 · act. 18–32 | V/D | Experta | 1 servicio × USD 815,82/mes × 66 ÷ 21 | 66 d.h. = 3,14 m | USD 2.564 | may–ago 2026 | Consumo durante desarrollo e integración; el original no da volumen (§10.4). |
| DAT4 | Integración con fuentes oficiales | Fase 5 · act. 24 | V/D | Experta | 1 global × USD 1.923 | 6 d.h. = 0,29 m | USD 1.923 | jul 2026 | Coincide con la actividad 24 del Gantt (§10.4). |
|  | **Subtotal datos, GIS e integraciones** |  |  |  |  |  | **USD 11.538** |  |  |

### Infraestructura y seguridad

| ID | Concepto | Paquete de trabajo (Gantt) | F/V · D/I | Método | Cantidad × costo unitario | Duración | Subtotal (USD) | Meses | Supuesto |
|---|---|---|---|---|---|---|---|---|---|
| INF1 | Infraestructura y hosting | Fases 3–8 · act. 11–40 | F/D | Experta | 1 servicio × USD 1.258,04/mes × 107 ÷ 21 | 107 d.h. = 5,10 m | USD 6.410 | may–sep 2026 | Se asume infraestructura dedicada; si se comparte con otros proyectos pasa a Indirecto (§10.5). |
| INF2 | Base de datos y almacenamiento | Fases 3–8 · act. 11–40 | V/D | Experta | 1 servicio × USD 629,02/mes × 107 ÷ 21 | 107 d.h. = 5,10 m | USD 3.205 | may–sep 2026 | Crece con el volumen de datos y reportes (§10.5). |
| INF3 | Monitoreo y disponibilidad | Fases 5–8 · act. 24–40 | F/D | Experta | 1 servicio × USD 854,67/mes × 63 ÷ 21 | 63 d.h. = 3,00 m | USD 2.564 | jul–sep 2026 | Desde las integraciones hasta el cierre (§10.5). |
| INF4 | Seguridad y controles de acceso | Fases 3–6 · act. 11–30 | F/D | Experta | 1 global × USD 3.846 | 72 d.h. = 3,43 m | USD 3.846 | may–ago 2026 | Se diseña en la arquitectura y se prueba en la actividad 30 (§10.5). |
| INF5 | Backup y recuperación | Fases 7–8 · act. 33–40 | F/D | Experta | 1 servicio × USD 2.804,38/mes × 24 ÷ 21 | 24 d.h. = 1,14 m | USD 3.205 | ago–sep 2026 | Desde la puesta en producción hasta el cierre (§10.5). |
|  | **Subtotal infraestructura y seguridad** |  |  |  |  |  | **USD 19.230** |  |  |

### Implementación y capacitación

| ID | Concepto | Paquete de trabajo (Gantt) | F/V · D/I | Método | Cantidad × costo unitario | Duración | Subtotal (USD) | Meses | Supuesto |
|---|---|---|---|---|---|---|---|---|---|
| IMP1 | Preparación del entorno productivo | Fase 7 · act. 33 | F/D | Experta | 1 global × USD 2.564 | 4 d.h. = 0,19 m | USD 2.564 | ago–sep 2026 | Coincide con la actividad 33 del Gantt (§10.6). |
| IMP2 | Capacitación de equipos internos | Fase 7 · act. 34 | V/D | Experta | 1 global × USD 1.923 | 6 d.h. = 0,29 m | USD 1.923 | ago–sep 2026 | Depende de la cantidad de personas a capacitar (§10.6). |
| IMP3 | Materiales y documentación operativa | Fase 7 · act. 34 | V/D | Experta | 1 global × USD 1.282 | 6 d.h. = 0,29 m | USD 1.282 | ago–sep 2026 | Coincide con la actividad 34 del Gantt (§10.6). |
| IMP4 | Soporte durante la puesta en funcionamiento | Fase 7 · act. 35 | V/D | Experta | 1 global × USD 1.923 | 3 d.h. = 0,14 m | USD 1.923 | sep 2026 | Coincide con la actividad 35 del Gantt (§10.6). |
|  | **Subtotal implementación y capacitación** |  |  |  |  |  | **USD 7.692** |  |  |

### Mantenimiento inicial

| ID | Concepto | Paquete de trabajo (Gantt) | F/V · D/I | Método | Cantidad × costo unitario | Duración | Subtotal (USD) | Meses | Supuesto |
|---|---|---|---|---|---|---|---|---|---|
| MAN1 | Corrección de errores iniciales | Posterior al cierre (fuera del Gantt) | V/D | Experta | 1 global × USD 6.410 | post-cierre | USD 6.410 | post-cierre (sin fecha) | Posterior al cierre; sin duración definida en el original (§10.7). |
| MAN2 | Soporte técnico | Posterior al cierre (fuera del Gantt) | V/D | Experta | 1 global × USD 4.487 | post-cierre | USD 4.487 | post-cierre (sin fecha) | Posterior al cierre; sin duración definida en el original (§10.7). |
| MAN3 | Ajustes menores y optimización | Posterior al cierre (fuera del Gantt) | V/D | Experta | 1 global × USD 3.846 | post-cierre | USD 3.846 | post-cierre (sin fecha) | Posterior al cierre; sin duración definida en el original (§10.7). |
| MAN4 | Monitoreo y mantenimiento | Posterior al cierre (fuera del Gantt) | V/D | Experta | 1 global × USD 3.205 | post-cierre | USD 3.205 | post-cierre (sin fecha) | Posterior al cierre; sin duración definida en el original (§10.7). |
|  | **Subtotal mantenimiento inicial (fuera de la línea base)** |  |  |  |  |  | **USD 17.948** |  |  |

### Peso de cada categoría

| Categoría | Importe (USD) | % del total con mantenimiento |
|---|---|---|
| Recursos humanos | USD 151.709 | 65,8 % |
| Desarrollo y tecnología | USD 22.435 | 9,7 % |
| Datos, GIS e integraciones | USD 11.538 | 5,0 % |
| Infraestructura y seguridad | USD 19.230 | 8,3 % |
| Implementación y capacitación | USD 7.692 | 3,3 % |
| Mantenimiento inicial | USD 17.948 | 7,8 % |

## Suma ascendente: de los paquetes de trabajo al presupuesto (Clase 4, p24)

La diapositiva de la cátedra arma el presupuesto de abajo hacia arriba: actividad → paquete de trabajo → centro contable → proyecto; al proyecto se le suma la **reserva de contingencia** (da la **línea base de costos**) y a la línea base la **reserva de gerencia** (da el **presupuesto**). Así queda el escenario B:

| Nivel (Clase 4, p24) | Importe (USD) | Cómo se obtiene |
|---|---|---|
| **Presupuesto** | **USD 266.868** | Línea base + reserva de gestión |
| Reserva de gestión (10 %) | USD 24.261 | Imprevistos no identificados; requiere aprobación de la dirección (p19) |
| **Línea base de costos** | **USD 242.607** | Proyecto + reserva de contingencia |
| Reserva de contingencia | USD 30.003 | Suma de los EMV de los riesgos identificados |
| **Proyecto** | **USD 212.604** | Suma de los 28 paquetes de trabajo (líneas del desglose) |
| ↳ Centro contable: Recursos humanos | USD 151.709 | Suma de sus paquetes de trabajo |
| ↳ Centro contable: Desarrollo y tecnología | USD 22.435 | Suma de sus paquetes de trabajo |
| ↳ Centro contable: Datos, GIS e integraciones | USD 11.538 | Suma de sus paquetes de trabajo |
| ↳ Centro contable: Infraestructura y seguridad | USD 19.230 | Suma de sus paquetes de trabajo |
| ↳ Centro contable: Implementación y capacitación | USD 7.692 | Suma de sus paquetes de trabajo |
| ↳ Paquetes de trabajo (28) | — | Cada uno referido a actividades del Gantt (columna «Paquete de trabajo» del desglose) |

El mantenimiento inicial (USD 17.948) ocurre **después del cierre**: queda fuera de la línea base y se informa aparte.

## Rubros de la Clase 4 (p17: «qué debemos estimar»)

| Rubro (p17) | Líneas del desglose | Importe (escenario B) | % del total con mantenimiento |
|---|---|---|---|
| Mano de obra | RH1, RH2, RH3, RH4, RH5, RH6, RH7, RH8, RH9 | USD 151.709 | 65,8 % |
| Materiales | IMP3 | USD 1.282 | 0,6 % |
| Subcontratistas y asesores | TEC4, TEC6, DAT3 | USD 10.256 | 4,4 % |
| Alquiler de equipo e instalaciones | TEC1, TEC2, TEC3, TEC5, INF1, INF2, INF3, INF4, INF5 | USD 33.973 | 14,7 % |
| Viajes | — | no previstos (no aplica) | 0,0 % |
| Otras actividades del proyecto (el original no distingue entre trabajo propio y contratado) | DAT1, DAT2, DAT4, IMP1, IMP2, IMP4, MAN1, MAN2, MAN3, MAN4 | USD 33.332 | 14,5 % |

*Clasificación propuesta:* el original no distingue entre trabajo propio y contratado, por eso hay un rubro «otras actividades». Las **reservas** (contingencia y gestión) se muestran en la suma ascendente.

## Costos indirectos (Clase 4, p14 y p16)

Costos indirectos (seguros, impuestos, espacio de trabajo y servicios compartidos del GCBA; Clase 4, p14): no se estiman en este presupuesto; se asume que los absorbe la organización. **Importe: USD 0.** Decisión del grupo: declararlo así (recomendado, es lo que dice el original) o sumar un porcentaje sobre la mano de obra con una justificación escrita.

## Escalera de reservas y comparación

| Concepto | Hoy (equipo, convertido) | Escenario A | Escenario B |
|---|---|---|---|
| Costos del proyecto (sin reservas) | USD 182.688 | USD 182.688 | USD 212.604 |
| Mantenimiento inicial posterior al cierre | USD 17.948 | USD 17.948 | fuera de la línea base |
| Reserva de contingencia | USD 20.064 (10 % plano) | USD 30.003 (Σ EMV) | USD 30.003 (Σ EMV) |
| Línea base de costos | — | USD 230.639 | USD 242.607 |
| Reserva de gestión | no existe | no definida | USD 24.261 (10 %) |
| **Total** | **USD 220.700** | **USD 230.639** | **USD 266.868** |
| Total con mantenimiento posterior | USD 220.700 | USD 230.639 | USD 284.816 |
| Equivalente en ARS (referencia, al tipo de cambio) | ARS 344,3 M | ARS 359,8 M | ARS 416,3 M |

- **A (mínimo esfuerzo):** mismos costos, contingencia derivada de los riesgos. **No se puede conservar el total del equipo (USD 220.700):** la contingencia calculada (USD 30.003) supera los USD 20.064 que había, así que el total sube USD 9.939 (4,5 %) o habría que recortar costos.
- **B:** mano de obra desde el Gantt con equipo proporcionado al alcance y reserva de gestión explícita: **USD 266.868** hasta el cierre y **USD 284.816** con el mantenimiento inicial posterior. **La comparación correcta es contra el total del equipo, que también incluye el mantenimiento: USD 284.816 contra USD 220.700, es decir 29,1 % más.** (Comparar USD 266.868 contra USD 220.700 daría 20,9 % y mezcla alcances distintos.)
- Con la escala de impactos propuesta, la **contingencia es el 14,1 % de los costos de B** (el equipo había puesto 10 %). Depende de esa escala (ver sensibilidad: de 7,1 % a 21,2 %): lo que faltaba era la **trazabilidad**, no una cifra exacta.

### Puente comparable: del total del equipo al escenario B

| Paso | Variación | Acumulado |
|---|---|---|
| Total del equipo, convertido (incluye el mantenimiento inicial) | — | USD 220.700 |
| Contingencia: 10 % plano → suma de los EMV | +USD 9.939 | USD 230.639 |
| Mano de obra: meses del equipo → personas × duración del Gantt | +USD 29.916 | USD 260.555 |
| Reserva de gestión (10 % de la línea base) | +USD 24.261 | USD 284.816 |
| **Escenario B con mantenimiento inicial** |  | **USD 284.816** |

1. **Contingencia: 10 % plano → suma de los EMV:** Contingencia calculada desde los riesgos identificados (Clase 4 p19–20), no un porcentaje plano.
2. **Mano de obra: meses del equipo → personas × duración del Gantt:** La duración sale de las fechas del Gantt del equipo y se explicitan las personas por rol (Clase 4 p16).
3. **Reserva de gestión (10 % de la línea base):** Reserva explícita para imprevistos no identificados (Clase 4 p19, p21, p24); no existía.

Diferencia de redondeo: el total del equipo convertido **línea por línea** es USD 220.700; convertido **de una sola vez** (ARS 344,3 M ÷ 1.560,00) da USD 220.705,13: 5,13 USD de diferencia, por redondear cada línea a dólares enteros.

## Recomendación para la entrega del 14/10

**Presentar el escenario B.** Razones: (1) es el que **responde literalmente** al pedido del profesor, porque cada número tiene fórmula, fuente y supuesto; (2) la mano de obra **concuerda con el Gantt** que se presenta en la sección 6 (con A, la sección 6 y la 10 se contradicen: analistas 3 meses contra 1,5); (3) **ya está calculado**: al equipo le quedan dos decisiones (personas por rol y tarifas) y pegar las tablas. **Regla de corte:** si no hay acuerdo sobre las personas por rol el 13/10 al mediodía, entregar **A** (se cambian solo la moneda y la contingencia) y dejar B en la defensa como mejora. En ambos casos: declarar el tipo de cambio y que las cifras son estimativas con fin académico.

### Sensibilidad de la contingencia a la escala de impactos (supuesta)

| Escala de impacto | Contingencia | % de los costos de B | % de los costos de A |
|---|---|---|---|
| ×0,5 | USD 15.002 | 7,1 % | 7,5 % |
| ×1,0 | USD 30.003 | 14,1 % | 15,0 % |
| ×1,5 | USD 45.005 | 21,2 % | 22,4 % |

## Curva S (escenario B, costos del proyecto por mes, alineados con el Gantt)

| Mes | Costo del mes | Acumulado |
|---|---|---|
| 04/2026 | USD 22.266 | USD 22.266 |
| 05/2026 | USD 44.136 | USD 66.402 |
| 06/2026 | USD 43.128 | USD 109.530 |
| 07/2026 | USD 47.639 | USD 157.169 |
| 08/2026 | USD 35.492 | USD 192.661 |
| 09/2026 | USD 19.943 | USD 212.604 |

### Curva S de la línea base (con contingencia)

En la Clase 4 la línea base incluye la reserva de contingencia (p24). Para mostrarla, la contingencia se reparte **en proporción al costo de cada mes**:

| Mes | Costo del mes + contingencia | Acumulado (línea base) |
|---|---|---|
| 04/2026 | USD 25.408 | USD 25.408 |
| 05/2026 | USD 50.365 | USD 75.773 |
| 06/2026 | USD 49.214 | USD 124.987 |
| 07/2026 | USD 54.362 | USD 179.349 |
| 08/2026 | USD 40.501 | USD 219.850 |
| 09/2026 | USD 22.757 | USD 242.607 |

La curva termina en **USD 242.607** (la línea base). La reserva de gestión (USD 24.261) no se distribuye: se asigna cuando la dirección la autoriza (p19).

Cada línea se reparte parejo entre el primer y el último día de las actividades de su ventana (`desglose.csv`, columna «Paquete de trabajo»). La curva termina en **USD 212.604** (los costos del proyecto, **sin** reservas); las reservas se asignan a la línea base cuando se las usa. El mantenimiento inicial (USD 17.948) es posterior al cierre y queda fuera.

## Chequeos de cordura

| Chequeo | Resultado |
|---|---|
| Las sumas cierran (líneas → categorías → total) | Sí: costos + contingencia + reserva = total, en A y en B; los totales son sumas de líneas redondeadas |
| La curva S termina en los costos del proyecto | Sí (USD 212.604) |
| Mano de obra sobre costos del proyecto | B 71,4 % (equipo: 66,7 %) |
| Tarifa mensual por rol (USD/mes, convertida del equipo) | PM 5.128; analistas 3.846; desarrolladores 6.410; datos/GIS 5.128; UX/UI 3.846; QA 3.846; seguridad 5.128; infraestructura 5.128; documentación 2.564 |
| Contingencia / costos | A 16,4 % · B 14,1 % |
| Efecto del tipo de cambio | ±20 % en el dólar mueve el total B entre USD 222.399 y USD 333.583 |
| Costos indirectos | No se imputan (a declarar); todas las líneas son directas |
| Unidades | USD enteros; 1 mes = 21 días hábiles; tipo de cambio único ARS 1.560,00 |

## Qué es verificado y qué es supuesto

- **Verificado:** que las sumas cierran, que cada línea sale de `cantidad × costo unitario` (o del importe del equipo ÷ tipo de cambio) y que la duración sale de las fechas del Gantt del equipo. `bash tools/run-all.sh` lo comprueba, incluso con otro tipo de cambio.
- **Supuesto (a acordar entre todos):** el **tipo de cambio** (a confirmar), las **tarifas** (son las del equipo; **no se contrastaron con datos de mercado**), las **personas por rol**, la **escala de impactos**, el 10 % de reserva de gestión y las ventanas de cada línea. Los importes globales no tienen cotización.
