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

### How to run

```bash
brew install hyperfine    # one-time, also needs rustc (rustup), clang, go, karac
./bench/bench.sh
```

`bench/bench.sh` builds the Rust file with `rustc -O`, the C file with `clang -O3`, the Kāra file with `karac build`, and the Go module with `go build` (all cached in `bench/target/`, gitignored), then runs five passes per the [BENCH.md protocol](../../../BENCH.md):

1. **Sink agreement** — every compiled mirror's stdout must equal `20_019_970_000_000` (Python opt-in via `KARA_BENCH_INCLUDE_PY=1`).
2. **Runtime (short, compiled)** — `hyperfine --warmup 5 --runs 30 --shell=none` across kara/rust/c/go. Inputs are `M = N = 1_000_000` perfectly-alternating sorted prefixes; each outer iter picks `off = k % R` with `R = 1000` and runs `middle_pair_off(base_a, off, M, base_b, off, N)`. `K = 10_000_000` outer iterations. The rotation makes each iter's inputs unique, defeating the cross-iteration CSE that would otherwise hoist the pure `middle_pair_off` call out of the loop and reduce the bench to a multiply-by-`K`.
3. **Runtime (long, py)** — `hyperfine --warmup 2 --runs 10` for the Python mirror in its own batch.
4. **Compile elapsed (cold)** — `hyperfine` with a `--prepare` step that deletes the artifact before every run, so each measurement is a fresh `karac build` / `rustc -O` / `clang -O3` invocation. Go is excluded per BENCH.md.
5. **Binary size, runtime memory, compile memory** — one row per comparator.

| File | What it does |
|---|---|
| [`bench/binary_search_partition.kara`](bench/binary_search_partition.kara) | M = N = 1_000_000, R = 1000, K = 10_000_000, rotated alternating-evens / alternating-odds inputs |
| [`bench/binary_search_partition.rs`](bench/binary_search_partition.rs) | Algorithmic mirror; compiled with `rustc -O` |
| [`bench/binary_search_partition.c`](bench/binary_search_partition.c) | Algorithmic mirror; raw `int64_t*` arrays; compiled with `clang -O3` |
| [`bench/go-seq/main.go`](bench/go-seq/main.go) | Algorithmic mirror; `[]int64` slices; `math.MinInt64`/`MaxInt64` sentinels; built with `go build` |
| [`bench/binary_search_partition.py`](bench/binary_search_partition.py) | Algorithmic mirror — same M, N, R, K, same offset+length API |

All five print the same sum-of-results sink (`Σ_{k<K} (lower + upper) = 20_019_970_000_000`) so the algorithm's output participates in I/O and can't be elided.

Note the bench's `middle_pair_off(a, a_off, a_len, b, b_off, b_len)` signature differs from the kata file's `middle_pair(a, b)`. The offset+length form lets the bench rotate inputs without sub-slicing on the inner loop, which would be zero-cost in Kāra/Rust/C/Go (slices are pointer + length) but `O(len)` per iter in Python (`list[a:b]` copies). All five languages here use the same offset form so the per-iter work stays comparable.

### Runtime — Kāra auto-par lands on top of the comparators

Snapshot — M5 Pro, 2026-05-23, hyperfine `--warmup 5 --runs 30 --shell=none`:

| Run | Mean ± σ | CPU% |
|---|---|---|
| **`kara binary_search_partition` (codegen, auto-par on reduction)** | **4.6 ± 0.4 ms** | ~410% (~3.3 cores) |
| `c    binary_search_partition` (clang -O3, single-thread) | 13.0 ± 0.3 ms | ~85% |
| `rust binary_search_partition` (rustc -O, single-thread)  | 16.8 ± 0.4 ms | ~86% |
| `go   binary_search_partition` (go build, single-thread)  | 29.5 ± 1.0 ms | ~91% |
| `py   binary_search_partition` (CPython, separate batch)  | 2.066 ± 0.032 s | ~99% |

