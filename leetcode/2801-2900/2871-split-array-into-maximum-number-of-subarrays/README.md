# 2871. Split Array Into Maximum Number of Subarrays

You are given an array `nums` consisting of **non-negative** integers.

We define the score of subarray `nums[l..r]` such that `l <= r` as
`nums[l] AND nums[l + 1] AND ... AND nums[r]` where **AND** is the
bitwise `AND` operation.

Consider splitting the array into one or more subarrays such that the
following conditions are satisfied:

- **Each** element of the array belongs to **exactly** one subarray.
- The sum of scores of the subarrays is the **minimum** possible.

Return *the **maximum** number of subarrays in a split that satisfies
the conditions above.*

A **subarray** is a contiguous part of an array.

```
nums = [1,0,2,0,1,2]  ->  3
nums = [5,7,1,3]      ->  1
```

**Constraints:** `1 <= nums.length <= 10^5`; `0 <= nums[i] <= 10^6`.

## Approaches

| file | mechanism |
|---|---|
| `split.kara` ★ | an AND only falls as it grows, so the least sum of scores is the AND of the whole array; if that is above 0 one subarray is best, and if it is 0 each subarray must score 0, so cut greedily each time the running AND reaches 0, a left-over tail joining the last part |
| `split_bits.kara` | the same greedy cut with the running AND kept as 20 flags, one per bit, 10^6 being under 2^20: a flag stays up only while every value since the last cut has its bit, and a part ends when none is left |
| `split_dp.kara` | no greedy assumed: with the whole AND 0, the most parts of the first i values that each score 0 is 1 + the most of the earlier prefixes j whose AND from j to i - 1 is 0; the ANDs of the subarrays ending at a place take at most 21 values, kept as (AND, most parts before), and carried from place to place |
| `split_fold.kara` | the greedy cut as one `fold` carrying (parts, running AND), the running AND starting again from all ones after each cut |
| `split_solution.kara` | a Rust solution as LeetCode's Rust users write it: `let mut cur = -1i32`, `cur &= x` over `&nums`, a cut counted when it reaches 0, and `ans.max(1)`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 4 lines: LeetCode's two examples; 10^5
values, LeetCode's most, all 0, all 2^20 - 1, and 1 and 2 by turns; then
3000 random arrays of 1 to 8 values from 0 to 7, and 30 of 10^4 to 10^5
up to 10^6, every other one with most bits set, as a total of
subarrays and a checksum. `split.py` mirrors the ★ arm and its output
is byte-identical.

```
3 1
100000 1 50000
3000 short arrays: 4526 subarrays, checksum 138467699
30 long arrays: 316788 subarrays, checksum 348914147
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every way to cut the array tried, each set of cuts read
as a bit mask of the n - 1 gaps, its parts' ANDs summed, the least sum
found, and the most parts among the cuts that reach it. It draws 2000
random arrays of 1 to 10 values from 0 to 7, then 50 of up to 3000 up
to 10^6, every other one with most bits set, all before any arm
answers; the literal reading is asked only of the first 2000.

| | property |
|---|---|
| P1 | up to 10 values, the answer is the literal reading's |
| P2 | a 0 put at the end: one more, or 1 when the whole AND was above 0 |
| P3 | the array reversed: the same answer |
| P4 | the first value written twice: the same answer, one more when it is 0 |
| P5 | from 1 to n, and 1 when the whole AND is above 0 |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases, 15572 subarrays: checksum
468423649, 61500 checks over 5 arms: 0 failures` under every lane in
Verification, and a Python reading of the same cases gives the same
checksum. On a failure it prints the first ten and then the count by
property.

P4 was first every value doubled. The bits arm failed it on 35 long
cases and only there: a doubled value passes 2^20, which the bits arm,
sized to LeetCode's bound, does not watch. Doubling breaks the
constraints rather than the arm, and P4 became one that keeps them. Its
first form, the same answer with the first value twice, failed every arm
on arrays that start with 0, which cuts there; it now says one more.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the running AND not started again after a cut | P1 1308, P3 1199, P6 1358 |
| M2 | ★: no floor of one part | P1 456, P5 456, P6 456 |
| M3 | bits: the top bit never watched | P1 936, P2 1594, P4 247, P6 984 |
| M4 | bits: a cut when one flag is left | P1 1420, P2 312, P4 743, P5 69, P6 1469 |
| M5 | dp: the empty prefix taken as unreachable | P1 936, P2 1594, P4 247, P6 984 |
| M6 | dp: equal ANDs not merged, the first kept | P1 936, P2 1594, P4 247, P6 984 |
| M7 | fold: the running AND carried through a cut | P1 1308, P3 1199, P6 1358 |
| M8 | fold: a cut counted on every value | P1 1802, P2 456, P4 1803, P5 288, P6 1852 |
| M9 | solution: a cut when the AND is odd | P1 1139, P2 255, P4 783, P5 99, P6 1189 |
| M10 | solution: the floor of one part as two | P1 1064, P2 1066, P4 72, P5 480, P6 1066 |

## Benchmarks

The bench draws 50 arrays of 10^5 values, LeetCode's most, up to 10^6,
every other one with most bits set, all of them first, then answers
each 10 times by the ★ arm in all five languages. Every implementation
prints `50 arrays of 100000, 10 rounds: 8881410 subarrays, checksum
734843197`.

BENCHTAB

## Verification

All five arms print the same output as `split.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

`split_dp.kara` and `split_fold.kara`, as first written, named the
running AND `and`, and `karac check` reported E_RESERVED_KEYWORD at each
use: `and` is Kāra's logical operator. `karac fix` wrote the raw
identifier `r#and` at every use, which the arms keep, as the fix the
compiler gives; a rename would read better. The other two arms checked
clean.

LeetCode's Rust template took 11 `karac fix` edits in one run, the
wrapper included: `struct Solution {}` added for the `impl`; `Vec<..>`
became `Vec[..]`; `let mut ans = 0` took `: i32`; `for &x in &nums`
became `for x in ref nums`; `|&x|` lost its `&`, the wrapper's `as i64`
went, an `i32` widening, and `Solution::` took `.`. `-1i32` and `cur &=
x` were accepted as written.
