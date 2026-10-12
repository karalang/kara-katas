# 410. Split Array Largest Sum

Given an array `nums` and an integer `k`, split `nums` into `k`
non-empty contiguous pieces so that the largest sum of any piece is as
small as possible, and return that sum.

```
nums = [7,2,5,10,8], k = 2  -> 18   ([7,2,5] and [10,8])
nums = [1,2,3,4,5],  k = 2  -> 9    ([1,2,3] and [4,5])
nums = [1,4,4],      k = 3  -> 4
```

**Constraints:** `1 <= nums.length <= 1000`; `0 <= nums[i] <= 10^6`;
`1 <= k <= min(50, nums.length)`.

## Approaches

| file | mechanism | time | space |
|---|---|---|---|
| `split_array.kara` ★ | binary search on the answer: for a cap, a greedy pass finds the fewest pieces that stay under it; that count only falls as the cap rises, so search the smallest cap needing at most `k` pieces, between the largest number and the total | O(n log(total)) | O(1) |
| `split_array_dp.kara` | dynamic programming over prefix sums: `best[i]`, the least largest sum of the first `i` numbers in `j` pieces, is the least over `p < i` of the larger of `best[p]` and the sum from `p` to `i`; one round per piece | O(k n^2) | O(n) |
| `split_array_memo.kara` | top-down recursion on (start, pieces left) with a memo: the first piece ends somewhere leaving a number for each later piece, and the search stops once the first piece alone is no better than the best found | O(k n^2) | O(k n) |
| `split_array_candidates.kara` | the answer is the sum of some piece, so collect every contiguous run's sum, sort, drop repeats, and binary search them with the greedy test | O(n^2 log n) | O(n^2) |
| `differential.kara` | the four arms on 3,000 random cases, five properties, one of them a brute force over every way to cut | — | — |

Every arm prints the same 11 lines: the three LeetCode examples, seven
edge cases (one number, all zeros, `k = 1`, `k = n`, numbers at the
limit, five pieces of six numbers, a longer array in eight pieces), and
for 2,000 random arrays of 1 to 40 numbers from 0 to 99, each split
into 1 to `n` pieces, the total of the answers and a checksum.
`split_array.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms. Each of 3,000 random
cases makes an array of 1 to 30 numbers below 1, 10, 100 or 1,000, so
that some arrays are all zeros and many hold repeats, and a `k` from 1
to `n`:

| | property |
|---|---|
| P1 | one piece costs the total, and `n` pieces the largest number |
| P2 | the answer is at least the largest number and the total divided by `k`, and at most the total |
| P3 | one more piece never raises the answer |
| P4 | for the first 10 numbers and a random `k`, the answer is the least largest sum over every way to cut them, tried one by one |
| P5 | the array reversed gives the same answer, and every number tripled gives three times the answer |

It prints `3000 cases, 4 arms, 60000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, each run under `karac __mir-run`.
All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | search: a piece may not reach the cap exactly | P1 80, P4 1144, P5 1247 |
| M2 | search: the search starts at 0, not the largest number | P1 2101, P2 745, P4 748, P5 416 |
| M3 | dp: the last piece needs two numbers | P1 3000, P2 1632, P3 338, P4 1781, P5 1632 |
| M4 | dp: a split costs its last piece alone | P1 1919, P2 1833, P4 1740, P5 1879 |
| M5 | memo: the first piece leaves one number too many for the rest | P1 2176, P3 177, P4 755, P5 741 |
| M6 | memo: the memo is keyed by `start + pieces` | P2 115, P3 103, P4 469, P5 1032 |
| M7 | candidates: a cap below one number still fits | P1 2101, P2 745, P4 748, P5 416 |
| M8 | candidates: a cap fits only with fewer than `k` pieces | P1 191, P4 1300 |

M2 and M7 are one mistake in two arms, a cap below the largest number
let through, and fail exactly the same checks. M1 escapes P2 because
its answers are one too large, still within the bounds. M8 answers for
`k - 1` pieces, and is wrong the same way on the reversed and tripled
arrays, so P5 cannot see it. M6 makes two (start, pieces) pairs share
a memo slot whenever they add up alike, so it is wrong only on some
arrays, and each property sees it on at most about a third of the
cases.

## Verification

All four arms print the same output as `split_array.py` on every
backend: `karac __mir-run` (the v2 MIR interpreter),
`karac __mir-llvm-run`, `karac run --interp`, LLJIT, `karac build` and
`KARAC_AUTO_PAR=1 karac build`. `karac check` passes on every file.
The differential prints `60000 checks, 0 failures` under
`karac __mir-run`, `karac __mir-llvm-run` and `karac run --interp`.
The frozen legacy codegen refuses it with `Index operator applied to
non-array type` on `[1, 10, 100, 1000][step(mut seed) % 4]`, an index
into an array literal, which stops LLJIT, `karac build` and
`KARAC_AUTO_PAR=1 karac build`; it also warns about reused `Vec`
arguments, since it predates bare parameters borrowing. Not filed.

## Benchmarks

The bench program uses the ★ arm on 10,000 random arrays of 1,000
numbers (the problem's limit) from 0 to 10^6, each split into 1 to 50
pieces, built from an LCG. It folds the answers into a total and a
checksum. Every implementation prints `10000 arrays of 1000 numbers:
total 448129277720, checksum 213918463`; a 20-array cut of the Kāra
program under `karac __mir-run` prints the same as the C program cut
the same way. Spot timings on a shared 4-core container, three runs
each (`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| Kāra (legacy `karac build`) | 0.25 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.28 to 0.30 s |
| C (`clang -O3`) | 0.34 to 0.39 s |
| Rust (`rustc -O`) | 0.35 to 0.38 s |
| Go | 0.47 to 0.50 s |
| Python | 17 s |

Almost all the time is the greedy pass, about 30 per array. The Kāra
and checked Rust programs ran faster than C and unchecked Rust in
every run; why has not been looked into. The Kāra program also prints
the same line under `karac __mir-llvm-run` in 2.0 to 2.4 s, compile
included; that JITs the MIR's IR without optimization passes, so it is
not a benchmark. The `karac build` time is the frozen legacy backend.

## Compiler findings

No new findings.
