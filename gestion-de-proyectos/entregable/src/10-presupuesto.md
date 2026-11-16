# 10. Gestión de costos - Presupuesto

Para respaldar la ejecución del cronograma y prever las reservas necesarias para la mitigación de los riesgos identificados, estimamos el presupuesto total del proyecto.

La gestión de costos tiene como objetivo estimar los recursos económicos necesarios para desarrollar, integrar, implementar y poner en funcionamiento la Modernización del Mapa Interactivo de la Ciudad.

El presupuesto se encuentra alineado con el alcance definido en el Project Charter, las actividades previstas en el cronograma y los recursos necesarios para desarrollar la capa geográfica común, las integraciones, el sistema de reportes ciudadanos, la validación colaborativa y las herramientas de gestión.

Los valores presentados son **estimativos y tienen finalidad académica**. El presupuesto definitivo deberá ajustarse en función del alcance aprobado, los recursos disponibles, las condiciones de contratación y las cotizaciones correspondientes al momento de ejecución.

## 10.1 Criterios y supuestos de costos

Para elaborar el presupuesto se consideran los siguientes criterios:

- El proyecto tendrá una duración aproximada de seis meses de ejecución.

- Se utilizará un equipo multidisciplinario compuesto por perfiles de gestión, análisis funcional, desarrollo, datos, GIS, UX/UI, infraestructura, seguridad y testing.

- Se aprovecharán, cuando sea posible, infraestructura, herramientas y canales digitales existentes.

- Las integraciones con sistemas y fuentes oficiales se consideran dentro del alcance, aunque su costo definitivo dependerá de las condiciones técnicas de cada sistema.

- El presupuesto contempla una primera versión operativa del producto y no el desarrollo de funcionalidades futuras no incluidas en el alcance.

- No se considera que los vecinos deban realizar ningún pago por utilizar el servicio.

- No se consideran ingresos provenientes de comercios, anunciantes o servicios patrocinados durante la primera implementación.

- Se incorpora una reserva de contingencia para cubrir los riesgos identificados en el punto 9, calculada a partir de su valor monetario esperado (EMV).

Los valores se expresan en **dólares estadounidenses (USD)**, con un tipo de cambio supuesto de **ARS 1.560 por USD** (referencia de octubre de 2026, a confirmar con la cotización oficial al momento de aprobar el presupuesto). El equipo estimó originalmente los importes en pesos argentinos (total ARS 344.300.000); cada línea se convirtió dividiendo por 1.560 y redondeando a USD enteros, y los subtotales y totales son la suma de las líneas ya convertidas. Por redondeo, el presupuesto base de costos (USD 200.633) difiere en menos de 0,01 % de la conversión directa del presupuesto base original (ARS 313.000.000 ÷ 1.560 = USD 200.641). La reserva de contingencia ya no es el 10 % plano de la estimación original del equipo (ARS 31.300.000, unos USD 20.064): se calcula a partir de los riesgos (punto 9.7 y apartado 10.8).

**Metodología de estimación.** La estimación se realizó con un enfoque ascendente (bottom-up): se identificaron los recursos y las actividades necesarios para ejecutar el alcance previsto. Para los recursos humanos, el costo surge de los meses de dedicación estimados y de un costo mensual de referencia para cada perfil. Para las categorías tecnológicas y operativas se asignaron importes estimativos a los principales conceptos de gasto, según su función dentro del proyecto, y los subtotales se obtuvieron sumando los conceptos de cada categoría. Finalmente se calculó el presupuesto base y se incorporó una reserva de contingencia calculada a partir del valor monetario esperado de los riesgos (punto 9.7). Por su carácter académico, los importes son supuestos de planificación que deberían validarse con cotizaciones y análisis de costos si el proyecto se ejecutara en un contexto real.

**Criterio anti-duplicación.** Los costos de recursos humanos corresponden a la dedicación de los perfiles asignados al proyecto; las demás categorías contemplan herramientas, licencias, servicios tecnológicos, infraestructura y actividades operativas específicas. Los conceptos de monitoreo, testing, soporte y documentación deben diferenciarse según su finalidad y su etapa de ejecución.

