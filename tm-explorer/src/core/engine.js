'use strict';

/**
 * ============================================================================
 * NUCLEO TM — SCAFFOLD (Fase 2)
 * ============================================================================
 * Contrato compartido entre el adaptador de replay (TDD) y el adaptador
 * MQL5 OnTick. El ORDEN de los eventos es la unica fuente de verdad.
 *
 * ESTADO: scaffold. La logica TM de clasificacion se implementa en Fase 3.
 * Este archivo NO implementa todavia reglas TM, ni siquiera las cerradas, para
 * respetar el ciclo TDD (tests rojos primero).
 *
 * ANTI-SPOILER (politica obligatoria):
 *   - Este archivo NO debe contener numeros de vela, precios ni la lectura
 *     esperada del golden.
 *   - El golden vive en tests/golden/ y solo se lee desde los tests.
 *   - Guardado por tests/harness.test.js.
 * ============================================================================
 */

const ENGINE_VERSION = '0.0.1-scaffold';

// Estados permitidos (ADENDA v4 §4 / REGLAS_CERRADAS §F).
const ESTADOS = Object.freeze([
  'CANDIDATA',
  'ACTIVA',
  'CONFIRMADA',
  'PENDIENTE',
  'RECLASIFICADA',
  'INTEGRADA',
  'INVALIDADA',
  'FINALIZADA'
]);

// Vocabulario modular permitido (§1.1 / REGLAS_CERRADAS §D).
const VOCABULARIO_MODULAR = Object.freeze(['1', '2', '3', 'MODULO', 'A', 'B', 'C', 'AUT', 'CUT']);

// Vocabulario de patrones permitido (§1.2).
const VOCABULARIO_PATRONES = Object.freeze(['TT', 'FT']);

// Direcciones.
const DIR = Object.freeze({ UP: 'ALCISTA', DOWN: 'BAJISTA', NONE: null });

/**
 * Snapshot de una lectura (una fotografia vigente).
 * @typedef {Object} Reading
 * @property {string} id
 * @property {string} estado            // uno de ESTADOS
 * @property {string[]} modular         // etiquetas de VOCABULARIO_MODULAR vigentes
 * @property {string[]} patrones        // etiquetas de VOCABULARIO_PATRONES vigentes
 * @property {Object} niveles           // modulo, A, B, autocorte, objetivo TT, SL...
 */

/**
 * Snapshot de vela (lo que compara el golden).
 * @typedef {Object} CandleState
 * @property {number} n
 * @property {?string} dir
 * @property {string[]} modular
 * @property {string[]} patrones
 * @property {string[]} eventos
 */

/**
 * Núcleo TM determinista.
 * Alimentar SIEMPRE en orden (por tick o por cierre de vela), nunca en desorden.
 */
class TMEngine {
  constructor(options = {}) {
    this.options = options;
    this.reset();
  }

  reset() {
    this._lastBarIndex = null;
    this._readings = [];        // Reading[]
    this._events = [];          // Evento TM emitidos (historia)
    this._statesByCandle = new Map(); // n -> CandleState
  }

  /**
   * Alimenta un tick. Devuelve los eventos TM emitidos en ese tick.
   * @param {Object} tick
   * @returns {Array<Object>} eventos
   */
  onTick(_tick) {
    // TODO(Fase 3): reconstruir movimientos tick a tick, aplicar medidas A1-A3
    // y las reglas B/C/F. Sin numeros de vela ni lectura cableada.
    return [];
  }

  /**
   * Alimenta una vela ya cerrada (replay por velas). Devuelve eventos.
   * @param {Object} bar
   * @returns {Array<Object>} eventos
   */
  onBar(_bar) {
    // TODO(Fase 3): misma logica que onTick, consolidada por vela.
    return [];
  }

  /** Lecturas vigentes (fotografia actual). */
  snapshot() {
    return this._readings.map((r) => ({ ...r }));
  }

  /**
   * Fotografia vigente al cierre de cada vela.
   * @returns {Map<number, CandleState>}
   */
  statesByCandle() {
    const out = new Map();
    for (const [n, s] of this._statesByCandle) {
      out.set(n, { ...s, modular: [...s.modular], patrones: [...s.patrones], eventos: [...s.eventos] });
    }
    return out;
  }

  /** Historia completa de eventos (lo que se sabia en cada tick). */
  get events() {
    return this._events.slice();
  }
}

module.exports = {
  TMEngine,
  ESTADOS,
  VOCABULARIO_MODULAR,
  VOCABULARIO_PATRONES,
  DIR,
  ENGINE_VERSION
};
