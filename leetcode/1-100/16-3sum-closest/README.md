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

- **`Vec.from_slice(Slice[i64])` + in-place `sort_by`** — same shape as kata [#15](../15-3sum/) and kata [#1665](../../1601-1700/1665-minimum-initial-energy-to-finish-tasks/): copy `nums` into an owned `Vec[i64]`, then `s.sort_by(|a, b| a.cmp(b))`. The bench below exposes a sort-dispatch overhead this exercises (per-compare callback through `karac_vec_sort_by`); see § Runtime — seq lane for the disassembly-grounded finding. Verified to compile and run under both `karac run` and `karac build`.
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

Snapshot — M5 Pro, 2026-05-29, hyperfine `--warmup 5 --runs 30 --shell=none`. All four comparators single-threaded; the kāra row is `KARAC_AUTO_PAR=0`.

| Implementation | Wall time |
|---|---|
| rust three_sum_closest                | **62.5 ± 0.8 ms** |
| **kāra three_sum_closest (seq)**      | **96.8 ± 0.6 ms** |
| c    three_sum_closest (clang -O3)    | 113.5 ± 1.0 ms |
| go   three_sum_closest                | 185.4 ± 4.9 ms |

This is the same sort-bound shape as kata 15, but the inner body is the abs-and-track-best comparator pair instead of a triplet-emit + Vec-push. Rust wins at **1.55×** over Kāra seq — a meaningful gap, not the dead-heat of kata 15 (where the per-iter Vec output dominated and both monomorphizing compilers landed identically).

**Where the gap comes from (verified by disassembly).** The inner two-pointer body is *not* the culprit — the `arm64` listings show both compilers emit instruction-for-instruction-equivalent 21-instruction loops, including branchless `cneg` for `abs(sum - target)` on Kāra (the `if x < 0 { -x } else { x }` helper LLVM-lowers to a `cmp` + `cneg`, identical to Rust's `(sum - target).abs()`). What differs is the **sort dispatch**: kata 15's `sort_by(|a, b| a.cmp(b))` goes through `karac_vec_sort_by` in the runtime, which calls the user's comparator thunk via a function pointer per comparison; Rust's `sort_unstable()` monomorphizes the comparator inline. With kata 15's per-iter `Vec[Vec[i64]]` allocation dominating, this indirect-call overhead was masked. Kata 16 drops the nested-Vec output, the allocator stops dominating, and the sort dispatch surfaces.

A confirmation experiment in [`/tmp/three_sum_closest_inssort.kara`] (same body, but `sort_by(|a, b| a.cmp(b))` swapped for a hand-rolled inline insertion sort) runs at **70.6 ± 2.5 ms** — 26 ms faster than the headline 96.8 ms, closing **76% of the gap to Rust** (now 1.13× behind). That's the load-bearing finding: the per-compare indirect call through `karac_vec_sort_by`'s C-ABI callback dominates the residual Rust gap on tight, short-N sorts, and inlining the comparator into the sort body would close most of it. Flagged for karac follow-up: monomorphize `Vec.sort` / `Vec.sort_by` with inline-Ord-closure comparators on integer element types into a typed fast-path that doesn't go through the runtime callback. (An earlier diagnosis in this README blamed `abs_i64` lowering; that was wrong, retracted above — the disassembly proves Kāra's abs is already branchless.)

Kāra still beats C on this kata: **C trails Kāra seq by 1.17×** (113.5 vs 96.8 ms). Same reason as kata 15 — `qsort`'s indirect comparator call lands per comparison, and Kāra's runtime callback pays a similar cost; Kāra's edge is that the rest of the inner loop runs in a much tighter codegen, while C also pays `qsort`'s tagged-int-compare convention. Once the sort fast-path lands in karac, the Kāra/C gap on this kata should widen. Go trails further at **1.91× behind Kāra seq**: `sort.Slice` also pays the per-comparison closure indirect call, with GC and scheduler overhead on top.

### Runtime — auto-par regime

The `sum = sum + three_sum_closest(...)` reduction is auto-par-eligible; the default `karac build` recognizes it and emits a `karac_par_reduce` dispatch. NOT comparable to the single-thread rows above (BENCH.md two-lane discipline) — reported separately so the production-default Kāra behavior stays visible:

| Implementation | Wall time | User-CPU |
|---|---|---|
| **kāra three_sum_closest (auto-par default)** | **10.8 ± 1.0 ms** | 118.1 ms |

The auto-par binary is **9.0× faster than the kāra seq binary** (96.8 → 10.8 ms), spreading the K=1M case-rotation reduction across the perf cores (~11× user-CPU-to-wall ratio on M5 Pro). This is the legitimate-win case (BENCH.md kata #4 path): a real wall-time speedup with the `karac_par_reduce` machinery's +17 KiB binary and +0.7 MiB peak RSS. Notably it spreads **better than kata 15** (which got 7.2× from the same machinery on the same N=16, K=1M shape) — the scalar-return body has no nested-Vec output for the workers to contend on, so the per-worker memory pressure stays flat where kata 15's per-call `Vec[Vec[i64]]` allocations created allocator contention. Same compiler, same auto-par dispatch — the body shape determines how cleanly the speedup lands.

### Runtime — Python

| Run | Mean ± σ |
|---|---|
| `py three_sum_closest` (K=100k) | 155.8 ± 0.4 ms |

Python at K=100k is 156 ms; projecting to the compiled mirrors' K=1M (~1.56 s) puts it **~16.1× slower than kāra seq**. Tighter than kata 14's ~37× and kata 15's ~11.5× — CPython's per-iteration interpreter overhead is amortized over a fair amount of work per call (`sorted()` in C, an O(N²) crawl, the per-iter `abs` calls), and the inner body's lack of `list.append` calls (kata 15 builds nested lists per hit) saves CPython more than it saves the compiled mirrors. Against the auto-par regime the cross-lane ratio is ~144×.

### Compile elapsed (cold)

`--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Compiler | Time |
|---|---|
| clang -O3 three_sum_closest.c           | **52.7 ± 0.4 ms** |
| **karac build three_sum_closest.kara**  | **71.1 ± 0.5 ms** |
| rustc -O three_sum_closest.rs           | 131.2 ± 1.3 ms |

Kāra compiles **1.85× faster than `rustc -O`** and sits at **1.35× of clang -O3** — same shape as the rest of the corpus.

### Binary size

| Implementation | Size |
|---|---|
| c    three_sum_closest            | 32.8 KiB |
| **kāra three_sum_closest (seq)**  | **359.4 KiB** |
| **kāra three_sum_closest (auto-par)** | **376.6 KiB** |
| rust three_sum_closest            | 456.0 KiB |
| go   three_sum_closest            | 2452.2 KiB |

The seq binary is identical in size to kata 15's seq binary (359.4 KiB both katas) — the `sort_by` + comparison-sort + `Vec.from_slice` runtime surface dominates, and dropping the nested-Vec output type doesn't subtract anything the seq image needs. The auto-par delta is again **+17 KiB**, the same as kata 15 (`karac_par_reduce` machinery cost), with the seq image already carrying most of the support code. Kāra ships **97 KiB under Rust on the seq row and 79 KiB under Rust on the auto-par row.**

### Runtime memory (peak)

| Implementation | Peak |
|---|---|
| c    three_sum_closest            | 1.1 MiB |
| **kāra three_sum_closest (seq)**  | **1.1 MiB** |
| rust three_sum_closest            | 1.1 MiB |
| **kāra three_sum_closest (auto-par)** | **1.8 MiB** |
| go   three_sum_closest            | 9.7 MiB |

Kāra seq's peak RSS lands at 1.11 MiB — within ~16 KiB of C and Rust, indistinguishable on the I/O at this granularity. The auto-par regime's 1.8 MiB is the worker pool's per-thread scratch + partials, **0.4 MiB *lower* than kata 15's 3.0 MiB** despite running on the same shape — because the body returns a scalar, the workers' per-iter live set is just the sorted buffer, not a freshly-allocated `Vec[Vec[i64]]`. Same auto-par dispatch, same hardware, lighter body shape → measurably tighter steady-state RSS. Go's 9.7 MiB carries its GC roots + scheduler arena (unchanged from kata 15).

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 three_sum_closest.c          | 2.6 MiB |
| **karac build three_sum_closest.kara** | **10.3 MiB** |
| rustc -O three_sum_closest.rs          | 37.4 MiB |

Kāra's compile-memory footprint is ~4.0× clang's and ~3.6× lower than rustc's on this kata — same shape as kata 15.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio is the codegen-vs-Rust gap. C calibrates the LLVM-backend floor, Go is the cross-runtime data point, and Python is the ergonomic foil. On this kata the **Kāra/Rust 1.55× gap is the load-bearing result** — kata 15 was a tie because the per-iter Vec output dominated; this kata removes that output, exposes the per-compare sort dispatch, and surfaces the `karac_vec_sort_by` callback-overhead gap (insertion-sort experiment closes 76% of it). Once that fast path lands in karac, this kata should reproduce kata 15's tie pattern. Kāra still leads C (qsort indirect-call penalty) and Go (sort.Slice closure + GC).
