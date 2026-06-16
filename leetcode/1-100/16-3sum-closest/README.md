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

Snapshot — M5 Pro, 2026-06-16, hyperfine `--warmup 5 --runs 30 --shell=none`. All comparators single-threaded; the kāra row is `KARAC_AUTO_PAR=0`. Numbers below are with the karac Slice 6.1 mono fast path landed (see § Sort-dispatch history below for the pre-fix story). The equal-safety `rust -C overflow-checks=on` lane is now recorded alongside the wrapping `rust -O` lane — it is the apples-to-apples Kāra-vs-Rust row, since Kāra checks overflow by default.

| Implementation | Wall time |
|---|---|
| rust three_sum_closest                | **58.7 ± 0.5 ms** |
| **kāra three_sum_closest (seq)**      | **65.8 ± 1.8 ms** |
| rust three_sum_closest (overflow-checks=on) | 67.3 ± 0.9 ms |
| c    three_sum_closest (clang -O3)    | 106.7 ± 1.2 ms |
| go   three_sum_closest                | 167.2 ± 0.8 ms |

This is the same sort-bound shape as kata 15. **The Kāra-vs-Rust headline is the equal-safety row.** Kāra checks integer overflow by default; `rustc -O` *silently wraps*, so the `rust -O` row runs a weaker safety contract. The apples-to-apples comparison is `rust -C overflow-checks=on`, which restores the same checked arithmetic Kāra ships by default — and against it **Kāra is actually faster, 0.98×** (65.8 vs 67.3 ms). The apparent "Rust leads by 1.08×" against `rust -O` is the overflow-check safety tax, not a codegen-quality gap: once Rust does the same per-`sum` checks Kāra does, Kāra's mono sort body edges ahead. Both compilers monomorphize their comparators (see § Sort-dispatch history below). **C trails Kāra by 1.62×** (106.7 vs 65.8 ms) — `qsort`'s indirect comparator call lands per comparison and there's no way to eliminate it without giving up the standard-library sort; note clang -O3 also skips the overflow checks. **Go trails by 2.54×** — `sort.Slice` also pays the per-comparison closure indirect call, with GC and scheduler overhead on top.

#### Sort-dispatch history (kata 16 → karac Slice 6.1)

**Pre-fix (2026-05-29, kata 16 ship):** Kāra seq landed at **96.8 ± 0.6 ms** — a 1.55× gap to Rust. The kata is in the corpus *because* it surfaced this gap and drove the karac fix. Initial diagnosis blamed `abs_i64` lowering — disassembly disproved it (Kāra's `if x < 0 { -x } else { x }` LLVM-lowers to a branchless `cmp` + `cneg`, identical to Rust's `.abs()` instruction-for-instruction; both inner two-pointer bodies are 21-instruction ARM64 loops with identical structure). The actual cause was the **sort dispatch**: `s.sort_by(|a, b| a.cmp(b))` routed through `karac_vec_sort_by` in the runtime, which called the user's comparator thunk via a function pointer per comparison; Rust's `sort_unstable()` monomorphized the comparator inline. A confirmation experiment (same body, hand-rolled inline insertion sort) ran at 70.6 ms, closing 76% of the gap and pinning the diagnosis.

**Post-fix (Slice 6.1 of the Vec[T] monomorphization roadmap, `docs/implementation_checklist/phase-7-codegen.md`):** karac now detects `Vec[i64].sort_by(inline_closure)` with no captures and emits a per-call-site `__vec_i64_sort_by_mono_<id>(data: *mut i64, len: i64)` function (Internal linkage) whose body is an insertion sort with the user's comparator inlined at the inner compare. No callback through `karac_vec_sort_by`, no function-pointer indirection — LLVM has direct visibility into both the sort algorithm and the comparator, so the compare-and-shift loop optimises end-to-end. Closes **94% of the original gap** (96.8 → ~63 ms, 1.55× → 1.08×) — better than the 76% the insertion-sort A/B predicted, because LLVM sees the comparator inside the surrounding K=1M outer loop's optimization context. This is the *runtime* half of the win, and it is intact on the current toolchain (the 63.1 ms re-bench above matches the post-fix snapshot).

