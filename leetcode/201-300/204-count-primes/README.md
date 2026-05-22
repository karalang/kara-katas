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

## Implementation

```kara
fn is_prime(n: i64) -> bool {
    if n < 2i64 { return false; }
    if n == 2i64 { return true; }
    if (n % 2i64) == 0i64 { return false; }
    let mut i: i64 = 3i64;
    while (i * i) <= n {
        if (n % i) == 0i64 { return false; }
        i = i + 2i64;
    }
    return true;
}

fn list_primes_under(n: i64) -> Vec[i64] {
    let mut primes: Vec[i64] = Vec.new();
    let mut k: i64 = 0i64;
    while k < n {
        if is_prime(k) {
            primes.push(k);
        }
        k = k + 1i64;
    }
    return primes;
}

fn count_primes(n: i64) -> i64 {
    return list_primes_under(n).len();
}
```

Two helpers exposed at the top level:

- **`is_prime(n)`** — trial division up to `√n`. Early-exits on divisibility by 2, then walks only odd factors. This keeps the inner loop's work proportional to `√n / 2` per *prime* candidate; composites are typically rejected after one or two trial divisions, so the average per-iter cost across `[0, n)` is much lower than the worst case.
- **`list_primes_under(n)`** — collects primes into a `Vec[i64]`. The bench workload uses this shape so the parallel-collect codegen path fires.
- **`count_primes(n)`** — LC #204's contract: returns the count. Built on `list_primes_under(n).len()` so the LC test cases share a single codepath with the bench.

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
| par | rust count (rayon par_iter)              | **36.7 ms ± 1.1 ms** | 561.4 ms | ~1530% (~15 cores) |
| par | **kāra count (codegen, #[par_unordered])** | **48.2 ms ± 3.3 ms** | 551.6 ms | ~1150% (~11 cores) |
| par | go   count (goroutines)                  | **50.4 ms ± 1.2 ms** | 523.8 ms | ~1040% (~10 cores) |
| seq | go   count                               | **456.0 ms ± 2.5 ms** | 489.8 ms | 107% |
| seq | **kāra count**                           | **509.8 ms ± 4.4 ms** | 505.0 ms | 99% |
| seq | c    count (clang -O3)                   | **511.3 ms ± 4.6 ms** | 506.9 ms | 99% |
| seq | rust count (rustc -O)                    | **512.5 ms ± 8.3 ms** | 507.1 ms | 99% |

Run `bench/bench.sh` to reproduce. Hyperfine, 10 runs after 3 warmups, M5 Pro under typical desktop load.

**Story 1 — per-core compiler quality (the kata's primary purpose).** Looking only at the seq lane: Kāra (510 ms), C (511 ms), and Rust (513 ms) are within **0.5% of each other** — essentially identical. Go is the outlier at 456 ms (11% faster than the others); see *Why is Go single-thread faster?* below. **The Kāra compiler is at parity with both Rust and C on single-threaded code.** No claim of a per-core advantage; the kata's value here is the *demonstration* that Kāra hasn't traded compiler quality for higher-level features. A careful reader looking for "what's the actual codegen cost of using Kāra?" gets a clean answer: ~0% vs C/Rust, ~12% behind Go on this specific shape.

**Story 2 — auto-parallelism vs library/runtime parallelism (a separate question with its own answer).** Kāra's `#[par_unordered]` is **1.31× slower than `rayon`** and **1.05× faster than Go's goroutines**. Brand-new auto-par lands within 31% of Rust's mature `rayon` work-stealing library *and* slightly ahead of Go's goroutine runtime — both have been hand-tuned for years. Kāra par + Go par both spend ~525-550 ms user-CPU across ~10-11 cores; rayon spends ~561 ms across ~15 cores. The Kāra-vs-rayon gap is concentrated in scheduler efficiency: rayon's per-worker deques + work-stealing distribute load better than karac's current single global queue + Condvar (the v1 MVP per `karac-rust/runtime/src/lib.rs § Pool`); Go's goroutine runtime sits at a comparable distribution efficiency to karac's MVP. The Phase 3 + 3.1 codegen work (worker-fn synthesis, amortized-doubling combine) is competitive with both rayon and Go at the worker-level; the runtime scheduler is the remaining gap, tracked at karac-rust `phase-7-codegen.md` line 163 ("real work-stealing scheduler") as the optimization target this comparison empirically validates.

### Why is Go single-thread faster?

Go beats Kāra/C/Rust by 11% on single-thread (456 ms vs ~510 ms). On this exact workload (`is_prime` trial division + `append` to a growing slice), the gap is likely a combination of:
- **Aggressive inlining of `isPrime`.** Go's compiler inlines aggressively even at the default optimization level. Rust's `rustc -O` and C's `clang -O3` *should* also inline, but inliner heuristics differ; Go may be inlining a version that beats LLVM's choice here.
- **Slice growth strategy.** Go's `append` grows a slice with a different doubling/growth heuristic than Rust's `Vec::push` (Go's specifics: doubles up to 1024, then grows by 25% per resize). At ~664k final elements, this hits fewer realloc-and-copy steps than Rust's strict doubling.
- **No bounds checks on the loop variable.** Go's `for k := int64(0); k < n; k++` lowers without per-iter bounds checks because the loop variable is local; Rust's `for k in 0..n` should be equivalent, but karac currently emits a per-iter signed-comparison that LLVM may or may not eliminate.

These are speculative attributions; running the binaries through `llvm-mca` or `perf stat -e instructions` would localize the exact difference. The headline finding for the kata: **Go has a genuine per-core edge on this shape, Kāra/C/Rust are at three-way parity.** No claim about Kāra's compiler being broken or backwards — just that there's a real per-core optimization opportunity surfaced by comparing against Go.

### Compile (cold)

| Implementation | Wall time |
|---|---|
| karac build count.kara | 58.7 ms ± 1.3 ms |
| rustc -O count.rs      | 86.3 ms ± 3.2 ms |
| clang -O3 count.c      | 41.5 ms ± 1.2 ms |

Kāra compiles ~1.4× slower than `clang -O3`, ~1.5× faster than `rustc -O`. Single-file builds aren't a stress test for the compiler — this number is dominated by LLVM mid-end passes (Kāra runs `default<O2>` per `src/codegen/optimization.rs`). The `rayon` row isn't included here because it's a multi-file Cargo project (incremental dep compile dominates and is a different measurement). The Go rows aren't included because `go build`'s first-run includes module resolution + std-lib link, and subsequent runs hit Go's build cache — neither is comparable to a single rustc/clang/karac single-file invocation.

### Binary size

| Implementation | Size |
|---|---|
| kara count (par)   |  311.9 KiB |
| kara count (seq)   |   49.0 KiB |
| rust count         |  455.6 KiB |
| rust+rayon count   |  451.8 KiB |
| go   count (seq)   | 2434.1 KiB |
| go   count (par)   | 2451.0 KiB |
| c    count         |   32.8 KiB |

C is the smallest (no runtime). Kāra single-thread is next at 49 KiB — the par-reduce surface only links in when something references it. Kāra parallel + Rust + Rust+rayon all sit in the 300-500 KiB range (Kāra is *smaller* than both Rust variants — `rustc -O` defaults include panic-unwind + `std` overhead that Kāra doesn't). Go binaries are an order of magnitude larger (~2.4 MiB) because the Go runtime statically links the goroutine scheduler + GC + reflection metadata into every binary — that's a deliberate Go design choice for deployment simplicity.

### Runtime memory (peak)

| Implementation | Peak RSS |
|---|---|
| kara count (par)     | 23.1 MiB |
| kara count (seq)     | 14.2 MiB |
| rust count           |  8.3 MiB |
| rust+rayon count     | 15.9 MiB |
| go   count (seq)     | 21.0 MiB |
| go   count (par)     | 27.2 MiB |
| c    count           |  6.2 MiB |

Kāra's parallel peak comes from the 10-worker thread pool (each with ~1 MiB stack reserved) + per-worker partial Vec slots during the merge. `rayon` and Go par sit in similar territory for the same reason (their thread/goroutine pools + per-worker partials). Kāra single-threaded skips the thread pool but still uses ~14 MiB — that's the `Vec[i64]` of 664k primes (~5 MiB live) plus the realloc-doubling overhead during growth. Go single-threaded sits at 21 MiB because Go's runtime allocates ~14 MiB of GC heap + stacks even before user code runs. Rust single-threaded is the smallest of the managed-language variants because Rust's `Vec::push` releases the old buffer mid-growth via a different path. C is the smallest overall because its bench pre-sizes the buffer at `cap = 700_000` and skips realloc entirely.

### Compile memory (cold)

| Implementation | Peak RSS |
|---|---|
| karac build count.kara |  9.2 MiB |
| rustc -O count.rs      | 27.2 MiB |
| clang -O3 count.c      |  2.6 MiB |

Kāra's compiler holds a much smaller working set than `rustc -O` (no incremental-compile cache, no macro expansion, simpler type system). Clang's small footprint reflects C's much simpler frontend.

## Caveats

- **N = 10⁷ is well above LC's max** (`n ≤ 5×10⁶`). The bench uses a larger N so the timed loop dominates startup/teardown overhead in hyperfine. At LC's actual limit (5M), wall times halve uniformly — same ratios within each lane, just less measurement headroom.
- **Cross-lane wall-time ratios are not the comparison this kata is for.** "Auto-par Kāra is N× faster than single-threaded Rust" is technically true at any N, but it's apples-to-oranges (parallel dispatch vs single-core codegen) and would silently let a parallel win hide a per-core regression. Both lanes have their own comparator in the table; readers checking compiler quality should look at the **seq lane** (kara vs rust vs c vs go), and readers checking parallel-runtime quality should look at the **par lane** (kara `#[par_unordered]` vs `rayon` vs Go goroutines). Mixing them is the user-CPU vs wall-clock confusion that earlier showed up while drafting the bench.
- **`rayon` beats Kāra par by 1.31× today.** Not a defeat — a concrete optimization target. `rayon` ships a per-worker-deque work-stealing scheduler; Kāra's runtime currently uses a single global queue + Condvar (the v1 MVP per `karac-rust/runtime/src/lib.rs § Pool`); Go's goroutine runtime sits at a comparable distribution efficiency to karac's MVP. Closing the gap to rayon is tracked in `karac-rust/docs/implementation_checklist/phase-7-codegen.md` line 163. The codegen work that *did* land (Phase 3 + 3.1) gets within 31% of mature hand-tuned `rayon` on the first iteration of the feature, while slightly beating Go's goroutine runtime.
- **Go beats Kāra/C/Rust by 11% on single-thread.** Not a defeat either — see *Why is Go single-thread faster?* above. The 510 ms Kāra / 511 ms C / 513 ms Rust three-way parity is the load-bearing finding for compiler quality. The Go-edge is a real per-core optimization opportunity worth investigating but not a "Kāra is broken" signal.
- **Order across the result `Vec` is unspecified** in the par lane. That's exactly why `#[par_unordered]` is required — it's the user's explicit opt-in to "I don't care about output order" semantics. For LC #204 (count only) and our bench (sum is order-invariant), this costs nothing. Workloads that need order-preservation would use a different reduction primitive (filed as a future karac-rust tracker entry).
