# 2294. Partition Array Such That Maximum Difference Is K

You are given an integer array `nums` and an integer `k`. You may
partition `nums` into one or more **subsequences** such that each
element in `nums` appears in **exactly** one of the subsequences.

Return *the **minimum** number of subsequences needed such that the
difference between the maximum and minimum values in each subsequence
is **at most*** `k`*.*

A **subsequence** is a sequence that can be derived from another
sequence by deleting some or no elements without changing the order of
the remaining elements.

```
nums = [3,6,1,2,5], k = 2   ->  2
nums = [1,2,3], k = 1       ->  2
nums = [2,2,4,5], k = 0     ->  3
```

**Constraints:** `1 <= nums.length <= 10^5`; `0 <= nums[i] <= 10^5`;
`0 <= k <= 10^5`.

A subsequence's minimum and maximum do not depend on its order, so the
order of `nums` does not matter. Sort it: the smallest number must be in
some group, that group may as well take every number up to `k` above
it, and the first number past that opens the next. O(n log n).

## Approaches

| file | mechanism |
|---|---|
| `partition.kara` ★ | `sort` a clone, then one pass: a group opens at the first number and at each number more than `k` above the one that opened the last |
| `partition_naive.kara` | no sort: while numbers are left, find the smallest and strike it and everything up to `k` above it with `retain`, one group each time. O(n * groups) |
| `partition_count.kara` | the values marked in a `Vec.filled(top + 1, false)` indexed by value, walked upwards, a group opening at each value present past the open group's reach. O(n + largest value) |
| `partition_struct.kara` | `struct Group` keeps its least and greatest number and says whether a number `fits`; the sorted numbers join the last group or open a new one |
| `partition_iter.kara` | `sort`, then `fold` the numbers into the count of groups and the low end of the open one |
| `partition_solution.kara` | LeetCode's Rust template: `mut nums: Vec<i32>` and `i32` in, `i32` out; `sort_unstable`, then `iter().skip(1)` from the first number as the start; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's three examples; one
number; repeats with `k` of 0; a `k` that spans 0 to 10^5; numbers
exactly `k` apart, each its own group's edge; then 3000 random arrays of
1 to 60 numbers from 0 to `top`, `top` from 1 to 200, `k` from 0 to 30,
with a checksum and the groups in all. `partition.py` mirrors the ★ arm
and its output is byte-identical.

`karac fix` carries the template in one call, reporting 8 edits:
`struct Solution;` to `struct Solution {}`; the parameter `mut nums:
Vec<i32>` to `nums: own Vec[i32]` with `let mut nums = nums;` at the
top of the body, and the brackets of the `Vec<i32>`; `sort_unstable` to
`sort`, since the library has only the stable sort, which is also an
unstable one; the `&` of `for &x` dropped; and in the adapter the `as
i64` on the template's `i32` answer dropped. The iterator arm was
written first with `sort_unstable` too: 1 edit.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every way to split the numbers into subsequences, each way
written as a restricted growth string (the first number in group 0,
each next one in a group already used or in the next new one), so that
each split is made once; of the ways where every group's largest and
smallest differ by at most `k`, the fewest groups. No sorting and no
greedy choice. It checks 300 random arrays of 1 to 8 numbers from 0 to
40 with `k` from 0 to 10; then 30 of multiples of `k` or `k + 1`, so
that numbers fall exactly at a group's reach or just past it; then 30
of one value repeated with a few others. All 360 are drawn before any
arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | `1 <= answer <=` the distinct values, and the answer is 1 just when the largest and smallest differ by at most `k` |
| P3 | the numbers reversed: the same answer |
| P4 | every number written twice: the same answer |
| P5 | `k` one larger: no more groups; `k` of 0: the distinct values |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 846839395, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that
generates every set partition recursively. On a failure it prints the
first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: the low end never moved | P1 229, P2 96, P4 356, P5 102, P6 229 |
| M3 | ★: unsorted | P1 234, P2 117, P3 208, P5 272, P6 234 |
| M5 | ★: the first group never counted | P1 135, P2 38, P5 40, P6 135 |
| M7 | naive: the largest for the smallest | P1 296, P2 296, P5 309, P6 296 |
| M8 | naive: the reach one more | P1 81, P2 10, P5 114, P6 81 |
| M9 | naive: the smallest from the first two | P1 155, P2 27, P3 159, P5 207, P6 155 |
| M12 | count: the largest value never marked | P1 265, P2 130, P5 360, P6 265 |
| M13 | count: the reach one short | P1 67, P2 7, P6 67 |
| M14 | count: the walk from 1 | P1 28, P2 4, P5 40, P6 28 |
| M17 | struct: a group's width k minus one | P1 83, P2 23, P4 37, P5 107, P6 83 |
| M19 | struct: only the first group asked | P1 171, P2 49, P4 296, P5 69, P6 171 |
| M20 | struct: unsorted | P1 150, P2 37, P4 296, P5 67, P6 150 |
| M22 | iter: the low end the last number | P1 80, P2 18, P6 80 |
| M24 | iter: the first number its own group | P1 225, P2 137, P5 320, P6 225 |
| M25 | iter: the reach twice k | P1 156, P2 30, P6 156 |
| M27 | solution: the first number skipped twice | P1 112, P2 37, P4 112, P5 238, P6 112 |
| M29 | solution: the count from 0 | P1 360, P2 171, P5 360, P6 360 |

