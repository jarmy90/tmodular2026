'use strict';

/**
 * Parser de los CSV de Teoria Modular.
 *
 * Formato: delimitado por ';', con cabecera en la primera linea.
 * Datos de entrada (solo OHLC / ticks: ninguna lectura TM cableada aqui).
 *
 * ANTI-SPOILER: este modulo no conoce la lectura esperada ni numeros de vela.
 */

const fs = require('fs');

const NUM_RE = /^-?\d+(\.\d+)?$/;

function stripBom(text) {
  return text.charCodeAt(0) === 0xfeff ? text.slice(1) : text;
}

function coerce(raw) {
  if (raw === undefined || raw === null) return null;
  const v = String(raw).trim();
  if (v === '') return null;
  return NUM_RE.test(v) ? Number(v) : v;
}

function parseDelimited(text, delimiter = ';') {
  const clean = stripBom(text);
  const lines = clean.split(/\r?\n/).filter((l) => l.trim() !== '');
  if (lines.length === 0) return { header: [], rows: [] };

  const header = lines[0].split(delimiter).map((h) => h.trim());
  const rows = [];

  for (let i = 1; i < lines.length; i++) {
    const cells = lines[i].split(delimiter);
    const obj = {};
    for (let c = 0; c < header.length; c++) {
      obj[header[c]] = coerce(cells[c]);
    }
    rows.push(obj);
  }

  return { header, rows };
}

/** Lee el CSV de ticks (bid/ask/last/... por tick). */
function loadTicks(filePath) {
  const { rows } = parseDelimited(fs.readFileSync(filePath, 'utf8'));
  return rows.map((r) => ({
    time: r.time,
    time_msc: r.time_msc,
    bid: r.bid,
    ask: r.ask,
    last: r.last,
    volume: r.volume,
    flags: r.flags,
    bar_index: r.bar_index,
    bar_start: r.bar_start
  }));
}

/** Lee el CSV de velas (OHLC por vela). */
function loadBars(filePath) {
  const { rows } = parseDelimited(fs.readFileSync(filePath, 'utf8'));
  return rows.map((r) => ({
    n: r.bar_index,
    inicio: r.inicio,
    fin: r.fin,
    open: r.open,
    high: r.high,
    low: r.low,
    close: r.close,
    direccion: r.direccion,
    cuerpo_pts: r.cuerpo_pts,
    rango_total_pts: r.rango_total_pts,
    cola_superior_pts: r.cola_superior_pts,
    cola_inferior_pts: r.cola_inferior_pts,
    ticks: r.ticks,
    time_open_msc: r.time_open_msc,
    time_high_msc: r.time_high_msc,
    time_low_msc: r.time_low_msc,
    time_close_msc: r.time_close_msc,
    gap_desde_cierre_anterior_pts: r.gap_desde_cierre_anterior_pts
  }));
}

module.exports = { parseDelimited, loadTicks, loadBars, coerce };
