# kara-katas — bench protocol

Per-kata benchmark setup. Each kata under `leetcode/*/` ships a `bench/bench.sh` that compares Kāra against same-shape implementations in Rust, C, Go (and Python where useful) on the same algorithmic workload. Workloads with no cross-iteration data dependency also add a *parallel lane* comparing Kāra's auto-par to Rust's `rayon` and Go's goroutines. This document is the protocol every kata `bench.sh` follows.

Mirror of [`karac-rust/bench/README.md`](../karac-rust/bench/README.md) — the discipline is shared between the kata corpus (runtime perf) and the karac-rust compile-quality tracks.

## What's measured

| Dimension | Tool | Discipline |
|---|---|---|
| Runtime elapsed time | `hyperfine` | `--warmup` + `--runs` tuned per workload duration (see below) |
| Runtime peak memory | `/usr/bin/time -l` (macOS BSD time) | Single sample; memory is stable run-to-run |
| Compile peak memory | `/usr/bin/time -l` | Single sample; artifact deleted before invocation for cold compile |
| **Compile elapsed time** | `hyperfine` | New — added 2026-05-20; matches karac-rust compile-speed gate |

## Hyperfine discipline

- **Short workloads (<50ms)**: `hyperfine --warmup 5 --runs 30 --shell=none`. At low run counts (10), startup jitter swamps the signal; 30 runs drowns it out.
- **Long workloads (>1s)**: `hyperfine --warmup 2 --runs 10 --shell=none`. Already <2% RSD at 10 runs; bumping runs adds wall-time without information.
- **Cold compile-elapsed**: `hyperfine --warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`. The `--prepare` deletes the build artifact before each run so every invocation measures a full cold compile.

## Comparison baselines

Per kata, ship sibling implementations. Each kata picks the subset of comparators its workload's lanes call for (see *Lanes* below for what "lane" means here).

### Seq lane — always required

Every kata's bench has at least the seq lane: single-threaded, no library help, same algorithm across all comparators. This is the **load-bearing per-core compiler-quality comparison** — what the kata corpus is primarily for.