## 10.2 Recursos humanos

Los recursos humanos representan el principal componente del presupuesto, debido a que el proyecto requiere la participación coordinada de diferentes perfiles durante las etapas de análisis, diseño, desarrollo, integración, pruebas e implementación.

| **Recurso** | **Dedicación estimada** | **Costo mensual supuesto** | **Costo estimado** |
|---|---|---|---|
| Project Manager | 6 meses | USD 5.128 | USD 30.768 |
| Analistas funcionales | 3 meses | USD 3.846 | USD 11.538 |
| Desarrolladores | 4 meses | USD 6.410 | USD 25.640 |
| Especialistas en datos y GIS | 4 meses | USD 5.128 | USD 20.512 |
| UX/UI | 2 meses | USD 3.846 | USD 7.692 |
| QA y testing | 2 meses | USD 3.846 | USD 7.692 |
| Seguridad informática | 1 mes | USD 5.128 | USD 5.128 |
| Infraestructura/DevOps | 2 meses | USD 5.128 | USD 10.256 |
| Documentación y capacitación | 1 mes | USD 2.564 | USD 2.564 |
| **Subtotal recursos humanos** |  |  | **USD 121.790** |

La estimación contempla dedicaciones parciales o específicas según la etapa del proyecto. No implica necesariamente que todos los perfiles trabajen durante todo el período de ejecución. Los meses de dedicación se estiman como dedicación efectiva a lo largo del proyecto, incluida la participación transversal de algunos perfiles en varias fases (por ejemplo, análisis, QA o infraestructura pueden intervenir también en validaciones, pruebas y puesta en funcionamiento), por lo que pueden superar la ventana de las actividades principales de ese rol en el cronograma del punto 6, que no asigna dedicación por persona.

La fórmula aplicada es: **costo estimado = meses de dedicación × costo mensual supuesto**. Por ejemplo, para el Project Manager se estima una dedicación de 6 meses a un costo mensual de referencia de USD 5.128, lo que da un costo imputado al proyecto de USD 30.768.

Los costos mensuales son valores imputados al proyecto por la dedicación de cada perfil y pueden contemplar honorarios o costos de contratación, cargas laborales y costos indirectos asociados. Por el carácter académico de la propuesta, son supuestos de planificación y no representan salarios ni cotizaciones de mercado verificados. Los importes de recursos humanos no incluyen licencias, infraestructura, servicios externos ni herramientas, que se presupuestan en las categorías correspondientes.

## 10.3 Desarrollo y tecnología

Esta categoría contempla los recursos tecnológicos necesarios para construir la solución y realizar las actividades de desarrollo y testing.

| **Concepto** | **Costo estimado** |
|---|---|
| Herramientas y ambientes de desarrollo | USD 5.128 |
| Licencias y herramientas de testing | USD 3.205 |
| Herramientas de monitoreo y gestión | USD 3.205 |
| Servicios tecnológicos complementarios | USD 4.487 |
| Herramientas de soporte y documentación | USD 3.205 |
| Otros servicios técnicos | USD 3.205 |
| **Subtotal desarrollo y tecnología** | **USD 22.435** |

Siempre que resulte técnicamente viable, se priorizará el aprovechamiento de herramientas y soluciones ya disponibles en el ecosistema tecnológico del proyecto.

## 10.4 Datos, GIS e integraciones

El proyecto depende de la disponibilidad y correcta integración de diferentes fuentes de información. Esta categoría contempla las actividades relacionadas con datos geográficos, APIs, normalización e integración.

| **Concepto** | **Costo estimado** |
|---|---|
| Preparación y normalización de datos | USD 3.205 |
| Desarrollo y configuración de APIs | USD 3.846 |
| Servicios de geocodificación y mapas | USD 2.564 |
| Integración con fuentes oficiales | USD 1.923 |
| **Subtotal datos, GIS e integraciones** | **USD 11.538** |

