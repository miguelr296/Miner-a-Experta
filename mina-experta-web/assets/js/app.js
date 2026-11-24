/* ============================================================
   MINA EXPERTA — Lógica de interfaz
   ============================================================ */

const $ = (sel, ctx = document) => ctx.querySelector(sel);
const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];

const state = {
  escenarioId: 'ESC-01',
  resultado: null,
  selectedMiner: 'm1',
  selectedTunnel: null,
  tab: 'decisiones',
  level: 'all',
  showBaseline: false,
  ruleFilter: 'all',
  view: { scale: 1, tx: 0, ty: 0 },
  drag: null,
  toastTimer: null
};

const COLOR_NIVEL = {
  normal: '#94a3b8',
  alerta: '#eab308',
  alto: '#f97316',
  peligro: '#dc2626'
};
const COLOR_DECISION = {
  evacuar: '#16a34a',
  refugiarse: '#2563eb',
  esperar: '#d97706'
};
const TIPO_NODO = {
  salida: { etiqueta: 'Salida', color: '#16a34a' },
  refugio: { etiqueta: 'Refugio', color: '#2563eb' },
  frente: { etiqueta: 'Frente de trabajo', color: '#d97706' },
  interseccion: { etiqueta: 'Intersección', color: '#94a3b8' }
};

/* ============================================================
   ARRANQUE
   ============================================================ */
document.addEventListener('DOMContentLoaded', () => {
  const params = new URLSearchParams(window.location.search);
  const escParam = params.get('esc');
  const tabParam = params.get('tab');
  if (['decisiones', 'reglas', 'traza', 'comparativa'].includes(tabParam)) state.tab = tabParam;
  const inicial = ESCENARIOS.some(e => e.id === escParam) ? escParam : 'ESC-01';
  renderScenarioList();
  bindEvents();
  seleccionarEscenario(inicial, { silencioso: true });
  const ver = params.get('ver');
  if (ver === 'catalogo') setTimeout(abrirCatalogoReglas, 120);
  else if (ver && ver.startsWith('tunel:')) setTimeout(() => abrirExplicacionTunel(ver.slice(6)), 120);
  else if (ver && ver.startsWith('minero:')) setTimeout(() => abrirExplicacionMinero(ver.slice(7)), 120);
});

function bindEvents() {
  $('#btnRun').addEventListener('click', () => ejecutarYRefrescar(true));
  $('#btnRules').addEventListener('click', abrirCatalogoReglas);
  $('#levelFilter').addEventListener('click', onLevelFilter);
  $('#toggleBaseline').addEventListener('change', e => {
    state.showBaseline = e.target.checked;
    renderMap();
  });
  $('#zoomIn').addEventListener('click', () => zoomBy(1.18));
  $('#zoomOut').addEventListener('click', () => zoomBy(1 / 1.18));
  $('#zoomReset').addEventListener('click', () => {
    state.view = { scale: 1, tx: 0, ty: 0 };
    applyZoom();
  });
  $('#tabs').addEventListener('click', onTabClick);
  $('#scenarioList').addEventListener('click', onScenarioClick);
  $('#tabBody').addEventListener('click', onTabBodyClick);

  const map = $('#mineMap');
  map.addEventListener('pointermove', onMapMove);
  map.addEventListener('pointerleave', hideTooltip);
  map.addEventListener('pointerdown', onMapDown);
  map.addEventListener('pointerup', onMapUp);
  map.addEventListener('pointercancel', onMapUp);
  map.addEventListener('wheel', onMapWheel, { passive: false });
  map.addEventListener('click', onMapClick);

  $('#inspector').addEventListener('click', onInspectorClick);
  $('#modalClose').addEventListener('click', cerrarModal);
  $('#modalBackdrop').addEventListener('click', e => {
    if (e.target.id === 'modalBackdrop') cerrarModal();
  });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      if (!$('#modalBackdrop').hidden) cerrarModal();
      else if (state.selectedTunnel) {
        state.selectedTunnel = null;
        renderMap();
        renderInspector();
      }
    }
  });
}

/* ============================================================
   ESCENARIOS
   ============================================================ */
function escenarioActual() {
  return ESCENARIOS.find(e => e.id === state.escenarioId) || ESCENARIOS[0];
}

function seleccionarEscenario(id, opciones = {}) {
  state.escenarioId = id;
  state.selectedTunnel = null;
  state.showBaseline = false;
  $('#toggleBaseline').checked = false;
  state.level = 'all';
  $$('#levelFilter button').forEach(b => b.classList.toggle('active', b.dataset.level === 'all'));
  ejecutarYRefrescar(!opciones.silencioso);
}

function ejecutarYRefrescar(mostrarToast) {
  const esc = escenarioActual();
  state.resultado = ejecutarMotor(esc);
  state.selectedMiner = state.resultado.mineros[0]?.id || null;
  renderScenarioList();
  renderHeader();
  renderKpis();
  renderMiniMetrics();
  renderMap();
  renderInspector();
  renderTab();
  updateConsole();
  if (mostrarToast) {
    showToast(`Inferencia ${esc.id} completada · ${state.resultado.resumen.reglas} reglas en ${state.resultado.resumen.duracion} ms`);
  }
}

function renderScenarioList() {
  const cont = $('#scenarioList');
  cont.innerHTML = ESCENARIOS.map(e => {
    const sev = e.severidad === 'critica' ? 'CRÍTICO' : 'RIESGO ALTO';
    return `
      <button class="scenario-card ${e.id === state.escenarioId ? 'active' : ''}" data-scenario="${e.id}" data-sev="${e.severidad}" type="button">
        <div class="scenario-top">
          <span class="scenario-code">${e.id} · ${e.hora}</span>
          <span class="severity ${e.severidad}">${sev}</span>
        </div>
        <h3>${e.nombre}</h3>
        <p>${e.evento}</p>
      </button>`;
  }).join('');
}

function onScenarioClick(e) {
  const card = e.target.closest('[data-scenario]');
  if (!card || card.dataset.scenario === state.escenarioId) return;
  seleccionarEscenario(card.dataset.scenario);
}

/* ============================================================
   CABECERA / KPIs
   ============================================================ */
function renderHeader() {
  const esc = escenarioActual();
  $('#topScenario').textContent = `${esc.id} · ${esc.nombre}`;
  $('#topClock').textContent = esc.hora;
  $('#scenarioTitle').textContent = esc.nombre;
  $('#scenarioDesc').textContent = esc.descripcion;
  document.title = `${esc.id} · Mina Experta`;
}

