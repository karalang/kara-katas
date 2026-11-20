# 1289. Minimum Falling Path Sum II

Given an `n x n` integer matrix `grid`, return the minimum sum of a falling
path with non-zero shifts: a choice of exactly one element from each row
such that no two elements chosen in adjacent rows are in the same column.

```
grid = [[1,2,3],[4,5,6],[7,8,9]]  ->  13      1 + 5 + 7
grid = [[7]]                      ->  7
```

**Constraints:** `1 <= n <= 200`, `-99 <= grid[i][j] <= 99`.

The arms are `fn min_falling_path_sum(grid: Vec[Vec[i64]]) -> i64`.

## Approaches

| file | mechanism |
|---|---|
| `min_falling_path_sum.kara` ★ | by keeping only the row above's two smallest path sums and the column of the smallest: a cell continues from the smallest unless that one ends in its own column, and then from the second. O(n^2) |
| `min_falling_path_sum_cubic.kara` | the plain dynamic programme: each cell's best sum is its value plus the least of the row above in every other column. O(n^3) |
| `min_falling_path_sum_sides.kara` | by prefix and suffix minima: the least of the row above outside column j is the smaller of the running minimum to its left and the one to its right, each built once per row. O(n^2) |
| `min_falling_path_sum_memo.kara` | by memoised recursion from the top: the best sum from (row, col) down is the cell plus the best from any other column of the next row, each answer kept in a `Map` keyed by the (row, col) tuple. O(n^3) |
| `min_falling_path_sum_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `dp` row cloned from the grid's first, a fresh `vec![i32::MAX; n]` per row filled by a triple loop, `*dp.iter().min().unwrap()`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's two examples, a grid of
ties, and one where every row's smallest value repeats (`13 7 2 -15`);
then 303 random grids, 300 up to 30 by 30 and 3 of 200 by 200, values
from -99 to 99 (`303 random grids: total -477505, checksum 557021457`).
`min_falling_path_sum.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac run` and
`karac build`, and under the AddressSanitizer build.

The Mend loop: the ★, cubic and memo arms checked clean as first
written. The sides arm wrote Rust's `.iter().copied()`, which Kāra spells
`.cloned()` for any `Clone` item: `E0236` said so and `karac fix` made the
change (1 fix). The solution arm takes one round of 8 fixes by `karac
fix`'s count: `Vec<..>` became `Vec[..]`, `vec![i32::MAX; n]` became
`Vec.filled(n, i32.MAX)`, `::` paths took `.`, `struct Solution;` became
`struct Solution {}`, and the wrapper's `as i64` was dropped as a
widening. No gap was met.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every way to choose one column in each row, no two
neighbouring rows in the same column, each summed, and the least. 2000
random grids up to 5 by 5; each property is checked on every arm.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | a number c added to every cell: the answer plus n times c |
| P3 | the columns permuted, the same way in every row: the same answer |
| P4 | the rows in reverse order: the same answer |
| P5 | a number c added to one row: the answer plus c |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 grids: checksum 232912153,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python gives the same
checksum.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: the old smallest not moved to second place when a new smallest comes | traps: `integer overflow` adding the second smallest |
| S2 | ★: every cell continues from the smallest, its own column or not | P1 876, P6 3504 |
| C1 | cubic: the cell's own column counted in the least of the row above | P1 876, P6 876 |
| C2 | cubic: the last column of the row above never looked at | traps: `integer overflow` adding the least |
| D1 | sides: the right-hand minimum taken from column j on, not j + 1 | P1 876, P6 876 |
| D2 | sides: the left-hand minimum not running, only the column before | P1 730, P3 855, P4 818, P6 730 |
| M1 | memo: from the top row, the same column allowed below | P1 515, P4 518, P6 515 |
| M2 | memo: every answer kept under column 0 | P1 623, P3 757, P4 330, P6 623 |
| O1 | solution: the row above's column added, not the cell's own | P1 1578, P4 1162, P6 1578 |
| O2 | solution: the second row skipped | P1 1586, P2 1520, P4 1184, P5 499, P6 1586 |

Eight are caught by P1, the statement read literally, and the other two
stop the program. S1 leaves the second smallest at `i64.MAX` whenever
the smallest changed hands, and C2, on a grid of two columns, leaves
column 0 nothing to continue from but `i64.MAX`; either sum then
overflows, and the overflow check stops the run on the first such grid.
S2, C1 and D1 are one mistake in three arms, a cell allowed to continue
from its own column, and fail on the same 876 grids, those where the
best path without the rule falls straight down somewhere. P2, a number
added to every cell, sees only O2, which skips a row and so adds the
number once too few; P5, a number added to one row, sees O2 when that
row is the one skipped. P3, the columns permuted, catches the edits
that depend on where a column sits (D2, the minimum to the left; M2,
everything stored under column 0). P4, the rows reversed, catches every
edit but the three about the own column: a path that may fall straight
down is still such a path read from the bottom up, so the wrong answer
is the same both ways.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (the row above's two smallest path sums) on 100 grids of 200 by 200,
built once, 300 rounds, every answer folded into a checksum. Every
program prints `300 rounds of 100 grids of 200 by 200: checksum
560540335`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 1.665 to 2.358 s | 1.762 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.705 to 2.109 s | 1.808 s |
| Rust (`rustc -O`) | 1.654 to 2.307 s | 1.788 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.702 to 2.600 s | 1.906 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 1.696 to 2.679 s | 1.881 s |
| C (`clang -O3`) | 1.626 to 2.086 s | 1.704 s |
| C (`clang -O3 -march=x86-64-v3`) | 1.562 to 1.875 s | 1.668 s |
| Go | 1.909 to 2.657 s | 2.031 s |
| Python | 92.54 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra is about 5% ahead of Rust with overflow checks on (1.808 s
against 1.906 s), and the two ranges overlap. C is about 6% ahead of
Kāra (1.704 s against 1.808 s); Kāra is about 11% ahead of Go (1.808 s
against 2.031 s). Python takes about 51x Kāra's time. No profile was
taken.
