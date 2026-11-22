# 2852. Sum of Remoteness of All Cells

You are given a **0-indexed** matrix `grid` of order `n * n`. Each cell
in this matrix has a value `grid[i][j]`, which is either a **positive**
integer or `-1` representing a blocked cell.

You can move from a non-blocked cell to any non-blocked cell that
shares an edge with it.

For any cell `(i, j)`, we represent its **remoteness** as `R[i][j]`
which is defined as the following:

- If the cell `(i, j)` is a **non-blocked** cell, `R[i][j]` is the sum
  of the values `grid[x][y]` such that there is **no path** from the
  **non-blocked** cell `(x, y)` to the cell `(i, j)`.
- For blocked cells, `R[i][j] == 0`.

Return *the sum of* `R[i][j]` *over all cells.*

```
grid = [[-1,1,-1],[5,-1,4],[-1,3,-1]]  ->  39
grid = [[-1,3,4],[-1,-1,-1],[3,-1,-1]]  ->  13
grid = [[1]]                            ->  0
```

**Constraints:** `1 <= n <= 300`; `1 <= grid[i][j] <= 10^6` or
`grid[i][j] == -1`.

## Approaches

| file | mechanism |
|---|---|
| `remote.kara` ★ | a cell reaches exactly the cells of its own region, so its remoteness is the sum of every open cell less its region's; each region flooded once, breadth first from a `VecDeque[(i64, i64)]`, adds its size times what lies outside it |
| `remote_union.kara` | union-find in a struct with `find` (path halving) and `join` (by size) methods, every open cell joined to its open neighbours right and below; each root then holds its region's size and sum |
| `remote_dfs.kara` | each region flooded depth first by recursion, the visit returning its cells' count and sum as a pair; a 300 x 300 grid open throughout recurses 90000 deep |
| `remote_set.kara` | the open cells not yet in a region kept in a `SortedSet[(i64, i64)]`: `pop_first` starts a region, grown from a stack, each cell taken out with `remove` as it is reached |
| `remote_solution.kara` | a Rust solution as LeetCode's Rust users write it: `use std::collections::VecDeque`, a `vec![vec![false; n]; n]` of seen cells, a breadth-first flood over `usize` places with `as i32` neighbours checked against `n as i32`, and `i64` sums from `grid[r][c] as i64`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 4 lines: LeetCode's three examples; 300 x
300, LeetCode's most, open throughout with 10^6 in every cell, every
other cell blocked, and every cell blocked; then 3000 random grids of 1
to 6, values up to 9, a cell blocked one time in 3, and 20 of up to 300,
values up to 10^6, blocked from 1 time in 10 to 6 in 10, as checksums.
`remote.py` mirrors the ★ arm and its output is byte-identical.

```
39 13 0
0 2024955000000000 0
3000 small grids: checksum 215017168
20 large grids: checksum 878514344
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: from every open cell, the cells it reaches found by a
search of its own over a `Set[(i64, i64)]`, and the values of the open
cells it does not reach added to the total. It draws 2000 random grids
of 1 to 6, values up to 9, a cell blocked one time in 3, then 50 of up
to 120, values up to 10^6, blocked from 1 time in 10 to 6 in 10, all
before any arm answers; the literal reading is asked only of the first
2000.

| | property |
|---|---|
| P1 | up to 6 x 6, the answer is the literal reading's |
| P2 | the grid transposed: the same answer |
| P3 | the grid turned a quarter: the same answer |
| P4 | every value doubled: the answer doubled |
| P5 | a blocked row and column added: the same answer |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 716180585, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. M1 and M6 fail the same checks: a region one
cell too large and one cell too small change the same answers.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each region counted one cell larger | P1 800, P6 843 |
| M2 | ★: the bottom row never entered | P1 1534, P2 1526, P3 1526, P5 1581, P6 1581 |
| M3 | union: neighbours below never joined | P1 1565, P2 1537, P3 1537, P6 1613 |
| M4 | union: a region's own sum not taken off | P1 1885, P6 1935 |
| M5 | union: the size of the smaller root kept | P1 754, P6 797 |
| M6 | dfs: a region's first cell not counted | P1 800, P6 843 |
| M7 | dfs: the neighbours' sums dropped | P1 1608, P2 560, P3 1380, P6 1656 |
| M8 | set: a neighbour to the left never followed | P1 831, P2 1011, P3 1223, P6 878 |
| M9 | set: each region one cell | P1 1608, P6 1656 |
| M10 | solution: a blocked cell flooded | P1 1597, P4 1654, P5 1935, P6 1645 |

## Benchmarks

The bench draws 20 grids of 300 x 300, LeetCode's most, values up to
10^6, a cell blocked from 1 time in 10 to 6 in 10, all of them first,
then answers each 10 times by the ★ arm in all five languages. C's
queue is an array of n * n cells, which a region never outgrows, and
Go's a slice taken from the front, where Kāra, Rust and Python grow a
deque. Every implementation prints `20 grids of 300 x 300, 10 rounds:
checksum 167416074`.

BENCHTAB

## Verification

All five arms print the same output as `remote.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The union arm's `join`, as first written, took both roots with `let
(mut ra, mut rb) = ..`, and `karac check` reported E0001 twice, `mut`
going before the whole pattern in Kāra; `karac fix` wrote `let mut (ra,
rb)`. The other arms checked clean.

LeetCode's Rust template took 34 `karac fix` edits in one run, the
wrapper included: the `use std::collections::VecDeque` line deleted,
`VecDeque` being in Kāra's prelude; `struct Solution {}` added for the
`impl`; `Vec<..>` became `Vec[..]` and `vec![vec![false; n]; n]`
`Vec.filled(n, Vec.filled(n, false))`; `for row in &grid` became `for
row in ref grid`, and `&v`, `&(dr, dc)` and `|&x|` lost their `&`;
`||`, `&&` and `!` became `or`, `and` and `not`; `let (mut cnt, mut
sum) = (0i64, 0i64)` became `let mut (cnt, sum) = (0, 0)`;
`VecDeque::new()` and `Solution::` took `.`; `v as i64` and `grid[r][c]
as i64`, `i32` widenings, lost their casts. The `as usize` casts of
`let (nr, nc) = (nr as usize, nc as usize);` went too, `usize` being
`i64`, and left `let (nr, nc) = (nr, nc);`, a binding of itself. Since
kara 0d28296389 the `self_rebinding` lint names it and its fix deletes the
line, as in kata 2851 (B-2026-11-21-206). The `r as i32 + dr` and `n as
i32` narrowings were accepted as written.
