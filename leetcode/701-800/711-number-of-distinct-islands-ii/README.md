# 711. Number of Distinct Islands II

You are given an `m x n` binary matrix `grid`. An island is a group of
`1`'s (representing land) connected 4-directionally (horizontal or
vertical). You may assume all four edges of the grid are surrounded by
water.

An island is considered to be the same as another if they have the same
shape, or have the same shape after rotation (90, 180, or 270 degrees
only) or reflection (left/right direction or up/down direction). Return
the number of distinct islands.

```
grid = [[1,1,0,0,0],
        [1,0,0,0,0],
        [0,0,0,0,1],
        [0,0,0,1,1]]  ->  1   (the two L shapes are one turned)
grid = [[1,1,0,0,0],
        [1,1,0,0,0],
        [0,0,0,1,1],
        [0,0,0,1,1]]  ->  1
```

**Constraints:** 1 <= `m`, `n` <= 50; `grid[i][j]` is either `0` or `1`.

## Approaches

A square has eight symmetries: a cell (r, c) can become (±r, ±c) or (±c,
±r). Two islands are the same shape when one of the eight, applied to
one island's cells, gives the other's cells moved by some offset. Moving
a sorted list of cells so its first cell is at the origin takes the
offset out, since the first cell of a sorted list is the same cell of
the shape wherever the shape sits.

| file | mechanism |
|---|---|
| `number_of_distinct_islands_ii.kara` ★ | each island's cells by recursive depth-first search; its canonical form the smallest of its eight symmetries, each sorted, moved to the origin and flattened to one list of numbers; the forms kept in a `Set[Vec[i64]]` |
| `number_of_distinct_islands_ii_bfs.kara` | each island by breadth-first search over a `VecDeque`; the same canonical form written out as a string, the smallest string the island's key, kept in a `Set[String]` |
| `number_of_distinct_islands_ii_sorted.kara` | no hash set: each island by depth-first search with an explicit stack over flat cell numbers; the ★ arm's canonical forms sorted at the end and the runs of equal ones counted |
| `number_of_distinct_islands_ii_pairwise.kara` | no canonical form: one island of each shape kept, sorted and moved to the origin; a new island is compared with every kept island of its size, trying its eight symmetries |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 14 lines: the two LeetCode examples; one cell,
all water and all land; an L turned four ways and an L beside its
mirror, one shape each; an S beside a Z, one shape since a mirror
counts; a bar across beside the same bar down; a plus beside another
pentomino, two shapes; a checkerboard of single cells; two random 50 by
50 grids, the problem's largest, at 45% and 60% land; and 300 random
grids up to 12 by 12, with the total and a checksum.
`number_of_distinct_islands_ii.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition.
The definition is written apart from all four arms and uses no lists of
cells. It labels the land by repeated relaxation, every land cell taking
the smallest number among its land neighbours until nothing changes;
draws each island as a picture of booleans in its bounding box; and
calls two islands the same when one of the eight pictures made by
turning one a quarter at a time, before and after mirroring it, equals
the other. 2,000 random grids are checked, 1 to 10 rows and columns, 15%
to 74% land.

| | property |
|---|---|
| P1 | the count is the definition's |
| P2 | the whole grid turned a quarter has the same count |
| P3 | the whole grid mirrored has the same count |
| P4 | the grid beside its own mirror, a column of water between, has the same count |

It prints `2000 grids (4577 distinct islands), 4 arms, 32000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Eleven edits to the differential, two or three to each arm, each run
under `karac __mir-run`. Ten are killed. M4 survives, and on these grids
rightly so: five more edits, E1 to E5, change nothing that can be seen
either, and the differential reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: only the first four symmetries | P1 163 |
| M2 | ★: the cell above not searched | P1 227, P2 272, P3 64, P4 193 |
| M3 | ★: the column never negated | P1 30, P2 47, P3 41, P4 696 |
| M4 | bfs: the key without separators | 0 |
| M5 | bfs: the last row never entered | P1 628, P2 638 |
| M6 | bfs: no step to the left | P1 560, P2 628, P3 626, P4 991 |
| M7 | sorted: each form compared with the first, not the one before | P1 301, P4 1373 |
| M8 | sorted: the columns not moved to the origin | P1 989, P2 349, P3 344, P4 1794 |
| M9 | sorted: the last column never entered | P1 630, P2 592, P3 571, P4 882 |
| M10 | pairwise: the column negated in one symmetry of four | P1 14, P2 27, P3 21, P4 1035 |
| M11 | pairwise: the cell below not searched | P1 1043, P2 874 |
| E1 | ★: the largest of the eight forms, not the smallest | 0 |
| E2 | pairwise: only a larger kept island ruled out by size | 0 |
| E3 | pairwise: the search not stopped at the first match | 0 |
| E4 | pairwise: moved so the last sorted cell is at the origin | 0 |
| E5 | ★: the swapped symmetries first | 0 |

