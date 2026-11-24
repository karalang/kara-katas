# 1293. Shortest Path in a Grid with Obstacles Elimination

You are given an `m x n` integer matrix `grid` where each cell is either
`0` (empty) or `1` (obstacle). You can move up, down, left, or right from
and to an empty cell in one step.

Return the minimum number of steps to walk from the upper left corner
`(0, 0)` to the lower right corner `(m - 1, n - 1)` given that you can
eliminate at most `k` obstacles. If it is not possible to find such a
walk return `-1`.

```
grid = [[0,0,0],[1,1,0],[0,0,0],[0,1,1],[0,0,0]], k = 1  ->  6
grid = [[0,1,1],[1,1,1],[1,0,0]], k = 1                  ->  -1
```

**Constraints:** `1 <= m, n <= 40`, `1 <= k <= m * n`, each cell is `0`
or `1`, and `grid[0][0] == grid[m - 1][n - 1] == 0`.

The arms are `fn shortest_path(grid: Vec[Vec[i64]], k: i64) -> i64`.

## Approaches

| file | mechanism |
|---|---|
| `shortest_path.kara` ★ | a breadth-first search level by level over (row, column, eliminations left) in a `VecDeque`, each cell remembering the most eliminations any state has reached it with; a later state with no more is no better and is dropped. When k covers the worst straight path, `m + n - 2` steps at once. O(mnk) |
| `shortest_path_visited.kara` | a breadth-first search with the steps in each state, every one of the `m n (k + 1)` states visited once, kept in a three-dimensional table of `bool`. O(mnk) |
| `shortest_path_astar.kara` | A*: states taken from a `PriorityQueue` of `(steps + distance to go, steps, row, column, left)`, smallest first, with a `Set` of the states done; the straight-line distance never overstates what is left, so the corner's first pop has the fewest steps. O(mnk log mnk) |
| `shortest_path_layers.kara` | one layer per number of eliminations used, from 0 up: layer e starts every obstacle next to a cell layer e - 1 reached one step further on, then spreads through the empty cells with a `PriorityQueue`, so each layer holds the fewest steps with at most e obstacles crossed. O(mnk log mn) |
| `shortest_path_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `VecDeque<(usize, usize, usize, i32)>` of states, a `vec![vec![vec![false; k + 1]; n]; m]` visited table, moves through `as i32` and back), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's two examples, a single
cell, and a wall of three obstacles with three eliminations and with two
(`6 -1 0 4 -1`); then 402 random grids, 400 up to 15 by 15 with obstacles
from 10 to 70 in 100 and k up to 6, and two of 40 by 40, the
constraints' largest (`402 random grids: 117 unreachable, steps total
3847, checksum 24788304`). `shortest_path.py` mirrors the ★ arm, and its
output is byte-identical. Every arm gives the same output under `karac
__mir-run`, `karac run` and `karac __mir-llvm-run`.

The Mend loop: the four Kāra arms checked clean as first written. The
A* and layers arms were first written for a largest-first queue, as
Rust's `BinaryHeap` is, with every priority negated; Kāra's
`PriorityQueue.new()` gives the smallest first (`docs/library/collections.md`),
so the A* arm answered 14 for LeetCode's first example, and the oracle
caught it. The layers arm still answered right, its relaxation correcting
any order, only more slowly. Both now push the plain priorities. The
Rust arm takes one round of 32 fixes by `karac fix`'s count, from 16
errors: the `use std::collections::VecDeque;` line deleted, since
`VecDeque` is in Kāra's prelude, `Vec<..>` to `Vec[..]`, `vec![..; ..]`
to `Vec.filled`, `struct Solution;` to `struct Solution {}`, `::` to
`.`, `&&`, `||` and `!` to `and`, `or` and `not`, the `&(dr, dc)` pattern
to `(dr, dc)`, `k as usize` to `k as i64`, the suffixes of `0usize`
dropped, the `let (nr, nc) = (nr as usize, nc as usize);` line deleted, the wrapper's `|&x|` to `|x|` and its
`as i64` dropped as a widening. Its output matches on the first run. No
gap was met.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every walk from the upper left corner that never comes back to
a cell, with the obstacles it steps on counted, and the fewest steps of
any that reaches the lower right corner on at most k of them. A shortest
walk never comes back to a cell, so these are enough. 2000 grids in four
kinds, 500 each: up to 4 by 4 with obstacles from 20 to 80 in 100; a
single row or column of up to 12 cells; a snake of 5 or 7 rows whose
every other row is a wall with one gap, at the right and the left in
turn, so that the shortest way with few eliminations doubles back, and
transposed half the time, so that it climbs; and up to 4 by 4 again. k is
up to 4, and up to 2 for a snake. Every grid, k and cell to clear is
drawn before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the grid transposed: the same answer |
| P3 | the grid turned half round, the corners swapped: the same answer |
| P4 | one more elimination: reachable whenever it was, in no more steps |
| P5 | one cell cleared: reachable whenever it was, in no more steps |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 grids: checksum 384894777,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run` and
`karac __mir-llvm-run`. Python gives the same checksum.

## Mutation testing

Ten edits to the differential, two to each arm, each run under both
`karac __mir-llvm-run` and `karac __mir-run`. Every one is killed, fails
the same way under both backends and not by a crash, and no two fail the
same checks, so all ten are kept.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the straight path taken from two eliminations short | P1 46, P6 184 |
| M2 | ★: obstacles not counted | P1 574, P6 2296 |
| M3 | visited: a step counted twice | P1 1364, P6 1364 |
| M4 | visited: no step up | P1 23, P2 45, P6 23 |
| M5 | A*: the distance to go counted twice | P3 1 |
| M6 | A*: any cell of the last row taken for the corner | P1 1161, P2 1594, P3 211, P6 1161 |
| M7 | layers: one layer short | P1 495, P6 495 |
| M8 | layers: the extra elimination spent on free cells | P1 776, P6 776 |
| M9 | solution: an obstacle crossed without spending | P1 221, P6 221 |
| M10 | solution: the last row or column taken for the corner | P1 1759, P3 154, P6 1759 |

P1 and P6 kill nine each, P3 three and P2 two; P4 and P5 kill none. The
first draft of the differential had no snakes, and M4 and M5 survived
it: on grids up to 4 by 4 a shortest walk almost never needs to go up or
back, and an A* that counts the distance to go twice is still exact
there. With the snakes in, M4 fails on the transposed ones that climb (P2),
and M5 fails once, on one turned grid (P3): an A* whose estimate
overstates is not exact, but on grids this small it almost always lands
on the shortest walk anyway.
The sufficient-k shortcut is exact at `m + n - 3`, since the straight
path's ends are never obstacles; M1 takes it two short of `m + n - 2`.

## Benchmarks

The bench builds 50 grids of 40 by 40, the constraints' largest, with
obstacles 30 in 100, once from its own generator, then makes 80 passes;
each flips one cell of every grid other than the corners and chooses k
from the checksum so far, up to 77, so no answer carries over, answers it
with the ★ arm and folds the steps plus the pass into the checksum. The
queue is the language's own: `VecDeque` in Kāra and Rust, `collections.deque`
in Python, a slice per level in Go, and in C a ring buffer grown by
doubling; `best` is a fresh table per call in all five. Every
implementation prints `80 passes over 50 grids of 40 by 40: checksum
185930614`.

BENCHTAB
