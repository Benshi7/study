# Completitud se mide contra la definición del negocio, no contando celdas vacías

Creía que un campo vacío baja la completitud aunque sea opcional (respondió 50% cuando era 100%). Para la cátedra, la completitud se mide por registro contra los atributos que el negocio define como obligatorios: un dato opcional no se considera.

**Evidence:** Falló la pregunta de los 10 clientes con el segundo nombre vacío (25/09). Verificado el 27/09: acertó las preguntas de completitud en la lección 0001 y dijo que le quedó claro.

**Implications:** Es un malentendido que viene del hábito de DE (profiling cuenta % de nulls por columna). Hay que separar **profiling** (medir) de **completitud** (juicio contra una regla). Repetir en la práctica espaciada.