function renderKpis() {
  const r = state.resultado.resumen;
  $('#kpis').innerHTML = `
    <div class="kpi ${r.cerrados ? 'danger' : 'ok'}">
      <span>Túneles cerrados</span>
      <strong>${r.cerrados}<small> / ${TUNELES.length}</small></strong>
    </div>
    <div class="kpi warn">
      <span>Riesgo alto</span>
      <strong>${r.alto}<small> túneles</small></strong>
    </div>
    <div class="kpi info">
      <span>Evacuando</span>
      <strong>${r.evacuando}<small> / ${state.resultado.mineros.length}</small></strong>
    </div>`;
}

function renderMiniMetrics() {
  const el = $('#miniMetrics');
  if (!el) return;
  const r = state.resultado.resumen;
  const afectados = r.refugiados + r.esperando;
  el.innerHTML = `
    <div class="mini-metric danger">
      <span><i></i>Túneles cerrados</span>
      <strong>${r.cerrados}<small>de ${TUNELES.length}</small></strong>
    </div>
    <div class="mini-metric warn">
      <span><i></i>Túneles afectados</span>
      <strong>${r.alto + r.alerta}<small>túneles</small></strong>
    </div>
    <div class="mini-metric ${afectados ? 'danger' : 'ok'}">
      <span><i></i>Mineros afectados</span>
      <strong>${afectados}<small>de ${state.resultado.mineros.length}</small></strong>
    </div>
    <div class="mini-metric ok">
      <span><i></i>Reglas activas</span>
      <strong>${r.reglasUnicas}<small>de ${REGLAS.length}</small></strong>
    </div>`;
}

function updateConsole() {
  const r = state.resultado;
  $('#consoleBadge').textContent = `${r.mineros.length} personas`;
  $('#consoleSub').textContent = `${r.resumen.evacuando} evacúan · ${r.resumen.refugiados} se refugian · ${r.resumen.esperando} esperan`;
  $('#tabCountDec').textContent = r.mineros.length;
  $('#tabCountRules').textContent = r.resumen.reglasUnicas;
  $('#tabCountTrace').textContent = r.traza.length;
  $('#inferenceStats').textContent = `${r.resumen.reglas} reglas aplicadas · ${r.resumen.duracion} ms`;
}

/* ============================================================
   PLANO SVG
   ============================================================ */
function renderMap() {
  const r = state.resultado;
  if (!r) return;
  const svg = $('#mineMap');
  const selectedMiner = r.mineros.find(m => m.id === state.selectedMiner) || null;

  const t1 = TUNELES.filter(t => nivelDeTunel(t) === 1).length;
  const t2 = TUNELES.filter(t => nivelDeTunel(t) === 2).length;
  const n1 = NODOS.filter(n => n.nivel === 1).length;
  const n2 = NODOS.filter(n => n.nivel === 2).length;

  let html = `<defs>
    <pattern id="gridP" width="38" height="38" patternUnits="userSpaceOnUse">
      <path d="M38 0H0V38" fill="none" stroke="#e2e8f0" stroke-width=".6" opacity=".8"/>
    </pattern>
    <filter id="softGlow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="2" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>`;

  html += '<g id="zoomLayer">';
  html += bandaNivel(1, 48, t1, n1);
  html += bandaNivel(2, 430, t2, n2);

  const orden = { normal: 0, alerta: 1, alto: 2, peligro: 3 };
  const tunelesOrdenados = TUNELES.slice().sort((a, b) => {
    const ta = r.porTunel[a.id];
    const tb = r.porTunel[b.id];
    if (a.id === state.selectedTunnel) return 1;
    if (b.id === state.selectedTunnel) return -1;
    return orden[ta.nivel] - orden[tb.nivel];
  });

  html += '<g id="tunnelsLayer">';
  tunelesOrdenados.forEach(t => { html += dibujarTunel(t, r.porTunel[t.id]); });
  html += '</g>';

  html += '<g id="routesLayer" pointer-events="none">';
  html += dibujarRutas(selectedMiner);
  html += '</g>';

  html += '<g id="nodesLayer">';
  NODOS.forEach(n => { html += dibujarNodo(n, r); });
  r.mineros.forEach(m => { html += dibujarMinero(m); });
  html += '</g>';
  html += '</g>';

  svg.innerHTML = html;
  svg.classList.remove('focus-1', 'focus-2');
  if (state.level !== 'all') svg.classList.add(`focus-${state.level}`);
  applyZoom();
}

function nivelDeTunel(t) {
  const a = NODOS.find(n => n.id === t.a);
  return a ? a.nivel : 1;
}

function bandaNivel(nivel, y, tuneles, nodos) {
  const cota = nivel === 1 ? 340 : 280;
  return `<g data-level="${nivel}">
    <rect class="level-band ${nivel === 2 ? 'n2' : ''}" x="44" y="${y}" width="892" height="332" rx="16"/>
    <rect x="44" y="${y}" width="892" height="332" rx="16" fill="url(#gridP)" opacity=".5"/>
    <text class="level-label" x="64" y="${y + 26}">NIVEL ${nivel}</text>
    <text class="level-sub" x="64" y="${y + 39}">COTA ${cota} · ${nodos} NODOS · ${tuneles} LABORES</text>
    <text class="level-sub" x="${908}" y="${y + 26}" text-anchor="end">SECTOR ${nivel === 1 ? 'NORTE' : 'SUR'}</text>
  </g>`;
}

function coords(id) {
  const n = NODOS.find(x => x.id === id);
  return { x: n.x, y: n.y };
}

