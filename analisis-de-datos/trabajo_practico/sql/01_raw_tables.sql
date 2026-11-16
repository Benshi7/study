-- 01_raw_tables.sql
-- Tablas de la capa RAW: una por CSV, con las mismas columnas y en el mismo orden.
-- Regla de esta capa: NO se corrige nada. Si el CSV trae algo raro, acá también aparece.
--
-- Capas: SQLite no tiene "esquemas" como Postgres, así que las capas se marcan con un
-- prefijo en el nombre de la tabla:
--   raw_   -> copia fiel de los CSV           (bronze en Medallion)
--   core_  -> tablas limpias con PK/FK        (silver)
--   mart_  -> tablas y vistas para Power BI   (gold)
--
-- Decisiones:
--  * Nombres de columna en minúscula (idpol en vez de IDpol). Es el único cambio respecto del CSV.
--  * raw_freq.idpol es TEXT: en el CSV hay una fila con "1.00E+05" (notación científica).
--    Si la declaráramos INTEGER, SQLite la convertiría SOLA a 100000, sin avisar, y perderíamos
--    la evidencia del problema. En raw queremos el dato tal como vino.
--  * Sin PK ni FK: en raw todavía no garantizamos unicidad ni integridad (eso lo medimos).
--  * DROP + CREATE: la capa raw se puede regenerar siempre desde los CSV.

DROP TABLE IF EXISTS raw_freq;
CREATE TABLE raw_freq (
    idpol       TEXT,      -- id de póliza, tal como viene en el CSV
    claimnb     INTEGER,   -- cantidad de siniestros declarada
    exposure    REAL,      -- años de vigencia
    vehpower    INTEGER,
    vehage      INTEGER,
    drivage     INTEGER,
    bonusmalus  INTEGER,
    vehbrand    TEXT,
    vehgas      TEXT,
    area        TEXT,
    density     INTEGER,
    region      TEXT
);

DROP TABLE IF EXISTS raw_sev;
CREATE TABLE raw_sev (
    idpol        INTEGER,  -- póliza a la que pertenece el siniestro
    claimamount  REAL      -- costo del siniestro
);
