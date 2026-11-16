# Medallion: la transformación pertenece a la capa de destino

En la lección 0013 contestó bien las tres preguntas de Medallion, pero dudó: "eliminar duplicados pasa entre Bronze y Silver; a Silver ya llegaría limpio". Se le dio el modelo "capa = dato + proceso que lo produce": el job que deduplica es el proceso de Silver, y Bronze nunca transforma.

**Evidence:** 27/09, lección 0013. Falló solo la dirección de las FK en el esquema estrella: las FK están en la fact y apuntan a la PK de cada dimensión. Dijo que fue por distracción y que ya lo entendió. En el recall hizo bien N:M (tabla intermedia) e integridad referencial (toda FK apunta a una PK existente).

**Implications:** Es otra instancia del sesgo de ingeniería ([[0001-experiencia-previa-data-engineer]]): piensa en el pipeline y no en la etiqueta de la cátedra. Regla para el examen: limpiar es Silver, agregar y modelar es Gold, crudo es Bronze. Se agregó un recuadro de trampa en la lección 0013. Todavía no contestó la pregunta de chequeo del JSONB (relacional) de [[0013-tipo-de-base-es-el-motor]].

**Verificado 27/09:** clasificó como Gold un job que agrega ventas mensuales por región. Además detectó que la pregunta de chequeo tenía un defecto: el job leía de Bronze, salteando Silver. Tenía razón; en el flujo canónico Gold lee de Silver. Clasifica por lo que el job produce y además cuestiona una premisa mal armada: buena señal.
