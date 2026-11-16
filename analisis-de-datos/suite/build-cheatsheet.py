# Builds suite/cheatsheet.html: runs every query in SQLite so each card shows its real result.
# Run: python3 suite/build-cheatsheet.py
import sqlite3, html
from pathlib import Path
c = sqlite3.connect(":memory:")
c.executescript("""
create table clientes(id int, nombre text, pais text, email text);
insert into clientes values(1,'Ana','AR','ana@x.com'),(2,'Beto','BR',NULL),(3,'Caro','AR','caro@x.com'),(4,'Dani','CL','dani@x.com');
create table facturas(id int, cliente_id int, total int);
insert into facturas values(10,1,100),(11,1,50),(12,2,80),(13,3,20);
""")
E = html.escape
SECTIONS = [
 ("Filtrar filas", "filtrar", [
  ("WHERE simple", "SELECT nombre\nFROM clientes\nWHERE pais = 'AR';", "Filtra <strong>filas</strong>. Texto entre comillas simples."),
  ("IN: varios valores", "SELECT nombre, pais\nFROM clientes\nWHERE pais IN ('AR', 'CL');", "Es lo mismo que <code>pais = 'AR' OR pais = 'CL'</code>."),
  ("BETWEEN incluye los extremos", "SELECT id, total\nFROM facturas\nWHERE total BETWEEN 50 AND 100;", "El 50 y el 100 <strong>entran</strong>: 3 filas."),
  ("LIKE: patrón de texto", "SELECT nombre\nFROM clientes\nWHERE nombre LIKE 'A%';", "<code>%</code> = cualquier cantidad de caracteres. <code>'A%'</code> = empieza con A."),
  ("IS NULL", "SELECT nombre\nFROM clientes\nWHERE email IS NULL;", "La forma correcta de buscar faltantes."),
  ("= NULL: la trampa", "SELECT nombre\nFROM clientes\nWHERE email = NULL;", "<strong>0 filas, sin error.</strong> <code>NULL = NULL</code> da UNKNOWN y WHERE solo deja pasar TRUE."),
 ]),
 ("Ordenar y recortar", "ordenar", [
  ("ORDER BY + LIMIT", "SELECT nombre\nFROM clientes\nORDER BY nombre DESC\nLIMIT 2;", "DESC = de mayor a menor (Z→A). LIMIT recorta <strong>después</strong> de ordenar."),
  ("Alias con AS", "SELECT id AS factura, total * 2 AS doble\nFROM facturas\nORDER BY doble DESC;", "ORDER BY puede usar el alias porque corre <strong>después</strong> del SELECT. WHERE no."),
 ]),
 ("Contar y agregar", "agregar", [
  ("COUNT(*) vs COUNT(col)", "SELECT COUNT(*), COUNT(email)\nFROM clientes;", "<code>COUNT(*)</code> cuenta filas; <code>COUNT(email)</code> ignora el NULL de Beto."),
  ("COUNT(DISTINCT)", "SELECT COUNT(DISTINCT pais)\nFROM clientes;", "AR, BR, CL: 3 valores <strong>distintos</strong>."),
  ("Agregados sobre toda la tabla", "SELECT SUM(total), AVG(total),\n       MIN(total), MAX(total)\nFROM facturas;", "Sin GROUP BY: <strong>una sola fila</strong> para toda la tabla."),
  ("GROUP BY: uno por grupo", "SELECT cliente_id, SUM(total) AS total\nFROM facturas\nGROUP BY cliente_id;", "En el SELECT: solo columnas del GROUP BY y agregados."),
  ("HAVING: filtrar grupos", "SELECT cliente_id, SUM(total) AS total\nFROM facturas\nGROUP BY cliente_id\nHAVING SUM(total) > 60;", "Filtro sobre un agregado → <strong>HAVING</strong>. En WHERE da error."),
  ("WHERE + GROUP BY + HAVING", "SELECT pais, COUNT(*) AS cant\nFROM clientes\nWHERE email IS NOT NULL\nGROUP BY pais\nHAVING COUNT(*) > 1;", "WHERE saca a Beto (filas) → agrupa → HAVING deja los grupos con más de 1."),
 ]),
 ("JOINs", "join", [
  ("INNER JOIN", "SELECT c.nombre, f.id, f.total\nFROM clientes c\nINNER JOIN facturas f ON f.cliente_id = c.id;", "Solo las filas con pareja. <strong>Dani no aparece.</strong>"),
  ("LEFT JOIN", "SELECT c.nombre, f.id, f.total\nFROM clientes c\nLEFT JOIN facturas f ON f.cliente_id = c.id;", "<strong>Todo el FROM</strong> (izquierda) + NULL donde no hay pareja."),
  ("LEFT JOIN + IS NULL = \"sin\"", "SELECT c.nombre\nFROM clientes c\nLEFT JOIN facturas f ON f.cliente_id = c.id\nWHERE f.id IS NULL;", "Los clientes <strong>sin</strong> facturas."),
  ("Dar vuelta el FROM", "SELECT f.id, c.nombre\nFROM facturas f\nLEFT JOIN clientes c ON c.id = f.cliente_id;", "Ahora la izquierda es <strong>facturas</strong>: 4 filas y Dani desaparece. El orden del ON no importa."),
  ("JOIN + GROUP BY", "SELECT c.nombre, SUM(f.total) AS total\nFROM clientes c\nINNER JOIN facturas f ON f.cliente_id = c.id\nGROUP BY c.nombre;", "Total por cliente <strong>con nombre</strong>."),
  ("LEFT JOIN + COUNT(col) = incluye 0", "SELECT c.nombre, COUNT(f.id) AS cant\nFROM clientes c\nLEFT JOIN facturas f ON f.cliente_id = c.id\nGROUP BY c.nombre;", "Con <code>COUNT(*)</code> Dani daría <strong>1</strong> (cuenta la fila con NULL). <code>COUNT(f.id)</code> da 0."),
 ]),
 ("Subconsultas y CTE", "sub", [
  ("Subconsulta en WHERE", "SELECT id, total\nFROM facturas\nWHERE total > (SELECT AVG(total) FROM facturas);", "El promedio es 62,5: pasan 100 y 80."),
  ("Subconsulta con IN", "SELECT nombre\nFROM clientes\nWHERE id IN (SELECT cliente_id FROM facturas);", "Clientes que <strong>tienen</strong> al menos una factura."),
  ("CTE: WITH", "WITH totales AS (\n  SELECT cliente_id, SUM(total) AS t\n  FROM facturas\n  GROUP BY cliente_id\n)\nSELECT cliente_id, t\nFROM totales\nWHERE t > 60;", "Parte la consulta en pasos con nombre. Acá WHERE sí sirve: <code>t</code> ya es una columna."),
 ]),
 ("Funciones ventana", "ventana", [
  ("SUM OVER (PARTITION BY)", "SELECT id, cliente_id, total,\n  SUM(total) OVER (PARTITION BY cliente_id) AS del_cliente\nFROM facturas;", "<strong>No colapsa</strong>: las 4 filas siguen, con el total del cliente al lado."),
  ("Acumulado: OVER (ORDER BY)", "SELECT id, total,\n  SUM(total) OVER (ORDER BY id) AS acumulado\nFROM facturas;", "ORDER BY dentro del OVER = suma <strong>hasta la fila actual</strong>."),
  ("ROW_NUMBER vs RANK", "WITH cant AS (\n  SELECT c.nombre, COUNT(f.id) AS n\n  FROM clientes c\n  LEFT JOIN facturas f ON f.cliente_id = c.id\n  GROUP BY c.nombre\n)\nSELECT nombre, n,\n  ROW_NUMBER() OVER (ORDER BY n DESC, nombre) AS rn,\n  RANK() OVER (ORDER BY n DESC) AS rk\nFROM cant;", "Beto y Caro empatan: RANK les da 2 a los dos y <strong>salta</strong> al 4."),
  ("LAG y LEAD", "SELECT id, total,\n  LAG(total)  OVER (ORDER BY id) AS anterior,\n  LEAD(total) OVER (ORDER BY id) AS siguiente\nFROM facturas;", "En los bordes: <strong>NULL</strong>, nunca 0."),
 ]),
]

