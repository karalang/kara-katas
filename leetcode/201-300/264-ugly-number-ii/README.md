# 264. Ugly Number II

An **ugly number** has only 2, 3, and 5 as prime factors (1 counts). Return the
`n`-th ugly number (1-indexed).

## Approach

Every ugly number after 1 is `2×`, `3×`, or `5×` a *smaller* ugly number, so
build the sequence in order with three merge pointers into the results so far —
one each for the ×2, ×3, ×5 streams. Each step takes the smallest of the three
candidates, appends it, and advances **every** pointer whose candidate equalled
it (advancing all ties dedupes values reachable two ways, e.g. `6 = 2×3 = 3×2`).
`O(n)` time and space.

## Files

- [`ugly_number_ii.kara`](ugly_number_ii.kara) — Kāra implementation.
- [`ugly_number_ii.py`](ugly_number_ii.py) — Python mirror (oracle).

Expected output (both): `1 12 15 24 36 80` (one per line).
