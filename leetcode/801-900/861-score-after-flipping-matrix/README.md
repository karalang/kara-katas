# 861. Score After Flipping Matrix

You are given an `m x n` binary matrix `grid`. A move chooses any row or
column and toggles each value in it: every `0` becomes a `1` and every
`1` a `0`. Every row of the matrix is read as a binary number, and the
score is the sum of these numbers. Return the highest score possible
after making any number of moves, including none.

```
grid = [[0,0,1,1],[1,0,1,0],[1,1,0,0]]  ->  39    (0b1111 + 0b1001 + 0b1111)
grid = [[0]]                            ->  1
```

**Constraints:** `1 <= m, n <= 20`; `grid[i][j]` is `0` or `1`.

## Approaches

| file | mechanism |
|---|---|
| `matrix_score.kara` ★ | a row's first bit is worth more than all its others together, so every row ends up starting with a 1. That fixes every row's flip, and then a cell is 1 exactly when it equals the first cell of its row, so a column's ones are counted with no flips made. Each column goes on its better side and is worth the larger of its ones and zeros; the columns are read off as one binary number, most significant first. O(mn) time, O(1) space |
| `matrix_score_flip.kara` | the flips made on a copy of the grid: each row that starts with a 0, then each column with fewer ones than zeros, then the rows read and added. O(mn) time and space |
| `matrix_score_bits.kara` | each row packed into one integer, first cell most significant; a row flip is an exclusive or with n ones. Bit k of the rows is counted for each column. O(mn) time, O(m) space |
| `matrix_score_climb.kara` | local search from the grid as given: each step works out what every row and column flip would gain and makes the best one, stopping when none gains. It cannot stop short: while a row starts with a 0, flipping it gains, and once none does the columns are independent. O(s * mn) for s steps |
| `matrix_score_iter.kara` | the ★ rule as one `fold` over the column indices, each column's ones counted with `filter` and `count` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 16 lines: LeetCode's two examples; ten more (a
single row, a single column, a tied column, rows that must both flip, a
4 x 4 grid); a 20 x 20 grid of zeros and a 20 x 20 chessboard, both
20,971,500; the sum of the scores of all 682 grids of one to three rows
and one to three columns, which is 11,118; and 2,000 random grids of up
to 20 x 20, with the sum of their scores and a checksum.
`matrix_score.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the grid packed into one integer, a bit per cell, and a
breadth-first search over every grid the moves can reach from it,
keeping the best score. Its 2,000 grids are all 682 grids up to 3 x 3
and 1,318 random grids of up to four rows and twelve cells; their scores
sum to 28,147.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | the answer is at least the grid's own score, and at most m rows of n ones |
| P3 | one row or column flipped first changes nothing (each of them in turn) |
| P4 | the rows in the reverse order change nothing |
| P5 | the answer is at least m times 2^(n-1): every row can start with a 1 |
| P6 | a copy of the first column added at the right doubles the answer and adds m |

It prints `2000 grids, scores sum to 28147, 101830 checks over 5 arms:
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

