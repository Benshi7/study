----------------
-- DESARROLLO --
----------------

-- DROP TABLE (DESA)--

DROP TABLE IF EXISTS DESA_TORRE;
DROP TABLE IF EXISTS DESA_PREPAGA;
DROP TABLE IF EXISTS DESA_PACIENTE;
DROP TABLE IF EXISTS DESA_HABITACION;
DROP TABLE IF EXISTS DESA_CONSULTORIO;
DROP TABLE IF EXISTS DESA_SERVICIO;
DROP TABLE IF EXISTS DESA_ESPECIALIDAD;
DROP TABLE IF EXISTS DESA_PROFESIONAL;
DROP TABLE IF EXISTS DESA_HISTORIA_CLINICA;
DROP TABLE IF EXISTS DESA_OCUPA;
DROP TABLE IF EXISTS DESA_PRESTADO;
DROP TABLE IF EXISTS DESA_PACIENTE_TELEFONO;
DROP TABLE IF EXISTS DESA_PROFESIONAL_TELEFONO;


-- CREATE TABLE (DESA)--

CREATE TABLE IF NOT EXISTS DESA_TORRE
(
  Id_Torre INT NOT NULL,
  Nombre VARCHAR(50) NOT NULL,
  TipoTorre VARCHAR(50) NOT NULL,
  Depto VARCHAR(5) NOT NULL,
  Calle VARCHAR(50) NOT NULL,
  Numero INT NOT NULL,
  Piso INT NOT NULL,
  PRIMARY KEY (Id_Torre)
);

CREATE TABLE IF NOT EXISTS DESA_PREPAGA
(
  Id_Prepaga INT NOT NULL,
  Nombre VARCHAR(50) NOT NULL,
  PRIMARY KEY (Id_Prepaga)
);

CREATE TABLE IF NOT EXISTS DESA_PACIENTE
(
  Id_Paciente INT NOT NULL,
  Fecha_Nacimiento DATE NOT NULL,
  Nombre VARCHAR(50) NOT NULL,
  Id_Prepaga INT NOT NULL,
  PRIMARY KEY (Id_Paciente),
  FOREIGN KEY (Id_Prepaga) REFERENCES DESA_PREPAGA(Id_Prepaga)
);

CREATE TABLE IF NOT EXISTS DESA_HABITACION
(
  Banio INT NOT NULL,
  Id_Habitacion INT NOT NULL,
  Cama INT NOT NULL,
  Numero INT NOT NULL,
  Longitud FLOAT NOT NULL,
  Piso INT NOT NULL,
  Closet INT NOT NULL,
  Ventana INT NOT NULL,
  Id_Torre INT NOT NULL,
  PRIMARY KEY (Id_Habitacion),
  FOREIGN KEY (Id_Torre) REFERENCES DESA_TORRE(Id_Torre)
);

CREATE TABLE IF NOT EXISTS DESA_CONSULTORIO
(
  Id_Consultorio INT NOT NULL,
  Piso INT NOT NULL,
  Numero INT NOT NULL,
  Longitud FLOAT NOT NULL,
  Id_Torre INT NOT NULL,
  PRIMARY KEY (Id_Consultorio),
  FOREIGN KEY (Id_Torre) REFERENCES DESA_TORRE(Id_Torre)
);

CREATE TABLE IF NOT EXISTS DESA_SERVICIO
(
  Id_Servicio INT NOT NULL,
  Nombre VARCHAR(50) NOT NULL,
  PRIMARY KEY (Id_Servicio)
);

CREATE TABLE IF NOT EXISTS DESA_ESPECIALIDAD
(
  Id_Especialidad INT NOT NULL,
  Nombre VARCHAR(50) NOT NULL,
  PRIMARY KEY (Id_Especialidad)
);

CREATE TABLE IF NOT EXISTS DESA_PROFESIONAL
(
  Id_Profesional INT NOT NULL,
  Nombre VARCHAR(50) NOT NULL,
  Id_Jefe INT NULL,
  Id_Especialidad INT NOT NULL,
  PRIMARY KEY (Id_Profesional),
  FOREIGN KEY (Id_Jefe) REFERENCES DESA_PROFESIONAL(Id_Profesional)
  FOREIGN KEY (Id_Especialidad) REFERENCES DESA_ESPECIALIDAD(Id_Especialidad)
);

