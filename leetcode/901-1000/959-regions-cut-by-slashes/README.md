# 959. Regions Cut By Slashes

An `n x n` grid is composed of `1 x 1` squares where each `1 x 1` square
consists of a `'/'`, `'\'`, or blank space `' '`. These characters
divide the square into contiguous regions. Given the grid `grid`
represented as a string array, return *the number of regions*. Note that
backslash characters are escaped, so a `'\'` is represented as `'\\'`.

```
grid = [" /","/ "]      ->  2
grid = [" /","  "]      ->  1
grid = ["/\\","\\/"]    ->  5
```

**Constraints:** `n == grid.length == grid[i].length`; `1 <= n <= 30`;
`grid[i][j]` is either `'/'`, `'\'`, or `' '`.

## Approaches

| file | mechanism |
|---|---|
| `regions_by_slashes.kara` ★ | four triangles per cell: each cell cut along both diagonals into a top, right, bottom and left triangle, joined in a union-find. A blank joins all four, a slash `/` the top with the left and the right with the bottom, a backslash the top with the right and the bottom with the left; each right triangle joins the left one of the cell beside it, each bottom the top of the cell below. The regions are the sets left. O(n^2 a(n^2)) |
| `regions_by_slashes_pixels.kara` | three pixels to a cell: a slash fills the three pixels of its diagonal, enough to keep the cell's two sides apart while every open side still touches its neighbour, and the regions are the groups of empty pixels joined edge to edge, each flooded with an explicit stack. O(n^2) |
| `regions_by_slashes_points.kara` | the corner points in a union-find, the border's points joined from the start: each slash is a segment between two corners, and when they are already joined it closes a loop and cuts one more region off the one region the square starts as. O(n^2 a(n^2)) |
| `regions_by_slashes_flood.kara` | the four triangles of each cell as a graph walked with an explicit stack, joined inside a cell by its character and across cells side to side; each walk from an unseen triangle is one region. O(n^2) |
| `regions_by_slashes_euler.kara` | Euler's formula: the border and the slashes make a plane graph on the (n + 1)^2 corner points with E - V + C + 1 faces for E segments, V points and C pieces, the outside among them, so the square holds E - V + C regions; C is counted by a breadth-first walk, a point no segment touches a piece of its own. O(n^2) |
| `differential.kara` | the five arms against the statement read literally, six properties |

The first draft of the differential's helper that swaps a slash for a
backslash returned its bare `String` parameter; `karac check` refused
that, since a bare parameter borrows, and `karac fix` made it `own`.

Every arm prints the same 20 lines: LeetCode's three examples and seven
more (one blank cell, one slash, one backslash, a cross of four, two
rows of slashes, a diamond inside a 4 by 4 grid, and a 3 by 3
checkerboard); for 300 random grids of 1 to 10 cells a side, 11,404
cells in all, the total of the regions and a checksum; four random grids
of LeetCode's largest size, 30 by 30, with blanks at chances 0, 3, 6
and 9 in 10; and five 30 by 30 grids tiled from a pattern: all slashes,
all backslashes, the two checkerboards and all blanks.
`regions_by_slashes.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the square drawn at five pixels to a cell, each slash a
diagonal line of five pixels, and the regions the groups of empty pixels
joined edge to edge. It checks 3,200 random grids, each with blanks at a
random chance from 0 to 9 in 10: 3,000 of up to 5 cells a side against
the statement, and 200 of up to 20 against the other properties; 60,318
cells in all.

| | property |
|---|---|
| P1 | the statement's answer, on the small cases |
| P2 | the grid turned a quarter turn, slashes and backslashes swapped, gives the same answer |
| P3 | the grid mirrored left for right, slashes and backslashes swapped, gives the same answer |
| P4 | the grid reflected in its main diagonal, each slash kept, gives the same answer |
| P5 | a slash or backslash in a random cell adds no region or one to the grid with that cell blank |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 grids of 60318 cells, regions: 11754, checksum
554305343, 95000 checks over 5 arms: 0 failures` under `karac __mir-run`
(37 s) and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error. The large grids were cut from up
to 30 cells a side to up to 20, which took about a quarter off the
interpreter run.

## Mutation testing