La utilización de servicios existentes podría reducir este componente. Por el contrario, la necesidad de desarrollar nuevas integraciones o adaptar sistemas existentes podría incrementar el costo.

## 10.5 Infraestructura y seguridad

Se contemplan los recursos necesarios para alojar la solución, almacenar información, realizar monitoreo y establecer controles básicos de seguridad.

| **Concepto** | **Costo estimado** |
|---|---|
| Infraestructura y hosting | USD 6.410 |
| Base de datos y almacenamiento | USD 3.205 |
| Monitoreo y disponibilidad | USD 2.564 |
| Seguridad y controles de acceso | USD 3.846 |
| Backup y recuperación | USD 3.205 |
| **Subtotal infraestructura y seguridad** | **USD 19.230** |

La arquitectura deberá dimensionarse de acuerdo con la cantidad esperada de usuarios, consultas al mapa, reportes ciudadanos y volumen de información geográfica.

## 10.6 Implementación y capacitación

Esta categoría contempla las actividades necesarias para preparar la puesta en funcionamiento de la solución y acompañar a los equipos responsables de su operación.

| **Concepto** | **Costo estimado** |
|---|---|
| Preparación del entorno productivo | USD 2.564 |
| Capacitación de equipos internos | USD 1.923 |
| Materiales y documentación operativa | USD 1.282 |
| Soporte durante la puesta en funcionamiento | USD 1.923 |
| **Subtotal implementación y capacitación** | **USD 7.692** |

La capacitación estará orientada principalmente a los equipos que administren la información, gestionen incidencias y utilicen las herramientas internas de seguimiento.

## 10.7 Mantenimiento inicial

Se contempla un período inicial de mantenimiento de dos meses posteriores a la puesta en producción, para atender errores, realizar ajustes menores y monitorear el funcionamiento de la solución.

| **Concepto** | **Costo estimado** |
|---|---|
| Corrección de errores iniciales | USD 6.410 |
| Soporte técnico | USD 4.487 |
| Ajustes menores y optimización | USD 3.846 |
| Monitoreo y mantenimiento | USD 3.205 |
| **Subtotal mantenimiento inicial** | **USD 17.948** |

Este monto corresponde al período inicial posterior a la puesta en producción y no representa el costo de mantenimiento permanente del sistema durante los años siguientes.

El período de dos meses se divide en dos tramos respecto de la fecha de cierre formal del proyecto (30/09/2026, ver punto 6). El importe se prorratea por días corridos, desde la puesta en producción (09/09/2026) hasta dos meses después (09/11/2026):

| **Tramo** | **Período** | **Días** | **Costo estimado** |
|---|---|---|---|
| Soporte pre-cierre | 09/09/2026 al 30/09/2026 | 21 | USD 6.179 |
| Soporte post-cierre | 01/10/2026 al 09/11/2026 | 40 | USD 11.769 |
| **Total mantenimiento inicial** | | **61** | **USD 17.948** |

El soporte pre-cierre forma parte del cronograma del proyecto. El soporte post-cierre queda fuera del cronograma y se realiza luego de la transferencia: se deberá definir la transferencia de responsabilidades al equipo operativo y confirmar la disponibilidad de recursos para completarlo. Para evitar duplicaciones, no deben volver a imputarse los costos de infraestructura, licencias ni las dedicaciones profesionales ya contempladas en otras categorías; si el mantenimiento lo realizara íntegramente el equipo interno, deberá verificarse que estos importes sean costos adicionales o recursos diferenciados respecto de los ya presupuestados.

## 10.8 Contingencia y reserva de gestión

**Reserva de contingencia.** Debido a la existencia de riesgos relacionados con integraciones, calidad de datos, disponibilidad de APIs, cambios de alcance, problemas técnicos y retrasos, se establece una reserva de contingencia igual a la suma de los valores monetarios esperados (EMV = probabilidad × impacto) de los 15 riesgos de la matriz, una vez considerado el efecto de su respuesta. El cálculo completo está en el punto 9.7.

