# Correlación entre la consigna, las clases y el documento maestro

Revisión del 12/10/2026 sobre `src/*.md` (documento consolidado). «p» = diapositiva de la cátedra (`raw/`). Las diapositivas que son imagen (matriz de interesados, matriz de comunicación, respuesta a riesgos, presupuestación) se miraron como imagen. **Clase 7 (Design Thinking) y Clase 8 no están en `raw/`**: el punto 4 no se puede contrastar con la cátedra.

## 1. Matriz: qué pide la cátedra → dónde está → estado

| Punto de la consigna | Qué piden las clases | Dónde está en el maestro | Estado |
|---|---|---|---|
| 1. Carátula | Consigna | `01-caratula.md` | Parcial: falta la nómina (`[Integrantes del grupo]`) |
| 2. Índice | Consigna | `02-indice.md` (automático) | Cubierto: 108 entradas con página, verificado en el PDF |
| Storytelling | Consigna: «no deben ser puntos sueltos» | `02b` + frase de enlace al inicio de cada punto | Cubierto: están las 8 transiciones entre puntos (3→4 se agregó; 7→8 y 8→9 se reforzaron) |
| 3. Canvas | Clase 1 p3–28: los 9 bloques; p6–9 propuesta de valor; p10–11 segmentos (priorizar); *Ejemplo Clase*: 9 bloques + «qué fortalecer» | `03-canvas.md`: figura de la Opción B + lista de 9 bloques del equipo | Inconsistente: la lista (visitantes, turistas, transporte) no coincide con la figura (hogares) |
| (Clase 1, OKR) | p29–33 OKR y objetivos SMART | Sin menciones (SMART, OKR) | Falta; no lo pide la consigna |
| 4. Design Thinking | Clase 7 (no disponible) | `04-design-thinking.md`: 5 fases, 5 figuras, test simulado | Parcial: sin cátedra para contrastar; marcado como investigación simulada |
| 5. Charter | Clase 3 p13–16: 13 elementos en 3 partes; `Project_Charter_Template5`: 24 campos | `05-project-charter.md`: 12 secciones (≈5.900 palabras) | Parcial: cubre 9 de 13. Faltan o son débiles: requisitos de alto nivel, presupuesto de alto nivel (5.8 solo categorías, sin cifra), autoridad del Director (5.11.2 solo responsabilidades), requisitos de aprobación y firmas. Objetivos sin metas medibles (p14) |
| 6. Gantt | Clase 3 p22–26 EDT; p30–35 secuencia; p36–38 duraciones; p39–49 Gantt, PERT y camino crítico; p51–56 línea base | `06-gantt.md` + Anexo A (40 actividades, CPM, 8 hitos) | Cubierto en Gantt, camino crítico e hitos. Falta EDT y línea base de cronograma; columna «Responsable» vacía en el Excel |
| 7. Stakeholders | Clase 3 p17–21: matriz poder × interés (2×2: gestionar de cerca / mantener satisfecho / mantener informado / monitorear) | `07-stakeholders.md`: 15 filas, las 4 estrategias | Cubierto en tabla; falta el cuadro 2×2 de p21 (mejora menor) |
| 8. Comunicación | Clase 6 p12 formal/informal, escrita/verbal; p15–18 barreras; p20 matriz (formato, emisor, receptor, medio, tipo, frecuencia, «requiere respuesta»); p21–28 negociación | `08-comunicacion.md`: matriz de 12 filas (qué, destinatarios, responsable, frecuencia, canal) | Parcial: faltan tipo de comunicación y «requiere respuesta»; barreras y negociación sin desarrollo |
| (Cambios) | Clase 5 p42–46, Clase 6 p4–8 | Charter 5.9.2–5.9.3 | Cubierto |
| 9. Riesgos | Clase 5 p17 redacción «Ante X, podría ocasionar Y, lo que impactaría en Z»; p27 importancia = P × I; p31 EMV = P × I y «con este valor generamos la reserva de contingencia»; p33–35 evitar / mitigar / transferir / aceptar; p20–21 riesgos positivos; p7–14 FODA | `09-riesgos.md`: 15 riesgos, P × I en escala 1–5 (aritmética verificada), acciones y contingencia | Parcial: sin EMV, respuestas solo «Mitigar» y «Evitar», sin riesgos positivos, sin FODA |
| 10. Presupuesto | Clase 4 p13–14 clasificación; p15 etapas; p18 técnicas de estimación; p19–21 contingencia vs gestión; p22–24 línea base y suma ascendente (actividad → paquete → proyecto → + contingencia = línea base → + reserva de gerencia = presupuesto); p26–29 ingresos; p5–10 PESTEL | `10-presupuesto.md`: 9 categorías + RRHH por perfil, en ARS (sumas verificadas: RRHH 190 M, base 313 M, total 344,3 M) | Parcial: contingencia plana, sin reserva de gestión, sin línea base, sin PESTEL; ingresos tratados (10.1) |

