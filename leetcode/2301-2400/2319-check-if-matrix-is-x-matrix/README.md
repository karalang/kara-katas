# 2319. Check if Matrix Is X-Matrix

A square matrix is said to be an **X-Matrix** if **both** of the
following conditions hold:

1. All the elements in the diagonals of the matrix are **non-zero**.
2. All other elements are 0.

Given a 2D integer array `grid` of size `n x n` representing a square
matrix, return `true` *if* `grid` *is an X-Matrix*. Otherwise, return
`false`.

```
grid = [[2,0,0,1],[0,3,1,0],[0,5,2,0],[4,0,0,2]]  ->  true
grid = [[5,7,0],[0,3,1],[0,5,0]]                  ->  false
```

**Constraints:** `n == grid.length == grid[i].length`; `3 <= n <= 100`;
`0 <= grid[i][j] <= 10^5`.

A cell lies on a diagonal when `i == j` or `i + j == n - 1`, and each
cell then has one rule: nonzero on a diagonal, zero off it. One walk
over the cells, stopping at the first that breaks its rule. O(n^2).

## Approaches

| file | mechanism |
|---|---|
| `xmatrix.kara` ★ | one walk over the cells, each compared as `on != (grid[i][j] != 0)` with `on` its place on a diagonal, and an early `return false` |
| `xmatrix_mask.kara` | the pattern drawn first: a `Vec.filled` grid of flags, both diagonals marked by walking them, then every cell compared against its flag. O(n^2) space |
| `xmatrix_count.kara` | counted: the nonzero cells, and those of them on a diagonal; an X has `2 n` of them on the diagonals, `2 n - 1` when `n` is odd and they share the centre, and none off them |
| `xmatrix_rows.kara` | row by row: each row's nonzero places `collect`ed from a `filter` over `0..n`, and compared with the `Vec` of `i` and `n - 1 - i`, one place for the middle row of an odd matrix |
| `xmatrix_iter.kara` | iterators: `all` the rows, `enumerate`d, have `all` their cells, `enumerate`d, nonzero exactly when they lie on a diagonal |
| `xmatrix_solution.kara` | LeetCode's Rust template: `i32` cells, a `usize` side, nested `if`s and an early `return false`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples; the
smallest X, the same with its centre zero, and with a stray value
beside the centre; an X of 100 by 100, and the same with one stray
value; then 2000 random grids of 3 to 8 by as many, each cell given
the wrong kind of value one time in 20 to 200, with a checksum and the
count of X's. `xmatrix.py` mirrors the ★ arm and its output is
byte-identical.