P1 kills all ten. M1 keeps only the four symmetries that do not swap
rows and columns, so a shape and its quarter turn get different forms;
only P1 sees it, since turning or mirroring the whole grid turns every
island alike and the count of classes it gets wrong stays the same.
P4 is the strongest after P1: a grid beside its mirror doubles every
island, and an arm that gets mirrors wrong, M3 and M10, now has twice as
many shapes to split. M4 drops the separators from the bfs arm's keys,
so `1,12;` and `11,2;` would both be `112`; on a grid at most 10 wide
every coordinate is one digit and a sign, so the keys still read one way
and nothing can see it. On the problem's 50 by 50 grids it could merge
two shapes, though a search over 417 shapes of a bar of 10 to 13 cells
with bumps found no two that collide. E1 takes the largest of the eight
forms, which is as canonical as the smallest; E2 rules out only a larger
kept island by size, and a smaller one then fails the exact comparison;
E3 keeps comparing after a match; E4 moves the last sorted cell to the
origin instead of the first, the same for the kept islands and the new;
and E5 tries the swapped symmetries first.

## Verification

Every arm prints the same output as `number_of_distinct_islands_ii.py`
under `karac __mir-run` (the v2 MIR interpreter) and `karac
__mir-llvm-run`, and under `karac __mir-llvm-asan` (AddressSanitizer)
with no error; the differential prints its line under all three. `karac
check` passes all four arms, the differential and the bench program. The
debug build that runs `__mir-llvm-run`, `__mir-llvm-asan` and `build
--mir` is at kara `6dc5c61842`; the release build that runs `check` and
`__mir-run` is built from the tree at `24740acba2`, the same compiler
source. No `runtime/src` change has landed since the runtime archives
were built.

The sanitizer lane cannot see a leak (kara B-2026-10-18-31), so the leak
check ran lane executables with the preloaded shim from kata 708, which
refuses the lane's hand-made stack so that LeakSanitizer sees `main`
(kata 708 showed it reporting a leak the lane misses). The
differential's executable, which calls all four arms on 8,000 grids
each, and the ★ and bfs arms' own report no leak. The sorted and
pairwise arms' executables finish before they can be copied out, so they
were checked only through the differential.

The frozen legacy backends refuse all four arms and the differential at
type checking: at a recursive call such as `collect(grid, mut seen,
...)`, whose `seen` is already a `mut ref`, where legacy wants the
marker dropped and design.md § Call-site `mut` markers now requires it
(kara B-2026-10-14-25), and at `*r` and the like over `iter()`, since
legacy gives those items by value where v2 gives references. They refuse
the bench program at the second. Legacy is frozen, so this is noted, not
filed.

## Benchmarks

The bench program uses the sorted arm, which needs no hash set and so is
the same algorithm in all five languages; the ★ arm's `Set` has no
counterpart in C. It makes 100 random 50 by 50 grids once, from 30% to
69% land, and counts the distinct islands in each ten times, summing the
counts. Every implementation prints `10 rounds of 100 grids of 50 by
50: 42770 distinct islands`, the Kāra program under `karac __mir-run`
included (in 49 s).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.47 to 0.61 s |
| Rust (`rustc -O`) | 0.42 to 0.45 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.45 to 0.48 s |
| Go | 0.78 to 0.85 s |
| Python | 3.7 s |
| Kāra (`karac build --mir`) | 0.61 to 0.71 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the legacy `karac build` refuses it (above). That
edit is by hand, on top of the `scripts/new-bench.sh` output. Under
`karac __mir-llvm-run` the program prints the same line in 3.5 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

So the v2 build is about 50% behind Rust and 20% behind C, and ahead of
Go. Under valgrind's cachegrind it runs 5.10 billion instructions,
against Rust's 4.02 and C's 3.33, with 924 million branches against
Rust's 523, and mispredicts 51 million against Rust's 30. 83 million of
its branches are indirect, close to C's 98 million, where C's come from
`qsort` calling its comparison through a pointer, against Rust's
23 million; that suggests v2's sorts call their comparison indirectly
too, though it was not traced. The comparison with C and Rust waits
until after M4.

## Compiler findings

None new.
