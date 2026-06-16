# 4. Median of Two Sorted Arrays

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** Array, Binary Search, Divide and Conquer &nbsp;·&nbsp; **Source:** [leetcode.com/problems/median-of-two-sorted-arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/)

Given two sorted arrays `nums1` and `nums2` of size `m` and `n` respectively, return the median of the two sorted arrays. The required runtime complexity is `O(log(m + n))`.

**Constraints:** `0 ≤ m, n ≤ 1000`, `1 ≤ m + n ≤ 2000`, `-10⁶ ≤ nums1[i], nums2[i] ≤ 10⁶`, both inputs sorted non-decreasing.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| Binary-search partition | O(log(min(m, n))) time, O(1) extra space | [`binary_search_partition.kara`](binary_search_partition.kara) ✓ via `karac run` / `karac build` | [`binary_search_partition.py`](binary_search_partition.py) ✓ |

`✓` runs end-to-end today.

### Why binary-search partition

The naive "merge then index" answer is O(m + n) and misses the problem's stated bound. The trick is that *we don't need the merged sequence* — only the value(s) at the middle index. Choosing a partition point `i` in `nums1` and the matching `j = (m + n + 1) / 2 − i` in `nums2` carves the two inputs into a "left half" of size `(m + n + 1) / 2` and a "right half" of size `(m + n) / 2`. The partition is **correct** when every value on the left is `≤` every value on the right — checked with two cross-comparisons, `nums1[i − 1] ≤ nums2[j]` and `nums2[j − 1] ≤ nums1[i]`.

Only `i` is searched — `j` is derived from the invariant — so the loop bounds are `[0, m]` and the runtime is `O(log m)`. Ensuring `m ≤ n` (by swapping inputs at the entry) makes it `O(log min(m, n))`, which also keeps `j` non-negative for every `i`.

## Kāra features exercised

