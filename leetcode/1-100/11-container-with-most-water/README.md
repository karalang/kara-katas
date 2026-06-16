# 11. Container With Most Water

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array, Two Pointers, Greedy &nbsp;·&nbsp; **Source:** [leetcode.com/problems/container-with-most-water](https://leetcode.com/problems/container-with-most-water/)

Given `n` non-negative integers `height[0..n)` interpreted as vertical line heights on the x-axis, pick two lines `i < j` so that the rectangle they form with the x-axis holds the most water. The rectangle's area is bounded by the **shorter** of the two lines times the horizontal distance:

```
area(i, j) = min(height[i], height[j]) * (j - i)
```

```
([1,8,6,2,5,4,8,3,7])        → 49     (between idx 1 and idx 8, h=7, w=7)
([1,1])                      → 1      (smallest non-trivial case)
([4,3,2,1,4])                → 16     (tall ends, full-width span)
([2,3,4,5,18,17,6])          → 17     (best is two adjacent tall cells)
```

**Constraints:** `2 ≤ n ≤ 10^5`, `0 ≤ height[i] ≤ 10^4`.

## Approaches

| Approach | Complexity | Kāra | Python | Rust |
|---|---|---|---|---|
| Two-pointer dominance argument | O(n) time, O(1) space | [`container.kara`](container.kara) ✓ via `karac run` / `karac build` | [`container.py`](container.py) ✓ | [`bench/container.rs`](bench/container.rs) ✓ (bench triad) |

`✓` runs end-to-end today. Interpreter and codegen produce identical output to the Python mirror across all 11 test cases.

## Why two-pointer (and not brute force)

Brute force is O(n²) — every pair (i, j) examined. At the LeetCode ceiling of n = 10⁵ that's 10¹⁰ pair-evaluations, comfortably over the time limit.

The two-pointer trick collapses it to O(n) with one observation: if you have `lo < hi` and `h[lo] ≤ h[hi]`, then the pair (lo, hi) is the **best** pair involving lo. Any pair (lo, hi') with hi' < hi has strictly smaller width, and its height is still capped by `min(h[lo], h[hi']) ≤ h[lo]`. So no such inward pair can beat (lo, hi); the whole column starting at lo can be retired in one step.

That argument is symmetric (when `h[hi] < h[lo]`, retire hi instead). Each step burns one pointer-advance and the loop terminates in at most `n - 1` steps.

## Two-pointer in five lines

```
fn max_area(heights):
    lo, hi, best = 0, n - 1, 0
    while lo < hi:
        h = min(heights[lo], heights[hi])
        best = max(best, h * (hi - lo))
        if heights[lo] < heights[hi]: lo += 1 else: hi -= 1
    return best
```

The whole algorithm is the if-else at the bottom; the rest is bookkeeping. The dominance argument means a single linear scan is provably optimal *for the answer*, even though the full O(n²) pair-table contains pairs we never examined — they're all dominated.

Subtle correctness anchor: when `h[lo] == h[hi]`, advancing either pointer is fine (the pair is already examined and any inward pair has both shorter width and height ≤ the tied value). The kata advances `lo` on equality for consistency.

## Kāra features exercised

- **`Slice[i64]` parameter to a non-recursive function** — `fn max_area(heights: Slice[i64]) -> i64` takes the input as an immutable slice; the LeetCode driver passes `Array[i64, N]` literals (which coerce to `Slice[i64]` per kata [#1](../1-two-sum/), [#4](../4-median-of-two-sorted-arrays/), [#88](../88-merge-sorted-array/)), the bench passes `Vec[i64].as_slice()` (per kata [#121](../../101-200/121-best-time-to-buy-and-sell-stock/)).
- **`if`-as-expression for `min`** — `let h: i64 = if h_lo < h_hi { h_lo } else { h_hi };` keeps the inner loop branch-free of a helper call. Same idiom as kata [#9](../9-palindrome-number/)'s `if r { 1i64 } else { 0i64 }` widening.
- **Two-pointer crawl with index-as-cursor** — the loop carries `lo` / `hi` cursors and indexes `heights[lo]` / `heights[hi]` directly, same pattern as kata [#88 merge-sorted-array](../88-merge-sorted-array/)'s `mut Slice[i64]` merge.
- **`Vec[i64]` for the bench input + `Vec.filled(n, 0i64)` pre-allocation** — same pattern as kata [#121](../../101-200/121-best-time-to-buy-and-sell-stock/)'s bench, avoids the log-N capacity-growth slowdown a naive `Vec.new()` + `push` loop would pay.
- **Sum-of-i64 reduction in the bench's outer loop** — `sum = sum + max_area(...)` is the slice-1 auto-par-on-reduction allow-list shape (associative + commutative `+`), recognized by default in `karac build` and lowered to a `karac_par_reduce` dispatch.

No `Vec` allocations inside the inner loop (the heights buffer lives in `main`; the two-pointer crawls in place); no `String` building; no `HashMap`. The hot path is just two array loads, a `min`, a multiply, and a conditional pointer-advance.

## Running

```bash
# Kāra — interpreter and codegen produce the same output today.
karac run   container.kara
karac build container.kara && ./container

# Python
python3 container.py

# Verify they agree
diff <(./container) <(python3 container.py) && echo OK
diff <(karac run container.kara) <(python3 container.py) && echo OK
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, and Go. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`container.{kara,rs,c,py}`, `go-seq/main.go`).

Per [`../../../BENCH.md`](../../../BENCH.md) § *Implicit auto-par*, this kata exercises karac's auto-par-on-reduction path: the K = 10,000,000 outer loop's `sum = sum + max_area_off(...)` accumulator is a textbook associative + commutative reduction, which the slice-1 concurrency analyzer recognizes and slice-3b codegen lowers to a `karac_par_reduce` dispatch *by default*. To honor BENCH.md's two-lane discipline (cross-lane wall-time ratios are not meaningful) the bench builds **two** kara binaries:

- **`container_kara_seq`** — built with `KARAC_AUTO_PAR=0` (codegen.rs Slice 6 gate — the documented mechanism for side-by-side seq-vs-par benchmarking of the same source). The within-lane row directly comparable to rustc -O / clang -O3 / go build.
- **`container_kara`** — default `karac build` output. Picks up auto-par dispatch (~14 cores active on this workload). Reported separately so the production-default Kara behavior stays visible.

**Workload.** N = 8 height arrays of width W = 16, all packed back-to-back in a flat `Vec[i64]` of size N·W = 128 and cycled by `k % N`. K = 10,000,000 outer iters. Heights drawn from a deterministic LCG modulo 50 — small enough to keep `min(h, h) * (hi - lo)` well inside i64 even at worst case (`49 * 15 = 735` per call), large enough that the two-pointer crawl exercises both branch directions. Sink = sum of `max_area` returns widened to i64 across K iters. All four compiled mirrors agree on `4897500000` before any timing runs; `bench.sh` fails loudly on mismatch.

### Runtime — seq lane (apples-to-apples, single-threaded)

Snapshot — M5 Pro, 2026-05-31, hyperfine `--warmup 5 --runs 30 --shell=none`:

| Implementation | Wall time | User-CPU | CPU% |
|---|---|---|---|
| go   container | **101.0 ms ± 1.6 ms** | 99.0 ms | 99% |
| c    container (clang -O3) | **146.5 ms ± 1.4 ms** | 144.0 ms | 99% |
| **kāra container** (`KARAC_AUTO_PAR=0`) | **191.3 ms ± 0.6 ms** | 189.0 ms | 99% |
| rust container (rustc -O) | **168.3 ms ± 1.4 ms** | 166.0 ms | 99% |

Kāra trails C by **~31%** (191.3 vs 146.5 ms, C ahead, i.e. C runs 0.77× of Kāra) — a per-core codegen-quality gap on a two-pointer kernel. The two-pointer hot path is two array loads + a `min` + a multiply + a conditional pointer-advance per iter; karac's seq codegen lowers this to a tight inner loop, but clang -O3 still gets a meaningfully tighter one on this shape this run.

Rust is **~12% ahead of Kāra** on this workload (168.3 vs 191.3 ms, i.e. Rust runs 0.88× of Kāra). Both Rust and Kāra inline `max_area_off` into the hot loop (verified via objdump — no `max_area_off` symbol survives in either binary); the residual gap is per-iteration codegen on the two-pointer body, where rustc's loop optimizer edges out karac's seq lowering this run.

Go is the outlier at **101.0 ms — ~47% faster than Kāra and ~31% faster than C**. Go's compiler is aggressive about both bounds-check elision (it can prove `l < r < len(heights)` survives the loop invariant) and per-call specialization across the eight distinct input cases. Same workload, same algorithm — different codegen tradeoffs. This is one of the rare LeetCode-corpus workloads where Go's straight-line speed wins on a per-core basis; kata [#10](../10-regular-expression-matching/)'s recursion-heavy regex matcher had Go trailing the Kāra/Rust/C tie by ~1.53×, and the broader corpus mean has Kāra and Rust ahead of Go.

### Runtime — auto-par regime (kara default, multi-core)

Same snapshot, default `karac build` output:

| Implementation | Wall time | User-CPU | CPU% |
|---|---|---|---|
| **kāra container** (auto-par on reduction) | **12.2 ms ± 1.7 ms** | 155.0 ms | ~1270% (~12.7 cores) |

Karac's auto-par-on-reduction recognizes the K=10M reduction in `main` and emits a `karac_par_reduce` dispatch — the binary carries `karac_par_reduce` + `karac_reduce_combine_add_i64` + `karac_reduce_worker_0` symbols, ~12.7 cores active during the run. The wall-time win *over the seq-lane Kāra row above* is **15.7×** (191.3 / 12.2); total CPU time goes down 18% (189.0 → 155.0 ms user) net of dispatch + per-worker fixed overhead. Net: real production wall-time speedup on this workload's shape, paid for in a +263 KiB binary footprint (see § *Binary size* below).

**Not headlined against the C / Rust / Go rows above.** Per BENCH.md's two-lane discipline, cross-lane wall-time ratios are not meaningful — naming "kara is 7× faster than go" here would conflate per-core codegen quality with whether the comparator opted into parallelism. The seq-lane table is the within-lane codegen-quality comparison; the auto-par row is what Kāra delivers as a *language-level* choice on top of that codegen-quality baseline (no source-level annotation; the analyzer recognizes the natural serial reduction). A follow-up CR can add a true par lane (`rayon::par_iter` + goroutines variants of the outer reduction) so this number lands against in-lane parallel comparators.

### Codegen vs Python

CPython at K = 1M takes **553.9 ± 4.6 ms** (single-core); projected to K = 10M that's ~5.54 s. Both Kāra rows beat the projection by wide margins, but the cross-lane caveat applies symmetrically: Kāra-seq vs CPython is the within-lane per-core comparison (~29× faster), and Kāra-auto-par vs CPython is the cross-lane regime comparison (~454× faster). The Python mirror is here as the ergonomic-foil data point per BENCH.md § *Comparison baselines*, not as a headline.

### Compile elapsed (cold)

Snapshot — M5 Pro, 2026-05-31, hyperfine `--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Workload | Kāra (`karac build`) | Rust (`rustc -O`) | C (`clang -O3`) |
|---|---|---|---|
| `container` | **76.1 ± 0.6 ms** | 93.5 ± 1.1 ms | 46.2 ± 0.4 ms |

Karac is **1.23× faster than rustc -O** and **1.65× slower than clang -O3**. (Compile *elapsed* is the load-confounded metric — the deterministic signals held: byte-identical binaries and the documented compile-memory floor. The shift vs 2026-05-25 is two-sided this run — karac +2.8 ms, rustc −5.0 ms — reflecting machine load, not a codegen change.) Single-file invocations only — `go build`'s first run mixes module resolution + std-lib link and isn't comparable to a single-file `rustc` / `clang` / `karac` invocation; excluded per BENCH.md.

### Binary size

| Implementation | Bytes | KiB |
|---|---|---|
| c    container | 33,485 | 32.7 |
| **kāra container (seq)** | **34,099** | **33.3** |
| kāra container (auto-par) | 303,104 | 296.0 |
| rust container | 466,330 | 455.4 |
| go   container | 2,492,518 | 2,434.1 |

The seq-lane Kāra binary sits **within 0.6 KiB of clang's** (33.3 vs 32.7 KiB) — same C-class minimum kata [#10](../10-regular-expression-matching/#binary-size) reports, and consistent with the cross-archive LTO + DCE work (landed 2026-05-12) plus the post-`e76f42b` `__TEXT,__jittmpl` segment compaction. The auto-par variant grows +263 KiB to carry the `karac_par_reduce` machinery (per-branch trampolines + reduction-combine globals + worker-pool registration) — same +263 KiB ballast kata [#4](../4-median-of-two-sorted-arrays/#binary-size), [#8](../8-string-to-integer-atoi/#binary-size), [#9](../9-palindrome-number/#binary-size), and [#10](../10-regular-expression-matching/#binary-size) carry when their outer reductions go auto-par. Here too the ballast pays for a real within-language wall-time win.

### Runtime memory (peak)

| Implementation | Bytes | MiB |
|---|---|---|
| **kāra container (seq)** | **1,081,344** | **1.0** |
| c    container | 1,064,960 | 1.0 |
| rust container | 1,114,112 | 1.1 |
| kāra container (auto-par) | 1,490,944 | 1.4 |
| go   container | 3,048,448 | 2.8 |

Kāra-seq's **1.0 MiB peak sits within 16 KiB of C's** (1,081,344 vs 1,064,960) — both lowest in the lane, 32 KiB under Rust. The two-pointer matcher allocates nothing inside the loop (the 128-element `Vec[i64]` heights buffer is fixed at 1 KiB and lives across all iterations), so steady state is dominated by libc + Mach-O loader overhead. Auto-par Kāra adds ~0.5 MiB for the lazy-init worker thread stacks — tunable downward via `KARAC_PAR_WORKERS` for memory-constrained targets. Go's 2.9 MiB carries its GC roots + scheduler arena overhead.

### Compile memory (cold)

| Compiler | Bytes | MiB |
|---|---|---|
| clang -O3 container.c | 2,726,298 | 2.6 |
| karac build container.kara | 14,050,918 | 13.4 |
| rustc -O container.rs | 29,464,986 | 28.1 |

Karac peaks at **13.4 MiB** vs rustc's **28.1 MiB** (2.1× lower) and clang's **2.6 MiB** (5.2× higher). The kara number includes the auto-par recognition pass + reduction codegen, which is bounded constant work per recognized site — the seq build path would shave a small constant off but not materially change the ratio. (The +0.8 MiB vs the 2026-05-25 snapshot is the documented fixed per-compile floor from karac feature-growth — content-independent, byte-identical output, tracked benign across katas #6–#11.)

### Numbers published here are reference data

The CI gate's source-of-truth aggregate lives in [`karac-rust/bench/compile_speed/`](../../../../karac-rust/bench/compile_speed/) (different corpus: curated subset + synthetic 10K-LOC stress program).
