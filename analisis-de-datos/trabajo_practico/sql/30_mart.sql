-- 30_mart.sql
-- Capa MART (gold): tablas planas, listas para analizar en Python o en Power BI.
-- Se corre con:  python src/build_mart.py
--   (el script calcula el tope de siniestros grandes y lo guarda en mart_parametro
--    ANTES de ejecutar este archivo: SQLite no tiene una función de percentil).
--
-- mart_poliza_analitica : 1 fila por póliza, con sus siniestros y montos ya sumados.
-- mart_siniestro        : 1 fila por siniestro, con el monto real y el monto con tope.


DROP TABLE IF EXISTS mart_siniestro;
DROP TABLE IF EXISTS mart_poliza_analitica;


-- =====================================================================
-- Siniestros, con el tope aplicado
-- =====================================================================
-- El tope recorta cada siniestro grande al valor del tope (no lo borra):
--   un siniestro de 1.000.000 con tope 16.451 cuenta como 16.451.
CREATE TABLE mart_siniestro AS
SELECT s.id_siniestro,
       s.idpol,
       s.claimamount                                         AS monto,
       MIN(s.claimamount, t.valor)                           AS monto_topeado,
       CASE WHEN s.claimamount > t.valor THEN 1 ELSE 0 END   AS es_grande
FROM core_siniestro s
CROSS JOIN (SELECT valor FROM mart_parametro WHERE nombre = 'tope_siniestro') t;


-- =====================================================================
-- Pólizas: una fila por póliza
-- =====================================================================
-- Para evitar el fan-out (ver 10_exploracion.sql, E7): primero se suman los siniestros
-- por póliza y DESPUÉS se hace el LEFT JOIN. Así cada póliza aparece una sola vez.
--
-- Las franjas tienen etiquetas que se ordenan bien como texto (Power BI ordena alfabéticamente):
-- por eso BonusMalus va con ceros ('050') y la antigüedad del vehículo también ('00').
CREATE TABLE mart_poliza_analitica AS
WITH montos_por_poliza AS (
    SELECT idpol,
           SUM(monto)          AS monto,
           SUM(monto_topeado)  AS monto_topeado,
           SUM(es_grande)      AS siniestros_grandes
    FROM mart_siniestro
    GROUP BY idpol
)
SELECT p.idpol,
       -- Medidas (lo que se suma)
       p.exposure,
       p.claimnb                                  AS siniestros,
       COALESCE(m.monto, 0)                       AS monto,
       COALESCE(m.monto_topeado, 0)               AS monto_topeado,
       COALESCE(m.siniestros_grandes, 0)          AS siniestros_grandes,
       -- Conductor
       p.drivage,
       CASE WHEN p.drivage <= 21 THEN '18-21'
            WHEN p.drivage <= 25 THEN '22-25'
            WHEN p.drivage <= 30 THEN '26-30'
            WHEN p.drivage <= 40 THEN '31-40'
            WHEN p.drivage <= 50 THEN '41-50'
            WHEN p.drivage <= 60 THEN '51-60'
            WHEN p.drivage <= 70 THEN '61-70'
            ELSE '71+' END                        AS franja_edad,
       p.bonusmalus,
       CASE WHEN p.bonusmalus = 50   THEN '050'
            WHEN p.bonusmalus <= 75  THEN '051-075'
            WHEN p.bonusmalus <= 100 THEN '076-100'
            ELSE '101+' END                       AS franja_bm,
       -- Vehículo
       p.vehage,
       -- Suposición: vehage 99/100 es un código de "desconocido" (Q10). Cae en '16+'.
       CASE WHEN p.vehage = 0   THEN '00'
            WHEN p.vehage <= 2  THEN '01-02'
            WHEN p.vehage <= 5  THEN '03-05'
            WHEN p.vehage <= 10 THEN '06-10'
            WHEN p.vehage <= 15 THEN '11-15'
            ELSE '16+' END                        AS franja_vehage,
       p.vehpower,
       p.vehbrand,
       p.vehgas,
       -- Zona
       p.area,
       p.density,
       d.region_nombre                            AS region,
       d.region_2016,
       -- Calidad (para la página de antes/después y para filtrar)
       p.claimnb_declarado,
       p.flag_lote_idpol_bajo,
       p.flag_exposure_recortada,
       p.flag_claimnb_corregido
FROM core_poliza p
JOIN core_dim_region d       ON d.region_codigo = p.region
LEFT JOIN montos_por_poliza m ON m.idpol = p.idpol;
