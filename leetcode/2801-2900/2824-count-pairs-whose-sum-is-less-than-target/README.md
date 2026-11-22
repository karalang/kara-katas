# 2824. Count Pairs Whose Sum is Less than Target

Given a **0-indexed** integer array `nums` of length `n` and an integer
`target`, return *the number of pairs* `(i, j)` *where* `0 <= i < j <
n` *and* `nums[i] + nums[j] < target`.

```
nums = [-1,1,2,3,1],         target = 2   ->  3
nums = [-6,2,5,-2,-7,-1,3],  target = -2  ->  10
```

**Constraints:** `1 <= nums.length == n <= 50`; `-50 <= nums[i],
target <= 50`.

## Approaches

| file | mechanism |
|---|---|
| `pairs.kara` ★ | the numbers sorted and two pointers closing in: when the ends sum below the target, the left end pairs with every number up to the right end and moves on, otherwise the right end comes in |
| `pairs_all.kara` | every pair, one expression: for each i, the slice after it filtered by the sum and counted, the counts summed; O(n^2) |
| `pairs_search.kara` | the numbers sorted, and for each i the numbers after it below `target - nums[i]` counted by `partition_point` on the rest of the slice |
| `pairs_counts.kara` | no sort: a fixed `Array[i64, 101]` of counts of the numbers seen so far, the bounds making that enough, and each new number pairs with every count below `target - v` |
| `pairs_solution.kara` | a Rust solution as LeetCode's Rust users write it: the `i32` numbers rebound `mut` and sorted by `sort_unstable`, two pointers in a `(mut i, mut j)` tuple, and `(j - i) as i32` added up, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 6 lines: LeetCode's two examples; one
number; 50 numbers all -50 under a target of 50, every pair; all 50
under -50, no pair; and 5000 random arrays of 1 to 50 numbers from -50
to 50 with targets from -50 to 50, as a total and a checksum.
`pairs.py` mirrors the ★ arm and its output is byte-identical.

```
3
10
0
1225
0
5000 arrays: 1038240 pairs, checksum 280673757
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every pair of indices i < j, counted when the two
numbers sum below the target. It draws 3000 random arrays of 1 to 50
numbers from -50 to 50, with targets from -50 to 50, all before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the numbers reversed: the same answer |
| P3 | the target one higher: no fewer pairs |
| P4 | every number negated and the target `1 - target`: the pairs counted there and here make every pair, `n(n - 1)/2` |
| P5 | every number one higher and the target two higher, or both lower, whichever keeps the numbers in -50..=50: the same answer |
| P6 | each arm agrees with at least three of the other four |

P5 first moved every number up by one, and the counts arm, whose table
holds only -50 to 50, failed on an index out of bounds at 51; the
property now keeps the numbers inside the constraints. P4's target can
reach 51, which every arm takes: the table holds numbers, not targets.

The differential prints `3000 cases: checksum 573283531, 90000 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the left end paired only with the right end | P1 2763, P4 2862, P6 2763 |
| M2 | ★: a sum at the target counted | P1 2036, P4 2310, P6 2036 |
| M3 | all: each number paired with itself too | P1 2913, P4 3000, P6 2913 |
| M4 | all: the pairs counted at or above the target | P1 2903, P3 2036, P6 2903 |
| M5 | search: the rest searched from i itself | P1 2913, P4 3000, P6 2913 |
| M6 | search: the numbers left unsorted | P1 2571, P2 2579, P4 2621, P6 2571 |
| M7 | counts: a number counted before it is paired | P1 2913, P4 3000, P6 2913 |
| M8 | counts: the seen values at the limit counted | P1 2036, P4 2310, P6 2036 |
| M9 | solution: the right end moved on a pair | P1 2667, P4 2755, P6 2667 |
| M10 | solution: one pair fewer for each move | P1 2836, P4 2928, P6 2836 |

## Benchmarks

The bench draws 200000 arrays of 50 numbers from -50 to 50, LeetCode's
most, with targets in the same range, all of them first, then answers
each 5 times by the ★ arm in all five languages, a copy sorted for
every answer. C sorts by `qsort`, Go by `slices.Sort`. Every
implementation prints `200000 arrays of 50, 5 rounds: 608998850 pairs,
checksum 329854672`.

BENCHTAB

## Verification

All five arms print the same output as `pairs.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms and the differential checked clean as first written.

LeetCode's Rust template took 14 `karac fix` edits in one run, the
wrapper included: `struct Solution {}` added for the `impl`; `nums`
became `own Vec[i32]`, since the body rebinds it `mut` and sorts it;
`sort_unstable` became `sort`; `let (mut i, mut j)` became `let mut (i,
j)`; `let mut ans = 0` took `: i32`, since `ans += (j - i) as i32`
leaves the literal at its default `i64` by design (design.md §8: `let
mut b = 0; b += y` with `y: i32` makes `b` an `i64`), and the `i32`
return would then narrow, E0200; `Vec<..>` became `Vec[..]`, `|&v|` lost
its `&`, `Solution::` took `.`, and the wrapper's `as i64` went. The
`(j - i) as i32`, a narrowing from the `i64` index, stays.
