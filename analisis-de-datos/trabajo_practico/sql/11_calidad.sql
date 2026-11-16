-- 11_calidad.sql
-- Consultas de CALIDAD de datos sobre la capa RAW. Solo detectan y cuentan: no corrigen nada.
-- Cada bloque se numera C1, C2, ... y esos códigos se usan en docs/04_hallazgos_calidad.md.
--
-- Cómo correrlo:  python src/run_sql.py 11_calidad.sql   (o abrir db/seguros.db en DBeaver)
--
-- Recordatorio: raw_freq.idpol es TEXT; para unir con sev usamos
-- CAST(CAST(f.idpol AS REAL) AS INTEGER)  (ver nota en 10_exploracion.sql).


-- =====================================================================
-- A. Nulos, duplicados y tipos
-- =====================================================================

-- C1. ¿Hay valores nulos en alguna columna?
-- Por qué: un nulo en exposure o en idpol rompería cualquier cálculo de frecuencia.
-- COUNT(*) - COUNT(col) = cantidad de nulos en esa columna.
SELECT 'raw_freq' AS tabla,
       COUNT(*) - COUNT(idpol)      AS nulos_idpol,
       COUNT(*) - COUNT(claimnb)    AS nulos_claimnb,
       COUNT(*) - COUNT(exposure)   AS nulos_exposure,
       COUNT(*) - COUNT(vehpower)   AS nulos_vehpower,
       COUNT(*) - COUNT(vehage)     AS nulos_vehage,
       COUNT(*) - COUNT(drivage)    AS nulos_drivage,
       COUNT(*) - COUNT(bonusmalus) AS nulos_bonusmalus,
       COUNT(*) - COUNT(vehbrand)   AS nulos_vehbrand,
       COUNT(*) - COUNT(vehgas)     AS nulos_vehgas,
       COUNT(*) - COUNT(area)       AS nulos_area,
       COUNT(*) - COUNT(density)    AS nulos_density,
       COUNT(*) - COUNT(region)     AS nulos_region
FROM raw_freq;

SELECT 'raw_sev' AS tabla,
       COUNT(*) - COUNT(idpol)       AS nulos_idpol,
       COUNT(*) - COUNT(claimamount) AS nulos_claimamount
FROM raw_sev;


-- C2. ¿Hay pólizas repetidas en freq?
-- Por qué: idpol tiene que ser clave primaria en core_poliza. Si se repite, no se puede.
SELECT idpol, COUNT(*) AS veces
FROM raw_freq
GROUP BY idpol
HAVING COUNT(*) > 1;           -- si no devuelve filas: no hay duplicados


-- C3. En sev, idpol SÍ puede repetirse (varios siniestros por póliza). ¿Hay filas idénticas
--     (misma póliza y mismo monto)?
-- Por qué: podrían ser siniestros duplicados por error o siniestros reales del mismo valor.
--          No se puede saber solo con estos datos, pero conviene medirlo.
SELECT COUNT(*) AS grupos_repetidos,
       SUM(veces) AS filas_involucradas
FROM (
    SELECT idpol, claimamount, COUNT(*) AS veces
    FROM raw_sev
    GROUP BY idpol, claimamount
    HAVING COUNT(*) > 1
) t;


-- C4. ¿Hay idpol en freq que no sean un número entero "limpio"?
-- Por qué: explica por qué pandas leía idpol como float.
-- GLOB '*[^0-9]*' = "tiene en algún lugar un carácter que NO es un dígito".
SELECT idpol, claimnb, exposure, region
FROM raw_freq
WHERE idpol GLOB '*[^0-9]*';

-- C4b. Si convertimos esa fila a 100000, ¿chocaría con otra póliza que ya tenga ese número?
-- Por qué: C2 compara idpol como TEXTO, así que '1.00E+05' y '100000' no los vería repetidos.
SELECT COUNT(*) AS polizas_con_idpol_100000
FROM raw_freq
WHERE CAST(CAST(idpol AS REAL) AS INTEGER) = 100000;   -- 1 = solo la fila rara, no hay choque


-- =====================================================================
-- B. Conciliación freq <-> sev
-- =====================================================================

