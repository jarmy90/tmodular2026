'use strict';

/**
 * ============================================================================
 * TESTS ROJOS — REGLAS RECIÉN CERRADAS POR EL EXPERTO (TDD, test primero)
 * ============================================================================
 *
 * Agente: TDD_GUIDE. Este archivo codifica las reglas cerradas por Javier y
 * DEBE FALLAR mientras el núcleo siga siendo scaffold (src/core/engine.js
 * devuelve [] / snapshot() vacío). NO se implementa lógica productiva aquí.
 *
 * ORDEN DE LECTURA que fundamenta estos tests:
 *   - 00_LEEME_PRIMERO_PRIORIDAD_DOCUMENTOS_TM.txt (§6 reglas que prevalecen)
 *   - DECISIONES_EXPERTO.md (DEC-001; C3/C2 pendientes de registrar)
 *   - REGLAS_CERRADAS.md (B1/B2, C concurrencia, D vocabulario, F reclasificación)
 *   - CONTRADICCIONES.md (C2 unidad AUT, C3 tocar vs superar, C4 vocabulario, C6 gap)
 *   - Prompt v2 §11 (tests mínimos) y §13 (anti-spoiler)
 *
 * MAPA REGLA (DEC-00X) -> TEST  (nota: DEC-00X aún no registradas literalmente
 * en DECISIONES_EXPERTO.md; aquí se reservan como huecos de decisión cerrada)
 *
 *   DEC-002 (origen C3 + C2) — AUT
 *     * AUT se confirma cuando B Grande SUPERA 127 % + 0,25 (no basta tocar y volver).
 *     * Si B Grande solo toca 127 % + 0,25 y vuelve, ese recorrido es B Grande y el
 *       movimiento que sube después es C Grande (sin AUT por el mero contacto).
 *     * El extra es 1 tick = 0,25 (no 0,025 ni 0,0625). DEC-001 fija 1 tick = 0,25 pts.
 *     Tests: A1, A2, A3, A4.
 *
 *   DEC-003 (origen C6) — Gap vs regla de 2
 *     * Al abrir vela nueva se evalúa PRIMERO el gap.
 *     * Si hay gap, NO se aplica la regla de 2 (no se confirma 2).
 *     Tests: B1, B2.
 *
 *   DEC-004 (origen §10.8 + C4) — Concurrencia y reclasificación
 *     * Las lecturas concurrentes se identifican como lectura 1 / 2 / 3.
 *     * Máximo 3 lecturas; no se abre una lectura por cada oscilación intravela.
 *     * Reclasificar no borra: el historial conserva el evento.
 *     Tests: C1, C2, C3.
 *
 *   DEC-005 (origen D + C4) — Vocabulario
 *     * Prohibido como clasificación en src/**, golden y estados:
 *       local · superior · estructura · giro · B excesiva · observador.
 *     Tests: D1, D2 (test estático; puede ser verde o rojo y debe existir).
 *
 * CONTRATO PÚBLICO ESPERADO DEL NÚCLEO (lo que estos tests exigen):
 *   - TMEngine.onTick(tick) -> Event[]                  (existe; hoy devuelve [])
 *   - TMEngine.snapshot() -> Reading[]                  (existe; hoy devuelve [])
 *   - TMEngine.statesByCandle() -> Map                 (existe; hoy vacío)
 *   - autTriggerOffset(aGrandeRange, opts) -> number   (AÚN NO EXISTE -> rojo)
 *       = 1.27 * aGrandeRange + (opts.extraTicks ?? 1) * (opts.tickSize ?? 0.25)
 *
 * Event esquema esperado: { type, lectura, estado, nivel? }
 *   type    ∈ { '1','2','3','POSIBLE_2','POSIBLE_3','3_FALLIDO','MODULO','A','B','C',
 *               'AUT','TT','CUT','GAP','SALIDA_EN_PLANO' }
 *   lectura ∈ { 'lectura 1','lectura 2','lectura 3' }
 * Reading (snapshot) esquema: { id:'lectura N', estado, modular, patrones, niveles }
 *
 * ANTI-SPOILER: fuente/fecha/símbolo/nº de vela no pueden aparecer en el núcleo
 * productivo. Aquí (tests) sí se permiten datos concretos; los escenarios usan
 * precios genéricos y NO cablean el golden de la muestra.
 * ============================================================================
 */

const { test } = require('node:test');
const assert = require('node:assert');
const fs = require('node:fs');
const path = require('node:path');

const engineMod = require('../src/core/engine');
const { TMEngine } = engineMod;

