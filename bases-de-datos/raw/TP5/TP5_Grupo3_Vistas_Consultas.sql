-- TP5 Clínica - Grupo 3
-- Vistas y consultas (correr después de TP5_Grupo3_Scrips.sql)

----------------------
-- AJUSTE DE DATOS --
----------------------

-- La torre 3 es la de consultas: se sacan sus habitaciones y esos pacientes pasan a la torre 1
UPDATE DESA_PACIENTE SET Id_Torre = 1 WHERE Id_Torre = 3;
DELETE FROM DESA_HABITACION WHERE Id_Torre = 3;

-- Habitaciones pares sin ventana
UPDATE DESA_HABITACION SET Posee_Ventanas = 0 WHERE Numero % 2 = 0;

-- Nombres sin "Dr." / "Dra."
UPDATE DESA_PROFESIONAL
SET Nombre_Profesional = REPLACE(REPLACE(Nombre_Profesional, 'Dra. ', ''), 'Dr. ', '');

-- Pediatras y consultas de Pediatría
INSERT INTO DESA_PROFESIONAL
(Id_Profesional, Nombre_Profesional, Telefono_Particular, Telefono_Urgencia, Id_Especialidad, Id_Jefe)
VALUES
(8, 'Carlos Benedetti', '4755-1240', '15-5-123-4564', 6, NULL),
(9, 'Lucía Fontana',    '4755-1241', '15-5-123-4565', 6, 8);

INSERT INTO DESA_CONSULTA
(Id_Consulta, Fecha_Consulta, Motivo_Consulta, Diagnostico, Id_Torre, Piso, Numero, Id_Servicio, Id_Profesional)
VALUES
(21, '2026-02-01', 'Control niño sano', 'Sano',        3, 1, 101, 6, 8),
(22, '2026-02-02', 'Fiebre',            'Faringitis',  3, 1, 102, 6, 9),
(23, '2026-02-03', 'Vacunación',        'Sano',        3, 1, 103, 6, 9);

INSERT INTO DESA_HISTORIA_CLINICA (Id_Historia, Id_Paciente, Id_Consulta)
VALUES (21, 14, 21), (22, 25, 22), (23, 14, 23);

-- Recarga de producción (insert select)
DELETE FROM PROD_PATIENT;
INSERT INTO PROD_PATIENT (Patient_Id, Name, Date_Birth, Age, Tower_Id, Floor, Number, Prepaid_Id)
SELECT Id_Paciente, Nombre, Fecha_Nacimiento, Edad, Id_Torre, Piso, Numero, Id_Prepaga FROM DESA_PACIENTE;

DELETE FROM PROD_ROOM;
INSERT INTO PROD_ROOM (Tower_Id, Floor, Number, Number_of_Bathrooms, Has_Closet, Number_of_Beds, Has_Windows, Occupancy_Date)
SELECT Id_Torre, Piso, Numero, Cantidad_Banios, Posee_Closet, Cantidad_Camas, Posee_Ventanas, Fecha_Ocupacion FROM DESA_HABITACION;

DELETE FROM PROD_PROFESSIONAL;
INSERT INTO PROD_PROFESSIONAL (Professional_Id, Professional_Name, Personal_Phone, Emergency_Phone, Specialty_Id, Supervisor_Id)
SELECT Id_Profesional, Nombre_Profesional, Telefono_Particular, Telefono_Urgencia, Id_Especialidad, Id_Jefe FROM DESA_PROFESIONAL;

DELETE FROM PROD_QUERY;
INSERT INTO PROD_QUERY (Query_Id, Query_Date, Query_Reason, Diagnostic, Tower_Id, Floor, Number, Service_Id, Professional_Id)
SELECT Id_Consulta, Fecha_Consulta, Motivo_Consulta, Diagnostico, Id_Torre, Piso, Numero, Id_Servicio, Id_Profesional FROM DESA_CONSULTA;

DELETE FROM PROD_CLINIC_HISTORY;
INSERT INTO PROD_CLINIC_HISTORY (History_Id, Patient_Id, Query_Id)
SELECT Id_Historia, Id_Paciente, Id_Consulta FROM DESA_HISTORIA_CLINICA;


------------
-- VISTAS --
------------

-- Todas las vistas apuntan a producción con sus campos en español

