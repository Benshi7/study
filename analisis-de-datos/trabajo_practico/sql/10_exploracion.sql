-- 10_exploracion.sql
-- Consultas de exploración sobre la capa RAW (solo lectura: no modifican nada).
--
-- Cómo correrlo:  python src/run_sql.py 10_exploracion.sql   (o abrir db/seguros.db en DBeaver)
--
-- Nota para todas las consultas que unen freq con sev:
--   raw_freq.idpol es TEXT (por la fila "1.00E+05") y raw_sev.idpol es INTEGER.
--   Para poder compararlos convertimos al vuelo:  CAST(CAST(f.idpol AS REAL) AS INTEGER)
--   (texto -> número decimal -> entero). Esto NO cambia la tabla, solo la consulta.
--   ¿Por qué no CAST(f.idpol AS INTEGER) directo? Porque SQLite lee solo los dígitos del
--   principio: CAST('1.00E+05' AS INTEGER) da 1, no 100000. Pasando por REAL sí da 100000.


-- E1. ¿Cuántas filas y cuántas pólizas distintas tiene cada tabla?
-- Por qué: confirma la granularidad (freq = 1 fila por póliza, sev = 1 fila por siniestro).
SELECT 'raw_freq' AS tabla, COUNT(*) AS filas, COUNT(DISTINCT idpol) AS idpol_distintos FROM raw_freq
UNION ALL
SELECT 'raw_sev', COUNT(*), COUNT(DISTINCT idpol) FROM raw_sev;


-- E2. ¿Cómo se distribuye la cantidad de siniestros declarada (ClaimNb)?
-- Por qué: ver qué tan raros son los siniestros y si hay valores extremos.
SELECT claimnb,
       COUNT(*) AS polizas,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 3) AS pct
FROM raw_freq
GROUP BY claimnb
ORDER BY claimnb;


-- E3. ¿Cómo se reparte la cartera (pólizas y exposición) por zona?
-- Por qué: antes de comparar riesgo por segmento hay que saber cuánto "peso" tiene cada uno.
SELECT area,
       COUNT(*)                     AS polizas,
       ROUND(SUM(exposure), 1) AS exposicion_anios,
       ROUND(AVG(density))          AS densidad_media
FROM raw_freq
GROUP BY area
ORDER BY area;


-- E4. Lo mismo por región, de mayor a menor exposición.
SELECT region,
       COUNT(*)                         AS polizas,
       ROUND(SUM(exposure), 1) AS exposicion_anios
FROM raw_freq
GROUP BY region
ORDER BY exposicion_anios DESC;


-- E5. ¿Cómo es la distribución de los montos de siniestro?
-- Por qué: si la media está muy por encima de la mediana, unos pocos siniestros grandes
--          pesan mucho (relacionado con la hipótesis H3).
-- SQLite no trae función de percentiles: la mediana y el p99 los calculamos en el notebook
-- (notebooks/01_comprension.ipynb). Acá alcanza con comparar media vs máximo.
SELECT COUNT(*)                    AS siniestros,
       ROUND(MIN(claimamount), 2)  AS minimo,
       ROUND(AVG(claimamount), 2)  AS media,
       ROUND(MAX(claimamount), 2)  AS maximo
FROM raw_sev;

-- E5b. ¿Cuántos siniestros superan 10 veces el monto medio? ¿Y cuánto suman?
-- Por qué: primera medida simple de "pocos siniestros grandes" para H3.
SELECT COUNT(*)                                                  AS siniestros_grandes,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM raw_sev), 2) AS pct_de_siniestros,
       ROUND(100.0 * SUM(claimamount) / (SELECT SUM(claimamount) FROM raw_sev), 2) AS pct_del_monto
FROM raw_sev
WHERE claimamount > 10 * (SELECT AVG(claimamount) FROM raw_sev);


-- E6. Primeras métricas de negocio de toda la cartera (versión CORRECTA).
-- Por qué: son los números de referencia contra los que después comparamos cada segmento.
-- Cómo: 1) agregamos sev por póliza (una fila por póliza), 2) LEFT JOIN a freq.
--       Así cada póliza aparece UNA sola vez y su exposición se suma una sola vez.
-- Mostramos la frecuencia calculada de dos formas porque ClaimNb y sev no coinciden
-- (ver 11_calidad.sql). Todavía NO corregimos: son números "antes de limpiar".
WITH sev_por_poliza AS (
    SELECT idpol,
           COUNT(*)         AS n_siniestros_sev,
           SUM(claimamount) AS monto_total
    FROM raw_sev
    GROUP BY idpol
),
cartera AS (
    SELECT f.exposure,
           f.claimnb,
           COALESCE(s.n_siniestros_sev, 0) AS n_siniestros_sev,   -- póliza sin siniestros -> 0
           COALESCE(s.monto_total, 0)      AS monto_total
    FROM raw_freq f
    LEFT JOIN sev_por_poliza s ON s.idpol = CAST(CAST(f.idpol AS REAL) AS INTEGER)
)
SELECT COUNT(*)                                                   AS polizas,
       ROUND(SUM(exposure), 1)                           AS exposicion_anios,
       -- Frecuencia = siniestros / exposición (NO el promedio de claimnb)
       ROUND((SUM(claimnb)          / SUM(exposure)), 4) AS frecuencia_con_claimnb,
       ROUND((SUM(n_siniestros_sev) / SUM(exposure)), 4) AS frecuencia_con_sev,
       -- Severidad = monto / cantidad de siniestros con monto
       ROUND((SUM(monto_total) / SUM(n_siniestros_sev)), 2) AS severidad_media,
       -- Prima pura = monto / exposición  (= frecuencia_con_sev x severidad)
       ROUND((SUM(monto_total) / SUM(exposure)), 2)     AS prima_pura
FROM cartera;


-- E7. Error clásico: el FAN-OUT (JOIN directo + SUM(exposure)).
-- Por qué: es el error más común al unir una tabla 1 con una tabla N. Lo mostramos al lado
--          de la versión correcta para explicarlo en la exposición.
-- Qué pasa: al hacer JOIN directo, una póliza con 3 siniestros aparece en 3 filas, y su
--           exposición se suma 3 veces. La exposición "crece" y la frecuencia queda mal.
SELECT 'INCORRECTO: JOIN directo' AS version,
       COUNT(*)                         AS filas_resultado,
       ROUND(SUM(f.exposure), 1) AS exposicion_sumada
FROM raw_freq f
LEFT JOIN raw_sev s ON s.idpol = CAST(CAST(f.idpol AS REAL) AS INTEGER)
UNION ALL
SELECT 'CORRECTO: agregar sev primero',
       COUNT(*),
       ROUND(SUM(f.exposure), 1)
FROM raw_freq f
LEFT JOIN (SELECT idpol, COUNT(*) AS n FROM raw_sev GROUP BY idpol) s
       ON s.idpol = CAST(CAST(f.idpol AS REAL) AS INTEGER);
