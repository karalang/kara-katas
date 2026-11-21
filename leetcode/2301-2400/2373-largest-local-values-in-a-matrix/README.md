# 2373. Largest Local Values in a Matrix

You are given an `n x n` integer matrix `grid`.

Generate an integer matrix `maxLocal` of size `(n - 2) x (n - 2)` such
that `maxLocal[i][j]` is equal to the **largest** value of the `3 x 3`
matrix in `grid` centered around row `i + 1` and column `j + 1`.

In other words, we want to find the largest value in every contiguous
`3 x 3` matrix in `grid`.

Return *the generated matrix*.

```
grid = [[9,9,8,1],[5,6,2,6],[8,2,6,4],[6,2,2,2]]                      ->  [[9,9],[8,6]]
grid = [[1,1,1,1,1],[1,1,1,1,1],[1,1,2,1,1],[1,1,1,1,1],[1,1,1,1,1]]  ->  [[2,2,2],[2,2,2],[2,2,2]]
```

**Constraints:** `n == grid.length == grid[i].length`; `3 <= n <= 100`;
`1 <= grid[i][j] <= 100`.

Each block of nine overlaps its neighbours in six cells, and the largest
of a block is the largest of its three rows' largest, so the work can be
split by rows and then by columns, or done as two overlapping steps of
`2 x 2`.

## Approaches

| file | mechanism |
|---|---|
| `local.kara` ★ | each cell of the answer the largest of the nine values of its block, read cell by cell. O(9 n^2) |
| `local_separable.kara` | the largest of each row's windows of three first, then the largest of each column of those in windows of three. O(6 n^2) |
| `local_pairs.kara` | the largest of each `2 x 2` block, and then the largest of each `2 x 2` block of those, since two overlapping steps of two cover three cells each way. O(8 n^2) |
| `local_deque.kara` | each line's windows of three by a deque of places whose values fall from front to back, the rows first and then the columns of those, turned back at the end. O(n^2) whatever the window |
| `local_iter.kara` | iterators: each cell the `max` of its block flattened by `flat_map` over the block's three rows |
| `local_solution.kara` | LeetCode's Rust template: a result of zeros from `vec![vec![0; n - 2]; n - 2]`, each cell raised to the largest of its block over `x in i..i + 3` and `y in j..j + 3`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 5 lines: LeetCode's two examples; a `3 x 3`
grid; a `100 x 100` grid of `(i j) % 100 + 1` and one of
`100 - (i + j) % 100`, folded to checksums; then 1000 random grids of
`3 x 3` to `12 x 12` with values from 1 up to 1 to 100, with a checksum
and how many answers hold one value throughout. `local.py` mirrors the
★ arm and its output is byte-identical, and the mirror was checked on
2000 random grids of up to `9 x 9` against every cell of the grid
scanned for each cell of the answer.

`check` first reports 4 errors on the template, and `karac fix` carries
it in one call, reporting 11 edits: `struct Solution;` given its
braces, `Vec<..>` its brackets, `vec![vec![0; n - 2]; n - 2]`
written `Vec.filled(n - 2, Vec.filled(n - 2, 0i32))`, and `Solution::`
written with a dot. The nested `vec!` first came out with a bare `0`,
an `i64` against the `Vec[Vec[i32]]` it returns, with no fix offered,
where the flat `vec![0; n]` gets its `0i32` (B-2026-11-21-42, fixed); the
template was carried again after the fix.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each cell `(i, j)` of the answer the largest value of the
whole grid among the cells whose row is from `i` to `i + 2` and whose
column is from `j` to `j + 2`, the whole grid scanned for each. No
blocks and no windows. It checks 300 random grids of `3 x 3` to
`12 x 12` with values from 1 up to 1 to 100; then 30 of up to `30 x 30`;
then 30 of up to `20 x 20` with values from 1 to 3. All 360 are drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | `n - 2` rows of `n - 2`, each cell at least the middle of its block and at most the grid's largest |
| P3 | the grid transposed: the answer transposed |
| P4 | every row of the grid reversed: every row of the answer reversed |
| P5 | every value `v` made `2 v + 1`: every value of the answer made `2 v + 1` |
| P6 | each arm agrees with at least three of the other five |