- **`Slice[i64]` parameter** — `middle_pair` takes both inputs by immutable slice; fresh `Array[i64, N]` literals at the call site coerce to `Slice[i64]` (same coercion as kata [#88](../88-merge-sorted-array/)).
- **Recursion across the `Slice[i64]` boundary** — the `m > n` swap is a one-deep self-call with arguments reversed; the second invocation skips the branch.
- **`i64.MIN` / `i64.MAX` as ±∞ sentinels** — primitive-type associated constants lowered to LLVM constants, used to collapse the four boundary cases into the interior cross-check shape.
- **`if cond { x } else { y }` as expression** — materialises the four sentinel-guarded values into `i64` bindings in one line each.
- **`else if` chain** — three-way branch on the cross-check outcome; parser desugars to nested `if`/`else`.
- **`Array[i64, 2]` return** — the same pair-shape used by kata [#1](../1-two-sum/) and kata [#5](../5-longest-palindromic-substring/); will become a real tuple once `Option[(i64, i64)]` is solid in the interpreter.

## Running

```bash
# Kāra (compiled or interpreted — both work)
karac run   binary_search_partition.kara
karac build binary_search_partition.kara && ./binary_search_partition

# Python
python3 binary_search_partition.py
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, and Go. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`binary_search_partition.{kara,rs,c}`, `go-seq/main.go`). The Python mirror [`bench/binary_search_partition.py`](bench/binary_search_partition.py) is gated behind `KARA_BENCH_INCLUDE_PY=1` — at K=10M calls it lands at ~2s and would block the bench by default.

Per [`../../../BENCH.md`](../../../BENCH.md), the workload is the binary-search inner loop carried by `middle_pair_off` over 1M-element inputs with `K = 10_000_000` outer iterations rotated by `off = k % R` (`R = 1000`) so per-iter inputs vary and CSE can't hoist. The outer reduction (`sum += pair[0] + pair[1]`) has a strict cross-iteration dependency — karac's auto-par-on-reduction recognizes it and emits a `karac_par_reduce` dispatch by default. The bench builds two kara binaries to keep the BENCH.md two-lane discipline honest:

- **`binary_search_partition_kara_seq`** — built with `KARAC_AUTO_PAR=0` (codegen.rs Slice 6 gate — documented mechanism for side-by-side seq-vs-par benchmarking of the same workload). The within-lane row directly comparable to rustc-O / clang-O3 / go build.
- **`binary_search_partition_kara`** — default `karac build` output. Picks up auto-par dispatch (~3.3 cores active on this workload). Reported separately so the production-default Kara behavior stays visible.

**Workload.** Two `Vec[i64]` inputs of `M + R = N + R = 1_001_000` elements built once: `base_a = [0, 2, 4, ...]` (alternating evens), `base_b = [1, 3, 5, ...]` (alternating odds). The hot loop calls `middle_pair_off(base_a, off, M, base_b, off, N)` 10M times where `off = k % R`; per-iter contribution to the sink is `4*off + (2M - 1)`. All five mirrors agree on `20_019_970_000_000` before any timing runs — `bench.sh` fails loudly on mismatch.

Note the bench's `middle_pair_off(a, a_off, a_len, b, b_off, b_len)` signature differs from the kata file's `middle_pair(a, b)`. The offset+length form lets the bench rotate inputs without sub-slicing on the inner loop, which would be zero-cost in Kāra/Rust/C/Go but `O(len)` per iter in Python (`list[a:b]` copies). All five languages use the same offset form so the per-iter work stays comparable.

### Runtime — seq lane

Snapshot — M5 Pro, 2026-06-16, hyperfine `--warmup 5 --runs 30 --shell=none`. The equal-safety `rust -C overflow-checks=on` lane is recorded alongside the wrapping `rust -O` lane — it is the apples-to-apples Kāra-vs-Rust row, since Kāra checks overflow by default:

| Implementation | Wall time | User-CPU | CPU% |
|---|---|---|---|
| c    binary_search_partition (clang -O3) | **12.4 ms ± 0.1 ms** | 11.0 ms | 92% |
| **kāra binary_search_partition** (`KARAC_AUTO_PAR=0`) | **16.9 ms ± 3.3 ms** | 14.0 ms | 91% |
| rust binary_search_partition (rustc -O)  | **15.8 ms ± 0.4 ms** | 14.0 ms | 94% |
| rust binary_search_partition (overflow-checks=on) | **15.9 ms ± 0.5 ms** | 14.0 ms | 94% |
| go   binary_search_partition             | **28.5 ms ± 0.4 ms** | 26.0 ms | 97% |

**The Kāra-vs-Rust headline is the equal-safety row.** Kāra checks integer overflow by default — the sink reduction `sum += pair[0] + pair[1]` and the partition index arithmetic are all checked adds. `rustc -O` *silently wraps*, so the apples-to-apples comparison is `rust -C overflow-checks=on`, which restores the same checked arithmetic Kāra ships by default. Against it Kāra runs **1.06×** (16.9 vs 15.9 ms — within σ given the kara row's wide spread this run). Note the equal-safety Rust row is statistically indistinguishable from `rust -O` here (15.9 vs 15.8 ms): the binary-search body has little hot integer arithmetic to check, so the overflow tax is near-zero for Rust — and Kāra still lands within noise of both. This is the cleanest per-core "is karac's codegen at parity with rustc?" answer for this workload.

The C win (~1.36×) is consistent across this kata family: clang's `int64_t*` + struct-return Pair maps to one fewer load + one register pair vs Rust's tuple-return + Kāra's `Array[i64, 2]` return — a constant per-call gap on top of the same algorithm; clang also skips the overflow checks Kāra runs. Go's 28.5 ms reflects per-iter slice-bounds checks + no SROA equivalent on the tuple return.

### Runtime — auto-par regime (kara default, multi-core)

Same snapshot, default `karac build` output:

| Implementation | Wall time | User-CPU | CPU% |
|---|---|---|---|
| **kāra binary_search_partition** (auto-par on reduction) | **4.0 ms ± 0.4 ms** | 19.0 ms | ~475% (~4.8 cores) |

Karac's auto-par-on-reduction recognizes the `sum +=` reduction in `main`'s K=10M loop and emits a `karac_par_reduce` dispatch — binary carries `karac_par_reduce` + `karac_reduce_combine_add_i64` + `karac_reduce_worker_0` symbols, ~4.8 cores active during the run. The wall-time win over the seq-lane Kāra row is **4.0×** (16.2 / 4.0); total CPU time goes up 36% (14.0 → 19.0 ms user) as the cost of dispatch + per-worker fixed overhead. Net: real production wall-time speedup, paid for in additional CPU and a +263 KiB binary footprint.

**Not headlined against the C / Rust / Go rows above.** Per BENCH.md's two-lane discipline, cross-lane wall-time ratios are not meaningful — naming "kara is 3× faster than rust" here would conflate per-core codegen quality with whether the comparator opted into parallelism. The seq lane above is the within-lane comparison; this row is what Kāra delivers as a *language-level* choice on top of that codegen-quality baseline. A follow-up CR can add a true par lane (rayon + goroutines variants of `main`'s outer reduction) so this number lands against in-lane comparators.

### How we got here

The first measurement on this bench landed at **1.83× of Rust** (kara 28.4 ms vs rust 15.5 ms). The README at that revision pre-baked a "bounds checks dominate" hypothesis to explain it. Empirical investigation killed that hypothesis:

1. **`objdump --syms` on both binaries.** Rust had `middle_pair_off` fully inlined into `main` — the symbol was gone. Kara had `_middle_pair_off` as a `g F __TEXT,__text` global symbol and `main` called it via `bl` 10M times.
2. **`objdump -d` on the inner loop.** Both implementations emit bounds checks (`cmp + b.hs <panic>`) on every indexed slice read; the instruction counts roughly match. Bounds checks were *not* the differentiator.
3. **Manual-inline experiment.** Pasted the binary-search body directly into kara's `main` (no callsite), measured: 17.0 ms — within noise of Rust. The inner loop itself was fine; the call was the problem.

Root cause: `src/codegen/functions.rs:117` was passing `None` to `module.add_function`, which inkwell maps to `ExternalLinkage`. External linkage forces LLVM to keep the function symbol live in the object file even after every call site has been inlined, and the inliner's cost model is more conservative with external callees. Rust by default emits non-`pub` items with internal/hidden linkage, so its inliner has free rein.

Fix shipped in karac [`bdac0d8`](../../../../karac-rust/): non-`pub`, non-FFI-marked user functions now emit `Linkage::Internal`. `pub` keeps External for future multi-crate compatibility; `#[no_mangle]` / `#[used]` keep External so FFI symbols / link-section anchors survive. With the patched karac, `objdump --syms` on this bench's binary shows `middle_pair_off`, `min_i64`, `max_i64` all elided — LLVM inlined them all and dropped the standalone definitions. Cross-kata regression check on the suite is in the [karac commit message](../../../../karac-rust/); the headline: no regressions; kata [#88](../88-merge-sorted-array/) also picked up a 13% speedup from the same change (its `merge` function was hit by the same external-linkage issue).

The lesson worth keeping: **don't pre-bake explanations for perf gaps.** The first three suspects ("bounds checks", "no autovectorization", "branch prediction") were all plausible — and all wrong. The actual cause was visible in five minutes of `objdump --syms` once we looked, but the rhetorical framing on the README would have buried it indefinitely.

### Compile elapsed (cold)

`--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Workload | Kāra (`karac build`) | Rust (`rustc -O`) | C (`clang -O3`) |
|---|---|---|---|
| `binary_search_partition` | **79.1 ms ± 0.5 ms** | 101.2 ms ± 1.5 ms | 46.8 ms ± 0.3 ms |

Single-file invocations only — the Go module's `go build` mixes module resolution + std-lib link with codegen and is deliberately excluded per BENCH.md. Karac is 1.28× faster than rustc and 1.69× slower than clang.

### Binary size

| Implementation | Bytes | KiB |
|---|---|---|
| c    binary_search_partition | 33,528 | 32.7 |
| **kāra binary_search_partition (seq)** | **34,072** | **33.3** |
| kāra binary_search_partition (auto-par) | 303,128 | 296.0 |
| rust binary_search_partition | 466,344 | 455.4 |
| go   binary_search_partition | 2,492,546 | 2,434.1 |

The seq-lane Kāra binary sits within ~1.5× of clang's. The auto-par variant grows +263 KiB to carry the par_reduce machinery (per-branch trampolines + reduction-combine globals + worker-pool registration) — the same +263 KiB ballast kata [#91](../91-decode-ways/#binary-size) saw when it was inappropriately auto-paring. Here the ballast is paid for in a real 4.0× wall-time win, so it stays in.

### Runtime memory (peak)

| Implementation | Bytes | MiB |
|---|---|---|
| c    binary_search_partition | 17,137,976 | 16.3 |
| **kāra binary_search_partition (seq)** | **17,170,744** | **16.4** |
| rust binary_search_partition | 17,187,128 | 16.4 |
| kāra binary_search_partition (auto-par) | 17,580,368 | 16.8 |
| go   binary_search_partition | 19,874,344 | 19.0 |
| py   binary_search_partition | 89,981,408 | 85.8 |

Kāra-seq is at C/Rust parity (within 0.05 MiB). Each compiled comparator holds two int64 buffers of `M + R = 1_001_000` elements (~8 MiB each, ~16 MiB total) which dominates the steady state. Auto-par Kāra adds ~0.4 MiB for worker stacks. Go's 19.0 MiB carries its GC roots + scheduler arena overhead. Python's 85.8 MiB is the CPython object-per-int representation on a 1M-element list.

### Compile memory (cold)

| Compiler invocation | Bytes | MiB |
|---|---|---|
| `clang -O3 binary_search_partition.c`      | 2,687,288  | 2.6 |
| **`karac build binary_search_partition.kara`** | **14,385,608** | **13.7** |
| `rustc -O binary_search_partition.rs`      | 30,900,872 | 29.5 |

Kāra's compile-memory footprint is ~5.3× clang's and ~2.1× smaller than rustc's on this kata.

### Numbers published here are reference data

The CI gate's source-of-truth aggregate lives in [`karac-rust/bench/compile_speed/`](../../../../karac-rust/bench/compile_speed/README.md) (different corpus: curated subset + synthetic 10K-LOC stress program).
