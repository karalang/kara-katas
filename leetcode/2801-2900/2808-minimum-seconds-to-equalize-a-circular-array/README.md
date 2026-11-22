# 2808. Minimum Seconds to Equalize a Circular Array

You are given a **0-indexed** array `nums` containing `n` integers.

At each second, you perform the following operation on the array:

- For every index `i` in the range `[0, n - 1]`, replace `nums[i]` with
  either `nums[i]`, `nums[(i - 1 + n) % n]`, or `nums[(i + 1) % n]`.

**Note** that all the elements get replaced simultaneously.

Return *the **minimum** number of seconds needed to make all elements
in the array* `nums` *equal*.

```
nums = [1, 2, 1, 2]      ->  1
nums = [2, 1, 3, 3, 2]   ->  2
nums = [5, 5, 5, 5]      ->  0
```

**Constraints:** `1 <= n == nums.length <= 10^5`; `1 <= nums[i] <=
10^9`.

## Approaches

The array ends as one of its values, and a value spreads one place each
way each second, so it fills the circle in half its widest gap between
neighbouring places, the gap from its last place round to its first
included; the answer is the least of those halves.

| file | mechanism |
|---|---|
| `seconds.kara` ★ | each value's places gathered in a `Map[i64, Vec[i64]]` by `entry().or_insert()`, the widest gap of each with the wrap, halved, the least kept |
| `seconds_sorted.kara` | no `Map`: the `(value, place)` pairs sorted, so each value's places come together in order, and each run's widest gap halved |
| `seconds_last.kara` | one pass: each value's first place, last place and widest gap so far in a `Map` of a small struct, updated through `get_mut` as the value comes round again, the wrap added at the end, the least by `min()` over `values()` |
| `seconds_twice.kara` | the circle unrolled: the array walked twice over, so the gap round the end is an ordinary gap the second time, last places and widest gaps in two `Map`s |
| `seconds_solution.kara` | a Rust solution as LeetCode's Rust users write it, a `HashMap<i32, Vec<usize>>` by `entry().or_default()`, the gaps by `windows(2)`, from `usize::MAX` down, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's three examples; 10^5
numbers, LeetCode's most, all different; the same with every third one
7; 3000 random arrays of 1 to 12 numbers from 1 to 4; and 50 of up to
10^5 numbers up to 10^9, from 10 values or from 10^9, the last two with
the sum of the seconds and a checksum. No output depends on the order a
`Map` is walked in, since only a least value is kept. `seconds.py`
mirrors the ★ arm and its output is byte-identical.

```
1
2
0
50000
1
3000 small arrays: seconds sum to 4046, checksum 591396848
50 large arrays: seconds sum to 450433, checksum 799277753
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: for each value, the places that can hold it after each
second, every place taking its own or a neighbour's of the second
before, round the circle, until every place can; the least such second
over the values, and no gaps. It draws 2000 random arrays of 1 to 12
numbers from 1 to 4, then 50 of up to 10^4 numbers up to 10^9, from 10
values or from 10^9, all before any arm answers; the literal reading is
asked only of the first 2000. The large arrays stop at 10^4 so that
the interpreter lane runs in under a minute; the harness covers 10^5.

| | property |
|---|---|
| P1 | up to 12 numbers, the seconds are the literal reading's |
| P2 | 0 just when every number is the same |
| P3 | the circle turned by a third: the same seconds |
| P4 | the numbers reversed: the same seconds |
| P5 | the numbers written twice over: the same, and no more than n / 2 |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 922338185, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the gap round the end left out | P1 1664, P2 1540, P3 55, P5 1690, P6 1690 |
| M2 | ★: the widest gap not halved | P1 2000, P2 215, P5 977, P6 2050 |
| M3 | sorted: a run cut after its first gap | P1 792, P2 10, P3 337, P4 279, P5 1451, P6 817 |
| M4 | sorted: the wrap measured from the run's first place to its first | P1 1473, P2 58, P5 2050, P6 1498 |
| M5 | last: the last place never moved on | P1 1473, P2 58, P5 2050, P6 1498 |
| M6 | last: the wrap gap taken from the first place to the last | P1 1680, P2 1527, P3 131, P5 1893, P6 1730 |
| M7 | twice: the array walked once | P1 1376, P2 766, P3 341, P5 1402, P6 1402 |
| M8 | twice: a gap kept only when it is the first | P1 1231, P2 1048, P3 561, P4 490, P6 1256 |
| M9 | solution: the pairs' gaps one short | P1 353, P2 67, P3 424, P6 364 |
| M10 | solution: the wrap gap from the first place alone | P1 1370, P2 979, P3 644, P4 567, P5 1396, P6 1396 |

## Benchmarks

The bench draws 20 arrays of 10^5 numbers, LeetCode's most, from 1000
values spread up to 10^9, all of them first, then answers each 20 times
by the ★ arm in all five languages, each with its standard hash map;
C, having none, uses an open-addressing table of growable arrays. Every
implementation prints `20 arrays of 10^5, 20 rounds: seconds sum to
571020, checksum 45318179`.

BENCHTAB

## Verification

All five arms print the same output as `seconds.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms and the harness checked clean as first written.

LeetCode's Rust template took 20 `karac fix` edits, the wrapper
included: the `use std::collections::HashMap;` went and
`HashMap<i32, Vec<usize>>` became `Map[i32, Vec[i64]]`, `HashMap::new()`
`Map.new()`; `usize` became `i64` and `usize::MAX` `i64.MAX`; `Vec<..>`
took `[..]`; the `&x` pattern in `for (i, &x)` and in the wrapper's
closure became `x`; `or_default()` became `or_insert(Vec.new())`;
`struct Solution {}` was added; and `Solution::` became `Solution.`,
the wrapper's `as i64` dropped.
