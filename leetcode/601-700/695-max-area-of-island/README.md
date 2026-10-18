# 695. Max Area of Island

You are given an m x n binary grid. An island is a group of 1's (land)
connected four-directionally (horizontally or vertically), and all four
edges of the grid are surrounded by water. The area of an island is the
number of cells with a value 1 in the island. Return the maximum area of
an island, or 0 if there is no island.

```
0010000000000
0000000111000
0110100000000
0100110010100
0100110011100
0000000000100
0000000111000
0000000110000   ->  6

00000000        ->  0
```

**Constraints:** 1 <= m, n <= 50; each cell is 0 or 1.

## Approaches

Every arm is `fn max_area_of_island(grid: Vec[Vec[i64]]) -> i64`.

| file | mechanism |
|---|---|
| `max_area_of_island.kara` ★ | from each land cell, a recursive depth-first search sinks the island in a copy of the grid and counts its cells; O(m n) |
| `max_area_of_island_bfs.kara` | the same sweep with a `VecDeque`, each cell marked as it is queued; O(m n) |
| `max_area_of_island_unionfind.kara` | union-find over the cells, the smaller set hung under the larger and its size added; the largest root size; O(m n α(m n)) |
| `max_area_of_island_runs.kara` | union-find over each row's runs of land, weighted by length, each run joined to the runs it overlaps in the row above; fewer nodes than cells when land comes in long stretches; O(m n) |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 5 lines: the two LeetCode examples; a 50 by
50 grid of land, a 50 by 50 checkerboard, and a 50 by 50 snake that runs
along every other row and turns at alternate ends, 1,275 cells in one
island; a column, a row, and two islands that touch only at a corner;
and 200 random grids of up to 50 by 50 with 10 to 80 percent land, the
largest areas summed and put into a checksum. `max_area_of_island.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition.
The definition is written apart from all four arms: every land cell is
labelled with its own number, and each label is lowered to the least of
its land neighbours' until nothing changes, so each island ends with one
label; the answer is the most cells that share a label. 3,000 random
grids of 1 to 12 by 1 to 12 are checked, with 20 to 80 percent land.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the mirror image, each row reversed, has the same answer |
| P3 | so has the grid with rows and columns swapped |
| P4 | the grid twice side by side, water between, has the same answer |

It prints `3000 grids, 4 arms, 48000 checks, 0 failures` under `karac
__mir-run` and `karac __mir-llvm-run`, and runs clean under `karac
__mir-llvm-asan`.

## Mutation testing

Thirteen edits to the differential, each run under `karac __mir-run`:
twelve that change answers, three to each arm, and one that does not.
All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: no step up | P1 775, P2 346, P3 990 |
| M2 | ★: a cell not counted | P1 2944 |
| M3 | ★: the last island kept, not the largest | P1 1842, P2 461, P3 760 |
| M4 | bfs: no step to the left | P1 1328, P2 1592, P3 1242 |
| M5 | bfs: the areas added up, not compared | P1 2390, P4 2944 |
| M6 | bfs: the last row never reached | P1 1580, P3 1906 |
| M7 | unionfind: a join adds one, not the smaller set's size | P1 1237, P2 1274, P3 1219 |
| M8 | unionfind: left and right neighbours never joined | P1 2378, P3 2041 |
| M9 | unionfind: every set starting at size 2 | P1 2944 |
| M10 | runs: runs that share one column not joined | P1 2148, P3 2163 |
| M11 | runs: each run one cell too long | P1 2944, P3 2085 |
| M12 | runs: no row compared with the one above | P1 2424, P3 2041 |
| E1 | unionfind: the smaller set made the root | 0 |

P1 kills all twelve; 2,944 is the number of grids with any land, so
M2, M9 and M11, which get every island wrong, fail every one of them.
P3 sees most mutants a second time, since swapping rows and columns
turns a mutant's blind spot along one axis onto the other: no step up,
no step left, no left and right join, no comparison with the row above,
the last row never reached. P2 sees fewer: a mirror keeps rows as rows,
so a mutant that misses the last row, never joins left and right
neighbours, or never compares a row with the one above fails the mirror
in the same way and agrees with itself. P4 sees only M5, the one mutant
whose answer grows with the number of islands. E1 is equivalent: hanging
the larger set under the smaller makes the trees deeper but still adds
each set's size to its new root, so every size stays right.

## Verification

Every arm prints the same output as `max_area_of_island.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints its line under all three. `karac check` passes all four arms, the
differential and the bench program. All with the compiler at kara
`f6a225c404` for both the debug build and the release build that runs
`check` and `__mir-run`, with runtime archives rebuilt after the last
`runtime/src` change.

The frozen legacy backends refuse all four arms and the differential at
type checking: at `*b` over `row.bytes().iter()` in the harness, and in
the runs arm at `*a`, `*b` and `*other` over a destructured `(a, b,
other)` from `above.iter()`, since legacy gives those items by value
where v2 gives references. They build the bench program as it is. Legacy
is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the union-find arm, the one that is the same
algorithm in all five languages. It builds 40 grids of 50 by 50 once,
with 30 to 70 percent land, then finds each grid's largest island in
each of 300 rounds, putting each area into a checksum. Every
implementation prints `300 rounds of 40 grids of 50 by 50: largest areas
sum to 4748400, checksum 506921845`, the Kāra program under `karac
__mir-run` included (in 51 s).

Each implementation allocates its parent and size arrays afresh for each
grid. Spot timings on a shared 4-core container, eight runs of each
compiled program, five of them interleaved, and two of Python
(`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.38 to 0.49 s |
| Rust (`rustc -O`) | 0.45 to 0.60 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.49 to 0.63 s |
| Go | 0.75 to 0.83 s |
| Python | 9.1 to 9.8 s |
| Kāra (`karac build --mir`) | 0.55 to 0.69 s |
| Kāra, legacy (`karac build`) | 0.48 to 0.61 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the legacy `karac build` builds the same file, and
its row is above. That edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 2.3 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

So the v2 build is about 1.15 times legacy here, a little behind Rust,
behind C, and ahead of Go. The comparison with C and Rust waits until
after M4.

## Compiler findings

None. `karac check` passed all four arms, the harness, the differential
and the bench program as first written.
