# 1463. Cherry Pickup II

You are given a `rows x cols` matrix `grid` representing a field of
cherries where `grid[i][j]` represents the number of cherries that you
can collect from the `(i, j)` cell. You have two robots that can collect
cherries for you: Robot #1 is located at the top-left corner `(0, 0)`,
and Robot #2 is located at the top-right corner `(0, cols - 1)`. Return
the maximum number of cherries collection using both robots by following
the rules below: from a cell `(i, j)`, robots can move to cell `(i + 1,
j - 1)`, `(i + 1, j)`, or `(i + 1, j + 1)`; when any robot passes
through a cell, it picks up all cherries, and the cell becomes an empty
cell; when both robots stay in the same cell, only one takes the
cherries; both robots cannot move outside of the grid at any moment; and
both robots should reach the bottom row in `grid`.

```
grid = [[3,1,1],[2,5,1],[1,5,5],[2,1,1]]                                    ->  24
grid = [[1,0,0,0,0,0,1],[2,0,0,0,0,3,0],[2,0,9,0,0,0,0],[0,3,0,5,4,0,0],[1,0,2,3,0,0,6]]  ->  28
```

**Constraints:** `rows == grid.length`, `cols == grid[i].length`, `2 <=
rows, cols <= 70`, and `0 <= grid[i][j] <= 100`.

The arms are `fn cherry_pickup(grid: Vec[Vec[i32]]) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `cherry_pickup.kara` ★ | the most cherries down to each row for each pair of robot columns, `-1` where the pair cannot be, the nine moves by `for da in -1..=1` and a tuple `let (x, y)`, a shared cell taken once, and the answer the largest over the last row through `iter().map(..).max()`. O(rows * cols^2) |
| `cherry_pickup_memo.kara` | the most cherries from each row down by recursion from the two corners, `i32.MIN` off the grid, each answer kept in a `Map[(i64, i64, i64), i32]` keyed by the tuple of row and columns, read back through `if let Some(known) = memo.get(..)`. O(rows * cols^2) |
| `cherry_pickup_table.kara` | a full three-dimensional `Vec[Vec[Vec[i32]]]` filled from the bottom row up, every pair of columns filled since any can be reached from below, each cell's moves as ranges clamped by `max` and `min`; the answer the top row's corner pair. O(rows * cols^2) |
| `cherry_pickup_ordered.kara` | only pairs with robot 1 at or left of robot 2, since a pair of paths that crosses picks what the pair swapped where they meet does, in one flat `Vec[i32]` of `cols * cols`, each robot's moves as an array literal `[a - 1, a, a + 1]`. O(rows * cols^2 / 2) |
| `cherry_pickup_solution.kara` | a Rust solution as LeetCode's Rust users write it (a three-dimensional `vec![vec![vec![-1; n]; n]; m]` filled row by row with `i32` columns cast to `usize`, the nine moves as `for d1 in -1..=1`, and the answer folded from the last row through `iter().flatten().max()`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's two examples and four
more, 2 by 2, 3 by 2 of 5s, and 70 by 70 of 100s and of 0s (`24 28 10 30
14000 0`); the constraints' most, 70 by 70 with 0 to 100 cherries a cell
(`70 by 70: 10972`); and 1000 random grids of 2 to 12 rows and columns,
0 to top cherries a cell, top from 0 to 100 (`1000 random grids: 470447
cherries, checksum 941446539`). `cherry_pickup.py` mirrors the ★ arm,
and its output is byte-identical. Every arm gives the same output under
`karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`.

The Mend loop: the memo and ordered arms check clean as first written.
The ★ arm filled each new row with `Vec.filled(cols, Vec.filled(cols,
-1))` and read it through `max`, a method, which does not fix the
literal's type, so `best = next` is refused with the elements of `next`
`i64`; `karac fix` writes `-1i32`, 1 fix. The table arm's `let mut below
= 0;`, read through `max` and added to an `i32`, is declared `below:
i32` the same way, 1 fix. The Rust solution takes one round of 11 fixes
by `karac fix`'s count: `struct Solution;` to `struct Solution {}`,
`Vec<..>` to `Vec[..]`, the three-deep `vec!` to `Vec.filled`, `||` to
`or`, and `.flatten()` to `.flat_map(\|v\| v.iter())`. Every arm's
output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every path of robot 1 down from its corner against every path
of robot 2, each cell's cherries taken once when both pass through it,
while there are at most 5 rows. LeetCode's examples, three edge cases (2
by 2, 3 by 2 of 5s, and one cell of cherries in the middle of the last
row), 70 by 70 of 100s, of 0s and the constraints' most, and 1995 random
grids, half of 2 to 5 rows and half of 2 to 12.

| | property |
|---|---|
| P1 | the statement read literally, while there are at most 5 rows |
| P2 | the grid mirrored left to right gives the same |
| P3 | every cell doubled gives double |
| P4 | a row of 0s more at the bottom gives the same |
| P5 | at least the two edge columns straight down, at most each row's two largest |
| P6 | the ★ arm's answer |

All 56,865 checks pass on every arm: `2003 cases: checksum 113736298,
56865 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, top-down through
`lru_cache`, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: a cell both robots stand on counted twice | P1 290, P5 351, P6 2576 |
| M2 | ★: robot 2's first cell not picked | P1 1290, P2 1902, P5 540, P6 7616 |
| M3 | memo: robot 1 never steps left | P1 321, P2 1034, P6 800 |
| M4 | memo: one cherry too many on the last row | P1 1358, P3 2003, P5 281, P6 2003 |
| M5 | table: robot 1 never comes from the left | P1 321, P2 1034, P6 800 |
| M6 | table: robot 2 started a column in | P1 1295, P2 1925, P5 277, P6 1906 |
| M7 | ordered: robot 2 never steps left | P1 914, P2 1651, P6 1488 |
| M8 | ordered: only the end with the robots back at the two edges taken | P1 984, P4 1363, P6 1512 |
| M9 | solution: a reached cell with 0 cherries so far taken as unreached | P1 21, P3 28, P5 28, P6 28 |
| M10 | solution: robot 2 moved as robot 1 moves | P1 1112, P6 1694 |

## Benchmarks

The bench draws 40 grids of 70 by 70, the constraints' most, with 0 to
100 cherries a cell, once; each is answered with the ★ arm after one
cell is set from the checksum so far, so no answer carries over, and the
answer is folded into the checksum. Each implementation keeps two rows
of 70 by 70 pair totals, a fresh one for every grid row: a `Vec` of
`Vec`s in Kāra, Rust and Go, static arrays copied with `memcpy` in C,
and lists in Python. Every implementation prints `40 grids of 70 by 70:
checksum 210564359`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.14 s against Rust's 0.12 s (0.13 s with overflow checks
on), C's 0.09 s and Go's 0.21 s; Python takes 10.1 s.
