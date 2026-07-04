# 59. Spiral Matrix II

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array, Matrix, Simulation &nbsp;·&nbsp; **Source:** [leetcode.com/problems/spiral-matrix-ii](https://leetcode.com/problems/spiral-matrix-ii/)

Given a positive integer `n`, generate an `n × n` matrix filled with the numbers `1 … n²` in clockwise spiral order.

```
n = 1  →  [[1]]
n = 2  →  [[1, 2],
           [4, 3]]
n = 3  →  [[1, 2, 3],
           [8, 9, 4],
           [7, 6, 5]]
```

**Constraints:** `1 ≤ n ≤ 20` (so `n² ≤ 400`, well inside i64).

This is the **inverse of [kata #54](../54-spiral-matrix/)**: #54 *reads* an existing matrix in spiral order, this one *writes* `1…n²` along the same traversal.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| **Boundary shrinking** — fill top/right/bottom/left edges of each ring, then shrink the four bounds inward | O(n²) time, O(n²) grid | [`spiral_matrix_ii.kara`](spiral_matrix_ii.kara) ✓ via `karac run` / `karac build` | [`spiral_matrix_ii.py`](spiral_matrix_ii.py) ✓ |
| **Direction-vector simulation** — walk a turtle, turn right when the next cell is out of bounds or already filled | O(n²) time, O(n²) grid | [`spiral_matrix_ii_sim.kara`](spiral_matrix_ii_sim.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter and codegen produce identical output for `n = 1…5`, and both approaches agree with each other and with the Python mirror.

## Why two solvers?

**Boundary shrinking** ([`spiral_matrix_ii.kara`](spiral_matrix_ii.kara)) is the direct form: keep `top`, `bottom`, `left`, `right` and fill one ring per outer iteration — top row L→R, right column T→B, bottom row R→L, left column B→T — shrinking each bound as its edge is consumed. The two `if` guards (fill the bottom row only if `top <= bottom`, the left column only if `left <= right`) are the whole correctness subtlety: on an **odd** `n` the center cell is filled by the top-row sweep alone, and without the guards the bottom/left sweeps would re-walk it or run backwards over an empty span. This mirrors kata #54's reader ring-with-guards exactly — the write version has the same edge cases as the read version.

**Direction simulation** ([`spiral_matrix_ii_sim.kara`](spiral_matrix_ii_sim.kara)) drops the boundary bookkeeping: hold a position and a direction index into the clockwise cycle `right → down → left → up`, write the value, then peek one step ahead — if it would leave the grid *or* land on an already-filled (nonzero) cell, turn right before stepping. The already-filled test is what closes the spiral inward. The out-of-bounds checks are ordered **before** the `grid[nr][nc] != 0` read and joined with `or`, so short-circuit evaluation guarantees the grid is never indexed out of range — the same discipline as kata #28's `j < nn and h[i + j] == nee[j]`.

## Kāra features exercised

- **Mutable `Vec[Vec[i64]]` grid with nested index-store** — `grid[r][c] = v`, the read/write of an inner heap `Vec` element through an outer `Vec` index. This is the historically delicate path (borrow-elided read of `v[i]` on a `Vec[Vec]`, and index-store of a heap `Vec` element — B-2026-06-19-6/7); both write and read-back are exact here on `karac run`, `karac build`, and the default auto-par build.
- **Grid construction via `Vec.filled(n, 0i64)` per row** — `n` rows each a fresh zero-filled inner `Vec`, pushed into the outer `Vec` (each row is an independent allocation, not an aliased shared buffer — the 2D-fill aliasing bug B-2026-06-19-8 is fixed).
- **Nested index-read as a guard** (sim) — `grid[nr][nc] != 0i64` behind a short-circuiting `or` chain of bounds checks, so an out-of-range `(nr, nc)` never reaches the read.
- **Fixed-size `Array[i64, 4]` direction tables** (sim) — `let dr: Array[i64, 4] = [0, 1, 0, -1];` indexed by the direction cursor `dr[dir]`, with `dir = (dir + 1i64) % 4i64` wrapping the clockwise cycle.
- **`for row in g.iter()` + inner `for x in row.iter()`** — nested iteration over the `Vec[Vec[i64]]` to render each row, building the line with an f-string accumulator.

## Running

```bash
# Kāra — interpreter and codegen produce the same output today.
karac run   spiral_matrix_ii.kara
karac build spiral_matrix_ii.kara && ./spiral_matrix_ii

# The simulation approach (identical output):
karac run spiral_matrix_ii_sim.kara

# Python
python3 spiral_matrix_ii.py

# Verify they all agree
diff <(karac run spiral_matrix_ii.kara) <(python3 spiral_matrix_ii.py)             && echo OK
diff <(karac run spiral_matrix_ii.kara) <(karac run spiral_matrix_ii_sim.kara)     && echo OK

# Full cross-language benchmark (Kāra / Rust / C / Go / Python + auto-par lanes)
bench/bench.sh
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`spiral_matrix_ii.{kara,rs,c,py}`, `go-seq/main.go`, plus the par-lane `spiral_matrix_ii_par.c`, `go-par/`, `rayon/`).

**Workload.** M = 9 sizes `n = 12…20`, rotated by `idx = k % M`. K = 180,000 iterations; each generates the `n × n` spiral matrix with the boundary-shrinking solver — a fresh nested grid of `n` inner rows (`n + 1` allocations) — and folds a **position-weighted checksum** `Σ grid[i][j] · (i·n + j + 1)` over every cell into the running total. The sink across all K iters is **1,100,752,800,000**, checked against every mirror before timing.

Two design choices are load-bearing and worth stating, because both are traps a naive spiral benchmark falls into:

- **Rotating `n` (not a fixed size) defeats loop-invariant code motion.** With a fixed `n`, `generate_matrix(n)` is loop-invariant and the compiler can hoist the entire per-iteration computation out of the K loop, leaving the benchmark measuring an empty loop. Rotating `n` over 9 sizes forces real work every iteration (same role as kata 56/57's rotated cases).
- **The checksum reads *every* cell**, so no mirror can dead-code the off-diagonal writes — the elision that made kata 57's first C mirror 20× too fast. All `n²` cells are materialized and read.
- **The C/Rust/Go grids all use the nested-allocation shape** (`int64**` / `Vec<Vec<i64>>` / `[][]int64`, `n + 1` allocations), matching Kāra's `Vec[Vec[i64]]` — not a single flat buffer. This keeps the allocation cost apples-to-apples.

Two-lane kata (BENCH.md § Implicit auto-par): the `total = total + <checksum>` accumulator is the slice-1 allow-list reduction, so `karac build` may emit a `karac_par_reduce` dispatch by default. The bench builds two kara binaries — `KARAC_AUTO_PAR=0` (seq) and default (auto-par) — reported separately.

Snapshot — Apple M5 Pro (6P+12E), Darwin 25.5.0, 2026-07-04, hyperfine `--warmup 5 --runs 30 -N`. karac 0.1.0, rustc 1.95.0, Apple clang 21.0.0, go 1.26.3. All numbers from the committed [`results.json`](bench/results.json).

### Runtime — seq lane

| Implementation | Wall time |
|---|---|
| c    spiral_matrix_ii (clang -O3)     | **67.4 ± 2.0 ms** |
| rust spiral_matrix_ii                 | 78.2 ± 2.0 ms |
| go   spiral_matrix_ii                 | 108.1 ± 2.8 ms |
| **kāra spiral_matrix_ii (seq)**       | **114.0 ± 2.4 ms** |

This kata is the corpus's **"where Kāra lags" data point** — the mirror image of [kata #57](../57-insert-interval/), where Kāra tied Rust on a flat-allocation sweep. Here **Kāra trails Rust by 1.46×** (114.0 vs 78.2) and C by 1.69×, heavier than the corpus norm. The difference is the workload shape: this one is dominated by **nested `Vec[Vec[i64]]` index access** — `grid[i][j]` is a double indirection (load the inner row's `{ptr,len,cap}`, then the element), and it happens `n²` times in the checksum fold *plus* on every store in the generator. The likely gap (a **hypothesis**, not yet profiled) is that Kāra re-derives the inner-row pointer and re-checks bounds on each `[i][j]` where Rust hoists the inner slice out of the `j` loop and elides the bounds checks LLVM can prove in-range. That makes nested-index-heavy code a concrete codegen-optimization target — the honest counterweight to #57's tie. C leads Rust by only 1.16×, both paying real nested-pointer chases.

### Runtime — auto-par regime

The `total = total + <checksum>` reduction is auto-par-eligible:

| Implementation | Wall time | User-CPU |
|---|---|---|
| rust spiral_matrix_ii (rayon par_iter) | **12.8 ± 0.7 ms** | 181 ms |
| c    spiral_matrix_ii (pthreads) | 14.5 ± 0.8 ms | 175 ms |
| **kāra spiral_matrix_ii (auto-par default)** | **20.5 ± 1.3 ms** | 274 ms |
| go   spiral_matrix_ii (goroutines) | 112.2 ± 2.0 ms | 295 ms |

Kāra's auto-par binary is **5.6× faster than its own seq binary** (114.0 → 20.5 ms) — much better parallel scaling than #57's 2.6×, because each iteration here does far more work (generate + fold an `n²` matrix) to amortize the dispatch overhead. It still trails rayon by 1.60×, carrying forward the seq-lane nested-index gap into each worker. Go's goroutine version is *no faster than its seq* (108 → 112 ms): the per-iter `[][]int64` allocation churn serializes on the GC/allocator across goroutines, exactly the contention the manual-free mirrors avoid.

### Runtime — Python

| Run | Mean ± σ |
|---|---|
| `py spiral_matrix_ii` (K=18k) | 240.5 ± 0.6 ms |

Python at K=18k is 240 ms; projecting to K=180k (~2.4 s) puts it **~21× slower than kāra seq**. Heavier multiple than the interval katas because the whole workload is nested list indexing in interpreter code, with no C-implemented `sorted()` to hide behind.

### Compile elapsed (cold)

| Compiler | Time |
|---|---|
| clang -O3 spiral_matrix_ii.c          | **53.6 ± 0.9 ms** |
| **karac build spiral_matrix_ii.kara** | **93.1 ± 1.1 ms** |
| rustc -O spiral_matrix_ii.rs          | 114.9 ± 0.9 ms |

Kāra compiles **1.23× faster than `rustc -O`** and sits at 1.74× of clang -O3 — same shape as the rest of the corpus.

### Binary size

| Implementation | Size |
|---|---|
| c    spiral_matrix_ii (seq)           | 32.8 KiB |
| **kāra spiral_matrix_ii (seq)**       | **33.4 KiB** |
| **kāra spiral_matrix_ii (auto-par)**  | **312.2 KiB** |
| rust spiral_matrix_ii (seq)           | 455.4 KiB |
| go   spiral_matrix_ii (seq)           | 2434.1 KiB |

Kāra seq sits within 0.6 KiB of C's no-frills floor — no sort, no runtime fallback to drag in. The auto-par binary's +279 KiB is the par-scheduler runtime.

### Runtime memory (peak)

| Implementation | Peak |
|---|---|
| c    spiral_matrix_ii (seq)           | 1.1 MiB |
| **kāra spiral_matrix_ii (seq)**       | **1.1 MiB** |
| rust spiral_matrix_ii (seq)           | 1.2 MiB |
| **kāra spiral_matrix_ii (auto-par)**  | **3.5 MiB** |
| go   spiral_matrix_ii (seq)           | 9.4 MiB |

Kāra seq's peak RSS is byte-identical to C's (1,196,344 B) — each matrix is allocated and freed inside the iteration, so steady state is flat across K. The auto-par 3.5 MiB is the worker pool's per-thread scratch (each thread holds a live matrix); Go's 9.4 MiB seq / 19.8 MiB par is its GC arena.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 spiral_matrix_ii.c          | 2.6 MiB |
| **karac build spiral_matrix_ii.kara** | **21.0 MiB** |
| rustc -O spiral_matrix_ii.rs          | 31.8 MiB |

Kāra's compile-memory footprint is ~8× clang's and ~1.5× lower than rustc's — same shape as the rest of the corpus.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap. On this kata that ratio is **1.46× (seq) / 1.60× (auto-par) in Rust's favor** — and that's the point of keeping it: unlike the flat-allocation katas where Kāra ties Rust, this nested-`Vec[Vec]` index-heavy workload exposes a standing codegen gap (inner-row pointer hoisting + bounds-check elision on `grid[i][j]`), a concrete optimization target rather than a headline win. C calibrates the LLVM floor, Go is the cross-runtime data point (and here shows GC-allocation contention defeating its own goroutine parallelism), Python is the ergonomic foil.
