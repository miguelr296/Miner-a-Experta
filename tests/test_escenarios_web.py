"""Comprobaciones del motor JavaScript para reglas, rutas y escenarios de referencia."""

from pathlib import Path
import subprocess


ARCHIVOS_JS = (
    Path(__file__).resolve().parents[1] / "mina-experta-web" / "assets" / "js"
)


def ejecutar_comprobacion(comprobacion):
    fuentes = [
        (ARCHIVOS_JS / archivo).read_text(encoding="utf-8-sig")
        for archivo in ("data.js", "engine.js", "planner.js", "casos.js", "explanations.js")
    ]
    programa = "\n".join([*fuentes, 'const assert = require("node:assert/strict");', comprobacion])
    subprocess.run(["node", "-"], input=programa.encode("utf-8"), check=True, cwd=ARCHIVOS_JS.parents[2])


def test_inundacion_cierra_la_rampa():
    ejecutar_comprobacion("""
const escenario = ESCENARIOS.find(e => e.id === 'ESC-04');
const tramo = 't_r4_s2';
const resultado = ejecutarMotor(escenario);
assert.equal(resultado.porTunel[tramo].cerrado, true);
assert.deepEqual(
  resultado.traza.filter(e => e.entidad === tramo && ['R-INU-01', 'R-RIESGO-01', 'R-RUTA-01'].includes(e.regla))
    .map(e => e.regla),
  ['R-INU-01', 'R-RIESGO-01', 'R-RUTA-01']
);
assert.equal(resultado.mineros.find(m => m.id === 'm4').rutaAsignada.destino, 's1');
assert.ok(resultado.mineros.every(m => m.rutaBase.destino !== 's2'));
const sinReporte = ejecutarMotor({ ...escenario, sensores: {} });
assert.equal(sinReporte.porTunel[tramo].cerrado, false);
assert.equal(sinReporte.mineros.find(m => m.id === 'm4').rutaAsignada.destino, 's2');
""")


def test_corte_electrico_distingue_el_respaldo():
    ejecutar_comprobacion("""
const escenario = ESCENARIOS.find(e => e.id === 'ESC-05');
const resultado = ejecutarMotor(escenario);
const sinRespaldo = resultado.porTunel.t_i1_i2;
assert.equal(sinRespaldo.ventilacion, 'critica');
assert.equal(sinRespaldo.nivel, 'alto');
assert.equal(sinRespaldo.cerrado, false);
assert.equal(sinRespaldo.costo, sinRespaldo.longitud * 3);
assert.equal(resultado.porTunel.t_i3_i6.ventilacion, 'conforme');
assert.deepEqual(
  resultado.traza.filter(e => e.regla === 'R-VEN-04').map(e => e.entidad), ['t_i1_i2']
);
const jorge = resultado.mineros.find(m => m.id === 'm1');
assert.equal(jorge.rutaBase.longitud, 470);
assert.equal(jorge.rutaAsignada.longitud, 480);
assert.ok(jorge.rutaAsignada.tuneles.every(t => t.id !== sinRespaldo.id));
""")


def test_resultados_de_los_cinco_escenarios():
    ejecutar_comprobacion("""
const fixture = JSON.parse(require('node:fs').readFileSync('tests/fixtures/escenarios_web.json', 'utf8'));
assert.equal(fixture.version, 1);
assert.deepEqual(Object.keys(fixture.casos), ESCENARIOS.map(e => e.id));

function resumirRuta(ruta) {
  if (!ruta) return null;
  const { destino, nodos, longitud, costo, exposicion } = ruta;
  return { destino, nodos, longitud, costo, puntajeRiesgo: exposicion };
}

for (const escenario of ESCENARIOS) {
  const { entrada, esperado } = fixture.casos[escenario.id];
  const { sensores, mineros } = escenario;
  assert.deepEqual({ sensores, mineros }, entrada, escenario.id + ': entrada');
  const resultado = ejecutarMotor(escenario);
  const tunelesAfectados = resultado.tuneles.filter(t => t.cerrado || t.nivel !== 'normal')
    .map(t => [t.id, t.nivel, t.cerrado, t.cerrado ? null : t.costo]);
  const decisiones = resultado.mineros.map(m => ({
    id: m.id,
    decision: m.decision,
    regla: m.reglaDecision,
    asignada: resumirRuta(m.rutaAsignada),
    lineaBase: resumirRuta(m.rutaBase)
  }));
  assert.deepEqual({ tunelesAfectados, mineros: decisiones }, esperado, escenario.id);

  for (const m of resultado.mineros) {
    assert.ok(!m.rutaAsignada?.tuneles.some(t => t.cerrado), escenario.id + ': ' + m.id);
  }
}
""")


