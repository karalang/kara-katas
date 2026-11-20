# 1664. Ways to Make a Fair Array

You are given an integer array `nums`. You can choose **exactly one**
index (**0-indexed**) and remove the element. Notice that the index of
the elements may change after the removal.

An array is **fair** if the sum of the odd-indexed values equals the sum
of the even-indexed values.

Return *the **number** of indices that you could choose such that after
the removal,* `nums` *is **fair**.*

```
nums = [2, 1, 6, 4]  ->  1
nums = [1, 1, 1]     ->  3
nums = [1, 2, 3]     ->  0
```

**Constraints:** `1 <= nums.length <= 10^5`; `1 <= nums[i] <= 10^4`.

## Approaches

| file | mechanism |
|---|---|
| `fair.kara` ★ | removing index i keeps the values before it where they are and moves every value after it to the other parity; with the totals by parity and the sums by parity so far, each index is checked in O(1). One pass after the totals, O(n) time, O(1) space |
| `fair_prefix.kara` | the same check from two prefix-sum `Vec`s, the even- and odd-indexed sums of the first i values, counted with `filter` over `0..n`. O(n) time and space |
| `fair_signed.kara` | each value signed, + at an even index and - at an odd one, so one total holds the difference; removing i flips every sign after it, so the array is fair exactly when the signed sum before i equals the signed sum after it. O(n) time, O(1) space |
| `fair_solution.kara` | a Rust solution as LeetCode's Rust users write it (the two totals, then one pass taking each value out of its total and comparing the swapped sums), carried by `karac fix`, which made 9 changes in one pass |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 9 lines: LeetCode's three examples and three
more (one value, two equal values, and seven ones), then the fair
removals and a checksum for 3000 random arrays of up to 8 values from 1
to 3, 300 of up to 1000 values up to 10, and 10 of up to `10^5` values
from 1 to 2, small values making fair removals common. `fair.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: each index removed in turn from a copy of the array, and the
even- and odd-indexed sums of what is left compared. It checks 3000
random arrays of up to 8 values from 1 to 3.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the array reversed gives the same answer |
| P3 | every value doubled gives the same answer |
| P4 | the answer is between 0 and n |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 999008626, 60000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the removed value left in the sums after it | P1 2306, P5 2306 |
| M2 | ★: each value added to the other parity's running sum | P1 922, P2 263, P5 922 |
| M3 | ★: the values after i kept at their parity | P1 1158, P5 1158 |
| M4 | prefix: the removed value counted in the sums after it | P1 2306, P5 2306 |
| M5 | prefix: an even index adds 1 to the odd sums | P1 1590, P2 797, P3 1267, P5 1590 |
| M6 | signed: the removed value's sign added back after it | P1 1726, P2 651, P5 1726 |
| M7 | signed: the running sum subtracts each signed value | P1 922, P2 263, P5 922 |
| M8 | template: the values after i kept at their parity | P1 1158, P5 1158 |
| M9 | template: an even-indexed value added to the left odd sum | P1 1158, P2 852, P5 1158 |
| M10 | template: an even-indexed value taken out of the odd total | P1 1761, P2 605, P5 1761 |

## Benchmarks

The bench draws 20 arrays of `10^5` values from 1 to 2, LeetCode's
largest length, all of them first, then answers each 50 times by the ★
arm in all five languages. Every implementation prints `20 arrays of
100000 values, 50 rounds: 237350 fair removals, checksum 851644160`. The
C build also runs clean under gcc's AddressSanitizer and
UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| Rust (`rustc -O -C overflow-checks=on`) | 0.295 s |
| Go | 0.327 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.079 s |
| Kāra (`karac build`) | 1.085 s |
| Rust (`rustc -O`) | 1.454 s |
| C (`clang -O3`) | 1.468 s |
| Python | 21 s |

The sequential Kāra build takes 0.74x Rust's time and 3.66x that of Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md).

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (1.022 s and 1.027 s on one
run).

## Verification

All four arms print the same output as `fair.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

The ★, prefix and signed arms checked clean as first written, the
`total[i % 2] += x` over a `[0, 0]` included: its open literals took
`i32` from `x`.

LeetCode's Rust template takes one `karac fix` of 9 edits, among them
`struct Solution {}` added, `Vec<i32>` to `Vec[i32]`, and both `let (mut
even, mut odd) = (0, 0);` and its twin to `let mut (even, odd) = (0,
0);`.
