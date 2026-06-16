/* explorer.js — Casey Chinese School · Character Explorer engine
   Pure vanilla, no dependencies. Renders the animated stroke-order "writer",
   the character info, the example sentence, and the wall of characters.
   Stroke data is makemeahanzi 1024 Y-up space (see char-data.js).            */
(function () {
  "use strict";
  var DATA = window.CHAR_DATA || [];
  if (!DATA.length) return;

  var LS = "ccs-charexp";
  var prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // ---- persisted state ----
  var saved = {};
  try { saved = JSON.parse(localStorage.getItem(LS)) || {}; } catch (e) {}
  var GROUPS = [];
  DATA.forEach(function (d) { if (GROUPS.indexOf(d.group) < 0) GROUPS.push(d.group); });
  var GROUP_ZH = window.CHAR_GROUPS || {};
  function zhFor(g) { return GROUP_ZH[g] || ""; }

  var startIdx = clamp(saved.idx || 0, 0, DATA.length - 1);
  var state = {
    idx: startIdx,
    pinyin: saved.pinyin !== false,        // shown by default
    rainbow: saved.rainbow !== false,        // colour on by default
    numbers: saved.numbers !== false,        // order numbers on by default
    speed: saved.speed || 1,               // 0.6 slow .. 1.6 fast
    // the wall opens on a theme, never the full 300-cell list; only a real
    // theme name is restored ("all" is a within-visit choice)
    wallGroup: GROUPS.indexOf(saved.wallGroup) >= 0 ? saved.wallGroup : DATA[startIdx].group
  };
  function persist() {
    try { localStorage.setItem(LS, JSON.stringify(state)); } catch (e) {}
  }

  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function $(s, r) { return (r || document).querySelector(s); }
  function $all(s, r) { return [].slice.call((r || document).querySelectorAll(s)); }

  // ---- rainbow palette (matches the textbook stroke-cell generator) ----
  function palette(n) {
    var out = [];
    for (var i = 0; i < n; i++) {
      var t = n <= 1 ? 0 : i / (n - 1);
      out.push("hsl(" + (8 + t * 282).toFixed(1) + " 64% 47%)");
    }
    return out;
  }

  // ---- order-number layout (ported from stroke-cell.js) ----
  function layoutNumbers(medians) {
    var orig = medians.map(function (m) { return [m[0][0], 900 - m[0][1]]; });
    var pos = orig.map(function (p) { return [p[0], p[1]]; });
    var R = 104;
    for (var it = 0; it < 90; it++) {
      for (var i = 0; i < pos.length; i++) {
        for (var j = i + 1; j < pos.length; j++) {
          var dx = pos[j][0] - pos[i][0], dy = pos[j][1] - pos[i][1];
          var dist = Math.hypot(dx, dy) || 0.01;
          if (dist < R) {
            var push = (R - dist) / 2; dx /= dist; dy /= dist;
            pos[i][0] -= dx * push; pos[i][1] -= dy * push;
            pos[j][0] += dx * push; pos[j][1] += dy * push;
          }
        }
      }
      for (var k = 0; k < pos.length; k++) {
        pos[k][0] += (orig[k][0] - pos[k][0]) * 0.06;
        pos[k][1] += (orig[k][1] - pos[k][1]) * 0.06;
      }
    }
    pos.forEach(function (p) {
      p[0] = clamp(p[0], 60, 964); p[1] = clamp(p[1], 60, 964);
    });
    return pos;
  }

  function medianPath(m) {
    return "M " + m.map(function (p) { return p[0] + " " + p[1]; }).join(" L ");
  }

  function gridSVG() {
    return '<svg class="writer__grid" viewBox="0 0 1024 1024" aria-hidden="true">' +
      '<rect x="3" y="3" width="1018" height="1018" rx="10" fill="none" class="g-frame"/>' +
      '<line class="g-dash" x1="512" y1="14" x2="512" y2="1010"/>' +
      '<line class="g-dash" x1="14" y1="512" x2="1010" y2="512"/>' +
      '<line class="g-diag" x1="40" y1="40" x2="984" y2="984"/>' +
      '<line class="g-diag" x1="984" y1="40" x2="40" y2="984"/></svg>';
  }

  // ---- build the writer for a character ----
  var writerEl, inkEls = [], seqTimers = [], stepIdx = 0;

  function buildWriter(d) {
    seqTimers.forEach(clearTimeout); seqTimers = [];
    stepIdx = 0;
    var n = d.s.length;
    var cols = state.rainbow ? palette(n) : null;
    var defs = "", ghosts = "", inks = "";
    for (var i = 0; i < n; i++) {
      var col = cols ? cols[i] : "var(--ink-cn)";
      defs += '<clipPath id="cp' + i + '"><path d="' + d.s[i] + '"/></clipPath>';
      ghosts += '<path class="ghost" d="' + d.s[i] + '"/>';
      inks += '<path class="ink" data-i="' + i + '" d="' + medianPath(d.m[i]) +
        '" fill="none" stroke="' + col + '" stroke-width="166" stroke-linecap="round" ' +
        'stroke-linejoin="round" clip-path="url(#cp' + i + ')"/>';
    }
    var nums = "";
    if (state.numbers) {
      var pos = layoutNumbers(d.m);
      pos.forEach(function (p, i) {
        var col = cols ? cols[i] : "var(--ink-cn)";
        nums += '<text x="' + p[0].toFixed(0) + '" y="' + p[1].toFixed(0) + '" ' +
          'text-anchor="middle" dominant-baseline="central" class="snum" fill="' + col + '">' +
          (i + 1) + '</text>';
      });
    }
    writerEl.innerHTML = gridSVG() +
      '<svg class="writer__char" viewBox="0 0 1024 1024" role="img" aria-label="' +
      d.ch + ' — animated stroke order, ' + n + ' strokes">' +
      '<defs>' + defs + '</defs>' +
      '<g transform="translate(0,900) scale(1,-1)">' + ghosts + inks + '</g>' +
      '<g class="writer__nums">' + nums + '</g></svg>';

    inkEls = $all(".ink", writerEl);
    inkEls.forEach(function (p) {
      var L = p.getTotalLength();
      p.dataset.len = L;
      p.style.strokeDasharray = L + "px";
      p.style.strokeDashoffset = L + "px";
    });
  }

  // CSS transitions (not WAAPI) — stroke-dashoffset keyframes are unreliable
  // cross-browser; transitions with explicit px units work everywhere and the
  // end state lives in inline style, so nothing fights the cascade afterwards.
  function resetStroke(p) {
    p.style.transition = "none";
    p.style.strokeDashoffset = p.dataset.len + "px";
  }
  function drawStroke(p, dur) {
    void p.getBoundingClientRect();          // commit the start value first
    p.style.transition = "stroke-dashoffset " + dur + "ms cubic-bezier(.45,.05,.3,1)";
    p.style.strokeDashoffset = "0px";
  }

  function showAll() {
    inkEls.forEach(function (p) {
      p.style.transition = "none";
      p.style.strokeDashoffset = "0px";
    });
    stepIdx = inkEls.length;
  }

  // Note: play() and step() run even under prefers-reduced-motion — they only
  // fire on an explicit user action (Replay/Step/option click), and the stroke
  // animation is the lesson content itself, not decoration. Reduced motion is
  // honoured where playback would start on its own: see render().
  function play() {
    seqTimers.forEach(clearTimeout); seqTimers = [];
    inkEls.forEach(resetStroke);
    stepIdx = 0;
    var i = 0;
    function next() {
      if (i >= inkEls.length) return;
      var p = inkEls[i], L = +p.dataset.len;
      var dur = clamp(220 + L * 0.34, 320, 900) / state.speed;
      drawStroke(p, dur);
      i++; stepIdx = i;
      var t = setTimeout(next, dur + 80 / state.speed);
      seqTimers.push(t);
    }
    next();
  }

  function step() {
    seqTimers.forEach(clearTimeout); seqTimers = [];
    if (stepIdx >= inkEls.length) {            // restart from blank
      inkEls.forEach(resetStroke);
      stepIdx = 0;
    }
    drawStroke(inkEls[stepIdx], 460 / state.speed);
    stepIdx++;
  }

  // ---- info panel ----
  var CJK = /[\u3400-\u9fff\u2e80-\u2eff\u31c0-\u31ef⺈㇏]+/g;
  function markCJK(str) {
    return str.replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(CJK, function (m) { return '<span class="zh-inline" lang="zh-Hans">' + m + "</span>"; });
  }
  function rubyFor(seg, focus) {
    return seg.map(function (pair) {
      var ch = pair[0], py = pair[1];
      if (!py) return '<span class="punc">' + ch + "</span>";
      var cls = ch === focus ? "ru focus" : "ru";
      return '<ruby class="' + cls + '">' + ch + "<rt>" + py + "</rt></ruby>";
    }).join("");
  }

  function renderInfo(d) {
    $("#ce-py").innerHTML = d.py;
    $("#ce-en").textContent = d.en;
    $("#ce-rad").innerHTML = '<span class="zh-inline" lang="zh-Hans">' + d.radical + "</span> " +
      '<span class="chip__t">radical 部首 · ' + d.radEn + "</span>";
    $("#ce-strokes").innerHTML = d.s.length + ' <span class="chip__t">stroke' + (d.s.length > 1 ? "s" : "") + " · 笔画</span>";
    $("#ce-origin").innerHTML = markCJK(d.origin);
    $("#ce-word").innerHTML = rubyFor(d.word.seg, d.ch);
    $("#ce-word-en").textContent = d.word.en;
    $("#ce-sentence").innerHTML = rubyFor(d.ex.seg, d.ch);
    $("#ce-sentence-en").textContent = d.ex.en;

    var tot = "" + DATA.length;
    var pos = "" + (state.idx + 1);
    while (pos.length < tot.length) pos = "0" + pos;
    $("#ce-pos").innerHTML = pos + ' <span class="sep">/</span> ' + tot;
    var gz = zhFor(d.group);
    $("#ce-group").textContent = d.group + (gz ? " · " + gz : "");
  }

  function updateWall() {
    $all(".wall__cell").forEach(function (b, i) {
      var on = i === state.idx;
      b.classList.toggle("is-active", on);
      b.setAttribute("aria-current", on ? "true" : "false");
    });
  }

  // ---- main render ----
  function render(animate) {
    var d = DATA[state.idx];
    buildWriter(d);
    renderInfo(d);
    updateWall();
    persist();
    if (animate !== false && !prefersReduced) requestAnimationFrame(play);
    else showAll();
  }

  // indices visible under the current wall theme filter
  function visibleIdxs() {
    var out = [];
    DATA.forEach(function (d, i) {
      if (state.wallGroup === "all" || d.group === state.wallGroup) out.push(i);
    });
    return out;
  }

  function go(delta) {
    var list = visibleIdxs();
    var p = list.indexOf(state.idx);
    state.idx = p < 0 ? list[0] : list[(p + delta + list.length) % list.length];
    render(true);
    // keep active wall cell in view (horizontal scroll only — never page scroll)
    var cell = $all(".wall__cell")[state.idx];
    if (cell && cell.parentElement) {
      var wall = cell.parentElement;
      var target = cell.offsetLeft - wall.clientWidth / 2 + cell.clientWidth / 2;
      if (wall.scrollWidth > wall.clientWidth) wall.scrollTo({ left: target, behavior: "smooth" });
    }
  }

  // ---- pinyin toggle ----
  function setPinyin(on) {
    state.pinyin = on;
    document.body.classList.toggle("no-pinyin", !on);
    var btn = $("#ce-pinyin");
    if (btn) { btn.setAttribute("aria-pressed", on ? "true" : "false"); btn.classList.toggle("is-off", !on); }
    persist();
  }

  // ---- options ----
  function setOpt(key, val) {
    state[key] = val; persist();
    render(false);            // rebuild without auto-replay
    syncOptUI();
    if (key !== "speed") play();
  }
  function syncOptUI() {
    var r = $("#opt-rainbow"), n = $("#opt-numbers");
    if (r) { r.setAttribute("aria-pressed", state.rainbow); r.classList.toggle("is-on", state.rainbow); }
    if (n) { n.setAttribute("aria-pressed", state.numbers); n.classList.toggle("is-on", state.numbers); }
  }

  // ---- read aloud ----
  // Primary: pre-generated MP3 files in learn/audio/ (XiaoxiaoNeural quality).
  // Fallback: Web Speech API, only if a real zh-* voice is confirmed available
  // (guards against Firefox/Arch espeak-ng outputting technical error strings,
  // and Chrome/Arch falling back to an English voice that mispronounces characters).
  var AUDIO_BASE = "learn/audio/";
  var currentAudio = null;

  function stopAudio() {
    if (currentAudio) { currentAudio.pause(); currentAudio.currentTime = 0; currentAudio = null; }
    $all(".say.is-speaking").forEach(function (b) { b.classList.remove("is-speaking"); });
  }

  function playFile(path, btn) {
    stopAudio();
    var a = new Audio(path);
    currentAudio = a;
    if (btn) btn.classList.add("is-speaking");
    a.onended = a.onerror = function () {
      if (currentAudio === a) currentAudio = null;
      if (btn) btn.classList.remove("is-speaking");
    };
    a.play();
  }

  // Web Speech fallback (used only when audio files are absent)
  function zhVoice() {
    if (!("speechSynthesis" in window)) return null;
    var vs = speechSynthesis.getVoices().filter(function (v) { return /^zh([-_]|$)/i.test(v.lang); });
    var cn = vs.filter(function (v) { return /CN|cmn|Hans/i.test(v.lang + " " + v.name); });
    return cn[0] || vs[0] || null;
  }
  function speakFallback(text, btn) {
    if (!text || !("speechSynthesis" in window) || !zhVoice()) return;
    speechSynthesis.cancel();
    $all(".say.is-speaking").forEach(function (b) { b.classList.remove("is-speaking"); });
    var u = new SpeechSynthesisUtterance(text);
    u.lang = "zh-CN";
    u.rate = 0.75;
    var v = zhVoice();
    if (v) u.voice = v;
    if (btn) {
      btn.classList.add("is-speaking");
      u.onend = u.onerror = function () { btn.classList.remove("is-speaking"); };
    }
    speechSynthesis.speak(u);
  }

  function speak(path, text, btn) {
    // Try the MP3 first; if the file is missing (404 or network error) fall back to TTS
    stopAudio();
    var a = new Audio(path);
    currentAudio = a;
    if (btn) btn.classList.add("is-speaking");
    a.onended = function () {
      if (currentAudio === a) currentAudio = null;
      if (btn) btn.classList.remove("is-speaking");
    };
    a.onerror = function () {
      if (currentAudio === a) currentAudio = null;
      if (btn) btn.classList.remove("is-speaking");
      speakFallback(text, btn);
    };
    a.play().catch(function () {
      currentAudio = null;
      if (btn) btn.classList.remove("is-speaking");
      speakFallback(text, btn);
    });
  }

  function initSpeech() {
    var sayBtn = $("#ce-say"), sayWordBtn = $("#ce-say-word"), saySentBtn = $("#ce-say-sent");
    if (!sayBtn) return;

    // Always show buttons — MP3 files work everywhere, TTS is a silent fallback
    sayBtn.hidden = false;
    sayBtn.addEventListener("click", function () {
      var i = state.idx;
      speak(AUDIO_BASE + "char-" + i + ".mp3", DATA[i].ch, sayBtn);
    });
    if (sayWordBtn) {
      sayWordBtn.hidden = false;
      sayWordBtn.addEventListener("click", function () {
        var i = state.idx, seg = DATA[i].word.seg;
        speak(AUDIO_BASE + "word-" + i + ".mp3", seg.map(function (p) { return p[0]; }).join(""), sayWordBtn);
      });
    }
    if (saySentBtn) {
      saySentBtn.hidden = false;
      saySentBtn.addEventListener("click", function () {
        var i = state.idx, seg = DATA[i].ex.seg;
        speak(AUDIO_BASE + "sent-" + i + ".mp3", seg.map(function (p) { return p[0]; }).join(""), saySentBtn);
      });
    }

    // Warm up voice list for fallback path
    if ("speechSynthesis" in window) speechSynthesis.getVoices();
  }

  // ---- build the wall ----
  function buildWall() {
    var wall = $("#ce-wall");
    wall.innerHTML = DATA.map(function (d, i) {
      return '<button class="wall__cell" data-i="' + i + '" type="button" ' +
        'aria-label="' + d.ch + " " + d.py + " — " + d.en + '">' +
        '<span class="wall__ch" lang="zh-Hans">' + d.ch + "</span>" +
        '<span class="wall__py">' + d.py + "</span></button>";
    }).join("");
    $all(".wall__cell", wall).forEach(function (b) {
      b.addEventListener("click", function () {
        state.idx = +b.dataset.i;
        render(true);
        var explorer = $("#explorer");
        if (explorer) explorer.scrollIntoView({ behavior: prefersReduced ? "auto" : "smooth", block: "start" });
      });
    });
  }

  // ---- wall theme filter ----
  function buildFilter() {
    var box = $("#ce-filter");
    if (!box) return;
    var chips = GROUPS.map(function (g) {
      return '<button class="fchip" data-g="' + g + '" type="button">' + g +
        '<span class="fchip__zh" lang="zh-Hans">' + zhFor(g) + "</span></button>";
    });
    chips.push('<button class="fchip" data-g="all" type="button">All<span class="fchip__zh" lang="zh-Hans">全部</span></button>');
    box.innerHTML = chips.join("");
    $all(".fchip", box).forEach(function (b) {
      b.addEventListener("click", function () { setFilter(b.dataset.g, true); });
    });
  }

  function setFilter(g, jump) {
    state.wallGroup = GROUPS.indexOf(g) >= 0 ? g : "all";
    applyFilter();
    persist();
    if (jump) {                      // picking a theme opens its first character
      var list = visibleIdxs();
      if (list.indexOf(state.idx) < 0) { state.idx = list[0]; render(true); }
    }
  }

  function applyFilter() {
    var cells = $all(".wall__cell");
    DATA.forEach(function (d, i) {
      cells[i].hidden = state.wallGroup !== "all" && d.group !== state.wallGroup;
    });
    $all(".fchip").forEach(function (b) {
      var on = b.dataset.g === state.wallGroup;
      b.classList.toggle("is-on", on);
      b.setAttribute("aria-pressed", on ? "true" : "false");
    });
    var title = $("#wall-title"), titleZh = $("#wall-zh");
    if (title) {
      title.textContent = state.wallGroup === "all"
        ? "All " + DATA.length + " characters"
        : state.wallGroup + " · " + visibleIdxs().length + " characters";
    }
    if (titleZh) {
      titleZh.textContent = state.wallGroup === "all"
        ? "三百常用字" : (zhFor(state.wallGroup) || "三百常用字");
    }
  }

  // ---- init ----
  function init() {
    writerEl = $("#ce-writer");
    buildWall();
    buildFilter();
    applyFilter();
    setPinyin(state.pinyin);
    initSpeech();

    $("#ce-replay").addEventListener("click", play);
    $("#ce-step").addEventListener("click", step);
    $("#ce-prev").addEventListener("click", function () { go(-1); });
    $("#ce-next").addEventListener("click", function () { go(1); });
    $("#ce-pinyin").addEventListener("click", function () { setPinyin(!state.pinyin); });

    var r = $("#opt-rainbow"), n = $("#opt-numbers");
    if (r) r.addEventListener("click", function () { setOpt("rainbow", !state.rainbow); });
    if (n) n.addEventListener("click", function () { setOpt("numbers", !state.numbers); });

    var radChip = $("#ce-rad");
    if (radChip) radChip.addEventListener("click", function () {
      if (window.CCS_RADICALS) {
        window.CCS_RADICALS.openFor(DATA[state.idx].radical);
        $("#radicals").scrollIntoView({ behavior: prefersReduced ? "auto" : "smooth" });
      }
    });

    // keyboard: arrow keys flip characters while the explorer is in view.
    // Space/Enter are deliberately left alone — hijacking Space breaks
    // scroll-by-keyboard, and Replay is a focusable button already.
    document.addEventListener("keydown", function (e) {
      if (/input|textarea|select/i.test((e.target.tagName || ""))) return;
      var stage = $("#explorer");
      var near = stage && isInView(stage);
      if (!near) return;
      if (e.key === "ArrowRight") { e.preventDefault(); go(1); }
      else if (e.key === "ArrowLeft") { e.preventDefault(); go(-1); }
    });

    syncOptUI();
    render(true);
  }

  function isInView(el) {
    var r = el.getBoundingClientRect();
    return r.top < window.innerHeight && r.bottom > 0;
  }

  // hand-off for the radicals section below: open a character from outside,
  // switching the wall to that character's theme so everything stays in step
  window.CCS_EXPLORER = {
    open: function (ch) {
      for (var i = 0; i < DATA.length; i++) {
        if (DATA[i].ch === ch) {
          state.idx = i;
          setFilter(DATA[i].group);
          render(true);
          return;
        }
      }
    }
  };

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
