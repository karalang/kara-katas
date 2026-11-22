# 2780. Minimum Index of a Valid Split

An element `x` of an integer array `arr` of length `m` is **dominant**
if **more than half** the elements of `arr` have a value of `x`.

You are given a **0-indexed** integer array `nums` of length `n` with
one **dominant** element.

You can split `nums` at an index `i` into two arrays `nums[0, ..., i]`
and `nums[i + 1, ..., n - 1]`, but the split is only **valid** if:

- `0 <= i < n - 1`
- `nums[0, ..., i]`, and `nums[i + 1, ..., n - 1]` have the same
  dominant element.

Here, `nums[i, ..., j]` denotes the subarray of `nums` starting at index
`i` and ending at index `j`, both ends being inclusive. Particularly, if
`j < i` then `nums[i, ..., j]` denotes an empty subarray.

Return *the **minimum** index of a **valid split***. If no valid split
exists, return `-1`.

```
nums = [1, 2, 2, 2]                    ->  2
nums = [2, 1, 3, 1, 1, 1, 7, 1, 2, 1]  ->  4
nums = [3, 3, 3, 3, 7, 2, 2]           ->  -1
```

**Constraints:** `1 <= nums.length <= 10^5`, `1 <= nums[i] <= 10^9`,
`nums` has exactly one dominant element.

## Approaches

A number more than half of each part is more than half of the whole, so
the one number a valid split can share is the whole array's dominant x;
a split at i is valid when x is more than half of the i + 1 numbers on
the left and of the n - i - 1 on the right.

| file | mechanism |
|---|---|
| `split.kara` ★ | x found by Boyer-Moore's vote and counted by `filter`, then the first split where x is more than half of each side, the left's count kept as the scan goes. O(n) |
| `split_counts.kara` | every number counted in a `Map` through `entry`, x the one `find` meets held more than n / 2 times, then the same scan. O(n) |
| `split_sorted.kara` | no counting table: x fills the middle of a sorted copy, and its count is the length of its run there, found by `partition_point` either side; then the same scan. O(n log n) |
| `split_sides.kara` | nothing known of the whole first: two `Map`s of counts, the right side's filled, and each number moved from right to left in turn; the left's counts only grow, so its most common number is kept as each count passes it, and a split is valid when that number is more than half of both sides. O(n) |
| `split_solution.kara` | a Rust solution as LeetCode's Rust users write it, a `HashMap<i32, i32>` of counts, x taken by `max_by_key` on the count, and a scan over `enumerate` with `cur * 2 > i + 1`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's three examples; one
number; `10^5` numbers, LeetCode's most, all `10^9`, and 49999
different ones before 50001 of the dominant; 3000 random arrays of 1 to
12 numbers from 1 to 4, more than half of them one number; and 20 of
`10^5` numbers up to `10^9`, the last two with the count of arrays that
split, the sum of their indices and a checksum. `split.py` mirrors the
★ arm and its output is byte-identical.

```
2
4
-1
-1
0
99998
3000 small arrays: 2400 split, indices sum to 1044, checksum 415284044
20 arrays of 10^5: 20 split, indices sum to 42, checksum 508795728
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: each split i in turn, the left part and the right part, and
for every number of the left part its count in each part by `filter`;
the split is valid when one number is more than half of both, and the
answer is the first valid one, or -1; no vote and no table. It draws
2000 random arrays of 1 to 12 numbers from 1 to 4 with a dominant one,
then 50 of up to 2000 numbers up to `10^9`, the others drawn from 3
values or from `10^9`, all before any arm answers; the literal reading
is asked only of the first 2000.

| | property |
|---|---|
| P1 | up to 12 numbers, the answer is the literal reading's |
| P2 | every number 1000 more: the same answer |
| P3 | the numbers written twice over: a split, and no later one |
| P4 | the numbers reversed: a split just when there was one |
| P5 | -1 or from 0 to n - 2, -1 for one number, and a split answered has one number more than half of each part |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 944688985, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases by the same counts gives the same checksum.
On a failure it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the dominant counted one short | P1 632, P3 393, P6 633 |
| M2 | ★: a vote for every number, so the first wins | P1 241, P3 337, P4 378, P6 254 |
| M3 | counts: a right part only half the dominant let through | P1 172, P4 104, P5 172, P6 172 |
| M4 | counts: the last split never tried | P1 204, P3 172, P4 76, P6 204 |
| M5 | sorted: the least number taken as the dominant | P1 550, P3 733, P6 599 |
| M6 | sorted: the dominant's run counted from the start | P1 101, P4 63, P5 101, P6 101 |
| M7 | sides: a new leader only two past the old | P1 185, P3 32, P4 63, P6 190 |
| M8 | sides: the right side never giving up a number | P1 185, P3 9, P4 88, P5 185, P6 185 |
| M9 | solution: a left part only half the dominant let through | P1 406, P4 104, P5 420, P6 420 |
| M10 | solution: each split index read one on | P1 1608, P3 221, P4 237, P5 140, P6 1657 |

## Benchmarks

The bench draws 20 arrays of `10^5` numbers up to `10^9`, LeetCode's
most, each with a dominant number, all of them first, then answers each
100 times by the ★ arm in all five languages. Every implementation
prints `20 arrays of 10^5, 100 rounds: indices sum to 1400, checksum
605066010`.

BENCHTAB

## Verification

All five arms print the same output as `split.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

Three of the own arms checked clean as first written. The sides arm
first read each count by Rust's `left.get(leader).copied().unwrap_or(0)`;
`karac check` refused `copied` and named `.cloned()`, or `opt ?? d` for
a `Copy` item. Written `if now > left.get(leader) ?? 0`, it failed
twice: "cannot compare 'i64' and 'Option[ref i64]'", and a `??` over a
`bool` whose help was to drop the fallback. `??` binds loosest of all,
so that is `(now > left.get(leader)) ?? 0`; nothing named the
precedence, and dropping the fallback was the wrong edit. That was kara
`B-2026-11-20-147`, fixed at `0d28296389`: the `??` now says it binds more
loosely than `>`, and `karac fix` writes `now > (left.get(leader) ??
0)`, as the arm now reads.

LeetCode's Rust template took 24 `karac fix` edits, the wrapper
included: `use std::collections::HashMap` became `struct Solution {}`;
the `Vec<..>`s became `Vec[..]`; `HashMap<i32, i32>` became `Map[i32,
i32]`; `for &x in &nums` became `for x in ref nums`; the patterns `(&x,
&total)`, `&c`, `&v` and the wrapper's `|&v|` dropped their `&`; `&&` became `and`; and `Solution::`
became `Solution.`, with the wrapper's `as i64` dropped. The `as i32`
casts on `nums.len()` and the index stayed.
