# kara-katas — bench protocol

Per-kata benchmark setup. Each kata under `leetcode/*/` ships a `bench/bench.sh` that compares Kāra against Rust, Python, and (where present) C implementations of the same algorithmic workload. This document is the protocol every kata `bench.sh` follows.

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

Per kata, ship parallel implementations:

- **Kāra**: `<approach>.kara` — the workload as written in Kāra. Built with `karac build` for codegen-mode runtime perf; also runnable via `karac run` for interpreter perf (where applicable).
- **Rust**: `<approach>.rs` — semantic peer. Same family as Kāra (LLVM, monomorphization, ownership). Built with `rustc -O`. The honest comparison.
- **Python**: `<approach>.py` — ergonomic foil. Establishes the "is the perf cliff worth the syntax?" framing.
- **C (optional)**: `<approach>.c` — perf calibration where the inner-loop-dominated gap to Rust is large. Adds `clang -O2` to the table; not required for every kata.

**Go translations** for the Go-comparison number: published at launch-time only, not on every kata's PRs. The karac-vs-go compile-time ratio is a launch deliverable with explicit framing ("Go optimizes for compile speed by design"); per-kata runtime Go numbers can be added opportunistically.

## Template `bench.sh` structure

Each kata's `bench/bench.sh` follows this skeleton:

```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# Tool checks
require hyperfine "brew install hyperfine"
require rustc     "rustup (https://rustup.rs)"
require karac     "cargo install --path . --features llvm  (from karac-rust)"

# Build (cached, only rebuilds on source change)
build_rust <each>.rs
build_kara <each>.kara

# === runtime — short workloads (codegen + python hash_map shape) ===
hyperfine --warmup 5 --runs 30 --shell=none \
    --command-name '...' '...' \
    ...

# === runtime — long workloads (interpreter shape) ===
hyperfine --warmup 2 --runs 10 --shell=none \
    --command-name '...' '...' \
    ...

# === runtime memory (peak) ===
print_mem '...' "$(mem_peak <command>)"
...

# === compile memory (cold) ===
for src in <files>; do
    rm -f <artifact>
    bytes=$(mem_peak karac build "$src")
    ...
done
for src in <rust files>; do
    rm -f <artifact>
    print_mem "rustc -O $src" "$(mem_peak rustc -O "$src" -o <out>)"
done

# === compile elapsed (cold) ===   [NEW — added 2026-05-20]
hyperfine --warmup 1 --runs 10 --shell=none \
    --prepare 'rm -f <artifacts>' \
    --command-name 'karac build <file>' 'karac build <file>' \
    --command-name 'rustc -O <file>' 'rustc -O <file> -o <out>'
```

The compile-elapsed block is the new piece (added 2026-05-20 per [`karac-rust/brainstorming/archive/v69_go_parity_gaps.md § Gap 1`](../karac-rust/brainstorming/archive/v69_go_parity_gaps.md)). It runs alongside the existing compile-memory block, using the same artifact-deletion-for-cold discipline but with hyperfine's repeated-measurement statistics instead of single-sample rusage.

## Output format

Per-kata `README.md` gains a **"Compile elapsed"** subsection alongside the existing "Codegen vs Rust" and "Codegen vs Python" tables. Format mirrors the runtime tables:

```markdown
### Compile elapsed (cold)

Snapshot — M5 Pro, 2026-XX-YY, hyperfine `--warmup 1 --runs 10 --shell=none`:

| Workload | Kāra (`karac build`) | Rust (`rustc -O`) | Gap |
|---|---|---|---|
| `brute_force` | XX.X ± Y.Y ms | ZZ.Z ± W.W ms | **N.Nx of Rust** |
| `hash_map`    | XX.X ± Y.Y ms | ZZ.Z ± W.W ms | **N.Nx of Rust** |
```

Numbers published here are **reference data** for the per-shape comparison. The CI gate's source-of-truth aggregate lives in [`karac-rust/bench/compile_speed/`](../karac-rust/bench/compile_speed/README.md) (different corpus: curated subset + synthetic 10K-LOC stress program).

## Relationship to `karac-rust`

`kara-katas` is the runtime-perf benchmarking surface; it lives independently of the compiler repo. The `karac-rust/bench/compile_speed/` CI gate copies *selected* katas as plain files (no sync infrastructure) — selection evolves over time. Kāra-katas keeps the full kata corpus for runtime-perf signal; both publish compile-elapsed numbers per the protocol above.

## Coverage roadmap

The current kata corpus is algorithmic-shape (~100 LOC each, optimizer-heavy). The multi-quarter work to close sample-skew coverage gaps (backend-shape, generics-heavy, effect-heavy, concurrent katas) is tracked in [`PLAN.md`](PLAN.md).

## See also

- [`PLAN.md`](PLAN.md) — corpus coverage roadmap; five axes, priority ordering, "done when" criterion.
- [`karac-rust/bench/README.md`](../karac-rust/bench/README.md) — the karac-rust bench tracks (compile_speed CI gate + hash_quality / hot_swap_cost / indirection_cost microbenches).
- [`karac-rust/brainstorming/archive/v69_go_parity_gaps.md § Gap 1`](../karac-rust/brainstorming/archive/v69_go_parity_gaps.md) — resolution provenance for the compile-elapsed measurement protocol.
