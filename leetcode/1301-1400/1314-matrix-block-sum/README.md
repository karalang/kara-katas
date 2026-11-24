# 1314. Matrix Block Sum

Given a `m x n` matrix `mat` and an integer `k`, return a matrix `answer`
where each `answer[i][j]` is the sum of all elements `mat[r][c]` for:

- `i - k <= r <= i + k,`
- `j - k <= c <= j + k`, and
- `(r, c)` is a valid position in the matrix.

```
mat = [[1,2,3],[4,5,6],[7,8,9]], k = 1  ->  [[12,21,16],[27,45,33],[24,39,28]]
mat = [[1,2,3],[4,5,6],[7,8,9]], k = 2  ->  [[45,45,45],[45,45,45],[45,45,45]]
```

**Constraints:** `m == mat.length`, `n == mat[i].length`, `1 <= m, n, k
<= 100`, `1 <= mat[i][j] <= 100`.

The arms are `fn matrix_block_sum(mat: Vec[Vec[i64]], k: i64) ->
Vec[Vec[i64]]`.

## Approaches

| file | mechanism |
|---|---|
| `matrix_block_sum.kara` ★ | a table of sums over every top-left rectangle, one row and one column wider than the matrix, so that any block's sum is four lookups: the rectangle to its bottom right corner, less the two beside it, plus the one they both took away. O(m n) |
| `matrix_block_sum_rows.kara` | a running sum along each row on its own, so that a block's slice of one row is two lookups; each cell's block then added up a row at a time. O(m n min(2k + 1, m)) |
| `matrix_block_sum_sliding.kara` | a window of width 2k + 1 slid along each row, adding the number coming in on the right and taking away the one leaving on the left, gives every cell its row's slice; the same window then slid down each column of those slices gives the blocks. O(m n) |
| `matrix_block_sum_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `vec![vec![0; n + 1]; m + 1]` table of top-left rectangle sums, each block's corners clamped by `i.saturating_sub(k)` and `(i + k + 1).min(m)` on `usize` indices), carried to Kāra by `karac fix` |
| `matrix_block_sum_clamped.kara` | a second Rust solution as LeetCode's Rust users write it (the prefix table and the loops in `i32`, each corner clamped by `(i - k).max(0)` and `(i + k).min(m - 1)` and cast `as usize` only to index), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's two examples, one cell, a
single row with k past its ends, and a single column
(`12,21,16/27,45,33/24,39,28 45,45,45/45,45,45/45,45,45 5 3,6,9,12,9
6/10/10/9`); then 600 random matrices of 1 to 100 rows and columns, the
constraints' most, with numbers from 1 to 100 and k from 1 to 100, most
of it small (`600 random matrices: sum of answers 60006893645, checksum
598285804`). `matrix_block_sum.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run` and `karac __mir-llvm-run`.

The Mend loop: the three Kāra arms checked clean as first written. The
first Rust arm takes one round of 28 fixes by `karac fix`'s count, from 9
errors: `struct Solution;` to `struct Solution {}`, `Vec<..>` to
`Vec[..]`, `vec![vec![0; n + 1]; m + 1]` to `Vec.filled(m + 1,
Vec.filled(n + 1, 0i32))`, `let k = k as usize` to `let k = k as i64`,
`|&x|` to `|x|`, `::` to `.`, and `i.saturating_sub(k)` to
`i.saturating_sub(k).max(0)`: `usize` is retyped to `i64`, where a
saturating subtraction no longer stops at 0, so the fix adds the floor
Rust's type gave. With the index an `i64` and only `k` written `usize`,
that floor was first missed and the fixed program indexed below 0
(B-2026-11-21-70, fixed since). The second Rust arm takes one round of 36
fixes from 9 errors: the same rewrites, with each `as usize` to `as i64`
and `res[i as usize][j as usize]` to `res[i][j]`. Both outputs match on
the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: for every cell, every position of the matrix looked at, and
its number added when both its row and its column are within k. 2000
matrices of 1 to 8 rows and 1 to 8 columns, k from 1 to 9, in four kinds,
500 each: numbers up to 3; up to 100; one number throughout; and a single
row or a single column. Every matrix and raise is drawn before any arm
answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the matrix turned on its side: the answer turned with it |
| P3 | the rows in the reverse order: the answer's rows reversed |
| P4 | every number raised: each answer raised that much for every cell of its block |
| P5 | k as large as the matrix: every answer the whole matrix's sum |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 matrices: checksum 326539340,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run` and
`karac __mir-llvm-run`. Python gives the same checksum.

## Mutation testing

Eleven edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`. One is left out: the Rust arm's
block a row short at the bottom fails exactly the checks the row arm
leaving out a block's last row fails. The ten kept, two to each arm, are
each killed, fail the same way under both backends and not by a crash, and
no two fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the first row never in a block | P1 2000, P2 1868, P3 1194, P4 2000, P5 2000, P6 8000 |
| M2 | ★: the shared corner taken away twice | P1 224, P3 224, P4 224, P6 896 |
| M3 | rows: the block's last row left out | P1 660, P2 1013, P3 660, P4 660, P6 660 |
| M4 | rows: each row's slice losing its first number | P1 2000, P2 1868, P4 2000, P5 2000, P6 2000 |
| M5 | sliding: the window started one too wide | P1 1013, P3 404, P4 1013, P6 1013 |
| M6 | sliding: the number leaving taken away a step early | P1 1013, P3 660, P4 1013, P6 1013 |
| M7 | solution: the block a row too tall at the top | P1 496, P2 759, P3 496, P4 496, P6 496 |
| M8 | solution: the rectangles' overlap never taken away | P1 1162, P3 907, P4 1162, P5 1162, P6 1162 |
| M9 | clamped: the block a column short on the right | P1 2000, P2 1874, P4 2000, P5 2000, P6 2000 |
| M10 | clamped: the block a row short at the top | P1 2000, P2 1868, P3 1044, P4 2000, P5 2000, P6 2000 |

P1, P4 and P6 kill all ten, P3 eight, P2 six and P5 five. Raising every
number (P4) raises each answer by the number of cells in its block, so it
sees every edit, each of which gets some block's cells or its arithmetic
wrong. Turning the matrix on its side (P2) catches the edits that treat
rows and columns differently, and misses the four that make the same
mistake both ways: the corner (M2), the sliding window, which is slid
along the rows and down the columns alike (M5, M6), and the table's
overlap (M8). Turning it upside down (P3) misses only the two edits that
go wrong along each row alone (M4, M9). A k as large as the matrix (P5)
makes every block the whole matrix, where the clamps hide a row too few or
too many and the corner and the window no longer matter, so it catches
only the edits that lose a row or a column whatever k is (M1, M4, M9,
M10) and the wrong table (M8).

## Benchmarks

The bench builds 20 matrices of 100 by 100, the constraints' most, with
numbers up to 100, once from its own generator; then makes 200 passes,
each setting one number of every matrix and choosing k from 1 to 100,
mostly small, both from the checksum so far, so no answer carries over,
answering it with the ★ arm and folding two of its sums, at places chosen
by the checksum, plus the pass into the checksum. Each call takes a fresh
table and answer in every language, a `calloc` and a `malloc` in C. Every
implementation prints `200 passes over 20 matrices of 100 by 100:
checksum 717657350`.

BENCHTAB
