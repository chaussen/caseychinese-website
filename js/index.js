  // sticky nav border
  const nav = document.getElementById('nav');
  const onScroll = () => nav.classList.toggle('scrolled', window.scrollY > 8);
  document.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  document.getElementById('footYear').textContent = new Date().getFullYear();

  // events: hide ones whose date has passed; show a note if none remain
  (function () {
    const now = new Date();
    let upcoming = 0;
    document.querySelectorAll('.event[data-date]').forEach(ev => {
      if (new Date(ev.dataset.date + 'T23:59:59') < now) ev.hidden = true;
      else upcoming++;
    });
    const empty = document.getElementById('eventsEmpty');
    if (empty && upcoming === 0) empty.hidden = false;
  })();


  // Reveal photos once they load; if a file is missing, the styled placeholder
  // stays visible. Lazy loading is left to the browser via loading="lazy".
  document.querySelectorAll('.photo img').forEach(img => {
    const mark = () => img.classList.add('loaded');
    if (img.complete && img.naturalWidth > 0) mark();
    else img.addEventListener('load', mark, { once: true });
  });

  // contact form — mailto approach (no server needed, works on static hosting).
  // Some devices have no mail app configured, so after the attempt we reveal
  // a fallback: the address plus a button that copies the composed message.
  const contactForm = document.getElementById('contactForm');
  const cfBtn = document.getElementById('cf-btn');
  const cfFallback = document.getElementById('cf-fallback');
  const cfCopy = document.getElementById('cf-copy');
  let cfText = '';
  contactForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const name    = document.getElementById('cf-name').value.trim();
    const email   = document.getElementById('cf-email').value.trim();
    const message = document.getElementById('cf-message').value.trim();
    cfText = 'Name: ' + name + '\nEmail: ' + email + '\n\nMessage:\n' + message;
    const subject = encodeURIComponent('Website enquiry — Casey Foundation Chinese School');
    window.location.href =
      'mailto:office@caseychinese.org?subject=' + subject + '&body=' + encodeURIComponent(cfText);
    cfBtn.innerHTML = 'Opening your email app… <span class="arrow">✓</span>';
    cfBtn.disabled = true;
    setTimeout(() => {
      cfBtn.innerHTML = 'Send message · 发送留言 <span class="arrow">→</span>';
      cfBtn.disabled = false;
      cfFallback.hidden = false;
    }, 1500);
  });
  cfCopy.addEventListener('click', () => {
    const done = () => { cfCopy.textContent = 'Copied ✓ · 已复制'; };
    const legacy = () => {
      const ta = document.createElement('textarea');
      ta.value = cfText; document.body.appendChild(ta);
      ta.select();
      try { if (document.execCommand('copy')) done(); } catch (e) {}
      ta.remove();
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(cfText).then(done, legacy);
    } else legacy();
  });

  // mobile nav
  const toggle = document.getElementById('navToggle');
  const links = document.getElementById('navLinks');
  const closeNav = () => {
    links.classList.remove('open');
    toggle.setAttribute('aria-expanded', 'false');
    document.body.classList.remove('nav-open');
  };
  toggle.addEventListener('click', () => {
    const isOpen = links.classList.toggle('open');
    toggle.setAttribute('aria-expanded', isOpen);
    document.body.classList.toggle('nav-open', isOpen);
  });
  links.querySelectorAll('a').forEach(a => a.addEventListener('click', closeNav));

  // a11y: language tags on Chinese text; aria-hidden on decorative dot bullets
  document.querySelectorAll('.zh, .zh-sans, .zh-para, .zh-title, .zh-title-sm, .zh-name, .zh-note, .zh-sub, .tb-h2cn, .tb-zh, .tb-cn, .zhh, .tb-pband__cn').forEach(el => el.setAttribute('lang', 'zh-Hans'));
  document.querySelectorAll('.dot').forEach(el => el.setAttribute('aria-hidden', 'true'));

  // gallery: cap the wall to a tidy preview, expand on demand.
  // The cap matches the CSS nth-child rule (>10 on desktop, >8 on small screens).
  (function () {
    const gallery = document.getElementById('galleryGrid');
    const foot = document.getElementById('galleryFoot');
    const btn = document.getElementById('galleryToggle');
    if (!gallery || !btn) return;
    const previewCount = () => window.matchMedia('(max-width: 920px)').matches ? 8 : 10;
    const total = gallery.querySelectorAll('.photo').length;

    function sync() {
      const hidden = total - previewCount();
      if (hidden > 0 && gallery.classList.contains('is-collapsed')) {
        foot.hidden = false;
        btn.querySelector('.label').textContent = 'Show all';
        btn.querySelector('.count').textContent = total + ' photos';
      } else if (hidden > 0) {
        foot.hidden = false;
        btn.querySelector('.label').textContent = 'Show less';
        btn.querySelector('.count').textContent = '';
      } else {
        foot.hidden = true;
      }
    }

    btn.addEventListener('click', () => {
      const expanded = gallery.classList.toggle('is-collapsed') === false;
      btn.setAttribute('aria-expanded', String(expanded));
      sync();
    });
    window.addEventListener('resize', sync, { passive: true });
    sync();
  })();
  // Render the four designed book covers for #textbooks Group 01
  (function () {
    const BANDS = [
      { glyph:'朱', py:'zhū',  name:'Cinnabar',  title:[['启','qǐ'],['蒙','méng']], sub:'Foundation',   yr:'Prep – Year 2',  caccent:'oklch(0.555 0.165 33)',  deep:'oklch(0.405 0.135 33)'  },
      { glyph:'青', py:'qīng', name:'Celadon',   title:[['初','chū'],['级','jí']],   sub:'Elementary',   yr:'Year 3 – 4',     caccent:'oklch(0.520 0.085 178)', deep:'oklch(0.395 0.070 180)' },
      { glyph:'靛', py:'diàn', name:'Indigo',    title:[['中','zhōng'],['级','jí']], sub:'Intermediate', yr:'Year 5 – 6',     caccent:'oklch(0.500 0.135 258)', deep:'oklch(0.375 0.115 260)' },
      { glyph:'黛', py:'dài',  name:'Aubergine', title:[['高','gāo'],['级','jí']],   sub:'Senior',       yr:'Year 7 – 10',    caccent:'oklch(0.470 0.130 332)', deep:'oklch(0.360 0.110 333)' },
    ];
    const ruby = (pairs) => pairs.map(([c, p]) => `<ruby>${c}<rt>${p}</rt></ruby>`).join('');
    const shelf = document.querySelector('[data-tb-shelf]');
    if (!shelf) return;
    BANDS.forEach((b, i) => {
      const el = document.createElement('div');
      el.className = 'tb-item';
      el.innerHTML = `
        <div class="tb-book" style="--caccent:${b.caccent};--deep:${b.deep}">
          <div class="book__pages"></div>
          <div class="book__face"><div class="cv">
            <div class="cv__top"><div class="cv__pig">
              <span class="g">${b.glyph}</span>
              <span class="py">${b.py}</span>
              <span class="nm">${b.name}</span>
            </div></div>
            <div class="cv__mid">
              <div class="cv__series">中文课本</div>
              <div class="cv__title">${ruby(b.title)}</div>
              <div class="cv__sub">Band ${i + 1} · ${b.sub}</div>
              <div class="cv__rule">${b.yr}</div>
            </div>
          </div></div>
        </div>
        <div class="tb-cap">
          <div class="cncn">${ruby(b.title)}</div>
          <div class="en">${b.sub}</div>
          <div class="yr">${b.yr}</div>
        </div>`;
      shelf.appendChild(el);
    });
    // apply lang attribute to the dynamically generated Chinese text
    shelf.querySelectorAll('.cncn, .cv__series, .cv__title, .g').forEach(el => el.setAttribute('lang', 'zh-Hans'));
  })();
