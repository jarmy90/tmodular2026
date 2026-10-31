'use strict';

/**
 * CLI de validacion ciega: replay + comparacion contra el golden.
 * Localiza la PRIMERA desviacion (vela y campo) sin revelar la logica.
 *
 * Uso:
 *   node src/replay/cli.js [ticksCsv] [goldenJson]
 */

const path = require('node:path');
const { TMEngine } = require('../core/engine');
const { replayTicks, firstDeviations } = require('./replay');
const { loadTicks } = require('./csv');
const { loadGolden, validateGolden } = require('../golden/format');

function main() {
  const root = path.join(__dirname, '..', '..');
  const ticksCsv = process.argv[2] || path.join(root, 'data', 'ticks_USTEC_2026-10-16_16-30.csv');
  const goldenPath = process.argv[3] || path.join(root, 'tests', 'golden', 'golden_velas_1_9.json');

  const golden = loadGolden(goldenPath);
  const goldenErrors = validateGolden(golden);
  if (goldenErrors.length) {
    console.error('Golden invalido:\n' + goldenErrors.join('\n'));
    process.exit(2);
  }

  const ticks = loadTicks(ticksCsv);
  const engine = new TMEngine();
  const events = replayTicks(engine, ticks);

  console.log(`ticks=${ticks.length} eventos=${events.length} goldenVelas=${golden.candles.length}`);

  const deviations = firstDeviations(engine.statesByCandle(), golden);
  if (deviations.length === 0) {
    console.log('GOLDEN OK — lectura TM reproducida hasta vela ' + golden.validationRange[1]);
    process.exit(0);
  }

  console.log(`Desviaciones=${deviations.length}. Primera: vela ${deviations[0].n} campo ${deviations[0].campo}`);
  for (const d of deviations.slice(0, 10)) {
    console.log(`  vela ${d.n} ${d.campo}: esperado=${JSON.stringify(d.esperado)} obtenido=${JSON.stringify(d.obtenido)}`);
  }
  process.exit(1);
}

main();
