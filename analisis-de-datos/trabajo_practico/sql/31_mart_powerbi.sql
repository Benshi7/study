-- 31_mart_powerbi.sql
-- Tablas chicas de apoyo para el dashboard de Power BI (páginas Mapa, Perfiles y Calidad).
-- Se corre con:  python src/build_mart.py   (después de 30_mart.sql)
-- Así ningún número del dashboard está escrito a mano: todos salen de una consulta.


DROP TABLE IF EXISTS mart_calidad_hallazgos;
DROP TABLE IF EXISTS mart_calidad_antes_despues;
DROP TABLE IF EXISTS mart_pareto;
DROP TABLE IF EXISTS mart_dim_region_mapa;


-- =====================================================================
-- Calidad: cuántos registros toca cada problema (tabla de docs/05_limpieza.md)
-- =====================================================================
-- Cada fila repite la consulta de 11_calidad.sql o de 21_antes_despues.sql indicada al lado.
CREATE TABLE mart_calidad_hallazgos AS
SELECT 'Q1/Q2' AS codigo, 'ClaimNb no coincide con sev' AS problema, 'Corregir' AS accion,
       (SELECT SUM(flag_claimnb_corregido) FROM core_poliza) AS registros                  -- A4
UNION ALL SELECT 'Q3', 'Lote IDpol ≤ 24.500 con problema de origen', 'Marcar',
       (SELECT SUM(flag_lote_idpol_bajo) FROM core_poliza)                                 -- A4
UNION ALL SELECT 'Q4', 'Siniestros sin póliza (huérfanos)', 'Apartar',
       (SELECT COUNT(*) FROM core_siniestro_huerfano)                                      -- A4
UNION ALL SELECT 'Q5', 'IDpol en notación científica (1.00E+05)', 'Corregir',
       (SELECT COUNT(*) FROM raw_freq WHERE idpol GLOB '*[^0-9]*')                         -- A4
UNION ALL SELECT 'Q7', 'Exposure > 1', 'Corregir',
       (SELECT SUM(flag_exposure_recortada) FROM core_poliza)                              -- A4
UNION ALL SELECT 'Q14', 'Regiones sin acentos (normalizadas)', 'Normalizar',
       (SELECT COUNT(*) FROM core_dim_region)                                              -- A6
UNION ALL SELECT 'Q6', 'Siniestros repetidos (misma póliza y monto)', 'Dejar',
       (SELECT SUM(veces) FROM (SELECT COUNT(*) AS veces FROM raw_sev
                                GROUP BY idpol, claimamount HAVING COUNT(*) > 1))          -- C3
UNION ALL SELECT 'Q8', 'Exposure muy chica (< 0,01)', 'Dejar',
       (SELECT COUNT(*) FROM raw_freq WHERE exposure < 0.01)                               -- C9
UNION ALL SELECT 'Q9', 'ClaimNb extremos (≥ 5)', 'Resuelto por Q1',
       (SELECT COUNT(*) FROM raw_freq WHERE claimnb >= 5)                                  -- C10
UNION ALL SELECT 'Q10', 'VehAge 99/100 (desconocido)', 'Dejar',
       (SELECT COUNT(*) FROM raw_freq WHERE vehage IN (99, 100))                           -- C12b
UNION ALL SELECT 'Q11', 'DrivAge > 90', 'Dejar',
       (SELECT COUNT(*) FROM raw_freq WHERE drivage > 90)                                  -- C12
UNION ALL SELECT 'Q12', 'Siniestros > 10× la media (cola pesada)', 'Dejar',
       (SELECT COUNT(*) FROM raw_sev
        WHERE claimamount > 10 * (SELECT AVG(claimamount) FROM raw_sev))                   -- E5b
UNION ALL SELECT 'Q13', 'Area redundante con Density (pólizas en bordes)', 'Dejar',
       (SELECT SUM(polizas) FROM (SELECT COUNT(*) AS polizas FROM raw_freq GROUP BY density
                                  HAVING COUNT(DISTINCT area) > 1));                       -- C13b


