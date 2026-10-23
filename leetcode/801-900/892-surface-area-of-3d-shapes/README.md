# 892. Surface Area of 3D Shapes

You are given an `n x n` grid where you have placed some `1 x 1 x 1`
cubes. Each value `v = grid[i][j]` represents a tower of `v` cubes
placed on top of cell `(i, j)`.

After placing these cubes, you have decided to glue any directly
adjacent cubes to each other, forming several irregular 3D shapes.

Return the total surface area of the resulting shapes.

**Note:** The bottom face of each shape counts toward its surface area.

```
grid = [[1,2],[3,4]]  ->  34
grid = [[1,1,1],[1,0,1],[1,1,1]]  ->  32
grid = [[2,2,2],[2,1,2],[2,2,2]]  ->  46
```

**Constraints:** `n == grid.length == grid[i].length`, `1 <= n <= 50`,
and `0 <= grid[i][j] <= 50`.

## Approaches

| file | mechanism |
|---|---|
| `surface_area.kara` ★ | six faces a cube, less the shared ones: a tower of v cubes shares v - 1 faces inside it and so shows 4v + 2, and two neighbouring towers share as many faces as the shorter is tall; count every tower, then take away twice the shorter of each pair of neighbours, right and down so each pair is seen once. O(n^2) |
| `surface_area_faces.kara` | the faces each tower shows: a top and a bottom when it has cubes, and on each of its four sides the part that rises above the neighbour there, a cell off the grid counting as height 0. O(n^2) |
| `surface_area_voxels.kara` | every cube built: the shapes as a grid of unit cubes, n by n by the tallest tower, and each face of each cube counted when the neighbour across it is empty or outside. O(n^2 * tallest) |
| `surface_area_sweeps.kara` | the steps along each row and column: walking a row from the edge, past each tower and off the far edge, every change of height shows that many faces facing along the row, and the same down each column; with a top and a bottom for each tower that has cubes, that is the whole surface. O(n^2) |
| `surface_area_layers.kara` | the outline of each layer: cut into layers one cube high, layer h holds the cells whose tower reaches h, and its sides are the edges between a cell in it and one outside it or off the grid. O(n^2 * tallest) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's three examples and three
more (an empty grid of one cell, a single tower of 50, and two towers
touching only at a corner), and for 300 random grids of LeetCode's
sizes, up to 50 by 50 with towers up to 50 high or, a third of the time,
up to 3 high with a cell in three empty, the total area, 6,939,398, of
4,482,796 cubes, with a checksum. `surface_area.py` mirrors the ★ arm
and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every unit square of the box around the shapes, in each of
the three orientations, counted when it has a cube on exactly one side,
so that a face glued between two cubes is not surface. It checks 3,200
random grids: 3,000 of up to 5 by 5 with towers up to 4 high against the
statement, and 200 of up to 20 by 20 with towers up to 3 or 50 high
against the other properties, half of them with a cell in three empty.
The ★ arm's areas sum to 899,934.

| | property |
|---|---|
| P1 | the statement's area, on up to 5 by 5 |
| P2 | the grid turned a quarter, and reflected across its diagonal, has the same area |
| P3 | every tower k times as tall, for k from 2 to 4, shows k times the sides and the same tops and bottoms |
| P4 | the grid and a second random grid on one grid, an empty row and column between them, show both their areas |
| P5 | one random tower a cube taller gains its four new sides less two faces for each neighbour taller than it was, and a top and a bottom if it was empty |
| P6 | each arm agrees with at least two of the other four |

