/* GURO PSP — 3D routing diagram.
   Deposits leave the cashier, pass the smart router and land at a PSP.
   Declines turn red, return to the router and cascade to another PSP. */
(function () {
'use strict';
var THREE = window.THREE;

const host = document.getElementById('scene');
const canvas = document.getElementById('flow');
const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
// weak or touch devices: cheaper rendering (no MSAA, lower pixel ratio, 30 fps)
const lite = window.matchMedia('(pointer: coarse)').matches || (navigator.hardwareConcurrency || 8) <= 4 ||
  (navigator.deviceMemory || 8) <= 4 || !!(navigator.connection && navigator.connection.saveData);

// WebGL with a real GPU only: software renderers (VMs, no-GPU PCs, headless) get the light SVG version instead
function webglOK() {
  try {
    const c = document.createElement('canvas'), gl = c.getContext('webgl2') || c.getContext('webgl');
    if (!gl) return false;
    const ext = gl.getExtension('WEBGL_debug_renderer_info');
    const r = ext ? String(gl.getParameter(ext.UNMASKED_RENDERER_WEBGL)) : '';
    const lose = gl.getExtension('WEBGL_lose_context'); if (lose) lose.loseContext();
    return !/swiftshader|llvmpipe|softpipe|software|basic render/i.test(r);
  } catch (e) { return false; }
}
var ok = false;
if (host && canvas && THREE && webglOK()) {
  try { init(); ok = true; } catch (err) { console.error('[guro] 3D scene failed', err); }
}
if (host && !ok) fallback2D();

function init() {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: !lite, alpha: true, powerPreference: lite ? 'low-power' : 'high-performance' });
  renderer.setClearColor(0x000000, 0);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(24, 1, 0.1, 80);
  const world = new THREE.Group();
  scene.add(world);

  const C = {
    lime: new THREE.Color('#d9ff3f'), mint: new THREE.Color('#7cf0c4'), red: new THREE.Color('#ff5a4c'),
    wire: new THREE.Color('#2a323c'), edge: new THREE.Color('#3a4450'), white: new THREE.Color('#f2ffd0')
  };

  /* ---------- lights ---------- */
  scene.add(new THREE.AmbientLight(0xffffff, 0.55));
  const key = new THREE.DirectionalLight(0xffffff, 1.6); key.position.set(-3, 6, 4); scene.add(key);
  const routerLight = new THREE.PointLight(0xd9ff3f, 6, 3.2, 2); routerLight.position.set(0, 0.7, 0); world.add(routerLight);

  /* ---------- floor grid ---------- */
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(12, 8), new THREE.ShaderMaterial({
    transparent: true, depthWrite: false,
    vertexShader: 'varying vec2 vP; void main(){ vP = position.xy; gl_Position = projectionMatrix*modelViewMatrix*vec4(position,1.0); }',
    fragmentShader: `varying vec2 vP;
      float line(float v, float w){ float f = abs(fract(v) - 0.5); return smoothstep(0.5 - w, 0.5, f); }
      void main(){
        vec2 g = vP * 2.5;
        float l = max(line(g.x, 0.02), line(g.y, 0.02));
        float fade = 1.0 - smoothstep(1.5, 4.8, length(vP * vec2(0.75, 1.0)));
        gl_FragColor = vec4(vec3(0.55, 0.65, 0.7), l * 0.12 * fade);
      }`
  }));
  floor.rotation.x = -Math.PI / 2; floor.position.y = -0.002; world.add(floor);

  /* ---------- nodes ---------- */
  const H = 0.16, R = 0.09;
  function rrShape(w, d, r) {
    const s = new THREE.Shape(), x = -w / 2, y = -d / 2;
    s.moveTo(x + r, y); s.lineTo(x + w - r, y); s.quadraticCurveTo(x + w, y, x + w, y + r);
    s.lineTo(x + w, y + d - r); s.quadraticCurveTo(x + w, y + d, x + w - r, y + d);
    s.lineTo(x + r, y + d); s.quadraticCurveTo(x, y + d, x, y + d - r);
    s.lineTo(x, y + r); s.quadraticCurveTo(x, y, x + r, y);
    return s;
  }
  const NODES = {
    cash:   { p: new THREE.Vector3(-2.15, 0, 0),    w: 1.05, d: 0.66 },
    router: { p: new THREE.Vector3(0, 0, 0),        w: 1.05, d: 0.66, router: true },
    a:      { p: new THREE.Vector3(2.15, 0, -1.08), w: 1.05, d: 0.6 },
    b:      { p: new THREE.Vector3(2.15, 0, 0),     w: 1.05, d: 0.6 },
    c:      { p: new THREE.Vector3(2.15, 0, 1.08),  w: 1.05, d: 0.6 }
  };
  const bodyMat = new THREE.MeshStandardMaterial({ color: 0x14181e, metalness: 0.55, roughness: 0.38 });
  Object.keys(NODES).forEach((k) => {
    const n = NODES[k];
    const shape = rrShape(n.w, n.d, R);
    const geo = new THREE.ExtrudeGeometry(shape, { depth: H, bevelEnabled: true, bevelThickness: 0.015, bevelSize: 0.015, bevelSegments: 3, curveSegments: 10 });
    geo.rotateX(-Math.PI / 2);
    const body = new THREE.Mesh(geo, bodyMat);
    body.position.copy(n.p);
    world.add(body);
    // top outline
    const pts = shape.getPoints(24).map(v => new THREE.Vector3(v.x, 0, -v.y));
    const outlineMat = new THREE.LineBasicMaterial({ color: n.router ? C.lime : C.edge, transparent: true, opacity: n.router ? 0.95 : 0.9 });
    const outline = new THREE.LineLoop(new THREE.BufferGeometry().setFromPoints(pts), outlineMat);
    outline.position.set(n.p.x, H + 0.017, n.p.z);
    world.add(outline);
    // floor glow under the node
    const glowMat = new THREE.MeshBasicMaterial({ color: n.router ? C.lime : C.mint, transparent: true, opacity: n.router ? 0.16 : 0, blending: THREE.AdditiveBlending, depthWrite: false });
    const glow = new THREE.Mesh(new THREE.ShapeGeometry(rrShape(n.w + 0.3, n.d + 0.3, 0.22)), glowMat);
    glow.rotation.x = -Math.PI / 2; glow.position.set(n.p.x, 0.001, n.p.z);
    world.add(glow);
    n.outline = outlineMat; n.glow = glowMat; n.flash = 0; n.flashColor = C.mint.clone();
    n.anchor = new THREE.Vector3(n.p.x, H + 0.02, n.p.z);
  });

  /* router ring */
  const ringMat = new THREE.MeshBasicMaterial({ color: C.lime, transparent: true, opacity: 0.8, blending: THREE.AdditiveBlending, depthWrite: false });
  const ring = new THREE.Mesh(new THREE.TorusGeometry(0.78, 0.006, 6, 120, Math.PI * 1.35), ringMat);
  ring.rotation.x = -Math.PI / 2; ring.position.set(0, 0.02, 0); world.add(ring);
  const ring2 = new THREE.Mesh(new THREE.TorusGeometry(0.88, 0.004, 6, 120, Math.PI * 0.6), ringMat.clone());
  ring2.material.opacity = 0.4; ring2.rotation.x = -Math.PI / 2; ring2.position.set(0, 0.02, 0); world.add(ring2);
  let ringBoost = 0;

  /* ---------- wires ---------- */
  const Y = 0.08;
  function wire(curve) {
    const base = new THREE.Mesh(new THREE.TubeGeometry(curve, 64, 0.014, 8, false), new THREE.MeshBasicMaterial({ color: C.wire }));
    const hotMat = new THREE.MeshBasicMaterial({ color: C.lime, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false });
    const hot = new THREE.Mesh(new THREE.TubeGeometry(curve, 64, 0.03, 8, false), hotMat);
    world.add(base, hot);
    return { curve, hot: hotMat, heat: 0, color: C.lime.clone() };
  }
  const inX = NODES.cash.p.x + NODES.cash.w / 2 + 0.02, rIn = -NODES.router.w / 2 - 0.02, rOut = NODES.router.w / 2 + 0.02, pIn = NODES.b.p.x - NODES.b.w / 2 - 0.02;
  const W = {
    in: wire(new THREE.LineCurve3(new THREE.Vector3(inX, Y, 0), new THREE.Vector3(rIn, Y, 0))),
    a: wire(new THREE.CubicBezierCurve3(new THREE.Vector3(rOut, Y, 0), new THREE.Vector3(1.15, Y, 0), new THREE.Vector3(0.95, Y, NODES.a.p.z), new THREE.Vector3(pIn, Y, NODES.a.p.z))),
    b: wire(new THREE.LineCurve3(new THREE.Vector3(rOut, Y, 0), new THREE.Vector3(pIn, Y, 0))),
    c: wire(new THREE.CubicBezierCurve3(new THREE.Vector3(rOut, Y, 0), new THREE.Vector3(1.15, Y, 0), new THREE.Vector3(0.95, Y, NODES.c.p.z), new THREE.Vector3(pIn, Y, NODES.c.p.z)))
  };

  /* ---------- pulses ---------- */
  const glowTex = (() => {
    const c = document.createElement('canvas'); c.width = c.height = 64;
    const g = c.getContext('2d'), gr = g.createRadialGradient(32, 32, 0, 32, 32, 32);
    gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.25, 'rgba(255,255,255,.55)'); gr.addColorStop(1, 'rgba(255,255,255,0)');
    g.fillStyle = gr; g.fillRect(0, 0, 64, 64);
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
  })();
  const coreGeo = new THREE.SphereGeometry(0.042, 16, 12);
  const pool = [];
  function makePulse() {
    const core = new THREE.Mesh(coreGeo, new THREE.MeshBasicMaterial({ color: C.white }));
    const halo = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex, color: C.lime, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false }));
    halo.scale.setScalar(0.42);
    const trail = [];
    for (let i = 0; i < 5; i++) {
      const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex, color: C.lime, transparent: true, opacity: 0.5 - i * 0.09, blending: THREE.AdditiveBlending, depthWrite: false }));
      s.scale.setScalar(0.2 - i * 0.025); trail.push(s); world.add(s);
    }
    world.add(core, halo);
    return { core, halo, trail, active: false };
  }
  for (let i = 0; i < 10; i++) pool.push(makePulse());
  function setPulseColor(p, col) { p.halo.material.color.copy(col); p.trail.forEach(s => s.material.color.copy(col)); p.core.material.color.copy(col).lerp(C.white, 0.55); }
  function showPulse(p, on) { p.core.visible = p.halo.visible = on; p.trail.forEach(s => s.visible = on); }
  pool.forEach(p => showPulse(p, false));

  /* ---------- bursts on the floor ---------- */
  const bursts = [];
  for (let i = 0; i < 8; i++) {
    const m = new THREE.Mesh(new THREE.RingGeometry(0.3, 0.33, 64), new THREE.MeshBasicMaterial({ color: C.mint, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide }));
    m.rotation.x = -Math.PI / 2; m.visible = false; world.add(m);
    bursts.push({ m, t: 1 });
  }
  function burst(node, col) {
    const b = bursts.find(x => x.t >= 1) || bursts[0];
    b.t = 0; b.m.visible = true; b.m.material.color.copy(col); b.m.position.set(node.p.x, 0.01, node.p.z);
  }

  /* ---------- HTML labels + fx chips ---------- */
  const labels = {};
  host.querySelectorAll('[data-node]').forEach(el => { labels[el.dataset.node] = el; });
  const fxLayer = document.getElementById('fx');
  const v = new THREE.Vector3();
  function toScreen(vec) {
    v.copy(vec).applyMatrix4(world.matrixWorld).project(camera);
    return { x: (v.x * 0.5 + 0.5) * cw, y: (-v.y * 0.5 + 0.5) * ch };
  }
  function chip(nodeKey, text, cls) {
    if (!fxLayer) return;
    const s = toScreen(NODES[nodeKey].anchor);
    const el = document.createElement('span');
    el.className = 'fxchip ' + cls; el.textContent = text;
    el.style.left = s.x + 'px'; el.style.top = (s.y - 46) + 'px';
    fxLayer.appendChild(el);
    setTimeout(() => el.remove(), 1100);
  }
  function flashNode(key, col, cls) {
    const n = NODES[key]; n.flash = 1; n.flashColor.copy(col);
    const el = labels[key];
    if (el) { el.classList.remove('ok', 'bad'); void el.offsetWidth; el.classList.add(cls); clearTimeout(el._t); el._t = setTimeout(() => el.classList.remove(cls), 700); }
  }

  /* ---------- transactions ---------- */
  const amounts = ['€50', '€100', '€150', '€200', '€300', '€500', 'C$100', 'A$200', 'NZ$150'];
  const methods = ['Visa', 'Mastercard', 'Apple Pay', 'Interac', 'Trustly', 'Google Pay'];
  const geos = ['CA', 'DE', 'AU', 'NZ', 'FI', 'IE', 'AT'];
  const codes = ['05 do not honor', '51 insufficient', '3DS timeout', '62 restricted'];
  const pick = a => a[(Math.random() * a.length) | 0];
  const SPEED = { in: 0.5, route: 0.55, back: 0.38, retry: 0.55 };
  const txs = [];

  function spawn() {
    const p = pool.find(x => !x.active); if (!p) return;
    const m = pick(methods), g = pick(geos);
    const target = m === 'Trustly' ? 'c' : (g === 'CA' ? 'b' : 'a');
    const alt = target === 'b' ? 'a' : 'b';
    const fail = Math.random() < 0.32;
    p.active = true; showPulse(p, true); setPulseColor(p, C.lime);
    p.hist = [];
    txs.push({ p, stage: 'in', t: 0, target, alt, fail, amt: pick(amounts), m, g, code: pick(codes) });
  }
  function emit(tx, cascade) {
    const info = cascade ? `${tx.m} · ${tx.g} · ${tx.code} → PSP ${tx.alt.toUpperCase()}` : `${tx.m} · ${tx.g} → PSP ${tx.target.toUpperCase()}`;
    window.dispatchEvent(new CustomEvent('guro:tx', { detail: { amt: tx.amt, info, status: cascade ? 'cascade ✓' : 'approved', cls: cascade ? 'cas' : 'ok' } }));
  }
  function pathFor(tx) {
    if (tx.stage === 'in') return { w: W.in, rev: false };
    if (tx.stage === 'route') return { w: W[tx.target], rev: false };
    if (tx.stage === 'back') return { w: W[tx.target], rev: true };
    return { w: W[tx.alt], rev: false };
  }
  const ease = t => t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
  const tmp = new THREE.Vector3();

  function step(dt) {
    for (let i = txs.length - 1; i >= 0; i--) {
      const tx = txs[i], p = tx.p;
      tx.t += dt / SPEED[tx.stage];
      const { w, rev } = pathFor(tx);
      w.heat = 1; w.color.copy(tx.stage === 'back' ? C.red : tx.stage === 'retry' ? C.mint : C.lime);
      const k = Math.min(1, tx.t), u = ease(k);
      w.curve.getPointAt(rev ? 1 - u : u, tmp);
      p.core.position.copy(tmp); p.halo.position.copy(tmp);
      p.hist.unshift(tmp.clone()); if (p.hist.length > 12) p.hist.pop();
      p.trail.forEach((s, j) => { const h = p.hist[Math.min(p.hist.length - 1, (j + 1) * 2)]; if (h) s.position.copy(h); });
      if (k < 1) continue;
      tx.t = 0;
      if (tx.stage === 'in') { tx.stage = 'route'; ringBoost = 1; NODES.router.flash = 0.6; NODES.router.flashColor.copy(C.lime); }
      else if (tx.stage === 'route') {
        if (tx.fail) { flashNode(tx.target, C.red, 'bad'); burst(NODES[tx.target], C.red); chip(tx.target, 'declined', 'bad'); setPulseColor(p, C.red); tx.stage = 'back'; }
        else { flashNode(tx.target, C.mint, 'ok'); burst(NODES[tx.target], C.mint); chip(tx.target, 'approved', 'ok'); emit(tx, false); finish(i); }
      } else if (tx.stage === 'back') { tx.stage = 'retry'; setPulseColor(p, C.mint); ringBoost = 1; }
      else { flashNode(tx.alt, C.mint, 'ok'); burst(NODES[tx.alt], C.mint); chip(tx.alt, 'cascade ✓', 'cas'); emit(tx, true); finish(i); }
    }
  }
  function finish(i) { const tx = txs[i]; tx.p.active = false; showPulse(tx.p, false); txs.splice(i, 1); }

  /* ---------- layout & camera fit ---------- */
  let cw = 1, ch = 1;
  const bounds = [];
  [-2.72, 2.72].forEach(x => [-1.42, 1.42].forEach(z => [0, 0.18].forEach(y => bounds.push(new THREE.Vector3(x, y, z)))));
  const look = new THREE.Vector3(0, 0, 0.05);
  let dist = 8, elev = 0.92, azim = -0.12;
  function placeCamera(mx, my) {
    const e = elev + my * 0.06, a = azim + mx * 0.14;
    camera.position.set(look.x + dist * Math.cos(e) * Math.sin(a), look.y + dist * Math.sin(e), look.z + dist * Math.cos(e) * Math.cos(a));
    camera.lookAt(look);
  }
  function layout() {
    cw = host.clientWidth; ch = host.clientHeight;
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, lite ? 1.25 : 2));
    renderer.setSize(cw, ch, false);
    camera.aspect = cw / ch; camera.updateProjectionMatrix();
    dist = 8;
    for (let it = 0; it < 6; it++) {
      placeCamera(0, 0); camera.updateMatrixWorld();
      let m = 0;
      bounds.forEach(b => { const q = b.clone().project(camera); m = Math.max(m, Math.abs(q.x), Math.abs(q.y)); });
      dist *= m / 0.97;
    }
  }
  layout();
  new ResizeObserver(() => layout()).observe(host);

  /* ---------- pointer parallax ---------- */
  const mouse = new THREE.Vector2(), mouseS = new THREE.Vector2();
  window.addEventListener('pointermove', (e) => {
    mouse.set((e.clientX / window.innerWidth) * 2 - 1, (e.clientY / window.innerHeight) * 2 - 1);
  }, { passive: true });

  function placeLabels() {
    world.updateMatrixWorld(); camera.updateMatrixWorld();
    Object.keys(labels).forEach(k => {
      const s = toScreen(NODES[k].anchor), el = labels[k];
      el.style.transform = `translate3d(${(s.x - el.offsetWidth / 2).toFixed(1)}px, ${(s.y - el.offsetHeight / 2).toFixed(1)}px, 0)`;
    });
  }

  /* ---------- loop ---------- */
  let visible = true, last = performance.now(), spawnIn = 0.3, time = 0;
  new IntersectionObserver(([en]) => { visible = en.isIntersecting; }, { threshold: 0 }).observe(host);

  const minStep = lite ? 1 / 30 : 0;
  function frame(now) {
    if (minStep && (now - last) / 1000 < minStep) { requestAnimationFrame(frame); return; }
    const dt = Math.min(0.05, (now - last) / 1000); last = now;
    if (visible && !document.hidden) {
      time += dt;
      spawnIn -= dt;
      if (spawnIn <= 0) { spawn(); spawnIn = 0.5 + Math.random() * 0.35; }
      step(dt);
      Object.values(W).forEach(w => { w.heat = Math.max(0, w.heat - dt * 2.4); w.hot.opacity = w.heat * 0.5; w.hot.color.copy(w.color); });
      Object.values(NODES).forEach(n => {
        n.flash = Math.max(0, n.flash - dt * 1.6);
        if (n.router) { n.glow.opacity = 0.08 + n.flash * 0.3; }
        else { n.glow.opacity = n.flash * 0.4; n.glow.color.copy(n.flashColor); n.outline.color.copy(C.edge).lerp(n.flashColor, n.flash); }
      });
      ringBoost = Math.max(0, ringBoost - dt * 2);
      ring.rotation.z += dt * (0.5 + ringBoost * 6);
      ring2.rotation.z -= dt * (0.3 + ringBoost * 3);
      routerLight.intensity = 5 + ringBoost * 6;
      bursts.forEach(b => { if (b.t < 1) { b.t = Math.min(1, b.t + dt * 1.8); b.m.scale.setScalar(1 + b.t * 2.2); b.m.material.opacity = 0.8 * (1 - b.t); if (b.t >= 1) b.m.visible = false; } });
      mouseS.lerp(mouse, 0.08);
      placeCamera(mouseS.x, mouseS.y);
      renderer.render(scene, camera);
      placeLabels();
    }
    requestAnimationFrame(frame);
  }

  // first paint right away, even if the tab is in the background
  placeCamera(0, 0); renderer.render(scene, camera); placeLabels();
  window.dispatchEvent(new CustomEvent('guro:ready'));
  if (reduce) {
    placeCamera(0, 0); renderer.render(scene, camera); placeLabels();
    new ResizeObserver(() => { renderer.render(scene, camera); placeLabels(); }).observe(host);
  } else {
    requestAnimationFrame(frame);
  }
}