CREATE TABLE IF NOT EXISTS DESA_HISTORIA_CLINICA
(
  Id_Consulta INT NOT NULL,
  Fecha DATE NOT NULL,
  Diagnostico VARCHAR(100) NOT NULL,
  Id_Paciente INT NOT NULL,
  Id_Servicio INT NOT NULL,
  Id_Profesional INT NOT NULL,
  PRIMARY KEY (Id_Paciente, Id_Consulta),
  FOREIGN KEY (Id_Paciente) REFERENCES DESA_PACIENTE(Id_Paciente),
  FOREIGN KEY (Id_Servicio) REFERENCES DESA_SERVICIO(Id_Servicio),
  FOREIGN KEY (Id_Profesional) REFERENCES DESA_PROFESIONAL(Id_Profesional)
);

CREATE TABLE IF NOT EXISTS DESA_OCUPA
(
  Fecha_Desde INT NOT NULL,
  Id_Habitacion INT NOT NULL,
  Id_Paciente INT NOT NULL,
  PRIMARY KEY (Id_Habitacion, Id_Paciente),
  FOREIGN KEY (Id_Habitacion) REFERENCES DESA_HABITACION(Id_Habitacion),
  FOREIGN KEY (Id_Paciente) REFERENCES DESA_PACIENTE(Id_Paciente)
);

CREATE TABLE IF NOT EXISTS DESA_PRESTADO
(
  Id_Servicio INT NOT NULL,
  Id_Consultorio INT NOT NULL,
  PRIMARY KEY (Id_Servicio, Id_Consultorio),
  FOREIGN KEY (Id_Servicio) REFERENCES DESA_SERVICIO(Id_Servicio),
  FOREIGN KEY (Id_Consultorio) REFERENCES DESA_CONSULTORIO(Id_Consultorio)
);

CREATE TABLE IF NOT EXISTS DESA_PACIENTE_TELEFONO
(
  Telefono VARCHAR(30) NOT NULL,
  Id_Paciente INT NOT NULL,
  PRIMARY KEY (Telefono, Id_Paciente),
  FOREIGN KEY (Id_Paciente) REFERENCES DESA_PACIENTE(Id_Paciente)
);

CREATE TABLE IF NOT EXISTS DESA_PROFESIONAL_TELEFONO
(
  Telefono VARCHAR(30) NOT NULL,
  Id_Profesional INT NOT NULL,
  PRIMARY KEY (Telefono, Id_Profesional),
  FOREIGN KEY (Id_Profesional) REFERENCES DESA_PROFESIONAL(Id_Profesional)
);

-- INSERT INTO (DESA) --

INSERT INTO DESA_TORRE
(Id_Torre, Nombre, TipoTorre, Depto, Calle, Numero, Piso)
VALUES
(1,	'Hospitalización',	'Hospitalización',	1,	'Av. Rivadavia',	1500,	1),
(2,	'Cirugías',	'Cirugías',	2,	'Av. Córdoba',	2500,	2),
(3,	'Consultas',	'Consultas',	3,	'Av. Belgrano',	3500,	3);

INSERT INTO DESA_PREPAGA
(Id_Prepaga, Nombre)
VALUES
(1, 'OSDE'),
(2, 'Swiss Medical'),
(3, 'Galeno');

INSERT INTO DESA_PACIENTE
(Id_Paciente, Fecha_Nacimiento, Nombre, Id_Prepaga)
VALUES
(1,	'1985-03-12', 'Juan Pérez',	1),
(2,	'1990-07-22', 'María Gómez',2),
(3,	'1978-11-05', 'Carlos López',3),
(4,	'1995-01-19', 'Ana Martínez',1),
(5,	'1965-12-30', 'José Rodríguez',2),
(6,	'1985-02-10', 'Pedro Suarez',2);

