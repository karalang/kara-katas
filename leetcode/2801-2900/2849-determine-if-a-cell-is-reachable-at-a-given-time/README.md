# 2849. Determine if a Cell Is Reachable at a Given Time

You are given four integers `sx`, `sy`, `fx`, `fy`, and a
**non-negative** integer `t`.

In an infinite 2D grid, you start at the cell `(sx, sy)`. Each second,
you **must** move to any of its adjacent cells.

Return `true` *if you can reach cell* `(fx, fy)` *after **exactly***
`t` ***seconds***, *or* `false` *otherwise*.

A cell's **adjacent cells** are the 8 cells around it that share at
least one corner with it. You can visit the same cell several times.

```
sx = 2, sy = 4, fx = 7, fy = 7, t = 6  ->  true
sx = 3, sy = 1, fx = 7, fy = 3, t = 3  ->  false
```

**Constraints:** `1 <= sx, sy, fx, fy <= 10^9`; `0 <= t <= 10^9`.

## Approaches

| file | mechanism |
|---|---|
| `reachable.kara` ★ | the fewest moves to the finish is the larger of the two distances, and spare moves can be spent on the way; only the start itself, at t = 1, cannot be reached, since a move must leave it |
| `reachable_square.kara` | the cells t moves reach make the square of side 2t + 1 around the start, all of it but the start at t = 1; the finish checked against the square's two ranges with `contains` |
| `reachable_plan.kara` | a plan of moves in a struct, diagonal ones for the shorter distance and straight ones for the rest, its length by a method; spare moves are spent by trading one straight move for two diagonal ones or one diagonal for two straight, which fails only for the empty plan with one spare |
| `reachable_layers.kara` | breadth first over the first two moves, each layer of offsets every neighbour of the one before, in a `Set[(i64, i64)]`; past two moves each one widens the square by one, so they are taken off both distances by a closure and the offset left is looked up |
| `reachable_solution.kara` | a Rust solution as LeetCode's Rust users write it: the two distances by `(sx - fx).abs()` on `i32`, the start itself answered first with `return t != 1`, then `dx.max(dy) <= t`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 5 lines: LeetCode's two examples; the start
itself at t = 0, 1 and 2; the far corner of LeetCode's grid with t just
enough and one short; then every start and finish within 1 to 4 with t
from 0 to 4, and 20000 random cases over LeetCode's grid with t within
3 of the distance, as counts and checksums. `reachable.py` mirrors the
★ arm and its output is byte-identical.

```
true false
true false true
true false
1280 small cases: 808 true, checksum 813557027
20000 random cases: 11425 true, checksum 449580720
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: the cells reachable in exactly t moves, found one move
at a time over a `Set[(i64, i64)]` of the infinite grid, and whether
the finish is among them. It draws 2000 random cases within 1 to 8 with
t up to 6, then 50 over LeetCode's grid with t within 3 of the
distance, all before any arm answers; the literal reading is asked only
of the first 2000.

| | property |
|---|---|
| P1 | t up to 6, the answer is the literal reading's |
| P2 | start and finish swapped: the same answer |
| P3 | the grid mirrored, x and y made 10^9 + 1 - x and 10^9 + 1 - y: the same answer |
| P4 | x and y swapped in both cells: the same answer |
| P5 | true at t: true at t + 2 |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases, 932 true: checksum 838454912,
61500 checks over 5 arms: 0 failures` under every lane in Verification,
and a Python reading of the same cases gives the same checksum. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the start reachable at t = 1 | P1 6, P6 6 |
| M2 | ★: the two distances added, as if moves were straight | P1 291, P6 319 |
| M3 | square: the square one short on each side | P1 127, P4 195, P6 131 |
| M4 | square: the start's exception dropped | P1 6, P6 6 |
| M5 | plan: the straight moves left out | P1 589, P6 611 |
| M6 | plan: spare moves spent only in pairs | P1 413, P6 432 |
| M7 | layers: one layer built, not two | P1 648, P5 269, P6 663 |
| M8 | layers: staying put taken as a move | P1 6, P6 6 |
| M9 | layers: the moves past two not taken off | P1 164, P6 170 |
| M10 | solution: the start reachable at any t | P1 6, P6 6 |

## Benchmarks

The bench draws 10^6 random cases on LeetCode's grid, the finish within
3 of the start and t within 2 of the distance, all of them first, then
answers each 20 times by the ★ arm in all five languages. Every
implementation prints `1000000 cases, 20 rounds: 12318640 true,
checksum 151586517`.

BENCHTAB

## Verification

All five arms print the same output as `reachable.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as first written.

LeetCode's Rust template took 3 `karac fix` edits in one run, the
wrapper included: `struct Solution {}` added for the `impl`; `&&`
became `and`, and `Solution::` took `.`. The `i32` parameters, the
`(sx - fx).abs()` on them and the wrapper's narrowing `as i32` casts
were accepted as written.
