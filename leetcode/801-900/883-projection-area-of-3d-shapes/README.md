# 883. Projection Area of 3D Shapes

You are given an `n x n` `grid` where we place some `1 x 1 x 1` cubes
that are axis-aligned with the `x`, `y`, and `z` axes. Each value
`v = grid[i][j]` represents a tower of `v` cubes placed on top of the
cell `(i, j)`. We view the projection of these cubes onto the `xy`, `yz`,
and `zx` planes. A projection is like a shadow, that maps our
3-dimensional figure to a 2-dimensional plane. We are viewing the
"shadow" when looking at the cubes from the top, the front, and the
side. Return the total area of all three projections.

```
grid = [[1,2],[3,4]]  ->  17
grid = [[2]]  ->  5
grid = [[1,0],[0,2]]  ->  8
```

**Constraints:** `n == grid.length == grid[i].length`, `1 <= n <= 50`,
`0 <= grid[i][j] <= 50`.

## Approaches

| file | mechanism |
|---|---|
| `projection_area.kara` ★ | one pass, rows and columns together: from above every cell holding a tower shows one square; from the front each row shows a column of squares as high as its tallest tower, and from the side each column of the grid the same. Reading `grid[i][j]` and `grid[j][i]` in the same loop gives row i's tallest tower and column i's together. O(n^2) |
| `projection_area_columns.kara` | row by row, keeping each column's tallest: the grid read once in row order, each row's tallest tower added as the row ends and a list holding the tallest tower met so far in every column, summed at the end. O(n^2) |
| `projection_area_transpose.kara` | the side view as the front view turned: the front view is the sum of the rows' tallest towers, and turning the grid over its diagonal makes its columns rows, so the side view is the front view of the turned grid. O(n^2), with a copy of the grid |
| `projection_area_layers.kara` | layer by layer: the shape cut into layers one cube high, layer h showing one square from the front for every row with a tower at least h high and one from the side for every such column, counted up to the tallest tower. O(n^2 * the tallest tower) |
| `projection_area_masks.kara` | views as sets of bits: a tower of v cubes is the set of levels 0 to v - 1, the number with its lowest v bits set, so a row's front view is the OR of its towers' numbers and its area the bits set; the top view of a row is the set of its columns holding a tower. Every set fits in 64 bits. O(n^2) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's three examples and seven
more (one empty cell; a 3 x 3 ring of towers 1 high around an empty
cell, and of towers 2 high around a tower 1 high; an empty 3 x 3 grid;
and 50 x 50 grids of towers all 50 high, of one tower 50 high in a
corner, and of towers `(i * j) % 51` high); the area of 3,000 grids of
up to 8 x 8 with towers up to 9 high, 250,885 in all; and of 1,000
grids of up to 50 x 50 with towers up to 50 high, with a checksum.
`projection_area.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every cube placed, each one projected onto the three planes,
and the distinct unit squares covered on each plane counted. It checks
3,400 cases: 3,000 grids of up to 6 x 6 with towers up to 7 high,
against the statement; and 400 of LeetCode's sizes, up to 50 x 50 with
towers up to 50 high, against the other properties. The ★ arm's areas
sum to 1,355,596.

| | property |
|---|---|
| P1 | the statement's area, on grids of up to 6 x 6 |
| P2 | the top view counts the towers, and the front and side views each show the tallest tower at least, and at most every cube and n columns of the tallest |
| P3 | the rows and the columns each in another order, and the grid turned over its diagonal, give the same area |
| P4 | a tower raised never shrinks the area, and adds at most its rise to each of the front and side views, and one square on top if its cell was empty |
| P5 | a second grid of up to 10 x 10 placed beside the first on the diagonal of a larger grid, the rest empty, gives the two areas added |
| P6 | each arm agrees with at least two of the other four |

P2 to P6 are checked on every case. P5's larger grids are up to 60
wide, more than LeetCode's 50, which the masks arm's 64-bit sets still
hold. It prints `3400 cases, areas sum to 1355596, 100000 checks over 5
arms: 0 failures` under `karac __mir-run` and `karac __mir-llvm-run`,
and the same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an empty cell counted on top | P1 2578, P2 1024, P5 3400, P6 2973 |
| M2 | ★: the side view read from the row again | P1 1872, P3 2244, P6 2244 |
| M3 | ★: each row and column read only from the diagonal on | P1 2374, P2 182, P3 2605, P6 2766 |
| M4 | columns: a column's tallest taken as its last tower | P1 2293, P2 124, P3 2594, P5 3123, P6 2685 |
| M5 | columns: a row's towers added up for the front view | P1 2325, P2 2135, P3 2244, P6 2717 |
| M6 | columns: an empty column showing one square from the side | P1 376, P2 253, P3 249, P6 382 |
| M7 | transpose: the grid never turned | P1 1872, P3 2244, P6 2244 |
| M8 | transpose: the top view counting cubes | P1 2751, P2 3070, P4 1781, P6 3150 |
| M9 | transpose: the first tower of each row never seen | P1 2369, P2 558, P3 2294, P5 2644, P6 2689 |
| M10 | layers: the top layer missed | P1 2805, P2 406, P4 404, P5 1519, P6 3204 |
| M11 | layers: a tower reaching a layer only above it | P1 2805, P2 393, P3 249, P6 3204 |
| M12 | layers: a layer 0 counted, which every row and column reaches | P1 3000, P2 1553, P6 3400 |
| M13 | masks: each tower one level taller | P1 3000, P2 1553, P6 3400 |
| M14 | masks: towers XORed into the side view | P1 2310, P3 2412, P4 429, P6 2702 |
| M15 | masks: the top view marking the row, not the column | P1 2325, P3 249, P6 2717 |

P1 and P6 kill all fifteen. M2 and M7 are one fault in two arms, the
side view taken to be the front view, and fail the same cases; only the
statement and the grid turned (P3) see it, as both views stay within
P2's bounds. M12 and M13 fail the same cases too: a layer 0 and a level
added to every tower, an empty one included, both add one square to
every row's front view and every column's side view, 2n in all. Only
M1, the empty cells of P5's larger grid each counted, fails P5 on every
case. None of the fifteen tried was equivalent or crashed, and none was
replaced.

## Verification

Every arm prints the same output as `projection_area.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `89d76e3ff2` and the runtime
archives at `e903d5b111`, with no runtime change between them. Under
`karac __mir-run` the arms take 1.5 to 2.2 s each, but for the layers
arm, which reads the grid once for every layer, at 14 s; the
differential takes 31 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The frozen legacy backends print the same output for all five arms
under the interpreter, the JIT and `karac build --legacy`, with and
without auto-par, and the same line for the differential under all but
the interpreter, which prints another sum (1,374,502) with 0 failures.
The arms agree with one another and with the statement there, so the
differential's random grids most likely differ. The differential draws
a grid's width inside the call that is also handed `mut seed`
(`random_grid(mut seed, next_random(mut seed) % 10 + 1, ...)`), and the
arms' harness never does; kata 882's differential and harness both did,
and there the interpreter's totals differed in every arm too. That
points at the order in which the interpreter evaluates those arguments
(inferred from the pattern, not traced). Legacy is frozen, so this is
noted, not filed.