INSERT INTO DESA_HABITACION
(Banio, Id_Habitacion, Cama, Numero, Longitud, Piso, Closet, Ventana, Id_Torre)
VALUES
(0,	1,	1,	101,	2,	1,	1,	1,	1),
(1,	2,	2,	102,	3,	1,	0,	1,	1),
(0,	3,	1,	103,	4,	1,	1,	0,	1),
(1,	4,	2,	201,	2,	2,	0,	0,	1),
(0,	5,	1,	202,	3,	2,	1,	1,	1),
(1,	6,	2,	203,	4,	2,	0,	1,	1),
(0,	7,	1,	301,	2,	3,	1,	1,	1),
(1,	8,	2,	302,	3,	3,	0,	0,	1),
(0,	9,	1,	303,	4,	3,	1,	0,	1),
(1,	10,	2,	401,	2,	4,	0,	1,	1),
(0,	11,	1,	402,	2,	4,	1,	1,	1),
(1,	12,	2,	403,	3,	4,	0,	1,	1),
(0,	13,	1,	501,	4,	5,	1,	0,	1),
(1,	14,	2,	502,	2,	5,	0,	0,	1),
(0,	15,	1,	503,	3,	5,	1,	1,	1),
(0,	16,	2,	101,	2,	1,	1,	1,	2),
(1,	17,	1,	102,	3,	1,	0,	1,	2),
(0,	18,	2,	103,	4,	1,	1,	0,	2),
(1,	19,	1,	201,	2,	2,	0,	0,	2),
(0,	20,	2,	202,	3,	2,	1,	1,	2),
(1,	21,	1,	203,	4,	2,	0,	1,	2),
(0,	22,	2,	301,	2,	3,	1,	1,	2),
(1,	23,	1,	302,	3,	3,	0,	0,	2),
(0,	24,	2,	303,	4,	3,	1,	0,	2),
(1,	25,	1,	401,	2,	4,	0,	1,	2),
(0,	26,	2,	402,	2,	4,	1,	1,	2),
(1,	27,	1,	403,	3,	4,	0,	1,	2),
(0,	28,	2,	501,	4,	5,	1,	0,	2),
(1,	29,	1,	502,	2,	5,	0,	0,	2),
(0,	30,	2,	503,	3,	5,	1,	1,	2);

INSERT INTO DESA_CONSULTORIO
(Id_Consultorio, Piso, Numero, Longitud, Id_Torre)
VALUES
(1,	1,	101,	1,	3),
(2,	1,	102,	2,	3),
(3,	1,	103,	3,	3),
(4,	2,	201,	1,	3),
(5,	2,	202,	2,	3),
(6,	2,	203,	3,	3),
(7,	3,	301,	1,	3),
(8,	3,	302,	2,	3),
(9,	3,	303,	3,	3);

INSERT INTO DESA_SERVICIO
(Id_Servicio, Nombre)
VALUES
(1, 'Cardiología'),
(2, 'Neurología'),
(3, 'Ginecología'),
(4, 'Dermatología'),
(5, 'Traumatología'),
(6, 'Pediatría');

INSERT INTO DESA_ESPECIALIDAD
(Id_Especialidad, Nombre)
VALUES
(1, 'Cirugía Cardiovascular'),
(2, 'Neurología'),
(3, 'Ginecología'),
(4, 'Dermatología'),
(5, 'Ortopedia'),
(6, 'Pediatría');

INSERT INTO DESA_PROFESIONAL
(Id_Profesional, Nombre, Id_Jefe, Id_Especialidad)
VALUES
(1,	'Alan Guevara',	null,	1),
(2,	'Juan Francisco Villarreal',	1,	1),
(3,	'Carlos Pascual Castillo',	1,	1),
(4,	'Ignat Krukovskiy',	null,	2),
(5,	'Mirkala Parra',	2,	2),
(6,	'Luis Santillan',	null,	3),
(7,	'Celia Bruno',	3,	3);

INSERT INTO DESA_HISTORIA_CLINICA
(Id_Consulta, Fecha, Diagnostico, Id_Paciente, Id_Servicio, Id_Profesional)
VALUES
(1,	'2026-01-06',	'A',	1,	1,	1),
(2,	'2026-02-16',	'B',	2,	2,	2),
(3,	'2026-03-05',	'C',	3,	3,	3),
(4,	'2026-04-08',	'D',	4,	4,	4),
(5,	'2026-07-13',	'E',	5,	5,	5),
(6,	'2026-08-23',	'F',	6,	6,	6);

