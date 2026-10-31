/* GURO PSP — interaction & motion layer (GSAP + ScrollTrigger, native scroll) */
(function () {
  'use strict';
  var html = document.documentElement;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var curtain = $('#curtain');
  var yr = $('#yr'); if (yr) yr.textContent = new Date().getFullYear();

  /* ---------- Telegram links: prefilled message + partner ref ---------- */
  (function () {
    var ref = null;
    try {
      var r = localStorage.getItem('guro_ref'), t = +localStorage.getItem('guro_ref_t') || 0;
      if (r && Date.now() - t < 7776000000) ref = r;
    } catch (e) {}
    /* If a bot username is set in <html data-tg-bot>, every CTA opens the bot with a start payload
       (source, language, partner) so the lead is tracked automatically. Otherwise: personal chat with prefilled text. */
    var bot = html.dataset.tgBot, user = html.dataset.tgUser || 'GuroArtem', href;
    if (bot) {
      var payload = (html.dataset.tgSrc ? 'site-' + html.dataset.tgSrc : 'site') + '_' + html.lang + (ref ? '_ref_' + ref : '');
      href = 'https://t.me/' + bot + '?start=' + encodeURIComponent(payload.slice(0, 64));
    } else {
      href = 'https://t.me/' + user + '?text=' + encodeURIComponent(html.dataset.tgMsg + (ref ? html.dataset.tgRef + ref : ''));
    }
    $$('[data-tg]').forEach(function (a) { a.href = href; });
  })();

  /* ---------- nav: burger ---------- */
  var nav = $('#nav'), burger = $('#burger');
  function setMenu(open) {
    nav.classList.toggle('is-open', open);
    burger.setAttribute('aria-expanded', open);
    burger.setAttribute('aria-label', open ? burger.dataset.close : burger.dataset.open);
  }
  burger.addEventListener('click', function () { setMenu(!nav.classList.contains('is-open')); });

  /* ---------- live log + approval rate (driven by the 3D scene) ---------- */
  (function () {
    var log = $('#log'), rateEl = $('#rate'), bar = $('#bar');
    if (!log) return;
    var rate = 74;
    function add(amt, info, st, cls) {
      var li = document.createElement('li');
      li.innerHTML = '<span></span><span class="info"></span><span></span>';
      li.children[0].textContent = amt; li.children[1].textContent = info;
      li.children[2].textContent = st; li.children[2].className = cls;
      log.insertBefore(li, log.firstChild);
      while (log.children.length > 4) log.removeChild(log.lastChild);
    }
    function bump() {
      rate += ((91 + Math.random() * 3) - rate) * 0.14;
      rateEl.textContent = rate.toFixed(1) + '%'; bar.style.width = rate + '%';
    }
    add('€100', 'Visa · DE → PSP A', 'approved', 'ok');
    add('C$200', 'Mastercard · CA · 05 do not honor → PSP A', 'cascade ✓', 'cas');
    add('€50', 'Trustly · FI → PSP C', 'approved', 'ok');
    if (reduce) { rateEl.textContent = '92.4%'; bar.style.width = '92.4%'; return; }

    var gotScene = false;
    window.addEventListener('guro:ready', function () { gotScene = true; });
    window.addEventListener('guro:tx', function (e) { var d = e.detail; add(d.amt, d.info, d.status, d.cls); bump(); });
    /* fallback ticker if WebGL is unavailable */
    setTimeout(function () {
      if (gotScene) return;  // the 3D scene is loaded lazily; it takes over the log as soon as it is ready
      var amounts = ['€50', '€100', '€200', '€300', 'C$100', 'A$200'], methods = ['Visa', 'Mastercard', 'Apple Pay', 'Interac', 'Trustly'], geos = ['CA', 'DE', 'AU', 'NZ', 'FI'];
      var pick = function (a) { return a[Math.floor(Math.random() * a.length)]; };
      (function loop() { setTimeout(function () {
        if (gotScene) return;
        if (!document.hidden) { var c = Math.random() < 0.35; add(pick(amounts), pick(methods) + ' · ' + pick(geos) + (c ? ' · 05 do not honor → PSP B' : ' → PSP A'), c ? 'cascade ✓' : 'approved', c ? 'cas' : 'ok'); bump(); }
        loop(); }, 1200 + Math.random() * 700); })();
    }, 2500);
  })();

  /* ---------- language switch with quick curtain ---------- */
  $$('.lang').forEach(function (a) {
    a.addEventListener('click', function (e) {
      try { localStorage.setItem('guro_lang', a.dataset.set); } catch (err) {}
      if (reduce || !window.gsap || e.metaKey || e.ctrlKey) return;
      e.preventDefault();
      curtain.style.visibility = 'visible';
      gsap.fromTo(curtain, { clipPath: 'inset(100% 0 0 0)' }, { clipPath: 'inset(0% 0 0 0)', duration: 0.4, ease: 'power3.inOut', onComplete: function () { location.href = a.href; } });
    });
  });
  window.addEventListener('pageshow', function (e) { if (e.persisted && curtain) curtain.style.visibility = 'hidden'; });

  /* ---------- anchors: native smooth scroll ---------- */
  $$('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var id = a.getAttribute('href'); if (id.length < 2) return;
      var t = document.querySelector(id); if (!t) return;
      e.preventDefault(); setMenu(false);
      window.scrollTo({ top: id === '#top' ? 0 : t.getBoundingClientRect().top + window.pageYOffset - 10, behavior: reduce ? 'auto' : 'smooth' });
    });
  });

  /* ---------- no GSAP? show everything and stop ---------- */
  if (!window.gsap || !window.ScrollTrigger) { html.classList.add('no-motion'); return; }
  gsap.registerPlugin(ScrollTrigger);

  /* ---------- text splitting ---------- */
  function splitChars(el) {
    var text = el.textContent.trim(); el.setAttribute('aria-label', text); el.textContent = '';
    var chars = [];
    text.split(/\s+/).forEach(function (word, i, arr) {
      var w = document.createElement('span'); w.className = 'w'; w.setAttribute('aria-hidden', 'true');
      Array.from(word).forEach(function (ch) { var c = document.createElement('span'); c.className = 'c'; c.textContent = ch; w.appendChild(c); chars.push(c); });
      el.appendChild(w); if (i < arr.length - 1) el.appendChild(document.createTextNode(' '));
    });
    return chars;
  }
  function splitWords(el, masked) {
    var text = el.textContent.trim(); el.setAttribute('aria-label', text); el.textContent = '';
    var words = [];
    text.split(/\s+/).forEach(function (word, i, arr) {
      var outer = document.createElement('span'); outer.setAttribute('aria-hidden', 'true');
      if (masked) { outer.className = 'wm'; var inner = document.createElement('span'); inner.className = 'wi'; inner.textContent = word; outer.appendChild(inner); words.push(inner); }
      else { outer.className = 'sw'; outer.textContent = word; words.push(outer); }
      el.appendChild(outer); if (i < arr.length - 1) el.appendChild(document.createTextNode(' '));
    });
    return words;
  }
  var heroChars = [];
  $$('#heroTitle [data-chars]').forEach(function (ln) { heroChars = heroChars.concat(splitChars(ln)); });
  var headWords = $$('[data-words]').map(function (el) { return { el: el, words: splitWords(el, true) }; });
  var scrubWords = $$('[data-scrub]').map(function (el) { return { el: el, words: splitWords(el, false) }; });

  if (reduce) {
    html.classList.add('no-motion');
    $$('.pcard, .steps li').forEach(function (c) { c.classList.add('is-on'); });
    $$('.steps-rail i, #pathFill').forEach(function (i) { i.style.transform = 'none'; });
    return;
  }

  /* ---------- nav shrink ---------- */
  ScrollTrigger.create({ start: 40, end: 'max', onToggle: function (s) { nav.classList.toggle('is-scrolled', s.isActive); } });

  /* ---------- intro: fast and crisp ---------- */
  gsap.set(heroChars, { yPercent: 110, opacity: 0 });
  gsap.set('#heroTitle .ln-metal .metal', { clipPath: 'inset(0 100% 0 0)' });
  gsap.set('[data-intro]', { y: 24, opacity: 0 });
  html.classList.add('motion-ready');
  gsap.timeline({ delay: 0.05 })
    .to(heroChars, { yPercent: 0, opacity: 1, duration: 0.6, ease: 'power4.out', stagger: 0.012 }, 0)
    .to('#heroTitle .ln-metal .metal', { clipPath: 'inset(0 0% 0 0)', duration: 0.7, ease: 'power3.out' }, 0.25)
    .to('[data-intro]', { y: 0, opacity: 1, duration: 0.6, ease: 'power3.out', stagger: 0.06 }, 0.2);

  /* ---------- section headings: masked word rise ---------- */
  headWords.forEach(function (h) {
    gsap.from(h.words, { yPercent: 110, duration: 0.65, ease: 'power4.out', stagger: 0.035, scrollTrigger: { trigger: h.el, start: 'top 90%' } });
  });

  /* ---------- generic reveal ---------- */
  gsap.set('[data-reveal]', { y: 28, opacity: 0 });
  ScrollTrigger.batch('[data-reveal]', {
    start: 'top 92%', once: true,
    onEnter: function (els) { gsap.to(els, { y: 0, opacity: 1, duration: 0.6, ease: 'power3.out', stagger: 0.06 }); }
  });

  /* ---------- scrubbed paragraph ---------- */
  scrubWords.forEach(function (s) {
    gsap.to(s.words, { opacity: 1, ease: 'none', stagger: 0.08, scrollTrigger: { trigger: s.el, start: 'top 85%', end: 'bottom 55%', scrub: true } });
  });

  /* ---------- count-ups ---------- */
  $$('[data-count]').forEach(function (el) {
    var end = +el.dataset.count, o = { v: 0 }; el.textContent = '0';
    ScrollTrigger.create({ trigger: el, start: 'top 95%', once: true, onEnter: function () {
      gsap.to(o, { v: end, duration: 1, ease: 'power3.out', onUpdate: function () { el.textContent = Math.round(o.v); } });
    } });
  });

  /* ---------- responsive scenes ---------- */
  var mm = gsap.matchMedia();
  mm.add('(min-width: 1101px)', function () {
    var track = $('#pathTrack'), fill = $('#pathFill'), cards = track ? $$('.pcard', track) : [];
    if (track) {
      var dist = function () { return Math.max(0, track.scrollWidth - window.innerWidth); };
      var hTween = gsap.to(track, {
        x: function () { return -dist(); }, ease: 'none',
        scrollTrigger: { trigger: '.path-pin', start: 'top top', end: function () { return '+=' + dist(); }, pin: true, scrub: true, invalidateOnRefresh: true,
          onUpdate: function (s) { gsap.set(fill, { scaleX: s.progress }); } }
      });
      cards.forEach(function (c) {
        ScrollTrigger.create({ trigger: c, containerAnimation: hTween, start: 'left 75%', onEnter: function () { c.classList.add('is-on'); }, onLeaveBack: function () { c.classList.remove('is-on'); } });
      });
    }

    var sc = $$('.scard');
    sc.forEach(function (c, i) {
      c.style.position = 'sticky'; c.style.top = 'calc(12vh + ' + (i * 26) + 'px)';
      if (i === sc.length - 1) return;
      gsap.to(c, { scale: 0.92 + i * 0.02, '--dim': 0.55, ease: 'none', scrollTrigger: { trigger: sc[i + 1], start: 'top bottom', end: 'top 25%', scrub: true } });
    });

    var steps = $$('.steps li');
    if (steps.length) gsap.to('.steps-rail i', { scaleX: 1, ease: 'none', scrollTrigger: { trigger: '#steps', start: 'top 80%', end: 'bottom 60%', scrub: true,
      onUpdate: function (s) { steps.forEach(function (li, i) { li.classList.toggle('is-on', s.progress >= i / (steps.length - 1) - 0.02); }); } } });

    return function () { $$('.scard').forEach(function (c) { c.style.position = ''; c.style.top = ''; }); };
  });
  mm.add('(max-width: 1100px)', function () {
    $$('.pcard, .scard').forEach(function (c) { gsap.from(c, { y: 30, opacity: 0, duration: 0.6, ease: 'power3.out', scrollTrigger: { trigger: c, start: 'top 92%' } }); });
    $$('.pcard, .steps li').forEach(function (c) { c.classList.add('is-on'); });
  });

  /* ---------- desktop pointer interactions ---------- */
  if (finePointer) {
    html.classList.add('has-cursor');
    var cur = $('#cursor'), ring = $('.cursor-ring', cur), dot = $('.cursor-dot', cur), label = $('.cursor-label', cur);
    var rx = gsap.quickTo(ring, 'x', { duration: 0.18, ease: 'power3' }), ry = gsap.quickTo(ring, 'y', { duration: 0.18, ease: 'power3' });
    window.addEventListener('pointermove', function (e) {
      if (!cur.classList.contains('is-live')) { gsap.set([ring, dot], { x: e.clientX, y: e.clientY }); cur.classList.add('is-live'); }
      rx(e.clientX); ry(e.clientY); gsap.set(dot, { x: e.clientX, y: e.clientY });
    }, { passive: true });
    window.addEventListener('pointerdown', function () { cur.classList.add('is-down'); });
    window.addEventListener('pointerup', function () { cur.classList.remove('is-down'); });
    document.addEventListener('mouseleave', function () { cur.classList.remove('is-live'); });
    $$('a, button, .tilt').forEach(function (el) {
      el.addEventListener('mouseenter', function () { var l = el.dataset.cursor; if (l) { label.textContent = l; cur.classList.add('is-label'); } else cur.classList.add('is-hover'); });
      el.addEventListener('mouseleave', function () { cur.classList.remove('is-label', 'is-hover'); });
    });

    $$('.magnetic').forEach(function (el) {
      var inner = el.firstElementChild;
      var xTo = gsap.quickTo(el, 'x', { duration: 0.35, ease: 'power3' }), yTo = gsap.quickTo(el, 'y', { duration: 0.35, ease: 'power3' });
      var ixTo = gsap.quickTo(inner, 'x', { duration: 0.35, ease: 'power3' }), iyTo = gsap.quickTo(inner, 'y', { duration: 0.35, ease: 'power3' });
      function origin(e) { var r = el.getBoundingClientRect(); el.style.setProperty('--x', (e.clientX - r.left) + 'px'); el.style.setProperty('--y', (e.clientY - r.top) + 'px'); }
      el.addEventListener('mouseenter', origin);
      el.addEventListener('mousemove', function (e) {
        var r = el.getBoundingClientRect(), mx = e.clientX - r.left - r.width / 2, my = e.clientY - r.top - r.height / 2;
        var k = el.classList.contains('btn-xl') ? 0.35 : 0.28;
        xTo(mx * k); yTo(my * k); ixTo(mx * 0.1); iyTo(my * 0.1);
      });
      el.addEventListener('mouseleave', function (e) { origin(e); gsap.to([el, inner], { x: 0, y: 0, duration: 0.7, ease: 'elastic.out(1, 0.4)', overwrite: true }); });
    });

    $$('.tilt').forEach(function (el) {
      var rxTo = gsap.quickTo(el, 'rotationX', { duration: 0.4, ease: 'power3' }), ryTo = gsap.quickTo(el, 'rotationY', { duration: 0.4, ease: 'power3' });
      gsap.set(el, { transformPerspective: 900 });
      el.addEventListener('mousemove', function (e) {
        var r = el.getBoundingClientRect(), px = (e.clientX - r.left) / r.width, py = (e.clientY - r.top) / r.height;
        el.style.setProperty('--mx', (px * 100) + '%'); el.style.setProperty('--my', (py * 100) + '%');
        ryTo((px - 0.5) * 8); rxTo((0.5 - py) * 6);
      });
      el.addEventListener('mouseleave', function () { rxTo(0); ryTo(0); });
    });
  }

  window.addEventListener('load', function () { ScrollTrigger.refresh(); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { ScrollTrigger.refresh(); });
})();
