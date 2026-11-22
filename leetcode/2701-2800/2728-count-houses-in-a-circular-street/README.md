# 2728. Count Houses in a Circular Street

You are given an object `street` of class `Street` that represents a
circular street and a positive integer `k` which represents a maximum
bound for the number of houses in that street (in other words, the
number of houses is less than or equal to `k`). Houses' doors could be
open or closed initially.

Initially, you are standing in front of a door to a house on this
street. Your task is to count the number of houses in the street.

The class `Street` contains the following functions which may help you:

- `void openDoor()`: Open the door of the house you are in front of.
- `void closeDoor()`: Close the door of the house you are in front of.
- `boolean isDoorOpen()`: Returns `true` if the door of the current
  house is open and `false` otherwise.
- `void moveRight()`: Move to the right house.
- `void moveLeft()`: Move to the left house.

Return `ans` *which represents the number of houses on this street.*

```
street = [0, 0, 0, 0], k = 10     ->  4
street = [1, 0, 1, 1, 0], k = 5   ->  5
```

**Constraints:** `n == number of houses`, `1 <= n <= k <= 10^3`.

## Approaches

The problem is interactive: the street is hidden, and a solution sees
only the door it stands at. Walking k houses one way passes every
house, so the doors can all be set one way, one door marked the other,
and the houses counted on the way round to the mark. Each arm takes the
street as a `mut ref Street`, which counts the moves; the harness plays
LeetCode's judge.

| file | mechanism |
|---|---|
| `count.kara` ★ | every door closed walking k houses right, the door here opened as the mark, and the houses counted walking right until it comes round. 2k + n moves |
| `count_left.kara` | the same walked left: every door closed walking k houses left, the door here opened, and the houses counted walking left back to it, a `loop` with a `return`. 2k + n moves |
| `count_closed.kara` | the mark inverted: every door opened walking k houses right, the door here closed, and the houses counted until the closed door comes round. 2k + n moves |
| `count_marks.kara` | by a walk of 2k: every door closed and the mark opened, then the street walked k more houses right with every step that meets the mark written down, and the count the first of them. 3k moves |
| `count_solution.kara` | a Rust solution as LeetCode's Rust users write it, the street by `&mut Street`, every door closed over k moves right, the mark opened, and `ans` counted moving right until it is open again, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; one house;
1000 houses, LeetCode's most, all open, with k = n, and 999 with k =
1000; 3000 random streets of 1 to 12 houses with k up to 15; and 300 of
up to 1000 with k up to 1000, the last two with the sum of the counts
and a checksum. `count.py` mirrors the ★ arm and its output is
byte-identical.

```
4
5
1
1000
999
3000 streets of up to 12: houses sum to 19714, checksum 316280814
300 streets of up to 1000: houses sum to 142450, checksum 800629466
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the houses of the judge's street counted where the judge
holds them; no walking. It draws 2000 random streets of 1 to 12 houses
with k up to 15, then 50 of up to 1000, LeetCode's most, with k up to
1000, all before any arm answers; the literal reading is asked only of
the first 2000.

| | property |
|---|---|
| P1 | up to 12 houses, the count is the literal reading's |
| P2 | every door turned the other way: the same count |
| P3 | the walk begun one house to the right: the same count |
| P4 | k seven more: the same count |
| P5 | from 1 to k, in no more than 3k moves |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 723020819, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. M4 and M5 never finish: a mutant that loops is
killed by the 600 s limit.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: only half of the k doors closed | P1 831, P2 1095, P3 714, P4 797, P6 870 |
| M2 | ★: the mark's own house not counted | P1 2000, P5 160, P6 2050 |
| M3 | left: the doors opened on the way, not closed | P1 1840, P6 1890 |
| M4 | left: the count stopped at the first closed door | killed under both: timed out (600 s) |
| M5 | closed: the mark left open | killed under both: timed out (600 s) |
| M6 | closed: the walk of k doors never opening them | P1 1680, P2 1890, P3 1329, P4 1145, P6 1730 |
| M7 | marks: the last meeting taken, not the first | P1 708, P4 1556, P6 719 |
| M8 | marks: the mark never made | killed under both: runtime error: index out of bounds |
| M9 | solution: the walk counted from the mark's house again | P1 1840, P6 1890 |
| M10 | solution: the mark's own house not counted | P1 2000, P5 160, P6 2050 |

## Benchmarks

The bench draws 300 streets of up to 1000 houses, LeetCode's most, with
k = 1000, all of them first, then walks each 500 times by the ★ arm in
all five languages, through a street that counts its moves; after the
first walk every street's doors are closed but its mark, where each walk
after starts. Every implementation prints `300 streets, 500 rounds:
houses sum to 76916500 in 226916500 moves, checksum 352814894`.

BENCHTAB

## Verification

All five arms print the same output as `count.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms and the harness checked clean as first written; the
harness's constructor took its doors as `own Vec[bool]` from the start,
the lesson of kata 2782.

LeetCode's Rust template took 7 `karac fix` edits, the wrapper included:
`struct Solution {}` added; `&mut Street` became `mut ref Street` in the
solution and the wrapper, and the wrapper's argument `mut street`; `!`
became `not`; the wrapper's `as i64` on the answer, an `i32` widening by
itself, was dropped; and `Solution::` became `Solution.`.