def test_limites_estrictos_de_gases():
    ejecutar_comprobacion("""
const tramo = 't_i2_f1';
for (const gas of ORDEN_GASES) {
  const umbral = UMBRALES[gas];
  const delta = umbral.tipo === 'min' ? -0.01 : 0.01;
  for (const [nivel, inferior] of [['alerta', 'normal'], ['alto', 'alerta'], ['peligro', 'alto']]) {
    const limite = umbral[nivel];
    for (const [valor, esperado] of [[limite - delta, inferior], [limite, inferior], [limite + delta, nivel]]) {
      const r = ejecutarMotor({ sensores: { [tramo]: { [gas]: valor } }, mineros: ['m1'] });
      const mensaje = gas + ' ' + valor;
      assert.equal(nivelGas(valor, umbral), esperado, mensaje);
      assert.equal(r.porTunel[tramo].nivel, esperado, mensaje);
      assert.equal(r.porTunel[tramo].cerrado, esperado === 'peligro', mensaje);
    }
  }
}
""")


def test_reglas_simultaneas_preservan_el_riesgo_mayor_y_la_traza():
    ejecutar_comprobacion("""
const tramo = 't_i2_f1';
const alerta = crearReglaSimulada('SIM-01', 'co', '>', 0, 'alerta');
const alto = crearReglaSimulada('SIM-02', 'co', '>', 0, 'alto');
const entrada = { sensores: { [tramo]: { co: 101, anfo: true, vel: 23 } }, mineros: ['m1'] };
for (const reglas of [[alerta, alto], [alto, alerta]]) {
  const r = ejecutarMotor(entrada, reglas);
  const tunel = r.porTunel[tramo];
  assert.equal(tunel.nivel, 'peligro');
  assert.equal(tunel.ventilacion, 'critica');
  assert.equal(tunel.cerrado, true);
  assert.ok(r.conflictos.some(c => c.entidad === tramo && c.regla === 'R-VEN-03' && c.contra === 'R-VEN-02'));
  const reglaIds = r.traza.filter(p => p.entidad === tramo).map(p => p.regla);
  assert.equal(reglaIds.length, new Set(reglaIds).size);
  const cierre = r.traza.find(p => p.entidad === tramo && p.regla === 'R-RIESGO-01');
  assert.equal(cierre.lecturas[0].origen, 'R-RIESGO-07');
  assert.deepEqual(cierre.escrituras, [{ atributo: 'cerrado', anterior: false, valor: true }]);
}
""")


def test_esperar_sin_salida_ni_refugio_y_refugiarse_si_hay_acceso():
    ejecutar_comprobacion("""
const aislado = ejecutarMotor({ sensores: { t_i2_f1: { derrumbe: true } }, mineros: ['m1'] });
assert.equal(aislado.mineros[0].reglaDecision, 'DEC-03');
assert.equal(aislado.mineros[0].rutaSalida, null);
assert.equal(aislado.mineros[0].rutaRefugio, null);
assert.equal(aislado.mineros[0].rutaAsignada, null);
const sinSalidas = ejecutarMotor({
  sensores: { t_s1_i1: { derrumbe: true }, t_r4_s2: { derrumbe: true } }, mineros: ['m1']
});
assert.equal(sinSalidas.mineros[0].reglaDecision, 'DEC-02');
assert.equal(sinSalidas.mineros[0].rutaSalida, null);
assert.equal(sinSalidas.mineros[0].rutaAsignada.destino, 'r1');
""")


