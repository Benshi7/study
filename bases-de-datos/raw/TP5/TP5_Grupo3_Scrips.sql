----------------
-- DESARROLLO --
----------------

-- DROP TABLE (DESA)--

DROP TABLE IF EXISTS DESA_TORRE;
DROP TABLE IF EXISTS DESA_ESPACIO;
DROP TABLE IF EXISTS DESA_HABITACION;
DROP TABLE IF EXISTS DESA_CONSULTORIO;
DROP TABLE IF EXISTS DESA_PREPAGA;  
DROP TABLE IF EXISTS DESA_PACIENTE;
DROP TABLE IF EXISTS DESA_SERVICIO;
DROP TABLE IF EXISTS DESA_ESPECIALIDAD; 
DROP TABLE IF EXISTS DESA_PROFESIONAL;
DROP TABLE IF EXISTS DESA_CONSULTA; 
DROP TABLE IF EXISTS DESA_HISTORIA_CLINICA;
DROP TABLE IF EXISTS DESA_PACIENTE_TELEFONOS;

-- CREATE TABLE (DESA)--

CREATE TABLE IF NOT EXISTS DESA_TORRE
(
  Id_Torre INT NOT NULL,
  Calle VARCHAR(20) NOT NULL,
  Numero INT NOT NULL,
  Piso INT NOT NULL,
  Dpto CHAR(1) NOT NULL,  
  Tipo VARCHAR(20) NOT NULL,
  PRIMARY KEY (Id_Torre)
);

CREATE TABLE IF NOT EXISTS DESA_ESPACIO
(
  Id_Torre INT NOT NULL,
  Piso INT NOT NULL,
  Numero INT NOT NULL,  
  Ancho FLOAT NOT NULL,
  Largo FLOAT NOT NULL,
  PRIMARY KEY (Id_Torre, Piso, Numero),
  FOREIGN KEY (Id_Torre) REFERENCES DESA_TORRE(Id_Torre)
);

CREATE TABLE IF NOT EXISTS DESA_HABITACION
(
  Id_Torre INT NOT NULL,
  Piso INT NOT NULL,
  Numero INT NOT NULL,
  Cantidad_Banios INT NOT NULL,
  Posee_Closet INT NOT NULL,
  Cantidad_Camas INT NOT NULL,
  Posee_Ventanas INT NOT NULL,
  Fecha_Ocupacion DATE NULL,
  PRIMARY KEY (Id_Torre, Piso, Numero),
  FOREIGN KEY (Id_Torre, Piso, Numero) REFERENCES DESA_ESPACIO(Id_Torre, Piso, Numero)
);

CREATE TABLE IF NOT EXISTS DESA_CONSULTORIO
(
  Id_Torre INT NOT NULL,
  Piso INT NOT NULL,
  Numero INT NOT NULL,
  PRIMARY KEY (Id_Torre, Piso, Numero),
  FOREIGN KEY (Id_Torre, Piso, Numero) REFERENCES DESA_ESPACIO(Id_Torre, Piso, Numero)
);

CREATE TABLE IF NOT EXISTS DESA_PREPAGA
(
  Id_Prepaga INT NOT NULL,
  Nombre_Prepaga VARCHAR(50) NOT NULL,
  PRIMARY KEY (Id_Prepaga)
);

CREATE TABLE IF NOT EXISTS DESA_PACIENTE
(
  Id_Paciente INT NOT NULL,
  Nombre VARCHAR(50) NOT NULL,
  Fecha_Nacimiento CHAR(8) NOT NULL,
  Edad INT NOT NULL,
  Id_Torre INT NOT NULL,
  Piso INT NOT NULL,
  Numero INT NOT NULL,
  Id_Prepaga INT NOT NULL,
  PRIMARY KEY (Id_Paciente),
  FOREIGN KEY (Id_Torre, Piso, Numero) REFERENCES DESA_HABITACION(Id_Torre, Piso, Numero),
  FOREIGN KEY (Id_Prepaga) REFERENCES DESA_PREPAGA(Id_Prepaga)
);

CREATE TABLE IF NOT EXISTS DESA_SERVICIO
(
  Id_Servicio INT NOT NULL,
  Nombre_Servicio VARCHAR(50) NOT NULL,
  PRIMARY KEY (Id_Servicio)
);

CREATE TABLE IF NOT EXISTS DESA_ESPECIALIDAD
(
  Id_Especialidad INT NOT NULL,
  Nombre_Especialidad VARCHAR(50) NOT NULL,
  PRIMARY KEY (Id_Especialidad)
);

CREATE TABLE IF NOT EXISTS DESA_PROFESIONAL
(
  Id_Profesional INT NOT NULL,
  Nombre_Profesional VARCHAR(50) NOT NULL,
  Telefono_Particular VARCHAR(50) NOT NULL,
  Telefono_Urgencia VARCHAR(50) NOT NULL,
  Id_Especialidad INT NOT NULL,
  Id_Jefe INT NULL,
  PRIMARY KEY (Id_Profesional),
  FOREIGN KEY (Id_Especialidad) REFERENCES DESA_ESPECIALIDAD(Id_Especialidad),
  FOREIGN KEY (Id_Jefe) REFERENCES DESA_PROFESIONAL(Id_Profesional)
);

