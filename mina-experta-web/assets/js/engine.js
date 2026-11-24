/* ============================================================
   MINA EXPERTA — Motor de inferencia y planificador
   Forward chaining con prioridad y refracción + Dijkstra.
   Implementación propia, sin librerías externas.
   ============================================================ */

const NIVEL_VALOR = { normal: 0, alerta: 1, alto: 2, peligro: 3 };
const ORDEN_GASES = ['co', 'no2', 'co2', 'h2s', 'o2'];

/* ---------- Utilidades de hechos ---------- */
function valorHecho(f, attr, porDefecto = null) {
  const h = f.get(attr);
  return h === undefined ? porDefecto : h.valor;
}

function prepararLecturas(escenario) {
  const lecturas = {};
  const adyacencia = {};
  TUNELES.forEach(t => { adyacencia[t.id] = []; });
  TUNELES.forEach(t => {
    TUNELES.forEach(o => {
      if (o.id !== t.id && (o.a === t.a || o.a === t.b || o.b === t.a || o.b === t.b)) {
        adyacencia[t.id].push(o.id);
      }
    });
    lecturas[t.id] = { ...SENSORES_BASE, ...(escenario.sensores[t.id] || {}) };
  });
  return { lecturas, adyacencia };
}

/* ---------- Mecánica de cada regla ---------- */
const MECANICAS = {};

const PREFIJO_GAS = { co: 'CO', no2: 'NO2', co2: 'CO2', h2s: 'H2S', o2: 'O2' };
const UMBRAL_NIVEL = { alerta: 'alerta', alto: 'alto', peligro: 'peligro' };

ORDEN_GASES.forEach(gas => {
  const cfg = UMBRALES[gas];
  ['alerta', 'alto', 'peligro'].forEach((nivel, i) => {
    const id = `R-${PREFIJO_GAS[gas]}-0${i + 1}`;
    const umbral = cfg[nivel];
    MECANICAS[id] = {
      cond: f => {
        const v = valorHecho(f, gas);
        return cfg.tipo === 'min' ? v < umbral : v > umbral;
      },
      out: { [`nivel_${gas}`]: nivel },
      detalle: f => `${cfg.nombre} = ${valorHecho(f, gas)} ${cfg.unidad} (umbral ${cfg.tipo === 'min' ? '<' : '>'} ${umbral}) → nivel ${nivel}`
    };
  });
});

MECANICAS['R-VEN-01'] = {
  cond: f => valorHecho(f, 'vel') < UMBRAL_VIENTO.minimo,
  out: { nivel_ventilacion: 'insuficiente' },
  detalle: f => `Velocidad del aire = ${valorHecho(f, 'vel')} m/min (mín. 20) → ventilación insuficiente`
};
MECANICAS['R-VEN-02'] = {
  cond: f => valorHecho(f, 'anfo') === true && valorHecho(f, 'vel') < UMBRAL_VIENTO.minimoAnfo,
  out: { nivel_ventilacion: 'critica' },
  detalle: f => `ANFO activo · velocidad ${valorHecho(f, 'vel')} m/min (mín. 25) → ventilación crítica`
};
MECANICAS['R-VEN-03'] = {
  cond: f => valorHecho(f, 'vel') >= UMBRAL_VIENTO.minimo,
  out: { nivel_ventilacion: 'conforme' },
  detalle: f => `Velocidad ${valorHecho(f, 'vel')} m/min ≥ 20 → ventilación conforme`
};
MECANICAS['R-FUE-01'] = {
  cond: f => valorHecho(f, 'incendio') === true,
  out: { nivel_riesgo: 'peligro' },
  detalle: () => 'Incendio reportado → nivel de riesgo = peligro'
};
MECANICAS['R-DER-01'] = {
  cond: f => valorHecho(f, 'derrumbe') === true,
  out: { cerrado: true },
  detalle: () => 'Derrumbe reportado → túnel cerrado'
};

const NIVELES_GAS_ATTR = ORDEN_GASES.map(g => `nivel_${g}`);

