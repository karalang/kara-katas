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

**Because each `is_prime(k)` call is independent — no cross-iteration data dependency, no shared state.** That property makes the workload work equally well across two lanes of the bench: (a) single-threaded per-core measurement, where the algorithm shape is identical across compilers and the comparison stays honest; and (b) the parallel lane (Kāra `#[par_order_free]`, Rust `rayon`, Go goroutines + `sync.WaitGroup`), where workers fan out across cores with zero coordination. A sieve, by contrast, writes to a shared array of "is this number composite" flags; parallelizing it requires either a segmented sieve (complex), a wheel-based parallel sieve (more complex), or a lock-protected shared array (kills parallelism) — and the cross-iteration data dependency makes even the seq lane harder to compare apples-to-apples.

A future sieve-based kata for the *count-only* version of LC #204 (where the optimal algorithm is the sieve, parallelism is moot, and the comparison is purely per-core compiler quality on a memory-streaming workload) is filed separately.

## Kāra features exercised

- **`Vec[i64]` + `push`** — growable buffer holds the primes list; the bench workload uses this shape so the parallel-collect codegen path fires.
- **Integer-typed literals** — `2i64`, `0i64`, `3i64` keep the inner loop in `i64` end-to-end without coercion.
- **`while` with composite guard** — `while (i * i) <= n` avoids the sqrt call and stays in integer arithmetic.
- **`#[par_order_free]`** (bench only) — opts the outer collect-loop into auto-par codegen (see `bench/count.kara`). Spelled `#[par_unordered]` before 2026-07-30 (renamed in B-2026-07-29-30, because the old name asserted that the output *is* reordered when in fact both collect paths preserve iteration order today — the attribute is the caller's promise not to depend on order, not a claim about behaviour). The old spelling still parses as a deprecated alias.

## Running

```bash
karac run count.kara
python3 count.py
diff <(karac run count.kara) <(python3 count.py) && echo OK
```

## Benchmarks

Bench harness lives in [`bench/`](bench/). All four mirrors solve the same N = 10^7 list-primes workload; the sink is the pair `(count, sum) = (664579, 3203324994356)` — count matches π(10^7) per OEIS A006988, sum agrees byte-for-byte across kara/rust/c implementations. Hyperfine, 10 runs after 3 warmups, on Apple M5 Pro (6 perf + 12 efficiency cores), 2026-11-01, karac g6697158fa (v2/MIR backend).

### Comparison framing — two fair comparisons, both apples-to-apples

The bench is structured around two like-for-like comparisons. **Cross-lane comparisons (e.g. "auto-par Kāra vs single-threaded Rust") are not meaningful** — they conflate the language's compiler quality with whether the comparator opted into parallelism, and would silently let the parallel win mask any per-core regression. Both comparisons below stay within their lane:

1. **Per-core compiler quality** — single-threaded Kāra vs single-threaded Rust (`rustc -O`) vs C (`clang -O3`) vs Go. Same algorithm, no library help, no parallelism. Measures how well each compiler turns the source into machine code on one core. This is the comparison the kata is *primarily* for; mirrors the framing in kata-7 (reverse-integer), kata-8 (atoi), kata-65 (valid-number).
2. **Built-in/library parallelism** — `#[par_order_free]` Kāra (auto-par built into the language) vs `rayon` Rust (third-party crate) vs Go's goroutines + `sync.WaitGroup` (built into the runtime). All three explicitly opted into parallelism; the comparison is "is Kāra's first-iteration auto-par competitive with mature parallel implementations from neighboring languages?" Surfaces real karac gaps (see story 2 below).

The table below contains both comparisons interleaved; the per-iter `is_prime()` work is heavy enough that both comparisons land on stable numbers.

### Runtime

| Lane | Implementation | Wall time | User-CPU | CPU% |
|---|---|---|---|---|
| par | rust count (rayon par_iter)              | **37.8 ms ± 0.6 ms** | 563.1 ms | ~1520% (~15 cores) |
| par | c    count (pthreads — metal floor)      | **49.0 ms ± 2.8 ms** | 564.4 ms | ~1160% (~12 cores) |
| par | go   count (goroutines)                  | **53.7 ms ± 1.0 ms** | 528.9 ms | ~1040% (~10 cores) |
| par | **kāra count (codegen, #[par_order_free])** | **66.9 ms ± 2.7 ms** | 721.5 ms | ~1090% (~11 cores) |
| seq | go   count                               | **479.8 ms ± 3.3 ms** | 481.1 ms | 104% |
| seq | c    count (clang -O3)                   | **544.1 ms ± 1.7 ms** | 538.9 ms | 100% |
| seq | rust count (rustc -O)                    | **549.0 ms ± 2.6 ms** | 543.8 ms | 100% |
| seq | rust count (overflow-checks=on)          | **579.0 ms ± 6.0 ms** | 574.0 ms | 100% |
| seq | **kāra count**                           | **587.6 ms ± 7.8 ms** | 583.2 ms | 100% |

Lane check: the par build's emitted IR (`KARAC_MIR_LL`) carries one call of `karac_mir_task_spawn`; the `KARAC_AUTO_PAR=0` seq build (`count_seq.kara`) carries none.

Run `bench/bench.sh` to reproduce. Hyperfine, 10 runs after 3 warmups, M5 Pro under typical desktop load.

**Story 1 — per-core compiler quality (the kata's primary purpose).** Looking only at the seq lane: the Kāra-vs-Rust headline is the **equal-safety** row. Kāra checks integer overflow by default; `rustc -O` *silently wraps*, so the `rust -O` row (549 ms) runs a weaker safety contract. The apples-to-apples comparison is `rust -C overflow-checks=on` (579.0 ms), which restores the same checked trial-division arithmetic Kāra ships by default — and against it Kāra is at **parity, 1.01×** (588 vs 579 ms, about one σ apart). Kāra is 1.07× wrapping `rust -O`; most of that is the overflow-check safety tax (checked Rust is itself 1.05× `rust -O`), not codegen quality. C (544 ms) and clang, like `rust -O`, also skip the overflow checks, so the Kāra-vs-C 1.08× gap likewise folds the safety tax in. Go is the outlier at 480 ms (~17% faster than the checked rows); see *Why is Go single-thread faster?* below. **The Kāra compiler is at parity with equal-safety Rust on single-threaded code** — it hasn't traded compiler quality for higher-level features. A careful reader looking for "what's the actual codegen cost of using Kāra?" gets a clean answer: parity with equal-safety Rust, 1.07–1.08× unchecked C/Rust, 1.22× Go on this specific shape. Against the previous feed (2026-08-05) these ratios are flat: 1.05× → 1.07× Rust `-O`, 1.06× → 1.08× C, 1.21× → 1.22× Go.

**Story 2 — auto-parallelism vs library/runtime parallelism (a separate question with its own answer).** Kāra's `#[par_order_free]` is **1.77× slower than `rayon`**, **1.37× slower than hand-written pthreads C**, and **1.25× slower than Go's goroutines** (2026-08-05: 1.63×, 1.27×, 1.18× — flat within this session's noise band). Brand-new auto-par lands within 77% of Rust's mature `rayon` work-stealing library and behind Go's goroutine runtime — both have been hand-tuned for years. Go par spends ~529 ms user-CPU across ~10 cores and Kāra par ~722 ms across ~11 cores; rayon spends ~563 ms across ~15 cores. The Kāra-vs-rayon gap is concentrated in scheduler efficiency: rayon's per-worker deques + work-stealing distribute load better than karac's current single global queue + Condvar (the v1 MVP per `karac-rust/runtime/src/lib.rs § Pool`); Go's goroutine runtime sits at a comparable distribution efficiency to karac's MVP. The Phase 3 + 3.1 codegen work (worker-fn synthesis, amortized-doubling combine) is competitive with both rayon and Go at the worker-level; the runtime scheduler is the remaining gap, tracked at karac-rust `phase-7-codegen.md` line 163 ("real work-stealing scheduler") as the optimization target this comparison empirically validates.

### Why is Go single-thread faster?

Go beats C/Rust by ~12% and Kāra by ~18% on single-thread (480 ms vs 544–588 ms). On this exact workload (`is_prime` trial division + `append` to a growing slice), the gap is likely a combination of:
- **Aggressive inlining of `isPrime`.** Go's compiler inlines aggressively even at the default optimization level. Rust's `rustc -O` and C's `clang -O3` *should* also inline, but inliner heuristics differ; Go may be inlining a version that beats LLVM's choice here.
- **Slice growth strategy.** Go's `append` grows a slice with a different doubling/growth heuristic than Rust's `Vec::push` (Go's specifics: doubles up to 1024, then grows by 25% per resize). At ~664k final elements, this hits fewer realloc-and-copy steps than Rust's strict doubling.
- **No bounds checks on the loop variable.** Go's `for k := int64(0); k < n; k++` lowers without per-iter bounds checks because the loop variable is local; Rust's `for k in 0..n` should be equivalent, but karac currently emits a per-iter signed-comparison that LLVM may or may not eliminate.

These are speculative attributions; running the binaries through `llvm-mca` or `perf stat -e instructions` would localize the exact difference. The headline finding for the kata: **Go has a genuine per-core edge on this shape; C and Rust `-O` are at parity, with Kāra 1.07–1.08× behind them and at parity with equal-safety Rust.** No claim about Kāra's compiler being broken or backwards — just that there's a real per-core optimization opportunity surfaced by comparing against Go.

### Compile (cold)

| Implementation | Wall time |
|---|---|
| karac build count.kara | 153.3 ms ± 1.9 ms |
| rustc -O count.rs      | 92.5 ms ± 1.3 ms |
| clang -O3 count.c      | 50.5 ms ± 4.0 ms |

Kāra compiles ~3.0× slower than `clang -O3` and ~1.7× slower than `rustc -O`. Single-file builds aren't a stress test for the compiler — this number is dominated by LLVM mid-end passes (Kāra runs `default<O2>` per `src/codegen/optimization.rs`). The `rayon` row isn't included here because it's a multi-file Cargo project (incremental dep compile dominates and is a different measurement). The Go rows aren't included because `go build`'s first-run includes module resolution + std-lib link, and subsequent runs hit Go's build cache — neither is comparable to a single rustc/clang/karac single-file invocation.

### Binary size

| Implementation | Size |
|---|---|
| kara count (par)   |  377.1 KiB |
| kara count (seq)   |  295.8 KiB |
| rust count         |  455.6 KiB |
| rust+rayon count   |  451.8 KiB |
| go   count (seq)   | 2434.1 KiB |
| go   count (par)   | 2451.0 KiB |
| c    count         |   32.8 KiB |
| c    count (pthreads) | 33.0 KiB |

C is the smallest (no runtime). Every v2/MIR Kāra binary is now ~300–390 KB where the legacy backend's were ~34 KB (the 2026-08-05 seq binary was 33.5 KiB, within ~700 bytes of clang), tracked as [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md); the par build adds ~81 KiB over seq. Kāra parallel + seq + Rust + Rust+rayon all sit in the 295–456 KiB range (Kāra is *smaller* than both Rust variants — `rustc -O` defaults include panic-unwind + `std` overhead that Kāra doesn't). Go binaries are an order of magnitude larger (~2.4 MiB) because the Go runtime statically links the goroutine scheduler + GC + reflection metadata into every binary — that's a deliberate Go design choice for deployment simplicity. (Both kara binaries dropped ~16 KiB each from the recorded snapshot after the 2026-05-25 `__TEXT,__jittmpl` segment re-scope in karac `e76f42b`.)

### Runtime memory (peak)

| Implementation | Peak RSS |
|---|---|
| kara count (par)     | 14.8 MiB |
| kara count (seq)     |  8.2 MiB |
| rust count           |  8.3 MiB |
| rust+rayon count     | 15.7 MiB |
| go   count (seq)     | 22.6 MiB |
| go   count (par)     | 26.5 MiB |
| c    count           |  6.1 MiB |
| c    count (pthreads) | 11.4 MiB |

Kāra's parallel peak comes from the 10-worker thread pool (each with ~1 MiB stack reserved) + per-worker partial Vec slots during the merge. `rayon` and Go par sit in similar territory for the same reason (their thread/goroutine pools + per-worker partials). Kāra single-threaded skips the thread pool but still uses ~8 MiB — that's the `Vec[i64]` of 664k primes (~5 MiB live) plus the realloc-doubling overhead during growth. Go single-threaded sits at 23 MiB because Go's runtime allocates ~14 MiB of GC heap + stacks even before user code runs. Rust single-threaded is the smallest of the managed-language variants because Rust's `Vec::push` releases the old buffer mid-growth via a different path. C is the smallest overall because its bench pre-sizes the buffer at `cap = 700_000` and skips realloc entirely.

### Compile memory (cold)

| Implementation | Peak RSS |
|---|---|
| karac build count.kara | 56.5 MiB |
| rustc -O count.rs      | 27.1 MiB |
| clang -O3 count.c      |  2.6 MiB |

Kāra's compiler now holds ~2.1× `rustc -O`'s working set on this file (the 2026-05-25 snapshot measured 13.2 MiB, about half of rustc's; this run is the v2/MIR karac). Clang's small footprint reflects C's much simpler frontend.

## Caveats

- **N = 10⁷ is well above LC's max** (`n ≤ 5×10⁶`). The bench uses a larger N so the timed loop dominates startup/teardown overhead in hyperfine. At LC's actual limit (5M), wall times halve uniformly — same ratios within each lane, just less measurement headroom.
- **Order across the result `Vec` is unspecified** in the par lane. That's exactly why `#[par_order_free]` is required — it's the user's explicit opt-in to "I don't care about output order" semantics. For LC #204 (count only) and our bench (sum is order-invariant), this costs nothing. Workloads that need order-preservation would use a different reduction primitive (filed as a future karac-rust tracker entry).