`karac fix` carries the template in one call, reporting 13 edits:
`struct Solution;` to `struct Solution {}`; the nine brackets of the
three `Vec<Vec<i32>>` and `Vec<Vec<i64>>`, in the method and in the
harness's wrapper; `||` to `or`; and, in the wrapper, the `&` of the
closure's `|&v|` pattern dropped and `Solution::check_x_matrix` to
`Solution.check_x_matrix`. The `usize` side stands as Kāra, as `len()`
and the loop variables follow it.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the cells of both diagonals are gathered into a
`Set[(i64, i64)]`, and the matrix is an X when every cell in the set is
nonzero and every cell outside it is zero. No arithmetic on `i + j`
past building the set. It checks 300 random grids of 3 to 8 by as
many, each cell wrong one time in 2 to 40; then 30 true X's; then 30
X's with one cell wrong. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | an X holds `2 n` nonzero cells, or `2 n - 1` when `n` is odd |
| P3 | the grid transposed: the same answer |
| P4 | every row reversed: the same answer |
| P5 | every nonzero value made 1: the same answer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases, 119 X's: checksum 420670945, 12960
checks over 6 arms: 0 failures` under every lane in Verification; the
checksum of the literal answers was checked against a Python reading
that builds the same cases and compares each with a mask of the two
diagonals. On a failure it prints the first ten and then the count by
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
| M3 | ★: the last column never looked at | P1 25, P2 25, P3 41, P4 46, P6 25 |
| M5 | ★: the first row never looked at | P1 26, P2 23, P3 39, P6 26 |
| M6 | ★: a 1 taken for a zero | P5 119 |
| M8 | mask: the last row never marked | P1 120, P2 1, P3 1, P6 120 |
| M9 | mask: a value off the diagonals never refused | P1 90, P2 90, P6 90 |
| M10 | mask: the last row never compared | P1 24, P2 23, P3 41, P6 24 |
| M14 | count: the diagonals never counted full | P1 42, P2 42, P6 42 |
| M15 | count: a stray value let pass in a 3 by 3 grid | P1 12, P2 12, P6 12 |
| M16 | count: the centre of an odd grid needed twice | P1 88, P2 19, P6 88 |
| M17 | rows: the middle row of an odd grid wanting two places | P1 69, P6 69 |
| M19 | rows: the top half of the rows only | P1 74, P2 67, P3 93, P6 74 |
| M20 | rows: only the number of places compared | P1 5, P3 7, P6 5 |
| M22 | iter: any row enough | P1 225, P2 192, P3 11, P6 225 |
| M23 | iter: any cell enough | P1 238, P2 205, P3 4, P6 238 |
| M24 | iter: the zero cells wanted on the diagonals | P1 119, P6 119 |
| M30 | solution: the upper triangle only | P1 54, P2 50, P3 108, P4 63, P6 54 |
| M31 | solution: the first column never looked at | P1 21, P2 19, P3 39, P4 46, P6 21 |

P1 and P6 kill sixteen, P2 thirteen, P3 ten, P4 three and P5 one. P5,
every nonzero value made 1, is the one that kills the ★ arm's 1 taken
for a zero (M6): the random values run from 1 to `10^5`, so no case
holds a 1 where it matters until P5 puts one in every nonzero cell. P2
fails where an edit lets through a grid with a stray value or a
missing one, which is any edit that stops looking at part of the grid.
P3, the grid transposed, fails where an edit looks at rows and columns
differently: a row or a column never looked at, half the rows, a
triangle. P4, every row reversed, swaps the two diagonals and the first
and last columns, and fails only where the edit leaves out a column or
a triangle; leaving out a row is the same after it.

Of the thirty-one, fourteen were not kept. One is equivalent and
killed by nothing: the rows arm reading the columns for the rows
(M18), since an X's transpose is an X and so is nothing else's. Nine
fail on every X and on nothing else, as the iter arm's zero cells
wanted on the diagonals (M24): the ★ arm's second diagonal one place
over (M1) and main diagonal not a diagonal (M4), the mask arm's second
diagonal never marked (M7) and test turned round (M11), the rows arm's
second place one over (M21), the iter arm's second diagonal two places
over (M25) and first row left out with the rest counted from 0 (M26),
and the template's cell on both diagonals the only diagonal cell (M27)
and nonzero diagonal cell refused (M28). The ★ arm's (M2) and the
template's (M29) value off the diagonals never refused, and the count
arm's values off the diagonals not counted against (M13), fail as the
mask arm's (M9); the count arm's shared centre counted twice (M12) as
the rows arm's middle row wanting two places (M17).

M10, M15, M16 and M31 replace edits that failed as others did: the
mask arm's main diagonal marked twice, the count arm's main diagonal
alone counted and its 1 taken for a zero, and the template's second
diagonal one place short. Edits that leave out the last row in the
rows and iter arms, the last cell of each row in the iter arm and the
first row in the iter arm were tried for them and fail as the mask
arm's last row never compared (M10), the ★ arm's last column (M3) and
its first row (M5).

## Verification

Every arm prints the same output as `xmatrix.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.3 to 0.5 s, the work being
2000 grids of at most 64 cells and one of `10^4`, and the differential
0.7 s there and 0.5 s under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 200 X-matrices of 100 by 100 once, then makes 400
passes over them with the ★ arm in all five languages: in each pass
every grid has one cell chosen at random, given the wrong kind of value
half the time, checked, and put back, so that half the checks walk the
whole grid and half stop at the cell. Every implementation prints `400
passes over 200 grids of 100 by 100: checksum 785002455`. Each keeps a
grid as a list of rows of 64-bit integers, C as an array of row
pointers.

BENCHTAB