-- C5. Siniestros SIN póliza (anti-join: filas de sev que no encuentran pareja en freq).
-- Por qué: impiden crear la FK en core_siniestro (ver docs/03_modelo_datos.md).
-- Nota de rendimiento: si pusiéramos el CAST directo en el ON, SQLite recorrería las 678 mil
-- pólizas por CADA siniestro (no termina nunca). Con MATERIALIZED calcula la lista de idpol
-- convertidos UNA vez, la guarda como tabla temporal y le arma un índice solo.
WITH polizas AS MATERIALIZED (
    SELECT CAST(CAST(idpol AS REAL) AS INTEGER) AS idpol FROM raw_freq
)
SELECT COUNT(*)                     AS siniestros_huerfanos,
       COUNT(DISTINCT s.idpol)      AS polizas_distintas,
       ROUND(SUM(s.claimamount), 2) AS monto_total
FROM raw_sev s
LEFT JOIN polizas p ON p.idpol = s.idpol
WHERE p.idpol IS NULL;              -- no encontró póliza = huérfano

-- C5b. Detalle por póliza huérfana.
WITH polizas AS MATERIALIZED (
    SELECT CAST(CAST(idpol AS REAL) AS INTEGER) AS idpol FROM raw_freq
)
SELECT s.idpol, COUNT(*) AS siniestros, ROUND(SUM(s.claimamount), 2) AS monto
FROM raw_sev s
LEFT JOIN polizas p ON p.idpol = s.idpol
WHERE p.idpol IS NULL
GROUP BY s.idpol
ORDER BY siniestros DESC;


-- Para C6 a C8 usamos la misma comparación: para cada póliza, ClaimNb (lo que dice freq)
-- contra n_sev (cuántas filas tiene en sev). La guardamos como vista TEMPORAL (desaparece
-- al cerrar la sesión) para no repetir el código.
CREATE TEMP VIEW conciliacion AS
SELECT CAST(CAST(f.idpol AS REAL) AS INTEGER)        AS idpol,
       f.claimnb,
       COALESCE(s.n_sev, 0)            AS n_sev
FROM raw_freq f
LEFT JOIN (SELECT idpol, COUNT(*) AS n_sev FROM raw_sev GROUP BY idpol) s
       ON s.idpol = CAST(CAST(f.idpol AS REAL) AS INTEGER);

-- C6. Pólizas que declaran siniestros (ClaimNb > 0) pero no tienen NINGUNO en sev.
-- Por qué: esos siniestros cuentan para la frecuencia pero no tienen monto -> la prima pura
--          quedaría subestimada si usamos ClaimNb.
SELECT COUNT(*)      AS polizas,
       SUM(claimnb)  AS siniestros_declarados_sin_monto
FROM conciliacion
WHERE claimnb > 0 AND n_sev = 0;

-- C7. Todas las pólizas cuyo ClaimNb difiere de la cantidad de filas en sev, por tipo.
SELECT CASE WHEN claimnb > 0 AND n_sev = 0 THEN 'ClaimNb > 0 y sin siniestros en sev'
            WHEN claimnb > n_sev           THEN 'ClaimNb mayor que sev (con algún siniestro)'
            ELSE                                'ClaimNb menor que sev'
       END                         AS tipo,
       COUNT(*)                    AS polizas,
       SUM(claimnb)                AS suma_claimnb,
       SUM(n_sev)                  AS suma_n_sev
FROM conciliacion
WHERE claimnb <> n_sev
GROUP BY 1
ORDER BY polizas DESC;

-- C8. ¿En qué rango de idpol se concentran las inconsistencias?
-- Por qué: si están todas juntas, sugiere un problema de origen (un lote de datos), no azar.
-- Comparamos contra el total de pólizas del tramo para ver el % afectado.
SELECT CASE WHEN idpol <= 24500   THEN '1) idpol <= 24.500'
            WHEN idpol <= 1000000 THEN '2) 24.501 - 1.000.000'
            ELSE                       '3) > 1.000.000'
       END                                             AS tramo_idpol,
       COUNT(*)                                        AS polizas_del_tramo,
       SUM(CASE WHEN claimnb <> n_sev THEN 1 ELSE 0 END) AS inconsistentes,
       ROUND(100.0 * SUM(CASE WHEN claimnb <> n_sev THEN 1 ELSE 0 END) / COUNT(*), 2) AS pct
FROM conciliacion
GROUP BY 1
ORDER BY 1;

-- C8b. Dentro de idpol <= 24.500: ¿hay ALGUNA póliza con siniestros en sev?
SELECT COUNT(*) AS polizas_tramo,
       SUM(CASE WHEN claimnb > 0 THEN 1 ELSE 0 END) AS con_claimnb_mayor_0,
       SUM(CASE WHEN n_sev  > 0 THEN 1 ELSE 0 END) AS con_filas_en_sev
