# 204. Count Primes

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Math, Number Theory, Array &nbsp;·&nbsp; **Source:** [leetcode.com/problems/count-primes](https://leetcode.com/problems/count-primes/)

Given an integer `n`, return the number of prime numbers strictly less than `n`.

```
n = 10   → 4   (primes < 10: 2, 3, 5, 7)
n = 0    → 0
n = 1    → 0
n = 100  → 25
```

**Constraints:** `0 ≤ n ≤ 5 × 10^6`.

## Approaches

| Approach | Complexity | Kāra | Python | Rust | C | Go |
|---|---|---|---|---|---|---|
| Trial division `is_prime(k)` over `[2, n)`, count matches | O(n·√n / ln n) time avg, O(π(n)) space if listing | [`count.kara`](count.kara) ✓ | [`count.py`](count.py) ✓ | [`bench/count.rs`](bench/count.rs) ✓ (bench septet) | [`bench/count.c`](bench/count.c) ✓ (bench septet) | [`bench/go-seq/main.go`](bench/go-seq/main.go) ✓ (bench septet) |

`✓` runs end-to-end today. Both `count.kara` and `count.py` emit `4, 25, 168, 1229, 9592` for the verification N's (10, 100, 1000, 10000, 100000) — matching OEIS A000720 (π(n), the prime-counting function).

## Why trial division, not the Sieve of Eratosthenes

The textbook solution to "count primes < n" is the Sieve of Eratosthenes — O(n log log n) time, O(n) space, beats trial division on any single-call benchmark. So why does this kata's bench use trial division?

**Because each `is_prime(k)` call is independent — no cross-iteration data dependency, no shared state.** That property makes the workload work equally well across two lanes of the bench: (a) single-threaded per-core measurement, where the algorithm shape is identical across compilers and the comparison stays honest; and (b) the parallel lane (Kāra `#[par_unordered]`, Rust `rayon`, Go goroutines + `sync.WaitGroup`), where workers fan out across cores with zero coordination. A sieve, by contrast, writes to a shared array of "is this number composite" flags; parallelizing it requires either a segmented sieve (complex), a wheel-based parallel sieve (more complex), or a lock-protected shared array (kills parallelism) — and the cross-iteration data dependency makes even the seq lane harder to compare apples-to-apples.

A future sieve-based kata for the *count-only* version of LC #204 (where the optimal algorithm is the sieve, parallelism is moot, and the comparison is purely per-core compiler quality on a memory-streaming workload) is filed separately.

## Kāra features exercised

- **`Vec[i64]` + `push`** — growable buffer holds the primes list; the bench workload uses this shape so the parallel-collect codegen path fires.
- **Integer-typed literals** — `2i64`, `0i64`, `3i64` keep the inner loop in `i64` end-to-end without coercion.
- **`while` with composite guard** — `while (i * i) <= n` avoids the sqrt call and stays in integer arithmetic.
- **`#[par_unordered]`** (bench only) — opts the outer collect-loop into auto-par codegen (see `bench/count.kara`).

## Running

```bash
karac run count.kara
python3 count.py
diff <(karac run count.kara) <(python3 count.py) && echo OK
```

## Benchmarks

Bench harness lives in [`bench/`](bench/). All four mirrors solve the same N = 10^7 list-primes workload; the sink is the pair `(count, sum) = (664579, 3203324994356)` — count matches π(10^7) per OEIS A006988, sum agrees byte-for-byte across kara/rust/c implementations. Hyperfine, 10 runs after 3 warmups, on Apple M5 Pro (6 perf + 12 efficiency cores).

### Comparison framing — two fair comparisons, both apples-to-apples

The bench is structured around two like-for-light comparisons. **Cross-lane comparisons (e.g. "auto-par Kāra vs single-threaded Rust") are not meaningful** — they conflate the language's compiler quality with whether the comparator opted into parallelism, and would silently let the parallel win mask any per-core regression. Both comparisons below stay within their lane:

1. **Per-core compiler quality** — single-threaded Kāra vs single-threaded Rust (`rustc -O`) vs C (`clang -O3`) vs Go. Same algorithm, no library help, no parallelism. Measures how well each compiler turns the source into machine code on one core. This is the comparison the kata is *primarily* for; mirrors the framing in kata-7 (reverse-integer), kata-8 (atoi), kata-65 (valid-number).
2. **Built-in/library parallelism** — `#[par_unordered]` Kāra (auto-par built into the language) vs `rayon` Rust (third-party crate) vs Go's goroutines + `sync.WaitGroup` (built into the runtime). All three explicitly opted into parallelism; the comparison is "is Kāra's first-iteration auto-par competitive with mature parallel implementations from neighboring languages?" Surfaces real karac gaps (see story 2 below).

The seven-row table below contains both comparisons interleaved; the per-iter `is_prime()` work is heavy enough that both comparisons land on stable numbers.

### Runtime

| Lane | Implementation | Wall time | User-CPU | CPU% |
|---|---|---|---|---|
| par | rust count (rayon par_iter)              | **35.0 ms ± 0.3 ms** | 561.0 ms | ~1590% (~16 cores) |
| par | **kāra count (codegen, #[par_unordered])** | **56.7 ms ± 1.4 ms** | 678.0 ms | ~1200% (~12 cores) |
| par | go   count (goroutines)                  | **48.3 ms ± 1.4 ms** | 513.0 ms | ~1070% (~11 cores) |
| seq | go   count                               | **431.5 ms ± 4.0 ms** | 459.0 ms | 108% |
| seq | **kāra count**                           | **521.1 ms ± 5.9 ms** | 517.0 ms | 99% |
| seq | c    count (clang -O3)                   | **487.9 ms ± 0.3 ms** | 484.0 ms | 99% |
| seq | rust count (rustc -O)                    | **494.5 ms ± 0.8 ms** | 491.0 ms | 99% |
| seq | rust count (overflow-checks=on)          | **519.6 ms ± 4.2 ms** | 516.0 ms | 99% |

Run `bench/bench.sh` to reproduce. Hyperfine, 10 runs after 3 warmups, M5 Pro under typical desktop load.

**Story 1 — per-core compiler quality (the kata's primary purpose).** Looking only at the seq lane: the Kāra-vs-Rust headline is the **equal-safety** row. Kāra checks integer overflow by default; `rustc -O` *silently wraps*, so the `rust -O` row (494 ms) runs a weaker safety contract. The apples-to-apples comparison is `rust -C overflow-checks=on` (519.6 ms), which restores the same checked trial-division arithmetic Kāra ships by default — and against it Kāra is at **dead parity, 1.00×** (521 vs 520 ms, inside σ). The residual ~5% gap to wrapping `rust -O` is the overflow-check safety tax, not codegen quality. C (487 ms) and clang, like `rust -O`, also skip the overflow checks, so the Kāra-vs-C ~7% gap likewise folds the safety tax in. Go is the outlier at 430 ms (~17% faster than the checked rows); see *Why is Go single-thread faster?* below. **The Kāra compiler is at parity with equal-safety Rust on single-threaded code** — it hasn't traded compiler quality for higher-level features. A careful reader looking for "what's the actual codegen cost of using Kāra?" gets a clean answer: parity with equal-safety Rust, ~7% vs unchecked C/Rust, ~21% behind Go on this specific shape.

**Story 2 — auto-parallelism vs library/runtime parallelism (a separate question with its own answer).** Kāra's `#[par_unordered]` is **1.61× slower than `rayon`** and **1.18× slower than Go's goroutines**. Brand-new auto-par lands within 61% of Rust's mature `rayon` work-stealing library and behind Go's goroutine runtime — both have been hand-tuned for years. Go par spends ~514 ms user-CPU across ~11 cores and Kāra par ~679 ms across ~12 cores; rayon spends ~561 ms across ~16 cores. The Kāra-vs-rayon gap is concentrated in scheduler efficiency: rayon's per-worker deques + work-stealing distribute load better than karac's current single global queue + Condvar (the v1 MVP per `karac-rust/runtime/src/lib.rs § Pool`); Go's goroutine runtime sits at a comparable distribution efficiency to karac's MVP. The Phase 3 + 3.1 codegen work (worker-fn synthesis, amortized-doubling combine) is competitive with both rayon and Go at the worker-level; the runtime scheduler is the remaining gap, tracked at karac-rust `phase-7-codegen.md` line 163 ("real work-stealing scheduler") as the optimization target this comparison empirically validates.

### Why is Go single-thread faster?

Go beats Kāra/C/Rust by ~14% on single-thread (430 ms vs ~500 ms). On this exact workload (`is_prime` trial division + `append` to a growing slice), the gap is likely a combination of:
- **Aggressive inlining of `isPrime`.** Go's compiler inlines aggressively even at the default optimization level. Rust's `rustc -O` and C's `clang -O3` *should* also inline, but inliner heuristics differ; Go may be inlining a version that beats LLVM's choice here.
- **Slice growth strategy.** Go's `append` grows a slice with a different doubling/growth heuristic than Rust's `Vec::push` (Go's specifics: doubles up to 1024, then grows by 25% per resize). At ~664k final elements, this hits fewer realloc-and-copy steps than Rust's strict doubling.
- **No bounds checks on the loop variable.** Go's `for k := int64(0); k < n; k++` lowers without per-iter bounds checks because the loop variable is local; Rust's `for k in 0..n` should be equivalent, but karac currently emits a per-iter signed-comparison that LLVM may or may not eliminate.

These are speculative attributions; running the binaries through `llvm-mca` or `perf stat -e instructions` would localize the exact difference. The headline finding for the kata: **Go has a genuine per-core edge on this shape, Kāra/C/Rust are at three-way parity.** No claim about Kāra's compiler being broken or backwards — just that there's a real per-core optimization opportunity surfaced by comparing against Go.

### Compile (cold)

| Implementation | Wall time |
|---|---|
| karac build count.kara | 76.1 ms ± 1.8 ms |
| rustc -O count.rs      | 93.0 ms ± 1.5 ms |
| clang -O3 count.c      | 45.9 ms ± 0.4 ms |

Kāra compiles ~1.7× slower than `clang -O3`, ~1.2× faster than `rustc -O`. Single-file builds aren't a stress test for the compiler — this number is dominated by LLVM mid-end passes (Kāra runs `default<O2>` per `src/codegen/optimization.rs`). The `rayon` row isn't included here because it's a multi-file Cargo project (incremental dep compile dominates and is a different measurement). The Go rows aren't included because `go build`'s first-run includes module resolution + std-lib link, and subsequent runs hit Go's build cache — neither is comparable to a single rustc/clang/karac single-file invocation.

### Binary size

| Implementation | Size |
|---|---|
| kara count (par)   |  296.1 KiB |
| kara count (seq)   |   33.2 KiB |
| rust count         |  455.6 KiB |
| rust+rayon count   |  451.8 KiB |
| go   count (seq)   | 2434.1 KiB |
| go   count (par)   | 2451.0 KiB |
| c    count         |   32.8 KiB |

C is the smallest (no runtime). Kāra single-thread is **within ~150 bytes of clang** at 33.2 KiB — the par-reduce surface only links in when something references it. Kāra parallel + Rust + Rust+rayon all sit in the 295-455 KiB range (Kāra is *smaller* than both Rust variants — `rustc -O` defaults include panic-unwind + `std` overhead that Kāra doesn't). Go binaries are an order of magnitude larger (~2.4 MiB) because the Go runtime statically links the goroutine scheduler + GC + reflection metadata into every binary — that's a deliberate Go design choice for deployment simplicity. (Both kara binaries dropped ~16 KiB each from the recorded snapshot after the 2026-05-25 `__TEXT,__jittmpl` segment re-scope in karac `e76f42b`.)

### Runtime memory (peak)

| Implementation | Peak RSS |
|---|---|
| kara count (par)     | 22.8 MiB |
| kara count (seq)     |  8.2 MiB |
| rust count           |  8.3 MiB |
| rust+rayon count     | 15.9 MiB |
| go   count (seq)     | 22.9 MiB |
| go   count (par)     | 24.3 MiB |
| c    count           |  6.1 MiB |

Kāra's parallel peak comes from the 10-worker thread pool (each with ~1 MiB stack reserved) + per-worker partial Vec slots during the merge. `rayon` and Go par sit in similar territory for the same reason (their thread/goroutine pools + per-worker partials). Kāra single-threaded skips the thread pool but still uses ~8 MiB — that's the `Vec[i64]` of 664k primes (~5 MiB live) plus the realloc-doubling overhead during growth. Go single-threaded sits at 23 MiB because Go's runtime allocates ~14 MiB of GC heap + stacks even before user code runs. Rust single-threaded is the smallest of the managed-language variants because Rust's `Vec::push` releases the old buffer mid-growth via a different path. C is the smallest overall because its bench pre-sizes the buffer at `cap = 700_000` and skips realloc entirely.

### Compile memory (cold)

| Implementation | Peak RSS |
|---|---|
| karac build count.kara | 13.2 MiB |
| rustc -O count.rs      | 27.1 MiB |
| clang -O3 count.c      |  2.5 MiB |

Kāra's compiler holds a much smaller working set than `rustc -O` (no incremental-compile cache, no macro expansion, simpler type system). Clang's small footprint reflects C's much simpler frontend.

## Caveats

- **N = 10⁷ is well above LC's max** (`n ≤ 5×10⁶`). The bench uses a larger N so the timed loop dominates startup/teardown overhead in hyperfine. At LC's actual limit (5M), wall times halve uniformly — same ratios within each lane, just less measurement headroom.
- **Order across the result `Vec` is unspecified** in the par lane. That's exactly why `#[par_unordered]` is required — it's the user's explicit opt-in to "I don't care about output order" semantics. For LC #204 (count only) and our bench (sum is order-invariant), this costs nothing. Workloads that need order-preservation would use a different reduction primitive (filed as a future karac-rust tracker entry).