(function () {
  var DATA = {"你":{"s":["M 272 567 Q 306 613 342 669 Q 370 718 395 743 Q 405 753 400 769 Q 396 782 365 808 Q 337 827 316 828 Q 297 827 305 802 Q 318 769 306 741 Q 267 647 207 560 Q 150 476 72 385 Q 60 375 58 367 Q 54 355 70 358 Q 82 359 109 384 Q 155 421 213 493 Q 226 509 241 527 L 272 567 Z","M 241 527 Q 262 506 258 375 Q 258 374 258 370 Q 254 253 221 135 Q 215 114 224 80 Q 236 44 248 32 Q 267 16 279 44 Q 294 86 294 134 Q 303 420 314 485 Q 321 515 295 543 Q 289 549 272 567 C 251 589 227 553 241 527 Z","M 521 560 Q 561 621 602 708 Q 620 751 638 773 Q 645 786 639 799 Q 633 811 602 830 Q 572 846 554 843 Q 535 839 546 817 Q 561 795 552 757 Q 513 619 407 448 Q 398 436 397 430 Q 394 418 409 423 Q 439 432 503 532 L 521 560 Z","M 503 532 Q 527 510 555 520 Q 795 608 782 549 Q 783 543 743 468 Q 736 458 741 453 Q 745 447 756 459 Q 852 532 894 549 Q 904 552 905 561 Q 906 574 876 592 Q 852 605 828 621 Q 800 637 783 630 Q 686 590 521 560 C 492 555 479 550 503 532 Z","M 568 72 Q 531 81 494 91 Q 482 94 483 86 Q 484 79 494 71 Q 569 7 596 -33 Q 611 -49 626 -36 Q 659 -3 661 82 Q 655 149 655 345 Q 656 382 667 407 Q 676 426 659 439 Q 634 461 604 470 Q 585 477 577 469 Q 571 462 582 447 Q 619 384 603 127 Q 597 82 589 74 Q 582 67 568 72 Z","M 444 320 Q 419 262 385 208 Q 364 180 381 144 Q 388 128 409 139 Q 460 181 468 264 Q 472 295 467 319 Q 463 328 456 328 Q 449 327 444 320 Z","M 738 307 Q 789 249 847 168 Q 860 146 876 139 Q 885 138 893 146 Q 908 159 900 204 Q 891 264 743 338 Q 734 345 731 332 Q 728 319 738 307 Z"],"m":[[[317,812],[342,786],[353,759],[303,663],[249,577],[181,485],[93,386],[68,367]],[[273,558],[274,525],[285,495],[284,441],[273,243],[256,123],[260,41]],[[556,828],[574,817],[595,783],[584,746],[539,640],[481,531],[428,453],[406,431]],[[513,532],[704,585],[796,597],[813,585],[827,563],[798,519],[746,460]],[[586,463],[615,438],[632,412],[627,73],[616,41],[604,30],[558,47],[490,85]],[[455,316],[437,243],[397,151]],[[742,326],[812,265],[856,216],[871,190],[878,154]]]},"好":{"s":["M 330 202 Q 361 175 399 134 Q 415 119 424 118 Q 433 118 439 128 Q 446 138 442 170 Q 435 206 361 247 L 319 270 Q 292 286 258 304 Q 237 314 240 335 Q 261 393 281 453 L 293 492 Q 317 568 337 644 Q 347 690 366 715 Q 379 737 373 750 Q 360 769 313 797 Q 294 810 276 801 Q 263 794 273 778 Q 303 733 247 486 L 236 442 Q 218 373 195 336 Q 185 314 206 296 Q 254 268 294 233 L 330 202 Z","M 294 233 Q 287 226 281 217 Q 250 180 196 143 Q 183 134 165 124 Q 149 114 133 104 Q 120 95 131 92 Q 212 86 327 199 Q 328 200 330 202 L 361 247 Q 406 322 421 385 Q 449 488 463 510 Q 473 526 458 537 Q 416 576 387 569 Q 374 565 378 550 Q 387 531 387 507 L 385 481 Q 384 469 382 455 Q 375 376 319 270 L 294 233 Z","M 387 507 Q 341 501 293 492 L 247 486 Q 183 479 115 468 Q 94 465 61 471 Q 48 471 45 462 Q 41 450 49 441 Q 68 422 96 400 Q 106 396 118 402 Q 190 436 236 442 L 281 453 Q 320 463 362 474 Q 372 478 385 481 C 414 489 417 511 387 507 Z","M 671 521 Q 788 635 822 648 Q 843 655 835 672 Q 831 688 760 725 Q 739 735 716 725 Q 661 703 575 676 Q 553 669 498 669 Q 473 669 482 648 Q 491 635 511 623 Q 544 605 578 627 Q 597 636 691 676 Q 706 682 719 673 Q 732 664 726 649 Q 693 595 655 531 C 640 505 649 500 671 521 Z","M 717 430 Q 702 497 671 521 L 655 531 Q 648 535 640 538 Q 618 547 608 540 Q 595 533 608 519 Q 645 491 653 444 Q 656 434 659 421 L 668 384 Q 701 204 658 103 Q 643 76 607 83 Q 576 89 548 94 Q 536 97 542 85 Q 546 78 564 65 Q 604 31 618 5 Q 628 -14 645 -11 Q 660 -10 687 17 Q 775 107 726 391 L 717 430 Z","M 726 391 Q 783 397 947 397 Q 966 398 971 406 Q 977 416 960 430 Q 909 467 848 454 Q 793 445 717 430 L 659 421 Q 562 409 452 393 Q 431 392 447 375 Q 460 362 478 357 Q 497 351 514 356 Q 586 375 668 384 L 726 391 Z"],"m":[[[282,788],[307,769],[327,733],[264,465],[216,321],[235,298],[386,194],[411,166],[424,133]],[[390,556],[417,530],[424,516],[422,504],[387,361],[338,255],[304,207],[260,165],[206,127],[137,97]],[[59,457],[107,434],[373,491],[380,501]],[[493,656],[517,646],[550,644],[680,692],[706,699],[743,696],[771,669],[765,657],[677,546],[674,535],[663,536]],[[613,530],[637,519],[659,499],[674,474],[687,432],[711,289],[709,166],[692,92],[672,59],[648,41],[551,85]],[[449,384],[504,377],[860,427],[906,426],[960,412]]]},"水":{"s":["M 535 506 Q 538 699 560 762 Q 578 793 520 817 Q 486 836 465 830 Q 447 823 463 799 Q 485 771 486 736 Q 490 697 478 121 Q 477 97 463 88 Q 454 81 432 88 Q 407 94 382 99 Q 348 111 351 100 Q 352 93 373 78 Q 440 24 457 -5 Q 476 -41 493 -42 Q 508 -43 524 -7 Q 543 41 541 117 Q 531 294 534 470 L 535 506 Z","M 154 501 Q 141 501 139 492 Q 138 485 153 477 Q 199 452 227 461 Q 333 489 343 489 Q 359 486 347 456 Q 296 326 249 262 Q 201 190 114 119 Q 99 106 110 103 Q 120 102 141 113 Q 217 153 281 224 Q 342 288 419 454 Q 429 478 441 489 Q 456 501 447 511 Q 437 524 399 537 Q 378 549 336 530 Q 270 509 154 501 Z","M 590 446 Q 630 476 766 584 Q 787 603 814 615 Q 838 627 825 647 Q 809 666 779 681 Q 752 696 738 692 Q 723 691 729 675 Q 735 639 659 553 Q 620 508 577 459 C 557 436 566 428 590 446 Z","M 577 459 Q 555 484 535 506 C 515 528 516 494 534 470 Q 756 161 817 160 Q 898 169 967 175 Q 995 178 996 185 Q 997 192 964 205 Q 810 253 753 295 Q 690 346 590 446 L 577 459 Z"],"m":[[[473,814],[500,795],[521,770],[508,455],[507,91],[485,42],[442,56],[371,91],[369,98],[358,98]],[[147,491],[209,482],[354,512],[381,505],[392,495],[384,459],[353,387],[280,261],[187,160],[113,110]],[[737,682],[750,671],[766,637],[721,583],[591,461],[590,452]],[[539,500],[550,465],[618,387],[729,271],[782,229],[820,207],[990,185]]]},"大":{"s":["M 494 476 Q 542 485 795 501 Q 817 502 822 512 Q 826 525 808 540 Q 750 580 707 569 Q 631 550 500 522 L 436 509 Q 331 490 213 469 Q 189 465 208 447 Q 241 420 294 432 Q 357 453 431 465 L 494 476 Z","M 487 437 Q 491 456 494 476 L 500 522 Q 510 711 528 763 Q 534 776 523 786 Q 501 805 459 822 Q 434 832 414 825 Q 390 816 410 796 Q 444 762 444 726 Q 445 602 436 509 L 431 465 Q 398 275 310 179 Q 303 173 297 166 Q 251 118 148 55 Q 133 48 130 43 Q 124 36 144 34 Q 195 34 300 104 Q 385 173 414 218 Q 444 266 480 396 L 487 437 Z","M 480 396 Q 501 357 575 245 Q 657 124 718 56 Q 746 22 774 22 Q 856 28 928 32 Q 959 33 959 41 Q 960 50 927 66 Q 753 144 719 174 Q 614 267 500 419 Q 493 429 487 437 C 469 461 465 422 480 396 Z"],"m":[[[210,458],[268,453],[514,503],[719,534],[770,529],[810,517]],[[416,810],[444,799],[482,759],[469,518],[448,394],[426,320],[386,231],[361,196],[307,140],[202,67],[138,41]],[[486,430],[500,393],[576,284],[660,182],[722,118],[774,77],[953,42]]]}};
  var ORDER = ["你", "好", "水", "大"];
  var host = document.getElementById('featWriter');
  var cycleEl = document.getElementById('featCycle');
  if (!host || !cycleEl) return;
  var idx = 0, timers = [], dwell = null, inkEls = [], started = false;
  var prefersReduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

  function gridSVG() {
    return '<svg viewBox="0 0 1024 1024" aria-hidden="true">' +
      '<rect x="3" y="3" width="1018" height="1018" rx="10" fill="none" class="fw-frame"/>' +
      '<line class="fw-dash" x1="512" y1="14" x2="512" y2="1010"/>' +
      '<line class="fw-dash" x1="14" y1="512" x2="1010" y2="512"/>' +
      '<line class="fw-diag" x1="40" y1="40" x2="984" y2="984"/>' +
      '<line class="fw-diag" x1="984" y1="40" x2="40" y2="984"/></svg>';
  }
  function mpath(m) { return 'M ' + m.map(function (p) { return p[0] + ' ' + p[1]; }).join(' L '); }
  function build(ch) {
    var d = DATA[ch], defs = '', gh = '', ink = '';
    for (var i = 0; i < d.s.length; i++) {
      defs += '<clipPath id="fcp' + i + '"><path d="' + d.s[i] + '"/></clipPath>';
      gh += '<path class="fw-ghost" d="' + d.s[i] + '"/>';
      ink += '<path class="fw-ink" d="' + mpath(d.m[i]) + '" fill="none" stroke="var(--red-deep)" ' +
        'stroke-width="166" stroke-linecap="round" stroke-linejoin="round" clip-path="url(#fcp' + i + ')"/>';
    }
    host.innerHTML = gridSVG() + '<svg viewBox="0 0 1024 1024"><defs>' + defs + '</defs>' +
      '<g transform="translate(0,900) scale(1,-1)">' + gh + ink + '</g></svg>';
    inkEls = [].slice.call(host.querySelectorAll('.fw-ink'));
    inkEls.forEach(function (p) { var L = p.getTotalLength(); p.dataset.len = L; p.style.strokeDasharray = L + 'px'; p.style.strokeDashoffset = L + 'px'; });
  }
  function clearT() { timers.forEach(clearTimeout); timers = []; if (dwell) clearTimeout(dwell); }
  function showAll() {
    clearT();
    inkEls.forEach(function (p) { p.style.transition = 'none'; p.style.strokeDashoffset = '0px'; });
  }
  function chips() {
    cycleEl.innerHTML = ORDER.map(function (c, i) {
      return '<button class="feat-chip' + (i === idx ? ' on' : '') + '" data-i="' + i + '" type="button" ' +
        'aria-pressed="' + (i === idx) + '" lang="zh-Hans" aria-label="Watch ' + c + ' written stroke by stroke">' + c + '</button>';
    }).join('');
  }
  function setChip() {
    [].slice.call(cycleEl.children).forEach(function (b, i) {
      var on = i === idx;
      b.classList.toggle('on', on);
      b.setAttribute('aria-pressed', on);
    });
  }
  function play() {
    var i = 0;
    (function step() {
      if (i >= inkEls.length) { if (!prefersReduced) dwell = setTimeout(next, 1700); return; }
      var p = inkEls[i], L = +p.dataset.len;
      var dur = Math.max(360, Math.min(820, 240 + L * 0.32));
      // CSS transition instead of WAAPI: stroke-dashoffset keyframes are
      // unreliable cross-browser; px-unit transitions work everywhere.
      void p.getBoundingClientRect();
      p.style.transition = 'stroke-dashoffset ' + dur + 'ms cubic-bezier(.45,.05,.3,1)';
      p.style.strokeDashoffset = '0px';
      i++; timers.push(setTimeout(step, dur + 90));
    })();
  }
  function show(n) { clearT(); idx = (n + ORDER.length) % ORDER.length; build(ORDER[idx]); setChip(); play(); }
  function next() { show(idx + 1); }

  // Under prefers-reduced-motion nothing plays on its own: the character is
  // shown fully drawn, and animation only runs on an explicit tap/click
  // (the strokes are the lesson content, matching learn/explorer.js policy).
  function start() { if (started) return; started = true; if (prefersReduced) { showAll(); return; } show(idx); }
  chips();
  build(ORDER[idx]);
  cycleEl.addEventListener('click', function (e) {
    var b = e.target.closest('.feat-chip'); if (!b) return; started = true; show(+b.dataset.i);
  });
  host.addEventListener('click', function () { started = true; show(idx); });
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (en) {
      if (en.isIntersecting) { start(); }
      else { started = false; clearT(); }
    });
  }, { threshold: 0.2 });
  io.observe(host);
  setTimeout(function () { var r = host.getBoundingClientRect(); if (r.top < innerHeight && r.bottom > 0) start(); }, 1200);
})();