-- =====================================================================
-- Calidad: indicadores antes y después de limpiar (misma consulta que A2)
-- =====================================================================
CREATE TABLE mart_calidad_antes_despues AS
SELECT 'Antes (ClaimNb original, exposure sin recortar)' AS version,
       COUNT(*)                                          AS polizas,
       ROUND(SUM(exposure), 1)                           AS exposicion,
       SUM(claimnb)                                      AS siniestros_version,
       ROUND(SUM(claimnb) / SUM(exposure), 4)            AS frecuencia_version,
       ROUND((SELECT SUM(claimamount) FROM core_siniestro) / SUM(exposure), 2) AS prima_pura_version
FROM raw_freq
UNION ALL
SELECT 'Después (core completo)',
       COUNT(*), ROUND(SUM(exposure), 1), SUM(claimnb),
       ROUND(SUM(claimnb) / SUM(exposure), 4),
       ROUND((SELECT SUM(claimamount) FROM core_siniestro) / SUM(exposure), 2)
FROM core_poliza
UNION ALL
SELECT 'Después (sin lote IDpol ≤ 24.500)',
       COUNT(*), ROUND(SUM(p.exposure), 1), SUM(p.claimnb),
       ROUND(SUM(p.claimnb) / SUM(p.exposure), 4),
       ROUND((SELECT SUM(s.claimamount) FROM core_siniestro s
              JOIN core_poliza q ON q.idpol = s.idpol
              WHERE q.flag_lote_idpol_bajo = 0) / SUM(p.exposure), 2)
FROM core_poliza p
WHERE p.flag_lote_idpol_bajo = 0;


-- =====================================================================
-- Pareto de siniestros (H3): ¿qué % del monto explica el k % de siniestros más caros?
-- =====================================================================
-- pct_siniestros va de 0 a 1 (0,01 = el 1 % más caro); pct_monto_acum va de 0 a 100.
-- Para el k %, se toman los ceil(k × n / 100) siniestros más caros.
-- (k × n + 99) / 100 con números enteros es una forma de redondear hacia arriba sin CEIL.
CREATE TABLE mart_pareto AS
WITH RECURSIVE k(valor) AS (                    -- genera los números 0, 1, ..., 100
    SELECT 0 UNION ALL SELECT valor + 1 FROM k WHERE valor < 100
),
ordenados AS (                                  -- siniestros del más caro al más barato
    SELECT ROW_NUMBER() OVER (ORDER BY claimamount DESC) AS puesto,
           SUM(claimamount) OVER (ORDER BY claimamount DESC
                                  ROWS UNBOUNDED PRECEDING) AS monto_acum
    FROM core_siniestro
),
totales AS (SELECT COUNT(*) AS n, SUM(claimamount) AS monto FROM core_siniestro)
SELECT k.valor / 100.0                                          AS pct_siniestros,
       ROUND(100 * COALESCE(o.monto_acum, 0) / t.monto, 2)      AS pct_monto_acum
FROM k
CROSS JOIN totales t
LEFT JOIN ordenados o ON o.puesto = (k.valor * t.n + 99) / 100
ORDER BY k.valor;


-- =====================================================================
-- Coordenadas de las regiones 2016, para el mapa de burbujas
-- =====================================================================
-- Dato EXTERNO (no sale del dataset): punto aproximado del centro de cada región.
-- Solo sirve para ubicar la burbuja en el mapa; no entra en ningún cálculo.
CREATE TABLE mart_dim_region_mapa (
    region_2016 TEXT PRIMARY KEY,
    latitud     REAL NOT NULL,
    longitud    REAL NOT NULL
);
INSERT INTO mart_dim_region_mapa VALUES
    ('Auvergne-Rhône-Alpes',        45.45,  4.39),
    ('Bourgogne-Franche-Comté',     47.24,  4.83),
    ('Bretagne',                    48.20, -2.93),
    ('Centre-Val de Loire',         47.48,  1.68),
    ('Corse',                       42.15,  9.10),
    ('Grand Est',                   48.70,  5.62),
    ('Hauts-de-France',             49.97,  2.78),
    ('Île-de-France',               48.71,  2.50),
    ('Normandie',                   49.12,  0.11),
    ('Nouvelle-Aquitaine',          45.40,  0.35),
    ('Occitanie',                   43.65,  2.15),
    ('Pays de la Loire',            47.47, -0.80),
    ('Provence-Alpes-Côte d''Azur', 43.94,  6.07);
