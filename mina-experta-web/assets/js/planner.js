/* Planificación de rutas y decisión por minero. */

const NIVEL_VALOR = { normal: 0, alerta: 1, alto: 2, peligro: 3 };

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
function resolverMinero(minero, grafoExperto, grafoBase) {
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