**Caveat — the headline is cross-lane.** Karac auto-parallelizes the `sum +=` reduction in `main`'s K = 10M loop (binary carries `karac_par_reduce` + `karac_reduce_combine_add_i64` + `karac_reduce_worker_0` symbols, ~3.3 cores active during the run). The kata source has no `#[par_unordered]` — this is implicit, codegen-driven auto-par from the post-`74f81cd` reduction-recognition work (gated by the `181b0ad` memory-bound rejection check). The C / Rust / Go mirrors here run single-threaded as written, so the per BENCH.md framing makes Kāra's 4.6 ms a **par-lane number** measured against **seq-lane comparators**.

**The honest within-lane reads.** Two reasonable ways to bracket this:

- **Single-thread snapshot (pre-auto-par regime, 2026-05-17):** kara 16.2 ms, rust 15.8 ms, py 2.021 s. Within the seq lane, kara was at **1.03× of Rust** — measurement-noise parity. That's still the cleanest "is karac's codegen at per-core parity with rustc?" answer for this workload, and the answer is yes.
- **Today's auto-par regime (2026-05-23):** kara 4.6 ms is what `karac build` produces for the source as written. Production code shipped to users runs *this* binary, not the hypothetical single-threaded one. The 3.5× speedup over the pre-auto-par snapshot is real and bankable for the use case where Kāra is the only compiler in the harness.

The right comparison framing depends on the question being asked. For "codegen-vs-Rust on a per-core basis" the 2026-05-17 snapshot stays load-bearing. For "how fast is Kāra on this kata as written" the 2026-05-23 4.6 ms is the answer.

