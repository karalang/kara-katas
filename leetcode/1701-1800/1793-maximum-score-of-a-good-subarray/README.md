# 1793. Maximum Score of a Good Subarray

Given an array of integers `nums` (0-indexed) and an integer `k`, the
score of a subarray `(i, j)` is `min(nums[i], nums[i + 1], ..., nums[j])
* (j - i + 1)`. A good subarray is one with `i <= k <= j`. Return the
largest score of a good subarray.

```
nums = [1,4,3,7,4,5],      k = 3  ->  15
nums = [5,5,4,5,4,1,1,1],  k = 0  ->  20
```

**Constraints:** `1 <= nums.length <= 10^5`, `1 <= nums[i] <= 2 * 10^4`,
and `0 <= k < nums.length`.

The arms are `fn maximum_score(nums: Vec[i32], k: i32) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `maximum_score.kara` ★ | two pointers out from `k`: of the two windows one number wider, the one grown toward the larger neighbour keeps the larger minimum, so the window grows that way one number at a time, and every width is scored at its best. O(n) |
| `maximum_score_stack.kara` | a monotonic stack: the best subarray with `nums[i]` as its minimum runs between the nearest smaller numbers on either side, one pass of a stack finds both for every index, and the windows that hold `k` are scored. O(n) |
| `maximum_score_search.kara` | binary search: the minimum of `nums[k - d..=k]` only falls as `d` grows, and so does that of `nums[k..=k + d]`, so for each minimum on one side `partition_point` finds how far the other side reaches. O(n log n) |
| `maximum_score_merge.kara` | the same two falling lists of minima walked together: as one side's minimum falls the other side reaches further, so its pointer only moves forward. O(n) |
| `maximum_score_solution.kara` | a Rust solution as LeetCode's Rust users write it (the two pointers on `usize` with the ends checked first), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's two examples (`15 20`);
six edges, one number, `k` at the start and at the end of a rising list,
every number alike, a valley at `k` and a peak at `k` (`7 5 9 12 5 6`);
the constraints' most, 100000 numbers of 20000, 100000 numbers climbing
1 to 20000 over and over with `k` at the end, and 100000 at random (`the
most: 2000000000 100010000 122536`); and 3000 random cases of 1 to 30
numbers (`3000 random cases: checksum 989509233`). `maximum_score.py`
mirrors the ★ arm, and its output is byte-identical. Every arm gives the
same output under `karac __mir-run`, `karac run`, `karac build` and
`karac __mir-llvm-run`.

The Mend loop: the ★ arm checks clean as first written. The harness
folds each answer into an `i64` checksum as `maximum_score(nums, k as
i32) as i64`, and check warns the cast is unnecessary, since an `i32`
widens to `i64` by itself; `karac fix` removes it, 1 fix. The stack,
search and merge arms start their best score as `let mut best = 0;`, and
check refuses it, the literal having kept its default `i64` where an
`i32` is returned; `karac fix` writes `let mut best: i32 = 0;`, 2 fixes
with the harness's. The Rust solution takes one round of 12 fixes by
`karac fix`'s count, and its diff is: `struct Solution;` to `struct
Solution {}`, `Vec<i32>` to `Vec[i32]` in both signatures, `k as usize`
to `k as i64`, `let (mut i, mut j)` to `let mut (i, j)`, `||` to `or`,
and `Solution::` to `Solution.`. Every arm's output matches on the first
run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every subarray from `i` to `j` with `i <= k <= j`, its
minimum found afresh, times its length, while there are at most 40
numbers. LeetCode's examples, the six edges, 3000 numbers at random and
3000 climbing 1 to 700 over and over, and 1990 random cases of 1 to 40
numbers. Each arm meets six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally, while there are at most 40 numbers |
| P2 | the numbers in reverse order, `k` with them, give the same answer |
| P3 | every number doubled doubles the answer |
| P4 | one more number at the end never lowers the answer |
| P5 | the number at `k` raised to the largest never lowers the answer |
| P6 | the ★ arm's answer |

The differential's literal reading was first written with `low as i64 *
(j - i + 1)`, and `karac fix` removed the cast, 1 fix. All 59,990 checks
pass on every arm: `2000 cases: checksum 593603598, 59990 checks over 5
arms: 0 failures`, under `karac __mir-run`, `karac run`, `karac build`
and `karac __mir-llvm-run`. Python, running the ★ arm's mirror over the
same cases, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: each window scored one number narrower | P1 1888, P6 7560 |
| M2 | ★: a number taken on the left never lowering the minimum | P1 1026, P2 1469, P4 161, P6 4112 |
| M3 | stack: a window that stops just short of k counted | P1 163, P2 258, P6 163 |
| M4 | stack: each window taken one number wider | P1 1998, P6 2000 |
| M5 | search: the left side's minima never reaching the first number | P1 942, P2 727, P6 942 |
| M6 | search: only the right side's first minimum searched from | P1 492, P2 986, P5 128, P6 492 |
| M7 | merge: only the left side's minima walked | P1 492, P2 986, P5 128, P6 492 |
| M8 | merge: the left side's list missing k itself | P1 1619, P2 603, P6 1621 |
| M9 | solution: the window grown toward the smaller neighbour | P1 787, P2 133, P4 31, P6 788 |
| M10 | solution: a number taken on the right never lowering the minimum | P1 1029, P2 1469, P6 1030 |

## Benchmarks

The bench builds 200 random lists of 1000 numbers once, and makes 40000
calls of the ★ arm, each list and its `k` drawn from the checksum so
far. It checks clean as first written. Every implementation prints
`40000 calls over 200 lists of 1000 numbers: checksum 874125351`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra is ahead of Rust here at 0.11 s against Rust's 0.15 s (0.11 s with
overflow checks on), C's 0.14 s and Go's 0.09 s; Python takes 7.8 s.
