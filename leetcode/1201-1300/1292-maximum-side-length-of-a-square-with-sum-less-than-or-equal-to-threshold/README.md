# 1292. Maximum Side Length of a Square with Sum Less than or Equal to Threshold

Given a `m x n` matrix `mat` and an integer `threshold`, return the
maximum side-length of a square with a sum less than or equal to
`threshold` or return `0` if there is no such square.

```
mat = [[1,1,3,2,4,3,2],[1,1,3,2,4,3,2],[1,1,3,2,4,3,2]], threshold = 4  ->  2
mat = [[2,2,2,2,2],[2,2,2,2,2],[2,2,2,2,2],[2,2,2,2,2],[2,2,2,2,2]], threshold = 1  ->  0
```

**Constraints:** `1 <= m, n <= 300`, `0 <= mat[i][j] <= 10^4`,
`0 <= threshold <= 10^5`.

The arms are `fn max_side_length(mat: Vec[Vec[i64]], threshold: i64) ->
i64`.

## Approaches

The values are never negative, so a square inside one that fits fits
too: the sides that fit are every side up to the answer.

| file | mechanism |
|---|---|
| `max_side_length.kara` ★ | two-dimensional prefix sums, built as it goes, and each cell the bottom-right corner of a square one longer than the best so far; the best grows by at most one per corner, so a corner that fits it raises it. O(mn) |
| `max_side_length_binary.kara` | the prefix sums, then a binary search on the side, each try scanning every position of a square of that side. O(mn log min(m, n)) |
| `max_side_length_every.kara` | the prefix sums, then from each top-left corner every side in turn until the square's sum passes the threshold. O(mn min(m, n)) |
| `max_side_length_sliding.kara` | no two-dimensional table: for a side k, the column sums of a band of k rows, moved down a row at a time, with a window of k of them sliding along the band; the side grows while some square of the next side fits. O(mn) per side tried |
| `max_side_length_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `vec![vec![0; n + 1]; m + 1]` prefix table, a `check` closure over it, and a binary search with `let mid = (lo + hi + 1) / 2`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's two examples, a threshold
of 0 over zeros and over ones, and a single cell at and above the
threshold (`2 0 2 0 1 0`); then 601 random matrices, 600 up to 30 by 30
in three kinds with values up to `10^4`, 100 and 9, and one of 100 by
100 with values up to 9, each with a threshold up to `10^5` (`601 random
matrices: sides total 4766, checksum 581546210`). `max_side_length.py`
mirrors the ★ arm, and its output is byte-identical. Every arm gives the
same output under `karac __mir-run`, `karac run` and `karac
__mir-llvm-run`.

The Mend loop: the four Kāra arms checked clean as first written. The
Rust arm takes one round of 20 fixes by `karac fix`'s count, from 9
errors: `Vec<..>` to `Vec[..]`, `vec![vec![0; n + 1]; m + 1]` to
`Vec.filled(m + 1, Vec.filled(n + 1, 0))`, `struct Solution;` to
`struct Solution {}`, `::` to `.`, `&&` to `and`, the closure's `|k:
usize| -> bool` to `|k: i64|`, `let (mut lo, mut hi)` to `let mut (lo,
hi)`, the wrapper's `|&x|` to `|x|`, and its `as i64` dropped as a
widening. Its output matches on the first run. No gap was met.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every square of every side, its cells added one by one, and
the longest side of any whose sum is at most the threshold. 2000 matrices
up to 8 by 8 in four kinds, 500 each: values up to 9, up to 100, mostly 0
with a few up to 50, and all one value. The threshold is drawn up to the
matrix's whole sum, so that the answer lands anywhere from 0 to the
shorter side. Every matrix, threshold and raise is drawn before any arm
answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the matrix transposed: the same answer |
| P3 | the matrix turned half round: the same answer |
| P4 | every cell and the threshold doubled: the same answer |
| P5 | the threshold raised: an answer at least as long |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 matrices: checksum 976791648,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run` and
`karac __mir-llvm-run`. Python gives the same checksum.

## Mutation testing

Ten edits to the differential, two to each arm, each run under both
`karac __mir-llvm-run` and `karac __mir-run`. Every one is killed, fails
the same way under both backends and not by a crash, and no two fail the
same checks, so all ten are kept.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: no square that reaches the top row | P1 584, P2 1088, P3 117, P6 2336 |
| M2 | ★: a sum equal to the threshold refused | P1 163, P6 652 |
| M3 | binary: a failed side taken two off | P1 175, P6 175 |
| M4 | binary: the bottom row of positions never tried | P1 595, P2 1069, P3 117, P6 595 |
| M5 | every: a sum equal to the threshold stops the growth | P1 163, P6 163 |
| M6 | every: no square that reaches the last column | P1 666, P2 1069, P3 122, P6 666 |
| M7 | sliding: the window takes off the wrong column | P1 142, P2 236, P3 196, P6 142 |
| M8 | sliding: the row leaving the band never taken off | P1 179, P2 295, P3 272, P6 179 |
| M9 | solution: the corner not taken off the prefix sum | P1 856, P3 361, P6 856 |
| M10 | solution: the search started from a side of 1 | P1 93, P6 93 |

P1 and P6 kill all ten, P3 six and P2 five; P4 and P5 kill none. The
edits that leave out an edge of the matrix (M1, M4, M6) or mishandle a
moving sum (M7, M8, M9) give a different answer once the matrix is turned
or transposed, and P2 and P3 see that. The rest go wrong the same way on
any matrix, and every edit here is blind to scale and keeps a higher
threshold at least as good, so doubling everything (P4) or raising the
threshold (P5) never shows them: those two properties hold for every arm
and catch nothing on their own.

## Benchmarks

The bench builds 20 matrices of 300 by 300, the constraints' largest,
with values up to 100, once from its own generator, then makes 100
passes; each sets one cell of every matrix and its threshold from the
checksum so far, so no answer carries over, answers it with the ★ arm and
folds the side plus the pass into the checksum. The prefix table is a
fresh zeroed table of rows in every language, as the ★ arm builds one per
call: `Vec.filled` in Kāra, `vec!` in Rust, `make` in Go, lists in Python
and a `calloc` per row in C. Every implementation prints `100 passes over
20 matrices of 300 by 300: checksum 208352724`.

BENCHTAB
