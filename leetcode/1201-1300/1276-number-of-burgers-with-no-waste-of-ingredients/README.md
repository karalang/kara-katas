# 1276. Number of Burgers with No Waste of Ingredients

Given two integers `tomatoSlices` and `cheeseSlices`. The ingredients of
different burgers are as follows:

- **Jumbo Burger:** `4` tomato slices and `1` cheese slice.
- **Small Burger:** `2` tomato slices and `1` cheese slice.

Return `[total_jumbo, total_small]` so that the number of remaining
`tomatoSlices` equal to `0` and the number of remaining `cheeseSlices`
equal to `0`. If it is not possible to make the remaining `tomatoSlices`
and `cheeseSlices` equal to `0` return `[]`.

```
tomatoSlices = 16, cheeseSlices = 7   ->  [1,6]
tomatoSlices = 17, cheeseSlices = 4   ->  []
tomatoSlices = 4, cheeseSlices = 17   ->  []
```

**Constraints:** `0 <= tomatoSlices, cheeseSlices <= 10^7`.

The arms are `fn num_of_burgers(tomato_slices: i64, cheese_slices: i64)
-> Vec[i64]`.

## Approaches

| file | mechanism |
|---|---|
| `num_of_burgers.kara` ★ | by algebra: `j` jumbo and `s` small burgers take 4j + 2s tomato and j + s cheese slices, so j = t / 2 - c and s = 2c - t / 2; an answer needs `t` even and both counts at least 0. O(1) |
| `num_of_burgers_search.kara` | by binary search: every cheese slice goes on a burger, so the jumbo count is from 0 to `c`; the tomato slices used, 2c + 2j, grow with it, and the count using exactly `t` is searched for with a captured closure. O(log c) |
| `num_of_burgers_cramer.kara` | by Cramer's rule: a `struct System` of a 2-by-2 linear system with a general `solve` over determinants returning `Option[(i64, i64)]`, the burgers its rows, and a `match` with a guard keeping only whole counts of at least 0 |
| `num_of_burgers_result.kara` | by `Result`: all small burgers to start, small swapped for jumbo two tomato slices at a time; each way it can fail an `Err` of an `enum Waste` naming why, carried by `?` |
| `num_of_burgers_solution.kara` | a Rust solution as LeetCode's Rust users write it (`i32` in, `Vec<i32>` out, `vec![]`, the jumbo count from the tomatoes left over by all small burgers), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's three examples, then `(0,
0)` and `(2, 1)` (`[1, 6] [] [] [0, 0] [0, 1]`); 3000 random cases, a
third made from burgers, a third a few slices off such a count, and a
third anything, half of them up to 10^7 (`3000 random cases: 1666 with
burgers, checksum 379250827`); and the constraints' top, 10^7 tomato
slices with 2,500,000, 5,000,000, 3,000,000 and 10^7 cheese slices, and
9,999,999 with 3,000,000 (`[2500000, 0] [0, 5000000] [2000000, 1000000]
[] []`). `num_of_burgers.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac run` and
`karac build`, and under the AddressSanitizer build.

The Mend loop: the four arms written in Kāra checked clean as first
written. The solution arm takes one round of 11 fixes by `karac fix`'s
count: `Vec<..>` to brackets, `vec![]` to `Vec.new()` and `vec![j, s]` to
`[j, s]`, `||` to `or`, the closure's `|&x|` to `|x|`, `struct
Solution;` to `struct Solution {}`, and `::` to `.`. No gap was met.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every count of jumbo and of small burgers the tomato slices
could make tried, and the one using every tomato and every cheese slice
the answer. 2000 random cases, a third made from up to 14 burgers of
each kind and the rest up to 80 tomato and 30 cheese slices.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the answer empty, or two counts of at least 0 using every slice |
| P3 | a jumbo burger's slices more: one more jumbo burger |
| P4 | a small burger's slices more: one more small burger |
| P5 | both counts doubled: both burger counts doubled |
| P6 | the ★ arm's answer |

P3 to P5 are checked when the arm finds burgers. All 60,000 checks pass on
every arm: `2000 cases: checksum 985543430, 60000 checks over 5 arms: 0
failures`, under `karac __mir-run`, `karac run`, `karac build` and the
AddressSanitizer build. Python gives the same checksum.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: the tomato count required to be a multiple of 4 | P1 409, P4 477, P6 1636 |
| S2 | ★: a negative small count let through | P1 201, P2 201, P6 804 |
| B1 | search: no answer without a jumbo burger | P1 67, P6 67 |
| B2 | search: the search goes one past the count it wants | P1 837, P4 49, P6 837 |
| C1 | Cramer: fractional counts truncated | P1 213, P2 213, P3 13, P4 7, P5 213, P6 213 |
| C2 | Cramer: a negative small count let through | P1 201, P2 201, P6 201 |
| R1 | result: no answer of jumbo burgers only | P1 49, P6 49 |
| R2 | result: two tomato slices short answered with -1 jumbo burgers | P1 18, P2 18, P5 18, P6 18 |
| O1 | solution: too few tomato slices let through | P1 261, P2 261, P6 261 |
| O2 | solution: no answer of jumbo burgers only | P1 49, P6 49 |

All ten are caught, every one by P1, the statement read literally. P2,
the slices used up, sees every edit that answers with a count that does
not fit, and misses the four that refuse an answer (S1, B1, R1, O2): an
empty answer always passes it, and P3 to P5 are asked only of an answer
with burgers, so those four are seen by P1 alone, apart from S1: one
more small burger takes a multiple of 4 tomato slices off it, so S1
refuses there (P4).

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (by algebra) on 100,000 random pairs of tomato and cheese slice
counts up to 10^7, a third made from burgers and a third near such a
count, drawn once; 1000 rounds, every answer folded into a checksum.
Every program prints `1000 rounds of 100000 pairs: checksum 874894270`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.591 to 0.713 s | 0.624 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.594 to 0.659 s | 0.616 s |
| Rust (`rustc -O`) | 0.574 to 0.601 s | 0.586 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.599 to 0.663 s | 0.620 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.585 to 0.625 s | 0.609 s |
| C (`clang -O3`) | 1.028 to 1.195 s | 1.062 s |
| C (`clang -O3 -march=x86-64-v3`) | 1.051 to 1.174 s | 1.085 s |
| Go | 0.657 to 0.805 s | 0.674 s |
| Python | 29.40 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on runs level with Kāra (0.620 s
against 0.616 s), and the two ranges overlap. C takes about 1.7x Kāra's
time; Kāra is about 9% ahead of Go (0.616 s against 0.674 s). Python
takes about 48x Kāra's time. No profile was taken.
