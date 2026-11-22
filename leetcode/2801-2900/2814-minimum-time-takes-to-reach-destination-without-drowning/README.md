# 2814. Minimum Time Takes to Reach Destination Without Drowning

You are given an `n * m` **0-indexed** grid of string `land`. Right
now, you are standing at the cell that contains `"S"`, and you want to
get to the cell containing `"D"`. There are three other types of cells
in this land:

- `"."`: These cells are empty.
- `"X"`: These cells are stone.
- `"*"`: These cells are flooded.

At each second, you can move to a cell that shares a side with your
current cell (if it exists). Also, at each second, every **empty cell**
that shares a side with a flooded cell becomes flooded as well.

There are two problems ahead of your journey:

- You can't step on stone cells.
- You can't step on flooded cells since you will drown (also, you can't
  step on a cell that will be flooded at the same time as you step on
  it).

Return *the **minimum** time it takes you to reach the destination in
seconds, or* `-1` *if it is impossible.*

**Note** that the destination will never be flooded.

```
land = [["D",".","*"],[".",".","."],[".","S","."]]                           ->  3
land = [["D","X","*"],[".",".","."],[".",".","S"]]                           ->  -1
land = [["D",".",".",".","*","."],[".","X",".","X",".","."],[".",".",".",".","S","."]]  ->  6
```

**Constraints:** `2 <= n, m <= 100`; `land` consists only of `"S"`,
`"D"`, `"."`, `"*"` and `"X"`; **exactly** one of the cells is `"S"`,
and **exactly** one is `"D"`.

This is a premium problem. Every arm lets the flood onto the start's
cell, read as an empty cell once the walker has left it; the Rust
solution's flood skips only stone and the destination, which agrees,
and so do the literal reading and the mirror.

## Approaches

| file | mechanism |
|---|---|
| `drowning.kara` ★ | the second each cell floods by one breadth-first search from every flooded cell at once over a `VecDeque`, then a breadth-first search from the start onto cells that are not stone and still dry the second after the step |
| `drowning_together.kara` | the flood and the walk a second at a time: two `Vec` frontiers, the water's grown first, then the walker's onto neighbours neither stone, nor wet, nor seen |
| `drowning_relax.kara` | by relaxation: the flood's seconds lowered over every cell pass after pass until nothing changes, then the walker's the same way, a step landing only before the water does; arriving sooner is never worse, since the water only grows |
| `drowning_heap.kara` | on flat cells: the land read once into a `Vec[char]` indexed by r * m + c, a closure for the neighbours, the flood by a breadth-first search over the indices and the walk by Dijkstra's search on a `PriorityQueue` |
| `drowning_solution.kara` | a Rust solution as LeetCode's Rust users write it, a `match` on `as_str()`, `usize` cells with `i32` bounds checks and `continue`s, `i32::MAX` for never, one `VecDeque` for both searches, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's three examples; 100 by
100 of open land, corner to corner; the same with a flood two cells
from the start; 3000 random lands of 2 to 5 by 2 to 5, a cell in five
stone and one in eight flooded; and 50 of up to 60 by 60 with one in
500 flooded, the last two with how many were reached and a checksum.
`drowning.py` mirrors the ★ arm and its output is byte-identical.

```
3
-1
6
198
-1
3000 small lands: 2030 reached, checksum 350544548
50 large lands: 31 reached, checksum 691483254
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: a second at a time, every empty cell beside a flooded one
floods, on a copy of the land, and the walker, wherever it could be, a
`Set` of cells, steps to each neighbour that is not stone and not
flooded after that second's spread, with no memory of where it has
been, until it stands on the destination or n * m seconds have gone; no
table of flood times. It draws 2000 random lands of 2 to 5 by 2 to 5
with a cell in eight flooded, then 50 of up to 40 by 40 with one in
500, all before any arm answers; the literal reading is asked only of
the first 2000.

| | property |
|---|---|
| P1 | up to 5 by 5, the answer is the literal reading's |
| P2 | -1, or from the start's Manhattan distance to the destination up to n * m - 1 |
| P3 | the land transposed: the same answer |
| P4 | the land mirrored left to right: the same answer |
| P5 | every flood dried: reached when it was, and no later |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 228502108, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. Eight are killed, each the same
way under both backends. M2 and M6 survive and are equivalent: water
that reaches the start reaches every cell beyond it later than the
walker can, along the water's own path, so keeping it off the start
changes no check the walker makes; and the destination never floods, so
its time stays at `i64.MAX` and the comparison alone already lets the
walker in. M4's walker list grows without bound and both backends end
with no output.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a step allowed onto a cell flooding as it lands | P1 142, P6 143 |
| M2 | ★: the water kept off the start | survives: equivalent (above) |
| M3 | together: the clock started a second late | P1 1332, P6 1362 |
| M4 | together: the walker allowed back onto cells seen | killed under both: no output, the walker list growing without bound |
| M5 | relax: the flood relaxed in one pass only | P1 49, P4 69, P6 57 |
| M6 | relax: the destination counted as flooding like any cell | survives: equivalent (above) |
| M7 | heap: the queue hands out the latest cell first | P1 39, P3 56, P4 15, P5 77, P6 59 |
| M8 | heap: a cell's right neighbour on the next row's edge too | P1 166, P2 118, P3 317, P4 328, P6 171 |
| M9 | solution: stone let in by the walk | P1 260, P6 275 |
| M10 | solution: the water let onto the destination | P1 350, P6 350 |

## Benchmarks

The bench draws 200 lands of 100 by 100, LeetCode's largest, a cell in
five stone and one in 5000 flooded, all of them first, then answers
each 5 times by the ★ arm in all five languages. Rust and Go keep the
land as strings, as Kāra does; C keeps one `char` a cell. Every
implementation prints `200 lands of 100 by 100, 5 rounds: seconds sum
to 21015, checksum 16937853`.

BENCHTAB

## Verification

All five arms print the same output as `drowning.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The heap arm first wrote its neighbour closure as Rust does, `|cell:
i64| -> Vec[i64] { .. }`; a Kāra closure does not declare its return
type, and `karac fix` dropped the `-> Vec[i64]`. The other own arms and
the harness checked clean as first written.

LeetCode's Rust template took 30 `karac fix` edits in one run, the
wrapper included: `struct Solution {}` added for the `use` line;
`Vec<..>` became `Vec[..]`; `vec![vec![i32::MAX; m]; n]` and `vec![vec![-1;
m]; n]` became `Vec.filled` and `i32::MAX` `i32.MAX`; `VecDeque::new`
and `Solution::` took `.`; `||` became `or`; the `as usize` casts went,
Kāra indexing by `i64`, and the `let (ni, nj) = (ni, nj);` they left
went too, by the `self_rebinding` lint's fix (kara 0d28296389,
B-2026-11-21-206); and the
wrapper's `land.clone()` and `as i64` went, a borrowed `land` passing
to a borrowed parameter and an `i32` widening implicitly. The `match`
on `land[i][j].as_str()` with `"*" => { .. }` and `"S" => start = (i,
j)` arms is Kāra as written.
