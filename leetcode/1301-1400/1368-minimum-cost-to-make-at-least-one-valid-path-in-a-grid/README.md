# 1368. Minimum Cost to Make at Least One Valid Path in a Grid

Given an `m x n` grid. Each cell of the grid has a sign pointing to the
next cell you should visit if you are currently in this cell. The sign
of `grid[i][j]` can be:

- `1` which means go to the cell to the right (`grid[i][j + 1]`)
- `2` which means go to the cell to the left (`grid[i][j - 1]`)
- `3` which means go to the lower cell (`grid[i + 1][j]`)
- `4` which means go to the upper cell (`grid[i - 1][j]`)

Notice that there could be some signs on the cells of the grid that
point outside the grid.

You will initially start at the upper left cell `(0, 0)`. A valid path
in the grid is a path that starts from the upper left cell `(0, 0)` and
ends at the bottom-right cell `(m - 1, n - 1)` following the signs on
the grid. The valid path does not have to be the shortest.

You can modify the sign on a cell with `cost = 1`. You can modify the
sign on a cell one time only.

Return the minimum cost to make the grid have at least one valid path.

```
grid = [[1,1,1,1],[2,2,2,2],[1,1,1,1],[2,2,2,2]]  ->  3
grid = [[1,1,3],[3,2,2],[1,1,4]]                  ->  0
grid = [[1,2],[4,3]]                              ->  1
```

**Constraints:** `1 <= m, n <= 100`, `1 <= grid[i][j] <= 4`.

Each arm is `fn min_cost(grid: Vec[Vec[i32]]) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `min_cost.kara` ★ | a 0-1 breadth-first search over the cells: a step the cell's sign points to costs 0 and goes to the front of a `VecDeque`, any other costs 1 and goes to its back, so cells leave the deque in cost order. O(m n) |
| `min_cost_dijkstra.kara` | Dijkstra's search with a `PriorityQueue` of (cost, row, column), min-first, stale entries skipped, stopping when the bottom right comes off. O(m n log(m n)) |
| `min_cost_layers.kara` | the cells reached at cost k are everything the signs lead to, for free, from the cells first reached at cost k; a walk follows the signs, and the unreached cells next to a layer start the layer of cost k + 1. O(m n) |
| `min_cost_sweeps.kara` | Bellman-Ford over the grid: passes over every cell, alternately from the top left and from the bottom right, each cell lowering its neighbours' costs, until a pass lowers nothing. O(m n) a pass |
| `min_cost_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `VecDeque` of `(usize, usize)`, `for (k, &(di, dj)) in dirs.iter().enumerate()`, `i as i32 + di` bounds checks, a `vec![vec![i32::MAX; n]; m]`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's three examples, one cell,
a 100 by 100 grid of 2s, every sign pointing left, and a 100 by 100
grid at random (`3 0 1 0 198 58`); and 2000 random grids of 1 to 30 by
1 to 30 folded into a checksum (`2000 random grids: costs total 23329,
checksum 994287856`). `min_cost.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac
__mir-run`, `karac run` and `karac __mir-llvm-run`.

