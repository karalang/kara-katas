# Benchmarks

The full chart set, redrawn from [`bench-results.json`](bench-results.json) by
[`scripts/bench-graph.py`](scripts/bench-graph.py). Start at the
[README](README.md) for the short version; this page is the complete picture.

**How to read every chart below:** each dot is one benchmarked *program* (a
kata × algorithm-approach). Every value is relative to **Rust = 1.0** (the flat
baseline line); **lower is always better** (faster / smaller / leaner). Kāra is
the orange dots. The dots are deliberately *not* connected — left-to-right order
carries no meaning, so these read as distributions across the suite, not as
trends or time series. (As the corpus grows the dots pile into a density band per
language — that band, and where Kāra's sits relative to the baseline, is the
whole story.) Raw absolute numbers are in the feed.

Languages: **Kāra** (`karac build`), **Rust** (`rustc -O`), **C** (`clang -O3`),
**Go** (`go build`). Python is excluded from these charts — at 10–70× the
compiled languages it would flatten everything; its numbers are in the per-kata
READMEs and the JSON feed.

**One baseline caveat, made explicit:** Kāra checks integer overflow by default;
`rustc -O` **silently wraps**. So the gray `Rust = 1.0` baseline is *unsafe* Rust —
on a workload that exercises overflowing arithmetic it is doing strictly less work
than Kāra. The runtime chart therefore overlays a goldenrod **Rust (checked)** ring
— `rustc -O -C overflow-checks=on`, the safety-matched build — on the katas where
the two diverge. That is the apples-to-apples number. Across the corpus the overflow
tax is the bulk of every apparent "Kāra is slower" gap: the worst offenders (#171
1.66×, #9 1.46×, #8 1.41× vs `rust -O`) collapse to **0.99× / 1.08× / 1.15×** once
both languages check, and Kāra's own checked-arithmetic codegen is at *exact* parity
with Rust's in isolation. Kāra even emits **fewer** instructions than safety-matched
Rust on 16 of the corpus's collection/pointer kernels (linked lists, trees, maps,
backtracking — `karac`'s ownership/RC codegen). What survives equal-safety is a
handful of string-building kernels (1-byte `push_str` loops, ~1.2×) and the
low-cardinality sort in #1665 — both tracked.

## Runtime — sequential lane

Single-threaded, same algorithm everywhere. This is the load-bearing
per-core compiler-quality comparison.

![Runtime, sequential lane](graphs/runtime-seq.png)

Kāra's cloud tracks C's closely and sits at or below the **Rust (checked)** rings
on most programs — i.e. at parity with *safety-matched* Rust, ahead on the
collection/pointer kernels, with the only daylight to the gray `rust -O` baseline
being the overflow checks Rust opts out of by default (see the baseline caveat
above). The residual equal-safety gaps are string-building kernels and #1665's sort.
Go trails on most single-threaded work.

## Binary size — sequential lane

Stripped native binary, on disk. Log scale, because Go is ~70× the others.

![Binary size, sequential lane](graphs/binary-seq.png)

Kāra emits C-sized binaries (~33 KiB) for most programs and rises to its
~285 KiB compute floor when it links the larger runtime surface (hash maps,
strings). Rust sits ~14× above C; Go ~70× above, carrying its runtime + GC in
every binary.

## Runtime peak memory — sequential lane

Peak RSS during execution.

![Runtime peak memory, sequential lane](graphs/rss-seq.png)

Kāra, C, and Rust cluster at parity (~1.0×) — Kāra runs leak-free at native
footprint. Go's GC heap pushes it to 2–8× depending on allocation pressure.

## Compile time — cold

Wall-clock for a full cold compile of one file (artifact deleted first). Go is
omitted: `go build` bundles module resolution + multi-package compile + link,
which isn't comparable to a single-file compiler invocation.

![Compile time, cold](graphs/compile-elapsed.png)

Kāra's compiler is faster than `rustc -O` on every program here (~0.55–0.8×),
sitting between clang (the LLVM single-file floor) and rustc.

## Compile peak memory — cold

Peak RSS of the compiler process. Go omitted for the same reason as above.

![Compile peak memory, cold](graphs/compile-rss.png)

Kāra compiles in ~0.3× of rustc's peak memory — again between clang and rustc,
with no algorithmic blowup.

## Auto-parallel speedup (Kāra)

Kāra's compiler automatically parallelizes dependency-free reductions and maps —
no `rayon`, no goroutines, no thread plumbing, and no data-race risk, because the
transform belongs to the compiler, not to you. This chart is *intra-Kāra*: the
auto-par binary against the **exact same source** compiled sequentially.

![Kāra auto-parallel speedup](graphs/autopar-speedup.png)

This is the one place Kāra does something mainstream languages don't hand you for
free — which also makes it the easiest chart to over-read, so read it carefully:

- **It applies to data-parallel reductions/maps over large datasets** — `Σ f(xᵢ)`
  over millions of independent inputs, the shape behind analytics rollups,
  numeric kernels, simulation, per-record/per-pixel work. It does **nothing** for
  I/O-bound, tiny, or sequentially-dependent loops, and the compiler's **cost gate
  declines** to parallelize loops too small to pay off. That's exactly why #4's
  ~hundred-nanosecond kernel earns only 3.7× while #204's heavier kernel reaches
  13.4×, against an 18-core ceiling.
- **The speedup is workload- and core-bound physics, not a universal multiplier**
  on your program. The honest claim is *ergonomic, safe, automatic parallelization
  where it applies* — these numbers are evidence it scales, not a promise about
  arbitrary code.
- **This is a real distribution now (26 programs), not a teaser.** Every kata
  whose `karac build` engages auto-par contributes a point; the spread from the
  cost-gate floor up to ~13× against the 18-core ceiling is the spectrum, not a
  single illustrative number.

### Cross-language parallel lane

The *other* parallel comparison — Kāra auto-par (zero parallel source) vs Rust
`rayon` vs Go goroutines vs a C-pthreads metal floor on the same workload — is
the headline chart in the **[README](README.md#parallel-lane--auto-par-vs-hand-tuned)**:

![Runtime, auto-parallel lane — relative to Rust](graphs/runtime-par.png)

**31 programs** now ship the full parallel comparator set. Across them Kāra's
auto-par runs at a median **1.13× of hand-tuned `rayon`** (typically within
~10–15%, with zero parallel source), is **faster than `rayon` outright on seven**
(best #22 0.47×), wins against Go's goroutines on **24 of 31** (goroutine dispatch
overhead swamps fine-grained reductions), and **edges or matches the raw-pthreads
C floor on nine** of the allocation-heavy ones — for none of the engineering cost.
A handful of string-/allocation-churn kernels trail both C and Go (worst #71
simplify, ~8.8× of C); the chart shows them. Katas whose per-call work is too
small for rayon/goroutine dispatch to win (parallelizing them by hand would
*lose* to sequential) contribute only the intra-language auto-par speedup above
and stay seq-only here. More points land automatically as parallel katas are added.

## Caveats

The same honesty notes from the [README](README.md#what-these-numbers-are--and-arent)
apply: these are single-file algorithm kernels, not applications; wall-times are
noise-limited (shared M5 Pro), while size and memory are stable. Read the shape,
not the last digit, and consult [`bench-results.json`](bench-results.json) for
the underlying numbers.
