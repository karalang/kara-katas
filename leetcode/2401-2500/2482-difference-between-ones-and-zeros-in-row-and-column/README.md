# 2482. Difference Between Ones and Zeros in Row and Column

You are given a **0-indexed** `m x n` binary matrix `grid`.

A **0-indexed** `m x n` difference matrix `diff` is created with the
following procedure:

- Let the number of ones in the `i`th row be `onesRow_i`.
- Let the number of ones in the `j`th column be `onesCol_j`.
- Let the number of zeros in the `i`th row be `zerosRow_i`.
- Let the number of zeros in the `j`th column be `zerosCol_j`.
- `diff[i][j] = onesRow_i + onesCol_j - zerosRow_i - zerosCol_j`

Return *the difference matrix* `diff`.

```
grid = [[0,1,1],[1,0,1],[0,0,1]]  ->  [[0,0,4],[0,0,4],[-2,-2,2]]
grid = [[1,1,1],[1,1,1]]          ->  [[5,5,5],[5,5,5]]
```

**Constraints:** `m == grid.length`; `n == grid[i].length`;
`1 <= m, n <= 10^5`; `1 <= m * n <= 10^5`; `grid[i][j]` is either `0`
or `1`.

A row of `n` cells with `r` ones has `n - r` zeros, and a column of `m`
cells with `c` ones has `m - c`, so `diff[i][j]` is `2 r + 2 c - m - n`:
one pass counts every row's and column's ones, and a second fills the
answer.

## Approaches

| file | mechanism |
|---|---|
| `diff.kara` ★ | by the ones alone: every row's and column's ones counted in one pass, and each answer `2 r + 2 c - m - n`. O(m n) |
| `diff_four.kara` | the four counts as the statement names them: ones and zeros of every row and column, each cell adding to two of the four, and each answer the statement's sum. O(m n) |
| `diff_signed.kara` | by signed sums: a one counts `+1` and a zero `-1`, so a row's or a column's sum is its ones less its zeros, and each answer the two sums added, written in place in a copy of the grid. O(m n) |
| `diff_transpose.kara` | by transposing: one counting function, a row's ones less its zeros, run over the grid's rows and over the rows of its transpose, built cell by cell. O(m n) |
| `diff_iter.kara` | iterators: the rows' ones by `map` and `sum`, the columns' by a `fold` over the rows adding each in with `zip`, and the answer by nested `map`s. O(m n) |
| `diff_solution.kara` | LeetCode's Rust template: `Vec<Vec<i32>>` in and out; the ones counted into two `vec![0; _]` lists, and the answer built by `map` and `collect` over two ranges with `as i32` casts on the sizes; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's two examples; then five
more, one cell of each bit, a single row, a single column, and a grid of
zeros; then the constraints' largest, `10^5` cells, as a row of `10^5`,
a column of `10^5` and a 316 by 316 square of random bits, each as a
checksum; and 3000 random grids of 1 to 8 rows and columns, as a
checksum. `diff.py` mirrors the ★ arm and its output is byte-identical,
and the mirror was checked on 5000 random grids of 1 to 9 rows and
columns against the statement's four counts taken cell by cell. The two
agreed on every grid.

`check` first reports 2 errors on the template, the two `Vec<Vec<i32>>`
in the signature, and `karac fix` carries it in one call, reporting 11
edits: the generic brackets of both, eight edits; each `vec![0; _]`
becomes `Vec.filled(_, 0i32)`, its element type taken from the grid's
values added into it; and `struct Solution {}` is added. The tuple
`let (m, n)`, the `as i32` casts and the chained `map` and `collect`
stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for every cell, its row and its column walked afresh and
their ones and zeros counted, four counts a cell, and the statement's
sum taken. No count is shared between cells. It checks 300 random grids
of 1 to 5 rows and columns, then 60 of up to 12, every bit drawn at
random. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | every bit flipped: every value negated |
| P3 | the grid transposed: the answer transposed |
| P4 | the rows in reverse order: the answer's rows in reverse order |
| P5 | a row of ones added below: every old value one more, and the new row's values those of the larger grid read literally |
| P6 | each arm agrees with at least three of the other five |

