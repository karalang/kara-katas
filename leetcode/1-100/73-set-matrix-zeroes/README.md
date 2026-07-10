# 73. Set Matrix Zeroes

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array · Hash Table · Matrix &nbsp;·&nbsp; **Source:** [leetcode.com/problems/set-matrix-zeroes](https://leetcode.com/problems/set-matrix-zeroes/)

Given an `m × n` matrix, if any cell is `0`, set that cell's **entire row and column** to `0` — **in place**.

```
[[1,1,1],       [[1,0,1],
 [1,0,1],   ->   [0,0,0],
 [1,1,1]]        [1,0,1]]

[[0,1,2,0],      [[0,0,0,0],
 [3,4,5,2],  ->   [0,4,5,0],
 [1,3,1,5]]       [0,3,1,0]]
```

**Constraints:** `1 ≤ m, n ≤ 200`; `-2³¹ ≤ matrix[i][j] < 2³¹`. **Follow-up:** the O(m·n)-space scratch-copy is trivial and the O(m+n)-space flag arrays are easy — can you do it with **O(1)** extra space?

## Approaches

| Approach | Extra space | Kāra | Python |
|---|---|---|---|
| **First row/col as markers** ★ — reuse row 0 and column 0 as the zero-flag storage | O(1) | [`set_matrix_zeroes.kara`](set_matrix_zeroes.kara) ✓ via `karac run` / `karac build` | [`set_matrix_zeroes.py`](set_matrix_zeroes.py) ✓ |
| **Row/column flag arrays** — two `Vec[bool]`, mark then apply | O(m+n) | [`set_matrix_zeroes_markers.kara`](set_matrix_zeroes_markers.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output across all ten test cases, under default (auto-par on) and `KARAC_AUTO_PAR=0` builds alike, and both approaches agree with each other and with the Python mirror.

## The trick — the matrix stores its own markers

The naïve fix needs a second matrix (O(m·n)) or two flag arrays (O(m+n)). The O(1) follow-up folds the marker storage **into the matrix itself**: row 0 and column 0 remember which columns/rows must be zeroed.

```
1. record separately whether row 0 / column 0 each ALREADY hold a zero   (two bools)
2. for every interior zero m[i][j]==0 (i≥1, j≥1): stamp m[i][0]=0 and m[0][j]=0
3. second interior pass: zero m[i][j] whenever its marker m[i][0] or m[0][j] is 0
4. finally zero row 0 / column 0 themselves iff the step-1 bools said so
```

The ordering is the whole subtlety. Steps 2 and 3 **must** be separate passes — a marker written in step 2 must not be misread as "this cell was originally zero" by a later cell in the same pass. And row 0 / column 0 are handled **dead last** (step 4), because while they serve as marker scratch their own data role must not be committed early. Step 1 has to run *before* step 2 overwrites those cells, which is why the two "did row0/col0 start with a zero" bits are captured up front.

**First row/col markers** ([`set_matrix_zeroes.kara`](set_matrix_zeroes.kara)) is the ★ — O(1) extra space, the full four-step dance above.

**Row/column flag arrays** ([`set_matrix_zeroes_markers.kara`](set_matrix_zeroes_markers.kara)) is the readable O(m+n) cross-check: two `Vec[bool]`, `row_zero` and `col_zero`; pass 1 marks, pass 2 applies. No marker/data-role collision (the flags live outside the matrix), so no ordering care beyond "mark before apply". It agrees with the ★ on every case.

This is the in-place-matrix-mutation cousin of kata [#48](../48-rotate-image/)'s ring rotation — the same `mut ref Vec[Vec[i64]]` nested index-write, here driven by a marker sweep rather than a cyclic four-way swap.

## Kāra features exercised

- **`mut ref Vec[Vec[i64]]` nested index-write** — `set_zeroes(m: mut ref Vec[Vec[i64]])` reads and writes `m[i][j]` across four passes; the in-place matrix-mutation idiom shared with kata [#48](../48-rotate-image/).
- **`let row = m[i]` on a borrowed matrix** — `print_grid`/`hash_grid` bind a row out of a `ref Vec[Vec[i64]]` then read it by `row.len()` / `row[j]`, the borrowed-nested-collection row binding kata [#48](../48-rotate-image/) exercised (B-2026-06-29-2).
- **`Vec[bool]` flag arrays** — the markers variant seeds two `Vec[bool]` with `Vec.new()`/`push(false)`, then `row_zero[i] = true` / reads `row_zero[i] or col_zero[j]`; boolean vectors as first-class storage.
- **`or` short-circuit in a hot condition** — `if m[i][0i64] == 0i64 or m[0i64][j] == 0i64` (Kāra spells it `or`, not `||`); the apply-pass predicate.
- **Matrix literals with varied shapes** — `[[1,1,1],[1,0,1],[1,1,1]]`, `[[0]]`, `[[5,0,9,3]]` (1×4), `[[5],[0],[9],[3]]` (4×1) — the `Vec[Vec[i64]]` literal driving 1×1, single-row, single-column and marker-role edge cases.

**v1 note.** Values are compared only against `0` and folded into a rolling hash; the harness uses non-negative values so the fold stays cross-language-identical. Both solvers verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — the nested `Vec[Vec[i64]]` marker sweep lowers consistently across all engines.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   set_matrix_zeroes.kara
karac build set_matrix_zeroes.kara && ./set_matrix_zeroes

# The O(m+n) flag-array approach (identical output):
karac run set_matrix_zeroes_markers.kara

# Python
python3 set_matrix_zeroes.py

# Verify they all agree
diff <(karac run set_matrix_zeroes.kara) <(python3 set_matrix_zeroes.py)                 && echo OK
diff <(karac run set_matrix_zeroes.kara) <(karac run set_matrix_zeroes_markers.kara)     && echo OK
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`set_matrix_zeroes.{kara,rs,c,py}`, `go-seq/main.go`).

> ✅ **M5-confirmed (2026-07-10).** Re-measured on the corpus's **Apple M5 Pro reference machine** (arm64, 6P+12E; clang 21 / rustc 1.95 / go 1.26; karac from current `main`), replacing the earlier x86-64 cloud-container snapshot. **Kāra is the fastest of the four on the M5 too** — in wall-clock *and* total CPU work. The also-rans reorder with the hardware (this workload is allocation/`realloc`-bound, so their order tracks the platform's allocator + GC, not the marker sweep): Go rises from slowest on the container to 2nd on the M5 as its concurrent GC overlaps on fast cores, while C's `realloc`-of-`realloc` becomes the slowest. `bench/results.json` records the M5 host.

**Workload.** The O(1)-space first-row/col marker algorithm (the ★), run **K = 100,000** times over a freshly built **20×20** matrix — each iteration fills the matrix with non-zero values, punches **three** zeros at `k`-dependent positions (so three rows + three columns get zeroed and the rest survive, keeping the result non-degenerate), runs `set_zeroes` in place, and folds the surviving grid into a rolling hash `acc = (acc*131 + v) % 1_000_000_007`. All five mirrors must agree on `222485272` before timing.

### A benchmark-fairness note (this is the headline)

The kata builds the matrix as a **`Vec[Vec[i64]]`** with **`Vec.new()` + `push`** — a *growing* dynamic array of *growing* rows. So every mirror here builds it the same way — Rust `Vec<Vec<i64>>::push`, Go `[][]int64` `append`, C a `realloc`-doubling vector of `realloc`-doubling rows, Python list-of-lists `append` — **not** a fixed 2-D array, which would be an apples-to-oranges heap-vs-stack comparison (the [#72](../72-edit-distance/) lesson). At **equal data-structure semantics**:

`--warmup 5 --runs 30 --shell=none`. **M5 Pro numbers.** kāra/Rust/C are strictly single-threaded (99.7 % CPU); Go's runtime uses ~1.18 cores (118 % CPU) for concurrent GC — but here kāra leads it on both wall-clock and user-CPU, so the GC overlap doesn't change the ranking.

| Implementation | Wall time | User-CPU | CPU % | Matrix storage |
|---|---|---|---|---|
| **kāra set_matrix_zeroes**            | **222.7 ± 1.7 ms** | **220.9 ms** | 99.6 % | `Vec.new()+push` (grows) |
| go   set_matrix_zeroes                | 361.7 ± 2.6 ms | 387.2 ms | 118 % | `append` (grows) |
| rust set_matrix_zeroes (rustc -O)     | 415.4 ± 13.5 ms | 413.1 ms | 99.7 % | `Vec::push` (grows) |
| c    set_matrix_zeroes (clang -O3)    | 499.1 ± 20.3 ms | 496.2 ms | 99.7 % | `realloc`-doubling |

**Kāra is the fastest of the four** when everyone builds the matrix the way the kata does — 1.62× ahead of Go's `append`, 1.87× ahead of Rust's `Vec::push`, and 2.24× ahead of C's `realloc`-grow, and it leads on *total CPU work* too (Go is the only mirror to exceed one core, ~1.18× via concurrent GC, but its 387 ms user-time is still well behind kāra's 221 ms). This is the same inversion [#72](../72-edit-distance/) documented: kāra's growing-`Vec` codegen + allocator path is *efficient*, and a naïve fixed-2-D-array mirror would understate kāra by comparing its heap `Vec` against native stack storage. It's the counterpart to the equal-*safety* row in [#69](../69-sqrtx/) and the equal-*memory-semantics* row in [#98](../98-validate-binary-search-tree/) — the honest cross-language number requires matching the **data-structure discipline**, not just the algorithm.

**Single-threaded, honestly.** The loop-carried hash is not a reduction karac's auto-par pass can split — `karac build --concurrency-report` reports `<no parallelization opportunities detected>`, so the default `karac build` stays serial (kāra runs at 99.6 % CPU, `User ≈ wall`). So this is a fair seq-vs-seq comparison against `rustc -O` / `clang -O3` / `go build`, not auto-par vs single-core.

One honest qualifier: this is **allocation/`realloc`-dominated** — all four spend most of their time building and freeing the 20×20 `Vec`-of-`Vec` each iteration, so it measures growing-dynamic-array throughput as much as the marker sweep itself. A fixed 2-D-array discipline would be faster for everyone, but is a *different* data structure than the kata's `Vec[Vec[i64]]`.

### Runtime — Python

| Run | Mean ± σ |
|---|---|
| `py set_matrix_zeroes` (same K=100k) | 3871 ± 20 ms |

Python runs the **same** K=100,000 and agrees on the sink, so it is cross-checked (not scaled down). At ~3.9 s it is **~17× slower than kāra seq** — the gap the compiled path buys on this allocation- and index-heavy workload.

### Compile elapsed (cold)

| Compiler | Time |
|---|---|
| clang -O3 set_matrix_zeroes.c          | **88.6 ms** |
| **karac build set_matrix_zeroes.kara** | **90.1 ms** |
| rustc -O set_matrix_zeroes.rs          | 106.4 ms |

On the M5 karac compiles at ~1.02× clang — a near-tie — and **~1.18× faster than rustc** (90.1 vs 106.4 ms) for this file.

### Binary size

| Implementation | Size |
|---|---|
| c    set_matrix_zeroes                | 32.8 KiB |
| **kāra set_matrix_zeroes**            | **33.4 KiB** |
| rust set_matrix_zeroes                | 455.8 KiB |
| go   set_matrix_zeroes                | 2.38 MiB |

On the M5 the runtime's allocation/panic floor dead-strips away, so kāra's `Vec`-heavy binary is **33.4 KiB — within ~0.6 KiB of C's 32.8 KiB**, the same lean ~33 KiB floor as the other `Vec`-based katas ([#62](../62-unique-paths/)–[#66](../66-plus-one/), [#72](../72-edit-distance/)) — far below Rust's 455.8 KiB and Go's 2.38 MiB. (A ~10× drop from the container's 324.5 KiB, which linked an unstripped floor.)

### Runtime memory (peak)

| Implementation | Peak |
|---|---|
| **kāra set_matrix_zeroes**            | **1.09 MiB** |
| rust set_matrix_zeroes                | 1.16 MiB |
| c    set_matrix_zeroes                | 1.19 MiB |
| go   set_matrix_zeroes                | 9.53 MiB |

Kāra/Rust/C sit within ~0.1 MiB of each other (each matrix allocated and freed inside the loop — flat steady state, no leak across 100,000 iterations), kāra the leanest; Go's 9.53 MiB reflects its GC arena churning the `append`-grown slices. (Absolute figures differ from the container's because macOS `time -l` "peak memory footprint" accounts differently than Linux max-RSS — compare within a host.)

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 set_matrix_zeroes.c          | **2.5 MiB** |
| **karac build set_matrix_zeroes.kara** | **21.0 MiB** |
| rustc -O set_matrix_zeroes.rs          | 29.9 MiB |

On the M5 karac's compile-memory footprint sits between clang (lowest) and rustc — under rustc's 29.9 MiB.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — and here, with both building the matrix via a growing `Vec`, **kāra leads Rust 1.87×** (and C 2.24×, Go 1.62×). C calibrates the `realloc` floor, Go is the GC/`append` data point (and the multicore-GC case — 118 % CPU, yet still behind kāra), Python the ergonomic foil. The load-bearing facts: the five-language sink agreement, that kāra is the *fastest* of the four — in wall-clock and total CPU work — at equal growing-`Vec` semantics, and — as [#72](../72-edit-distance/) first showed — that comparing kāra's heap `Vec[Vec]` against a native fixed 2-D array would understate it.
