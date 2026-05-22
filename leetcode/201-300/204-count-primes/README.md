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

| Approach | Complexity | Kāra | Python | Rust | C |
|---|---|---|---|---|---|
| Trial division `is_prime(k)` over `[2, n)`, count matches | O(n·√n / ln n) time avg, O(π(n)) space if listing | [`count.kara`](count.kara) ✓ via `karac run` / `karac build` | [`count.py`](count.py) ✓ | [`bench/count.rs`](bench/count.rs) ✓ (bench quad) | [`bench/count.c`](bench/count.c) ✓ (bench quad) |

`✓` runs end-to-end today. Both `count.kara` and `count.py` emit `4, 25, 168, 1229, 9592` for the verification N's (10, 100, 1000, 10000, 100000) — matching OEIS A000720 (π(n), the prime-counting function).

## Why trial division, not the Sieve of Eratosthenes

The textbook solution to "count primes < n" is the Sieve of Eratosthenes — O(n log log n) time, O(n) space, beats trial division on any single-call benchmark. So why does this kata's bench use trial division?

**Because each `is_prime(k)` call is independent — no cross-iteration data dependency, no shared state.** That property makes the workload work equally well across two lanes of the bench: (a) single-threaded per-core measurement, where the algorithm shape is identical across compilers and the comparison stays honest; and (b) the parallel lane (Kāra `#[par_unordered]` + Rust `rayon`), where workers fan out across cores with zero coordination. A sieve, by contrast, writes to a shared array of "is this number composite" flags; parallelizing it requires either a segmented sieve (complex), a wheel-based parallel sieve (more complex), or a lock-protected shared array (kills parallelism) — and the cross-iteration data dependency makes even the seq lane harder to compare apples-to-apples.

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

The bench is structured around two like-for-like comparisons. **Cross-framing comparisons (e.g. "auto-par Kāra vs single-threaded Rust") are not meaningful** — they conflate the language's compiler quality with whether the comparator opted into parallelism, and would silently let the parallel win mask any per-core regression. Both comparisons below stay within their lane:

1. **Per-core compiler quality** — single-threaded Kāra vs single-threaded Rust (`rustc -O`) vs C (`clang -O3`). Same algorithm, no library help, no parallelism. Measures how well each compiler turns the source into machine code on one core. This is the comparison the kata is *primarily* for; mirrors the framing in kata-7 (reverse-integer), kata-8 (atoi), kata-65 (valid-number).
2. **Auto-parallelism vs library parallelism** — `#[par_unordered]` Kāra vs `rayon` Rust (`.into_par_iter().filter(...).collect()`). Both implementations explicitly opted into parallelism; the comparison is "is Kāra's first-iteration auto-par competitive with a mature work-stealing library?" Surfaces real karac gaps (the scheduler is currently the bottleneck — see story 2 below).

The five-row table below contains both comparisons interleaved; the per-iter `is_prime()` work is heavy enough that both comparisons land on stable numbers.

### Runtime

