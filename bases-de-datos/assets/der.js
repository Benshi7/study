/* ============================================================================
   der.js — interactive drills for the conceptual model (DER) and its passage
   to the relational model (MER).

   Four widgets, all opt-in through a data attribute:

     [data-glosario]        renders the cátedra's Chen primitives as SVG cards
     [data-notacion]        "which symbol?" drill over those primitives
     [data-especializacion] total/parcial x exclusiva/solapada explorer, with
                            the legal-state enumeration and the record count
     [data-mapeo]           DER element -> relational mapping drill, graded

   Notation follows raw/Material_Examen/unidad 2.pdf, which is the cátedra's
   own deck, NOT Elmasri's. Two differences matter and are wired in here:
     - total participation is drawn with a CIRCLE on the supertype line
       (parcial = no circle), not with a double line;
     - exclusividad (disjunta) is drawn with an ARC crossing the subtype legs
       (solapada = no arc), not with a "d"/"o" letter inside a circle.

   Shapes stroke with currentColor, so light and dark themes need no second
   asset. Every figure carries role="img" and a <title> for screen readers.
   ========================================================================== */

(function () {
  "use strict";

  /* ------------------------------------------------------------------ utils */

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  function svg(titulo, inner, vb) {
    return '<svg class="dx__forma" viewBox="' + (vb || "0 0 180 92") + '" ' +
           'role="img" aria-label="' + esc(titulo) + '">' +
           "<title>" + esc(titulo) + "</title>" + inner + "</svg>";
  }

  /* ----------------------------------------------------------------- shapes */

  var FORMAS = {
    entidad: {
      nombre: "Entidad fuerte",
      que: "Rectángulo simple. Existe por sí misma.",
      dibujo: function (t) {
        return svg("Entidad fuerte: rectángulo",
          '<rect class="fill" x="24" y="28" width="132" height="36"/>' +
          '<rect class="line" x="24" y="28" width="132" height="36"/>' +
          '<text class="txt" x="90" y="47">' + esc(t || "Empleado") + "</text>");
      }
    },
    entidadDebil: {
      nombre: "Entidad débil",
      que: "Rectángulo doble. No puede formar su clave sola: hereda la del fuerte.",
      dibujo: function (t) {
        return svg("Entidad débil: rectángulo de doble línea",
          '<rect class="fill" x="20" y="24" width="140" height="44"/>' +
          '<rect class="line" x="20" y="24" width="140" height="44"/>' +
          '<rect class="line" x="25" y="29" width="130" height="34"/>' +
          '<text class="txt" x="90" y="47">' + esc(t || "Hijo") + "</text>");
      }
    },
    relacion: {
      nombre: "Relación",
      que: "Rombo. Vincula entidades. El grado es cuántas vincula.",
      dibujo: function (t) {
        return svg("Relación: rombo",
          '<polygon class="fill" points="90,20 168,46 90,72 12,46"/>' +
          '<polygon class="line" points="90,20 168,46 90,72 12,46"/>' +
          '<text class="txt txt--sm" x="90" y="47">' + esc(t || "Trabaja en") + "</text>");
      }
    },
    relacionDebil: {
      nombre: "Relación débil",
      que: "Rombo doble. Une una entidad fuerte con una débil.",
      dibujo: function (t) {
        return svg("Relación débil: rombo de doble línea",
          '<polygon class="fill" points="90,16 172,46 90,76 8,46"/>' +
          '<polygon class="line" points="90,16 172,46 90,76 8,46"/>' +
          '<polygon class="line" points="90,24 160,46 90,68 20,46"/>' +
          '<text class="txt txt--sm" x="90" y="47">' + esc(t || "Tiene por") + "</text>");
      }
    },
    atributo: {
      nombre: "Atributo",
      que: "Elipse simple. Un valor por ocurrencia.",
      dibujo: function (t) {
        return svg("Atributo: elipse",
          '<ellipse class="fill" cx="90" cy="46" rx="74" ry="26"/>' +
          '<ellipse class="line" cx="90" cy="46" rx="74" ry="26"/>' +
          '<text class="txt" x="90" y="47">' + esc(t || "Nombre") + "</text>");
      }
    },
    atributoClave: {
      nombre: "Atributo clave",
      que: "Elipse con el nombre SUBRAYADO. Identifica la ocurrencia.",
      dibujo: function (t) {
        return svg("Atributo clave: elipse con el texto subrayado",
          '<ellipse class="fill" cx="90" cy="46" rx="74" ry="26"/>' +
          '<ellipse class="line" cx="90" cy="46" rx="74" ry="26"/>' +
          '<text class="txt sub" x="90" y="47">' + esc(t || "Id_Empleado") + "</text>");
      }
    },
    atributoMulti: {
      nombre: "Atributo multivaluado",
      que: "Elipse DOBLE. Varios valores para la misma ocurrencia. La cátedra también lo llama grupo repetitivo.",
      dibujo: function (t) {
        return svg("Atributo multivaluado: elipse de doble línea",
          '<ellipse class="fill" cx="90" cy="46" rx="78" ry="30"/>' +
          '<ellipse class="line" cx="90" cy="46" rx="78" ry="30"/>' +
          '<ellipse class="line" cx="90" cy="46" rx="70" ry="23"/>' +
          '<text class="txt" x="90" y="47">' + esc(t || "Teléfono") + "</text>");
      }
    },
    atributoDerivado: {
      nombre: "Atributo derivable",
      que: "Elipse PUNTEADA. Se calcula desde otro atributo. Se dibuja, pero no se guarda.",
      dibujo: function (t) {
        return svg("Atributo derivable: elipse punteada",
          '<ellipse class="fill" cx="90" cy="46" rx="74" ry="26"/>' +
          '<ellipse class="dash" cx="90" cy="46" rx="74" ry="26"/>' +
          '<text class="txt" x="90" y="47">' + esc(t || "Edad") + "</text>");
      }
    },
    atributoCompuesto: {
      nombre: "Atributo compuesto",
      que: "Elipse con elipses colgando. Se parte en sus componentes.",
      dibujo: function (t) {
        return svg("Atributo compuesto: elipse con dos elipses hijas",
          '<ellipse class="fill" cx="90" cy="22" rx="52" ry="18"/>' +
          '<ellipse class="line" cx="90" cy="22" rx="52" ry="18"/>' +
          '<text class="txt txt--sm" x="90" y="23">' + esc(t || "Dirección") + "</text>" +
          '<path class="line" d="M64 36 L40 56 M116 36 L140 56"/>' +
          '<ellipse class="fill" cx="40" cy="70" rx="36" ry="15"/>' +
          '<ellipse class="line" cx="40" cy="70" rx="36" ry="15"/>' +
          '<text class="txt txt--sm" x="40" y="71">Calle</text>' +
          '<ellipse class="fill" cx="140" cy="70" rx="36" ry="15"/>' +
          '<ellipse class="line" cx="140" cy="70" rx="36" ry="15"/>' +
          '<text class="txt txt--sm" x="140" y="71">Número</text>');
      }
    },
    isa: {
      nombre: "Especialización (ES / ISA)",
      que: "Triángulo con ES. El supertipo arriba, los subtipos abajo.",
      dibujo: function () {
        return svg("Especialización: triángulo con la palabra ES",
          '<rect class="fill" x="56" y="6" width="68" height="24"/>' +
          '<rect class="line" x="56" y="6" width="68" height="24"/>' +
          '<text class="txt txt--sm" x="90" y="19">Persona</text>' +
          '<path class="line" d="M90 30 L90 40"/>' +
          '<polygon class="fill" points="70,40 110,40 90,62"/>' +
          '<polygon class="line" points="70,40 110,40 90,62"/>' +
          '<text class="txt txt--sm" x="90" y="48">ES</text>' +
          '<path class="line" d="M90 62 L40 74 M90 62 L140 74"/>' +
          '<rect class="fill" x="6" y="74" width="68" height="16"/>' +
          '<rect class="line" x="6" y="74" width="68" height="16"/>' +
          '<text class="txt txt--sm" x="40" y="83">Docente</text>' +
          '<rect class="fill" x="106" y="74" width="68" height="16"/>' +
          '<rect class="line" x="106" y="74" width="68" height="16"/>' +
          '<text class="txt txt--sm" x="140" y="83">Alumno</text>');
      }
    }
  };

  /* -------------------------------------------------------------- glosario */

  function glosario(root) {
    var ul = el("ul", "dx__glosario");
    Object.keys(FORMAS).forEach(function (k) {
      var f = FORMAS[k];
      var li = el("li");
      li.innerHTML = f.dibujo() +
        "<h4>" + esc(f.nombre) + "</h4><p>" + esc(f.que) + "</p>";
      ul.appendChild(li);
    });
    root.appendChild(ul);
  }

  /* ------------------------------------------------------- notación drill */

  function notacion(root, d) {
    var i = 0, bloqueada = false;

    var q = el("p", "dx__q");
    var paso = el("p", "dx__paso");
    var ul = el("ul", "dx__opciones");
    var fb = el("div", "dx__fb");
    fb.hidden = true;
    var bar = el("div", "dx__bar");
    var bSig = el("button", "dx__btn", "Siguiente");
    bSig.type = "button";
    bSig.disabled = true;
    bar.appendChild(bSig);

    root.appendChild(paso);
    root.appendChild(q);
    root.appendChild(ul);
    root.appendChild(fb);
    root.appendChild(bar);

    function pinta() {
      var it = d.items[i];
      bloqueada = false;
      bSig.disabled = true;
      fb.hidden = true;
      paso.textContent = (i + 1) + " de " + d.items.length;
      q.textContent = it.pregunta;
      ul.innerHTML = "";

      var ops = it.opciones.slice();
      for (var j = ops.length - 1; j > 0; j--) {
        var r = Math.floor(Math.random() * (j + 1));
        var t = ops[j]; ops[j] = ops[r]; ops[r] = t;
      }

      ops.forEach(function (clave) {
        var f = FORMAS[clave];
        if (!f) return;
        var li = el("li");
        var b = el("button", "dx__opt");
        b.type = "button";
        b.dataset.forma = clave;
        b.innerHTML = f.dibujo(it.etiquetas && it.etiquetas[clave]) +
                      "<span>" + esc(f.nombre) + "</span>";
        li.appendChild(b);
        ul.appendChild(li);
      });
    }

    ul.addEventListener("click", function (ev) {
      var b = ev.target.closest(".dx__opt");
      if (!b || bloqueada) return;
      bloqueada = true;

      var it = d.items[i];
      var ok = b.dataset.forma === it.correcta;

      Array.prototype.forEach.call(ul.querySelectorAll(".dx__opt"), function (o) {
        o.disabled = true;
        if (o === b) o.classList.add(ok ? "ok" : "mal");
        else if (o.dataset.forma === it.correcta && !ok) o.classList.add("perdida");
      });

      fb.hidden = false;
      fb.className = "dx__fb " + (ok ? "ok" : "mal");
      fb.innerHTML = "<b>" + (ok ? "Correcto." : "No.") + "</b> " + it.porque;
      bSig.disabled = i >= d.items.length - 1;
      if (bSig.disabled) bSig.textContent = "Terminaste";
    });

    bSig.addEventListener("click", function () {
      if (i < d.items.length - 1) { i++; pinta(); }
    });

    pinta();
  }

  /* --------------------------------------------- especialización explorer */

  function isaSVG(o) {
    var k = o.k, W = 360, m = 12, gap = 8;
    var w = (W - 2 * m - (k - 1) * gap) / k;
    var apexY = 96, subY = 150, subH = 26;

    var s = "";
    /* supertype */
    s += '<rect class="fill" x="130" y="8" width="100" height="28"/>';
    s += '<rect class="line" x="130" y="8" width="100" height="28"/>';
    s += '<text class="txt txt--sm" x="180" y="23">' + esc(o.super) + "</text>";
    /* stem */
    s += '<path class="line" d="M180 36 L180 66"/>';
    /* TOTAL marker: a circle on the stem (cátedra, unidad 2 p.11) */
    if (o.total) {
      s += '<circle class="fill" cx="180" cy="51" r="7"/>';
      s += '<circle class="line" cx="180" cy="51" r="7"/>';
    }
    /* triangle */
    s += '<polygon class="fill" points="152,66 208,66 180,' + apexY + '"/>';
    s += '<polygon class="line" points="152,66 208,66 180,' + apexY + '"/>';
    s += '<text class="txt txt--sm" x="180" y="77">ES</text>';

    /* legs + subtypes */
    var centros = [];
    for (var j = 0; j < k; j++) {
      var cx = m + w / 2 + j * (w + gap);
      centros.push(cx);
      s += '<path class="line" d="M180 ' + apexY + " L" + cx.toFixed(1) + " " + subY + '"/>';
      s += '<rect class="fill" x="' + (cx - w / 2).toFixed(1) + '" y="' + subY +
           '" width="' + w.toFixed(1) + '" height="' + subH + '"/>';
      s += '<rect class="line" x="' + (cx - w / 2).toFixed(1) + '" y="' + subY +
           '" width="' + w.toFixed(1) + '" height="' + subH + '"/>';
      s += '<text class="txt txt--sm" x="' + cx.toFixed(1) + '" y="' + (subY + subH / 2 + 1) +
           '">' + esc(o.subs[j]) + "</text>";
    }

    /* EXCLUSIVA marker: an arc crossing the legs (cátedra, unidad 2 p.11) */
    if (o.exclusiva) {
      var yArc = 126;
      var t = (yArc - apexY) / (subY - apexY);
      var xL = 180 + (centros[0] - 180) * t;
      var xR = 180 + (centros[k - 1] - 180) * t;
      s += '<path class="line" d="M' + xL.toFixed(1) + " " + yArc +
           " Q180 " + (yArc + 22) + " " + xR.toFixed(1) + " " + yArc + '"/>';
    }

    var etiqueta = (o.total ? "Total" : "Parcial") + ", " +
                   (o.exclusiva ? "Exclusiva" : "Solapada");
    return svg("Especialización " + etiqueta + " de " + o.super, s, "0 0 360 190");
  }

  function subconjuntos(n) {
    var out = [];
    for (var m = 0; m < (1 << n); m++) {
      var s = [];
      for (var j = 0; j < n; j++) if (m & (1 << j)) s.push(j);
      out.push(s);
    }
    return out.sort(function (a, b) { return a.length - b.length; });
  }

  function especializacion(root, d) {
    /* Start at the simplest case — two subtypes, which is the TP1 Farmacia
       shape — so the first enumeration is 4 rows, not 16. The slider grows it. */
    var estado = { total: true, exclusiva: true, k: 2 };

    var ejes = el("div", "dx__ejes");
    function eje(rotulo, a, b, campo) {
      var wrap = el("div", "dx__eje");
      wrap.appendChild(el("b", null, rotulo));
      [[a, true], [b, false]].forEach(function (par) {
        var btn = el("button", "dx__btn", par[0]);
        btn.type = "button";
        btn.dataset.campo = campo;
        btn.dataset.val = String(par[1]);
        wrap.appendChild(btn);
      });
      return wrap;
    }
    ejes.appendChild(eje("Participación", "Total", "Parcial", "total"));
    ejes.appendChild(eje("Solapamiento", "Exclusiva", "Solapada", "exclusiva"));
    root.appendChild(ejes);

    var panel = el("div", "dx__panelesp");
    var lienzo = el("div", "dx__lienzo");
    var info = el("div");
    panel.appendChild(lienzo);
    panel.appendChild(info);
    root.appendChild(panel);

    var kwrap = el("label", "dx__k");
    kwrap.appendChild(el("span", null, "Subtipos:"));
    var slider = document.createElement("input");
    slider.type = "range";
    slider.min = "2";
    slider.max = String(d.subs.length);
    slider.value = String(estado.k);
    var kval = el("b", null, String(estado.k));
    kwrap.appendChild(slider);
    kwrap.appendChild(kval);
    root.appendChild(kwrap);

    function pinta() {
      var subs = d.subs.slice(0, estado.k);

      Array.prototype.forEach.call(ejes.querySelectorAll(".dx__btn"), function (b) {
        b.setAttribute("aria-pressed",
          String(String(estado[b.dataset.campo]) === b.dataset.val));
      });

      lienzo.innerHTML = isaSVG({
        super: d.super, subs: subs, k: estado.k,
        total: estado.total, exclusiva: estado.exclusiva
      });

      var clave = (estado.total ? "t" : "p") + (estado.exclusiva ? "e" : "s");
      var caso = d.casos[clave];

      info.innerHTML = "";
      info.appendChild(el("p", "dx__veredicto",
        (estado.total ? "Total" : "Parcial") + " · " +
        (estado.exclusiva ? "Exclusiva (disjunta)" : "Solapada")));

      var cat = el("p", "dx__catedra");
      cat.innerHTML = "<b>Ejemplo de la cátedra:</b> " + caso.ejemplo;
      info.appendChild(cat);

      info.appendChild(el("p", "dx__hint", caso.regla));

      /* enumeration of legal supertype states */
      var subs2 = subconjuntos(estado.k);
      var legales = 0;
      var tabla = el("div", "dx__estados");
      var t = document.createElement("table");
      subs2.forEach(function (s) {
        var ok = (!estado.total || s.length >= 1) && (!estado.exclusiva || s.length <= 1);
        if (ok) legales++;
        var tr = document.createElement("tr");
        var td1 = el("td", ok ? "" : "no",
          s.length ? s.map(function (j) { return subs[j]; }).join(" + ") : "(ninguno)");
        var td2 = el("td", null, ok ? "posible" : "no permitido");
        tr.appendChild(td1); tr.appendChild(td2);
        t.appendChild(tr);
      });
      tabla.appendChild(t);
      info.appendChild(tabla);

      var f = el("p", "dx__formula");
      f.innerHTML = caso.formula.replace(/\bk\b/g, "<b>" + estado.k + "</b>") +
                    " = <b>" + legales + "</b> estados posibles";
      info.appendChild(f);
    }

    ejes.addEventListener("click", function (ev) {
      var b = ev.target.closest(".dx__btn");
      if (!b) return;
      estado[b.dataset.campo] = b.dataset.val === "true";
      pinta();
    });

    slider.addEventListener("input", function () {
      estado.k = Number(slider.value);
      kval.textContent = String(estado.k);
      pinta();
    });

    pinta();
  }

  /* ------------------------------------------------------------ mapeo drill */

  function mapeo(root, d) {
    var corregido = false;

    var mapa = el("div", "dx__mapa");
    d.items.forEach(function (it, idx) {
      var row = el("div", "dx__item");
      var p = el("p");
      p.innerHTML = it.elemento + "<em>" + esc(it.contexto || "") + "</em>";
      row.appendChild(p);

      var sel = el("select", "dx__sel");
      sel.dataset.i = String(idx);
      sel.appendChild(new Option("¿qué pasa con esto?", ""));
      d.reglas.forEach(function (r) { sel.appendChild(new Option(r.texto, r.id)); });
      row.appendChild(sel);
      mapa.appendChild(row);
    });
    root.appendChild(mapa);

    var bar = el("div", "dx__bar");
    var bCorregir = el("button", "dx__btn", "Corregir");
    var bReset = el("button", "dx__btn", "Reiniciar");
    bCorregir.type = bReset.type = "button";
    bar.appendChild(bCorregir);
    bar.appendChild(bReset);
    root.appendChild(bar);

    var marc = el("div", "dx__marcador");
    marc.hidden = true;
    root.appendChild(marc);

    var esquema = el("div", "dx__esquema");
    esquema.hidden = true;
    root.appendChild(esquema);

    function reset() {
      corregido = false;
      bCorregir.disabled = false;
      marc.hidden = true;
      esquema.hidden = true;
      Array.prototype.forEach.call(mapa.querySelectorAll(".dx__sel"), function (s) {
        s.value = ""; s.className = "dx__sel"; s.disabled = false;
      });
    }

    function corregir() {
      var bien = 0, mal = [];
      d.items.forEach(function (it, idx) {
        var sel = mapa.querySelector('.dx__sel[data-i="' + idx + '"]');
        var ok = sel.value === it.regla;
        sel.className = "dx__sel " + (ok ? "ok" : "mal");
        sel.disabled = true;
        if (ok) bien++; else mal.push(it);
      });

      corregido = true;
      bCorregir.disabled = true;
      marc.hidden = false;
      marc.innerHTML = "<b>" + bien + " de " + d.items.length + " bien.</b>";

      if (mal.length) {
        var ul = el("ul");
        mal.forEach(function (it) {
          var r = d.reglas.filter(function (x) { return x.id === it.regla; })[0];
          var li = el("li");
          li.innerHTML = it.elemento + " → <b>" + esc(r ? r.texto : it.regla) + "</b>. " +
                         (it.porque || "");
          ul.appendChild(li);
        });
        marc.appendChild(ul);
      }

      esquema.hidden = false;
      esquema.innerHTML = "<h4>" + esc(d.tituloEsquema || "La respuesta de la cátedra") + "</h4>";
      d.esquema.forEach(function (r) {
        var p = el("p", "dx__rel");
        p.innerHTML = r;
        esquema.appendChild(p);
      });
    }

    bCorregir.addEventListener("click", function () { if (!corregido) corregir(); });
    bReset.addEventListener("click", reset);
  }

  /* -------------------------------------------------------------- bootstrap */

  var TIPOS = [
    ["data-glosario", function (r) { glosario(r); }],
    ["data-notacion", notacion],
    ["data-especializacion", especializacion],
    ["data-mapeo", mapeo]
  ];

  function build(root, fn, necesitaDatos) {
    if (root.dataset.dxReady) return;
    root.dataset.dxReady = "1";

    var d = null;
    if (necesitaDatos) {
      var raw = root.querySelector(".dx__datos");
      if (!raw) return;
      try { d = JSON.parse(raw.textContent); }
      catch (e) {
        root.appendChild(el("p", "dx__hint", "No se pudo leer los datos del ejercicio."));
        return;
      }
      if (d.etiqueta) root.appendChild(el("span", "dx__label", d.etiqueta));
      if (d.consigna) root.appendChild(el("p", "dx__hint", d.consigna));
    }
    fn(root, d);
  }

  function boot() {
    TIPOS.forEach(function (par) {
      Array.prototype.forEach.call(document.querySelectorAll("[" + par[0] + "]"),
        function (r) { build(r, par[1], par[0] !== "data-glosario"); });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