MECANICAS['R-RIESGO-07'] = {
  cond: f => NIVELES_GAS_ATTR.some(a => valorHecho(f, a) === 'peligro'),
  out: { nivel_riesgo: 'peligro' },
  detalle: f => `${resumenNiveles(f, ['peligro'])} → nivel de riesgo = peligro`
};

MECANICAS['R-RIESGO-01'] = {
  cond: f => valorHecho(f, 'nivel_riesgo') === 'peligro',
  out: { cerrado: true },
  detalle: () => 'Nivel de riesgo = peligro → túnel cerrado'
};
MECANICAS['R-RIESGO-02'] = {
  cond: f => NIVELES_GAS_ATTR.some(a => valorHecho(f, a) === 'alto') || valorHecho(f, 'nivel_ventilacion') === 'critica',
  out: { nivel_riesgo: 'alto' },
  detalle: f => `${resumenNiveles(f, ['alto'])} → nivel de riesgo = riesgo alto`
};
MECANICAS['R-RIESGO-03'] = {
  cond: f => NIVELES_GAS_ATTR.some(a => valorHecho(f, a) === 'alerta') ||
    valorHecho(f, 'nivel_ventilacion') === 'insuficiente' ||
    valorHecho(f, 'propagacion') === true,
  out: { nivel_riesgo: 'alerta' },
  detalle: f => `${resumenNiveles(f, ['alerta'])} → nivel de riesgo = alerta`
};
MECANICAS['R-RIESGO-04'] = {
  cond: f => valorHecho(f, 'vecino_evento') === true,
  out: { propagacion: true },
  detalle: () => 'Túnel vecino con incendio o derrumbe → propagación = sí'
};
MECANICAS['R-RIESGO-05'] = {
  cond: f => valorHecho(f, 'nivel_riesgo') === 'alto',
  out: { multiplicador: 3 },
  detalle: () => 'Riesgo alto → multiplicador de costo ×3'
};
MECANICAS['R-RIESGO-06'] = {
  cond: f => valorHecho(f, 'nivel_riesgo') === 'alerta',
  out: { multiplicador: 2 },
  detalle: () => 'Nivel alerta → multiplicador de costo ×2'
};
MECANICAS['R-RUTA-01'] = {
  cond: f => valorHecho(f, 'cerrado') === true,
  out: { transitable: false },
  detalle: () => 'Túnel cerrado → arista bloqueada para el planificador'
};
MECANICAS['R-RUTA-02'] = {
  cond: f => (valorHecho(f, 'multiplicador', 1) || 1) > 1,
  out: { costo_dinamico: true },
  detalle: f => `Multiplicador ×${valorHecho(f, 'multiplicador')} → costo = longitud × multiplicador`
};

function resumenNiveles(f, nivelesBuscados) {
  const partes = [];
  ORDEN_GASES.forEach(g => {
    const v = valorHecho(f, `nivel_${g}`);
    if (v && nivelesBuscados.includes(v)) partes.push(`${UMBRALES[g].nombre} ${v}`);
  });
  if (nivelesBuscados.includes('alerta') && valorHecho(f, 'nivel_ventilacion') === 'insuficiente') partes.push('ventilación insuficiente');
  if (nivelesBuscados.includes('alto') && valorHecho(f, 'nivel_ventilacion') === 'critica') partes.push('ventilación crítica');
  if (nivelesBuscados.includes('alerta') && valorHecho(f, 'propagacion') === true) partes.push('propagación vecina');
  return partes.length ? partes.join(' · ') : 'indicadores en nivel';
}

