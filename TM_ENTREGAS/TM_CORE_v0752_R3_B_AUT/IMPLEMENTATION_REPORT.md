# Implementation report — 0.7.5.2-R3

## Where the rule lives

- B candidate tracking starts in `CanonicalEngine._track_primary_b_aut` and in the concurrent-reading B transition path. The active `BigBTracker` measures from the end of A, preserves the extreme through counter-swings and bar boundaries, confirms B Grande on the first tick at 100%, and confirms B-route AUT on the first tick strictly above `127% * A + 0.25`.
- Equality at the AUT boundary remains B Grande. The comparison is integer-price arithmetic and strict `>`.
- After B Grande confirmation, the first contrary tick is emitted as C Grande directly; no C-candidate state is emitted.
- A-source AUT is handled in the active-reading A path, using strict crossing of the attacked module/1-2-3 base. It carries `A_CROSSES_STRUCTURE_BASE`, closes/integrates the superseded reading, and creates a dominant new 1 from the A movement. It creates no B.
- B-source AUT carries `B_EXCEEDS_127_PLUS_0_25`; the two causes remain metadata on the same formal AUT function.
- A/B state is stored on Reading / BigBTracker and survives `serialize_state` / `restore_state`.

## Validation status

- 15 new cases cover 99.99%, 100%, 120%, exact boundary, strict next increment, direct-C, strict A-base crossing, oscillations, bar/chunk serialization, GAP/planar/initial-tail/2 gates, integrated engine transitions, and the full real feed.
- 20 legacy tests run on their bundled original v0.10 feed.
- The full feed replay is compared to v003 only after raw output is written. The 16:23 AUT expectation conflicts with the new universal B rule and remains a visible failure.
- R0062/R0064 values are checked against the frozen legacy reference; record actual result in `out/RUN_SUMMARY.json`.
- Physical transition prefixes are separately run against truncated CSV inputs and fresh subprocesses; record actual result in `out/TRANSITION_PREFIXES.json`.
- Passing synthetic tests and determinism do not prove full autonomous reading accuracy. No replay blind, AFS2 or production readiness is claimed.
