# 1287. Element Appearing More Than 25% In Sorted Array

Given an integer array sorted in non-decreasing order, there is exactly
one integer in it that occurs more than 25% of the time. Return that
integer.

```
arr = [1,2,2,6,6,6,6,7,10]  ->  6
arr = [1,1]                 ->  1
```

**Constraints:** `1 <= arr.length <= 10^4`, `0 <= arr[i] <= 10^5`.

The arms are `fn find_special_integer(arr: Vec[i64]) -> i64`.

## Approaches

| file | mechanism |
|---|---|
| `find_special_integer.kara` ★ | by stride: a value filling more than a quarter of a sorted array is still there n / 4 places on from its first index, and no other value is; the first i where `arr[i] == arr[i + n / 4]` gives it. O(n) |
| `find_special_integer_bounds.kara` | by binary search: such a value covers one of the positions n / 4, n / 2 and 3n / 4, so each candidate there is counted by the bounds of its run, found with `partition_point`. O(log n) |
| `find_special_integer_runs.kara` | by runs: one pass measures each run of equal values and stops at the first longer than a quarter. O(n) |
| `find_special_integer_counts.kara` | by a map of counts, as if the array were not sorted: every value counted in a `Map` by `entry().or_insert()`, then the one past a quarter found. O(n) |
| `find_special_integer_solution.kara` | a Rust solution as LeetCode's Rust users write it (`windows(n / 4 + 1)`, the first window whose ends agree, `.map(\|w\| w[0])`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's two examples, a single
number, and a winner at each end (`6 1 5 3 4`); and 1020 random problems,
1000 of up to 400 numbers and 20 of 10^4, each with one value planted
more than a quarter of the time and the rest kept at a quarter or below
(`1020 random problems: total 16421393, checksum 317940159`). The map arm
walks a `Map`, whose order is random per process, but only one value can
pass a quarter, so the order does not show. `find_special_integer.py`
mirrors the ★ arm, and its output is byte-identical. Every arm gives the
same output under `karac run` and `karac build`, and under the
AddressSanitizer build.

The Mend loop: the four arms written in Kāra checked clean as first
written. The solution arm takes one round of 6 fixes by `karac fix`'s
count: `Vec<..>` became `Vec[..]`, `::` paths took `.`, `struct
Solution;` became `struct Solution {}`, the wrapper's `as i64` was
dropped as a widening, and `.into_iter()` was put after `windows(q + 1)`,
which in Kāra is a collection of slices rather than an iterator. No gap
was met.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: for each number, how many times it occurs, counted over the
whole array, and the first whose count is more than 25% of the length.
2000 random problems of up to 60 numbers, made as the harness makes
them; each property is checked on every arm.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the answer occurs more than a quarter of the time |
| P3 | every number shifted by the same amount: the answer shifted |
| P4 | every number negated and the order reversed: the answer negated |
| P5 | one more copy of the answer put in its run: the same answer |
| P6 | the ★ arm's answer |

All 60,000 checks pass on every arm: `2000 problems: checksum 338371313,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python gives the same
checksum.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both except
C2, as explained below.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: compared half the stride on (`arr[i + n / 8]`) | P1 217, P2 217, P4 362, P6 868 |
| S2 | ★: the scan starting at index 1 | P1 33, P2 33, P3 33, P4 41, P5 33, P6 132 |
| B1 | bounds: the candidate at 3n / 4 left out | P1 42, P2 42, P3 41, P4 80, P6 42 |
| B2 | bounds: every run taken to end one past its start | P1 1908, P2 1908, P3 1906, P4 1908, P5 29, P6 1908 |
| R1 | runs: a run of exactly a quarter accepted | P1 13, P2 13, P4 21, P6 13 |
| R2 | runs: the first number of each later run skipped | P1 94, P2 94, P3 94, P4 114, P5 37, P6 94 |
| C1 | counts: a third, not a quarter, as the bar | P1 208, P2 208, P3 208, P4 208, P6 208 |
| C2 | counts: every count starting at 1 | P1 84, P2 84, P4 117, P6 84 (`__mir-run`); P1 76, P2 76, P4 115, P6 76 (`karac run`) |
| O1 | solution: a window compared with its middle, not its end | P1 217, P2 217, P4 362, P6 217 |
| O2 | solution: windows a fifth of the length, not a quarter | P1 27, P2 27, P4 44, P6 27 |

All ten are caught, every one by P1, the statement read literally, and
by P2, which asks only that the answer occur more than a quarter of the
time. P4, every number negated and the order reversed, catches all ten
too, and more often than P1 for most, since it fails when the mutant is
wrong on either the array or its mirror. P3, every
number shifted, sees only the edits that miss values by their position
(S2, B1, B2, R2) or by a bar that counts (C1). C2 gives every value one
extra count, so several can pass a quarter, and the counts arm returns
the first of them in its walk of the `Map`, whose order is random per
process: its failure counts differ between the two runs, and between any
two runs of either, which is the map's order, not a compiler fault.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (the first i where arr[i] equals arr[i + n / 4]) on 100 sorted
arrays of 10^5 numbers, built once, 1000 rounds, every answer folded
into a checksum. Every program prints `1000 rounds of 100 arrays of
100000 numbers: checksum 714924460`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 2.400 to 2.679 s | 2.543 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 2.432 to 2.812 s | 2.511 s |
| Rust (`rustc -O`) | 2.540 to 2.843 s | 2.676 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.541 to 2.754 s | 2.588 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 2.515 to 2.922 s | 2.602 s |
| C (`clang -O3`) | 2.549 to 3.243 s | 2.594 s |
| C (`clang -O3 -march=x86-64-v3`) | 2.628 to 2.832 s | 2.670 s |
| Go | 3.306 to 3.745 s | 3.528 s |
| Python | 382.14 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on runs level with Kāra (2.588 s
against 2.511 s), and the two ranges overlap. C runs level with Kāra
(2.594 s against 2.511 s); Kāra is about 29% ahead of Go (2.511 s
against 3.528 s). Python takes about 152x Kāra's time. No profile was
taken.
