/* ============================================================================
   normalizador.js — interactive dependency drill for normalization exercises.

   One widget renders a flat (un-normalized) table and lets the student work out,
   attribute by attribute, WHY each column is in the wrong place. It has two
   modes:

     explorar — click a column header, get the dependency chain and the verdict
     examen   — every header becomes a <select>; the student classifies all of
                them, then grades. Nothing is revealed before grading.

   Markup contract — one JSON block, nothing else:

     <div class="nx" data-normalizador>
       <script type="application/json" class="nx__datos">{ ... }</script>
     </div>

   Data contract:

     clave        array of column ids forming the composite primary key
     columnas[]   { id, nombre, tipo, determinante[], porque, destino? }
                  tipo ∈ clave | total | parcial | transitiva | derivado
                  determinante: column ids this attribute really depends on
                  porque: one or two sentences, shown in the panel
                  destino: the table it ends up in, shown after grading
     filas[][]    row values, positionally aligned with columnas
     derivado?    { col, factores[], op } — renders the arithmetic proof
     resultado[]  { tabla, pk[], cols[] } — the final normalized schema

   Adding a new exercise means writing a new JSON block. Never fork this file.
   ========================================================================== */

(function () {
  "use strict";

  var TIPOS = {
    clave: {
      etiqueta: "Parte de la clave",
      titulo: "Es clave, no se clasifica",
      veredicto: "Forma parte de la clave primaria. Las formas normales hablan de los " +
                 "atributos NO clave, así que a este no se le aplica el test."
    },
    total: {
      etiqueta: "Depende de la clave entera",
      titulo: "Dependencia total — se queda",
      veredicto: "Necesita la clave completa para determinarse. Cumple 2FN y no pasa " +
                 "por ningún intermediario, así que también cumple 3FN. Se queda donde está."
    },
    parcial: {
      etiqueta: "Depende de media clave",
      titulo: "Dependencia parcial — viola 2FN",
      veredicto: "Se determina con SOLO UNA PARTE de la clave compuesta. Eso es una " +
                 "dependencia parcial: viola la 2FN. El atributo se muda a una tabla nueva " +
                 "cuya clave primaria es esa parte."
    },
    transitiva: {
      etiqueta: "Depende de un campo no clave",
      titulo: "Dependencia transitiva — viola 3FN",
      veredicto: "La clave llega a este atributo de rebote, pasando por otro atributo que " +
                 "no es clave. Eso es una dependencia transitiva: viola la 3FN. Se muda " +
                 "junto con su determinante, y ése pasa a ser la clave de la tabla nueva."
    },
    derivado: {
      etiqueta: "Se calcula con otros campos",
      titulo: "Atributo derivable — se elimina",
      veredicto: "No es un dato, es una cuenta. No se guarda en ninguna tabla: se calcula " +
                 "cuando hace falta. Guardarlo permite que el total contradiga a sus " +
                 "propios factores."
    }
  };

  var ORDEN = ["clave", "total", "parcial", "transitiva", "derivado"];

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  function build(root) {
    if (root.dataset.nxReady) return;
    root.dataset.nxReady = "1";

    var raw = root.querySelector(".nx__datos");
    if (!raw) return;

    var d;
    try {
      d = JSON.parse(raw.textContent);
    } catch (e) {
      root.appendChild(el("p", "nx__hint", "No se pudo leer los datos del ejercicio."));
      return;
    }

    var cols = d.columnas || [];
    var porId = {};
    cols.forEach(function (c, i) { c._i = i; porId[c.id] = c; });

    var modo = "explorar";
    var corregido = false;

    /* -- chrome ----------------------------------------------------------- */

    root.appendChild(el("span", "nx__label", d.etiqueta || "Ejercicio"));
    if (d.consigna) root.appendChild(el("p", "nx__hint", d.consigna));

    var bar = el("div", "nx__bar");
    var bExplorar = el("button", "nx__btn", "Explorar");
    var bExamen = el("button", "nx__btn", "Modo examen");
    var bCorregir = el("button", "nx__btn", "Corregir");
    var bReiniciar = el("button", "nx__btn", "Reiniciar");
    bExplorar.type = bExamen.type = bCorregir.type = bReiniciar.type = "button";
    bCorregir.hidden = true;
    bReiniciar.hidden = true;
    bar.appendChild(bExplorar);
    bar.appendChild(bExamen);
    bar.appendChild(bCorregir);
    bar.appendChild(bReiniciar);
    root.appendChild(bar);

    /* -- table ------------------------------------------------------------ */

    var scroll = el("div", "nx__scroll");
    var tabla = el("table", "nx__tabla");
    var thead = el("thead");
    var trh = el("tr");

    cols.forEach(function (c) {
      var th = el("th");
      th.dataset.col = c.id;

      var btn = el("button", "nx__col", c.nombre);
      btn.type = "button";
      btn.dataset.col = c.id;
      th.appendChild(btn);

      var sel = el("select", "nx__sel");
      sel.hidden = true;
      sel.dataset.col = c.id;
      sel.appendChild(new Option("¿qué es?", ""));
      ORDEN.forEach(function (t) { sel.appendChild(new Option(TIPOS[t].etiqueta, t)); });
      th.appendChild(sel);

      trh.appendChild(th);
    });

    thead.appendChild(trh);
    tabla.appendChild(thead);

    var tbody = el("tbody");
    (d.filas || []).forEach(function (fila) {
      var tr = el("tr");
      fila.forEach(function (v, i) {
        var td = el("td", null, String(v));
        if (cols[i]) td.dataset.col = cols[i].id;
        tr.appendChild(td);
      });
      tbody.appendChild(tr);
    });
    tabla.appendChild(tbody);
    scroll.appendChild(tabla);
    root.appendChild(scroll);

    /* -- legend ----------------------------------------------------------- */

    var leyenda = el("ul", "nx__leyenda");
    ORDEN.forEach(function (t) {
      var li = el("li");
      var sw = el("span", "nx__swatch is-" + t);
      li.appendChild(sw);
      li.appendChild(document.createTextNode(TIPOS[t].etiqueta));
      leyenda.appendChild(li);
    });
    root.appendChild(leyenda);

    /* -- panels ----------------------------------------------------------- */

    var panel = el("div", "nx__panel");
    panel.hidden = true;
    root.appendChild(panel);

    var marcador = el("p", "nx__marcador");
    marcador.hidden = true;
    root.appendChild(marcador);

    var prueba = el("div", "nx__prueba");
    prueba.hidden = true;
    root.appendChild(prueba);

    var resultado = el("div", "nx__resultado");
    resultado.hidden = true;
    root.appendChild(resultado);

    /* -- helpers ---------------------------------------------------------- */

    /* Only the cells. The header <button> and <select> carry the same data-col
       for event routing, and tinting or outlining those too doubles the border
       and leaks the answer into the select in exam mode. */
    function celdas(id) {
      return tabla.querySelectorAll('th[data-col="' + id + '"], td[data-col="' + id + '"]');
    }

    function limpiarFoco() {
      Array.prototype.forEach.call(tabla.querySelectorAll(".is-foco, .is-fuente"),
        function (n) { n.classList.remove("is-foco", "is-fuente"); });
    }

    function pintar(mostrarTipos) {
      cols.forEach(function (c) {
        Array.prototype.forEach.call(celdas(c.id), function (n) {
          ORDEN.forEach(function (t) { n.classList.remove("is-" + t); });
          if (mostrarTipos) n.classList.add("is-" + c.tipo);
        });
      });
    }

    function nombres(ids) {
      return (ids || []).map(function (i) {
        return porId[i] ? porId[i].nombre : i;
      });
    }

    function cadena(c) {
      var claveTxt = nombres(d.clave).join(" + ");
      var wrap = el("p", "nx__cadena");

      if (c.tipo === "clave") {
        wrap.innerHTML = "<b>" + claveTxt + "</b>  ← la clave primaria";
        return wrap;
      }
      if (c.tipo === "derivado" && d.derivado && d.derivado.col === c.id) {
        wrap.innerHTML = nombres(d.derivado.factores).join(" " + (d.derivado.op || "×") + " ") +
                         "  =  <b>" + c.nombre + "</b>";
        return wrap;
      }
      if (c.tipo === "transitiva") {
        wrap.innerHTML = "<b>" + claveTxt + "</b>  →  <i>" + nombres(c.determinante).join(", ") +
                         "</i>  →  " + c.nombre;
        return wrap;
      }
      wrap.innerHTML = "<b>" + nombres(c.determinante).join(" + ") + "</b>  →  " + c.nombre;
      return wrap;
    }

    function explicar(id) {
      var c = porId[id];
      if (!c) return;

      limpiarFoco();
      Array.prototype.forEach.call(celdas(id), function (n) { n.classList.add("is-foco"); });
      (c.determinante || []).forEach(function (dep) {
        if (dep === id) return;
        Array.prototype.forEach.call(celdas(dep), function (n) { n.classList.add("is-fuente"); });
      });

      panel.hidden = false;
      panel.className = "nx__panel tipo-" + c.tipo;
      panel.innerHTML = "";
      panel.appendChild(el("h4", null, c.nombre + " — " + TIPOS[c.tipo].titulo));
      panel.appendChild(cadena(c));
      if (c.porque) panel.appendChild(el("p", null, c.porque));
      panel.appendChild(el("p", null, TIPOS[c.tipo].veredicto));
      if (c.destino) {
        panel.appendChild(el("p", null, "Termina en: " + c.destino));
      }
    }

    function pintarPrueba() {
      if (!d.derivado) return;
      var info = d.derivado;
      var col = porId[info.col];
      if (!col) return;

      prueba.hidden = false;
      prueba.innerHTML = "";
      prueba.appendChild(el("h4", null, "La prueba: " + col.nombre + " no es un dato"));

      var t = el("table");
      (d.filas || []).forEach(function (fila) {
        var vals = info.factores.map(function (f) { return Number(fila[porId[f]._i]); });
        var prod = vals.reduce(function (a, b) { return a * b; }, 1);
        var real = Number(fila[col._i]);
        var tr = el("tr");
        tr.appendChild(el("td", null, vals.join(" " + (info.op || "×") + " ")));
        tr.appendChild(el("td", null, "="));
        tr.appendChild(el("td", null, String(prod)));
        tr.appendChild(el("td", prod === real ? "ok" : "", prod === real ? "✓ coincide" : "✗ no coincide"));
        t.appendChild(tr);
      });
      prueba.appendChild(t);
      prueba.appendChild(el("p", "nx__hint",
        "Sale de una multiplicación en TODAS las filas. Es un atributo derivable: " +
        "no se guarda. Éste es el error que el docente marca siempre."));
    }

    function pintarResultado() {
      if (!d.resultado || !d.resultado.length) return;
      resultado.hidden = false;
      resultado.innerHTML = "";
      resultado.appendChild(el("h4", null, "El modelo en 3FN"));
      d.resultado.forEach(function (r) {
        var p = el("p", "nx__rel");
        var pk = r.pk.map(function (x) { return "<b><u>" + x + "</u></b>"; }).join(", ");
        var rest = r.cols.length ? ", " + r.cols.join(", ") : "";
        p.innerHTML = r.tabla + " (" + pk + rest + ")";
        resultado.appendChild(p);
      });
      resultado.appendChild(el("p", "nx__hint",
        "Cada tabla con su clave primaria subrayada. No poner las claves es el " +
        "error nº 2 del docente."));
    }

    /* -- modes ------------------------------------------------------------ */

    function setModo(m) {
      modo = m;
      corregido = false;
      bExplorar.setAttribute("aria-pressed", String(m === "explorar"));
      bExamen.setAttribute("aria-pressed", String(m === "examen"));
      bCorregir.hidden = m !== "examen";
      bCorregir.disabled = false;
      bReiniciar.hidden = m !== "examen";
      panel.hidden = true;
      marcador.hidden = true;
      prueba.hidden = true;
      resultado.hidden = true;
      limpiarFoco();

      Array.prototype.forEach.call(root.querySelectorAll(".nx__sel"), function (s) {
        s.hidden = m !== "examen";
        s.value = "";
        s.className = "nx__sel";
        s.disabled = false;
      });
      Array.prototype.forEach.call(root.querySelectorAll(".nx__col"), function (b) {
        b.disabled = m === "examen";
      });

      pintar(m === "explorar");
    }

    function corregir() {
      var bien = 0, mal = [];
      cols.forEach(function (c) {
        var sel = root.querySelector('.nx__sel[data-col="' + c.id + '"]');
        if (!sel) return;
        var ok = sel.value === c.tipo;
        sel.className = "nx__sel " + (ok ? "ok" : "mal");
        sel.disabled = true;
        if (ok) bien++;
        else mal.push(c);
      });

      corregido = true;
      bCorregir.disabled = true;
      pintar(true);

      marcador.hidden = false;
      marcador.textContent = bien + " de " + cols.length + " bien.";

      if (mal.length) {
        var ul = el("ul", "nx__errores");
        mal.forEach(function (c) {
          var li = el("li");
          li.innerHTML = "<b>" + c.nombre + "</b> — es <i>" + TIPOS[c.tipo].etiqueta.toLowerCase() +
                         "</i>. " + (c.porque || "");
          ul.appendChild(li);
        });
        marcador.appendChild(ul);
      } else {
        marcador.appendChild(el("p", "nx__hint",
          "Las nueve. Ahora escribilo a mano, que el jueves no hay select."));
      }

      pintarPrueba();
      pintarResultado();
    }

    /* -- wiring ----------------------------------------------------------- */

    root.addEventListener("click", function (ev) {
      var b = ev.target.closest(".nx__col");
      if (b && !b.disabled) { explicar(b.dataset.col); return; }
      if (ev.target === bExplorar) setModo("explorar");
      if (ev.target === bExamen) setModo("examen");
      if (ev.target === bCorregir && !corregido) corregir();
      if (ev.target === bReiniciar) setModo("examen");
    });

    setModo("explorar");
  }

  function boot() {
    Array.prototype.forEach.call(document.querySelectorAll("[data-normalizador]"), build);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