P2 holds because flipping every bit swaps each count of ones with the
count of zeros beside it. P3 holds because the transpose swaps rows and
columns, and the sum is symmetric in the two. P4 holds because a row's
counts do not depend on where it stands and a column's not on the order
of its cells. P5 holds because the new row leaves every old row's counts
as they were and adds a one to every column.

The differential prints `360 cases: checksum 519673925, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and counts the same way. On a failure it prints the
first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: the rows' length taken for the columns' | P1 304, P2 304, P3 304, P5 360, P6 304 |
| M3 | ★: a column's ones added at the row's number | P1 242, P2 219, P3 304, P4 172, P5 283, P6 242 |
| M5 | ★: the last column never counted | P1 293, P2 360, P3 312, P5 360, P6 293 |
| M8 | four: the bits read the other way round | P1 359, P5 360, P6 359 |
| M9 | four: the column's zeros added | P1 343, P2 360, P3 336, P5 343, P6 343 |
| M10 | four: the columns' zeros read mirrored | P1 222, P3 297, P5 222, P6 222 |
| M14 | signed: the sums multiplied | P1 358, P2 325, P5 360, P6 358 |
| M15 | signed: the first row never counted | P1 360, P3 350, P4 293, P5 360, P6 360 |
| M16 | signed: each column's sum given to the one before | P1 252, P3 322, P5 252, P6 252 |
| M17 | transpose: zeros not taken away | P1 343, P2 360, P5 343, P6 343 |
| M20 | transpose: the last row left out of every column | P1 360, P3 315, P4 243, P5 360, P6 360 |
| M21 | transpose: every row taken as the first | P1 266, P3 322, P4 208, P5 290, P6 266 |
| M23 | iter: the columns' ones capped at one | P1 233, P2 286, P3 286, P5 340, P6 233 |
| M24 | iter: the first cell of each row skipped | P1 292, P2 360, P3 306, P5 360, P6 292 |
| M25 | iter: the rows answered backwards | P1 243, P3 297, P5 343, P6 243 |
| M28 | solution: the columns' length added | P1 360, P2 360, P3 304, P5 360, P6 360 |
| M29 | solution: a column's ones read at the row's number | P1 252, P3 322, P4 157, P5 252, P6 252 |

P1, P5 and P6 kill all seventeen, P3 fourteen, P2 nine, and P4 five.

Fourteen are not kept. Two fail exactly as a kept one: the signed arm's
only the ones counted (M12) as the transpose arm's zeros not taken away
(M17), and the transpose arm's columns taken right to left (M18) as the
four arm's columns' zeros read mirrored (M10). Eleven more fail in five
groups, alike within each and apart from every kept one: the ★ arm's
ones counted once and cell counted again (M1, M6); the ★ arm's rows'
ones never counted and the iter arm's column's ones counted once (M4,
M22); the four arm's row's zeros never counted and the template's
every cell a one in its row (M7, M27); the four arm's zero too many in
every row, the iter arm's column a one ahead and the template's one
too many in every row (M11, M26, M31), each moving every value by the
same amount; and the signed arm's column's sum taken away and the
transpose arm's column's balance taken away (M13, M19). The template's
only the cells on or past the diagonal counted (M30) fails apart from
every kept one, the template having its two kept already. No edit
crashes, and every edit is killed by some check.

## Verification

Every arm prints the same output as `diff.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.4 to 4.5 s and the differential 1.6 s; under `karac __mir-llvm-asan` the arms take 0.7 to 1.5 s and the differential 1.1 s, and under `karac run` the differential takes 0.7 s.

## Benchmarks

The bench builds 20 random 100 by 100 grids once from its own
generator, then makes 180 passes; each flips one cell of every grid,
chosen by the checksum so far, so no answer repeats the last, answers
the grid, and folds every value plus the pass into the checksum. The
bench uses the ★ arm in all five languages, each answer a fresh list of
rows in Kāra, Rust, Go and Python; C keeps each grid, and writes each
answer, as one flat array. Every implementation prints `180 passes
over 20 grids of 100 by 100: checksum 248546846`.

BENCHTAB