CREATE TABLE IF NOT EXISTS DESA_CONSULTA
(
  Id_Consulta INT NOT NULL,
  Fecha_Consulta DATE NOT NULL,
  Motivo_Consulta VARCHAR(100) NOT NULL,  
  Diagnostico VARCHAR(100) NOT NULL,
  Id_Torre INT NOT NULL,
  Piso INT NOT NULL,
  Numero INT NOT NULL,
  Id_Servicio INT NOT NULL,
  Id_Profesional INT NOT NULL,
  PRIMARY KEY (Id_Consulta),
  FOREIGN KEY (Id_Torre, Piso, Numero) REFERENCES DESA_CONSULTORIO(Id_Torre, Piso, Numero),
  FOREIGN KEY (Id_Servicio) REFERENCES DESA_SERVICIO(Id_Servicio),
  FOREIGN KEY (Id_Profesional) REFERENCES DESA_PROFESIONAL(Id_Profesional)
);

CREATE TABLE IF NOT EXISTS DESA_HISTORIA_CLINICA
(
  Id_Historia INT NOT NULL,
  Id_Paciente INT NOT NULL,
  Id_Consulta INT NOT NULL,
  PRIMARY KEY (Id_Historia, Id_Paciente, Id_Consulta),
  FOREIGN KEY (Id_Paciente) REFERENCES DESA_PACIENTE(Id_Paciente),
  FOREIGN KEY (Id_Consulta) REFERENCES DESA_CONSULTA(Id_Consulta)
);

CREATE TABLE IF NOT EXISTS DESA_PACIENTE_TELEFONOS
(
  Telefonos VARCHAR(20) NOT NULL,
  Id_Paciente INT NOT NULL,
  PRIMARY KEY (Telefonos, Id_Paciente),
  FOREIGN KEY (Id_Paciente) REFERENCES DESA_PACIENTE(Id_Paciente)
);

-- INSERT INTO (DESA) --

INSERT INTO DESA_TORRE (Id_Torre, Calle, Numero, Piso, Dpto, Tipo)
VALUES(1, 'Av. Rivadavia',1500 , 1, 'A', 'Hospitalización'),
	  (2, 'Av. Córdoba',2500 , 2, 'B', 'Cirugías'),
	  (3, 'Av. Belgrano',3500 , 3, 'C', 'Consultas');

INSERT INTO DESA_ESPACIO (Id_Torre, Piso, Numero, Ancho, Largo)
VALUES
(1, 1, 101, 1.5, 2.5),
(1, 1, 102, 3.5, 4.5),
(1, 1, 103, 5.5, 6.5),
(1, 1, 104, 7.5, 7.5),
(1, 1, 105, 9.5, 10.5),
(1, 2, 201, 1.5, 2.5),
(1, 2, 202, 3.5, 4.5),
(1, 2, 203, 5.5, 6.5),
(1, 2, 204, 7.5, 7.5),
(1, 2, 205, 9.5, 10.5),
(1, 3, 301, 1.5, 2.5),
(1, 3, 302, 3.5, 4.5),
(1, 3, 303, 5.5, 6.5),
(1, 3, 304, 7.5, 7.5),
(1, 3, 305, 9.5, 10.5),
(1, 4, 401, 1.5, 2.5),
(1, 4, 402, 3.5, 4.5),
(1, 4, 403, 5.5, 6.5),
(1, 4, 404, 7.5, 7.5),
(1, 4, 405, 9.5, 10.5),
(1, 5, 501, 1.5, 2.5),
(1, 5, 502, 3.5, 4.5),
(1, 5, 503, 5.5, 6.5),
(1, 5, 504, 7.5, 7.5),
(1, 5, 505, 9.5, 10.5),
(2, 1, 101, 1.5, 2.5),
(2, 1, 102, 3.5, 4.5),
(2, 1, 103, 5.5, 6.5),
(2, 1, 104, 7.5, 7.5),
(2, 1, 105, 9.5, 10.5),
(2, 2, 201, 1.5, 2.5),
(2, 2, 202, 3.5, 4.5),
(2, 2, 203, 5.5, 6.5),
(2, 2, 204, 7.5, 7.5),
(2, 2, 205, 9.5, 10.5),
(2, 3, 301, 1.5, 2.5),
(2, 3, 302, 3.5, 4.5),
(2, 3, 303, 5.5, 6.5),
(2, 3, 304, 7.5, 7.5),
(2, 3, 305, 9.5, 10.5),
(2, 4, 401, 1.5, 2.5),
(2, 4, 402, 3.5, 4.5),
(2, 4, 403, 5.5, 6.5),
(2, 4, 404, 7.5, 7.5),
(2, 4, 405, 9.5, 10.5),
(2, 5, 501, 1.5, 2.5),
(2, 5, 502, 3.5, 4.5),
(2, 5, 503, 5.5, 6.5),
(2, 5, 504, 7.5, 7.5),
(2, 5, 505, 9.5, 10.5),
(3, 1, 101, 1.5, 2.5),
(3, 1, 102, 3.5, 4.5),
(3, 1, 103, 5.5, 6.5),
(3, 1, 104, 7.5, 7.5),
(3, 1, 105, 9.5, 10.5),
(3, 2, 201, 1.5, 2.5),
(3, 2, 202, 3.5, 4.5),
(3, 2, 203, 5.5, 6.5),
(3, 2, 204, 7.5, 7.5),
(3, 2, 205, 9.5, 10.5),
(3, 3, 301, 1.5, 2.5),
(3, 3, 302, 3.5, 4.5),
(3, 3, 303, 5.5, 6.5),
(3, 3, 304, 7.5, 7.5),
(3, 3, 305, 9.5, 10.5),
(3, 4, 401, 1.5, 2.5),
(3, 4, 402, 3.5, 4.5),
(3, 4, 403, 5.5, 6.5),
(3, 4, 404, 7.5, 7.5),
(3, 4, 405, 9.5, 10.5),
(3, 5, 501, 1.5, 2.5),
(3, 5, 502, 3.5, 4.5),
(3, 5, 503, 5.5, 6.5),
(3, 5, 504, 7.5, 7.5),
(3, 5, 505, 9.5, 10.5);

