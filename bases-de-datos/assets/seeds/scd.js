/* SCD — Slow Change Dimension, tipo 2 (una fila = una foto con Fecha_Inicio y Fecha_Fin).
   CUSTOMER_GROUP reproduce la tabla del modelo de parcial "bd parcial 1a" (raw/Material_Examen),
   con sus mismos nombres de columna: el cliente 125269 tiene las 8 fotos del modelo, tal cual.
   Los otros tres clientes (3362, 22365 y 9946) los inventé para que el indicador y las consultas
   tengan más de un caso; los nombres salen de CUSTOMER_NAME del mismo modelo.
   Las fechas van como texto AAAA-MM-DD: en SQLite eso es lo que permite comparar y usar BETWEEN.
   La foto vigente termina en 2100-12-31 (la fecha de fin "muy futurista" del deck).
   SALDO_CLIENTE también es inventada: una medida (Saldo) que cambia por foto, para practicar
   sumas y promedios sobre toda la historia, sobre la foto actual o sobre una fecha. */
window.SQL_SEEDS = window.SQL_SEEDS || {};
window.SQL_SEEDS.scd = `
CREATE TABLE CUSTOMER_NAME (
  CG_Id   INTEGER      NOT NULL PRIMARY KEY,
  CG_Name VARCHAR(60)  NOT NULL
);
CREATE TABLE CUSTOMER_GROUP (
  Customer_Group_Id        INTEGER     NOT NULL,
  Start_Dt                 DATE        NOT NULL,
  SIC_Cd                   INTEGER     NOT NULL,
  CG_Begin_Dt              DATE        NOT NULL,
  Officer_Id               INTEGER     NOT NULL,
  Banking_Group_Id         INTEGER     NOT NULL,
  Telephone_Ind            CHAR(2)     NOT NULL,
  CG_Type_Cd               INTEGER     NOT NULL,
  Customer_Group_Assoc_Id  INTEGER     NOT NULL,
  End_Dt                   DATE        NOT NULL,
  PRIMARY KEY (Customer_Group_Id, Start_Dt),
  FOREIGN KEY (Customer_Group_Id) REFERENCES CUSTOMER_NAME (CG_Id)
);

CREATE TABLE SALDO_CLIENTE (
  Id_Cliente   INTEGER NOT NULL,
  Fecha_Inicio DATE    NOT NULL,
  Fecha_Fin    DATE    NOT NULL,
  Saldo        INTEGER NOT NULL,
  PRIMARY KEY (Id_Cliente, Fecha_Inicio),
  FOREIGN KEY (Id_Cliente) REFERENCES CUSTOMER_NAME (CG_Id)
);

INSERT INTO CUSTOMER_NAME (CG_Id, CG_Name) VALUES
  (125269, 'Gomez, Juan Carlos'), (3362, 'Alves,Camila'), (22365, 'Lorena, Urso'), (9946, 'Lucas, Sanchez');

INSERT INTO CUSTOMER_GROUP VALUES
  (125269, '2005-05-01', 173001, '2005-05-26', 110, 3, 'No', -1, 81, '2007-11-01'),
  (125269, '2007-11-02', 173001, '2005-05-26', 110, 3, 'No', -1, 81, '2014-11-02'),
  (125269, '2014-11-03', 173001, '2005-05-26', 110, 3, 'Si', 24, 81, '2015-05-03'),
  (125269, '2015-05-04', 182001, '2005-05-26', 110, 3, 'Si', 24, 81, '2016-12-01'),
  (125269, '2016-12-02', 182001, '2005-05-26',  11, 3, 'Si', 24, 81, '2021-12-01'),
  (125269, '2021-12-02', 182001, '2005-05-26', -15, 3, 'Si', 24, 81, '2022-02-01'),
  (125269, '2022-02-02', 182001, '2005-05-26',  11, 3, 'Si', 24, 81, '2023-02-01'),
  (125269, '2023-02-02', 182001, '2005-05-26', 978, 3, 'Si', 24, 81, '2100-12-31'),
  (3362,   '2010-03-15', 173001, '2010-03-15',  15, 7, 'Si', 24, 81, '2019-06-30'),
  (3362,   '2019-07-01', 173001, '2010-03-15',  30, 7, 'Si', 24, 81, '2100-12-31'),
  (22365,  '2018-01-10', 182001, '2018-01-10',  12, 2, 'No', 24, 65, '2100-12-31'),
  (9946,   '2012-09-01', 194001, '2012-09-01',  18, 6, 'Si', -1, 81, '2020-12-31'),
  (9946,   '2021-01-01', 194001, '2012-09-01',  18, 6, 'Si', 24, 81, '2100-12-31');

INSERT INTO SALDO_CLIENTE VALUES
  (125269, '2021-01-01', '2021-06-30', 1000),
  (125269, '2021-07-01', '2021-12-31', 1500),
  (125269, '2022-01-01', '2022-12-31',  800),
  (125269, '2023-01-01', '2100-12-31', 2000),
  (3362,   '2022-01-01', '2022-06-30',  500),
  (3362,   '2022-07-01', '2100-12-31',  700),
  (22365,  '2023-01-01', '2100-12-31',  300);
`;
