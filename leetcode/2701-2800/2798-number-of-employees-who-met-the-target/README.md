# 2798. Number of Employees Who Met the Target

There are `n` employees in a company, numbered from `0` to `n - 1`.
Each employee `i` has worked for `hours[i]` hours in the company.

The company requires each employee to work for **at least** `target`
hours.

You are given a **0-indexed** array of non-negative integers `hours` of
length `n` and a non-negative integer `target`.

Return *the integer denoting the number of employees who worked at
least* `target` *hours*.

```
hours = [0, 1, 2, 3, 4], target = 2  ->  3
hours = [5, 1, 4, 2, 2], target = 6  ->  0
```

**Constraints:** `1 <= n == hours.length <= 50`, `0 <= hours[i], target
<= 10^5`.

## Approaches

| file | mechanism |
|---|---|
| `met.kara` ★ | the hours at or above the target kept by `filter` and counted. O(n) |
| `met_loop.kara` | by hand: a count raised for each employee whose hours reach the target. O(n) |
| `met_short.kara` | by the ones who fell short: the hours below the target counted by `fold`, and the rest of the team the answer. O(n) |
| `met_sorted.kara` | by sorting: the hours sorted, the first place at or above the target found by `partition_point`, and the places from it on counted. O(n log n) |
| `met_solution.kara` | a Rust solution as LeetCode's Rust users write it, `hours.iter().filter(\|&&h\| h >= target).count() as i32`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; a target of
0, met by everyone; 50 hours of `10^5`, LeetCode's most, against a
target at them and just above; and 3000 random teams of 1 to 50 with
hours and targets up to 20, and 3000 with them up to `10^5`, each with
the sum of the counts and a checksum. `met.py` mirrors the ★ arm and its
output is byte-identical.

```
3
0
3
50
0
3000 teams, hours up to 20: met sum to 40324, checksum 317482960
3000 teams, hours up to 100000: met sum to 37338, checksum 197639844
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: each employee's hours spent one at a time against the hours
still owed, and the employee counted when nothing is owed at the end; no
comparison of hours with the target. It draws 2000 random teams of 1 to
50 with hours and targets up to 20, then 50 with them up to `10^5`, all
before any arm answers; the literal reading is asked only of the first
2000.

| | property |
|---|---|
| P1 | hours up to 20, the count is the literal reading's |
| P2 | the hours and the target 1000 more: the same count |
| P3 | the target one more: less by those who worked just the target |
| P4 | the hours reversed: the same count |
| P5 | from 0 to n, and n when the target is 0 |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 602476928, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: only hours above the target counted | P1 1255, P3 1329, P5 1216, P6 1255 |
| M2 | ★: the first employee left out | P1 1055, P3 102, P4 678, P5 2050, P6 1081 |
| M3 | loop: those who fell short counted | P1 1935, P3 1255, P5 2050, P6 1984 |
| M4 | loop: the count started at 1 | P1 2000, P5 2050, P6 2050 |
| M5 | short: those just at the target counted short | P1 1255, P3 1329, P5 1216, P6 1255 |
| M6 | short: the short ones answered | P1 1935, P3 1255, P5 2050, P6 1984 |
| M7 | sorted: the hours left unsorted | P1 1580, P3 1169, P4 1454, P6 1625 |
| M8 | sorted: the place found one past the target's | P1 1255, P3 1329, P5 1216, P6 1255 |
| M9 | solution: the hours compared with the target less one | P1 1216, P3 1349, P6 1216 |
| M10 | solution: the last employee left out | P1 1051, P3 77, P4 678, P5 2050, P6 1073 |

## Benchmarks

The bench draws 20000 teams of 50, LeetCode's most, with hours and
targets up to `10^5`, all of them first, then answers each 500 times by
the ★ arm in all five languages. Every implementation prints `20000
teams of 50, 500 rounds: met sum to 249153500, checksum 4978142`.

BENCHTAB

## Verification

All five arms print the same output as `met.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

All four own arms and the differential checked clean as first written.

LeetCode's Rust template took 9 `karac fix` edits, the wrapper
included: `struct Solution {}` added; the `Vec<..>`s became `Vec[..]`;
the closure `|&&h|` and the wrapper's `|&h|` dropped their `&`s; the
wrapper's `as i64` on the answer, an `i32` widening by itself, was
dropped; and `Solution::` became `Solution.`. The `count() as i32`
stayed.
