/* Conjuntos — dos tablas A y B con un solo campo, Id_Art, como en los diagramas del repaso
   del 2do parcial (2026-11-05). Los valores están elegidos para que cada región del Venn
   tenga datos distintos y se puedan reconocer a simple vista:
     sólo A        → 1, 2, 3
     A y B         → 4, 5, 6
     sólo B        → 7, 8
   Id_Art es PRIMARY KEY en las dos: cada tabla es un conjunto (sin repetidos), así que un
   JOIN no duplica filas. */
window.SQL_SEEDS = window.SQL_SEEDS || {};
window.SQL_SEEDS.conjuntos = `
CREATE TABLE A (
  Id_Art INTEGER NOT NULL PRIMARY KEY
);
CREATE TABLE B (
  Id_Art INTEGER NOT NULL PRIMARY KEY
);
INSERT INTO A (Id_Art) VALUES (1), (2), (3), (4), (5), (6);
INSERT INTO B (Id_Art) VALUES (4), (5), (6), (7), (8);
`;