/* ---------- Motor forward chaining ---------- */
function ejecutarMotor(escenario) {
  const inicio = performance.now();
  const { lecturas, adyacencia } = prepararLecturas(escenario);
  const hechos = new Map();

  TUNELES.forEach(t => {
    const f = new Map();
    const l = lecturas[t.id];
    ['co', 'no2', 'co2', 'h2s', 'o2', 'vel', 'anfo', 'incendio', 'derrumbe'].forEach(attr => {
      f.set(attr, { valor: l[attr], prioridad: 0, regla: 'sensor' });
    });
    const vecinoEvento = adyacencia[t.id].some(id => lecturas[id].incendio || lecturas[id].derrumbe);
    f.set('vecino_evento', { valor: vecinoEvento, prioridad: 0, regla: 'sensor' });
    f.set('nivel_riesgo', { valor: 'normal', prioridad: 0, regla: 'base' });
    f.set('multiplicador', { valor: 1, prioridad: 0, regla: 'base' });
    f.set('cerrado', { valor: false, prioridad: 0, regla: 'base' });
    f.set('transitable', { valor: true, prioridad: 0, regla: 'base' });
    hechos.set(t.id, f);
  });

  const reglasOrdenadas = REGLAS
    .filter(r => MECANICAS[r.id])
    .slice()
    .sort((a, b) => b.prioridad - a.prioridad);

  const disparadas = new Set();
  const traza = [];
  const conflictos = [];
  let paso = 0;
  let iteracion = 0;
  let huboCambio = true;

  while (huboCambio && iteracion < 30) {
    huboCambio = false;
    iteracion++;
    for (const regla of reglasOrdenadas) {
      for (const tunel of TUNELES) {
        const clave = `${regla.id}|${tunel.id}`;
        if (disparadas.has(clave)) continue;
        const f = hechos.get(tunel.id);
        const mec = MECANICAS[regla.id];
        if (!mec.cond(f)) continue;

        let bloqueada = false;
        let reglaGanadora = null;
        Object.entries(mec.out).forEach(([attr, valor]) => {
          const existente = f.get(attr);
          if (existente && existente.prioridad > regla.prioridad && existente.valor !== valor) {
            bloqueada = true;
            reglaGanadora = existente.regla;
          }
        });

        if (bloqueada) {
          disparadas.add(clave);
          if (regla.id === 'R-VEN-03') {
            conflictos.push({
              regla: regla.id,
              contra: reglaGanadora,
              entidad: tunel.id,
              entidadNombre: tunel.nombre,
              detalle: `R-VEN-03 descartada en ${tunel.nombre}: la conclusión ya la fijó ${reglaGanadora} con mayor prioridad y especificidad.`
            });
          }
          continue;
        }

        Object.entries(mec.out).forEach(([attr, valor]) => {
          f.set(attr, { valor, prioridad: regla.prioridad, regla: regla.id });
        });
        disparadas.add(clave);
        huboCambio = true;
        paso++;
        traza.push({
          paso,
          tipo: 'regla',
          regla: regla.id,
          categoria: regla.categoria,
          nombre: regla.nombre,
          entidad: tunel.id,
          entidadNombre: tunel.nombre,
          prioridad: regla.prioridad,
          fuente: regla.fuente,
          detalle: mec.detalle(f)
        });
      }
    }
  }

  const tuneles = TUNELES.map(t => {
    const f = hechos.get(t.id);
    const nivel = valorHecho(f, 'nivel_riesgo', 'normal');
    const cerrado = valorHecho(f, 'cerrado', false) === true;
    const multiplicador = cerrado ? Infinity : (valorHecho(f, 'multiplicador', 1) || 1);
    return {
      ...t,
      lecturas: lecturas[t.id],
      nivel,
      cerrado,
      multiplicador,
      costo: cerrado ? Infinity : Math.round(t.longitud * multiplicador),
      propagacion: valorHecho(f, 'propagacion', false) === true
    };
  });

  const porTunel = Object.fromEntries(tuneles.map(t => [t.id, t]));
  const grafoExperto = construirGrafo(tuneles, 'experto');
  const grafoBase = construirGrafo(tuneles, 'base');

  const mineros = escenario.mineros.map(id => {
    const base = MINEROS_BASE.find(m => m.id === id);
    return resolverMinero(base, grafoExperto, grafoBase, porTunel, tuneles);
  });

  mineros.forEach(m => {
    paso++;
    traza.push({
      paso,
      tipo: 'decision',
      regla: m.reglaDecision,
      categoria: 'DEC',
      nombre: m.decision === 'evacuar' ? 'Evacuar a superficie' : m.decision === 'refugiarse' ? 'Refugiarse' : 'Esperar brigada',
      entidad: m.id,
      entidadNombre: m.nombre,
      prioridad: 70,
      fuente: 'SUPUESTO',
      detalle: m.justificacion
    });
  });

  const reglasDisparadas = {};
  traza.filter(e => e.tipo === 'regla' || e.tipo === 'decision').forEach(e => {
    if (!reglasDisparadas[e.regla]) reglasDisparadas[e.regla] = { regla: e.regla, total: 0, tuneles: new Set() };
    reglasDisparadas[e.regla].total++;
    reglasDisparadas[e.regla].tuneles.add(e.entidadNombre);
  });
  Object.values(reglasDisparadas).forEach(r => { r.tuneles = [...r.tuneles]; });

  const duracion = Math.max(1, Math.round(performance.now() - inicio));

  return {
    escenario,
    tuneles,
    porTunel,
    mineros,
    traza,
    conflictos,
    reglasDisparadas,
    resumen: {
      cerrados: tuneles.filter(t => t.cerrado).length,
      alto: tuneles.filter(t => t.nivel === 'alto').length,
      alerta: tuneles.filter(t => t.nivel === 'alerta').length,
      normales: tuneles.filter(t => t.nivel === 'normal').length,
      reglas: traza.filter(e => e.tipo === 'regla').length,
      reglasUnicas: Object.keys(reglasDisparadas).length,
      conflictos: conflictos.length,
      evacuando: mineros.filter(m => m.decision === 'evacuar').length,
      refugiados: mineros.filter(m => m.decision === 'refugiarse').length,
      esperando: mineros.filter(m => m.decision === 'esperar').length,
      duracion,
      iteraciones: iteracion
    }
  };
}

