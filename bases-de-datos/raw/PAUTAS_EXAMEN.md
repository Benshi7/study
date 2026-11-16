Parcial de Base de Datos — pautas de la clase

Sep 17, 2026 · @Bruno

El parcial es el jueves que viene a las 18:30, en papel, dura una hora exacta, y hay que aprobar teoría y práctica por separado: sacar todo de una parte y nada de la otra es desaprobado.

Formato y tipo de preguntas

La cantidad de preguntas no quedó cerrada. Primero dijo "cinco preguntas… o no, menos va a ser: cuatro preguntas teóricas seguramente y tres o cuatro prácticas", y más adelante "yo supongo que vamos a hacer tres y tres, algo así".

• Teoría: preguntas abiertas para desarrollar, más "algún multiple choice por ahí puede ser que tengan". Son puntuales y suelen pedir justificación ("¿por qué?", "justifique").

• Práctica: ejercicios, no preguntas: un diagrama entidad-relación / MER y uno de normalización.

• Es en papel, la hoja la dan ellos. No hace falta llevar computadora, y hay que dibujar a mano.

• No hay examen modelo de años anteriores: "no vamos a tomar nada que no hayamos dado".

Cómo se aprueba

No es 50% y 50% promediable: hay que aprobar las dos partes por separado. Lo aclaró respondiendo a un compañero que preguntó justamente eso.

Si toma…

Hace falta…

5 preguntas por parte

3 de teórica y 3 de práctica, para tener un 4

3 preguntas por parte

2 de teórica y 2 de práctica

El ejemplo que dio: 5 de teoría bien y 2 de práctica → el examen es un 2. Aclaró que el caso típico es al revés: el que ya trabaja con bases de datos resuelve la práctica fácil, no estudia la teoría y desaprueba.

El recuperatorio es del examen completo, no de la parte que falló: "se va a recuperar el primer examen o el segundo examen".

Qué entra de teoría

Todo lo visto desde la clase 1 hasta la de hoy, y sale de los PPT: "si se leen todo eso y lo estudian, prácticamente tienen aprobada la parte teórica".

• Índices: nombre de los tipos y para qué sirve cada uno, qué beneficio tiene cada uno. Dio una pregunta textual: ¿cuál de todos los índices ordena físicamente los campos? → el agrupado, más el "justifique".

• Transacciones: en algún parcial tomó las definiciones de ACID.

• Normalización: nombrar las tres formas normales y cuál es el fin que busca la normalización.

• Modelo entidad-relación: relaciones unarias y binarias, atributo derivable (qué es y para qué se usa), historicidad.

• Especialización: exclusiva o solapada, y la parte de exclusividad.

• Notación de memoria, porque no van a tener la herramienta que dibuja sola: atributos multivaluados (doble elipse), elipse punteada o no, cardinalidades uno a uno / uno a muchos y dónde va la pata de gallo.

Qué entra de práctica

Dos ejercicios que "van de cajón": modelado y normalización.

• Modelado (DER / MER): un enunciado corto del estilo de los que hicieron en clase con el otro profesor — mencionó libros, autos, farmacia, celulares — para armar el diagrama entidad-relación.

• Normalización: una tabla con campos que hay que descomponer en n tablas, poniendo la clave primaria de cada una.

También dijo que la parte de normalización puede venir mezclada: una pregunta teórica sobre las formas normales y después el ejercicio.

Errores típicos que marcan

Los nombró como los que ven siempre en los exámenes:

1\. Modelar los campos calculados. Si la tabla trae el precio y un total que es la multiplicación, ese campo derivado no va cuando se pasa a las tablas normalizadas. "Si lo ponen, está mal".

2\. No poner las claves primarias de las tablas resultantes.

3\. En teoría, no acordarse para qué sirve cada tipo de índice.

