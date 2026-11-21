# 1730. Shortest Path to Get Food

You are starving and you want to eat food as quickly as possible. You
want to find the shortest path to arrive at any food cell.

You are given an `m x n` character matrix, `grid`, of these different
types of cells:

- `'*'` is your location. There is **exactly one** `'*'` cell.
- `'#'` is a food cell. There may be **multiple** food cells.
- `'O'` is free space, and you can travel through these cells.
- `'X'` is an obstacle, and you cannot travel through these cells.

You can travel to any adjacent cell north, east, south, or west of your
current location if there is not an obstacle.

Return *the **length** of the shortest path for you to reach **any**
food cell*. If there is no path for you to reach food, return `-1`.

```
grid = [["X","X","X","X","X","X"],
        ["X","*","O","O","O","X"],
        ["X","O","O","#","O","X"],
        ["X","X","X","X","X","X"]]                    ->  3
grid = [["X","X","X","X","X"],
        ["X","*","X","O","X"],
        ["X","O","X","#","X"],
        ["X","X","X","X","X"]]                        ->  -1
grid = [["X","X","X","X","X","X","X","X"],
        ["X","*","O","X","O","#","O","X"],
        ["X","O","O","X","O","O","X","X"],
        ["X","O","O","O","O","#","O","X"],
        ["X","X","X","X","X","X","X","X"]]            ->  6
```

**Constraints:** `m == grid.length`; `n == grid[i].length`;
`1 <= m, n <= 200`; `grid[row][col]` is `'*'`, `'X'`, `'O'`, or `'#'`;
the `grid` contains **exactly one** `'*'`.

LeetCode marks the problem premium, so there is no Rust template to carry
over: all four arms are Kāra written for it.

## Approaches

| file | mechanism |
|---|---|
| `food.kara` ★ | a breadth-first search from you: every step costs the same, so cells come off a `VecDeque` in order of distance and the first food off it is the nearest; a cell's distance, set when first reached, marks it seen. O(m n) |
| `food_levels.kara` | no queue: the cells at distance d are a list, the next list every unseen open neighbour of them, the cells numbered `r * cols + c`; the first level holding food gives the answer, an empty level -1. O(m n) |
| `food_reverse.kara` | the search run backwards from every food at once, all at distance 0; the distance at which it first reaches you is the shortest way to any of them. O(m n) |
| `food_dijkstra.kara` | Dijkstra's search, every step weighed 1: a `PriorityQueue` of (distance, cell) settles the nearest cell first, a shorter way pushing a cell again. O(m n log(m n)) |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 8 lines: LeetCode's three examples, you alone
with no food, and a long way round; then how often food was reached,
the steps summed and a checksum for 3000 random grids of up to 5 by 5,
300 of up to 50 by 50 and 5 of up to 200 by 200, each cell an obstacle
with a chance of 1 in 4, food 1 in 10, free otherwise, and you on one
cell. `food.py` mirrors the ★ arm and its output is byte-identical.

```
3
-1
6
-1
10
3000 grids of up to 5 by 5: food reached 1334 times, steps sum to 2667, checksum 832992328
300 grids of up to 50 by 50: food reached 282 times, steps sum to 718, checksum 29865440
5 grids of up to 200 by 200: food reached 5 times, steps sum to 11, checksum 963916245
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: the cells you can stand on after k steps, each step to an
adjacent cell that is not an obstacle, grown one step at a time over the
whole grid, with no queue; the first k at which a food cell is among
them, or -1 once they stop growing. It checks 3000 random grids of 1 to
5 rows and columns, each cell an obstacle with a chance of 3 in 10, food
1 in 10, free otherwise, and you on one cell. Every case is drawn before
any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the grid mirrored left to right gives the same answer |
| P3 | the grid transposed, rows made columns, gives the same answer |
| P4 | a border of obstacles put round the grid gives the same answer |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 953670894, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement, the same cells within k steps as a `set`,
gives the same checksum. On a failure it prints the first ten and then
the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. M1, M2, M4, M7 and M8 each get every
answer wrong where food can be reached, and nothing else, so they fail
the very same checks: 1279 of the 3000 grids reach food. The properties
catch the mutants that break a symmetry: M3, a direction lost, fails P2
and P3, and M5 and M6, an edge of the grid that cannot be entered, fail
P4, whose border moves that edge.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each step counted twice | P1 1279, P5 1279 |
| M2 | ★: only free cells entered, so food never is | P1 1279, P5 1279 |
| M3 | ★: east given as west a second time | P1 432, P2 827, P3 588, P5 432 |
| M4 | levels: each level counted as two steps | P1 1279, P5 1279 |
| M5 | levels: the last column never entered from its left | P1 207, P2 395, P3 348, P4 207, P5 207 |
| M6 | reverse: the first row never entered | P1 464, P3 605, P4 464, P5 464 |
| M7 | reverse: the foods start at distance 1 | P1 1279, P5 1279 |
| M8 | dijkstra: a neighbour pushed at the distance of the cell it came from | P1 1279, P5 1279 |
| M9 | dijkstra: the farthest cell taken first | P1 213, P2 52, P3 191, P5 213 |
| M10 | dijkstra: obstacles walked through | P1 216, P5 216 |

## Benchmarks

The bench draws 10 random 200 by 200 grids, LeetCode's largest, each
cell an obstacle with a chance of 1 in 4 and food 1 in 20000, so that a
grid holds two foods on average and the search covers much of it, all of
them first, then answers each 200 times by the ★ arm in all five
languages. Every implementation prints `10 grids of 200 by 200, 200
rounds: answers sum to 248000, checksum 512956020`. Kāra, Rust and
Python keep a deque of (row, column) pairs, Go a slice of them it
appends to, and C an array of cell numbers. The C build also runs clean
under gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `21cdf88b69` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.558 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.615 s |
| Kāra (`karac build`) | 0.634 s |
| Rust (`rustc -O`) | 0.643 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.657 s |
| Go | 1.677 s |
| Python | 15 s |

The sequential Kāra build is level with Rust and 6% faster than Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md). C
is the fastest here at 0.558 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.621 s and 0.625 s on one
run).

## Verification

All four arms print the same output as `food.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `21cdf88b69`.

## Writing it

All four arms and the differential checked clean as first written. The
search's moves are a list of `(dr, dc)` pairs added to an `i64` row and
column, which go below zero at the edge and are tested before they
index; the levels arm numbers its cells instead and tests the edge
before stepping. `PriorityQueue.new()` gives the smallest first, so the
Dijkstra arm pushes `(distance, cell)` with no `Reverse`.

`arm_name` in the differential indexes a list of string literals for a
`Str`, as #1662's does (B-2026-11-19-131).