INSERT INTO DESA_HABITACION
(Id_Torre, Piso, Numero, Cantidad_Banios, Posee_Closet, Cantidad_Camas, Posee_Ventanas, Fecha_Ocupacion)
VALUES
(1, 1, 101, 1, 0, 1, 1, '2026-01-01'),
(1, 1, 102, 2, 1, 1, 1, '2026-01-02'),
(1, 1, 103, 1, 0, 1, 1, '2026-01-03'),
(1, 1, 104, 2, 1, 1, 1, '2026-01-04'),
(1, 1, 105, 1, 0, 1, 1, '2026-01-05'),
(1, 2, 201, 1, 0, 1, 1, '2026-01-06'),
(1, 2, 202, 2, 1, 1, 1, '2026-01-07'),
(1, 2, 203, 1, 0, 1, 1, '2026-01-08'),
(1, 2, 204, 2, 1, 1, 1, '2026-01-09'),
(1, 2, 205, 1, 0, 1, 1, '2026-01-10'),
(1, 3, 301, 1, 0, 1, 1, '2026-01-01'),
(1, 3, 302, 2, 1, 1, 1, '2026-01-02'),
(1, 3, 303, 1, 0, 1, 1, '2026-01-03'),
(1, 3, 304, 2, 1, 1, 1, '2026-01-04'),
(1, 3, 305, 1, 0, 1, 1, '2026-01-05'),
(1, 4, 401, 1, 0, 1, 1, '2026-01-06'),
(1, 4, 402, 2, 1, 1, 1, '2026-01-07'),
(1, 4, 403, 1, 0, 1, 1, '2026-01-08'),
(1, 4, 404, 2, 1, 1, 1, '2026-01-09'),
(1, 4, 405, 1, 0, 1, 1, '2026-01-10'),
(1, 5, 501, 1, 0, 1, 1, '2026-01-11'),
(1, 5, 502, 2, 1, 1, 1, '2026-01-12'),
(1, 5, 503, 1, 0, 1, 1, '2026-01-13'),
(1, 5, 504, 2, 1, 1, 1, '2026-01-14'),
(1, 5, 505, 1, 0, 1, 1, '2026-01-15'),
(2, 1, 101, 1, 0, 1, 1, '2026-01-16'),
(2, 1, 102, 2, 1, 1, 1, '2026-01-17'),
(2, 1, 103, 1, 0, 1, 1, '2026-01-18'),
(2, 1, 104, 2, 1, 1, 1, '2026-01-19'),
(2, 1, 105, 1, 0, 1, 1, '2026-01-20'),
(2, 2, 201, 1, 0, 1, 1, '2026-01-21'),
(2, 2, 202, 2, 1, 1, 1, '2026-01-22'),
(2, 2, 203, 1, 0, 1, 1, '2026-01-23'),
(2, 2, 204, 2, 1, 1, 1, '2026-01-24'),
(2, 2, 205, 1, 0, 1, 1, '2026-01-25'),
(2, 3, 301, 1, 0, 1, 1, '2026-01-26'),
(2, 3, 302, 2, 1, 1, 1, '2026-01-27'),
(2, 3, 303, 1, 0, 1, 1, '2026-01-28'),
(2, 3, 304, 2, 1, 1, 1, '2026-01-29'),
(2, 3, 305, 1, 0, 1, 1, '2026-01-30'),
(2, 4, 401, 1, 0, 1, 1, '2026-02-01'),
(2, 4, 402, 2, 1, 1, 1, '2026-02-02'),
(2, 4, 403, 1, 0, 1, 1, '2026-02-03'),
(2, 4, 404, 2, 1, 1, 1, '2026-02-04'),
(2, 4, 405, 1, 0, 1, 1, '2026-02-05'),
(2, 5, 501, 1, 0, 1, 1, '2026-02-01'),
(2, 5, 502, 2, 1, 1, 1, '2026-02-01'),
(2, 5, 503, 1, 0, 1, 1, '2026-02-02'),
(2, 5, 504, 2, 1, 1, 1, '2026-02-02'),
(2, 5, 505, 1, 0, 1, 1, '2026-02-10'),
(3, 1, 101, 1, 0, 1, 1, '2026-03-10'),
(3, 1, 102, 2, 1, 1, 1, '2026-03-11'),
(3, 1, 103, 1, 0, 1, 1, '2026-03-12'),
(3, 1, 104, 2, 1, 1, 1, '2026-03-13'),
(3, 1, 105, 1, 0, 1, 1, '2026-03-14'),
(3, 2, 201, 1, 0, 1, 1, '2026-03-15'),
(3, 2, 202, 2, 1, 1, 1, '2026-03-16'),
(3, 2, 203, 1, 0, 1, 1, '2026-03-17'),
(3, 2, 204, 2, 1, 1, 1, '2026-03-18'),
(3, 2, 205, 1, 0, 1, 1, '2026-03-19'),
(3, 3, 301, 1, 0, 1, 1, '2026-04-01'),
(3, 3, 302, 2, 1, 1, 1, '2026-04-02'),
(3, 3, 303, 1, 0, 1, 1, '2026-04-03'),
(3, 3, 304, 2, 1, 1, 1, '2026-04-04'),
(3, 3, 305, 1, 0, 1, 1, '2026-04-05'),
(3, 4, 401, 1, 0, 1, 1, '2026-04-06'),
(3, 4, 402, 2, 1, 1, 1, '2026-04-07'),
(3, 4, 403, 1, 0, 1, 1, '2026-04-08'),
(3, 4, 404, 2, 1, 1, 1, '2026-04-09'),
(3, 4, 405, 1, 0, 1, 1, '2026-04-10'),
(3, 5, 501, 1, 0, 1, 1, '2026-05-01'),
(3, 5, 502, 2, 1, 1, 1, '2026-05-02'),
(3, 5, 503, 1, 0, 1, 1, '2026-05-03'),
(3, 5, 504, 2, 1, 1, 1, '2026-05-04'),
(3, 5, 505, 1, 0, 1, 1, '2026-05-05');

