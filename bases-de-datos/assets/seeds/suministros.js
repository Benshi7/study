/* SUMINISTROS — la base que subió el profe (raw/SUMINISTROS/SUMINISTROS.sql), con sus
   mismos nombres de columna (P_Id, C_Id, T_Id), así lo que escribas acá corre igual en
   DBeaver. Son los mismos datos que los modelos de parcial bd parcial 1a/1b (seed "envios"). */
window.SQL_SEEDS = window.SQL_SEEDS || {};
window.SQL_SEEDS.suministros = `
CREATE TABLE PROVEEDORES (
  P_Id      CHAR(2)     NOT NULL PRIMARY KEY,
  PNombre   VARCHAR(50) NOT NULL,
  Categoria SMALLINT    NOT NULL,
  Ciudad    VARCHAR(30) NOT NULL
);
CREATE TABLE COMPONENTES (
  C_Id    CHAR(2)     NOT NULL PRIMARY KEY,
  CNombre VARCHAR(50) NOT NULL,
  Color   VARCHAR(20) NOT NULL,
  Peso    SMALLINT    NOT NULL,
  Ciudad  VARCHAR(30) NOT NULL
);
CREATE TABLE ARTICULOS (
  T_Id    CHAR(2)     NOT NULL PRIMARY KEY,
  TNombre VARCHAR(50) NOT NULL,
  Ciudad  VARCHAR(30) NOT NULL
);
CREATE TABLE ENVIOS (
  P_Id     CHAR(2) NOT NULL,
  C_Id     CHAR(2) NOT NULL,
  T_Id     CHAR(2) NOT NULL,
  Cantidad INTEGER NOT NULL,
  PRIMARY KEY (P_Id, C_Id, T_Id),
  FOREIGN KEY (P_Id) REFERENCES PROVEEDORES (P_Id),
  FOREIGN KEY (C_Id) REFERENCES COMPONENTES (C_Id),
  FOREIGN KEY (T_Id) REFERENCES ARTICULOS (T_Id)
);

INSERT INTO PROVEEDORES (P_Id, PNombre, Categoria, Ciudad) VALUES
  ('P1', 'CARLOS', 20, 'SEVILLA'), ('P2', 'JUAN', 10, 'MADRID'), ('P3', 'JOSE', 30, 'SEVILLA'),
  ('P4', 'INMA', 20, 'SEVILLA'),   ('P5', 'EVA', 30, 'CACERES');

INSERT INTO COMPONENTES (C_Id, CNombre, Color, Peso, Ciudad) VALUES
  ('C1', 'X3A', 'ROJO', 12, 'SEVILLA'),  ('C2', 'B85', 'VERDE', 17, 'MADRID'),
  ('C3', 'C4B', 'AZUL', 17, 'MALAGA'),   ('C4', 'C4B', 'ROJO', 14, 'SEVILLA'),
  ('C5', 'VT8', 'AZUL', 12, 'MADRID'),   ('C6', 'C30', 'ROJO', 19, 'SEVILLA');

INSERT INTO ARTICULOS (T_Id, TNombre, Ciudad) VALUES
  ('T1', 'CLASIFICADORA', 'MADRID'), ('T2', 'PERFORADORA', 'MALAGA'), ('T3', 'LECTORA', 'CACERES'),
  ('T4', 'CONSOLA', 'CACERES'),      ('T5', 'MEZCLADORA', 'SEVILLA'), ('T6', 'TERMINAL', 'BARCELONA'),
  ('T7', 'CINTA', 'SEVILLA');

INSERT INTO ENVIOS (P_Id, C_Id, T_Id, Cantidad) VALUES
  ('P1','C1','T1',200), ('P1','C1','T4',700), ('P2','C3','T1',400), ('P2','C3','T2',200),
  ('P2','C3','T3',200), ('P2','C3','T4',500), ('P2','C3','T5',600), ('P2','C3','T6',400),
  ('P2','C3','T7',800), ('P2','C5','T2',100), ('P3','C3','T1',200), ('P3','C4','T2',500),
  ('P4','C6','T3',300), ('P4','C6','T7',300), ('P5','C2','T2',200), ('P5','C2','T4',100),
  ('P5','C5','T4',500), ('P5','C5','T7',100), ('P5','C6','T2',200), ('P5','C1','T4',100),
  ('P5','C3','T4',200), ('P5','C4','T4',800), ('P5','C5','T5',400), ('P5','C6','T4',500);
`;
