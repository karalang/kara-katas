# kara-katas — corpus coverage plan

> **Status:** Open, 2026-05-20. Tracks gaps in current corpus coverage and the work to close them. Implemented incrementally — one shape at a time. Sourced from `karac-rust/brainstorming/v69_go_parity_gaps.md § Gap 1` (sample-skew note).

## Current corpus snapshot

All katas today are **LeetCode-derived algorithmic challenges** (~100 LOC each, optimizer-heavy), distributed across `leetcode/1-100`, `101-200`, `201-300`, `1601-1700`, `3601-3700`. Each kata ships parallel `.kara` / `.py` / `.rs` implementations + a `bench/bench.sh` measuring runtime + compile-memory.

## Why the current corpus isn't enough

Algorithmic katas are **front-end-light**: small file count, few functions, no traits or generics beyond stdlib built-ins, no rich effect declarations. They exercise the optimizer (codegen, LLVM passes) well but systematically under-sample:

- Type-checker scaling with function count, generic instantiations, trait impl count
- Effect-checker scaling with effect-set size and resource-declaration count
- Ownership-analysis scaling with parameter modes, mutation patterns, RC fallback sites
- Front-end-vs-backend cost split at scale (where does wall-clock go at 10K LOC?)

This is the **kata sample skew** noted in `karac-rust/brainstorming/v69_go_parity_gaps.md § Gap 1`. Closing it is a multi-quarter effort; this plan tracks the work incrementally.

## Coverage dimensions

A complete benchmarking corpus measures along five axes. Each row is a `[ ]` checkbox so we can tick as we go.

### 1. Shape

- [x] **Algorithmic** — LeetCode-derived; covered today.
- [ ] **Backend service** — HTTP server with handlers, request/response, JSON parsing. Stresses IO + effects + concurrency.
- [ ] **CLI tool** — argument parsing, file IO, structured output. Stresses stdlib breadth.
- [ ] **Systems / data-pipeline** — file ingestion, transformation, write-out. Stresses allocation patterns + ownership.
- [ ] **Concurrent / par-heavy** — par-blocks, task groups, channels under load. Stresses scheduler + auto-concurrency runtime.

### 2. Scale (LOC)

- [x] **Small (~100 LOC)** — leetcode shape; covered today.
- [ ] **Medium (~1K LOC)** — single-file with multiple modules, fuller stdlib usage.
- [ ] **Large (~10K LOC)** — multi-file; the scale at which Go-shop engineers compare us. **Highest priority for closing sample skew.**

### 3. Language-feature stress

- [x] Arithmetic + arrays + loops — covered today.
- [ ] **Generics-heavy** — many `Vec[T]`, `Map[K,V]`, custom `[T: Ord]` functions.
- [ ] **Trait-heavy** — many trait impls, dynamic dispatch via trait objects (when supported).
- [ ] **Effect-heavy** — rich resource declarations + many effect-annotated public fns.
- [ ] **Ownership-stress** — mixed owned / `ref` / `mut ref` parameters extensively, including RC fallback sites.
- [ ] **Layout-stress** — `layout` blocks (SoA, field grouping) exercising the layout codegen path.

### 4. Stdlib breadth

- [x] `Array[T, N]`, `Slice[T]`, basic integer / float ops.
- [ ] `Vec[T]` workloads.
- [ ] `Map[K, V]` / `Set[T]` workloads — partial today (hash_map kata).
- [ ] `Option[T]` / `Result[T, E]` pattern-matching workloads.
- [ ] `String` / formatted-output workloads.
- [ ] `std.io` / `std.fs` workloads.
- [ ] `std.net` / `std.http` workloads — once Phase 8 Backend Platform spine lands.
- [ ] `std.par` / `std.task` workloads — par-blocks, task groups.
- [ ] `std.tracing` workloads — span propagation across a request.

### 5. Comparison targets

- [x] **Rust** — semantic peer; convergence target. Covered today.
- [x] **Python** — ergonomic foil. Covered today.
- [ ] **Go** — backend competitor. Add to backend-shape katas as a priority; defer for algorithmic katas (low information value).
- [ ] **C** — perf calibration. Add for inner-loop-dominated katas where the rustc gap is large.

## Priority ordering

1. **Backend-shape, medium scale, generics-heavy, with Go comparison — v1-required.** The highest-value single kata to add; closes multiple coverage gaps at once. Candidate: a small JSON-API server (e.g., a TODO list service) at ~500–1000 LOC. **This kata is also the real-shape public-quote number for the compile-speed gate in karac-rust** (per `karac-rust/brainstorming/v69_go_parity_gaps.md § Gap 1` resolution 2026-05-20, option 1). Without it, v1 cannot quote a backend-shape compile-time number against Rust or Go. Must land before v1.
2. **Synthetic 10K-LOC front-end-stress** — referenced from `karac-rust/bench/compile_speed/`. Lives in karac-rust, not here, but its patterns inform what this plan develops.
3. **Effect-heavy + ownership-stress katas** — once the backend-service shape exists, derive variants that pressure-test these axes.
4. **Concurrent / par-heavy katas** — after Phase 8 Backend Platform spine + concurrency runtime stabilizes.
5. **Stdlib-breadth fillers** — opportunistic; add as stdlib modules mature.

## "Done" criterion

This plan closes when:

1. At least one kata exists for each shape (5 rows under §1).
2. At least one kata at each scale (small / medium / large).
3. Each language-feature stress axis has at least one representative kata.
4. Each stdlib module that's part of the v1 commitment surface has at least one kata exercising it.

The corpus doesn't need to be exhaustive — it needs to be representative across the dimensions that produce different measurement results. A few well-chosen katas per axis beat a hundred algorithmic ones.

## Tracking new katas

When adding a kata that closes a coverage gap, tick the box above and add a one-line note linking to the kata's directory. Keep this doc current as the corpus grows.
