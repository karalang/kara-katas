# 18. 4Sum

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array, Two Pointers, Sorting &nbsp;·&nbsp; **Source:** [leetcode.com/problems/4sum](https://leetcode.com/problems/4sum/)

Given an integer array `nums` and an integer `target`, return every distinct quadruplet `[nums[a], nums[b], nums[c], nums[d]]` (with `a`, `b`, `c`, `d` pairwise distinct) that sums to `target`. The result set must contain no duplicate quadruplets.

```
([1, 0, -1, 0, -2, 2], target=0)  → [-2,-1,1,2], [-2,0,0,2], [-1,0,0,1]
([2, 2, 2, 2, 2],       target=8)  → [2,2,2,2]
([1, 2, 3, 4],          target=100)→ (none)
```

**Constraints:** `1 ≤ nums.length ≤ 200`, `-10^9 ≤ nums[i] ≤ 10^9`, `-10^9 ≤ target ≤ 10^9`.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| Sort, fix `s[a]` and `s[b]`, two-pointer the suffix for the remaining pair; dedup at all four positions, prune by reachable-sum window | O(n³) time, O(n) extra (sorted copy) | [`four_sum.kara`](four_sum.kara) ✓ via `karac run` / `karac build` | [`four_sum.py`](four_sum.py) ✓ |

`✓` runs end-to-end today. Interpreter and codegen produce identical output to the Python mirror across all nine test cases.

## Why sort + two-pointer (and what changes from kata #15 / #16)

4Sum is the natural one-level lift of kata [#15](../15-3sum/)'s 3Sum. Brute force is O(n⁴); sorting first collapses it to O(n³): fix the two smallest elements `s[a]` and `s[b]`, then two-pointer the sorted suffix `s[b+1 .. n)` for a pair summing to `target - s[a] - s[b]`. The pair-search steering rule is the `sign(sum - target)` form kata [#16](../16-3sum-closest/) introduced, not 3Sum's `sign(sum)`:

```
sum < target  ⇒  the low value is too small, advance `lo`.
sum > target  ⇒  the high value is too big,  retreat `hi`.
sum == target ⇒  record the quadruplet, then step *both* inward.
```

So this kata sits at the intersection of its two predecessors: it keeps kata 15's **dedup-and-emit** machinery (it produces a `Vec[Vec[i64]]`, not a scalar) but adopts kata 16's **arbitrary `target`** (not a fixed 0). Three shape points are worth pulling out:

- **Dedup lifts one level.** Equal values are adjacent after the sort, so "skip a value we already used" stays a single backward-look — now applied at *four* positions: `a` (`s[a] == s[a-1]`), `b` (`b > a+1 && s[b] == s[b-1]`), and the `lo`/`hi` skip-runs after each hit. No HashSet of seen quadruplets needed, same as kata 15.

- **The `s[i] > 0` early-out becomes a reachable-window prune.** Kata 15 could `break` once the smallest element went positive — with a fixed target of 0, all-positive triplets can't reach it. Kata 16 noted that an arbitrary `target` *erases that monotone wall*. 4Sum restores a comparable prune by bounding each fixed prefix against the window of sums still reachable from it: after fixing `a`, if the smallest completion `s[a]+s[a+1]+s[a+2]+s[a+3]` already exceeds `target` we `break`; if the largest completion `s[a]+s[n-3]+s[n-2]+s[n-1]` still undershoots we `continue`. The same two prunes apply after fixing `b`. They never change the output — every mirror emits the identical quadruplet set — they just trim dead `a`/`b` prefixes so the O(n³) constant stays small.

- **`i64` is load-bearing here, not a uniformity default.** Kata 15's entries are bounded by 10⁵, so a three-term sum stays well inside i32. 4Sum bounds entries *and* `target` by 10⁹, so a four-term sum can reach 4×10⁹ — past i32's 2.1×10⁹ ceiling but comfortably inside i64. This is the first kata in the 1–100 run where the width is forced by the arithmetic rather than chosen to match the rest of the corpus.

## Kāra features exercised

- **`Vec.from_slice(Slice[i64])` + in-place `sort_by`** — same shape as kata [#15](../15-3sum/) and kata [#16](../16-3sum-closest/): copy `nums` into an owned `Vec[i64]`, then `s.sort_by(|a, b| a.cmp(b))`. Routes through karac's monomorphized `Vec[i64].sort_by(inline_closure)` fast path (no captures). Verified to compile and run under both `karac run` and `karac build`.
- **Nested two-pointer inside two fixed cursors** — the `lo`/`hi` crawl is the index-as-cursor pattern from kata [#11](../11-container-with-most-water/), [#15](../15-3sum/), and [#88](../88-merge-sorted-array/), here nested two deep under the `a`/`b` fixes for the O(n³) shape.
- **`Vec[Vec[i64]]` nested output with per-hit `Vec.push`** — each quadruplet is a freshly-allocated 4-element `Vec[i64]` pushed onto the result, same alloc/free path as kata 15's triplets but four-wide. This is the allocator-stress shape kata 16 deliberately dropped (it returned a scalar).
- **Multi-level `continue` / `break` with backward-look dedup** — `if a > 0 and s[a] == s[a-1] { continue; }` and the inner `while lo < hi and s[lo] == s[lo-1]` skip-runs exercise labeled-free loop control across three nesting levels.
- **Scalar `+` reduction in the bench** — `sum = sum + r.len()` is the slice-1 auto-par-on-reduction allow-list shape (associative + commutative `+`, scalar accumulator over a `Vec[Vec[i64]]`-returning call), recognized by default in `karac build` and lowered to a `karac_par_reduce` dispatch.

## Running

```bash
# Kāra — interpreter and codegen produce the same output today.
karac run   four_sum.kara
karac build four_sum.kara && ./four_sum

# Python
python3 four_sum.py

# Verify they agree
diff <(./four_sum)              <(python3 four_sum.py) && echo OK
diff <(karac run four_sum.kara) <(python3 four_sum.py) && echo OK
```

## Benchmarks
Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`four_sum.{kara,rs,c,py}`, `go-seq/main.go`).

**Workload.** M = 8 distinct test cases, each a `Vec[i64]` of N = 16 values drawn from a deterministic 31-bit LCG into the range `[-10, 10]`, built once into a `Vec[Vec[i64]]` before the timed loop. Per outer iter we rotate `idx = k % M` and call `four_sum` on that case with a per-case target from a small bag `{-20, -8, -3, 0, 2, 6, 12, 24}` — some land inside the reachable four-term-sum window (quadruplets emitted, the min/max prunes stay quiet), some sit at the edge or outside (the prunes short-circuit whole `a`/`b` prefixes). The eight `(case, target)` pairs keep the call from being loop-invariant (LLVM can't hoist it) and stop the branch predictor from learning any single sort / two-pointer / prune trajectory.

K = 1,000,000 outer iterations. Each call does a `Vec.from_slice` copy, an O(N log N) sort, an O(N³) two-fix + two-pointer scan, and allocates a `Vec[Vec[i64]]` of however many target-sum quadruplets the case holds (each quad a 4-element `Vec[i64]`). Across the eight cases there are **132 quadruplets**, so the sink — the running total of every returned `Vec`'s `.len()` — is `(K / M) × 132` = `125000 × 132` = **16,500,000**; all five mirrors must agree before any timing begins. The LCG stays inside i64 with no wraparound (`1103515245 × state` never exceeds ~2.37×10¹⁸ < i64::MAX), so every mirror reproduces the same stream and the same quadruplet counts.

This is the **O(N³) peer to kata 15's O(N²)**: the same `Vec[Vec[i64]]` alloc/free path and the same sort + two-pointer core, one polynomial order heavier in the scan and four-wide rows instead of three. Because the cubic scan now dominates the per-call cost, the sort is a smaller fraction of the total than it is in 3Sum — so this kata stresses inner-loop *scan* codegen more than sort dispatch.

Two-lane kata (BENCH.md § Implicit auto-par): the `sum = sum + r.len()` accumulator is the slice-1 allow-list reduction shape, so `karac build` emits a `karac_par_reduce` dispatch by default. The bench builds two kara binaries — `KARAC_AUTO_PAR=0` for the within-lane seq comparison, default for the auto-par regime — and reports them in separate tables per the two-lane discipline.

### Runtime — seq lane

M5 Pro, 2026-10-31 (`results.json` `measured_at` 2026-11-01T01:02Z), karac 0.9.0-dev.14057+g6697158fa (v2/MIR backend), hyperfine `--warmup 5 --runs 30 --shell=none`. All comparators single-threaded; the kāra row is `KARAC_AUTO_PAR=0`. The `rust -C overflow-checks=on` row is the equal-safety comparator, since Kāra checks overflow by default.

| Implementation | Wall time |
|---|---|
| rust four_sum                      | **543.0 ± 10.5 ms** |
| **kāra four_sum (seq)**            | **557.8 ± 11.1 ms** |
| c    four_sum (clang -O3)          | 562.4 ± 30.4 ms |
| rust four_sum (overflow-checks=on) | 567.8 ± 13.5 ms |
| go   four_sum                      | 671.0 ± 27.6 ms |

On the seq lane **Kāra is level with the native field**: 1.03× behind wrapping `rust -O`, 0.98× of the equal-safety `overflow-checks=on` build (i.e. a hair ahead), 0.99× of C (inside C's ±30 ms σ), and 1.20× ahead of Go. That is flat against the 2026-07-28 feed (1.05× Rust, 1.02× C). The mechanism is the one kata 15 establishes: on N=16 inputs a fully-inlined insertion sort (karac's mono `sort_by` fast path) competes with Rust's general `sort_unstable`/ipnsort and C's indirect-call `qsort`, and Kāra's small-`Vec` allocator path stays competitive on the four-wide nested output. The interesting shift from kata 15 is the **margin over C**: on the same 2026-10-31 toolchain Kāra leads C by 1.12× on O(n²) 3Sum but only **1.01× here** on O(n³) 4Sum. The sort — where Kāra's inlined comparator most outruns `qsort`'s per-comparison indirect call — is a smaller fraction of the cubic scan's runtime, so Kāra's sort-driven edge over C dilutes as the scan grows. (C and Rust are within σ of each other here, 562.4 vs 543.0 ms — vs kata 15 where Rust's sort pulls it clear of C; on the cubic scan the sort's contribution shrinks enough that C's tighter scalar loop catches up.) Against Rust the gap stays within codegen-quality noise on both katas (0.99× / 1.03×). **Go trails by 1.20×** — `sort.Slice` pays a per-comparison closure indirect call and the `[][]int64` quadruplet output adds GC pressure the manual-free mirrors don't carry.

Note (2026-11-07, karac g97681763d): the seq re-run reads Kāra 1.10× C, 1.12× `rustc -O` and 1.06× equal-safety Rust, so the lead over C quoted here is history; par Kāra 97.4 ms against rayon's 115.8 ms.

### Runtime — auto-par regime

The `sum = sum + r.len()` reduction is auto-par-eligible; the default `karac build` recognizes it and emits a `karac_par_reduce` dispatch. NOT comparable to the single-thread rows above (BENCH.md two-lane discipline) — reported separately so the production-default Kāra behavior stays visible:

| Implementation | Wall time | User-CPU |
|---|---|---|
| **kāra four_sum (auto-par default)** | **102.7 ± 9.4 ms** | 1463.5 ms |
| rust four_sum (rayon par_iter)       | 107.9 ± 14.2 ms | 1773.2 ms |
| c    four_sum (pthreads)             | 123.6 ± 14.1 ms | 1896.8 ms |
| go   four_sum (goroutines + WaitGroup) | 653.8 ± 47.4 ms | 1573.6 ms |

The auto-par binary is **5.4× faster than the kāra seq binary** (557.8 → 102.7 ms), spreading the K=1M case-rotation reduction across the cores (~14.3× user-CPU-to-wall ratio on M5 Pro). It is now **ahead of rayon (0.95×, within σ) and of C pthreads (0.83×, i.e. C is 1.20× slower)**, and 6.4× ahead of Go, using the least user-CPU of the four; on the 2026-07-28 feed it was 1.17× behind rayon and 1.04× behind C. This is the legitimate-win case (BENCH.md kata #4 path): a real wall-time speedup at the cost of the `karac_par_reduce` machinery's binary delta (see § Binary size) and a higher steady-state RSS. As in kata 15, the per-worker allocator contention of the nested-`Vec` output caps the speedup below the perf-core count — a sort+allocate body parallelizes less cleanly than a pure arithmetic reduction — but the win is still substantial.

### Runtime — Python

| Run | Mean ± σ |
|---|---|
| `py four_sum` (K=100k) — last measured 2026-06-05, not re-run | 692.4 ± 3.6 ms |

Python is not in the 2026-10-31 feed (the run did not set `KARA_BENCH_INCLUDE_PY`); the figure and ratios in this paragraph are from the 2026-06-05 snapshot. Python at K=100k was 692–701 ms; projecting to the compiled mirrors' K=1M (~7.01 s) put it **~19.5× slower than kāra seq** at the time. Wider than kata 15's ~13.5× because the cubic scan shifts the balance away from `sorted()` (the C-implemented builtin CPython leans on): more of the per-call time is now interpreter-level Python loop overhead on the two-fix + two-pointer body, which the compiled mirrors run as native code. Against the auto-par regime the cross-lane ratio was ~165×.

### Compile elapsed (cold)

`--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Compiler | Time |
|---|---|
| clang -O3 four_sum.c           | **62.2 ± 1.2 ms** |
| rustc -O four_sum.rs           | 149.4 ± 3.9 ms |
| **karac build four_sum.kara**  | **253.1 ± 2.0 ms** |

Kāra compiles **1.69× slower than `rustc -O`** and at **4.07× of clang -O3** on the v2/MIR backend. (The 2026-06-05 legacy snapshot read 109.1 ms, 1.53× faster than rustc.)

### Binary size

| Implementation | Size |
|---|---|
| c    four_sum                      | 32.9 KiB |
| **kāra four_sum (seq)**            | **295.8 KiB** |
| **kāra four_sum (auto-par)**       | **393.2 KiB** |
| rust four_sum                      | 472.9 KiB |
| go   four_sum                      | 2452.2 KiB |

Every v2/MIR Kāra binary is ~300–390 KB where the legacy backend's were ~34 KB, tracked as [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md). Today's seq binary is 295.8 KiB (63% of Rust's 472.9 KiB) and the auto-par row adds +97.5 KiB for the `karac_par_reduce` dispatch. The rest of this paragraph is the legacy backend's history. The legacy seq binary landed at 33.5 KiB — well above C's 32.9 KiB (C's `int64_t **` rows need no runtime archive). The excess over the ~33 KiB no-sort floor is the **libstd floor pulled in by `sort_by`**: Slice 6.4's length dispatch always emits a `karac_vec_sort_by` fallback branch alongside the inlined mono sort, and the runtime sort's `slice::sort_by` reaches std's panic infrastructure — keeping the DWARF symbolizer (`gimli`/`addr2line`/`object`/`rustc_demangle`) and its libstd retinue alive through `-dead_strip`. It is reachable through `s.sort_by(...)`, not through the `Vec[Vec[i64]]` output: a minimal Kāra program with no `sort_by` builds to ~33 KiB with none of that surface, and kata [#16](../16-3sum-closest/) — which returns a scalar `i64`, no nested `Vec` — lands within 8 bytes of kata 15's seq binary. This is the same floor every auto-par binary pays via `karac_par_reduce`; see [kata 16 § Binary size](../16-3sum-closest/README.md) for the full history (including why the Slice 6.1-era 33 KiB readings were real but mono-only) and [kata 15 § Binary size](../15-3sum/README.md) for the bisection. The 2026-05-30 snapshot of this section read 410.8 / 450.8 KiB — the floor *plus* rlib-contamination from a mis-built runtime archive (seq −118,816 B / par −125,600 B recovered on today's clean rebuild, same incident as katas #14–#17). On the legacy backend the auto-par row added **+33.3 KiB** over seq for the `karac_par_reduce` + worker-pool surface — a small marginal add, since the seq binary already carries the floor that dominates. Reclaiming the floor for sort-only binaries is tracked on the karac side in `phase-7-codegen.md` Slice 6.2+. Go's 2.4 MiB is its static runtime.

### Runtime memory (peak)

| Implementation | Peak |
|---|---|
| **kāra four_sum (seq)**            | **1.1 MiB** |
| rust four_sum                      | 1.2 MiB |
| c    four_sum                      | 1.1 MiB |
| **kāra four_sum (auto-par)**       | **3.0 MiB** |
| go   four_sum                      | 9.9 MiB |

Kāra seq's peak RSS (1,196,368 B) sits within a page of Rust's and C's (1,212,728 B / 1,163,576 B) — the per-iter `Vec[Vec[i64]]` is allocated and freed inside `four_sum`, so steady state stays flat across the K=1M loop. The auto-par regime's 3.0 MiB (3,097,032 B; rayon 3.8 MiB, C pthreads 2.8 MiB) is the worker pool's per-thread scratch + partials over the four-wide nested output; Go's 9.9 MiB carries its GC roots + scheduler arena.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 four_sum.c          | 2.6 MiB |
| rustc -O four_sum.rs          | 38.4 MiB |
| **karac build four_sum.kara** | **64.8 MiB** |

Kāra's compile-memory footprint on the v2/MIR backend is ~24.8× clang's and 1.69× rustc's on this kata. (The 2026-06-05 legacy snapshot read 17.5 MiB, ~2.2× below rustc.)

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio is the codegen-vs-Rust gap. C calibrates the LLVM-backend floor, Go is the cross-runtime data point, and Python is the ergonomic foil. On this O(n³) sort-and-emit kata **Kāra is 1.03× behind Rust** (2026-10-31) — close to the 0.99× kata 15 carries on the O(n²) version, and traced to the same cause (inlined insertion sort competes with `sort_unstable` on N=16, allocator path holds on the nested-`Vec` output); against the equal-safety overflow-checked Rust build it is 0.98×. Against C the story is more visible: Kāra's lead compresses from 1.12× (kata 15) to 1.01× here as the cubic scan dilutes the sort's share of runtime, and C pulls within σ of Rust. The Rust gap is the load-bearing number and it stays inside codegen-quality noise across both katas.
