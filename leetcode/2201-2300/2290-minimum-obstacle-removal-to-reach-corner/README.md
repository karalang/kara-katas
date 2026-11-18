# 2290. Minimum Obstacle Removal to Reach Corner

You are given a **0-indexed** 2D integer array `grid` of size `m x n`.
Each cell has one of two values:

- `0` represents an **empty** cell,
- `1` represents an **obstacle** that may be removed.

You can move up, down, left, or right from and to an empty cell.

Return *the **minimum** number of **obstacles** to **remove** so you can
move from the upper left corner* `(0, 0)` *to the lower right corner*
`(m - 1, n - 1)`.

```
grid = [[0,1,1],[1,1,0],[1,1,0]]               ->  2
grid = [[0,1,0,0,0],[0,1,0,1,0],[0,0,0,1,0]]   ->  0
```

**Constraints:** `m == grid.length`; `n == grid[i].length`;
`1 <= m, n <= 10^5`; `2 <= m * n <= 10^5`; `grid[i][j]` is either `0`
or `1`; `grid[0][0] == grid[m - 1][n - 1] == 0`.

A shortest path where a step onto an empty cell costs 0 and a step onto
an obstacle costs 1. With only two weights a deque keeps the cells in
order of cost: a 0-step goes to the front, a 1-step to the back, and
each cell is settled the first time it comes off. O(m * n).

## Approaches

| file | mechanism |
|---|---|
| `obstacles.kara` ★ | the 0-1 breadth-first search over a `VecDeque[(i64, i64)]`, the cells' best costs in a flat `Vec.filled(m * n, i64.MAX)`, a cell settled when it first comes off |
| `obstacles_naive.kara` | Bellman-Ford on the grid: every cell relaxed from its four neighbours, sweep after sweep, until a sweep changes nothing. O((m n)^2) at worst |
| `obstacles_heap.kara` | Dijkstra: a `PriorityQueue[(i64, i64, i64)]` of cost, row and column, smallest first, and a `Set[(i64, i64)]` of the cells settled. O(m n log(m n)) |
| `obstacles_struct.kara` | `struct Field` floods level by level: `flood` reaches every cell it can at the current cost through empty cells, by a stack, and returns the obstacles on the edge, which start the next level |
| `obstacles_iter.kara` | a plain FIFO `VecDeque` of the cells whose cost just fell, revisited each time it falls again (SPFA); the neighbours by `map` and `filter` over the four moves and `collect` |
| `obstacles_solution.kara` | LeetCode's Rust template: `Vec<Vec<i32>>` in, `i32` out; the 0-1 search over `usize` indexes and `i32` distances, with `vec![vec![i32::MAX; n]; m]`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples; one cell;
one row and one column, each with obstacles to pass; a wall to break
through once; a winding path of empty cells that needs no removal; then
2000 random grids of 1 to 20 by 1 to 20, each cell an obstacle with
chance from 1 in 10 to 9 in 10 and the corners empty, with a checksum
and the obstacles removed in all. `obstacles.py` mirrors the ★ arm and
its output is byte-identical.

`karac fix` carries the template in one call, reporting 14 edits: the
`use std::collections::VecDeque;` line deleted, since `VecDeque` is in
the prelude; `struct Solution;` to `struct Solution {}`; the
`Vec<Vec<i32>>` brackets, three edits; `i32::MAX` and `VecDeque::new`
to `.` paths; the `&` of `for &(di, dj)` dropped; `||` to `or` three
times; the two `vec![..; n]` to `Vec.filled(n, ..)`; and in the adapter
the `as i64` on the template's `i32` answer dropped. The `0usize` and
`0i32` suffixes and the `as usize` / `as i32` casts stay as written.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for `k = 0, 1, 2, ..`, is there a way from corner to corner
that passes through at most `k` obstacles? A breadth-first search over
the states (row, column, obstacles passed so far), each state seen
once, answers each `k`, with no costs, no deque and no ordering; the
answer is the first `k` that has a way. It checks 300 random grids
drawn as the arms' harness draws them; then 30 where every other row is
a wall with one gap or, one time in three, none; then 30 of obstacles
everywhere but the corners. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | `0 <= answer <=` the obstacles along the top row and the right column, a way that is always there |
| P3 | the grid transposed: the same answer |
| P4 | the grid turned half round, so that the corners swap: the same answer |
| P5 | the first obstacle in reading order cleared: the answer the same or one less |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 201668941, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading by Dijkstra
over `heapq`. On a failure it prints the first ten and then the count
by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: every step to the back | P1 51, P6 51 |
| M2 | ★: the steps the other way round | P1 298, P2 229, P3 214, P4 214, P5 15, P6 298 |
| M6 | ★: the corner's own cell counted | P1 360, P2 91, P6 360 |
| M7 | naive: the left neighbour from column 2 | P1 344, P2 344, P3 34, P6 344 |
| M8 | naive: the row above never looked at | P1 340, P2 340, P3 34, P6 340 |
| M9 | naive: the answer from the top-right corner | P1 228, P3 268, P4 177, P6 228 |
| M12 | heap: largest first | P1 319, P2 295, P3 241, P4 242, P5 12, P6 319 |
| M14 | heap: the upward move lost | P1 19, P3 50, P6 19 |
| M15 | heap: the corner checked by row alone | P1 184, P3 225, P4 130, P6 184 |
| M18 | struct: the left neighbour lost | P1 11, P3 20, P4 15, P6 11 |
| M20 | struct: the cost raised twice | P1 264, P2 172, P5 169, P6 264 |
| M21 | struct: obstacles flooded through | P1 264, P6 264 |
| M22 | iter: a cell never revisited | P1 269, P3 238, P4 238, P6 269 |
| M24 | iter: the obstacle of the cell left | P1 51, P3 62, P4 54, P5 8, P6 51 |
| M26 | iter: the cell's row by modulo | P1 268, P2 143, P3 132, P4 79, P6 268 |
| M27 | solution: the left move lost | P1 33, P3 50, P6 33 |
| M31 | solution: a cell relaxed when no cheaper | P1 359, P2 359, P6 359 |

