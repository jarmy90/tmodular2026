# Changelog 0.7.5.2-R3

- Add a reusable per-tick Big B range tracker with the exact 100% confirmation and strict 127% + 0.25 AUT boundary.
- Integrate tick transitions in the live primary reading and the active concurrent reading; preserve anchors through bar changes.
- Add explicit AUT causes `B_EXCEEDS_127_PLUS_0_25` and `A_CROSSES_STRUCTURE_BASE`.
- Confirm direct A-source AUT only on strict crossing of the attacked structure base; promote that A to the new dominant 1 without a synthetic B or TT.
- Start C Grande directly after confirmed B; absorb counter-moves inside candidate B without resetting its maximum.
- Add 16 synthetic, streaming, serialization and full-feed tests; preserve original legacy assertions and bundle their original feed.
- Add proposal R2 of the canonical tree and keep v2.12 as the approved base.
- Preserve the v003 golden and report its incompatible 16:23 AUT expectation.
