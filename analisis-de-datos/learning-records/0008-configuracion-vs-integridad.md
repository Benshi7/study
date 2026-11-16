# Configuración es "nació mal"; integridad es "se rompió después"

Clasificó el caso de las fechas `2026/25/09` (con estándar AAAA-MM-DD) como integridad, pensándolo desde el código. Lo corrigió solo: configuración es que el dato no cumple el estándar o requerimiento definido. Se le dio el modelo "vida del dato" (nace → viaja → se usa) con la pregunta clave "¿estuvo bien alguna vez?".

**Evidence:** Lección 0001, 27/09: 8 de 9, solo falló configuración y explicó bien por qué.

**Implications:** Resto de las dimensiones consolidadas (completitud con opcionales ya OK: ver [[0002-completitud-contra-definicion-de-negocio]]). Tempestividad la entiende, pero todavía necesita recordar que la premisa es "hay un error" ([[0007-el-enunciado-define-el-mundo]]). En el repaso espaciado, volver a preguntar configuración vs integridad.
