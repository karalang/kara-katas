# 407. Trapping Rain Water II

Given an `m x n` grid of cell heights, return how much rain water the
grid can hold. Water over a cell stays only if it cannot run off the
edge of the grid.

```
heightMap = [[1,4,3,1,3,2],
             [3,2,1,3,2,4],
             [2,3,3,2,3,1]]  -> 4
```

**Constraints:** `1 <= m, n <= 200`; `0 <= heightMap[i][j] <= 2 * 10^4`.

## Approaches

| file | mechanism | time | space |
|---|---|---|---|
| `trapping_rain_water_ii.kara` ★ | a min-heap walking in from the border: every border cell starts in a `PriorityQueue` keyed by height; the lowest comes out, its key is the water level around it, and each unvisited neighbour below that level holds the difference and joins at the higher of the two | O(mn log(mn)) | O(mn) |
| `trapping_rain_water_ii_sorted.kara` | the same walk with a `SortedSet` of (level, row, column) as the priority queue, taking its `min` and removing it | O(mn log(mn)) | O(mn) |
| `trapping_rain_water_ii_relax.kara` | water levels relaxed to a fixed point: inner cells start at the tallest height and each sweep lowers a cell to the higher of its own height and its lowest neighbour's level, as in Bellman-Ford, until nothing changes | O((mn)^2) worst case | O(mn) |
| `trapping_rain_water_ii_layers.kara` | one flood per layer of water: between consecutive distinct heights `a < b`, a cell no higher than `a` holds `b - a` unless a path of cells below `b` drains it to the border, found by a flood fill from the border | O(H mn) for H distinct heights | O(mn) |
| `differential.kara` | the four arms on 2,000 random cases whose answers are known by construction, five properties | — | — |

Every arm prints the same 10 lines: the two LeetCode examples, seven
edge cases (one cell, one row, a 2 x 2 grid, a pit, a wall with a low
cell in it, a rim with one low cell, two basins at different levels),
and for 1,000 random grids of 1 to 12 rows and columns with heights from
0 to 9, the total water and a checksum. `trapping_rain_water_ii.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms. Each of 2,000 random
cases builds grids whose answers are known without solving them:

| | property |
|---|---|
| P1 | a bowl, a border all of height `H` around cells below `H`, holds the sum of `H - h` over its inner cells |
| P2 | a grid of fewer than 3 rows or columns holds nothing |
| P3 | raising every cell by the same amount changes nothing |
| P4 | the grid transposed holds the same water |
| P5 | raising one border cell never lowers the water |

It prints `2000 cases, 4 arms, 40000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, each run under `karac __mir-run`.
All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | heap: a neighbour joins the heap at its own height, not the water level | P1 1967, P4 32 |
| M2 | heap: the heap pops the highest cell first | P4 86, P5 1 |
| M3 | sorted: only three directions are walked | P4 1055 |
| M4 | sorted: border cells are not marked as seen | P5 239 |
| M5 | relax: inner cells start at 0 instead of the tallest height | P1 2000, P3 1282 |
| M6 | relax: the right neighbour is left out of the lowest level | P4 1055 |
| M7 | layers: the flood drains through cells as high as the layer | P5 4 |
| M8 | layers: a trapped cell holds 1 per layer, not its depth | P1 1224, P5 12 |

Only P1 knows an answer outright; the other four relate an arm's
answers to each other, so a mutant that is wrong the same way on every
grid can pass them. M2 and M7 are killed narrowly. Popping the highest
cell first still fills a bowl correctly, because every inner cell of a
bowl takes the border's level whatever the order; M7 lets water drain
through a cell exactly as high as the layer, which changes the answer
only on the rare grids where such a cell is the only way out. M3 and
M6 both lose a direction and fail the same checks: transposing the grid
turns the missing direction into a different one.

## Verification

