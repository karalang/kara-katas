# 931. Minimum Falling Path Sum

Given an `n x n` array of integers `matrix`, return the minimum sum of
any falling path through `matrix`.

A falling path starts at any element in the first row and chooses the
element in the next row that is either directly below or diagonally
left/right. Specifically, the next element from position `(row, col)`
will be `(row + 1, col - 1)`, `(row + 1, col)`, or `(row + 1, col + 1)`.

```
matrix = [[2,1,3],[6,5,4],[7,8,9]]  ->  13   (1, 5, 7 or 1, 4, 8)
matrix = [[-19,57],[-40,-5]]        ->  -59  (-19, -40)
```

**Constraints:** `n == matrix.length == matrix[i].length`;
`1 <= n <= 100`; `-100 <= matrix[i][j] <= 100`.

## Approaches

| file | mechanism |
|---|---|
| `min_falling_path_sum.kara` ★ | one row of sums at a time: each row's cheapest path to every cell is the cell plus the least of the up to three sums above it, kept in a new `Vec` per row; the answer is the least of the last row. O(n²), O(n) space |
| `min_falling_path_sum_inplace.kara` | the same sums written over a copy of the matrix, the cells above each one bounded by `lo` and `hi`. O(n²), O(n²) space |
| `min_falling_path_sum_rising.kara` | the sums run from the bottom row up, each cell plus the least of the up to three cells below; the answer is the least of the top row. O(n²), O(n) space |
| `min_falling_path_sum_memo.kara` | a recursion from each top cell, the cheapest path down from a cell being the cell plus the least of the three below, memoised in a `Vec[Vec[Option[i64]]]`; n calls deep. O(n²) |
| `min_falling_path_sum_shift.kara` | each row of sums shifted one place left and one place right, the gaps padded with 1,000,000,000, and the elementwise least of the three added to the next row. O(n²), O(n) space |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and five more
(one cell, cheap opposite corners joined along both diagonals, a zigzag of
cheap cells, the cheapest path straight down an edge, and all 100s);
for 300 random matrices of 1 to 60 rows with values from -100 to 100,
the answers' sum and a checksum; and three of LeetCode's largest, 100 x
100: random, all -100 (-10,000), and a checkerboard of -100 and 100
(-10,000, down a diagonal). `min_falling_path_sum.py` mirrors the ★ arm
and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every falling path enumerated, each row's step left, straight
or right written as a digit in base 3, steps off either edge skipped,
and the least sum kept. It checks 3,200 random matrices: 3,000 of 1 to 6
rows with values from -100 to 100 against the statement, and 200 of 1 to
60 rows, each with values within a random spread of 1 to 100, against
the other properties; 291,947 cells in all.

