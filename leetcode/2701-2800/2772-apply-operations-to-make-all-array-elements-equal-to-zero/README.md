# 2772. Apply Operations to Make All Array Elements Equal to Zero

You are given a **0-indexed** integer array `nums` and a positive
integer `k`.

You can apply the following operation on the array **any** number of
times:

- Choose **any** subarray of size `k` from the array and **decrease**
  all its elements by `1`.

Return `true` *if you can make all the array elements equal to* `0`*,
or* `false` *otherwise*.

A **subarray** is a contiguous non-empty part of an array.

```
nums = [2, 2, 3, 1, 1, 0], k = 3  ->  true
nums = [1, 3, 1, 1], k = 2        ->  false
```

**Constraints:** `1 <= k <= nums.length <= 10^5`, `0 <= nums[i] <=
10^6`.

## Approaches

Only how many windows start at each place matters, not their order, and
the first number still above 0 can be brought down only by windows
starting at it: so the count at every start is forced, from the left.

| file | mechanism |
|---|---|
| `zero.kara` ★ | from the left, as many windows start at each place as its number still needs; the windows covering a place are a running sum, each window's count taken off again k places on through a difference array. False when a number falls below 0 or a window would run past the end. O(n) |
| `zero_queue.kara` | the windows still open kept in a `VecDeque` of (place where they end, how many), oldest first, popped from the front by `while let` once they end and pushed on the back as they start. O(n) |
| `zero_fenwick.kara` | the numbers as differences in a Fenwick tree, a `struct Fenwick` with a `mut ref self` add; each place's number as it now stands read by a prefix sum, and the windows started there subtracted as a range by two adds. O(n log n) |
| `zero_back.kara` | the same greedy from the right, a window reversed being a window: the last number still above 0 can be brought down only by windows ending at it, their counts in a `Vec` indexed by where they end. O(n) |
| `zero_solution.kara` | a Rust solution as LeetCode's Rust users write it, `k` taken as a `usize`, a `vec![0i64; n + 1]` difference array and a running sum, each number widened by `as i64`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; a window of
1; `10^5` numbers, LeetCode's most, all `10^6` with a window of all of
them, and the same with one of them 1 less; 3000 random arrays of 1 to
12 numbers built by up to 2 operations at each start, half with one
number moved 1 up or down; and 20 arrays of `10^5` built by up to 9
with windows up to 1000, the last two with the count of true and a
checksum. `zero.py` mirrors the ★ arm and its output is byte-identical.

```
true
false
true
true
false
3000 small arrays: 1869 true, checksum 28624912
20 arrays of 10^5: 11 true, checksum 446089507
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every array reachable by operations, each a window of k
numbers all above 0 taken down by 1, searched from the array given with
the arrays already seen in a `Set`; true when the all-zero array is
among them; no greedy. It draws 2000 random arrays of 1 to 7 numbers
built by up to 2 operations at each start, half with one number moved,
then 50 of up to 3000 built by up to 9 with windows up to 300, all
before any arm answers; the literal reading is asked only of the first
2000.

| | property |
|---|---|
| P1 | up to 7 numbers, the answer is the literal reading's |
| P2 | the numbers reversed: the same answer |
| P3 | every number doubled: the same answer |
| P4 | a window of 1: true |
| P5 | true only when the sum is a multiple of k; and one more operation on the first window: the same answer |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 88000068, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases by the same search gives the same checksum.
On a failure it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. The first M9, a number below 0 let into the
solution arm's window, left every answer the same across the 2050 cases,
so they do not tell it apart; the first M10 overflowed `i64` before any
property was asked. Both were replaced by the two solution edits below.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the windows never taken off where they end | P1 670, P2 297, P4 1186, P5 182, P6 693 |
| M2 | ★: the windows ending at a place taken off as one | P1 395, P2 298, P3 298, P4 665, P5 239, P6 418 |
| M3 | queue: a window kept open one place too long | P1 620, P2 322, P4 699, P5 305, P6 643 |
| M4 | queue: a number below 0 let through | P1 295, P2 315, P5 311, P6 311 |
| M5 | fenwick: the windows started never added back k places on | P1 670, P2 297, P4 1186, P5 182, P6 693 |
| M6 | fenwick: the first number not put in | P1 501, P2 469, P4 648, P5 315, P6 524 |
| M7 | back: a window let start before the first place | P1 118, P2 193, P5 136, P6 118 |
| M8 | back: the windows never dropped k places back | P1 645, P2 297, P4 1175, P5 100, P6 668 |
| M9 | solution: a window's end adding its amount back the wrong way | P1 705, P2 221, P4 1514, P5 140, P6 728 |
| M10 | solution: the first number never asked | P1 513, P2 314, P5 326, P6 536 |

## Benchmarks

The bench draws 20 arrays of `10^5` numbers, LeetCode's most, built by
up to 9 operations at each start of a window up to 1000, half with one
number moved, all of them first, then answers each 40 times by the ★ arm
in all five languages. A false answer stops at the first number that
cannot be met. Every implementation prints `20 arrays of 10^5, 40
rounds: 440 true, checksum 838456822`.

BENCHTAB

## Verification

All five arms print the same output as `zero.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as first written.

LeetCode's Rust template took 13 `karac fix` edits, the wrapper
included: `struct Solution {}` added; the `Vec<..>`s became `Vec[..]`;
`let k = k as usize` became `let k = k as i64`, the window being added
to an index; `vec![0i64; n + 1]` became `Vec.filled(n + 1, 0)`;
`nums[i] as i64` dropped its cast, an `i32` widening as it is; `||`
became `or`; the wrapper's `&Vec<i64>` became `ref Vec[i64]`; the `&x`
pattern dropped its `&`; and `Solution::` became `Solution.`.