DROP VIEW IF EXISTS Vista_Torre;
CREATE VIEW Vista_Torre AS
SELECT Tower_Id AS Id_Torre, Street AS Calle, Number AS Numero, Floor AS Piso,
       Department AS Dpto, Type AS Tipo
FROM PROD_TOWER;

DROP VIEW IF EXISTS Vista_Espacio;
CREATE VIEW Vista_Espacio AS
SELECT Tower_Id AS Id_Torre, Floor AS Piso, Number AS Numero, Width AS Ancho, Long AS Largo
FROM PROD_SPACE;

DROP VIEW IF EXISTS Vista_Habitacion;
CREATE VIEW Vista_Habitacion AS
SELECT Tower_Id AS Id_Torre, Floor AS Piso, Number AS Numero,
       Number_of_Bathrooms AS Cantidad_Banios, Has_Closet AS Posee_Closet,
       Number_of_Beds AS Cantidad_Camas, Has_Windows AS Posee_Ventanas,
       Occupancy_Date AS Fecha_Ocupacion
FROM PROD_ROOM;

DROP VIEW IF EXISTS Vista_Consultorio;
CREATE VIEW Vista_Consultorio AS
SELECT Tower_Id AS Id_Torre, Floor AS Piso, Number AS Numero
FROM PROD_CONSULTATION;

DROP VIEW IF EXISTS Vista_Prepaga;
CREATE VIEW Vista_Prepaga AS
SELECT Prepaid_Id AS Id_Prepaga, Prepaid_Name AS Nombre_Prepaga
FROM PROD_PREPAID;

DROP VIEW IF EXISTS Vista_Paciente;
CREATE VIEW Vista_Paciente AS
SELECT Patient_Id AS Id_Paciente, Name AS Nombre, Date_Birth AS Fecha_Nacimiento, Age AS Edad,
       Tower_Id AS Id_Torre, Floor AS Piso, Number AS Numero, Prepaid_Id AS Id_Prepaga
FROM PROD_PATIENT;

DROP VIEW IF EXISTS Vista_Paciente_Telefonos;
CREATE VIEW Vista_Paciente_Telefonos AS
SELECT Phones AS Telefono, Patient_Id AS Id_Paciente
FROM PROD_PATIENT_PHONES;

DROP VIEW IF EXISTS Vista_Servicio;
CREATE VIEW Vista_Servicio AS
SELECT Service_Id AS Id_Servicio, Service_Name AS Nombre_Servicio
FROM PROD_SERVICE;

DROP VIEW IF EXISTS Vista_Especialidad;
CREATE VIEW Vista_Especialidad AS
SELECT Specialty_Id AS Id_Especialidad, Specialty_Name AS Nombre_Especialidad
FROM PROD_SPECIALTY;

DROP VIEW IF EXISTS Vista_Profesional;
CREATE VIEW Vista_Profesional AS
SELECT Professional_Id AS Id_Profesional, Professional_Name AS Nombre_Profesional,
       Personal_Phone AS Telefono_Particular, Emergency_Phone AS Telefono_Urgencia,
       Specialty_Id AS Id_Especialidad, Supervisor_Id AS Id_Jefe
FROM PROD_PROFESSIONAL;

DROP VIEW IF EXISTS Vista_Consulta;
CREATE VIEW Vista_Consulta AS
SELECT Query_Id AS Id_Consulta, Query_Date AS Fecha_Consulta, Query_Reason AS Motivo_Consulta,
       Diagnostic AS Diagnostico, Tower_Id AS Id_Torre, Floor AS Piso, Number AS Numero,
       Service_Id AS Id_Servicio, Professional_Id AS Id_Profesional
FROM PROD_QUERY;

DROP VIEW IF EXISTS Vista_Historia_Clinica;
CREATE VIEW Vista_Historia_Clinica AS
SELECT History_Id AS Id_Historia, Patient_Id AS Id_Paciente, Query_Id AS Id_Consulta
FROM PROD_CLINIC_HISTORY;


------------------
-- RRHH_MEDICOS --
------------------

-- Todos los campos de la entidad médico
-- Indicador de médico jefe (SI/NO): es jefe si tiene algún médico a cargo
-- Indicador de especialidad de riesgo: especialidades con Id 2 y 3
-- Jefes: Id-primeras seis letras del nombre-especialidad (ej. 1-Carlos-Pediatra); resto: solo la especialidad

