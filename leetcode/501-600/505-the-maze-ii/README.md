# 505. The Maze II

There is a ball in a `maze` with empty spaces (represented as `0`) and
walls (represented as `1`). The ball can go through the empty spaces by
rolling up, down, left or right, but it won't stop rolling until
hitting a wall. When the ball stops, it could choose the next
direction.

Given the `m x n` `maze`, the ball's `start` position and the
`destination`, where `start = [start_row, start_col]` and
`destination = [destination_row, destination_col]`, return the
shortest distance for the ball to stop at the destination. If the ball
cannot stop at `destination`, return `-1`.

The distance is the number of empty spaces traveled by the ball from
the start position (excluded) to the destination (included).

You may assume that the borders of the maze are all walls.

```
maze = [[0,0,1,0,0],[0,0,0,0,0],[0,0,0,1,0],[1,1,0,1,1],[0,0,0,0,0]]
start = [0,4], destination = [4,4]  ->  12
start = [0,4], destination = [3,2]  ->  -1

maze = [[0,0,0,0,0],[1,1,0,0,1],[0,0,0,0,0],[0,1,0,0,1],[0,1,0,0,0]]
start = [4,3], destination = [0,1]  ->  -1
```

**Constraints:** `1 <= m, n <= 100`; `maze[i][j]` is `0` or `1`;
`start` and `destination` are empty cells, and different; the maze
holds at least two empty cells.

## Approaches

Every arm is `fn shortest_distance(maze: Vec[Vec[i64]], start:
Vec[i64], destination: Vec[i64]) -> i64`. The ball can only stop
against a wall or the edge, so those cells are the graph, and each roll
is an edge as long as the cells it covers.

| file | mechanism |
|---|---|
| `shortest_distance.kara` ★ | Dijkstra with a smallest-first `PriorityQueue[(i64, i64, i64)]` of (distance, row, column); a cell is settled the first time it leaves the queue and later entries for it are skipped, and the destination's settling is the answer |
| `shortest_distance_relax.kara` | relaxing until nothing improves: the best distance so far for every cell, `i64.MAX` for none, and a `VecDeque` of the cells whose distance has just improved |
| `shortest_distance_scan.kara` | Dijkstra without a queue: each round scans every cell for the nearest one not yet settled, kept as an `Option[(i64, i64)]`, and a round that finds none means the destination cannot be reached. O((mn)^2) |
| `shortest_distance_dfs.kara` | depth-first search: roll every way, recursively, carrying the distance; a cell already reached by a way no longer than this one ends the branch, and the grid of best distances goes down the recursion as `mut ref Vec[Vec[i64]]` |
| `differential.kara` | the four arms on 1,500 random mazes, five properties |

