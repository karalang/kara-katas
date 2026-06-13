# 1. Two Sum

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Array, Hash Table &nbsp;·&nbsp; **Source:** [leetcode.com/problems/two-sum](https://leetcode.com/problems/two-sum/)

Given an array of integers `nums` and an integer `target`, return the indices of the two numbers such that they add up to `target`.

You may assume each input has exactly one solution, and you may not use the same element twice.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| Brute force (nested loops) | O(n²) time, O(1) space | [`brute_force.kara`](brute_force.kara) ✓ | [`brute_force.py`](brute_force.py) ✓ |
| Hash map (single pass) | O(n) time, O(n) space | [`hash_map.kara`](hash_map.kara) ✓ | [`hash_map.py`](hash_map.py) ✓ |

`✓` runs end-to-end today.

## Kāra features exercised

- **Fixed-size `Array[i64, N]`** — stack-allocated array literals at the call site.
- **`Slice[i64]` parameter coercion** — `Array[i64, N]` arguments pass as `Slice[i64]` without an explicit conversion.
- **`Slice.len()` + indexed access** — O(1) length and O(1) indexed read.
- **Half-open range `for`** — `0..n` and `(i+1)..n` drive the nested loops.
- **Array-literal tail return** — `[i, j]` and `[-1, -1]` flow out as the function's last expression.
- **`Map[K, V]` (`hash_map.kara` only)** — generic runtime hashmap with `.new()`, `.get(k) -> Option[V]`, `.insert(k, v)`.

Both approaches return `[-1, -1]` as a sentinel until `Option[(i64, i64)]` lands in return position. No `Vec` or strings yet.

## Running

```bash
# Kāra
karac run brute_force.kara
karac run hash_map.kara

# Python (any version with PEP 604 union syntax — 3.10+)
python3 brute_force.py
python3 hash_map.py
```

## Benchmarks

### How to run

```bash
brew install hyperfine    # also needs rustc, clang, go, karac
./bench/bench.sh
```

`bench/bench.sh` follows the [kara-katas bench protocol](../../../BENCH.md): builds same-algorithm mirrors in Kāra, Rust, C, Go (and Python, optional), checks they print the same stdout sink, then times them with hyperfine. **brute_force** runs K=100 independent O(n²) two_sum calls — heavy enough per call that karac's auto-par-on-reduction parallelizes the `for _ in 0..100` loop with no parallel source, so it has both a seq lane (codegen quality) and a **par lane** (auto-par vs hand-tuned C/rayon/goroutines). **hash_map** stays seq-only — its ~5 K inserts/call are too light, and the runtime correctly keeps it serial.

| File | What it does |
|---|---|
| [`bench/brute_force.kara`](bench/brute_force.kara) | N=5000 deterministic input, **K=100** outer two_sum calls (scaled from 10 so the per-call O(n²) work clears the runtime auto-par gate — see par lane), sentinel target so brute force never short-circuits (full 12,497,500 inner-loop comparisons per call) |
| [`bench/hash_map.kara`](bench/hash_map.kara) | N=5000, **K=10**, same target; single-pass `Map[i64, i64]` (stays seq-only) |
| [`bench/brute_force.{rs,c,py}`](bench/) + [`bench/go-seq/brute_force/`](bench/go-seq/brute_force/) | Algorithmic mirrors — same N, K, target |
| par-lane (brute_force): [`bench/rayon/`](bench/rayon/), [`bench/go-par/`](bench/go-par/), [`bench/brute_force_par.c`](bench/brute_force_par.c) | hand-tuned-parallel mirrors of the K=100 reduction |
| [`bench/hash_map.{rs,c,py}`](bench/) + [`bench/go-seq/hash_map/`](bench/go-seq/hash_map/) | Same; idiomatic hashmap per language (`std::collections::HashMap` in Rust, open-addressing in C, `map[int64]int` in Go) |

`brute_force` mirrors print `-200` (K=100 × −2); `hash_map` mirrors print `-20` (K=10 × −2) — a sum-of-results sink so the output participates in I/O and can't be elided.

### Runtime — seq lane

Snapshot — M5 Pro, 2026-06-13, hyperfine `--warmup 5 --runs 30..40 --shell=none`, native binaries via `karac build` (`KARAC_AUTO_PAR=0` for the brute_force seq row), `rustc -O`, `clang -O3`, `go build`. Within-lane comparisons only. **brute_force now auto-pars** under default `karac build` (its K=100 reduction clears the runtime gate — par lane below); the seq row here is the `KARAC_AUTO_PAR=0` twin. `hash_map` stays seq-only (`nm -gU | grep karac_par_reduce` empty — per-call work too light, runtime correctly declines).

`brute_force` — inner-loop-dominated (~1.25 B comparisons total at K=100):

| Implementation | Wall time | User-CPU | Within-workload ratio |
|---|---|---|---|
| c    brute_force (clang -O3)     | **281 ms ± 2 ms**     | 279 ms  | 0.90× of Kāra |
| rust brute_force (rustc -O)      | 283 ms ± 2 ms         | 281 ms  | 0.91× of Kāra |
| go   brute_force                 | 284 ms ± 1 ms         | 282 ms  | 0.91× of Kāra |
| **kāra brute_force (seq)**       | **312 ms ± 21 ms**    | 310 ms  | **1.00×** (baseline) |

Kāra is **1.10× behind** the C/Rust/Go cluster (all tied ~283 ms — a trivial O(n²) loop every backend compiles identically). At the old K=10 these were dead-even (Kāra 29.5 vs C 29.6 ms); the gap that opens at K=100 is Kāra's `two_sum` returning a `Vec[i64]` — one heap allocation per call, ×100 — where the Rust/C/Go mirrors return a non-allocating `Option`/tuple. That allocator traffic also widens Kāra's σ (amplified by the 3 concurrent build agents on the box during this snapshot).

### Runtime — par lane (auto-par vs hand-tuned vs metal floor)

brute_force only. The K=100 independent O(n²) calls are embarrassingly parallel; all four parallelize that *same* reduction across the 18 cores — the difference is what the programmer wrote:

| | parallel code written | wall time | total CPU |
|---|---|---|---|
| Rust + rayon | `rayon` crate + `.into_par_iter()` | 22.0 ms | 334 ms |
| **Kāra (auto-par)** | **none** — compiler parallelized the `for _` reduction | **28.6 ms** | 399 ms |
| C + pthreads *(metal floor)* | raw `pthread_create`/`join` + chunk + merge | 47.6 ms | 342 ms |
| Go goroutines | chunk + `sync.WaitGroup` + merge | 65.9 ms | 505 ms |

**Kāra's auto-par beats the raw-pthreads metal floor (1.7×) and goroutines (2.3×) — second only to hand-tuned rayon (1.30× ahead) — with zero parallel source**, an ~11× speedup over its own seq binary (312 → 28.6 ms). As on #394's fine-grained workload, the C "floor" isn't the floor: per-process `pthread` spawn over 100 chunks loses to the pooled work-stealing schedulers (rayon, Kāra's `karac_par_reduce`). (Multi-core within the par lane; per [BENCH.md](../../../BENCH.md)'s two-lane discipline, *not* comparable to the single-thread seq rows above.)

**Buyer reframe.** The canonical "kata #1" — and Kāra parallelizes it for free: the speedup a Rust team buys with a crate + an API rewrite, a Go team with hand-rolled chunk/merge, and a C team with raw thread plumbing, Kāra emits from the same single-threaded source — out-running the C floor and goroutines. Colorless parallelism on the most-recognized interview problem there is.

`hash_map` — algorithm-dominated (~50 K inserts/lookups total):

| Implementation | Wall time | User-CPU | Within-workload ratio |
|---|---|---|---|
| c    hash_map (open-addressing)  | **1.1 ms ± 0.0 ms**   | 0.4 ms  | 0.79× of Kāra |
| **kāra hash_map (codegen)**      | **1.4 ms ± 0.1 ms**   | 0.6 ms  | **1.00×** (baseline) |
| rust hash_map (`HashMap`)        | 1.9 ms ± 0.1 ms       | 1.1 ms  | 1.36× of Kāra |
| go   hash_map (`map[int64]int`)  | 2.3 ms ± 0.1 ms       | 1.3 ms  | 1.64× of Kāra |

Kāra is **faster than Rust's `HashMap` and Go's `map`** here; the C row uses a workload-specific open-addressing table (no genuine "C hashmap" exists in libc), so it sits below by construction. The improvement vs the M1 snapshot (Kāra was at 1.4× of Rust) lines up with the Phase 4 monomorphization work — `Map[K, V]` no longer dispatches through erased function pointers when the key/value types are known at the call site — though disentangling that contribution from the M1→M5 hardware change would need a per-machine before/after. The headline number on M5 is what it is: Kāra-with-generic-Map beats Rust's `HashMap<i64, usize>` on this workload size.

Cross-workload ratios across this table (e.g. "C hash_map is 25× faster than Kāra brute_force") are arithmetic but not meaningful — different algorithms, not different language quality.

### Runtime — long workloads (interp + Python)

Same snapshot, hyperfine `--warmup 2 --runs 10 --shell=none`. These rows are kept in a separate batch because they cost orders of magnitude more wall time and would balloon the short-workload table.

| Run | Mean ± σ |
|---|---|
| `kara hash_map` (interp) | 12.54 s ± 0.11 s |
| `py brute_force` (K=100) | 19.39 s ± 0.38 s |

`karac run` re-runs the entire front-end every invocation (lex → parse → resolve → typecheck → effects → ownership) before tree-walking — the 12.5 s here is the pipeline rerun + tree-walk dispatch on every AST node, not the algorithm. `kara brute_force (interp)` is omitted at N=5000: tree-walk × 12.5 M comparisons takes a long time per run and doesn't add information beyond "tree-walk doesn't scale to N²." The interpreter-vs-codegen gap is **not** a Kāra-vs-X comparison — it's the cost of skipping `karac build`. Future work tracked in the [interpreter perf brainstorm](../../../../kara/brainstorming/archive/v62_interpreter_perf_and_binary_size.md).

Python is **11× slower** than Kāra codegen on `hash_map` (15.5 ms vs 1.4 ms) and **~62× slower** on `brute_force` (19.4 s vs 312 ms seq, both at K=100) — the gap CPython opens against any compiled-with-codegen language at workload sizes that put algorithm time above interpreter-startup floors. (Against Kāra's *auto-par* brute_force at 28.6 ms, Python is ~680× slower.)

### Compile elapsed (cold)

Snapshot — M5 Pro, 2026-05-23, hyperfine `--warmup 1 --runs 10 --shell=none` with `--prepare` deleting the artifact before each run:

| Workload | Kāra (`karac build`) | Rust (`rustc -O`) | C (`clang -O3`) |
|---|---|---|---|
| `brute_force` | **54.6 ± 1.8 ms** | 79.5 ± 0.8 ms | 44.8 ± 0.5 ms |
| `hash_map`    | **60.0 ± 2.6 ms** | 114.5 ± 2.0 ms | 41.9 ± 0.4 ms |

`karac build` is **1.46× faster than `rustc -O`** on `brute_force` and **1.91× faster** on `hash_map`, sitting between clang (the floor for an LLVM-backed single-file compile) and rustc (which carries more frontend work per file). Multi-file projects (Go modules, Cargo) are deliberately excluded from this table — first-invocation `go build` and `cargo build` mix dep resolution + link and aren't comparable to a single-file `karac`/`rustc`/`clang` invocation.

### Binary size

| Implementation | Size |
|---|---|
| c    brute_force (seq / par) | 32.8 / 32.9 KiB |
| c    hash_map    | 32.9 KiB |
| kāra brute_force (seq)       | 32.8 KiB |
| **kāra brute_force (par, auto-par)** | **505.4 KiB** |
| kāra hash_map    | 278.6 KiB |
| rust brute_force (seq / par+rayon) | 455.4 / 453.0 KiB |
| rust hash_map    | 457.0 KiB |
| go   brute_force (seq / par) | 2434.1 / 2451.0 KiB |
| go   hash_map    | 2434.2 KiB |

The `kara brute_force (par)` binary is +473 KiB over the seq twin — the `karac_par_reduce` worker/dispatch machinery statically linked in (the standing auto-par footprint cost). The `kara hash_map` row is heavier than `kara brute_force (seq)` because the runtime hashmap (probing + growth + finalizer plumbing) is statically linked; the seq brute-force binary only links the array/println runtime slice. Go's ~2.4 MiB on every binary is the Go runtime + GC + reflection — a deliberate Go design choice, not workload-driven.

### Runtime memory (peak, RSS)

| Implementation | Peak |
|---|---|
| c    brute_force (seq / par) | 1.0 / 1.4 MiB |
| kāra brute_force (seq)       | 1.0 MiB |
| kāra brute_force (par, auto-par) | 2.9 MiB |
| rust brute_force (seq / par) | 1.1 / 1.7 MiB |
| c    hash_map | 1.3 MiB |
| kāra hash_map (codegen) | 1.3 MiB |
| rust hash_map | 1.3 MiB |
| go   brute_force | 3.0 MiB |
| go   hash_map | 4.4 MiB |
| py   brute_force | 7.1 MiB |
| py   hash_map | 7.2 MiB |
| kāra hash_map (interp) | 19.8 MiB |

Kāra, Rust, and C all sit at the same per-workload memory floor (~1 MiB for brute force, ~1.3 MiB for hash map) — the hashmap variants pay for the runtime hashtable. Go's baseline includes the runtime + GC; Python's includes the CPython interpreter. The `kara hash_map (interp)` row carries the `karac` binary itself (~7 MB with `--features llvm`) plus the AST/value heap karac walks at runtime — `karac run` is interpreter overhead + algorithm working set, not algorithm alone. The 14.6 → 19.8 MiB drift from the 2026-05-22 snapshot reflects added frontend state from the slice-shipping work that landed since (push_str arm + Vec.filled arm + the wider stdlib_seq enumeration).

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 brute_force.c | 2.6 MiB |
| clang -O3 hash_map.c    | 2.6 MiB |
| karac build brute_force.kara | 8.9 MiB |
| karac build hash_map.kara    | 8.9 MiB |
| rustc -O brute_force.rs | 27.1 MiB |
| rustc -O hash_map.rs    | 37.4 MiB |

`karac` compiles both files in **~9 MiB peak** — between clang and rustc, with no algorithmic blowup signature (a 10× spike here is what catches frontend regressions like the 2026-05-12 `Array[T, N]` Maranget O(N²) fix). Go is omitted from the compile-memory row per BENCH.md — `go build`'s first invocation mixes module resolution + std-lib link and isn't comparable to a single-file invocation.

### Why this kata is in the harness

Two-sum is the canonical "small, dual-algorithm" entry: the same problem expressed as O(n²) array scan and O(n) hashmap lookup, so it exercises two distinct codegen paths (tight inner loop with bounds-check elision; generic runtime collection) on a workload small enough to surface compile-pipeline overhead. The brute-force row is what the autovectorizer can do when the loop is clean; the hash_map row is what the runtime collection costs over a hand-rolled probing table.
