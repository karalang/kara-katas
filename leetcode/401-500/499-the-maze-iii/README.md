# 499. The Maze III

There is a ball in a `maze` with empty spaces (represented as `0`) and
walls (represented as `1`). The ball can go through the empty spaces by
rolling up, down, left or right, but it won't stop rolling until
hitting a wall. When the ball stops, it could choose the next
direction. There is also a hole in this maze. The ball will drop into
the hole if it rolls onto the hole.

Given the `m x n` `maze`, the ball's position `ball` and the hole's
position `hole`, where `ball = [ball_row, ball_col]` and
`hole = [hole_row, hole_col]`, return a string `instructions` of all
the instructions that the ball should follow to drop in the hole with
the shortest distance possible. If there are multiple valid
instructions, return the lexicographically minimum one. If the ball
can't drop in the hole, return `"impossible"`.

If there is a way for the ball to drop in the hole, the answer
`instructions` should contain the characters `'u'` (i.e., up), `'d'`
(i.e., down), `'l'` (i.e., left), and `'r'` (i.e., right).

The distance is the number of empty spaces traveled by the ball from
the start position (excluded) to the destination (included).

You may assume that the borders of the maze are all walls.

```
maze = [[0,0,0,0,0],[1,1,0,0,1],[0,0,0,0,0],[0,1,0,0,1],[0,1,0,0,0]]
ball = [4,3], hole = [0,1]  ->  "lul"
ball = [4,3], hole = [3,0]  ->  "impossible"

maze = [[0,0,0,0,0,0,0],[0,0,1,0,0,1,0],[0,0,0,0,1,0,0],[0,0,0,0,0,0,1]]
ball = [0,4], hole = [3,5]  ->  "dldr"
```

**Constraints:** `1 <= m, n <= 100`; `maze[i][j]` is `0` or `1`;
`ball` and `hole` are empty cells, and different.

## Approaches

Every arm is `fn find_shortest_way(maze: Vec[Vec[i64]], ball: Vec[i64],
hole: Vec[i64]) -> String`. The states are the cells the ball can stop
in: against a wall or the edge, or in the hole as it rolls over it.
Each is settled with the least distance and, among equal distances,
the least instructions in alphabetical order. That is sound because a
cell can only be reached again by a longer way: every roll covers at
least one cell, so instructions that extend another to the same cell
are always longer, and a best way is made of best ways.

| file | mechanism |
|---|---|
| `the_maze_iii.kara` ★ | Dijkstra with a min-first `PriorityQueue[(i64, String, i64, i64)]` of (distance, instructions, row, column), which orders the pairs itself; a cell is settled the first time it leaves the queue, and later entries for it are skipped |
| `the_maze_iii_relax.kara` | relaxing until nothing improves: the best pair so far for each cell, as `Option[(i64, String)]`, and a `VecDeque` of cells whose best has changed |
| `the_maze_iii_scan.kara` | Dijkstra without a queue: the best pairs in flat arrays, and each round a scan of every cell for the least unsettled one |
| `the_maze_iii_sorted.kara` | Dijkstra on a `SortedSet` with one entry per cell, removed and reinserted when the cell gets a better pair, and the least taken with `min`; where each roll stops is worked out first for every cell and direction |
| `differential.kara` | the four arms on 1,500 random mazes, five properties |

