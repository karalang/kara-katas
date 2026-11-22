# 2770. Maximum Number of Jumps to Reach the Last Index

You are given a **0-indexed** array `nums` of `n` integers and an
integer `target`.

You are initially positioned at index `0`. In one step, you can jump
from index `i` to any index `j` such that:

- `0 <= i < j < n`
- `-target <= nums[j] - nums[i] <= target`

Return *the **maximum number of jumps** you can make to reach index*
`n - 1`.

If there is no way to reach index `n - 1`, return `-1`.

```
nums = [1, 3, 6, 4, 1, 2], target = 2  ->  3
nums = [1, 3, 6, 4, 1, 2], target = 3  ->  5
nums = [1, 3, 6, 4, 1, 2], target = 0  ->  -1
```

**Constraints:** `2 <= nums.length == n <= 1000`, `-10^9 <= nums[i] <=
10^9`, `0 <= target <= 2 * 10^9`.

## Approaches

Jumps only go forward, so the indices in order are an order of the
jumps' graph, and the most jumps to an index depend only on the indices
before it.

| file | mechanism |
|---|---|
| `jumps.kara` ★ | the most jumps that reach each index from 0, or -1, each index taking the best of the reached indices before it within target of its number, plus one. O(n^2) |
| `jumps_memo.kara` | the most jumps from each index to the last, or -1, by a recursive call remembered in a `Vec[Option[i64]]`: the last index needs none, any other takes the best of the later indices within target that reach the end, plus one. O(n^2), recursing as deep as n |
| `jumps_push.kara` | the jumps built as a graph first, each index's later indices within target gathered by `filter` and `collect`; then each reached index, in order, pushes its count plus one along its jumps. O(n^2) time and space |
| `jumps_tree.kara` | the numbers sorted and deduplicated, and a segment tree, a `struct MaxTree` with a `mut ref self` method, holding for each number the most jumps of any index so far with it; each index asks the tree for the best over the numbers within target of its own, found by `partition_point`, and puts its own count in. O(n log n) |
| `jumps_solution.kara` | a Rust solution as LeetCode's Rust users write it, a `vec![-1; n]` table and each difference taken in `i64`, `(nums[j] as i64 - nums[i] as i64).abs()`, since two `i32`s can be `2 * 10^9` apart, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples; 1000
numbers, LeetCode's most, rising by 1 with a target of 1, the ends of
LeetCode's range in turn with a target of `2 * 10^9`, all equal with a
target of 0, and the same with the last one apart; 3000 random arrays of
2 to 12 numbers from 0 to 9 with targets from 0 to 4; and 20 arrays of
1000 from `-10^9` to `10^9` with targets up to `2 * 10^9`, the last two
with the count reached, the sum of the jumps and a checksum.
`jumps.py` mirrors the ★ arm and its output is byte-identical.

```
3
5
-1
999
999
999
-1
3000 small arrays: 1706 reached, jumps sum to 6586, checksum 775421465
20 arrays of 1000: 20 reached, jumps sum to 14367, checksum 52539681
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every set of the indices between the first and the last, as
the bits of a number, taken as the indices a path stops at, kept when
every jump in it is within target, and the most jumps over those kept,
or -1; no table. It draws 2000 random arrays of 2 to 12 numbers from 0
to 9 with targets from 0 to 4, then 40 of up to 300 from `-10^9` to
`10^9` with targets up to `2 * 10^9`, all before any arm answers; the
literal reading is asked only of the first 2000.

| | property |
|---|---|
| P1 | up to 12 numbers, the answer is the literal reading's |
| P2 | every number negated: the same answer |
| P3 | every number 1000 more: the same answer |
| P4 | the target one more: no fewer jumps |
| P5 | -1 or from 1 to n - 1, and n - 1 when the target is at least the greatest number less the least |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2040 cases: checksum 187316881, 61200 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases by the same paths gives the same checksum. On
a failure it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. M3 and M8 fail the same checks: both leave the
last index out of reach in every case, one in the memo arm and one in
the tree.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an unreached index jumped from | P1 492, P5 224, P6 496 |
| M2 | ★: only jumps up allowed | P1 849, P2 980, P5 86, P6 889 |
| M3 | memo: the last index counted unreachable | P1 1136, P5 139, P6 1176 |
| M4 | memo: the first jump that reaches the end kept | P1 50, P4 7, P6 79 |
| M5 | push: a jump within target less 1 only | P1 743, P5 56, P6 743 |
| M6 | push: only the next index tried | P1 955, P6 990 |
| M7 | tree: the window's top end left out | P1 469, P2 609, P5 28, P6 469 |
| M8 | tree: the first index never put in | P1 1136, P5 139, P6 1176 |
| M9 | solution: the difference taken without its sign | P1 780, P2 1480, P6 813 |
| M10 | solution: each count raised to the earlier one, not one more | P1 1136, P5 1176, P6 1176 |

## Benchmarks

The bench draws 40 arrays of 1000 numbers from `-10^9` to `10^9`,
LeetCode's most, with targets up to `2 * 10^9`, all of them first, then
answers each 5 times by the ★ arm in all five languages. Every
implementation prints `40 arrays of 1000, 5 rounds: 190 reached, jumps
sum to 130155, checksum 865623586`.

BENCHTAB

## Verification

All five arms print the same output as `jumps.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The ★, memo and push arms checked clean as first written. The tree arm
wrote Rust's `fn raise(mut self, ..)` for the method that writes the
tree; `karac check` refused it, a receiver that writes being `mut ref
self` in Kāra, and `karac fix` wrote that.

LeetCode's Rust template took 13 `karac fix` edits, the wrapper
included: `struct Solution {}` added; the `Vec<..>`s became `Vec[..]`;
`vec![-1; n]` became `Vec.filled(n, -1i32)`, the table's type taken
from the `i32` it returns; `&&` became `and`; `target as i64` dropped
its cast, an `i32` widening into the `i64` comparison as it is; the
wrapper's `&Vec<i64>` became `ref Vec[i64]`; the `&x` pattern dropped
its `&`; and `Solution::` became `Solution.`, with the wrapper's `as
i64` dropped. The casts of the numbers to `i64` stayed.
