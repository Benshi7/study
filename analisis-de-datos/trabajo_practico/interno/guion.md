# 08 — Guion de la exposición

**Objetivo:** 15 minutos (máximo de la consigna: 20). 13 slides, una por cada punto de las
"Pautas de exposición", más portada y preguntas. La presentación es `presentacion/index.html`:
con la tecla **S** se abre el modo presentador con estas notas y un reloj.

No se lee: cada slide tiene una idea, y el orador la cuenta con sus palabras.
En tres momentos se muestra **código en vivo** y en uno el **dashboard**.

## Reparto

| Orador | Pautas | Slides | Tiempo | Qué tener abierto |
|---|---|---|---:|---|
| Bruno | 1 · caso, 2 · pregunta | 1–3 | 2:00 | — |
| Juan Pablo | 3 · dataset, 4 · flujo técnico | 4–5 | 3:00 | `notebooks/00_etl_demo.ipynb` |
| Uriel | 5 · calidad, 6 · EDA | 6–8 | 4:00 | `sql/11_calidad.sql`, `notebooks/03_eda.ipynb` |
| Nicolás | 7 · dashboard, 8 · insights | 9–11 | 4:10 | `powerbi/TP_freMTPL2.pbix` |
| Bruno | 9 · limitaciones y mejoras | 12 | 1:05 | — |
| Todos | Preguntas | 13 | resto | — |

Total ≈ 14 minutos.

## Slide por slide

| # | Slide | Orador · tiempo | Idea a transmitir |
|---:|---|---|---|
| 1 | Portada | Bruno · 0:15 | Somos el equipo de pricing, le hablamos a la dirección técnica |
| 2 | El caso | Bruno · 0:40 | Cobrar lo mismo a todos genera selección adversa |
| 3 | Pregunta | Bruno · 1:05 | Prima pura por perfil, H1–H3, qué es exposición y relatividad |
| 4 | Dataset | Juan Pablo · 1:15 | Dos tablas (pólizas 1 → N siniestros) que hay que conciliar |
| 5 | Flujo técnico | Juan Pablo · 1:45 | raw → core → mart con un comando y controles. **Código en vivo** |
| 6 | Calidad | Uriel · 1:45 | Las tablas no cerraban; frecuencia 0,1007 → 0,0738. **Consulta SQL en vivo** |
| 7 | EDA · conductor | Uriel · 1:15 | H1: el BonusMalus pesa más que la edad (van juntos) |
| 8 | EDA · zona y vehículo | Uriel · 1:00 | H2: la ciudad choca más seguido, no más caro; diésel +14 %. **Notebook en vivo** |
| 9 | Dashboard | Nicolás · 2:30 | **Demo en Power BI**: Perfiles filtrando por combustible |
| 10 | Insight · tope | Nicolás · 0:50 | H3: 3 siniestros hacían ver a los jóvenes 13× más caros; con tope, 3,6× |
| 11 | Conclusiones | Nicolás · 0:50 | Las 3 hipótesis se confirman, con matices |
| 12 | Limitaciones y mejoras | Bruno · 1:05 | No es tarifa, asociación no causa; GLM y más datos |
| 13 | Preguntas | Todos | Cada uno responde lo suyo |

## Preguntas probables y respuesta corta

| Pregunta | Respuesta |
|---|---|
| ¿Por qué no promediaron los siniestros por póliza? | Las pólizas no duran lo mismo: se divide por la exposición |
| ¿Por qué no borraron el lote IDpol ≤ 24.500? | Borrarlo también sesga; lo marcamos y sin él la frecuencia da igual (0,0739) |
| ¿Por qué el tope en el percentil 99? | Sin tope, 3 siniestros mueven una franja entera. Es configurable |
| ¿La edad causa más choques? | Mostramos asociación, no causa; además edad y BonusMalus se mezclan |
| ¿Por qué SQLite y no un motor con servidor? | Un archivo, sin instalación; alcanza para 700 mil filas y es reproducible |
