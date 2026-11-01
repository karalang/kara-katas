# 16. 3Sum Closest

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array, Two Pointers, Sorting &nbsp;·&nbsp; **Source:** [leetcode.com/problems/3sum-closest](https://leetcode.com/problems/3sum-closest/)

Given an integer array `nums` (n ≥ 3) and an integer `target`, return the sum `nums[i] + nums[j] + nums[k]` (with `i`, `j`, `k` pairwise distinct) whose value is closest to `target`. The problem guarantees a unique answer in magnitude; ties on `|sum - target|` are resolved by whichever the algorithm visits first (LeetCode accepts any).

```
([-1, 2, 1, -4],  target=1)    → 2     (-1 + 2 + 1)
([0, 0, 0],       target=1)    → 0
([1, 1, 1, 0],    target=-100) → 2
```

**Constraints:** `3 ≤ nums.length ≤ 500`, `-10^3 ≤ nums[i] ≤ 10^3`, `-10^4 ≤ target ≤ 10^4`.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| Sort, then fix `s[i]` and two-pointer the suffix, tracking the running closest sum | O(n²) time, O(n) extra (sorted copy) | [`three_sum_closest.kara`](three_sum_closest.kara) ✓ via `karac run` / `karac build` | [`three_sum_closest.py`](three_sum_closest.py) ✓ |

`✓` runs end-to-end today. Interpreter and codegen produce identical output to the Python mirror across all nine test cases.

## Why sort + two-pointer (and what changes from kata #15)

The shape is the same one kata [#15](../15-3sum/) uses: sort, then for each fixed smallest element `s[i]` collapse the remaining pair search into a single linear crawl over the sorted suffix `s[i+1 .. n)`. The steering rule is `sign(sum - target)` instead of `sign(sum)`:

```
sum < target  ⇒  current sum too small,  advance `lo`.
sum > target  ⇒  current sum too big,    retreat `hi`.
sum == target ⇒  unbeatable distance 0,  return immediately.
```

Two shape changes are worth pulling out, because they make this kata noticeably tighter than #15 in the inner loop:

- **No dedup machinery.** Kata 15 had to skip repeated smallest values (outer dedup) and walk past repeated pair values after each hit (inner dedup) to avoid emitting duplicate triplets. Here we only emit one scalar at the end, so redundant `(i, lo, hi)` comparisons are wasted work but not *wrong* work — we drop the dedup entirely. The inner `while lo < hi` body is just `sum`, two `abs` compares, and a branch.

- **No `s[i] > 0` early-out.** Kata 15 could `break` once the smallest element went positive — all-positive triplets can never sum to 0. With an arbitrary `target` no such monotone wall exists; a positive `s[i]` may still yield the closest sum (`target=100`, `s=[5,5,5]` returns 15). The only early-exit is the exact-hit return.

`best` is seeded with the first valid triplet `s[0]+s[1]+s[2]` rather than a sentinel + bool flag — LeetCode's `n ≥ 3` constraint makes this safe and lets the hot loop's update guard be a clean numeric compare.

## Kāra features exercised

- **`Vec.from_slice(Slice[i64])` + in-place `sort_by`** — same shape as kata [#15](../15-3sum/) and kata [#1665](../../1601-1700/1665-minimum-initial-energy-to-finish-tasks/): copy `nums` into an owned `Vec[i64]`, then `s.sort_by(|a, b| a.cmp(b))`. As of karac Slice 6.1, this pattern (`Vec[i64].sort_by` with inline-closure comparator, no captures) routes through the monomorphized fast path — see § Sort-dispatch history under § Runtime — seq lane. Verified to compile and run under both `karac run` and `karac build`.
- **Two-pointer crawl with `lo`/`hi` cursors** — same index-as-cursor pattern as kata [#11](../11-container-with-most-water/), [#15](../15-3sum/), and [#88](../88-merge-sorted-array/), with the steering rule swapped from `sign(sum)` to `sign(sum - target)`.
- **Inline `abs_i64` helper** — the hot loop calls `abs_i64(sum - target) < abs_i64(best - target)` twice per non-exact-hit step. The helper is a one-line `if x < 0 { -x } else { x }`; verified by `arm64` disassembly to LLVM-lower to a branchless `cmp` + `cneg`, matching Rust's `.abs()` instruction-for-instruction.
- **Early-return from a nested `while`** — `if sum == target { return sum; }` short-circuits both loops at once, same shape as kata [#1](../1-two-sum/)'s brute-force `return [i, j]`.
- **Scalar `+` reduction in the bench** — `sum = sum + three_sum_closest(...)` is the slice-1 auto-par-on-reduction allow-list shape (associative + commutative `+`, scalar accumulator), recognized by default in `karac build` and lowered to a `karac_par_reduce` dispatch. Lighter per-iter memory footprint than kata 15's `sum + r.len()` Vec-returning shape, which the auto-par bench picks up cleanly.

## Running

```bash
# Kāra — interpreter and codegen produce the same output today.
karac run   three_sum_closest.kara
karac build three_sum_closest.kara && ./three_sum_closest

# Python
python3 three_sum_closest.py

# Verify they agree
diff <(./three_sum_closest)              <(python3 three_sum_closest.py) && echo OK
diff <(karac run three_sum_closest.kara) <(python3 three_sum_closest.py) && echo OK
```

## Benchmarks
Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`three_sum_closest.{kara,rs,c,py}`, `go-seq/main.go`).

**Workload.** M = 8 distinct test cases, each a `Vec[i64]` of N = 16 values drawn from a deterministic 31-bit LCG into the range `[-10, 10]`, built once into a `Vec[Vec[i64]]` before the timed loop. Per outer iter we rotate `idx = k % M` and call `three_sum_closest` on that case with a per-case target picked from a small bag `{-12, -6, -1, 0, 1, 5, 11, 19}` — some targets land inside the reachable-sum window (exact-hit return fires), some sit outside it (the running `best` saturates at a suffix extremum). The eight target/case pairs keep the closest-tracking branch from learning any single (sum, target) delta pattern, and the exact-hit returns mean different rotations exercise different early-exit paths.

K = 1,000,000 outer iterations; the call is never loop-invariant (LLVM can't hoist it) and the eight distinct (case, target) pairs keep the branch predictor from fully learning any single sort/two-pointer trajectory. The sink — the running total of every returned closest-sum — is **2,125,000** across all five mirrors; bench.sh fails loudly on mismatch before timing starts. The LCG stays inside i64 with no wraparound (`1103515245 × state` never exceeds ~2.37×10¹⁸ < i64::MAX), so every mirror reproduces the same stream and the same per-call closest sums.

This kata's per-iter body is **strictly lighter** than kata 15's — same Vec-copy + sort, the same O(N²) crawl, but no nested `Vec[Vec[i64]]` output (just a single i64 return) and no dedup machinery. That makes the seq-lane comparison directly about the inner-loop codegen for the two-pointer + abs-and-track-best body, with the allocator's noise floor sharply reduced relative to kata 15.

Two-lane kata (BENCH.md § Implicit auto-par): the `sum = sum + three_sum_closest(...)` accumulator is the slice-1 allow-list reduction shape, so `karac build` emits a `karac_par_reduce` dispatch by default. The bench builds two kara binaries — `KARAC_AUTO_PAR=0` for the within-lane seq comparison, default for the auto-par regime — and reports them in separate tables per the two-lane discipline.

### Runtime — seq lane

M5 Pro, 2026-10-31 (`results.json` `measured_at` 2026-11-01T01:00Z), karac 0.9.0-dev.14057+g6697158fa (v2/MIR backend), hyperfine `--warmup 5 --runs 30 --shell=none`. All comparators single-threaded; the kāra row is `KARAC_AUTO_PAR=0`. (See § Sort-dispatch history below for the pre-Slice-6.1 story.) The equal-safety `rust -C overflow-checks=on` lane is now recorded alongside the wrapping `rust -O` lane — it is the apples-to-apples Kāra-vs-Rust row, since Kāra checks overflow by default.

| Implementation | Wall time |
|---|---|
| rust three_sum_closest                | **71.4 ± 4.3 ms** |
| rust three_sum_closest (overflow-checks=on) | 79.7 ± 5.8 ms |
| **kāra three_sum_closest (seq)**      | **93.2 ± 2.3 ms** |
| c    three_sum_closest (clang -O3)    | 124.3 ± 4.8 ms |
| go   three_sum_closest                | 205.1 ± 24.1 ms |

This is the same sort-bound shape as kata 15. **The Kāra-vs-Rust headline is the equal-safety row.** Kāra checks integer overflow by default; `rustc -O` *silently wraps*, so the `rust -O` row runs a weaker safety contract. The apples-to-apples comparison is `rust -C overflow-checks=on`, which restores the same checked arithmetic Kāra ships by default — and against it **Kāra is 1.17× behind** (93.2 vs 79.7 ms); against wrapping `rust -O` it is 1.31× behind, of which Rust's own overflow-check tax is 1.12× (79.7 vs 71.4 ms). On the 2026-07-28 feed these ratios were 0.96× and 1.08×. That move is not a MIR regression: against the last legacy build (dd86e3955, Oct 2026) the MIR binary runs 0.76× its instructions and 0.74× its cycles, so the 07-28 feed came from a faster July karac and the slowdown happened within the legacy era. **C trails Kāra by 1.33×** (124.3 vs 93.2 ms) — `qsort`'s indirect comparator call lands per comparison and there's no way to eliminate it without giving up the standard-library sort; note clang -O3 also skips the overflow checks. **Go trails by 2.20×** — `sort.Slice` also pays the per-comparison closure indirect call, with GC and scheduler overhead on top.

#### Sort-dispatch history (kata 16 → karac Slice 6.1)

**Pre-fix (2026-05-29, kata 16 ship):** Kāra seq landed at **96.8 ± 0.6 ms** — a 1.55× gap to Rust. The kata is in the corpus *because* it surfaced this gap and drove the karac fix. Initial diagnosis blamed `abs_i64` lowering — disassembly disproved it (Kāra's `if x < 0 { -x } else { x }` LLVM-lowers to a branchless `cmp` + `cneg`, identical to Rust's `.abs()` instruction-for-instruction; both inner two-pointer bodies are 21-instruction ARM64 loops with identical structure). The actual cause was the **sort dispatch**: `s.sort_by(|a, b| a.cmp(b))` routed through `karac_vec_sort_by` in the runtime, which called the user's comparator thunk via a function pointer per comparison; Rust's `sort_unstable()` monomorphized the comparator inline. A confirmation experiment (same body, hand-rolled inline insertion sort) ran at 70.6 ms, closing 76% of the gap and pinning the diagnosis.

**Post-fix (Slice 6.1 of the Vec[T] monomorphization roadmap, `docs/implementation_checklist/phase-7-codegen.md`):** karac now detects `Vec[i64].sort_by(inline_closure)` with no captures and emits a per-call-site `__vec_i64_sort_by_mono_<id>(data: *mut i64, len: i64)` function (Internal linkage) whose body is an insertion sort with the user's comparator inlined at the inner compare. No callback through `karac_vec_sort_by`, no function-pointer indirection — LLVM has direct visibility into both the sort algorithm and the comparator, so the compare-and-shift loop optimises end-to-end. Closes **94% of the original gap** (96.8 → ~63 ms, 1.55× → 1.08×) — better than the 76% the insertion-sort A/B predicted, because LLVM sees the comparator inside the surrounding K=1M outer loop's optimization context. This is the *runtime* half of the win. (The figures in this subsection are 2026-05/06 history; the current seq ratio is in the table above.)

An earlier snapshot of this section also claimed the seq binary collapsed from 359.4 KiB to 33.0 KiB, on the reasoning that the inlined mono comparator lets `karac_vec_sort_by` + its runtime-archive dependencies get DCE'd. That was true only for the Slice 6.1 mono-only window: Slice 6.4's length dispatch (needed so large-N sorts don't regress to O(N²)) re-emits a `karac_vec_sort_by` fallback branch at every `sort_by` call site, which re-links the runtime sort and the libstd floor it reaches. The seq binary was **294.8 KiB** at the 2026-06-05 re-bench; the 33 KiB figure was specific to the mono-only dispatch. (Under the v2/MIR backend every Kāra binary is ~300–390 KB, so today's size no longer isolates this effect.) See § Binary size for the full breakdown and the no-sort control.

### Runtime — auto-par regime

The `sum = sum + three_sum_closest(...)` reduction is auto-par-eligible; the default `karac build` recognizes it and emits a `karac_par_reduce` dispatch. NOT comparable to the single-thread rows above (BENCH.md two-lane discipline) — reported separately so the production-default Kāra behavior stays visible:

| Implementation | Wall time | User-CPU |
|---|---|---|
| rust three_sum_closest (rayon par_iter) | **9.8 ± 0.7 ms** | 118.3 ms |
| c    three_sum_closest (pthreads)  | 14.7 ± 0.9 ms | 178.0 ms |
| **kāra three_sum_closest (auto-par default)** | **15.7 ± 1.7 ms** | 171.4 ms |
| go   three_sum_closest (goroutines + WaitGroup) | 86.1 ± 7.9 ms | 303.9 ms |

The auto-par binary is **5.95× faster than the kāra seq binary** (93.2 → 15.7 ms), spreading the K=1M case-rotation reduction across the cores (~10.9× user-CPU-to-wall ratio on M5 Pro). Against the parallel comparators it is **1.59× behind rayon** (1.25× on the 2026-07-28 feed), 1.07× behind C pthreads, and 5.5× ahead of Go. (History: before Slice 6.1 the auto-par speedup was 9.0×, 96.8 → 10.8 ms; the mono sort body sped up the seq baseline more than the par lane, compressing the ratio.) This is the legitimate-win case (BENCH.md kata #4 path): a real wall-time speedup, with the `karac_par_reduce` machinery costing **+97.5 KiB of binary over seq** (see § Binary size). Peak memory is 2.1 MiB.

### Runtime — Python

| Run | Mean ± σ |
|---|---|
| `py three_sum_closest` (K=100k) — last measured 2026-06-16, not re-run | 143.3 ± 0.8 ms |

Python is not in the 2026-10-31 feed (the run did not set `KARA_BENCH_INCLUDE_PY`); the figure above and the ratios in this paragraph are from the 2026-06-16 snapshot. Python at K=100k was 143–149 ms; projecting to the compiled mirrors' K=1M (~1.49 s) put it **~23.6× slower than kāra seq** at the time. Wider than kata 15's ~13.5× because Kāra seq got faster (kata 15 still dominated by per-iter Vec alloc which CPython also pays); kata 16's mono fast path meant the per-call cost on Kāra had dropped sharply while CPython's relative cost stayed put. Against the auto-par regime the cross-lane ratio was ~181×.

### Compile elapsed (cold)

`--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Compiler | Time |
|---|---|
| clang -O3 three_sum_closest.c           | **54.5 ± 1.1 ms** |
| rustc -O three_sum_closest.rs           | 144.9 ± 12.9 ms |
| **karac build three_sum_closest.kara**  | **214.7 ± 4.2 ms** |

Kāra compiles **1.48× slower than `rustc -O`** and at **3.94× of clang -O3** on the v2/MIR backend. (The 2026-06-16 snapshot read 86.4 ms for karac, 1.60× faster than rustc, on the legacy backend.)

### Binary size

| Implementation | Size |
|---|---|
| c    three_sum_closest            | 32.8 KiB |
| **kāra three_sum_closest (seq)**  | **295.8 KiB** |
| **kāra three_sum_closest (auto-par)** | **393.2 KiB** |
| rust three_sum_closest            | 456.0 KiB |
| go   three_sum_closest            | 2452.2 KiB |

Every v2/MIR Kāra binary is ~300–390 KB where the legacy backend's were ~34 KB (the 2026-07-28 feed had this kata's seq binary at 33.7 KiB); tracked as [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md). The history below is the legacy backend's.

**Correction (2026-06-05 re-bench — supersedes the 2026-05-30 correction).** The history of this section, with each number's actual cause:

- **33.0 KiB (Slice 6.1 era, 2026-05-29):** real, but specific to the *mono-only* dispatch — the inlined comparator let `karac_vec_sort_by` + its runtime-archive dependencies get DCE'd, exactly as originally reasoned.
- **Slice 6.4 (same day) re-linked the runtime sort:** the length dispatch (`len ≤ 64` → inlined mono insertion sort, above → `karac_vec_sort_by` runtime callback) is required so large-N sorts don't regress to O(N²) — kata [#1665](../../1601-1700/1665-minimum-initial-energy-to-finish-tasks/)'s N=50k went 3.2 ms → 1.1 s under a strawman mono-only build. The fallback branch survives `-dead_strip` unless LLVM can const-prove the vec small, and `karac_vec_sort_by`'s `slice::sort_by` reaches std's panic infrastructure — keeping the DWARF symbolizer (`gimli`/`addr2line`/`object`/`rustc_demangle`) and its libstd retinue alive. That is **the same ~262 KiB libstd floor every auto-par binary pays** via `karac_par_reduce` (kata [#14](../14-longest-common-prefix/)'s auto-par binary: 312.5 KiB with zero sorts) — **not a sort-specific "symbolized sort-panic fix"** as the 05-30 correction guessed. A minimal no-`sort_by` program still builds to 32.8 KiB with zero gimli/addr2line symbols (re-verified 2026-06-05).
- **410.8 KiB (the 05-30 reading):** the floor *plus* ~116 KiB of transient inflation from a build-contaminated runtime archive (plain `cargo build` co-emits rlib + staticlib, defeating fat-LTO DCE — same incident as kata #14/#15 § Binary size). Rebuilt per the documented `cargo rustc … --crate-type staticlib` discipline, today's seq binary is **294.8 KiB** (`__text` 211,344 B of a 301,872 B image).

This kata remains the control: it returns a scalar `i64`, no nested `Vec`, yet lands within 8 bytes of kata [#15](../15-3sum/)'s seq binary (still true on 2026-10-31: 302,896 vs 302,888 B) — confirming the shared surface is not output-allocation machinery. The auto-par row adds **+97.5 KiB** over seq on the MIR backend (+17.2 KiB on the 2026-06-05 legacy build). The kara rows ship at 65% (seq) and 86% (auto-par) of Rust's 456.0 KiB; C's 32.8 KiB is the floor (no runtime archive, no symbolized panics). Reclaiming the ~262 KiB for sort-only binaries (a non-panicking lean large-N sort entry) is tracked on the karac side in `phase-7-codegen.md` Slice 6.2+.

### Runtime memory (peak)

| Implementation | Peak |
|---|---|
| c    three_sum_closest            | 1.0 MiB |
| **kāra three_sum_closest (seq)**  | **1.0 MiB** |
| rust three_sum_closest            | 1.1 MiB |
| **kāra three_sum_closest (auto-par)** | **2.1 MiB** |
| go   three_sum_closest            | 9.7 MiB |

Kāra seq's peak RSS (1,098,064 B) is one 16 KiB page below Rust's (1,114,424 B) and two pages above C (1,065,272 B) — indistinguishable at this granularity. The auto-par regime's 2.1 MiB (2,163,120 B; rayon 2.3 MiB, C pthreads 1.6 MiB) is the worker pool's per-thread scratch + partials, **0.8 MiB *lower* than kata 15's 2.9 MiB** despite running on the same shape — the body returns a scalar so workers' per-iter live set is just the sorted buffer, not a freshly-allocated `Vec[Vec[i64]]`. Same compiler, same auto-par dispatch, lighter body shape → measurably tighter steady-state RSS.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 three_sum_closest.c          | 2.6 MiB |
| rustc -O three_sum_closest.rs          | 37.1 MiB |
| **karac build three_sum_closest.kara** | **61.5 MiB** |

Kāra's compile-memory footprint on the v2/MIR backend is ~23.7× clang's and 1.66× rustc's on this kata. (The 2026-06-16 legacy snapshot read 14.8 MiB, ~2.5× below rustc.)

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio is the codegen-vs-Rust gap. C calibrates the LLVM-backend floor, Go is the cross-runtime data point, and Python is the ergonomic foil. On this kata the **load-bearing result is the equal-safety ratio: Kāra is 1.17× behind `rust -C overflow-checks=on`** (2026-10-31; it was at parity, 0.98×, in the 2026-06-16 snapshot). Against wrapping `rust -O` it is 1.31× behind, 1.12× of which is Rust's own overflow-check tax; see the runtime section above for why this is a legacy-era drift rather than a MIR regression. The kata's first ship at 1.55× was the natural-pull trigger for karac Slice 6.1, which monomorphizes `Vec[i64].sort_by` inline-closure comparators into the user binary; the post-fix gap closed to codegen-quality noise, and to parity once safety was matched. Kata 15 with the same fix runs level with Rust (0.99×, see [`15-3sum/README.md`](../15-3sum/README.md)). Kāra leads C by 1.33× and Go by 2.20× on this kata — the qsort indirect-call penalty and `sort.Slice` closure overhead are no longer offset on the Kāra side.
