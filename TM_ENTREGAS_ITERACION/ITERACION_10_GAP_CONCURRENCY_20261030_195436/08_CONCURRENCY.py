"""Concurrencia TM: una lectura principal (L1) y una local secundaria (L2).

Cada lectura tiene su propio Reader, sus propias referencias, su propia
genealogía, sus propios tiempos y su propia autoridad. Un tick puede afectar
a ambas, pero nunca se transfieren extremos, módulos ni genealogías.

Máximo dos escalas activas. Una lectura local no sustituye L1.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from tm_reference_interpreter_v1_direct_aut import Reader, Tick


@dataclass
class ReadingSpec:
    reading_id: str
    ticks: list[Tick]
    parent_reading_id: str = ""


@dataclass
class CompositeResult:
    states: dict = field(default_factory=dict)
    leaks: list = field(default_factory=list)
    readings: list = field(default_factory=list)

    def ok(self) -> bool:
        return not self.leaks


class CompositeReader:
    """Ejecuta hasta dos lecturas independientes y audita fugas."""

    MAX_READINGS = 2

    def __init__(self, specs: list[ReadingSpec]):
        if len(specs) > self.MAX_READINGS:
            raise ValueError("maximo dos escalas activas")
        self.specs = specs

    def run(self) -> CompositeResult:
        result = CompositeResult()
        readers: dict[str, Reader] = {}
        for spec in self.specs:
            rd = Reader(spec.ticks, reading_id=spec.reading_id).run()
            readers[spec.reading_id] = rd
            result.states[spec.reading_id] = rd.summary()
            result.readings.append({
                "reading_id": spec.reading_id,
                "parent_reading_id": spec.parent_reading_id,
                "ticks": len(spec.ticks),
                "first_tick": spec.ticks[0].seq if spec.ticks else None,
                "last_tick": spec.ticks[-1].seq if spec.ticks else None,
            })
            # Propiedad: el estado declara su propia lectura.
            if rd.summary()["reading_id"] != spec.reading_id:
                result.leaks.append(
                    f"OWNERSHIP: {spec.reading_id} declara "
                    f"{rd.summary()['reading_id']}")
        self._audit_reference_ownership(readers, result)
        return result

    def _audit_reference_ownership(self, readers: dict[str, Reader],
                                   result: CompositeResult) -> None:
        # Cero fugas: cada lectura conserva sus propios originales y extremos
        # dentro del rango de precios de SUS propios ticks.
        for rid, rd in readers.items():
            prices = [t.price for t in rd.ticks]
            if not prices:
                continue
            lo, hi = min(prices), max(prices)
            r = rd.reading
            for name, value in (("one_origin", r.one_origin),
                                ("one_extreme", r.one_extreme),
                                ("two_origin", r.two_origin),
                                ("two_extreme", r.two_extreme),
                                ("mod_origin", r.mod_origin),
                                ("mod_extreme", r.mod_extreme),
                                ("a_origin", r.a_origin),
                                ("a_extreme", r.a_extreme),
                                ("c_origin", r.c_origin),
                                ("c_extreme", r.c_extreme),
                                ("n_origin", r.n_origin),
                                ("n_extreme", r.n_extreme)):
                if value and not (lo <= value <= hi):
                    result.leaks.append(
                        f"CROSS_READING_REFERENCE_LEAK: {rid}.{name}={value} "
                        f"fuera de su rango [{lo},{hi}]")
