# 1749. Maximum Absolute Sum of Any Subarray

You are given an integer array `nums`. The **absolute sum** of a
subarray `[nums_l, nums_l+1, ..., nums_r-1, nums_r]` is `abs(nums_l +
nums_l+1 + ... + nums_r-1 + nums_r)`.

Return *the **maximum** absolute sum of any **(possibly empty)**
subarray of* `nums`.

```
nums = [1, -3, 2, 3, -4]        ->  5    [2, 3]
nums = [2, -5, 1, -4, 3, -2]    ->  8    [-5, 1, -4]
```

**Constraints:** `1 <= nums.length <= 10^5`; `-10^4 <= nums[i] <= 10^4`.

## Approaches

| file | mechanism |
|---|---|
| `abs.kara` ★ | Kadane's scan both ways: the largest absolute sum is the largest subarray sum or minus the smallest, and one walk keeps the best sum ending here in each direction, dropping a run once it turns against its direction. O(n) |
| `abs_prefix.kara` | every subarray sum is the difference of two prefix sums, the empty prefix included, so the answer is the highest prefix sum less the lowest, whichever comes first. O(n) |
| `abs_scan.kara` | the prefix sums come out of `scan`, and a `fold` keeps their highest and lowest, both starting from the empty prefix's 0. O(n) |
| `abs_solution.kara` | a Rust solution as LeetCode's Rust users write it, `let (mut mx, mut mn, mut s) = (0, 0, 0)` and a `for x in nums` loop with the `max` and `min` methods, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 8 lines: LeetCode's two examples, then one
value, all negative values, and 100000 values of -10000, LeetCode's
largest answer; then the sum of the answers and a checksum for 3000
random arrays of up to 8 values within 5, 300 of up to 1000 within
10000, and 10 of up to 100000 within 10000, LeetCode's limits.
`abs.py` mirrors the ★ arm and its output is byte-identical.

```
5
8
7
14
1000000000
3000 arrays of up to 8 values within 5: answers add to 22598, checksum 586896597
300 arrays of up to 1000 values within 10000: answers add to 213688316, checksum 289601489
10 arrays of up to 100000 values within 10000: answers add to 870796534, checksum 149706256
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every non-empty subarray summed in `i64`, and the largest
absolute value of those sums. It checks 3000 random arrays of 1 to 8
values from -6 to 6, each with a random value to append. Every case is
drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the array reversed gives the same answer |
| P3 | the array negated gives the same answer |
| P4 | one more value at the end never lowers the answer |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 191931358, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading, every slice summed and its absolute value taken, gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. A first M3, the high run clamped at 0
after the value is added rather than before, is equivalent: it changes
only runs that end below 0, which never decide a maximum of at least 0.
It was replaced.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: only the high run counted | P1 1363, P3 2814, P5 1363 |
| M2 | ★: the low run never restarted | P1 502, P2 713, P3 1021, P5 502 |
| M3 | ★: the high run the largest value so far, not a sum | P1 1105, P3 2113, P5 1105 |
| M4 | prefix: the highest and lowest prefix added, not subtracted | P1 1988, P2 1802, P3 2884, P4 656, P5 1988 |
| M5 | prefix: the highest prefix not starting from the empty one | P1 774, P2 894, P3 1620, P5 774 |
| M6 | prefix: the lowest taken over the values, not the prefixes | P1 1965, P2 1802, P3 2500, P5 1965 |
| M7 | scan: each prefix sum given out one value late | P1 1551, P2 1853, P5 1551 |
| M8 | scan: the lowest held at or above minus the highest | P1 1678, P2 1653, P3 2911, P5 1678 |
| M9 | solution: the lowest taken over the values, not the running sum | P1 1965, P2 1802, P3 2500, P5 1965 |
| M10 | solution: the larger of the highest and minus the lowest, not their difference | P1 1062, P2 1688, P5 1062 |

## Benchmarks

The bench draws 20 random arrays of 100000 values within 10000,
LeetCode's limits, all of them first, then answers each 40 times by the
★ arm in all five languages. Every implementation prints `20 arrays of
100000 values, 40 rounds: answers add to 112710399040, checksum
511612146`. The C build also runs clean under gcc's AddressSanitizer and
UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `21cdf88b69` on LLVM 22:

| | median |
|---|---|
| Rust (`rustc -O`) | 0.126 s |
| C (`clang -O3`) | 0.138 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.144 s |
| Kāra (`karac build`) | 0.146 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.146 s |
| Go | 0.154 s |
| Python | 9.9 s |

The sequential Kāra build takes 1.14x Rust's time and 0.99x that of Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md).
The gap to plain Rust is the overflow checks: with them on, Rust takes
Kāra's time.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes
nothing here: its user time is not above its real time (0.145 s and
0.146 s on one run).

## Verification

All four arms print the same output as `abs.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `21cdf88b69`.

## Writing it

The ★ arm was first written with `let mut high = 0;`, `low` and `best`
the same, and took one `karac fix` of 3 edits: a literal binding
defaults to `i64` and the function returns `i32`, so each became `: i32`.
The prefix arm took the same fix for `prefix` and `highest`; `lowest`
needed none, since `min(lowest, prefix)` gives it `prefix`'s type. The
scan arm's `fold((0, 0), ..)` took one fix to `(0i32, 0i32)`.

LeetCode's Rust template took one `karac fix` of 13 edits: `struct
Solution {}` added, `Vec<i32>` written `Vec[i32]`, `let (mut mx, mut mn,
mut s)` written `let mut (mx, mn, s)` with its literals typed
`(0i32, 0i32, 0i32)`, and `Solution::max_absolute_sum` written
`Solution.max_absolute_sum`. The `max` and `min` methods and the
consuming `for x in nums` carried over as written.

The differential and the bench checked clean as generated.
