# 2790. Maximum Number of Groups With Increasing Length

You are given a **0-indexed** array `usageLimits` of length `n`.

Your task is to create **groups** using numbers from `0` to `n - 1`,
ensuring that each number, `i`, is used no more than `usageLimits[i]`
times in total **across all groups**. You must also satisfy the
following conditions:

- Each group must consist of **distinct** numbers, meaning that no
  duplicate numbers are allowed within a single group.
- Each group (except the first one) must have a length **strictly
  greater** than the previous group.

Return *an integer denoting the **maximum** number of groups you can
create while satisfying these conditions.*

```
usageLimits = [1, 2, 5]  ->  3
usageLimits = [2, 1, 2]  ->  2
usageLimits = [1, 1]     ->  1
```

**Constraints:** `1 <= usageLimits.length <= 10^5`, `1 <= usageLimits[i]
<= 10^9`.

## Approaches

k groups are best made of sizes 1 to k, needing k(k + 1) / 2 places.
Taking the limits from the least, one more group can be filled once the
limits taken so far sum to the next triangular number, and each number
taken adds at most one group. The cut arm reaches the same answer
another way, by the cut condition of the flow from numbers to groups.

| file | mechanism |
|---|---|
| `groups.kara` ★ | the limits sorted from the least, a running sum of places, and one more group whenever it reaches `(groups + 1) * (groups + 2) / 2`. O(n log n) |
| `groups_cut.kara` | by binary search and a cut: k groups of sizes 1 to k can be filled just when, for each t up to k, the t largest groups' `t * k - t(t - 1) / 2` places are met by the numbers each given at most t times, the sum of `min(u, t)`; those sums found once for every t from the sorted limits, and the greatest such k searched. O(n log n) |
| `groups_counts.kara` | a `SortedMap` from each limit to how many numbers have it, walked from the least limit, the numbers of one limit taken one at a time into the ★ arm's running sum. O(n log n) |
| `groups_fold.kara` | the ★ arm's walk as one `fold` over the sorted limits, its state the tuple (groups, places). O(n log n) |
| `groups_solution.kara` | a Rust solution as LeetCode's Rust users write it, `mut usage_limits` `sort_unstable`d and an `i64` running sum against `(ans + 1) * (ans + 2) / 2`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's three examples; one
number allowed `10^9` times; `10^5` numbers each allowed `10^9` times,
LeetCode's most, and each allowed once; 3000 random arrays of 1 to 12
limits from 1 to 10; and 20 of `10^5` limits up to `10^9`, the last two
with the sum of the answers and a checksum. `groups.py` mirrors the ★
arm and its output is byte-identical.

```
3
2
1
1
100000
446
3000 small arrays: groups sum to 18361, checksum 220533699
20 arrays of 10^5: groups sum to 2000000, checksum 363526282
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: groups chosen one after another, each a set of distinct
numbers by the bits of a mask, longer than the group before it, and no
number used more times than its limit; every such run of groups
searched, and the longest kept; no sorting and no sums. It draws 2000
random arrays of 1 to 5 limits from 1 to 6, then 50 of up to 2000 limits
up to `10^9`, all before any arm answers; the literal reading is asked
only of the first 2000.

| | property |
|---|---|
| P1 | up to 5 numbers, the answer is the literal reading's |
| P2 | the limits reversed: the same answer |
| P3 | a number allowed `10^9` times added: the answer or one more |
| P4 | every limit cut to n: the same answer |
| P5 | from 1 to n, and k groups' k(k + 1) / 2 places no more than the limits' sum |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 262306441, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases by the same search gives the same checksum. On
a failure it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: one number adding as many groups as its places reach | P1 1182, P3 2050, P4 1088, P5 1130, P6 1232 |
| M2 | ★: the limits left unsorted | P1 80, P2 46, P4 34, P6 80 |
| M3 | cut: each number above t given only t - 1 | P1 2000, P5 2050, P6 2050 |
| M4 | cut: the largest groups counted one place short each | P1 260, P5 158, P6 260 |
| M5 | counts: each limit's numbers taken once | P1 745, P4 850, P6 745 |
| M6 | counts: a limit's first number counted twice | P1 1927, P3 2050, P4 1314, P5 1976, P6 1977 |
| M7 | fold: the places spent on each group forgotten | P1 1026, P4 668, P6 1026 |
| M8 | fold: one group counted before any number | P1 675, P4 589, P5 725, P6 725 |
| M9 | solution: the limits sorted from the greatest | P1 102, P3 162, P4 50, P6 102 |
| M10 | solution: a sum just reaching the next group's places not enough | P1 624, P4 313, P5 65, P6 624 |

## Benchmarks

The bench draws 20 arrays of `10^5` limits, every other one up to
`10^9`, LeetCode's most, and the rest up to `10^5`, so that the groups
run out before the numbers do; all of them first, then answers each 10
times by the ★ arm in all five languages, each answer sorting its own
copy. Every implementation prints `20 arrays of 10^5, 10 rounds: groups
sum to 19991730, checksum 552623391`.

BENCHTAB

## Verification

All five arms print the same output as `groups.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

Three of the own arms checked clean as first written. The cut arm was
written as Rust writes it, a closure `|k: i64| -> bool` and `let (mut
low, mut high) = (0, n)`; `karac check` refused both, a closure
declaring no return type and `mut` going before the whole pattern, and
`karac fix` made them `|k: i64|` and `let mut (low, high)`. Its first
draft also searched the sorted limits by `partition_point` for each t
inside every probe, which under the interpreter took minutes over the
large cases; the sums are now found once.

LeetCode's Rust template took 12 `karac fix` edits, the wrapper
included: `struct Solution {}` added; the `Vec<..>`s became `Vec[..]`;
the `mut usage_limits` parameter became `usage_limits: own Vec[i32]`
with a `let mut usage_limits = usage_limits;` rebinding; `sort_unstable`
became `sort`; `for &x` and the wrapper's `|&v|` dropped their `&`; the
wrapper's `as i64` on the answer, an `i32` widening by itself, was
dropped; and `Solution::` became `Solution.`.