INSERT INTO DESA_OCUPA
(Fecha_Desde, Id_Habitacion, Id_Paciente)
VALUES
('2026-08-01',	1,	1),
('2026-08-02',	2,	2),
('2026-08-03',	3,	3),
('2026-08-04',	4,	4),
('2026-08-05',	5,	5);

INSERT INTO DESA_PRESTADO
(Id_Servicio, Id_Consultorio)
VALUES
(1,	1),
(2,	2),
(3,	3),
(4,	4),
(5,	5);

INSERT INTO DESA_PACIENTE_TELEFONO
(Telefono, Id_Paciente)
VALUES
('15-5-555-0001',1),
('15-5-555-0002',2),
('15-5-555-0003',3),
('15-5-555-0004',4),
('15-5-555-0005',5),
('15-5-555-0006',6);

INSERT INTO DESA_PROFESIONAL_TELEFONO
(Telefono, Id_Profesional)
VALUES
('15-5-555-1001',1),
('15-5-555-2002',2),
('15-5-555-3003',3),
('15-5-555-4004',4),
('15-5-555-5005',5);


----------------
-- PRODUCCION --
----------------

-- DROP TABLE (PROD)--

DROP TABLE IF EXISTS PROD_TOWER;
DROP TABLE IF EXISTS PROD_HEALTH_PLAN;
DROP TABLE IF EXISTS PROD_PATIENT;
DROP TABLE IF EXISTS PROD_ROOM;
DROP TABLE IF EXISTS PROD_CONSULTING_ROOM;
DROP TABLE IF EXISTS PROD_SERVICE;
DROP TABLE IF EXISTS PROD_SPECIALTY;
DROP TABLE IF EXISTS PROD_PROFESSIONAL;
DROP TABLE IF EXISTS PROD_MEDICAL_RECORD;
DROP TABLE IF EXISTS PROD_OCCUPIES;
DROP TABLE IF EXISTS PROD_PROVIDED;
DROP TABLE IF EXISTS PROD_PATIENT_PHONE;
DROP TABLE IF EXISTS PROD_PROFESSIONAL_PHONE;

-- CREATE TABLE (PROD) --

CREATE TABLE IF NOT EXISTS PROD_TOWER
(
  Tower_Id INT NOT NULL,
  Name VARCHAR(50) NOT NULL,
  TowerType VARCHAR(50) NOT NULL,
  Department VARCHAR(5) NOT NULL,
  Street VARCHAR(50) NOT NULL,
  Number INT NOT NULL,
  Floor INT NOT NULL,
  PRIMARY KEY (Tower_Id)
);

CREATE TABLE IF NOT EXISTS PROD_HEALTH_PLAN
(
  Id_Health_Plan INT NOT NULL,
  Name VARCHAR(50) NOT NULL,
  PRIMARY KEY (Id_Health_Plan)
);

CREATE TABLE IF NOT EXISTS PROD_PATIENT
(
  Patient_Id INT NOT NULL,
  Birthday DATE NOT NULL,
  Name VARCHAR(50) NOT NULL,
  Id_Health_Plan INT NOT NULL,
  PRIMARY KEY (Patient_Id),
  FOREIGN KEY (Id_Health_Plan) REFERENCES PROD_HEALTH_PLAN(Id_Health_Plan)
);

CREATE TABLE IF NOT EXISTS PROD_ROOM
(
  Bathroom INT NOT NULL,
  Room_Id INT NOT NULL,
  Bed INT NOT NULL,
  Number INT NOT NULL,
  Length FLOAT NOT NULL,
  Floor INT NOT NULL,
  Closet INT NOT NULL,
  Window INT NOT NULL,
  Tower_Id INT NOT NULL,
  PRIMARY KEY (Room_Id),
  FOREIGN KEY (Tower_Id) REFERENCES PROD_TOWER(Tower_Id)
);

CREATE TABLE IF NOT EXISTS PROD_CONSULTING_ROOM
(
  Consulting_Room_Id INT NOT NULL,
  Floor INT NOT NULL,
  Number INT NOT NULL,
  Length FLOAT NOT NULL,
  Tower_Id INT NOT NULL,
  PRIMARY KEY (Consulting_Room_Id),
  FOREIGN KEY (Tower_Id) REFERENCES PROD_TOWER(Tower_Id)
);

