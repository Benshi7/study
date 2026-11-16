# 7. Análisis exploratorio

El EDA está en dos notebooks:

- `notebooks/02_historia.ipynb` responde las tres hipótesis con edad, BonusMalus y zona. De ahí salen
  los gráficos de la presentación (`presentacion/img/a1_*` a `a3_*`).
- `notebooks/03_eda.ipynb` completa el análisis con el resto: estructura del dataset, estadísticas
  descriptivas, distribuciones, variables categóricas, correlaciones, variables del vehículo,
  densidad y región, cruces entre variables y outliers.

El `03_eda` lee `export/polizas.csv` y `export/siniestros.csv`, que es el mismo dataset que usa Power
BI.

## Cómo lo trabajamos

- Los indicadores se calculan sumando y dividiendo (siniestros sobre exposición), nunca promediando
  por póliza.
- Al lado de cada indicador mostramos cuánta exposición tiene el segmento. Un resultado sobre el
  0,5 % de la cartera no vale lo mismo que uno sobre el 25 %.
- Cada frecuencia lleva un intervalo de confianza del 95 %, con la aproximación de Poisson.
- La prima pura la medimos con tope en el percentil 99 (16.451 €), por lo que se ve en H3.
- Cuando una variable parecía importante, la comparamos dentro de grupos parecidos para ver si el
  efecto era propio o venía de otra variable con la que está mezclada.

## Resultados de las hipótesis

**H1. El BonusMalus pesa más que la edad: se confirma, con un matiz.** Mirando cada variable por
separado, los conductores de 18 a 21 años tienen 2,86 veces la frecuencia promedio y los que tienen
BonusMalus con recargo (más de 100), 4,77 veces. En prima pura con tope, 3,56 y 4,92 veces. Pero las
dos variables están relacionadas (correlación de −0,57): un conductor nuevo arranca con BonusMalus
100, así que los jóvenes tienen BonusMalus alto por ser nuevos. Comparando conductores con el mismo
BonusMalus, la diferencia por edad se achica mucho.

**H2. En la ciudad se choca más seguido, no más caro: se confirma.** La frecuencia relativa va de 0,74
en la zona A (rural) a 1,30 en la zona E. Dividiendo la cartera en deciles de densidad, va de 0,70 a
1,32. La severidad no sigue ese orden.

**H3. Pocos siniestros grandes dominan el costo: se confirma.** El 1 % de los siniestros explica el
38 % del costo. Los tres siniestros más grandes (4,1, 1,4 y 1,3 millones) son de conductores de 18 a
20 años, y alcanzan para que, sin tope, esa franja parezca 13 veces más cara que el promedio. Con el
tope en el percentil 99, la relación baja a 3,6 veces. El tope recorta el 30,7 % del monto total.

## El resto de las variables

| Variable | Qué muestra | ¿Es confiable? | ¿Serviría para tarifar? |
|---|---|---|---|
| BonusMalus | El efecto más fuerte: de alrededor de 0,7 a 4,9 veces el promedio | Sí, aunque la franja de más de 100 es solo el 1 % de la cartera | Sí, es la principal |
| Edad | 18 a 21 años, unas 3,6 veces | Está mezclada con el BonusMalus | Sí, pero junto con el BonusMalus |
| Densidad | Sube de forma ordenada, de 0,70 a 1,32 | Sí: cada decil tiene alrededor del 10 % de la cartera | Sí, usando solo una entre densidad, zona o región |
| Combustible | Los diésel tienen un 14 % más de frecuencia | Sí: la diferencia se mantiene dentro de cada edad, BonusMalus y zona | Sí |
| Antigüedad del vehículo | Los autos de 16 años o más cuestan alrededor de un 30 % menos | Sí, el intervalo no llega a 1 | Sí, en pocas franjas |
| Región | El sudeste y París son más caros, Centre más barato | En parte: buena parte del efecto es densidad, y las regiones chicas son inestables | Con cuidado, y no junto con la densidad |
| Potencia | Efecto débil, sube algo en las potencias altas | Las potencias de 12 o más casi no tienen pólizas | Agrupada en pocas franjas |
| Marca | B12 sale barata y B11 cara | Poco: B12 está mezclada con autos nuevos y la marca es anónima | No por sí sola |

## Outliers

Los montos tienen una cola muy larga: el máximo es de 4.075.400 € con una mediana de 1.172 €. No los
consideramos errores sino siniestros reales, por eso no los borramos y en su lugar usamos el tope.
También aparecen valores repetidos que no son outliers sino montos fijos: 1.204 € aparece en el 18 %
de los siniestros y 1.128,12 € en el 12 %. Investigando, encontramos que corresponden a la
convención IRSA, un acuerdo entre aseguradoras francesas que fija un monto para los choques chicos
entre dos autos (ver documento 9).

Los vehículos de 99 o 100 años y los conductores de más de 90 quedan en las franjas de los extremos,
así que no mueven los resultados.

## Control del lote sospechoso

Repetimos el análisis sin las pólizas del lote de `IDpol` ≤ 24.500 (ver documentos 4 y 5) y las
relatividades no cambian. La decisión de recalcular y marcar ese lote, en vez de borrarlo, no afecta
las conclusiones.

## Qué nos deja el EDA

1. Además del conductor (edad y BonusMalus), el lugar donde vive (densidad) y el auto (combustible y
   antigüedad) también separan perfiles de riesgo.
2. Varias variables se pisan entre sí: edad con BonusMalus, densidad con zona y región, marca con
   antigüedad. Mirar una por vez puede exagerar o esconder efectos. El paso siguiente sería un modelo
   que las analice todas juntas.
3. Aparecieron limitaciones nuevas: casi un tercio de los montos son importes fijos de convención, y
   la cartera está concentrada en Centre-Val de Loire, así que no representa a toda Francia.
