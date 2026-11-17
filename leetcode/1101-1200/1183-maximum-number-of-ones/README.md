# 1183. Maximum Number of Ones

Consider a matrix `M` of `width * height` cells, each `0` or `1`, in which
every square sub-matrix of `sideLength * sideLength` cells holds at most
`maxOnes` ones. Return the largest number of ones `M` can hold.

```
width = 3, height = 3, sideLength = 2, maxOnes = 1  ->  4
    [1, 0, 1]
    [0, 0, 0]
    [1, 0, 1]
width = 3, height = 3, sideLength = 2, maxOnes = 2  ->  6
    [1, 0, 1]
    [1, 0, 1]
    [1, 0, 1]
```

**Constraints:** `1 <= width, height <= 100`, `1 <= sideLength <= width,
height`, `0 <= maxOnes <= sideLength * sideLength`.

The arms are `fn maximum_number_of_ones(width: i64, height: i64,
side_length: i64, max_ones: i64) -> i64`. The two Rust arms keep the
method LeetCode gives Rust users, over `i32`, inside `impl Solution`, and a
one-line `maximum_number_of_ones` calls it.

## Approaches

Every cell lies on one position of the `side * side` square, its row and
column taken modulo `side`, and every square of the matrix holds each
position exactly once. Putting ones on the same `max_ones` positions in
every square therefore meets the limit everywhere, and no matrix can do
better, so the answer is the `max_ones` positions with the most cells.
Position `(i, j)` has `(width - i - 1) / side + 1` columns and `(height - j
- 1) / side + 1` rows of cells.

