# 2762. Continuous Subarrays

You are given a **0-indexed** integer array `nums`. A subarray of `nums`
is called **continuous** if:

- Let `i`, `i + 1`, ..., `j` be the indices in the subarray. Then, for
  each pair of indices `i <= i1, i2 <= j`, `0 <= |nums[i1] - nums[i2]| <=
  2`.

Return *the total number of **continuous** subarrays.*

A subarray is a contiguous **non-empty** sequence of elements within an
array.

```
nums = [5, 4, 2, 4]  ->  8
nums = [1, 2, 3]     ->  6
```

**Constraints:** `1 <= nums.length <= 10^5`, `1 <= nums[i] <= 10^9`.

## Approaches

A subarray is continuous when its greatest and least lie at most 2
apart, and every subarray of a continuous one is continuous too, so for
each right end the continuous subarrays ending there are those starting
from some left end on: the answer is the sum of those windows' lengths.

| file | mechanism |
|---|---|
| `continuous.kara` ★ | two `VecDeque`s of indices, the values rising in one and falling in the other, so their fronts are the window's least and greatest, popped at the back by `while let Some(back) = .. .back()`; the window shrinks from the left while the fronts lie more than 2 apart. O(n) |
| `continuous_map.kara` | the window's values counted in a `SortedMap`, its least and greatest by `first` and `last` through `let .. else`; a value's count taken down as the window shrinks and the key removed at 0. O(n) |
| `continuous_last.kara` | the window ending at right - 1 already rules out every earlier pair, so the new left end only has to pass the last index of any value more than 2 from the new one: a `Map` of the last index of each value in the window, at most three keys, trimmed by `retain`. O(n) |
| `continuous_sparse.kara` | sparse tables of the least and greatest of every stretch of `2^k` numbers in a `struct Sparse`, each row built from the one before by `map` and `collect`; any range's span from two overlapping stretches, and two pointers. O(n log n) |
| `continuous_solution.kara` | a Rust solution as LeetCode's Rust users write it, a `BTreeMap<i32, i32>` of counts by `*freq.entry(x).or_insert(0) += 1`, the least and greatest by `keys().next()` and `keys().next_back()`, and a count taken down through `get_mut`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples; one number;
neighbours 3 apart, so only the single numbers; `10^5` equal numbers,
LeetCode's most; `10^5` rising by 1; 3000 random arrays of 1 to 30
numbers from 1 to 6; and 20 random walks of `10^5` steps of -1, 0 or 1,
the last two with the sum of the answers and a checksum.
`continuous.py` mirrors the ★ arm and its output is byte-identical.

```
8
6
1
4
5000050000
299997
3000 small arrays: subarrays sum to 107857, checksum 526484705
20 walks of 100000: subarrays sum to 17957345, checksum 57609221
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every pair `i <= j`, counted when every two numbers in
`nums[i..=j]` lie at most 2 apart, each pair of indices asked by `all`
in turn; no window. It draws 2000 random arrays of 1 to 12 numbers from
1 to 6, then 100 of up to 2000 numbers, a walk of steps from -2 to 2,
all before any arm answers; the literal reading is asked only of the
first 2000.

| | property |
|---|---|
| P1 | up to 12 numbers, the answer is the literal reading's |
| P2 | every number 1000 more: the same answer |
| P3 | the numbers reversed: the same answer |
| P4 | every number x made `10^9 + 1 - x`: the same answer |
| P5 | from n to n (n + 1) / 2; and a number 3 above the greatest put at the end: one more |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2100 cases: checksum 415451572, 63000 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases by the same `all`s gives the same checksum. On
a failure it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the deque of least values kept falling | P1 1559, P5 2100, P6 1659 |
| M2 | ★: a window 3 apart let stand | P1 1304, P5 715, P6 1404 |
| M3 | map: a window 2 apart taken as too wide | P1 1337, P6 1437 |
| M4 | map: the least read by `last`, so the window never shrinks | P1 1559, P5 2100, P6 1659 |
| M5 | last: only values above the new one ruled out | P1 1352, P3 1506, P4 1506, P5 2100, P6 1452 |
| M6 | last: the left end put on the far value itself | P1 1559, P3 1192, P5 2100, P6 1659 |
| M7 | sparse: the second stretch put at the range's start | P1 1348, P3 1141, P5 1449, P6 1448 |
| M8 | sparse: the greatest from the first stretch alone | P1 1011, P3 1147, P4 1311, P5 1401, P6 1111 |
| M9 | solution: the least key taken for the greatest | P1 1559, P5 2100, P6 1659 |
| M10 | solution: each right end counted one short | P1 2000, P5 2100, P6 2100 |

## Benchmarks

The bench draws 20 random walks of `10^5` numbers, LeetCode's most,
with steps from -2 to 2, all of them first, then answers each 10 times
by the ★ arm in all five languages: the deques are `VecDeque` in Kāra
and Rust, `collections.deque` in Python, and an array or slice with a
head index in C and Go. Every implementation prints `20 walks of 100000,
10 rounds: subarrays sum to 83411090, checksum 230950379`.

BENCHTAB

## Verification

All five arms print the same output as `continuous.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as first written. The differential
first passed `nums.clone()` to each arm, and `karac check` warned that
the parameter only borrows it; the clones went.

LeetCode's Rust template took 16 `karac fix` edits, the wrapper
included: `use std::collections::BTreeMap` became `struct Solution {}`;
`Vec<i32>` and `Vec<i64>` became `Vec[i32]` and `Vec[i64]`;
`BTreeMap<i32, i32>` and `BTreeMap::new()` became `SortedMap[i32, i32]`
and `SortedMap.new()`; the `&nums[left]` arguments dropped their `&`;
`(right - left + 1) as i64` lost its cast, `nums.len()` being an `i64`
here; the `&x` pattern dropped its `&`; and `Solution::` became
`Solution.`. The `entry(..).or_insert(0)`, `keys().next_back()` and
`get_mut` stayed as written, though the `SortedMap` table in kara's
library reference listed neither `entry` nor `get_mut`; that was kara
`B-2026-11-20-145`, fixed at `0d28296389`.
