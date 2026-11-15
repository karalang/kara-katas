# 1582. Special Positions in a Binary Matrix

Given an `m x n` binary matrix `mat`, return the number of special
positions in `mat`.

A position `(i, j)` is called special if `mat[i][j] == 1` and all other
elements in row `i` and column `j` are `0` (rows and columns are
0-indexed).

```
mat = [[1,0,0],[0,0,1],[1,0,0]]  ->  1
mat = [[1,0,0],[0,1,0],[0,0,1]]  ->  3
```

**Constraints:** `m == mat.length`; `n == mat[i].length`;
`1 <= m, n <= 100`; `mat[i][j]` is either `0` or `1`.

## Approaches

| file | mechanism |
|---|---|
| `special.kara` ★ | the sum of each row and of each column by iterator chains, then each row's 1s whose row and column both sum to 1 counted by a `filter` over its columns. O(m n) |
| `special_rows.kara` | a row with exactly one 1 names the one column it can be special in, found by `position`; an `all` over the other rows checks that column. O(m n) |
| `special_owners.kara` | one pass gives each column an owner, the row of its only 1 so far, or `MANY` once a second 1 turns up, and counts each row's 1s; a special position is a column whose owner row holds one 1. O(m n) |
| `special_solution.kara` | LeetCode's Rust template (index loops filling `vec![0; m]` and `vec![0; n]` counts, then a second pass), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and four more
(`[[1]]`, `[[0]]`, a row of two 1s, and a 4 x 4 with one row of two),
then the special positions and a checksum for 3000 random matrices of up
to 5 x 5, 300 of up to 100 x 100 and 30 more of up to 100 x 100, each
cell 1 with a chance of one in 1 to 4, 100 and 400, drawn per matrix.
`special.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: each 1 checked against every other cell of its row and of its
column. It checks 3000 matrices of 1 to 5 rows and columns, each cell 1
with a chance of one in 1 to 4, every random choice drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the matrix transposed leaves the answer |
| P3 | the rows in reverse order leave the answer |
| P4 | each row reversed leaves the answer |
| P5 | a row of zeros added leaves the answer |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 627896441, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

The first M6 added `row.len() / row.len()` in place of 1, which is 1;
it was equivalent and was replaced.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a 0 counted where its row and column both sum to 1 | P1 711, P6 711 |
| M2 | ★: the column sums skip the first row | P1 851, P2 984, P3 673, P6 851 |
| M3 | ★: a row summing to 0 and a column to 2 still pass | P1 614, P2 848, P6 614 |
| M4 | rows: any row with a 1 is checked, its first 1 taken | P1 748, P2 1209, P4 451, P6 748 |
| M5 | rows: only the rows below are checked in the column | P1 676, P2 1208, P3 457, P6 676 |
| M6 | rows: the rows whose column is not alone counted | P1 1590, P2 1345, P6 1590 |
| M7 | owners: a column's owner is the last row with a 1 in it | P1 676, P2 1208, P3 457, P6 676 |
| M8 | owners: the owner row's count of 1s not checked | P1 1024, P2 1345, P6 1024 |
| M9 | template: the column counts never filled | P1 813, P6 813 |
| M10 | template: `a and b or c` in place of `a and b and c` | P1 1965, P2 1380, P5 1682, P6 1965 |

## Benchmarks

The bench draws 2000 matrices of 100 x 100 first, each cell 1 with a
chance of one in 100, and counts each by the ★ arm, in all five
languages. Every implementation prints `2000 matrices of 100 x 100:
special positions 27122, checksum 649417526`. Every row is its own
allocation in every language, and the C mirror mallocs the two sum
buffers on each call as the Kāra arm does.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `76e5a13ad` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.165 s |
| Rust (`rustc -O`) | 0.172 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.191 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.297 s |
| Kāra (`karac build`) | 0.299 s |
| Go | 0.347 s |
| Python | 6.0 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.224 s and 0.296 s on one run).

Kāra is 1.55x Rust under overflow checks by median, and none of it is the
answer. With the counting removed the bench takes 0.246 s against Rust's
0.129 s; with ten counts a matrix, each pass adds 0.037 s against Rust's
0.044 s, so the ★ arm itself runs at 0.85x. The gap is the drawing: the
matrices are built by `(0..100).map(|_| ..).collect()`, and a range's
`map(..).collect()` costs about 28 instructions an item in a `karac
build` binary against 4.4 for the push loop it stands for, and 30
against Rust's 13 when the closure writes the captured seed. That is
kara `B-2026-11-15-16`.

## Verification

All four arms print the same output as `special.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`76e5a13ad`.

## Writing it

The ★, rows and owners arms were written in Kāra and checked as written.

The Rust template took two rounds of `karac fix`:

1. thirteen edits: the `Vec<..>` types to `Vec[..]`, `&&` to `and`, the
   `|&x|` pattern to a plain name, and `Solution::` to `Solution.`;
2. `vec![0; m]` and `vec![0; n]` to `Vec.filled(m, 0)` and
   `Vec.filled(n, 0)`, and the wrapper's `as i64` dropped.

It then checks and agrees with no hand edit.
