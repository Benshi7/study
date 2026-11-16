# Memoria de cálculo del presupuesto (una página)

> Moneda: **USD**, con **un único tipo de cambio: ARS 1.560,00 por USD** (Banco Nación, dólar oficial (venta), cotización publicada por El Cronista el 09/10/2026 (el mismo medio da el mayorista en 1.541,90); esa fuente repite cifras del día anterior: a confirmar con el cierre oficial; fecha 09/10/2026; a confirmar). Cambiar ese valor en `tools/data.py` recalcula todo. Cada importe se redondea a dólares enteros **por línea** y los totales suman líneas.

## Los 8 pasos (en el orden de la Clase 4, p15)

1. **Fijar la moneda y el tipo de cambio.** Los importes del equipo están en pesos; se convierten a USD con una sola constante. El tipo de cambio es un factor Económico del PESTEL (Clase 4, p7) y está tratado como riesgo (R19).
2. **Tomar la duración del Gantt.** Para cada rol o servicio, *días hábiles* = unión de las actividades donde interviene (fechas Inicio–Fin del Excel del equipo, lunes a viernes). **21 días hábiles = 1 mes.** (Clase 4, p16: la estimación parte de la estimación de recursos y tiempos).
3. **Estimar cada paquete de trabajo.** `cantidad × costo unitario × duración` (p16), considerando costos directos e indirectos. Técnica (p18): *paramétrica simple* para la mano de obra (tarifa × personas × tiempo) y *experta* para el resto; no hay datos para *análoga*.
4. **Clasificar** cada línea (p13–14): fijo/variable y directo/indirecto. Todas son directas; los indirectos están declarados en USD 0.
5. **Sumar hacia arriba** (p24): paquetes de trabajo → centros contables → **proyecto = USD 212.604**.
6. **Calcular la contingencia** (p19–20; Clase 5 p31: *EMV = P × I, con este valor generamos la reserva de contingencia*): suma de los EMV de los riesgos identificados = **USD 30.003**. Proyecto + contingencia = **línea base USD 242.607**.
7. **Agregar la reserva de gestión** (p19, p21, p24): 10 % de la línea base = **USD 24.261** → **presupuesto USD 266.868**. El mantenimiento inicial (USD 17.948) es posterior al cierre: se informa aparte (total con mantenimiento: **USD 284.816**).
8. **Presentar la curva S** (p23): cada línea se reparte parejo entre el primer y el último día de su ventana; el acumulado mensual termina en el costo del proyecto, y con la contingencia termina en la línea base.

## Un ejemplo por tipo de costo (se reproducen con una calculadora)

| Tipo | Línea | Fórmula con números | Resultado |
|---|---|---|---|
| Mano de obra (paramétrica) | RH3 Desarrolladores | 3 pers. × USD 6.410,26/mes × 53 ÷ 21 | USD 48.535 |
| Herramienta mensual (experta, fija) | TEC1 Herramientas y ambientes de desarrollo | 1 servicio × USD 1.297,45/mes × 83 ÷ 21 | USD 5.128 |
| Importe global (experta, variable) | TEC4 Servicios tecnológicos complementarios | 1 global × USD 4.487 | USD 4.487 |
| Servicio mensual (experta, fijo) | INF1 Infraestructura y hosting | 1 servicio × USD 1.258,04/mes × 107 ÷ 21 | USD 6.410 |
| Mantenimiento (posterior al cierre) | MAN1 Corrección de errores iniciales | 1 global × USD 6.410; **fuera de la línea base** | USD 6.410 |
| Contingencia (un riesgo) | R01 Falta de disponibilidad de APIs o fuentes necesarias | P 30 % × impacto USD 7.692 (nivel 4) | USD 2.308 |
| Contingencia (total) | Σ EMV de los 19 riesgos | suma de los EMV residuales | USD 30.003 |
| Reserva de gestión | 10 % de la línea base | USD 242.607 × 10 % | USD 24.261 |
| Curva S (un mes de una línea) | TEC3 Herramientas de monitoreo y gestión | USD 24,47 por día hábil × 23 d.h. de julio | USD 563 |

## Los totales, como los muestra la cátedra (p24)

| Nivel | Importe |
|---|---|
| Presupuesto | USD 266.868 |
| Reserva de gestión (10 %) | USD 24.261 |
| Línea base de costos | USD 242.607 |
| Reserva de contingencia (Σ EMV) | USD 30.003 |
| Proyecto (Σ de 28 paquetes de trabajo) | USD 212.604 |

**Qué es supuesto:** el tipo de cambio, las tarifas (las del equipo, convertidas), las personas por rol, los importes globales sin cotización y la escala de impactos de los riesgos. **Qué se verifica solo:** que las sumas cierran y que cada línea sale de su fórmula (`bash tools/run-all.sh`).
