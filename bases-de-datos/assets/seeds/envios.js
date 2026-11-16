/* Proveedores / Componentes / Artículos / Envíos — las cuatro tablas del modelo de
   examen raw/Material_Examen/bd parcial 1a.jpg y 1b.jpg, copiadas tal cual.
   Las columnas P#, C#, T# se llaman P, C y T porque # no es válido en un nombre. */
window.SQL_SEEDS = window.SQL_SEEDS || {};
window.SQL_SEEDS.envios = `
CREATE TABLE PROVEEDORES (P CHAR(2) PRIMARY KEY, PNOMBRE VARCHAR(20), CATEGORIA INT, CIUDAD VARCHAR(20));
CREATE TABLE COMPONENTES (C CHAR(2) PRIMARY KEY, CNOMBRE VARCHAR(20), COLOR VARCHAR(10), PESO INT, CIUDAD VARCHAR(20));
CREATE TABLE ARTICULOS   (T CHAR(2) PRIMARY KEY, TNOMBRE VARCHAR(20), CIUDAD VARCHAR(20));
CREATE TABLE ENVIOS (
  P CHAR(2) REFERENCES PROVEEDORES (P),
  C CHAR(2) REFERENCES COMPONENTES (C),
  T CHAR(2) REFERENCES ARTICULOS (T),
  CANTIDAD INT,
  PRIMARY KEY (P, C, T)
);

INSERT INTO PROVEEDORES VALUES
  ('P1', 'CARLOS', 20, 'SEVILLA'), ('P2', 'JUAN', 10, 'MADRID'), ('P3', 'JOSE', 30, 'SEVILLA'),
  ('P4', 'INMA', 20, 'SEVILLA'),   ('P5', 'EVA', 30, 'CACERES');

INSERT INTO COMPONENTES VALUES
  ('C1', 'X3A', 'ROJO', 12, 'SEVILLA'),  ('C2', 'B85', 'VERDE', 17, 'MADRID'),
  ('C3', 'C4B', 'AZUL', 17, 'MALAGA'),   ('C4', 'C4B', 'ROJO', 14, 'SEVILLA'),
  ('C5', 'VT8', 'AZUL', 12, 'MADRID'),   ('C6', 'C30', 'ROJO', 19, 'SEVILLA');

INSERT INTO ARTICULOS VALUES
  ('T1', 'CLASIFICADORA', 'MADRID'), ('T2', 'PERFORADORA', 'MALAGA'), ('T3', 'LECTORA', 'CACERES'),
  ('T4', 'CONSOLA', 'CACERES'),      ('T5', 'MEZCLADORA', 'SEVILLA'), ('T6', 'TERMINAL', 'BARCELONA'),
  ('T7', 'CINTA', 'SEVILLA');

INSERT INTO ENVIOS VALUES
  ('P1','C1','T1',200), ('P1','C1','T4',700), ('P2','C3','T1',400), ('P2','C3','T2',200),
  ('P2','C3','T3',200), ('P2','C3','T4',500), ('P2','C3','T5',600), ('P2','C3','T6',400),
  ('P2','C3','T7',800), ('P2','C5','T2',100), ('P3','C3','T1',200), ('P3','C4','T2',500),
  ('P4','C6','T3',300), ('P4','C6','T7',300), ('P5','C2','T2',200), ('P5','C2','T4',100),
  ('P5','C5','T4',500), ('P5','C5','T7',100), ('P5','C6','T2',200), ('P5','C1','T4',100),
  ('P5','C3','T4',200), ('P5','C4','T4',800), ('P5','C5','T5',400), ('P5','C6','T4',500);
`;
