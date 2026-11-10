# 1099. Two Sum Less Than K

Given an array `nums` of integers and an integer `k`, return the maximum
`sum` such that there exist `i < j` with `nums[i] + nums[j] = sum` and
`sum < k`. If no `i`, `j` exist satisfying this equation, return `-1`.

```
nums = [34,23,1,24,75,33,54,8], k = 60  ->  58
nums = [10,20,30],              k = 15  ->  -1
```

**Constraints:** `1 <= nums.length <= 100`; `1 <= nums[i] <= 1000`;
`1 <= k <= 2000`.

The arms are `fn two_sum_less_than_k(nums: Vec[i64], k: i64) -> i64`.
The two places must differ, but the values need not: `[7, 7]` pairs 7
with itself.

## Approaches

| file | mechanism |
|---|---|
| `two_sum_less_than_k.kara` ★ | sorting and two pointers: a pair whose sum is under `k` makes every pair with a smaller right value under `k` too, so the left pointer moves on; a pair at or over `k` moves the right pointer in. O(n log n) |
| `two_sum_less_than_k_pairs.kara` | every pair, as the statement reads: `flat_map` over the index pairs `i < j`, the sums under `k` kept by `filter`, then `max` and `unwrap_or(-1)`. O(n^2) |
| `two_sum_less_than_k_counts.kara` | counting instead of sorting: how many times each value 1 to 1000 occurs, in a `[0; 1001]` array, then two pointers over the values themselves; a value pairs with itself only when it occurs twice |
| `two_sum_less_than_k_search.kara` | sorting and binary search: for each value, `partition_point` counts the sorted values below `k` minus it, and the largest of those before it in the order is its best partner |
| `two_sum_less_than_k_set.kara` | one pass, the input never sorted: a `SortedSet[i64]` of the values seen so far, the best partner of each value the last of the range below `k` minus it (`range(i64.MIN, k - x).next_back()`), then the value joins the set |
| `two_sum_less_than_k_solution.kara` | LeetCode's Rust template (`impl Solution`, `mut nums: Vec<i32>`, `sort_unstable`, `let (mut i, mut j) = (0usize, nums.len() - 1)`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 13 lines: the answers for LeetCode's two
examples and nine more (one value, a pair of equal values just under and
at `k`, four copies of one value, two 1000s and then 999 and 1000 at `k`
= 2000, a `k` below every sum, two pairs at exactly `k` - 1, the best of
four values one under `k` = 1001), then over
2000 random arrays of 1 to 100 values how many had a pair and their sums
(`1854 with a pair, sums total 1889682, checksum 253680252`), and 100
values, LeetCode's most, at every `k` from 1 to 2000 (`answers sum to
1972405`). `two_sum_less_than_k.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every pair `i < j`, the largest sum under `k`, or -1. It
checks 2000 problems in four kinds of 500: 1 to 40 values from 1 to 1000
with `k` from 1 to 2000; 1 to 6 values from 1 to 5 with `k` from 1 to
12; 2 to 20 copies of one value with `k` within one of twice it; and 2
to 30 values with `k` one of their pair sums, or one more. Every random
choice is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal one |
| P2 | an answer is -1, or under `k` and the sum of two values at different places |
| P3 | the values reversed and rotated give the same answer |
| P4 | a found answer `a` is found again under `a + 1`, and under `a` something smaller is; none found stays none under `k - 1`; above every sum the answer is the two largest values, and one above the two smallest it is those two |
| P5 | every value moved up by `d`, as far as 1000 allows, and `k` by `2d`: the answer moves up by `2d`, or stays -1 |
| P6 | the values twice over never do worse, and adding `k - 1`, which pairs with nothing under `k`, changes nothing |

All 72,000 checks pass on every arm: `2000 problems: checksum
942064914, 72000 checks over 6 arms: 0 failures`. A Python reading of
the same problems gives the same checksum.