def test_empate_de_costo_entre_rutas_y_destinos():
    ejecutar_comprobacion("""
function arista(nodo, peso, nivel) {
  return { nodo, peso, tunel: { nivel, longitud: peso } };
}
const grafo = new Map([
  ['i1', [arista('i2', 1, 'alto'), arista('i3', 2, 'normal')]],
  ['i2', [arista('s1', 3, 'normal')]],
  ['i3', [arista('s1', 2, 'normal'), arista('s2', 2, 'normal')]]
]);
assert.deepEqual(mejorRuta(grafo, 'i1', ['s1'], true).nodos, ['i1', 'i3', 's1']);
const destinos = new Map([['i1', [arista('s1', 4, 'alto'), arista('s2', 4, 'normal')]]]);
assert.equal(mejorRuta(destinos, 'i1', ['s1', 's2'], true).destino, 's2');
assert.equal(mejorRuta(destinos, 'i1', ['s2', 's1'], true).destino, 's2');
assert.equal(mejorRuta(destinos, 'i1', ['s1', 's2'], false).destino, 's1');
assert.equal(mejorRuta(destinos, 'i1', ['r1', 'r2'], true), null);
""")


def test_intercambio_reproduce_una_regla_sin_ejecutar_codigo_del_archivo():
    ejecutar_comprobacion("""
const escenario = ESCENARIOS[0];
const regla = crearReglaSimulada('SIM-01', 'co', '>', 80, 'peligro');
const recuperado = importarCaso(exportarCaso(escenario, [regla]));
const reglas = recuperado.reglasDelCaso.map(r => crearReglaSimulada(r.id, r.sensor, r.operador, r.umbral, r.nivel));
assert.equal(ejecutarMotor(recuperado, reglas).mineros[0].reglaDecision, 'DEC-03');
const sinRegla = importarCaso(exportarCaso(escenario, null));
assert.deepEqual(sinRegla.reglasDelCaso, []);
assert.equal(ejecutarMotor(sinRegla).mineros[0].reglaDecision, 'DEC-01');
const invalido = JSON.parse(exportarCaso(escenario, [regla]));
invalido.reglas[0].umbral = '80';
assert.throws(() => importarCaso(JSON.stringify(invalido)), /umbral válido/);
""")


def test_comparacion_del_recalculo():
    ejecutar_comprobacion("""
const entrada = ESCENARIOS[0];
const antes = ejecutarMotor(entrada);
const tramo = 't_i2_f1';
const conCierre = ejecutarMotor({
  ...entrada,
  sensores: { ...entrada.sensores, [tramo]: { ...entrada.sensores[tramo], co: 101 } }
});
const cambios = compararResultados(antes, conCierre);
assert.deepEqual(cambios.tuneles.map(c => c.actual.id), [tramo]);
assert.equal(cambios.tuneles[0].previo.cerrado, false);
assert.equal(cambios.tuneles[0].actual.cerrado, true);
assert.equal(cambios.decisiones, 1);
assert.equal(cambios.rutas, 1);
assert.deepEqual(cambios.mineros.map(c => c.actual.id), ['m1']);

const normal = { sensores: {}, mineros: ['m1'] };
const conAlerta = { ...normal, sensores: { [tramo]: { co: 30 } } };
const soloCosto = compararResultados(ejecutarMotor(normal), ejecutarMotor(conAlerta));
assert.equal(soloCosto.rutas, 0);
assert.equal(soloCosto.decisiones, 0);
assert.equal(soloCosto.mineros.length, 1);
assert.ok(soloCosto.mineros[0].actual.rutaAsignada.costo > soloCosto.mineros[0].previo.rutaAsignada.costo);
assert.deepEqual(compararResultados(antes, ejecutarMotor(entrada)), {
  tuneles: [], mineros: [], decisiones: 0, rutas: 0
});
""")
