/* ============================================================
   MINA EXPERTA — Base de conocimiento y escenarios
   Prototipo de interfaz · datos ficticios con umbrales del
   DS 024-2016-EM (valores de exposición laboral).
   ============================================================ */

const MINA = {
  nombre: 'Unidad Minera San Rafael',
  tipo: 'Mina metálica subterránea · Polimetálica',
  socavon: 'Socavón Principal',
  niveles: [
    { id: 1, nombre: 'Nivel 1', cota: 340 },
    { id: 2, nombre: 'Nivel 2', cota: 280 }
  ]
};

/* Nodos: coordenadas de dibujo y conexión real del grafo.
   tipo: salida | refugio | frente | interseccion */
const NODOS = [
  { id: 's1', nombre: 'Socavón Principal', corto: 'SOC-1', tipo: 'salida', nivel: 1, x: 92, y: 225, salida: true },
  { id: 'i1', nombre: 'Cruce Norte', corto: 'CRU-N', tipo: 'interseccion', nivel: 1, x: 252, y: 225 },
  { id: 'i2', nombre: 'Galería 340', corto: 'GAL-340', tipo: 'interseccion', nivel: 1, x: 420, y: 140 },
  { id: 'i3', nombre: 'Bifurcación Este', corto: 'BIF-E', tipo: 'interseccion', nivel: 1, x: 420, y: 320 },
  { id: 'i6', nombre: 'Crucero Central', corto: 'CRU-C', tipo: 'interseccion', nivel: 1, x: 420, y: 230 },
  { id: 'r1', nombre: 'Refugio R-1', corto: 'R-1', tipo: 'refugio', nivel: 1, x: 592, y: 225 },
  { id: 'f1', nombre: 'Frente 340-N', corto: 'F-340N', tipo: 'frente', nivel: 1, x: 592, y: 92 },
  { id: 'f2', nombre: 'Frente 340-S', corto: 'F-340S', tipo: 'frente', nivel: 1, x: 592, y: 352 },
  { id: 'r2', nombre: 'Refugio R-2', corto: 'R-2', tipo: 'refugio', nivel: 1, x: 760, y: 225 },
  { id: 'i4', nombre: 'Galería 280', corto: 'GAL-280', tipo: 'interseccion', nivel: 2, x: 225, y: 570 },
  { id: 'r3', nombre: 'Refugio R-3', corto: 'R-3', tipo: 'refugio', nivel: 2, x: 392, y: 570 },
  { id: 'f3', nombre: 'Frente 280-N', corto: 'F-280N', tipo: 'frente', nivel: 2, x: 558, y: 482 },
  { id: 'i5', nombre: 'Cruce Sur', corto: 'CRU-S', tipo: 'interseccion', nivel: 2, x: 558, y: 668 },
  { id: 'f4', nombre: 'Frente 280-S', corto: 'F-280S', tipo: 'frente', nivel: 2, x: 742, y: 722 },
  { id: 'r4', nombre: 'Refugio R-4', corto: 'R-4', tipo: 'refugio', nivel: 2, x: 750, y: 570 },
  { id: 's2', nombre: 'Rampa de Escape', corto: 'RAM-2', tipo: 'salida', nivel: 2, x: 900, y: 570, salida: true }
];

