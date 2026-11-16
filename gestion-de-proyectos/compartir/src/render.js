/* Build-time renderer for the Canvas section of the shareable deliverable.
   Pure functions: CANVAS_DATA in, HTML string out. Used only by tools/build-compartir.sh (Node),
   so the generated page shows all four options even without JavaScript. The page script only
   adds tabs and the copy button on top (progressive enhancement). */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.CanvasRender = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  function esc(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  var SUGGESTED_LABEL = 'Sugerencia del borrador, a votar entre todos';

  function list(items) {
    return '<ul>' + items.map(function (t) { return '<li>' + esc(t) + '</li>'; }).join('') + '</ul>';
  }

  function optionPanel(data, id) {
    var o = data.options[id];
    var title = data.titleOf(id);
    var star = o.suggested
      ? ' <span class="star" aria-hidden="true">★</span> <span class="chip sug">' + esc(SUGGESTED_LABEL) + '</span>'
      : '';
    var facts = [
      ['Cliente principal', o.cliente],
      ['Quién paga', o.paga],
      ['Interno / externo', o.borde],
      ['El riesgo de elegirla', o.riesgo],
    ].map(function (f) { return '<div><dt>' + esc(f[0]) + '</dt><dd>' + esc(f[1]) + '</dd></div>'; }).join('');

    var cells = data.order.map(function (k) {
      var b = data.blocks[k];
      return '<article class="cv ' + esc(k) + '"><h4><span class="n">' + b.n + '</span>' + esc(b.name) + '</h4>' + list(o.blocks[k]) + '</article>';
    }).join('');

    var flow = o.flow.map(function (r) {
      return '<li><span class="sec">' + esc(r[0]) + '</span> <strong>' + esc(r[1]) + '</strong><p>' + esc(r[2]) + '</p></li>';
    }).join('');

    return '<section class="opt-panel" id="opt-' + id + '" data-opt="' + id + '" role="tabpanel" aria-labelledby="tab-' + id + '">' +
      '<h3 class="opt-title">' + esc(title) + star + '</h3>' +
      '<p class="opt-idea">' + esc(o.idea) + '</p>' +
      '<dl class="opt-facts">' + facts + '</dl>' +
      '<div class="canvas" role="group" aria-label="' + esc(title) + '">' + cells + '</div>' +
      '<h4 class="sub">Qué cambia en el resto del TP con esta opción</h4>' +
      '<ol class="flow">' + flow + '</ol>' +
      '<p class="copy-row js-only"><button type="button" class="copy-btn" data-copy="' + id + '">Copiar esta opción como texto</button> <span class="copy-status" role="status" aria-live="polite"></span></p>' +
      '</section>';
  }

  function tabs(data) {
    var ids = Object.keys(data.options);
    return '<div class="tabs js-only" role="tablist" aria-label="Opciones de modelo de negocio">' + ids.map(function (id) {
      var o = data.options[id];
      var suggested = !!o.suggested;
      return '<button type="button" role="tab" id="tab-' + id + '" aria-controls="opt-' + id + '" aria-selected="' + suggested + '" tabindex="' + (suggested ? 0 : -1) + '" data-opt="' + id + '">' +
        '<span class="tag">Opción ' + id.toUpperCase() + (suggested ? ' <span aria-hidden="true">★</span><span class="sr">(sugerida)</span>' : '') + '</span>' + esc(o.name) + '</button>';
    }).join('') + '</div>';
  }

  function definitions(data) {
    var items = data.order.map(function (k) {
      var b = data.blocks[k];
      return '<div><dt>' + b.n + ' · ' + esc(b.name) + '</dt><dd>' + esc(b.def) + '</dd></div>';
    }).join('');
    return '<details class="defs"><summary>Qué va en cada bloque (definiciones de la cátedra)</summary><dl>' + items + '</dl></details>';
  }

  function comparison(data) {
    var head = ['Opción', 'Segmento principal', 'De dónde sale la plata', 'Trabajo en el TP', 'Lo que van a preguntar', 'Conviene si…'];
    var rows = data.comparison.map(function (r) {
      var o = data.options[r.id];
      var label = '<strong>' + esc(r.id.toUpperCase()) + '</strong> · ' + esc(o.name) + (o.suggested ? ' <span class="star" aria-hidden="true">★</span><span class="sr">(sugerida)</span>' : '');
      return '<tr data-row="' + r.id + '">' +
        '<th scope="row" data-label="' + head[0] + '">' + label + '</th>' +
        '<td data-label="' + head[1] + '">' + esc(r.segmento) + '</td>' +
        '<td data-label="' + head[2] + '">' + esc(r.plata) + '</td>' +
        '<td data-label="' + head[3] + '"><span class="chip lvl-' + esc(r.trabajo.nivel) + '">' + esc(r.trabajo.texto) + '</span></td>' +
        '<td data-label="' + head[4] + '">' + esc(r.pregunta) + '</td>' +
        '<td data-label="' + head[5] + '">' + esc(r.conviene) + '</td></tr>';
    }).join('');
    return '<div class="table-wrap"><table class="stack" id="tabla-comparador"><caption class="muted cap">Comparación de las cuatro opciones</caption><thead><tr>' +
      head.map(function (h) { return '<th scope="col">' + h + '</th>'; }).join('') + '</tr></thead><tbody>' + rows + '</tbody></table></div>';
  }

  function valueMaps(data) {
    function side(key, label) {
      var v = data.valueMaps[key];
      function block(t, items) { return '<h5>' + t + '</h5>' + list(items); }
      return '<div class="vmap"><h4>' + label + ' · <span class="muted">' + esc(v.who) + '</span></h4>' +
        '<div class="vcol"><p class="vh">Bloque de cliente</p>' + block('Tareas del cliente', v.tareas) + block('Frustraciones', v.frust) + block('Beneficios esperados', v.benef) + '</div>' +
        '<div class="vcol"><p class="vh">Bloque de valor</p>' + block('Propuesta de valor', v.pv) + block('Generadores de alivio', v.alivio) + block('Generadores de satisfacción', v.satis) + '</div></div>';
    }
    return '<div class="vmaps">' + side('vecino', 'Lado vecino') + side('gcba', 'Lado GCBA (quien paga)') + '</div>';
  }

  function renderCanvasSection(data) {
    var ids = Object.keys(data.options);
    var rec = data.recommendation;
    return '' +
      '<div class="note" id="sugerencia"><strong>' + esc(SUGGESTED_LABEL) + '</strong>' +
      '<strong>' + esc(rec.titulo) + '</strong> ' + esc(rec.texto) + '</div>\n' +
      '<h3 id="modelos">Los cuatro modelos sobre los mismos nueve bloques</h3>\n' +
      definitions(data) + '\n' +
      tabs(data) + '\n' +
      '<div class="opts">' + ids.map(function (id) { return optionPanel(data, id); }).join('\n') + '</div>\n' +
      '<h3 id="comparador">Comparar antes de decidir</h3>\n' +
      '<p>Las cuatro son defendibles. No son igual de fáciles de escribir ni de sostener en la defensa.</p>\n' +
      comparison(data) + '\n' +
      '<h3 id="mapa-de-valor">Mapa de valor del segmento de ejemplo</h3>\n' +
      '<p>Se desarma la propuesta de valor en seis partes, como en el ejemplo de la cátedra. Sirve para cualquiera de las cuatro opciones: el bloque de cliente se completa primero y el de valor responde a lo que aparece ahí.</p>\n' +
      valueMaps(data);
  }

  return { renderCanvasSection: renderCanvasSection, SUGGESTED_LABEL: SUGGESTED_LABEL };
});
