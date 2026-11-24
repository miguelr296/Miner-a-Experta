/* ============================================================
   MINA EXPERTA — Motor de inferencia
   Forward chaining con prioridad y refracción + Dijkstra.
   Implementación propia, sin librerías externas.
   ============================================================ */

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
function inferirTuneles(escenario) {
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
        const lecturasRegla = new Map();
        const memoriaConsultada = {
          get(atributo) {
            const hecho = f.get(atributo);
            lecturasRegla.set(atributo, { atributo, valor: hecho?.valor, origen: hecho?.regla });
            return hecho;
          }
        };
        if (!mec.cond(memoriaConsultada)) continue;

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

        const escrituras = Object.entries(mec.out).map(([atributo, valor]) => {
          const anterior = f.get(atributo)?.valor;
          f.set(atributo, { valor, prioridad: regla.prioridad, regla: regla.id });
          return { atributo, anterior, valor };
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
          lecturas: [...lecturasRegla.values()],
          escrituras,
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

  return { tuneles, traza, conflictos, paso, iteracion };
}

/* ---------- Ejecución de un escenario ---------- */
function ejecutarMotor(escenario) {
  const inicio = performance.now();
  const { tuneles, traza, conflictos, iteracion, paso: ultimoPaso } = inferirTuneles(escenario);
  let paso = ultimoPaso;
  const porTunel = Object.fromEntries(tuneles.map(t => [t.id, t]));
  const grafoExperto = construirGrafo(tuneles, 'experto');
  const grafoBase = construirGrafo(tuneles, 'base');
  const grafoPorDistancia = construirGrafo(tuneles, 'distancia');

  const mineros = escenario.mineros.map(id => {
    const base = MINEROS_BASE.find(m => m.id === id);
    return resolverMinero(base, grafoExperto, grafoBase, grafoPorDistancia);
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
