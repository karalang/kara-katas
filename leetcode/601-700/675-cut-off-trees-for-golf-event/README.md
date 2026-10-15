# 675. Cut Off Trees for Golf Event

A forest is a grid: 0 is a wall, 1 open ground, and a number above 1 a
tree of that height, which can be walked over. Starting at (0, 0) and
moving a step at a time up, down, left or right, cut every tree in order
of height, shortest first; the heights are distinct. Return the fewest
steps that takes, or -1 if some tree cannot be reached.

```
[[1,2,3],[0,0,4],[7,6,5]]  ->  6
[[1,2,3],[0,0,0],[7,6,5]]  -> -1   (the bottom row is cut off)
[[2,3,4],[0,0,5],[8,7,6]]  ->  6   (the first tree is at the start)
```

**Constraints:** 1 <= rows, columns <= 50; 0 <= `forest[i][j]` <=
10^9; the heights of the trees are distinct.

## Approaches

Every arm is `fn cut_off_tree(forest: Vec[Vec[i64]]) -> i64`, and every
arm takes the same route, since the order of the trees fixes it: from
(0, 0) to the shortest tree, then to the next. Trees stay walkable once
cut, so the answer is a sum of shortest walks, and the arms differ in
how each walk is found.

| file | mechanism |
|---|---|
| `cut_off_trees_for_golf_event.kara` ★ | breadth-first search, a layer of the queue at a time; O(trees * rows * cols) |
| `cut_off_trees_for_golf_event_astar.kara` | A* search with a `PriorityQueue` ordered by steps taken plus the Manhattan distance left; O(trees * rows * cols * log(rows * cols)) |
| `cut_off_trees_for_golf_event_bidir.kara` | breadth-first search from both ends, growing the smaller frontier, until the two meet; O(trees * rows * cols) |
| `cut_off_trees_for_golf_event_detours.kara` | Hadlock's search for the fewest steps away from the target, the walk being the Manhattan distance plus two for each; O(trees * rows * cols) |
| `differential.kara` | the four arms against distances found by relaxation, five properties |

Every arm prints the same 14 lines: the three LeetCode examples and
seven corners, among them one cell, empty and a tree, a row, a column
cut by a wall, a wall to walk round and cells walled apart; a 50 by
50 serpentine whose two tallest trees sit at the ends of its 1,225-step
path; two random 50 by 50 forests, one without walls and one with them;
and a checksum of 200 random forests up to 20 by 20, walls on
0, 10, 25 or 40 in 100 cells, with how many can be cleared.
`cut_off_trees_for_golf_event.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which finds each walk's length by relaxing every open cell against its
neighbours until nothing changes, with no queue and no search order.
That is affordable up to 6 by 6, and 200 forests that small are checked
against it. A further 400 random forests up to 15 by 15 are held to the
other four properties; across all 600, walls cover 0, 15, 30 or 45 in
100 cells and trees 20, 40 or 60 in 100.

| | property |
|---|---|
| P1 | the answer is the definition's (small forests only) |
| P2 | -1, or at least the route's Manhattan distances added up |
| P3 | -1, or of the same parity as that sum, since every step changes `r + c` by one |
| P4 | the forest transposed has the same answer |
| P5 | knocking down one wall never lengthens a possible route or makes it impossible |

It prints `600 forests (200 against the definition, 387 reachable),
4 arms, 10400 checks, 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and runs clean under `karac __mir-llvm-asan`.

## Mutation testing

