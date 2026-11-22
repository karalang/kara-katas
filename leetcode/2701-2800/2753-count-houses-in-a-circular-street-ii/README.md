# 2753. Count Houses in a Circular Street II

You are given an object `street` of class `Street` that represents a
circular street and a positive integer `k` which represents a maximum
bound for the number of houses in that street (in other words, the
number of houses is less than or equal to `k`). Houses' doors could be
open or closed initially (at least one is open).

Initially, you are standing in front of a door to a house on this
street. Your task is to count the number of houses in the street.

The class `Street` contains the following functions which may help you:

- `void closeDoor()`: Close the door of the house you are in front of.
- `boolean isDoorOpen()`: Returns `true` if the door of the current
  house is open and `false` otherwise.
- `void moveRight()`: Move to the right house.

Return `ans` *which represents the number of houses on this street.*

```
street = [1, 1, 1, 1, 1], k = 5   ->  5
street = [1, 0, 1, 0], k = 7      ->  4
```

**Constraints:** `n == number of houses`, `1 <= n <= k <= 10^5`,
`street` is circular by definition, and at least one door is open.

## Approaches

The problem is interactive: the street is hidden, and a solution sees
only the door it stands at and can only close doors and move right. From
an open door, a walk of k houses right passes every house and comes back
to the start at step n; closing each open door met leaves the start's
own door the last open one met, so the last step that meets an open
door is n. Each arm takes the street as a `mut ref Street`, which counts
the moves; the harness plays LeetCode's judge.

| file | mechanism |
|---|---|
| `count.kara` ★ | walked right to an open door, then k houses right, every open door met closed and its step kept; the last step kept is the count. Fewer than 2k moves |
| `count_left.kara` | the same walked left, a `while` counting the steps by hand. Fewer than 2k moves |
| `count_marks.kara` | the steps that meet an open door all written down in a `Vec`, and the count its last |
| `count_fold.kara` | the walk of k as a `fold` over the steps, the closure holding the street as a `mut ref` and carrying the last step met |
| `count_solution.kara` | a Rust solution as LeetCode's Rust users write it, the street by `&mut Street`, `ans` set to each step within k that meets an open door, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; one house;
10^5 houses, LeetCode's most, all open, and one open among them, with
k = 10^5; 3000 random streets of 1 to 12 houses with k up to 15; and 30
of up to 10^5 with k up to 10^5, the last two with the sum of the counts
and a checksum. `count.py` mirrors the ★ arm and its output is
byte-identical.

```
5
4
1
100000
100000
3000 streets of up to 12: houses sum to 19389, checksum 367657236
30 streets of up to 100000: houses sum to 410275, checksum 941228907
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the houses of the judge's street counted where the judge
holds them; no walking. It draws 2000 random streets of 1 to 12 houses
with k up to 15, then 50 of up to 2000 with k up to 2000, all before any
arm answers; the literal reading is asked only of the first 2000.

| | property |
|---|---|
| P1 | up to 12 houses, the count is the literal reading's |
| P2 | every door open: the same count |
| P3 | the walk begun one house to the right: the same count |
| P4 | k seven more: the same count |
| P5 | from 1 to k, in no more than 2k moves |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 995920439, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the walk of k begun without first finding an open door | P1 720, P2 743, P3 1210, P6 743 |
| M2 | ★: the open doors met left open | P1 1595, P2 648, P3 461, P4 2047, P6 1644 |
| M3 | left: the steps counted before the move | P1 1174, P2 1210, P3 571, P6 1210 |
| M4 | left: the walk one house short of k | P1 244, P2 168, P3 70, P4 244, P5 24, P6 244 |
| M5 | marks: the first meeting taken, not the last | P1 1663, P2 828, P3 581, P6 1713 |
| M6 | marks: the steps counted from 0 | P1 2000, P5 175, P6 2050 |
| M7 | fold: the last step kept whether or not it met an open door | P1 1756, P4 2050, P6 1806 |
| M8 | fold: an open door met never closed | P1 1595, P2 648, P3 461, P4 2047, P6 1644 |
| M9 | solution: the walk of k run to k - 1 | P1 244, P2 153, P3 78, P4 244, P5 24, P6 244 |
| M10 | solution: the first open door met kept, not the last | P1 1663, P2 828, P3 581, P6 1713 |

## Benchmarks

The bench draws 30 streets of up to 10^5 houses, LeetCode's most, with
k = 10^5, all of them first, then walks each 20 times by the ★ arm in
all five languages, every walk on a fresh copy of its street, since the
walk closes the doors it meets, through a street that counts its moves.
Every implementation prints `30 streets, 20 rounds: houses sum to
9613320 in 60000660 moves, checksum 682769773`.

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
`fold` arm's closure captures the `mut ref Street` parameter and moves
it, which the checker accepts as written.

LeetCode's Rust template took 7 `karac fix` edits, the wrapper included:
`struct Solution {}` added; `&mut Street` became `mut ref Street` in the
solution and the wrapper, and the wrapper's argument `mut street`; `!`
became `not`; the wrapper's `as i64` on the answer, an `i32` widening by
itself, was dropped; and `Solution::` became `Solution.`.
