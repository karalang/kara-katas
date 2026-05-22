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

**Because trial division is embarrassingly parallel and the sieve is not.** Each `is_prime(k)` call is independent — no cross-iteration data dependency, no shared state. The bench's outer loop carries a `#[par_unordered]` attribute and the workers fan out across cores with zero coordination. A sieve, by contrast, writes to a shared array of "is this number composite" flags; parallelizing it requires either a segmented sieve (complex), a wheel-based parallel sieve (more complex), or a lock-protected shared array (kills parallelism).

This kata's purpose is to demonstrate the auto-par codegen path landed in karac's Phase 3 collect-style reduction work — and trial division is the workload that surfaces the speedup most clearly. A future sieve-based kata for the *count-only* version of LC #204 is filed separately.

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

### Comparison framing

Four mirrors, two framings worth measuring:

1. **"What does a programmer write?"** — Rust and C mirrors are idiomatic single-threaded. This shows the win when auto-par triggers on code a programmer would write without reaching for a parallelism library.
2. **"What if they do reach for a library?"** — A `rayon` Rust mirror (`bench/rayon/`) uses `.into_par_iter().filter(...).collect()`, the canonical hand-parallelized form. This shows the gap between Kāra's auto-par and a mature, hand-tuned Rust parallelism library.

Both rows are in the table below.

### Runtime

| Implementation | Wall time | User-CPU | CPU% | vs Kāra |
|---|---|---|---|---|
| rust count (rayon par_iter)                 | **36.3 ms ± 1.0 ms** | 561.8 ms | ~1500% (~15 cores) | 1.26× faster |
| **kāra count (codegen, #[par_unordered])** | **45.8 ms ± 0.5 ms** | 549.6 ms | ~1200% (~12 cores) | 1.00× |
| rust count (single-threaded)                | 501.5 ms ± 4.1 ms    | 495.9 ms | 99%   | 10.95× slower |
| c    count (single-threaded, clang -O3)     | 504.3 ms ± 13.8 ms   | 497.3 ms | 99%   | 11.01× slower |

Run `bench/bench.sh` to reproduce.

**The two stories.** Kāra's auto-par is **10.95× faster than idiomatic single-threaded Rust** and **1.26× slower than hand-parallelized `rayon` Rust**. Both are honest finds:

- The 10.95× number is the *transparency* story: the same source code an LC #204 solver writes happens to be the parallel implementation, no library import or restructuring required.
- The 1.26× number is the *competitiveness* story: brand-new auto-par (Phase 3 of karac's reduction codegen, shipped 2026-05-21) lands within 26% of `rayon`, a mature library with years of work-stealing-scheduler tuning. The gap is concentrated in worker-fan-out efficiency (rayon distributes across ~15 cores; karac across ~12) — see karac's `phase-7-codegen.md` line 163 ("real work-stealing scheduler" follow-up) for the codegen-side optimization target.

User-CPU numbers tell the underlying mechanics: idiomatic Rust and C each spend ~500 ms on a single core. Both Kāra and `rayon` spend ~555 ms of CPU total — they do the same total work — but the wall time depends on how widely that work spreads. Kāra's `karac_par_reduce` runtime currently uses a single global queue + Condvar (the v1 MVP); rayon uses per-worker deques with work-stealing. The codegen path itself (worker fn, per-worker private `Vec[i64]`, amortized-doubling merge) is competitive with rayon's equivalent.

### Compile (cold)

| Implementation | Wall time |
|---|---|
| karac build count.kara | 55.7 ms ± 0.4 ms |
| rustc -O count.rs      | 80.2 ms ± 1.5 ms |
| clang -O3 count.c      | 39.8 ms ± 0.6 ms |

Kāra compiles ~1.4× slower than `clang -O3`, ~1.4× faster than `rustc -O`. Single-file builds aren't a stress test for the compiler — this number is dominated by LLVM mid-end passes (Kāra runs `default<O2>` per `src/codegen/optimization.rs`). The `rayon` row isn't included here because it's a multi-file Cargo project (incremental dep compile dominates and is a different measurement).

### Binary size

| Implementation | Size |
|---|---|
| kara count        | 311.9 KiB |
| rust count        | 455.6 KiB |
| rust+rayon count  | 451.8 KiB |
| c    count        |  32.8 KiB |

Kāra's binary is larger than C's because it links `libkarac_runtime.a` (the par-reduce dispatch + worker pool + descriptor machinery). Rust's binary is larger than Kāra's because `rustc -O` defaults include the panic-unwind machinery + `std`. Adding `rayon` barely changes Rust's size (Rust's runtime overhead dominates over the rayon scheduler). With `-C panic=abort -C strip=symbols` Rust binaries shrink considerably, but those aren't the default profile.

### Runtime memory (peak)

| Implementation | Peak RSS |
|---|---|
| kara count (codegen) | 22.6 MiB |
| rust count           |  8.3 MiB |
| rust+rayon count     | 15.9 MiB |
| c    count           |  6.2 MiB |

Kāra's higher peak comes from the 12-worker thread pool (each with ~1 MiB stack reserved) + per-worker partial Vec slots during the merge. `rayon` sits in between for the same reason (15-worker thread pool + per-worker partials). Rust/C single-threaded each hold a single contiguous `Vec[i64]` / `int64_t[]` of ~5 MiB (664k × 8 bytes + headroom) and no thread pool.

### Compile memory (cold)

| Implementation | Peak RSS |
|---|---|
| karac build count.kara |  9.2 MiB |
| rustc -O count.rs      | 27.2 MiB |
| clang -O3 count.c      |  2.6 MiB |

Kāra's compiler holds a much smaller working set than `rustc -O` (no incremental-compile cache, no macro expansion, simpler type system). Clang's small footprint reflects C's much simpler frontend.

## Caveats

- **N = 10⁷ is well above LC's max** (`n ≤ 5×10⁶`). The bench uses a larger N so the timed loop dominates startup/teardown overhead in hyperfine. At LC's actual limit (5M), the runtime would be ~25 ms Kāra vs ~250 ms Rust — same ratios, just less measurement headroom.
- **Order across the result `Vec` is unspecified.** That's exactly why `#[par_unordered]` is required — it's the user's explicit opt-in to "I don't care about output order" semantics. For LC #204 (count only) and our bench (sum is order-invariant), this costs nothing. Workloads that need order-preservation would use a different reduction primitive (filed as a future tracker entry).
- **`rayon` beats Kāra by 1.26× today.** That's not a defeat — it's a concrete optimization target. `rayon` ships a per-worker-deque work-stealing scheduler; Kāra's runtime currently uses a single global queue (the v1 MVP per `karac-rust/runtime/src/lib.rs § Pool`). Closing the gap is tracked in `phase-7-codegen.md` line 163. The codegen work that *did* land (Phase 3 + 3.1) gets within 26% of mature hand-tuned parallel Rust on the first iteration — the headline isn't "Kāra beats rayon," it's "Kāra's auto-par is competitive with rayon while requiring zero source-level changes vs the single-threaded version."
- **The single-threaded baselines aren't a strawman.** Most LC #204 solutions in any language are written as a serial loop — that's the audience the 10.95× framing speaks to. The `rayon` framing speaks to a different audience: parallelism specialists. Both audiences exist and both numbers matter.
