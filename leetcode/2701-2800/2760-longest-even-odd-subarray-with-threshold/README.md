# 2760. Longest Even Odd Subarray With Threshold

You are given a **0-indexed** integer array `nums` and an integer
`threshold`.

Find the length of the **longest subarray** of `nums` starting at index
`l` and ending at index `r` `(0 <= l <= r < nums.length)` that
satisfies the following conditions:

- `nums[l] % 2 == 0`
- For all indices `i` in the range `[l, r - 1]`, `nums[i] % 2 !=
  nums[i + 1] % 2`
- For all indices `i` in the range `[l, r]`, `nums[i] <= threshold`

Return *an integer denoting the length of the longest such subarray.*

A **subarray** is a contiguous non-empty sequence of elements within an
array.

```
nums = [3, 2, 5, 4], threshold = 5  ->  3
nums = [1, 2],       threshold = 2  ->  1
nums = [2, 3, 4, 5], threshold = 4  ->  3
```

**Constraints:** `1 <= nums.length <= 100`, `1 <= nums[i] <= 100`, `1
<= threshold <= 100`.

## Approaches

| file | mechanism |
|---|---|
| `threshold.kara` ★ | one pass with the length of the good run ending here: a number over the threshold ends any run, one of the other parity from the last keeps a run going, and otherwise an even number starts a run of 1. O(n) |
| `threshold_brute.kara` | every subarray `l..=r` checked in full against the three rules. O(n^3) |
| `threshold_pairs.kara` | which neighbours may stand together worked out first over `zip` with `skip(1)` into a `Vec[bool]`; a run starts at each good even number and grows while its right neighbour may join. O(n) |
| `threshold_dp.kara` | `ending[i]`, the longest good subarray ending at i, from `ending[i - 1]` when the two may stand together, else 1 or 0 by a `starts` closure; the answer by `iter().max()`. O(n) |
| `threshold_solution.kara` | a Rust solution as LeetCode's Rust users write it, from each good start l a `while` loop running r on, with `usize` indices and `ans as i32`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's three examples; no even
number; 100 numbers alternating from 2, LeetCode's most; a run cut short
by a number over the threshold; and 20000 random arrays of 1 to 100
numbers with thresholds up to 100, with the sum of the answers and a
checksum. `threshold.py` mirrors the ★ arm and its output is
byte-identical.

```
3
1
3
0
100
3
20000 arrays: lengths sum to 76755, checksum 292738091
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every pair `l <= r`, kept when `nums[l]` is even, every
neighbouring pair in `l..=r` differs in parity, and every number in it
is within the threshold, each condition asked by `all` over its own
range. It draws 3000 random arrays of 1 to 15 numbers up to 10 with
thresholds up to 10, then 500 of up to 100 numbers up to 100, all before
any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | every number and the threshold 2 more: the same answer |
| P3 | the threshold raised to 100: no shorter; and lowered below every number: 0 |
| P4 | an odd number put at the front: the same answer |
| P5 | from 0 to n, and 0 just when no even number is within the threshold |
| P6 | each arm agrees with at least three of the other four |

The differential prints `3500 cases: checksum 928690633, 105000 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases by the same `all`s gives the same checksum. On
a failure it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a run kept going on the same parity | P1 1473, P6 1473 |
| M2 | ★: a number equal to the threshold taken as over | P1 623, P5 273, P6 623 |
| M3 | brute: an odd first number let through | P1 1370, P4 645, P5 572, P6 1370 |
| M4 | brute: the last pair's parity never asked | P1 1168, P6 1168 |
| M5 | pairs: each run counted one short | P1 2587, P5 984, P6 2587 |
| M6 | pairs: the right neighbour's threshold never asked | P1 784, P6 784 |
| M7 | dp: a number following no run | P1 434, P5 254, P6 434 |
| M8 | dp: only the run at the end answered | P1 1878, P5 1388, P6 1878 |
| M9 | solution: the threshold asked only of the first number | P1 945, P6 945 |
| M10 | solution: a first number over the threshold let start | P1 1303, P3 3310, P5 723, P6 1303 |

## Benchmarks

The bench draws 100000 arrays of 100 numbers up to 100 with thresholds
up to 100, LeetCode's most, all of them first, then answers each 10
times by the ★ arm in all five languages. Every implementation prints
`100000 arrays of 100, 10 rounds: lengths sum to 3360300, checksum
664579217`.

BENCHTAB

## Verification

All five arms print the same output as `threshold.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as first written.

LeetCode's Rust template took 11 `karac fix` edits, the wrapper
included: `struct Solution {}` added; `Vec<i32>` and `Vec<i64>` became
`Vec[i32]` and `Vec[i64]`; each `&&` became `and`; the `&x` pattern
dropped its `&`; and `Solution::` became `Solution.`, with the
wrapper's `as i64` dropped. The `usize` indices took no edit, since
`nums.len()` is an `i64` here and `n`, `l` and `r` follow it, and `ans
as i32` stayed.
