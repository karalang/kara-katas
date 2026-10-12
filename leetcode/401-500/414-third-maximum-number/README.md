# 414. Third Maximum Number

Given an integer array `nums`, return the third largest distinct number
in it. If there is no third largest distinct number, return the largest.

```
nums = [3,2,1]    -> 1
nums = [1,2]      -> 2   (no third, so the largest)
nums = [2,2,3,1]  -> 1   (the two 2s count as one value)
```

**Constraints:** `1 <= nums.length <= 10^4`; `-2^31 <= nums[i] <= 2^31 - 1`.

## Approaches

| file | mechanism | time | space |
|---|---|---|---|
| `third_max.kara` ★ | three slots: keep the three largest distinct values seen, largest first, each an `Option`; a value already held is skipped, a larger one takes its slot and pushes the smaller ones down | O(n) | O(1) |
| `third_max_set.kara` | a `SortedSet` that drops its smallest whenever it holds four; at the end its smallest is the answer if it holds three, else its largest | O(n) | O(1) |
| `third_max_sort.kara` | sort a copy, then walk down from the largest counting each new distinct value until the third | O(n log n) | O(n) |
| `third_max_heap.kara` | a largest-first `PriorityQueue` built from the numbers, popped in falling order with repeats skipped, until the third distinct value | O(n + k log n) | O(n) |
| `differential.kara` | the four arms on 3,000 random arrays, five properties, one of them a brute force over every pair | — | — |

Every arm prints the same 12 lines: the three LeetCode examples, eight
edge cases (one number, all equal, two distinct with a repeat, three
distinct each twice, a falling run, all negative, the two limits with
0, the lower limit twice with another value twice), and for 2,000
random arrays of 1 to 40 numbers drawn from a range of 1 to 20 values,
so that repeats are common, the total of the answers and a checksum.
`third_max.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms. Each of 3,000 random
cases makes an array of 1 to 30 numbers drawn from a range of 1 to 12
values around a random centre:

| | property |
|---|---|
| P1 | the answer is the value with exactly two larger distinct values, found by looking at every pair, or the largest if there is none |
| P2 | the array reversed, or rotated by a random amount, gives the same answer |
| P3 | adding a constant to every number adds it to the answer, and tripling every number triples the answer |
| P4 | every number written twice gives the same answer |
| P5 | on `d` distinct consecutive values from `c`, in a scrambled order with repeats, the answer is `c + d - 3` when `d >= 3`, else `c + d - 1` |

It prints `3000 cases, 4 arms, 60000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, each run under `karac __mir-run`.
All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | slots: a repeat of the second value is not skipped | P1 1630, P2 423, P4 1023, P5 1427 |
| M2 | slots: a new largest loses the old second | P1 320, P2 765, P4 320, P5 356 |
| M3 | set: the set keeps four values | P1 1922, P5 1494 |
| M4 | set: the largest is dropped, not the smallest | P1 1922, P5 1494 |
| M5 | sort: the second distinct value is returned | P1 2653, P5 2504 |
| M6 | sort: with fewer than three, the smallest is returned | P1 357, P5 505 |
| M7 | heap: each value is compared with the largest, not the last | P1 1820, P4 833, P5 1595 |
| M8 | heap: the queue pops the smallest first | P1 2327, P5 2025 |

No mutant fails P3: every arm and mutant only compares numbers, so
a shift or a positive scale moves its wrong answer exactly as it moves
the right one. Only the two slot mutants depend on the order of the
input, and so only they fail P2. M3 and M4 fail the same checks, the
arrays with four or more distinct values, with different wrong answers:
M3 returns the largest and M4 the smallest. M1 and M7 count a repeat
as a new value, which P4's doubled arrays make more likely. Leaving
out `third == Some(x)` from the ★ arm's repeat test would be an
equivalent mutant, since a repeat of the third value never passes any
of the later tests, so it is not used.

## Verification

`third_max.kara`, `third_max_sort.kara` and `third_max_heap.kara`
print the same output as `third_max.py` on every backend:
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`,
`karac run --interp`, LLJIT, `karac build` and `KARAC_AUTO_PAR=1 karac
build`. `third_max_set.kara` matches under `karac __mir-run` and
`karac __mir-llvm-run`. `karac check` passes on every file. The
differential prints `60000 checks, 0 failures` under `karac __mir-run`
and `karac __mir-llvm-run`.

The frozen legacy typechecker refuses the set arm and the differential:
it types `SortedSet.min()` and `max()` as `Option[i64]` where the
library gives `Option[ref i64]`, and so refuses the `*` in
`*top.min().unwrap()`. That stops `karac run --interp`, LLJIT,
`karac build` and `KARAC_AUTO_PAR=1 karac build` on both. Not filed.

## Benchmarks

The bench program uses the ★ arm on one array of 10,000 numbers (the
problem's limit) spread across the `i32` range. Each of 50,000 rounds
replaces one number with a fresh random one and finds the third maximum
again, so no compiler can hoist the search out of the loop; it folds
the answers into a total and a checksum. Every implementation prints
`50000 rounds on 10000 numbers: total 107318057620496, checksum
811171744`; a 100-round cut of the Kāra program under `karac __mir-run`
prints the same as the C program cut the same way. Spot timings on a
shared 4-core container, two or three runs each (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| Rust (`rustc -O -C overflow-checks=on`) | 0.67 to 0.73 s |
| Rust (`rustc -O`) | 0.69 to 1.01 s |
| Kāra (legacy `karac build`) | 1.41 to 1.60 s |
| C (`clang -O3`) | 1.42 to 1.55 s |
| Go | 1.66 to 1.74 s |
| Python | 45 s |

C and Go keep a flag beside each slot, where Rust and Kāra use an
`Option`; why the `Option` programs ran as fast as or faster than C has
not been looked into. The Kāra program also prints the same line under
`karac __mir-llvm-run` in 6.4 s, compile included; that JITs the
MIR's IR without optimization passes, so it is not a benchmark. The
`karac build` time is the frozen legacy backend.

## Compiler findings

No new findings. `distinct` is a reserved word in Kāra, so the sort and
heap arms count with `found`.
