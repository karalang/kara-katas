# 519. Random Flip Matrix

There is an `m x n` binary grid `matrix` with all the values set `0`
initially. Design an algorithm to randomly pick an index `(i, j)` where
`matrix[i][j] == 0` and flips it to `1`. All the indices `(i, j)` where
`matrix[i][j] == 0` should be equally likely to be returned.

Optimize your algorithm to minimize the number of calls made to the
built-in random function of your language and optimize the time and
space complexity.

Implement the `Solution` class:

- `Solution(int m, int n)` Initializes the object with the size of the
  binary matrix `m` and `n`.
- `int[] flip()` Returns a random index `[i, j]` of the matrix where
  `matrix[i][j] == 0` and flips it to `1`.
- `void reset()` Resets all the values of the matrix to be `0`.

```
Solution(3, 1)
flip() -> [1, 0], flip() -> [2, 0], flip() -> [0, 0]
reset()
flip() -> [2, 0]
(each flip any cell still 0, each equally likely)
```

**Constraints:** `1 <= m, n <= 10^4`; there will be at least one free
cell for each call to `flip`; at most `1000` calls will be made to
`flip` and `reset`.

## Approaches

Every arm is a `Solution` with `fn new(m: i64, n: i64, seed: i64) ->
Solution`, `fn flip(mut ref self) -> Vec[i64]` and `fn reset(mut ref
self)`. The arms draw from a seeded generator of their own (`Draw`, as
in kata 497: a linear congruential generator giving 15 bits a step),
so that every run, and the Python mirror, draws the same values.
`below(n)` puts two steps together into 30 bits and draws again when
they land in the last, incomplete run of `n`, so it is exactly uniform
on `[0, n)`; the largest grid, 10^8 cells, is under 2^30.

| file | mechanism | draws per flip |
|---|---|---|
| `random_flip_matrix.kara` ★ | a shuffle kept in a map: the cells numbered row by row are one array, a flip draws a slot among the free ones at the front, returns its cell and moves the last free slot's cell into it; only the slots whose cell moved are stored | 1 |
| `random_flip_matrix_reject.kara` | the flipped cells in a set; draw a cell of the whole grid until it is one not flipped | the cells over the free ones, on average |
| `random_flip_matrix_sorted.kara` | the flipped cells' numbers kept in order; draw k below the free count and walk the list to the k-th free cell, then put it in where the walk stopped | 1 |
| `random_flip_matrix_rows.kara` | a count of flipped cells per row and the flipped cells in a set; draw k, walk the rows to the one holding the k-th free cell, then walk its cells | 1 |
| `differential.kara` | each arm held to five properties |

The sorted and rows arms make the same flips from the same seed, the
k-th free cell in row order; the other two draw differently, so the
harness prints only what every correct arm must make true. Every arm
prints the same 9 lines: for the example, whether three flips flip
every cell and a flip after the reset is a cell; for one cell, the
flip before and after a reset; for grids of 1 by 7, 3 by 1, 2 by 3 and
3 by 3, flipped through and reset 300 times per cell on one solution,
whether every run flips every cell once and every cell gets its share
at every turn within 5 standard deviations; for 3 by 3, 4,500 times
four flips and a reset, whether the flips are different cells and the
first flip after a reset is fair; for the problem's largest, 10,000 by
10,000 and 999 flips, whether they are different cells and spread
evenly over 20 bands of rows and 20 of columns; and whether one seed
twice gives the same 300 flips, resets included, and another seed
other ones. `random_flip_matrix.py` mirrors the ★ arm, draws the same
flips, and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms, sharing one copy of
`Draw`. Each arm is held to the properties below on its own: 1,500
random grids of up to 3, 40 or 300 on a side in turn, with 30 calls
each, about one in eight a reset and always one when the grid is full,
for P1 and P2; and ten seeded runs for P3 to P5.

| | property |
|---|---|
| P1 | every flip is a cell of the grid |
| P2 | no cell is flipped twice between resets |
| P3 | the first flip of a fresh grid of 2 to 12 cells, from 3,000 seeds: every cell its share, within 5 standard deviations |
| P4 | every cell of a grid of 2 to 6 cells flipped, then a reset, 200 times per cell on one solution: every cell its share at every turn |
| P5 | after a reset partway through a grid of 4 to 12 cells, 3,000 times: the next flip gives every cell its share |