/* Túneles (aristas). longitud en metros. */
const TUNELES = [
  { id: 't_s1_i1', nombre: 'Galería Principal', a: 's1', b: 'i1', longitud: 150, via: 'galeria' },
  { id: 't_i1_i2', nombre: 'Crucero Norte', a: 'i1', b: 'i2', longitud: 175, via: 'galeria' },
  { id: 't_i1_i3', nombre: 'Galería 340', a: 'i1', b: 'i3', longitud: 180, via: 'galeria' },
  { id: 't_i1_i6', nombre: 'By-pass Central', a: 'i1', b: 'i6', longitud: 95, via: 'galeria' },
  { id: 't_i2_i6', nombre: 'Crucero Central', a: 'i2', b: 'i6', longitud: 90, via: 'galeria' },
  { id: 't_i3_i6', nombre: 'Rampa Central', a: 'i3', b: 'i6', longitud: 90, via: 'rampa' },
  { id: 't_i2_f1', nombre: 'Galería 340-N', a: 'i2', b: 'f1', longitud: 145, via: 'galeria' },
  { id: 't_i3_f2', nombre: 'Galería 340-S', a: 'i3', b: 'f2', longitud: 155, via: 'galeria' },
  { id: 't_i2_r1', nombre: 'By-pass Norte', a: 'i2', b: 'r1', longitud: 185, via: 'galeria' },
  { id: 't_i3_r1', nombre: 'By-pass Sur', a: 'i3', b: 'r1', longitud: 190, via: 'galeria' },
  { id: 't_r1_r2', nombre: 'Galería Este', a: 'r1', b: 'r2', longitud: 175, via: 'galeria' },
  { id: 't_r2_r4', nombre: 'Chimenea Norte', a: 'r2', b: 'r4', longitud: 60, via: 'chimenea' },
  { id: 't_i1_i4', nombre: 'Rampa Norte', a: 'i1', b: 'i4', longitud: 220, via: 'rampa' },
  { id: 't_i4_r3', nombre: 'Galería 280', a: 'i4', b: 'r3', longitud: 175, via: 'galeria' },
  { id: 't_r3_f3', nombre: 'Galería 280-N', a: 'r3', b: 'f3', longitud: 175, via: 'galeria' },
  { id: 't_f3_i5', nombre: 'Bajada Norte', a: 'f3', b: 'i5', longitud: 190, via: 'rampa' },
  { id: 't_r3_i5', nombre: 'Bajada Sur', a: 'r3', b: 'i5', longitud: 175, via: 'rampa' },
  { id: 't_i5_f4', nombre: 'Galería 280-S', a: 'i5', b: 'f4', longitud: 195, via: 'galeria' },
  { id: 't_i5_r4', nombre: 'Crucero Sur', a: 'i5', b: 'r4', longitud: 195, via: 'galeria' },
  { id: 't_r4_f4', nombre: 'By-pass 280-S', a: 'r4', b: 'f4', longitud: 155, via: 'galeria' },
  { id: 't_r4_s2', nombre: 'Rampa de Escape', a: 'r4', b: 's2', longitud: 155, via: 'rampa' }
];

/* Sensores por defecto: aire limpio y ventilación normal. */
const SENSORES_BASE = {
  co: 4,          // ppm
  no2: 0.4,       // ppm
  co2: 420,       // ppm
  h2s: 0.1,       // ppm
  o2: 20.9,       // %
  vel: 85,        // m/min
  anfo: false,
  incendio: false,
  derrumbe: false
};

const MINEROS_BASE = [
  { id: 'm1', nombre: 'Jorge Salazar', iniciales: 'JS', rol: 'Operador de voladura', nodo: 'f1', edad: 41, turno: 'A' },
  { id: 'm2', nombre: 'Rosa Paredes', iniciales: 'RP', rol: 'Ayudante de frente', nodo: 'f2', edad: 34, turno: 'A' },
  { id: 'm3', nombre: 'Miguel Chávez', iniciales: 'MC', rol: 'Perforista', nodo: 'f3', edad: 38, turno: 'B' },
  { id: 'm4', nombre: 'Elmer Ccopa', iniciales: 'EC', rol: 'Operador de scoop', nodo: 'f4', edad: 29, turno: 'B' },
  { id: 'm5', nombre: 'Lucía Mendoza', iniciales: 'LM', rol: 'Supervisora de seguridad', nodo: 'i1', edad: 45, turno: 'A' }
];

/* ============================================================
   ESCENARIOS
   Cada uno define lecturas de sensores y eventos reportados.
   ============================================================ */