- **Kāra**: `<approach>.kara` — the workload as written in Kāra. Built with `karac build` for codegen-mode runtime perf; also runnable via `karac run` for interpreter perf (where applicable).
- **Rust**: `<approach>.rs` — semantic peer (same LLVM backend, monomorphization, ownership). Built with `rustc -O`. The honest single-thread comparison.
- **C**: `<approach>.c` — codegen calibration point. Built with `clang -O3`. Same LLVM backend as Kāra and Rust; gap to C is the cost of the higher-level abstractions both Kāra and Rust pay.
- **Go**: `bench/go-seq/main.go` + `go.mod` — separate cross-runtime data point. Built with `go build` (Go has no `-O` flag; default is already optimized). Has been a standing baseline since 2026-05-21 (was "launch-only" in the prior protocol — upgraded after kata #204 surfaced a real per-core gap worth tracking continuously, not just at launch).
- **Python (optional)**: `<approach>.py` — ergonomic foil. Establishes the "is the perf cliff worth the syntax?" framing. Often skipped from the timed run for large-N workloads (Python at N=10⁷ trial-division takes ~30s; gate behind `KARA_BENCH_INCLUDE_PY=1` if so).

### Par lane — when the workload admits parallelism

When the workload's outer loop has no cross-iteration data dependency, the kata adds a **parallel lane**. The comparison shifts from "is Kāra's compiler at parity?" to "is Kāra's built-in auto-par competitive with neighboring languages' parallel offerings?"

- **Kāra**: `bench/<approach>.kara` — same source as the seq mirror but with `#[par_unordered]` (or whatever parallel attribute fits) on the outer loop. Exercises the karac runtime's `karac_par_reduce` path.
- **Rust + rayon**: `bench/rayon/` — its own Cargo project (rayon is a third-party crate; no `rustc` single-file path). Carries `Cargo.toml` + `Cargo.lock` (committed for reproducibility) + `src/main.rs` using `.into_par_iter().filter(...).collect()` or whichever rayon idiom matches the shape.
- **Go goroutines**: `bench/go-par/` — its own Go module (each Go executable needs a module root). `goroutines + sync.WaitGroup`, per-worker private slice, final merge — mirrors Kāra and rayon's per-worker-partials shape.

A kata without an obvious parallel lane (e.g., kata-7 reverse-integer, where each call is independent but the workload's per-call work is too small to amortize dispatch) stays seq-only. The decision is per-kata; not every workload benefits from a par lane.

### Lanes — what the framing means

A **lane** is a comparator class within which apples-to-apples wall-clock comparisons make sense. The two lanes in this protocol are *seq* (single-threaded codegen quality) and *par* (parallel-runtime quality). **Cross-lane comparisons are explicitly not meaningful** — e.g. "parallel Kāra is N× faster than single-threaded Rust" conflates the language's compiler quality with whether the comparator opted into parallelism, and would silently let a parallel win mask a per-core regression. Each kata's README quotes ratios *within* lanes, never *across* them.

The two-lane discipline locked in after kata #204 (2026-05-21) — see [`leetcode/201-300/204-count-primes/README.md § Comparison framing`](leetcode/201-300/204-count-primes/README.md) for the worked example.

## Template `bench.sh` structure

Each kata's `bench/bench.sh` follows this skeleton. The seq-only and seq+par variants share most of the structure; par-lane additions are flagged inline.

```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# Tool checks
require hyperfine "brew install hyperfine"
require rustc     "rustup (https://rustup.rs)"
require clang     "xcode-select --install / your distro's clang"
require go        "brew install go / your distro's golang"
require karac     "cargo install --path . --features llvm  (from karac-rust)"
# Par-lane only:
require cargo     "rustup (https://rustup.rs) — needed for the rayon variant"

# Build (cached, only rebuilds on source change)
build_rust <each>.rs
build_c    <each>.c
build_kara <each>.kara
build_go   go-seq   # builds bench/go-seq/main.go via its own go.mod
# Par-lane only:
build_kara <each>.kara   # the #[par_unordered] one
( cd rayon && cargo build --release --quiet )
cp -f rayon/target/release/<bin> target/<bin>
build_go   go-par

# Sink agreement — every mirror's stdout must be byte-identical before timing.
# Loop pattern handles N mirrors cleanly; see kata #204's bench.sh for the canonical shape.
for pair in "rust:$rust_sink" "c:$c_sink" "go_seq:$go_seq_sink" ...; do
    ...
done

# === runtime ===
# Short workloads (<50ms): --warmup 5 --runs 30 (startup jitter swamps the signal at 10 runs)
# Long workloads (>1s):   --warmup 2 --runs 10 (already <2% RSD at 10 runs; more is wasted wall)
# Mixed seq+par: one hyperfine call, all lanes interleaved (table presentation groups by lane).
hyperfine --warmup 3 --runs 10 --shell=none \
    --command-name 'kara count'                    './target/count_kara' \
    --command-name 'rust count (single-threaded)'  './target/count_rust' \
    --command-name 'c    count'                    './target/count_c' \
    --command-name 'go   count (single-threaded)'  './target/count_go_seq' \
    # Par lane (only when the workload has one):
    --command-name 'kara count (#[par_unordered])' './target/count_par_kara' \
    --command-name 'rust count (rayon par_iter)'   './target/count_rayon' \
    --command-name 'go   count (goroutines)'       './target/count_go_par'

# === runtime memory (peak) ===
print_mem '...' "$(mem_peak <command>)"
...

# === compile memory (cold) ===
# Per-language compile-memory rows. Rayon and Go are typically omitted —
# rayon is a multi-file Cargo project (incremental dep compile dominates),
# Go's `go build` mixes module resolution + std-lib link on first run.
# Both are different measurements from a single-file rustc/clang/karac invocation.
for src in <files>; do
    rm -f <artifact>
    print_mem "karac build $src" "$(mem_peak karac build "$src")"
    ...
done

# === compile elapsed (cold) ===
hyperfine --warmup 1 --runs 10 --shell=none \
    --prepare 'rm -f <artifacts>' \
    --command-name 'karac build <file>' 'karac build <file>' \
    --command-name 'rustc -O <file>' 'rustc -O <file> -o <out>' \
    --command-name 'clang -O3 <file>' 'clang -O3 <file> -o <out>'
```

The compile-elapsed block was added 2026-05-20 per [`karac-rust/brainstorming/archive/v69_go_parity_gaps.md § Gap 1`](../karac-rust/brainstorming/archive/v69_go_parity_gaps.md). The Go and rayon par-lane additions were locked 2026-05-21 from kata #204 — see that kata's `bench/bench.sh` for the canonical multi-language, multi-lane shape.

### Multi-language project structure under `bench/`

```text
bench/
├── bench.sh                # the driver
├── <approach>.kara         # single-file Kara mirror (seq, or seq+par if .kara
│                           #   carries #[par_unordered])
├── <approach>.rs           # single-file rustc -O mirror (seq)
├── <approach>.c            # single-file clang -O3 mirror (seq)
├── <approach>.py           # optional Python mirror (often sink-only)
├── go-seq/                 # Go seq variant — its own module
│   ├── go.mod
│   └── main.go
├── go-par/                 # Go par variant — its own module (par-lane only)
│   ├── go.mod
│   └── main.go
├── rayon/                  # Rust+rayon par variant — its own Cargo project (par-lane only)
│   ├── .gitignore          #   target/
│   ├── Cargo.toml          #   pins rayon version
│   ├── Cargo.lock          #   committed for reproducibility
│   └── src/main.rs
└── target/                 # bench-shared build output (gitignored)
    ├── <approach>_kara
    ├── <approach>          # rust
    ├── <approach>_c
    └── go_seq, go_par, <rayon>
```

Each compiled language that needs a project root (Go, Rust+rayon) gets its own subdir with a tiny manifest. Single-file mirrors (Kara, vanilla Rust, C, Python) sit flat in `bench/`. The shared `target/` collects all binaries so hyperfine can reference them uniformly.

## Output format

Per-kata `README.md` gains a **"Benchmarks"** section with sub-tables for runtime (split by lane), compile elapsed, binary size, and runtime/compile memory. Format mirrors the protocol below.

### Runtime — lane-aware table

When the kata has both seq and par lanes, interleave them with a `Lane` column so readers can do within-lane comparisons without doing arithmetic across rows:

```markdown
| Lane | Implementation | Wall time | User-CPU | CPU% |
|---|---|---|---|---|
| par | rust count (rayon par_iter)               | **36.7 ms ± 1.1 ms** | 561.4 ms | ~1530% (~15 cores) |
| par | **kāra count (codegen, #[par_unordered])** | **48.2 ms ± 3.3 ms** | 551.6 ms | ~1150% (~11 cores) |
| par | go   count (goroutines)                   | **50.4 ms ± 1.2 ms** | 523.8 ms | ~1040% (~10 cores) |
| seq | go   count                                | **456.0 ms ± 2.5 ms** | 489.8 ms | 107% |
| seq | **kāra count**                            | **509.8 ms ± 4.4 ms** | 505.0 ms | 99% |
| seq | c    count (clang -O3)                    | **511.3 ms ± 4.6 ms** | 506.9 ms | 99% |
| seq | rust count (rustc -O)                     | **512.5 ms ± 8.3 ms** | 507.1 ms | 99% |
```

Notes that should always accompany the table:

- The two-lane framing intro: "Both comparisons stay within their lane; cross-lane wall-time ratios are not meaningful."
- One paragraph per lane with the lane's headline finding, written as a within-lane ratio ("Kāra/C/Rust are within 0.5% of each other"; "Kāra `#[par_unordered]` is 1.31× slower than `rayon`").
- For seq-only katas, drop the `Lane` column and present a flat 4-row table (Kāra, Rust, C, Go).

### Compile elapsed (cold)

```markdown
### Compile elapsed (cold)

Snapshot — M5 Pro, 2026-XX-YY, hyperfine `--warmup 1 --runs 10 --shell=none`:

| Workload | Kāra (`karac build`) | Rust (`rustc -O`) | C (`clang -O3`) |
|---|---|---|---|
| `<approach>` | XX.X ± Y.Y ms | ZZ.Z ± W.W ms | UU.U ± V.V ms |
```

Multi-file projects (rayon Cargo project, Go modules) are deliberately excluded from the compile-elapsed table — `cargo build`'s first run includes dep resolution + link, and `go build`'s first run includes module resolution + std-lib link; neither is comparable to a single-file `rustc`/`clang`/`karac` invocation.

### Binary size, runtime memory, compile memory

Standard one-row-per-comparator tables. Include all lanes; binary size for Go is expected to be ~10× the others (Go statically links its runtime + GC + reflection — a deliberate Go design choice, called out in the per-table commentary).

### Numbers published here are reference data

The CI gate's source-of-truth aggregate lives in [`karac-rust/bench/compile_speed/`](../karac-rust/bench/compile_speed/README.md) (different corpus: curated subset + synthetic 10K-LOC stress program).

## Relationship to `karac-rust`

`kara-katas` is the runtime-perf benchmarking surface; it lives independently of the compiler repo. The `karac-rust/bench/compile_speed/` CI gate copies *selected* katas as plain files (no sync infrastructure) — selection evolves over time. Kāra-katas keeps the full kata corpus for runtime-perf signal; both publish compile-elapsed numbers per the protocol above.

## Coverage roadmap

The current kata corpus is algorithmic-shape (~100 LOC each, optimizer-heavy). The multi-quarter work to close sample-skew coverage gaps (backend-shape, generics-heavy, effect-heavy, concurrent katas) is tracked in [`PLAN.md`](PLAN.md).

## See also

- [`PLAN.md`](PLAN.md) — corpus coverage roadmap; five axes, priority ordering, "done when" criterion.
- [`leetcode/201-300/204-count-primes/`](leetcode/201-300/204-count-primes/) — worked example of the seq + par mixed-lane protocol locked 2026-05-21. Bench script, multi-language project layout (rayon + Go modules), README's lane-aware table presentation.
- [`karac-rust/bench/README.md`](../karac-rust/bench/README.md) — the karac-rust bench tracks (compile_speed CI gate + hash_quality / hot_swap_cost / indirection_cost microbenches).
- [`karac-rust/brainstorming/archive/v69_go_parity_gaps.md § Gap 1`](../karac-rust/brainstorming/archive/v69_go_parity_gaps.md) — resolution provenance for the compile-elapsed measurement protocol.