It prints `1500 cases and 10 runs, 4 arms, 12120 checks, 0 failures`
under `karac __mir-run`.

## Mutation testing

Twelve edits to `differential.kara`, two to each arm that change its
flips, and four that do not, each run under `karac __mir-run`. All
eight that change flips are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the last free slot's cell taken as the slot's own number, whatever moved there | P2 335, P4 8 |
| M2 | ★: the cell split into row and column by the row count | P1 1284, P3 7, P4 10, P5 9 |
| M3 | reject: a flipped cell is taken again | P2 688 |
| M4 | reject: the larger of two draws | P3 10, P4 10, P5 10 |
| M5 | sorted: the walk stops at a flipped cell equal to it (`<` for `<=`) | P2 688, P4 10 |
| M6 | sorted: the cell pushed on the end, so the list is not in order | P2 511, P4 8 |
| M7 | rows: a row's count never goes up | P1 542, P4 5 |
| M8 | rows: the column walk counts flipped cells too | P2 560, P4 6 |
| E1 | ★: a reset makes a new map | 0 |
| E2 | reject: the row and the column drawn apart | 0 |
| E3 | sorted: k counted from the last free cell | 0 |
| E4 | rows: a reset zeroes the counts in place | 0 |

M4 is the only one that keeps every flip a fresh cell of the grid: it
only bends the chances, toward the cells numbered last, so only the
counting properties see it, and all thirty of its counting checks
fail. M2 is caught by P1 wherever the grid is not square; on a square
it is right, which is why P2 sees nothing. M7 never counts a row as
filling, so the column walk runs off the end of the row: P1. The
other five return a cell already flipped, and P2 sees them. E2 to E4
draw differently from the arms they edit but every cell is still
equally likely, which is what the counting properties check: none of
them fails one.

## Verification

Every arm prints the same output as `random_flip_matrix.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and runs clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints `12120 checks, 0 failures` on the first two and runs clean under
the third. `karac check` passes on every arm, the differential and the
bench program.

On the frozen legacy backends the reject, sorted and rows arms agree:
`karac run --interp`, LLJIT, legacy `karac build` and a
`KARAC_AUTO_PAR=1` build print the same output. Legacy `karac build`
warns on each of them that `p` is "moved here, used again here", where
the harness lends a flip to `number_of` and then reads it; the output
is right all the same. The ★ arm, the differential and the bench
program are refused by all of them at type checking: legacy types the
value a `Map`'s `get` returns and the items of a `Vec`'s `iter()` by
value, so it refuses `*cell`, `*op` and `*i`, "unary '*' requires 'ref
T' ... found 'i64'". Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 10,000 random grids of up
to 10,000 by 10,000 and makes 1,000 calls on each (the problem's
most): a reset one time in a hundred and whenever the grid is full,
else a flip, folding every flip into a checksum. Every implementation
prints `10000 grids, 1000 calls each: checksum 206361612`, the Kāra
program under `karac __mir-run` included (in 76 s).

Every mirror keeps the moved slots in its language's own map, a fresh
one per grid: `HashMap` in Rust, a built-in map in Go, a dict in
Python. C has none, so its mirror is a 4,096-slot open-addressing
table with linear probing; a reset empties only the slots in use.
Spot timings on a shared 4-core container, three runs each (two for
Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.12 to 0.15 s |
| Rust (`rustc -O`) | 0.56 to 0.64 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.55 to 0.57 s |
| Go | 0.87 to 0.98 s |
| Python | 13.2 to 15.3 s |
| Kāra (`karac build --mir`) | 0.95 to 1.01 s |

The legacy `karac build` refuses this program at the same `*cell` (see
Verification). So `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend. That edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`0736eef763`. Under `karac __mir-llvm-run` the program prints the same
line in 9.5 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

## Compiler findings

None filed. Every arm, the differential and the bench program run
right on the v2 backends, and `karac check` passes on all of them as
first written.
