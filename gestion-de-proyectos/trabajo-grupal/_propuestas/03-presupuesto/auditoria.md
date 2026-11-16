# Auditoría del presupuesto contra el material de la cátedra

> **Veredicto.** Los números **cierran** y la estructura **coincide** con la Clase 4 en lo esencial (escalera de reservas, P × I, clasificación, técnicas). Se registraron **9 hallazgos** (1 alto, 4 medios, 2 bajos, 2 informativos; el más importante: una comparación que mezclaba alcances); los de contenido están resueltos en `presupuesto.md` y quedan **dos decisiones** del grupo (base de la reserva e indirectos). Lo que **no** se puede verificar desde el material: las tarifas, los importes globales y el tipo de cambio contra el mercado.

## Qué se miró

- **Clase 4 (Gestión de costos):** texto de las p12–24 y p26–29 y **las imágenes de p23 (curva S), p24 (suma ascendente) y p29 (valor tiempo del dinero)**. Clase 5 p31 (EMV).
- **Ejemplo Clase:** es un Canvas de un negocio de insumos médicos; su único contenido de costos es el bloque «Estructura de costos» (p13). **No trae un presupuesto de proyecto**: el modelo a imitar es el de la Clase 4.
- **Pack:** `presupuesto.md`, `desglose.csv` (32 líneas), `model.csv`, `04-riesgos.csv`, `02-gantt/schedule.csv`.

## Lo verificado contra las diapositivas

| Qué dice la cátedra | Dónde | Resultado |
|---|---|---|
| Escalera de reservas: proyecto + contingencia = línea base; + reserva de gerencia = presupuesto | p24 (imagen) | Coincide con el pack |
| Contingencia = probabilidad × impacto (ejemplo: acero $500.000, 30 % de que suba 10 % → $15.000) | p20 | Coincide: el pack usa P × I por riesgo |
| EMV = P × I y «con este valor generamos la reserva de contingencia» | Clase 5 p31 | Coincide: contingencia = Σ EMV |
| Reserva de gestión: 10 % del presupuesto total, sin riesgos específicos | p19, p21 | Coincide; la base del % es ambigua (hallazgo 9) |
| Qué estimar: mano de obra, materiales, subcontratistas, alquiler de equipo e instalaciones, viajes, reservas | p17 | Mapeado (tabla de rubros) |
| Técnicas: análoga, paramétrica, experta | p18 | Se usan paramétrica y experta; análoga no (sin datos previos) |
| Costo por paquete de trabajo, directos e indirectos; parte de la estimación de recursos y tiempos | p16 | Coincide (indirectos declarados en 0) |
| Clasificación fijo/variable y directo/indirecto | p13–14 | Coincide |
| Curva S como línea base de desempeño; flujo de caja esperado | p23 (imagen) | Coincide; el pack muestra una curva por escenario B y la de línea base |
| Valor tiempo del dinero con tasa de descuento (ejemplo de inversión) | p29 (imagen) | No aplica: es un proyecto público sin flujo de ingresos modelado; si se agregara, la lógica es la de esa tabla |

## Hallazgos

| # | Hallazgo | Gravedad | Estado |
|---|---|---|---|
| 1 | La comparación «+20,9 % sobre el total del equipo» mezclaba alcances: B sin mantenimiento contra el equipo con mantenimiento. | Alta (un profesor la detecta) | **Corregido:** comparación homogénea, USD 284.816 contra USD 220.700 = **+29,1 %**, con puente de tres pasos. |
| 2 | La aritmética mostrada no se reproducía con calculadora: en 17 líneas «cantidad × costo mostrado» difería del subtotal (hasta USD 121) por mostrar la tarifa sin centavos y los meses redondeados. | Media (es justo lo que pidió el profesor) | **Corregido:** se muestra «tarifa con centavos × días hábiles ÷ 21 (× personas)»; un test independiente la recalcula desde los CSV. |
| 3 | No estaba la presentación «suma ascendente» de la Clase 4 (p24). | Media | **Agregado:** pirámide paquetes → centros contables → proyecto → línea base → presupuesto. |
| 4 | La curva S no incluía la contingencia, pero la línea base de la cátedra sí (p24). | Media | **Agregado:** segunda curva que termina en la línea base. |
| 5 | Los costos indirectos solo se mencionaban («conviene declararlo»), sin una fila; la p16 pide considerar directos e indirectos. | Baja | **Agregado:** fila declarada en USD 0 con decisión del grupo. |
| 6 | Los rubros de «qué estimar» (p17) no estaban mapeados. | Baja | **Agregado:** tabla de rubros (clasificación propuesta). |
| 7 | Redondeo: el total del equipo convertido línea por línea (USD 220.700) difiere 5,13 USD de convertirlo de una vez. | Informativa | Declarado en el puente; no cambia ninguna conclusión. |
| 8 | Se usa un único tipo de cambio de octubre de 2026 para un proyecto simulado de abril a septiembre de 2026; la fuente es secundaria. | Informativa | Declarado; sensibilidad ±20 % en el documento; **a confirmar con el cierre oficial**. |
| 9 | La base del 10 % de reserva de gestión es ambigua en la cátedra: p21 («10 % del presupuesto total, $100.000»), p24 (ejemplo $60 sobre una línea base de $240). Si fuera 10 % del total final, la reserva sería USD 26.956 y el presupuesto USD 269.563. | Media (decisión) | Se mantiene 10 % **de la línea base** (USD 24.261) y se declara; alternativa a decidir. |

