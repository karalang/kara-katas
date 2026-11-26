# 1765. Map of Highest Peak

You are given an integer matrix `isWater` of size `m x n` that
represents a map of land and water cells. If `isWater[i][j] == 0`, cell
`(i, j)` is a land cell. If `isWater[i][j] == 1`, cell `(i, j)` is a
water cell. You must assign each cell a height in a way that follows
these rules: the height of each cell must be non-negative; if the cell
is a water cell, its height must be `0`; any two adjacent cells must
have an absolute height difference of at most `1`. A cell is adjacent to
another cell if the former is directly north, east, south, or west of
the latter. Find an assignment of heights such that the maximum height
in the matrix is maximized. Return an integer matrix `height` of size `m
x n` where `height[i][j]` is cell `(i, j)`'s height. If there are
multiple solutions, return any of them.

```
isWater = [[0,1],[0,0]]              ->  [[1,0],[2,1]]
isWater = [[0,0,1],[1,0,0],[0,0,0]]  ->  [[1,1,0],[0,1,1],[1,2,2]]
```

**Constraints:** `1 <= m, n <= 1000`, `isWater[i][j]` is `0` or `1`, and
there is at least one water cell.

The arms are `fn highest_peak(is_water: Vec[Vec[i32]]) ->
Vec[Vec[i32]]`. Every arm returns the same answer of the many the
statement allows: each cell at its distance to the nearest water, which
is the highest each cell can be at once.

## Approaches

| file | mechanism |
|---|---|
| `highest_peak.kara` ★ | a breadth-first search from every water cell at once, with a `VecDeque`: each land cell's height is set when the search first reaches it, one above the cell it came from. O(m n) |
| `highest_peak_passes.kara` | two passes of the Manhattan distance transform: from the top left, each cell at most one above its upper and left neighbours, then from the bottom right, at most one above its lower and right ones. O(m n) |
| `highest_peak_layers.kara` | the search a layer at a time: the cells at one height in a `Vec`, the next layer built from their unreached neighbours, with no queue. O(m n) |
| `highest_peak_heap.kara` | Dijkstra's algorithm with a `PriorityQueue` of `(height, row, column)`, smallest first, every step of weight 1. O(m n log(m n)) |
| `highest_peak_solution.kara` | a Rust solution as LeetCode's Rust users write it (`vec![vec![-1; n]; m]`, `usize` cells, `i32` offsets checked before the cast back), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the heights the statement asks for, five more properties |

Every arm prints the same 4 lines: LeetCode's two examples (`[[1, 0],
[2, 1]] [[1, 1, 0], [0, 1, 1], [1, 2, 2]]`); five edges, one cell of
water, one row with water at one end, one column, every cell water, and
water at two opposite corners; the constraints' most, 1000 by 1000 with
water in one corner alone, so that the highest peak is 1998, and with
one cell in a hundred water, each as its highest height and a digest
(`the most: 1998 449866588, 29 19889764`); and 3000 random grids of 1 to
8 by 1 to 8 (`3000 random grids: checksum 876376819`). `highest_peak.py`
mirrors the ★ arm, and its output is byte-identical. Every arm gives the
same output under `karac __mir-run`, `karac run`, `karac build` and
`karac __mir-llvm-run`.

The Mend loop: the ★, passes and heap arms check clean as first written.
The layers arm was first written with `let (r, c) = (*r, *c);` at the
top of `for (r, c) in layer.iter()`, as Rust needs, and check refused
the two `*`: the tuple pattern over a borrowed `(i64, i64)` already
binds the two numbers by value. `karac fix` took it in 3 fixes, the two
`*` dropped and then the line itself, which had become `let (r, c) = (r,
c);`. The Rust solution takes one round of 24 fixes by `karac fix`'s
count, and its diff is: the `use std::collections::VecDeque;` line
deleted, since `VecDeque` is in the prelude, `struct Solution;` to
`struct Solution {}`, `Vec<Vec<i32>>` to `Vec[Vec[i32]]` in both
signatures, `vec![vec![-1; n]; m]` to `Vec.filled(m, Vec.filled(n,
-1))`, `VecDeque::new()` to `VecDeque.new()`, `for &(dx, dy)` to `for
(dx, dy)`, `&&` to `and` three times, `(x as usize, y as usize)` to `(x
as i64, y as i64)` and `Solution::` to `Solution.`. Every arm's output
matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the heights the
statement asks for, measured from every water cell in turn: each cell
the least Manhattan distance to any water cell. LeetCode's examples, the
edges, and 1990 random grids of 1 to 7 by 1 to 7, each with its own
chance of water. Each arm meets six properties on each case:

| property | what it checks |
|---|---|
| P1 | the heights the statement asks for |
| P2 | the statement's rules: the grid's shape, water at 0, no height below 0, and neighbours at most 1 apart |
| P3 | the grid transposed gives the heights transposed |
| P4 | the grid mirrored left to right gives the heights mirrored |
| P5 | a row of water added below leaves each cell at the lower of its height and its distance to that row |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 cases: checksum 191128602,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, measuring from
every water cell, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: each new cell put at the front of the queue | P1 1343, P2 1343, P3 1111, P4 747, P5 1591, P6 5372 |
| M2 | ★: the step down made a step down and right | P1 1199, P2 1122, P3 1529, P4 1032, P5 147, P6 4796 |
| M3 | passes: the second pass's columns walked left to right | P1 402, P2 402, P3 685, P4 676, P6 402 |
| M4 | passes: land started at the larger side, less than the farthest a cell can be | P1 80, P6 80 |
| M5 | layers: no step down into the last row | P1 865, P2 865, P3 1364, P5 594, P6 865 |
| M6 | layers: each step left one too high | P1 1308, P2 1308, P3 1562, P4 1623, P5 810, P6 1308 |
| M7 | heap: a cell skipped when its height is already final | P1 1934, P2 1934, P5 1934, P6 1934 |
| M8 | heap: each cell queued at its parent's height | P1 1504, P6 1504 |
| M9 | solution: the step up made a step up and right | P1 1200, P2 1127, P3 1557, P4 1017, P5 804, P6 1200 |
| M10 | solution: no step into the last column | P1 1800, P2 1800, P3 1870, P4 1657, P6 1800 |

## Benchmarks

The bench builds one 800 by 800 grid once, one cell in 5000 water, and
makes 100 calls of the ★ arm, each first flipping one cell chosen from
the checksum so far. Each implementation's queue is its own language's:
Rust's `VecDeque`, a C array as large as the grid, and a Go slice read
from its head. Every implementation prints `100 calls on 800 by 800:
checksum 620701108`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra is ahead of Rust here at 0.62 s against Rust's 0.65 s (0.71 s with
overflow checks on), C's 0.46 s and Go's 4.3 s; Python takes 53.1 s.
