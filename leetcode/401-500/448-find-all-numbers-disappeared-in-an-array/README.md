# 448. Find All Numbers Disappeared in an Array

Given an array `nums` of `n` integers where `nums[i]` is in the range
`[1, n]`, return an array of all the integers in the range `[1, n]`
that do not appear in `nums`.

```
nums = [4,3,2,7,8,2,3,1]  ->  [5,6]
nums = [1,1]              ->  [2]
```

**Constraints:** `1 <= n <= 10^5`; `1 <= nums[i] <= n`.
**Follow-up:** could you do it without extra space and in O(n) time?
The returned list does not count as extra space.

## Approaches

Every arm is `fn find_disappeared_numbers(nums: own Vec[i64]) ->
Vec[i64]`: it takes the array and may use it as scratch space, as the
follow-up asks. Every arm returns the missing numbers in ascending
order.

| file | mechanism |
|---|---|
| `find_disappeared.kara` ★ | marking by sign: each value `x` makes slot `x - 1` negative, reading slots by absolute value; the slots left positive are the missing numbers. O(n) time, no extra space |
| `find_disappeared_cyclic.kara` | cyclic sort: swap each value toward its home slot until it is home or its home holds a copy; a slot holding anything but its own number marks a missing one. O(n) time, no extra space |
| `find_disappeared_seen.kara` | the plain reference: tick each value off in a table of `n` flags. O(n) extra space, which the follow-up rules out |
| `find_disappeared_sorted.kara` | sort, then walk 1 to `n` beside the sorted values. O(n log n) |
| `differential.kara` | the four arms on 1,500 random cases, five properties |

Every arm prints the same 9 lines: the two LeetCode examples, six edge
cases (one number, nothing missing, one value repeated throughout,
the smallest missing twice over, and everything between the two ends
missing), and for 300 random arrays of 1
to 200 numbers the count of missing numbers and a checksum. Half the
random arrays draw every number at random; the other half are a
shuffle of 1 to `n` with up to a quarter of the slots overwritten by
copies of others. `find_disappeared.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random arrays of 1 to 60 numbers, built from a random set of
present values (each of 1 to `n` kept with chance 1, 1/2, 1/10 or
1/1,000), each placed at least once and the other slots filled from
the set, shuffled.

| | property |
|---|---|
| P1 | the answer is the numbers left out of the set, ascending |
| P2 | the answer is strictly ascending, within 1 to `n`, and as long as `n` minus the number of values present |
| P3 | the same numbers in another order give the same answer |
| P4 | renaming every value through a shuffle of 1 to `n` renames the answer |
| P5 | `n` copies of one value miss every other number, and a shuffle of 1 to `n` misses none |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | marks: a slot holding 1 is never marked | P1 556, P2 556, P3 562, P4 592, P5 1500 |
| M2 | marks: the last slot is never reported | P1 483, P2 483, P3 483, P4 823, P5 1377 |
| M3 | cyclic: values only move forward | P1 359, P2 359, P3 364, P4 355 |
| M4 | cyclic: a slot holding a larger value counts as home | P1 1072, P2 1072, P3 1073, P4 1053, P5 1376 |
| M5 | seen: 1 is never reported | P1 874, P2 874, P3 874, P4 858, P5 1376 |
| M6 | seen: the value `n` is never ticked off | P1 1017, P2 1017, P3 1017, P4 677, P5 1500 |
| M7 | sorted: the walk steps past at most one value per number | P1 606, P2 606, P3 606, P4 594 |
| M8 | sorted: the array is reversed instead of sorted | P1 949, P2 949, P3 953, P4 941, P5 1457 |

P5 misses M3 and M7. On a shuffle of 1 to `n`, by the time the cyclic
sort reaches slot `i` every earlier slot holds its own number, so the
value at `i` has its home at `i` or later and moving values only
forward is enough. M7 goes wrong only when a repeated value comes
before a number that is present: after `n` copies of one value nothing
present follows, and a shuffle of 1 to `n` repeats nothing. The first
M7 tried, stopping the walk one short of the end, is an equivalent
mutant: the last sorted value is the largest, so the walk never needs
to step past it.

## Verification

All four arms print the same output as `find_disappeared.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file. The differential prints
`30000 checks, 0 failures` on both. The four arms and the differential
also run clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak.

On the frozen legacy backends every arm matches under
`karac run --interp`, LLJIT and `karac build`, with and without
`KARAC_AUTO_PAR=1`. The differential prints `0 failures` under
`karac run --interp`; `karac build` stops on an index into an array
literal in its harness ("Index operator applied to non-array type").
Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm on the workload of #442: one random
array of 1,000,000 numbers, the first 300,000 of a shuffle of 1 to `n`
twice and the next 400,000 once, so 300,000 numbers are missing; built
once, then 20 times copied and searched. Every implementation prints
`20 rounds on 1000000 numbers: 6000000 missing, checksum 323785225`,
the Kāra program under `karac __mir-run` included (in 25 s).

The mirrors keep the ★ arm's structure. Spot timings on a shared
4-core container, three runs each (two for Python; `bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.32 s |
| Rust (`rustc -O`) | 0.24 to 0.26 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.35 to 0.37 s |
| Go | 0.51 to 0.67 s |
| Python | 15.0 to 15.4 s |
| Kāra (legacy `karac build`) | 0.29 to 0.32 s |

The Kāra program prints the same line under `karac __mir-llvm-run` in
1.3 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

## Compiler findings

No new findings.
