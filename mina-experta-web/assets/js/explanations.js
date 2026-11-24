/* ---------- Explicaciones ---------- */
function explicarTunel(resultado, tunelId) {
  const t = resultado.porTunel[tunelId];
  const reglas = resultado.traza.filter(e => e.tipo === 'regla' && e.entidad === tunelId);
  return {
    tunel: t,
    lecturas: t.lecturas,
    minerosEnRuta: resultado.mineros.filter(m =>
      m.rutaAsignada?.tuneles.some(tramo => tramo.id === tunelId)
    ),
    reglas,
    conflictos: resultado.conflictos.filter(c => c.entidad === tunelId)
  };
}

function explicarMinero(resultado, mineroId) {
  const m = resultado.mineros.find(x => x.id === mineroId);
  if (!m) return [];
  const pasos = [{
    tipo: 'hecho',
    titulo: 'Punto de partida',
    detalle: `${m.nombre} se encuentra en ${m.nodoNombre}.`
  }];

  if (m.cierresEnReferencia.length) {
    const cierres = m.cierresEnReferencia.map(tunel => {
      const cierre = resultado.traza.find(e => e.entidad === tunel.id &&
        (e.regla === 'R-DER-01' || e.regla === 'R-RIESGO-01'));
      return cierre ? `${tunel.nombre} (${cierre.regla})` : tunel.nombre;
    });
    pasos.push({
      tipo: 'regla',
      titulo: 'El camino más corto tiene un cierre',
      detalle: `Por distancia, el camino más corto a superficie pasa por ${cierres.join(', ')}. El planificador excluye esos tramos cerrados.`
    });
  }

  if (m.rutaSalida && m.rutaBase &&
      m.rutaSalida.tuneles.map(t => t.id).join() !== m.rutaBase.tuneles.map(t => t.id).join()) {
    const costoBaseAjustado = m.rutaBase.tuneles.reduce((total, t) => total + t.costo, 0);
    const tramos = m.rutaBase.tuneles.filter(t =>
      t.multiplicador > 1 && !m.rutaSalida.tuneles.some(elegido => elegido.id === t.id)
    );
    const nombres = tramos.map(t => `${t.nombre} (${etiquetaNivel(t.nivel)}, ×${t.multiplicador})`);
    const empate = costoBaseAjustado === m.rutaSalida.costo;
    const desempate = empate && m.rutaSalida.exposicion < m.rutaBase.exposicion
      ? ` Con el mismo costo, el planificador prefiere el menor puntaje de riesgo (${m.rutaSalida.exposicion} frente a ${m.rutaBase.exposicion}).`
      : '';
    pasos.push({
      tipo: 'ruta',
      titulo: m.decision === 'evacuar' ? 'Por qué cambia la ruta a superficie' : 'Comparación de rutas a superficie',
      detalle: `La línea base propone ${m.rutaBase.longitud} m. Con las reglas de riesgo, su costo es ${costoBaseAjustado}. La ruta del sistema recorre ${m.rutaSalida.longitud} m con costo ${m.rutaSalida.costo}.` +
        (nombres.length ? ` La ruta del sistema evita ${nombres.join(', ')}.` : '') + desempate
    });
  }

  if (m.decision === 'refugiarse' && m.rutaSalida) {
    const tramos = m.rutaSalida.tuneles.filter(t => t.nivel === 'alto');
    pasos.push({
      tipo: 'regla',
      titulo: 'La salida cruza tramos de riesgo alto',
      detalle: `La ruta a ${nombreNodo(m.rutaSalida.destino)} pasa por ${tramos.map(t => t.nombre).join(', ')}. Se compara su costo con el de llegar al refugio.`
    });
  }

  pasos.push({
    tipo: 'decision',
    titulo: etiquetaDecision(m.decision),
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
