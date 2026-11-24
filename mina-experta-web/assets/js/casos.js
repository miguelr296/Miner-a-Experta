/* Formato de intercambio para la topología incluida en el prototipo. */
const FORMATO_CASO = 'mina-experta/caso';
const VERSION_CASO = 1;

function exportarCaso(escenario, reglas) {
  const { nombre, descripcion, hora, sensores, mineros } = escenario;
  return JSON.stringify({
    formato: FORMATO_CASO,
    version: VERSION_CASO,
    escenario: { nombre, descripcion, hora, sensores, mineros },
    ...(reglas ? { reglas: reglas.map(r => r.definicion) } : {})
  }, null, 2);
}

function importarCaso(texto) {
  let caso;
  try {
    caso = JSON.parse(texto);
  } catch {
    throw new Error('El archivo no contiene JSON válido.');
  }
  if (caso?.formato !== FORMATO_CASO || caso.version !== VERSION_CASO) {
    throw new Error('El formato o la versión del archivo no es compatible.');
  }

  const e = caso.escenario;
  const nombre = typeof e?.nombre === 'string' ? e.nombre.trim() : '';
  if (!nombre || nombre.length > 60 || typeof e.descripcion !== 'string' ||
      e.descripcion.length > 240 || typeof e.hora !== 'string' || !/^([01]\d|2[0-3]):[0-5]\d$/.test(e.hora) ||
      !Array.isArray(e.mineros) || !e.mineros.length || new Set(e.mineros).size !== e.mineros.length ||
      !e.mineros.every(id => MINEROS_BASE.some(m => m.id === id)) ||
      !e.sensores || typeof e.sensores !== 'object' || Array.isArray(e.sensores)) {
    throw new Error('El archivo contiene datos de escenario no válidos.');
  }

  for (const [id, lecturas] of Object.entries(e.sensores)) {
    if (!TUNELES.some(t => t.id === id) || !lecturas || typeof lecturas !== 'object' || Array.isArray(lecturas) ||
        Object.entries(lecturas).some(([clave, valor]) => !Object.hasOwn(SENSORES_BASE, clave) ||
          (typeof SENSORES_BASE[clave] === 'boolean' ? typeof valor !== 'boolean' : !Number.isFinite(valor) || valor < 0))) {
      throw new Error('El archivo contiene túneles, lecturas o eventos no válidos.');
    }
  }

  const reglas = Object.hasOwn(caso, 'reglas') ? caso.reglas : [];
  if (!Array.isArray(reglas)) throw new Error('Las reglas deben estar en una lista.');
  const ids = new Set();
  const reglasDelCaso = reglas.map(r => {
    if (!r || typeof r.id !== 'string' || !/^SIM-[0-9]+$/.test(r.id) || ids.has(r.id)) {
      throw new Error('El archivo contiene identificadores de reglas no válidos o duplicados.');
    }
    ids.add(r.id);
    return crearReglaSimulada(r.id, r.sensor, r.operador, r.umbral, r.nivel).definicion;
  });
  return { nombre, descripcion: e.descripcion, hora: e.hora, sensores: e.sensores, mineros: e.mineros, reglasDelCaso };
}
