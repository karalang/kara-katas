# 628. Maximum Product of Three Numbers

Given an integer array `nums`, find three numbers whose product is the
largest and return that product.

```
nums = [1,2,3]     ->  6
nums = [1,2,3,4]   ->  24
nums = [-1,-2,-3]  ->  -6
```

**Constraints:** 3 to 10,000 values, each from -1,000 to 1,000.

## Approaches

Every arm is `fn maximum_product(nums: Vec[i64]) -> i64`. The largest
product is either the three largest values multiplied, or the largest
value times the two smallest, which wins when those two are negative and
their product outweighs the second and third largest.

| file | mechanism |
|---|---|
| `maximum_product.kara` ★ | one pass keeping the three largest and the two smallest values seen so far; O(n) |
| `maximum_product_sorted.kara` | a sorted copy, the last three values against the first two times the last; O(n log n) |
| `maximum_product_counts.kara` | a count for each value from -1,000 to 1,000, walked down from the top for the three largest and up from the bottom for the two smallest, a value taken as often as it occurs; O(n + 2,001) |
| `maximum_product_heap.kara` | every value pushed onto a largest-first and a smallest-first `PriorityQueue`, three popped from one and two from the other; O(n log n) |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 16 lines: the three LeetCode examples; nine
more (two negatives beating the second and third largest, negative
values only, zeros, one negative with two positives, a zero beside
negatives, the extremes either way, one value repeated, and two equal
negatives among positives); a total and checksum over 300 random cases
of 3 to 50 values from -1,000 to 1,000; and the answers for
10,000 values, for 10,000 negative values, and for 10,000 values from
-10 to 10, most of them repeated. `maximum_product.py` mirrors the ★ arm
and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
the largest product over every three positions. Each of 1,000 random
cases is 3 to 8 values from -10 to 10, so that zeros, repeats and
negatives are common.

| | property |
|---|---|
| P1 | the product is the definition's |
| P2 | the values in reverse order give the same product |
| P3 | every value doubled gives eight times the product |
| P4 | a 0 added gives the product, or 0 if that is larger |
| P5 | some three of the values multiply to the product |

It prints `1000 cases (5501 values), 4 arms, 20000 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and runs clean under
`karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: only the three largest values multiplied | P1 535, P4 132 |
| M2 | ★: a new largest value pushing the old largest to third | P1 144, P2 339, P5 144 |
| M3 | sorted: the first three values multiplied instead of the first two and the last | P1 530, P4 191 |
| M4 | sorted: the second largest value used twice | P1 447, P5 447 |
| M5 | counts: the third largest value with the two smallest | P1 582, P4 181, P5 70 |
| M6 | counts: each smallest value taken one too large | P1 599, P3 582, P4 78, P5 510 |
| M7 | heap: the third largest value with the two smallest | P1 582, P4 181, P5 70 |
| M8 | heap: the two smallest taken from a second largest-first queue | P1 901, P4 132, P5 745 |
| E1 | ★: a value tied with the smallest becoming the smallest | 0 |
| E2 | sorted: the ends multiplied in the other order | 0 |
| E3 | counts: the loop test as at most two taken | 0 |
| E4 | heap: the two candidates compared the other way round | 0 |

P1 kills all eight. M5 and M7 are the same edit in two arms, the third
largest value put where the largest belongs beside the two smallest, so
they fail the same counts. P2 sees only M2, whose largest three depend
on the order the values arrive in. P3 sees only M6: doubling every value
turns its off-by-one into an off-by-two, so the product no longer scales
by eight. P4 sees all but M2 and M4. P5 sees the mutants whose product
is no three of the values at all, as with a value used twice or shifted
by one. The four survivors cannot change an answer: a tie for the
smallest swaps two equal values, multiplication and `max` do not care
about order, and a length test of at most two is the same test as below
three.

## Verification

Every arm prints the same output as `maximum_product.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes every arm, the
differential and the bench program. All at kara `ea2a2da2be` for the
debug build and `991a9861ad` for the release build that runs `check` and
`__mir-run`.

The frozen legacy backends refuse every file at type checking. They type
the items of a `Vec`'s `iter()` by value, so `*x` is an error, and they
still hold the old rule that an argument which is already a `mut ref`,
as `seed` is inside `random_values`, drops its call-site `mut` marker.
Legacy is frozen, so these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 20 inputs of 10,000 values,
the problem's most, each from -spread to spread for a random spread from
1 to 1,000, once; then 20,000 times answers one of them, picked by the
round, putting each answer into a checksum. Every implementation prints
`20 inputs, 20000 rounds: checksum 507255702`, the Kāra program under
`karac __mir-run` included (in 276 s).

Each implementation is the same one pass over a flat array of 64-bit
integers. Spot timings on a shared 4-core container, three runs each
(two for Python; `bench.sh` timings need a quiet machine), each
including making the inputs:

| | time |
|---|---|
| C (`clang -O3`) | 0.41 to 0.42 s |
| Rust (`rustc -O`) | 0.39 to 0.41 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.38 to 0.41 s |
| Go | 0.30 to 0.33 s |
| Python | 8.3 to 8.5 s |
| Kāra (`karac build --mir`) | 0.28 to 0.29 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, since the legacy `karac build` refuses the `*x`;
that edit is by hand, on top of the `scripts/new-bench.sh` output. A
copy outside the kata that reads `x` without the `*` and takes `nums` as
`ref Vec[i64]` builds under legacy and takes 0.35 to 0.42 s, so the
v2 build is ahead of legacy here. Under `karac __mir-llvm-run` the
program prints the same line in 2.3 s, compile included; that JITs the
MIR's IR without optimization passes, so it is not a benchmark.

The Kāra build is the fastest compiled row in these runs, ahead of C and
Rust by about a quarter. The program is not profiled, so why is not
established.

## Compiler findings

None. The legacy failures above are not filed because legacy is frozen.
