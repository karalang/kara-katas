# 1269. Number of Ways to Stay in the Same Place After Some Steps

You have a pointer at index `0` in an array of size `arrLen`. At each
step, you can move 1 position to the left, 1 position to the right in the
array, or stay in the same place (the pointer should not be placed
outside the array at any time).

Given two integers `steps` and `arrLen`, return the number of ways such
that your pointer is still at index `0` after exactly `steps` steps. Since
the answer may be too large, return it modulo `10^9 + 7`.

```
steps = 3, arrLen = 2   ->  4
steps = 2, arrLen = 4   ->  2
steps = 4, arrLen = 2   ->  8
```

**Constraints:** `1 <= steps <= 500`; `1 <= arrLen <= 10^6`.

The arms are `fn num_ways(steps: i64, arr_len: i64) -> i64`.

## Approaches

| file | mechanism |
|---|---|
| `num_ways.kara` ★ | by rows: the ways to stand on each cell after each step, a row at a time; a pointer more than half the steps from home cannot come back, so only the first `steps / 2 + 1` cells are kept. O(steps * min(steps, arrLen)) |
| `num_ways_memo.kara` | by memoised recursion: the ways home from a cell with some steps left are the ways after each of the three moves, a cell farther than the steps left a dead end, the memo a table by steps left and cell |
| `num_ways_fold.kara` | by folding: the steps folded over the row of ways, each new row built by a `map` over the cells |
| `num_ways_matrix.kara` | by matrix powers: a step is a tridiagonal matrix of ones over the reachable cells, and the answer the top-left entry of its `steps`-th power, by repeated squaring. O(w^3 log steps) |
| `num_ways_map.kara` | by a walker that remembers: a struct holding the array's length and a `Map` from (cell, steps left) to the ways home, its `mut ref self` method recursing on the three moves |
| `num_ways_solution.kara` | a Rust solution as LeetCode's Rust users write it (`i32` in and out, a `const MOD` in the body, `vec!` rows shifted by a cell so both ends read a zero, `std::cmp::min`, `..=`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's three examples and a fourth
(`4 2 8 127784505`); 2000 random cases of 1 to 100 steps, in an array of 1
to 60 cells or of a million (`2000 random cases: checksum 530443588`);
and the constraints' top, 500 steps in a million cells, in one, two and
three, and 430 steps in 148,488 (`374847123 1 695241507 937512805
525833932`). `num_ways.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac run` and
`karac build`, and under the AddressSanitizer build.

The Mend loop: the ★, memo, fold and matrix arms checked clean as first
written. The map arm's method was first written with Rust's `mut self`;
the check names the receiver Kāra writes, `mut ref self`, and `karac fix`
made the edit. The solution arm takes one round of 10 fixes by `karac
fix`'s count: `std::cmp::min` to `min`, `vec![0i64; n]` to `Vec.filled(n,
0)`, `as usize` to `as i64`, `struct Solution;` to `struct Solution {}`,
`::` to `.`, and the wrapper's `as i64`, a lossless widening, removed.
Rust's `1_000_000_007`, the `const` inside the body, `..=` and the `as
i32` on the way out all stay as they are. No gap was met.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every sequence of moves, each left, right or stay, counted
when the pointer never leaves the array and ends at index 0, by
enumerating all `3^steps` of them. 2000 random cases of 1 to 10 steps in
1 to 8 cells, and with each a longer walk of 1 to 60 steps.

| | property |
|---|---|
| P1 | the statement read literally: all `3^steps` sequences enumerated |
| P2 | a cell more is never fewer ways |
| P3 | in one cell, only staying: one way |
| P4 | the longer walk in a million cells, and in any number past half its steps, has the same ways |
| P5 | the longer walk with room enough is a Motzkin path: its ways are the Motzkin number, by its own recurrence |
| P6 | the ★ arm's answer |

All 72,000 checks pass on every arm: `2000 cases: checksum 693573530,
72000 checks over 6 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python gives the same
checksum.

## Mutation testing

Twelve edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: the last cell but one never takes the ways from its right | P1 1585, P5 1962, P6 7925 |
| S2 | ★: one step short (`1..steps`) | P1 1585, P5 1962, P6 7925 |
| M1 | memo: staying recursed as a second move right | P1 1828, P3 2000, P5 1965, P6 1828 |
| M2 | memo: a move left spends two steps | P1 1585, P5 1962, P6 1585 |
| F1 | fold: staying dropped from each new row | P1 2000, P3 2000, P5 2000, P6 2000 |
| F2 | fold: the walk starts on cell 1 as well as home | P1 1585, P5 1962, P6 1585 |
| X1 | matrix: the diagonal dropped, so no step stays | P1 2000, P3 2000, P5 2000, P6 2000 |
| X2 | matrix: the power squared by the step matrix, not by itself | P1 1386, P5 1842, P6 1386 |
| W1 | map: staying dropped from the three moves | P1 2000, P3 2000, P5 2000, P6 2000 |
| W2 | map: the pointer allowed one cell past the end (`>` for `>=`) | P1 625, P3 1807, P6 625 |
| O1 | solution: the last kept cell never updated (`1..max_pos`) | P1 2000, P3 2000, P5 2000, P6 2000 |
| O2 | solution: the row not capped at the array's length | P1 625, P3 1807, P6 625 |

All twelve are caught by P1, the statement read literally. The 415
cases of a single step or a single cell pass every edit that only
miscounts a longer walk in a wider array, which is why so many rows
stop at 1585. P3, one cell, sees every
edit that lets the pointer move when it cannot: a dropped stay, a
stay turned into a move, a cell past the end. W2 and O2 are the same
mistake made two ways, a pointer let onto the cell past the array, and
fail on exactly the same cases. P2, a cell more is never fewer ways,
and P4 catch nothing here: every edit keeps the answer's growth in the
array's length. S1 and S2 break the ★ arm itself, so the checksum moves
(`885077060` and `346087311`) and P6, which compares every arm with the
★ one, fails on all five others. W2 replaced a first W2 that swapped
the memo key's two parts, which ran for over an hour without
finishing: the swapped key misses on almost every lookup, and the
walk's recursion is exponential without the memo. M2 replaced a first
M2 that hit the interpreter's step limit.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (the ways to stand on each of the first `steps / 2 + 1` cells, a new
row per step) on 1000 random cases of 1 to 500 steps in 1 to 400 cells
or a million, drawn once, 20 rounds; every answer folded into a
checksum. Every program prints `20 rounds of 1000 cases: checksum
995433448`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 1.072 to 1.200 s | 1.128 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.093 to 1.179 s | 1.128 s |
| Rust (`rustc -O`) | 1.016 to 1.138 s | 1.054 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.171 to 1.315 s | 1.201 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 1.158 to 1.358 s | 1.242 s |
| C (`clang -O3`) | 0.981 to 1.147 s | 1.069 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.865 to 1.044 s | 0.921 s |
| Go | 2.794 to 3.111 s | 2.853 s |
| Python | 97.49 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra is about 6% ahead of Rust with overflow checks on (1.128 s
against 1.201 s), and the two ranges overlap. C is about 5% ahead of
Kāra (1.069 s against 1.128 s); Go takes about 2.5x Kāra's time. Python
takes about 86x Kāra's time. No profile was taken.