function dibujarTunel(t, d) {
  const a = coords(t.a);
  const b = coords(t.b);
  const mx = (a.x + b.x) / 2;
  const my = (a.y + b.y) / 2;
  const dx = b.x - a.x;
  const dy = b.y - a.y;
  const len = Math.hypot(dx, dy) || 1;
  const nx = -dy / len;
  const ny = dx / len;
  const nivel = d.nivel;
  const visual = d.cerrado ? 'peligro' : nivel;
  const selected = state.selectedTunnel === t.id;

  let extra = '';
  if (visual !== 'normal') {
    const off = 17;
    const fx = mx + nx * off;
    const fy = my + ny * off;
    if (visual === 'peligro') {
      extra += `<g class="flag flag-peligro" transform="translate(${fx.toFixed(1)},${fy.toFixed(1)})">
        <rect class="flag-bg" x="-32" y="-9" width="64" height="18" rx="4"/>
        <text class="tunnel-flag" text-anchor="middle" y="3.7">CERRADO</text>
      </g>`;
    } else {
      const txt = visual === 'alto' ? '×3' : '×2';
      const cls = visual === 'alto' ? 'flag-alto' : 'flag-alerta';
      extra += `<g class="flag ${cls}" transform="translate(${fx.toFixed(1)},${fy.toFixed(1)})">
        <rect class="flag-bg" x="-15" y="-9" width="30" height="18" rx="4"/>
        <text class="tunnel-flag" text-anchor="middle" y="3.7">${txt}</text>
      </g>`;
    }
  }

  if (d.lecturas.incendio) {
    extra += `<g class="event-icon" transform="translate(${(mx - nx * 16).toFixed(1)},${(my - ny * 16).toFixed(1)})">
      <circle r="10" fill="#fef2f2" stroke="#fca5a5" stroke-width="1" opacity=".95"/>
      <path d="M0 -5.4c.2 2.6-1.8 3.6-2.8 5.2-1.1 1.8-.4 3.9 1.5 4.4 2.1.6 4.2-.8 4.2-3.2 0-1.3-.5-2.3-1.4-3.3-.1 1-.6 1.4-1.1 1.7.3-1.7.2-3.3-.4-4.8Z" fill="#dc2626"/>
    </g>`;
  }
  if (d.lecturas.derrumbe) {
    extra += `<g class="event-icon" transform="translate(${(mx - nx * 16).toFixed(1)},${(my - ny * 16).toFixed(1)})">
      <circle r="10" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1" opacity=".95"/>
      <path d="M-4.8 3.5 0 -3.8l4.8 7.3H-4.8Z" fill="#94a3b8" opacity=".9"/>
      <path d="M-2.7 1.4-.4-1.8l2.2 3.2h-4.5Z" fill="#cbd5e1"/>
    </g>`;
  }

  let label = '';
  if (selected) {
    label = `<text class="tunnel-label" x="${mx.toFixed(1)}" y="${(my + 26).toFixed(1)}" text-anchor="middle">${escapar(t.nombre)} · ${t.longitud} m</text>`;
  } else if (t.via === 'chimenea') {
    label = `<text class="tunnel-label" x="${(mx - 16).toFixed(1)}" y="${my.toFixed(1)}" text-anchor="middle" transform="rotate(-90 ${(mx - 16).toFixed(1)} ${my.toFixed(1)})">CHIMENEA · 60 m</text>`;
  }

  const riskClass = visual !== 'normal' ? `tunnel-risk ${visual}` : '';
  return `<g class="tunnel-group ${selected ? 'selected' : ''}" data-tunel="${t.id}" data-level="${d.nivel}">
    <line class="tunnel-base" x1="${a.x}" y1="${a.y}" x2="${b.x}" y2="${b.y}"/>
    <line class="tunnel-inner" x1="${a.x}" y1="${a.y}" x2="${b.x}" y2="${b.y}"/>
    ${visual !== 'normal' ? `<line class="${riskClass}" x1="${a.x}" y1="${a.y}" x2="${b.x}" y2="${b.y}"/>` : ''}
    <line class="tunnel-shine" x1="${a.x}" y1="${a.y}" x2="${b.x}" y2="${b.y}"/>
    <line class="tunnel-hit" x1="${a.x}" y1="${a.y}" x2="${b.x}" y2="${b.y}"/>
    ${extra}
    ${label}
  </g>`;
}

function dibujarNodo(n, r) {
  const config = TIPO_NODO[n.tipo];
  const selectedByTunnel = state.selectedTunnel && (r.porTunel[state.selectedTunnel]?.a === n.id || r.porTunel[state.selectedTunnel]?.b === n.id);
  const mineros = r.mineros.filter(m => m.nodo === n.id);
  let shape = '';
  if (n.tipo === 'salida') {
    shape = `<circle class="node-shape" r="11.5" fill="#f0fdf4" stroke="${config.color}" stroke-width="2.5"/>
      <path d="M-3.5 3.5 3.5-3.5M-1.6-3.5h5.1v5.1" fill="none" stroke="#15803d" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>`;
  } else if (n.tipo === 'refugio') {
    shape = `<rect class="node-shape" x="-11" y="-11" width="22" height="22" rx="5" fill="#eff6ff" stroke="${config.color}" stroke-width="2.2"/>
      <path d="M-4.8-1.8 0-5.8l4.8 4v5.6h-9.6v-5.6Z" fill="none" stroke="#2563eb" stroke-width="1.5" stroke-linejoin="round"/>`;
  } else if (n.tipo === 'frente') {
    shape = `<polygon class="node-shape" points="0,-10.5 10.5,0 0,10.5 -10.5,0" fill="#fffbeb" stroke="${config.color}" stroke-width="2.2"/>
      <circle r="2.8" fill="#d97706"/>`;
  } else {
    shape = `<circle class="node-shape" r="7" fill="#ffffff" stroke="#94a3b8" stroke-width="2"/>
      <circle r="2" fill="#64748b"/>`;
  }
  const labelY = n.y + (n.tipo === 'interseccion' ? 21 : 26);
  const mineroTag = mineros.length ? `<circle cx="14" cy="-14" r="3.8" fill="#0f172a" stroke="#ffffff" stroke-width="1.2"/>` : '';
  return `<g class="node-group ${selectedByTunnel ? 'selected' : ''}" data-node="${n.id}" data-level="${n.nivel}" transform="translate(${n.x},${n.y})">
    <circle class="node-halo" r="20" stroke="${config.color}" opacity=".28"/>
    ${shape}
    ${mineroTag}
    <text class="node-label" y="${labelY - n.y}">${escapar(n.nombre)}</text>
  </g>`;
}

function dibujarMinero(m) {
  const n = NODOS.find(x => x.id === m.nodo);
  if (!n) return '';
  const color = COLOR_DECISION[m.decision];
  const cls = m.decision === 'refugiarse' ? 'refugio' : m.decision === 'esperar' ? 'waiting' : '';
  const sel = state.selectedMiner === m.id ? 'selected' : '';
  return `<g class="minero-group ${cls} ${sel}" data-minero="${m.id}" data-level="${n.nivel}" transform="translate(${n.x + 25},${n.y - 26})">
    <line x1="-25" y1="26" x2="0" y2="0" stroke="${color}" stroke-width="1" opacity=".35"/>
    <circle class="minero-halo" r="16" fill="${hexAlpha(color, .13)}" stroke="${color}"/>
    <circle class="minero-core" r="10.5" fill="${color}" stroke="#ffffff"/>
    <text class="minero-initials" y="3.2">${m.iniciales}</text>
  </g>`;
}

