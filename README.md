# Kāra Katas

Classic algorithm problems (LeetCode-style) implemented in **[Kāra](https://github.com/karalang/kara)** and mirrored, algorithm-for-algorithm, in **C, Rust, Go, and Python**. The corpus does double duty: it exercises the Kāra compiler against real code, and it benchmarks Kāra's compiled output against mainstream languages on identical workloads.

Kāra is a young systems language. The point of the charts below is narrow and honest: on these problems, Kāra's compiled output already lands *in the pack* with C, Rust, and Go — not in some "early experiment" tier off to the side.

## Runtime — sequential lane

Single-threaded, same algorithm in every language, native binaries (`karac build` / `rustc -O` / `clang -O3` / `go build`). Each dot is one benchmarked program; lower is faster; everything is relative to Rust = 1.0. The dots aren't connected by a line because left-to-right order is meaningless — read it as a distribution, not a trend.

![Runtime, sequential lane — relative to Rust](graphs/runtime-seq.svg)

Kāra's orange dots sit clustered around the Rust baseline — ahead on the allocation- and string-heavy workloads, behind on a couple, tracking C's green cloud closely. It loses on some programs, and the chart shows that plainly.

## Binary size

![Binary size, sequential lane — relative to Rust, log scale](graphs/binary-seq.svg)

Kāra emits **C-sized binaries** (~33 KiB) for most programs, rising to its ~285 KiB compute floor when a program pulls in the larger runtime surface (hash maps, strings). Either way it sits far below Rust, and roughly **70× smaller than Go**, which carries its runtime + GC in every binary.

## The rest of the picture

Five more charts — compile time, compile memory, runtime memory, Kāra's automatic-parallelization speedup, and the methodology behind all of them — live in **[BENCHMARKS.md](BENCHMARKS.md)**.

## What these numbers are — and aren't

- **Same algorithm, same workload** per program, across all languages. The comparison is of *compiled output and runtime quality*, not of who can write the cleverest solution.
- These are **single-file algorithm kernels**, not whole applications. They measure codegen and runtime behavior on tight loops; they do **not** claim to predict real-world application performance.
- **Wall-time numbers are noise-limited** (measured on a shared M5 Pro under load) — treat them as approximate and read the *shape*, not the third digit. The deterministic metrics (binary size, peak memory) are stable run-to-run.
- Raw data for every chart lives in **[`bench-results.json`](bench-results.json)**; the measurement protocol is **[BENCH.md](BENCH.md)**.

## Reproducing

Each kata ships a `bench/bench.sh` that builds every language's mirror, checks they all print the same result, then times and measures them:

```bash
brew install hyperfine          # also needs karac, rustc, clang, go
cd leetcode/1-100/1-two-sum/bench && ./bench.sh   # writes bench/results.json

./scripts/consolidate-bench.sh  # merge all per-kata results → bench-results.json
python3 scripts/bench-graph.py  # redraw graphs/*.svg from the consolidated feed
```