const ROOT = path.join(__dirname, '..');
const SRC_DIR = path.join(ROOT, 'src');
const GOLDEN_DIR = path.join(__dirname, 'golden');

// Vocabulario prohibido como clasificación (REGLAS_CERRADAS §D / CONTRADICCIONES C4).
const PROHIBIDOS = ['local', 'superior', 'estructura', 'giro', 'b excesiva', 'observador'];
const LECTURA_RE = /^lectura [123]$/;

// ---------------------------------------------------------------------------
// Utilidades de escena (precios genéricos; sin símbolo/fecha/golden).
// ---------------------------------------------------------------------------

let _ms = 1_000_000;
function tick(bid, bar) {
  _ms += 250;
  return { time_msc: _ms, bid, ask: bid + 0.25, bar_index: bar };
}

function ramp(from, to, steps, bar) {
  const out = [];
  const d = (to - from) / steps;
  for (let i = 0; i <= steps; i++) out.push(tick(from + d * i, bar));
  return out;
}

function feed(ticks) {
  const engine = new TMEngine();
  const events = [];
  for (const t of ticks) events.push(...(engine.onTick(t) || []));
  return { engine, events };
}

function types(events) {
  return events.map((e) => (e && e.type) || e);
}
function hasType(events, type) {
  return types(events).includes(type);
}

// Escenario modular genérico: 1 -> 2 -> 3 fallido -> módulo(1+2) -> A Grande -> B Grande.
// A Grande = 82,00 -> 118,00 (rango 36,00). B Grande bajista desde 118,00.
//   nivel 100 %         = 118,00 - 36,00        = 82,00
//   nivel 127 %         = 118,00 - 1,27 * 36,00 = 72,28
//   nivel AUT 127 %+1t  = 72,28 - 0,25          = 72,03   (bajista)
const A_FINAL = 118.0;
const A_RANGE = 36.0;
const LEVEL_127 = A_FINAL - 1.27 * A_RANGE; // 72,28
const AUT_LEVEL = LEVEL_127 - 0.25;         // 72,03

function buildAutTicks({ reach = AUT_LEVEL - 0.23, andReturn = false } = {}) {
  _ms = 1_000_000;
  const out = [];
  out.push(...ramp(100, 91, 9, 1));       // 1 bajista
  out.push(...ramp(91, 82, 9, 2));        // 2 bajista (salida en plano: open=close=91)
  out.push(...ramp(82, 87, 5, 3));        // contrario > 50 % de 2 -> 3 fallido, inicia A Grande
  out.push(...ramp(87, A_FINAL, 31, 4));  // A Grande alcista hasta 118
  out.push(...ramp(A_FINAL, reach, 40, 5)); // B Grande bajista hasta 'reach'
  if (andReturn) out.push(...ramp(reach, 90, 18, 6)); // movimiento contrario alcista -> C Grande
  return out;
}

function buildGapBoundaryTicks({ gapDown = true } = {}) {
  _ms = 5_000_000;
  const out = [];
  out.push(...ramp(100, 91, 9, 1));                 // 1 bajista
  const open2 = gapDown ? 89.0 : 91.0;              // gap bajista a favor de 1 / sin gap
  out.push(...ramp(open2, 82, 9, 2));
  return out;
}

function buildConcurrentTicks() {
  const out = buildAutTicks({ reach: AUT_LEVEL - 0.23 });
  out.push(...ramp(AUT_LEVEL - 0.23, 95, 24, 7));   // contrario -> posible 1 / C
  out.push(...ramp(95, 68, 27, 8));                 // nuevo extremo -> segunda lectura
  return out;
}

function buildOscillationTicks(oscillations = 12) {
  const out = buildAutTicks({ reach: AUT_LEVEL - 0.23 });
  let bar = 7;
  let price = AUT_LEVEL - 0.23;
  for (let i = 0; i < oscillations; i++) {
    const target = price + (i % 2 === 0 ? 3 : -3);
    out.push(...ramp(price, target, 3, bar));
    price = target;
    if (i % 2 === 1) bar++;
  }
  return out;
}

function buildReclassifyTicks() {
  _ms = 9_000_000;
  const out = [];
  out.push(...ramp(100, 91, 9, 1));  // 1
  out.push(...ramp(91, 82, 9, 2));   // 2
  out.push(...ramp(82, 90, 8, 3));   // corrección -> reclasifica velas previas como módulo + A Grande
  out.push(...ramp(90, 78, 12, 4));  // nuevo extremo -> evento RECLASIFICADA sin borrar el previo
  return out;
}

