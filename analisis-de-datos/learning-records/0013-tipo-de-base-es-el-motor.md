# Tipo de base = el motor según su propósito, no el stack real

En la lección 0012 (10 de 12) respondió "documental" para "dashboards analíticos sobre millones de registros"; la respuesta es columnar. El otro error, en N:M, fue un misclick. Él mismo planteó la duda: en su trabajo usa JSONB en Postgres y analiza datos relacionales de forma columnar en Databricks o como DataFrame.

**Evidence:** 27/09, lección 0012. En el slide (`unicaba_fundamentos_sql.pdf`) dice "Relacionales, NoSQL, columnares y más" y "Documentales (NoSQL)": para la cátedra, NoSQL es documental y la columnar es una categoría aparte.

**Implications:** Se dieron tres ejes que no hay que mezclar:
1. **Tipo de base**: el motor y su propósito. Es lo que evalúa la cátedra.
2. **Tipo de columna** dentro del motor: JSONB no convierte a Postgres en documental.
3. **Herramienta o formato de análisis**: Databricks, Parquet o pandas no cambian el tipo de la base de origen.

Su caso del trabajo (relacional para operar, columnar para analizar) es el flujo OLTP → OLAP de la lección 0013. Es otra instancia de [[0007-el-enunciado-define-el-mundo]]: clasificar por la palabra clave del caso de uso. Se agregó un recuadro de trampa en la lección 0012.
