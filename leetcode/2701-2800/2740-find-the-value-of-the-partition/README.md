# 2740. Find the Value of the Partition

You are given a **positive** integer array `nums`.

Partition `nums` into two arrays, `nums1` and `nums2`, such that:

- Each element of the array `nums` belongs to either the array `nums1`
  or the array `nums2`.
- Both arrays are **non-empty**.
- The value of the partition is **minimized**.

The value of the partition is `|max(nums1) - min(nums2)|`.

Here, `max(nums1)` denotes the maximum element of the array `nums1`, and
`min(nums2)` denotes the minimum element of the array `nums2`.

Return *the integer denoting the value of such partition.*

```
nums = [1, 3, 2, 4]  ->  1
nums = [100, 1, 10]  ->  9
```

**Constraints:** `2 <= nums.length <= 10^5`, `1 <= nums[i] <= 10^9`.

## Approaches

Whatever the partition, `max(nums1)` and `min(nums2)` are two numbers of
the array, so its value is at least the least difference between two of
them; and cutting the sorted array between those two reaches it. The
answer is the least gap between neighbours in sorted order.

| file | mechanism |
|---|---|
| `partition.kara` ★ | the array taken `own`, sorted in place, and the least gap between neighbours. O(n log n) |
| `partition_radix.kara` | a least-significant-byte radix sort, a counting pass for each of the four bytes a number up to `10^9` has, between two buffers swapped by `mem.swap`, then the least gap. O(n) |
| `partition_set.kara` | the numbers put in a `SortedSet` one at a time: a number already there makes the answer 0, and otherwise its new neighbours, the last of a `range` below it and the first of a `range_inclusive` above, are the only gaps it can narrow. O(n log n) |
| `partition_pairs.kara` | no sorting: the least difference over every two numbers. O(n^2) |
| `partition_solution.kara` | a Rust solution as LeetCode's Rust users write it, `mut nums` sorted by `sort_unstable`, then `windows(2)`, `map` and `min`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; two equal
numbers; the two ends of LeetCode's range; 50 numbers spread evenly, so
that every gap is the answer; 2000 random arrays of 2 to 20 numbers up to
100; and 20 of 2000 numbers up to `10^9`, each batch with the sum of its
answers and a checksum. `partition.py` mirrors the ★ arm and its output
is byte-identical.

```
1
9
0
999999999
7
2000 small arrays: values sum to 6870, checksum 735782987
20 arrays of 2000 numbers: values sum to 5608, checksum 846866227
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every way of putting each number in `nums1` or `nums2`, both
non-empty, as the bits of a number, with `|max(nums1) - min(nums2)|`
taken over each; no sorting and no pairs. It draws 1500 random arrays of
2 to 10 numbers up to 30, then 300 of up to 300 numbers up to `10^9`, all
before any arm answers; the literal reading is asked only of the first
1500.

| | property |
|---|---|
| P1 | up to 10 numbers, the answer is the literal reading's |
| P2 | the numbers reversed: the same answer |
| P3 | a number added to every number: the same answer |
| P4 | the answer at most `10^9`, and every number doubled: the answer doubled |
| P5 | one of the numbers listed twice: 0 |
| P6 | each arm agrees with at least three of the other four |

The differential prints `1800 cases: checksum 15044749, 54000 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases, over every split by bits, gives the same
checksum. On a failure it prints the first ten and then the count by
property.

P4 doubles rather than triples: the solution arm narrows to `i32` as
LeetCode's signature does, and Kāra's `as` refuses at run time a number
that does not fit, where Rust's wraps; three times `10^9` does not fit.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. M3 and M4 fail no small case: with numbers up
to 30, only the lowest byte differs, and that byte is sorted.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the first gap never looked at | P1 405, P4 172, P5 213, P6 411 |
| M2 | ★: each number against the one halfway back | P1 577, P5 951, P6 865 |
| M3 | radix: three bytes sorted, not four | P4 197, P5 298, P6 298 |
| M4 | radix: every pass on the lowest byte | P2 196, P3 10, P4 182, P5 297, P6 297 |
| M5 | set: a repeated number not taken as 0 | P1 613, P4 6, P5 1800, P6 613 |
| M6 | set: the neighbour above never asked | P1 377, P2 1012, P4 122, P6 532 |
| M7 | pairs: each number paired with itself too | P1 887, P6 1187 |
| M8 | pairs: the last number never paired | P1 531, P2 571, P4 172, P5 201, P6 541 |
| M9 | solution: the array left unsorted | P1 1381, P2 1720, P5 1681, P6 1679 |
| M10 | solution: the widest gap taken | P1 1323, P5 1794, P6 1619 |

P4 asks first that the answer is at most `10^9`, the largest a gap can
be, so that an arm that gives up with `i64.MAX`, as M1, M5, M6 and M8 do
on two numbers, fails a check rather than overflowing the doubling.

## Benchmarks

The bench draws 20 arrays of `10^5` numbers up to `10^9`, LeetCode's
most, all of them first, then answers each 10 times by the ★ arm in all
five languages, each time on a fresh copy, so that the sort does the
work every time. C sorts with `qsort`, Go with `slices.Sort`, Rust and
Kāra with `sort` and Python with `sorted`. Every implementation prints
`20 arrays of 100000 numbers, 10 rounds: values sum to 40, checksum
605162868`; with `10^5` numbers up to `10^9`, most arrays hold two equal
numbers, so most answers are 0.

BENCHTAB

## Verification

All five arms print the same output as `partition.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The ★ and pairs arms checked clean as first written. The radix arm
wrote Rust's `std.mem.swap(..)`; `karac check` says Kāra's library needs
no `std` path, and `karac fix` made it `mem.swap`. The set arm wrote
Rust's `seen.range(..x).next_back()` and `seen.range(x + 1..).next()`;
`karac check` says Kāra's `range` takes both ends, with no fix, since
which end to name is the writer's choice, and the arm names `i64.MIN`
and `i64.MAX`, the first as `range(i64.MIN, x).rev().next()`.

LeetCode's Rust template took one `karac fix` of 10 edits, the wrapper
included: `struct Solution {}` added; `mut nums: Vec<i32>` became `nums:
own Vec[i32]` with a `let mut nums = nums;`; `sort_unstable` became
`sort`; `windows(2)` gained `.into_iter()`, since Kāra's `windows` gives
a `Vec` of slices; and in the wrapper the `&x` pattern dropped its `&`,
`Solution::` became `Solution.` and the `as i64` dropped.
