# 1272. Remove Interval

A set of real numbers can be represented as the union of several
disjoint intervals, where each interval is in the form `[a, b)`. A real
number `x` is in the set if one of its intervals `[a, b)` contains `x`
(i.e. `a <= x < b`).

You are given a sorted list of disjoint intervals `intervals`
representing a set of real numbers as described above, where
`intervals[i] = [ai, bi]` represents the interval `[ai, bi)`. You are
also given another interval `toBeRemoved`.

Return the set of real numbers with the interval `toBeRemoved` removed
from `intervals`. In other words, return the set of real numbers such
that every `x` in the set is in `intervals` but not in `toBeRemoved`.
Your answer should be a sorted list of disjoint intervals as described
above.

```
intervals = [[0,2],[3,4],[5,7]], toBeRemoved = [1,6]                     ->  [[0,1],[6,7]]
intervals = [[0,5]], toBeRemoved = [2,3]                                 ->  [[0,2],[3,5]]
intervals = [[-5,-4],[-3,-2],[1,2],[3,5],[8,9]], toBeRemoved = [-1,4]    ->  [[-5,-4],[-3,-2],[4,5],[8,9]]
```

**Constraints:** `1 <= intervals.length <= 10^4`; `-10^9 <= ai < bi <=
10^9`.

The arms are `fn remove_interval(intervals: Vec[Vec[i64]],
to_be_removed: Vec[i64]) -> Vec[Vec[i64]]`.

## Approaches

| file | mechanism |
|---|---|
| `remove_interval.kara` ★ | by one pass: an interval the cut misses kept whole, and one it meets keeping its part before the cut and its part after, either possibly empty. O(n) |
| `remove_interval_flat.kara` | by `flat_map`: each interval mapped to its two pieces clipped to the cut from either side, those not empty kept, and the pieces flattened in order |
| `remove_interval_binary.kara` | by binary search: two `partition_point`s find the first interval ending after the cut starts and the first starting at or after it ends; the intervals before the one and from the other are copied by `to_vec` and `extend_from_slice`, and only the first and last met are clipped. O(log n + the answer) |
| `remove_interval_tree.kara` | in a `SortedMap`: the intervals as a map from start to end; those the cut meets found by `range` and a filter, taken out, and their ends outside the cut put back. O(n log n) |
| `remove_interval_retain.kara` | by `retain`: the outside parts of the intervals the cut meets saved, those intervals dropped from a copy by `retain` with a captured closure, the parts appended, and `sort_by_key` on the start. O(n log n) |
| `remove_interval_solution.kara` | a Rust solution as LeetCode's Rust users write it (`Vec<Vec<i32>>`, `for iv in intervals`, `vec![..]` pushes), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, five more properties |

Every arm prints the same 5 lines: LeetCode's three examples; 3000 random
cases of 1 to 30 intervals from -100 (`3000 random cases: 42273
intervals kept, checksum 108070733`); and the constraints' top, 10^4
intervals from -10^9 cut through the middle and past both ends (`7007 and
0 intervals kept, checksum 955867888`). `remove_interval.py` mirrors the
★ arm, and its output is byte-identical. Every arm gives the same output
under `karac run` and `karac build`, and under the AddressSanitizer
build.

The Mend loop: the five arms written in Kāra checked clean as first
written. The solution arm takes one round of 26 fixes by `karac fix`'s
count: `Vec<..>` to brackets, `vec![]` to `Vec.new()` and `vec![s, e]` to
`[s, e]`, `||` to `or`, the closures' `|&x|` to `|x|`, `struct Solution;`
to `struct Solution {}`, and `::` to `.`. Rust's `for iv in intervals`
over the parameter stays: the loop reads the borrowed `Vec`. No gap was
met.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally on whole numbers: each interval walked a unit at a time, a unit
`[x, x + 1)` staying when it is not in the cut, and each run of units
that stay one interval of the answer. 2000 random cases of 1 to 12
intervals from -20, each gap 0 to 3 and each length 1 to 4 (so two
intervals can touch), cut by 1 to 20 units from -25 to 54.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | sorted, disjoint, and none empty |
| P3 | the cut made in two halves at a random point, the same answer |
| P4 | a cut that meets nothing changes nothing |
| P5 | the length lost is the cut's overlap with the intervals |
| P6 | the ★ arm's answer |

All 72,000 checks pass on every arm: `2000 cases: checksum 421816611,
72000 checks over 6 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python gives the same
checksum.

## Mutation testing

Twelve edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: the part after the cut starts a unit late | P1 178, P2 78, P3 26, P5 178, P6 890 |
| S2 | ★: an interval starting at the cut keeps an empty part before it | P1 148, P2 148, P3 298, P6 740 |
| F1 | flat: the part before the cut clipped to its end | P1 696, P3 193, P5 696, P6 696 |
| F2 | flat: empty pieces kept | P1 259, P2 259, P3 470, P6 259 |
| B1 | binary: the part after the cut taken from the first interval met | P1 138, P3 45, P5 138, P6 138 |
| B2 | binary: the intervals after the cut dropped | P1 470, P3 161, P5 470, P6 470 |
| T1 | tree: the part after the cut a unit short | P1 178, P2 78, P3 118, P5 178, P6 178 |
| T2 | tree: a met interval not taken out | P1 621, P2 171, P3 218, P5 621, P6 621 |
| R1 | retain: an interval meeting the cut by one unit treated as missing it | P1 160, P3 104, P5 160, P6 160 |
| R2 | retain: the result not sorted | P1 239, P2 239, P6 239 |
| O1 | solution: the part after the cut starts where the cut does | P1 178, P3 260, P5 178, P6 178 |
| O2 | solution: every interval treated as met | P1 1949, P2 1784, P3 1571, P4 2000, P5 1949, P6 1949 |

All twelve are caught, every one by P1, the statement read literally. P5,
the length lost, sees every edit that keeps or drops the wrong amount, and
misses only the three whose answers cover the right units in the wrong
shape: S2 and F2 keep an empty interval and R2 leaves the parts out of
order, which P2 catches. P4, a cut that meets nothing, catches only O2,
the one edit that touches intervals the cut misses.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (one pass; an interval the cut misses kept whole, one it meets
keeping its parts before and after) on 20 random lists of 10,000
intervals drawn once, each cut three ways, 40 rounds; every interval
kept folded into a checksum. Each interval is its own two-element array,
as LeetCode's `int[][]` is. Every program prints `40 rounds of 20 lists
cut 3 ways: checksum 574666609`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.469 to 0.623 s | 0.485 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.463 to 0.550 s | 0.481 s |
| Rust (`rustc -O`) | 0.652 to 0.755 s | 0.689 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.649 to 0.707 s | 0.664 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.678 to 0.736 s | 0.709 s |
| C (`clang -O3`) | 0.404 to 0.506 s | 0.433 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.403 to 0.503 s | 0.426 s |
| Go | 0.741 to 0.911 s | 0.800 s |
| Python | 5.493 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra is about 28% ahead of Rust with overflow checks on (0.481 s
against 0.664 s). C is about 10% ahead of Kāra (0.433 s against 0.481
s); Go takes about 1.7x Kāra's time. Python takes about 11x Kāra's time.
No profile was taken.
