# 1091. Shortest Path in Binary Matrix

Given an `n x n` binary matrix `grid`, return the length of the shortest
**clear path** in the matrix. If there is no clear path, return `-1`.

A **clear path** in a binary matrix is a path from the **top-left** cell
(`(0, 0)`) to the **bottom-right** cell (`(n - 1, n - 1)`) such that:

- all the visited cells of the path are `0`;
- all the adjacent cells of the path are **8-directionally** connected
  (they are different and share an edge or a corner).

The **length of a clear path** is the number of visited cells of this
path.

```
grid = [[0,1],[1,0]]                  ->  2
grid = [[0,0,0],[1,1,0],[1,1,0]]      ->  4
grid = [[1,0,0],[1,1,0],[1,1,0]]      ->  -1
```

**Constraints:** `n == grid.length == grid[i].length`; `1 <= n <= 100`;
`grid[i][j]` is `0` or `1`.

The arms are `fn shortest_path_binary_matrix(grid: Vec[Vec[i64]]) -> i64`.

## Approaches

| file | mechanism |
|---|---|
| `shortest_path_binary_matrix.kara` ★ | breadth-first search: a `VecDeque[(i64, i64)]` of cells and a grid of distances (`Vec.filled(n, Vec.filled(n, -1))`); each cell taken from the front gives its open, unreached neighbours (`for dr in -1..=1`, `for dc in -1..=1`) the next distance, so a cell's first distance is its shortest. Returns when the corner leaves the queue. O(n^2) |
| `shortest_path_binary_matrix_levels.kara` | breadth-first by levels: a `Vec` frontier of the cells first reached at the current length, the next built from their neighbours (ranges clamped with `max(0)` and `min(n)`), each cell closed in the arm's own `clone()` of the grid as it joins. O(n^2) |
| `shortest_path_binary_matrix_astar.kara` | A*: a `PriorityQueue` (smallest first) of (estimate, length, row, column), the estimate the length plus `max(n - 1 - row, n - 1 - column)`, the cells still needed with no wall in the way, from a closure over `n`. The bound is consistent, so the corner's first pop is final; stale entries are skipped against a grid of best lengths |
| `shortest_path_binary_matrix_meet.kara` | bidirectional breadth-first search: one search from each corner, each with a `Map[(i64, i64), i64]` of lengths, the smaller frontier grown a level at a time by a helper taking `mut ref` to its own map and the best meeting; a level that meets the other search ends the search with the best sum less one |
| `shortest_path_binary_matrix_relax.kara` | relaxation with no queue (Bellman-Ford on the grid): every open cell's length lowered to one more than its shortest neighbour's, in sweeps alternately from the top left and from the bottom right, until a sweep changes nothing. O(n^2) a sweep, as many sweeps as the path winds |
| `shortest_path_binary_matrix_solution.kara` | LeetCode's Rust template (`use std::collections::VecDeque`, `mut grid: Vec<Vec<i32>>`, a `[(i32, i32); 8]` of directions, `(0usize, 0usize, 1)` queued, `as i32` and `as usize` around each step, cells closed as queued), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 16 lines: LeetCode's three examples and nine
more (one cell open and one blocked, a blocked corner, two winding
corridors, a wall with no gap, an open grid, a cross of walls, a path
only on the diagonal), a count,
sum and checksum over 2000 random grids of 1 to 12 cells a side, a
quarter to a half blocked (`1275 without a path, lengths sum to 4863,
checksum 656403505`), and three grids of 100 by 100, LeetCode's largest,
10, 30 and 40% blocked (`105`, `113`, `123`).
`shortest_path_binary_matrix.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally, with no queue: the cells a clear path of at most k cells can
end on, grown from the start by every open cell touching one of them, k
by one, until they stop growing; the answer is the first k that holds
the corner. It checks 2000 problems: 1400 grids of 1 to 8 cells a side
and 600 of 1 to 16, a fifth to a half blocked, or one in four a winding
corridor (every other row a wall with one gap, at the right end and the
left end in turn, then one cell in eight flipped), and the corners
opened in three grids of four. Every random choice is drawn before any
arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the grid transposed gives the same answer |
| P3 | the grid turned half round, so the path is walked from the other corner, gives the same answer |
| P4 | one blocked cell opened makes no path longer, and loses none |
| P5 | a path takes at least n cells and at most every open one |
| P6 | every cell on no shortest path blocked (by the lengths from both corners, read literally) gives the same answer |

All 72,000 checks pass on every arm: `2000 problems: checksum 296132632,
72000 checks over 6 arms: 0 failures`. A Python breadth-first search
over the same problems gives the same checksum.

The corridors were added after a first run of the mutations below: on
random grids alone, the solution arm with no step to the left failed
one check in 72,000 and the levels arm giving up paths longer than 2n
failed one, since a random grid's shortest path rarely runs left or
long. With the corridors they fail 52 and 22.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`, each failing the same way
under both. Four survive, as they must: the A* arm expanding its stale
entries again, the two-ended search growing only from the start, the
relaxation sweeping forward every time (each changes only the work),
and the two-ended search stopping a level at its first meeting, which
we found no grid to tell from the best meeting in the level (none in
200,000 random grids of up to 14 cells a side). The other 26 are all
caught. Fifteen are kept, no two failing the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: no step to the left | P1 95, P2 116, P6 7 |
| M2 | ★: the last row walked through its walls | P1 120, P2 224, P3 226, P6 9 |
| M3 | ★: a stack, depth first | P1 167, P2 250, P3 256, P4 16, P6 167 |
| M4 | levels: a blocked start searched from | P1 76, P3 121, P5 21 |
| M5 | levels: paths longer than 2n given up | P1 22 |
| M6 | A*: the city-block estimate, which overestimates | P1 57, P2 78, P3 109, P4 3, P6 57 |
| M7 | A*: the largest estimate first | P1 771, P2 221, P3 398, P4 134, P6 747 |
| M8 | A*: done on reaching the last row | P1 404, P2 646, P3 687, P4 9, P6 20 |
| M9 | two-ended: a new cell given its parent's length | P1 1016, P5 1016 |
| M10 | two-ended: the one-cell grid not handled | P1 199 |
| M11 | relax: walls given lengths too | P1 1108 |
| M12 | relax: one sweep only | P1 61, P2 92, P6 4 |
| M13 | solution: no step down and right | P1 1203, P6 828 |
| M14 | solution: done on the last row or column | P1 903, P3 331, P6 259 |
| M15 | solution: no step to the left | P1 26, P2 26 |

