# 2711. Difference of Number of Distinct Values on Diagonals

Given a 2D `grid` of size `m x n`, you should find the matrix `answer`
of size `m x n`.

The cell `answer[r][c]` is calculated by looking at the diagonal values
of the cell `grid[r][c]`:

- Let `leftAbove[r][c]` be the number of **distinct** values on the
  diagonal to the left and above the cell `grid[r][c]` not including
  the cell `grid[r][c]` itself.
- Let `rightBelow[r][c]` be the number of **distinct** values on the
  diagonal to the right and below the cell `grid[r][c]`, not including
  the cell `grid[r][c]` itself.
- Then `answer[r][c] = |leftAbove[r][c] - rightBelow[r][c]|`.

Return the matrix `answer`.

```
grid = [[1,2,3],[3,1,5],[3,2,1]]  ->  [[1,1,0],[1,0,1],[0,1,1]]
grid = [[1]]                      ->  [[0]]
```

**Constraints:** `1 <= m, n, grid[i][j] <= 50`.

## Approaches

| file | mechanism |
|---|---|
| `diagonals.kara` ★ | each diagonal, from its start on the top row or the left column, swept down once, each cell given the number of distinct values seen above it, and then up once, each cell's count replaced by its distance from the number of distinct values below it. A table of the 50 values says which were seen. O(m n) |
| `diagonals_walk.kara` | for each cell, the diagonal walked up-left from it and down-right from it, each walk's values gathered into a `Set[i64]`, and the two sets' sizes compared. O(m n min(m, n)) |
| `diagonals_bits.kara` | the values are at most 50, so a set of them fits in a `u64` mask. One pass from the top-left builds, for every cell, the mask of the values above it from the cell up-left of it; one pass from the bottom-right does the same below; a cell's answer is the two masks' `count_ones` apart. O(m n) |
| `diagonals_solution.kara` | a Rust solution as LeetCode's Rust users write it, `usize` indices, a `HashSet<i32>` built per cell from `while` walks guarded by `i > 0 && j > 0`, and `abs_diff`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; a row and a
column; a 4 by 4 checkerboard of two values; for 50 by 50, LeetCode's
largest, with every diagonal distinct, the corner's and the centre's
answers and the sum; then the differences summed and a checksum for 1000
random grids of 1 to 50 rows and columns, values up to a random cap of
1 to 50. `diagonals.py` mirrors the ★ arm and its output is
byte-identical.

```
[[1, 1, 0], [1, 0, 1], [0, 1, 1]]
[[0]]
[[0, 0, 0, 0, 0]]
[[0], [0], [0]]
[[1, 1, 1, 0], [1, 0, 0, 1], [1, 0, 0, 1], [0, 1, 1, 1]]
50 by 50, all distinct along diagonals: corner 49, centre 1, sum 41650
1000 grids: differences sum to 3668597, checksum 301442456
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: for each cell, every cell of the grid asked whether it lies
on the same diagonal, r - c the same, and whether above or below, the
distinct values of each side kept in a list free of repeats. It checks
600 random grids of up to 8 by 8 with values up to a cap of 1 to 6, then
40 of up to 50 by 50 with values up to 50. Every case is drawn before
any arm answers.

| | property |
|---|---|
| P1 | up to 8 by 8, the answer is the literal reading's |
| P2 | the grid transposed: the answer transposed |
| P3 | the grid turned half round: the answer turned half round |
| P4 | every value v made 51 - v: the same answer |
| P5 | every cell's answer is between 0 and the longer of its two diagonal halves |
| P6 | each arm agrees with at least two of the other three |

The differential prints `640 cases: checksum 59356216, 15360 checks over
4 arms: 0 failures` under every lane in Verification, and a Python
reading of the same 600 small cases, cell against cell, gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. P4 kills none of them: no edit here
looks at a value other than to tell it from another. M2, M3 and M10 fail
the same cases, as do M1 and M4: each pair miscounts the same cells by
the same amount.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the count above written after the cell's own value | P1 600, P3 503, P5 640, P6 640 |
| M2 | ★: the table of seen values kept from the sweep down | P1 465, P3 503, P6 503 |
| M3 | walk: the walk up stops one short of the edge | P1 465, P3 503, P6 503 |
| M4 | walk: the cell itself counted below | P1 600, P3 503, P5 640, P6 640 |
| M5 | bits: the mask below takes the cell's own value | P1 268, P3 305, P6 304 |
| M6 | bits: the mask above walks the anti-diagonal | P1 275, P2 310, P3 318, P6 311 |
| M7 | solution: the walk up-left starts at the cell | P1 269, P3 305, P6 305 |
| M8 | solution: the walk down-right goes down a column | P1 324, P2 403, P3 367, P5 341, P6 361 |
| M9 | ★: diagonals start only on the top row | P1 394, P2 489, P3 432, P6 432 |
| M10 | walk: the difference signed | P1 465, P3 503, P6 503 |

## Benchmarks

The bench draws 2000 grids of 50 by 50, LeetCode's largest, values up to
a random cap of 1 to 50, all of them first, then answers each 5 times by
the ★ arm in all five languages and folds every cell of every answer.
Every implementation prints `2000 grids of 50 by 50, 5 rounds:
differences sum to 193145865, checksum 432157979`.

BENCHTAB

## Verification

All four arms print the same output as `diagonals.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The ★ and walk arms checked clean as first written. The bits arm took
one `karac fix` of 2 edits: an `as i64` on each `count_ones()` dropped,
since it already answers `i64`.

LeetCode's Rust template took one `karac fix` of 22 edits: the `use
std::collections::HashSet;` became `struct Solution {}`, the
`Vec<Vec<i32>>` types `Vec[Vec[i32]]`, `vec![vec![0; n]; m]` became
`Vec.filled(m, Vec.filled(n, 0))`, `HashSet::new()` became `Set.new()`,
`let (mut x, mut y)` became `let mut (x, y)`, and `&&` became `and`.
