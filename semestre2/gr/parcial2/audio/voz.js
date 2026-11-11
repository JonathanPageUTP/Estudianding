/* ============================================================
   VOZ · lectura en voz alta compartida (guía y resumen)
   - Si hay MP3 generado para la sección (window.VOZ_AUDIO), usa <audio>:
     sigue sonando con la pantalla apagada y muestra controles en la
     pantalla de bloqueo (Media Session).
   - Si no, usa la voz del navegador (se corta al bloquear la pantalla).
   - Voz.dump() devuelve los textos que se leen, para generar los MP3
     (audio/generar_paginas.py).
   ============================================================ */
(function () {
  "use strict";
  var EXPAND = {
    "CIO": "CIO, Chief Information Officer,", "CISO": "CISO, Chief Information Security Officer,", "CEO": "CEO, Chief Executive Officer,",
    "CTO": "CTO, Chief Technology Officer,", "DPO": "DPO, Delegado de Protección de Datos,", "RACI": "RACI, matriz de asignación de responsabilidades,",
    "COBIT": "COBIT, Control Objectives for Information and related Technology,", "ITIL": "ITIL, IT Infrastructure Library,", "PDCA": "PDCA, Plan Do Check Act,",
    "RFP": "RFP, Request for Proposal,", "GRC": "GRC, Gobernanza, Riesgo y Cumplimiento,", "SLA": "SLA, nivel de servicio,", "SaaS": "SaaS, Software como Servicio,",
    "DRSEI": "D, R, S, E, I,"
  };
  var KEYS = new RegExp("\\b(" + Object.keys(EXPAND).join("|") + ")\\b", "g");

  function speakable(t, said) {
    t = t.replace(/[\u{1F000}-\u{1FAFF}\u{2600}-\u{27BF}\u{2B00}-\u{2BFF}\u{FE0F}\u{200D}\u{20E3}]/gu, " ");
    t = t.replace(/↔/g, " y viceversa ").replace(/→/g, " lleva a ").replace(/≥/g, " mayor o igual que ").replace(/≤/g, " menor o igual que ")
         .replace(/≠/g, " distinto de ").replace(/⊃/g, " contiene a ").replace(/(\d)\s?×/g, "$1 por").replace(/×/g, " por ")
         .replace(/·/g, ", ").replace(/[—–]/g, ", ").replace(/\|/g, ", y ").replace(/\t/g, ": ")
         .replace(/▾|▴|▸/g, "").replace(/(\d)\s?%/g, "$1 por ciento")
         .replace(/\bRRHH\b/g, "recursos humanos").replace(/\bTI\b/g, "T I").replace(/\bHW\b/g, "hardware").replace(/\bSW\b/g, "software")
         .replace(/\bJA\b/g, "Junta de Andalucía");
    t = t.replace(KEYS, function (m) { if (said[m]) return m; said[m] = 1; return EXPAND[m]; });
    return t.replace(/\s+/g, " ").trim();
  }

  var o, synth, hasTTS, AUD, items = [], audio, player, rate = 1, voice = null;
  var queue = [], qi = 0, curIdx = 0, curEl = null, playing = false, paused = false, gen = 0, said = {};
  var aMode = false, aBlocks = [], aTimes = [], playlist = [], pi = 0;

  function rawText(el) {
    if (o.textOf) { var x = o.textOf(el); if (x != null) return x; }
    if (el.getAttribute("data-tts")) return el.getAttribute("data-tts");
    if (el.tagName === "TR") return Array.prototype.map.call(el.cells, function (c) { return c.textContent; }).join("\t");
    return el.innerText || el.textContent;
  }
  function blocks(sec) {
    var list = Array.prototype.slice.call(sec.querySelectorAll(o.blocks)).filter(function (el) {
      return !el.closest(o.skip || "#vozNone") && !el.closest("." + o.btnClass) && el.textContent.trim();
    });
    return list.filter(function (el) { return !list.some(function (x) { return x !== el && x.contains(el); }); });
  }
  function texts(sec) {
    var s = {};
    return blocks(sec).map(function (el) { return speakable(rawText(el), s); });
  }
  function hasAudio(sec) { return !!AUD[o.key(sec)]; }
  function clearHi() { if (curEl) curEl.classList.remove(o.hiClass); curEl = null; }
  function mark(el) {
    clearHi(); curEl = el; el.classList.add(o.hiClass);
    if (document.visibilityState === "visible") {
      var r = el.getBoundingClientRect();
      if (r.top < 120 || r.bottom > window.innerHeight - 110) el.scrollIntoView({ behavior: "smooth", block: "center" });
    }
  }
  function $(id) { return document.getElementById(id); }
  function setPP() { var b = $("vozPP"); b.textContent = paused ? "▶" : "⏸"; b.setAttribute("aria-label", paused ? "Reanudar" : "Pausar"); }
  function show(sec) {
    $("vozNow").textContent = "🔊 " + (o.title(sec) || "");
    setPP(); player.classList.add("show"); document.body.classList.add("voz-playing");
  }
  function mediaSession(sec) {
    if (!("mediaSession" in navigator)) return;
    try {
      navigator.mediaSession.metadata = new MediaMetadata({ title: o.title(sec) || "", artist: o.artist || "" });
      navigator.mediaSession.setActionHandler("play", function () { if (paused) toggle(); });
      navigator.mediaSession.setActionHandler("pause", function () { if (!paused) toggle(); });
      navigator.mediaSession.setActionHandler("nexttrack", function () { if (pi + 1 < playlist.length) playAt(pi + 1); });
      navigator.mediaSession.setActionHandler("previoustrack", function () { if (pi > 0) playAt(pi - 1); else audio.currentTime = 0; });
      navigator.mediaSession.setActionHandler("stop", stop);
    } catch (e) {}
  }

  /* --- voz del navegador --- */
  function nextTTS() {
    clearHi();
    if (!playing) return;
    if (qi >= queue.length) { if (pi + 1 < playlist.length) playAt(pi + 1); else stop(); return; }
    curIdx = qi;
    var el = queue[qi++];
    var txt = speakable(rawText(el), said);
    if (!txt) { nextTTS(); return; }
    mark(el);
    var u = new SpeechSynthesisUtterance(txt);
    u.lang = voice ? voice.lang : "es-ES"; if (voice) u.voice = voice; u.rate = rate;
    var my = gen;
    u.onend = u.onerror = function () { if (playing && my === gen) nextTTS(); };
    synth.speak(u);
  }

  /* --- reproducción --- */
  function playAt(i) {
    var sec = playlist[i]; pi = i;
    gen++; synth.cancel(); audio.pause(); clearHi();
    if (o.onOpen) o.onOpen(sec);
    paused = false; playing = true;
    if (hasAudio(sec)) {
      var a = AUD[o.key(sec)];
      aMode = true; aBlocks = blocks(sec); aTimes = a.t;
      audio.src = o.base + a.src; audio.playbackRate = rate;
      audio.play().catch(function () { paused = true; setPP(); });
      show(sec); mediaSession(sec);
    } else if (hasTTS) {
      aMode = false; said = {}; queue = blocks(sec); qi = 0;
      show(sec); nextTTS();
    } else if (i + 1 < playlist.length) playAt(i + 1);
    else stop();
  }
  function stop() {
    gen++; playing = false; paused = false; synth.cancel(); audio.pause(); aMode = false; playlist = []; clearHi();
    player.classList.remove("show"); document.body.classList.remove("voz-playing");
    if ("mediaSession" in navigator) try { navigator.mediaSession.metadata = null; } catch (e) {}
  }
  function toggle() {
    if (aMode) {
      if (paused) { paused = false; audio.play(); } else { paused = true; audio.pause(); }
      setPP(); return;
    }
    // pausa propia: pause/resume de speechSynthesis falla en Chrome Android
    if (paused) { paused = false; playing = true; qi = curIdx; setPP(); nextTTS(); }
    else { paused = true; playing = false; gen++; synth.cancel(); setPP(); if (curEl) curEl.classList.add(o.hiClass); }
  }

  window.Voz = {
    speakable: speakable,
    dump: function () {
      var out = {};
      items.forEach(function (sec) {
        if (o.onOpen) o.onOpen(sec);  // igual que al reproducir
        out[o.key(sec)] = { title: o.title(sec), texts: texts(sec) };
      });
      return out;
    },
    playAll: function () {
      playlist = items.filter(function (s) { return o.visible ? o.visible(s) : true; });
      if (playlist.length) playAt(0);
    },
    init: function (opts) {
      o = opts;
      o.hiClass = o.hiClass || "tts-on"; o.btnClass = o.btnClass || "kit-tts"; o.base = o.base || "";
      items = opts.sections;
      AUD = window.VOZ_AUDIO || {};
      synth = window.speechSynthesis;
      hasTTS = !!(synth && window.SpeechSynthesisUtterance);
      if (!hasTTS) synth = { cancel: function () {}, getVoices: function () { return []; }, speak: function () {} };
      if (!hasTTS && !items.some(hasAudio)) return;
      try { rate = +localStorage.getItem(o.rateKey) || 1; } catch (e) {}
      function pick() {
        var vs = synth.getVoices().filter(function (v) { return /^es/i.test(v.lang); });
        voice = vs.filter(function (v) { return /es-(ES|MX|US|419)/i.test(v.lang); })[0] || vs[0] || null;
      }
      pick(); if (hasTTS && synth.onvoiceschanged !== undefined) synth.onvoiceschanged = pick;

      audio = new Audio(); audio.preload = "none";
      audio.addEventListener("timeupdate", function () {
        if (!aMode) return;
        var t = audio.currentTime, k = 0;
        for (var i = 0; i < aTimes.length; i++) if (aTimes[i] <= t + 0.15) k = i;
        if (aBlocks[k] && aBlocks[k] !== curEl) mark(aBlocks[k]);
      });
      audio.addEventListener("ended", function () { if (pi + 1 < playlist.length) playAt(pi + 1); else stop(); });

      player = document.createElement("div"); player.id = o.playerId || "vozPlayer";
      player.setAttribute("role", "region"); player.setAttribute("aria-label", "Reproductor de voz");
      player.innerHTML = '<span class="now" id="vozNow">🔊</span>' +
        '<button type="button" id="vozPrev" aria-label="Sección anterior">⏮</button>' +
        '<button type="button" id="vozPP" aria-label="Pausar">⏸</button>' +
        '<button type="button" id="vozNext" aria-label="Sección siguiente">⏭</button>' +
        '<button type="button" id="vozStop" aria-label="Detener">⏹</button>' +
        '<select id="vozRate" aria-label="Velocidad">' + [0.8, 0.9, 1, 1.1, 1.2, 1.3].map(function (r) {
          return '<option value="' + r + '"' + (r === rate ? " selected" : "") + '>' + r.toFixed(1) + '×</option>';
        }).join("") + '</select>';
      document.body.appendChild(player);
      $("vozStop").addEventListener("click", stop);
      $("vozPP").addEventListener("click", toggle);
      $("vozPrev").addEventListener("click", function () { if (pi > 0) playAt(pi - 1); else if (aMode) audio.currentTime = 0; else playAt(0); });
      $("vozNext").addEventListener("click", function () {
        if (pi + 1 < playlist.length) playAt(pi + 1);
        else { var j = items.indexOf(playlist[pi]); if (j >= 0 && j + 1 < items.length) { playlist = [items[j + 1]]; playAt(0); } }
      });
      $("vozRate").addEventListener("change", function () {
        rate = +this.value; audio.playbackRate = rate;
        try { localStorage.setItem(o.rateKey, rate); } catch (e) {}
      });

      items.forEach(function (sec) {
        var target = o.target(sec); if (!target) return;
        var b = document.createElement("button");
        b.type = "button"; b.className = o.btnClass; b.textContent = "🔊 Escuchar";
        b.setAttribute("aria-label", "Escuchar esta sección");
        b.addEventListener("click", function (e) {
          e.preventDefault(); e.stopPropagation();
          // desde aquí sigue con las secciones siguientes, como un podcast
          var j = items.indexOf(sec); playlist = items.slice(j); playAt(0);
        });
        target.appendChild(b);
      });
      if (o.allTarget) {
        var all = document.createElement("button");
        all.type = "button"; all.className = o.allClass || o.btnClass; all.textContent = "🎧 Escuchar todo";
        all.setAttribute("aria-label", "Escuchar todas las secciones seguidas");
        all.addEventListener("click", function () { window.Voz.playAll(); });
        o.allTarget.insertBefore(all, o.allBefore || null);
      }
      window.addEventListener("pagehide", function () { synth.cancel(); });
    }
  };
})();