P1 catches all fifteen; P6 nine, P2 eight, P3 seven, P4 four, P5 two.
P2 and P3 see the edits that treat directions or ends apart (a missing
step, the last row, a stack's order) and none that miscount length
alike in every direction; P5 sees those that miscount by a constant,
as P1 does. P6 is the one property that follows the path: a search
that returns too long a path (A*'s overestimate, the stack) gives
another length once every cell off the shortest paths is walled, and
so does one that cannot take a needed step. Three edits (M5, M10, M11)
are seen by P1 alone: they are wrong the same way in every direction
and by no constant.

Of the eleven caught but not kept, all fail exactly or nearly as
another edit and were not needed: each step counted twice (★ and
levels) and every length one more (relax) or the meeting cell counted
twice, alike to M9's family; the start cell not counted (★, levels,
solution); no step up (levels, A*) alike to M12; the solution arm as a
stack exactly as M3; and the relaxation taking no step from the left
(`P1 1203`).

## Verification

Every arm prints the same output as `shortest_path_binary_matrix.py`
under `karac __mir-run` (the v2 MIR interpreter), `karac
__mir-llvm-run`, and `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer) with no error. `karac run` and a `karac build` binary
print the same output for every arm and the differential. `karac check
--output=json` reports nothing on any file, and `karac fix` has nothing
to apply. Under `karac __mir-run` the differential takes 20 s.

The Rust arm reaches a clean check in two rounds of `karac fix`. The
first round is the syntax: the `use` line deleted, `struct Solution;` to
`struct Solution {}`, `mut grid: Vec<Vec<i32>>` to `grid: own
Vec[Vec[i32]]` with `let mut grid = grid;` at the body's start (Rust's
`mut` binding of an owned parameter), `[(i32, i32); 8]` to `Array[(i32,
i32), 8]`, `VecDeque::new` to `VecDeque.new`, `||` and `&&` to `or` and
`and`, and `for &(dr, dc)` to `for (dr, dc)`. The second is the integer
widths: `0usize` to `0`, and `nr as usize` to `nr as i64`, since Kāra
indexes with `i64`; that also settles the two comparisons of a `usize`
with an `i64` it reported, and drops an `as i64` that widens by itself.
The fix left a blank line where the `use` line was; `karac fmt` removes
it, and the arm does not keep it.

The differential's `show` was first written with Rust's turbofish,
`.collect::[Vec[String]]().join("")`. `karac check` refuses it: Kāra has
no call-site type arguments, and the message says to bind the
`collect` with a typed `let` first, which the arm does. That edit has no
machine fix, as it moves an expression out of a closure into a
statement.

## Benchmarks

The bench builds 200 random grids of 100 by 100 cells, LeetCode's
largest, 25 to 44% blocked with both corners open, once. Each of 20
rounds answers every grid with the ★ arm, folding the lengths into a
checksum. Every implementation prints `20 rounds over 200 grids of 100
by 100: 900 without a path, lengths sum to 364460, checksum 844445842`.
Each mirror runs the same search with a fresh grid of distances per
call: Rust a `VecDeque` and `Vec<Vec<i64>>`, Go a slice used as a queue
and `[][]int64`, Python a `deque` and lists, and C a ring of n^2 slots
and one flat `malloc`'d array of distances.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `c9f04eb673`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| C (`clang -O3 -march=x86-64-v3`) | 0.990 to 1.121 s | 1.042 s |
| C (`clang -O3`) | 0.970 to 1.096 s | 1.050 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.119 to 1.260 s | 1.165 s |
| Kāra (`karac build`) | 1.119 to 1.224 s | 1.190 s |
| Rust (`rustc -O`) | 1.285 to 1.465 s | 1.342 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 1.345 to 1.561 s | 1.392 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.356 to 1.566 s | 1.408 s |
| Go | 1.648 to 1.825 s | 1.711 s |
| Python | 35.8 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte.

The work is 4000 searches, each over much of a 10^4-cell grid:
eight neighbours tested per cell taken, each test a bounds check, a
read of the grid and one of the distances. Kāra is 16% ahead of
overflow-checked Rust at the same ISA and 13% ahead of plain `rustc
-O`; both index nested `Vec`s with a bounds check on each level. C,
with no checks and one flat array of distances, takes 89% of Kāra's
time, and Go 1.47x. Python takes 31x.
