# 1162. As Far from Land as Possible

Given an `n x n` `grid` containing only values `0` and `1`, where `0`
represents water and `1` represents land, find a water cell such that
its distance to the nearest land cell is maximized, and return the
distance. If no land or water exists in the grid, return `-1`.

The distance used in this problem is the Manhattan distance: the
distance between two cells `(x0, y0)` and `(x1, y1)` is `|x0 - x1| +
|y0 - y1|`.

```
grid = [[1,0,1],[0,0,0],[1,0,1]]  ->  2
grid = [[1,0,0],[0,0,0],[0,0,0]]  ->  4
```

**Constraints:** `n == grid.length == grid[i].length`; `1 <= n <= 100`;
`grid[i][j]` is `0` or `1`.

The arms are `fn max_distance(grid: Vec[Vec[i64]]) -> i64`.

## Approaches

The answer is the largest, over the water cells, of each one's distance
to its nearest land; the arms differ in how they find every cell's
nearest land without trying every pair.

| file | mechanism |
|---|---|
| `max_distance.kara` ★ | a breadth-first search from every land cell at once: the land starts the queue at distance 0 in a flat distance array, each water cell is reached first from its nearest land, and the last cell reached is the farthest. O(n^2) |
| `max_distance_dp.kara` | two sweeps: each cell's distance taken first from above and the left in reading order, then from below and the right in reverse, since a nearest land cell lies in one of the four quadrants and each sweep sees two. O(n^2) |
| `max_distance_rings.kara` | rings: the land grows by one ring of water a round, a `Set[(i64, i64)]` of the cells taken and the newest ring as the frontier, until no water is left; the rounds it took are the answer. O(n^2) set operations |
| `max_distance_rows.kara` | row by row: in each row, every column's distance to that row's nearest land, by a sweep each way; a cell's nearest land is the least, over the rows, of the rows apart plus that row's distance at its column. O(n^3) |
| `max_distance_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, the `Vec<Vec<i32>>` rebound `mut` and marked in place, a `VecDeque` of `(usize, usize)`, a `dirs` array walked with `for &(di, dj)`, `as i32` and `as usize` round trips for the bounds), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's examples (2, 4); one land
cell and one water cell (-1, -1); all land and all water (-1, -1); a
cell two away diagonally (`[[0,1],[0,0]]`: 2); land in two opposite
corners of 4 by 4 (3). Then 1000 random grids of 1 to 20 a side with
land at odds from 1 in 100 to 99 (`1000 random grids: total 3337,
checksum 172379210`), and three of 100 a side, the constraints' most:
one land cell in a corner (198), one in the middle (100), and land at
odds 1 in 500 (50). `max_distance.py` mirrors the ★ arm and its output
is byte-identical; a Python reading that tries every water cell against
every land cell gives the same output.

The Mend loop: the four Kāra arms check clean as written. The Rust arm
takes three rounds (18, 1 and 4 edits): `Vec<Vec<i32>>` to
`Vec[Vec[i32]]`, `VecDeque::new()` to `VecDeque.new()`, `||` to `or`,
`for &(di, dj)` to `for (di, dj)`, `Solution::` to `Solution.`, the
adapter's `|&c|` to `|c|`, and the `use std::collections::VecDeque` line
deleted; then `struct Solution {}`; then the parameter made `own
Vec[Vec[i32]]`, since `let mut grid = grid` moves it, and the `as
usize` casts and the adapter's `as i64` dropped. That last round leaves
`let (x, y) = (x, y);`, a rebinding that now does nothing; it is kept as
the fix wrote it. The `VecDeque`, the `dirs` array and the `as i32`
casts are kept. Its output matches on the first run.

Writing the harness found a gap in the diagnostics: a method that does
not exist, called inside a `map` closure (`c.parse_int()` while parsing
the grids), drew a second error from the `collect()` after it, naming
the poisoned type, `` trait bound `C: FromIterator[<error>]` is not
satisfied ``. That is kara B-2026-11-15-48, fixed at `1bdebaaa70`; the method's own
error is now the only one.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every water cell's distance to every land cell, the nearest
kept, and the farthest of those. It checks 1200 grids in four kinds of
300: 1 to 6 a side and 1 to 14 a side, land at odds from 1 in 100 to 99;
5 to 24 a side with one to three land cells; and 5 to 24 a side at odds
from 2 to 50 in 100. The literal reading runs where the water cells
times the land cells are at most 40,000, on 1174 of the grids. Every
random choice the properties make is drawn before any arm answers.

| | property |
|---|---|
| P1 | the distance is the literal one (1174 grids) |
| P2 | one of the square's eight symmetries, drawn, keeps the distance |
| P3 | a water cell made land never raises the distance, nor takes it below 1, while land and two water cells remain |
| P4 | a land cell made water never lowers the distance, while two land cells remain |
| P5 | the grid among its mirror images, a square of twice the side, keeps the distance: a mirrored land cell is never nearer than its original |
| P6 | one land cell alone, at a drawn place `(a, b)` of the same side, is `max(a, n-1-a) + max(b, n-1-b)` away, or -1 when `n` is 1 |

All 33,100 checks pass on every arm: `1200 grids (1174 read literally):
checksum 160558181, 33100 checks over 5 arms: 0 failures`, in 43 s
under `karac __mir-run`. A Python reading of the same draws, with the
mirror against the literal reading, gives the same checksum.

## Mutation testing

Nineteen edits to the differential, three or four to each arm, each run
under `karac __mir-run` and `karac __mir-llvm-run` with
`KARAC_HASH_SEED=1`, each failing the same way under both. Eighteen are
caught and one is equivalent: the two-sweep arm's best starting at 0
rather than -1 (D2), since an all-land grid then answers 0, which the
arm's own `best == 0` test already turns into -1.

| # | mutation | failures by property |
|---|---|---|
| B1 | ★: a grid of all land answers 0 | P1 110, P6 78 |
| B2 | ★: each step counted twice | P1 956, P6 1122 |
| B3 | ★: no step to the left | P1 492, P2 458, P3 74, P4 49, P5 483, P6 520 |
| B4 | ★: a land cell reached again | P1 295, P2 238, P3 52, P4 53, P5 465 |
| D1 | dp: the second sweep never looks right | P1 647, P2 310, P3 424, P4 35, P5 158, P6 948 |
| D3 | dp: the no-land mark too small | P1 318, P3 318, P4 88, P5 318, P6 1109 |
| D4 | dp: the first sweep never looks left | P1 645, P2 330, P3 398, P4 46, P5 400, P6 960 |
| R1 | rings: stopped with one water cell left | P1 525, P3 23, P5 529, P6 991 |
| R2 | rings: a diagonal step taken | P1 190, P2 242, P5 128, P6 250 |
| R3 | rings: a grid of all land answers 0 | P1 110, P6 78 |
| W1 | rows: the distance as the larger of the two | P1 712, P6 1122 |
| W2 | rows: land to the right one farther | P1 389, P2 336, P5 303, P6 599 |
| W3 | rows: only the rows above and its own | P1 629, P2 336, P5 580, P6 942 |
| W4 | rows: a grid of no land answers its no-land mark | P1 108, P5 108 |
| X1 | solution: the land's mark of 1 counted as a step | P1 956, P6 1122 |
| X2 | solution: the last row never reached | P1 251, P2 289, P3 10, P5 252, P6 528 |
| X3 | solution: a diagonal step taken | P1 190, P2 242, P5 128, P6 250 |
| X4 | solution: a grid of all land answers 0 | P1 110, P6 78 |

P1 catches all eighteen, P6 sixteen, P5 twelve, P2 nine, P3 seven and
P4 five. The symmetry (P2) sees exactly the edits that favour one
direction or side, and is blind to the ones that are wrong the same way
everywhere (B2, W1). The all-land edits (B1, R3, X4) are seen only by
P1 and by P6's one-cell grids of side 1, and the no-land edit (W4) only
by P1 and P5, whose doubled grid of no land answers a mark twice as
large.

## Benchmarks

`bench/` times the ★ arm against the same breadth-first search in C,
Rust, Go and Python, each over a flat distance array and a queue of cell
indices allocated per call (static arrays in C). 16 grids of 100 by 100,
the constraints' most, are built once, two each at land odds from 1 in
1000 to 9 in 10; each of 300 rounds flips one random cell of every grid
and solves it. Every program prints `300 rounds over 16 grids of 100 by
100: total 54174, checksum 187934664`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `f5f9065de8`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| C (`clang -O3 -march=x86-64-v3`) | 0.441 to 0.562 s | 0.467 s |
| C (`clang -O3`) | 0.440 to 0.505 s | 0.476 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.583 to 0.812 s | 0.612 s |
| Kāra (`karac build`) | 0.578 to 0.711 s | 0.615 s |
| Rust (`rustc -O`) | 0.601 to 0.770 s | 0.641 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.676 to 0.833 s | 0.692 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.676 to 0.773 s | 0.699 s |
| Go | 1.398 to 1.633 s | 1.481 s |
| Python | 28.5 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane; a plain `karac build` gives the same binary, byte
for byte, so the two Kāra rows are one program timed twice. Kāra takes
about 0.88x overflow-checked Rust's time, the equal-safety comparison,
and about 1.3x C's, whose arrays are allocated once. Go, which makes
its distance array and grows its queue by `append` on every call, takes
about 2.4x Kāra's time, and Python about 47x.
