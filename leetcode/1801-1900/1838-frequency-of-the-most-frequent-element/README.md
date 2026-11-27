# 1838. Frequency of the Most Frequent Element

The frequency of an element is the number of times it occurs in an
array. You are given an integer array `nums` and an integer `k`. In one
operation, you can choose an index of `nums` and increment the element
at that index by `1`. Return the maximum possible frequency of an
element after performing at most `k` operations.

```
nums = [1,2,4], k = 5      ->  3
nums = [1,4,8,13], k = 5   ->  2
nums = [3,9,6], k = 2      ->  1
```

**Constraints:** `1 <= nums.length <= 10^5`, `1 <= nums[i] <= 10^5`, `1
<= k <= 10^5`.

The arms are `fn max_frequency(nums: Vec[i64], k: i64) -> i64`.

## Approaches

| file | mechanism |
|---|---|
| `max_frequency.kara` ★ | the numbers sorted, and a window over them whose numbers are all raised to its last; that costs the last times the window's length less the window's sum, and the window drops its first number while that passes `k`. The longest window is the answer. O(n log n) |
| `max_frequency_search.kara` | the numbers sorted and summed from the first, and for each number the earliest start of a run ending at it that `k` raises to it, found by a binary search on the start: the cost only falls as the start moves on. O(n log n) |
| `max_frequency_grow.kara` | the ★ arm's window that never shrinks: when raising it to its last passes `k`, its first number goes and it moves on whole, so it only ever grows, and its length at the end is the longest that fit. O(n log n) |
| `max_frequency_count.kara` | the ★ arm's window over the values in place of a sorted list: how many of each value there are, counted up to the largest, and a window of values, the target its last, that gives up numbers from its smallest value while raising them passes `k`, only as many of that value as must go. O(n + M), M the largest number |
| `max_frequency_solution.kara` | a Rust solution as LeetCode's Rust users write it (`mut nums` sorted in place, the window's sum an `i64` and every `i32` cast up to it), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's three examples; five
edges, one number, every number the same, a `k` that raises nothing, one
that raises every number, and one that raises a number only part of the
way (`1 3 1 3 2`); the constraints' most, 10^5 numbers from 1 to 10^5
with `k` of 10^5 and with `k` of 1 (`the most: 491 9`); and 3000 random
cases of 1 to 10 numbers from 1 to 20, with `k` from 1 to 30 (`3000
random cases: checksum 188995833`). `max_frequency.py` mirrors the ★
arm, and its output is byte-identical. Every arm gives the same output
under `karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`.

The Mend loop: every arm and the harness check clean as first written.
The Rust solution takes 28 fixes by `karac fix`'s count, and its diff
is: `struct Solution {}` added above the `impl`; `mut nums: Vec<i32>` to
`nums: own Vec[i32]` with `let mut nums = nums;` at the body's start;
`nums.sort_unstable()` to `nums.sort()`; `let (mut l, mut sum, mut ans)
= (0, 0i64, 0)` to `let mut (l, sum, ans) = (0, 0, 0)`, the `i64` the
literal's default; the five `as i64` casts in the window's sum and cost
taken off, an `i32` widening to `i64` without one; `Solution::` to
`Solution.` at the harness's 10 calls; and the harness's `as i64` on the
result taken off. `ans as i32` at the return, which narrows, is Kāra as
it stands. The solution takes a `Vec[i32]`, so its harness builds its
lists as `Vec[i32]` and copies its largest list for the first of the two
calls on it. Every arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every set of the numbers that could be raised to one value,
the value its largest, as raising past it only costs more, and the
largest set whose raising costs at most `k`. It runs 2000 random cases
of 1 to 10 numbers from 1 to 20, with `k` from 1 to 30. Each arm meets
six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | at most every number, and at least the most of any one value there already |
| P3 | the numbers in reverse order give the same answer |
| P4 | a larger `k` never gives less |
| P5 | every number 7 larger gives the same answer |
| P6 | the ★ arm's answer |

It checks clean as first written. All 60,000 checks pass on every arm:
`2000 cases: checksum 261387666, 60000 checks over 5 arms: 0 failures`,
under `karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`. Python, over the same cases, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash. The count
arm's second edit was first to take a dropped number off the sum at the
target's value; it stopped on a division by zero, a crash, and it now
keeps a window costing `k + 1`. The solution's first edit was first to
take a dropped number off the sum one more than it is; it stopped on an
index out of bounds, and it now takes the cost of a window one number
short.

| | edit | failures by property |
|---|---|---|
| M1 | ★: a window costing exactly `k` shrunk | P1 179, P6 716 |
| M2 | ★: the first number dropped from the window but not from its sum | P1 517, P5 556, P6 2068 |
| M3 | search: a start costing exactly `k` refused | P1 179, P6 179 |
| M4 | search: each prefix sum one more for each number | P1 663, P6 663 |
| M5 | grow: the window's length taken one short | P1 2000, P2 318, P6 2000 |
| M6 | grow: the numbers walked in reverse of their order, unsorted | P1 1140, P3 1043, P6 1140 |
| M7 | count: one number more dropped when the over is a multiple of the cost of each | P1 3, P6 3 |
| M8 | count: a window costing `k + 1` kept | P1 149, P6 149 |
| M9 | solution: the cost of a window taken one number short | P1 1296, P5 526, P6 1296 |
| M10 | solution: each window's length taken one short | P1 2000, P2 318, P6 2000 |

## Benchmarks

The bench builds one list of 10^5 numbers from 1 to 10^5 once and makes
200 calls of the ★ arm on its first 50000 to 99999 numbers, with `k`
from 1 to 10^5, each run's length and `k` drawn from the checksum so
far. Each call copies its run, and the arm sorts a copy of its own. It
checks clean as first written. Every implementation prints `200 calls:
checksum 117465396`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra is ahead of Rust here at 0.41 s against Rust's 0.56 s (0.57 s with
overflow checks on), C's 2.1 s and Go's 1.7 s; Python takes 6.8 s.