// ===========================================================================
// A. AUT — DEC-002 (origen C3 + C2)
// ===========================================================================

test('AUT (DEC-002): nivel = 1,27·A Grande + 1 tick (0,25); no 0,025 ni 0,0625', () => {
  const fn = engineMod.autTriggerOffset;
  assert.strictEqual(
    typeof fn,
    'function',
    'Falta exportar autTriggerOffset(aGrandeRange, opts) desde src/core/engine.js (ROJO: aún no existe)'
  );
  assert.strictEqual(fn(100, { tickSize: 0.25, extraTicks: 1 }), 127.25);
  assert.notStrictEqual(fn(100, { tickSize: 0.25, extraTicks: 1 }), 127.025);  // no 0,025
  assert.notStrictEqual(fn(100, { tickSize: 0.25, extraTicks: 1 }), 127.0625); // no 0,0625
});

test('ROJO AUT (DEC-002/C3): AUT se confirma cuando B Grande SUPERA 127 % + 0,25', () => {
  const { events } = feed(buildAutTicks({ reach: AUT_LEVEL - 0.23 })); // 71,80 < 72,03
  assert.ok(
    hasType(events, 'AUT'),
    `Se espera evento AUT al superar 127 %+0,25 (nivel ${AUT_LEVEL}); eventos=${JSON.stringify(types(events))}`
  );
});

test('ROJO AUT (DEC-002/C3): tocar 127 %+0,25 y volver NO confirma AUT; el que sube después es C Grande', () => {
  const { events } = feed(buildAutTicks({ reach: AUT_LEVEL, andReturn: true })); // toca 72,03 y vuelve
  assert.ok(!hasType(events, 'AUT'), 'No debe haber AUT si B Grande solo toca el nivel y vuelve');
  assert.ok(
    hasType(events, 'C'),
    `El movimiento contrario posterior a B Grande debe clasificarse como C Grande; eventos=${JSON.stringify(types(events))}`
  );
});

test('ROJO AUT (DEC-002/C2): a 127 %+0,0625 NO confirma AUT; a 127 %+0,25 (superado) SÍ', () => {
  const below = feed(buildAutTicks({ reach: LEVEL_127 - 0.0625 })); // 72,2175: solo 127 %+0,0625
  assert.ok(!hasType(below.events, 'AUT'), 'Con extra 0,0625 (0,25 tick) NO debe confirmarse AUT');
  const over = feed(buildAutTicks({ reach: AUT_LEVEL - 0.03 })); // 72,00: supera 127 %+0,25
  assert.ok(hasType(over.events, 'AUT'), 'Con extra 0,25 (1 tick) SÍ debe confirmarse AUT');
});

// ===========================================================================
// B. GAP vs regla de 2 — DEC-003 (origen C6)
// ===========================================================================

test('ROJO gap (DEC-003/C6): al abrir vela nueva se evalúa primero el gap y NO se aplica la regla de 2', () => {
  const { events } = feed(buildGapBoundaryTicks({ gapDown: true }));
  assert.ok(
    hasType(events, 'GAP'),
    `Se espera evento GAP en la frontera de vela; eventos=${JSON.stringify(types(events))}`
  );
  assert.ok(!hasType(events, '2'), 'Con gap NO debe confirmarse 2 (no se aplica la regla de 2)');
  assert.ok(!hasType(events, 'POSIBLE_2'), 'Con gap NO debe abrirse posible 2');
});

test('ROJO regla de 2 (DEC-003/C6): sin gap, la regla de 2 sí puede confirmar 2', () => {
  const { events } = feed(buildGapBoundaryTicks({ gapDown: false }));
  assert.ok(!hasType(events, 'GAP'), 'Sin gap no debe emitirse GAP');
  assert.ok(
    hasType(events, '2'),
    `Sin gap debe poder confirmarse 2; eventos=${JSON.stringify(types(events))}`
  );
});

// ===========================================================================
// C. CONCURRENCIA y RECLASIFICACIÓN — DEC-004 (origen §10.8 + C4)
// ===========================================================================

test('ROJO concurrencia (DEC-004/§10.8): lecturas identificadas lectura 1/2/3, máximo 3', () => {
  const { engine } = feed(buildConcurrentTicks());
  const snap = engine.snapshot();
  assert.ok(snap.length >= 2, `deben coexistir dos lecturas válidas; snapshot=${JSON.stringify(snap)}`);
  assert.ok(snap.length <= 3, 'máximo operativo: tres lecturas matemáticamente válidas');
  for (const r of snap) {
    assert.match(String(r.id), LECTURA_RE, `id de lectura fuera de "lectura 1..3": ${r.id}`);
  }
});

