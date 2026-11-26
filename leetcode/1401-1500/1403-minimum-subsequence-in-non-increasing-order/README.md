# 1403. Minimum Subsequence in Non-Increasing Order

Given the array `nums`, obtain a subsequence of the array whose sum of
elements is strictly greater than the sum of the non included elements
in such subsequence.

If there are multiple solutions, return the subsequence with minimum
size and if there still exist multiple solutions, return the subsequence
with the maximum total sum of all its elements. A subsequence of an
array can be obtained by erasing some (possibly zero) elements from the
array.

Note that the solution with the given constraints is guaranteed to be
unique. Also return the answer sorted in non-increasing order.

```
nums = [4, 3, 10, 9, 8]  ->  [10, 9]     19 against 15
nums = [4, 4, 7, 6, 7]   ->  [7, 7, 6]   20 against 8; [7, 7] is 14 against 14
```

**Constraints:** `1 <= nums.length <= 500`, `1 <= nums[i] <= 100`.

Each arm is `fn min_subsequence(nums: Vec[i32]) -> Vec[i32]`. The fewest
numbers are the largest ones, and among as many numbers the largest sum
is theirs too, so the answer is the k largest for the least k that
outweighs the rest.

## Approaches

| file | mechanism |
|---|---|
| `min_subsequence.kara` ★ | sorted by `sort()` and `reverse()`, the largest taken one by one, each moved from the rest's sum to the taken sum, until the taken sum is the larger. O(n log n) |
| `min_subsequence_counting.kara` | a counting sort: how many of each value from 1 to 100 in a fixed `[0; 101]` array, then the values walked down from 100, a copy taken while any are left, until the taken sum is more than half the total. O(n + 100) |
| `min_subsequence_heap.kara` | a `PriorityQueue.max_first()` of the numbers, popped until the taken sum is the larger. O(n + k log n) |
| `min_subsequence_prefix.kara` | sorted rising with the prefix sums beside, the most numbers that can be left out found by `partition_point` as the last prefix under half the total, and the rest of the list returned by `iter().rev().collect()`. O(n log n) |
| `min_subsequence_solution.kara` | a Rust solution as LeetCode's Rust users write it (sorted falling by `sort_unstable_by(\|a, b\| b.cmp(a))`, the total by `iter().sum()`, and `for &n in nums.iter()` pushing until `sum > total - sum`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's two examples and four more
(`[10 9] [7 7 6] [6] [1 1] [3 1] [5 5 5]`); the constraints' most, 500
numbers of 100, of 1, and drawn, how many are taken and the drawn ones'
sum (`500 numbers: 251 251 146, sum 12557`); and 2000 random cases of 1
to 40 numbers (`2000 random cases: 14129 taken, checksum 830006163`).
`min_subsequence.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★, heap and prefix arms check clean as first written.
The counting arm indexed its array with `count[x as i64]`; check warns
that the cast is unnecessary, an `i32` index widening to `i64` by
itself, and `karac fix` drops it, 1 fix. The Rust solution takes one
round of 20 fixes by `karac fix`'s count: `struct Solution;` to `struct
Solution {}`, the parameter `mut nums: Vec<i32>` to `nums: own Vec[i32]`
with `let mut nums = nums;` in the body, `Vec<i32>` to `Vec[i32]`,
`sort_unstable_by` to `sort_by`, `Vec::new` to `Vec.new`, the `&`
dropped from the pattern `&n`, which matches through the reference
already, and `Solution::` to `Solution.`. Its output matches on the
first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every subsequence of up to 10 numbers tried, those whose sum
is more than the rest's kept, the fewest numbers first and then the
largest sum, sorted falling. LeetCode's examples and eight edge cases
(one number, two equal, one large number among small ones, all equal, 1
to 10, 500 of 100), and 1993 random cases, 1 to 10 numbers two times in
three and else 11 to 500, up to 100, 5, 2 or 30.

| | property |
|---|---|
| P1 | the statement read literally, on up to 10 numbers |
| P2 | drawn from the numbers, each used no more often than it is there, in non-increasing order, and more than the rest |
| P3 | one number fewer cannot do it: the answer without its last, smallest number is not more than the rest |
| P4 | the order the numbers come in does not matter: the list reversed gives the same |
| P5 | every number doubled doubles the answer's numbers, when every one is within 50 |
| P6 | the ★ arm's answer |

All 54,395 checks pass on every arm (P1 and P5 apply to some cases
only): `2003 cases: checksum 61268697, 54395 checks over 5 arms: 0
failures`, under `karac __mir-run`, `karac run`, `karac build` and
`karac __mir-llvm-run`. Python, taking the k largest for the least k,
gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: stopping once the taken sum is as large as the rest, not larger | P1 151, P2 213, P6 852 |
| M2 | ★: the sort not reversed, so the smallest are taken first | P1 1154, P2 1776, P6 7272 |
| M3 | counting: stopping once the taken sum is half the total | P1 151, P2 213, P6 213 |
| M4 | counting: a value's count not lowered when one is taken, so the largest is taken again and again | P1 731, P2 1229, P6 1229 |
| M5 | heap: `PriorityQueue.new()`, popping the smallest first | P1 1154, P2 1776, P6 1818 |
| M6 | heap: each number taken put first, so the answer comes out rising | P1 731, P2 1229, P6 1229 |
| M7 | prefix: a prefix of exactly half the total left out | P1 151, P2 213, P6 213 |
| M8 | prefix: the answer's smallest number left out too | P1 1338, P2 2003, P6 2003 |
| M9 | solution: sorted rising instead of falling | P1 1154, P2 1776, P6 1818 |
| M10 | solution: the taken sum starting at 1 | P1 293, P2 411, P5 192, P6 411 |

M1, M3 and M7 are the same mistake, a tie with the rest taken as enough,
and M4 and M6 fail the same checks: each is wrong exactly when the
answer holds two different values, M4 repeating the largest and M6
putting them in the wrong order.

## Benchmarks

The bench draws a pool of 10^5 numbers from 1 to 100 and runs the ★ arm
on 20000 windows of 500 numbers in a row, each window's start drawn from
the checksum so far, folding how many are taken and the smallest of them
into the checksum. Every implementation prints `20000 windows of 500
numbers: checksum 858918616`.

BENCHTAB
