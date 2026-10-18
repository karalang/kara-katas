# 704. Binary Search

Given an array of integers `nums` which is sorted in ascending order,
and an integer `target`, write a function to search `target` in `nums`.
If `target` exists, then return its index. Otherwise, return -1. You
must write an algorithm with O(log n) runtime complexity.

```
nums = [-1,0,3,5,9,12], target = 9  ->  4
nums = [-1,0,3,5,9,12], target = 2  ->  -1
```

**Constraints:** 1 <= `nums.length` <= 10^4; -10^4 < `nums[i]`, `target`
< 10^4; all the integers in `nums` are unique; `nums` is sorted in
ascending order.

## Approaches

Every arm is `fn search(nums: Vec[i64], target: i64) -> i64`; the bare
parameter borrows the array.

| file | mechanism |
|---|---|
| `binary_search.kara` ★ | a closed range [lo, hi] that must hold the target if anything does, halved at its middle until the middle is the target or the range is empty |
| `binary_search_lower.kara` | the first index whose value is not below the target, found by narrowing a half-open range [lo, hi) with one comparison a step and no early exit; the answer if the value there is the target |
| `binary_search_recursive.kara` | the ★ arm's halving written as a recursive function of the range still to search; O(log n) stack |
| `binary_search_stdlib.kara` | `Vec.binary_search`, which returns the index of an equal element or `None` |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 15 lines: the two LeetCode examples; the first
and last values, targets below and above them all and one between two
values; one value searched for itself, below and above it; two values,
the problem's extremes, each and between them; 10,000 values, the
problem's most, -9,999 to 9,999 in steps of 2, searched for every number
in that range; and 1,000 random arrays of 1 to 300 values, each searched
for one target, with a checksum. `binary_search.py` mirrors the ★ arm
and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition.
The definition is written apart from all four arms: look at every value
in turn, without the order, and answer the index of the one equal to
`target`. 3,000 random arrays are checked, of 1 to 40 values and one
case in ten of up to 1,000, increasing from -60 by 1 to a random 1 to
4, each searched for a target that is one of its values half of the
time.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | every value and the target 5,000 higher, the same answer |
| P3 | the values negated and reversed and the target negated, the answer counted from the other end |
| P4 | every value searched for finds its own index |

It prints `3000 arrays (2279 with the target), 4 arms, 48000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan`.

## Mutation testing

Eleven edits to the differential, two or three to each arm, each run
under `karac __mir-run`. All eleven are killed. Four more edits, E1 to
E4, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: stopping while one index is left | P1 1026, P3 1098, P4 3000 |
| M2 | ★: the upper end moved two below the middle | P1 674, P3 934, P4 2884 |
| M3 | ★: the low end returned for a match | P1 867, P3 1441, P4 2884 |
| M4 | lower: an equal value passed over too | P1 2279, P4 3000 |
| M5 | lower: any value not below the target taken as it | P1 570, P3 721 |
| M6 | lower: the low end moved two past the middle | P1 1428, P3 1066, P4 2944 |
| M7 | recursive: the upper half starting two past the middle | P1 893, P3 943, P4 2944 |
| M8 | recursive: a range of one taken as empty | P1 1026, P3 1098, P4 3000 |
| M9 | recursive: the first range ending before the last value | P1 191, P3 342, P4 3000 |
| M10 | stdlib: index 0 answered for a missing target | P1 721, P3 697 |
| M11 | stdlib: one above the target searched for | P1 2650, P3 2158, P4 3000 |
| E1 | ★: the middle written `(lo + hi) / 2` | 0 |
| E2 | lower: the middle written `lo + (hi - lo) / 2` | 0 |
| E3 | ★: an equal middle sending the search right | 0 |
| E4 | lower: the range ending before the last value | 0 |

P1 kills all eleven and P3 all but M4; P4 kills every mutant that loses
a value that is there. M4 lets the lower-bound arm pass over a value
equal to the target, so it never finds one; P3 does not see it, because
a target that is missing stays missing in the mirrored array too. M5 and
M10 only answer wrongly for a missing target, which P4 never searches
for. P2 sees none, since every arm only compares values and moving them
all keeps every comparison. E1 and E2 swap the two ways of writing the
middle, the same for indices this small. E3 sends an equal middle right,
but the ★ arm has already returned on it. E4 ends the lower-bound arm's
range before the last value: when the target is at or past the last
value the search stops there anyway, and the check after the loop is the
same.

## Verification

Every arm prints the same output as `binary_search.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`79a6c2eb9a` for both the debug build and the release build that runs
`check` and `__mir-run`, with runtime archives rebuilt after the last
`runtime/src` change.

The frozen legacy backends refuse all four arms at type checking, at
`next_random(mut seed)` inside the harness's `random_sorted`, whose
`seed` is already a `mut ref`: legacy wants the marker dropped, while on
v2 the marked forward is the spelling (kara B-2026-10-14-25). The legacy
`karac build` builds the differential, with an ownership warning, and it
prints the same line; `karac run --interp` does not finish it within
60 s. Legacy builds the bench program as it is. Legacy is frozen, so
this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm, the same in all five languages. It
builds 100 arrays of 10,000 increasing values from -9,999 once, each
1 or 2 above the one before; then in each of 5 rounds it searches every
array for every number from -9,999 to 9,999 and folds the indices into a
checksum. Every implementation prints `5 rounds of 100 arrays of
10000: 5000000 found, checksum 269262680`, the Kāra program under `karac
__mir-run` included (in 49 s).

Every implementation keeps the arrays as a vector of vectors, or C as
100 `malloc`'d blocks, and searches through a function given the array
and the target. Spot timings on a shared 4-core container, eight runs of
each compiled program, five of them interleaved, and two of Python
(`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.42 to 0.45 s |
| Rust (`rustc -O`) | 0.41 to 0.46 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.44 to 0.50 s |
| Go | 0.52 to 0.56 s |
| Python | 12.3 to 12.6 s |
| Kāra (`karac build --mir`) | 0.53 to 0.57 s |
| Kāra, legacy (`karac build`) | 0.51 to 0.55 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the legacy `karac build` builds the same file, and
its row is above. That edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 2.6 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

So the v2 build is level with legacy and Go here, about 15% behind Rust
with overflow checks and about 25% behind C and plain Rust. The
comparison with C and Rust waits until after M4.

## Compiler findings

None. `karac check` passed all four arms, the harness, the differential
and the bench program as first written, and every surface agreed.
