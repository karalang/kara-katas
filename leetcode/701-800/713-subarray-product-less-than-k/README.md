# 713. Subarray Product Less Than K

Given an array of integers `nums` and an integer `k`, return the number
of contiguous subarrays where the product of all the elements in the
subarray is strictly less than `k`.

```
nums = [10, 5, 2, 6], k = 100  ->  8
  ([10], [5], [2], [6], [10, 5], [5, 2], [2, 6], [5, 2, 6])
nums = [1, 2, 3],     k = 0    ->  0
```

**Constraints:** 1 <= `nums.length` <= 3 * 10^4; 1 <= `nums[i]` <=
1000; 0 <= `k` <= 10^6.

## Approaches

Every number is at least 1, so widening a subarray never lowers its
product: the subarrays below k that end at a given place are exactly its
suffixes up to some length, and those that start at a given place are
its prefixes up to some length.

| file | mechanism |
|---|---|
| `subarray_product_less_than_k.kara` ★ | a sliding window: extend it right one number at a time, divide numbers out from the left while the product is k or more, and count the right - left + 1 subarrays ending at the right end; O(n) |
| `subarray_product_less_than_k_starts.kara` | the same window from its other end: for each start, move the end on while the product stays below k, count the subarrays from that start, then divide the start out; O(n) |
| `subarray_product_less_than_k_brute.kara` | every start, extended until its product reaches k, the first failure ending that start; O(n * L), L the longest subarray counted |
| `subarray_product_less_than_k_logs.kara` | prefix sums of logarithms, which never fall, and a binary search from each start for the last end whose sum stays below ln k less a margin of 10^-9, so a product of exactly k is not counted; O(n log n) |
| `differential.kara` | the four arms against the definition, four properties |

The logs arm's margin is safe because ln k - ln(k - 1) is more than
10^-7 for every k up to 10^6, two orders above the margin, and the
rounding in a sum of 30,000 logarithms is far below that.

Every arm prints the same 15 lines: the two LeetCode examples; k of
1 and 2 over ones; a single number below, at and above k; products
reaching k exactly; the largest numbers against the largest k; four 3s
against k = 81 and 82; 3,000 ones with k = 2; 30,000 numbers, the
problem's most, from 1 to 3 and from 1 to 1,000 with k = 10^6; and
500 random arrays with a checksum. `subarray_product_less_than_k.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which takes every pair of ends and builds that subarray's product from
scratch, holding it at k once it reaches k so it cannot overflow, and
counts the products below k. 3,000 cases are checked, each two random
arrays of 0 to 12 numbers from 1 up to 1 to 12, with k from 0 to 299.

| | property |
|---|---|
| P1 | the count is the definition's |
| P2 | the array reversed has the same count |
| P3 | the two arrays with a number of k or more between them count the sum of their counts |
| P4 | the two arrays joined count at least the sum of their counts, and at most that plus every subarray that crosses the join |

It prints `3000 arrays (56350 subarrays), 4 arms, 48000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Eleven edits to the differential, two or three to each arm, each run
under `karac __mir-run`. All eleven are killed, M11 by stopping the
program. Three more edits, E1 to E3, change nothing that can be seen,
and the differential rightly reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a product of exactly k kept | P1 92, P3 2982 |
| M2 | ★: the right number divided out instead of the left | P1 1155, P2 1210, P3 2725, P4 112 |
| M3 | ★: one subarray too few counted at each end | P1 2748, P3 2982 |
| M4 | starts: a product of exactly k let in | P1 96, P3 2990 |
| M5 | starts: the window not restarted when the end falls one behind | P1 63, P2 26, P3 2760, P4 18 |
| M6 | brute: the cut one below k | P1 82 |
| M7 | brute: a product of exactly k counted | P1 96, P3 2990 |
| M8 | logs: the margin added, not taken away | P1 92, P3 2982 |
| M9 | logs: the sums measured from one past the start | P1 1591, P2 980, P3 2982 |
| M10 | logs: the end found counted as well | P1 2748, P3 2982 |
| M11 | brute: a failed product skipped rather than ending the start | stops: integer overflow |
| E1 | logs: only k = 0 answered early | 0 |
| E2 | starts: the start divided out even from an empty window | 0 |
| E3 | logs: a margin of 1e-8 | 0 |

P1 kills every mutant that runs to the end, and P3 every one but
M6. P3's wall is exactly k, so the four that let a product of exactly k
through, M1, M4, M7 and M8, count the wall itself, and the two that
miscount at every end, M3 and M10, miscount at the wall's end too.
M6, which cuts at k - 1, fails only P1, in the 82 cases with a subarray
whose product is exactly k - 1. M11 skips a failed product and carries
on multiplying instead of ending that start, and the product overflows:
Kāra checks integer overflow, so the program stops with `integer
overflow` rather than counting wrong. E1 answers only k = 0 early in the
logs arm, and for k = 1 its limit is below zero, so it counts nothing
anyway; E2 divides the start out of an empty window, leaving the product
0 until the window restarts at 1, which it always does next; E3 widens
the margin to 10^-8, still far below the gap it guards.

## Verification

Every arm prints the same output as `subarray_product_less_than_k.py`
under `karac __mir-run` (the v2 MIR interpreter) and `karac
__mir-llvm-run`, and under `karac __mir-llvm-asan` (AddressSanitizer)
with no error; the differential prints its line under all three. `karac
check` passes all four arms, the differential and the bench program. The
debug build that runs `__mir-llvm-run`, `__mir-llvm-asan` and `build
--mir` and the release build that runs `check` and `__mir-run` are both
at kara `4ac59f62cb`, whose last compiler change is `500dff0834`. No
`runtime/src` change has landed since the runtime archives were built.

The sanitizer lane cannot see a leak (kara B-2026-10-18-31), so the leak
check copied each arm's and the differential's lane executable as it was
linked and ran it with the preloaded shim from kata 708, which refuses
the lane's hand-made stack so that LeakSanitizer sees `main` (kata
708 showed it reporting a leak the lane misses): all five print their
output and report no leak.

The frozen legacy backends run three arms, the ★, starts and brute arms,
and print the same output under `karac run --interp`, `karac run`,
`karac build` and a `KARAC_AUTO_PAR=1` build. They refuse the logs arm,
the differential and the bench program at type checking, at `*x` over
`iter()`, since legacy gives those items by value where v2 gives
references. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It makes ten
arrays of 30,000 numbers once, from 1 to 2 up to 1 to 1,000, and counts
each for k = 10^6 in 200 rounds, summing the counts. Every
implementation prints `200 rounds of 10 arrays of 30000, k =
1000000: sum 629822200`, the Kāra program under `karac __mir-run`
included (in 20 s).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and three of Python (`bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.49 to 0.54 s |
| Rust (`rustc -O`) | 0.47 to 0.52 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.48 to 0.55 s |
| Go | 0.47 to 0.60 s |
| Python | 5.2 to 5.8 s |
| Kāra (`karac build --mir`) | 0.51 to 0.54 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the legacy `karac build` refuses it (above). That
edit is by hand, on top of the `scripts/new-bench.sh` output. Under
`karac __mir-llvm-run` the program prints the same line in 1.9 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

So all five compiled programs are level. Under valgrind's cachegrind the
v2 build runs 1.88 billion instructions against C's 1.25 and Rust's
1.49, and 614 million branches against 240 and 362, but all three
mispredict the same 29 million: whether the window's left end moves
depends on the data, and those misses, which no implementation avoids,
appear to set the time, so the extra, well-predicted work costs little.
That reading is inferred from the counts, not traced. The comparison
with C and Rust waits until after M4.

## Compiler findings

None new.