const ESCENARIOS = [
  {
    id: 'ESC-01',
    nombre: 'Voladura en Frente 340',
    corto: 'Voladura con gases',
    severidad: 'alta',
    hora: '06:42',
    evento: 'Voladura con ANFO',
    descripcion: 'Disparo no programado en el Frente 340-N. La ventilación auxiliar no alcanza el caudal requerido y los gases de voladura migran por el By-pass Norte.',
    sensores: {
      t_i2_f1: { co: 88, no2: 8.4, o2: 19.2, vel: 18, anfo: true },
      t_i3_f2: { co: 54, no2: 6.1, o2: 19.4, vel: 23, anfo: true },
      t_i2_r1: { co: 65, no2: 3.6, o2: 20.1, vel: 40 },
      t_i3_r1: { co: 29, no2: 2.1, o2: 20.2, vel: 45 },
      t_i1_i2: { co: 20, o2: 20.5, vel: 62 },
      t_i1_i3: { co: 18, o2: 20.6, vel: 64 },
      t_i1_i6: { co: 14, o2: 20.7, vel: 70 },
      t_r1_r2: { co: 12, o2: 20.6, vel: 60 }
    },
    mineros: ['m1', 'm2', 'm3', 'm4', 'm5'],
    nota: 'Ningún túnel alcanza el nivel de peligro inmediato: el sistema gradúa el riesgo y evita el By-pass Norte.'
  },
  {
    id: 'ESC-02',
    nombre: 'Incendio en Galería Principal',
    corto: 'Incendio en galería',
    severidad: 'critica',
    hora: '14:18',
    evento: 'Incendio de equipo diésel',
    descripcion: 'Incendio declarado en la Galería Principal, entre el Socavón y el Cruce Norte. El humo avanza hacia las labores del Nivel 1 y bloquea la salida principal.',
    sensores: {
      t_s1_i1: { co: 210, no2: 7.2, o2: 17.4, vel: 34, incendio: true },
      t_i1_i2: { co: 72, no2: 4.8, o2: 18.9, vel: 38 },
      t_i1_i3: { co: 58, no2: 4.1, o2: 19.1, vel: 40 },
      t_i1_i6: { co: 44, no2: 3.2, o2: 19.3, vel: 36 },
      t_i2_r1: { co: 22, o2: 20.3, vel: 16 },
      t_i2_i6: { co: 25, o2: 20.1, vel: 28 },
      t_i3_i6: { co: 24, o2: 20.2, vel: 30 },
      t_i2_f1: { co: 18, o2: 20.6, vel: 55 },
      t_i3_f2: { co: 16, o2: 20.7, vel: 58 },
      t_i3_r1: { co: 21, o2: 20.5, vel: 62 },
      t_r1_r2: { co: 8, o2: 20.8, vel: 100 },
      t_r2_r4: { co: 5, o2: 20.9, vel: 80 },
      t_r4_s2: { co: 6, o2: 20.9, vel: 95 }
    },
    mineros: ['m1', 'm2', 'm3', 'm4', 'm5'],
    nota: 'La salida principal queda cerrada. El sistema reasigna a todos los mineros hacia la Rampa de Escape.'
  },
  {
    id: 'ESC-03',
    nombre: 'Derrumbe y falla de ventilación',
    corto: 'Derrumbe + ventilación',
    severidad: 'critica',
    hora: '22:05',
    evento: 'Derrumbe en dos frentes',
    descripcion: 'Derrumbe reportado en la Galería 340-N y en la Rampa de Escape. El ventilador principal del Nivel 2 opera al 30 %, con deficiencia de oxígeno en las labores inferiores.',
    sensores: {
      t_i2_f1: { co: 8, o2: 20.7, vel: 20, derrumbe: true },
      t_r4_s2: { co: 6, o2: 20.8, vel: 18, derrumbe: true },
      t_i4_r3: { o2: 17.6, co2: 14000, vel: 8 },
      t_r3_i5: { o2: 18.1, co2: 10000, vel: 10 },
      t_i5_r4: { o2: 18.8, co2: 7000, vel: 12 },
      t_i5_f4: { o2: 18.4, co2: 8500, vel: 11 },
      t_r3_f3: { o2: 19.0, co2: 6000, vel: 14 },
      t_r4_f4: { o2: 18.9, co2: 6500, vel: 13 },
      t_f3_i5: { o2: 18.6, co2: 7200, vel: 10 },
      t_r2_r4: { o2: 19.4, vel: 24 },
      t_i1_i4: { o2: 20.1, vel: 35 }
    },
    mineros: ['m1', 'm2', 'm3', 'm4', 'm5'],
    nota: 'La línea base no puede cruzar las labores con O₂ bajo TWA. El sistema graduó el riesgo y decidió refugiar o evacuar según cada minero.'
  }
];

/* ============================================================
   UMBRALES (configuración · D13)
   Niveles: normal · alerta · alto · peligro
   ============================================================ */