El presupuesto base es:

- Recursos humanos: USD 121.790

- Desarrollo y tecnología: USD 22.435

- Datos, GIS e integraciones: USD 11.538

- Infraestructura y seguridad: USD 19.230

- Implementación y capacitación: USD 7.692

- Mantenimiento inicial: USD 17.948

**Presupuesto base: USD 200.633**

Reserva de contingencia (suma de los EMV residuales, punto 9.7):

**USD 41.206**

Esta reserva equivale al 20,5 % del presupuesto base. El porcentaje es un resultado del cálculo, no una regla, y reemplaza al 10 % plano de la estimación original del equipo (USD 20.063 al tipo de cambio supuesto).

La **línea base de costos** es el presupuesto base más la reserva de contingencia: USD 241.839. Es la referencia con la que se comparará el avance del proyecto.

La contingencia deberá utilizarse únicamente frente a situaciones justificadas que generen un desvío respecto de la planificación inicial. Su utilización deberá ser registrada y aprobada por el responsable del proyecto de acuerdo con el mecanismo de control de cambios definido. Se aplicará únicamente ante riesgos identificados (punto 9) que se materialicen y requieran acciones de respuesta, o ante desvíos justificados; cada utilización deberá documentarse y justificarse. Los cambios que superen las atribuciones del responsable del proyecto o modifiquen el presupuesto total aprobado deberán elevarse al Sponsor para su autorización.

**Reserva de gestión.** Es un concepto distinto: cubre eventos imprevistos o riesgos no identificados durante la planificación, no está asignada a riesgos específicos y requiere la aprobación de la alta dirección para utilizarse. No está incluida en el presupuesto total de este punto ni financiada. Su inclusión y su monto son una decisión pendiente del Sponsor. A modo de referencia, el ejemplo de la cátedra usa el 10 % del presupuesto; aplicado a la línea base de costos serían USD 24.107.

## 10.9 Presupuesto total

| **Categoría** | **Presupuesto estimado** |
|---|---|
| Recursos humanos | USD 121.790 |
| Desarrollo y tecnología | USD 22.435 |
| Datos, GIS e integraciones | USD 11.538 |
| Infraestructura y seguridad | USD 19.230 |
| Implementación y capacitación | USD 7.692 |
| Mantenimiento inicial | USD 17.948 |
| **Presupuesto base** | **USD 200.633** |
| Reserva de contingencia (EMV) | USD 41.206 |
| **PRESUPUESTO TOTAL ESTIMADO** | **USD 241.839** |

La composición del presupuesto se resume en el siguiente gráfico.

![Composición del presupuesto en USD: categorías, contingencia y línea base de costos](img/presupuesto.png)

Por lo tanto, el presupuesto estimado para la primera implementación de la Modernización del Mapa Interactivo de la Ciudad asciende a **USD 241.839**, que es la línea base de costos (presupuesto base de USD 200.633 más reserva de contingencia de USD 41.206). No incluye reserva de gestión.

El financiamiento previsto corresponde principalmente al presupuesto destinado a proyectos de modernización y transformación digital del Gobierno de la Ciudad. En el marco de la propuesta, no se contempla ningún pago por parte de los vecinos.

La posibilidad de incorporar posteriormente servicios comerciales, beneficios patrocinados o espacios de visibilidad para comercios y servicios locales se considera una **línea de evolución futura** y no forma parte del esquema financiero de la primera versión.

**Consideración final sobre el presupuesto**

El presupuesto deberá ser revisado ante modificaciones significativas del alcance, cambios en las integraciones, incorporación de nuevas funcionalidades, variaciones de costos tecnológicos o modificaciones en la estrategia de implementación.

La estimación presentada permite contar con una referencia económica inicial para evaluar la viabilidad del proyecto y mantener alineados **alcance, cronograma, recursos y costos**.
