# 2304. Minimum Path Cost in a Grid

You are given a **0-indexed** `m x n` integer matrix `grid` consisting
of **distinct** integers from `0` to `m * n - 1`. You can move in this
matrix from a cell to any other cell in the **next** row. That is, if
you are in cell `(x, y)` such that `x < m - 1`, you can move to any of
the cells `(x + 1, 0)`, `(x + 1, 1)`, ..., `(x + 1, n - 1)`. **Note**
that it is not possible to move from cells in the last row.

Each possible move has a cost given by a **0-indexed** 2D array
`moveCost` of size `(m * n) x n`, where `moveCost[i][j]` is the cost of
moving from a cell with value `i` to a cell in column `j` of the next
row. The cost of moving from cells in the last row of `grid` can be
ignored.

The cost of a path in `grid` is the **sum** of all values of cells
visited plus the **sum** of costs of all the moves made. Return *the
**minimum** cost of a path that starts from any cell in the **first**
row and ends at any cell in the **last** row.*

```
grid = [[5,3],[4,0],[2,1]],
moveCost = [[9,8],[1,5],[10,12],[18,6],[2,4],[14,3]]        ->  17
grid = [[5,1,2],[4,0,3]],
moveCost = [[12,10,15],[20,23,8],[21,7,1],[8,1,13],[9,10,25],[5,3,2]]  ->  6
```

**Constraints:** `m == grid.length`; `n == grid[i].length`;
`2 <= m, n <= 50`; `grid` consists of distinct integers from `0` to
`m * n - 1`; `moveCost.length == m * n`; `moveCost[i].length == n`;
`1 <= moveCost[i][j] <= 100`.

A path's cost up to a cell depends only on the cell it came from, so
the least cost of reaching each cell of a row is the least, over the
cells of the row above, of their own least cost plus the move, plus
the cell's value. One row of these at a time is enough: O(m n^2), at
most 125000 steps. The largest cost is under `50 * 2500 + 49 * 100`.

## Approaches

| file | mechanism |
|---|---|
| `path.kara` ★ | row by row: `best[j]` the least cost of a path ending at column `j` of the row so far, and each column of the next row the least of `best[k]` plus the move from the value at column `k`, plus its own value, in a fresh `Vec.filled(n, i64.MAX)` |
| `path_memo.kara` | top down: `cost_from(r, c)` the least cost from a cell to the last row, its value plus the least move and `cost_from` the cell reached, each cell's answer kept in a `mut ref Vec[Vec[i64]]` memo, -1 until found |
| `path_dijkstra.kara` | Dijkstra over the cells: a `PriorityQueue` of (cost so far, row, column), the first row entered at its values, the first cell of the last row taken ending the cheapest path. O(m n^2 log(m n)) |
| `path_iter.kara` | `grid.windows(2)` `fold`ed from the first row's values, each pair of rows `map`ping every column of the lower one to its value plus the `min` over the upper row, `zip`ped with the costs so far, of the cost and the move |
| `path_push.kara` | pushed forward over the whole table: `dist[r][c]` the first row's values and `i64.MAX` below, and every cell, row by row, offering each cell of the next row its cost plus the move plus that cell's value, the least offer kept |
| `path_solution.kara` | LeetCode's Rust template: `Vec<Vec<i32>>` in, a `vec![i32::MAX; n]` row for each step, `as usize` to index the move costs by a cell's value, and `*dp.iter().min().unwrap()`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 6 lines: LeetCode's two examples; the
smallest grid with every move 1; a grid whose one cheap move, 1 among
costs of 100, is from the corner; a 50 by 50 grid, the largest; then
1000 random grids of 2 to 8 rows and columns, the numbers shuffled and
move costs from 1 to 100, with a checksum and the costs in all.
`path.py` mirrors the ★ arm and its output is byte-identical.

`karac fix` carries the template in one call, reporting 10 edits:
`struct Solution;` to `struct Solution {}`; the six brackets of the two
`Vec<Vec<i32>>`, to `Vec[Vec[i32]]`; `i32::MAX` to `i32.MAX`, and then
the `vec![i32.MAX; n]` it sits in to `Vec.filled(n, i32.MAX)`; and,
in the harness's wrapper, the `as i64` on the template's `i32` answer,
which widens on its own. The `as usize` and the `*` before
`dp.iter().min().unwrap()` stand as Kāra.

The iter arm was first written `grid.windows(2).fold(..)`, as in Rust.
In Kāra `windows` gives a `Vec` of the windows, and a `Vec` has no
`fold`: `karac check` says so, writes out
`grid.windows(2).into_iter().fold(...)`, and `karac fix` makes that one
edit. `check` also reports, from the same line, `tuple pattern used but
type is ?T5` at the closure `|(v, b)|` inside the `fold`: an error that
follows from the first, the closure's parameter left untyped when
`fold` is not found, and gone with the one edit.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every path, one column for each row, walked from the first
row to the last by recursion, its cost the values of its cells plus the
cost of each move, and the least kept. No table, no memo. It checks 300
random grids of 2 to 4 rows and columns; then 30 whose move costs are
all 1; then 30 of up to 6 rows and 5 columns, up to 15625 paths. All
360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the answer is at least each row's least value plus 1 for each move, and at most the cost of the path straight down the first column |
| P3 | the columns reversed, in the grid and in the move costs: the same answer |
| P4 | every move cost 1 more: the answer grows by the number of moves, `m - 1` |
| P5 | the move costs from the values in the last row redrawn: the same answer |
| P6 | each arm agrees with at least three of the other five |

