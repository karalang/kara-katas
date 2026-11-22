# 2742. Painting the Walls

You are given two **0-indexed** integer arrays, `cost` and `time`, of
size `n` representing the costs and the time taken to paint `n`
different walls respectively. There are two painters available:

- A **paid painter** that paints the `i`-th wall in `time[i]` units of
  time and takes `cost[i]` units of money.
- A **free painter** that paints **any** wall in `1` unit of time at a
  cost of `0`. But the free painter can only be used if the paid painter
  is already **occupied**.

Return *the minimum amount of money required to paint the* `n` *walls.*

```
cost = [1, 2, 3, 2], time = [1, 2, 3, 2]  ->  3
cost = [2, 3, 4, 2], time = [1, 1, 1, 1]  ->  4
```

**Constraints:** `1 <= cost.length <= 500`, `cost.length ==
time.length`, `1 <= cost[i] <= 10^6`, `1 <= time[i] <= 500`.

## Approaches

The free painter paints one wall in each unit the paid painter is busy,
so a set of paid walls works exactly when the walls left over number no
more than the paid walls' total time: paying for wall i covers
`time[i] + 1` walls.

| file | mechanism |
|---|---|
| `walls.kara` ★ | `least[j]`, the cheapest way to cover j walls, capped at n: a knapsack filled one wall at a time, j falling so that each wall is paid for once. O(n^2) |
| `walls_memo.kara` | top down: the cheapest way to cover `left` more walls from wall i on, by skipping wall i or paying for it, a recursive function with a `Map[(i64, i64), i64]` memo passed `mut ref`. O(n^2) |
| `walls_table.kara` | the knapsack with its rows kept, `table[i][j]` over the first i walls, each row built from the one before by `map` over the walls covered. O(n^2) time and space |
| `walls_balance.kara` | each wall either paid for, giving the free painter `time[i]` more units, or painted free, using one up; `least[b]` over the balance so far, shifted by n so that it can go below 0 on the way, and kept at n once past it; the answer the least over balances of 0 or more. O(n^2) |
| `walls_solution.kara` | a Rust solution as LeetCode's Rust users write it, an `i32` knapsack `vec![i32::MAX / 2; n + 1]`, `zip` over the two arrays and `.max(0) as usize` for the walls left, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; one wall;
one slow cheap wall that frees all the others; ten walls of one unit
each, so that half of them are paid for; 2000 random sets of 1 to 10
walls costing up to 100 and taking up to 10; and 20 of 500 walls,
LeetCode's most, costing up to `10^6` and taking up to 20, so that many
of them are paid for, each batch with the sum of its answers and a
checksum. `walls.py` mirrors the ★ arm and its output is byte-identical.

```
3
4
7
1
15
2000 small cases: costs sum to 54284, checksum 10006850
20 cases of 500 walls: costs sum to 31884294, checksum 280271358
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every set of walls the paid painter could take, as the bits
of a number, kept when the walls left to the free painter, one a unit,
fit in the units the paid painter is busy, and the cheapest kept; no
knapsack. It draws 1000 random sets of 1 to 10 walls costing up to 50
and taking up to 6, then 200 of up to 100 walls costing up to `10^6` and
taking up to 20, all before any arm answers; the literal reading is
asked only of the first 1000.

| | property |
|---|---|
| P1 | up to 10 walls, the answer is the literal reading's |
| P2 | the walls listed in reverse order: the same answer |
| P3 | every cost doubled: the answer doubled |
| P4 | every wall taking one unit longer: an answer no larger |
| P5 | a wall added: an answer no larger than the old one and its cost |
| P6 | each arm agrees with at least three of the other four |

The differential prints `1200 cases: checksum 671040231, 36000 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases, over every set of paid walls, gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. M1 and M5 fail the same checks, both leaving
out the wall the paid painter paints while the free one works.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a paid wall covers only its time, not its time and itself | P1 418, P6 528 |
| M2 | ★: j rising, so a wall paid for twice | P1 401, P6 563 |
| M3 | memo: each answer stored for one wall fewer to cover | P1 45, P2 148, P4 1, P5 8, P6 159 |
| M4 | memo: a wall paid for never skipped | P1 740, P2 1082, P5 108, P6 934 |
| M5 | table: the free painter's wall not counted | P1 418, P6 528 |
| M6 | table: each row from the first, not the one before | P1 757, P2 485, P3 709, P5 168, P6 947 |
| M7 | balance: a balance below 0 kept at the end | P1 1000, P6 1200 |
| M8 | balance: the balance capped at n, not 2n | P1 676, P2 1075, P6 857 |
| M9 | solution: one more wall covered than paid for | P1 282, P6 385 |
| M10 | solution: the cheaper of the two never kept | P1 741, P2 1082, P6 930 |

## Benchmarks

The bench draws 20 sets of 500 walls, LeetCode's most, costing up to
`10^6` and taking up to 20 units, all of them first, then answers each
100 times by the ★ arm in all five languages. Every implementation
prints `20 cases of 500 walls, 100 rounds: costs sum to 2975079500,
checksum 528022945`.

BENCHTAB

## Verification

All five arms print the same output as `walls.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as first written.

LeetCode's Rust template took one `karac fix` of 13 edits, the wrapper
included: `struct Solution {}` added, `Vec<i32>` became `Vec[i32]`,
`vec![i32::MAX / 2; n + 1]` became `Vec.filled(n + 1, i32.MAX / 2)`, the
`(&c, &t)` pattern and the wrapper's `&x` patterns dropped their `&`, and
`Solution::` became `Solution.` with the `as i64` dropped. `(j as i32 -
t - 1).max(0) as usize` is Kāra as it stands.
