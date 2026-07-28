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
`rustc -O` **silently wraps** — defined behavior (not UB), but a wrong value where
Kāra would trap. So the gray **Rust (default)** baseline is doing strictly less work
than Kāra on a workload that exercises overflowing arithmetic. The runtime chart therefore overlays a goldenrod **Rust (checked)** ring
— `rustc -O -C overflow-checks=on`, the safety-matched build — on the katas where
the two diverge. That is the apples-to-apples number. Across the corpus the overflow
tax is the bulk of every apparent "Kāra is slower" gap: the worst offenders (#171
1.66×, #9 1.46×, #8 1.41× vs `rust -O`) collapse to **0.99× / 1.08× / 1.15×** once
both languages check, and Kāra's own checked-arithmetic codegen is at *exact* parity
with Rust's in isolation. Kāra even emits **fewer** instructions than safety-matched
Rust on 16 of the corpus's collection/pointer kernels (linked lists, trees, maps,
backtracking — `karac`'s ownership/RC codegen). What survives equal-safety is a
handful of string-shaped kernels (~1.2×) and the low-cardinality sort in #1665 —
both tracked.

**Retracted, and what actually happened (2026-07-28).** An earlier revision of
this file held six katas (#128, #133, #141, #160, #242, #290) out of the feed,
attributing their multi-threaded `seq` lanes to nondeterministic runtime
auto-par in `karac 3e9a12ed`. **That attribution was wrong.** All 244 katas are
back in the feed; nothing about the compiler was at fault.

The cause was in this repo's own harness. Both compile-cost lanes rebuilt the
kāra binary to time a cold `karac build` — *without* `KARAC_AUTO_PAR=0` — and
then `mv`'d the result over `target/<stem>_kara`, the exact artifact the seq
runtime lane, `size_put` and `mem_put` read. Two consequences:

- `size_put` / `mem_put` run after `ce_end`, so on **81 of 240** katas (every
  one where the seq and default builds differ) binary size and peak RSS were
  measured on the auto-par binary while runtime was measured on the seq binary
  — mixed provenance inside a single `results.json`.
- The *next* run of the same `bench.sh` found a "fresh" auto-par binary, so
  `build_kara`'s mtime guard skipped the rebuild and the runtime lane silently
  timed a **parallel** binary in a lane labelled `seq`.

That second effect is what the six were. It only bites on a **re-bench**, which
is why the x86 container — which benches each kata once — always read 99.8% CPU
and appeared to exonerate the compiler. The corrections are large:

| kata | published (poisoned) | corrected | inflation |
|---|---|---|---|
| #242 | 9.51 ms @ 1178% | 96.49 ms @ 99.4% | **10.1×** |
| #133 | 25.09 ms @ 1306% | 182.02 ms @ 98.9% | **7.3×** |
| #128 | 9.39 ms @ 1068% | 67.43 ms @ 99.2% | **7.2×** |
| #160 | 23.87 ms @ 1042% | 156.59 ms @ 99.6% | **6.6×** |
| #290 | 40.45 ms @ 1008% | 152.77 ms @ 99.5% | 3.8× |
| #141 | 156.27 ms @ 674% | 205.45 ms @ 99.6% | 1.3× |

#133's poisoned figure is dated **2026-06-15** — this defect has been inflating
published Kāra seq numbers, in Kāra's own favour, for at least six weeks. Fixed
by retargeting both compile-cost lanes to a throwaway `<stem>_kara.ce` path
(202 `bench.sh` + `scripts/new-bench.sh`); the measured binary is never touched.
Corpus-wide check after the fix: **0** katas show a kāra `seq` lane above 150%
CPU.

**Provenance of this feed — three compiler generations.** 99 katas measured on
`karac 7db7009e` with the fixed harness, 77 on `3e9a12ed`, 68 on older June/July
builds. Only the 81 katas whose seq and default builds differ needed
re-measuring for the fix (on the rest the two builds are byte-identical, so the
clobber was a no-op); the remainder were left on their original toolchain rather
than re-run. The corpus-level median below therefore averages across three
compilers and is softer than a single number implies.

**A known-flaky kata.** #133's hand-written `par {}` binary exits on SIGTRAP in
roughly **1.7%** of runs (1 in 60, silent, no diagnostic). At that rate a
35-invocation hyperfine batch fails ~45% of the time, so its par-lane numbers
should be treated as provisional. Whether this is a regression is **not**
established — the June run's success is equally consistent with "worked then"
and "was already flaky and got lucky."

**What the overflow tax actually is, measured (2026-07-27).** The phrase "overflow
tax" undersells the mechanism on array kernels: checked arithmetic does not add a
few instructions per iteration, it **forfeits vectorization entirely**. Disassembled
on the M5 for [#122](leetcode/101-200/122-best-time-to-buy-and-sell-stock-ii/)
(`profit += max(0, p[i]-p[i-1])` over 2M `i64`), inside the *same* Rust symbol:

| build | vector instrs | overflow-check branches | mean |
|---|---|---|---|
| `rustc -O` (wraps) | **240** | 0 | 6.4 ms |
| `rustc -O -C overflow-checks=on` | **0** | 29 | 15.6 ms |
| `karac` (checks by default) | **0** | per-op `b.vs`/`b.vc` | 14.4 ms |

So Kāra's apparent 2.3× deficit against `rustc -O` on this kata is a vectorized-vs-
scalar comparison wearing a costume, and against the safety-matched build Kāra is
**ahead** (14.4 vs 15.6 ms). Rust forfeits exactly the same vectorization when asked
for the same guarantee — this is the price of the contract, not a `karac` codegen
gap. It also sets the ceiling on what fixing checked-arithmetic codegen could ever
recover on such kernels: ~2.4×, and only by teaching the vectorizer to keep the
checks, which neither compiler does today.

**Correction (2026-07-26):** the string-shaped residual was long attributed to
1-byte `push_str` loops. Measured on
[#127](leetcode/101-200/127-word-ladder/), that attribution is **wrong**: a
104k-iteration char-by-char `String` build is a dead tie with Rust (5.5 ms vs
5.4 ms), while building and probing a `Map[String, _]` of 3,125 keys is
**2.45×** behind an equal-hash Rust `HashMap` (37.9 ms vs 15.5 ms). Filed as
`B-2026-07-26-2`.

**Correction to the correction (same day, after acting on it).** The sentence
above originally continued "— and that one ratio accounts for the whole kata
deficit." That was an *inference from a microbenchmark*, and it did not
survive contact with a fix. Two measured improvements to the String-keyed map
landed in `karac` (a direct rehash on growth, and a monomorphised String-key
lookup probe; ~1.13× each on the path each targets) and **#127 did not move**
— 1.82× against the equal-hash Rust lane afterwards versus 1.62× before, i.e.
unchanged within this container's cross-session variance. The reason is
visible once looked for: ~20 of every 25 candidate lookups in #127 **miss**,
and a miss stops at the first empty bucket — one byte load, no comparison — so
the probe was never that kata's hot path.

The map really is ~2× behind and that is worth fixing on its own merits. But
**where a corpus-level deficit lives has to be established by intervention,
not by an isolated microbenchmark** — on this bug, isolated benchmarks
predicted the wrong culprit twice running.

**A second baseline caveat — CPU baseline, found 2026-07-26 and not yet
corrected corpus-wide.** `karac build` targets **`x86-64-v3`** (Haswell+, AVX2)
by default on x86-64 — a deliberate deploy-baseline commitment in the language
design (`cpu-baseline = "v3"`), not an accident. `clang -O3` and `rustc -O` at
*their* defaults target **`x86-64` v1** (SSE2). So on x86 hosts every lane in
this corpus compares an AVX2 Kāra binary against baseline-ISA C and Rust.

How much that is worth depends entirely on whether the kernel vectorizes:

- On the **vast majority** of the corpus — pointer chasing, maps, trees,
  backtracking, string building, branchy DP — it is worth nothing measurable,
  because none of it vectorizes at any baseline.
- On a **vectorizable array kernel** it is worth a lot. Measured on
  [#260](leetcode/201-300/260-single-number-iii/) (a two-pass XOR over 200k
  `i64`): Kāra appears **1.44× ahead of C** at the two languages' defaults, and
  the entire lead evaporates — a four-way tie inside 1.06× — once C and Rust are
  rebuilt with `-march=x86-64-v3` / `-C target-cpu=x86-64-v3`. Forcing Kāra down
  to `--target-cpu=x86-64` costs it the same 1.4×.

Every previously published number in this corpus was measured before this was
noticed. Nothing is being withdrawn — the bias is one-directional and only bites
where SIMD applies, which is a small minority of these kernels, and it did not
manufacture Kāra's *losses* (e.g. [#137](leetcode/101-200/137-single-number-ii/)
loses 7.9× to C **with** AVX2 in hand). But **any Kāra win on an array kernel
should be re-checked at equal baseline before it is quoted**, and new
array-shaped katas carry an explicit equal-baseline lane, the same way the
equal-safety `rust_ovf` lane works above. The apples-to-apples comparison
matches *both* axes: equal safety **and** equal ISA baseline.

**Corpus-wide correction landed (2026-07-27).** The equal-baseline lane is no
longer per-kata and opt-in. `scripts/bench-lib.sh` now carries `isa_build_c` /
`isa_build_rust` / `isa_rt_cmds`, wired into every migrated `bench.sh` (226 of
244; the 18 multi-approach katas still need doing by hand). They add two twins:

- **`c_v3`** — `clang -O3 -march=x86-64-v3`
- **`rust_v3`** — `rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`, matched
  on *both* axes at once, and therefore the single honest apples-to-apples number

Each twin's output is verified against the Kāra binary's sink before it is timed,
so a twin that traps or diverges is dropped with a warning rather than measured.
Charts render them as optional overlays; the out-of-the-box `rust` / `c` lanes
stay in the feed, because "what a user gets by default" is a real and separate
question from "whose codegen is better." Both are published; neither is allowed
to stand in for the other.

**These lanes are x86-only, and that is a measured decision, not an assumption.**
On aarch64 the helpers are deliberate no-ops. Checked on the M5 (2026-07-27):
`clang` defaults to `-mcpu=apple-m1` and `rustc` likewise, and rebuilding at
`-mcpu=generic` produces different binaries but statistically identical times
(6.3–6.8 ms, σ 0.7–0.9 on #122). Forcing the lane on via `BENCH_ISA_FORCE=1
ISA_LEVEL=native` confirms it from the other side: `c_v3` 5.93 ms vs `c` 5.93 ms,
`rust_v3` 16.39 ms vs `rust_ovf` 16.36 ms. There is no ARM baseline gap to
correct, so the Apple-Silicon numbers in this corpus never carried this caveat.

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