## 2. Incoherencias entre secciones (por prioridad)

| # | Incoherencia | Evidencia | Decisión del grupo que la cierra |
|---|---|---|---|
| 1 | La contingencia es 10 % plano de la base y no sale de la matriz de riesgos, que no tiene valor monetario. El punto 10 promete «reservas para la mitigación de los riesgos identificados». Clase 5 p31 y Clase 4 p19–24 piden otra cosa | `10-presupuesto.md:3`, `:127`, `:145`; `09-riesgos.md:54–70` | Escenario A o B del presupuesto y base de la reserva de gestión; pasar a USD |
| 2 | Inicio y duración: Charter dice inicio 10/04 y «6 meses (24 semanas)»; el Gantt empieza el 01/04 y dura 126 días hábiles | `05-project-charter.md:21–24`; `06-gantt.md:37`; `12-anexo-a.md:7`, `:134` | Fecha de inicio oficial (01/04 o 10/04) |
| 3 | 8 hitos en el Charter, el Gantt y el Excel, pero 7 «Gates» en 6.5; nombres distintos («Finalización de integraciones» vs «Integraciones validadas») | `05-project-charter.md:860–885`; `06-gantt.md:39–52`, `:80–92` | 8 hitos o 7 gates |
| 4 | Charter sin cifras de presupuesto y con 12 riesgos; el punto 9 tiene 15 y el 10 tiene $344,3 M. «Baja adopción por parte de comercios» no tiene ID en la matriz | `05-project-charter.md:409–475`, `:517–530`; `09-riesgos.md:56–70` | Charter en la plantilla de 24 campos (Charter largo como anexo) |
| 5 | La lista de segmentos del Canvas (vecinos, turistas, transporte, actores culturales) no coincide con la figura ni con Design Thinking (hogares) | `03-canvas.md:15` | Qué Canvas es la referencia del punto 3 |
| 6 | El resumen ejecutivo dice que Design Thinking sirve para «empatizar profundamente con los ciudadanos» y testear, sin aclarar que es simulado; el punto 4 sí lo aclara | `02b-resumen-ejecutivo.md:13` vs `04-design-thinking.md` (nota sobre el método) | Ninguna: corrección de redacción pendiente de aprobación |
| 7 | La matriz de stakeholders dice estar alineada con Canvas y Charter e incluye USIG, Hacienda y miBA, que no aparecen en el Canvas ni en el Charter | `07-stakeholders.md:46`; `rg` sin resultados en `03` y `05` | Reconciliar actores entre Canvas, Charter y matriz |
| 8 | Mantenimiento inicial de $28 M «posterior a la puesta en producción» (09/09), pero el cierre es el 30/09: quedan 3 semanas | `10-presupuesto.md:111–123`; `06-gantt.md:51–52` | Mantenimiento dentro o fuera del alcance del proyecto |
| 9 | La priorización de riesgos nombra 8 de los 13 riesgos Alto o Crítico (omite R03, R07, R10, R13, R14) | `09-riesgos.md:98–114` | Ninguna: ampliar o aclarar el criterio |
| 10 | El encabezado de la tabla de hitos dice «Matriz» en lugar de «Hito» (errata del original, dejada a propósito) | `06-gantt.md:43` | Ninguna: se corrige si el grupo lo aprueba |

Coherentes (verificado): nombre del proyecto, 8 fases y 8 hitos en 5.12, 6.3 y Anexo A (las fechas figuran solo en 6.3 y Anexo A y son iguales); 15 riesgos R01–R15 con nivel = P × I; totales del presupuesto; contingencia 10 % repetida igual en Canvas, resumen ejecutivo y punto 10; ingresos comerciales fuera de la primera implementación en Canvas, Charter y presupuesto.

## 3. Cambios de hoy en el maestro

- Segmento «hogares de la Ciudad» en el punto 4 y en las figuras del Canvas y de la historia de usuario (CAMBIOS E.21–E.22). La persona Lucía conserva «dos chicos en edad escolar» como ejemplo de un hogar.
- Frases de enlace: nueva 3→4; 7→8 y 8→9 reforzadas (CAMBIOS E.23–E.24).