function dibujarRutas(m) {
  if (!m) return '';
  let out = '';
  if (state.showBaseline && m.rutaBase) {
    out += `<path class="route-base" d="${pathD(m.rutaBase.nodos)}"/>`;
  }
  if (m.rutaAsignada) {
    const tipo = m.decision === 'refugiarse' ? 'refugio' : m.decision === 'esperar' ? 'espera' : '';
    out += `<path class="route-glow ${tipo}" d="${pathD(m.rutaAsignada.nodos)}"/>`;
    out += `<path class="route-line ${tipo}" d="${pathD(m.rutaAsignada.nodos)}"/>`;
    const fin = coords(m.rutaAsignada.destino);
    out += `<circle class="route-node-ring ${tipo}" cx="${fin.x}" cy="${fin.y}" r="14"/>`;
    const ini = coords(m.nodo);
    out += `<circle class="route-node-ring ${tipo}" cx="${ini.x}" cy="${ini.y}" r="11"/>`;
  }
  return out;
}

function pathD(nodos) {
  return nodos.map((id, i) => {
    const c = coords(id);
    return `${i === 0 ? 'M' : 'L'}${c.x},${c.y}`;
  }).join(' ');
}

function hexAlpha(hex, alpha) {
  const n = parseInt(hex.slice(1), 16);
  const r = (n >> 16) & 255;
  const g = (n >> 8) & 255;
  const b = n & 255;
  return `rgba(${r},${g},${b},${alpha})`;
}

/* ============================================================
   INTERACCIÓN DEL MAPA
   ============================================================ */
function onLevelFilter(e) {
  const btn = e.target.closest('[data-level]');
  if (!btn) return;
  state.level = btn.dataset.level;
  $$('#levelFilter button').forEach(b => b.classList.toggle('active', b === btn));
  const svg = $('#mineMap');
  svg.classList.remove('focus-1', 'focus-2');
  if (state.level !== 'all') svg.classList.add(`focus-${state.level}`);
}

function onMapMove(e) {
  if (state.drag && state.drag.active) {
    const dx = e.clientX - state.drag.x;
    const dy = e.clientY - state.drag.y;
    if (Math.hypot(dx, dy) > 3) state.drag.moved = true;
    const rect = e.currentTarget.getBoundingClientRect();
    const k = 980 / Math.max(rect.width, 1);
    state.view.tx = state.drag.tx + dx * k;
    state.view.ty = state.drag.ty + dy * k;
    applyZoom();
    hideTooltip();
    return;
  }
  const tunelEl = e.target.closest('[data-tunel]');
  const mineroEl = e.target.closest('[data-minero]');
  const nodoEl = e.target.closest('[data-node]');
  if (tunelEl) showTunnelTooltip(e, tunelEl.dataset.tunel);
  else if (mineroEl) showMinerTooltip(e, mineroEl.dataset.minero);
  else if (nodoEl) showNodeTooltip(e, nodoEl.dataset.node);
  else hideTooltip();
}

function onMapDown(e) {
  if (e.button !== 0) return;
  state.drag = { active: true, x: e.clientX, y: e.clientY, tx: state.view.tx, ty: state.view.ty, moved: false };
  $('#mineMap').classList.add('dragging');
}

function onMapUp() {
  if (!state.drag) return;
  state.drag.active = false;
  $('#mineMap').classList.remove('dragging');
  setTimeout(() => { if (state.drag) state.drag.moved = false; }, 80);
}

function onMapWheel(e) {
  e.preventDefault();
  const factor = e.deltaY < 0 ? 1.1 : 1 / 1.1;
  zoomBy(factor);
}

function zoomBy(factor) {
  const s0 = state.view.scale;
  const s1 = Math.min(2.4, Math.max(0.65, s0 * factor));
  if (s1 === s0) return;
  const cx = 490;
  const cy = 405;
  state.view.tx = cx - (cx - state.view.tx) * (s1 / s0);
  state.view.ty = cy - (cy - state.view.ty) * (s1 / s0);
  state.view.scale = s1;
  applyZoom();
}

function applyZoom() {
  const g = $('#zoomLayer');
  if (!g) return;
  g.setAttribute('transform', `translate(${state.view.tx.toFixed(2)},${state.view.ty.toFixed(2)}) scale(${state.view.scale.toFixed(3)})`);
}

function onMapClick(e) {
  if (state.drag && state.drag.moved) return;
  const mineroEl = e.target.closest('[data-minero]');
  if (mineroEl) {
    seleccionarMinero(mineroEl.dataset.minero, true);
    return;
  }
  const tunelEl = e.target.closest('[data-tunel]');
  if (tunelEl) {
    state.selectedTunnel = state.selectedTunnel === tunelEl.dataset.tunel ? null : tunelEl.dataset.tunel;
    renderMap();
    renderInspector();
    return;
  }
  const nodoEl = e.target.closest('[data-node]');
  if (nodoEl) {
    const minero = state.resultado.mineros.find(m => m.nodo === nodoEl.dataset.node);
    if (minero) seleccionarMinero(minero.id, true);
  }
}

function seleccionarMinero(id, desdeMapa = false) {
  state.selectedMiner = id;
  renderMap();
  renderTab();
  if (desdeMapa) {
    const card = $(`[data-miner-card="${id}"]`);
    if (card) card.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
  }
}

/* ---------- Tooltips ---------- */
function showTunnelTooltip(e, id) {
  const t = state.resultado.porTunel[id];
  if (!t) return;
  const l = t.lecturas;
  const est = nivelTexto(t.nivel);
  const tooltip = $('#tooltip');
  tooltip.innerHTML = `
    <h4>${escapar(t.nombre)}</h4>
    <div class="tt-sub">${t.via.toUpperCase()} · ${t.longitud} m</div>
    <span class="tt-risk" style="color:${COLOR_NIVEL[t.nivel]};background:${hexAlpha(COLOR_NIVEL[t.nivel], .13)};border:1px solid ${hexAlpha(COLOR_NIVEL[t.nivel], .35)}">${est}</span>
    <div class="tt-row"><span>CO</span><b>${fmt(l.co)} ppm</b></div>
    <div class="tt-row"><span>O₂</span><b>${fmt(l.o2, 1)} %</b></div>
    <div class="tt-row"><span>Velocidad aire</span><b>${fmt(l.vel)} m/min</b></div>
    <div class="tt-row"><span>Costo de ruta</span><b>${t.cerrado ? 'bloqueado' : `×${t.multiplicador} → ${fmt(t.costo)}`}</b></div>`;
  positionTooltip(e, tooltip);
}