A follow-up CR can add a true par lane (rayon + goroutines variants of `main`'s outer reduction) so the auto-par result lands against in-lane comparators; until then, the seq-lane numbers below treat C / Rust / Go as the within-lane comparator set, and Kāra's row stands apart with the par caveat.

### How we got here

The first measurement on this bench landed at **1.83× of Rust** (kara 28.4 ms vs rust 15.5 ms). The README at that revision pre-baked a "bounds checks dominate" hypothesis to explain it. Empirical investigation killed that hypothesis:

1. **`objdump --syms` on both binaries.** Rust had `middle_pair_off` fully inlined into `main` — the symbol was gone. Kara had `_middle_pair_off` as a `g F __TEXT,__text` global symbol and `main` called it via `bl` 10M times.
2. **`objdump -d` on the inner loop.** Both implementations emit bounds checks (`cmp + b.hs <panic>`) on every indexed slice read; the instruction counts roughly match. Bounds checks were *not* the differentiator.
3. **Manual-inline experiment.** Pasted the binary-search body directly into kara's `main` (no callsite), measured: 17.0 ms — within noise of Rust. The inner loop itself was fine; the call was the problem.

Root cause: `src/codegen/functions.rs:117` was passing `None` to `module.add_function`, which inkwell maps to `ExternalLinkage`. External linkage forces LLVM to keep the function symbol live in the object file even after every call site has been inlined, and the inliner's cost model is more conservative with external callees. Rust by default emits non-`pub` items with internal/hidden linkage, so its inliner has free rein.

Fix shipped in karac [`bdac0d8`](../../../../karac-rust/): non-`pub`, non-FFI-marked user functions now emit `Linkage::Internal`. `pub` keeps External for future multi-crate compatibility; `#[no_mangle]` / `#[used]` keep External so FFI symbols / link-section anchors survive. With the patched karac, `objdump --syms` on this bench's binary shows `middle_pair_off`, `min_i64`, `max_i64` all elided — LLVM inlined them all and dropped the standalone definitions. Cross-kata regression check on the suite is in the [karac commit message](../../../../karac-rust/); the headline: no regressions; kata [#88](../88-merge-sorted-array/) also picked up a 13% speedup from the same change (its `merge` function was hit by the same external-linkage issue).

The lesson worth keeping: **don't pre-bake explanations for perf gaps.** The first three suspects ("bounds checks", "no autovectorization", "branch prediction") were all plausible — and all wrong. The actual cause was visible in five minutes of `objdump --syms` once we looked, but the rhetorical framing on the README would have buried it indefinitely.

### Compile time and binary size

Snapshot — M5 Pro, 2026-05-23, hyperfine `--warmup 1 --runs 10` with `--prepare 'rm -f <artifact>'` so each measurement is cold:

| Compiler | Compile time | Binary size |
|---|---|---|
| `clang -O3 binary_search_partition.c`      | 43.5 ± 1.0 ms | 32.7 KiB |
| **`karac build binary_search_partition.kara`** | **60.8 ± 0.6 ms** | **312.0 KiB** |
| `rustc -O binary_search_partition.rs`      | 87.9 ± 0.6 ms | 455.4 KiB |
| `go build` (Go module)                     | — (excluded; mixes module + std-lib link) | 2434.1 KiB |

Kāra compiles this kata **1.45× faster** than `rustc -O` and produces a binary **~31% smaller than Rust**. The Kāra binary grew from the 2026-05-17 snapshot's 32.9 KiB to today's 312.0 KiB — that's the auto-par runtime worker-pool + reduction infrastructure (`karac_par_reduce`, `karac_reduce_combine_add_i64`, `karac_reduce_worker_0`, plus the thread-pool init) getting linked in once the codegen reduction-recognition pass started selecting it for this source. The runtime contribution is still well below Rust's full stdlib footprint; `clang -O3` is 1.40× faster at compile and 9.5× smaller because C carries no language runtime, just libc.

### Runtime memory (peak)

| Run | Peak RSS |
|---|---|
| `rust binary_search_partition` | 16.4 MiB |
| `c    binary_search_partition` | 16.4 MiB |
| **`kara binary_search_partition` (codegen, auto-par)** | **16.8 MiB** |
| `go   binary_search_partition` | 19.0 MiB |
| `py   binary_search_partition` | 85.7 MiB |

**Parity with Rust and C on memory** (within 0.4 MiB). All three compiled comparators hold two int64 buffers of `M + R = 1_001_000` elements (~8 MiB each, ~16 MiB total), and that dominates the steady state. Kāra's auto-par worker stacks add ~0.4 MiB on top — well-behaved given the ~3× wall-time win. Go's 19.0 MiB carries its GC roots + scheduler arena overhead. Python's 85.7 MiB is the CPython object-per-int representation on a 1M-element list.

### Why Rust / C / Go / Python are in the harness

Same rationale as [`1-two-sum/README.md § Why Rust is in the harness`](../1-two-sum/README.md#why-rust-is-in-the-harness) and the [BENCH.md comparator policy](../../../BENCH.md#comparison-baselines):

- **Rust** is Kāra's semantic peer (compiled, ownership-aware, LLVM-backed). The pre-auto-par snapshot (1.03× of Rust on 2026-05-17) is the cleanest per-core codegen-vs-rustc data point on this kata; today's 3.68×-faster wall-time is the consequence of karac's auto-par discovering a reduction in the kata's `main`, and the comparison is cross-lane.
- **C** is the codegen calibration point — same LLVM backend as Kāra and Rust, no language runtime overhead. C beats Rust here (13.0 ms vs 16.8 ms) by a small margin attributable to its struct-return pair layout vs Rust's tuple return; both are single-thread, and the Kāra-single-thread story sits with them at the 16 ms band per the 2026-05-17 snapshot.
- **Go** is the cross-runtime data point — GC + scheduler + statically-linked runtime, but a thoroughly-tuned native compiler. Standing baseline since 2026-05-21 (BENCH.md update). Go's 29.5 ms here is consistent with its 2× tax over single-thread Kāra/Rust on tight integer loops (per-iter slice-bounds-check, no scalar-replacement-of-aggregates equivalent on the tuple return).
- **Python** is the ergonomic foil. The 2.066 s landing (~450× slower than auto-par Kāra) is the textbook "compiled vs interpreted" cliff this workload hits hard — bytecode dispatch per `if/elif` arm + four conditional indexed reads + min/max calls dominate the algorithm's actual work.
