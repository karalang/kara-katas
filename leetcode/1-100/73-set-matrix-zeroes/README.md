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

> ⚠️ **Machine caveat.** Measured on a **shared x86-64 Linux cloud container** (Intel Xeon @ 2.80 GHz, 4 vCPU, Linux 6.18.5; karac from current `main`). These are container numbers only — this kata has **no M5 `results.json` yet**; it will be re-benched on the corpus's Apple M5 Pro and the canonical table added then. Don't compare absolute times/sizes/RSS against sibling katas' M5 tables; [`bench/results.container-x86.json`](bench/results.container-x86.json) records the real host.

**Workload.** The O(1)-space first-row/col marker algorithm (the ★), run **K = 100,000** times over a freshly built **20×20** matrix — each iteration fills the matrix with non-zero values, punches **three** zeros at `k`-dependent positions (so three rows + three columns get zeroed and the rest survive, keeping the result non-degenerate), runs `set_zeroes` in place, and folds the surviving grid into a rolling hash `acc = (acc*131 + v) % 1_000_000_007`. All five mirrors must agree on `222485272` before timing.

### A benchmark-fairness note (this is the headline)

The kata builds the matrix as a **`Vec[Vec[i64]]`** with **`Vec.new()` + `push`** — a *growing* dynamic array of *growing* rows. So every mirror here builds it the same way — Rust `Vec<Vec<i64>>::push`, Go `[][]int64` `append`, C a `realloc`-doubling vector of `realloc`-doubling rows, Python list-of-lists `append` — **not** a fixed 2-D array, which would be an apples-to-oranges heap-vs-stack comparison (the [#72](../72-edit-distance/) lesson). At **equal data-structure semantics**:

`--warmup 5 --runs 30 --shell=none`. All single-threaded. **Cloud-container numbers.**

| Implementation | Wall time | Matrix storage |
|---|---|---|
| **kāra set_matrix_zeroes**            | **450.1 ± 6.3 ms** | `Vec.new()+push` (grows) |
| c    set_matrix_zeroes (clang -O3)    | 716.3 ± 14.5 ms | `realloc`-doubling |
| rust set_matrix_zeroes (rustc -O)     | 805.6 ± 17.0 ms | `Vec::push` (grows) |
| go   set_matrix_zeroes                | 1053.3 ± 22.2 ms | `append` (grows) |

**Kāra is the fastest of the four** when everyone builds the matrix the way the kata does — ahead of C's `realloc`-grow (1.59×), Rust's `Vec::push` (1.79×), and Go's `append` (2.34×). This is the same inversion [#72](../72-edit-distance/) documented: kāra's growing-`Vec` codegen + allocator path is *efficient*, and a naïve fixed-2-D-array mirror would understate kāra by comparing its heap `Vec` against native stack storage. It's the counterpart to the equal-*safety* row in [#69](../69-sqrtx/) and the equal-*memory-semantics* row in [#98](../98-validate-binary-search-tree/) — the honest cross-language number requires matching the **data-structure discipline**, not just the algorithm.

**Single-threaded, honestly.** The loop-carried hash is not a reduction karac's auto-par pass can split, so the default `karac build` stays serial — verified equal to `KARAC_AUTO_PAR=0` (450 vs 467 ms, `User ≈ wall` on both). So this is a fair seq-vs-seq comparison against `rustc -O` / `clang -O3` / `go build`, not auto-par vs single-core.

One honest qualifier: this is **allocation/`realloc`-dominated** — all four spend most of their time building and freeing the 20×20 `Vec`-of-`Vec` each iteration, so it measures growing-dynamic-array throughput as much as the marker sweep itself. A fixed 2-D-array discipline would be faster for everyone, but is a *different* data structure than the kata's `Vec[Vec[i64]]`.

### Runtime — Python

| Run | Mean ± σ |
|---|---|
| `py set_matrix_zeroes` (same K=100k) | 12535 ± 155 ms |

Python runs the **same** K=100,000 and agrees on the sink, so it is cross-checked (not scaled down). At ~12.5 s it is **~28× slower than kāra seq** — the gap the compiled path buys on this allocation- and index-heavy workload.

### Compile elapsed (cold)

| Compiler | Time |
|---|---|
| rustc -O set_matrix_zeroes.rs          | **206.4 ms** |
| clang -O3 set_matrix_zeroes.c          | 224.6 ms |
| **karac build set_matrix_zeroes.kara** | **297.4 ms** |

On this container karac compiles at ~1.32× clang and ~1.44× rustc for this file.

### Binary size

| Implementation | Size |
|---|---|
| c    set_matrix_zeroes                | 19.8 KiB |
| **kāra set_matrix_zeroes**            | **324.5 KiB** |
| go   set_matrix_zeroes                | 2.12 MiB |
| rust set_matrix_zeroes                | 3.78 MiB |

The `Vec`-heavy solver links the runtime's allocation/panic floor, so kāra's binary is 324.5 KiB — the same ~324 KiB floor as the other `Vec`-based katas ([#62](../62-unique-paths/)–[#66](../66-plus-one/), [#72](../72-edit-distance/)) — still far below Rust's 3.8 MiB and Go's 2.1 MiB, above C's 19.8 KiB.

### Runtime memory (peak)

| Implementation | Peak |
|---|---|
| c    set_matrix_zeroes                | 1.66 MiB |
| rust set_matrix_zeroes                | 2.11 MiB |
| **kāra set_matrix_zeroes**            | **2.29 MiB** |
| go   set_matrix_zeroes                | 7.36 MiB |

Kāra/C/Rust sit within ~0.6 MiB of each other (each matrix allocated and freed inside the loop — flat steady state, no leak across 100,000 iterations); Go's 7.36 MiB reflects its GC arena churning the `append`-grown slices.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| **karac build set_matrix_zeroes.kara** | **87.1 MiB** |
| clang -O3 set_matrix_zeroes.c          | 99.8 MiB |
| rustc -O set_matrix_zeroes.rs          | 111.0 MiB |

On this container karac has the lowest compile-memory footprint of the three.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — and here, with both building the matrix via a growing `Vec`, **kāra leads Rust 1.79×** (and C 1.59×, Go 2.34×). C calibrates the `realloc` floor, Go is the GC/`append` data point, Python the ergonomic foil. The load-bearing facts: the five-language sink agreement, that kāra is the *fastest* of the four at equal growing-`Vec` semantics, and — as [#72](../72-edit-distance/) first showed — that comparing kāra's heap `Vec[Vec]` against a native fixed 2-D array would understate it.