function showMinerTooltip(e, id) {
  const m = state.resultado.mineros.find(x => x.id === id);
  if (!m) return;
  const tooltip = $('#tooltip');
  tooltip.innerHTML = `
    <h4>${escapar(m.nombre)}</h4>
    <div class="tt-sub">${escapar(m.rol)} · ${escapar(m.nodoNombre)}</div>
    <span class="tt-risk" style="color:${COLOR_DECISION[m.decision]};background:${hexAlpha(COLOR_DECISION[m.decision], .13)};border:1px solid ${hexAlpha(COLOR_DECISION[m.decision], .35)}">${etiquetaDecision(m.decision)}</span>
    <div class="tt-row"><span>Ruta</span><b>${m.rutaAsignada ? `${m.rutaAsignada.longitud} m` : 'sin ruta'}</b></div>
    <div class="tt-row"><span>Regla</span><b>${m.reglaDecision}</b></div>`;
  positionTooltip(e, tooltip);
}

function showNodeTooltip(e, id) {
  const n = NODOS.find(x => x.id === id);
  if (!n) return;
  const cfg = TIPO_NODO[n.tipo];
  const mineros = state.resultado.mineros.filter(m => m.nodo === id);
  const tooltip = $('#tooltip');
  tooltip.innerHTML = `
    <h4>${escapar(n.nombre)}</h4>
    <div class="tt-sub">${cfg.etiqueta} · NIVEL ${n.nivel}</div>
    <div class="tt-row"><span>Código</span><b>${n.corto}</b></div>
    <div class="tt-row"><span>Mineros</span><b>${mineros.length || '—'}</b></div>`;
  positionTooltip(e, tooltip);
}

function positionTooltip(e, tooltip) {
  const pad = 14;
  let x = e.clientX + 16;
  let y = e.clientY + 16;
  const w = tooltip.offsetWidth || 220;
  const h = tooltip.offsetHeight || 120;
  if (x + w > window.innerWidth - pad) x = e.clientX - w - 16;
  if (y + h > window.innerHeight - pad) y = e.clientY - h - 16;
  tooltip.style.left = `${x}px`;
  tooltip.style.top = `${y}px`;
  tooltip.classList.add('visible');
}

function hideTooltip() {
  $('#tooltip').classList.remove('visible');
}

function showToast(msg) {
  const toast = $('#toast');
  toast.textContent = msg;
  toast.classList.add('show');
  clearTimeout(state.toastTimer);
  state.toastTimer = setTimeout(() => toast.classList.remove('show'), 3200);
}

/* ============================================================
   INSPECTOR DE TÚNEL
   ============================================================ */
function renderInspector() {
  const el = $('#inspector');
  const t = state.selectedTunnel ? state.resultado.porTunel[state.selectedTunnel] : null;
  if (!t) {
    el.hidden = true;
    el.innerHTML = '';
    return;
  }
  const l = t.lecturas;
  const gasLevels = {
    co: nivelGas(l.co, UMBRALES.co),
    o2: nivelGas(l.o2, UMBRALES.o2),
    no2: nivelGas(l.no2, UMBRALES.no2),
    vel: l.vel < UMBRAL_VIENTO.minimo ? 'alerta' : 'normal'
  };
  el.innerHTML = `
    <div class="inspector-head">
      <div class="insp-copy">
        <h3>${escapar(t.nombre)}</h3>
        <span class="sub">${t.via.toUpperCase()} · ${t.longitud} m · NIVEL ${t.nivel}</span>
      </div>
      <span class="risk-badge ${t.nivel}">${nivelTexto(t.nivel)}</span>
      <button class="icon-btn" data-close-inspector aria-label="Cerrar">✕</button>
    </div>
    <div class="sensor-grid">
      ${celdaSensor('CO', fmt(l.co), 'ppm', gasLevels.co)}
      ${celdaSensor('O₂', fmt(l.o2, 1), '%', gasLevels.o2)}
      ${celdaSensor('NO₂', fmt(l.no2, 1), 'ppm', gasLevels.no2)}
      ${celdaSensor('Aire', fmt(l.vel), 'm/min', gasLevels.vel)}
    </div>
    <div class="inspector-foot">
      <span>${t.cerrado ? 'Arista bloqueada' : `Costo ${t.longitud} m × ${t.multiplicador} = <b class="mono">${fmt(t.costo)}</b>`}</span>
      <button class="btn btn-ghost small" data-why="${t.id}" type="button">¿Por qué?</button>
    </div>`;
  el.hidden = false;
}

function celdaSensor(nombre, valor, unidad, nivel) {
  return `<div class="sensor-cell"><span>${nombre}</span><strong class="${nivel === 'normal' ? '' : nivel === 'alerta' ? 'warn' : 'danger'}">${valor} <small>${unidad}</small></strong></div>`;
}

function onInspectorClick(e) {
  if (e.target.closest('[data-close-inspector]')) {
    state.selectedTunnel = null;
    renderMap();
    renderInspector();
    return;
  }
  const why = e.target.closest('[data-why]');
  if (why) abrirExplicacionTunel(why.dataset.why);
}

/* ============================================================
   PESTAÑAS
   ============================================================ */
function onTabClick(e) {
  const btn = e.target.closest('[data-tab]');
  if (!btn) return;
  state.tab = btn.dataset.tab;
  $$('#tabs .tab').forEach(b => b.classList.toggle('active', b === btn));
  renderTab();
}

function renderTab() {
  $$('#tabs .tab').forEach(b => b.classList.toggle('active', b.dataset.tab === state.tab));
  const body = $('#tabBody');
  const render = {
    decisiones: renderDecisiones,
    reglas: renderReglas,
    traza: renderTraza,
    comparativa: renderComparativa
  }[state.tab];
  body.innerHTML = `<div class="tab-pane">${render()}</div>`;
}