CREATE TABLE IF NOT EXISTS PROD_SERVICE
(
  Service_Id INT NOT NULL,
  Name VARCHAR(50) NOT NULL,
  PRIMARY KEY (Service_Id)
);

CREATE TABLE IF NOT EXISTS PROD_SPECIALTY
(
  Specialty_Id INT NOT NULL,
  Name VARCHAR(50) NOT NULL,
  PRIMARY KEY (Specialty_Id)
);

CREATE TABLE IF NOT EXISTS PROD_PROFESSIONAL
(
  Professional_Id INT NOT NULL,
  Name VARCHAR(50) NOT NULL,
  Boss_Id INT NULL,
  Specialty_Id INT NOT NULL,
  PRIMARY KEY (Professional_Id),
  FOREIGN KEY (Boss_Id) REFERENCES PROD_PROFESSIONAL(Professional_Id)
  FOREIGN KEY (Specialty_Id) REFERENCES PROD_SPECIALTY(Specialty_Id)
);

CREATE TABLE IF NOT EXISTS PROD_MEDICAL_RECORD
(
  Consultation_Id INT NOT NULL,
  Date Date NOT NULL,
  Diagnostic VARCHAR(100) NOT NULL,
  Patient_Id INT NOT NULL,
  Service_Id INT NOT NULL,
  Professional_Id INT NOT NULL,
  PRIMARY KEY (Patient_Id, Consultation_Id),
  FOREIGN KEY (Patient_Id) REFERENCES PROD_PATIENT(Patient_Id),
  FOREIGN KEY (Service_Id) REFERENCES PROD_SERVICE(Service_Id),
  FOREIGN KEY (Professional_Id) REFERENCES PROD_PROFESSIONAL(Professional_Id)
);

CREATE TABLE IF NOT EXISTS PROD_OCCUPIES
(
  From_Date DATE NOT NULL,
  Room_Id INT NOT NULL,
  Patient_Id INT NOT NULL,
  PRIMARY KEY (Room_Id, Patient_Id),
  FOREIGN KEY (Room_Id) REFERENCES PROD_ROOM(Room_Id),
  FOREIGN KEY (Patient_Id) REFERENCES PROD_PATIENT(Patient_Id)
);

CREATE TABLE IF NOT EXISTS PROD_PROVIDED
(
  Service_Id INT NOT NULL,
  Consulting_Room_Id INT NOT NULL,
  PRIMARY KEY (Service_Id, Consulting_Room_Id),
  FOREIGN KEY (Service_Id) REFERENCES PROD_SERVICE(Service_Id),
  FOREIGN KEY (Consulting_Room_Id) REFERENCES PROD_CONSULTING_ROOM(Consulting_Room_Id)
);

CREATE TABLE IF NOT EXISTS PROD_PATIENT_PHONE
(
  Phone VARCHAR(30) NOT NULL,
  Patient_Id INT NOT NULL,
  PRIMARY KEY (Phone, Patient_Id),
  FOREIGN KEY (Patient_Id) REFERENCES PROD_PATIENT(Patient_Id)
);

CREATE TABLE IF NOT EXISTS PROD_PROFESSIONAL_PHONE
(
  Phone VARCHAR(30) NOT NULL,
  Professional_Id INT NOT NULL,
  PRIMARY KEY (Phone, Professional_Id),
  FOREIGN KEY (Professional_Id) REFERENCES PROD_PROFESSIONAL(Professional_Id)
);

-- INSERT INTO - SELECT (PROD)--

INSERT INTO PROD_TOWER
(Tower_Id, Name, TowerType, Department, Street, "Number", Floor)
SELECT Id_Torre, Nombre, TipoTorre, Depto, Calle, Numero, Piso
FROM DESA_TORRE;

INSERT INTO PROD_HEALTH_PLAN
(Id_Health_Plan, Name)
SELECT Id_Prepaga, Nombre
FROM DESA_PREPAGA;

INSERT INTO PROD_PATIENT
(Patient_Id, Birthday, Name, Id_Health_Plan)
SELECT Id_Paciente, Fecha_Nacimiento, Nombre, Id_Prepaga
FROM DESA_PACIENTE;