INSERT INTO DESA_CONSULTORIO
(Id_Torre, Piso, Numero)
VALUES
(3, 1, 101),
(3, 1, 102),
(3, 1, 103),
(3, 1, 104),
(3, 1, 105),
(3, 2, 201),
(3, 2, 202),
(3, 2, 203),
(3, 2, 204),
(3, 2, 205),
(3, 3, 301),
(3, 3, 302),
(3, 3, 303),
(3, 3, 304),
(3, 3, 305),
(3, 4, 401),
(3, 4, 402),
(3, 4, 403),
(3, 4, 404),
(3, 4, 405),
(3, 5, 501),
(3, 5, 502),
(3, 5, 503),
(3, 5, 504),
(3, 5, 505);

INSERT INTO DESA_PREPAGA
(Id_Prepaga, Nombre_Prepaga)
VALUES
(1, 'OSDE'),
(2, 'Swiss Medical'),
(3, 'Galeno');

INSERT INTO DESA_PACIENTE (Id_Paciente, Nombre, Fecha_Nacimiento, Edad, Id_Torre, Piso, Numero, Id_Prepaga) VALUES
(1, 'Juan Pérez', '19850312', 41, 1, 1, 101, 2),
(2, 'María Gómez', '19900722', 35, 2, 2, 203, 1),
(3, 'Carlos López', '19781105', 47, 3, 3, 305, 3),
(4, 'Ana Martínez', '19950119', 31, 1, 4, 402, 2),
(5, 'José Rodríguez', '19651230', 60, 2, 5, 504, 1),
(6, 'Laura Fernández', '20000415', 26, 3, 1, 102, 3),
(7, 'Pedro Sánchez', '19820928', 43, 1, 2, 201, 2),
(8, 'Lucía Ramírez', '19930614', 33, 2, 3, 303, 1),
(9, 'Miguel Torres', '19750809', 50, 3, 4, 405, 3),
(10, 'Sofía Díaz', '19881025', 38, 1, 5, 501, 2),
(11, 'Jorge Ruiz', '19920203', 34, 2, 1, 104, 1),
(12, 'Elena Castro', '19600517', 66, 3, 2, 202, 3),
(13, 'Daniel Vargas', '19841201', 41, 1, 3, 301, 2),
(14, 'Valentina Ortiz', '19980911', 27, 2, 4, 403, 1),
(15, 'Mateo Silva', '19710325', 55, 3, 5, 505, 3),
(16, 'Camila Morales', '19890630', 36, 1, 1, 103, 2),
(17, 'Lucas Herrera', '19941118', 31, 2, 2, 205, 1),
(18, 'Martina Medina', '19680704', 57, 3, 3, 302, 3),
(19, 'Joaquín Castro', '19810420', 45, 1, 4, 404, 2),
(20, 'Paula Romero', '19961208', 29, 2, 5, 502, 1),
(21, 'Gabriel Sosa', '19770115', 49, 3, 1, 105, 3),
(22, 'Florencia Benítez', '19910529', 35, 1, 2, 204, 2),
(23, 'Agustín Acosta', '19830810', 42, 2, 3, 304, 1),
(24, 'Victoria Flores', '19700223', 56, 3, 4, 401, 3),
(25, 'Nicolás Molina', '19970907', 28, 1, 5, 503, 2),
(26, 'Carla Delgado', '19861012', 39, 2, 1, 101, 1),
(27, 'Facundo Rojas', '19920321', 34, 3, 2, 203, 3),
(28, 'Julieta Navarro', '19790616', 46, 1, 3, 305, 2),
(29, 'Esteban Bravo', '19801127', 45, 2, 4, 402, 1),
(30, 'Rocío Campos', '19950819', 31, 3, 5, 504, 3),
(31, 'Gonzalo Paredes', '19670411', 59, 1, 1, 102, 2),
(32, 'Jimena Iglesias', '19881205', 37, 2, 2, 201, 1),
(33, 'Federico Cabrera', '19900130', 36, 3, 3, 303, 3),
(34, 'Natalia Paz', '19740522', 52, 1, 4, 405, 2),
(35, 'Mariano Ríos', '19830914', 42, 2, 5, 501, 1),
(36, 'Clara Mendez', '19990308', 27, 3, 1, 104, 3),
(37, 'Ignacio Vega', '19721018', 53, 1, 2, 202, 2),
(38, 'Micaela Quiroga', '19870726', 38, 2, 3, 301, 1),
(39, 'Bruno Figueroa', '19930214', 33, 3, 4, 403, 3),
(40, 'Antonella Maldonado', '19811109', 44, 1, 5, 505, 2),
(41, 'Ezequiel Mansilla', '19760603', 50, 2, 1, 103, 1),
(42, 'Melina Peralta', '19960417', 30, 3, 2, 205, 3),
(43, 'Damián Ponce', '19850125', 41, 1, 3, 302, 2),
(44, 'Sabrina Cáceres', '19910831', 34, 2, 4, 404, 1),
(45, 'Franco Godoy', '19691211', 56, 3, 5, 502, 3),
(46, 'Brenda Albornoz', '19940506', 32, 1, 1, 105, 2),
(47, 'Mauricio Avalos', '19780219', 48, 2, 2, 204, 1),
(48, 'Solange Coronel', '19890923', 36, 3, 3, 304, 3),
(49, 'Leandro Ferreyra', '19821030', 43, 1, 4, 401, 2),
(50, 'Julián Gamarra', '19970712', 28, 2, 5, 503, 1),
(51, 'Romina Juarez', '19730401', 53, 3, 1, 101, 3),
(52, 'Hernán Leiva', '19860315', 40, 1, 2, 203, 2),
(53, 'Patricia Luna', '19921120', 34, 2, 3, 305, 1),
(54, 'Adrián Montenegro', '19660825', 59, 3, 4, 402, 3),
(55, 'Gimena Ojeda', '19840107', 42, 1, 5, 504, 2),
(56, 'Renzo Orellana', '19950618', 31, 2, 1, 102, 1),
(57, 'Silvina Palma', '19750912', 50, 3, 2, 201, 3),
(58, 'Tomás Peralta', '19880228', 38, 1, 3, 303, 2),
(59, 'Verónica Quevedo', '19901004', 35, 2, 4, 405, 1),
(60, 'Walter Roldán', '19641219', 61, 3, 5, 501, 3),
(61, 'Zoe Toledo', '19980515', 28, 1, 1, 104, 2),
(62, 'Alfonso Varela', '19710722', 54, 2, 2, 202, 1),
(63, 'Beatriz Zarate', '19831108', 42, 3, 3, 301, 3),
(64, 'Cristian Baez', '19930419', 33, 1, 4, 403, 2),
(65, 'Daniela Carrizo', '19800814', 45, 2, 5, 505, 1),
(66, 'Emiliano Donatti', '19960102', 30, 3, 1, 103, 3),
(67, 'Fabiola Escudero', '19770327', 49, 1, 2, 205, 2),
(68, 'Gastón Farias', '19890611', 37, 2, 3, 302, 1),
(69, 'Helena Garay', '19940925', 31, 3, 4, 404, 3),
(70, 'Iván Huenuqueo', '19681015', 57, 1, 5, 502, 2),
(71, 'Jazmín Ibarra', '19910218', 35, 2, 1, 105, 1),
(72, 'Kevin Jara', '19820509', 44, 3, 2, 204, 3),
(73, 'Lorena Ledesma', '19991203', 26, 1, 3, 304, 2),
(74, 'Marcos Maciel', '19740716', 51, 2, 4, 401, 1),
(75, 'Nadia Neira', '19870330', 39, 3, 5, 503, 3);