All four arms print the same output as `trapping_rain_water_ii.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file. The differential prints
`40000 checks, 0 failures` under `karac __mir-run` and
`karac __mir-llvm-run`. The heap, relaxation and layers arms also match
under `karac run --interp`.

The arms run under `karac __mir-llvm-run` since compiler commit
62f5f6de04 added the `String.as_str` native: the harness's
`show(name: Str, ...)` is passed string literals, which the MIR types
as `String` and converts with `String.as_str`. The frozen legacy
backends refuse the rest. Its typechecker refuses
`*t` on `SortedSet.min`'s result in the sorted arm and the differential;
its codegen passes a literal where `show` takes a `Str` with the wrong
layout (LLVM module verification fails), and has no chained indexed
receiver such as `level[r - 1][c].min(...)` in the relaxation arm, which
it reports as deferred. None of these is filed.

## Benchmarks

The bench program uses the ★ arm on 60 random 200 x 200 grids (the
problem's limit) with heights from 0 to 19,999, built from an LCG, and
folds the water into a total and a checksum. Every implementation
prints `60 grids of 200 x 200: 7627607015 units of water, checksum
593333912`; a 2-grid cut of the Kāra program under `karac __mir-run`
prints the same as the C program cut the same way. C has no heap type,
so its mirror carries a binary min-heap ordered as the tuples are in
the other mirrors; Rust uses `BinaryHeap` with `Reverse`, Go
`container/heap` and Python `heapq`.

### Apple M5 Pro, 2026-11-07

30 runs each, 5 warmups, on the Apple M5 Pro, karac `0.8.0-dev.14781+g3dc7786b7`
(g3dc7786b7, the v2/MIR backend), measured 2026-11-07, with the Kāra binary built
`KARAC_AUTO_PAR=0`. This is the kata's first M5 measurement; Python was not run.
The last column is Kāra's mean over that row's mean.

| implementation | mean | Kāra / this |
|---|---|---|
| rust `-O` | 154.1 ms ± 3.5 | 1.36× |
| rust `-O -C overflow-checks=on` (equal-safety) | 162.2 ms ± 2.8 | 1.29× |
| c `clang -O3` | 165.9 ms ± 2.9 | 1.26× |
| **kāra `karac build`, seq** | **209.9 ms ± 2.0** | **—** |
| go `go build` | 366.3 ms ± 5.5 | 0.57× |

Kāra is 1.36× `rustc -O`, 1.29× equal-safety Rust, 1.26× C and 0.57× Go. The 1.29× gap to equal-safety Rust matches the legacy build's 1.5× on the container; it was not investigated. Against the legacy backend (exact counts, dd86e3955, `KARAC_AUTO_PAR=0`) Kāra executes 0.72× the instructions in 0.71× the cycles.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 60.5 ms ± 1.0 | 32.9 KiB | 1.8 MiB |
| rust | 131.6 ms ± 2.1 | 455.8 KiB | 2.2 MiB |
| kāra | 163.6 ms ± 3.9 | 67.0 KiB | 2.0 MiB |
| go | — | 2451.5 KiB | 9.2 MiB |

`karac build` is 2.7× clang's cold compile and 1.2× rustc's. Kāra's
68,568-byte binary is 2.0× clang's and 6.8× smaller than rustc's. Raw numbers are in
[`bench/results.json`](bench/results.json). The sink matches across the Kāra,
Rust, C and Go builds (`60 grids of 200 x 200: 7627607015 units of water, checksum 593333912`).

### Container x86-64 history

Spot timings on a shared 4-core
container (`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| Rust (`rustc -O -C overflow-checks=on`) | 0.35 s |
| Rust (`rustc -O`) | 0.36 s |
| C (`clang -O3`) | 0.39 s |
| Kāra (legacy `karac build`) | 0.54 s |
| Go | 1.0 s |
| Python | 4.5 s |

The Kāra program also prints the same line under `karac __mir-llvm-run`
in 2.0 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark. The `karac build` time is the frozen
legacy backend.

## Compiler findings

No new findings.
