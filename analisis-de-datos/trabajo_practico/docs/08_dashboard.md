# 8. Dashboard en Power BI

El dashboard es `powerbi/TP_freMTPL2.pbix`. Lee los CSV que deja el ETL en `export/`, así que no
limpia ni corrige nada: eso ya pasó antes. Cómo abrirlo está en `powerbi/README.md`.

## Páginas

Cada página responde una pregunta y se relaciona con alguna hipótesis.

| Página | Pregunta | Qué muestra | Hipótesis |
|---|---|---|---|
| Cartera | ¿Cómo es la cartera y cuánto pesan los siniestros grandes? | Pólizas, exposición, frecuencia, severidad y prima pura; frecuencia y severidad por zona; curva de Pareto del costo | H2 y H3 |
| Perfiles | ¿Quién cuesta más y cuánto se aparta del promedio? | Relatividad de prima pura por edad, BonusMalus y antigüedad del vehículo, con una tabla del peso de cada franja | H1 |
| Mapa | ¿Dónde cuesta más? | Mapa de burbujas por región (tamaño = exposición, color = relatividad), ranking de regiones y tabla | H2 |
| Calidad | ¿Podemos confiar en los datos? | Registros corregidos y marcados, frecuencia antes y después de la limpieza, y la tabla de problemas | Calidad |

Las páginas Cartera, Perfiles y Mapa tienen segmentadores por zona y combustible (y Cartera y Perfiles
también por antigüedad del vehículo).

## Decisiones

- **Las medidas suman y dividen.** La frecuencia es la suma de siniestros sobre la suma de
  exposición, igual que en SQL y en Python. Nunca se promedia la cantidad de siniestros por póliza.
  Las medidas están en texto en `powerbi/02_medidas.dax` y las consultas de carga en
  `powerbi/01_power_query.m`.
- **Prima pura con y sin tope.** La página Cartera muestra las dos: con tope (115,79) para comparar
  perfiles y sin tope (167,18), que es el costo real de la cartera.
- **Relatividades contra toda la cartera.** Cuando se aplica un filtro, la relatividad sigue
  comparando contra el promedio de toda la cartera, no contra el grupo filtrado. Lo aclaramos con un
  texto en la página Perfiles.
- **El segmentador de antigüedad no filtra su propio gráfico** en la página Perfiles: si no, el
  gráfico por antigüedad quedaba con una sola barra.
- **El mapa usa latitud y longitud** en lugar de los nombres de las regiones, porque Power BI a veces
  ubica mal las regiones francesas. Las coordenadas son centros aproximados que cargamos nosotros:
  sirven para ubicar las burbujas, no para dibujar los límites.
- **Los avisos van escritos en la página.** En el mapa aclaramos que falta Lorraine, que Centre-Val de
  Loire tiene alrededor del 29 % de la exposición y que las regiones de 2016 son un dato externo.
- **Los segmentos chicos se avisan.** La tabla de Perfiles muestra el porcentaje de exposición de cada
  franja y un aviso cuando la muestra es chica.

## Cómo comprobamos que da bien

Las relatividades que calculamos en Python están en `powerbi/valores_esperados.csv`. Con el
dashboard sin filtros, las relatividades por edad, BonusMalus y antigüedad tienen que coincidir con
ese archivo. Por ejemplo: 18 a 21 años, 3,56; BonusMalus de más de 100, 4,92.
