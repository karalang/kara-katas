# 54. Spiral Matrix

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array · Matrix · Simulation &nbsp;·&nbsp; **Source:** [leetcode.com/problems/spiral-matrix](https://leetcode.com/problems/spiral-matrix/)

Given an `m × n` matrix, return **all** its elements in **spiral order** — start at the top-left,
walk right, then down, then left, then up, spiralling inward until every cell has been emitted.

```
[[1,2,3],[4,5,6],[7,8,9]]                →  [1,2,3,6,9,8,7,4,5]
[[1,2,3,4],[5,6,7,8],[9,10,11,12]]       →  [1,2,3,4,8,12,11,10,9,5,6,7]
[[1,2,3,4,5]]                            →  [1,2,3,4,5]           single row
[[1],[2],[3],[4]]                        →  [1,2,3,4]             single column
```

**Constraints:** `m == matrix.length`, `n == matrix[i].length`, `1 ≤ m, n ≤ 10`,
`−100 ≤ matrix[i][j] ≤ 100`. The matrix need not be square, so every solver must handle wide,
tall, single-row and single-column shapes — this kata pins three of them.

## Why this kata — one traversal, three ways to decide the turns

Spiral Matrix is a pure *simulation* problem: there is no clever math, only the question of **how you
decide when to turn**. The kata is about seeing that the same clockwise walk can be driven three
structurally different ways — by shrinking walls, by remembering where you've been, or by a
closed-form run-length pattern — that all emit the identical sequence.

| Lens | Extra state | How the turn is decided |
|---|---|---|
| **Boundary shrinking** ★ | four `i64` walls, `O(1)` | walk to the current wall, then move the wall inward |
| **Direction + visited grid** | a `Vec[Vec[bool]]`, `O(m·n)` | turn right when the next cell is off-grid or already emitted |
| **Run-length simulation** | two `i64` counters, `O(1)` | take a run of the pre-computed length, then turn |

**Boundary shrinking** holds `top / bottom / left / right` and peels one ring per outer iteration:
top row →, right column ↓, bottom row ←, left column ↑, shrinking the matching wall after each pass.
**Direction + visited** forgets the walls entirely and simulates a walker that keeps going straight
until the next step would leave the matrix or revisit a cell, at which point it rotates its heading
clockwise. **Run-length simulation** drops *both* the walls and the grid: it exploits the fact that
the spiral is a fixed sequence of straight runs whose lengths are `n, m−1, n−1, m−2, n−2, …`,
cycling the four headings and stopping at the first non-positive run.

**The shared correctness pin — a degenerate final row or column must not be emitted twice.** When the
matrix has an odd number of rows or columns, the innermost layer collapses to a single line. On the
`3×3` that lone cell is the middle `5`; on a `1×5` it is the whole row. Each solver has a *different*
guard against re-emitting it:

- **Boundary shrinking** re-checks the (already-shrunk) walls with `if top <= bottom` before the
  bottom-row pass and `if left <= right` before the left-column pass, and skips them when the
  rectangle has collapsed to a line.
- **Direction + visited** needs no special case: the lone leftover line simply turns the walker back
  into already-visited cells, and *that* forces the turns that terminate the walk.
- **Run-length simulation** never represents the extra pass: a single row has `ver = m − 1 = 0`, so
  the walk stops after the first horizontal run; a single column drains its one horizontal run of
  length 1, then the vertical run, then hits a length-0 run and stops.

Three guards, one rule — that convergence is the kata.

### The run-length pattern, spelled out

For an `m × n` matrix the spiral is a sequence of straight runs whose lengths, in order, are
`n, m−1, n−1, m−2, n−2, m−3, …`: the horizontal runs count down `n, n−1, n−2, …` and the vertical
runs count down `m−1, m−2, m−3, …`, interleaved. Cycling the four clockwise headings
(right, down, left, up) and taking the next run's worth of steps before each turn reproduces the
spiral exactly, and the runs go non-positive precisely when the matrix is exhausted — so `if run <= 0
{ break }` is the whole termination logic, no bounds test and no visited grid.

## Approaches

| Approach | File | Time · Space | Turn decided by |
|---|---|---|---|
| **Boundary shrinking** ★ | [`spiral_boundary.kara`](spiral_boundary.kara) | `O(m·n)` · `O(1)` | four shrinking walls |
| **Direction + visited grid** | [`spiral_visited.kara`](spiral_visited.kara) | `O(m·n)` · `O(m·n)` | off-grid or already-visited peek |
| **Run-length simulation** | [`spiral_steps.kara`](spiral_steps.kara) | `O(m·n)` · `O(1)` | pre-computed run lengths |
| Oracle | [`spiral_matrix.py`](spiral_matrix.py) | `O(m·n)` | mirrors the ★ solver + identical output format |

All three `.kara` files share a line-for-line-identical test harness (12 cases spanning square, wide,
tall, single-row, single-column, deep-`5×5` and negative-valued matrices, one bracketed spiral per
line plus a `sums:` fold of per-case positional checksums `Σ (k+1)·seq[k]`) and diff byte-for-byte
against the Python oracle under `karac run`, `karac build`, and the default auto-par build.

## What this kata surfaced

A **clean pass** — like [#51 N-Queens](../51-n-queens/) and [#53 Maximum Subarray](../53-maximum-subarray/),
all three solvers compiled and produced the oracle's output byte-for-byte on the first A/B run across
`karac run`, `karac build` (`KARAC_AUTO_PAR=0`), and the default auto-par build. No compiler gap
turned up.

The exercises that could plausibly have snagged each behaved correctly on all three surfaces:
**chained nested-index reads** `m[r][right]` / `m[bottom][c2]` off a `ref Vec[Vec[i64]]` parameter
(the same borrowed-nested-collection shape that hid
[B-2026-06-29-2](../../../../kara/docs/bug-ledger.md) in [#48 Rotate Image](../48-rotate-image/),
here in *read* position and at arbitrary rows rather than a single bound row); **negative integer
literals inside a nested `Vec[Vec[i64]]` literal** (`[[-1, -2], [-3, -4]]`) flowing through the
by-value `grid` parameter; a **nested `Vec.filled(rows, Vec.filled(cols, false))`** building
independent `false` rows for the visited grid; and the run-length solver's negative loop-start
`c = -1i64` with `Array[i64, 4]` direction vectors carrying a `-1` element. The auto-par build did
not mis-parallelize any of the three sequential fill/traverse loops.

The only friction was three of my own surface-syntax slips the parser caught immediately — Kāra spells
the operators `and` / `or` / `not` (not `&&` / `||` / `!`), and `seq` is a reserved token so the
sequence binding is named `order`. Each was a one-line parse error, not a compiler gap.

## Kāra features exercised

- **Chained nested-index reads on a borrowed matrix** — `m[top][c]`, `m[r][right]`,
  `m[bottom][c2]`, `m[r2][left]` off a `ref Vec[Vec[i64]]` parameter, indexing arbitrary rows and
  columns in read position.
- **`Vec[Vec[bool]]` visited grid** via `Vec.filled(rows, Vec.filled(cols, false))` with the chained
  nested-index assign `visited[r][c] = true`.
- **`Array[i64, 4]` direction vectors** carrying a negative `-1` step, cycled with `d = (d + 1) % 4`.
- **Negative literals inside nested `Vec[Vec[i64]]` literals** passed by value into the harness.
- **`mut ref String` accumulator** threaded through a shared `report` helper to fold each case's
  positional checksum into one `sums:` summary line.

## Benchmarks

```bash
brew install hyperfine    # one-time, also needs rustc (rustup), clang, go, karac
./bench/bench.sh          # KARA_BENCH_INCLUDE_PY=1 to include the Python row
```

`bench/bench.sh` builds the Rust file with `rustc -O`, the C file with `clang -O3`, the Kāra file
with `karac build` (`KARAC_AUTO_PAR=0`), and the Go module with `go build` (all cached in
`bench/target/`, gitignored), then times them with `hyperfine` per the
[BENCH.md protocol](../../../BENCH.md) and writes [`bench/results.json`](bench/results.json).

| File | What it does |
|---|---|
| [`bench/spiral_bench.kara`](bench/spiral_bench.kara) | **Boundary-spiral kernel** over 200 000 LCG-filled 24×24 matrices, one `i64` sink |
| [`bench/spiral_bench.rs`](bench/spiral_bench.rs) | mirror; `rustc -O` |
| [`bench/spiral_bench.c`](bench/spiral_bench.c) | mirror; `clang -O3` |
| [`bench/go-seq/main.go`](bench/go-seq/main.go) | mirror; `go build` |
| [`bench/spiral_bench.py`](bench/spiral_bench.py) | mirror; CPython |

**Workload.** A deterministic LCG (the classic glibc recurrence, `state ← (1103515245·state + 12345)
mod 2³¹`) fills a fixed 24×24 buffer with pseudo-random values in `[-50, 49]`, the ★ solver's
boundary-shrinking spiral then walks it and folds each cell into a **position-weighted checksum**
`(pos+1)·value`, where `pos` is the cell's rank in the spiral. The weighting is the point: it makes
the *traversal order* observable, so the kernel is genuinely "walk the matrix spirally" and cannot
collapse to an order-independent row-major sum. Each matrix's checksum is folded into one `i64` sink
over 200 000 matrices, and the 24×24 buffer is a single fixed stack array reused every iteration — no
per-iteration allocation. Everything is overflow-safe by construction (Kāra **traps on `i64`
overflow** by default — [design.md § Arithmetic Overflow](../../../../kara/docs/design.md)):
`state < 2³¹` keeps the product `1103515245·state < 2⁶¹` inside `i64`, and the fold stays far below
`i64`. The generator and traversal are integer-only and identical across languages, so the sink folds
to one **bit-exact, cross-language-diffable** value (`-16442722648`) that every language prints
identically.

### Runtime

Snapshot — M5 Pro, 2026-07-03, hyperfine `--warmup 5 --runs 30`, means:

| Implementation | Wall time | User-CPU |
|---|---|---|
| **`kara spiral_bench`** (codegen, seq) | **217.3 ms ± 3.2 ms** | 214.8 ms |
| `c    spiral_bench` (clang -O3) | 162.3 ms ± 1.5 ms | 159.8 ms |
| `rust spiral_bench` (rustc -O) | 183.1 ms ± 5.3 ms | 180.2 ms |
| `rust spiral_bench` (`-C overflow-checks=on`) | 224.3 ms ± 3.0 ms | 221.3 ms |
| `go   spiral_bench` (go build) | 340.8 ms ± 1.0 ms | 336.9 ms |
| `py   spiral_bench` (CPython) | 15940 ms | — |

**Here the overflow checks show — and against a safety-matched compiler Kāra still comes out
ahead.** The hot path per cell is a position-weight multiply `(pos+1)·value` folded into the
accumulator, on top of the per-cell LCG fill (a multiply and a modulo). Kāra **traps on integer
overflow by default** ([design.md § Arithmetic Overflow](../../../../kara/docs/design.md)); `clang
-O3`, `rustc -O`, and Go all **silently wrap**. Unlike [#53](../53-maximum-subarray/), where a
dominant modulo hid the checks and all four compilers tied at the noise floor, this kernel's
traversal multiply has no such latency to hide under — so the default-safe build lands **217.3 ms**,
trailing unsafe `clang -O3` (162.3, **1.34×**) and unsafe `rustc -O` (183.1, **1.19×**). But the fair
comparison holds a compiler to the *same* overflow safety: against `rustc -O -C overflow-checks=on`
(224.3 ms) Kāra is a hair **faster** (1.03×), and it stays **1.57× ahead of Go** (340.8 ms) and
**~73× ahead of CPython**.

This is the [#52](../52-n-queens-ii/) pattern, not the [#53](../53-maximum-subarray/) one: on a
kernel whose arithmetic isn't already modulo-bound, Kāra's default-safe output pays a visible margin
against the wrapping compilers — but matched safety-for-safety it is level with or ahead of Rust. The
cost is exactly the overflow checks C and `rustc -O` choose to skip, no more.

### Compile time, binary size, memory

Snapshot — M5 Pro, 2026-07-03, hyperfine `--warmup 1 --runs 10` (compile, cold via `--prepare`);
size and peak RSS are single deterministic samples.

| Compiler | Compile (cold) | Binary | Peak RSS |
|---|---|---|---|
| `clang -O3` | 46.9 ms | 32.9 KiB | 1.00 MiB |
| `rustc -O` | 84.6 ms | 455.4 KiB | 1.06 MiB |
| **`karac build`** | **85.5 ms** | **33.2 KiB** | **1.00 MiB** |
| `go build` | — (excluded; mixes module + std-lib link) | 2434.1 KiB | 2.78 MiB |

Kāra emits a binary **~13.7× smaller than Rust** and line-ball with C (33.2 vs 32.9 KiB), and ties C
for peak RSS (~1.0 MiB, ~2.8× under Go and ~6.8× under CPython). Its cold compile is on par with
`rustc -O` (85.5 vs 84.6 ms) and trails `clang` (46.9 ms), matching the shape of the tiny integer
kernels in [#52](../52-n-queens-ii/) and [#53](../53-maximum-subarray/).
