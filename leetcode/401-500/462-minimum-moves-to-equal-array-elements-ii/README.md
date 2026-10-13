# 462. Minimum Moves to Equal Array Elements II

Given an integer array `nums` of size `n`, return the minimum number of
moves required to make all array elements equal. In one move, you can
increment or decrement an element of the array by `1`. Test cases are
designed so that the answer fits in a 32-bit integer.

```
nums = [1,2,3]      ->  2    (1 -> 2, 3 -> 2)
nums = [1,10,2,9]   ->  16
```

**Constraints:** `1 <= nums.length <= 10^5`; `-10^9 <= nums[i] <= 10^9`.

## Approaches

Every arm is `fn min_moves2(nums: own Vec[i64]) -> i64`. Moving every
number to a target `t` costs the sum of `|x - t|`, and that sum is least
when `t` is a median.

| file | mechanism |
|---|---|
| `min_moves2.kara` ★ | sort, take the middle element, sum the distances to it. O(n log n) |
| `min_moves2_pairs.kara` | sort, then add up the difference of the smallest and largest, the second smallest and second largest, and so on inward: any target between a pair costs exactly its difference, and the median lies between every pair. O(n log n) |
| `min_moves2_select.kara` | quickselect: partition around the middle element into smaller, equal and larger, keep the part holding position `n / 2`, then sum the distances to it. O(n) on average |
| `min_moves2_every.kara` | the plain reference: try every number as the target (the cost has its corners only at the numbers) and keep the cheapest. O(n²) |
| `differential.kara` | the four arms on 1,500 random cases, five properties |

Every arm prints the same 9 lines: the two LeetCode examples, one
number, two numbers, all equal, the extremes of the range, an 11-number
array, one far outlier, and for 300 random arrays of 1 to 200 numbers
(within ±5, ±1,000 or ±10^9) the total of the answers and a checksum.
Answers are `i64`: the random arrays go past the 32-bit range the
problem promises. `min_moves2.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random cases.

| | property |
|---|---|
| P1 | on 1 to 7 numbers within 0 to 6, the answer is brute force's: the cheapest of every whole target from the least number to the most |
| P2 | on 1 to 60 numbers within ±1 to ±10^6, reversing and rotating the array keeps the answer |
| P3 | adding a constant to every number keeps it, and multiplying every number by `k` multiplies it by `k` |
| P4 | adding one number below all the others and one above all of them adds their difference |
| P5 | an array of zeros and ones costs the fewer of the two |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the middle of the unsorted array is the target | P1 577, P2 1211, P4 718, P5 562 |
| M2 | ★: signed distances are summed | P1 1172, P4 1500, P5 801 |
| M3 | pairs: the innermost pair is skipped | P1 499, P5 144 |
| M4 | pairs: the array is not sorted | P1 1015, P2 1368, P4 1132, P5 1413 |
| M5 | select: the least number is the target | P1 904, P4 1500, P5 657 |
| M6 | select: the first number of the kept part is returned | P1 507, P2 963, P4 239, P5 344 |
| M7 | every: the costliest target is kept | P1 1028, P4 1500, P5 1312 |
| M8 | every: only the first number is tried | P1 593, P2 1220, P4 173, P5 576 |

P1, the only property with an independent answer, sees all eight. P3
sees none: adding a constant or scaling by a positive `k` keeps the
order of the numbers, so every mutant's wrong answer moves with the
right one. P2 sees only the mutants that depend on where numbers sit
in the array (M1, M4, M6, M8). M3 survives P4, since the new outermost
pair leaves the innermost pair where it was.

## Verification

All four arms print the same output as `min_moves2.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file. The differential prints
`30000 checks, 0 failures` on both. The four arms and the differential
also run clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak.

On the frozen legacy backends every arm matches under
`karac run --interp`. LLJIT and `karac build` stop in the legacy code
generator on the harness's index into an array literal ("Index operator
applied to non-array type"), in every arm. The legacy type checker
rejects the differential, which reads loop items through `*x` where v2
lends them by reference. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 1,000,000 random numbers
within ±10^9 once; each of 10 rounds sets one number at a random index
to a new random value, then hands a copy of the array to `min_moves2`,
which sorts it and sums the distances to the median. Every
implementation prints `10 rounds on 1000000 numbers: 5001046714300076
moves in all, checksum 380866641`, the Kāra program under
`karac __mir-run` included (in 14 s).

The sort is each language's own: Kāra's `Vec.sort`, Rust's stable
`sort`, Go's `slices.Sort`, C's `qsort` with a comparison function, and
Python's `list.sort`. Sorting is the bulk of the work, so the table compares
sorts more than anything else. Spot timings on a shared 4-core
container, three runs each (two for Python; `bench.sh` timings need a
quiet machine):

| | time |
|---|---|
| C (`clang -O3`, `qsort`) | 1.48 to 1.64 s |
| Rust (`rustc -O`) | 0.30 to 0.35 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.33 to 0.40 s |
| Go | 1.05 to 1.13 s |
| Python | 4.2 to 4.3 s |
| Kāra (legacy `karac build`) | 0.20 to 0.25 s |
| Kāra (`karac build --mir`) | 2.42 to 2.58 s |

`bench.sh` builds with legacy `karac build`, which accepts this
program. The v2 compiled backend is about ten times slower here because
its `Vec.sort` sorts an index permutation through a function pointer
and copies the result back, which B-2026-10-12-30 (filed from kata 455)
already records; nothing new is filed. Under `karac __mir-llvm-run` the
program prints the same line in 9.6 s, compile included; that JITs the
MIR's IR without optimization passes, so it is not a benchmark.

## Compiler findings

No new findings. The bench measures B-2026-10-12-30 again.
