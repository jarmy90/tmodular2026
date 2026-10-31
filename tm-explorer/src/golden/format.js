'use strict';

/**
 * Formato y validacion del golden.
 *
 * El golden es la lectura TM esperada. Vive FUERA del motor y solo lo leen los
 * tests. Usa exclusivamente vocabulario TM (REGLAS_CERRADAS §D).
 *
 * Esquema:
 * {
 *   "version": 1,
 *   "meta": { "simbolo", "fecha", "sesion", "fuente", "notas" },
 *   "validationRange": [1, 9],
 *   "candles": [
 *     { "n": 1, "dir": "BAJISTA", "modular": ["1"], "patrones": [], "eventos": ["1"] },
 *     ...
 *   ]
 * }
 */

const fs = require('fs');
const { VOCABULARIO_MODULAR, VOCABULARIO_PATRONES, ESTADOS } = require('../core/engine');

const GOLDEN_VERSION = 1;

function loadGolden(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function validateGolden(golden) {
  const errors = [];
  if (!golden || typeof golden !== 'object') return ['golden no es un objeto'];
  if (golden.version !== GOLDEN_VERSION) errors.push(`version debe ser ${GOLDEN_VERSION}`);
  if (!Array.isArray(golden.validationRange) || golden.validationRange.length !== 2) {
    errors.push('validationRange debe ser [inicio, fin]');
  }
  if (!Array.isArray(golden.candles) || golden.candles.length === 0) {
    errors.push('candles debe ser un array no vacio');
    return errors;
  }

  const allowedMod = new Set(VOCABULARIO_MODULAR);
  const allowedPat = new Set(VOCABULARIO_PATRONES);

  golden.candles.forEach((c, i) => {
    if (typeof c.n !== 'number') errors.push(`candles[${i}].n debe ser numero`);
    for (const m of c.modular || []) {
      if (!allowedMod.has(m) && !String(m).startsWith('MODULO')) {
        errors.push(`candles[${i}] modular "${m}" fuera de vocabulario TM`);
      }
    }
    for (const p of c.patrones || []) {
      const base = String(p).split('_')[0];
      if (!allowedPat.has(base)) errors.push(`candles[${i}] patron "${p}" fuera de vocabulario TM`);
    }
  });

  return errors;
}

module.exports = { loadGolden, validateGolden, GOLDEN_VERSION, VOCABULARIO_MODULAR, VOCABULARIO_PATRONES, ESTADOS };