FROM conciliacion
WHERE idpol <= 24500;


-- =====================================================================
-- C. Rangos sospechosos
-- =====================================================================

-- C9. Exposición fuera de lo esperable.
-- Por qué: la exposición es el denominador de la frecuencia. > 1 año en una vigencia anual es
--          raro; muy cerca de 0 genera frecuencias enormes con un solo siniestro.
-- Umbral "cercana a 0": < 0.01 años (unos 3,6 días). Es un umbral elegido por nosotros.
SELECT SUM(CASE WHEN exposure > 1     THEN 1 ELSE 0 END) AS exposure_mayor_1,
       MAX(exposure)                                     AS exposure_max,
       SUM(CASE WHEN exposure < 0.01  THEN 1 ELSE 0 END) AS exposure_menor_001,
       MIN(exposure)                                     AS exposure_min
FROM raw_freq;

-- C9b. ¿Cómo se distribuyen las exposiciones mayores a 1?
SELECT ROUND(exposure, 2) AS exposure, COUNT(*) AS polizas
FROM raw_freq
WHERE exposure > 1
GROUP BY 1
ORDER BY 1;

-- C10. ClaimNb extremos: pólizas con 5 o más siniestros declarados.
-- Por qué: 5+ siniestros en un año es muy poco común; puede ser una flota o un error.
SELECT idpol, claimnb, exposure, drivage, bonusmalus
FROM raw_freq
WHERE claimnb >= 5
ORDER BY claimnb DESC;

-- C11. Montos de siniestro <= 0 y los más grandes.
SELECT SUM(CASE WHEN claimamount <= 0 THEN 1 ELSE 0 END) AS montos_no_positivos
FROM raw_sev;

SELECT idpol, claimamount
FROM raw_sev
ORDER BY claimamount DESC
LIMIT 10;

-- C12. Edades, antigüedad del vehículo y BonusMalus fuera de rango.
-- Reglas: DrivAge >= 18 (edad mínima para conducir en Francia),
--         BonusMalus entre 50 y 350 (escala francesa), VehAge > 40 lo tomamos como sospechoso.
SELECT SUM(CASE WHEN drivage < 18                      THEN 1 ELSE 0 END) AS drivage_menor_18,
       SUM(CASE WHEN drivage > 90                      THEN 1 ELSE 0 END) AS drivage_mayor_90,
       SUM(CASE WHEN vehage > 40                       THEN 1 ELSE 0 END) AS vehage_mayor_40,
       SUM(CASE WHEN bonusmalus NOT BETWEEN 50 AND 350 THEN 1 ELSE 0 END) AS bonusmalus_fuera_rango
FROM raw_freq;

-- C12b. Detalle de VehAge alto.
SELECT vehage, COUNT(*) AS polizas
FROM raw_freq
WHERE vehage > 40
GROUP BY vehage
ORDER BY vehage;


-- =====================================================================
-- D. Consistencia entre columnas y categorías
-- =====================================================================

-- C13. Area <-> Density: ¿las zonas se ordenan por densidad o se solapan?
-- Por qué: si Area es solo Density "en tramos", son variables redundantes.
SELECT area,
       MIN(density) AS densidad_min,
       MAX(density) AS densidad_max,
       COUNT(*)     AS polizas
FROM raw_freq
GROUP BY area
ORDER BY area;

-- C13b. ¿Algún valor de densidad aparece en más de una zona?
SELECT density, GROUP_CONCAT(DISTINCT area) AS zonas, COUNT(*) AS polizas
FROM raw_freq
GROUP BY density
HAVING COUNT(DISTINCT area) > 1
ORDER BY density;

-- C14. Valores de las categóricas: ¿hay variantes de escritura o espacios de más?
SELECT 'region' AS columna, region AS valor, COUNT(*) AS polizas,
       (region <> TRIM(region)) AS tiene_espacios
FROM raw_freq GROUP BY region
UNION ALL
SELECT 'vehbrand', vehbrand, COUNT(*), (vehbrand <> TRIM(vehbrand)) FROM raw_freq GROUP BY vehbrand
UNION ALL
SELECT 'vehgas',   vehgas,   COUNT(*), (vehgas   <> TRIM(vehgas))   FROM raw_freq GROUP BY vehgas
ORDER BY columna, valor;