INSERT INTO DESA_SERVICIO
(Id_Servicio, Nombre_Servicio)
VALUES
(1, 'Cardiología'),
(2, 'Neurología'),
(3, 'Ginecología'),
(4, 'Dermatología'),
(5, 'Traumatología'),
(6, 'Pediatría');

INSERT INTO DESA_ESPECIALIDAD
(Id_Especialidad, Nombre_Especialidad)
VALUES
(1, 'Cirugía Cardiovascular'),
(2, 'Neurología'),
(3, 'Ginecología'),
(4, 'Dermatología'),
(5, 'Ortopedia'),
(6, 'Pediatría');

INSERT INTO DESA_PROFESIONAL
(Id_Profesional, Nombre_Profesional, Telefono_Particular, Telefono_Urgencia, Id_Especialidad, Id_Jefe)
VALUES
(1, 'Dr. Alan Guevara', '4755-1234', '15-5-123-4567', 1, NULL),
(2, 'Dr. Juan Francisco Villarreal', '4755-1235', '15-5-123-4568', 1, 1),
(3, 'Dr. Carlos Pascual Castillo', '4755-1236', '15-5-123-4569', 1, 1),
(4, 'Dr. Ignat Krukovskiy', '4755-1237', '15-5-123-4560', 2, NULL),
(5, 'Dra. Mirkala Parra', '4755-1238', '15-5-123-4561', 2, 4),
(6, 'Dr. Luis Santillan', '4755-1239', '15-5-123-4562', 3, NULL),
(7, 'Dra. Celia Bruno', '4755-1230', '15-5-123-4563', 3, 6);

