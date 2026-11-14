# 1568. Minimum Number of Days to Disconnect Island

You are given an `m x n` binary grid `grid` where `1` represents land and
`0` represents water. An island is a maximal 4-directionally (horizontal
or vertical) connected group of `1`s. The grid is said to be connected
if we have exactly one island, otherwise it is said to be disconnected.
In one day, we are allowed to change any single land cell `(1)` into a
water cell `(0)`. Return the minimum number of days to disconnect the
grid.

```
grid = [[0,1,1,0],[0,1,1,0],[0,0,0,0]]   ->  2
grid = [[1,1]]                           ->  2
```

**Constraints:** `1 <= m, n <= 30`; `grid[i][j]` is `0` or `1`.

## Approaches

The answer is never more than 2: the topmost land cell of the island's
leftmost column has at most two land neighbours, and turning both to
water cuts it off (or leaves no land, which is not one island either).
So the question is only whether the grid is already disconnected (0) and
whether one cell can do it (1).

| file | mechanism |
|---|---|
| `days.kara` ★ | the islands counted by a walk on a stack; not exactly one needs no day, and otherwise each land cell is taken away in turn to see whether one day is enough. O((m n)^2) |
| `days_cuts.kara` | one day is enough exactly when the island is one cell or has a cut vertex, so one depth-first walk (a method on a `struct` taking `mut ref self`) counts the islands and finds cut vertices by Tarjan's low links. O(m n) |
| `days_union.kara` | the islands counted by union-find with path compression, each land cell joined to the land above it and to its left; the land cells listed once by a `flat_map` and each taken away in turn. O((m n)^2 α(m n)) |
| `days_solution.kara` | LeetCode's Rust template (`min_days(grid: Vec<Vec<i32>>) -> i32`, the ★ arm with a recursive search over `usize` indices), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 13 lines: LeetCode's two examples, then `[[1]]`,
`[[0, 0]]`, `[[1, 0, 1]]`, `[[1, 1, 1]]`, a full 2 by 2 and 3 by 3, a
bent path, and a ring; then how many need 0, 1 and 2 days and a checksum
for 3000 random grids of up to 4 by 4, 300 of up to 10 by 10 and 30 of up
to 30 by 30, each with its own share of land from 6 to 9 cells in 10.
`days.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally, which does not assume the answer is at most 2: no cell, then
every land cell, then every two, and so on, each set turned to water and
the islands counted by a recursive flood, the first count that leaves
other than one island the answer. It checks 3000 grids of 1 to 4 rows
and columns with their own share of land from 5 to 9 cells in 10, every
random choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is 0, 1 or 2, and 0 when there is no land |
| P3 | the grid transposed leaves the answer |
| P4 | every row reversed leaves the answer |
| P5 | a row of water put below and a column of water put on the right each leave the answer |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 256189584, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the walk never steps up | P1 280, P3 293, P6 280 |
| M2 | ★: a cell taken away is not put back | P1 716, P6 716 |
| M3 | ★: only no land needs no day | P1 678, P6 678 |
| M4 | cuts: a child's subtree reaching back to the cell itself does not cut it | P1 65, P3 46, P4 45, P6 65 |
| M5 | cuts: a root with one child taken for a cut vertex | P1 716, P6 716 |
| M6 | cuts: a lone cell needs two days | P1 399, P6 399 |
| M7 | union: land joined only to the land above | P1 1432, P3 708, P6 1432 |
| M8 | union: a join leaves the count of islands | P1 1793, P6 1793 |
| M9 | template: the search steps up only from row 2 on | P1 241, P3 288, P6 241 |
| M10 | template: one day when no single cell does it | P1 716, P6 716 |

## Benchmarks

The bench builds 20 grids of 30 by 30 once, all land but for a water
cell one time in 20, and makes 5 passes, each turning one cell of every
grid over and asking it by the ★ arm, in all five languages. Every count
of islands allocates its marks and its stack, but in C, where both are
static and the marks are cleared by `memset`. Every implementation prints
`5 passes over 20 grids of 30 by 30: 0 need 0 days, 70 need 1, 30 need
2, checksum 622898032`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5a1b79539` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.261 s |
| Rust (`rustc -O`) | 0.334 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.348 s |
| Kāra (`karac build`) | 0.353 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.367 s |
| Go | 0.754 s |
| Python | 21.7 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.33 s and 0.33 s on one run).

Kāra is 0.95x Rust under overflow checks by median. Not traced. C's lead
is its static marks and stack, which the other four allocate on every
count of islands, 900 times a call.

## Verification

All four arms print the same output as `days.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change. Checked at kara `5a1b79539`;
the template and the differential again at `49a607740`.

## Writing it

The ★ and cuts arms were written in Kāra and checked as written. The
union-find arm was first written with Rust's `move |c| (r, c)` inside its
`flat_map`; `karac fix` deleted the `move` in one round.

The Rust template took five rounds of `karac fix`, 15 changed lines,
then 1 added, then 8, 2 and 1 changed:

1. the `Vec<..>` types to `Vec[..]`, `&Vec<..>` and `&mut Vec<..>`
   parameters to `ref` and `mut ref`, `&grid` and `&mut seen` arguments
   to `grid` and `mut seen`, `&&` and `||` to `and` and `or`, `!seen` to
   `not seen`, the wrapper's `|&x|` to `|x|`, and `Self::` and
   `Solution::` to `Solution.`;
2. `struct Solution {}` added;
3. `grid` to `own`, since the method writes it, the inner `vec![..]` to
   `Vec.filled`, `dfs`'s `usize` indices to `i64`, `mut` added to the
   recursive calls' `seen`, and the wrapper's `as i64` dropped (an `i32`
   widens);
4. the outer `vec![..]` to `Vec.filled`, and `dfs`'s `ref` on `grid`
   dropped as redundant.

At kara `5a1b79539`, `count`'s `ref grid`, just as redundant, kept its
`ref`: the lint skipped every function whose name was read as a value
anywhere, matched by name alone, so the harness's `count` parameter
counted. Filed as B-2026-11-14-21 and fixed in `49a607740`; a fifth
round now drops that `ref` too, and the template is kept as that round
leaves it. It checks and agrees with no hand edit.