const UMBRALES = {
  co:    { nombre: 'CO', unidad: 'ppm', tipo: 'max', alerta: 25, alto: 50, peligro: 100, fuente: 'DS 024-2016-EM · Anexo 15, ítem 33' },
  no2:   { nombre: 'NO₂', unidad: 'ppm', tipo: 'max', alerta: 3, alto: 5, peligro: 10, fuente: 'DS 024-2016-EM · Anexo 15, ítem 21' },
  co2:   { nombre: 'CO₂', unidad: 'ppm', tipo: 'max', alerta: 5000, alto: 30000, peligro: 60000, fuente: 'DS 024-2016-EM · Anexo 15, ítem 20' },
  h2s:   { nombre: 'H₂S', unidad: 'ppm', tipo: 'max', alerta: 10, alto: 15, peligro: 30, fuente: 'DS 024-2016-EM · Anexo 15, ítem 5' },
  o2:    { nombre: 'O₂', unidad: '%', tipo: 'min', alerta: 19.5, alto: 18, peligro: 16, fuente: 'DS 024-2016-EM · Anexo 15, ítem 36' }
};

const UMBRAL_VIENTO = {
  minimo: 20,
  minimoAnfo: 25,
  maximo: 250,
  fuente: 'DS 024-2016-EM · Art. 248'
};

/* ============================================================
   CATÁLOGO DE REGLAS
   categoria: DIAG | RIESGO | RUTA | DEC
   fuente: NORMA | SUPUESTO
   ============================================================ */