## Benchmarks

The bench program uses the ★ arm, in all five languages: 100 grids of
40 x 40 to 50 x 50 with towers up to 50 high, a quarter of the cells
empty; in each grid 1,000 towers are rebuilt one at a time, a random
cell given a random height, and the area taken after each, 100,000
areas over about 2 x 10^8 cells in all. The grid is a `Vec` of `Vec`s
in Kāra and Rust, as LeetCode passes it, a slice of slices in Go, a list
of lists in Python and an array of row pointers in C. Every
implementation prints `100 grids, 1000 towers rebuilt in each: area
612174289, checksum 190304639`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.15 to 0.17 s | 0.16 s |
| Rust (`rustc -O`) | 0.25 to 0.29 s | 0.26 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.24 to 0.30 s | 0.25 s |
| Go | 0.28 to 0.31 s | 0.29 s |
| Python | 21.6 s | |
| Kāra (`karac build --mir`) | 0.24 to 0.32 s | 0.25 s |
| Kāra legacy (`karac build --legacy`) | 0.24 to 0.27 s | 0.25 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 882's does.

v2 takes 1.03 times Rust's median time under overflow checks, 1.01
times legacy's and 1.60 times C's. Under valgrind's cachegrind C runs
2.68 billion instructions, Rust with overflow checks 4.49 billion,
legacy 4.27 billion and v2 4.35 billion. v2 runs the most branches,
1.02 billion against about 0.85 billion for Rust and legacy, and
mispredicts 57.8 million of them, 5.7%, where Rust and legacy mispredict
4.8 and 4.7 million, 0.6%: v2 most likely branches on a comparison the
others turn into a conditional move, such as the running maximum or the
empty-cell test (inferred from the counts, not read from the machine
code). C mispredicts 4.7 million of its 0.11 billion branches. The
comparison with C and Rust waits until after M4.
