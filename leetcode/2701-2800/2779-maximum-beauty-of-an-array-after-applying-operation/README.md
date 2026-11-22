# 2779. Maximum Beauty of an Array After Applying Operation

You are given a **0-indexed** array `nums` and a **non-negative**
integer `k`.

In one operation, you can do the following:

- Choose an index `i` that **hasn't been chosen before** from the range
  `[0, nums.length - 1]`.
- Replace `nums[i]` with any integer from the range `[nums[i] - k,
  nums[i] + k]`.

The **beauty** of the array is the length of the longest subsequence
consisting of equal elements.

Return *the **maximum** possible beauty of the array* `nums` *after
applying the operation any number of times.*

**Note** that you can apply the operation to each index **only once**.

A **subsequence** of an array is a new array generated from the
original array by deleting some elements (possibly none) without
changing the order of the remaining elements.

```
nums = [4, 6, 1, 2], k = 2   ->  3
nums = [1, 1, 1, 1], k = 10  ->  4
```

**Constraints:** `1 <= nums.length <= 10^5`, `0 <= nums[i], k <=
10^5`.

## Approaches

Numbers can all be made one value v just when v lies in every one of
their reaches `[x - k, x + k]`, that is when they lie within 2k of each
other; the order of a subsequence plays no part.

| file | mechanism |
|---|---|
| `beauty.kara` ★ | the numbers sorted and the widest window with its greatest at most 2k above its least found by two pointers. O(n log n) |
| `beauty_sweep.kara` | no sorting: every reach written as +1 and -1 in a difference array over every value the numbers can reach, and the most reaches covering one value read by a running sum. O(n + V), V the values' span |
| `beauty_search.kara` | the numbers sorted; from each as the least, the first number more than 2k above it found by `partition_point`, and the numbers between counted, the most taken by `max`. O(n log n) |
| `beauty_events.kara` | each reach as two events, `(x - k, 1)` and `(x + k + 1, -1)`, sorted as pairs so an end comes before a start at one value; the most reaches open at once. O(n log n) |
| `beauty_solution.kara` | a Rust solution as LeetCode's Rust users write it, `mut nums` sorted by `sort_unstable` and a window whose left end moves on while `nums[r] - nums[l] > 2 * k`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples; `10^5`
numbers, LeetCode's most, all 0 with k = 0, 0 to 99999 with k = 0 and
with `k = 10^5`, and spaced by 3 with k = 1; 3000 random arrays of 1 to
12 numbers from 0 to 20 with k from 0 to 5; and 20 arrays of `10^5`
numbers up to `10^5` with k up to 1000, the last two with the sum of
the beauties and a checksum. `beauty.py` mirrors the ★ arm and its
output is byte-identical.

```
3
4
100000
1
100000
1
3000 small arrays: beauties sum to 10346, checksum 535996332
20 arrays of 10^5: beauties sum to 24680, checksum 99151538
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: for every value v the numbers can reach, the numbers whose
reach `[x - k, x + k]` holds v counted, and the beauty the most for any
v; no sorting. It draws 2000 random arrays of 1 to 12 numbers from 0 to
20 with k from 0 to 5, then 50 of up to 2000 numbers up to `10^5` with
k up to 1000 or up to `10^5`, all before any arm answers; the literal
reading is asked only of the first 2000.

| | property |
|---|---|
| P1 | up to 12 numbers, the answer is the literal reading's |
| P2 | every number 1000 more: the same answer |
| P3 | k one more: no less |
| P4 | the numbers reversed: the same answer |
| P5 | from the most repeats of one number to n, and n when 2k reaches from the least number to the greatest |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 789130379, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases by the same values gives the same checksum.
On a failure it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the window held to k, not 2k | P1 1008, P5 95, P6 1057 |
| M2 | ★: the numbers left unsorted | P1 1439, P4 1333, P6 1472 |
| M3 | sweep: each reach ended one value early | P1 777, P5 351, P6 778 |
| M4 | sweep: the reach started at x, not x - k | P1 1008, P5 95, P6 1057 |
| M5 | search: the window's top end left out | P1 777, P5 351, P6 778 |
| M6 | search: every window counted one more | P1 2000, P5 317, P6 2050 |
| M7 | events: an end put at x + k, so it closes before a start there | P1 777, P5 351, P6 778 |
| M8 | events: the starts and ends left in the order made | P1 1620, P5 1215, P6 1670 |
| M9 | solution: a gap of 2k + 1 let into the window | P1 619, P6 621 |
| M10 | solution: the left end never moved | P1 1700, P6 1733 |

## Benchmarks

The bench draws 20 arrays of `10^5` numbers up to `10^5`, LeetCode's
most, with k up to 1000, all of them first, then answers each 10 times
by the ★ arm in all five languages, every answer sorting its own copy:
Kāra's `sort`, Rust's `sort`, Go's `slices.Sort`, Python's `sorted` and
C's `qsort`. Every implementation prints `20 arrays of 10^5, 10 rounds:
beauties sum to 220500, checksum 136003588`.

BENCHTAB

## Verification

All five arms print the same output as `beauty.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as first written.

LeetCode's Rust template took 12 `karac fix` edits, the wrapper
included: `struct Solution {}` added; Rust's `mut nums: Vec<i32>`
parameter became `nums: own Vec[i32]` with `let mut nums = nums;` at the
body's start; the `Vec<..>`s became `Vec[..]`; `sort_unstable` became
`sort`; the wrapper's `&Vec<i64>` became `ref Vec[i64]`; the `&x`
pattern dropped its `&`; and `Solution::` became `Solution.`, with the
wrapper's `as i64` dropped. The method's `ans as i32` stayed, the window
being counted in `i64`.
