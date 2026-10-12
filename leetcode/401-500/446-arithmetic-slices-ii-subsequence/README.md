# 446. Arithmetic Slices II - Subsequence

Given an integer array `nums`, return the number of its arithmetic
subsequences. A sequence is arithmetic when it has at least three
elements and every two consecutive elements differ by the same amount.
A subsequence keeps some elements, possibly none, in their order;
subsequences at different indexes count separately even when their
values agree.

```
nums = [2,4,6,8,10]  ->  7   ([2,4,6], [4,6,8], [6,8,10], [2,4,6,8], [4,6,8,10], [2,4,6,8,10], [2,6,10])
nums = [7,7,7,7,7]   ->  16  (every choice of three or more)
```

**Constraints:** `1 <= nums.length <= 1000`;
`-2^31 <= nums[i] <= 2^31 - 1`; the answer fits in 32 bits.

## Approaches

Every arm is `fn number_of_arithmetic_slices(nums: Vec[i64]) -> i64`.
Values are `i64`, so differences of two 32-bit values (up to 2^32) and
`2 * nums[j] - nums[i]` cannot overflow.

| file | mechanism |
|---|---|
| `arithmetic_slices.kara` ★ | a map of differences per index: `ending[i][d]` counts the subsequences of two or more values that end at `i` with difference `d`. Each earlier `j` extends those ending at `j` and starts the pair `(j, i)`; the extensions are the slices. O(n²) expected time and space |
| `arithmetic_slices_pairs.kara` | counting by the last two values: `slices[j][i]` sums, over each earlier `k` holding `2 * nums[j] - nums[i]`, one for `(k, j, i)` plus `slices[k][j]`. A map from each value to its indexes finds the `k`'s |
| `arithmetic_slices_sorted.kara` | the ★ recurrence with each index's counts as a list of (difference, count) pairs, sorted and merged, searched by binary search. O(n² log n) |
| `arithmetic_slices_memo.kara` | memoized recursion from the front: `from(k, j)` counts the ways to continue a slice that starts `nums[k], nums[j]`, so each slice is counted once, by its first two values |
| `differential.kara` | the four arms on 1,500 random cases, five properties |

Every arm prints the same 9 lines: the two LeetCode examples, short
arrays of one, two and three values, the 32-bit overflow case
`[0, 2000000000, -294967296]` (0: the differences are 2·10⁹ and
-2294967296), a case of values at both 32-bit limits, a mixed case,
and for 300 random arrays of 1 to 60 values (spread over 3, 10, 100 or
1,000,000 values around 0) the total count and a checksum. The narrow
spreads repeat values and differences, so their counts run into the
millions, past the 32-bit bound the problem promises; `i64` holds them.
`arithmetic_slices.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random cases.

| | property |
|---|---|
| P1 | on a small array (1 to 10 values spread over 2, 3, 5 or 100), the count is brute force's over every choice of indexes |
| P2 | `m` equal values, `m` up to 40, hold 2^m - 1 - m - m(m - 1)/2 slices: every choice of three or more |
| P3 | reversing an array of 1 to 40 values (spread over 3, 10, 100 or 1,000,000) keeps its count |
| P4 | mapping each value `x` to `a * x + b`, `a` one of 1, -1, 2, -3 or 1,000, keeps the count |
| P5 | an arithmetic progression of `m` distinct values, with steps up to 2^31 - 1 so that differences pass 32 bits, holds one slice for each index step, start and length of three or more that fits |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | maps: a pair is counted but never extended | P1 432, P2 1387, P5 1387 |
| M2 | maps: index 0 is never an earlier value | P1 642, P2 1418, P3 812, P5 1418 |
| M3 | pairs: `k` may be `j` itself | P1 975, P2 1458 |
| M4 | pairs: the difference's sign is dropped | P1 642, P3 899, P4 374, P5 553 |
| M5 | sorted: the binary search finds the end of a difference's run | P1 789, P2 1418, P5 1418 |
| M6 | sorted: a later count replaces an equal difference's | P1 494, P2 1387, P3 727 |
| M7 | memo: the third value never directly follows the second | P1 678, P2 1418, P3 830, P5 1418 |
| M8 | memo: the first two values are never neighbours | P1 682, P2 1418, P3 836, P5 1418 |

P4 sees only M4: a negative `a` turns a falling slice into a rising one,
and only M4 treats the two differently. P2 misses M4 for the same
reason, since equal values have difference 0. M3 and M6 need repeated
values or repeated differences at one index, which the progressions of
P5 never have. M1, M3 and M5 behave the same on an array and its
reversal, so P3 misses them; M1 fails P2 and P5 only once `m` reaches
4, where the first slice of four values appears.

## Verification

All four arms print the same output as `arithmetic_slices.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file. The differential prints
`30000 checks, 0 failures` on both. The four arms and the differential
also run clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak.

On the frozen legacy backends the maps, pairs and memo arms match under
`karac run --interp`; LLJIT and `karac build` stop in the legacy code
generator on the harness's index into an array literal ("Index
operator applied to non-array type"). The sorted arm and the
differential do not pass the legacy type checker, which predates bare
parameters borrowing (D5): it refuses passing an element of a
`Vec[Vec[(i64, i64)]]` to a bare parameter (`E_INDEX_MOVE_NON_COPY`).
The bench program builds and matches under legacy `karac build`.
Legacy is frozen, so these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 20 random arrays of 1,000
values from -500 to 499 once, then counts the slices in each. Every
implementation prints `20 arrays of 1000: 1987875 slices, checksum
558431196`, the Kāra program under `karac __mir-run` included (in 18 s).

The mirrors keep the ★ arm's structure: a hash map per index from
difference to count. Rust's `HashMap` hashes with SipHash, as Kāra's
`Map` does; Go uses its built-in map; C has no hash map, so it uses a
small open-addressing table per index (linear probing, doubled at half
full) with a 64-bit mixing hash, which is cheaper per lookup than
SipHash. Spot timings on a shared 4-core container, three runs each
(two for Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.69 to 0.76 s |
| Rust (`rustc -O`) | 0.66 to 0.78 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.70 to 0.78 s |
| Go | 1.0 to 1.2 s |
| Python | 2.9 to 3.0 s |
| Kāra (legacy `karac build`) | 0.79 to 0.93 s |

The run is dominated by building 20,000 hash maps of up to 999
entries, so all three compiled languages land close together. The Kāra
program prints the same line under `karac __mir-llvm-run` in 19 s,
compile included; that JITs the MIR's IR without optimization passes,
so it is not a benchmark.

## Compiler findings

No new findings.
