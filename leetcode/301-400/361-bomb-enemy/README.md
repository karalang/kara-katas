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

Not measured yet. The bench programs in `bench/` and their C, Rust, Go and
Python mirrors are written and agree on the printed checksum, but the timings
still have to be taken on a quiet machine. This section will carry the table
when they are. The Kāra and Rust versions copy the rows into byte vectors
before the pass. The C and Go versions build the grid as bytes to begin with,
so they skip that one `O(rows * cols)` copy.

## Compiler findings

- **MIR builder: an iterator built inside a closure.** The ★ arm reads the
  grid with
  `grid.iter().map(|r| r.bytes().iter().collect()).collect()`, and
  `karac __mir-run` refuses it with "an iterator value is not lowered yet"
  (the corpus's existing `mir-gap:an iterator value` bucket). Every other
  backend runs it.
