# 2833. Furthest Point From Origin

You are given a string `moves` of length `n` consisting only of
characters `'L'`, `'R'`, and `'_'`. The string represents your movement
on a number line starting from the origin `0`.

In the `ith` move, you can choose one of the following directions:

- move to the left if `moves[i] = 'L'` or `moves[i] = '_'`
- move to the right if `moves[i] = 'R'` or `moves[i] = '_'`

Return *the **distance from the origin** of the **furthest** point you
can get to after* `n` *moves*.

```
moves = "L_RL__R"  ->  3
moves = "_R__LL_"  ->  5
moves = "_______"  ->  7
```

**Constraints:** `1 <= moves.length == n <= 50`; `moves` consists only
of characters `'L'`, `'R'` and `'_'`.

## Approaches

| file | mechanism |
|---|---|
| `furthest.kara` ★ | counting: every blank is best spent the way the fixed moves already lean, so the gap between the L and R counts, by `chars().filter(..).count()`, plus every blank |
| `furthest_walk.kara` | two walks over `chars()`, one with every blank a step left and one with every blank a step right, and the furthest of the two ends |
| `furthest_fold.kara` | one `fold` over `bytes()` into a pair, the position the fixed moves reach and the blanks still free, matched byte by byte |
| `furthest_reach.kara` | every position in reach: a `Vec[bool]` over -n..=n, each move spreading the set one step left, right or both, and the furthest set position at the end; O(n^2) |
| `furthest_solution.kara` | a Rust solution as LeetCode's Rust users write it: three counters in `let (mut l, mut r, mut u)`, a `match` over `chars()`, and `(l - r).abs() + u` as `i32`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 6 lines: LeetCode's three examples; one move
of each kind; "LR" 25 times and "L" 50 times, LeetCode's most; then
20000 random strings of 1 to 50 moves, the blank drawn 0 to 5 times in
6, as a total and a checksum. `furthest.py` mirrors the ★ arm and its
output is byte-identical.

```
3
5
7
1 1 1
0 50
20000 random strings: distances total 287436, checksum 879980914
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every way of taking the blanks left or right, by a bit
mask, each walked from 0, and the furthest end. It draws 2000 random
strings of 1 to 12 moves, then 50 of up to 50, all before any arm
answers; the literal reading is asked only of the first 2000.

| | property |
|---|---|
| P1 | up to 12 moves, the answer is the literal reading's |
| P2 | the moves reversed: the same answer |
| P3 | every L made R and every R made L: the same answer |
| P4 | one blank added at the end: one further |
| P5 | "LR" added at the end: the same answer |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 541352947, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the blanks left out | P1 1473, P4 2050, P6 1513 |
| M2 | ★: the gap taken without its sign | P1 1045, P3 1568, P6 1077 |
| M3 | walk: only the walk with the blanks left | P1 785, P3 1106, P4 436, P6 812 |
| M4 | walk: a blank taken as the step before it | P1 785, P3 1106, P4 436, P6 812 |
| M5 | fold: a blank taken as a step right | P1 286, P3 1106, P4 245, P6 294 |
| M6 | fold: the blanks against the lean | P1 1071, P4 681, P6 1106 |
| M7 | reach: a step right from an L | killed under both: runtime error: called unwrap() on None |
| M8 | reach: the nearest end, not the furthest | P1 1363, P4 1292, P6 1403 |
| M9 | solution: a blank counted as an R | P1 286, P3 1106, P4 245, P6 294 |
| M10 | solution: the gap and the blanks subtracted | P1 1473, P4 2050, P6 1513 |

## Benchmarks

The bench draws 10^5 strings of 50 moves, LeetCode's most, all of them
first, then answers each 100 times by the ★ arm in all five languages.
Every implementation prints `100000 strings of 50, 100 rounds:
distances total 273829800, checksum 259364196`.

BENCHTAB

## Verification

All five arms print the same output as `furthest.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

Three of the four own arms checked clean as first written. The fold
arm wrote `moves.bytes().fold(..)`, and `bytes()` is a `Slice` in
Kāra: `karac check` reported E0236, "no method 'fold' on type 'Slice':
iterator adaptors/terminals require an explicit `.iter()`", and `karac
fix` inserted the `.iter()`. The same run also reported "tuple pattern
used but type is `?T0`" for the `let (at, free)` the fold fed, a
follow-on of the first error that the same fix cleared.

LeetCode's Rust template took 11 `karac fix` edits in one run, the
wrapper included: `struct Solution {}` added for the `impl`; `let (mut
l, mut r, mut u) = (0, 0, 0)` became `let mut (l, r, u) = (0i32, 0i32,
0i32)`, its literals given the `i32` the return wants, since the
`.abs()` method beside them would otherwise settle them to `i64`
(design.md §8); `&str` became `Str`; `Solution::` took `.`, and the
wrapper's `as i64` went.
