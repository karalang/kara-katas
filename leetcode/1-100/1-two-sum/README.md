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
<!-- bench-staleness -->
> **Figures in this section are the 2026-10-29 snapshot** in [`bench/results.json`](bench/results.json) (M5 Pro, 6P+12E, `karac 0.1.0-dev.13686+g04628b0eb` — the v2/MIR backend, which has replaced the legacy backend). The [charts](../../../BENCHMARKS.md) render from the same feed.

### How to run

```bash
brew install hyperfine    # also needs rustc, clang, go, karac
./bench/bench.sh
```

`bench/bench.sh` follows the [kara-katas bench protocol](../../../BENCH.md): builds same-algorithm mirrors in Kāra, Rust, C, Go (and Python, optional), checks they print the same stdout sink, then times them with hyperfine. **brute_force** runs K=100 independent O(n²) two_sum calls — heavy enough per call that karac's auto-par parallelizes the `for _ in 0..100` loop with no parallel source, so it has both a seq lane (codegen quality) and a **par lane** (auto-par vs hand-tuned C/rayon/goroutines). **hash_map** stays seq-only — its ~5 K inserts/call are too light to be worth splitting.

| File | What it does |
|---|---|
| [`bench/brute_force.kara`](bench/brute_force.kara) | N=5000 deterministic input, **K=100** outer two_sum calls (scaled from 10 so the per-call O(n²) work clears the runtime auto-par gate — see par lane), sentinel target so brute force never short-circuits (full 12,497,500 inner-loop comparisons per call) |
| [`bench/hash_map.kara`](bench/hash_map.kara) | N=5000, **K=10**, same target; single-pass `Map[i64, i64]`; written as a seq-only lane, but the M4 runtime now auto-parallelizes the default build — see [B-2026-10-28-38](../../../../kara/docs/bugs-v2.jsonl) |
| [`bench/brute_force.{rs,c,py}`](bench/) + [`bench/go-seq/brute_force/`](bench/go-seq/brute_force/) | Algorithmic mirrors — same N, K, target |
| par-lane (brute_force): [`bench/rayon/`](bench/rayon/), [`bench/go-par/`](bench/go-par/), [`bench/brute_force_par.c`](bench/brute_force_par.c) | hand-tuned-parallel mirrors of the K=100 reduction |
| [`bench/hash_map.{rs,c,py}`](bench/) + [`bench/go-seq/hash_map/`](bench/go-seq/hash_map/) | Same; idiomatic hashmap per language (`std::collections::HashMap` in Rust, open-addressing in C, `map[int64]int` in Go) |

`brute_force` mirrors print `-200` (K=100 × −2); `hash_map` mirrors print `-20` (K=10 × −2) — a sum-of-results sink so the output participates in I/O and can't be elided.

### Re-bench 2026-10-29 — what moved

Classified old (previous feed snapshot, legacy backend, `karac 0.1.0 f80bb80b605f`) → new (this snapshot, v2/MIR backend). Comparator rows (C, Rust, Go) are flat throughout, so every Kāra movement below is Kāra's own.

| Metric | Old → new | Class | Cause |
|---|---|---|---|
| brute_force seq (codegen) | 306.7 → 331.3 ms ± 29.7 | noise / load | hyperfine flagged statistical outliers on this row (max 417 ms, min 292 ms); C/Rust/Go seq moved ≤ 0.5% |
| brute_force par (auto-par) | 27.6 → 29.8 ms | noise / load | still ahead of the C-pthreads floor (48.8 ms) and Go (67.1 ms); 1.35× of rayon (22.1 ms) |
| hash_map codegen | 1.2 → 1.8 ms | regression (deliberate) + lane caveat | `Map` hashing is now per-process-keyed SipHash-1-3 — a security fix (HashDoS resistance), not a codegen loss. The default binary is also now auto-parallel (223% CPU) for no wall gain over its `KARAC_AUTO_PAR=0` twin — [B-2026-10-28-38](../../../../kara/docs/bugs-v2.jsonl) |
| hash_map `karac run` | 41.9 → 105.9 ms | regression | on v2, `karac run` compiles before it runs, so this row is now compile latency — [B-2026-10-28-37](../../../../kara/docs/bugs-v2.jsonl) |
| binary size | +302,784 B seq / +84,144 B par / +118,560 B hash_map | regression | the MIR backend's binary floor (runtime linked whole) — [B-2026-10-28-36](../../../../kara/docs/bugs-v2.jsonl) |
| `karac build` elapsed / peak RSS | 93 → 171 ms, 24 → 70 MiB | regression | v2 compile-pipeline cost; `rustc -O` and `clang -O3` flat — [B-2026-10-28-37](../../../../kara/docs/bugs-v2.jsonl) |