/* ---------- Grafo y Dijkstra ---------- */
function construirGrafo(tuneles, modo) {
  const adj = new Map();
  NODOS.forEach(n => adj.set(n.id, []));
  tuneles.forEach(t => {
    if (modo === 'experto' && t.cerrado) return;
    if (modo === 'base' && esBloqueoBase(t)) return;
    const peso = modo === 'experto' ? t.costo : t.longitud;
    adj.get(t.a).push({ nodo: t.b, peso, tunel: t });
    adj.get(t.b).push({ nodo: t.a, peso, tunel: t });
  });
  return adj;
}

function esBloqueoBase(t) {
  if (t.lecturas.incendio || t.lecturas.derrumbe) return true;
  return ORDEN_GASES.some(g => nivelGas(t.lecturas[g], UMBRALES[g]) === 'peligro');
}

function dijkstra(adj, inicio, desempatarRiesgo = false) {
  const dist = new Map();
  const riesgo = new Map();
  const prev = new Map();
  NODOS.forEach(n => { dist.set(n.id, Infinity); riesgo.set(n.id, Infinity); });
  dist.set(inicio, 0);
  riesgo.set(inicio, 0);
  const pendientes = new Set(NODOS.map(n => n.id));

  while (pendientes.size) {
    let actual = null;
    let mejor = Infinity;
    pendientes.forEach(id => {
      if (dist.get(id) < mejor) { mejor = dist.get(id); actual = id; }
    });
    if (actual === null) break;
    pendientes.delete(actual);

    for (const arista of adj.get(actual) || []) {
      const alt = dist.get(actual) + arista.peso;
      const altRiesgo = riesgo.get(actual) + (desempatarRiesgo ? NIVEL_VALOR[arista.tunel.nivel] : 0);
      const actualDist = dist.get(arista.nodo);
      const mismoCosto = Math.abs(alt - actualDist) < 0.0001;
      if (alt < actualDist || (mismoCosto && altRiesgo < riesgo.get(arista.nodo))) {
        dist.set(arista.nodo, alt);
        riesgo.set(arista.nodo, altRiesgo);
        prev.set(arista.nodo, { desde: actual, tunel: arista.tunel });
      }
    }
  }
  return { dist, prev };
}