INSERT INTO DESA_CONSULTA
(Id_Consulta, Fecha_Consulta, Motivo_Consulta, Diagnostico, Id_Torre, Piso, Numero, Id_Servicio, Id_Profesional)
VALUES
(1 ,'2026-01-01','Control de rutina','Arritmia',3,1,101,1,1),
(2 ,'2026-01-02','Dolor de cabeza','Coágulo',3,2,102,2,2),
(3 ,'2026-01-03','Chequeo','Anticonceptivo',3,3,103,3,3),
(4 ,'2026-01-04','Tratamiento para la piel','Protector solar',3,4,104,4,4),
(5 ,'2026-01-05','Esguince de tobillo','Reposo',3,5,105,5,5),
(6 ,'2026-01-06','Control de rutina','Arritmia',3,1,101,1,1),
(7 ,'2026-01-07','Dolor de cabeza','Coágulo',3,2,102,2,2),
(8 ,'2026-01-08','Chequeo','Anticonceptivo',3,3,103,3,3),
(9 ,'2026-01-09','Tratamiento para la piel','Protector solar',3,4,104,4,4),
(10,'2026-01-10','Esguince de tobillo','Reposo',3,5,105,5,5),
(11,'2026-01-01','Control de rutina','Arritmia',3,1,101,1,1),
(12,'2026-01-02','Dolor de cabeza','Coágulo',3,2,102,2,2),
(13,'2026-01-03','Chequeo','Anticonceptivo',3,3,103,3,3),
(14,'2026-01-04','Tratamiento para la piel','Protector solar',3,4,104,4,4),
(15,'2026-01-05','Esguince de tobillo','Reposo',3,5,105,5,5),
(16,'2026-01-06','Control de rutina','Arritmia',3,1,101,1,1),
(17,'2026-01-07','Dolor de cabeza','Coágulo',3,2,102,2,2),
(18,'2026-01-08','Chequeo','Anticonceptivo',3,3,103,3,3),
(19,'2026-01-09','Tratamiento para la piel','Protector solar',3,4,104,4,4),
(20,'2026-01-10','Esguince de tobillo','Reposo',3,5,105,5,5);

INSERT INTO DESA_HISTORIA_CLINICA
(Id_Historia, Id_Paciente, Id_Consulta)
VALUES
 (1, 1,	 1),
 (2, 2,	 2),
 (3, 3,	 3),
 (4, 4,	 4),
 (5, 5,	 5),
 (6, 1,	 6),
 (7, 2,	 7),
 (8, 3,	 8),
 (9, 4,	 9),
(10, 5,	10),
(11, 1,	11),
(12, 2,	12),
(13, 3,	13),
(14, 4,	14),
(15, 5,	15),
(16, 1,	16),
(17, 2,	17),
(18, 3,	18),
(19, 4,	19),
(20, 5,	20);

INSERT INTO DESA_PACIENTE_TELEFONOS
(Telefonos, Id_Paciente)
VALUES
('15-5-555-0001',1),
('15-5-555-0002',2),
('15-5-555-0003',3),
('15-5-555-0004',4),
('15-5-555-0005',5),
('15-5-555-0006',6),
('15-5-555-0007',7),
('15-5-555-0008',8),
('15-5-555-0009',9),
('15-5-555-0010',10),
('15-5-555-0011',11),
('15-5-555-0012',12),
('15-5-555-0013',13),
('15-5-555-0014',14),
('15-5-555-0015',15),
('15-5-555-0016',16),
('15-5-555-0017',17),
('15-5-555-0018',18),
('15-5-555-0019',19),
('15-5-555-0020',20);


