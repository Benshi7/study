# 9. Conclusiones, limitaciones y mejoras

## Conclusiones

Volviendo a la pregunta del caso, los perfiles con mayor costo esperado son los conductores con
BonusMalus con recargo (4,9 veces el promedio en prima pura con tope) y los de 18 a 21 años (3,6
veces). La zona urbana también suma, sobre todo porque choca más seguido.

| Hipótesis | Resultado |
|---|---|
| H1. El historial pesa más que la edad | Se confirma, con un matiz: edad y BonusMalus están mezclados, y buena parte del efecto de la edad es en realidad BonusMalus. |
| H2. Más frecuencia en zonas urbanas, no más severidad | Se confirma: la frecuencia va de 0,70 a 1,32 según la densidad y la severidad no sigue ese orden. |
| H3. Pocos siniestros grandes dominan el costo | Se confirma: el 1 % de los siniestros es el 38 % del costo, y tres siniestros alcanzaban para que los jóvenes parecieran 13 veces más caros. |

Antes de todo eso, una conclusión sobre los datos: si no hubiéramos conciliado las dos tablas, la
frecuencia habría quedado un 36 % más alta.

## Datos externos que usamos

| Dato | Para qué lo usamos | Fuente |
|---|---|---|
| Origen del dataset | Saber qué es cada tabla y qué versión usamos. La copia de Kaggle tiene 678.013 pólizas y 26.639 siniestros; la versión actual de CASdatasets ya viene depurada y es algo más chica. | [CASdatasets][cas], [OpenML][openml], [copia de Kaggle][kaggle] |
| Regla del BonusMalus | Explicar por qué los jóvenes tienen BonusMalus alto y validar el rango 50 a 350. En Francia el coeficiente arranca en 1,00, baja un 5 % por cada año sin siniestros hasta un mínimo de 0,50 y sube un 25 % por cada siniestro con responsabilidad, hasta 3,50. En el dataset está multiplicado por 100. | [Resumen del sistema][bm1], [Asamblea Nacional de Francia][bm2] |
| Regiones de 2016 | Agrupar las 21 regiones viejas en las 13 actuales, para el EDA y el mapa. La ley 2015-29 unió regiones sin cambiar sus departamentos. | [Vie-publique][ley1], [texto de la ley][ley2] |
| Convención IRSA | Explicar los montos repetidos. Es un acuerdo entre aseguradoras francesas que fija un monto para los daños materiales de choques entre dos vehículos (1.678 € en 2021, 2.030 € en 2026). | [Le Lynx][irsa1], [Resilier][irsa2], [Leocare][irsa3] |
| Coordenadas de las regiones | Ubicar las burbujas del mapa. Son centros aproximados que cargamos nosotros, no datos oficiales. | |

El dataset no dice de qué año es. Como usa las regiones de antes de 2016, sabemos que es anterior a
esa fecha, pero no podemos precisar el año.

## Limitaciones de los datos

| # | Limitación | Qué implica |
|---|---|---|
| D1 | No está la prima que se cobró | Medimos el costo esperado, no la rentabilidad. No podemos decir qué segmento da pérdida. |
| D2 | Solo responsabilidad civil | No incluye daños propios, robo ni cristales. |
| D3 | No hay fechas | No podemos ver evolución en el tiempo ni estacionalidad. |
| D4 | Los datos son anteriores a 2016 | Los costos de reparación y el parque automotor cambiaron. Las relatividades envejecen mejor que los montos en euros. |
| D5 | Casi un tercio de los montos son importes fijos de la convención IRSA (1.204 € en el 18 % de los siniestros y 1.128,12 € en el 12 %) | En esos casos el monto no es el costo real del choque, y la severidad queda "aplastada" alrededor de esos valores. |
| D6 | Una sola aseguradora, con el 29 % de la exposición en Centre-Val de Loire | Los resultados describen esta cartera, no el mercado francés. |
| D7 | Falta la región Lorraine | Grand Est aparece incompleta en el mapa. |
| D8 | Marca anonimizada | Podemos comparar marcas pero no saber cuáles son. |
| D9 | Lote de `IDpol` ≤ 24.500 con conteos inválidos (9.139 pólizas) | Recalculamos el conteo y lo marcamos. Comprobamos que no cambia los resultados. |
| D10 | 195 siniestros sin póliza | Es un costo real que no podemos asignar a ningún perfil. |
| D11 | Los montos podrían incluir reservas | Si un siniestro estaba abierto, su monto es una estimación que puede cambiar. El dataset no lo aclara. |
| D12 | Faltan variables importantes, como los kilómetros recorridos o el uso del auto | Efectos como el del diésel o la antigüedad del auto probablemente reflejan cuánto se maneja, y eso no lo podemos medir. |
| D13 | Valores dudosos que dejamos (vehículos de 99 o 100 años, conductores de más de 90, exposiciones de menos de 0,01) | Son pocos y quedan en las franjas de los extremos. |