P6 was first written with a column of zeros added at the right, and all
five arms failed it on 5,965 checks: once the rows are flipped to start
with a 1, the new column holds a 1 in every flipped row, so it is worth
the larger of its counts, not m. The property was wrong, not the arms. A
copy of the first column becomes all ones under the same row flips, and
that is the property kept.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a cell counted as a one by its own value | P1 1193, P3 6662, P4 1193, P5 274, P6 1193 |
| M2 | ★: no column flipped | P1 1041, P3 5780, P4 1041, P6 1041 |
| M3 | ★: the first column left out | P1 2000, P2 1483, P3 10366, P4 2000, P5 2000, P6 2000 |
| M4 | flip: no row flipped | P1 1606, P3 8506, P4 1606, P5 1002, P6 1606 |
| M5 | flip: the columns with more ones flipped | P1 1516, P2 262, P3 8416, P4 1516, P6 2000 |
| M6 | flip: the last column never flipped | P1 715, P3 3895, P4 715 |
| M7 | bits: the last cell taken for the first | P1 1003, P2 119, P3 5944, P4 1003 |
| M8 | bits: a row flipped one bit short | P1 1193, P2 107, P3 6662, P4 1193, P5 277, P6 1193 |
| M9 | bits: the columns weighted in reverse | P1 1038, P2 131, P3 6163, P4 1038, P6 453 |
| M10 | climb: no row moved | P1 1193, P3 6662, P4 1193, P5 274, P6 1193 |
| M11 | climb: a move that gains 1 not made | P1 885, P3 4476, P4 885, P5 253, P6 107 |
| M12 | climb: one move at most | P1 1100, P3 6346, P4 1100, P5 115, P6 1268 |
| M13 | iter: a cell counted as a one by its own value | P1 1193, P3 6662, P4 1193, P5 274, P6 1193 |
| M14 | iter: the fold started at 1 | P1 2000, P2 2000, P3 10366, P4 2000, P5 2000, P6 2000 |
| M15 | iter: each column on its worse side | P1 2000, P2 1796, P3 10366, P4 2000, P5 2000, P6 2000 |

P1, P3 and P4 kill all fifteen. M1, M10 and M13 are one fault, no row
ever flipped, and fail the same cases. A first draft of M11, a column's
gain with its sign turned, never finished: the climb flipped a column
back and forth for ever, since each flip then looked like a gain. It was
replaced by one that ends.

## Verification

Every arm prints the same output as `matrix_score.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and under
`karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `43a401a57b`. Under `karac
__mir-run` the arms take under a second, the climb 4.8 s, and the
differential 4.4 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The frozen legacy backends run the ★ and `iter` arms through `karac run
--legacy --interp`, `karac run --legacy`, `karac build` and a
`KARAC_AUTO_PAR=1` build with the same output. They refuse the flip and
bits arms and the differential at a `*` on a `for` element, saying the
element is copied, where v2 yields a reference to each element, and the
climb arm at `climb_row_value(g[i])`, where legacy reads a bare parameter
as owned and so a move out of an index (`E_INDEX_MOVE_NON_COPY`), and v2
borrows it. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm, in all five languages: a random 20 x 20
grid, LeetCode's largest, built once, and 1,000,000 rounds that each flip
one cell, score the grid, and flip the cell back, so every round reads
all 400 cells. Every implementation prints `1000000 rounds on a 20 by 20
grid: scores sum to 17854976526365, checksum 313330102`, the Kāra
program under `karac __mir-run` included, in 522 s.

Spot timings on a shared 4-core container, eight interleaved runs of
each compiled program and one of Python (`bench.sh` timings need a quiet
machine):

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.16 to 0.21 s | 0.18 s |
| Rust (`rustc -O`) | 0.26 to 0.32 s | 0.28 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.44 to 0.49 s | 0.46 s |
| Go | 0.32 to 0.40 s | 0.36 s |
| Python | 14.5 s | |
| Kāra (`karac build --mir`) | 0.32 to 0.38 s | 0.34 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 860's does. The frozen legacy `karac build`
binary takes 0.29 to 0.33 s against v2's 0.32 to 0.36 s over five
interleaved runs each.

v2 takes 0.74 times Rust's median time under overflow checks, 1.2 times
Rust's without them, and 1.9 times C's. The difference is in the branch
on each cell: under valgrind's cachegrind C runs 2.50 billion
instructions with 21 million branches and 1.0 million mispredicted, so
clang has made the per-cell test branch-free; Rust without overflow
checks 5.11 billion with 825 million branches and 21 million
mispredicted; v2 4.09 billion with 1,303 million branches and 207
million mispredicted, one for about every two cells, which is a branch
on the random cell value itself (not traced further). The comparison
with C and Rust waits until after M4.
