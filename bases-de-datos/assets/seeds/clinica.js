/* Clínica — modelo relacional derivado del DER de la cátedra (TP5 DDL-DML).
   Es el resultado de la lección 0040: cada tabla sale de una decisión de mapeo
   explicada ahí. Usado por las lecciones 0031–0039 y practica/tp5-clinica.html.
   "Hoy", para todos los ejercicios, es 2026-10-15. */
window.SQL_SEEDS = window.SQL_SEEDS || {};
window.SQL_SEEDS.clinica = `
CREATE TABLE TORRE (
  Cod_Torre   INT          PRIMARY KEY,
  Nombre      VARCHAR(30)  NOT NULL,
  Tipo_Torre  VARCHAR(20)  NOT NULL CHECK (Tipo_Torre IN ('Hospitalización', 'Consulta')),
  Calle       VARCHAR(40)  NOT NULL,
  Numero      INT          NOT NULL,
  Piso        INT,
  Depto       CHAR(2)
);

CREATE TABLE HABITACION (
  Cod_Habitacion INT          PRIMARY KEY,
  Cod_Torre      INT          NOT NULL REFERENCES TORRE (Cod_Torre),
  Piso           INT          NOT NULL,
  Numero         INT          NOT NULL,
  Ancho          DECIMAL(4,2) NOT NULL,
  Largo          DECIMAL(4,2) NOT NULL,
  Cant_Banios    INT          NOT NULL DEFAULT 1,
  Posee_Closet   CHAR(1)      NOT NULL DEFAULT 'N' CHECK (Posee_Closet IN ('S', 'N')),
  Cant_Camas     INT          NOT NULL CHECK (Cant_Camas > 0),
  Posee_Ventana  CHAR(1)      NOT NULL CHECK (Posee_Ventana IN ('S', 'N')),
  UNIQUE (Cod_Torre, Piso, Numero)
);

CREATE TABLE CONSULTORIO (
  Cod_Consultorio INT          PRIMARY KEY,
  Cod_Torre       INT          NOT NULL REFERENCES TORRE (Cod_Torre),
  Piso            INT          NOT NULL,
  Numero          INT          NOT NULL,
  Ancho           DECIMAL(4,2) NOT NULL,
  Largo           DECIMAL(4,2) NOT NULL,
  UNIQUE (Cod_Torre, Piso, Numero)
);

CREATE TABLE SERVICIO (
  Cod_Servicio INT         PRIMARY KEY,
  Nombre       VARCHAR(30) NOT NULL UNIQUE
);

CREATE TABLE SERVICIO_CONSULTORIO (
  Cod_Servicio    INT NOT NULL REFERENCES SERVICIO (Cod_Servicio),
  Cod_Consultorio INT NOT NULL REFERENCES CONSULTORIO (Cod_Consultorio),
  PRIMARY KEY (Cod_Servicio, Cod_Consultorio)
);

CREATE TABLE PREPAGA (
  Cod_Prepaga INT         PRIMARY KEY,
  Nombre      VARCHAR(30) NOT NULL
);

CREATE TABLE PACIENTE (
  Cod_Paciente  INT         PRIMARY KEY,
  Nombre        VARCHAR(50) NOT NULL,
  F_Nacimiento  DATE        NOT NULL,
  Cod_Prepaga   INT         REFERENCES PREPAGA (Cod_Prepaga)
);

CREATE TABLE PACIENTE_TELEFONO (
  Cod_Paciente INT         NOT NULL REFERENCES PACIENTE (Cod_Paciente),
  Telefono     VARCHAR(20) NOT NULL,
  PRIMARY KEY (Cod_Paciente, Telefono)
);

CREATE TABLE OCUPACION (
  Cod_Habitacion   INT  NOT NULL REFERENCES HABITACION (Cod_Habitacion),
  Cod_Paciente     INT  NOT NULL REFERENCES PACIENTE (Cod_Paciente),
  F_Desde          DATE NOT NULL,
  F_Hasta_Prevista DATE,
  PRIMARY KEY (Cod_Habitacion, Cod_Paciente, F_Desde),
  CHECK (F_Hasta_Prevista >= F_Desde)
);

CREATE TABLE ESPECIALIDAD (
  Cod_Especialidad INT         PRIMARY KEY,
  Nombre           VARCHAR(30) NOT NULL
);

CREATE TABLE PROFESIONAL (
  Cod_Profesional  INT         PRIMARY KEY,
  Nombre           VARCHAR(50) NOT NULL,
  Cod_Especialidad INT         NOT NULL REFERENCES ESPECIALIDAD (Cod_Especialidad),
  Cod_Jefe         INT         REFERENCES PROFESIONAL (Cod_Profesional)
);

CREATE TABLE PROFESIONAL_TELEFONO (
  Cod_Profesional INT         NOT NULL REFERENCES PROFESIONAL (Cod_Profesional),
  Telefono        VARCHAR(20) NOT NULL,
  Tipo            VARCHAR(10) NOT NULL CHECK (Tipo IN ('Particular', 'Urgencia')),
  PRIMARY KEY (Cod_Profesional, Telefono)
);

CREATE TABLE HISTORIA_CLINICA (
  Cod_Paciente    INT          NOT NULL REFERENCES PACIENTE (Cod_Paciente),
  Id_Consulta     INT          NOT NULL,
  Fecha           DATE         NOT NULL,
  Diagnostico     VARCHAR(100),
  Cod_Servicio    INT          NOT NULL REFERENCES SERVICIO (Cod_Servicio),
  Cod_Profesional INT          NOT NULL REFERENCES PROFESIONAL (Cod_Profesional),
  PRIMARY KEY (Cod_Paciente, Id_Consulta)
);

INSERT INTO TORRE VALUES
  (1, 'Torre Norte', 'Hospitalización', 'Av. Rivadavia', 1500, NULL, NULL),
  (2, 'Torre Sur',   'Hospitalización', 'Av. Rivadavia', 1520, NULL, NULL),
  (3, 'Torre Este',  'Consulta',        'Av. Belgrano',  3500, 1,    'A');

INSERT INTO HABITACION VALUES
  (1, 1, 1, 101, 3.5, 4.0, 1, 'S', 1, 'S'),
  (2, 1, 1, 102, 3.5, 4.0, 1, 'N', 2, 'N'),
  (3, 1, 2, 201, 4.0, 5.0, 2, 'S', 2, 'S'),
  (4, 1, 2, 202, 4.0, 5.0, 1, 'N', 1, 'S'),
  (5, 1, 3, 301, 3.0, 3.5, 1, 'N', 1, 'N'),
  (6, 2, 1, 101, 3.5, 4.0, 1, 'S', 1, 'S'),
  (7, 2, 1, 102, 3.5, 4.0, 1, 'S', 2, 'N'),
  (8, 2, 2, 201, 5.0, 6.0, 2, 'S', 3, 'S');

INSERT INTO CONSULTORIO VALUES
  (1, 3, 1, 101, 3.0, 3.0),
  (2, 3, 1, 102, 3.0, 3.0),
  (3, 3, 2, 201, 3.5, 4.0),
  (4, 3, 2, 202, 3.5, 4.0);

INSERT INTO SERVICIO VALUES
  (1, 'Cardiología'), (2, 'Pediatría'), (3, 'Neurología'), (4, 'Ginecología'), (5, 'Fisioterapia');

INSERT INTO SERVICIO_CONSULTORIO VALUES
  (1, 1), (2, 2), (2, 3), (3, 3), (4, 4), (5, 4);

INSERT INTO PREPAGA VALUES
  (1, 'OSDE'), (2, 'Swiss Medical'), (3, 'Galeno'), (4, 'Medifé');

INSERT INTO PACIENTE VALUES
  (1,  'Juan Pérez',      '1985-03-12', 1),
  (2,  'María Gómez',     '1990-07-22', 2),
  (3,  'Tomás López',     '2018-11-05', 1),
  (4,  'Ana Martínez',    '1995-01-19', 3),
  (5,  'José Rodríguez',  '1958-12-30', 1),
  (6,  'Lucía Fernández', '2020-04-15', 2),
  (7,  'Pedro Sánchez',   '1982-09-28', NULL),
  (8,  'Sofía Díaz',      '1988-10-25', 3),
  (9,  'Mateo Silva',     '2015-03-25', 1),
  (10, 'Elena Castro',    '1960-05-17', NULL);

INSERT INTO PACIENTE_TELEFONO VALUES
  (1, '11-4000-0001'), (1, '11-5000-0001'), (2, '11-4000-0002'), (3, '11-4000-0003'),
  (5, '11-4000-0005'), (5, '11-5000-0005'), (6, '11-4000-0006'), (8, '11-4000-0008'),
  (9, '11-4000-0009');

INSERT INTO OCUPACION VALUES
  (1, 1,  '2026-10-01', '2026-10-20'),
  (2, 5,  '2026-10-05', '2026-10-25'),
  (2, 10, '2026-10-10', '2026-10-18'),
  (3, 4,  '2026-10-12', '2026-10-16'),
  (6, 7,  '2026-10-08', '2026-10-30'),
  (8, 2,  '2026-10-11', '2026-10-14');

INSERT INTO ESPECIALIDAD VALUES
  (1, 'Cardiología'), (2, 'Neurología'), (3, 'Ginecología'), (4, 'Pediatría'), (5, 'Kinesiología');

INSERT INTO PROFESIONAL VALUES
  (1, 'Carlos Méndez', 4, NULL),
  (4, 'Laura Gil',     1, NULL),
  (6, 'Marta Vera',    2, NULL),
  (8, 'Sofía Luna',    5, NULL),
  (2, 'Ana Ruiz',      4, 1),
  (3, 'Jorge Paz',     4, 1),
  (5, 'Diego Sosa',    1, 4),
  (7, 'Pablo Ríos',    3, 6);

INSERT INTO PROFESIONAL_TELEFONO VALUES
  (1, '4755-1001', 'Particular'), (1, '15-6000-1001', 'Urgencia'),
  (2, '4755-1002', 'Particular'), (2, '15-6000-1002', 'Urgencia'),
  (3, '4755-1003', 'Particular'), (3, '15-6000-1003', 'Urgencia'),
  (4, '4755-1004', 'Particular'), (4, '15-6000-1004', 'Urgencia'),
  (5, '4755-1005', 'Particular'), (5, '15-6000-1005', 'Urgencia'),
  (6, '4755-1006', 'Particular'), (6, '15-6000-1006', 'Urgencia'),
  (7, '4755-1007', 'Particular'), (7, '15-6000-1007', 'Urgencia'),
  (8, '4755-1008', 'Particular'), (8, '15-6000-1008', 'Urgencia');

INSERT INTO HISTORIA_CLINICA VALUES
  (1, 1, '2026-01-10', 'Arritmia',          1, 4),
  (1, 2, '2026-03-02', 'Control normal',    1, 5),
  (2, 1, '2026-02-01', 'Migraña',           3, 6),
  (3, 1, '2026-02-14', 'Bronquitis',        2, 2),
  (3, 2, '2026-05-20', 'Control niño sano', 2, 1),
  (4, 1, '2026-03-15', 'Control anual',     4, 7),
  (5, 1, '2026-07-07', 'Hipertensión',      1, 4),
  (5, 2, '2026-09-01', 'Hipertensión',      1, 5),
  (6, 1, '2026-04-03', 'Varicela',          2, 3),
  (8, 1, '2026-08-19', 'Esguince',          5, 8),
  (9, 1, '2026-06-11', 'Otitis',            2, 2);
`;
