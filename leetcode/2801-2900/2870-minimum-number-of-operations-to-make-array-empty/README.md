# 2870. Minimum Number of Operations to Make Array Empty

You are given a **0-indexed** array `nums` consisting of positive
integers.

There are two types of operations that you can apply on the array **any**
number of times:

- Choose **two** elements with **equal** values and **delete** them from
  the array.
- Choose **three** elements with **equal** values and **delete** them
  from the array.

Return *the **minimum** number of operations required to make the array
empty, or* `-1` *if it is not possible*.

```
nums = [2,3,3,2,2,4,2,3,4]  ->  4
nums = [2,1,2,2,3,3]        ->  -1
```

**Constraints:** `2 <= nums.length <= 10^5`; `1 <= nums[i] <= 10^6`.

## Approaches

| file | mechanism |
|---|---|
| `empty.kara` ★ | each value is removed on its own, two or three at a time, and f copies take ceil(f / 3) operations, with 4 = 2 + 2 when f leaves a remainder of 1; a value seen once cannot go. The counts come from the sorted array's runs |
| `empty_map.kara` | the counts in a `Map`, then summed over its values, which needs no order: ceil(f / 3) each, or -1 if any count is 1 |
| `empty_dp.kara` | the fewest operations for f copies by dynamic programming, not by formula: best[f] = 1 + the better of best[f - 2] and best[f - 3], with 1 unreachable, up to the largest count; the counts by sorting |
| `empty_cases.kara` | threes as many as will go, by the remainder: 3q takes q; 3q + 2 takes q + 1; 3q + 1 gives a three back for two twos, q + 1 again, but only once q is at least 1. The counts by a `Map`'s `entry` |
| `empty_solution.kara` | a Rust solution as LeetCode's Rust users write it: a `HashMap` counted with `*cnt.entry(x).or_insert(0) += 1`, then `(c + 2) / 3` summed over `cnt.values()`, returning -1 on a count of 1, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 4 lines: LeetCode's two examples; 10^5
values, LeetCode's most, all equal, and every value twice; then 3000
random arrays of 2 to 10 values from 1 to 4, and 30 of 10^4 to 10^5,
every other one with each value it holds 2 to 8 times and the rest with
counts from 1 up, all shuffled, as a total of the answers, -1 included,
and a checksum. `empty.py` mirrors the ★ arm and its output is
byte-identical.

```
4 -1
33334 50000
3000 short arrays: -520 operations, checksum 252995981
30 long arrays: 315491 operations, checksum 630017908
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every way to take two or three equal values at a time
searched from the array's counts, the fewest operations that empty it
kept, each set of counts searched once and kept in a `Map[String, i64]`
by its counts written out. It draws 2000 random arrays of 2 to 10
values from 1 to 4, then 50 of up to 3000, every other one with each
value it holds at least twice, all before any arm answers; the literal
reading is asked only of the first 2000.

| | property |
|---|---|
| P1 | up to 10 values, the answer is the literal reading's |
| P2 | every value v made 2v + 1: the same answer |
| P3 | the array three times over: n |
| P4 | two more of the first value: the same answer or one more, when the array can be emptied |
| P5 | -1 exactly when a value is seen once, else from n / 3 to n / 2 |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases, 18216 operations: checksum
83261639, 61500 checks over 5 arms: 0 failures` under every lane in
Verification, and a Python reading of the same cases gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a run of one let through | P1 1573, P5 1598, P6 1598 |
| M2 | ★: f / 3 rounded down | P1 398, P5 423, P6 423 |
| M3 | map: a count kept one short | P1 1018, P5 1040, P6 1043 |
| M4 | map: rounded to halves | P1 251, P3 2050, P5 271, P6 276 |
| M5 | dp: three never taken | P1 251, P3 2050, P5 271, P6 276 |
| M6 | dp: a new run's count started at 0 | P1 1018, P5 1040, P6 1043 |
| M7 | cases: 3q + 1 taken as q | P1 107, P5 45, P6 132 |
| M8 | cases: 3q + 2 taken as q | P1 366, P4 253, P5 339, P6 391 |
| M9 | solution: a count of 1 let through | P1 1573, P5 1598, P6 1598 |
| M10 | solution: rounded one past | P1 231, P3 2050, P5 213, P6 256 |

## Benchmarks

The bench draws 50 arrays of 10^5 values, LeetCode's most, each value
held 2 to 8 times and up to 10^6, all of them shuffled first, then
answers each 10 times by the ★ arm in all five languages; each sorts a
fresh copy, C by `qsort`. Every implementation prints `50 arrays of
100000, 10 rounds: 16373260 operations, checksum 940373214`.

BENCHTAB

## Verification

All five arms print the same output as `empty.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as first written, `*counts.entry(v)
.or_insert(0) += 1` and a `return -1` from inside a `match` arm among
them.

LeetCode's Rust template took 14 `karac fix` edits in one run, the
wrapper included: `use std::collections::HashMap;` went and `struct
Solution {}` came for the `impl`, `HashMap::new()` becoming
`Map.new()`; `Vec<..>` became `Vec[..]`; `for &x in &nums` became `for
x in ref nums` and `for &c in cnt.values()` lost its `&`; `|&x|` lost its
`&`, the wrapper's `as i64` went, an `i32` widening, and `Solution::`
took `.`. `*cnt.entry(x).or_insert(0) += 1` was accepted as written.