P2 to P6 are checked on every grid. It prints `3200 cases, 64313
cells, surface area 899934 in all, 95000 checks over 5 arms: 0
failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an empty cell given a top and a bottom | P1 2400, P3 2577, P4 3200, P5 1058, P6 2577 |
| M2 | ★: the faces shared with the tower below never taken away | P1 2110, P2 1976, P5 1137, P6 2294 |
| M3 | ★: one face of each pair shared across a row taken away, not two | P1 2144, P2 1976, P5 1186, P6 2328 |
| M4 | faces: the step down to the left neighbour never counted | P1 2784, P2 1976, P5 2239, P6 2981 |
| M5 | faces: a step up to a taller neighbour below taken away | P1 1659, P2 1861, P5 967, P6 1839 |
| M6 | faces: the last row taken as off the grid | P1 2052, P2 2154, P4 2238, P5 787, P6 2238 |
| M7 | voxels: a face onto the top layer of the box always counted | P1 2642, P3 2979, P4 2115, P5 972, P6 2838 |
| M8 | voxels: each tower's bottom cube left empty | P1 2642, P3 2970, P5 1290, P6 2838 |
| M9 | voxels: the faces looking down never counted | P1 2784, P3 2981, P5 1058, P6 2981 |
| M10 | sweeps: the far end of each column never counted | P1 2663, P2 2260, P4 2860, P5 1430, P6 2860 |
| M11 | sweeps: only steps up counted along a row | P1 2135, P2 2521, P4 2870, P5 1408, P6 2321 |
| M12 | sweeps: an empty tower given a top and a bottom | P1 2400, P3 2577, P4 3200, P5 1058, P6 2577 |
| M13 | layers: the top layer never outlined | P1 2784, P3 2981, P4 2350, P5 1035, P6 2981 |
| M14 | layers: a cell in the second row counted as on the edge | P1 1958, P2 1884, P4 1634, P5 574, P6 2138 |
| M15 | layers: an equal neighbour to the right counted as outside | P1 1953, P2 2185, P3 2136, P5 724, P6 2136 |

P1, P5 and P6 kill all fifteen. M1 and M12 are one fault in two arms
and fail the same cases. P2 kills exactly the mutants that treat one
direction differently from another (M2 to M6, M10, M11, M14, M15); the
voxels mutants and those that miscount tops and bottoms are the same
in every direction, so turning the grid does not move them. P3 kills
the faults that do not scale with the towers' height, such as a top
and bottom for an empty cell or a missing top layer, which stay the
same while the sides grow k times. P4 kills the faults that depend on
the grid as a whole, its size, its empty cells or its tallest tower,
all of which the second grid and the empty row and column between them
change. No mutant was replaced.

## Verification

Every arm prints the same output as `surface_area.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build and the runtime archives are both at
kara `5502146bed`. Under `karac __mir-run` the arms take 0.6 to 18.5 s
each (the voxels arm, which builds every cube, is the slow one) and the
differential 24 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The frozen legacy interpreter, JIT and `karac build --legacy`, with and
without auto-par, print the same output for the ★, faces and sweeps
arms. Every legacy lane refuses the voxels and layers arms and the
differential, because `*v` on an element of `row.iter()` is rejected
(legacy's iterator gives the value itself), and the bench program,
where `grids[g]` passed to a function is a move out of an index
(`E_INDEX_MOVE_NON_COPY`). Legacy is frozen, so these are not filed.

## Benchmarks

The bench program uses the ★ arm, in all five languages: 400 random
grids of 50 by 50, LeetCode's largest, with towers up to 50 high, built
once; then 80 passes, each raising one tower of every grid by a cube and
measuring every grid again, 32,000 measurements in all. Kāra's, Rust's,
Go's and Python's grids are vectors of rows; C's are one flat array.
Every implementation prints `32000 measurements of 400 grids of 50 by
50: surface area 2979961402, checksum 828055420`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.20 to 0.24 s | 0.21 s |
| Rust (`rustc -O`) | 0.16 to 0.21 s | 0.18 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.26 to 0.31 s | 0.27 s |
| Go | 0.22 to 0.28 s | 0.25 s |
| Python | 19.6 s | |
| Kāra (`karac build --mir`) | 0.29 to 0.36 s | 0.30 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 891's does. Legacy refuses the bench program
(above), so it has no row.

v2 takes 1.13 times Rust's median time under overflow checks and 1.41
times C's. Under valgrind's cachegrind C runs 2.03 billion
instructions with 42 million branches, Rust with overflow checks 3.09
billion with 961 million and v2 3.29 billion with 1.03 billion. Most
likely clang turned the `min`s and the `v > 0` test into branch-free
code and the overflow checks keep Rust and Kāra from doing the same
(inferred from the branch counts, not from the generated code). The
comparison with C and Rust waits until after M4.
