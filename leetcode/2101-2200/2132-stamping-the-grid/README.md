# 2132. Stamping the Grid

You are given an `m x n` binary matrix `grid` where each cell is either
`0` (empty) or `1` (occupied).

You are then given stamps of size `stampHeight x stampWidth`. We want to
fit the stamps such that they follow the given restrictions and
requirements:

1. Cover all the empty cells.
2. Do not cover any of the occupied cells.
3. We can put as many stamps as we want.
4. Stamps can overlap with each other.
5. Stamps are not allowed to be rotated.
6. Stamps must stay completely inside the grid.

Return `true` if it is possible to fit the stamps while following the
given restrictions and requirements. Otherwise, return `false`.

```
grid = [[1,0,0,0],[1,0,0,0],[1,0,0,0],[1,0,0,0],[1,0,0,0]], 4, 3  ->  true
grid = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]], 2, 2              ->  false
```

**Constraints:** `m == grid.length`; `n == grid[r].length`;
`1 <= m, n <= 10^5`; `1 <= m * n <= 2 * 10^5`; `grid[r][c]` is either
`0` or `1`; `1 <= stampHeight, stampWidth <= 10^5`.

Since stamps may overlap, nothing is lost by laying a stamp everywhere
one fits; the question is then whether every empty cell lies under at
least one. A prefix sum of the occupied cells says in O(1) whether a
stamp fits at a corner, and a prefix sum of the stamps laid down, as
marks in a difference table, says how many lie over a cell. O(mn).

## Approaches

| file | mechanism |
|---|---|
| `stamp.kara` ★ | flat `Vec[i64]` tables, one wider than the grid: the occupied cells' prefix sum, then each fitting stamp's four marks, summed in place over the grid while the empty cells are checked |
| `stamp_rows.kara` | the same tables as `Vec[Vec[i64]]` rows, a stamp's fit asked of a closure over the sums |
| `stamp_runs.kara` | no sums: each cell's run of empty cells to its right, the rows below with such a run of the stamp's width giving the corners; then a cell is covered when the latest corner in its row's reach, and the latest such row in its column's, are near enough |
| `stamp_struct.kara` | a `struct Sums` built from a grid and asked for a block's total (`ref self`), and a `struct Marks` stamped on and settled in place (`mut ref self`) |
| `stamp_window.kara` | each cell a corner, 1, when a stamp fits there; a second prefix sum over the corners counts those in the stamp's reach of each cell, cut off at the grid's edge; `map`/`collect` and `all` over ranges |
| `stamp_solution.kara` | LeetCode's Rust template: `vec![vec![0i32; n + 1]; m + 1]` tables, `h..=m` ranges and `usize` casts, carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples and four more
(every cell occupied under a stamp too big, one empty cell, one under a
stamp too tall, and a stamp that fits the grid exactly), each with its
answer; then the count stamped and a checksum over 2000 random grids of
1 to 6 by 1 to 6, a cell occupied one time in 2, 4 or 8 in turn, under a
stamp of 1 to 4 by 1 to 4; then the constraints' largest, 200000 cells:
400 by 500 empty under a stamp its size, 1 by 200000 with every 1000th
cell occupied under 1 by 999, and 400 by 500 with a cell in 200 occupied
under 2 by 2. `stamp.py` mirrors the ★ arm and its output is
byte-identical.