| file | mechanism |
|---|---|
| `maximum_number_of_ones.kara` ★ | each position's cell count pushed onto a `Vec`, sorted largest first with `sort_by`, and the first `max_ones` summed with `take` and `sum`. O(side^2 log side) |
| `maximum_number_of_ones_classes.kara` | a position's column is on `width / side + 1` columns when it is among the first `width % side`, on `width / side` otherwise, and the same for rows, so the positions fall into four classes; the ones go to the classes with the most cells first. O(1) |
| `maximum_number_of_ones_heap.kara` | the counts pushed into a `PriorityQueue.max_first()` and `max_ones` of them popped. O(side^2 + max_ones log side) |
| `maximum_number_of_ones_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `vec![]` of counts, `sort_unstable_by(\|a, b\| b.cmp(a))`, `iter().take(max_ones as usize).sum()`), carried to Kāra by `karac fix` |
| `maximum_number_of_ones_chain.kara` | another Rust solution, one iterator chain (`(0..side * side).map(..)` over the positions in row order, `collect::<Vec<_>>()`, sorted ascending and summed from the back with `.iter().rev().take(..).sum::<i32>()`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's two examples; a single cell
with no one allowed and with one (`small 1: 0`, `small 2: 1`); a matrix
that every one fits in (`small 3: 14` for 7 by 2, side 2, four ones); a
matrix where the side does not divide either dimension (`small 4: 12` for
5 by 8, side 3, two ones); the constraints' extremes, side 1 with one one
(`largest 1: 10000`) and one square of side 100 with every cell a one
(`largest 2: 10000`), and 100 by 99 with side 7 (`largest 3: 4216`); and
3000 random cases over the constraints' whole range (`3000 random
matrices: checksum 463633975`). `maximum_number_of_ones.py` mirrors the ★
arm and its output is byte-identical; it also asserts that the answer
equals the statement read literally (every 0/1 matrix, every square) on
all 160 cases with at most 12 cells. Every arm gives the same output under
`karac run` and `karac build`.

The Mend loop: the ★, classes and heap arms take no fixes. The Rust arms
take one round each, and their outputs match on the first run. The
solution arm takes 7 fixes: `struct Solution;` to `struct Solution {}`,
`vec![]` to `Vec.new()`, `sort_unstable_by` to `sort_by`, the `as usize`
and `as i64` casts dropped, and `Solution::` to `Solution.`. The chain arm
takes 8: the same struct and path fixes and casts, and both turbofishes
removed, `collect::<Vec<_>>()` moving its type to the binding as
`let mut counts: Vec[i32]`.

No gaps: the kata found nothing to file.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every 0/1 matrix of the given size, its ones counted, kept when
every square holds at most `max_ones`. It runs every case with at most 12
cells (160 cases, the largest 4096 matrices each) against the literal
reading, then 400 random cases over the constraints' whole range.

| | property |
|---|---|
| P1 | the statement read literally (the 160 small cases) |
| P2 | the matrix turned on its side (`width` and `height` swapped) has the same answer |
| P3 | one more one allowed per square never lowers the answer, and `side * side` fills the matrix |
| P4 | the answer is between `max_ones` times the whole squares that fit and `max_ones` times the squares that cover |
| P5 | a matrix cut down to whole squares holds exactly `max_ones` per square |
| P6 | the ★ arm's answer |

All 14,800 checks pass on every arm: `160 small and 400 random cases:
checksum 674651016, 14800 checks over 5 arms: 0 failures`, in 23 s under
`karac __mir-run`, and the same under `karac run` and `karac build`.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both. All ten
are caught.

| # | mutation | failures by property |
|---|---|---|
| A1 | ★: counts sorted smallest first | P1 37, P6 1488 |
| A2 | ★: rows counted along the width | P1 87, P2 457, P3 76, P4 323, P5 363, P6 1824 |
| C1 | classes: the corner class sized by the width twice | P1 21, P2 327, P3 10, P4 54, P6 256 |
| C2 | classes: every class taken whole | P1 110, P4 381, P5 478, P6 478 |
| H1 | heap: one pop fewer | P1 110, P3 82, P4 155, P5 485, P6 485 |
| H2 | heap: smallest popped first | P1 37, P6 372 |
| X1 | solution: a column's cells counted from `width - i` | P1 100, P2 387, P3 82, P4 137, P5 485, P6 394 |
| X2 | solution: the largest count skipped | P1 77, P3 82, P4 72, P5 82, P6 360 |
| R1 | chain: the row read as the column | P1 3, P3 6, P6 199 |
| R2 | chain: the smallest counts summed | P1 37, P6 372 |

A mutation of the ★ arm fails P6 on every arm. Taking the smallest counts
(A1, H2, R2) fails only P1 and P6: it is still symmetric, monotone,
within the bounds, and exact when every count is equal, which is P5's
case. P2 catches the faults that treat the two dimensions differently (A2,
C1, X1). R1 counts only the positions on the square's diagonal, each
`side` times over; that goes wrong only when the best positions are ones
the diagonal misses, so it is the hardest to catch: 3 of the 160 small
cases.

## Benchmarks

`bench/` times the ★ arm against the same algorithm in C, Rust, Go and
Python: 1000 random cases over the constraints' whole range, built once,
then 100 rounds over all of them, each answer folded into a checksum.
Every program prints `100 rounds of 1000 cases: checksum 750879489`. Each
sorts the counts largest first with its standard sort: `sort_by` in Kāra
and Rust, `qsort` in C, `sort.Slice` in Go, `list.sort(reverse=True)` in
Python.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and two of Python, with karac `2a5724c2d4`
and kata 1186's two fixes, on LLVM 22:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.290 to 0.321 s | 0.294 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.282 to 0.339 s | 0.302 s |
| Rust (`rustc -O`) | 0.476 to 0.552 s | 0.497 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.503 to 0.540 s | 0.520 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.475 to 0.559 s | 0.506 s |
| C (`clang -O3`) | 1.556 to 1.797 s | 1.616 s |
| C (`clang -O3 -march=x86-64-v3`) | 1.662 to 1.810 s | 1.722 s |
| Go | 1.432 to 1.595 s | 1.522 s |
| Python | 5.19 to 5.23 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane; user time is within 12% of wall time for both Kāra
rows, so both ran on one core. Kāra takes about 0.58x the time of
overflow-checked Rust, the equal-safety comparison, 0.19x C's and 0.2x
Go's; Python takes about 17x Kāra's. The work is sorting: about 580
counts a case on average and at most 10,000, with at most four distinct
values arriving in runs, since the counts change only where a row or
column passes `width % side` or `height % side`. C's `qsort` and Go's
`sort.Slice` call their comparison through a function value on every
compare; where Kāra's lead over Rust comes from was not profiled.
