# 885. Spiral Matrix III

You start at the cell `(rStart, cStart)` of an `rows x cols` grid facing
east. The northwest corner is at the first row and column in the grid,
and the southeast corner is at the last row and column. You will walk in
a clockwise spiral shape to visit every position in this grid. Whenever
you move outside the grid's boundary, we continue our walk outside the
grid (but may return to the grid boundary later). Eventually, we reach
all `rows * cols` spaces of the grid. Return an array of coordinates
representing the positions of the grid in the order you visited them.

```
rows = 1, cols = 4, rStart = 0, cStart = 0  ->  [[0,0],[0,1],[0,2],[0,3]]
rows = 5, cols = 6, rStart = 1, cStart = 4  ->  [[1,4],[1,5],[2,5],[2,4],[2,3],[1,3],[0,3],[0,4],[0,5],[3,5],[3,4],[3,3],[3,2],[2,2],[1,2],[0,2],[4,5],[4,4],[4,3],[4,2],[4,1],[3,1],[2,1],[1,1],[0,1],[4,0],[3,0],[2,0],[1,0],[0,0]]
```

**Constraints:** `1 <= rows, cols <= 100`, `0 <= rStart < rows`,
`0 <= cStart < cols`.

## Approaches

| file | mechanism |
|---|---|
| `spiral_matrix_iii.kara` ★ | walking the spiral: east 1, south 1, west 2, north 2, east 3, and on, two legs of each length and a right turn after each, a step at a time off the grid as well as on it, keeping the positions inside the grid. O(max(rows, cols)^2) |
| `spiral_matrix_iii_rings.kara` | ring by ring: the positions k steps from the start in both directions at most, and exactly k in one, form a ring, walked down its east side, west along its south side, up its west side and east along its north side, with each side's part outside the grid skipped. O(max(rows, cols)^2) |
| `spiral_matrix_iii_ranked.kara` | each position's place, then a sort: ring k comes after the (2k - 1)^2 positions inside it, and along the ring a position's offset follows from which side it is on, so every position's place in the spiral has a formula, and sorting the grid by it gives the order. O(rows * cols * log(rows * cols)) |
| `spiral_matrix_iii_turns.kara` | turning right whenever it can: a spiral is the walk that turns right whenever the position on its right is new; starting facing north, it turns east at once, and a board wide enough for the spiral marks every position visited. O(max(rows, cols)^2) |
| `spiral_matrix_iii_clipped.kara` | legs clipped to the grid: each leg lies in one row or column, so its part inside the grid is one run, found from the leg's ends without walking it. O(rows * cols + max(rows, cols)) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's two examples and eight
more (a 1 x 1 grid; a 3 x 3 grid from its centre; a 2 x 2 grid from its
bottom right; a column of 4 and a row of 5 from inside; 100 x 100 grids
from opposite corners; and a column of 100); the positions of 2,000
grids of up to 8 x 8 with the start anywhere, 39,781 in all, with a
checksum of every position in order; and of 100 grids of up to
100 x 100, with a checksum. Answers of more than 12 positions are shown
by their first four, their last, their count and the checksum.
`spiral_matrix_iii.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the walk written out as a string of moves, `E S W W N N E E E
S S S ...`, one letter a move, then taken from the start with the
positions inside the grid kept in order. It checks 2,100 cases: 2,000
grids of up to 7 x 7 against the statement, and 100 of up to 100 x 100,
LeetCode's sizes, against the other properties, each with the start
anywhere.

| | property |
|---|---|
| P1 | the statement's walk, on grids of up to 7 x 7 |
| P2 | rows * cols positions, the start first, each inside the grid and none twice |
| P3 | the grid inside a larger one, up to 5 more rows and columns on each side and the start moved with it: the larger grid's order, kept to this grid's positions and moved back, is this grid's order |
| P4 | the distance from the start, the larger of the row and column distances, never falls along the order |
| P5 | the start's row alone is walked one step right, one left, two right, two left and on, skipping the ends, and its column alone the same, down then up |
| P6 | each arm agrees with at least two of the other four |

P2 to P6 are checked on every case. It prints `2100 cases, orders
summing to checksum 707772476, 62500 checks over 5 arms: 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the walk starting south | P1 1226, P5 906, P6 1317 |
| M2 | ★: turning left after each leg | P1 1597, P5 915, P6 1696 |
| M3 | ★: a position one row past the grid kept | P1 1357, P2 1423, P3 1423, P5 1910, P6 1423 |
| M4 | rings: the east side started at its top corner | P1 819, P2 907, P6 907 |
| M5 | rings: the west side walked down | P1 961, P6 1058 |
| M6 | rings: the south side started at its east corner | P1 806, P2 892, P6 892 |
| M7 | ranked: the south side placed after the west side | P1 772, P6 865 |
| M8 | ranked: the top right corner put on the east side | P1 819, P2 907, P4 907, P6 907 |
| M9 | ranked: rings measured by the sum of the distances | P1 1462, P4 1453, P6 1560 |
| M10 | turns: turning left whenever it can | P1 1597, P5 906, P6 1696 |
| M11 | turns: starting facing east | P1 1226, P5 906, P6 1317 |
| M12 | turns: the start not marked as visited | P1 1903, P2 2003, P3 2079, P4 1791, P5 2003, P6 2003 |
| M13 | clipped: the west leg started at its corner | P1 806, P2 892, P6 892 |
| M14 | clipped: the legs lengthened after every four | P1 1955, P2 2055, P3 2065, P4 1843, P5 2055, P6 2055 |
| M15 | clipped: the south leg one column to the west | P1 1104, P2 1194, P3 1548, P4 611, P5 894, P6 1194 |

