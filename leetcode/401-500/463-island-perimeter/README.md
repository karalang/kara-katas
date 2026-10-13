# 463. Island Perimeter

You are given a `row x col` `grid` representing a map where
`grid[i][j] = 1` represents land and `grid[i][j] = 0` represents water.
Grid cells are connected horizontally and vertically (not diagonally).
The grid is completely surrounded by water, and there is exactly one
island (one or more connected land cells). The island doesn't have
"lakes", meaning the water inside isn't connected to the water around
the island. One cell is a square with side length 1. Determine the
perimeter of the island.

```
grid = [[0,1,0,0],[1,1,1,0],[0,1,0,0],[1,1,0,0]]  ->  16
grid = [[1]]                                      ->  4
grid = [[1,0]]                                    ->  4
```

**Constraints:** `1 <= row, col <= 100`; `grid[i][j]` is `0` or `1`;
there is exactly one island.

## Approaches

Every arm is `fn island_perimeter(grid: Vec[Vec[i64]]) -> i64`, and
borrows the grid.

| file | mechanism |
|---|---|
| `island_perimeter.kara` ★ | four sides per land cell, less two per edge two land cells share; each shared edge is found once by looking only right and down. O(rows × cols) |
| `island_perimeter_sides.kara` | for every land cell, count the sides that face water or the edge of the grid. O(rows × cols) |
| `island_perimeter_walk.kara` | there is one island, so start at any land cell and visit it all depth first with a stack, counting every step that would leave the land. O(rows × cols) |
| `island_perimeter_crossings.kara` | read each row from outside the grid to outside it again and count the changes between water and land; columns the same way. O(rows × cols) |
| `differential.kara` | the four arms on 1,500 random islands, five properties |

Every arm prints the same 11 lines: the three LeetCode examples, a
full 3×3 square, one cell in the middle of the sea, a row, a column, a
U, a plus, a staircase, and for 300 random islands on seas of 1 to 40
by 1 to 40 the number of land cells, the total perimeter and a
checksum. A random island is a random walk of land, after which every
lake is filled in, so each one keeps the problem's promise.
`island_perimeter.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random islands, made the same way as the harness's.

| | property |
|---|---|
| P1 | on seas up to 6 by 6, the answer is brute force's: every unit edge of the grid, inside or on its border, with land on exactly one side |
| P2 | on seas up to 20 by 20, transposing, flipping upside down and mirroring keep the answer |
| P3 | blowing every cell up to a `k × k` block, `k` from 2 to 4, multiplies it by `k` |
| P4 | a border of 0 to 2 cells of water on each side keeps it |
| P5 | a solid `a × b` rectangle, `a` and `b` from 1 to 8, with 0 to 3 cells of water on each side, gives `2 (a + b)` |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: only edges shared sideways are counted | P1 873, P2 1202, P3 1500, P5 1307 |
| M2 | ★: a shared edge hides only one side | P1 1074, P3 1500, P5 1478 |
| M3 | sides: the edge of the grid counts as land | P1 1480, P4 1226, P5 1036 |
| M4 | sides: water cells count their land sides | P1 1463, P3 1497, P4 1481, P5 1494 |
| M5 | walk: the start cell is not marked seen | P1 1074, P2 809, P3 1500, P5 1478 |
| M6 | walk: water is walked like land | P1 1400, P4 1481, P5 1491 |
| M7 | crossings: the right edge of a row is not crossed | P1 917, P2 1323, P4 502, P5 362 |
| M8 | crossings: each column starts on land | P1 1320, P2 1461, P4 1393, P5 1466 |

P1, the only property with an independent answer, sees all eight. P2
sees the mutants that treat one direction differently from another
(M1, M7, M8) and M5, whose double count depends on which cell the walk
starts from. P3 cannot see a mutant whose wrong answer is also
multiplied by `k` when the grid is blown up, as M3, M6, M7 and M8's
are. P4 sees the mutants that treat the edge of
the grid as something other than water.

A first M3, which looked at the left side twice and the right side
never, was equivalent and was replaced: every row of land has as many
left ends as right ends.

## Verification

All four arms print the same output as `island_perimeter.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file. The differential prints
`30000 checks, 0 failures` on both. The four arms and the differential
also run clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak.

On the frozen legacy backends every arm and the differential match
under `karac run --interp`, LLJIT and `karac build` (also with
`KARAC_AUTO_PAR=1`). Legacy `karac build` warns that the harness moves
`grid` into its first call and uses it again, which under v2 is a
borrow. Legacy `karac build` rejects the bench program (see
Benchmarks). Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 2 islands once, each on a
1,000 × 1,000 sea, from a random walk of 998² steps inside a ring of
water, with its lakes filled in. Each of 200 rounds, for each island,
puts one land cell on top of a random cell of the island's topmost row
(which joins the island and closes off no water), takes the perimeter,
and takes the cell back. Every implementation keeps a grid as rows of
separately allocated rows, like `Vec[Vec[i64]]`, and prints
`200 rounds on 2 islands of 1000x1000: perimeter 3586000 in all,
checksum 802551197`, the Kāra program under `karac __mir-run`
included (in 103 s).

The legacy `karac build` rejects the bench program (it moves
`grids[g]` out of the index, where v2 borrows it), so `bench.sh` builds
the Kāra program with `karac build --mir`, the v2 compiled backend.
That edit is by hand, on top of the `scripts/new-bench.sh` output.

Spot timings on a shared 4-core container, three runs each (two for
Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.39 to 0.41 s |
| Rust (`rustc -O`) | 0.31 to 0.35 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.32 to 0.41 s |
| Go | 0.62 to 0.66 s |
| Python | 18.9 to 19.1 s |
| Kāra (`karac build --mir`) | 0.47 to 0.63 s |

Under `karac __mir-llvm-run` the program prints the same line in
2.6 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

## Compiler findings

No new findings.
