# 490. The Maze

There is a ball in a `maze` with empty spaces (`0`) and walls (`1`). The
ball can go through the empty spaces by rolling up, down, left or right,
but it won't stop rolling until hitting a wall. When the ball stops, it
could choose the next direction.

Given the `m × n` maze, the ball's `start` position and the
`destination`, where `start = [row, col]` and `destination = [row, col]`,
return `true` if the ball can stop at the destination, otherwise return
`false`.

You may assume that the borders of the maze are all walls.

```
maze = [[0,0,1,0,0],
        [0,0,0,0,0],
        [0,0,0,1,0],
        [1,1,0,1,1],
        [0,0,0,0,0]],  start = [0,4], destination = [4,4]  ->  true
                       start = [0,4], destination = [3,2]  ->  false
```

**Constraints:** `1 <= m, n <= 100`; `maze[i][j]` is `0` or `1`; `start`
and `destination` are empty cells and are not the same cell.

## Approaches

Every arm is `fn has_path(maze: Vec[Vec[i64]], start: Vec[i64],
destination: Vec[i64]) -> bool`. The ball only ever stops against a wall
or the edge, so the search runs over stopping cells, not over all cells.

| file | mechanism |
|---|---|
| `the_maze.kara` ★ | breadth first over stopping cells: from each, roll four ways until the next cell is a wall or off the board; a `VecDeque` of the cells to roll from and a grid of the cells already queued |
| `the_maze_dfs.kara` | depth first, recursively, with a `Set[(i64, i64)]` of the cells reached; stops as soon as the destination is reached |
| `the_maze_table.kara` | the stops worked out first: one sweep along each row and column in each direction fills four tables of where a roll from each cell stops, then a breadth-first search only looks them up |
| `the_maze_backward.kara` | backwards from the destination: for each direction the destination is blocked in, every open cell behind it back to a wall rolls into it; mark those, then the cells that roll into each marked cell, and so on; the answer is whether the start is marked |
| `differential.kara` | the four arms on 1,500 random mazes, five properties |

Every arm prints the same 9 lines: the two LeetCode examples, a third
maze, two cells in a row, the middle of a row (never a stop), a column,
an open room from inside to a corner and from a corner to the middle,
and for 300 random mazes (1 to 12 by 1 to 12 cells, a wall in each cell
with odds of 1 in 5, 1 in 3 or 1 in 2 in turn) how many destinations
were reached and a checksum. `the_maze.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random mazes of 1 to 8 by 1 to 8 cells, at the same three odds,
each with three different open cells: a start, a destination and a
further destination. The reference marks every stopping cell the ball
can reach, pass after pass, until a pass marks nothing new.

| | property |
|---|---|
| P1 | the answer is whether the reference marks the destination |
| P2 | the maze transposed (start and destination too) gives the same answer |
| P3 | the maze upside down gives the same answer |
| P4 | start to destination and destination to the further destination make start to the further destination |
| P5 | a destination the ball reaches has a wall or the edge beside it |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, in 2.2 s, and a count for each property when
anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the destination's column is checked against its row | P1 470, P2 477, P3 437, P4 5, P5 13 |
| M2 | ★: the ball never rolls right | P1 293, P2 291 |
| M3 | dfs: any cell in the destination's row counts | P1 381, P2 577, P4 18, P5 58 |
| M4 | dfs: a roll right stops one short of the edge | P1 315, P2 453, P5 15 |
| M5 | table: a roll left stops on the wall, not after it | P1 224, P2 283, P3 158 |
| M6 | table: the roll down is left out | P1 270, P2 291, P3 374 |
| M7 | backward: a cell counts as a stop even when open ahead | P1 474, P5 89 |
| M8 | backward: the walk behind goes forward in rows | P1 221, P2 286 |

P2 and P3 compare an arm with itself, so they only see a mutant that
treats a direction differently from its mirror image. Transposing swaps
rows with columns, and every mutant but M7 treats the two differently.
Turning upside down swaps up with down and leaves left and right alone,
so it misses M2 and M4 (only right is broken), M3 (the row check is the
same either way up) and M8 (up and down are broken alike). M7 breaks
every direction alike, and only P1 and P5 see it.

## Verification

All four arms print the same output as `the_maze.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
`karac check` passes on every file, the bench program included. The
differential prints `30000 checks, 0 failures` on both. The four arms
and the differential also run clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak.

The frozen legacy backends agree on all four arms and the differential:
`karac run --interp`, LLJIT, legacy `karac build` and a
`KARAC_AUTO_PAR=1` build print the same output. Legacy `karac build`
warns that a value (`first`, or the differential's `maze`) is "moved
here, used again here", where a function lends it twice and legacy
reads the first as a move; the output is right all the same. The bench
program does not build on legacy (see Benchmarks). Legacy is frozen, so
this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 60 mazes of 300 by 300
cells (a wall in each cell with odds of 1 in 6, and a start and a
destination on open cells) once, then solves each once. Every
implementation prints `60 mazes of 300 by 300: the destination reached
in 16, checksum 855775730`, the Kāra program under `karac __mir-run`
included (in 21 s).

The Rust mirror uses a `VecDeque` like the ★ arm; C and Go keep the
queue in an array with a moving head, since every cell joins it at most
once; Python uses `collections.deque`. Spot timings on a shared 4-core
container, three runs each (two for Python; `bench.sh` timings need a
quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.09 to 0.10 s |
| Rust (`rustc -O`) | 0.13 to 0.14 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.13 to 0.16 s |
| Go | 0.22 s |
| Python | 3.3 to 3.4 s |
| Kāra (`karac build --mir`) | 0.21 to 0.22 s |

The legacy `karac build` refuses this program: "cannot move out of an
index expression", on `has_path(mazes[k], starts[k], destinations[k])`,
which v2 reads as a borrow. So `bench.sh` builds the Kāra program with
`karac build --mir`, the v2 compiled backend. That edit is by hand, on
top of the `scripts/new-bench.sh` output. The `--mir` row is timed at
kara `d9a7136c58`. Under `karac __mir-llvm-run` the program prints the
same line in 1.6 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

## Compiler findings

None. Every arm, the differential and the bench program ran first time
on the v2 backends.
