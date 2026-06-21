/* radicals.js — Casey Chinese School · Radical corner
   Renders the radical detail card and the radical wall on characters.html.
   Example characters are matched live from CHAR_DATA (same page), so the
   card always reflects exactly what's in the 300-character library.
   Clicking an example hands over to the explorer via window.CCS_EXPLORER.  */
(function () {
  "use strict";
  var RD = window.RADICAL_DATA || [];
  var DATA = window.CHAR_DATA || [];
  if (!RD.length || !DATA.length) return;

  var prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var cur = 0;

  function $(s, r) { return (r || document).querySelector(s); }
  function $all(s, r) { return [].slice.call((r || document).querySelectorAll(s)); }

  // characters in the library that carry this radical (or ARE its full form)
  function examplesFor(rd) {
    return DATA.filter(function (d) {
      return d.radical === rd.r || (rd.v && (d.radical === rd.v || d.ch === rd.v));
    });
  }

  var CJK = /[㐀-鿿⺼⻊]+/g;
  function markCJK(str) {
    return str.replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(CJK, function (m) { return '<span class="zh-inline" lang="zh-Hans">' + m + "</span>"; });
  }

  function render() {
    var rd = RD[cur];
    var ex = examplesFor(rd);

    $("#rd-glyph").textContent = rd.r;
    $("#rd-variant").innerHTML = rd.v
      ? 'full form · 本字 <span class="zh-inline" lang="zh-Hans">' + rd.v + "</span>"
      : "";
    $("#rd-variant").hidden = !rd.v;
    $("#rd-name").textContent = (rd.py ? rd.py + " · " : "") + rd.en;
    $("#rd-nick").innerHTML = '<span class="zh-inline" lang="zh-Hans">' + rd.nick + "</span> " +
      rd.nickPy + ' — "' + rd.nickEn + '"';
    $("#rd-pos").textContent = rd.pos;
    $("#rd-mean").innerHTML = markCJK(rd.mean) +
      (rd.zhMean ? '<span class="rad-zh" lang="zh-Hans">' + rd.zhMean + "</span>" : "");
    $("#rd-story").innerHTML = markCJK(rd.story);

    var tipBlock = $("#rd-tip-block");
    if (rd.tip) { tipBlock.hidden = false; $("#rd-tip").innerHTML = markCJK(rd.tip); }
    else tipBlock.hidden = true;

    $("#rd-ex-count").textContent = ex.length + " of our 300";
    $("#rd-ex").innerHTML = ex.map(function (d) {
      return '<button class="rad-ex" type="button" data-ch="' + d.ch + '" ' +
        'title="' + d.py + " — " + d.en.replace(/"/g, "&quot;") + '" ' +
        'aria-label="' + d.ch + " " + d.py + " — " + d.en.replace(/"/g, "&quot;") +
        '. Open in the explorer above">' +
        '<span class="rad-ex__ch" lang="zh-Hans">' + d.ch + "</span>" +
        '<span class="rad-ex__py">' + d.py + "</span></button>";
    }).join("");
    $all(".rad-ex", $("#rd-ex")).forEach(function (b) {
      b.addEventListener("click", function () {
        if (window.CCS_EXPLORER) {
          window.CCS_EXPLORER.open(b.dataset.ch);
          $("#explorer").scrollIntoView({ behavior: prefersReduced ? "auto" : "smooth" });
        }
      });
    });

    var xb = $("#rd-xtr-block");
    if (rd.xtr && rd.xtr.length) {
      xb.hidden = false;
      $("#rd-xtr").innerHTML = rd.xtr.map(function (x) {
        return '<span class="rad-xtr"><span class="zh-inline" lang="zh-Hans">' + x[0] +
          "</span> " + x[1] + " · " + x[2] + "</span>";
      }).join("");
    } else xb.hidden = true;

    $all(".rad-tile").forEach(function (b, i) {
      var on = i === cur;
      b.classList.toggle("is-active", on);
      b.setAttribute("aria-current", on ? "true" : "false");
    });
  }

  function buildWall() {
    $("#rd-wall").innerHTML = RD.map(function (rd, i) {
      return '<button class="rad-tile" type="button" data-i="' + i + '" ' +
        'aria-label="' + (rd.py ? rd.py + " — " : "") + rd.en + '">' +
        '<span class="rad-tile__r" lang="zh-Hans">' + rd.r + "</span>" +
        '<span class="rad-tile__en">' + rd.en.split(/[,—]/)[0].trim() + "</span></button>";
    }).join("");
    $all(".rad-tile").forEach(function (b) {
      b.addEventListener("click", function () {
        cur = +b.dataset.i;
        render();
        var card = document.querySelector("#radicals .rad-card");
        if (card) card.scrollIntoView({ behavior: prefersReduced ? "auto" : "smooth" });
      });
    });
  }

  // API for the explorer: open the radical card for the character's radical glyph
  window.CCS_RADICALS = {
    openFor: function (radicalGlyph) {
      for (var i = 0; i < RD.length; i++) {
        if (RD[i].r === radicalGlyph || RD[i].v === radicalGlyph) {
          cur = i; render(); return;
        }
      }
    }
  };

  function init() {
    if (!$("#rd-wall")) return;
    buildWall();
    render();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