DROP VIEW IF EXISTS RRHH_Medicos;
CREATE VIEW RRHH_Medicos AS
SELECT P.Professional_Id    AS Id_Profesional,
       P.Professional_Name  AS Nombre_Profesional,
       P.Personal_Phone     AS Telefono_Particular,
       P.Emergency_Phone    AS Telefono_Urgencia,
       P.Specialty_Id       AS Id_Especialidad,
       P.Supervisor_Id      AS Id_Jefe,
       CASE WHEN EXISTS (SELECT 1 FROM PROD_PROFESSIONAL S WHERE S.Supervisor_Id = P.Professional_Id)
            THEN 'SI' ELSE 'NO' END                       AS Es_Jefe,
       CASE WHEN P.Specialty_Id IN (2, 3)
            THEN 'SI' ELSE 'NO' END                       AS Especialidad_Riesgo,
       CASE WHEN EXISTS (SELECT 1 FROM PROD_PROFESSIONAL S WHERE S.Supervisor_Id = P.Professional_Id)
            THEN P.Professional_Id || '-' || SUBSTR(P.Professional_Name, 1, 6) || '-' || E.Specialty_Name
            ELSE E.Specialty_Name END                     AS Identificador
FROM PROD_PROFESSIONAL P
JOIN PROD_SPECIALTY E ON E.Specialty_Id = P.Specialty_Id;


---------------
-- CONSULTAS --
---------------

-- 1. Listar los pacientes que se atendieron en el servicio de Pediatría
SELECT DISTINCT PA.Id_Paciente, PA.Nombre
FROM Vista_Paciente PA
JOIN Vista_Historia_Clinica H ON H.Id_Paciente = PA.Id_Paciente
JOIN Vista_Consulta C         ON C.Id_Consulta = H.Id_Consulta
JOIN Vista_Servicio S         ON S.Id_Servicio = C.Id_Servicio
WHERE S.Nombre_Servicio = 'Pediatría';

-- 2. Listar los teléfonos de los pacientes que pertenezcan a OSDE
SELECT PA.Nombre, T.Telefono
FROM Vista_Paciente PA
JOIN Vista_Prepaga PR           ON PR.Id_Prepaga = PA.Id_Prepaga
JOIN Vista_Paciente_Telefonos T ON T.Id_Paciente = PA.Id_Paciente
WHERE PR.Nombre_Prepaga = 'OSDE';

-- 3. Informar la cantidad de habitaciones de la Torre 1
SELECT COUNT(*) AS Cantidad_Habitaciones
FROM Vista_Habitacion
WHERE Id_Torre = 1;

-- 4. Listar el nombre de los pacientes internados en habitaciones con ventana
SELECT PA.Nombre, H.Id_Torre, H.Piso, H.Numero
FROM Vista_Paciente PA
JOIN Vista_Habitacion H ON H.Id_Torre = PA.Id_Torre
                       AND H.Piso     = PA.Piso
                       AND H.Numero   = PA.Numero
WHERE H.Posee_Ventanas = 1;

-- 5. Listar los médicos que no son jefes y su especialidad
SELECT Nombre_Profesional, E.Nombre_Especialidad
FROM RRHH_Medicos R
JOIN Vista_Especialidad E ON E.Id_Especialidad = R.Id_Especialidad
WHERE R.Es_Jefe = 'NO';

-- 6. Listar los médicos que son supervisados por un médico determinado (ej. Alan Guevara)
SELECT M.Id_Profesional, M.Nombre_Profesional
FROM Vista_Profesional M
JOIN Vista_Profesional J ON J.Id_Profesional = M.Id_Jefe
WHERE J.Nombre_Profesional = 'Alan Guevara';


-------------
-- TRIGGER --
-------------

-- Un espacio no puede ser habitación y consultorio a la vez
DROP TRIGGER IF EXISTS TRG_Habitacion_Disjunta;
CREATE TRIGGER TRG_Habitacion_Disjunta
BEFORE INSERT ON PROD_ROOM
FOR EACH ROW
WHEN EXISTS (SELECT 1 FROM PROD_CONSULTATION C
             WHERE C.Tower_Id = NEW.Tower_Id AND C.Floor = NEW.Floor AND C.Number = NEW.Number)
BEGIN
  SELECT RAISE(ABORT, 'Ese espacio ya es un consultorio');
END;
