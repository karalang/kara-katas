# 2769. Find the Maximum Achievable Number

Given two integers, `num` and `t`. A **number** `x` is **achievable** if
it can become equal to `num` after applying the following operation **at
most** `t` times:

- Increase or decrease `x` by `1`, and *simultaneously* increase or
  decrease `num` by `1`.

Return the **maximum** possible value of `x`.

```
num = 4, t = 1  ->  6
num = 3, t = 2  ->  7
```

**Constraints:** `1 <= num, t <= 50`.

## Approaches

An operation changes the gap `x - num` by -2, 0 or +2, so x meets num
within t operations just when the gap is even and at most 2t either way.

| file | mechanism |
|---|---|
| `achievable.kara` ★ | x down by 1 and num up by 1 at every operation closes the gap by 2, so the answer is `num + 2 * t`. O(1) |
| `achievable_walk.kara` | every x from num + 3t down walked toward num, the greater stepping down and the other up while they differ and an operation is left; the first x that meets num is the answer. O(t^2) |
| `achievable_reach.kara` | backwards from a gap of 0, the gaps that can close within t operations gathered step by step in a `SortedSet`, each grown by -2, 0 and +2; the greatest, read by `max`, gives x. O(t^2 log t) |
| `achievable_table.kara` | a `Vec[bool]` over every x from num - 2t - 2 to num + 2t + 2 of whether x has met num within k operations, built up from k = 0, where only num itself has; the greatest x marked. O(t^2) |
| `achievable_solution.kara` | a Rust solution as LeetCode's Rust users write it, `num + t * 2` in `i32`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 5 lines: LeetCode's two examples; LeetCode's
least and most, 1 and 1 and 50 and 50; and every num and t from 1 to 50,
with the sum of the answers and a checksum. `achievable.py` mirrors the
★ arm and its output is byte-identical.

```
6
7
3
150
2500 pairs: answers sum to 191250, checksum 207378025
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: for every x from num - 4t to num + 4t, every pair of x and num
reachable by up to t operations, each moving x by 1 either way and num
by 1 either way, gathered in a `Set`; x achievable when one of them has
x equal to num, and the greatest such x the answer; no gap. It takes
every num and t from 1 to 50; the literal reading is asked only up to
num 25 and t 4.

| | property |
|---|---|
| P1 | up to num 25 and t 4, the answer is the literal reading's |
| P2 | num one more: the answer one more |
| P3 | t one more: the answer two more |
| P4 | the answer meets num: x down and num up by 1 meet within t steps |
| P5 | one and two more than the answer never meet num that way |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2500 cases: checksum 871836664, 75000 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases by the same pairs gives the same checksum. On
a failure it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. The answer being num + 2t, many edits land on
the same wrong formula and fail the same checks: M1 and M8 give num + t,
M2, M3 and M4 num + 2t - 2, M6 and M7 num + 2t + 2, and M9 and M10 2num
+ t.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: x only t above num | P1 100, P3 2500, P4 1250, P5 2500, P6 2500 |
| M2 | ★: one operation fewer | P1 100, P5 2500, P6 2500 |
| M3 | walk: the walk one step short | P1 100, P5 2500, P6 2500 |
| M4 | walk: the search started below the answer | P1 100, P5 2500, P6 2500 |
| M5 | reach: the gap never growing | P1 100, P3 2500, P5 2500, P6 2500 |
| M6 | reach: one round too many | P1 100, P4 2500, P6 2500 |
| M7 | table: num marked one place off | P1 100, P4 2500, P6 2500 |
| M8 | table: the gap moved by 1, not 2 | P1 100, P3 2500, P4 1250, P5 2500, P6 2500 |
| M9 | solution: num doubled, not t | P1 96, P2 2500, P3 2500, P4 1850, P5 1225, P6 2450 |
| M10 | solution: num and t passed swapped | P1 96, P2 2500, P3 2500, P4 1850, P5 1225, P6 2450 |

## Benchmarks

The bench draws `10^6` random pairs of num and t from 1 to 50, all of
them first, then answers each 50 times by the ★ arm in all five
languages, each answer folded into a running checksum. The answer is one
addition, so the bench measures the loop and the checksum's chain of
remainders more than the problem. Every implementation prints `1000000
pairs, 50 rounds: answers sum to 3822529000, checksum 687076878`.

BENCHTAB

## Verification

All five arms print the same output as `achievable.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The ★ and table arms checked clean as first written. The walk arm wrote
Rust's `let (mut a, mut b) = (x, num)`; `karac check` refused it, as
Kāra puts `mut` before the whole pattern, and `karac fix` wrote `let
mut (a, b) = (x, num)`. The reach arm read the greatest gap by Rust's
`BTreeSet::last`; `karac check` said Kāra's `SortedSet` calls it `max`,
and `karac fix` wrote `gaps.max()`.

LeetCode's Rust template took 3 `karac fix` edits, the wrapper included:
`struct Solution {}` added, and `Solution::` became `Solution.`, with
the wrapper's `as i64` dropped.