P1, P2 and P6 kill all seventeen, P5 fourteen, P4 five and P3 two. P2
fails for every edit because each one, somewhere, counts one group when
the numbers do not all fit one, or more than one when they do, or more
groups than there are values. P5 at `k` of 0, where the answer is the
distinct values, catches every edit except three that miscount only
where `k` is large enough to matter: the reach one short, the low end
the last number, and the reach twice `k`. P3, the numbers reversed,
fails only where an arm reads the numbers in their given order: the ★
arm unsorted and the naive arm's smallest from the first two. P4,
every number twice, fails where a duplicate changes the count: a
low end that never moves, a group's width one short, only the first
group asked, the struct arm unsorted, and the template's second number
skipped.

Of the thirty-one, fourteen were not kept, and none crashes or differs
between the backends. A group's reach `k` minus one in the ★ and iter
arms (M1, M23) fails as the struct arm's width `k` minus one (M17); the
★ arm's low end the last number and the struct arm's least never kept
and width against the most alone (M4, M18, M21) as the iter arm's low
end the last number (M22); the ★ arm's group for every `k + 1` apart
(M6) in a way of its own; the naive arm's only the smallest struck and
the count arm's every value its own group (M10, M15) together; the
naive arm's groups counted twice when two are left (M11) and the count
arm's reach from the start (M16) each in a way of its own; the iter
arm's reversed (M26) as the naive arm's largest for the smallest (M7);
the template's start never moved (M28) as the struct arm's only the
first group asked (M19); the template's `k` plus one (M30) as the naive
arm's reach one more (M8); and the template's unsorted (M31) as the ★
arm's (M3).

The naive arm's reach one less, as first drafted, `x - low >= k`,
would keep every number when `k` is 0 and never end; it was replaced
by the reach one more (M8) before the run.

## Verification

Every arm prints the same output as `partition.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.3 to 0.5 s. The differential
takes 1.4 s.

## Benchmarks

The bench builds 20 arrays of 10^5 numbers from 0 to 10^5 once, then
makes 5 passes over all of them, array `a` answered with `k = 7a` in
the first pass and one more in each pass after, with the ★ arm in all
five languages; each call sorts a copy. Every implementation prints `5
passes over 20 arrays of 10^5: checksum 435550478`. C sorts with
`qsort` and a comparison function, Rust with the stable `sort` as Kāra
does, Go with `slices.Sort` and Python with `sorted`.

BENCHTAB
