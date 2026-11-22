# 2838. Maximum Coins Heroes Can Collect

There is a battle and `n` heroes are trying to defeat `m` monsters. You
are given two **1-indexed** arrays of **positive** integers `heroes`
and `monsters` of length `n` and `m`, respectively. `heroes[i]` is the
power of the `ith` hero, and `monsters[i]` is the power of the `ith`
monster.

The `ith` hero can defeat the `jth` monster if `monsters[j] <=
heroes[i]`.

You are also given a **1-indexed** array `coins` of length `m`
consisting of **positive** integers. `coins[i]` is the number of coins
that each hero earns after defeating the `ith` monster.

Return *an array* `ans` *of length* `n` *where* `ans[i]` *is the
**maximum** number of coins that the* `ith` *hero can collect from
this battle*.

**Notes:** the health of a hero doesn't get reduced after defeating a
monster; multiple heroes can defeat a monster, but each monster can be
defeated by a given hero only once.

```
heroes = [1,4,2], monsters = [1,1,5,2,3], coins = [2,3,4,5,6]  ->  [5,16,10]
heroes = [5], monsters = [2,3,1,2], coins = [10,6,5,2]          ->  [23]
heroes = [4,4], monsters = [5,7,8], coins = [1,1,1]             ->  [0,0]
```

**Constraints:** `1 <= n == heroes.length <= 10^5`; `1 <= m ==
monsters.length <= 10^5`; `coins.length == m`; `1 <= heroes[i],
monsters[i], coins[i] <= 10^9`.

## Approaches

| file | mechanism |
|---|---|
| `coins.kara` ★ | the monsters `zip`ped with their coins and sorted, prefix sums of the coins, and for each hero the count of monsters no stronger by `partition_point` |
| `coins_sweep.kara` | one sweep: heroes and monsters each in order of power by an index sort (`sort_by_key`), and a running sum of the coins of every monster passed, read off for each hero in turn |
| `coins_floor.kara` | a `SortedMap` from each power to its monsters' coins through `entry().or_insert()`, then a second one to the coins of every monster at most that strong; a hero's coins are the entry at the `floor` of its power |
| `coins_each.kara` | every hero against every monster, the coins of each one no stronger added; O(nm), for the harness's sizes |
| `coins_solution.kara` | a Rust solution as LeetCode's Rust users write it: the monsters' indices sorted with `sort_unstable_by_key`, an `i64` prefix of their coins over `vec![0i64; m + 1]`, and `partition_point` for each hero; its wrapper converts with a closure over `&Vec<i64>` and `collect::<Vec<i32>>()`; carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 6 lines: LeetCode's three examples; a hero
beating every monster of 10^9 coins and one beating none; then 3000
random battles of 1 to 6 heroes and monsters with powers up to 8, and
50 of up to 1000 each with powers and coins up to 10^9, as checksums.
`coins.py` mirrors the ★ arm and its output is byte-identical.

```
[5, 16, 10]
[23]
[0, 0]
[3000000000, 0]
3000 small battles: checksum 171244115
50 large battles: coins total 3164897486653847, checksum 44196301
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: each hero meets every monster in turn and takes the
coins of each one it beats. It draws 2000 random battles of 1 to 6
heroes and monsters with powers up to 8, then 50 of up to 800 each
with powers and coins up to 10^9, all before any arm answers; the
literal reading, O(nm), is asked of every case.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the heroes reversed: the answer reversed |
| P3 | the monsters and their coins reversed together: the same answer |
| P4 | every power doubled: the same answer |
| P5 | a monster of power 1 with 7 coins added: every answer 7 more |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 108504676, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a monster as strong as the hero left out | P1 1325, P5 723, P6 1325 |
| M2 | ★: the pairs left unsorted | P1 1107, P3 1350, P5 1634, P6 1107 |
| M3 | sweep: the heroes taken in the order given | P1 1114, P2 1215, P6 1114 |
| M4 | sweep: a monster as strong as the hero left out | P1 1325, P5 723, P6 1325 |
| M5 | floor: monsters of one power keep only the last one's coins | P1 760, P3 692, P5 727, P6 760 |
| M6 | floor: the entry strictly below the power | P1 1325, P5 723, P6 1325 |
| M7 | each: the weaker monsters' coins taken | P1 2033, P5 1998, P6 2033 |
| M8 | each: the last monster never met | P1 1620, P3 1507, P5 1979, P6 1620 |
| M9 | solution: the prefix one place behind | P1 1887, P3 530, P5 1216, P6 1887 |
| M10 | solution: the monsters sorted by their coins | P1 1124, P3 423, P5 1327, P6 1124 |

## Benchmarks

The bench draws 10 battles of 10^5 heroes and 10^5 monsters,
LeetCode's most, powers and coins up to 10^9, all of them first, then
answers each 5 times by the ★ arm in all five languages. C sorts with
`qsort` and Go with `sort.Slice`, both on the pair as Kāra, Rust and
Python do. Every implementation prints `10 battles of 100000, 5
rounds: checksum 453106472`.

BENCHTAB

## Verification

All five arms print the same output as `coins.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as first written.

LeetCode's Rust template took 37 `karac fix` edits in one run, the
wrapper included: `struct Solution {}` added for the `impl`; `Vec<..>`
became `Vec[..]` and `usize` `i64`; `sort_unstable_by_key` became
`sort_by_key`; `vec![0i64; m + 1]` became `Vec.filled(m + 1, 0)`;
`coins[i] as i64` lost its cast, an `i32` widening; `|&i|`, `|&h|`,
`|&x|` and `for (k, &i)` lost their `&`; in the wrapper `|v:
&Vec<i64>|` became `|v: ref Vec[i64]|`, `collect::<Vec<i32>>()` a bare
`collect()` that the parameter's `Vec[i32]` fixes, and `to32(&heroes)`
`to32(heroes)`; `Solution::` took `.`.
