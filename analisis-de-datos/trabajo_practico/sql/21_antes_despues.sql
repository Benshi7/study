-- 21_antes_despues.sql
-- Compara RAW (antes) contra CORE (después) para mostrar el efecto de cada corrección.
-- Solo lectura. Se corre con:  python src/run_sql.py 21_antes_despues.sql
-- Los códigos (A1, A2, ...) se usan en docs/05_limpieza.md.


-- A1. Conciliación: ¿cuántas pólizas tienen un conteo de siniestros que NO coincide con
--     sus filas de siniestros? Antes: ClaimNb vs raw_sev. Después: claimnb vs core_siniestro.
-- Por qué: es el problema central (Q1/Q2). Después de limpiar tiene que dar 0.
WITH sev_raw AS MATERIALIZED (SELECT idpol, COUNT(*) AS n FROM raw_sev GROUP BY idpol),
     sev_core AS MATERIALIZED (SELECT idpol, COUNT(*) AS n FROM core_siniestro GROUP BY idpol)
SELECT 'antes (raw)' AS momento, COUNT(*) AS polizas_inconsistentes
FROM raw_freq f
LEFT JOIN sev_raw s ON s.idpol = CAST(CAST(f.idpol AS REAL) AS INTEGER)
WHERE f.claimnb <> COALESCE(s.n, 0)
UNION ALL
SELECT 'después (core)', COUNT(*)
FROM core_poliza p
LEFT JOIN sev_core s ON s.idpol = p.idpol
WHERE p.claimnb <> COALESCE(s.n, 0);


-- A2. Indicadores de la cartera: antes vs después.
-- Por qué: muestra cuánto cambian los números del negocio por limpiar los datos.
--   frecuencia = siniestros / exposición;  prima pura = monto / exposición
--   El monto es el mismo en todas las filas: los siniestros huérfanos nunca entran porque no
--   tienen póliza (ni exposición) a la que asignarse.
SELECT 'antes: ClaimNb original, exposure sin recortar' AS version,
       COUNT(*)                                              AS polizas,
       ROUND(SUM(exposure), 1)                               AS exposicion,
       SUM(claimnb)                                          AS siniestros,
       ROUND(SUM(claimnb) / SUM(exposure), 4)                AS frecuencia,
       ROUND((SELECT SUM(claimamount) FROM core_siniestro) / SUM(exposure), 2) AS prima_pura
FROM raw_freq
UNION ALL
SELECT 'después: core completo',
       COUNT(*), ROUND(SUM(exposure), 1), SUM(claimnb),
       ROUND(SUM(claimnb) / SUM(exposure), 4),
       ROUND((SELECT SUM(claimamount) FROM core_siniestro) / SUM(exposure), 2)
FROM core_poliza
UNION ALL
SELECT 'después: core sin lote idpol <= 24500',
       COUNT(*), ROUND(SUM(p.exposure), 1), SUM(p.claimnb),
       ROUND(SUM(p.claimnb) / SUM(p.exposure), 4),
       ROUND((SELECT SUM(s.claimamount) FROM core_siniestro s
              JOIN core_poliza q ON q.idpol = s.idpol
              WHERE q.flag_lote_idpol_bajo = 0) / SUM(p.exposure), 2)
FROM core_poliza p
WHERE p.flag_lote_idpol_bajo = 0;


-- A3. Severidad media: antes (todo raw_sev, incluye huérfanos) vs después (core_siniestro).
SELECT 'antes (raw_sev)'       AS momento, COUNT(*) AS siniestros,
       ROUND(AVG(claimamount), 2) AS severidad_media FROM raw_sev
UNION ALL
SELECT 'después (core_siniestro)', COUNT(*), ROUND(AVG(claimamount), 2) FROM core_siniestro
UNION ALL
SELECT 'apartados (huérfanos)',    COUNT(*), ROUND(AVG(claimamount), 2) FROM core_siniestro_huerfano;


-- A4. ¿Cuántos registros tocó cada corrección? (resumen para la página de calidad en Power BI)
SELECT 'Q1/Q2 claimnb recalculado desde sev' AS correccion, SUM(flag_claimnb_corregido) AS registros
FROM core_poliza
UNION ALL
SELECT 'Q3 pólizas del lote idpol <= 24500 (marcadas)', SUM(flag_lote_idpol_bajo) FROM core_poliza
UNION ALL
SELECT 'Q4 siniestros huérfanos apartados', COUNT(*) FROM core_siniestro_huerfano
UNION ALL
SELECT 'Q5 idpol no entero convertido',
       (SELECT COUNT(*) FROM raw_freq WHERE idpol GLOB '*[^0-9]*')
UNION ALL
SELECT 'Q7 exposure recortada a 1', SUM(flag_exposure_recortada) FROM core_poliza;


-- A5. Q5 en detalle: tipo de dato de idpol antes y después.
-- typeof() dice cómo guardó SQLite cada valor: 'text', 'integer', 'real'.
SELECT 'antes (raw_freq)' AS momento, typeof(idpol) AS tipo, COUNT(*) AS filas
FROM raw_freq GROUP BY typeof(idpol)
UNION ALL
SELECT 'después (core_poliza)', typeof(idpol), COUNT(*)
FROM core_poliza GROUP BY typeof(idpol);

SELECT idpol, claimnb_declarado, exposure, region
FROM core_poliza
WHERE idpol = 100000;            -- la fila que venía como '1.00E+05'


-- A6. Q14: regiones normalizadas y su región 2016.
SELECT d.region_2016,
       GROUP_CONCAT(d.region_nombre, ' + ') AS regiones_anteriores,
       SUM(n.polizas)                       AS polizas
FROM core_dim_region d
JOIN (SELECT region, COUNT(*) AS polizas FROM core_poliza GROUP BY region) n
  ON n.region = d.region_codigo
GROUP BY d.region_2016
ORDER BY polizas DESC;