P5's redrawn costs are those the statement says to ignore: no path
moves from the last row.

The differential prints `360 cases: checksum 42150724, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that
builds the same cases and takes the least over `itertools.product` of
the columns. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: the move priced to the column it comes from | P1 302, P6 302 |
| M4 | ★: the first column of the row above never taken from | P1 210, P2 64, P3 303, P6 210 |
| M5 | ★: the answer the first column's | P1 218, P3 355, P6 218 |
| M10 | memo: the path started only from the first column | P1 225, P3 356, P6 225 |
| M11 | memo: the most, not the least, of the moves | P1 360, P2 277, P6 360 |
| M12 | memo: one answer kept for every cell of a row | P1 325, P3 354, P6 325 |
| M14 | dijkstra: the move priced by the column, not the value | P1 307, P2 21, P3 309, P5 201, P6 307 |
| M15 | dijkstra: the next cell's value left out | P1 335, P2 38, P6 335 |
| M16 | dijkstra: a cell marked settled when pushed, and so skipped when taken | P1 360, P2 360, P4 360, P6 360 |
| M18 | iter: the move priced from the lower row's value | P1 327, P2 49, P5 354, P6 327 |
| M19 | iter: the most, not the least, of the moves | P1 360, P2 263, P6 360 |
| M22 | iter: the costs so far paired a column on | P1 317, P2 13, P3 214, P6 317 |
| M23 | push: the last column's offer taken even when dearer | P1 295, P2 122, P3 352, P6 295 |
| M24 | push: the first row started at 0 | P1 315, P2 22, P6 315 |
| M27 | push: the answer from the second row | P1 247, P2 49, P4 247, P6 247 |
| M28 | solution: the move priced from the cell below | P1 323, P2 21, P5 349, P6 323 |
| M31 | solution: the answer the largest | P1 358, P2 83, P6 358 |

P1 and P6 kill all seventeen, P2 thirteen, P3 seven, P5 three and P4
two. P3, the columns reversed, fails wherever an edit leans on a
column's place: a first or last column treated apart, a move priced by
a column number, or the costs so far paired a column on. P5 fails only where an edit prices a move from
a value it should not, which can be a last-row value: the move priced
by a column number, from the lower row's value, or from the cell
below. P4, every move 1 dearer, fails only where the answer has the
wrong number of moves: the Dijkstra arm answering -1, with none, and
the push arm answering from the second row, with one. P2 misses four
whose answers stay inside its bounds: the ★ arm's move priced to the
column it comes from and its answer the first column's, and the memo
arm's start from the first column only and one answer for a row.

Of the thirty-one, fourteen were not kept. One is equivalent and killed
by nothing: the memo never read (M7), which only repeats work. Two
crash: the memo arm pricing a move from the last row (M8) indexes past
the grid, and the push arm never offering to the last row (M26) leaves
`i64.MAX` there to overflow. The move priced from the cell below in
the ★ arm (M1) fails as the template's (M28); the cell's own value
left out in the ★ (M3), iter (M20) and template (M29) arms as the
Dijkstra arm's (M15); the move priced by the column in the memo arm
(M9) as the Dijkstra arm's (M14); the first row entered at nothing in
the Dijkstra arm (M13) and the fold begun at zeros in the iter arm
(M21) as the push arm's first row started at 0 (M24); the Dijkstra
arm's second row taken as the last (M17) as the push arm's answer from
the second row (M27); and the push arm's move priced to the column it
offers from (M25) as the ★ arm's (M2). The ★ arm's straight-down moves
only (M6) and the template's last column never taken from (M30) fail
apart from every kept one, and were left out to keep three to an arm.

## Verification

Every arm prints the same output as `path.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★, memo and push arms take 0.5 to 0.6 s,
the iter and template arms 1.1 to 1.2 s, and the Dijkstra arm, which
pushes every move into its queue, 2.1 s. The differential takes 1.3 s
there and 0.7 s under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 20 grids of 50 by 50, the numbers 0 to 2499 shuffled,
and 20 tables of move costs from 1 to 100 once, then makes 40 passes,
grid `a` in pass `p` priced by table `(a + p) % 20`, with the ★ arm in
all five languages. Every implementation prints `40 passes over 20
grids of 50 by 50: checksum 509264388`. Each keeps the grid and the
table as 64-bit integers: nested `Vec`s in Kāra and Rust, fixed arrays
in C, nested slices in Go and lists in Python.

BENCHTAB
