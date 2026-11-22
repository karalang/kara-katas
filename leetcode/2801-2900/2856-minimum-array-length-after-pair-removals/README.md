# 2856. Minimum Array Length After Pair Removals

You are given a **0-indexed sorted** array of integers `nums`.

You can perform the following operation any number of times:

- Choose **two** indices, `i` and `j`, where `i < j`, such that
  `nums[i] < nums[j]`.
- Then, remove the elements at indices `i` and `j` from `nums`. The
  remaining elements retain their original order, and the array is
  re-indexed.

Return *an integer that denotes the **minimum** length of* `nums`
*after performing the operation any number of times (**including
zero**).*

Note that `nums` is sorted in **non-decreasing** order.

```
nums = [1,3,4,9]  ->  0
nums = [2,3,6,9]  ->  0
nums = [1,1,2]    ->  1
```

**Constraints:** `1 <= nums.length <= 10^5`; `1 <= nums[i] <= 10^9`;
`nums` is sorted in non-decreasing order.

## Approaches

| file | mechanism |
|---|---|
| `length.kara` ★ | any two different values can go together, so only the commonest value can be left over: with m of it among n, more than half leaves 2m - n of it, and otherwise everything pairs off but one when n is odd; the array is sorted, so m is the longest run |
| `length_pointers.kara` | two pointers: each value of the first half paired greedily with the next larger value of the second half; every pair made takes two away |
| `length_heap.kara` | the removals played out: the count of each value in a `Map`, the counts in a `PriorityQueue.max_first()`, and the two largest taken one from each while two different values are left |
| `length_middle.kara` | a value in more than half the places of a sorted array must hold the middle one, so only `nums[n / 2]` is counted, its two ends found with `partition_point`, and the ★'s rule settles it |
| `length_solution.kara` | a Rust solution as LeetCode's Rust users write it: a `HashMap<i32, usize>` of counts by `*cnt.entry(x).or_insert(0) += 1`, the largest by `values().max().unwrap()`, and the rule on it, `(2 * mx - n) as i32` or `(n % 2) as i32`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 4 lines: LeetCode's three examples and one
element; 10^5 of one value, LeetCode's most, and 10^5 with one value
in 50001 places; then 3000 random sorted arrays of 1 to 8 values up
to 4, and 40 of up to 10^5 values from 1 to k for k up to 1000, one
time in four with a run of one value up to 10^9 making up to three
quarters, as a total left and a checksum. `length.py` mirrors the ★
arm and its output is byte-identical.

```
0 0 1 1
100000 2
3000 short arrays: 2272 left, checksum 705874745
40 long arrays: 22 left, checksum 55920335
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every pair i < j with nums[i] < nums[j] tried as the
next removal, a search over the arrays that can be left, each seen
once in a `Map[String, i64]` keyed by its values written out, to the
shortest reachable. It draws 2000 random sorted arrays of 1 to 8
values up to 4, then 50 of up to 3000 values, one time in four with a
long run of one value, all before any arm answers; the literal reading
is asked only of the first 2000.

| | property |
|---|---|
| P1 | up to 8 values, the answer is the literal reading's |
| P2 | every value doubled: the same answer |
| P3 | a value below all and one above all added: max(a - 2, n % 2) |
| P4 | every value v made 10^9 + 1 - v and the array reversed: the same answer |
| P5 | from 0 to n, and as even as n |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 52781957, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a
Python reading of the same cases gives the same checksum. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. Three first drafts, of M2, M3 and M7, left
every answer as it was, equivalent to the arm, and were replaced by the
edits listed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the run not reset at a new value | P1 1677, P3 2050, P6 1727 |
| M2 | ★: an odd length with no majority left at 0 | P1 418, P3 959, P5 447, P6 447 |
| M3 | pointers: the second pointer not moved past a pair | P1 85, P3 14, P4 133, P6 88 |
| M4 | pointers: equal values allowed to pair | P1 232, P6 236 |
| M5 | heap: the second count put back before it is spent | P1 475, P3 475, P5 475, P6 495 |
| M6 | heap: what is left counted as one | P1 232, P3 19, P5 190, P6 236 |
| M7 | middle: the middle value's count one short | P1 232, P6 236 |
| M8 | middle: the upper end stopping before the middle value | P1 232, P6 236 |
| M9 | solution: odd length not left with one | P1 418, P3 959, P5 447, P6 447 |
| M10 | solution: the excess counted once, not twice | P1 232, P3 22, P5 219, P6 236 |

## Benchmarks

The bench draws 5000 sorted arrays of 1000 values, each from 1 to k for
k up to 1000, one time in four with a run of one value making up to
three quarters, all of them first, then answers each 50 times by the ★
arm in all five languages. C lays the arrays end to end in one
allocation and sorts with `qsort`. Every implementation prints `5000
arrays, 50 rounds: 5210400 left, checksum 194518776`.

BENCHTAB

## Verification

All five arms print the same output as `length.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as first written. The differential's
`[0].iter().cloned().chain(nums.iter())` drew an associated-type
error, `VecIter[i64]` having `Item = ref i64` where `i64` is wanted,
as Rust's E0271 says too; `nums.iter()` took `.cloned()`.

LeetCode's Rust template took 17 `karac fix` edits in one run, the
wrapper included: `use std::collections::HashMap` became `struct
Solution {}`, Kāra's `Map` needing no import; `Vec<..>` and
`HashMap<i32, usize>` became `Vec[..]` and `Map[i32, i64]`;
`HashMap::new` became `Map.new`; `for &x in &nums` became `for x in ref
nums`; `|&x|` lost its `&`; `Solution::` took `.`, and the wrapper's
`as i64` went, an `i32` widening. `*cnt.values().max().unwrap()` and
`(2 * mx - n) as i32` were accepted as written.
