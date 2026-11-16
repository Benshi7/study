# Análisis de Datos I Glossary

Terminología de la cátedra (UNICABA 2026) para el bloque "Introducción a los datos". Solo se incluyen los términos que el estudiante ya usó correctamente.

## Calidad de datos

**Consistencia**:
Dimensión de calidad que evalúa si el mismo hecho tiene el mismo valor en todos los sistemas y reportes.
_Avoid_: coherencia, sincronización

**Completitud**:
Dimensión de calidad que evalúa si cada registro tiene todos los atributos que el negocio define como obligatorios; un campo opcional no cuenta.
_Avoid_: porcentaje de nulls, cobertura

**Tempestividad**:
Dimensión de calidad que evalúa si el dato está disponible a tiempo; el dato puede ser correcto pero llegar tarde.
_Avoid_: actualidad, frescura, latencia

**Duplicados** (unicidad):
Dimensión de calidad que evalúa si un registro se repite innecesariamente.
_Avoid_: redundancia

**Precisión**:
Dimensión de calidad que evalúa si el valor refleja con exactitud la realidad que se quiso registrar.
_Avoid_: exactitud numérica, accuracy

## Tipos de datos

**Dato cualitativo ordinal**:
Dato no cuantificable cuyas categorías tienen un orden que importa (alto / medio / bajo, calificaciones).
_Avoid_: categórico ordenado, escala

## Tipos de análisis

**Análisis descriptivo**:
Análisis que resume una muestra con valores característicos (media, mediana, desvío) y responde "¿qué pasó?". Comparar la misma métrica entre períodos sigue siendo descriptivo.
_Avoid_: reporting, estadística básica

**Análisis exploratorio**:
Análisis que cruza variables o segmentos en busca de patrones o relaciones que no se ven a primera vista con el descriptivo. Produce una afirmación, no una hipótesis.
_Avoid_: EDA, data mining

**Análisis diagnóstico**:
Análisis que profundiza en las causas de un comportamiento y responde "¿por qué pasó?".
_Avoid_: análisis causal, root cause

**Análisis prescriptivo**:
Análisis que usa los resultados de los otros tipos para responder "¿qué tenemos que hacer?".
_Avoid_: recomendación, análisis de decisión

## Roles C-level

**CDO (Chief Data Officer)**:
Director de Datos: define la estrategia de uso y explotación de los datos y las políticas de gestión, de forma transversal a toda la empresa.
_Avoid_: Chief Development Officer, Chief Digital Officer

**CBDO (Chief Business Development Officer)**:
Impulsa el crecimiento de la empresa a través de nuevas oportunidades de negocio. El CEO, en cambio, fija la visión y la estrategia general.
_Avoid_: director de desarrollo, CDO

## Bases de datos

**Integridad referencial**:
Garantía del modelo relacional de que toda FK apunta a un registro existente, a través de la PK de la otra tabla.
_Avoid_: integridad (la dimensión de calidad: "¿llegó sin romperse?")

**Tabla intermedia**:
Tabla que resuelve una relación N:M entre dos tablas, por ejemplo Detalle_Pedido entre Productos y Pedidos.
_Avoid_: tabla puente, junction table
