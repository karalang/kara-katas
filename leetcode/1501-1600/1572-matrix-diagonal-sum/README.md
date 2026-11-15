# 1572. Matrix Diagonal Sum

Given a square matrix `mat`, return the sum of the matrix diagonals. Only
include the sum of all the elements on the primary diagonal and all the
elements on the secondary diagonal that are not part of the primary
diagonal.

```
mat = [[1,2,3],[4,5,6],[7,8,9]]                       ->  25
mat = [[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1]]       ->  8
mat = [[5]]                                           ->  5
```

**Constraints:** `n == mat.length == mat[i].length`; `1 <= n <= 100`;
`1 <= mat[i][j] <= 100`.

## Approaches

| file | mechanism |
|---|---|
| `diagonal.kara` ★ | each row's two diagonal cells added by index, and the centre, which both diagonals share in an odd matrix, taken off once. O(n) |
| `diagonal_fold.kara` | each row folded to the cells it has on the two diagonals, one where they meet, by `iter().enumerate().map(..).sum()`. O(n) |
| `diagonal_cells.kara` | every cell visited, and the ones on either diagonal added: the centre counts once because it is visited once. O(n²) |
| `diagonal_solution.kara` | LeetCode's Rust template (`diagonal_sum(mat: Vec<Vec<i32>>) -> i32`), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's three examples, then
`[[1, 2], [3, 4]]` and a 3 by 3 matrix of 100s and 1s; then the sum of
the answers and a checksum for 3000 random matrices of 1 to 5 rows of
values from 1 to 3, and 3000 of 1 to 100 rows of values from 1 to 100.
`diagonal.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: the positions of both diagonals gathered into one
`SortedSet`, so a cell on both is in it once, and their values added. It
checks 3000 matrices of 1 to 7 rows of values from 1 to 9, every random
choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the matrix transposed leaves the answer |
| P3 | the rows in reverse order leave the answer |
| P4 | every value doubled doubles the answer |
| P5 | every value raised by 1 adds one for each diagonal cell, `2n - n % 2` |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 470027450, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

The first M5 read the other diagonal one cell to the right, `n - i`,
which ran off the end of the first row: killed by an index out of
bounds rather than by a property, so it was replaced.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the centre taken off in an even matrix in place of an odd one | P1 3000, P3 1111, P5 3000, P6 3000 |
| M2 | ★: the main diagonal read twice, the second time in place of the other | P1 2415, P3 2415, P6 2415 |
| M3 | ★: the last row left out | P1 3000, P2 2264, P3 2383, P5 3000, P6 3000 |
| M4 | fold: the centre counted twice | P1 1751, P5 1751, P6 1751 |
| M5 | fold: the other diagonal's cell added twice, in place of the main one | P1 2415, P3 2415, P6 2415 |
| M6 | fold: the first row left out | P1 3000, P2 2264, P3 2383, P5 3000, P6 3000 |
| M7 | cells: the other diagonal one cell to the right | P1 2442, P3 2430, P5 1249, P6 2442 |
| M8 | cells: only the half of the other diagonal above the main one | P1 2572, P2 2360, P3 2366, P5 2572, P6 2572 |
| M9 | template: the centre test one off | P1 3000, P2 1106, P3 1104, P5 3000, P6 3000 |
| M10 | template: the other diagonal's cell added in place of the main one | P1 2415, P3 2415, P6 2415 |

## Benchmarks

An O(n) answer over a matrix that fits in the constraints takes no
measurable time, so the bench builds one matrix of 1001 rows of values
from 1 to 100 once, then runs 200000 rounds that each write one random
cell and sum the diagonals again, by the ★ arm, in all five languages.
The write makes every round's answer depend on the last, so no compiler
can hoist the sum out of the loop. Every implementation prints `200000
rounds on 1001 rows: sums total 20318596015, checksum 598615240`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `572956a03` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.289 s |
| Rust (`rustc -O`) | 0.326 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.330 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.340 s |
| Kāra (`karac build`) | 0.351 s |
| Go | 0.437 s |
| Python | 16.9 s |

Kāra is 0.97x Rust under overflow checks by median, a tie inside the
run-to-run spread. Each round reads one cell from every one of the 1001
rows, so most of the time in every language is the cache misses of that
walk, which no language avoids.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.313 s and 0.319 s on one run).

## Verification

All four arms print the same output as `diagonal.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change. Checked at kara `572956a03`.

## Writing it

The ★, fold and cells arms were written in Kāra and checked as written.

The Rust template took two rounds of `karac fix`, 3 changed lines, then
2:

1. the `Vec<..>` types to `[..]`, the wrapper's `|&x|` to `|x|`, and
   `Solution::` to `Solution.`;
2. `sum`'s literal to `sum: i32`, and the wrapper's `as i64` dropped
   (an `i32` widens to `i64` on its own).

It then checks and agrees with no hand edit.