An earlier snapshot of this section also claimed the seq binary collapsed from 359.4 KiB to 33.0 KiB, on the reasoning that the inlined mono comparator lets `karac_vec_sort_by` + its runtime-archive dependencies get DCE'd. That was true only for the Slice 6.1 mono-only window: Slice 6.4's length dispatch (needed so large-N sorts don't regress to O(N²)) re-emits a `karac_vec_sort_by` fallback branch at every `sort_by` call site, which re-links the runtime sort and the libstd floor it reaches. The current seq binary is **294.8 KiB**. The runtime speedup landed and held; the 33 KiB figure was specific to the mono-only dispatch. See § Binary size for the full breakdown and the no-sort control.

### Runtime — auto-par regime

The `sum = sum + three_sum_closest(...)` reduction is auto-par-eligible; the default `karac build` recognizes it and emits a `karac_par_reduce` dispatch. NOT comparable to the single-thread rows above (BENCH.md two-lane discipline) — reported separately so the production-default Kāra behavior stays visible:

| Implementation | Wall time | User-CPU |
|---|---|---|
| **kāra three_sum_closest (auto-par default)** | **8.4 ± 0.9 ms** | 97.0 ms |

The auto-par binary is **7.7× faster than the kāra seq binary** (63.1 → 8.2 ms), spreading the K=1M case-rotation reduction across the perf cores (~11.7× user-CPU-to-wall ratio on M5 Pro). Note the speedup ratio dropped from the pre-Slice-6.1 9.0× (96.8 → 10.8 ms) — auto-par's absolute wall time improved (10.8 → 8.2 ms) because each worker now runs the faster mono sort body, but the seq baseline improved more, so the ratio compresses. This is the legitimate-win case (BENCH.md kata #4 path): a real wall-time speedup with the `karac_par_reduce` machinery's **+17.2 KiB binary over seq** (see § Binary size — both lanes carry the libstd floor that `sort_by` already pulls in, so the par-reduce + worker-pool surface is a small marginal add). Per-worker memory pressure stays flat at 1.7 MiB.

### Runtime — Python

| Run | Mean ± σ |
|---|---|
| `py three_sum_closest` (K=100k) | 143.3 ± 0.8 ms |

Python at K=100k is 149 ms; projecting to the compiled mirrors' K=1M (~1.49 s) puts it **~23.6× slower than kāra seq**. Wider than kata 15's ~13.5× because Kāra seq got faster (kata 15 still dominated by per-iter Vec alloc which CPython also pays); kata 16's mono fast path means the per-call cost on Kāra has dropped sharply while CPython's relative cost stayed put. Against the auto-par regime the cross-lane ratio is ~181×.

### Compile elapsed (cold)

`--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Compiler | Time |
|---|---|
| clang -O3 three_sum_closest.c           | **52.0 ± 0.6 ms** |
| **karac build three_sum_closest.kara**  | **86.4 ± 0.5 ms** |
| rustc -O three_sum_closest.rs           | 133.4 ± 2.0 ms |

Kāra compiles **1.60× faster than `rustc -O`** and sits at **1.54× of clang -O3** — same shape as the rest of the corpus. (05-30 read 68.8 / 46.2 / 118.6 — karac and clang both rose ~6–10% in this batch, so treat the drift as environmental, not a compiler change.)

### Binary size

| Implementation | Size |
|---|---|
| c    three_sum_closest            | 32.8 KiB |
| **kāra three_sum_closest (seq)**  | **33.5 KiB** |
| **kāra three_sum_closest (auto-par)** | **312.3 KiB** |
| rust three_sum_closest            | 456.0 KiB |
| go   three_sum_closest            | 2452.2 KiB |

**Correction (2026-06-05 re-bench — supersedes the 2026-05-30 correction).** The history of this section, with each number's actual cause:

- **33.0 KiB (Slice 6.1 era, 2026-05-29):** real, but specific to the *mono-only* dispatch — the inlined comparator let `karac_vec_sort_by` + its runtime-archive dependencies get DCE'd, exactly as originally reasoned.
- **Slice 6.4 (same day) re-linked the runtime sort:** the length dispatch (`len ≤ 64` → inlined mono insertion sort, above → `karac_vec_sort_by` runtime callback) is required so large-N sorts don't regress to O(N²) — kata [#1665](../../1601-1700/1665-minimum-initial-energy-to-finish-tasks/)'s N=50k went 3.2 ms → 1.1 s under a strawman mono-only build. The fallback branch survives `-dead_strip` unless LLVM can const-prove the vec small, and `karac_vec_sort_by`'s `slice::sort_by` reaches std's panic infrastructure — keeping the DWARF symbolizer (`gimli`/`addr2line`/`object`/`rustc_demangle`) and its libstd retinue alive. That is **the same ~262 KiB libstd floor every auto-par binary pays** via `karac_par_reduce` (kata [#14](../14-longest-common-prefix/)'s auto-par binary: 312.5 KiB with zero sorts) — **not a sort-specific "symbolized sort-panic fix"** as the 05-30 correction guessed. A minimal no-`sort_by` program still builds to 32.8 KiB with zero gimli/addr2line symbols (re-verified 2026-06-05).
- **410.8 KiB (the 05-30 reading):** the floor *plus* ~116 KiB of transient inflation from a build-contaminated runtime archive (plain `cargo build` co-emits rlib + staticlib, defeating fat-LTO DCE — same incident as kata #14/#15 § Binary size). Rebuilt per the documented `cargo rustc … --crate-type staticlib` discipline, today's seq binary is **294.8 KiB** (`__text` 211,344 B of a 301,872 B image).

This kata remains the control: it returns a scalar `i64`, no nested `Vec`, yet lands within 8 bytes of kata [#15](../15-3sum/)'s seq binary — confirming the shared surface is the sort-pulled libstd floor, not output-allocation machinery. The *runtime* mono-sort win is intact (see § Runtime — seq lane and § Sort-dispatch history). The auto-par row adds only **+17.2 KiB** over seq, since the seq binary already carries the floor that dominates the image. Both kara rows ship at ~65% of Rust's 456.0 KiB; C's 32.8 KiB is the floor (no runtime archive, no symbolized panics). Reclaiming the ~262 KiB for sort-only binaries (a non-panicking lean large-N sort entry) is tracked on the karac side in `phase-7-codegen.md` Slice 6.2+.

### Runtime memory (peak)

| Implementation | Peak |
|---|---|
| c    three_sum_closest            | 1.0 MiB |
| **kāra three_sum_closest (seq)**  | **1.1 MiB** |
| rust three_sum_closest            | 1.1 MiB |
| **kāra three_sum_closest (auto-par)** | **1.7 MiB** |
| go   three_sum_closest            | 9.3 MiB |

Kāra seq's peak RSS (1,114,400 B) is byte-for-byte identical to Rust's and within one page of C (1,098,016 B) — indistinguishable at this granularity. (All three shifted down ~48 KiB vs the 05-30 readings — the same environment-wide dyld/OS page shift seen across the #12–#15 re-benches.) The auto-par regime's 1.7 MiB is the worker pool's per-thread scratch + partials, **1.3 MiB *lower* than kata 15's 3.0 MiB** despite running on the same shape — the body returns a scalar so workers' per-iter live set is just the sorted buffer, not a freshly-allocated `Vec[Vec[i64]]`. Same compiler, same auto-par dispatch, lighter body shape → measurably tighter steady-state RSS.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 three_sum_closest.c          | 2.5 MiB |
| **karac build three_sum_closest.kara** | **14.8 MiB** |
| rustc -O three_sum_closest.rs          | 37.2 MiB |

Kāra's compile-memory footprint is ~4.1× clang's and ~3.5× lower than rustc's on this kata — same shape as kata 15. (+0.1 MiB vs 05-30 — within the content-independent karac compile-mem floor band tracked across the corpus.)

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio is the codegen-vs-Rust gap. C calibrates the LLVM-backend floor, Go is the cross-runtime data point, and Python is the ergonomic foil. On this kata the **load-bearing result is equal-safety parity: Kāra is 0.98× of `rust -C overflow-checks=on`** — a hair faster than safety-matched Rust. (The ~1.08× against wrapping `rust -O` is the overflow-check tax, not a codegen gap; see the runtime section above.) The kata's first ship at 1.55× was the natural-pull trigger for karac Slice 6.1, which monomorphizes `Vec[i64].sort_by` inline-closure comparators into the user binary; the post-fix gap closed to codegen-quality noise, and to parity once safety is matched. Kata 15 with the same fix also runs **faster than Rust** (see [`15-3sum/README.md`](../15-3sum/README.md)). Kāra leads C by 1.62× and Go by 2.54× on this kata — the qsort indirect-call penalty and `sort.Slice` closure overhead are no longer offset on the Kāra side.
