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

`bench/bench.sh` follows the [kara-katas bench protocol](../../../BENCH.md): builds same-algorithm mirrors in Kāra, Rust, C, Go (and Python, optional), checks they print the same stdout sink, then times them with hyperfine. Both approaches are seq-only — the per-call work (~12.5 M comparisons for brute force; ~5 K inserts for hash map) is small enough that a par lane would mostly measure dispatch overhead, so the kata measures pure codegen quality.

| File | What it does |
|---|---|
| [`bench/brute_force.kara`](bench/brute_force.kara) | N=5000 deterministic input, K=10 outer iterations, sentinel target so brute force never short-circuits (full 12,497,500 inner-loop comparisons per call) |
| [`bench/hash_map.kara`](bench/hash_map.kara) | Same N, K, target; single-pass `Map[i64, i64]` |
| [`bench/brute_force.{rs,c,py}`](bench/) + [`bench/go-seq/brute_force/`](bench/go-seq/brute_force/) | Algorithmic mirrors — same N, K, target |
| [`bench/hash_map.{rs,c,py}`](bench/) + [`bench/go-seq/hash_map/`](bench/go-seq/hash_map/) | Same; idiomatic hashmap per language (`std::collections::HashMap` in Rust, open-addressing in C, `map[int64]int` in Go) |

All mirrors print `-20` (sum-of-results sink so the algorithm's output participates in I/O and can't be elided).

### Runtime — seq lane

Snapshot — M5 Pro, 2026-05-23, hyperfine `--warmup 5 --runs 30 --shell=none`, native binaries via `karac build`, `rustc -O`, `clang -O3`, `go build`. Within-lane comparisons only; the two workloads are listed separately because their algorithmic complexities differ. Both kara binaries verified seq via `nm -gU | grep karac_par_reduce` (no auto-par symbols present) per BENCH.md § Implicit auto-par.

`brute_force` — inner-loop-dominated (~125 M comparisons total):

| Implementation | Wall time | User-CPU | Within-workload ratio |
|---|---|---|---|
| **kāra brute_force (codegen)**   | **29.5 ms ± 0.1 ms**  | 28.2 ms | **1.00×** (baseline) |
| c    brute_force (clang -O3)     | 29.6 ms ± 0.1 ms      | 28.3 ms | 1.00× of Kāra |
| go   brute_force                 | 30.6 ms ± 0.2 ms      | 29.0 ms | 1.04× of Kāra |
| rust brute_force (rustc -O)      | 32.0 ms ± 1.0 ms      | 30.6 ms | 1.08× of Kāra |

Kāra is at **C parity** on the brute-force inner loop. The earlier 2.9× gap to Rust (M1, 2026-05-06) was the cost of an unelided bounds-check blocking LLVM's autovectorizer; that closed once bounds-check elision landed. Kāra, C, Go, and Rust now all sit within ~10% of each other on this workload — within run-to-run jitter and not a meaningful per-language ranking.

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
| `py brute_force`         | 2.01 s ± 0.05 s |

`karac run` re-runs the entire front-end every invocation (lex → parse → resolve → typecheck → effects → ownership) before tree-walking — the 12.5 s here is the pipeline rerun + tree-walk dispatch on every AST node, not the algorithm. `kara brute_force (interp)` is omitted at N=5000: tree-walk × 12.5 M comparisons takes a long time per run and doesn't add information beyond "tree-walk doesn't scale to N²." The interpreter-vs-codegen gap is **not** a Kāra-vs-X comparison — it's the cost of skipping `karac build`. Future work tracked in the [interpreter perf brainstorm](../../../../karac-rust/brainstorming/archive/v62_interpreter_perf_and_binary_size.md).

Python is **11× slower** than Kāra codegen on `hash_map` (15.5 ms vs 1.4 ms) and **68× slower** on `brute_force` (2.01 s vs 29.5 ms) — the gap CPython opens against any compiled-with-codegen language at workload sizes that put algorithm time above interpreter-startup floors.

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
| c    brute_force | 32.8 KiB |
| c    hash_map    | 32.9 KiB |
| kāra brute_force | 48.9 KiB |
| kāra hash_map    | 294.8 KiB |
| rust brute_force | 455.4 KiB |
| rust hash_map    | 457.0 KiB |
| go   brute_force | 2434.1 KiB |
| go   hash_map    | 2434.2 KiB |

The `kara hash_map` row is heavier than `kara brute_force` because the runtime hashmap (probing + growth + finalizer plumbing) is statically linked in; the brute-force binary only links the array/println slice of the runtime. Rust pays the same kind of `HashMap` static-link cost but at a higher baseline. Go's ~2.4 MiB on every binary is the Go runtime + GC + reflection — a deliberate Go design choice, not workload-driven.

### Runtime memory (peak, RSS)

| Implementation | Peak |
|---|---|
| c    brute_force | 1.1 MiB |
| kāra brute_force (codegen) | 1.1 MiB |
| rust brute_force | 1.1 MiB |
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