----------------
-- PRODUCCION --
----------------

-- DROP TABLE (PROD)--

DROP TABLE IF EXISTS PROD_TOWER;
DROP TABLE IF EXISTS PROD_SPACE;
DROP TABLE IF EXISTS PROD_ROOM;
DROP TABLE IF EXISTS PROD_CONSULTATION;
DROP TABLE IF EXISTS PROD_PREPAID;
DROP TABLE IF EXISTS PROD_PATIENT;
DROP TABLE IF EXISTS PROD_SERVICE;
DROP TABLE IF EXISTS PROD_SPECIALTY;
DROP TABLE IF EXISTS PROD_PROFESSIONAL;
DROP TABLE IF EXISTS PROD_QUERY;
DROP TABLE IF EXISTS PROD_CLINIC_HISTORY;
DROP TABLE IF EXISTS PROD_PATIENT_PHONES;

-- CREATE TABLE (PROD) --

CREATE TABLE IF NOT EXISTS PROD_TOWER
( 
Tower_Id INT NOT NULL, 
Street VARCHAR(20) NOT NULL, 
Number INT NOT NULL,
Floor INT NOT NULL, 
Department CHAR(1) NOT NULL, 
Type VARCHAR(20) NOT NULL, 
PRIMARY KEY (Tower_Id)
);

CREATE TABLE IF NOT EXISTS PROD_SPACE
( 
Tower_Id INT NOT NULL, 
Floor INT NOT NULL, 
Number INT NOT NULL,
Width FLOAT NOT NULL, 
Long FLOAT NOT NULL, 
PRIMARY KEY (Tower_Id, Floor, Number), 
FOREIGN KEY (Tower_Id) REFERENCES PROD_TOWER(Tower_Id)
);

CREATE TABLE IF NOT EXISTS PROD_ROOM
(
Tower_Id INT NOT NULL,
Floor INT NOT NULL,
Number INT NOT NULL,
Number_of_Bathrooms INT NOT NULL,
Has_Closet INT NOT NULL,
Number_of_Beds INT NOT NULL,
Has_Windows INT NOT NULL,
Occupancy_Date DATE NULL,
PRIMARY KEY (Tower_Id, Floor, Number),
FOREIGN KEY (Tower_Id, Floor, Number) REFERENCES PROD_SPACE(Tower_Id, Floor, Number)
);

CREATE TABLE IF NOT EXISTS PROD_CONSULTATION
( 
Tower_Id INT NOT NULL, 
Floor INT NOT NULL, 
Number INT NOT NULL,
PRIMARY KEY (Tower_Id, Floor, Number), 
FOREIGN KEY (Tower_Id, Floor, Number) REFERENCES PROD_SPACE(Tower_Id, Floor, Number)
);

CREATE TABLE IF NOT EXISTS PROD_PREPAID
( 
Prepaid_Id INT NOT NULL, 
Prepaid_Name VARCHAR(50) NOT NULL, 
PRIMARY KEY (Prepaid_Id)
);

CREATE TABLE IF NOT EXISTS PROD_PATIENT
( 
Patient_Id INT NOT NULL, 
Name VARCHAR(50) NOT NULL, 
Date_Birth CHAR(8) NOT NULL, 
Age INT NOT NULL, 
Tower_Id INT NOT NULL, 
Floor INT NOT NULL, 
Number INT NOT NULL,
Prepaid_Id INT NOT NULL, 
PRIMARY KEY (Patient_Id), 
CONSTRAINT PROD_PATIENT_PROD_ROOM_FK FOREIGN KEY (Tower_Id, Floor, Number) REFERENCES PROD_ROOM(Tower_Id, Floor, Number), 
FOREIGN KEY (Prepaid_Id) REFERENCES PROD_PREPAID(Prepaid_Id)
);

CREATE TABLE IF NOT EXISTS PROD_SERVICE
(
Service_Id INT NOT NULL,
Service_Name VARCHAR(50) NOT NULL,
PRIMARY KEY (Service_Id)
);

CREATE TABLE IF NOT EXISTS PROD_SPECIALTY
(
Specialty_Id INT NOT NULL,
Specialty_Name VARCHAR(50) NOT NULL,
PRIMARY KEY (Specialty_Id)
);

CREATE TABLE IF NOT EXISTS PROD_PROFESSIONAL
(
Professional_Id INT NOT NULL,
Professional_Name VARCHAR(50) NOT NULL,
Personal_Phone VARCHAR(50) NOT NULL,
Emergency_Phone VARCHAR(50) NOT NULL,
Specialty_Id INT NOT NULL,
Supervisor_Id INT NULL,
PRIMARY KEY (Professional_Id),
FOREIGN KEY (Specialty_Id) REFERENCES PROD_SPECIALTY(Specialty_Id),
FOREIGN KEY (Supervisor_Id) REFERENCES PROD_PROFESSIONAL(Professional_Id)
);

