# 329. Longest Increasing Path in a Matrix

Given an `m x n` integer matrix, return the length of the longest strictly
increasing path. From each cell you may move up, down, left or right, never
diagonally and never outside the matrix.

```
[[9, 9, 4], [6, 6, 8], [2, 1, 1]]  ->  4     (1, 2, 6, 9)
[[3, 4, 5], [3, 2, 6], [2, 2, 1]]  ->  4     (3, 4, 5, 6)
[[1]]                              ->  1
```

## Approaches

Point an edge from every cell to each strictly larger neighbour. "Strictly
larger" cannot cycle, so the cells form a directed acyclic graph and the
answer is its longest path, counted in cells. The three arms find that path
three ways.

| file | mechanism | cost |
|---|---|---|
| `longest_increasing_path.kara` ★ | depth-first search from every cell; a memo keeps each cell's answer, so each cell is searched once | `O(mn)` time, `O(mn)` space and recursion |
| `longest_increasing_path_topo.kara` | Kahn's algorithm: peel the cells with no larger neighbour, layer by layer; the number of layers is the answer | `O(mn)` time, `O(mn)` space, no recursion |
| `longest_increasing_path_sorted.kara` | sort the cells by value, largest first, and fill each cell's answer from its larger neighbours, which are already final | `O(mn log mn)` time, `O(mn)` space |
| `differential.kara` | the three arms and a memo-free search on 607 grids, seven properties | — |
| `bench/longest_increasing_path.kara` | 20 re-solves of a 500 x 500 grid by the ★ arm | — |

Every arm prints the same 16 lines: the three examples, five edge cases (a
row, a column, all equal, a 3 x 3 snake and the 64-bit extremes), a 100 x 100
snake whose path visits every cell, three small random grids, and four
larger random grids up to 300 x 200. The three arms' output is
byte-identical, and `longest_increasing_path.py` mirrors the ★ arm.

## Why ties need no care

Equal neighbours are never consecutive on a strictly increasing path, so no
arm has to order them. The sorted arm can take a run of equal values in any
order, because none of them reads another's answer; the layer-peeling arm
counts only strictly larger neighbours, so equal ones never hold a cell back.
Mutants M7 and M12 below change exactly these choices and survive.

The snake case is there for depth: its one path runs through all 10,000
cells, so the ★ arm recurses 10,000 deep and the layer-peeling arm makes
10,000 layers of one cell each.

## Differential

`differential.kara` runs the three arms and `brute`, the same search without
a memo, on seven hand-picked grids and 600 pseudo-random grids of 1 to 6 rows
and columns with values in `[0, k)` for `k` from 1 to 9, so most grids have
ties and several local maxima.

| | property |
|---|---|
| P1 | all four answers agree |
| P2 | `1 <= answer <= rows * cols` |
| P3 | transposing the grid keeps the answer |
| P4 | mirroring every row keeps the answer |
| P5 | negating every value keeps the answer (each path runs backwards) |
| P6 | adding a constant to every value keeps the answer |
| P7 | the memo yields a witness: a path of exactly that many cells, each adjacent to the last and strictly larger |

`rounds 607, cells 7353, failures 0`, and all properties hold, on every
surface.

## Mutation testing

Twelve edits to the copies inside `differential.kara`, each built and run.

| # | mutation | outcome | how |
|---|---|---|---|
| M1 | DFS: treat a memo of 0 as an answer (`>= 0` for `> 0`) | **killed** | P1, P2, P4, P5, P7, from `[[0]]` |
| M2 | DFS: step to neighbours that are not smaller (`>=` for `>`) | **killed** | stack overflow: equal neighbours recurse into each other forever |
| M3 | DFS: never store the answer in the memo | **killed** | P7 only, from `[[1], [2], [3]]` |
| M4 | DFS: count a cell as 0 instead of 1 | **killed** | P1, P2, P4, P5, P7, from `[[0]]` |
| M5 | layers: seed with cells that have one larger neighbour | **killed** | P1, P4, from `[[0]]` |
| M6 | layers: release equal neighbours too (`<=` for `<`) | **killed** | P1, P4, from the first example |
| M7 | layers: release a cell when its count reaches 0 or below (`<=` for `==`) | silent (equivalent) | — |
| M8 | sorted: smallest first | **killed** | P1, P5, from `[[1], [2], [3]]` |
| M9 | sorted: read a neighbour that is not larger (`>=` for `>`) | **killed** | P1, P5, from `[[5, 5, 5]]` |
| M10 | sorted: never take the bottom-right cell's answer | **killed** | P1, P5, from `[[0]]` |
| M11 | DFS: look only down and right | **killed** | P1, P4, P5, from the first example |
| M12 | sorted: break ties by cell index | silent (equivalent) | — |

M7 is equivalent because a cell's count of larger neighbours drops by one
for each of them, and each is peeled once, so it reaches 0 once and never
goes below. M12 is equivalent by the tie argument above.

M3 keeps every answer right and only throws the memo away, which makes the
search exponential. Only P7 notices, because the witness is rebuilt from the
memo's contents.

## Verification

All three arms plus the differential are byte-identical under `karac run`
(LLJIT), `karac run --interp`, `karac build` with `KARAC_AUTO_PAR=0`, and the
default auto-parallelising `karac build`. All four programs are
valgrind-clean at `-O0` with `KARAC_AUTO_PAR=0`. The auto-parallel build
reports one "possibly lost" record, 1,216 bytes in 4 blocks: the thread-local
storage of the worker pool's threads, allocated by `pthread_create` and still
held at exit. The three arms' output is byte-identical to
`longest_increasing_path.py`.

