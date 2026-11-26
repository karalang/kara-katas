# 1498. Number of Subsequences That Satisfy the Given Sum Condition

You are given an array of integers `nums` and an integer `target`.
Return the number of non-empty subsequences of `nums` such that the sum
of the minimum and maximum element on it is less or equal to `target`.
Since the answer may be too large, return it modulo `10^9 + 7`.

```
nums = [3,5,6,7], target = 9         ->  4
nums = [3,3,6,8], target = 10        ->  6
nums = [2,3,3,4,6,7], target = 12    ->  61
```

**Constraints:** `1 <= nums.length <= 10^5`, `1 <= nums[i] <= 10^6` and
`1 <= target <= 10^6`.

The arms are `fn num_subseq(nums: Vec[i32], target: i32) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `num_subseq.kara` ★ | the values sorted, then two pointers: while the least and the most left sum to at most the target, every subsequence holding the least and any of the values up to the most counts, 2 to the power of their number, from a table; else the most is too big for any least left. O(n log n) |
| `num_subseq_bsearch.kara` | the values sorted; for each value as the least, a binary search with `partition_point` for how far the most may reach. O(n log n) |
| `num_subseq_modpow.kara` | the ★ arm's two pointers with no table of powers: each power of 2 taken by squaring as it is needed. O(n log n) |
| `num_subseq_counting.kara` | the values, at most 10^6, counted by value instead of sorted; the two pointers walk the values that occur, each copy of the least's value counted once as the least. O(n + V) |
| `num_subseq_solution.kara` | a Rust solution as LeetCode's Rust users write it (`mut nums: Vec<i32>` sorted in place with `sort_unstable`, `usize` pointers), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's three examples (`4 6 61`);
six edges, one value that fits and one that does not, every value too
big, every value equal, the target exactly twice the least, and two
values whose sum is the target (`1 0 0 15 1 2`); the constraints' most,
100000 values of 1 with the target 2, so that every subsequence counts,
and 100000 values up to 1000000 with targets of 1000000 and 500000
(`100000 values: 607723519 916064288 134079388`); and 3000 random arrays
of 1 to 30 values from 1 to 50 (`3000 random arrays: checksum
504648443`). `num_subseq.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★ and bsearch arms check clean as first written. The
modpow arm was first written `let (mut lo, mut hi) = ..`, and `karac
fix` moved the `mut` before the pattern in 3 fixes. The counting arm's
`lo + hi > target as i64` took 1 fix, the cast dropped. The Rust
solution takes one round of 18 fixes by `karac fix`'s count, and its
diff is: `struct Solution;` to `struct Solution {}`, `mut nums:
Vec<i32>` to `nums: own Vec[i32]` with `let mut nums = nums;`, the plain
wrapper's parameter `own` as well, and so the harness's first call on
`big` given `big.clone()`, `sort_unstable()` to `sort()`, `vec![1i64;
n]` to `Vec.filled(n, 1)`, `let (mut l, mut r) = (0usize, n - 1)` to
`let mut (l, r) = (0, n - 1)`, `0i64` to `0` and `Solution::` to
`Solution.`. Every arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every non-empty subsequence, one bit of a mask for each
value, whose least and most sum to at most the target. LeetCode's
examples, the edges, and 1991 random arrays of 1 to 12 values from 1 to
30, the target from 1 to 60. Each arm meets six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | no more than the non-empty subsequences there are |
| P3 | the values in reverse order count the same |
| P4 | a larger target counts no fewer |
| P5 | a value as large as the target, in no subsequence that counts, changes nothing |
| P6 | the ★ arm's answer |

The cases are a `let` annotated `Vec[(Vec[i32], i32)]` with the fixed
cases written in it, as check advises: pushed one at a time,
`cases.push(([3, 5, 6, 7], 9))` is refused, an array literal inside the
tuple leaving the tuple's number at the default `i64` (B-2026-11-26-9).
The solution's copy takes its array by value, so the dispatcher hands it
`nums.clone()`. All 60,000 checks pass on every arm: `2000 cases:
checksum 713401307, 60000 checks over 5 arms: 0 failures`, under `karac
__mir-run`, `karac run`, `karac build` and `karac __mir-llvm-run`.
Python, counting with `itertools.combinations`, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: a least and most summing to the target refused | P1 621, P6 2484 |
| M2 | ★: the least alone, with no value left beside it, never counted | P1 984, P6 3936 |
| M3 | bsearch: the search stops at a least that makes the target with itself | P1 206, P6 206 |
| M4 | bsearch: each least's subsequences counted one short | P1 1618, P6 1618 |
| M5 | modpow: the exponent divided by 3 each round | P1 1167, P4 179, P6 1167 |
| M6 | modpow: two values dropped when the most is too big | P1 748, P5 1618, P6 748 |
| M7 | counting: each copy counted before it is passed | P1 1618, P2 983, P6 1618 |
| M8 | counting: a value too big to pair with itself still counted | P1 1016, P5 51, P6 1016 |
| M9 | solution: only the least checked against the target | P1 1014, P5 1618, P6 1014 |
| M10 | solution: every other least skipped | P1 1258, P6 1258 |

## Benchmarks

The bench keeps one array of 100000 values up to 1000000 and makes 200
calls of the ★ arm, each with a target chosen from the checksum so far
and first moving one value, so each call sorts a copy of 100000 values
with the language's own sort (C's `qsort` through a comparison function,
Go's `slices.Sort`). Every implementation prints `200 calls over 100000
values: checksum 953092143`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra is ahead of Rust here at 0.64 s against Rust's 0.76 s (0.73 s with
overflow checks on), C's 3.4 s and Go's 2.3 s; Python takes 9.2 s.
