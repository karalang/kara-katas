# 2863. Maximum Length of Semi-Decreasing Subarrays

You are given an integer array `nums`.

Return *the length of the **longest semi-decreasing** subarray of*
`nums`*, and* `0` *if there are no such subarrays.*

- A **subarray** is a contiguous non-empty sequence of elements within
  an array.
- A non-empty array is **semi-decreasing** if its first element is
  **strictly greater** than its last element.

```
nums = [7,6,5,4,3,2,1,6,10,11]              ->  8
nums = [57,55,50,60,61,58,63,59,64,60,63]   ->  6
nums = [1,2,3,4]                            ->  0
```

**Constraints:** `1 <= nums.length <= 10^5`; `-10^9 <= nums[i] <=
10^9`.

## Approaches

| file | mechanism |
|---|---|
| `semi.kara` ★ | the best start for any end is a value larger than everything before it, so the starts worth trying are the prefix maxima, kept on a stack in rising order; walking the ends from the right, each start above the end's value is matched with it, the furthest end it can have, and popped |
| `semi_sorted.kara` | the indices sorted by value, largest first, with `sort_by`; walking down the values, the smallest index among strictly larger values is the best start for every index of the current value, equal values taken as one group |
| `semi_search.kara` | suffix minima: low[j], the least value from j to the end, never falls as j moves right, so for each start the furthest end with a smaller value is found by `partition_point` on low |
| `semi_pointers.kara` | two pointers over prefix maxima and suffix minima, both rising: a stretch from i to j holds a start above an end exactly when high[i] > low[j], and j only moves right as i does |
| `semi_solution.kara` | a Rust solution as LeetCode's Rust users write it: a `Vec<usize>` stack of the prefix maxima, then `for j in (0..n).rev()` popping with `while let Some(&i) = stk.last()` and `ans.max((j - i + 1) as i32)`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 4 lines: LeetCode's three examples; 10^5
values falling, LeetCode's most, 10^5 rising and 10^5 equal; then 3000
random arrays of 1 to 8 values from 0 to 5, and 30 of 10^4 to 10^5,
every other one random over LeetCode's range and the rest rising with
five values moved, as a total of lengths and a checksum. `semi.py`
mirrors the ★ arm and its output is byte-identical.

```
8 6 0
100000 0 0
3000 short arrays: lengths total 10282, checksum 704880595
30 long arrays: lengths total 1386642, checksum 176726232
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every subarray from i to j > i tried, kept when its
first value is strictly greater than its last, and the longest taken.
It draws 2000 random arrays of 1 to 12 values from 0 to 6, then 50 of
up to 500, every other one rising with three values moved, all before
any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the array reversed and negated: the same answer |
| P3 | every value v made 2v + 1: the same answer |
| P4 | a value above all of them put first: n + 1 |
| P5 | 0 exactly when the array never falls, else from 2 to n |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases, lengths total 20210: checksum
126812935, 61500 checks over 5 arms: 0 failures` under every lane in
Verification, and a Python reading of the same cases gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. Two first drafts of M7 left every answer as it
was, equivalent to the arm, and were replaced.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: one short of the length | P1 1712, P4 2050, P5 181, P6 1712 |
| M2 | ★: an equal end taken as smaller | P1 755, P5 338, P6 755 |
| M3 | sorted: the smallest value first | P1 1718, P4 2050, P5 270, P6 1718 |
| M4 | sorted: an equal value's index taken in before its group is scored | P1 498, P5 81, P6 498 |
| M5 | search: an end allowed to equal the start's value | P1 498, P5 81, P6 498 |
| M6 | search: the suffix minimum taken from the wrong side | P1 1260, P2 723, P5 1123, P6 1260 |
| M7 | pointers: a first value equal to the last allowed | P1 171, P2 329, P5 108, P6 171 |
| M8 | pointers: the end held back one place | P1 1111, P2 686, P4 2050, P5 120, P6 1111 |
| M9 | solution: an end equal to the start accepted | P1 755, P5 338, P6 755 |
| M10 | solution: one short of the length | P1 1712, P4 2050, P5 181, P6 1712 |

## Benchmarks

The bench draws 100 arrays of 10^5 values, LeetCode's most, every other
one random over LeetCode's range and the rest rising with five values
moved, all of them first, then answers each 10 times by the ★ arm in
all five languages; C keeps the stack in one array allocated once.
Every implementation prints `100 arrays of 100000, 10 rounds: lengths
total 83622580, checksum 110242461`.

BENCHTAB

## Verification

All five arms print the same output as `semi.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The ★ arm, as first written, popped with Rust's `while let Some(&i) =
starts.last()`, and `karac check` reported E0001, the `&` pattern
copying a value out of a borrowed `Some`; `karac fix` wrote `while let
Some(i) = starts.last().cloned()`. The other arms checked clean.

LeetCode's Rust template took 16 `karac fix` edits in one run, the
wrapper included: `struct Solution {}` added for the `impl`; `Vec<..>`
became `Vec[..]` and `Vec<usize>` became `Vec[i64]`; `vec![]` became
`Vec.new()`; `||` became `or`; `let mut ans = 0` took `: i32`; `Some(&i)
= stk.last()` became `Some(i) = stk.last().cloned()`; `|&x|` lost its
`&`; `Solution::` took `.`, and the wrapper's `as i64` went, an `i32`
widening. `nums[*stk.last().unwrap()]` and `(j - i + 1) as i32` were
accepted as written.