/* ---------- 2D fallback (no WebGL): animated SVG diagram ---------- */
function fallback2D() {
  host.classList.add('scene-2d');
  var ns = 'http://www.w3.org/2000/svg';
  var svg = document.createElementNS(ns, 'svg');
  svg.setAttribute('viewBox', '0 0 560 300'); svg.setAttribute('class', 'scene-svg');
  svg.innerHTML =
    '<path class="w" id="f0" d="M118 150 H220"/>' +
    '<path class="w" id="fa" d="M340 150 C 380 150, 380 60, 420 60"/>' +
    '<path class="w" id="fb" d="M340 150 H420"/>' +
    '<path class="w" id="fc" d="M340 150 C 380 150, 380 240, 420 240"/>' +
    '<rect class="n" x="18" y="118" width="100" height="64" rx="12"/>' +
    '<rect class="n hub" x="220" y="118" width="120" height="64" rx="12"/>' +
    '<rect class="n" id="ra" x="420" y="30" width="120" height="60" rx="12"/>' +
    '<rect class="n" id="rb" x="420" y="120" width="120" height="60" rx="12"/>' +
    '<rect class="n" id="rc" x="420" y="210" width="120" height="60" rx="12"/>' +
    '<g id="fdots"></g>';
  host.insertBefore(svg, host.firstChild);
  var pos = { cash: [68, 150], router: [280, 150], a: [480, 60], b: [480, 150], c: [480, 240] };
  function placeLabels() {
    var w = host.clientWidth, h = host.clientHeight, s = Math.min(w / 560, h / 300), ox = (w - 560 * s) / 2, oy = (h - 300 * s) / 2;
    host.querySelectorAll('[data-node]').forEach(function (el) {
      var p = pos[el.dataset.node];
      el.style.transform = 'translate3d(' + (ox + p[0] * s - el.offsetWidth / 2) + 'px,' + (oy + p[1] * s - el.offsetHeight / 2) + 'px,0)';
    });
  }
  placeLabels(); window.addEventListener('resize', placeLabels);
  window.dispatchEvent(new CustomEvent('guro:ready'));
  if (reduce) return;
  var dots = svg.querySelector('#fdots');
  function run(id, dur, color, rev) {
    return new Promise(function (res) {
      var path = svg.querySelector('#' + id), L = path.getTotalLength(), c = document.createElementNS(ns, 'circle');
      c.setAttribute('r', 5); c.setAttribute('fill', color); c.style.filter = 'drop-shadow(0 0 6px ' + color + ')';
      dots.appendChild(c);
      var t0 = null;
      function f(t) { if (!t0) t0 = t; var k = Math.min(1, (t - t0) / dur), e = k < .5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2;
        var pt = path.getPointAtLength(L * (rev ? 1 - e : e)); c.setAttribute('cx', pt.x); c.setAttribute('cy', pt.y);
        if (k < 1) requestAnimationFrame(f); else { c.remove(); res(); } }
      requestAnimationFrame(f);
    });
  }
  function flash(k, cls) { var r = svg.querySelector('#r' + k), el = host.querySelector('[data-node="' + k + '"]');
    r.classList.add(cls); el.classList.add(cls); setTimeout(function () { r.classList.remove(cls); el.classList.remove(cls); }, 600); }
  var amounts = ['€50', '€100', '€200', '€300', 'C$100', 'A$200'], methods = ['Visa', 'Mastercard', 'Apple Pay', 'Interac', 'Trustly'], geos = ['CA', 'DE', 'AU', 'NZ', 'FI'];
  function pick(a) { return a[Math.floor(Math.random() * a.length)]; }
  function tx() {
    var m = pick(methods), g = pick(geos), t = m === 'Trustly' ? 'c' : (g === 'CA' ? 'b' : 'a'), alt = t === 'b' ? 'a' : 'b', fail = Math.random() < .32, amt = pick(amounts);
    return run('f0', 450, '#d9ff3f').then(function () { return run('f' + t, 450, '#d9ff3f'); }).then(function () {
      if (!fail) { flash(t, 'ok'); window.dispatchEvent(new CustomEvent('guro:tx', { detail: { amt: amt, info: m + ' · ' + g + ' → PSP ' + t.toUpperCase(), status: 'approved', cls: 'ok' } })); return; }
      flash(t, 'bad');
      return run('f' + t, 350, '#ff5a4c', true).then(function () { return run('f' + alt, 450, '#7cf0c4'); }).then(function () {
        flash(alt, 'ok'); window.dispatchEvent(new CustomEvent('guro:tx', { detail: { amt: amt, info: m + ' · ' + g + ' · 05 do not honor → PSP ' + alt.toUpperCase(), status: 'cascade ✓', cls: 'cas' } }));
      });
    });
  }
  (function loop() { (document.hidden ? Promise.resolve() : tx()).then(function () { setTimeout(loop, 250); }); })();
}
})();
