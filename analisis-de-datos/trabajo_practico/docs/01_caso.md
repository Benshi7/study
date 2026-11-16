# 1. Definición del caso

## Tema

Elegimos trabajar con seguros de autos. En particular, con el riesgo de siniestros en el seguro de
responsabilidad civil (los daños que un conductor le causa a terceros), usando la cartera pública
freMTPL2 de una aseguradora francesa.

## Por qué es relevante

Una aseguradora tiene que poner el precio antes de saber cuánto le va a costar cada cliente. Si le
cobra lo mismo a todos, los clientes de bajo riesgo terminan pagando de más y se van a otra compañía
que les cobre menos, mientras que los de alto riesgo pagan de menos y se quedan. Con el tiempo la
cartera se llena de los perfiles más caros. Este fenómeno se conoce como selección adversa.

Por eso, saber cuánto cuesta en promedio cada perfil de cliente es la base para armar cualquier
tarifa: permite ver a quién se le está cobrando de más y a quién de menos.

## Rol y público

Presentamos el trabajo como si fuéramos el equipo de pricing (tarificación) de la aseguradora. El
público es la dirección técnica, que es quien decide si ajustar la tarifa de algún segmento. Es gente
que conoce el negocio pero no necesariamente el detalle técnico, así que los resultados los
mostramos con indicadores del negocio (frecuencia, severidad, prima pura) y no con código.

## Pregunta

¿Qué perfiles de conductor y de vehículo tienen mayor costo esperado de siniestros (prima pura), y
cuánto se apartan del promedio de la cartera?

## Hipótesis

| # | Hipótesis | Cómo la analizamos |
|---|-----------|--------------------|
| H1 | El historial del conductor (BonusMalus) separa el riesgo más que la edad. | Frecuencia por franja de edad y de BonusMalus, y el cruce entre las dos. |
| H2 | En las zonas más densas o urbanas hay más frecuencia de siniestros, pero no necesariamente más severidad. | Frecuencia y severidad por zona (`Area`) y por tramos de densidad. |
| H3 | El costo está dominado por unos pocos siniestros muy grandes, más que por el perfil del asegurado. | Qué porcentaje del costo total explican los siniestros más grandes. |

Sobre H1: que un BonusMalus alto tenga más siniestros es esperable, porque el BonusMalus sube
justamente cuando el conductor tiene siniestros. Lo que queremos ver es si pesa más que un dato del
perfil como la edad, sabiendo que los conductores nuevos (y por lo tanto jóvenes) arrancan con un
BonusMalus alto.

Las hipótesis pueden confirmarse o no. Si alguna no se cumple, eso también es un resultado.

## Conceptos que usamos

| Término | Qué es | Cómo se calcula |
|---------|--------|-----------------|
| Exposición | Tiempo que la póliza estuvo vigente, en años (0,5 es medio año). | Viene en el dataset (`Exposure`). |
| Frecuencia | Cantidad de siniestros por año asegurado. | Siniestros ÷ exposición. |
| Severidad | Costo promedio de un siniestro. | Monto total ÷ cantidad de siniestros. |
| Prima pura | Costo esperado de siniestros por año de póliza. | Frecuencia × severidad, que es lo mismo que monto total ÷ exposición. |
| Relatividad | Cuánto se aparta un segmento del promedio. | Indicador del segmento ÷ indicador de toda la cartera. Por ejemplo, 1,30 quiere decir que cuesta un 30 % más. |

Dos aclaraciones. La frecuencia no es el promedio de siniestros por póliza: como las pólizas no
estuvieron vigentes el mismo tiempo, hay que dividir por la exposición. Y la prima pura es el costo,
no el precio que paga el cliente: no incluye gastos, comisiones ni ganancia.

## Alcance y límites iniciales

- El dataset no tiene la prima que se le cobró a cada cliente, así que medimos el costo esperado y no
  la rentabilidad.
- Solo cubre responsabilidad civil. No incluye daños propios ni robo.
- No hay fechas, por lo que no podemos analizar la evolución en el tiempo.
- La marca del vehículo está anonimizada (B1, B2, ...): podemos comparar marcas pero no saber cuáles son.
- Suponemos que los montos están en euros.
- Lo que encontremos son asociaciones, no causas.

## Cómo contamos la historia

Ordenamos el análisis en cuatro preguntas. Primero, si podemos confiar en los datos: antes de
calcular nada conciliamos pólizas y siniestros y mostramos qué estaba mal y cómo lo resolvimos.
Después, quién es más riesgoso, comparando frecuencia y severidad por edad, BonusMalus, zona y
vehículo (H1 y H2). Tercero, cuánto debería costar cada perfil, pasando a prima pura y relatividades
y viendo cuánto pesan los siniestros grandes (H3). Y por último, qué no podemos afirmar con estos
datos, para que la dirección técnica sepa hasta dónde usar las conclusiones.
