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
