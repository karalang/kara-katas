# 2850. Minimum Moves to Spread Stones Over Grid

You are given a **0-indexed** 2D integer matrix `grid` of size `3 * 3`,
representing the number of stones in each cell. The grid contains
exactly `9` stones, and there can be **multiple** stones in a single
cell.

In one move, you can move a single stone from its current cell to any
other cell if the two cells share a side.

Return *the **minimum number of moves** required to place one stone in
each cell*.

```
grid = [[1,1,0],[1,1,1],[1,2,1]]  ->  3
grid = [[1,3,0],[1,0,0],[1,0,3]]  ->  4
```

**Constraints:** `grid.length == grid[i].length == 3`; `0 <=
grid[i][j] <= 9`; the sum of `grid` is `9`.

## Approaches

| file | mechanism |
|---|---|
| `moves.kara` ★ | each stone past the first in a cell must go to some empty cell, at the cells' distance on the grid, rows and columns added; the empty cells are given to the spare stones in every way by backtracking over a `mut ref Vec[bool]`, and the cheapest kept |
| `moves_permute.kara` | the empty cells in an order of their indices, given to the spare stones one to one, the order taken through every permutation by the next-permutation step (the last rise, the swap past it, the tail reversed with `order[i..].reverse()`) |
| `moves_mask.kara` | dynamic programming over subsets: best[mask] the cheapest way to give the empty cells in mask to the first `count_ones()` spare stones, each mask extended by one more cell |
| `moves_flow.kara` | a min-cost flow: the source feeds each cell its spare stones, every such cell reaches every empty one at their distance, each empty cell drains one to the sink; shortest augmenting paths by Bellman-Ford over a network struct of paired edges |
| `moves_solution.kara` | a Rust solution as LeetCode's Rust users write it: the spare stones and empty cells as `Vec<(i32, i32)>` from `i as i32`, and a nested `fn dfs` over `&Vec` and `&mut Vec<bool>` from `i32::MAX`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 3 lines: LeetCode's two examples; a grid
already spread, and all nine stones in a corner and in the middle; then
every grid of nine stones, all 24310, as a total, the most and a
checksum. `moves.py` mirrors the ★ arm and its output is
byte-identical.

```
3 4
0 18 12
24310 grids: 163168 moves in all, at most 18, checksum 593939041
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: one stone moved to a cell sharing a side at a time, a
breadth-first search over every grid of nine stones out from the one
spread, each grid kept as its nine counts in base ten in a `Map[i64,
i64]` to its fewest moves; since a move can be made back, that is the
fewest to spread it. It draws 2000 random grids, each stone dropped
into one of the nine cells, then 50 with every stone dropped into one
of at most three, all before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the grid transposed: the same answer |
| P3 | the grid mirrored left to right: the same answer |
| P4 | the grid turned a quarter: the same answer |
| P5 | at least the count of empty cells, at most four times it |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases, 24310 grids searched: checksum
394512210, 61500 checks over 5 arms: 0 failures` under every lane in
Verification, and a Python reading of the same cases gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a stone's column distance left out | P1 1966, P2 1630, P4 1630, P5 1321, P6 1966 |
| M2 | ★: an empty cell never freed for the next try | P1 509, P2 711, P3 532, P4 771, P6 509 |
| M3 | ★: every stone in a cell counted spare | killed under both: runtime error: integer overflow |
| M4 | permute: the first permutation only | P1 509, P2 711, P3 532, P4 771, P6 509 |
| M5 | permute: the tail left unreversed | P1 144, P2 283, P3 209, P4 220, P6 144 |
| M6 | mask: every cell costed from the first stone | P1 1513, P2 424, P3 401, P4 821, P6 1513 |
| M7 | mask: the last stone's cell never added | P1 1922, P2 667, P3 849, P4 1097, P5 503, P6 1922 |
| M8 | flow: one spare stone sent from each cell | P1 1139, P5 755, P6 1139 |
| M9 | flow: the edge back never given room | P1 218, P2 108, P3 274, P4 272, P6 218 |
| M10 | solution: a stone's row distance left out | P1 1953, P2 1630, P4 1630, P5 1291, P6 1953 |

## Benchmarks

The bench makes every grid of nine stones, all 24310, first, then
answers each 5 times by the ★ arm in all five languages. C holds the
spare stones and empty cells in fixed arrays of 9 where the others push
to vectors. Every implementation prints `24310 grids, 5 rounds: 815840
moves, checksum 956284654`.

BENCHTAB

## Verification

All five arms print the same output as `moves.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as first written. The harness passed
each grid as `minimum_moves(grid.clone())`, and `karac check` reported
`redundant_clone`, "`grid.clone()` copies `grid` for a parameter that
only borrows it"; `karac fix` passed `grid`.

LeetCode's Rust template took 34 `karac fix` edits in one run, the
wrapper included: `struct Solution {}` added for the `impl`; the nested
`fn dfs`, E0001 "a `fn` cannot be declared inside a function body",
moved above the `impl`, its `usize` index becoming `i64`, `&Vec<..>`
`ref Vec[..]` and `&mut Vec<bool>` `mut ref Vec[bool]`; `Vec<..>`
became `Vec[..]`, `vec![]` `Vec.new()` and `vec![false; to.len()]`
`Vec.filled(to.len(), false)`; `i32::MAX` became `i32.MAX` and `!` `not`;
the call `dfs(0, &from, &to, &mut used)` became `dfs(0, from, to, mut
used)`; `|&x|` lost its `&`, the wrapper's `as i64` went, an `i32`
widening, and `Solution::` took `.`. The `(i as i32, j as i32)` pushes
were accepted as written.