## Limitaciones del análisis

| # | Limitación | Por qué importa |
|---|---|---|
| A1 | Asociación no es causa | Que los diésel choquen más no significa que el motor diésel cause choques: puede tener que ver con quién los maneja y cuánto. |
| A2 | Hay variables mezcladas | Edad con BonusMalus, densidad con zona y región, marca con antigüedad. Mirar una variable por vez puede exagerar o esconder efectos. |
| A3 | Los segmentos más caros son los más chicos | Los de 18 a 21 años son el 1,2 % de la exposición y los BonusMalus de más de 100, el 1,0 %. Sus números son menos estables. |
| A4 | El tope cambia los resultados | Sin tope los jóvenes parecen 13 veces más caros y con tope 3,6. Elegimos el percentil 99, pero es una decisión nuestra. |
| A5 | Son relatividades simples, no una tarifa | Una tarifa real estima todos los efectos juntos y suma gastos, impuestos y margen. |
| A6 | Los intervalos de confianza son aproximados | Los calculamos solo para la frecuencia. La prima pura no tiene intervalo porque también depende de la severidad, que varía mucho. |
| A7 | No validamos con otros datos | Medimos lo que pasó en esta cartera, pero no probamos si las relatividades funcionan para pólizas nuevas. |

## Mejoras posibles

| Mejora | Qué resolvería |
|---|---|
| Un modelo multivariado (GLM de Poisson para la frecuencia y Gamma para la severidad) | Separaría los efectos de cada variable cuando están mezcladas (A2 y A5). |
| Separar los datos en una parte para calcular y otra para probar | Permitiría saber si los resultados se sostienen (A7). |
| Ajustar los segmentos chicos hacia el promedio (credibilidad) | Haría más estables los números de los segmentos con poca exposición (A3). |
| Conseguir las primas cobradas | Permitiría calcular la rentabilidad real por segmento (D1). |
| Conseguir kilometraje y uso del vehículo | Ayudaría a explicar los efectos del combustible y la antigüedad (D12). |
| Tener varios años de datos | Permitiría ver tendencias y si las relatividades se mantienen (D3 y D4). |
| Separar los montos de convención de los costos reales | Daría una severidad más realista (D5). |
| Un mapa con los límites oficiales de las regiones | Reemplazaría las burbujas por un mapa más preciso. |

## Fuentes

Consultadas en noviembre de 2026.

- [CASdatasets, French Motor Third-Part Liability datasets][cas]
- [OpenML, French-Motor-Claims-Datasets-freMTPL2freq][openml]
- [Copia de Kaggle, vía Baselight][kaggle]
- [Bonus-malus: coeficientes y cálculo][bm1]
- [Asamblea Nacional de Francia, respuesta sobre el coeficiente de reducción-aumento][bm2]
- [Vie-publique, ley del 16/01/2015 sobre la delimitación de las regiones][ley1]
- [Ley n.° 2015-29 del 16/01/2015][ley2]
- [Le Lynx, convención IRSA][irsa1]
- [Resilier.com, monto IRSA 2021][irsa2]
- [Leocare, monto IRSA 2026][irsa3]

[cas]: https://dutangc.github.io/CASdatasets/reference/freMTPL.html
[openml]: https://api.openml.org/d/43593
[kaggle]: https://baselight.app/u/kaggle/dataset/karansarpal_fremtpl2_french_motor_tpl_insurance_claims
[bm1]: https://www.toutsurmesfinances.com/assurance/definition-calcul-coefficients-connaitre-son-bonus-malus-auto-dans-son-assurance.html
[bm2]: https://questions.assemblee-nationale.fr/dyn/10/questions/QANR5L10QE39014.pdf
[ley1]: https://www.vie-publique.fr/loi/20720-elections-regionales-elections-departementales-calendrier
[ley2]: https://www.puy-de-dome.gouv.fr/contenu/telechargement/10160/112045/file/LOI_No2015-29_DU_16_JANVIER_2015_-_joe_20150117_0001.pdf
[irsa1]: https://www.lelynx.fr/assurance-auto/sinistre/indemnisation/convention-irsa/
[irsa2]: https://www.resilier.com/guides/assurances/assurance-auto-2022
[irsa3]: https://leocare.eu/fr/assurance-auto-en-ligne/sinistre/indemnisation/convention-irsa/