| | property |
|---|---|
| P1 | the statement's answer, on the small matrices |
| P2 | at least `n` times the least value and at most the cheapest column taken straight down |
| P3 | the same answer for the matrix mirrored left to right |
| P4 | every value raised by `k`, from -20 to 20, raises the answer by `n·k` |
| P5 | the matrix grown by a column of 1,000,000 at the right and a last row of `w`, from -100 to 100, gives the answer plus `w` |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 matrices, 291947 cells, answers summing to -462885,
95000 checks over 5 arms: 0 failures` under `karac __mir-run` (14.5 s)
and `karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan`
with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the cell up and right never used from the next to last column | P1 699, P3 1380, P5 720, P6 720 |
| M2 | ★: only the cell straight above | P1 2134, P6 2326 |
| M3 | ★: the cell up and left taken when larger | P1 2085, P2 865, P3 2675, P6 2275 |
| M4 | inplace: nothing from the right | P1 1587, P3 2217, P6 1777 |
| M5 | inplace: the rightmost cell above never read | P1 1865, P2 424, P3 2608, P5 656, P6 2056 |
| M6 | inplace: the last column never the answer | P1 648, P2 304, P3 1314, P5 653, P6 653 |
| M7 | rising: the top row never added | P1 2514, P2 772, P4 2675, P5 448, P6 2701 |
| M8 | rising: below right never used from the first column | P1 641, P3 1380, P6 660 |
| M9 | rising: the greatest of the top row | P1 2541, P2 1824, P5 3200, P6 2736 |
| M10 | memo: below left never used from column 1 | P1 644, P3 1335, P6 667 |
| M11 | memo: the next to last row taken as the bottom | P1 2504, P2 807, P4 2675, P5 3184, P6 2697 |
| M12 | memo: column 1 never a start | P1 759, P2 268, P3 1162, P6 770 |
| M13 | shift: the gap at the left filled with 0 | P1 170, P2 9, P3 285, P4 411, P5 314, P6 171 |
| M14 | shift: the gap at the right filled with 0 | P1 170, P2 12, P3 285, P4 425, P5 454, P6 173 |
| M15 | shift: the cell straight above left out | P1 1831, P2 710, P6 2020 |

P1 and P6 kill all fifteen, P2 and P3 ten each, P5 eight and P4 four.
P3 misses the five whose mistakes are as symmetric as the mirror (M2,
M7, M9, M11 and M15). P2 misses the five that only take moves away and
always keep the step straight down (M1, M2, M4, M8 and M10), so their
answers rise but never past the cheapest straight column. P4 kills only
the mutants that count the wrong number of rows (M7 and M11) or bring in
a fixed 0 that does not move with `k` (M13 and M14); every other mistake
shifts with the values. P5 misses the seven whose error is the same on
the grown matrix as on the original (M2, M3, M4, M8, M10, M12 and M15):
the column of 1,000,000 is never on a cheapest path, and the added row
carries the same mistake down with it.

Five other edits were tried and set aside. One timed out (memo keeping
every result in column 0, which misses the memo almost every time and
turns the recursion exponential). One failed exactly the same checks as
a kept mutant (★ never using the cell up and left from column 1, as M8).
Three were sound but beyond three an arm (inplace replacing each cell
rather than adding to it, rising taking the larger of below and below
left, and shift starting its answer from 0).

## Verification

Every arm prints the same output as `min_falling_path_sum.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `9913c68556` and the runtime
archives at `5502146bed`, with no change to the runtime between them.
Under `karac __mir-run` the arms take 0.8 to 1.9 s each (memo the
slowest) and the differential 14.5 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The inplace, rising and memo arms print the same output under the frozen
legacy interpreter, the legacy JIT and both legacy builds, with and
without auto-par; the builds of the memo arm also warn that `matrix` is
moved and then used again, which v2's borrowing parameters make untrue.
Legacy refuses the ★ and shift arms, the differential and the bench
program at the first `*` on an element of a `Vec[i64]`'s `.iter()`
("unary '*' requires 'ref T', ... found 'i64'"), legacy's older rule;
under v2 the element is a reference and the `*` is required. Legacy is
frozen, so none of this is filed.

## Benchmarks

The bench program builds 100 matrices of 100 x 100 once, LeetCode's
largest, with values from -100 to 100, and in each of 150 rounds runs
the ★ arm on every matrix, each round starting from a different one.
Every implementation prints `150 rounds over 100 matrices of 100 x 100:
answers summing to -98220450, checksum 944257761`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.11 to 0.15 s | 0.13 s |
| Rust (`rustc -O`) | 0.25 to 0.30 s | 0.28 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.25 to 0.32 s | 0.27 s |
| Go | 1.23 to 1.36 s | 1.31 s |
| Python | 26.4 s | |
| Kāra (`karac build --mir`) | 0.25 to 0.33 s | 0.28 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Legacy cannot build it (see
Verification). Python's run is about 206 times C's.

v2 takes 1.02 times Rust's median time under overflow checks and 2.17
times C's. C swaps two row buffers, while Rust, Go, Kāra and Python
allocate a new row of sums each step, as the ★ arm does. Under
valgrind's cachegrind v2 runs 4.21 billion instructions and 1.09 billion
branches with 3.02 million mispredicted, Rust with overflow checks 4.52
billion, 1.02 billion and 3.41 million, and C 2.12 billion, 0.30 billion
and 1.53 million. That C's lead comes from reusing its two buffers, and
Go's 1.31 s from allocating and zeroing each row, is inferred, not
profiled.
