# 1102. Path With Maximum Minimum Value

Given an `m x n` integer matrix `grid`, return the maximum score of a
path starting at `(0, 0)` and ending at `(m - 1, n - 1)` moving in the
4 cardinal directions.

The score of a path is the minimum value in that path. For example,
the score of the path `8 → 4 → 5 → 9` is `4`.

```
grid = [[5,4,5],[1,2,6],[7,4,6]]                    ->  4
grid = [[2,2,1,2,2,2],[1,2,2,2,1,2]]                ->  2
grid = [[3,4,6,3,4],[0,2,1,1,7],[8,8,3,2,7],
        [3,2,4,9,8],[4,1,2,0,0],[4,6,5,4,3]]        ->  3
```

**Constraints:** `m == grid.length`; `n == grid[i].length`; `1 <= m, n
<= 100`; `0 <= grid[i][j] <= 10^9`.

The arms are `fn maximum_minimum_path(grid: Vec[Vec[i64]]) -> i64`. The
start and the end are on every path, so the answer is never above
either of their values, and a 1 by 1 grid's answer is its one value.

## Approaches

| file | mechanism |
|---|---|
| `maximum_minimum_path.kara` ★ | a best-first search: a `PriorityQueue.max_first()` of cells keyed by the best minimum a path from the start can carry into them, so each cell is settled once, with the largest minimum it can have, and the end's is the answer. O(mn log mn) |
| `maximum_minimum_path_union.kara` | union-find over the cells from the largest value down, sorted with `sort_by` on the tuple's first field: each cell joins the neighbours already in, and the first value at which the start and the end share a group is the answer. `find` finds the root, then points the path at it |
| `maximum_minimum_path_search.kara` | binary search over the grid's values, collected with `flat_map`, sorted and `dedup`ed: a path of cells all at least `v` exists for every `v` up to the answer and none above, each probe a depth-first search with a `Vec` as the stack |
| `maximum_minimum_path_relax.kara` | relaxation with a `VecDeque`: every cell keeps the best minimum found so far, and a cell whose best rises puts its neighbours back in the queue, until nothing rises |
| `maximum_minimum_path_flood.kara` | a flood that spreads as the threshold falls: the cells grouped by value in a `SortedMap[i64, Vec[(i64, i64)]]` through `entry(..).or_insert(..)`, taken from the largest down with `iter().rev()`, and each one opened; an open cell next to the flooded region, or the start, floods, and the flood spreads through every open cell it touches. A closure gives each cell's neighbours |
| `maximum_minimum_path_solution.kara` | a Rust solution as LeetCode's Rust users write it (`use std::collections::BinaryHeap`, `vis` marked as cells are pushed, a `dirs` array, `as i32` and `as usize` round trips), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 13 lines: the answers for LeetCode's three
examples and seven more (one cell, a start of 0, a low cell in a single
row and in a single column, a wall to walk round, four values of 10^9,
a way that must turn back up), then over 2000 random grids of up to 12
by 12 the sum of the answers (`minimums total 201316, checksum
988526839`), and two grids of 100 by 100, LeetCode's largest: values
below 10^9 at random, and a snake, one winding path of high values
through low ones, 5050 cells long. `maximum_minimum_path.py` mirrors the
★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every path from the start to the end that visits no cell
twice, walked one step at a time, and the largest of their minimums. (A
path that comes back to a cell has the same minimum as the one that
cuts the loop out, so the simple paths are enough.) Walking every path
needs small grids, so every grid has at most 16 cells. It checks 2000
problems in four kinds of 500: up to 4 by 4 with values below 10; up to
4 by 4 with values below 3, so that many paths tie; one row or one
column of 1 to 12 cells below 1000; and a snake of values 10 to 19
through values below 10, 5 rows by 2 or 3 columns or the same
transposed, along the first row, back along the middle one and along
the last, so that the best path must step left, or up. Every random
choice is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal one |
| P2 | the answer is a value of the grid, no larger than either end, and by a second reading, a mark spread one sweep at a time, a path of cells at least that large exists and none of cells above it |
| P3 | the grid transposed, and turned half round so that the start and the end change places, give the same answer |
| P4 | every value `v` moved to `2v + 1` moves the answer the same way |
| P5 | every value capped at `cap` gives the answer capped at `cap` |
| P6 | one cell lowered to 0 never raises the answer, and the same cell raised to the grid's largest value never lowers it |

All 72,000 checks pass on every arm: `2000 problems: checksum
360548956, 72000 checks over 6 arms: 0 failures`. A Python reading of
the same problems, walking every path, gives the same checksum.