CREATE TABLE IF NOT EXISTS PROD_QUERY
( 
Query_Id INT NOT NULL, 
Query_Date DATE NOT NULL, 
Query_Reason VARCHAR(100) NOT NULL, 
Diagnostic VARCHAR(100) NOT NULL, 
Tower_Id INT NOT NULL, 
Floor INT NOT NULL, 
Number INT NOT NULL,
Service_Id INT NOT NULL, 
Professional_Id INT NOT NULL, 
PRIMARY KEY (Query_Id), 
FOREIGN KEY (Tower_Id, Floor, Number) REFERENCES PROD_CONSULTATION(Tower_Id, Floor, Number), 
FOREIGN KEY (Service_Id) REFERENCES PROD_SERVICE(Service_Id), 
FOREIGN KEY (Professional_Id) REFERENCES PROD_PROFESSIONAL(Professional_Id)
);

CREATE TABLE IF NOT EXISTS PROD_CLINIC_HISTORY
( 
History_Id INT NOT NULL, 
Patient_Id INT NOT NULL, 
Query_Id INT NOT NULL, 
PRIMARY KEY (History_Id, Patient_Id, Query_Id), 
FOREIGN KEY (Patient_Id) REFERENCES PROD_PATIENT(Patient_Id), 
FOREIGN KEY (Query_Id) REFERENCES PROD_QUERY(Query_Id)
);

CREATE TABLE IF NOT EXISTS PROD_PATIENT_PHONES
(
  Phones VARCHAR(20) NOT NULL,
  Patient_Id INT NOT NULL, 
  PRIMARY KEY (Phones, Patient_Id),
  FOREIGN KEY (Patient_Id) REFERENCES PROD_PATIENT(Patient_Id)
);

-- INSERT INTO - SELECT (PROD)--

INSERT INTO PROD_TOWER
(Tower_Id, Street, Number, Floor, Department, Type)
SELECT Id_Torre, Calle, Numero, Piso, Dpto, Tipo
FROM DESA_TORRE;

INSERT INTO PROD_SPACE
(Tower_Id, Floor, Number, Width, Long)
SELECT Id_Torre, Piso, Numero, Ancho, Largo
FROM DESA_ESPACIO;

INSERT INTO PROD_ROOM
(Tower_Id, Floor, Number, Number_of_Bathrooms, Has_Closet, Number_of_Beds, Has_Windows, Occupancy_Date)
SELECT Id_Torre, Piso, Numero, Cantidad_Banios, Posee_Closet, Cantidad_Camas, Posee_Ventanas, Fecha_Ocupacion
FROM DESA_HABITACION;

INSERT INTO PROD_CONSULTATION
(Tower_Id, Floor, Number)
SELECT Id_Torre, Piso, Numero
FROM DESA_CONSULTORIO;

INSERT INTO PROD_PREPAID
(Prepaid_Id, Prepaid_Name)
SELECT Id_Prepaga, Nombre_Prepaga
FROM DESA_PREPAGA;

INSERT INTO PROD_PATIENT
(Patient_Id, Name, Date_Birth, Age, Tower_Id, Floor, Number, Prepaid_Id)
SELECT Id_Paciente, Nombre, Fecha_Nacimiento, Edad, Id_Torre, Piso, Numero, Id_Prepaga
FROM DESA_PACIENTE;

INSERT INTO PROD_SPECIALTY
(Specialty_Id, Specialty_Name)
SELECT Id_Especialidad, Nombre_Especialidad
FROM DESA_ESPECIALIDAD;

INSERT INTO PROD_SERVICE
(Service_Id, Service_Name)
SELECT Id_Servicio, Nombre_Servicio
FROM DESA_SERVICIO;

INSERT INTO PROD_PROFESSIONAL
(Professional_Id, Professional_Name, Personal_Phone, Emergency_Phone, Specialty_Id, Supervisor_Id)
SELECT Id_Profesional, Nombre_Profesional, Telefono_Particular, Telefono_Urgencia, Id_Especialidad, Id_Jefe
FROM DESA_PROFESIONAL;

INSERT INTO PROD_QUERY
(Query_Id, Query_Date, Query_Reason, Diagnostic, Tower_Id, Floor, Number, Service_Id, Professional_Id)
SELECT Id_Consulta, Fecha_Consulta, Motivo_Consulta, Diagnostico, Id_Torre, Piso, Numero, Id_Servicio, Id_Profesional
FROM DESA_CONSULTA;

INSERT INTO PROD_CLINIC_HISTORY
(History_Id, Patient_Id, Query_Id)
SELECT Id_Historia, Id_Paciente, Id_Consulta
FROM DESA_HISTORIA_CLINICA;

INSERT INTO PROD_PATIENT_PHONES
(Phones, Patient_Id)
SELECT Telefonos, Id_Paciente
FROM DESA_PACIENTE_TELEFONOS;
