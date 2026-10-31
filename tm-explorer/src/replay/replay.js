'use strict';

/**
 * Arnes de replay offline determinista.
 *
 * Reproduce exactamente los mismos ticks en el mismo orden y alimenta el
 * nucleo TM. Es el equivalente del futuro adaptador MQL5 OnTick.
 *
 * ANTI-SPOILER: no conoce la lectura esperada; solo entrega OHLC/ticks.
 */

const { loadTicks, loadBars } = require('./csv');

/**
 * Replay por ticks.
 * @param {import('../core/engine').TMEngine} engine
 * @param {Array<Object>} ticks
 * @returns {Array<Object>} eventos emitidos (en orden)
 */
function replayTicks(engine, ticks) {
  engine.reset();
  const events = [];
  for (const tick of ticks) {
    const emitted = engine.onTick(tick) || [];
    for (const e of emitted) events.push(e);
  }
  return events;
}

/**
 * Replay por velas cerradas.
 * @param {import('../core/engine').TMEngine} engine
 * @param {Array<Object>} bars
 * @returns {Array<Object>} eventos emitidos (en orden)
 */
function replayBars(engine, bars) {
  engine.reset();
  const events = [];
  for (const bar of bars) {
    const emitted = engine.onBar(bar) || [];
    for (const e of emitted) events.push(e);
  }
  return events;
}

function normList(list) {
  return Array.isArray(list) ? [...list].map(String).sort() : [];
}

/**
 * Compara la fotografia por vela del motor contra el golden.
 * Devuelve [] si coincide; si no, una lista de desviaciones ordenadas,
 * con la PRIMERA desviacion identificada (para localizar el primer tick/vela).
 *
 * @param {Map<number, Object>} actualStates
 * @param {Object} golden
 * @returns {Array<Object>}
 */
function firstDeviations(actualStates, golden) {
  const deviations = [];
  const [from, to] = golden.validationRange || [1, golden.candles.length];

  for (const expected of golden.candles) {
    const n = expected.n;
    if (n < from || n > to) continue;

    const actual = actualStates.get(n);
    if (!actual) {
      deviations.push({ n, campo: 'estado', esperado: expected, obtenido: null, motivo: 'sin estado para la vela' });
      continue;
    }

    const campos = [
      ['dir', expected.dir, actual.dir],
      ['modular', normList(expected.modular), normList(actual.modular)],
      ['patrones', normList(expected.patrones), normList(actual.patrones)],
      ['eventos', normList(expected.eventos), normList(actual.eventos)]
    ];

    for (const [campo, exp, got] of campos) {
      if (exp === undefined) continue;
      const same = Array.isArray(exp) ? JSON.stringify(exp) === JSON.stringify(got) : exp === got;
      if (!same) deviations.push({ n, campo, esperado: exp, obtenido: got });
    }
  }

  return deviations;
}

module.exports = { replayTicks, replayBars, firstDeviations, loadTicks, loadBars };
