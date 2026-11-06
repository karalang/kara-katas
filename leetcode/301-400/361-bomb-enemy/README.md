# 361. Bomb Enemy

Given a grid of walls `'W'`, enemies `'E'` and empty cells `'0'`, return the
most enemies one bomb can kill. The bomb goes on an empty cell and kills every
enemy in its row and column, up to the nearest wall in each direction.

```
grid = ["0E00",
        "E0WE",
        "0E00"]   ->  3   (the bomb at row 1, column 1)
grid = ["WWW",
        "000",
        "EEE"]    ->  1
```

**Constraints:** `1 <= rows, cols <= 500`.

## Approaches

| file | mechanism | cost |
|---|---|---|
| `bomb_enemy.kara` ★ | one row-major pass; a row count recomputed at the row's start and after each wall, and per-column counts recomputed at the top and below each wall | `O(rows * cols)` |
| `bomb_enemy_brute.kara` | from every empty cell, walk in all four directions until a wall or the edge | `O(rows * cols * (rows + cols))` |
| `bomb_enemy_sweeps.kara` | four sweeps, one per direction, each with a running count that a wall resets, added into a per-cell total | `O(rows * cols)` |
| `differential.kara` | the three arms against an oracle that pairs every empty cell with every enemy, 30,000 checks, five properties | — |

Every arm prints the same 13 lines: both LeetCode examples, ten edge cases
(an empty grid, one empty cell, one enemy and nowhere to stand, walls only,
a wall that shields, a column, enemies all around one cell, the best cell in
a corner, enemies that do not block each other, two segments in one row),
and a checksum over 1,000 random grids. `bomb_enemy.py` mirrors the ★ arm
and its output is byte-identical.

The ★ arm's saving is that every cell of a wall-to-wall segment shares the
segment's count. So the row count is computed once per row segment, and each
column keeps its own count, which is reused down the column until a wall.

## Differential

`differential.kara` holds copies of the three arms, plus an oracle that never
walks from a cell. For each empty cell it looks at every enemy in the same
row or column and counts it when no wall lies strictly between the two. The
test draws 2,000 random grids of 1 to 6 by 1 to 6 cells.

| | property |
|---|---|
| P1 | every arm returns the oracle's answer |
| P2 | transposing the grid does not change the answer |
| P3 | reversing every row does not change the answer |
| P4 | turning one enemy into a wall never raises the answer |
| P5 | the answer is at most the number of enemies, and 0 with no empty cell |

It prints `2000 cases, 30000 checks, 4873 enemies in total, 0 failures`
under `karac run --interp`, LLJIT, and both builds.

## Mutation testing

Ten edits to the copies inside `differential.kara`, each run under
`karac run --interp`. All ten are killed.

| # | mutation | how |
|---|---|---|
| M1 | cached: the row count is not reset after a wall | P1, P2, P3 and P5, 3827 failures |
| M2 | cached: the column count ignores walls | P1 and P2, 234 failures |
| M3 | cached: the row count is recomputed only at the row's start | P1, P2 and P3, 651 failures |
| M4 | cached: a bomb may stand on an enemy | P1 and P5, 2186 failures |
| M5 | brute: walks only three directions | P1 and P2, 1375 failures |
| M6 | brute: a wall does not stop the walk | P1, 278 failures |
| M7 | sweeps: the downward sweep is missing | P1 and P2, 1361 failures |
| M8 | sweeps: a wall does not reset the run | P1, P2 and P3, 384 failures |
| M9 | oracle: walls are ignored | P1, 447 failures |
| M10 | oracle: counts every enemy in the grid | P1, 3354 failures |

## Verification

All three arms and the differential are byte-identical under `karac run`
(LLJIT), `karac run --interp`, `karac build`, and
`KARAC_AUTO_PAR=1 karac build`, and the three arms match `bomb_enemy.py` byte
for byte. Under `karac __mir-run` (the v2 MIR interpreter) the brute and
sweep arms match too, but the ★ arm and the differential do not build yet
(below). The bench program prints
`60 grids: 2503 enemies in total, checksum 408591223` under `karac build`, as
do its C, Rust, Go and Python mirrors.

## Benchmarks

The bench program runs the cached one-pass count over 60 random 400 x 400
grids. The Kāra build and its C, Rust, Go and Python mirrors agree on the
printed checksum. The Kāra and Rust versions copy the rows into byte vectors
before the pass. The C and Go versions build the grid as bytes to begin with,
so they skip that one `O(rows * cols)` copy.

### Apple M5 Pro, 2026-11-06

30 runs each, 5 warmups, on the Apple M5 Pro, karac `0.8.0-dev.14606+g162ee7a0e`
(g162ee7a0e, the v2/MIR backend), measured 2026-11-06, with the Kāra binary built
`KARAC_AUTO_PAR=0`. This is the kata's first measurement; Python was not run.
The last column is Kāra's mean over that row's mean.

| implementation | mean | Kāra / this |
|---|---|---|
| c `clang -O3` | 98.1 ms ± 0.7 | 1.14× |
| rust `-O` | 101.8 ms ± 0.7 | 1.10× |
| rust `-O -C overflow-checks=on` (equal-safety) | 103.5 ms ± 1.2 | 1.08× |
| **kāra `karac build`, seq** | **111.7 ms ± 1.2** | **—** |
| go `go build` | 152.0 ms ± 0.7 | 0.73× |

Kāra is 1.10× `rustc -O`, 1.08× equal-safety Rust, 1.14× C and 0.73× Go.
The gaps were not investigated on this host.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 48.5 ms ± 0.7 | 32.9 KiB | 1.2 MiB |
| rust | 123.2 ms ± 3.2 | 455.6 KiB | 1.6 MiB |
| kāra | 142.5 ms ± 2.4 | 66.9 KiB | 1.7 MiB |
| go | — | 2450.4 KiB | 7.6 MiB |

`karac build` is 2.9× clang's cold compile and 1.2× rustc's. Kāra's
68,552-byte binary is 2.0× clang's and 6.8× smaller than rustc's. Raw numbers are in
[`bench/results.json`](bench/results.json). The sink matches across the Kāra,
Rust, C and Go builds (`60 grids: 2503 enemies in total, checksum 408591223`).

## Compiler findings

- **MIR builder: an iterator built inside a closure.** The ★ arm reads the
  grid with
  `grid.iter().map(|r| r.bytes().iter().collect()).collect()`, and
  `karac __mir-run` refuses it with "an iterator value is not lowered yet"
  (the corpus's existing `mir-gap:an iterator value` bucket). Every other
  backend runs it.
