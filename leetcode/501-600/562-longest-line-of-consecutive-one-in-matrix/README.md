# 562. Longest Line of Consecutive One in Matrix

Given an `m x n` binary matrix `mat`, return the length of the longest
line of consecutive one in the matrix. The line could be horizontal,
vertical, diagonal, or anti-diagonal.

```
mat = [[0,1,1,0],[0,1,1,0],[0,0,0,1]]  ->  3
mat = [[1,1,1,1],[0,1,1,0],[0,0,0,1]]  ->  4
```

**Constraints:** `1 <= m, n <= 10^4`; `1 <= m * n <= 10^4`; `mat[i][j]`
is either `0` or `1`.

## Approaches

Every arm is `fn longest_line(mat: Vec[Vec[i64]]) -> i64`. A line is a
run of ones across a row, down a column, down and to the right, or down
and to the left.

| file | mechanism |
|---|---|
| `longest_line.kara` ★ | a one ends four lines, each one longer than the same line at the cell before it; the rows walked in order, keeping only the previous row's three downward counts in `Vec`s and the running count along the row; O(m n) |
| `longest_line_brute.kara` | from every one, each of the four directions walked until a zero or the edge; O(m n (m + n)) |
| `longest_line_starts.kara` | walks only from where a line starts, a one whose cell before it is a zero or off the matrix, so each cell is walked over once per direction; O(m n) |
| `longest_line_table.kara` | the ★ arm's counts kept for every cell, as a `Vec[Vec[(i64, i64, i64, i64)]]` read back by tuple field; O(m n) time and space |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 13 lines: eight matrices at the edges (the two
examples, one cell zero and one, one row, one column, and the longest
line on a diagonal and on an anti-diagonal), a total and checksum over
300 random matrices of 1 to 12 by 1 to 12 with ones 30 to 90 times in a
hundred, and the problem's most, 10,000 cells: all ones as 100 by
100, 1 by 10,000 and 10,000 by 1, and 100 by 100 with ones 70 times in a
hundred. `longest_line.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
the statement read literally: every straight run of cells in the four
directions, from every cell and of every length, checked cell by cell,
and the longest that is all ones. Each arm is held to the properties
below on 1,000 random matrices of 1 to 8 by 1 to 8, ones half the time
or 85 times in a hundred, in turn.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the answer is no longer than the longer side, and is 0 exactly when there are no ones |
| P3 | the matrix transposed gives the same answer |
| P4 | the matrix mirrored left to right gives the same answer |
| P5 | one cell set to one does not shorten the answer |

It prints `1000 cases, 4 arms, 20000 checks, 0 failures` under `karac
__mir-run` and `karac __mir-llvm-run`, and runs clean under `karac
__mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the anti-diagonal count read from straight above | P1 20, P4 33 |
| M2 | ★: the count along the row never reset | P1 164, P3 318 |
| M3 | brute: the anti-diagonal walked as a second diagonal | P1 20, P4 33 |
| M4 | brute: the last row never walked into | P1 459, P2 118, P3 676 |
| M5 | starts: the cell before a start looked for on the wrong side across | P1 314, P3 682 |
| M6 | starts: the walk's two steps swapped | P1 218, P4 278, P5 4 |
| M7 | table: the anti-diagonal count read from the neighbour's diagonal count | P1 33, P3 56, P4 55 |
| M8 | table: the count across read from the left neighbour's count down | P1 444, P2 143, P3 629, P4 188 |
| E1 | ★: the width read from the last row | 0 |
| E2 | brute: no check that the row is not negative | 0 |
| E3 | starts: the anti-diagonal walked up and to the right | 0 |
| E4 | table: a zero cell tested as not one | 0 |

Transposing a matrix turns rows into columns and leaves both diagonals
where they were; mirroring it swaps the two diagonals and leaves rows
and columns alone. So the two properties split the mutants by what they
get wrong. M1 and M3 both lose the anti-diagonals, the same cases in the
same numbers, and only P4 among the properties sees it: a matrix whose
longest line is anti-diagonal is answered short, its mirror image is
not. M2, M4 and M5 treat rows and columns differently, which P3 sees.
M6 swaps the steps of the walk: across becomes down and down becomes
across, which transposing undoes, and the anti-diagonal walks up, which
mirroring exposes. E1 is safe because every row has the same length;
E2 because the walk never goes up; E3 because an anti-diagonal is the
same cells walked either way.

## Verification

Every arm prints the same output as `longest_line.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. `karac check`
passes on every arm, the differential and the bench program, with no
warnings.

The frozen legacy backends: every arm prints the same output under
`karac run` and `karac build`, and under `KARAC_AUTO_PAR=1 karac build`;
the starts arm after an ownership warning that `mat` is moved into
`is_one` and used again, where under v2 the parameter borrows. Under
`karac run --interp` the ★ and table arms print it; the brute and starts
arms print the first 10 lines and are still on the 1 by 10,000 matrix
when a 60 s limit stops them. The differential prints `0 failures` under
`karac build`, with the same warning, and does not finish under `karac
run --interp` within 120 s. Legacy refuses the bench program (see
Benchmarks). Legacy is frozen, so these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 100 random matrices of
10,000 cells, the problem's most, once: 1 by 10,000, 10 by 1,000, 100 by
100, 1,000 by 10 and 10,000 by 1 in turn, with ones 50 to 95 times in a
hundred; then 100 times over every matrix is answered. Every
implementation prints `100 matrices of 10000 cells, 100 rounds: total
343700, checksum 409941977`, the Kāra program under `karac __mir-run`
included (198 s).

Every implementation allocates the three fresh rows of counts for each
row of the matrix as the Kāra arm does: `vec!` in Rust, `make` in Go,
`calloc` in C and lists in Python. The tall matrices make that
allocation a large part of the work, three tiny arrays for each of
10,000 rows. Spot timings on a shared 4-core container, three runs each
(two for Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.99 to 2.08 s |
| Rust (`rustc -O`) | 2.32 to 2.42 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.36 to 2.49 s |
| Go | 2.05 to 2.09 s |
| Python | 24.9 to 25.7 s |
| Kāra (`karac build --mir`) | 1.93 to 2.12 s |

The legacy `karac build` refuses this program: it moves `matrices[(round
* 7 + g) % count]` out of the index (E_INDEX_MOVE_NON_COPY) where
v2 borrows it. So `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`e17ae2b58d`. Under `karac __mir-llvm-run` the program prints the same
line in 5.5 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark. The Kāra row is level
with C's and Go's and a little ahead of Rust's.

## Compiler findings

None new. Nothing was filed from this kata; the legacy failures above
are not filed because legacy is frozen.