function onTabBodyClick(e) {
  const explainBtn = e.target.closest('[data-explain]');
  if (explainBtn) {
    abrirExplicacionMinero(explainBtn.dataset.explain);
    return;
  }
  const filterBtn = e.target.closest('[data-rule-filter]');
  if (filterBtn) {
    state.ruleFilter = filterBtn.dataset.ruleFilter;
    renderTab();
    return;
  }
  const card = e.target.closest('[data-miner-card]');
  if (card) seleccionarMinero(card.dataset.minerCard, false);
}

/* ---------- Decisiones ---------- */
function renderDecisiones() {
  const r = state.resultado;
  const tarjetas = r.mineros.map(m => {
    const badges = { evacuar: 'EVACUAR', refugiarse: 'REFUGIARSE', esperar: 'ESPERAR' };
    const clase = m.decision === 'refugiarse' ? 'refugiado' : m.decision === 'esperar' ? 'waiting' : 'evacuando';
    const selected = state.selectedMiner === m.id ? 'selected' : '';
    return `<article class="miner-card ${clase} ${selected}" data-miner-card="${m.id}">
      <div class="miner-head">
        <div class="avatar">${m.iniciales}</div>
        <div class="miner-id">
          <h3>${escapar(m.nombre)}</h3>
          <p>${escapar(m.rol)} · ${escapar(m.nodoNombre)}</p>
        </div>
        <span class="decision-badge ${m.decision}">${badges[m.decision]}</span>
      </div>
      ${pasosRuta(m)}
      <div class="miner-foot">
        <span class="reason">${escapar(m.motivo)}</span>
        <button class="link-btn" data-explain="${m.id}" type="button">Ver detalle</button>
      </div>
    </article>`;
  }).join('');

  return tarjetas;
}

function pasosRuta(m) {
  if (!m.rutaAsignada) {
    return `<div class="route-steps"><span class="step-pill start">${codigoNodo(m.nodo)}</span><span class="step-arrow">·</span><span class="step-pill refugio">Sin ruta transitable</span></div>`;
  }
  const nodos = m.rutaAsignada.nodos;
  const mostrar = nodos.length <= 6 ? nodos : [nodos[0], nodos[1], nodos[Math.floor(nodos.length / 2)], nodos[nodos.length - 2], nodos[nodos.length - 1]];
  const pills = mostrar.map((id, i) => {
    const esInicio = id === nodos[0];
    const esFin = id === nodos[nodos.length - 1];
    let cls = '';
    if (esInicio) cls = 'start';
    else if (esFin) cls = m.decision === 'refugiarse' ? 'refugio' : 'end';
    return `<span class="step-pill ${cls}">${codigoNodo(id)}</span>`;
  }).join('<span class="step-arrow">›</span>');
  const extra = nodos.length > 6 ? '' : '';
  return `<div class="route-steps">${pills}${extra}</div>`;
}

function codigoNodo(id) {
  const n = NODOS.find(x => x.id === id);
  return n ? n.corto : id;
}

/* ---------- Reglas ---------- */
function renderReglas() {
  const r = state.resultado;
  const disparadas = REGLAS.filter(x => r.reglasDisparadas[x.id]);
  const filtros = ['all', 'DIAG', 'RIESGO', 'RUTA', 'DEC'];
  const chips = filtros.map(f => {
    const label = f === 'all' ? 'Todas' : f;
    const count = f === 'all' ? disparadas.length : disparadas.filter(x => x.categoria === f).length;
    return `<button class="chip ${state.ruleFilter === f ? 'active' : ''}" data-rule-filter="${f}" type="button">${label} · ${count}</button>`;
  }).join('');

  const lista = disparadas
    .filter(x => state.ruleFilter === 'all' || x.categoria === state.ruleFilter)
    .sort((a, b) => b.prioridad - a.prioridad)
    .map(reg => {
      const d = r.reglasDisparadas[reg.id];
      const where = d.tuneles.slice(0, 3).join(' · ') + (d.tuneles.length > 3 ? ` +${d.tuneles.length - 3}` : '');
      return `<div class="rule-item">
        <div class="rule-item-head">
          <span class="rule-id">${reg.id}</span>
          <span class="cat-pill ${reg.categoria}">${reg.categoria}</span>
          <span class="source-pill ${reg.fuente}">${reg.fuente}</span>
          <span class="fire-count">${d.total}×</span>
        </div>
        <h4>${escapar(reg.nombre)}</h4>
        <div class="rule-where">${escapar(where)}</div>
      </div>`;
    }).join('');

  return `<div class="rule-filters">${chips}</div>
    <div class="rules-note">Se muestran las reglas que se dispararon en este escenario. <strong>${r.resumen.reglasUnicas}</strong> de <strong>${REGLAS.length}</strong> reglas de la base fueron utilizadas.</div>
    ${lista || '<div class="empty-state">No hay reglas disparadas con este filtro.</div>'}`;
}

/* ---------- Traza ---------- */
function renderTraza() {
  const r = state.resultado;
  if (!r.traza.length) return '<div class="empty-state">Sin eventos de inferencia.</div>';
  const conflictos = r.conflictos.map(c => `<div class="trace-conflict"><strong>Conflicto resuelto</strong> · ${escapar(c.detalle)}</div>`).join('');
  const filas = r.traza.map(e => {
    const cat = e.categoria || 'DEC';
    return `<div class="trace-row">
      <span class="trace-step">${String(e.paso).padStart(2, '0')}</span>
      <div class="trace-content">
        <div class="trace-top">
          <span class="cat-pill ${cat}">${cat}</span>
          <span class="trace-rule">${e.regla}</span>
          <span class="trace-entity">${escapar(e.entidadNombre)}</span>
          <span class="trace-prio">P${e.prioridad}</span>
        </div>
        <p>${escapar(e.detalle)}</p>
      </div>
    </div>`;
  }).join('');
  return `<div class="trace-tools"><span>Orden de disparo · prioridad descendente</span><span>${r.traza.length} eventos</span></div>
    ${conflictos}
    <div class="trace-list">${filas}</div>`;
}