P1 and P2 lean on the literal pairs, and P4's two ends on the values
sorted. P3, P5, P6 and the rest of P4 compare the arm only with itself.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`, each failing the same way
under both. All thirty are caught. Fifteen are kept, no two failing the
same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a sum of `k` itself allowed | P1 609, P2 609, P4 1644, P6 157 |
| M2 | ★: the right pointer moved after a fit | P1 889, P4 1274 |
| M3 | ★: no pair answered 0 | P1 630, P2 630, P4 630, P5 623 |
| M4 | ★: the last two values never paired | P1 340, P4 1373 |
| M5 | ★: never sorted | P1 905, P3 848, P4 1125 |
| M6 | pairs: a value paired with itself | P1 301, P2 301, P4 1352 |
| M7 | pairs: the smallest sum under `k` | P1 1065, P4 1294, P6 1087 |
| M8 | pairs: the first value never on the left | P1 265, P3 296, P4 683 |
| M9 | counts: 1000 never paired | P1 1, P4 21, P5 10 |
| M10 | counts: a value never paired with its own copy | P1 227, P4 738 |
| M11 | search: the smallest value never a partner | P1 268, P4 1404 |
| M12 | search: never sorted | P1 929, P2 666, P3 854, P4 1188, P6 150 |
| M13 | set: the smallest partner under `k`, not the largest | P1 867, P3 813, P4 1178 |
| M14 | set: the last sum found, not the largest | P1 765, P3 806, P4 979 |
| M15 | set: a sum of `k` - 1 not allowed | P1 659, P4 1915 |

P1 and P4 catch all fifteen, P3 five, P2 four, P6 three and P5 two. M9
is the narrow one: the counting arm never pairing 1000 changes the
answer only when 1000 is in the best pair, which one random problem in
2000 has; P4 sees it in 21, since asking above every sum makes the two
largest values the answer, and P5 in 10, where moving every value up
brings one to 1000. P3, P5 and P6, which compare the arm only with
itself, catch nine; they miss the six edits that answer wrongly the
same way whatever the order, the scale or the copies, such as a value
paired with itself (M6) or one never paired with its own copy (M10).

The fifteen not kept all fail exactly as a kept edit: a sum of `k`
itself allowed is M1 in all six arms; the right pointer moved after a
fit (M2) is also the search arm always taking the smallest value as the
partner and the solution arm moving its right pointer; no pair answered
0 (M3) is also the pairs and solution arms; never sorted (M5) is also
the solution arm; a value paired with itself (M6) is also the counts,
search and set arms; the counts arm not counting copies is M10; and the
solution arm never pairing the smallest value is M11.

## Verification

Every arm prints the same output as `two_sum_less_than_k.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
every arm and the differential. `karac check --output=json` reports
nothing on any file, and `karac fix` has nothing to apply.

The kata found one gap, fixed in the compiler:

- The set arm was written as Rust writes it, `seen.range(..k -
  x).next_back()`. Kāra's `range` and `range_inclusive` take both ends,
  and since kata 2070 the refusal names the end to supply, but `karac
  fix` had nothing to apply. Over an integer element type the missing
  end is the type's `MIN` or `MAX`, so the edit is now written: `..b` to
  `range(T.MIN, b)`, `..=b` to `range_inclusive(T.MIN, b)`, `a..` to
  `range_inclusive(a, T.MAX)`, on a `SortedSet` or a `SortedMap`'s keys,
  and `..` to `iter()` over any type. Over any other type, a `String`
  say, the advice stands alone (kara B-2026-11-10-31, pinned by
  `tests/kata_1099_open_range_fix.rs`).

With that, `karac fix` makes every change the arms needed: the set
arm's `range(i64.MIN, k - x)`, `||` to `or` and `let (mut lo, mut hi)`
to `let mut (lo, hi)` in the counts arm, and the `move` dropped from the
pairs arm's inner closure. The ★ and search arms needed none. LeetCode's
template reaches a clean check in three rounds: the syntax (`mut nums:
Vec<i32>` to `nums: own Vec[i32]` and a `let mut nums = nums;`, `let
(mut i, mut j)` to `let mut (i, j)`), then `struct Solution {}`, then
`sort_unstable()` to `sort()`, `0usize` to `0`, and `ans: i32` on the
`-1`.

## Benchmarks

The bench builds 64 arrays of 100 values from 1 to 1000 once, LeetCode's
most. Each of 400 rounds changes one value in every array and asks it
for the best pair under 8 values of `k` with the ★ arm, which sorts a
copy: 204,800 calls. Every implementation prints `400 rounds over 64
arrays of 100 values: 201732 of 204800 with a pair, checksum
359992173`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `33ef2a7ad2`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.201 to 0.216 s | 0.204 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.199 to 0.242 s | 0.205 s |
| Rust (`rustc -O`) | 0.220 to 0.380 s | 0.229 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.221 to 0.303 s | 0.234 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.228 to 0.272 s | 0.242 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.664 to 0.732 s | 0.679 s |
| C (`clang -O3`) | 0.694 to 0.746 s | 0.709 s |
| Go | 0.808 to 0.931 s | 0.872 s |
| Python | 2.740 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra and Rust tie within about 10%. C sorts with `qsort` and Go
with `sort.Slice`, as the kata convention has every mirror use its
library's sort, and both take 3.5 to 4.3x Kāra's time on 100 values,
where Kāra's and Rust's sorts can inline the comparison. Python takes
about 13x Kāra's time.