## Recálculo independiente

Un test (`tools/test_audit_independent.py`) recalcula **sin usar el modelo**: los totales desde `desglose.csv` y `04-riesgos.csv` (costos + Σ EMV + reserva = USD 266.868; con mantenimiento, USD 284.816), los días hábiles de cada rol desde las fechas escritas del Excel, y cada línea con su fórmula mostrada (tarifa con centavos × días hábiles ÷ 21). Las sumas de la curva S también se recalculan. Resultado: **sin diferencias** (más allá del redondeo a dólares enteros).

## Razonabilidad: qué es verificado, supuesto y sin contrastar

| Indicador | Valor | Lectura |
|---|---|---|
| Mano de obra sobre costos del proyecto | B 71,4 % · equipo 66,7 % | Es la categoría dominante; **sin contrastar con el mercado** |
| Costo promedio por persona-mes (B) | USD 5.057 (30,0 persona-mes) | Sale de las tarifas del equipo convertidas; **sin contrastar con el mercado** |
| Tarifas mensuales convertidas | Project Manager USD 5.128; Analistas funcionales USD 3.846; Desarrolladores USD 6.410; Especialistas en datos y GIS USD 5.128; UX/UI USD 3.846; QA y testing USD 3.846; Seguridad informática USD 5.128; Infraestructura/DevOps USD 5.128; Documentación y capacitación USD 2.564 | Son las del equipo (pesos ÷ meses de su tabla §10.2); **sin contrastar con el mercado** |
| Contingencia sobre costos del proyecto | 14,1 % (rango 7,1 %–21,2 % según la escala de impactos) | Depende de una escala de impactos **supuesta**; lo que se verifica es la trazabilidad, no la cifra |
| Infraestructura y seguridad sobre costos del proyecto | 9,0 % | Importes globales del equipo, **sin cotización** |
| Mantenimiento inicial sobre costos del proyecto | 8,4 % | Importe global del equipo; sin duración definida |
| Efecto del tipo de cambio | ±20 % mueve el total B entre USD 222.399 y USD 333.583 | Es el supuesto más sensible: conviene explicitarlo en el documento |

**Verificado:** coherencia aritmética, correspondencia con la Clase 4/5, duraciones desde las fechas del Excel. **Supuesto:** tipo de cambio, personas por rol, escala de impactos, 10 % de reserva. **Sin contrastar con el mercado:** tarifas, importes globales, infraestructura. Este paquete no cita referencias de mercado porque no se consultaron fuentes verificables; si el equipo quiere defender las tarifas, necesita una cotización o una fuente.

## Puente con el total del equipo y con el campo (12) del Charter

| Paso | Variación | Acumulado |
|---|---|---|
| Total del equipo (§10), convertido | — | USD 220.700 |
| Contingencia: 10 % plano → suma de los EMV | +USD 9.939 | USD 230.639 |
| Mano de obra: meses del equipo → personas × duración del Gantt | +USD 29.916 | USD 260.555 |
| Reserva de gestión (10 % de la línea base) | +USD 24.261 | USD 284.816 |

El campo **(12) Summary Budget** del Charter en plantilla debe mostrar **USD 266.868** (línea base USD 242.607 + reserva de gestión USD 24.261) **más** el mantenimiento inicial posterior al cierre de USD 17.948; ambos números salen de este puente y un test los compara.

## Decisiones para el grupo

1. **Base de la reserva de gestión:** 10 % de la línea base (propuesto) o 10 % del total final (hallazgo 9).
2. **Costos indirectos:** dejarlos en cero declarado (propuesto) o sumar un porcentaje justificado.
3. **Escenario A o B** y la regla de corte del 13/10 (ver `presupuesto.md`).
4. **Tipo de cambio de referencia:** confirmar con el cierre oficial.
