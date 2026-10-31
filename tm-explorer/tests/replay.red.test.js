'use strict';

/**
 * TESTS ROJOS — Validacion ciega (Fase 2, TDD).
 *
 * Estos tests DEBEN fallar mientras el nucleo TM siga siendo scaffold.
 * Codifican la lectura golden de las velas 1-9. Se pondran verdes en Fase 3
 * cuando el motor aplique las reglas cerradas.
 *
 * Politica anti-spoiler: el motor NO conoce el golden; aqui solo se compara
 * su salida contra el golden almacenado.
 */

const { test } = require('node:test');
const assert = require('node:assert');
const path = require('node:path');

const { TMEngine } = require('../src/core/engine');
const { replayTicks, replayBars, firstDeviations } = require('../src/replay/replay');
const { loadTicks, loadBars } = require('../src/replay/csv');
const { loadGolden, validateGolden } = require('../src/golden/format');

const DATA = path.join(__dirname, '..', 'data');
const GOLDEN_PATH = path.join(__dirname, 'golden', 'golden_velas_1_9.json');
const TICKS_CSV = path.join(DATA, 'ticks_USTEC_2026-10-16_16-30.csv');
const BARS_CSV = path.join(DATA, 'velas_USTEC_2026-10-16_16-30.csv');

function report(deviations) {
  if (deviations.length === 0) return '';
  const first = deviations[0];
  const shown = deviations.slice(0, 5).map(
    (d) => `vela ${d.n} campo ${d.campo}: esperado=${JSON.stringify(d.esperado)} obtenido=${JSON.stringify(d.obtenido)}`
  );
  return `Primera desviacion -> vela ${first.n} campo ${first.campo}\n` + shown.join('\n');
}

test('golden es valido y usa solo vocabulario TM', () => {
  const golden = loadGolden(GOLDEN_PATH);
  const errors = validateGolden(golden);
  assert.deepStrictEqual(errors, [], `Golden invalido:\n${errors.join('\n')}`);
});

test('ROJO: replay por ticks reproduce la lectura TM velas 1-9', () => {
  const golden = loadGolden(GOLDEN_PATH);
  const ticks = loadTicks(TICKS_CSV);
  const engine = new TMEngine();
  replayTicks(engine, ticks);

  const deviations = firstDeviations(engine.statesByCandle(), golden);
  assert.deepStrictEqual(deviations, [], report(deviations));
});

test('ROJO: replay por velas reproduce la lectura TM velas 1-9', () => {
  const golden = loadGolden(GOLDEN_PATH);
  const bars = loadBars(BARS_CSV);
  const engine = new TMEngine();
  replayBars(engine, bars);

  const deviations = firstDeviations(engine.statesByCandle(), golden);
  assert.deepStrictEqual(deviations, [], report(deviations));
});