P1 walks every path and P2 judges the answer by thresholds; P3 to P6
compare the arm only with itself.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`, each failing the same way
under both. All thirty are caught. Fifteen are kept, no two failing the
same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a cell keyed by its own value, not the path's minimum | P1 1285, P2 1285, P3 1635 |
| M2 | ★: the smallest minimum taken first | P1 737, P2 737, P3 1 |
| M3 | ★: only right and down | P1 500, P2 500 |
| M4 | ★: the start's value never counted | P1 360, P2 360, P3 698 |
| M5 | union: one step toward the root | P1 950, P2 950, P3 721, P5 661, P6 287 |
| M6 | union: the end of the first row taken for the end | P1 777, P2 777, P3 1598 |
| M7 | union: a cell numbered by the wrong row length | stops: index out of bounds |
| M8 | search: a cell equal to the bound shut out | P1 665, P2 665, P3 144, P5 213, P6 35 |
| M9 | search: the values never sorted | P1 840, P2 840, P3 1266, P5 287, P6 295 |
| M10 | relax: a risen cell never looked at again | P1 1727, P2 1727 |
| M11 | relax: never a step up | P1 241, P2 241, P3 500 |
| M12 | flood: the start never flooded | P1 2000, P2 2000 |
| M13 | flood: no cell opened but the ones that flood | P1 1635, P2 1635, P3 380, P5 816, P6 107 |
| M14 | solution: a cell's own value never counted | P1 1272, P2 1272, P3 1635 |
| M15 | solution: every value halved on the way in | P1 1561, P2 1561, P4 1243, P5 884 |

Of the fourteen that run to the end, P1 and P2 catch all fourteen, P3
ten, P5 five, P6 four and P4 one. P1 and P2 fail on the same problems
every time: a value of the grid that a path of cells at least that
large reaches, and no path above it, is the literal answer. The snakes
are what M3 and M11 need: no other problem's best path steps left or
up, so a search that only goes right and down fails on the 500 snakes
and nothing else, and one that never steps up on the 241 snakes that
climb, then on all 500 once P3 turns them round. Before the snakes
were added, M3, M11 and two edits not kept passed every check.
P4 sees only M15, the one edit that changes the values rather than
which cells a path may use: halving `2v + 1` is not `2(v / 2) + 1`.
P3 to P6, which compare the arm only with itself, catch all but three:
M3, M10 and M12 answer wrongly the same way whatever the grid's
orientation, scale or cap. M7, numbering the cells by the wrong row
length, stops on an index past the end.

Of the fifteen not kept, six fail as a kept edit: the relax arm
carrying a cell's own value and the solution arm answering the end's
own value fail as M1, the search arm never checking the start as M4,
the solution arm never stepping up, or stepping left in its place, as
M11, and the flood spreading into closed cells as M14. The other nine
fail in ways of their own but were not needed: the ★ arm taking the
last row or column for the end, the union and flood arms taking the
cells smallest first, the union arm joining a neighbour before it is
in, the search arm taking the last row for the end and never stepping
right, the relax arm answering the bottom-left corner and never leaving
the first row downward, and the flood never stepping down.

## Verification

Every arm prints the same output as `maximum_minimum_path.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
every arm and the differential. `karac check --output=json` reports
nothing on any file, and `karac fix` has nothing to apply.

The kata found no compiler gap. The ★ arm was written as Kāra, and the
other five as Rust writes them; `karac fix` carried every Rust spelling
to a clean check, in three to five rounds each: `Vec<..>` to `Vec[..]`,
`vec![vec![false; n]; m]` to `Vec.filled(m, Vec.filled(n, false))`,
`Vec::new()` and `VecDeque::new()` to `.new()`, `&mut Vec<usize>` to
`mut ref Vec[i64]` with every `usize` index and `as usize` / `as i64`
cast between them dropped, `&&`, `||` and `!` to `and`, `or` and
`not`, `for &(r, c) in` to `for (r, c) in`, `cmp(&a.0)` to `cmp(a.0)`,
`flatten()` on the rows to `flat_map(|v| v.iter())`, the closure's
`-> Vec<(usize, usize)>` dropped, and in the Rust solution `use
std::collections::BinaryHeap` dropped, `BinaryHeap::new()` to
`PriorityQueue.max_first()`, `0usize` to `0` and `struct Solution {}`
declared. Two leftovers read oddly but are what `karac fix` leaves: the
relax arm's `best[(m - 1)][(n - 1)]`, once `best[(m - 1) as usize]..`,
and the solution's `let (x, y) = (x, y);`, once the `as usize` round
trip.

## Benchmarks

The bench builds 32 grids of 100 by 100 once, LeetCode's largest, with
values below 10^9. Each of 8 rounds halves one cell in every grid and
solves it with the ★ arm: 256 searches over up to 10^4 cells each.
Every implementation prints `8 rounds over 32 grids of 100 by 100:
minimums total 56128209144, checksum 667005405`. C and Go each carry a
binary max-heap of `(minimum, row, column)` compared as tuples, as
Kāra's `PriorityQueue` and Rust's `BinaryHeap` do; Python negates the
key for `heapq`, which breaks ties the other way but settles every cell
with the same minimum.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `33ef2a7ad2`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| Rust (`rustc -O`) | 0.306 to 0.333 s | 0.312 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.315 to 0.360 s | 0.329 s |
| C (`clang -O3`) | 0.320 to 0.366 s | 0.334 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.324 to 0.381 s | 0.338 s |
| Kāra (`karac build`) | 0.325 to 0.361 s | 0.341 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.338 to 0.406 s | 0.349 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.330 to 0.358 s | 0.349 s |
| Go | 0.744 to 0.874 s | 0.784 s |
| Python | 4.210 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra, C and Rust sit within the spread of one another; Go takes
about 2.2x their time. Python takes about 12x Kāra's time.
