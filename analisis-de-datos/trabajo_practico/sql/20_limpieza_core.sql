-- 20_limpieza_core.sql
-- Carga la capa CORE a partir de RAW, aplicando las decisiones de docs/04_hallazgos_calidad.md.
-- RAW no se toca: todo se lee de raw_ y se escribe en core_.
-- Se corre con:  python src/build_core.py   (que antes recrea las tablas con 02_core_tables.sql)
--
-- Cada paso indica qué problema (Q1, Q2, ...) resuelve.


-- =====================================================================
-- Paso 1. Dimensión de regiones  (resuelve Q14: nombres sin acentos)
-- =====================================================================
-- Dato EXTERNO (no sale del dataset): nombres oficiales de las regiones anteriores a 2016 y la
-- región a la que pasaron con la reforma territorial francesa (ley 2015-29, vigente desde 2016).
INSERT INTO core_dim_region (region_codigo, region_nombre, region_2016) VALUES
    ('Alsace',                      'Alsace',                     'Grand Est'),
    ('Champagne-Ardenne',           'Champagne-Ardenne',          'Grand Est'),
    ('Aquitaine',                   'Aquitaine',                  'Nouvelle-Aquitaine'),
    ('Limousin',                    'Limousin',                   'Nouvelle-Aquitaine'),
    ('Poitou-Charentes',            'Poitou-Charentes',           'Nouvelle-Aquitaine'),
    ('Auvergne',                    'Auvergne',                   'Auvergne-Rhône-Alpes'),
    ('Rhone-Alpes',                 'Rhône-Alpes',                'Auvergne-Rhône-Alpes'),
    ('Bourgogne',                   'Bourgogne',                  'Bourgogne-Franche-Comté'),
    ('Franche-Comte',               'Franche-Comté',              'Bourgogne-Franche-Comté'),
    ('Bretagne',                    'Bretagne',                   'Bretagne'),
    ('Centre',                      'Centre',                     'Centre-Val de Loire'),
    ('Corse',                       'Corse',                      'Corse'),
    ('Ile-de-France',               'Île-de-France',              'Île-de-France'),
    ('Languedoc-Roussillon',        'Languedoc-Roussillon',       'Occitanie'),
    ('Midi-Pyrenees',               'Midi-Pyrénées',              'Occitanie'),
    ('Nord-Pas-de-Calais',          'Nord-Pas-de-Calais',         'Hauts-de-France'),
    ('Picardie',                    'Picardie',                   'Hauts-de-France'),
    ('Basse-Normandie',             'Basse-Normandie',            'Normandie'),
    ('Haute-Normandie',             'Haute-Normandie',            'Normandie'),
    ('Pays-de-la-Loire',            'Pays de la Loire',           'Pays de la Loire'),
    ('Provence-Alpes-Cotes-D''Azur', 'Provence-Alpes-Côte d''Azur', 'Provence-Alpes-Côte d''Azur');
-- ('' dentro de un texto = un apóstrofo; así se escribe "D'Azur" en SQL)
-- Si en raw_freq apareciera una región que no está en esta lista, el Paso 2 fallaría por la FK:
-- es un control automático de que no se nos escapó ninguna.


-- =====================================================================
-- Paso 2. Pólizas
-- =====================================================================
-- Q5  idpol '1.00E+05' -> 100000: CAST pasando por REAL (CAST directo a INTEGER daría 1).
-- Q1/Q2  claimnb = cantidad de siniestros que realmente están en sev (los que tienen monto).
--        El valor original se guarda en claimnb_declarado.
-- Q3  flag_lote_idpol_bajo marca el lote idpol <= 24500 (problema de origen). NO se borra:
--     el EDA puede calcular con y sin ese lote.
-- Q7  exposure > 1 se recorta a 1 (suponemos vigencias de un año como máximo).
-- Q6, Q8, Q9, Q10, Q11, Q13: se dejan como están (ver docs/05_limpieza.md).
INSERT INTO core_poliza (
    idpol, claimnb, claimnb_declarado, exposure, vehpower, vehage, drivage, bonusmalus,
    vehbrand, vehgas, area, density, region,
    flag_lote_idpol_bajo, flag_exposure_recortada, flag_claimnb_corregido
)
WITH siniestros_por_poliza AS MATERIALIZED (   -- MATERIALIZED: se calcula una vez (ver 11_calidad.sql, C5)
    SELECT idpol, COUNT(*) AS n_sev
    FROM raw_sev
    GROUP BY idpol
),
freq AS (
    SELECT CAST(CAST(idpol AS REAL) AS INTEGER) AS idpol_ok, *
    FROM raw_freq
)
SELECT f.idpol_ok                                       AS idpol,
       COALESCE(s.n_sev, 0)                             AS claimnb,
       f.claimnb                                        AS claimnb_declarado,
       MIN(f.exposure, 1.0)                             AS exposure,   -- MIN de dos valores = el menor
       f.vehpower, f.vehage, f.drivage, f.bonusmalus,
       f.vehbrand, f.vehgas, f.area, f.density, f.region,
       CASE WHEN f.idpol_ok <= 24500 THEN 1 ELSE 0 END  AS flag_lote_idpol_bajo,
       CASE WHEN f.exposure > 1      THEN 1 ELSE 0 END  AS flag_exposure_recortada,
       CASE WHEN f.claimnb <> COALESCE(s.n_sev, 0) THEN 1 ELSE 0 END AS flag_claimnb_corregido
FROM freq f
LEFT JOIN siniestros_por_poliza s ON s.idpol = f.idpol_ok;


-- =====================================================================
-- Paso 3. Siniestros con póliza  (relación 1:N, la FK se controla en cada fila)
-- =====================================================================
-- Q6: las filas repetidas (misma póliza y monto) se mantienen: pueden ser siniestros reales.
INSERT INTO core_siniestro (idpol, claimamount)
SELECT idpol, claimamount
FROM raw_sev
WHERE idpol IN (SELECT idpol FROM core_poliza);


-- =====================================================================
-- Paso 4. Siniestros huérfanos  (resuelve Q4)
-- =====================================================================
-- No pueden ir a core_siniestro (la FK los rechazaría). Los guardamos aparte en vez de borrarlos.
INSERT INTO core_siniestro_huerfano (idpol, claimamount)
SELECT idpol, claimamount
FROM raw_sev
WHERE idpol NOT IN (SELECT idpol FROM core_poliza);
