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

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, and Go. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`binary_search_partition.{kara,rs,c}`, `go-seq/main.go`, and the par-lane mirrors `binary_search_partition_par.c`, `rayon/`, `go-par/`). Every number in the tables below is from [`bench/results.json`](bench/results.json). The Python mirror [`bench/binary_search_partition.py`](bench/binary_search_partition.py) is gated behind `KARA_BENCH_INCLUDE_PY=1` — at K=10M calls it lands at ~2s and would block the bench by default; it is not in the current feed.

Per [`../../../BENCH.md`](../../../BENCH.md), the workload is the binary-search inner loop carried by `middle_pair_off` over 1M-element inputs with `K = 10_000_000` outer iterations rotated by `off = k % R` (`R = 1000`) so per-iter inputs vary and CSE can't hoist. The outer reduction (`sum += pair[0] + pair[1]`) is recognized by karac's implicit auto-par, which parallelizes it by default. On the current v2/MIR backend that dispatch goes through the M4 task runtime — detect it with `nm -gU target/binary_search_partition_kara | grep karac_mir_task_spawn` (the legacy backend's `karac_par_reduce` symbol no longer appears). The bench builds two kara binaries to keep the BENCH.md two-lane discipline honest:

- **`binary_search_partition_kara_seq`** — built with `KARAC_AUTO_PAR=0` (the documented gate for side-by-side seq-vs-par benchmarking of the same workload). The within-lane row directly comparable to rustc-O / clang-O3 / go build.
- **`binary_search_partition_kara`** — default `karac build` output. Picks up auto-par dispatch (654% CPU on this workload). Reported in the par lane against C+pthreads, Rust+rayon and Go goroutines.

**Workload.** Two `Vec[i64]` inputs of `M + R = N + R = 1_001_000` elements built once: `base_a = [0, 2, 4, ...]` (alternating evens), `base_b = [1, 3, 5, ...]` (alternating odds). The hot loop calls `middle_pair_off(base_a, off, M, base_b, off, N)` 10M times where `off = k % R`; per-iter contribution to the sink is `4*off + (2M - 1)`. All mirrors agree on `20_019_970_000_000` before any timing runs — `bench.sh` fails loudly on mismatch.

Note the bench's `middle_pair_off(a, a_off, a_len, b, b_off, b_len)` signature differs from the kata file's `middle_pair(a, b)`. The offset+length form lets the bench rotate inputs without sub-slicing on the inner loop, which would be zero-cost in Kāra/Rust/C/Go but `O(len)` per iter in Python (`list[a:b]` copies). All languages use the same offset form so the per-iter work stays comparable.

Snapshot — Apple M5 Pro (6P+12E), Darwin 25.6.0, measured 2026-10-29 (UTC); karac 0.1.0-dev.13686+g04628b0eb (v2/MIR backend), rustc 1.95.0, Apple clang 21.0.0, go 1.26.3; hyperfine `--warmup 5 --runs 30 --shell=none`.

### Re-bench 2026-10-29 — what moved

- **Seq lane: holds.** Kāra 16.4 ms vs 15.9 ms on the previous snapshot; the kara-seq binary retires the same instruction count as the legacy backend (556 M vs 564 M), so the shift is noise. Comparators moved −1.5% to +1.4%.
- **Par lane: regression.** Kāra auto-par went 3.9 → 5.9 ms (+52%) while rayon (+1.8%), goroutines (+5.1%) and the C floor (+4.2%) barely moved. It used to edge rayon; it is now 1.44× rayon and roughly level with Go. Measured cause, tracked as B-2026-10-28-35: on the M4 runtime, going multi-worker adds a constant ~207 M instructions (+37%) independent of worker count, and 2 workers give no speedup at twice the CPU.
- **Binary size: regression.** Kāra seq binary +302 KB (now 336,648 B), auto-par binary +84 KB; tracked as B-2026-10-28-36. Comparator binaries unchanged.
- **Compile cost: regression.** `karac build` 96 → 184 ms and 25 → 70 MiB peak RSS, while rustc and clang stayed flat; tracked as B-2026-10-28-37.

### Runtime — seq lane

The equal-safety `rust -C overflow-checks=on` lane is recorded alongside the wrapping `rust -O` lane — it is the apples-to-apples Kāra-vs-Rust row, since Kāra checks overflow by default:

| Implementation | Wall time | User-CPU | CPU% |
|---|---|---|---|
| c    binary_search_partition (clang -O3) | **12.0 ms ± 0.1 ms** | 10.7 ms | 96% |
| **kāra binary_search_partition** (`KARAC_AUTO_PAR=0`) | **16.4 ms ± 0.5 ms** | 14.5 ms | 96% |
| rust binary_search_partition (rustc -O)  | **15.6 ms ± 0.2 ms** | 13.9 ms | 96% |
| rust binary_search_partition (overflow-checks=on) | **15.7 ms ± 0.4 ms** | 14.3 ms | 97% |
| go   binary_search_partition             | **27.6 ms ± 0.2 ms** | 25.8 ms | 99% |

**The Kāra-vs-Rust headline is the equal-safety row.** Kāra checks integer overflow by default — the sink reduction `sum += pair[0] + pair[1]` and the partition index arithmetic are all checked adds. `rustc -O` *silently wraps*, so the apples-to-apples comparison is `rust -C overflow-checks=on`, which restores the same checked arithmetic Kāra ships by default. Against it Kāra runs **1.05×** (16.4 vs 15.7 ms), and 1.05× against `rust -O` (16.4 vs 15.6 ms). The equal-safety Rust row is statistically indistinguishable from `rust -O` here: the binary-search body has little hot integer arithmetic to check, so the overflow tax is near-zero for Rust.

The C lead (Kāra 1.37×, Rust 1.30× of clang) is consistent across this kata family: clang's `int64_t*` + struct-return Pair maps to one fewer load + one register pair vs Rust's tuple-return + Kāra's `Array[i64, 2]` return — a constant per-call gap on top of the same algorithm; clang also skips the overflow checks Kāra runs. Go's 27.6 ms reflects per-iter slice-bounds checks + no SROA equivalent on the tuple return.

### Runtime — par lane (auto-par vs hand-written parallel)

Same snapshot. All four rows run the same outer reduction in parallel; only the Kāra row has no parallel source code:

| Implementation | Wall time | User-CPU | CPU% |
|---|---|---|---|
| c    binary_search_partition_par (pthreads, C floor) | **3.4 ms ± 0.2 ms** | 16.1 ms | 513% |
| rust binary_search_partition (rayon `into_par_iter`) | **4.1 ms ± 0.5 ms** | 22.1 ms | 660% |
| **kāra binary_search_partition** (auto-par, no parallel code) | **5.9 ms ± 0.3 ms** | 35.8 ms | 655% |
| go   binary_search_partition (goroutines + WaitGroup) | **6.2 ms ± 0.3 ms** | 35.7 ms | 611% |

**These rows are not comparable to the seq-lane rows above.** Per BENCH.md's two-lane discipline, a ratio between a par row and a seq row conflates codegen quality with whether the program opted into parallelism; compare par rows only with each other.

Within the lane, Kāra auto-par is 1.73× the C pthreads floor, 1.44× Rust+rayon, and 0.94× Go goroutines (slightly ahead). Against its own seq build the auto-par binary is 2.81× faster in wall time (16.4 → 5.9 ms) for 2.46× the user CPU (14.5 → 35.8 ms). On the previous snapshot it was 3.9 ms and ahead of rayon; the gap that opened is the multi-worker fixed cost tracked as B-2026-10-28-35 (see the re-bench note above). The buyer-facing point stands — a parallel speedup with no `par`, no `Send`/`Sync` reasoning and no thread pool in the source — but on this snapshot it lands at goroutine level, not rayon level.

### How we got here

The first measurement on this bench landed at **1.83× of Rust** (kara 28.4 ms vs rust 15.5 ms). The README at that revision pre-baked a "bounds checks dominate" hypothesis to explain it. Empirical investigation killed that hypothesis:

1. **`objdump --syms` on both binaries.** Rust had `middle_pair_off` fully inlined into `main` — the symbol was gone. Kara had `_middle_pair_off` as a `g F __TEXT,__text` global symbol and `main` called it via `bl` 10M times.
2. **`objdump -d` on the inner loop.** Both implementations emit bounds checks (`cmp + b.hs <panic>`) on every indexed slice read; the instruction counts roughly match. Bounds checks were *not* the differentiator.
3. **Manual-inline experiment.** Pasted the binary-search body directly into kara's `main` (no callsite), measured: 17.0 ms — within noise of Rust. The inner loop itself was fine; the call was the problem.

Root cause: `src/codegen/functions.rs:117` was passing `None` to `module.add_function`, which inkwell maps to `ExternalLinkage`. External linkage forces LLVM to keep the function symbol live in the object file even after every call site has been inlined, and the inliner's cost model is more conservative with external callees. Rust by default emits non-`pub` items with internal/hidden linkage, so its inliner has free rein.

Fix shipped in karac [`bdac0d8`](../../../../karac-rust/): non-`pub`, non-FFI-marked user functions now emit `Linkage::Internal`. `pub` keeps External for future multi-crate compatibility; `#[no_mangle]` / `#[used]` keep External so FFI symbols / link-section anchors survive. With the patched karac, `objdump --syms` on this bench's binary shows `middle_pair_off`, `min_i64`, `max_i64` all elided — LLVM inlined them all and dropped the standalone definitions. Cross-kata regression check on the suite is in the [karac commit message](../../../../karac-rust/); the headline: no regressions; kata [#88](../88-merge-sorted-array/) also picked up a 13% speedup from the same change (its `merge` function was hit by the same external-linkage issue).

The lesson worth keeping: **don't pre-bake explanations for perf gaps.** The first three suspects ("bounds checks", "no autovectorization", "branch prediction") were all plausible — and all wrong. The actual cause was visible in five minutes of `objdump --syms` once we looked, but the rhetorical framing on the README would have buried it indefinitely.

The 2026-10-29 numbers in this section are on the v2/MIR backend's M4 auto-par runtime; the linkage fix above is a legacy-backend history and is unchanged by it.

### Compile elapsed (cold)

`--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Workload | Kāra (`karac build`) | Rust (`rustc -O`) | C (`clang -O3`) |
|---|---|---|---|
| `binary_search_partition` | **184.4 ms ± 3.2 ms** | 87.0 ms ± 0.9 ms | 44.3 ms ± 1.0 ms |

Single-file invocations only — the Go module's `go build` mixes module resolution + std-lib link with codegen and is deliberately excluded per BENCH.md. Karac is 2.12× slower than rustc and 4.16× slower than clang on this snapshot (it was faster than rustc before the regression tracked as B-2026-10-28-37).

### Binary size

| Implementation | Bytes | KiB |
|---|---|---|
| c    binary_search_partition (seq) | 33,528 | 32.7 |
| c    binary_search_partition_par (pthreads) | 33,728 | 32.9 |
| **kāra binary_search_partition (seq)** | **336,648** | **328.8** |
| kāra binary_search_partition (auto-par) | 403,848 | 394.4 |
| rust binary_search_partition (rayon) | 464,928 | 454.0 |
| rust binary_search_partition (seq) | 466,360 | 455.4 |
| go   binary_search_partition (seq) | 2,492,546 | 2,434.1 |
| go   binary_search_partition (goroutines) | 2,509,906 | 2,451.1 |

The seq-lane Kāra binary grew +302 KB on this snapshot and is now ~10× clang's (it was within ~1.5× before); that growth is tracked as B-2026-10-28-36. The auto-par variant adds a further 67,200 B (65.6 KiB) over the seq build for the M4 task runtime. Both remain smaller than Rust's.

### Runtime memory (peak)

| Implementation | Bytes | MiB |
|---|---|---|
| c    binary_search_partition (seq) | 17,138,000 | 16.3 |
| rust binary_search_partition (seq) | 17,170,768 | 16.4 |
| **kāra binary_search_partition (seq)** | **17,187,176** | **16.4** |
| c    binary_search_partition_par (pthreads) | 17,531,240 | 16.7 |
| kāra binary_search_partition (auto-par) | 17,646,048 | 16.8 |
| rust binary_search_partition (rayon) | 18,006,376 | 17.2 |
| go   binary_search_partition (seq) | 19,677,712 | 18.8 |
| go   binary_search_partition (goroutines) | 20,693,448 | 19.7 |

Kāra-seq is at C/Rust parity (within 0.05 MiB). Each compiled comparator holds two int64 buffers of `M + R = 1_001_000` elements (~8 MiB each, ~16 MiB total) which dominates the steady state. Auto-par Kāra adds ~0.4 MiB for worker stacks, below rayon's +0.8 MiB. Go carries its GC roots + scheduler arena overhead.

### Compile memory (cold)

| Compiler invocation | Bytes | MiB |
|---|---|---|
| `clang -O3 binary_search_partition.c`      | 2,736,440  | 2.6 |
| `rustc -O binary_search_partition.rs`      | 30,900,776 | 29.5 |
| **`karac build binary_search_partition.kara`** | **73,548,328** | **70.1** |

Kāra's compile-memory footprint is ~27× clang's and ~2.4× rustc's on this kata, up from 25 MiB on the previous snapshot (B-2026-10-28-37).

### Numbers published here are reference data

The CI gate's source-of-truth aggregate lives in [`karac-rust/bench/compile_speed/`](../../../../karac-rust/bench/compile_speed/README.md) (different corpus: curated subset + synthetic 10K-LOC stress program).