| Lane | Implementation | Wall time | User-CPU | CPU% |
|---|---|---|---|---|
| par | rust count (rayon par_iter)              | **38.7 ms ± 1.9 ms** | 561.5 ms | ~1450% (~15 cores) |
| par | **kāra count (codegen, #[par_unordered])** | **53.4 ms ± 2.7 ms** | 552.5 ms | ~1030% (~10 cores) |
| seq | c    count (clang -O3)                   | **518.0 ms ± 7.2 ms** | 513.7 ms | 99% |
| seq | rust count (rustc -O)                    | **527.3 ms ± 6.9 ms** | 523.0 ms | 99% |
| seq | **kāra count**                           | **530.1 ms ± 54.6 ms** | 513.2 ms | 97% |

Run `bench/bench.sh` to reproduce. Hyperfine, 10 runs after 3 warmups, M5 Pro under typical desktop load (the Kāra-seq stddev is wide because one run caught a system hiccup; mean is the load-bearing number).

**Story 1 — per-core compiler quality (the kata's primary purpose).** Kāra's single-thread codegen sits within ~3% of Rust's `rustc -O` and C's `clang -O3` on the same workload — same algorithm, same trial-division shape, same `Vec[i64]` push path. **The compiler is at parity with both Rust and C on single-threaded code.** No claim of a per-core advantage; the kata's value here is the *demonstration* that Kāra hasn't traded compiler quality for higher-level features. A careful reader looking for "what's the actual codegen cost of using Kāra?" gets a clean answer: ~0%.

**Story 2 — auto-parallelism vs `rayon` (a separate question with its own answer).** Kāra's `#[par_unordered]` is **1.38× slower than `rayon`** — brand-new auto-par lands within 38% of a mature work-stealing library on first iteration. Both implementations spend the same ~555 ms of total user-CPU (same total work). The gap is concentrated in scheduler efficiency: rayon distributes across ~15 cores via per-worker deques with work-stealing; karac currently uses a single global queue + Condvar (the v1 MVP per `karac-rust/runtime/src/lib.rs § Pool`) and distributes across ~10. The codegen-side work (Phase 3 of karac-rust's reduction codegen + Phase 3.1's amortized-doubling combine, both 2026-05-21) is competitive with rayon at the worker-fn / merge level; the runtime scheduler is the remaining gap, tracked at karac-rust `phase-7-codegen.md` line 163 ("real work-stealing scheduler") as the optimization target this comparison empirically validates.

### Compile (cold)

| Implementation | Wall time |
|---|---|
| karac build count.kara | 60.1 ms ± 2.7 ms |
| rustc -O count.rs      | 85.3 ms ± 4.1 ms |
| clang -O3 count.c      | 42.5 ms ± 1.7 ms |

Kāra compiles ~1.4× slower than `clang -O3`, ~1.4× faster than `rustc -O`. Single-file builds aren't a stress test for the compiler — this number is dominated by LLVM mid-end passes (Kāra runs `default<O2>` per `src/codegen/optimization.rs`). The `rayon` row isn't included here because it's a multi-file Cargo project (incremental dep compile dominates and is a different measurement).

### Binary size

| Implementation | Size |
|---|---|
| kara count (par)  | 311.9 KiB |
| kara count (seq)  |  49.0 KiB |
| rust count        | 455.6 KiB |
| rust+rayon count  | 451.8 KiB |
| c    count        |  32.8 KiB |

Kāra's parallel binary is larger than C's because it links the parts of `libkarac_runtime.a` the par-reduce path needs (dispatch + worker pool + descriptor machinery). The single-threaded Kāra binary drops to 49 KiB — the runtime's par-reduce surface isn't linked in when nothing references it, leaving only the minimal startup + libc-glue archive code. Rust's binary is larger than either Kāra variant because `rustc -O` defaults include the panic-unwind machinery + `std`. Adding `rayon` barely changes Rust's size (Rust's runtime overhead dominates over the rayon scheduler). With `-C panic=abort -C strip=symbols` Rust binaries shrink considerably, but those aren't the default profile.

### Runtime memory (peak)

| Implementation | Peak RSS |
|---|---|
| kara count (par)     | 23.2 MiB |
| kara count (seq)     | 14.2 MiB |
| rust count           |  8.3 MiB |
| rust+rayon count     | 15.8 MiB |
| c    count           |  6.2 MiB |

Kāra's parallel peak comes from the 10-worker thread pool (each with ~1 MiB stack reserved) + per-worker partial Vec slots during the merge. `rayon` sits in similar territory for the same reason (15-worker thread pool + per-worker partials). Kāra single-threaded skips the thread pool but still uses ~14 MiB — that's the `Vec[i64]` of 664k primes (~5 MiB live) plus the realloc-doubling overhead during the growth phase (the final doubling allocates 2× the final size before the previous buffer is freed). Rust single-threaded hits a smaller peak because Rust's `Vec::push` releases the old buffer mid-growth via a different path. C single-threaded is the smallest because its bench pre-sizes the buffer at `cap = 700_000` and skips realloc entirely.

### Compile memory (cold)

| Implementation | Peak RSS |
|---|---|
| karac build count.kara |  9.2 MiB |
| rustc -O count.rs      | 27.2 MiB |
| clang -O3 count.c      |  2.6 MiB |

Kāra's compiler holds a much smaller working set than `rustc -O` (no incremental-compile cache, no macro expansion, simpler type system). Clang's small footprint reflects C's much simpler frontend.

## Caveats

- **N = 10⁷ is well above LC's max** (`n ≤ 5×10⁶`). The bench uses a larger N so the timed loop dominates startup/teardown overhead in hyperfine. At LC's actual limit (5M), wall times halve uniformly — ~26 ms Kāra par, ~265 ms Kāra/Rust/C seq — same ratios within each lane, just less measurement headroom.
- **Cross-lane wall-time ratios are not the comparison this kata is for.** "Auto-par Kāra is N× faster than single-threaded Rust" is technically true at any N, but it's apples-to-oranges (parallel dispatch vs single-core codegen) and would silently let a parallel win hide a per-core regression. Both lanes have their own comparator in the table; readers checking compiler quality should look at the **seq lane** (kara vs rust vs c), and readers checking parallel-runtime quality should look at the **par lane** (kara `#[par_unordered]` vs `rayon`). Mixing them is the user-CPU vs wall-clock confusion that earlier showed up while drafting the bench.
- **`rayon` beats Kāra par by 1.38× today.** Not a defeat — a concrete optimization target. `rayon` ships a per-worker-deque work-stealing scheduler; Kāra's runtime currently uses a single global queue + Condvar (the v1 MVP per `karac-rust/runtime/src/lib.rs § Pool`). Closing the gap is tracked in `karac-rust/docs/implementation_checklist/phase-7-codegen.md` line 163. The codegen work that *did* land (Phase 3 + 3.1) gets within 38% of mature hand-tuned parallel Rust on the first iteration of the feature.
- **Order across the result `Vec` is unspecified** in the par lane. That's exactly why `#[par_unordered]` is required — it's the user's explicit opt-in to "I don't care about output order" semantics. For LC #204 (count only) and our bench (sum is order-invariant), this costs nothing. Workloads that need order-preservation would use a different reduction primitive (filed as a future karac-rust tracker entry).