const REGLAS = [
  // --- DIAG: gases -------------------------------------------------
  { id: 'R-CO-01', categoria: 'DIAG', nombre: 'CO sobre TWA', si: 'CO > 25 ppm', entonces: 'Nivel de CO = alerta', prioridad: 40, fuente: 'NORMA', detalle: 'CO sobre el límite de exposición de 8 h.', cita: 'Anexo 15, ítem 33' },
  { id: 'R-CO-02', categoria: 'DIAG', nombre: 'CO sobre riesgo alto', si: 'CO > 50 ppm', entonces: 'Nivel de CO = riesgo alto', prioridad: 45, fuente: 'SUPUESTO', detalle: 'Dos veces el TWA; criterio del equipo (D12).', cita: 'D12' },
  { id: 'R-CO-03', categoria: 'DIAG', nombre: 'CO en peligro inmediato', si: 'CO > 100 ppm', entonces: 'Nivel de CO = peligro', prioridad: 50, fuente: 'SUPUESTO', detalle: 'Umbral de cierre por CO; supuesto del equipo (D12).', cita: 'D12' },
  { id: 'R-NO2-01', categoria: 'DIAG', nombre: 'NO₂ sobre TWA', si: 'NO₂ > 3 ppm', entonces: 'Nivel de NO₂ = alerta', prioridad: 40, fuente: 'NORMA', detalle: 'NO₂ sobre el TWA de 3 ppm.', cita: 'Anexo 15, ítem 21' },
  { id: 'R-NO2-02', categoria: 'DIAG', nombre: 'NO₂ sobre STEL', si: 'NO₂ > 5 ppm', entonces: 'Nivel de NO₂ = riesgo alto', prioridad: 45, fuente: 'NORMA', detalle: 'Supera el STEL de 5 ppm.', cita: 'Anexo 15, ítem 21' },
  { id: 'R-NO2-03', categoria: 'DIAG', nombre: 'NO₂ en peligro inmediato', si: 'NO₂ > 10 ppm', entonces: 'Nivel de NO₂ = peligro', prioridad: 50, fuente: 'SUPUESTO', detalle: 'Dos veces el STEL; supuesto del equipo.', cita: 'D12' },
  { id: 'R-O2-01', categoria: 'DIAG', nombre: 'Deficiencia de oxígeno', si: 'O₂ < 19,5 %', entonces: 'Nivel de O₂ = alerta', prioridad: 40, fuente: 'NORMA', detalle: 'O₂ bajo el mínimo de 19,5 % (Art. 246).', cita: 'Anexo 15, ítem 36' },
  { id: 'R-O2-02', categoria: 'DIAG', nombre: 'O₂ bajo riesgo alto', si: 'O₂ < 18 %', entonces: 'Nivel de O₂ = riesgo alto', prioridad: 45, fuente: 'SUPUESTO', detalle: 'Umbral de riesgo alto definido por el equipo.', cita: 'D12' },
  { id: 'R-O2-03', categoria: 'DIAG', nombre: 'O₂ en peligro inmediato', si: 'O₂ < 16 %', entonces: 'Nivel de O₂ = peligro', prioridad: 50, fuente: 'SUPUESTO', detalle: 'Umbral de cierre por deficiencia de O₂.', cita: 'D12' },
  { id: 'R-CO2-01', categoria: 'DIAG', nombre: 'CO₂ sobre TWA', si: 'CO₂ > 5 000 ppm', entonces: 'Nivel de CO₂ = alerta', prioridad: 40, fuente: 'NORMA', detalle: 'CO₂ sobre el TWA de 5 000 ppm.', cita: 'Anexo 15, ítem 20' },
  { id: 'R-CO2-02', categoria: 'DIAG', nombre: 'CO₂ sobre riesgo alto', si: 'CO₂ > 30 000 ppm', entonces: 'Nivel de CO₂ = riesgo alto', prioridad: 45, fuente: 'NORMA', detalle: 'Supera el STEL de 30 000 ppm.', cita: 'Anexo 15, ítem 20' },
  { id: 'R-CO2-03', categoria: 'DIAG', nombre: 'CO₂ en peligro inmediato', si: 'CO₂ > 60 000 ppm', entonces: 'Nivel de CO₂ = peligro', prioridad: 50, fuente: 'SUPUESTO', detalle: 'Dos veces el STEL; supuesto del equipo.', cita: 'D12' },
  { id: 'R-H2S-01', categoria: 'DIAG', nombre: 'H₂S sobre TWA', si: 'H₂S > 10 ppm', entonces: 'Nivel de H₂S = alerta', prioridad: 40, fuente: 'NORMA', detalle: 'H₂S sobre el TWA de 10 ppm.', cita: 'Anexo 15, ítem 5' },
  { id: 'R-H2S-02', categoria: 'DIAG', nombre: 'H₂S sobre STEL', si: 'H₂S > 15 ppm', entonces: 'Nivel de H₂S = riesgo alto', prioridad: 45, fuente: 'NORMA', detalle: 'Supera el STEL de 15 ppm.', cita: 'Anexo 15, ítem 5' },
  { id: 'R-H2S-03', categoria: 'DIAG', nombre: 'H₂S en peligro inmediato', si: 'H₂S > 30 ppm', entonces: 'Nivel de H₂S = peligro', prioridad: 50, fuente: 'SUPUESTO', detalle: 'Dos veces el STEL; supuesto del equipo.', cita: 'D12' },
  { id: 'R-VEN-01', categoria: 'DIAG', nombre: 'Ventilación insuficiente', si: 'Velocidad del aire < 20 m/min', entonces: 'Nivel de ventilación = insuficiente', prioridad: 35, fuente: 'NORMA', detalle: 'Por debajo del mínimo legal de 20 m/min.', cita: 'Art. 248' },
  { id: 'R-VEN-02', categoria: 'DIAG', nombre: 'Ventilación crítica con ANFO', si: 'ANFO = sí Y velocidad < 25 m/min', entonces: 'Nivel de ventilación = crítica', prioridad: 60, fuente: 'NORMA', detalle: 'Con ANFO se exigen 25 m/min. Regla específica: gana el conflicto por prioridad y especificidad.', cita: 'Art. 248' },
  { id: 'R-VEN-03', categoria: 'DIAG', nombre: 'Ventilación general conforme', si: 'Velocidad ≥ 20 m/min', entonces: 'Nivel de ventilación = conforme', prioridad: 30, fuente: 'NORMA', detalle: 'Regla general. En conflicto con R-VEN-02 pierde por prioridad.', cita: 'Art. 248' },
  { id: 'R-FUE-01', categoria: 'DIAG', nombre: 'Incendio declarado', si: 'Incendio reportado = sí', entonces: 'Nivel de riesgo = peligro', prioridad: 80, fuente: 'NORMA', detalle: 'Un incendio activo hace intransitable la labor.', cita: 'Procedimiento de emergencia' },
  { id: 'R-DER-01', categoria: 'DIAG', nombre: 'Derrumbe reportado', si: 'Derrumbe reportado = sí', entonces: 'Túnel cerrado', prioridad: 85, fuente: 'NORMA', detalle: 'La caída de rocas se modela como evento reportado que bloquea la labor.', cita: 'D04' },

  // --- RIESGO: agregación y propagación ----------------------------
  { id: 'R-RIESGO-07', categoria: 'RIESGO', nombre: 'Agregación de peligro por gas', si: 'Algún gas en peligro inmediato', entonces: 'Nivel de riesgo = peligro', prioridad: 79, fuente: 'SUPUESTO', detalle: 'Traslada el diagnóstico del gas al riesgo del túnel y habilita la regla de cierre.', cita: 'D09 / D12' },
  { id: 'R-RIESGO-01', categoria: 'RIESGO', nombre: 'Cierre por peligro inmediato', si: 'Nivel de riesgo = peligro', entonces: 'Túnel cerrado', prioridad: 90, fuente: 'SUPUESTO', detalle: 'Solo el nivel de peligro inmediato cierra un túnel.', cita: 'D09 / D12' },
  { id: 'R-RIESGO-02', categoria: 'RIESGO', nombre: 'Agregación de riesgo alto', si: 'Algún gas en riesgo alto O ventilación crítica', entonces: 'Nivel de riesgo = riesgo alto', prioridad: 75, fuente: 'SUPUESTO', detalle: 'El túnel conserva el peor nivel de sus indicadores.', cita: 'D09' },
  { id: 'R-RIESGO-03', categoria: 'RIESGO', nombre: 'Agregación de alerta', si: 'Algún gas en alerta O ventilación insuficiente O propagación', entonces: 'Nivel de riesgo = alerta', prioridad: 55, fuente: 'SUPUESTO', detalle: 'Nivel mínimo de afectación cuando no hay riesgo alto.', cita: 'D09' },
  { id: 'R-RIESGO-04', categoria: 'RIESGO', nombre: 'Propagación desde túnel vecino', si: 'Túnel vecino con incendio o derrumbe', entonces: 'Propagación de riesgo = sí', prioridad: 54, fuente: 'SUPUESTO', detalle: 'El efecto sobre túneles vecinos no está en la norma (D11).', cita: 'SUPUESTO' },
  { id: 'R-RIESGO-05', categoria: 'RIESGO', nombre: 'Costo por riesgo alto', si: 'Nivel de riesgo = riesgo alto', entonces: 'Multiplicador de costo = 3', prioridad: 65, fuente: 'SUPUESTO', detalle: 'Reglas que solo aumentan el costo (D01).', cita: 'D01' },
  { id: 'R-RIESGO-06', categoria: 'RIESGO', nombre: 'Costo por alerta', si: 'Nivel de riesgo = alerta', entonces: 'Multiplicador de costo = 2', prioridad: 60, fuente: 'SUPUESTO', detalle: 'Reglas que solo aumentan el costo (D01).', cita: 'D01' },

  // --- RUTA --------------------------------------------------------
  { id: 'R-RUTA-01', categoria: 'RUTA', nombre: 'Arista no transitable', si: 'Túnel cerrado = sí', entonces: 'Arista bloqueada para el planificador', prioridad: 95, fuente: 'SUPUESTO', detalle: 'El planificador excluye la arista del grafo.', cita: 'D01' },
  { id: 'R-RUTA-02', categoria: 'RUTA', nombre: 'Costo dinámico de la arista', si: 'Multiplicador de costo > 1', entonces: 'Costo = longitud × multiplicador', prioridad: 50, fuente: 'SUPUESTO', detalle: 'El planificador consume los costos que producen las reglas.', cita: 'D02' },

  // --- DEC: decisión ----------------------------------------------
  { id: 'DEC-01', categoria: 'DEC', nombre: 'Evacuar a superficie', si: 'Ruta a salida viable Y costo de riesgo aceptable', entonces: 'Minero EVACÚA', prioridad: 70, fuente: 'SUPUESTO', detalle: 'Se elige la salida de menor costo ajustado por riesgo.', cita: 'Nivel 2' },
  { id: 'DEC-02', categoria: 'DEC', nombre: 'Refugiarse', si: 'Ruta a salida inviable o muy expuesta Y refugio ≤ 400 m', entonces: 'Minero SE REFUGIA', prioridad: 75, fuente: 'SUPUESTO', detalle: 'Se prefiere esperar en una estación hermética antes que cruzar riesgo alto.', cita: 'Anexo 19' },
  { id: 'DEC-03', categoria: 'DEC', nombre: 'Esperar brigada', si: 'Sin ruta a salida Y sin refugio alcanzable', entonces: 'Minero ESPERA BRIGADA', prioridad: 80, fuente: 'SUPUESTO', detalle: 'Se mantiene comunicación y se solicita rescate.', cita: 'Nivel 2' }
];

const CATEGORIAS = {
  DIAG: { nombre: 'Diagnóstico', color: '#38bdf8' },
  RIESGO: { nombre: 'Riesgo', color: '#f59e0b' },
  RUTA: { nombre: 'Ruta', color: '#a78bfa' },
  DEC: { nombre: 'Decisión', color: '#34d399' }
};
