# 778. Swim in Rising Water

`grid` is an `n` by `n` grid of elevations. Rain starts falling, and at
time `t` the water everywhere is at depth `t`: the swimmer can move from
a square to any of its four neighbours when both are at elevation at
most `t`, and can swim any distance in no time. Return the least time
at which the swimmer, starting at the top left square, can reach the
bottom right one.

```
grid = [[0,2],[1,3]]                                      ->  3
grid = [[0,1,2,3,4],[24,23,22,21,5],[12,13,14,15,16],
        [11,17,18,19,20],[10,9,8,7,6]]                    ->  16
```

**Constraints:** `n` is from 1 to 50, and the grid holds every integer
from 0 to `n² - 1` once.

## Approaches

The answer is the least, over every way from the top left to the bottom
right, of the highest square on the way: a bottleneck path.

| file | mechanism |
|---|---|
| `swim_in_rising_water.kara` ★ | Dijkstra with a way's highest square as its cost: a smallest-first `PriorityQueue` of (highest so far, square) settles the squares in order of that cost, and the bottom right's is the answer; O(n² log n) |
| `swim_in_rising_water_binary.kara` | binary search on the time, from the higher corner to `n² - 1`, each guess checked by a flood fill over the squares at most that high; O(n² log n) |
| `swim_in_rising_water_unionfind.kara` | the squares flooded in order of elevation, which is one new square at each time, each joined to its flooded neighbours in a disjoint-set forest, until the two corners share a set; O(n² α(n²)) |
| `swim_in_rising_water_bucket.kara` | the swimmer's reach grown time by time: a table from elevation to square is a bucket queue, a square touching the reach waits for its time, and at that time a flood fill takes in it and every square it opens up below the water; O(n²) |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 10 lines: LeetCode's two examples; one square;
the top left the highest square; four other small grids; a random 50 by
50 grid, LeetCode's limit; a 50 by 50 snake, 0 to 2,499 laid along the
rows with every other row backwards; then 300 random grids of 1 to 20
squares a side, with the sum of the answers and a checksum.
`swim_in_rising_water.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
every simple way from the top left to the bottom right walked by depth
first search, and the least of their highest squares. Its 1,100 random
grids are 1,000 of 1 to 5 squares a side, where that walk is cheap, and
100 of 6 to 40. A quarter hold their values in a random order, a
quarter are snakes, a quarter have the values along the rows all
forwards, and a quarter are a winding corridor: the even rows joined at
alternate ends by one square of the odd row between them, laid with the
lowest values in the corridor's order and the walls' values above them
in a random order, which is the shape of LeetCode's second example. The
last three kinds then have up to `n` random pairs of values traded.

| | property |
|---|---|
| P1 | the answer is the definition's (grids up to 5 a side) |
| P2 | the grid transposed, turned half round, or reflected in the other diagonal gives the same answer: each keeps the corners as the corners |
| P3 | two values below the answer traded, or two above it, give the same answer, since the squares under water at each time up to the answer are the same |
| P4 | the squares of elevation at most the answer join the corners, and those at most one less do not |

It prints `1100 grids (answers sum to 55462), 4 arms, 17200 checks, 0
failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the highest so far forgotten | P1 266, P2 887, P3 69, P4 303 |
| M2 | ★: the top left's own height ignored | P1 108, P2 697, P3 21, P4 113 |
| M3 | ★: only right and down moves | P1 22, P3 12, P4 50 |
| M4 | binary: the search cut one short | P1 80, P3 24, P4 92 |
| M5 | binary: the flood stopping below `t` | P1 410, P2 351, P4 473 |
| M6 | binary: the bottom row or right side counted as across | P1 86, P2 135, P3 20, P4 105 |
| M7 | unionfind: neighbours joined flooded or not | P1 158, P3 31, P4 193 |
| M8 | unionfind: find returning the square itself | P1 787, P4 887 |
| M9 | unionfind: only right and down neighbours joined | P1 752, P2 430, P3 20, P4 852 |
| M10 | bucket: squares not waiting flooded too | P1 266, P2 887, P3 70, P4 306 |
| M11 | bucket: the fill taking squares one above the water | P1 336, P2 487, P3 146, P4 387 |
| M12 | bucket: squares touched above the water never waiting | P1 679, P2 694, P4 774 |

