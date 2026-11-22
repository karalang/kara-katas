# 2848. Points That Intersect With Cars

You are given a **0-indexed** 2D integer array `nums` representing the
coordinates of the cars parking on a number line. For any index `i`,
`nums[i] = [start_i, end_i]` where `start_i` is the starting point of
the `ith` car and `end_i` is the ending point of the `ith` car.

Return *the number of integer points on the line that are covered with
**any part** of a car.*

```
nums = [[3,6],[1,5],[4,7]]  ->  7
nums = [[1,3],[5,8]]        ->  7
```

**Constraints:** `1 <= nums.length <= 100`; `nums[i].length == 2`;
`1 <= start_i <= end_i <= 100`.

## Approaches

| file | mechanism |
|---|---|
| `points.kara` ★ | the road is only 100 long, so each car marks its points in an `Array[bool, 101]` from `[false; 101]`, and the marked ones are counted |
| `points_merge.kara` | the cars as `(i64, i64)` sorted by where they start with `sort_by_key`, then merged into runs, a car that starts past the end of the run so far closing it; works for any length of road |
| `points_sweep.kara` | a difference array: each car adds one where it starts and takes one away just past where it ends, and a running sum by `scan` counts the points with at least one car on them |
| `points_set.kara` | every car's points spelt out by `flat_map` over its range and gathered into a `Set`, the answer its size |
| `points_solution.kara` | a Rust solution as LeetCode's Rust users write it: a `[false; 102]` of marks over `for v in nums.iter()`, the inner range `v[0] as usize..=v[1] as usize`, and `iter().filter(\|&&b\| b).count() as i32`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 5 lines: LeetCode's two examples; one car of
one point and one over the whole road; 100 cars, LeetCode's most, each
of one point; then 3000 random parkings of 1 to 6 cars within 1 to 20,
and 300 of 1 to 100 cars within 1 to 100, as totals and checksums.
`points.py` mirrors the ★ arm and its output is byte-identical.

```
7 7
1 100
100
3000 short roads: 32478 points, checksum 120866498
300 long roads: 28250 points, checksum 146669782
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every integer point from 1 to 100 asked whether any
car starts at or before it and ends at or after it. It draws 2000
random parkings of 1 to 6 cars within 1 to 20, then 50 of 1 to 100
cars within 1 to 100, all before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the cars in the other order: the same answer |
| P3 | the road mirrored, x made 101 - x: the same answer |
| P4 | the first car parked twice: the same answer |
| P5 | a car over the whole road added: 100 |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 517303103, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a car's last point left off | P1 2050, P5 2050, P6 2050 |
| M2 | ★: point 100 never counted | P1 49, P3 382, P5 2050, P6 49 |
| M3 | merge: the cars left unsorted | P1 1435, P2 1631, P3 1590, P5 2006, P6 1435 |
| M4 | merge: a car starting at the run's last point closing it | P1 522, P2 82, P3 187, P4 339, P5 73, P6 522 |
| M5 | merge: a car inside the run shortening it | P1 756, P2 276, P3 947, P4 121, P5 2023, P6 756 |
| M6 | sweep: the change taken away at the end, not after it | P1 2050, P5 2050, P6 2050 |
| M7 | sweep: points with two cars only | P1 2023, P4 1342, P5 2037, P6 2023 |
| M8 | set: each car's last point left off | P1 2050, P5 2050, P6 2050 |
| M9 | solution: each car's first point left off | P1 2050, P5 2050, P6 2050 |
| M10 | solution: the unmarked points counted | P1 2049, P5 2050, P6 2049 |

## Benchmarks

The bench draws 10^4 parkings of up to 100 cars, LeetCode's most, all
of them first, then answers each 50 times by the ★ arm in all five
languages, each answer marking a fresh road of 101 places. Every
implementation prints `10000 parkings, 50 rounds: 47033600 points,
checksum 943753208`.

BENCHTAB

## Verification

All five arms print the same output as `points.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The merge arm, as first written, took the first car with `let (mut lo,
mut hi) = cars[0];`, and `karac check` reported E0001 twice, `mut`
going before the whole pattern in Kāra; `karac fix` wrote Kāra's `let mut
(lo, hi) = cars[0];`. The sweep arm's `scan` closure, written as Rust
writes it with `*cars += d; Some(*cars)`, drew E0200 on the state
parameter, which a Kāra `scan` passes by value and takes back from the
closure's pair; `karac fix` rewrote it to `let cars = cars + d;
Some((cars, cars))`. The other arms checked clean.

LeetCode's Rust template took 14 `karac fix` edits in one run, the
wrapper included: `struct Solution {}` added for the `impl`; `Vec<..>`
became `Vec[..]`; `|&&b|` and `|&x|` lost their `&`; `Solution::` took
`.`, and the wrapper's `as i64` went, an `i32` widening. The inclusive
range `v[0] as usize..=v[1] as usize` and `count() as i32` were
accepted as written.