INSERT INTO PROD_ROOM
(Bathroom, Room_Id, Bed, "Number", "Length", Floor, Closet, "Window", Tower_Id)
SELECT Banio, Id_Habitacion, Cama, Numero, Longitud, Piso, Closet, Ventana, Id_Torre
FROM DESA_HABITACION;

INSERT INTO PROD_CONSULTING_ROOM
(Consulting_Room_Id, Floor, "Number", "Length", Tower_Id)
SELECT Id_Consultorio, Piso, Numero, Longitud, Id_Torre
FROM DESA_CONSULTORIO;

INSERT INTO PROD_SERVICE
(Service_Id, Name)
SELECT Id_Servicio, Nombre
FROM DESA_SERVICIO;

INSERT INTO PROD_SPECIALTY
(Specialty_Id, Name)
SELECT Id_Especialidad, Nombre
FROM DESA_ESPECIALIDAD;

INSERT INTO PROD_PROFESSIONAL
(Professional_Id, Name, Boss_Id, Specialty_Id)
SELECT Id_Profesional, Nombre, Id_Jefe, Id_Especialidad
FROM DESA_PROFESIONAL;

INSERT INTO PROD_MEDICAL_RECORD
(Consultation_Id, Date, Diagnostic, Patient_Id, Service_Id, Professional_Id)
SELECT Id_Consulta, Fecha, Diagnostico, Id_Paciente, Id_Servicio, Id_Profesional
FROM DESA_HISTORIA_CLINICA;

INSERT INTO PROD_OCCUPIES
(From_Date, Room_Id, Patient_Id)
SELECT Fecha_Desde, Id_Habitacion, Id_Paciente
FROM DESA_OCUPA;

INSERT INTO PROD_PROVIDED
(Service_Id, Consulting_Room_Id)
SELECT Id_Servicio, Id_Consultorio
FROM DESA_PRESTADO;

INSERT INTO PROD_PATIENT_PHONE
(Phone, Patient_Id)
SELECT Telefono, Id_Paciente
FROM DESA_PACIENTE_TELEFONO;

INSERT INTO PROD_PROFESSIONAL_PHONE
(Phone, Professional_Id)
SELECT Telefono, Id_Profesional
FROM DESA_PROFESIONAL_TELEFONO;

------------
-- Vistas --
------------
/*
  ● Para las vistas usar como prefijo Vista_Nombre (Ej: Vista_Torre).
  ● Crear todas las vistas apuntando a producción con sus campos en español.
*/

DROP VIEW IF EXISTS Vista_Consultorio;
CREATE VIEW Vista_Consultorio
AS 
SELECT 
	Consulting_Room_Id as Id_Consultorio,
	Floor as Piso, 
	Number as Numero, 
	Length as Longitud, 
	Tower_Id as Id_Torre
FROM PROD_CONSULTING_ROOM;

DROP VIEW IF EXISTS Vista_Especialidad;
CREATE VIEW Vista_Especialidad
AS 
SELECT 
	Specialty_Id as Id_Especialidad, 
	Name as Nombre
FROM PROD_SPECIALTY;

DROP VIEW IF EXISTS Vista_Habitacion;
CREATE VIEW Vista_Habitacion
AS 
SELECT 
	Bathroom as Banio, 
	Room_Id as Id_Habitacion, 
	Bed as Cama, 
	Number as Numero, 
	Length as Longitud, 
	Floor as Piso, 
	Closet, 
	Window as Ventana, 
	Tower_Id as Id_Torre
FROM PROD_ROOM;

DROP VIEW IF EXISTS Vista_Historia_Clinica;
CREATE VIEW Vista_Historia_Clinica
AS 
SELECT 
	Consultation_Id as Id_Consulta, 
	Date as Fecha,
	Diagnostic as Diagnostico, 
	Patient_Id as Id_Paciente, 
	Service_Id as Id_Servicio, 
	Professional_Id as Id_Profesional
FROM PROD_MEDICAL_RECORD;

DROP VIEW IF EXISTS Vista_Ocupa;
CREATE VIEW Vista_Ocupa
AS 
SELECT 
	From_Date as Fecha_Desde, 
	Room_Id as Id_Habitacion, 
	Patient_Id as Id_Paciente