P1 and P6 kill all fifteen. M1 and M11 are one fault in two arms, the
spiral turned a quarter so that its first step goes south, and fail the
same cases; M6 and M13 are another, the south-east corner of each ring
walked twice. M5 and M7 are the closest to surviving: each reorders the
positions within a ring, which keeps every position once (P2), keeps
the distance from the start rising (P4), and is the same reordering in
the larger grid (P3), so only the statement and the arms' vote see it.
One mutant was replaced: one leg of each length, tried first for M1,
spaces the spiral's legs two apart, so some positions are never walked
and the walk never ends (stopped at 120 s).

## Verification

Every arm prints the same output as `spiral_matrix_iii.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build and the runtime archives are both at
kara `fe44986b7e`. Under `karac __mir-run` the arms take 0.6 to 1.8 s
each (the turns arm, stepping on a board every position of the spiral's
square, the slowest) and the differential 19 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The frozen legacy backends' interpreter, JIT and `karac build
--legacy`, with and without auto-par, print the same output for all five
arms. They refuse the differential, where a position is passed on from
the answer by index (`ring(got[i], ...)`), which legacy takes as a move
out of the `Vec`. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm, in all five languages: 6,000 grids of
50 x 50 to 100 x 100 with the start anywhere, 33,702,119 positions in
all, each grid's whole answer built and its last and middle positions
folded into a checksum. The answer is a `Vec` of two-element `Vec`s in
Kāra and Rust, as LeetCode returns it, a slice of slices in Go, a list
of lists in Python and in C an array of pointers to pairs, each pair
allocated on its own, as LeetCode's C signature returns it. Every
implementation prints `6000 grids of up to 100 x 100: 33702119 cells,
checksum 527933169`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.79 to 0.88 s | 0.85 s |
| Rust (`rustc -O`) | 1.02 to 1.16 s | 1.05 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.03 to 1.14 s | 1.08 s |
| Go | 1.70 to 2.01 s | 1.86 s |
| Python | 9.4 s | |
| Kāra (`karac build --mir`) | 0.96 to 1.16 s | 0.98 s |
| Kāra legacy (`karac build --legacy`) | 0.93 to 1.04 s | 0.98 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 884's does.

v2 takes 0.91 times Rust's median time under overflow checks, 1.00
times legacy's and 1.15 times C's. Under valgrind's cachegrind C runs
12.71 billion instructions, Rust with overflow checks 16.11 billion,
legacy 16.20 billion and v2 15.85 billion. Every implementation
allocates each position on its own, which most likely makes up most of
the time and keeps the five close (inferred from the layouts and counts,
not profiled). The comparison with C and Rust waits until after M4.