test('ROJO concurrencia (DEC-004/§10.8): una oscilación intravela no abre una lectura por oscilación', () => {
  const { engine } = feed(buildOscillationTicks(12));
  const snap = engine.snapshot();
  assert.ok(snap.length >= 1, 'debe existir al menos una lectura válida');
  assert.ok(snap.length <= 3, `12 oscilaciones NO deben crear 12 lecturas (máx 3); snapshot=${snap.length}`);
});

test('ROJO reclasificación (DEC-004/F): reclasificar no borra; el historial conserva el evento previo', () => {
  const { events } = feed(buildReclassifyTicks());
  assert.ok(events.length >= 2, `debe haber historial de eventos; eventos=${events.length}`);
  const first = events[0];
  assert.ok(first && first.lectura, 'los eventos llevan lectura de origen');
  const reclasi = events.find(
    (e) => e && (e.estado === 'RECLASIFICADA' || e.estado === 'INTEGRADA' || e.type === 'RECLASIFICADA')
  );
  assert.ok(reclasi, 'debe registrarse un evento RECLASIFICADA/INTEGRADA al reasignar movimientos');
  assert.strictEqual(reclasi.lectura, first.lectura, 'la reclasificación conserva el historial de la misma lectura');
});

// ===========================================================================
// D. VOCABULARIO — DEC-005 (origen D + C4). Test estático.
// ===========================================================================

function listFiles(dir) {
  const out = [];
  if (!fs.existsSync(dir)) return out;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name === 'node_modules' || entry.name === '.git') continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) out.push(...listFiles(full));
    else out.push(full);
  }
  return out;
}

function escapeRe(s) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

test('VOCAB (DEC-005/D): src/** no usa términos prohibidos como clasificación', () => {
  const files = listFiles(SRC_DIR).filter((f) => /\.(js|cjs|mjs|json)$/.test(f));
  const offenders = [];
  for (const f of files) {
    const text = fs.readFileSync(f, 'utf8');
    for (const token of PROHIBIDOS) {
      const body = escapeRe(token).replace(/\s+/g, '[ _-]');
      const re = new RegExp("(['\"`])\\s*" + body + "\\s*\\1", 'i');
      if (re.test(text)) offenders.push(`${path.relative(ROOT, f)}: "${token}" como etiqueta entrecomillada`);
    }
    if (/B_?EXCESIVA|v3_2_BEX|\bBEX\b/.test(text)) {
      offenders.push(`${path.relative(ROOT, f)}: término/mecanismo anulado (B(excesiva)/BEX) presente`);
    }
  }
  assert.deepStrictEqual(offenders, [], 'Vocabulario prohibido como clasificación en src/**:\n' + offenders.join('\n'));
});

function collectJsonStrings(value, acc) {
  if (typeof value === 'string') acc.push(value);
  else if (Array.isArray(value)) for (const v of value) collectJsonStrings(v, acc);
  else if (value && typeof value === 'object') for (const v of Object.values(value)) collectJsonStrings(v, acc);
  return acc;
}

test('VOCAB (DEC-005/D): golden y artefactos de estados no usan términos prohibidos', () => {
  const jsonFiles = listFiles(GOLDEN_DIR).filter((f) => f.endsWith('.json'));
  const estadoFiles = listFiles(ROOT).filter(
    (f) => /(^|[\\/])[^\\/]*estado[^\\/]*\.(json|csv)$/i.test(f) && !f.endsWith('.test.js')
  );
  const files = [...new Set([...jsonFiles, ...estadoFiles])];
  const offenders = [];
  for (const f of files) {
    const raw = fs.readFileSync(f, 'utf8');
    let candidates;
    if (f.endsWith('.json')) {
      try {
        candidates = collectJsonStrings(JSON.parse(raw), []);
      } catch {
        candidates = [raw];
      }
    } else {
      candidates = raw.split(/[;,\r\n]+/);
    }
    for (let c of candidates) {
      c = String(c).trim().toLowerCase().replace(/[_\-]+/g, ' ').replace(/\s+/g, ' ');
      if (!c) continue;
      for (const token of PROHIBIDOS) {
        const re = new RegExp('(^| )' + escapeRe(token) + '( |$)');
        if (c === token || re.test(c)) {
          offenders.push(`${path.relative(ROOT, f)}: "${token}" en valor de clasificación "${c}"`);
        }
      }
    }
  }
  assert.deepStrictEqual(offenders, [], 'Vocabulario prohibido en golden/estados:\n' + offenders.join('\n'));
});