FROM PROD_OCCUPIES;

DROP VIEW IF EXISTS Vista_Paciente;
CREATE VIEW Vista_Paciente
AS 
SELECT 
	Patient_Id as Id_Paciente, 
	Birthday as Fecha_Nacimiento, 
	Name as Nombre, 
	Id_Health_Plan as Id_Prepaga
FROM PROD_PATIENT;

DROP VIEW IF EXISTS Vista_Paciente_Telefono;
CREATE VIEW Vista_Paciente_Telefono
AS 
SELECT 
	Phone as Telefono, 
	Patient_Id as Id_Paciente
FROM PROD_PATIENT_PHONE;

DROP VIEW IF EXISTS Vista_Prepaga;
CREATE VIEW Vista_Prepaga
AS 
SELECT 
	Id_Health_Plan as Id_Prepaga, 
	Name as Nombre
FROM PROD_HEALTH_PLAN;

DROP VIEW IF EXISTS Vista_Prestado;
CREATE VIEW Vista_Prestado
AS 
SELECT 
	Service_Id as Id_Servicio, 
	Consulting_Room_Id as Id_Consultorio
FROM PROD_PROVIDED;

DROP VIEW IF EXISTS Vista_Profesional;
CREATE VIEW Vista_Profesional
AS 
SELECT 
	Professional_Id as Id_Profesional, 
	Name as Nombre, 
	Boss_Id as Id_Jefe, 
	Specialty_Id as Id_Especialidad
FROM PROD_PROFESSIONAL;

DROP VIEW IF EXISTS Vista_Profesional_Telefono;
CREATE VIEW Vista_Profesional_Telefono
AS 
SELECT 
	Phone as Telefono, 
	Professional_Id as Id_Profesional
FROM PROD_PROFESSIONAL_PHONE;

DROP VIEW IF EXISTS Vista_Servicio;
CREATE VIEW Vista_Servicio
AS 
SELECT 
	Service_Id as Id_Servicio, 
	Name as Nombre
FROM PROD_SERVICE;

DROP VIEW IF EXISTS Vista_Torre;
CREATE VIEW Vista_Torre
AS 
SELECT 
	Tower_Id as Id_Torre, 
	Name as Nombre, 
	TowerType as TipoTorre, 
	Department as Depto, 
	Street as Calle, 
	Number as Numero, 
	Floor as Piso
FROM PROD_TOWER;
 

/*
● Crear la vista RRHH_Medicos con las siguientes características:
● Todos los campos de la entidad medico.
● Indicador de medico jefe. (SI/NO)
● Indicador de especialidad de riesgo para las especialidades con Id 2 y 3.
● Para los médicos jefes se requiere un campo que sea la concatenación del
  campo Id de médico , las primeras seis letras del nombre y el nombre de su especialidad.
  Ejemplo (1-Carlos-Pediatra) para el resto de los médicos solo su especialidad (Pediatria
*/

DROP VIEW IF EXISTS Vista_RRHH_Medicos;
CREATE VIEW IF NOT EXISTS Vista_RRHH_Medicos 
AS 
SELECT pp.Professional_Id AS Id_Profesional, 
       pp.Name AS Nombre, 
       pp.Boss_Id AS Id_Jefe, 
       pp.Specialty_Id AS Id_Especialidad, 
CASE WHEN EXISTS (SELECT 1 FROM PROD_PROFESSIONAL s WHERE s.Boss_Id = pp.Professional_Id) THEN 'Si' ELSE 'No' END AS Jefe,
CASE WHEN pp.Specialty_Id IN(2,3) THEN 'Si' ELSE 'No' END AS Especialidad_de_riesgo,
CASE WHEN EXISTS (SELECT 1 FROM PROD_PROFESSIONAL s WHERE s.Boss_Id = pp.Professional_Id) THEN CONCAT(pp.Professional_Id, '-', SUBSTR(pp.Name,1,6), '-', ps.Name ) ELSE ps.Name END AS Medico
from prod_professional pp
INNER JOIN PROD_SPECIALTY ps ON (pp.Specialty_Id = ps.Specialty_Id);