Thirty-four edits to the differential, each run under
`karac __mir-llvm-run`; fifteen are kept, three to each arm, and all
fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a slash joining the top with the right | P1 866, P2 1041, P3 1097, P4 789, P6 1003 |
| M2 | ★: a blank joining only three triangles | P1 2257, P2 547, P3 674, P4 549, P5 95, P6 2436 |
| M3 | ★: each right triangle joined to the right one beside it | P1 1239, P2 1432, P3 1567, P4 1458, P6 1399 |
| M4 | pixels: a slash drawn as a backslash | P1 1017, P2 1076, P3 1076, P6 1154 |
| M5 | pixels: two pixels to a diagonal | P1 2209, P6 2377 |
| M6 | pixels: a step left from the first column wrapping to the row above | P1 1433, P2 1288, P3 1234, P4 1090, P5 94, P6 1577 |
| M7 | points: the square not counted as a region | P1 3000, P6 3200 |
| M8 | points: a loop counted twice | P1 2209, P5 2070, P6 2377 |
| M9 | points: the bottom border left out | P1 1426, P2 995, P4 995, P6 1554 |
| M10 | flood: a backslash joining opposite triangles | P1 994, P2 798, P3 798, P6 1132 |
| M11 | flood: a top touching the top above, not the bottom | P1 1303, P2 1668, P3 1051, P4 1681, P5 18, P6 1465 |
| M12 | flood: a right side touching nothing beside it | P1 2389, P2 1708, P3 1700, P4 1424, P5 234, P6 2581 |
| M13 | euler: the right border left out | P1 3000, P2 979, P3 1277, P4 995, P6 3200 |
| M14 | euler: a slash not counted as a segment | P1 2584, P5 1130, P6 2777 |
| M15 | euler: a slash walked one way only | P1 1452, P2 1373, P4 1373, P6 1621 |

P1 and P6 kill all fifteen, P2 eleven (all but M5, M7, M8 and M14), P3
nine (M1 to M4, M6, M10 to M13), P4 nine (M1 to M3, M6, M9, M11 to M13,
M15) and P5 six (M2, M6, M8, M11, M12, M14).

Nineteen other edits were tried and set aside. Four failed exactly the
same checks as a kept one: points leaving the border unjoined, as M5;
points and flood treating a slash as a backslash, as M4; and euler
counting one piece too many, as M7. Twelve were sound but beyond three
an arm: ★ joining each bottom to the bottom below, counting every union
and not joining the last two columns; pixels never stepping down into
the last pixel row and drawing a backslash as a slash; points drawing a
backslash down the cell's right side; flood joining a bottom to the left
triangle below, a left side to the left one beside it, and a blank's
triangles only three at a time; and euler drawing a slash down the
right side, leaving out the points no segment touches, and drawing the
top border upright. One ran out of time: points joining a root to the
second corner itself rather than to its root, which can make a cycle
that `find` walks for ever.

Two were equivalent. ★ finding roots without flattening the path: the
roots are the same, only reached in more steps. And pixels not marking
the start before flooding: a neighbour marks it and pushes it again, and
a start alone in its region is never visited again, since the scan has
passed it.

## Verification

Every arm prints the same output as `regions_by_slashes.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `cb8ffcccec`, the runtime
archives rebuilt at the same commit. Under `karac __mir-run` points
takes 0.25 s, euler 0.41 s, ★ and pixels 0.48 s and flood 0.93 s, and
the differential 37 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench program makes 100 random grids of 30 by 30 once, with blanks
at chances 0 to 9 in 10 in turn. In each of 300 rounds it runs the ★ arm
on every grid, each round starting from a different one, and folds the
regions into a checksum. Every implementation prints `300 rounds over
100 grids of 30 by 30: 1135800 regions, checksum 212697042`. Each call
makes a union-find of 3,600 triangles: a `Vec` in Kāra and Rust, a slice
in Go and a list in Python, while C keeps it in an array on the stack and
allocates nothing.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.83 to 0.95 s | 0.86 s |
| Rust (`rustc -O`) | 0.93 to 1.04 s | 0.99 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.95 to 1.03 s | 1.01 s |
| Go | 1.35 to 1.50 s | 1.43 s |
| Python | 52.4 s | |
| Kāra (`karac build --mir`) | 1.23 to 1.39 s | 1.29 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 61 times
C's.

v2 takes 1.28 times Rust's median time under overflow checks and 1.50
times C's. Under valgrind's cachegrind v2 runs 10.33 billion
instructions and 2.35 billion branches with 194 million mispredicted,
Rust with overflow checks 7.03 billion, 2.03 billion and 110 million,
and C 5.05 billion, 1.03 billion and 94.5 million.