P1 and P6 kill all seventeen, P3 twelve, P2 and P4 eight each, and P5
four. P3, the grid transposed, misses the five edits that treat rows
and columns alike: every step to the back, the corner's own cell
counted, the cost raised twice, obstacles flooded through, and a cell
relaxed when no cheaper. P4, the grid turned half round, misses the same
five and four edits that drop one kind of move: the naive arm's left
neighbour from column 2 and row above never looked at, the heap arm's
upward move lost and the template's left move lost. P2 misses
the nine edits whose wrong answers stay between 0 and the top row and
right column's obstacles. P5, the first obstacle cleared, kills only
edits that can make an answer rise when an obstacle goes, or fall by
two: the ★ arm's steps the other way round, the heap arm's largest
first, the struct arm's cost raised twice and the iter arm's obstacle
of the cell left.

Of the thirty-one, fourteen were not kept. The ★ arm's two moves only
(M3) fails as its every step to the back (M1); its step costing 1
always (M4), the template's bottom row out of reach (M29) and the
template's a cell relaxed when no cheaper (M31) fail alike, and the
last is kept; the naive arm's start not zero (M10), the struct arm's
level from 1 (M19) and the template's start one (M30) as the ★ arm's
corner's own cell counted (M6); the naive arm's right neighbour from
the left (M11) as the template's left move lost (M27); the heap arm's
cost of a step not added (M13) and the template's obstacle not counted
(M28) as the struct arm's obstacles flooded through (M21); and the heap
arm's cost of a step doubled (M16) as the struct arm's cost raised
twice (M20). The iter arm's column bound the row's and diagonal for the
left (M23, M25) fail in ways of their own, past the three kept for that
arm. The ★ arm's cell settled at its first cost (M5) passes all 12960
checks. The struct arm's right neighbour lost (M17) never ends under
either backend: the flood never reaches the last column, so the level
loop looks for the corner forever; it was stopped by hand.

Four edits as first drafted were replaced and run again: the naive
arm's one sweep only and the template's free step to the back, which
passed every check; and the naive arm's cell's own obstacle not added
and the struct arm's edge flooded too, which never ended. The naive
replacements are M7 and M9, the template's M27, and the struct arm's
M17, which also never ends.

## Verification

Every arm prints the same output as `obstacles.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★ arm takes 1.3 s, the struct arm 1.5 s,
the template 1.8 s and the naive arm 3 s. The heap arm, whose `Set` of
settled cells hashes a tuple for every neighbour looked at, takes 6.4
s, and the iterator arm, which builds a `Vec` of neighbours for every
cell it takes off and takes some cells off more than once, 8.7 s. The
differential takes 21 s there and 0.9 s under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 10 grids of 200 by 200 once, each cell an obstacle
with chance 4 in 10 and the corners empty, then makes 5 passes over all
of them summing the answers, with the ★ arm in all five languages.
Every implementation prints `5 passes over 10 grids of 200x200:
checksum 50578165`. C and Go keep the deque as a ring buffer of their
own; Kāra, Rust and Python use their library's `VecDeque` and `deque`.

BENCHTAB