/* ---------- Comparativa ---------- */
function renderComparativa() {
  const r = state.resultado;
  const conSalida = r.mineros.filter(m => m.rutaSalida);
  const expSistema = sum(conSalida.map(m => m.rutaSalida.exposicion));
  const expBase = sum(conSalida.map(m => m.rutaBase ? m.rutaBase.exposicion : 0));
  const lenSistema = sum(conSalida.map(m => m.rutaSalida.longitud));
  const lenBase = sum(conSalida.map(m => m.rutaBase ? m.rutaBase.longitud : 0));
  const diferencia = expBase - expSistema;

  const filas = r.mineros.map(m => {
    const sistema = m.rutaSalida
      ? `${fmt(m.rutaSalida.longitud)} m · exp ${m.rutaSalida.exposicion}`
      : 'Sin ruta';
    const base = m.rutaBase
      ? `${fmt(m.rutaBase.longitud)} m · exp ${m.rutaBase.exposicion}`
      : 'Sin ruta';
    let dif = '—';
    let clase = 'info';
    if (m.rutaSalida && m.rutaBase) {
      const d = m.rutaBase.exposicion - m.rutaSalida.exposicion;
      dif = d > 0 ? `−${d} riesgo` : d < 0 ? `+${Math.abs(d)}` : 'igual';
      clase = d > 0 ? 'ok' : d < 0 ? 'danger' : 'info';
    } else if (m.rutaSalida && !m.rutaBase) {
      dif = 'base sin ruta';
      clase = 'ok';
    } else if (!m.rutaSalida && m.rutaBase) {
      dif = 'sistema sin ruta';
      clase = 'danger';
    }
    return `<tr>
      <td>${escapar(m.nombre)}<br><span class="badge-mini ${m.decision === 'evacuar' ? 'ok' : m.decision === 'refugiarse' ? 'info' : 'warn'}">${etiquetaDecision(m.decision)}</span></td>
      <td class="mono">${sistema}</td>
      <td class="mono">${base}</td>
      <td><span class="badge-mini ${clase}">${dif}</span></td>
    </tr>`;
  }).join('');

  return `<div class="compare-hero">
      <div class="compare-card system">
        <span>Exposición · sistema experto</span>
        <strong>${expSistema}</strong>
        <small>${fmt(lenSistema)} m de recorrido evaluado</small>
      </div>
      <div class="compare-card">
        <span>Exposición · línea base</span>
        <strong>${expBase}</strong>
        <small>${fmt(lenBase)} m de recorrido evaluado</small>
      </div>
    </div>
    <div class="compare-note">La línea base es un <strong>Dijkstra con filtro por umbral crítico</strong> (D06): ignora los multiplicadores de riesgo y la propagación. La exposición suma el nivel de cada tramo (normal 0 · alerta 1 · alto 2).</div>
    <table class="compare-table">
      <thead><tr><th>Minero</th><th>Sistema</th><th>Base</th><th>Δ</th></tr></thead>
      <tbody>${filas}</tbody>
    </table>
    <div class="compare-foot">${diferencia > 0
      ? `El sistema reduce el índice de exposición en <strong>${diferencia} punto(s)</strong> respecto de la línea base${diferencia >= 2 ? ', evitando tramos que el filtro binario no detecta.' : '.'}`
      : diferencia === 0
        ? 'Ambas estrategias coinciden en exposición para este escenario; el sistema además explica y cuantifica el riesgo de cada tramo.'
        : 'La línea base obtiene menor exposición en este caso porque su filtro bloquea más túneles; el sistema prioriza rutas viables con costo ajustado.'
    }</div>`;
}

function sum(arr) { return arr.reduce((a, b) => a + b, 0); }

/* ============================================================
   MODALES
   ============================================================ */
function abrirModal(eyebrow, titulo, html) {
  $('#modalEyebrow').textContent = eyebrow;
  $('#modalTitle').textContent = titulo;
  $('#modalBody').innerHTML = html;
  $('#modalBackdrop').hidden = false;
  document.body.style.overflow = 'hidden';
}

function cerrarModal() {
  $('#modalBackdrop').hidden = true;
  $('#modalBody').innerHTML = '';
  document.body.style.overflow = '';
}

function abrirCatalogoReglas() {
  const r = state.resultado;
  const grupos = ['DIAG', 'RIESGO', 'RUTA', 'DEC'];
  const html = `<div class="modal-kpis">
      <div class="modal-kpi"><span>Reglas</span><strong>${REGLAS.length}</strong></div>
      <div class="modal-kpi"><span>Norma</span><strong>${REGLAS.filter(x => x.fuente === 'NORMA').length}</strong></div>
      <div class="modal-kpi"><span>Supuesto</span><strong>${REGLAS.filter(x => x.fuente === 'SUPUESTO').length}</strong></div>
      <div class="modal-kpi"><span>Disparadas</span><strong>${r ? r.resumen.reglasUnicas : 0}</strong></div>
    </div>
    <p class="modal-note" style="margin-bottom:14px">Base de conocimiento separada del motor (D03, D13). Cada regla declara si su umbral proviene de la norma o es un supuesto del equipo (D11). La prioridad resuelve conflictos; la refracción evita disparos repetidos.</p>
    ${grupos.map(cat => {
      const regs = REGLAS.filter(x => x.categoria === cat);
      return `<section class="modal-section">
        <h3>${CATEGORIAS[cat].nombre} · ${regs.length} reglas</h3>
        <div class="rule-catalog-grid">
          ${regs.map(reg => {
            const fired = r && r.reglasDisparadas[reg.id];
            return `<div class="rule-catalog-item">
              <div class="rc-left">
                <span class="rule-id">${reg.id}</span>
                <span class="cat-pill ${reg.categoria}">${reg.categoria}</span>
                <span class="source-pill ${reg.fuente}">${reg.fuente}</span>
              </div>
              <div>
                <h4>${escapar(reg.nombre)}</h4>
                <div class="logic"><b>SI</b> ${escapar(reg.si)} <b>→ ENTONCES</b> ${escapar(reg.entonces)}</div>
                <p>${escapar(reg.detalle)}</p>
                <div class="cita">${escapar(reg.cita)}</div>
              </div>
              <div class="rc-right">
                <span class="rule-prio">P${reg.prioridad}</span>
                ${fired ? `<span class="fire-count">${fired.total}×</span>` : '<span class="rule-prio">—</span>'}
              </div>
            </div>`;
          }).join('')}
        </div>
      </section>`;
    }).join('')}`;
  abrirModal('Base de conocimiento', 'Catálogo de reglas', html);
}

