'use strict';

/**
 * TESTS VERDES — Infraestructura del arnes (Fase 2).
 *
 * Verifican parser, determinismo del replay, formato del golden y, sobre todo,
 * la politica ANTI-SPOILER: el nucleo no puede conocer la lectura esperada.
 */

const { test } = require('node:test');
const assert = require('node:assert');
const fs = require('node:fs');
const path = require('node:path');

const { TMEngine, VOCABULARIO_MODULAR, VOCABULARIO_PATRONES, ESTADOS } = require('../src/core/engine');
const { replayTicks, replayBars } = require('../src/replay/replay');
const { loadTicks, loadBars } = require('../src/replay/csv');
const { loadGolden, validateGolden } = require('../src/golden/format');

const ROOT = path.join(__dirname, '..');
const DATA = path.join(ROOT, 'data');
const GOLDEN_PATH = path.join(__dirname, 'golden', 'golden_velas_1_9.json');
const TICKS_CSV = path.join(DATA, 'ticks_USTEC_2026-10-16_16-30.csv');
const BARS_CSV = path.join(DATA, 'velas_USTEC_2026-10-16_16-30.csv');

test('parser de velas: 20 velas con OHLC numerico', () => {
  const bars = loadBars(BARS_CSV);
  assert.strictEqual(bars.length, 20);
  const b1 = bars[0];
  assert.strictEqual(b1.n, 1);
  assert.strictEqual(typeof b1.open, 'number');
  assert.strictEqual(typeof b1.high, 'number');
  assert.strictEqual(typeof b1.low, 'number');
  assert.strictEqual(typeof b1.close, 'number');
  assert.ok(b1.high >= b1.low);
});

test('parser de ticks: campos numericos y bar_index presente', () => {
  const ticks = loadTicks(TICKS_CSV);
  assert.ok(ticks.length > 1000, `esperado >1000 ticks, hay ${ticks.length}`);
  const t0 = ticks[0];
  assert.strictEqual(typeof t0.time_msc, 'number');
  assert.strictEqual(typeof t0.bid, 'number');
  assert.strictEqual(typeof t0.ask, 'number');
  assert.strictEqual(typeof t0.bar_index, 'number');
});

test('ticks ordenados de forma no decreciente en time_msc', () => {
  const ticks = loadTicks(TICKS_CSV);
  for (let i = 1; i < ticks.length; i++) {
    assert.ok(ticks[i].time_msc >= ticks[i - 1].time_msc, `tick ${i} fuera de orden`);
  }
});

test('replay es determinista: dos pasadas producen los mismos eventos', () => {
  const ticks = loadTicks(TICKS_CSV);
  const a = replayTicks(new TMEngine(), ticks);
  const b = replayTicks(new TMEngine(), ticks);
  assert.deepStrictEqual(a, b);
});

test('replay por velas es determinista', () => {
  const bars = loadBars(BARS_CSV);
  const a = replayBars(new TMEngine(), bars);
  const b = replayBars(new TMEngine(), bars);
  assert.deepStrictEqual(a, b);
});

test('contrato del motor: onTick devuelve array y reset limpia estado', () => {
  const engine = new TMEngine();
  assert.ok(Array.isArray(engine.onTick({ time_msc: 0, bid: 100, ask: 101, bar_index: 1 })));
  assert.strictEqual(engine.statesByCandle().size, 0);
  assert.deepStrictEqual(engine.snapshot(), []);
});

test('vocabulario expuesto coincide con el dosiser TM', () => {
  assert.deepStrictEqual(VOCABULARIO_MODULAR, ['1', '2', '3', 'MODULO', 'A', 'B', 'C', 'AUT', 'CUT']);
  assert.deepStrictEqual(VOCABULARIO_PATRONES, ['TT', 'FT']);
  assert.ok(ESTADOS.includes('CONFIRMADA') && ESTADOS.includes('RECLASIFICADA'));
});

test('golden: version, rango de validacion y vocabulario TM', () => {
  const golden = loadGolden(GOLDEN_PATH);
  assert.deepStrictEqual(validateGolden(golden), []);
  assert.deepStrictEqual(golden.validationRange, [1, 9]);
  assert.strictEqual(golden.candles.length, 9);
});

test('ANTI-SPOILER: el nucleo no contiene precios ni la lectura esperada', () => {
  const engineSrc = fs.readFileSync(path.join(ROOT, 'src', 'core', 'engine.js'), 'utf8');
  const forbidden = [
    '29742', '29.742', '29838', '29.838', '29820', '29.820',
    'VELA 1', 'VELA 2', 'AUT inmediato', 'CUT confirmado', '127 %'
  ];
  for (const token of forbidden) {
    assert.ok(!engineSrc.includes(token), `El nucleo contiene dato prohibido (anti-spoiler): "${token}"`);
  }
});

test('ANTI-SPOILER: el golden vive fuera del nucleo', () => {
  assert.ok(fs.existsSync(GOLDEN_PATH));
  assert.ok(!GOLDEN_PATH.includes(path.join('src', 'core')));
  assert.ok(GOLDEN_PATH.includes('golden'));
});
