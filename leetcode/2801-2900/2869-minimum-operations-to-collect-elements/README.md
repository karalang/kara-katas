# 2869. Minimum Operations to Collect Elements

You are given an array `nums` of positive integers and an integer `k`.

In one operation, you can remove the last element of the array and add
it to your collection.

Return *the **minimum number of operations** needed to collect elements*
`1, 2, ..., k`.

```
nums = [3,1,5,4,2], k = 2  ->  4
nums = [3,1,5,4,2], k = 5  ->  5
nums = [3,2,5,3,1], k = 3  ->  4
```

**Constraints:** `1 <= nums.length <= 50`; `1 <= nums[i] <=
nums.length`; `1 <= k <= nums.length`; the input is generated such that
you can collect elements `1, 2, ..., k`.

## Approaches

| file | mechanism |
|---|---|
| `collect.kara` ★ | the values are taken from the end, so walk from the right, setting bit v of a mask for each v up to k, and stop when all k bits are set |
| `collect_set.kara` | the values up to k gathered into a `Set` from the right, counting operations until it holds k of them |
| `collect_last.kara` | each value's last place in one pass from the left; every value up to k must be taken, so the walk from the end reaches the earliest of those last places, and the operations are n less it |
| `collect_search.kara` | for each value from 1 to k, `rposition` finds its last place, and the earliest of them is where the walk must reach |
| `collect_solution.kara` | a Rust solution as LeetCode's Rust users write it: a `HashSet` filled from `nums.iter().rev().enumerate()`, returning `i as i32 + 1` once it holds `k as usize` values, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 4 lines: LeetCode's three examples; 50
values, LeetCode's most, falling with k = 50 and rising with k = 25;
then 3000 random arrays of 1 to 8 values from 1 to n and 3000 of 50,
each holding 1, with k drawn from those whose 1..k all appear, as a
total of operations and a checksum. `collect.py` mirrors the ★ arm and
its output is byte-identical.

```
4 5 4
50 50
3000 short arrays: 7813 operations, checksum 432604666
3000 long arrays: 74034 operations, checksum 261672105
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: the last value taken off and put in a collection, one
operation at a time, until the collection holds every value from 1 to
k. It draws 2000 random arrays of 1 to 8 values from 1 to n, then 50 of
50, each holding 1, with k drawn as the harness draws it, all before
any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | a value above k put at the end: one more |
| P3 | a value from 1 to k put at the front: the same answer |
| P4 | from k to n |
| P5 | k one less: no more |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases, 6265 operations: checksum
683695316, 61500 checks over 5 arms: 0 failures` under every lane in
Verification, and a Python reading of the same cases gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the full mask one bit short | P1 1667, P2 1403, P3 1129, P4 165, P5 181, P6 1667 |
| M2 | ★: the operations counted one short | P1 2050, P4 995, P6 2050 |
| M3 | set: values above k gathered too | P1 982, P2 1975, P6 982 |
| M4 | set: the walk stopped one value early | P1 1808, P2 1403, P3 788, P4 374, P5 141, P6 1808 |
| M5 | last: each value's first place kept | P1 1068, P3 2050, P6 1068 |
| M6 | last: the latest of the last places taken | P1 647, P4 481, P5 267, P6 647 |
| M7 | search: the first place found, not the last | P1 1068, P3 2050, P6 1068 |
| M8 | search: k left out | P1 306, P4 165, P6 306 |
| M9 | solution: values above k gathered too | P1 982, P2 1975, P6 982 |
| M10 | solution: the operation not counted on the stop | P1 2050, P4 995, P6 2050 |

## Benchmarks

The bench draws 50000 arrays of 50 values, LeetCode's most, each with
its k, all of them first, then answers each 20 times by the ★ arm in
all five languages. Every implementation prints `50000 arrays of 50, 20
rounds: 24187320 operations, checksum 777137872`.

BENCHTAB

## Verification

All five arms print the same output as `collect.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as first written. The differential, as
first written, built its front value as `(c as i64) % k + 1`, and `karac
check` warned that the cast was redundant, `c` from `enumerate` being an
`i64` already; the cast was taken off.

LeetCode's Rust template took 14 `karac fix` edits in one run, the
wrapper included: `use std::collections::HashSet;` became `struct
Solution {}`, the import going and `HashSet::new()` becoming
`Set.new()`; `Vec<..>` became `Vec[..]`; `(i, &x)` lost its `&`; `k as
usize` lost its cast, and so did the wrapper's `as i64`, both widenings;
`|&x|` lost its `&`, and `Solution::` took `.`. `return i as i32 + 1`
and `nums.len() as i32` were accepted as written.
