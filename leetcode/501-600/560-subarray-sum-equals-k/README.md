# 560. Subarray Sum Equals K

Given an array of integers `nums` and an integer `k`, return the total
number of subarrays whose sum equals to `k`. A subarray is a contiguous
non-empty sequence of elements within an array.

```
nums = [1,1,1], k = 2  ->  2
nums = [1,2,3], k = 3  ->  2
```

**Constraints:** `1 <= nums.length <= 2 * 10^4`; `-1000 <= nums[i] <=
1000`; `-10^7 <= k <= 10^7`.

## Approaches

Every arm is `fn subarray_sum(nums: Vec[i64], k: i64) -> i64`. A
subarray from i to j sums to k exactly when the prefix sum up to j less
the prefix sum before i is k.

| file | mechanism |
|---|---|
| `subarray_sum.kara` ★ | one walk, counting each prefix sum seen so far in a `Map` (the empty prefix, 0, once at the start): each new prefix sum s ends as many subarrays as there were earlier prefix sums s - k; `get(...) ?? 0` and `m[s] = ...`; O(n) |
| `subarray_sum_brute.kara` | every start, with a running sum out to every end; O(n^2) |
| `subarray_sum_prefix.kara` | the prefix sums in a `Vec`, then every pair of them; O(n^2) |
| `subarray_sum_entry.kara` | the ★ arm's walk on a `SortedMap`, read with `if let Some(c)` and counted with `*seen.entry(s).or_insert(0) += 1`; O(n log n) |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 11 lines: eight arrays at the edges (the two
examples, one element equal to k and not, all zeros, sums that fall as
well as rise, and k reached only by the whole array), a count and
checksum over 300 random arrays of 1 to 40 elements in -5 to 5, and two
arrays of 5,000 elements, all zeros and random values in -1000 to
1000. The problem allows 20,000 elements; 5,000 keeps the two quadratic
arms quick under the MIR interpreter, where 20,000 took the brute arm
54 s. `subarray_sum.py` mirrors the ★ arm and its output is
byte-identical.

No output depends on the order a `Map` is walked in: the ★ arm only
looks keys up.

## Differential

`differential.kara` holds copies of the four arms and the definition,
the statement read literally: every subarray, summed from scratch,
O(n^3). Each arm is held to the properties below on 1,000 random arrays
of 1 to 25 elements: values in -3 to 3 with k in -4 to 4, or values in
-1000 to 1000 with k the sum of a randomly chosen subarray, in turn.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the answer is between 0 and n(n+1)/2, the number of subarrays |
| P3 | the array reversed gives the same answer |
| P4 | the array negated gives the same answer for -k |
| P5 | one more element at the end does not lower the answer |

It prints `1000 cases, 4 arms, 20000 checks, 0 failures` under `karac
__mir-run` and `karac __mir-llvm-run`, and runs clean under `karac
__mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the empty prefix counted 0 times, not once | P1 321, P3 465 |
| M2 | ★: each prefix sum's count set to 1, not raised | P1 298, P3 264 |
| M3 | brute: each start's own element skipped (`j` from `i + 1`) | P1 321, P3 465 |
| M4 | brute: sums of k or more counted | P1 900, P4 956 |
| M5 | prefix: the empty prefix left out of the pairs | P1 321, P3 465 |
| M6 | prefix: the pair's difference taken the wrong way round | P1 870 |
| M7 | entry: `k - s` looked up, not `s - k` | P1 816, P3 531 |
| M8 | entry: a new prefix sum counted from 1, not 0 | P1 810, P3 493 |
| E1 | ★: the empty prefix stored with `seen[0] = 1` | 0 |
| E2 | brute: the test written `sum - k == 0` | 0 |
| E3 | prefix: `j` from 0, so the first pass has no pairs | 0 |
| E4 | entry: the empty prefix stored through `entry` | 0 |

M1, M3 and M5 fail on the same cases in the same numbers because they
are one mistake made three ways: each loses exactly the subarrays that
start at index 0. Reversed, those become the subarrays that end at the
last index, which the mutants do count, so P3 sees them too. M4 and
M6 misjudge a subarray's sum, not which subarrays there are; negating
the array turns M4's "k or more" into "k or less", which P4 sees.
M6 counts the sums equal to -k and M7 the pairs of prefix sums that add
up to k, and negating the array and k leaves both counts alone, so
P4 cannot see them. M2 and M8 go wrong only when a prefix sum comes
round again, which the small values make common.

## Verification

Every arm prints the same output as `subarray_sum.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. `karac check`
passes on every arm, the differential and the bench program.

The frozen legacy backends: every arm prints the same output under
`karac run` and `karac build`, and under `KARAC_AUTO_PAR=1 karac build`.
Under `karac run --interp` the ★ and entry arms print it; the brute and
prefix arms print the first 10 lines and are still on the last, a
quadratic walk of 5,000 values, when a 60 s limit stops them. The
differential prints `0 failures` under `karac build`, after an ownership
warning that `nums` is moved and used again. Legacy refuses the bench
program (see Benchmarks). Legacy is frozen, so these are noted, not
filed.

## Benchmarks

The bench program uses the ★ arm. It builds 100 random arrays of
20,000 values from -1000 to 1000, the problem's most, once; then
20 times over every array is answered for a fresh k from -1000 to
1000. Every implementation prints `100 arrays of 20000, 20 rounds:
2483087 subarrays, checksum 887144882`, the Kāra program under `karac
__mir-run` included (62 s).

Every implementation counts the prefix sums in a fresh hash map per
array, as the Kāra arm does: Rust's `HashMap` with its `entry` API, Go's
`map[int64]int64`, and Python's `dict`. C has no hash map, so the C
program has its own: open addressing with linear probing, sized once to
twice the array and hashed with one multiplication. Spot timings on a
shared 4-core container, three runs each (two for Python; `bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.17 to 1.21 s |
| Rust (`rustc -O`) | 2.61 to 2.80 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.80 to 2.94 s |
| Go | 2.72 to 2.95 s |
| Python | 6.53 to 6.92 s |
| Kāra (`karac build --mir`) | 2.93 to 3.36 s |

The legacy `karac build` refuses this program: it moves `arrays[(round *
7 + g) % count]` out of the index (E_INDEX_MOVE_NON_COPY) where
v2 borrows it. So `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`136e218505`. Under `karac __mir-llvm-run` the program prints the same
line in 31.5 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark. The Kāra row is within
about a fifth of Rust's and level with Go's. C's lead is its table: it
never grows and its hash is one multiplication, where Rust's `HashMap`
hashes with SipHash-1-3, and Kāra's `Map` does too.

## Compiler findings

None new. Nothing was filed from this kata; the legacy failures above
are not filed because legacy is frozen.