def result_table(sql):
    cur = c.execute(sql)
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()
    head = "".join(f"<th>{E(str(x))}</th>" for x in cols)
    def cell(v):
        if v is None: return '<td class="null">NULL</td>'
        if isinstance(v, float): v = f"{v:g}".replace(".", ",")
        return f"<td>{E(str(v))}</td>"
    body = "".join("<tr>" + "".join(cell(v) for v in r) + "</tr>" for r in rows) or f'<tr><td class="empty" colspan="{len(cols)}">0 filas</td></tr>'
    n = len(rows)
    return f'<div class="res"><div class="res-h">Resultado · {n} fila{"s" if n != 1 else ""}</div><div class="tw"><table>{"<tr>"+head+"</tr>"}{body}</table></div></div>'

cards = []
n = 0
for title, kind, items in SECTIONS:
    cards.append(f'<h2 class="sec" id="{kind}">{E(title)}</h2><div class="grid">')
    for name, sql, note in items:
        n += 1
        cards.append(f'<article class="card k-{kind}"><div class="card-h"><span class="num">{n:02d}</span><h3>{E(name)}</h3></div>'
                     f'<pre class="sql">{E(sql)}</pre>{result_table(sql)}<p class="note">{note}</p></article>')
    cards.append("</div>")

tpl = Path(__file__).with_name("cheatsheet.tpl.html").read_text()
out = tpl.replace("{{CARDS}}", "\n".join(cards)).replace("{{N}}", str(n))
Path(__file__).with_name("cheatsheet.html").write_text(out)
print("cards:", n)