P3 and P4 hold because the blocks of the transposed or mirrored grid are
the old blocks transposed or mirrored, with the same nine values. P5
holds because `2 v + 1` keeps the order of the values, so the largest
of a block stays the largest; the `+ 1` makes a cell left at 0 fail
it, where doubling alone would keep it at 0.

The differential prints `360 cases: checksum 653177290, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and scans the whole grid for each cell. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the block's last row left out | P1 312, P3 324, P6 312 |
| M3 | ★: the largest started at 50 | P1 249, P2 178, P5 249, P6 249 |
| M4 | ★: only the block's diagonal read | P1 345, P4 349, P6 345 |
| M8 | separable: the middle row of each block left out | P1 316, P2 293, P3 327, P6 316 |
| M9 | separable: each row's windows listed backwards | P1 291, P2 241, P3 294, P6 291 |
| M11 | separable: the third cell of a row's window taken by min | P1 353, P2 326, P3 347, P4 339, P6 353 |
| M12 | pairs: one step of 2 x 2 only | P1 360, P2 360, P6 360 |
| M13 | pairs: the bottom right of each 2 x 2 left out | P1 311, P4 326, P6 311 |
| M14 | pairs: only the top row of each 2 x 2 | P1 338, P2 316, P3 347, P6 338 |
| M18 | deque: a place kept one step too long | P1 289, P4 277, P6 289 |
| M19 | deque: the deque never trimmed from the back | P1 353, P2 333, P4 355, P6 353 |
| M21 | deque: the column windows not turned back | P1 294, P2 221, P4 294, P6 294 |
| M23 | iter: the smallest of the block | P1 357, P2 353, P6 357 |
| M25 | iter: two of each row's three | P1 308, P3 324, P4 333, P6 308 |
| M26 | iter: the block's first row left out | P1 315, P3 331, P6 315 |
| M29 | solution: only the cells on and below the diagonal filled | P1 322, P2 322, P3 322, P4 322, P5 322, P6 322 |
| M31 | solution: the answer's first row left at zero | P1 360, P2 360, P3 322, P5 360, P6 360 |

P1 and P6 kill all seventeen, P2 eleven, P3 nine, P4 eight and P5
three. P5, every value made `2 v + 1`, fails only the edits whose answer
does not come from the grid's values alone: the largest started at 50
in the ★ arm, which the small values never pass, the cells above the
diagonal and the first row left at the template's zero. P3, the grid
transposed, passes the edits that treat rows and columns alike, as the
diagonal read alone and the windows' places kept one step too long, and
P4, the rows reversed, passes those that treat the left and the right
alike, as a block's last row or the middle row left out.

Of the thirty-one, fourteen were not kept. The block's last row left
out in the iter and template arms (M22, M28) fails as in the ★ arm (M1);
each row's windows of two in the separable and deque arms (M7, M20) as
two of each row's three in the iter arm (M25); and the deque kept
rising (M17) as the iter arm's smallest of the block (M23). The ★ arm's
first column left out (M2), answer's last row left out (M5) and block's
last cell taken (M6), the separable arm's rows written bottom up (M10),
the pairs arm's top right and bottom left left out (M15, M16), and the
template's cells started at 7 (M27) and first column read thrice (M30)
fail apart from every kept one, and were left out to keep three to an
arm and two to the template. The iter arm's answer's last column left
out (M24) stops with an index out of bounds in the differential's
transpose, which reads a square answer.

## Verification

Every arm prints the same output as `local.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.6 to 1.9 s, and the differential
9.2 s there and 0.77 s under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 10 grids of `100 x 100` once from the harness's
generator, grid `a` holding random values from 1 to `10 (a + 1)`, then
makes 200 passes, pass `p` folding each cell of each answer plus `p`
into the checksum, with the ★ arm in all five languages. Every
implementation prints `200 passes over 10 grids of 100 x 100: checksum
350137494`. Every implementation builds each answer afresh in each
call.

BENCHTAB