### Runtime — seq lane

Snapshot — M5 Pro, 2026-10-29, hyperfine `--warmup 5 --runs 30 --shell=none`, native binaries via `karac build` (`KARAC_AUTO_PAR=0` for the brute_force seq row), `rustc -O`, `clang -O3`, `go build`. Within-lane comparisons only. **brute_force auto-pars** under the default `karac build` (par lane below); the seq row here is the `KARAC_AUTO_PAR=0` twin. Auto-par engagement is visible in the binary: the par build carries the v2 task runtime (`nm -gU | grep karac_mir_task_spawn`), which replaced the legacy `karac_par_reduce` dispatch.

`brute_force` — inner-loop-dominated (~1.25 B comparisons total at K=100):

| Implementation | Wall time | Min | User-CPU | Within-workload ratio |
|---|---|---|---|---|
| rust brute_force (rustc -O)      | **281.9 ms ± 1.2 ms** | 280.8 ms | 279.8 ms | 0.85× of Kāra |
| c    brute_force (clang -O3)     | 282.5 ms ± 1.8 ms     | 279.8 ms | 280.1 ms | 0.85× of Kāra |
| go   brute_force                 | 283.7 ms ± 2.2 ms     | 281.8 ms | 281.0 ms | 0.86× of Kāra |
| rust brute_force (`-C overflow-checks=on`) | 318.6 ms ± 28.0 ms | 290.6 ms | 316.1 ms | 0.96× of Kāra |
| **kāra brute_force (seq)**       | **331.3 ms ± 29.7 ms** | 292.2 ms | 328.8 ms | **1.00×** (baseline) |

