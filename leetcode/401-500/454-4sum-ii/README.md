# 454. 4Sum II

Given four integer arrays `nums1`, `nums2`, `nums3` and `nums4`, all of
length `n`, return the number of tuples `(i, j, k, l)` such that
`0 <= i, j, k, l < n` and
`nums1[i] + nums2[j] + nums3[k] + nums4[l] == 0`.

```
nums1 = [1,2], nums2 = [-2,-1], nums3 = [-1,2], nums4 = [0,2]  ->  2
nums1 = [0],   nums2 = [0],     nums3 = [0],    nums4 = [0]    ->  1
```

**Constraints:** `1 <= n <= 200`; `-2^28 <= nums[i] <= 2^28`.

## Approaches

Every arm is
`fn four_sum_count(nums1: Vec[i64], nums2: Vec[i64], nums3: Vec[i64], nums4: Vec[i64]) -> i64`.

| file | mechanism |
|---|---|
| `four_sum.kara` ★ | count every sum of the first two arrays in a `Map`, then for each sum of the last two add the count of its negation. O(n²) |
| `four_sum_pointers.kara` | sort both lists of pair sums and walk one from the bottom and the other from the top; where a sum meets its negation, multiply the lengths of the two runs. O(n² log n) |
| `four_sum_search.kara` | sort the pair sums of the first two arrays, and for each pair sum `s` of the last two find the run equal to `-s` with two binary searches. O(n² log n) |
| `four_sum_cubic.kara` | the plain reference: count the fourth array's values, then try every choice from the first three. O(n³) |
| `differential.kara` | the four arms on 1,500 random cases, five properties |

Every arm prints the same 7 lines: the two LeetCode examples, one tuple
that misses, all zeros (81 tuples), the two extremes, a mixed case, and
for 300 random cases of 1 to 40 numbers per array (spread over 3, 11,
101 or every value from -2^28 to 2^28) the total tuples and a checksum.
`four_sum.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random cases.

| | property |
|---|---|
| P1 | on 1 to 5 numbers per array within -3 to 3, the count is brute force's over every tuple |
| P2 | on 1 to 15 numbers per array over a mixed spread, shuffling each array keeps the count |
| P3 | passing the arrays in another order keeps it |
| P4 | negating every number keeps it |
| P5 | adding a constant to the first array and taking it from the third keeps it |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | map: the sum is looked up, not its negation | P1 1026, P3 946, P5 1010 |
| M2 | map: a repeated pair sum counts once | P1 931, P3 590 |
| M3 | pointers: matching runs are added, not multiplied | P1 1075, P3 586 |
| M4 | pointers: the right run is taken as one sum | P1 912, P3 568 |
| M5 | search: the search finds the first sum above the target | P1 1056, P4 975 |
| M6 | search: the last sum is never reached | P1 596, P3 552, P4 666 |
| M7 | cubic: the third number's sign is flipped | P1 991, P3 935, P5 999 |
| M8 | cubic: the third number is read from the fourth array | P1 1080, P3 985, P5 984 |

P1, the only property with an independent answer, sees all eight. P2
sees none: every arm, mutated or not, counts or sorts each array's
values and never depends on their order. P3 catches the mutants that
treat the arrays unequally, and P4 the search mutants, whose off-by-one
does not survive turning the sums around.

## Verification

All four arms print the same output as `four_sum.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file. The differential prints
`30000 checks, 0 failures` on both. The four arms and the differential
also run clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak.

On the frozen legacy backends every arm matches under
`karac run --interp`, and the differential prints `0 failures` there.
LLJIT and `karac build` stop in the legacy code generator on the
harness's index into an array literal ("Index operator applied to
non-array type"), in every arm and the differential. Legacy
`karac build` also rejects the bench program (see Benchmarks). Legacy
is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 4 random arrays of 1,000
numbers from -50,000 to 50,000 once, then runs 10 rounds; each round
sets one number in every array to a new random value and counts the
tuples, which fills a fresh map with 1,000,000 pair sums and makes
1,000,000 lookups. Every implementation prints `10 rounds on 4 arrays
of 1000: 66673855 tuples, checksum 380080746`, the Kāra program under
`karac __mir-run` included (in 29 s).

The legacy `karac build` rejects the bench program (it moves
`arrays[0]` out of the index, where v2 borrows it), so `bench.sh` builds
the Kāra program with `karac build --mir`, the v2 compiled backend.
That edit is by hand, on top of the `scripts/new-bench.sh` output.

The mirrors keep the ★ arm's structure: count the pair sums in a hash
map, then look up the negations. Rust's `HashMap` hashes with
SipHash-1-3, the same family as Kāra's `Map`; Go uses its built-in
map; C has no map, so its mirror is an open-addressing table with
linear probing and a 64-bit mixing hash, doubled when half full. Spot
timings on a shared 4-core container, three runs each (two for Python;
`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.39 to 0.43 s |
| Rust (`rustc -O`) | 0.51 to 0.55 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.50 to 0.58 s |
| Go | 0.60 to 0.67 s |
| Python | 3.9 s |
| Kāra (`karac build --mir`) | 3.7 to 4.6 s |

Kāra is 7 to 9 times slower than Rust here, and the cost is in the
compiled backend's map (B-2026-10-12-29, below). Under
`karac __mir-llvm-run` the program prints the same line in 17 s,
compile included; that JITs the MIR's IR without optimization passes,
so it is not a benchmark.

## Compiler findings

- **B-2026-10-12-29** (MIR runtime, open, performance): a hashed `Map`
  on the compiled MIR backend costs about 9 times a Rust `HashMap` per
  lookup. The runtime's table indexes its entries with a std
  `HashMap<u64, Vec<usize>>` keyed by the key's hash, so each key is
  hashed twice and each new key allocates a bucket. A probe of
  10,000,000 lookups on a 200,003-key map takes 2.05 s compiled, against
  0.23 s in Rust. The output is correct; only the time is off.
- No correctness findings. `Option.copied()`, reached for first in the
  ★ arm's lookup, does not exist in Kāra's library or spec; the arms
  use `sums.get(key).unwrap_or(0)`, the form other katas use.
