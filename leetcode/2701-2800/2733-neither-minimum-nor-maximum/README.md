# 2733. Neither Minimum nor Maximum

Given an integer array `nums` containing **distinct positive** integers,
find and return **any** number from the array that is neither the
minimum nor the maximum value in the array, or **`-1`** if there is no
such number.

Return *the selected integer.*

```
nums = [3, 2, 1, 4]  ->  2 or 3
nums = [1, 2]        ->  -1
nums = [2, 1, 3]     ->  2
```

**Constraints:** `1 <= nums.length <= 100`, `1 <= nums[i] <= 100`, all
the integers of `nums` are distinct.

## Approaches

| file | mechanism |
|---|---|
| `neither.kara` ★ | one pass for the least and the greatest, a second for the first number that is neither; with the numbers distinct there is one exactly when there are three or more. O(n) |
| `neither_three.kara` | any three distinct numbers hold one that is neither the array's least nor its greatest: the middle of the first three, sorted as an `Array[i64, 3]`. O(1) |
| `neither_sort.kara` | a sorted copy has the least first and the greatest last, so its second number is neither, given three or more. O(n log n) |
| `neither_find.kara` | the least and the greatest by `min` and `max`, then `find` for a number that is neither, and `unwrap_or(-1)`. O(n) |
| `neither_solution.kara` | a Rust solution as LeetCode's Rust users write it, `nums[..3].to_vec()` sorted and its middle returned, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

The arms may name different numbers: on `[3, 2, 1, 4]` the ★ and find
arms name 3 and the others 2. The output therefore checks each answer
rather than printing it: an answer must be a number of the array that is
neither its least nor its greatest, or -1 exactly when there is none.

Every arm prints the same 4 lines: whether its answer to LeetCode's first
example is right; the other two examples, each with one answer only; and
5000 random arrays, a quarter of 1 to 3 distinct numbers and the rest of
1 to 100, from 1 to 100, with how many had an answer, how many answers
were wrong, and a checksum of which had one. `neither.py` mirrors the ★
arm and its output is byte-identical.

```
true
-1
2
5000 arrays: 4116 with an answer, 0 wrong, checksum 53935129
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: a number may be answered when some number of the array is
below it and some above it, with no least or greatest found. It draws
2000 random arrays of 1 to 10 distinct numbers from 1 to 100, then 500
of 1 to 100, all before any arm answers.

| | property |
|---|---|
| P1 | the answer is one the literal reading allows, and -1 exactly when it allows none |
| P2 | the array reversed: a number named or not, the same |
| P3 | every number x made 101 - x: a number named or not, the same, and the number named there allowed there |
| P4 | every number doubled: a number named or not, the same |
| P5 | a number is named exactly when there are three or more |
| P6 | each arm agrees with at least three of the other four on whether a number is named |

The differential prints `2500 cases: checksum 329608782, 75000 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. M1, M2 and M8 fail the same checks: each lets
the greatest number through as an answer, the first number that is not
the least.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the greatest kept as the least | P1 642, P3 629, P5 216, P6 216 |
| M2 | ★: the greatest let through | P1 642, P3 629, P5 216, P6 216 |
| M3 | three: the last of the three taken | P1 899, P3 930 |
| M4 | three: the three never sorted | P1 575, P3 575 |
| M5 | sort: the least taken | P1 2081, P3 2081 |
| M6 | sort: two numbers taken as enough | P1 216, P3 216, P5 216, P6 216 |
| M7 | find: 0 for none | P1 419, P3 419, P5 419, P6 419 |
| M8 | find: the greatest found by `min` | P1 642, P3 629, P5 216, P6 216 |
| M9 | solution: the least of the three taken | P1 930, P3 899 |
| M10 | solution: two numbers sliced off, not three | P1 630, P3 607 |

## Benchmarks

The bench draws 2000 arrays of 1 to 100 distinct numbers from 1 to 100,
LeetCode's bounds, all of them first, then answers each 3000 times by
the ★ arm's two passes in all five languages. Every implementation
prints `2000 arrays, 3000 rounds: answers sum to 305805000, checksum
450197362`.

BENCHTAB

## Verification

All five arms print the same output as `neither.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as first written.

LeetCode's Rust template took one `karac fix` of 8 edits, the wrapper
included: `struct Solution {}` added, `Vec<i32>` became `Vec[i32]`, and
in the wrapper the `&x` pattern dropped its `&`, `Solution::` became
`Solution.` and the `as i64` dropped. `nums[..3].to_vec()` is Kāra as it
stands.