No compiler gap was met. `karac fix` carries the template in three
rounds of 14, 5 and 4 edits: Rust's spellings (`Vec<..>` to brackets,
`&&` to `and`, `struct Solution;` to `struct Solution {}`, the adapter's
`&Vec` to `ref Vec` and its `|&v|` to `|v|`, `Solution::` to `.`); then
the `as usize` of the stamp's sides to `as i64`, since they meet `i64`
ranges, and each inner `vec![0i32; n + 1]` to `Vec.filled`; then each
outer `vec![..; m + 1]`, whose fix overlaps the inner one's and so waits
a round, and the `ref` dropped from the adapter's parameter, which
borrows already.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for every empty cell, every placement of the stamp over it is
tried, kept only if wholly inside the grid, and each of its cells looked
at for an occupied one; no sum is kept. It checks 300 random grids of 1
to 6 by 1 to 6, a cell occupied one time in 2, 4 or 8 in turn, under a
stamp of 1 to 4 by 1 to 4; then 30 empty grids under a stamp of 1 to 7
by 1 to 7, which fits or not by its size alone; then 30 grids with one
occupied cell. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the grid transposed, the stamp's sides swapped: the same answer |
| P3 | the grid mirrored left to right: the same answer |
| P4 | the grid turned upside down: the same answer |
| P5 | a row of occupied cells added below: the same answer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 grids: checksum 69913169, 12960 checks over
6 arms: 0 failures` under every lane in Verification; the checksum of
the literal answers (51 of the 360 stamped) was checked against a Python
reading of the same grids by the same search. On a failure it prints the
first ten and then the count by property.

## Mutation testing

Twenty-nine edits to the differential, four to six to each arm, each run
under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are kept,
three to each Kāra arm and two to the Rust-template arm. Each kept one
is killed, fails the same way under both backends and not by a crash,
and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the last row of corners never tried | P1 43, P2 7, P4 6, P5 43, P6 43 |
| M3 | ★: the marks never taken off below | P1 18, P2 32, P4 29, P6 18 |
| M5 | ★: an occupied cell needing a stamp too | P1 35, P5 16, P6 35 |
| M6 | rows: the stamp one column short | P1 51, P2 72, P3 26, P5 15, P6 51 |
| M8 | rows: the stamps read one cell up | P1 48, P6 48 |
| M29 | rows: the fit missing the block's top right | P1 21, P2 14, P4 12, P6 21 |
| M10 | runs: a run of one less enough | P1 78, P2 76, P3 9, P5 15, P6 78 |
| M11 | runs: the rows below never reset | P1 19, P2 31, P4 29, P6 19 |
| M12 | runs: a stamp's reach one row longer | P1 10, P2 17, P4 15, P6 10 |
| M15 | struct: a block missing its corner | P1 12, P3 7, P4 6, P5 1, P6 12 |
| M16 | struct: settle never subtracting the overlap | P1 10, P3 11, P4 14, P6 10 |
| M17 | struct: the stamp's lower edge left unmarked | P1 21, P2 33, P3 4, P4 31, P6 21 |
| M19 | window: the corners kept off the last column | P1 46, P2 7, P3 2, P6 46 |
| M20 | window: the window one row short | P1 16, P2 20, P6 16 |
| M21 | window: the window one column too wide | P1 7, P2 17, P3 6, P6 7 |
| M24 | solution: the adapter's stamp sides swapped | P1 39, P6 39 |
| M25 | solution: a stamp fitting at any count | P1 148, P5 35, P6 148 |

P1 and P6 kill all seventeen, P2 eleven, P4 eight, P3 seven and P5 six.
The grid has four symmetries the answer keeps, and an edit that is off
by one at one edge or along one axis breaks them: P2's transpose sees
an edit that treats rows and columns unlike (M1, M3, M6, M10 to M12,
M17, M19 to M21, M29), P3's mirror one that treats the left and right
edges unlike (M6, M10, M15 to M17, M19, M21), and P4's turn one that
treats the top and bottom unlike (M1, M3, M11, M12, M15 to M17, M29).
Two fail P1 alone, since their wrong answer is the same on every turn of
the grid: M8 reads each row's stamps from the row above, so an empty
cell on the top row finds none and the answer is false wherever the
grid has one; and the adapter's swapped sides (M24) give the grid and
its transpose, with its sides swapped, the same wrong answer.
P5 adds a row of occupied
cells, which needs no stamp but blocks any that would reach it; it sees
the edits that let a stamp sit over an occupied cell (M5, M25), and
those whose wrong answer at the bottom edge the new row moves (M1, M6,
M10, M15).

Of the twenty-nine, twelve were not kept. One is equivalent: the
adapter handing the template its grid upside down, which P4 says gives
the same answer. One fails by a crash: the rows arm's mark one column
on, which indexes past the table's edge under both backends. Five fail
as a kept one does: the rows arm's mark one column short, its corner's
own mark dropped and the runs arm's reach one column short as M8; the
window arm's occupied cell needing a corner as M5; and the template's
last row of corners as M1. Five are killed with checks of their own but
were left out because their arms keep their share: the ★ arm's stamp
over one occupied cell (P1 75, P5 6, P6 75) and its marks summed along
rows only (P1 40, P2 17, P4 2, P6 40); the runs arm's run carried past
an occupied cell (P1 22, P2 34, P3 29, P6 22); the struct arm's stamp
laid where it fits a cell (P1 65, P3 60, P4 37, P5 61, P6 65); and the
template's adapter reading every cell empty (P1 150, P5 35, P6 150).

## Verification

Every arm prints the same output as `stamp.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.2 s to 3.6 s and the
differential 0.7 s.

## Benchmarks

The bench builds a grid of 400 by 500 once, rooms of 3 by 3 behind
walls on every row and column that leaves 3 over when divided by 4;
then solves it 100 times, one cell flipped and a stamp of 1 to 3 by 1 to
3 drawn before each solve and the cell flipped back after, with the ★
arm in all five languages. A flipped wall leaves an empty cell only a 1
by 1 stamp covers, and a flipped room cell leaves a room some stamps
cannot cover, so 28 of the 100 are stamped. Every implementation prints
`100 solves: 28 stamped, checksum 907241154`.

BENCHTAB
