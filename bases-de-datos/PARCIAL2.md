# 2do parcial — tips del docente (2026-10-22)

Dichos **de pasada** en clase, sin confirmar del todo. El modelo de examen que tenemos puede no
ser el formato final. Si el docente dice otra cosa, esto manda por debajo.

## Fecha

**Jueves 12/11/2026, 18:30 hs, puntual.** Antes hay que entregar los 6 TPs, cada uno en su carpeta (TP1–TP6), o se pierde la promoción.

## Formato

Igual que el 1er parcial: teoría y práctica, **se aprueban por separado**.

| Parte | Qué es | Con qué se prepara |
|---|---|---|
| Teoría | **Choice, en papel** | Lecciones de teoría (0027, 0028, 0029, 0041 y 0049–0051), el repaso 0053 y el simulacro de la suite |
| Práctica | **Todo SQL** | Constructor SQL, `practica/tp5-clinica.html`, lecciones 0031–0040 |

**Si hay una sola sesión de estudio:** `lessons/0055-la-clase-del-parcial.html`. Resume todo lo
de abajo en 7 bloques de 10 minutos, con un ejercicio corregible por bloque.

## Qué puede pedir la práctica

Lo que el docente nombró, y dónde está cubierto:

| Pedido | Cobertura | Estado |
|---|---|---|
| DDL (CREATE, restricciones, ALTER, DROP) | Lecciones 0031 y 0038, con `sqlbox` | ✅ |
| DML (INSERT, UPDATE, DELETE) | Lección 0037 | ✅ |
| Consultas para resolver ("dos de la dificultad de SUMINISTROS") | Constructor SQL, 31 ejercicios | ✅ |
| Crear una vista, **con indicadores** | Lección 0039 (`CASE`, `EXISTS`) y `RRHH_Medicos` del TP5 | ✅ |
| **Usar la vista** para resolver una consulta ("pegarle a la vista") | TP5 y ejercicio 7 de la lección 0052 | ✅ |
| **Conjuntos** (repaso 05/11): diagrama o expresión → SQL, **dos soluciones**, preferido JOIN + WHERE | Lección 0054: regiones, FULL JOIN + WHERE, simplificación y 8 ejercicios | ✅ |
| Slow Change Dimension: **estado actual** y **estado a una fecha** | Lección 0052 con 8 ejercicios corregibles (incluye el modelo 1a), fichas y clasificador de la suite | ✅ |
| SCD: **la anteúltima foto** (lo repitió varias veces en clase) | Lección 0052, sección 07: MAX sin la vigente, −1 día y LAG, más 4 ejercicios "Anteúltima" | ✅ |

Dijo que seguramente se olvidó de mencionar otras cosas: no dar por cerrado este listado.

## Lecciones opcionales (no las nombró)

La clase de transacciones y seguridad no está entre lo que nombró para el parcial, pero algún
concepto puede aparecer en el choice. Hechas desde capturas de la clase (sin el PPT todavía), en
`raw/Clase Transacciones (capturas)/`:

| Lección | Tema |
|---|---|
| 0042 | Problemas de concurrencia: pérdida de actualización, suma incorrecta, lectura sucia, no repetible, fantasma |
| 0043 | Planificaciones en serie / no en serie, operaciones en conflicto, serialización, bloqueos y 2PL, deadlock, MVCC |
| 0044 | Tipos de fallos, estados de una transacción, log UNDO/REDO, planificaciones recuperables / sin cascada / estrictas |
| 0047 | DAC/MAC, GRANT / REVOKE, WITH GRANT OPTION, revocación en cascada, vistas como seguridad |

El resumen del audio de esa clase tiene errores: cuenta "Abortada" como estado (el slide tiene
Confirmada) y dice que la planificación estricta es "la unión" de las otras dos (es la más
restrictiva). Las lecciones siguen los slides.

## Ejemplos de choice que dio el docente

"La diferencia entre data warehouse, data marts, OLAP, etc., y la definición de los temas." La
lección 0053 junta las diferencias que se confunden (DW/Data Mart, DW/OLAP, OLTP/OLAP, ODS/DW,
MOLAP/ROLAP/HOLAP, estrella/copo de nieve, Inmon/Kimball, MDM/DQ/ETL, CRM/ERP, SCD tipo 1/tipo 2)
y las pregunta como choice.

## Sumas y promedios sobre la historia

También puede venir "sumar el saldo histórico y sacarle el promedio". Lo que se decide primero es
**qué filas entran** (lección 0052, sección 06):

| El enunciado dice | Filas | Condición |
|---|---|---|
| "histórico", "a lo largo del tiempo" | todas las fotos | ninguna sobre fechas |
| "actual", "vigente" | la foto vigente | `Fecha_Fin = '2100-12-31'` |
| "al 31/12/2021" | la foto que cubre esa fecha | `'2021-12-31' BETWEEN Fecha_Inicio AND Fecha_Fin` |
| "hasta el 31/12/2021" | las que empezaron hasta esa fecha | `Fecha_Inicio <= '2021-12-31'` |
| "anteriores a la actual" | todas menos la vigente | `Fecha_Fin <> '2100-12-31'` |

La histórica **ya incluye** la última foto: no se suma aparte. `AVG` sobre fotos es un promedio
simple (cada foto pesa igual). Sobre la vista actual no se puede calcular nada histórico.

## SCD: las dos únicas consultas que pidió

```sql
-- Estado a una fecha: siempre una sola foto cumple
SELECT * FROM Tabla WHERE '2023/04/01' BETWEEN Fecha_Inicio AND Fecha_Fin;
-- Estado actual: la foto vigente lleva la fecha de fin ficticia
SELECT * FROM Tabla WHERE Fecha_Fin = '2100-12-31';
```

Fecha_Fin de cada foto = Fecha_Inicio de la siguiente − 1.

**La convención de la "fecha actual"** (dicha por el docente): la foto vigente termina en
`2100-12-31`. El deck dice "por defecto suele utilizarse… ejemplo 31/12/2100" (y 01/01/1000 para el
inicio): en el examen, copiar la fecha de fin abierta que traiga la tabla.

## El modelo 1a es esto mismo

`raw/Material_Examen/bd parcial 1a.jpg` ya trae `CUSTOMER_GROUP` con 8 fotos y `CUSTOMER_NAME`:
(a) vista con la información actual completa y campos en castellano, (b) indicador Externo/Propio
(oficial < 21 **y** banca > 4), (c) todos los clientes al 31/01/2021. Más el punto 1, **graficar los
componentes genéricos de un DW** (lección 0050). Todo está en las lecciones 0050 y 0052.

## Vistas del TP de SCD: qué campos

- **Histórica** (`P_Mstr_LK_Clientes_Hist`): todos los campos en español, con `Fecha_Inicio` y `Fecha_Fin`.
- **Actual** (`P_Mstr_LK_Clientes`): filtra `Fecha_Fin = '2100-12-31'`; `Fecha_Fin` se puede omitir.
  La consigna no lista sus campos: decisión de diseño, no del deck.
- Las preguntas con fecha ("al 14/02/2021") sólo se resuelven sobre la histórica.

## Trampa de SQLite

Las fechas son texto. Mezclar `'2023/04/01'` con `'2023-04-30'` compara mal sin dar error:
usar siempre `AAAA-MM-DD`.