The Mend loop: the dijkstra arm checks clean. The ★ arm's `let step =
if .. { 0 } else { 1 }`, added to an `i32` cost, is refused (E0200), and
`karac fix` writes `let step: i32` (1 fix). The layers arm's `let (mut
r, mut c) = (r, c)` is Rust's spelling, and the fix writes `let mut (r,
c)` (1 line, 3 fixes by `karac fix`'s count). The sweeps arm's `as i64`
on `grid.len()`, already an `i64`, draws two warnings, and the fix drops
both casts. The Rust solution takes 18 fixes: the `use` line deleted,
`struct Solution;` to `struct Solution {}`, `Vec<Vec<i32>>` to
`Vec[Vec[i32]]`, `vec![vec![i32::MAX; n]; m]` to `Vec.filled(m,
Vec.filled(n, i32.MAX))`, `VecDeque::new()` to `VecDeque.new()`, the
`&(di, dj)` pattern to `(di, dj)`, `||` to `or`, and the same `let w:
i32` as the ★ arm; `0usize`, `i as i32 + di` and `ni as usize` stand as
Rust wrote them. Every arm matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every way through the grid that visits no cell twice,
each costing the cells on it whose sign must change, and the cheapest
of them. A cell is never worth changing twice, so the simple paths are
all that need trying, and there are few enough on a grid of up to 16
cells. It checks the examples and one cell, 1500 random grids of 1 to 4
by 1 to 4, which the literal reading checks, and 500 of 1 to 12 by 1 to
12, which the other properties check; each case also has one cell
given a random sign, for P4.

| | property |
|---|---|
| P1 | the statement read literally, on grids of up to 16 cells |
| P2 | the grid transposed, right and down signs swapped and left and up, the same cost |
| P3 | the cost is 0 exactly when following the signs from the top left reaches the bottom right |
| P4 | one cell's sign changed moves the cost by at most 1 |
| P5 | the cost is no more than going all the way right then down, or down then right |
| P6 | the ★ arm's cost |

All 58,220 checks pass on every arm: `2004 cases: checksum 620238389,
58220 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run` and `karac __mir-llvm-run`; the checksum folds the literal cost on
the small grids and the ★ arm's on the larger. Python, with its own
Dijkstra on every grid, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash, and no two
fail the same checks. A first M10, every step stored at cost 1, failed
exactly as M5 did, since both turn the search into counting steps, and
was replaced.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a cell's cost set only when first reached | P1 171, P2 536, P3 1, P4 20, P5 80, P6 1448 |
| M2 | ★: the signs read one direction off | P1 1005, P2 1173, P3 114, P5 823, P6 5480 |
| M3 | dijkstra: the right and left signs swapped | P1 799, P2 1345, P3 128, P5 292, P6 1091 |
| M4 | dijkstra: a change costed 2 | P1 1435, P4 425, P5 1639, P6 1815 |
| M5 | layers: a sign followed one cell only | P1 1131, P3 83, P5 1468, P6 1511 |
| M6 | layers: the next layer only right and down | P6 4 |
| M7 | sweeps: stopped after two passes | P1 7, P3 1, P6 60 |
| M8 | sweeps: an up sign read as down | P1 598, P2 1165, P3 117, P6 921 |
| M9 | solution: the down and up moves swapped | P1 758, P2 1345, P3 119, P5 287, P6 1056 |
| M10 | solution: the sign read at the cell stepped to | P1 773, P3 138, P5 293, P6 1043 |

P6 kills all ten, P1 nine, P3 eight, P5 seven, P2 five and P4 two. The
one P1 misses, the layers arm growing a layer only right and down (M6),
is caught only by the ★ arm on four of the larger grids: on a grid of up
to 16 cells a path that must turn back left or up for less is rare, and
the edit only overcharges, never past a staircase, which goes only right
and down (P5). Transposing the grid (P2) catches the edits that treat
the two axes differently: signs read one off (M2), right and left
swapped (M3), up read as down (M8), down and up swapped (M9), and a cost
fixed at first reach (M1), which depends on the order the moves are
tried. The 0 test (P3) catches every edit that misreads where a sign
points or charges a step the signs make, but not a change costed 2 (M4)
or the layers' right-and-down growth (M6), which leave free paths free.
One changed cell (P4) moves a correct cost by at most 1, which only a
change costed 2 (M4) and a cost fixed at first reach (M1) break. The
staircase bound (P5) catches the edits that overcharge or misread signs
along it, but not the sweeps stopped early (M7), whose first pass
already settles every staircase, or an up sign read as down (M8), which
makes some down steps free and so only undercharges.

## Benchmarks

The bench builds 20 grids of 100 by 100 signs, the constraints' most,
once; then makes 600 rounds, each changing one cell's sign and finding
the cheapest valid path through that grid with the ★ arm, both drawn
from the checksum so far. Every implementation prints `600 rounds over
20 grids of 100 by 100: checksum 370127390`. The work is a 0-1
breadth-first search over 10^4 cells, the same in every language; the C
and Go deques are ring buffers of cell indices, Rust's and Kāra's a
`VecDeque` of (row, column) pairs.

BENCHTAB