Fourteen edits to the differential, two to each arm that change its
answers and six that do not, each run under `karac __mir-run`. All eight
that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the tallest tree cut first | P1 107, P2 103, P3 187 |
| M2 | ★: walls walked through | P1 70 |
| M3 | ★: the tree of height 2 left standing | P1 77, P2 181, P3 12 |
| M4 | astar: the distance to go counted twice | P4 30, P5 2 |
| M5 | astar: the last row never entered | P1 98, P4 81 |
| M6 | bidir: the meeting step not counted | P1 123, P2 320, P3 167 |
| M7 | bidir: a side meeting its own cells | P1 127, P2 272, P3 164, P5 2 |
| M8 | detours: a detour counted once, not twice | P1 22, P3 59 |
| E1 | bidir: always the start's side grown | 0 |
| E2 | astar: stale entries taken up again | 0 |
| E3 | detours: a sideways step counted free | 0 |
| E4 | detours: a finished cell taken up again | 0 |
| E5 | astar: a cell's first distance kept | 0 |
| E6 | astar: the distance to the start used as the guess | 0 |

P1 kills seven of the eight; M4 it misses. M4 counts the distance left
twice, which can make A* settle on a longer walk, but on forests of 6 by
6 it never does; P4 sees it, since the same forest transposed is
explored in another order and can find the shorter walk, and P5 twice.
M2, walls walked through, breaks only P1: walking through walls keeps
every other property. The six survivors cannot change an answer. Growing
only the start's side is a plain breadth-first search that stops at the
target. A* taking up a stale entry finds nothing shorter from it. Every
step on a grid changes the Manhattan distance by one, so no step is
sideways. A finished cell taken up again pushes only unfinished
neighbours. The last two are A* facts: keeping a cell's first distance
is safe because the queue breaks ties in its order by the steps taken,
and a later neighbour can only offer a shorter distance when it ties the
first in that order with fewer steps, so it comes out first; and the
Manhattan distance to the start, as a guess, turns A* into Dijkstra's
search over steps reweighted to 0 or 2, which finds the same shortest
walks.

## Verification

Every arm prints the same output as `cut_off_trees_for_golf_event.py`
under `karac __mir-run` (the v2 MIR interpreter) and `karac
__mir-llvm-run`, and runs clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak. The differential prints its line under all three. `karac check`
passes all four arms, the differential and the bench program. All with
the compiler at kara `8d40e1a762` for the debug build and `85dccd703c`
for the release build that runs `check` and `__mir-run`, with runtime
archives newer than the last `runtime/src` change.

The frozen legacy backends print the same output for every arm under the
JIT and `karac build`, with and without `KARAC_AUTO_PAR=1`; `karac
build` warns that `forest` is moved into `show` and used again, and
builds anyway. The legacy interpreter prints the same output for the
detours arm, and runs out of the 60 s limit partway through the other
three, after the same lines as far as it gets. The differential prints
its line under the legacy `karac build`; the legacy interpreter does not
finish it within 60 s.

## Benchmarks

The bench program uses the ★ arm. It cuts the trees of 40 random 50 by
50 forests, the problem's largest, from the same generator in every
language, walls on 10 in 100 cells and trees on 30, and puts each answer
into a checksum. Every implementation prints `40 forests of
50x50, 35 reachable: checksum 907312465`, the Kāra program under `karac
__mir-run` included (in 291 s).

Each implementation is the same search, allocating its marks and its
queue for each walk, so this measures the breadth-first search and the
allocator. Spot timings on a shared 4-core container, three runs each
(two for Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.50 to 0.54 s |
| Rust (`rustc -O`) | 0.63 to 0.66 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.65 to 0.73 s |
| Go | 1.16 to 1.23 s |
| Python | 18.3 to 18.7 s |
| Kāra (`karac build --mir`) | 0.85 to 0.91 s |
| Kāra, legacy (`karac build`) | 0.76 to 0.85 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the frozen legacy `karac build` builds it too, and
its row is above. Under `karac __mir-llvm-run` the program prints the
same line in 3.9 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

So the v2 build is about a tenth behind legacy, a third behind Rust and
two thirds behind C, and ahead of Go. It has not been profiled. The
comparison with C and Rust waits until after M4.

## Compiler findings

None new. All four arms, the differential and the bench program pass
`karac check` and run the same on both v2 backends.
