/* Pure logic for tp/decisiones.html (offline voting) and tp/avance.html (progress tracker).
   No DOM, no storage: everything here is deterministic so it can be tested from node.
   Lives only in tp/assets/ (not synced from assets/).

   Ballot code : "TPV1." + base64url(JSON {v:1, n:name, t:timestamp, d:{decisionId:[optionId, reason?]}})
   State code  : "TPS1." + base64url(JSON {v:1, sections:{...}, checklist:{...}})

   Merge rules (documented in tp/LEEME.txt):
   - Ballots: same person = same normalized name (case, accents and spaces ignored).
     The ballot with the newest timestamp wins; equal timestamps -> the later one in the pasted text.
   - State: per section (and per checklist item) the entry with the newest timestamp wins;
     equal timestamps keep the local one. */
(function (root, factory) {
  if (typeof module === "object" && module.exports) module.exports = factory();
  else root.TPLogic = factory();
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  var STATUSES = ["sin-empezar", "borrador", "revision", "listo"];
  var STATUS_WEIGHT = { "sin-empezar": 0, borrador: 1 / 3, revision: 2 / 3, listo: 1 };
  var MAX_NAME = 60;
  var MAX_REASON = 200;
  var MAX_TEXT = 2000;

  /* ---------- helpers ---------- */

  function clip(value, max) {
    return String(value == null ? "" : value).trim().slice(0, max);
  }

  function normalizeName(name) {
    return String(name == null ? "" : name)
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .replace(/\s+/g, " ")
      .trim()
      .toLowerCase();
  }

  function b64urlEncode(text) {
    if (typeof Buffer !== "undefined") return Buffer.from(text, "utf8").toString("base64url");
    var bytes = new TextEncoder().encode(text);
    var bin = "";
    for (var i = 0; i < bytes.length; i++) bin += String.fromCharCode(bytes[i]);
    return btoa(bin).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
  }

  // Throws Error with a Spanish message when the input is not valid base64url text.
  function b64urlDecode(text) {
    if (!/^[A-Za-z0-9_-]+$/.test(text)) throw new Error("Código incompleto o con caracteres inválidos");
    if (text.length % 4 === 1) throw new Error("Código incompleto o con caracteres inválidos");
    if (typeof Buffer !== "undefined") return Buffer.from(text, "base64url").toString("utf8");
    var b64 = text.replace(/-/g, "+").replace(/_/g, "/");
    while (b64.length % 4) b64 += "=";
    var bin = atob(b64);
    var bytes = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
    return new TextDecoder("utf-8").decode(bytes);
  }

  // Codes pasted from chats often end with punctuation: strip it before decoding.
  function stripTrailingPunctuation(token) {
    return token.replace(/[.,;:!?)\]"'»”]+$/, "");
  }

  function parseJson(text) {
    try {
      return JSON.parse(text);
    } catch (e) {
      throw new Error("El contenido del código no es JSON válido");
    }
  }

  function clone(value) {
    return JSON.parse(JSON.stringify(value));
  }

  /* ---------- ballots ---------- */

  function encodeBallot(ballot) {
    var name = clip(ballot && ballot.name, MAX_NAME);
    if (!name) throw new Error("Falta el nombre de quien vota");
    var d = {};
    var votes = (ballot && ballot.votes) || {};
    Object.keys(votes).forEach(function (id) {
      var v = votes[id];
      if (!v || !v.option) return;
      var reason = clip(v.reason, MAX_REASON);
      d[id] = reason ? [String(v.option), reason] : [String(v.option)];
    });
    var ts = Number(ballot && ballot.ts);
    return "TPV1." + b64urlEncode(JSON.stringify({ v: 1, n: name, t: isFinite(ts) ? ts : 0, d: d }));
  }

  function decodeBallotPayload(token) {
    var payload = parseJson(b64urlDecode(token));
    if (!payload || typeof payload !== "object" || Array.isArray(payload)) throw new Error("Formato de voto no reconocido");
    if (payload.v !== 1) throw new Error("Versión de código no soportada (v" + payload.v + ")");
    var name = clip(payload.n, MAX_NAME);
    if (!name) throw new Error("Falta el nombre de quien vota");
    if (!payload.d || typeof payload.d !== "object" || Array.isArray(payload.d)) throw new Error("Votos con formato inválido");
    var votes = {};
    Object.keys(payload.d).forEach(function (id) {
      var entry = payload.d[id];
      if (!Array.isArray(entry) || typeof entry[0] !== "string" || !entry[0]) throw new Error("Votos con formato inválido");
      votes[id] = { option: entry[0], reason: clip(entry[1], MAX_REASON) };
    });
    var ts = Number(payload.t);
    return { name: name, ts: isFinite(ts) ? ts : 0, votes: votes };
  }

  // Finds every "TPV1.…" code in free text (chat exports, several people pasted together).
  function decodeBallots(text) {
    var out = { ballots: [], errors: [] };
    if (text == null || !String(text).trim()) return out;
    var lines = String(text).split(/\r?\n/);
    var found = false;
    lines.forEach(function (lineText, i) {
      var re = /TPV1\.(\S*)/g;
      var m;
      while ((m = re.exec(lineText))) {
        found = true;
        var token = stripTrailingPunctuation(m[1]);
        try {
          var ballot = decodeBallotPayload(token);
          ballot.line = i + 1;
          out.ballots.push(ballot);
        } catch (e) {
          out.errors.push({ line: i + 1, snippet: ("TPV1." + m[1]).slice(0, 40), reason: e.message });
        }
      }
    });
    if (!found) out.errors.push({ line: 1, snippet: String(text).trim().slice(0, 40), reason: "No se encontró ningún código de votos (empieza con TPV1.)" });
    return out;
  }

  function dedupeBallots(ballots) {
    var byName = {};
    var order = [];
    (ballots || []).forEach(function (b, index) {
      var key = normalizeName(b.name);
      if (!key) return;
      var current = byName[key];
      if (!current) order.push(key);
      // Newer timestamp wins; on a tie the later ballot in the list wins.
      if (!current || (b.ts || 0) >= (current.ballot.ts || 0)) byName[key] = { ballot: b, index: index };
    });
    return order.map(function (key) {
      return byName[key].ballot;
    });
  }

  function tally(decisions, ballots, opts) {
    opts = opts || {};
    var quorum = opts.quorum > 0 ? opts.quorum : 1;
    var roster = (opts.roster || []).map(function (n) { return String(n).trim(); }).filter(Boolean);
    var participants = (ballots || []).map(function (b) { return b.name; });
    var ignored = [];

    var results = (decisions || []).map(function (decision) {
      var counts = {};
      var voters = {};
      decision.options.forEach(function (o) {
        counts[o.id] = 0;
        voters[o.id] = [];
      });
      var reasons = [];
      var voted = {};
      (ballots || []).forEach(function (b) {
        var vote = b.votes && b.votes[decision.id];
        if (!vote) return;
        if (!Object.prototype.hasOwnProperty.call(counts, vote.option)) {
          ignored.push({ name: b.name, decision: decision.id, option: vote.option, reason: "Opción desconocida" });
          return;
        }
        counts[vote.option] += 1;
        voters[vote.option].push(b.name);
        voted[normalizeName(b.name)] = true;
        if (vote.reason) reasons.push({ name: b.name, option: vote.option, reason: vote.reason });
      });

      var total = 0;
      var max = 0;
      Object.keys(counts).forEach(function (id) {
        total += counts[id];
        if (counts[id] > max) max = counts[id];
      });
      var leaders = max > 0 ? Object.keys(counts).filter(function (id) { return counts[id] === max; }) : [];
      var status = total === 0 ? "sin-votos" : leaders.length > 1 ? "empate" : "ganadora";
      var winner = status === "ganadora" ? leaders[0] : null;

      return {
        id: decision.id,
        title: decision.title,
        total: total,
        counts: counts,
        voters: voters,
        reasons: reasons,
        winner: winner,
        tie: status === "empate" ? leaders : [],
        status: status,
        share: winner ? max / total : 0,
        majority: winner ? max * 2 > total : false,
        quorumMet: total >= quorum,
        missing: participants.filter(function (name) { return !voted[normalizeName(name)]; }),
      };
    });

    // Known decision ids for votes that point to decisions that no longer exist.
    var known = {};
    (decisions || []).forEach(function (d) { known[d.id] = true; });
    (ballots || []).forEach(function (b) {
      Object.keys(b.votes || {}).forEach(function (id) {
        if (!known[id]) ignored.push({ name: b.name, decision: id, option: b.votes[id].option, reason: "Decisión desconocida" });
      });
    });

    var have = {};
    participants.forEach(function (n) { have[normalizeName(n)] = true; });
    return {
      decisions: results,
      participants: participants,
      ignored: ignored,
      quorum: quorum,
      missingRoster: roster.filter(function (n) { return !have[normalizeName(n)]; }),
    };
  }

  function optionLabel(decision, id) {
    var o = decision.options.filter(function (x) { return x.id === id; })[0];
    return o ? o.label : id;
  }

  function exportClosed(decisions, result) {
    var closed = [];
    var pending = [];
    result.decisions.forEach(function (r, i) {
      var decision = decisions[i];
      if (r.status === "ganadora" && r.quorumMet) {
        var note = r.majority ? "" : ", sin mayoría absoluta";
        closed.push("- **" + r.title + "** → **" + optionLabel(decision, r.winner) + "** (" + r.counts[r.winner] + " de " + r.total + " votos" + note + ")");
      } else if (r.status === "empate") {
        pending.push("- **" + r.title + "**: empate entre " + r.tie.map(function (id) { return optionLabel(decision, id); }).join(" y "));
      } else if (r.status === "sin-votos") {
        pending.push("- **" + r.title + "**: sin votos");
      } else {
        pending.push("- **" + r.title + "**: faltan votos para el quórum (" + r.total + " de " + result.quorum + ")");
      }
    });
    var md = "### Decisiones del equipo\n\n";
    md += closed.length ? closed.join("\n") : "No hay decisiones cerradas todavía.";
    if (pending.length) md += "\n\n**Pendientes**\n\n" + pending.join("\n");
    return md + "\n";
  }

  /* ---------- progress tracker state ---------- */

  function emptyState() {
    return { v: 1, sections: {}, checklist: {} };
  }

  function setSection(state, n, patch, now) {
    var next = clone(state);
    patch = patch || {};
    if (patch.status !== undefined && STATUSES.indexOf(patch.status) < 0) throw new Error("Estado desconocido: " + patch.status);
    var key = String(n);
    var old = next.sections[key] || { status: "sin-empezar", owner: "", reviewer: "", notes: "", checks: {}, ts: 0 };
    var checks = Object.assign({}, old.checks, patch.checks || {});
    next.sections[key] = {
      status: patch.status !== undefined ? patch.status : old.status,
      owner: patch.owner !== undefined ? clip(patch.owner, MAX_NAME) : old.owner,
      reviewer: patch.reviewer !== undefined ? clip(patch.reviewer, MAX_NAME) : old.reviewer,
      notes: patch.notes !== undefined ? clip(patch.notes, MAX_TEXT) : old.notes,
      checks: checks,
      ts: now,
    };
    return next;
  }

  function setChecklist(state, id, done, now) {
    var next = clone(state);
    next.checklist[id] = { done: !!done, ts: now };
    return next;
  }

  function newest(a, b) {
    // Newest timestamp wins; on a tie keep `a` (the local entry).
    return (b.ts || 0) > (a.ts || 0) ? b : a;
  }

  function mergeMaps(a, b) {
    var out = {};
    Object.keys(a || {}).forEach(function (k) { out[k] = clone(a[k]); });
    Object.keys(b || {}).forEach(function (k) {
      out[k] = out[k] ? clone(newest(out[k], b[k])) : clone(b[k]);
    });
    return out;
  }

  function mergeState(a, b) {
    return { v: 1, sections: mergeMaps(a.sections, b.sections), checklist: mergeMaps(a.checklist, b.checklist) };
  }

  function encodeState(state) {
    return "TPS1." + b64urlEncode(JSON.stringify(state));
  }

  function normalizeState(raw) {
    if (!raw || typeof raw !== "object" || Array.isArray(raw) || typeof raw.sections !== "object" || raw.sections === null || Array.isArray(raw.sections)) {
      throw new Error("Formato de estado no reconocido");
    }
    var state = emptyState();
    Object.keys(raw.sections).forEach(function (k) {
      var s = raw.sections[k] || {};
      if (STATUSES.indexOf(s.status) < 0) throw new Error("Formato de estado no reconocido (estado inválido en la sección " + k + ")");
      var checks = {};
      Object.keys(s.checks || {}).forEach(function (c) { checks[c] = !!s.checks[c]; });
      state.sections[k] = {
        status: s.status,
        owner: clip(s.owner, MAX_NAME),
        reviewer: clip(s.reviewer, MAX_NAME),
        notes: clip(s.notes, MAX_TEXT),
        checks: checks,
        ts: Number(s.ts) || 0,
      };
    });
    var list = raw.checklist && typeof raw.checklist === "object" ? raw.checklist : {};
    Object.keys(list).forEach(function (id) {
      state.checklist[id] = { done: !!(list[id] && list[id].done), ts: Number(list[id] && list[id].ts) || 0 };
    });
    return state;
  }

  function decodeState(text) {
    if (text == null) return { state: null, error: "No se encontró ningún código de estado (empieza con TPS1.)" };
    var m = /TPS1\.(\S*)/.exec(String(text));
    if (!m) return { state: null, error: "No se encontró ningún código de estado (empieza con TPS1.)" };
    try {
      return { state: normalizeState(parseJson(b64urlDecode(stripTrailingPunctuation(m[1])))), error: null };
    } catch (e) {
      return { state: null, error: e.message };
    }
  }

  function progress(state, total) {
    var counts = { "sin-empezar": 0, borrador: 0, revision: 0, listo: 0 };
    var sum = 0;
    for (var n = 1; n <= total; n++) {
      var s = state.sections[String(n)];
      var status = s ? s.status : "sin-empezar";
      counts[status] += 1;
      sum += STATUS_WEIGHT[status];
    }
    return { percent: total ? Math.round((sum / total) * 100) : 0, counts: counts };
  }

  return {
    STATUSES: STATUSES,
    normalizeName: normalizeName,
    encodeBallot: encodeBallot,
    decodeBallots: decodeBallots,
    dedupeBallots: dedupeBallots,
    tally: tally,
    exportClosed: exportClosed,
    emptyState: emptyState,
    normalizeState: normalizeState,
    setSection: setSection,
    setChecklist: setChecklist,
    mergeState: mergeState,
    encodeState: encodeState,
    decodeState: decodeState,
    progress: progress,
  };
});