function reconstruir(prev, inicio, destino) {
  const nodos = [destino];
  const tuneles = [];
  let actual = destino;
  let guardia = 0;
  while (actual !== inicio && prev.has(actual) && guardia++ < 100) {
    const p = prev.get(actual);
    tuneles.push(p.tunel);
    actual = p.desde;
    nodos.push(actual);
  }
  if (actual !== inicio) return null;
  nodos.reverse();
  tuneles.reverse();
  return { nodos, tuneles };
}

function mejorRuta(adj, inicio, destinos, desempatarRiesgo = false) {
  const { dist, prev } = dijkstra(adj, inicio, desempatarRiesgo);
  let destino = null;
  let mejor = Infinity;
  destinos.forEach(id => {
    if (dist.has(id) && dist.get(id) < mejor) { mejor = dist.get(id); destino = id; }
  });
  if (destino === null || !isFinite(mejor)) return null;
  const camino = reconstruir(prev, inicio, destino);
  if (!camino) return null;
  const longitud = camino.tuneles.reduce((s, t) => s + t.longitud, 0);
  return {
    ...camino,
    destino,
    costo: Math.round(mejor),
    longitud: Math.round(longitud),
    exposicion: exponerRuta(camino.tuneles),
    tramosAlto: camino.tuneles.filter(t => t.nivel === 'alto').length,
    tramosAlerta: camino.tuneles.filter(t => t.nivel === 'alerta').length
  };
}

function exponerRuta(tuneles) {
  return tuneles.reduce((s, t) => s + NIVEL_VALOR[t.nivel], 0);
}

/* ---------- Decisión por minero ---------- */
function resolverMinero(minero, grafoExperto, grafoBase, porTunel, tuneles) {
  const salidas = NODOS.filter(n => n.salida).map(n => n.id);
  const refugios = NODOS.filter(n => n.tipo === 'refugio').map(n => n.id);

  const rutaSalida = mejorRuta(grafoExperto, minero.nodo, salidas, true);
  const rutaRefugio = mejorRuta(grafoExperto, minero.nodo, refugios, true);
  const rutaBase = mejorRuta(grafoBase, minero.nodo, salidas, false);

  let decision = 'evacuar';
  let reglaDecision = 'DEC-01';
  let justificacion = '';
  let motivo = '';
  let rutaAsignada = rutaSalida;

  if (!rutaSalida) {
    if (rutaRefugio) {
      decision = 'refugiarse';
      reglaDecision = 'DEC-02';
      rutaAsignada = rutaRefugio;
      justificacion = `Sin ruta viable a superficie. El ${nombreNodo(rutaRefugio.destino)} está a ${rutaRefugio.longitud} m y es alcanzable.`;
      motivo = 'Sin ruta a salida';
    } else {
      decision = 'esperar';
      reglaDecision = 'DEC-03';
      rutaAsignada = null;
      justificacion = 'Sin ruta a superficie y sin refugio alcanzable. Se solicita brigada de rescate y se mantiene comunicación.';
      motivo = 'Aislado por derrumbe';
    }
  } else {
    const ratio = rutaRefugio ? rutaSalida.costo / Math.max(rutaRefugio.costo, 1) : Infinity;
    const refugioCercano = rutaRefugio && rutaRefugio.longitud <= 400;
    const expuesta = rutaSalida.tramosAlto >= 1 && ratio > 2.5 && refugioCercano;
    if (expuesta) {
      decision = 'refugiarse';
      reglaDecision = 'DEC-02';
      rutaAsignada = rutaRefugio;
      justificacion = `La ruta a superficie cuesta ${rutaSalida.costo} y cruza ${rutaSalida.tramosAlto} tramo(s) de riesgo alto. El ${nombreNodo(rutaRefugio.destino)} está a ${rutaRefugio.longitud} m (costo ${rutaRefugio.costo}).`;
      motivo = 'Ruta de evacuación muy expuesta';
    } else {
      decision = 'evacuar';
      reglaDecision = 'DEC-01';
      rutaAsignada = rutaSalida;
      justificacion = `Ruta a ${nombreNodo(rutaSalida.destino)} viable: ${rutaSalida.longitud} m de recorrido, costo ajustado ${rutaSalida.costo}.`;
      motivo = rutaSalida.tramosAlto ? 'Evacúa con protección respiratoria' : 'Ruta despejada';
    }
  }

  const exposicionBase = rutaBase ? rutaBase.exposicion : null;

  return {
    ...minero,
    nodoNombre: nombreNodo(minero.nodo),
    decision,
    reglaDecision,
    justificacion,
    motivo,
    rutaSalida,
    rutaRefugio,
    rutaBase,
    rutaAsignada,
    exposicion: rutaSalida ? rutaSalida.exposicion : null,
    exposicionBase,
    longitud: rutaSalida ? rutaSalida.longitud : null,
    longitudBase: rutaBase ? rutaBase.longitud : null
  };
}