P1 and P4 each kill all twelve. P2 compares the grid with three images
of it that keep the corners as the corners, so it sees only mutants
that treat the directions, or the two corners, differently. M3 takes
the best of the ways that go only right and down, and the three images
carry those ways onto one another, so its wrong answer is the same each
time; M4, M7 and M8 are wrong in the same way in every direction. M3 is
also the one first choice that nearly survived: on random grids, snakes
and rows all forwards the best way almost always goes only right and
down, and the first version of the differential saw it in 5 of its
17,200 checks. The winding corridors, where every way below the walls
turns back on itself, were added for it.

## Verification

Every arm prints the same output as `swim_in_rising_water.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`4f079681eb`, whose last compiler change is `ecb1a0322e`. The runtime
archives were built after the last runtime change, `176f59738b`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends accept all four arms, and each prints the
same output under the legacy interpreter (`karac run --interp`; the ★
arm in 69 s), the legacy JIT (`karac run`), `karac build` and an
auto-par build, each build with a warning that a borrowed `grid` is used
after a move, since legacy predates borrowed parameters. Legacy refuses
the differential at its type check: in `for v in row.iter()` and
`for at in order.iter()` it takes the items for `i64` rather than
references, so `*v` and `*at` are errors. It refuses the bench at
`swim_in_water(grids[g])`, as a move out of an index; the bench timing
below is of a copy whose parameter is `ref Vec[Vec[i64]]`. Legacy is
frozen, so all this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. 64 grids of 50
by 50, LeetCode's limit, are built once: half hold 0 to 2,499 in a
random order, a quarter are snakes and a quarter have the values along
the rows all forwards, each of those with 50 random pairs of values
traded. Each of 3,000 rounds answers the next grid. Every implementation
prints `3000 rounds of 50 x 50 grids: answers sum to 6653387, checksum
805291479`, the Kāra program under `karac __mir-run` included (in
430 s).

Every round runs Dijkstra over a 50 by 50 grid: up to 2,500 squares
settled and up to four pushes onto the priority queue for each,
so the bench measures a binary heap of pairs and the neighbour checks
around it. Rust's queue is `BinaryHeap<Reverse<(i64, i64)>>`, C's a
hand-written binary heap of the same pairs and Go's `container/heap`,
whose interface boxes each pair it pushes. Spot timings on a shared
4-core container, eight runs of each compiled program, five of them
interleaved, and three of Python (`bench.sh` timings need a quiet
machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.74 to 0.89 s |
| Rust (`rustc -O`) | 0.75 to 0.89 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.81 to 1.01 s |
| Go | 2.84 to 3.17 s |
| Python | 9.78 to 10.34 s |
| Kāra (`karac build --mir`) | 1.86 to 2.21 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, since the legacy `karac build` refuses it (see
Verification); that edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 5.3 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

At the medians of the interleaved runs the v2 build takes 1.91 s,
against C's 0.78, Rust's 0.79 (0.90 under overflow checks) and Go's
2.93. Under valgrind's cachegrind v2 runs 12.3 billion instructions and
2.05 billion branches, against Rust's 4.59 billion and 0.44 billion and
C's 4.73 billion and 0.53 billion, and mispredicts 124 million branches
to their 29 and 31 million. Half of v2's instructions are in two
functions outside `main` that the binary carries no names for, so where
the difference lies is not profiled. The legacy build of the copy ran
1.60 to 1.78 s, a median of 1.72 s in the interleaved runs, so v2 takes
1.11 times legacy. The comparison with C and Rust waits until after M4.

## Compiler findings

Nothing new.