Every arm prints the same 9 lines: the three LeetCode examples, two
cells, a hole in the middle of a row (the ball drops in as it rolls
over it), a column, a tie between `dr` and `rd` in an open room, a
corner walled in, and for 300 random mazes (1 to 12 by 1 to 12 cells,
a wall in each cell with odds of 1 in 5, 1 in 3 or 1 in 2 in turn, a
ball and a hole in two different open cells) how many reached the
hole, how many instructions those took and a checksum of every answer.
`the_maze_iii.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random mazes of 1 to 9 by 1 to 9 cells (a wall in each cell with
odds of 1 in 5, 1 in 3 or 1 in 2 in turn, at least three open cells),
with a ball and a hole in two different open cells. The reference
works with distances alone and then picks letters: it finds the least
distance from every cell to the hole by relaxing until nothing
changes, then from the ball takes the first letter in alphabetical
order whose roll keeps to a least distance, until it reaches the hole.

| | property |
|---|---|
| P1 | the instructions are the reference's |
| P2 | the instructions roll the ball into the hole: every roll moves it, and it drops in at the end of the last one and not before |
| P3 | the maze transposed gives a way of the same length (or none) |
| P4 | the maze upside down gives a way of the same length (or none) |
| P5 | a wall added in a cell the way never rolls over makes the way no longer, and never impossible |

P5 is checked only when there is a way and it misses the new wall, so
the count of checks depends on the mazes: it prints `1500 cases, 4
arms, 27088 checks, 0 failures` under `karac __mir-run`.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the ball rolls on over the hole | P1 387, P2 17 |
| M2 | ★: left and right swap letters | P1 673, P2 672, P3 491, P5 1 |
| M3 | relax: a tie keeps the instructions later in alphabetical order | P1 96 |
| M4 | relax: only a shorter distance counts as better | P1 29 |
| M5 | scan: a tie keeps the instructions later in alphabetical order | P1 96 |
| M6 | scan: an equal distance always replaces | P1 63 |
| M7 | sorted: an equal distance never replaces | P1 33 |
| M8 | sorted: a roll's length counts rows only | P1 673, P3 486 |

M3 to M7 all get the tie between equal distances wrong and nothing
else, so the way is as long as it should be, still rolls into the
hole, and passes P2 to P5; only the reference sees them. M3 and M5 are
the same mistake in two arms and fail the same 96 cases. M1 mostly
finds a different way to a hole it can now only stop in against a
wall; in 17 cases its instructions roll over the hole before their
end, which P2 catches. M8 still gives a way that works, so P2 passes,
but a longer one; the transposed maze, whose rows are the columns,
gives a different length and P3 sees that.

Three more edits are equivalent, and show where the arms are robust.
Trying the moves in another order changes nothing in the ★ arm, since
the queue orders the instructions, not the order they were pushed in.
In the scan arm, settling the cell with the later instructions first
among cells at the least distance changes nothing, since neither can
improve the other: every roll adds distance. And in the sorted arm,
leaving a replaced entry in the set changes nothing, since the better
entry for the same cell always comes out first and the stale one only
reaches cells already settled or holding better pairs. Each gives 0
failures.

## Verification

All four arms print the same output as `the_maze_iii.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
`karac check` passes on every file, the bench program included. The
differential prints `27088 checks, 0 failures` on both. The four arms
and the differential also run clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak.

The frozen legacy backends agree only on the scan arm, where `karac
run --interp`, LLJIT, legacy `karac build` and a `KARAC_AUTO_PAR=1`
build all print the same output. On the others:

- ★ arm: `karac run --interp` prints the same output. LLJIT and the
  legacy-built binary both abort with "free(): double free detected in
  tcache 2".
- relax arm: `karac run --interp` prints the same output. LLJIT and
  legacy `karac build` fail in codegen on `best[row][col].clone()`:
  "chained indexed receivers (`a[i][j].clone(...)`) are deferred to
  v1.x".
- sorted arm: all three refuse `*d` at type checking ("unary '*'
  requires 'ref T' ... found 'i64'"), reading what `Map.get` returns as
  a value where v2 reads it as a borrow. The differential carries a
  copy of that arm and is refused the same way.

Legacy is frozen, so these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 1,000 mazes of 100 by 100
(the problem's most), a wall in each cell with odds of 1 in 4, with a
ball and a hole in two different open cells, once. Then it solves each
once. Every implementation prints `1000 mazes of 100 by 100: the hole
reached in 718, 23118 instructions in all, checksum 486756249`, the
Kāra program under `karac __mir-run` included (in 87 s).

The mirrors keep the ★ arm's queue of (distance, instructions, row,
column) pairs, each entry owning its own copy of its instructions:
Rust a `BinaryHeap` of `Reverse(...)` with `String`s, Go
`container/heap`, Python `heapq`, and C a binary heap it writes
itself, comparing with `strcmp`, of `malloc`ed strings. Spot timings
on a shared 4-core container, three runs each (two for Python;
`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.40 to 0.49 s |
| Rust (`rustc -O`) | 0.62 to 0.67 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.66 to 0.71 s |
| Go | 1.11 to 1.26 s |
| Python | 6.9 to 7.0 s |
| Kāra (`karac build --mir`) | 0.75 to 0.80 s |

The legacy `karac build` refuses this program: "cannot move out of an
index expression", on `find_shortest_way(all[k], balls[k], holes[k])`,
which v2 reads as borrows. So `bench.sh` builds the Kāra program with
`karac build --mir`, the v2 compiled backend. That edit is by hand, on
top of the `scripts/new-bench.sh` output. The `--mir` row is timed at
kara `d9a7136c58`. Under `karac __mir-llvm-run` the program prints the
same line in 3.2 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

## Compiler findings

None filed. Every arm, the differential and the bench program run
right on the v2 backends. `karac check` refused two lines of the first
draft of the sorted arm, and `karac fix` repaired both:
`let (_, _, name) = moves[k]` cannot move the letter out of the `Vec`
(it became `moves[k].2.clone()`), and `next.1 >= *p` dereferences a
`String` borrow that compares as it is (it became `next.1 >= p`). The
first draft also called `SortedSet.pop_first`, which Kāra's `SortedSet`
does not have; the arm takes `min()`, clones it and removes it, as
`docs/library/collections.md` lists.