function nombreNodo(id) {
  const n = NODOS.find(x => x.id === id);
  return n ? n.nombre : id;
}

function nivelGas(valor, cfg) {
  if (cfg.tipo === 'min') {
    if (valor < cfg.peligro) return 'peligro';
    if (valor < cfg.alto) return 'alto';
    if (valor < cfg.alerta) return 'alerta';
    return 'normal';
  }
  if (valor > cfg.peligro) return 'peligro';
  if (valor > cfg.alto) return 'alto';
  if (valor > cfg.alerta) return 'alerta';
  return 'normal';
}

/* ---------- Explicaciones ---------- */
function explicarTunel(resultado, tunelId) {
  const t = resultado.porTunel[tunelId];
  const reglas = resultado.traza.filter(e => e.tipo === 'regla' && e.entidad === tunelId);
  return {
    tunel: t,
    lecturas: t.lecturas,
    reglas,
    conflictos: resultado.conflictos.filter(c => c.entidad === tunelId)
  };
}

function explicarMinero(resultado, mineroId) {
  const m = resultado.mineros.find(x => x.id === mineroId);
  const pasos = [];
  pasos.push({ tipo: 'hecho', titulo: 'Ubicación conocida', detalle: `${m.nombre} se encuentra en ${m.nodoNombre}.` });

  const tunelesAsignados = m.rutaAsignada ? m.rutaAsignada.tuneles : [];
  if (tunelesAsignados.length) {
    const riesgos = tunelesAsignados.filter(t => t.nivel !== 'normal');
    pasos.push({
      tipo: 'ruta',
      titulo: 'Ruta evaluada por el planificador',
      detalle: `${m.rutaAsignada.longitud} m · costo ajustado ${m.rutaAsignada.costo} · ${riesgos.length} tramo(s) con riesgo.`
    });
    riesgos.slice(0, 4).forEach(t => {
      const reglas = resultado.traza.filter(e => e.entidad === t.id && e.tipo === 'regla').slice(-2);
      pasos.push({
        tipo: 'regla',
        titulo: `${t.nombre} · ${etiquetaNivel(t.nivel)}`,
        detalle: reglas.length ? reglas.map(r => `${r.regla}: ${r.detalle}`).join(' · ') : `Multiplicador ×${t.multiplicador}.`
      });
    });
  }

  if (m.rutaRefugio) {
    pasos.push({
      tipo: 'hecho',
      titulo: 'Alternativa de refugio',
      detalle: `${nombreNodo(m.rutaRefugio.destino)} a ${m.rutaRefugio.longitud} m, costo ${m.rutaRefugio.costo}.`
    });
  }

  pasos.push({
    tipo: 'decision',
    titulo: `Decisión: ${etiquetaDecision(m.decision)}`,
    detalle: `${m.reglaDecision} · ${m.justificacion}`
  });
  return pasos;
}

function etiquetaNivel(nivel) {
  return { normal: 'Normal', alerta: 'Alerta', alto: 'Riesgo alto', peligro: 'Peligro inmediato' }[nivel] || nivel;
}

function etiquetaDecision(d) {
  return { evacuar: 'Evacuar a superficie', refugiarse: 'Refugiarse', esperar: 'Esperar brigada' }[d] || d;
}

function nombreRegla(id) {
  const r = REGLAS.find(x => x.id === id);
  return r ? r.nombre : id;
}
