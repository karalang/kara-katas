# 1504. Count Submatrices With All Ones

Given an `m x n` binary matrix `mat`, return the number of submatrices
(rectangles of adjacent rows and columns) whose cells are all ones.

```
mat = [[1,0,1],[1,1,0],[1,1,0]]          ->  13
mat = [[0,1,1,0],[0,1,1,1],[1,1,1,0]]    ->  24
```

**Constraints:** `1 <= m, n <= 150`; every cell is 0 or 1.

## Approaches

| file | mechanism |
|---|---|
| `submat.kara` ★ | row by row, each column's height of ones ending at that row; the rectangles with bottom-right corner `(i, j)` are those ending at the nearest shorter column `k` to its left plus `heights[j] * (j - k)` new ones, `k` from a stack of increasing heights. O(m n) |
| `submat_left.kara` | the same heights, and for each cell a walk left keeping the least height, adding it until it is 0. O(m n^2) |
| `submat_rows.kara` | by row bands: for each top row, extend the band down, keeping which columns are all ones over it; a run of `r` such columns adds `r` rectangles at its right end. O(m^2 n) |
| `submat_iter.kara` | with iterators: the heights are a `scan` over the rows, and each cell's count is a second `scan` over the heights to its left read backwards (`rev`), keeping the least, cut by `take_while` at 0 and `sum`med |
| `submat_solution.kara` | LeetCode's Rust template (`vec![0; n]`, `for row in &mat`, `(0..=j).rev()`), the walk-left shape, carried by `karac fix` (11 edits, then 2) to Kāra that checks once two `i32`s are written by hand (B-2026-11-07-57) |
| `differential.kara` | all five arms against the statement read literally, six properties |

Every arm prints the same 11 lines: the counts for LeetCode's two
examples and six more, then the sum and a checksum of the counts for 2000
matrices of up to 6 x 6, 100 of up to 40 x 40, and 3 of up to 150 x 150,
each with its share of ones drawn per matrix. `submat.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every rectangle, checked cell by cell. It checks 2000 problems
of up to 5 x 5. Every random choice of a problem (the matrix, a cell to
set) is drawn before any arm answers.

| | property |
|---|---|
| P1 | the count is the statement read literally |
| P2 | the matrix transposed leaves the count |
| P3 | the matrix turned half round leaves the count |
| P4 | one more cell set to 1 never lowers the count |
| P5 | the count is at least the number of ones and at most `m (m + 1) / 2 * n (n + 1) / 2`, which an all-ones matrix reaches |
| P6 | each arm agrees with at least two of the other four |

The differential prints `2000 problems: checksum 128952304, 60000 checks
over 5 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Twenty-four edits to the differential, four to six to each arm, each run
under `karac __mir-run` and `karac __mir-llvm-run`. Twelve are kept. All
but one are killed and each fails the same way under both backends, one
of them by a crash; the survivor is equivalent. No two kept ones fail the
same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a column with no shorter one to its left counted `j` wide, not `j + 1` | P1 1403, P2 1344, P3 959, P5 861, P6 1403 |
| M2 | ★: the count at the shorter column `k` not carried | P1 336, P2 234, P3 430, P4 1, P6 336 |
| M3 | ★: a 0 leaving its column's height as it was | P1 990, P2 1105, P3 1022, P6 990 |
| M4 | left: the walk stopping at height 1, not 0 | P1 1677, P2 1023, P5 1182, P6 1677 |
| M5 | left: each column's own height, not the least so far | P1 336, P2 421, P3 421, P6 336 |
| M6 | left: one per column walked, not the least height | P1 981, P2 1017, P5 203, P6 981 |
| M7 | rows: bands of at most two rows | P1 554, P2 702, P5 130, P6 554 |
| M8 | rows: a broken run halved, not reset | P1 156, P2 249, P3 238, P6 156 |
| M9 | rows: a column's band read from its bottom row only | P1 1015, P2 1140, P3 1016, P6 1015 |
| M10 | iter: the heights to the left read forwards | P1 907, P2 1005, P3 962, P5 482, P6 907 |
| M11 | iter: the heights starting at 1, not 0 | P1 1379, P2 1344, P3 966, P5 371, P6 1379 |
| M12 | Rust: the walk left leaving out the cell's own column | P1 1677, P2 1017, P5 1406, P6 1677 |

P1, P2 and P6 kill all twelve, P3 eight, P5 seven, and P4 one. P2 kills
every edit because every arm reads the matrix by rows and none by columns:
an edit that miscounts wide rectangles or tall ones changes when the
matrix is transposed. P4 sees only M2, which loses the rectangles reaching
past a shorter column, so a 1 that joins two runs can lower the count.

The other twelve: the ★ arm popping the stack on `>` for `>=` survives
and is equivalent (with equal heights, carrying from the equal column
gives the same count). The walk-left arm stopping one column early
crashes under both backends, an index out of bounds. The iterator and Rust
arms' edits fall on the walk-left arm's signatures (stopping at 1, own
height, one per column) or on M1 and M7; the Rust arm's walk-left shape
is the walk-left arm's, so only one of its edits is kept.

## Rust template

The Rust arm was written as LeetCode's Rust template plus a thin `i64`
wrapper. `karac fix` carries it in two rounds (11 edits, then 2) to one
error: `let mut ans = 0;` takes `i64` on the spot, and `ans` is returned
as the template's `i32`. B-2026-11-07-57 (open) tracks that a literal's
type is not fixed by `+=` or by a generic call; here both are in play, as
`Vec.filled(n, 0)` leaves the heights `i64` too. With `heights: Vec[i32]`
and `ans: i32` written by hand (each alone is not enough, measured), it
checks, prints the ★ arm's output, and is the fifth arm of the
differential. Drop both annotations when B-2026-11-07-57 lands.

## Benchmarks

The bench builds 400 matrices of 150 x 150 once, with a share of ones from
50% to 99%, and counts each by the ★ arm, in all five languages. Every
implementation prints `400 matrices of 150 x 150: sum 221336822, checksum
520319547`. Building the 9 million cells (one random draw each) is part of
every timing and is a large share of it (not measured apart).

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `83c2a5580` on LLVM 22:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.139 to 0.204 s | 0.166 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.165 to 0.184 s | 0.179 s |
| Kāra (`karac build`) | 0.164 to 0.188 s | 0.180 s |
| Rust (`rustc -O`) | 0.174 to 0.212 s | 0.187 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.174 to 0.202 s | 0.188 s |
| Go | 0.311 to 0.371 s | 0.343 s |
| Python | 4.08 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time (0.143 s) is below its real time (0.227 s).

Kāra is 0.95x Rust under overflow checks by median, inside the spread of
every native language but Go.

## Verification

Every arm prints the same output as `submat.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check` reports nothing on any of them.
Under `karac __mir-run` the arms take 0.3 to 0.7 s, but the iterator arm
2.1 s, and the differential 3.3 s.

## Writing it

The four Kāra arms were written in Kāra and checked with no diagnostic;
`karac fix` made two edits to the differential.