function abrirExplicacionTunel(id) {
  const ex = explicarTunel(state.resultado, id);
  const t = ex.tunel;
  const l = ex.lecturas;
  const filasGas = ORDEN_GASES.map(g => {
    const cfg = UMBRALES[g];
    const nivel = nivelGas(l[g], cfg);
    const limite = cfg.tipo === 'min' ? `< ${cfg.alerta}` : `> ${cfg.alerta}`;
    return `<tr>
      <td>${cfg.nombre}</td>
      <td class="mono">${fmt(l[g], g === 'o2' ? 1 : 0)} ${cfg.unidad}</td>
      <td class="mono">${limite} ${cfg.unidad}</td>
      <td><span class="lvl ${nivel}">${nivelTexto(nivel)}</span></td>
    </tr>`;
  }).join('');
  const ventilacion = `<tr>
      <td>Velocidad del aire</td>
      <td class="mono">${fmt(l.vel)} m/min</td>
      <td class="mono">≥ ${UMBRAL_VIENTO.minimo} m/min</td>
      <td><span class="lvl ${l.vel < UMBRAL_VIENTO.minimo ? 'alerta' : 'normal'}">${l.vel < UMBRAL_VIENTO.minimo ? 'Alerta' : 'Normal'}</span></td>
    </tr>`;
  const cadena = ex.reglas.map(reg => `<div class="explain-step regla">
      <h4><span class="rule-tag">${reg.regla}</span>${escapar(reg.nombre)}</h4>
      <p>${escapar(reg.detalle)} <span style="color:#9ca3af">· prioridad ${reg.prioridad} · ${reg.fuente}</span></p>
    </div>`).join('');
  const conflictos = ex.conflictos.length
    ? `<section class="modal-section"><h3>Conflictos resueltos</h3>${ex.conflictos.map(c => `<div class="trace-conflict">${escapar(c.detalle)}</div>`).join('')}</section>`
    : '';
  const conclusion = t.cerrado
    ? `El túnel queda <strong style="color:#dc2626">cerrado</strong>. El planificador lo excluye del grafo y recalcula todas las rutas.`
    : t.nivel === 'normal'
      ? 'El túnel no tiene afectación: conserva su longitud como costo base.'
      : `El túnel sigue <strong>transitable</strong> con un costo de <strong>${fmt(t.costo)}</strong> (${t.longitud} m × ${t.multiplicador}).`;

  abrirModal('Explicación ¿por qué?', t.nombre, `
    <div class="modal-kpis">
      <div class="modal-kpi"><span>Nivel</span><strong>${nivelTexto(t.nivel)}</strong></div>
      <div class="modal-kpi"><span>Multiplicador</span><strong>${t.cerrado ? '—' : `×${t.multiplicador}`}</strong></div>
      <div class="modal-kpi"><span>Longitud</span><strong>${t.longitud} m</strong></div>
      <div class="modal-kpi"><span>Reglas</span><strong>${ex.reglas.length}</strong></div>
    </div>
    <section class="modal-section">
      <h3>Lecturas de sensores</h3>
      <table class="sensor-table">
        <thead><tr><th>Indicador</th><th>Lectura</th><th>Umbral TWA</th><th>Nivel</th></tr></thead>
        <tbody>${filasGas}${ventilacion}</tbody>
      </table>
    </section>
    <section class="modal-section">
      <h3>Cadena de inferencia</h3>
      <div class="explain-chain">${cadena || '<p class="modal-note">Sin reglas disparadas para este túnel.</p>'}</div>
    </section>
    ${conflictos}
    <section class="modal-section">
      <h3>Conclusión</h3>
      <p class="modal-note">${conclusion}</p>
    </section>`);
}

function abrirExplicacionMinero(id) {
  const m = state.resultado.mineros.find(x => x.id === id);
  if (!m) return;
  const pasos = explicarMinero(state.resultado, id);
  const cadena = pasos.map(p => `<div class="explain-step ${p.tipo}">
      <h4>${escapar(p.titulo)}</h4>
      <p>${escapar(p.detalle)}</p>
    </div>`).join('');
  const ruta = m.rutaAsignada
    ? `<div class="route-steps" style="padding:0; flex-wrap:wrap; white-space:normal; gap:5px">${m.rutaAsignada.nodos.map((n, i) => `<span class="step-pill ${i === 0 ? 'start' : i === m.rutaAsignada.nodos.length - 1 ? (m.decision === 'refugiarse' ? 'refugio' : 'end') : ''}">${codigoNodo(n)}</span>`).join('<span class="step-arrow">›</span>')}</div>`
    : '<div class="compare-note" style="margin:0">No hay ruta transitable. El minero permanece en su ubicación y solicita brigada.</div>';
  const comparacion = m.rutaBase
    ? `La línea base llegaría a salida en ${fmt(m.rutaBase.longitud)} m con exposición ${m.rutaBase.exposicion}.`
    : 'La línea base no encuentra ruta a superficie en este escenario.';

  abrirModal('Explicación ¿cómo?', m.nombre, `
    <div class="modal-kpis">
      <div class="modal-kpi"><span>Decisión</span><strong>${etiquetaDecision(m.decision)}</strong></div>
      <div class="modal-kpi"><span>Recorrido</span><strong>${m.rutaAsignada ? `${fmt(m.rutaAsignada.longitud)} m` : '—'}</strong></div>
      <div class="modal-kpi"><span>Costo</span><strong>${m.rutaAsignada ? fmt(m.rutaAsignada.costo) : '—'}</strong></div>
      <div class="modal-kpi"><span>Regla</span><strong>${m.reglaDecision}</strong></div>
    </div>
    <section class="modal-section">
      <h3>Cadena de razonamiento</h3>
      <div class="explain-chain">${cadena}</div>
    </section>
    <section class="modal-section">
      <h3>Ruta asignada</h3>
      ${ruta}
    </section>
    <section class="modal-section">
      <h3>Comparación con la línea base</h3>
      <p class="modal-note">${comparacion}</p>
    </section>`);
}

/* ============================================================
   FORMATO
   ============================================================ */
function fmt(n, dec = 0) {
  if (n === null || n === undefined || Number.isNaN(n)) return '—';
  return Number(n).toLocaleString('es-PE', { minimumFractionDigits: dec, maximumFractionDigits: dec });
}

function nivelTexto(nivel) {
  return { normal: 'Normal', alerta: 'Alerta', alto: 'Riesgo alto', peligro: 'Peligro inmediato' }[nivel] || nivel;
}

function etiquetaDecision(d) {
  return { evacuar: 'Evacuar a superficie', refugiarse: 'Refugiarse', esperar: 'Esperar brigada' }[d] || d;
}

function escapar(texto) {
  return String(texto)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}
