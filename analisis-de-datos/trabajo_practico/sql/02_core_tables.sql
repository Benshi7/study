-- 02_core_tables.sql
-- Tablas de la capa CORE: datos limpios, con tipos correctos, claves y reglas.
-- Este archivo solo crea la ESTRUCTURA. Los datos los carga sql/20_limpieza_core.sql.
--
-- Modelo: una póliza tiene 0..N siniestros (relación 1:N por idpol).
--         cada póliza pertenece a una región (core_dim_region).
--
-- IMPORTANTE: en SQLite las claves foráneas vienen DESACTIVADAS. Hay que ejecutar
--   PRAGMA foreign_keys = ON;
-- en cada conexión (src/db.py lo hace solo). Si no, la FK existe pero no se controla.

-- Se borran en orden inverso: primero las tablas que apuntan, después las apuntadas.
DROP TABLE IF EXISTS core_siniestro;
DROP TABLE IF EXISTS core_siniestro_huerfano;
DROP TABLE IF EXISTS core_poliza;
DROP TABLE IF EXISTS core_dim_region;

-- Dimensión de regiones: normaliza los nombres (vienen sin acentos) y agrega la región
-- según la reforma territorial de 2016 (13 regiones), útil para mapas en Power BI.
CREATE TABLE core_dim_region (
    region_codigo   TEXT PRIMARY KEY,   -- el valor tal como viene en el CSV (ej. 'Rhone-Alpes')
    region_nombre   TEXT NOT NULL,      -- nombre oficial con acentos (ej. 'Rhône-Alpes')
    region_2016     TEXT NOT NULL       -- región actual que la contiene (ej. 'Auvergne-Rhône-Alpes')
);

-- Una fila por póliza.
CREATE TABLE core_poliza (
    idpol             INTEGER PRIMARY KEY,          -- ahora sí entero y único
    claimnb           INTEGER NOT NULL CHECK (claimnb >= 0),          -- siniestros según sev (corregido)
    claimnb_declarado INTEGER NOT NULL CHECK (claimnb_declarado >= 0), -- ClaimNb original, para el antes/después
    exposure          REAL    NOT NULL CHECK (exposure > 0 AND exposure <= 1), -- recortada a 1 año
    vehpower          INTEGER NOT NULL,
    vehage            INTEGER NOT NULL CHECK (vehage >= 0),
    drivage           INTEGER NOT NULL CHECK (drivage >= 18),
    bonusmalus        INTEGER NOT NULL CHECK (bonusmalus BETWEEN 50 AND 350),
    vehbrand          TEXT    NOT NULL,
    vehgas            TEXT    NOT NULL,
    area              TEXT    NOT NULL CHECK (area IN ('A','B','C','D','E','F')),
    density           INTEGER NOT NULL CHECK (density > 0),
    region            TEXT    NOT NULL REFERENCES core_dim_region (region_codigo),
    -- Marcas de calidad (0 = no, 1 = sí). No borran nada: permiten filtrar o comparar después.
    flag_lote_idpol_bajo  INTEGER NOT NULL CHECK (flag_lote_idpol_bajo IN (0,1)),  -- idpol <= 24500
    flag_exposure_recortada INTEGER NOT NULL CHECK (flag_exposure_recortada IN (0,1)),
    flag_claimnb_corregido  INTEGER NOT NULL CHECK (flag_claimnb_corregido IN (0,1))
);

-- Una fila por siniestro. Su póliza TIENE que existir (FK).
CREATE TABLE core_siniestro (
    id_siniestro  INTEGER PRIMARY KEY,              -- SQLite la numera sola (1, 2, 3, ...)
    idpol         INTEGER NOT NULL REFERENCES core_poliza (idpol),
    claimamount   REAL    NOT NULL CHECK (claimamount > 0)
);

-- Siniestros cuya póliza NO está en freq. No pueden ir a core_siniestro (la FK lo impide),
-- pero tampoco los borramos: los guardamos aparte para poder contarlos y explicarlos.
CREATE TABLE core_siniestro_huerfano (
    id_huerfano   INTEGER PRIMARY KEY,
    idpol         INTEGER NOT NULL,                 -- sin FK, a propósito
    claimamount   REAL    NOT NULL,
    motivo        TEXT    NOT NULL DEFAULT 'idpol inexistente en freq'
);

CREATE INDEX idx_siniestro_idpol ON core_siniestro (idpol);
