# 1827. Minimum Operations to Make the Array Increasing

You are given an integer array `nums` (0-indexed). In one operation, you
can choose an element of the array and increment it by `1`. For example,
if `nums = [1,2,3]`, you can choose to increment `nums[1]` to make `nums
= [1,3,3]`. Return the minimum number of operations needed to make
`nums` strictly increasing. An array `nums` is strictly increasing if
`nums[i] < nums[i+1]` for all `0 <= i < nums.length - 1`. An array of
length `1` is trivially strictly increasing.

```
nums = [1,1,1]      ->  3
nums = [1,5,2,4,1]  ->  14
nums = [8]          ->  0
```

**Constraints:** `1 <= nums.length <= 5000`, `1 <= nums[i] <= 10^4`.

The arms are `fn min_operations(nums: Vec[i64]) -> i64`.

## Approaches

| file | mechanism |
|---|---|
| `min_operations.kara` ★ | each number must pass the one before it as raised, so a number at or below it is raised to one more, and the raise is counted. O(n) |
| `min_operations_fold.kara` | the ★ arm's walk as one `fold`, carrying the last number as raised and the count so far, each number raised to the larger of itself and one past the last. O(n) |
| `min_operations_prefix.kara` | with no walk carrying the last number: the number at place `i` is raised to `i` plus the largest `nums[j] - j` over the places `j` up to it, as each number before it, raised, pushes it one more per place between; the count is what those targets add. O(n) |
| `min_operations_recursive.kara` | by recursion on the list's length: the first `n - 1` numbers made increasing give their count and their last number as raised, and the last number is raised past it. O(n) |
| `min_operations_solution.kara` | a Rust solution as LeetCode's Rust users write it (the ★ arm's walk in `i32`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's three examples; five
edges, two equal numbers, a list already increasing, one strictly
decreasing, a large number early lifting all after it, and the largest
value then the smallest (`1 0 20 21 10000`); the constraints' most, 5000
numbers all 1, all 10^4, and falling from 10^4 (`the most: 12497500
12497500 24995000`); and 3000 random cases of 1 to 12 numbers from 1 to
20 (`3000 random cases: checksum 572416011`). `min_operations.py`
mirrors the ★ arm, and its output is byte-identical. Every arm gives the
same output under `karac __mir-run`, `karac run`, `karac build` and
`karac __mir-llvm-run`.

The Mend loop: every arm checks clean as first written. The harness was
first written with its lists as `vec![..]`; check warned 8 times that
`vec!` is deprecated for the list literal, and `karac fix` wrote `[1, 1,
1]` for `vec![1, 1, 1]`, 8 fixes. The Rust solution takes 19 fixes by
`karac fix`'s count, and its diff is: `struct Solution {}` added above
the `impl`; `Vec<i32>` to `Vec[i32]`; `let mut prev = 0` and `let mut
ans = 0` to `let mut prev: i32 = 0` and `let mut ans: i32 = 0`, as a
bare literal binding is an `i64` and the walk compares and adds it with
the `i32` numbers; `for &x in nums.iter()` to `for x in ..`;
`Solution::` to `Solution.` at the harness's 12 calls; and the harness's
`as i64` on the result taken off. The solution takes a `Vec[i32]`, so
its harness builds its lists as `Vec[i32]`. Every arm's output matches
on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: one operation at a time, the first number not above the one
before it raised by one, until the list is strictly increasing, and the
operations counted. It runs 2000 random cases of 1 to 10 numbers from 1
to 20, a quarter of them from 1 to 3, each with a place to cut it. Each
arm meets six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | no operations exactly when the list is already strictly increasing |
| P3 | every number raised by the same amount takes the same count |
| P4 | a number put last above every number the list can be raised to adds nothing |
| P5 | the list cut in two takes at least what the two pieces take alone, as the first piece only lifts the second |
| P6 | the ★ arm's answer |

It checks clean as first written. All 60,000 checks pass on every arm:
`2000 cases: checksum 776669219, 60000 checks over 5 arms: 0 failures`,
under `karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`. Python, over the same cases, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: each raise counted one too many | P1 1675, P6 6700 |
| M2 | ★: a number equal to the last left as it is | P1 421, P2 79, P6 1684 |
| M3 | fold: a number raised only to the last, not past it | P1 1675, P2 79, P6 1675 |
| M4 | fold: the whole raised number counted, not the raise | P1 2000, P2 325, P3 2000, P4 2000, P6 2000 |
| M5 | prefix: the place left out of the lift | P1 1274, P2 124, P4 2000, P6 1274 |
| M6 | prefix: each target taken without its place | P1 1799, P2 455, P4 2000, P5 416, P6 1799 |
| M7 | recursive: the empty list's last taken as 1 | P1 222, P2 53, P3 222, P6 222 |
| M8 | recursive: a number raised only past two below the last | P1 1675, P2 276, P6 1675 |
| M9 | solution: a raised number carried one higher | P1 1416, P4 1005, P6 1416 |
| M10 | solution: a number above the last carried one lower | P1 1675, P2 79, P6 1675 |

Writing the mutants turned up a refusal, filed as B-2026-11-27-6: the
fold with its accumulator pattern annotated, `|(prev, total): (i64,
i64), x| (x, total + x.max(prev))` over `nums.iter()`, is refused
"expected 'i64', found 'ref i64'" at the tuple's `x`, where the same
closure without the annotation checks clean, and so does `let p: (i64,
i64) = (x, 1)`. The arm keeps its unannotated closure, as first written.

## Benchmarks

The bench builds one list of 10^4 numbers from 1 to 10^4 once and makes
10000 calls of the ★ arm on runs of 2500 to 4999 of its numbers, each
run's start and length drawn from the checksum so far. Each call copies
its run, as the arm takes its list by value. It checks clean as first
written. Every implementation prints `10000 calls: checksum 513640169`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra is ahead of Rust here at 0.04 s against Rust's 0.05 s (0.06 s with
overflow checks on), C's 0.07 s and Go's 0.17 s; Python takes 2.5 s.