The benchmark kernel's sink matches all four language twins and Python
(`sink 354060968`).

## Benchmarks

`bench/longest_increasing_path.kara` and its four mirrors time the ★ arm as
written. A 500 x 500 grid of values in `[0, 999]` is built once. Each of 20
punches replaces the value of one random cell and solves the whole grid
again with a fresh memo. The sink is a rolling hash of each answer and the
punched cell. Every twin walks the four neighbours by looping over a literal
of four direction pairs, and recurses rather than keeping its own stack.

> **Host:** only the x86-64 Linux cloud container lane exists so far, in
> [`bench/results.container-x86.json`](bench/results.container-x86.json). The
> canonical Apple M5 Pro lane (`bench/results.json`) is not measured yet, and
> `bench-lib.sh` refuses to write it from Linux. Absolute milliseconds are NOT
> comparable between hosts. Only the **within-file cross-language ratios** are.

30 runs each, on a 4-core x86-64 Linux container, karac built from `main`
at `f4b946e17` with the fixes for B-2026-10-02-70 and -71 applied, measured
2026-10-02. Python is its own lane.

| implementation | mean | vs fastest |
|---|---|---|
| c `-march=x86-64-v3` (matched-ISA) | 129.2 ms ± 3.6 | 1.00× |
| c `clang -O3` | 135.5 ms ± 8.7 | 1.05× |
| rust `-C target-cpu=x86-64-v3` + overflow-checks (matched) | 165.0 ms ± 5.8 | 1.28× |
| rust `-O` | 167.2 ms ± 15.5 | 1.29× |
| rust `-O -C overflow-checks=on` (equal-safety) | 169.4 ms ± 11.2 | 1.31× |
| **kāra `karac build`** | **190.5 ms ± 10.9** | **1.47×** |
| go `go build` | 250.2 ms ± 9.2 | 1.94× |
| python 3 | 3750 ms ± 59 | 29.0× |

**Kāra is 12% behind equal-safety Rust and 41% behind C.** Before
B-2026-10-02-70 it was 279 ms, 1.65x Rust: the neighbour loop's literal was
built as a heap `Vec` on every call, 5,000,000 allocations over the run. With
that gone the program makes 10,677 allocations, about what the grid and the
memos need. Where the remaining gap to Rust sits has not been measured.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 99.5 ms ± 3.0 | 15.9 KiB | 5.1 MiB |
| rust | 194.0 ms ± 5.6 | 3865.9 KiB | 5.7 MiB |
| kāra | 394.2 ms ± 13.9 | 341.6 KiB | 6.1 MiB |
| go | — | 2179.6 KiB | 10.8 MiB |
| python | — | — | 17.4 MiB |

`karac build` is 4× clang's cold compile and 2× rustc's. Kāra's binary is
21× clang's and 11× smaller than rustc's. Raw numbers are in
`bench/results.container-x86.json`. Methodology and caveats are in
[`BENCHMARKS.md`](../../../BENCHMARKS.md).

## Compiler findings

**No wrong answers.** Every program was byte-identical on every surface from
the first run. Three slowdowns, all fixed:

- **B-2026-10-02-61 (perf, medium, fixed in `2025d6e66`): `--interp`
  re-derived static analyses on every block entry and call.** Each time a
  block was entered the interpreter recomputed which statement last uses each
  of its bindings, and each call re-walked the callee's whole body for one
  ownership question. Both are properties of the source alone. A profile of
  the ★ arm's search on a 40 x 40 grid put 40% of its instructions there. Both
  are now computed once a run, and the ★ arm takes 15.6 s under `--interp`
  instead of 28.9 s.
- **B-2026-10-02-70 (perf, medium, fixed in `b50bfacd3`): `karac build`
  heap-allocated a loop's literal on every execution.** A bracketed literal is
  a `Vec`, so `for (dr, dc) in [(-1, 0), (1, 0), (0, -1), (0, 1)]` built and
  freed a four-element heap buffer on every call of the search: 5,000,000
  allocations over the benchmark. A literal of plain scalars that only a loop
  consumes now goes into a stack array, as the same literal bound to an
  `Array` local always did, and the benchmark takes 191 ms instead of 279 ms.
- **B-2026-10-02-71 (perf, medium, fixed in `c8e87b65d`): `--interp` closures
  captured every function in the program.** A closure's captured environment
  was a copy of every scope, the global one included, and each call copied it
  into the closure's frame. A `sort_by` comparator therefore cost a copy of
  every function's parameters and defaults per comparison, and the sorted arm
  took 174 s under `--interp`. Closures now capture local scopes only and
  reach the globals through the ordinary lookup, and the arm takes 11.7 s.

The ★ arm still takes 15.6 s under `--interp` against 0.4 s under the JIT.
The profile's next hot spots are ownership questions asked through the
drop-schedule audit path, which belong to that work and are noted in
B-2026-10-02-61.

`karac check` flagged a `mut` marker on an argument that was already `mut
ref`, once in the ★ arm's harness and seven times in the differential (E0219),
and `karac fix` removed them. That says little about the diagnostics: the
author already knows the language, which is why authoring like this never
counts toward the machine-fix rate.
