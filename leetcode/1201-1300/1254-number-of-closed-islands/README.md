# 1254. Number of Closed Islands

Given a 2D `grid` consists of `0`s (land) and `1`s (water). An *island*
is a maximal 4-directionally connected group of `0`s and a *closed
island* is an island totally (all left, top, right, bottom) surrounded
by `1`s.

Return the number of *closed islands*.

```
grid = [[1,1,1,1,1,1,1,0],[1,0,0,0,0,1,1,0],[1,0,1,0,1,1,1,0],[1,0,0,0,0,1,0,1],[1,1,1,1,1,1,1,0]]  ->  2
grid = [[0,0,1,0,0],[0,1,0,1,0],[0,1,1,1,0]]                                                          ->  1
grid = [[1,1,1,1,1,1,1],[1,0,0,0,0,0,1],[1,0,1,1,1,0,1],[1,0,1,0,1,0,1],[1,0,1,1,1,0,1],[1,0,0,0,0,0,1],[1,1,1,1,1,1,1]]  ->  2
```

**Constraints:** `1 <= grid.length, grid[0].length <= 100`;
`0 <= grid[i][j] <= 1`.

The arms are `fn closed_island(grid: Vec[Vec[i64]]) -> i64`, the grid
taken by value (`own`) where the arm floods it.

## Approaches

| file | mechanism |
|---|---|
| `closed_island.kara` ★ | depth first, by recursion over a `mut ref` grid: each island flooded to water from its first cell, and counted when no cell of it reached the edge; all four neighbours visited before the answers are combined, so the whole island is flooded |
| `closed_island_bfs.kara` | breadth first: each island walked with a `VecDeque` and a `seen` grid, the grid left as it is, and counted when none of its cells lies on the edge |
| `closed_island_border.kara` | the edge first: every island touching the edge sunk from its edge cells with an explicit stack, then each island left counted and sunk |
| `closed_island_dsu.kara` | union-find in a `Dsu` struct with path compression: land joined to the land right of it and below it, every edge cell to one more node for the outside, and the closed islands the roots of land other than the outside's |
| `closed_island_solution.kara` | a Rust solution as LeetCode's Rust users write it (`Self::dfs(&mut grid, i as i32, j as i32)`, `\|\|` and `&&`, `Vec<Vec<i32>>`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's three examples; the total
and a checksum of the counts for 500 random grids of 1 to 100 rows and
columns with 20 to 80 in 100 of land (`total 74343, checksum 787232716`);
and two 100 by 100 grids at the constraints' top, a single winding path
of land framed by water, whose flooding recurses about 4850 cells deep
(1), and land on every other cell like a chessboard (4802). The ★ arm's
recursion runs that deep under `karac __mir-run`, `karac run`, `karac
build` and the AddressSanitizer build alike. `closed_island.py` mirrors
the ★ arm, and its output is byte-identical. Every arm gives the same
output under `karac run` and `karac build`, and under the
AddressSanitizer build.

The Mend loop: the ★ and edge-first arms were first written with
`own grid: Vec[Vec[i64]]`, the mode before the name, and `karac fix`
moves it into the type, `grid: own Vec[Vec[i64]]` (E0002). The breadth
first and union-find arms checked clean as first written. The solution
arm takes one round of fixes, 26 edits by `karac fix`'s count (`struct
Solution;` to `struct Solution {}`, `Vec<Vec<i32>>` to brackets twice,
the parameter to `own` since the method floods the grid it was given,
`&mut Vec<..>` to `mut ref Vec[..]`, `Self::dfs(&mut grid, ..)` to
`Solution.dfs(mut grid, ..)` at all five calls, and the three `||` and
four `&&` to `or` and `and`). All five check clean.

## Gaps

None found: every arm, as written, checks after its fixes, and runs and
builds alike.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every land cell given its own number, each taking the least
number of a land neighbour until none changes, so that the cells of an
island share one; an island closed when no cell of it lies on the edge.
2000 cases of 1 to 8 rows and columns with 20 to 80 in 100 of land.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the grid transposed gives the same count |
| P3 | the grid mirrored left to right gives the same count |
| P4 | a frame of water around the grid closes every island: the count is the number of islands |
| P5 | a frame of land around the grid gives the same count |
| P6 | the ★ arm's count |

All 60,000 checks pass on every arm: `2000 grids: checksum 225024792,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python, walking the
islands with a stack, gives the same checksum.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: the four neighbours joined with a short-circuiting `and`, so an island is left half flooded | P1 478, P2 324, P3 416, P5 1115, P6 1912 |
| S2 | ★: beyond the edge taken as water | P1 1914, P5 1377, P6 7656 |
| B1 | breadth first: the right edge not taken as the edge | P1 405, P2 498, P3 443, P5 405, P6 405 |
| B2 | breadth first: the step right made a second step left | P1 485, P2 525, P3 382, P4 1362, P5 479, P6 485 |
| D1 | edge first: the column before the right edge sunk in its place | P1 352, P2 489, P3 469, P4 1684, P5 352, P6 352 |
| D2 | edge first: the sinking never steps right | P1 351, P2 420, P3 406, P4 1362, P5 382, P6 351 |
| U1 | union-find: land never joined to the land below | P1 669, P2 676, P4 1393, P5 923, P6 669 |
| U2 | union-find: the outside's root counted when it is a land cell | P1 1577, P2 4, P3 24, P5 423, P6 1577 |
| L1 | solution: the right neighbour's answer dropped | P1 441, P2 507, P3 474, P5 441, P6 441 |
| L2 | solution: water taken as open | P1 403, P4 1916, P6 403 |

All ten are caught, every one by P1, the statement read literally, and
by P6, which fails on the other four arms too when the ★ arm is the one
mutated (S1, S2). P5, the frame of land, catches nine: it joins every
edge island into one that touches everything, which an arm that floods
or joins only part of an island (S1, B2, D2, U1), misses an edge (S2,
B1, D1, L1), or counts the outside (U2) gets wrong. Only L2, which
counts no island at all, keeps it, and P4, the frame of water, catches
L2 with the four that split or miss islands outright (B2, D1, D2, U1).
P2 and P3, the grid transposed and mirrored, catch the ones that treat
one side or one direction differently; U1 drops only the joins
downwards, which mirroring left to right does not move, so P3 keeps it.
S2, which takes the edge as water, keeps P2, P3 and P4: it counts every
island, the true count of a grid framed by water.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (each island flooded to water by recursion from its first cell, and
counted when no cell of it reached the edge) on 100 random 100 by 100
grids built once, each with its own share of land from 20 to 80 in 100;
each copied and asked 40 times, every count folded into a checksum.
Every program prints `40 rounds of 100 grids of 100 by 100: checksum
782789038`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.648 to 0.742 s | 0.679 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.645 to 0.768 s | 0.684 s |
| Rust (`rustc -O`) | 0.634 to 0.702 s | 0.672 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.648 to 0.717 s | 0.677 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.635 to 0.752 s | 0.678 s |
| C (`clang -O3`) | 0.565 to 0.671 s | 0.590 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.564 to 0.598 s | 0.583 s |
| Go | 0.767 to 0.863 s | 0.799 s |
| Python | 14.81 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on runs level with Kāra (0.677 s
against 0.684 s), and the two ranges overlap. C is about 14% ahead of
Kāra (0.590 s against 0.684 s); Kāra is about 14% ahead of Go (0.684 s
against 0.799 s). Python takes about 22x Kāra's time. No profile was
taken.
