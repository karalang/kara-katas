# 1277. Count Square Submatrices with All Ones

Given a `m * n` matrix of ones and zeros, return how many **square**
submatrices have all ones.

```
matrix = [[0,1,1,1],[1,1,1,1],[0,1,1,1]]  ->  15
matrix = [[1,0,1],[1,1,0],[1,1,0]]        ->  7
```

In the first, there are 10 squares of side 1, 4 of side 2 and 1 of side
3; in the second, 6 of side 1 and 1 of side 2.

**Constraints:** `1 <= arr.length <= 300`; `1 <= arr[0].length <= 300`;
`0 <= arr[i][j] <= 1`.

The arms are `fn count_squares(matrix: Vec[Vec[i64]]) -> i64`.

## Approaches

| file | mechanism |
|---|---|
| `count_squares.kara` ★ | by dynamic programming: the largest all-ones square with its bottom right corner at a 1 is one more than the smallest of those ending above it, to its left and diagonally above; that side is also the number of squares ending there, and the answer is their sum. O(mn) |
| `count_squares_row.kara` | by one row: the ★ arm's sides kept for the previous row only, the diagonal neighbour saved before it is overwritten. O(n) memory |
| `count_squares_prefix.kara` | by prefix sums: a square's sum read from a table of the sums above and to the left through a captured closure; from each top left corner squares of side 1, 2, ... counted while their sum is their area. O(mn min(m, n)) |
| `count_squares_levels.kara` | by levels: a square of side k + 1 is four of side k overlapping, so each level is a grid of `bool`s one smaller each way than the last, made from it, until none is left; the answer the `true`s over every level |
| `count_squares_memo.kara` | by memoised recursion: the side of the largest square ending at a cell asked of the three cells before it, each answer kept in a `Map[(i64, i64), i64]` |
| `count_squares_solution.kara` | a Rust solution as LeetCode's Rust users write it (`mut matrix: Vec<Vec<i32>>` taken and overwritten in place with the sides, `.min()` chains), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's two examples (`15 7`); 2000
random matrices of 1 to 12 by 1 to 12, half, four fifths and nineteen
twentieths ones (`2000 random matrices: 109329 squares, checksum
196015362`); and the constraints' top, 300 by 300 all ones, whose count is
the sum of the squares to 300, and nine tenths ones, and a row and a
column of 300 ones (`9045050 198791 300 300`). `count_squares.py` mirrors
the ★ arm, and its output is byte-identical. Every arm gives the same
output under `karac run` and `karac build`, and under the
AddressSanitizer build.

The Mend loop: the ★, row, prefix and memo arms checked clean as first
written. The levels arm was written with Rust's `filter(|x| **x)`; E0209
said a `bool` is copied and the `*` should go, and `karac fix` dropped
one. The solution arm takes one round of 15 fixes by `karac fix`'s count:
Rust's `mut matrix` parameter became `matrix: own Vec[Vec[i32]]` with
`let mut matrix = matrix;` at the top of the body, `Vec<..>` went to
brackets, `&&` to `and`, `res` was given the `i32` type Rust inferred from
the return, the wrapper's `as i64` on the `i32` answer was dropped as a
widening Kāra does by itself, and `struct Solution;`, `::` and the
closure's `|&x|` took Kāra's spelling. No gap was met.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every square submatrix, each top left corner and each side
that fits, its cells looked at one by one. 2000 random matrices of 1 to 8
by 1 to 8, half, four fifths and nineteen twentieths ones.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | at least the number of ones, at most the number of squares that fit |
| P3 | the matrix transposed, the same count |
| P4 | the rows in reverse order, the same count |
| P5 | one 1 turned to 0, a smaller count |
| P6 | the ★ arm's count |

All 72,000 checks pass on every arm: `2000 matrices: checksum 324330684,
72000 checks over 6 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python gives the same
checksum.

## Mutation testing

Twelve edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: the diagonal neighbour left out | P1 906, P4 883, P6 4530 |
| S2 | ★: the larger of the sides above and to the left taken | P1 1099, P4 970, P6 5495 |
| R1 | row: the diagonal read from the row being written | P1 906, P4 883, P6 906 |
| R2 | row: the last column skipped | P1 1886, P2 1209, P3 1738, P5 674, P6 1886 |
| P1 | prefix: a square one cell short of full counted | P1 1585, P5 1047, P6 1585 |
| P2 | prefix: squares of side 4 and up never counted | P1 202, P6 202 |
| L1 | levels: a square grown from three of its four smaller ones | P1 904, P3 921, P4 883, P6 904 |
| L2 | levels: each level's first column skipped | P1 967, P3 928, P6 967 |
| M1 | memo: the first row read as zeros | P1 1896, P2 1189, P3 1715, P4 1158, P5 664, P6 1896 |
| M2 | memo: an answer kept under the transposed cell | P1 449, P3 454, P4 557, P5 7, P6 449 |
| O1 | solution: a 0 grown from its neighbours | P1 1163, P4 895, P5 855, P6 1163 |
| O2 | solution: no cell counting more than 2 squares | P1 528, P6 528 |

All twelve are caught, every one by P1, the statement read literally.
P3, the matrix transposed, sees only the five edits that treat rows and
columns differently (R2, L1, L2, M1, M2); P4, the rows reversed, sees
most of the rest, since a square's corner moves from bottom right to top
right and an edit to the three neighbours there shows. P2, the bounds,
sees the two that lose whole cells (R2, M1), and P5, a 1 lowered, a count
that cannot fall. The two that only cap the count (P2, O2) are seen by
P1 alone.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (dynamic programming over the sides of the largest squares) on 40
random 300-by-300 matrices, half, four fifths, nineteen twentieths and
99 in 100 ones, drawn once; 50 rounds, every count folded into a
checksum. Every program prints `50 rounds of 40 matrices of 300 by 300:
checksum 783541048`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.916 to 1.038 s | 0.984 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.931 to 1.010 s | 0.974 s |
| Rust (`rustc -O`) | 1.297 to 1.371 s | 1.337 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.331 to 1.441 s | 1.367 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 1.330 to 1.418 s | 1.374 s |
| C (`clang -O3`) | 1.118 to 1.200 s | 1.148 s |
| C (`clang -O3 -march=x86-64-v3`) | 1.091 to 1.186 s | 1.113 s |
| Go | 1.378 to 1.500 s | 1.451 s |
| Python | 33.92 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra is about 29% ahead of Rust with overflow checks on (0.974 s
against 1.367 s). Kāra is about 15% ahead of C (0.974 s against 1.148
s); Kāra is about 33% ahead of Go (0.974 s against 1.451 s). Python
takes about 35x Kāra's time. No profile was taken.