Every arm prints the same 10 lines: the three LeetCode examples, two
cells, a destination the ball rolls past, a column, the far corner of
an open room, a corner walled in, a dead end that forces the long way
round, and for 300 random mazes (1 to 12 by 1 to 12 cells, a wall in
each cell with odds of 1 in 5, 1 in 3 or 1 in 2 in turn, a start and a
destination in two different open cells) how many reached the
destination, the distances in all and a checksum of every answer.
`shortest_distance.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random mazes of 1 to 9 by 1 to 9 cells (a wall in each cell with
odds of 1 in 5, 1 in 3 or 1 in 2 in turn, at least three open cells),
with a start, a destination and a third cell, all different and open.

| | property |
|---|---|
| P1 | the distance is the reference's, which sweeps every cell and direction, again and again, until no distance improves |
| P2 | the distance is -1, or at least the rows and columns between the two cells and of the same parity, since each step moves one cell |
| P3 | the maze transposed gives the same distance |
| P4 | the maze upside down gives the same distance |
| P5 | stopping at the third cell on the way is never shorter: when the ball can stop there and go on, the distance is no more than the two together |

P5 is checked only when the ball can stop at the third cell and get
from it to the destination, so the count of checks depends on the
mazes: it prints `1500 cases, 4 arms, 25060 checks, 0 failures` under
`karac __mir-run`.

## Mutation testing

Ten edits to `differential.kara`, two to each arm and two equivalent
ones, each run under `karac __mir-run`. All eight non-equivalent ones
are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the queue is largest-first (`PriorityQueue.max_first()`) | P1 253, P3 21, P4 135, P5 4 |
| M2 | ★: a roll of one cell is not taken (`steps > 1`) | P1 467 |
| M3 | relax: every roll counts 1, not the cells it covers | P1 350, P2 311 |
| M4 | relax: an improved cell is not queued again | P1 319, P5 36 |
| M5 | scan: a longer distance replaces a shorter one (`>` for `<`) | P1 197, P4 111, P5 8 |
| M6 | scan: the farthest cell is settled first (`>` for `<`) | P1 48, P3 14, P4 27, P5 6 |
| M7 | dfs: any cell reached before ends the branch, however long the way that reached it | P1 247, P3 189, P4 234, P5 3 |
| M8 | dfs: the ball never rolls right | P1 286, P3 279 |
| E1 | dfs: a roll of no cells recurses too (`if true`) | 0 |
| E2 | ★: a settled cell is queued again | 0 |

E1 is equivalent because a roll of no cells recurses into the same cell
with the same distance, and the first test in the recursion ends it. E2
is equivalent because the ★ arm skips a settled cell when it leaves the
queue: the extra entries cost time and change nothing.

M2, M3 and M4 each answer for a different graph, the same one whichever
way the maze is turned, so P3 and P4 pass and only the reference sees
M2: without the one-cell rolls the ball reaches fewer cells, but by
ways that are still right. M3 counts rolls, not cells, so its distances
can come out shorter than the cells between, which P2 sees. M4 never
queues anything but the start, so it reaches only the cells one roll
away; P5 sees it when the third cell is one roll from the start and
the destination one roll from the third cell. M1, M5, M6 and M7 give answers that depend on the
order cells are reached in, which the transposed and the upside-down
maze change. M8 is the one that leaves out a direction: upside down
keeps left and right, so P4 passes, and the transposed maze turns its
rolls right into rolls down, which P3 sees.

## Verification

All four arms print the same output as `shortest_distance.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and run clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints `25060 checks, 0 failures` on both and runs clean under the
third. `karac check` passes on every file, the bench program included.

The frozen legacy backends agree on all four arms: `karac run
--interp`, LLJIT, legacy `karac build` and a `KARAC_AUTO_PAR=1` build
print the same output. Legacy `karac build` warns on each arm that
`first` is "moved here, used again here", where the harness passes the
first maze to two calls that v2 reads as borrows; the output is right
all the same. Neither legacy backend runs the differential, at the
line that turns the maze upside down, `maze.iter().rev().cloned()
.collect()`: `karac run --interp` stops at "method 'cloned' not found
on type 'unknown'", and legacy `karac build` at "`Iterator.rev()` is
not yet supported ... for this chain shape". Legacy is frozen, so
these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 2,000 mazes of 100 by 100
(the problem's most), a wall in each cell with odds of 1 in 4, with a
start and a destination in two different open cells, once. Then it
solves each once. Every implementation prints `2000 mazes of 100 by
100: the destination reached in 495, distance 64162 in all, checksum
525942359`, the Kāra program under `karac __mir-run` included (in
171 s).

Every mirror keeps a smallest-first queue of (distance, row, column)
triples and a fresh grid of best distances for each maze: Rust a
`BinaryHeap` of `Reverse(...)`, Go `container/heap`, Python `heapq`,
and C a binary heap it writes itself. Spot timings on a shared 4-core
container, three runs each (two for Python; `bench.sh` timings need a
quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.89 to 0.93 s |
| Rust (`rustc -O`) | 0.91 to 0.95 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.97 to 1.04 s |
| Go | 2.06 to 2.32 s |
| Python | 15.0 to 15.4 s |
| Kāra (`karac build --mir`) | 1.35 to 1.44 s |

The legacy `karac build` refuses this program: "cannot move out of an
index expression", on `shortest_distance(all[k], starts[k],
destinations[k])`, which v2 reads as borrows. So `bench.sh` builds the
Kāra program with `karac build --mir`, the v2 compiled backend. That
edit is by hand, on top of the `scripts/new-bench.sh` output. The
`--mir` row is timed at kara `486f47f97d`. Under `karac
__mir-llvm-run` the program prints the same line in 3.7 s, compile
included; that JITs the MIR's IR without optimization passes, so it is
not a benchmark.

## Compiler findings

None filed. Every arm, the differential and the bench program run
right on the v2 backends, and `karac check` passes on all of them as
first written.