On the mean Kāra is ~1.17× behind the C/Rust/Go cluster (all 282–284 ms); on the min it is 1.04× behind C. `two_sum` returns a stack `Array[i64, 2]` and allocates nothing — the remaining gap is the per-iteration overflow check on the inner `nums[i] + nums[j]` add (Kāra's default trapping arithmetic; `wrapping_add` is the escape). The equal-safety comparator, `rustc -O -C overflow-checks=on`, lands at 318.6 ms (min 290.6 ms) — within 4% of Kāra on the mean and 1% on the min, with the same wide σ. That σ is P/E-core scheduling on the M5 Pro's hybrid chip plus concurrent load (hyperfine flagged statistical outliers on the Kāra row this run); take the min column as the load-immune signal.

### Runtime — par lane (auto-par vs hand-tuned vs metal floor)

brute_force only, hyperfine `--warmup 10 --runs 50 --shell=none`. The K=100 independent O(n²) calls are embarrassingly parallel; all four parallelize that *same* reduction across the 18 cores — the difference is what the programmer wrote:

| | parallel code written | wall time | total CPU |
|---|---|---|---|
| Rust + rayon | `rayon` crate + `.into_par_iter()` | 22.1 ms | 340 ms |
| **Kāra (auto-par)** | **none** — compiler parallelized the `for _` reduction | **29.8 ms** | 392 ms |
| C + pthreads *(metal floor)* | raw `pthread_create`/`join` + chunk + merge | 48.8 ms | 343 ms |
| Go goroutines | chunk + `sync.WaitGroup` + merge | 67.1 ms | 508 ms |

**Kāra's auto-par beats the raw-pthreads metal floor (1.64×) and goroutines (2.26×) — second only to hand-tuned rayon (1.35× ahead) — with zero parallel source**, an ~11× speedup over its own seq binary (331.3 → 29.8 ms). As on #394's fine-grained workload, the C "floor" isn't the floor: per-process `pthread` spawn over 100 chunks loses to the pooled work-stealing schedulers (rayon, Kāra's `karac_mir_task_spawn` runtime). (Multi-core within the par lane; per [BENCH.md](../../../BENCH.md)'s two-lane discipline, *not* comparable to the single-thread seq rows above.)

**Buyer reframe.** The canonical "kata #1" — and Kāra parallelizes it for free: the speedup a Rust team buys with a crate + an API rewrite, a Go team with hand-rolled chunk/merge, and a C team with raw thread plumbing, Kāra emits from the same single-threaded source — out-running the C floor and goroutines. Colorless parallelism on the most-recognized interview problem there is.

`hash_map` — algorithm-dominated (~50 K inserts/lookups total):

| Implementation | Wall time | User-CPU | Within-workload ratio |
|---|---|---|---|
| c    hash_map (open-addressing)  | **1.1 ms ± 0.0 ms**   | 0.4 ms  | 0.65× of Kāra |
| **kāra hash_map (codegen)**      | **1.8 ms ± 0.1 ms**   | 2.0 ms  | **1.00×** (baseline) |
| rust hash_map (`-C overflow-checks=on`) | 1.9 ms ± 0.1 ms | 1.2 ms | 1.10× of Kāra |
| rust hash_map (`HashMap`)        | 2.0 ms ± 0.2 ms       | 1.2 ms  | 1.13× of Kāra |
| go   hash_map (`map[int64]int`)  | 2.3 ms ± 0.1 ms       | 1.3 ms  | 1.28× of Kāra |

Kāra is still **faster than Rust's `HashMap` and Go's `map`** here, now with a per-process-keyed SipHash-1-3 `Map` hash — the same HashDoS-resistant family Rust's `HashMap` uses by default. That hash is why this row moved 1.2 → 1.8 ms since the previous feed; it is a deliberate security trade, not a codegen loss. **Lane caveat:** the Kāra row is the default build, which the M4 runtime now fans out across cores (223% CPU, user time above wall). Its `KARAC_AUTO_PAR=0` twin runs the same program in 26.8 M instructions against 31.2 M, at an indistinguishable wall time on a 2 ms process, so the activation buys nothing and is filed as a cost-model fault, [B-2026-10-28-38](../../../../kara/docs/bugs-v2.jsonl). The seq path itself is not slower than legacy's: 26.9 M instructions today against 31.6 M from legacy at the switch commit. The C row uses a workload-specific open-addressing table with no keyed hash (no genuine "C hashmap" exists in libc), so it sits below by construction.

Cross-workload ratios across these tables (e.g. "C hash_map is ~290× faster than Kāra brute_force") are arithmetic but not meaningful — different algorithms, not different language quality.

### Runtime — long workloads (interp + Python)

Same snapshot, hyperfine `--warmup 2 --runs 10 --shell=none`. These rows are kept in a separate batch because they cost orders of magnitude more wall time and would balloon the short-workload table.

| Run | Mean ± σ |
|---|---|
| `kara hash_map` (`karac run`) | 105.9 ms ± 1.8 ms |

On the v2 backend `karac run` compiles the program before running it, so this row is now compile latency plus a 1.8 ms run — it moved 41.9 → 105.9 ms with the same compile-pipeline cost that the compile-elapsed table shows ([B-2026-10-28-37](../../../../kara/docs/bugs-v2.jsonl)). It is **not** a Kāra-vs-X comparison — it is the cost of skipping a separate `karac build`. `kara brute_force` under `karac run` is omitted. The Python mirrors are sink-checked by `bench.sh` but were not timed in this snapshot (no Python rows in `results.json`), so no Python ratio is quoted here.

### Compile elapsed (cold)

Snapshot — M5 Pro, 2026-10-29, hyperfine `--warmup 1 --runs 10 --shell=none` with `--prepare` deleting the artifact before each run:

| Workload | Kāra (`karac build`) | Rust (`rustc -O`) | C (`clang -O3`) |
|---|---|---|---|
| `brute_force` | **171.4 ± 2.0 ms** | 72.6 ± 0.4 ms | 44.1 ± 1.5 ms |
| `hash_map`    | **175.4 ± 1.4 ms** | 114.4 ± 1.4 ms | 48.7 ± 0.5 ms |

`karac build` is now **2.36× slower than `rustc -O`** on `brute_force` and **1.53× slower** on `hash_map` — it was ahead of rustc on both in the previous feed (93 / 95 ms). rustc and clang are flat, so the 93 → 171 ms move is Kāra's v2 compile pipeline ([B-2026-10-28-37](../../../../kara/docs/bugs-v2.jsonl)). Both files still compile flat relative to each other — no algorithmic blowup signature. Multi-file projects (Go modules, Cargo) are deliberately excluded from this table — first-invocation `go build` and `cargo build` mix dep resolution + link and aren't comparable to a single-file `karac`/`rustc`/`clang` invocation.

### Binary size

| Implementation | Size |
|---|---|
| c    brute_force (seq / par) | 32.8 / 32.9 KiB |
| c    hash_map    | 33.0 KiB |
| kāra brute_force (seq)       | 328.7 KiB |
| **kāra brute_force (par, auto-par)** | **378.2 KiB** |
| kāra hash_map    | 394.6 KiB |
| rust brute_force (seq / par+rayon) | 455.4 / 453.0 KiB |
| rust hash_map    | 457.0 KiB |
| go   brute_force (seq / par) | 2434.1 / 2451.0 KiB |
| go   hash_map    | 2434.2 KiB |

Every Kāra binary grew on the MIR backend: +302,784 B on the seq brute_force binary (33.0 → 328.7 KiB), +84,144 B on the par build, +118,560 B on hash_map ([B-2026-10-28-36](../../../../kara/docs/bugs-v2.jsonl)). The seq binary no longer links only the array/println slice of the runtime, so Kāra now sits between C and Rust rather than at C's size. The par build is +49.5 KiB over the seq twin — the `karac_mir_task_spawn` worker/dispatch machinery (the standing auto-par footprint cost). Go's ~2.4 MiB on every binary is the Go runtime + GC + reflection — a deliberate Go design choice, not workload-driven.

### Runtime memory (peak, RSS)

| Implementation | Peak |
|---|---|
| c    brute_force (seq / par) | 1.0 / 1.4 MiB |
| kāra brute_force (seq)       | 1.0 MiB |
| kāra brute_force (par, auto-par) | 2.4 MiB |
| rust brute_force (seq / par) | 1.1 / 1.7 MiB |
| c    hash_map | 1.3 MiB |
| kāra hash_map (codegen) | 2.4 MiB |
| rust hash_map | 1.3 MiB |
| go   brute_force (seq / par) | 2.6 / 4.2 MiB |
| go   hash_map | 4.1 MiB |
| kāra hash_map (`karac run`) | 58.5 MiB |

Kāra seq brute_force sits at the same ~1 MiB floor as C and Rust. The Kāra par build (1.4 → 2.4 MiB) and hash_map (1.3 → 2.4 MiB) peaks rose with the MIR runtime and are now ~1 MiB above the C/Rust rows — both are auto-parallel builds, and the pool's threads cost about 1 MiB ([B-2026-10-28-36](../../../../kara/docs/bugs-v2.jsonl)); Go's baseline includes the runtime + GC. The `kara hash_map (karac run)` row is the peak of the `karac` process, which on v2 compiles the program before running it — it tracks the compile-memory table below (23.0 → 58.5 MiB), not the algorithm's working set.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 brute_force.c | 2.6 MiB |
| clang -O3 hash_map.c    | 2.6 MiB |
| karac build brute_force.kara | 70.0 MiB |
| karac build hash_map.kara    | 69.0 MiB |
| rustc -O brute_force.rs | 26.1 MiB |
| rustc -O hash_map.rs    | 37.3 MiB |

`karac` now peaks at **~70 MiB** on both files — up from ~24 MiB in the previous feed and above rustc, while rustc and clang are flat ([B-2026-10-28-37](../../../../kara/docs/bugs-v2.jsonl)). The two files are within 1 MiB of each other, so there is no per-program algorithmic blowup signature (a spike on one file is what catches frontend regressions like the 2026-05-12 `Array[T, N]` Maranget O(N²) fix); the growth is a fixed cost of the v2 pipeline. Go is omitted from the compile-memory row per BENCH.md — `go build`'s first invocation mixes module resolution + std-lib link and isn't comparable to a single-file invocation.

### Why this kata is in the harness

Two-sum is the canonical "small, dual-algorithm" entry: the same problem expressed as O(n²) array scan and O(n) hashmap lookup, so it exercises two distinct codegen paths (tight inner loop with bounds-check elision; generic runtime collection) on a workload small enough to surface compile-pipeline overhead. The brute-force row is what the autovectorizer can do when the loop is clean; the hash_map row is what the runtime collection costs over a hand-rolled probing table.

## Calibration re-probe (2026-10-06)

Re-probed with new phrasings, on all four surfaces plus valgrind, as part of a ten-kata calibration batch (katas 1-49, against kata 352's probing). Added [`differential.kara`](differential.kara): a hash map and a two-pointer existence check against a brute-force oracle over 3000 random arrays, duplicates and negatives included (clean everywhere). Gaps found, in the kara bug ledger:

- **B-2026-10-06-73** — `(vec![], 5)` against a `(Vec[i64], i64)` slot was refused at check time (fixed).
- **B-2026-10-06-74** — a `find` / `filter` predicate written over the element by value is refused, where design.md gives the parameter as `ref Self.Item`.
- **B-2026-10-06-75** — `find` / `find_map` over a tuple or unit-only-enum element is refused by `karac build`.
- **B-2026-10-06-76** — a non-empty `Set[..]` literal anywhere, and an empty `Map[]` / `Set[]` outside a `let`, have no codegen lowering.
