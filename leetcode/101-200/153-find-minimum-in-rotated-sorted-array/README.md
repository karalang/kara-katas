# 153. Find Minimum in Rotated Sorted Array

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array, Binary Search &nbsp;·&nbsp; **Source:** [leetcode.com/problems/find-minimum-in-rotated-sorted-array](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/)

Given an array of unique integers that was originally sorted in ascending order and then rotated between `1` and `n` times, return the minimum element. Required to run in `O(log n)`.

**Constraints:** `1 ≤ nums.length ≤ 5000`, `-5000 ≤ nums[i] ≤ 5000`, all values unique, input is a rotation of a sorted array.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| Linear scan: walk once, track running min | O(n) time, O(1) space | [`linear_scan.kara`](linear_scan.kara) ✓ via `karac run` | [`linear_scan.py`](linear_scan.py) ✓ |
| Binary search: compare `nums[mid]` to `nums[hi]` | O(log n) time, O(1) space | [`binary_search.kara`](binary_search.kara) ✓ via `karac run` | [`binary_search.py`](binary_search.py) ✓ |

`✓` runs end-to-end today. Binary search is the canonical solution — linear scan is a baseline to compare codegen against.

The header comment in [`binary_search.kara`](binary_search.kara) covers why comparing `nums[mid]` against `nums[hi]` (rather than `nums[lo]`) lets the no-rotation case terminate without a special-case first/last guard.

## Kāra features exercised

- **`Slice[i64]` parameter** — function takes an immutable slice; LeetCode case-driver passes `Array[i64, N]` literals, bench passes `Vec[i64].as_slice()`.
- **Indexed slice access** — `nums[0]`, `nums[mid]`, `nums[hi]` inside the loops.
- **`for i in 1..n`** (linear) and **`while lo < hi`** (binary) — both loop forms with mutable accumulators.
- **`%` and `/` on `i64`** — bench workload generates the rotated array via `((i + r) % n) + 1`.
- **`u64` indices in `binary_search.kara`** — `lo`/`hi`/`mid` carried as `u64` so the backend emits the unsigned mid-compute (`sub + add ..., lsr #1`) instead of the signed-rounding `subs + cinc + add ..., asr #1` shape. Re-verified 2026-06-06 on current karac (A/B asm of this source vs an `i64` rewrite): the gap is still real — the plain-`i64` form still pays the 3-instruction `cinc + asr` mid-compute and a signed `b.lt` guard, so the `u64` carry stays load-bearing, not stylistic. The karac-side fix (make the naturally-written `i64` form emit the unsigned shape, e.g. via `len()` non-negativity range info) is tracked in kara `docs/implementation_checklist/phase-7-codegen.md` § "Signed-index mid-compute parity", which names this bench source as its natural-pull trigger; when it lands, the `u64` carry and this bullet both go (re-bench ceremony applies).

## Running

```bash
# Kāra
karac run linear_scan.kara
karac run binary_search.kara

# Python
python3 linear_scan.py
python3 binary_search.py
```

## Benchmarks

### How to run

```bash
brew install hyperfine    # one-time, also needs rustc (rustup) and karac
./bench/bench.sh
```

`bench/bench.sh` builds the Rust files with `rustc -O`, the C files with `clang -O3`, the Go mirrors with `go build`, and the Kāra files with `karac build` (all cached in `bench/target/`, gitignored), then measures runtime, cold-compile time, binary size, and peak RSS for both approaches against the same rotated sorted array (`N = 2_000_000`, pivot `R = N/3`, values in `[1, N]`).

| File | What it does |
|---|---|
| [`bench/linear_scan.kara`](bench/linear_scan.kara) | N=2_000_000, K=10 outer iterations, full O(n) scan per call |
| [`bench/linear_scan.py`](bench/linear_scan.py) | Algorithmic mirror — same N, K, generator (gated behind `KARA_BENCH_INCLUDE_PY=1`) |
| [`bench/linear_scan.rs`](bench/linear_scan.rs) | Algorithmic mirror; compiled with `rustc -O` |
| [`bench/linear_scan.c`](bench/linear_scan.c) / [`bench/go-seq/`](bench/go-seq/) | Algorithmic mirrors; `clang -O3` / `go build` |
| [`bench/binary_search.kara`](bench/binary_search.kara) | N=2_000_000, K=2_000_000 outer iterations (each call is ~21 comparisons, so large K is needed for measurable wall time) |
| [`bench/binary_search.py`](bench/binary_search.py) | Algorithmic mirror — same N, K (same `KARA_BENCH_INCLUDE_PY` gate) |
| [`bench/binary_search.rs`](bench/binary_search.rs) | Algorithmic mirror; `black_box(&data)` keeps LLVM from hoisting the pure call out of the K loop |
| [`bench/binary_search.c`](bench/binary_search.c) / [`bench/go-seq/`](bench/go-seq/) | Algorithmic mirrors; `clang -O3` / `go build` |

All compiled mirrors print the same sum-of-results sink per workload (linear: `10`; binary: `2_000_000`) so the algorithm's output participates in I/O and can't be elided; bench.sh fails loudly on mismatch.

### Codegen vs Rust (the headline)

Snapshot — M5 Pro, 2026-06-17, hyperfine `--warmup 5 --runs 30 --shell=none`. Seq lane (both workloads single-threaded):

| Workload | Kāra (codegen) | Rust | C (clang -O3) | Go | Kāra : Rust |
|---|---|---|---|---|---|
| `linear_scan` (K=10) | 5.1 ± 0.2 ms | 5.6 ± 1.5 ms | 4.8 ± 0.1 ms | 9.7 ± 1.5 ms | **kāra 1.10× faster** |
| `binary_search` (K=2M) | 39.1 ± 1.2 ms | 51.4 ± 1.0 ms | 38.8 ± 0.4 ms | 35.0 ± 1.6 ms | **kāra 1.31× faster** |

**The binary-search midpoint BCE fix landed kāra at C parity here.** Before [`B-2026-06-16-1`](../../../../kara/docs/bug-ledger.md), `binary_search` ran **66.1 ms — 1.76× behind C** (and behind Rust), because the per-iteration `nums[mid]` bounds check survived `-O2`: folding `mid < len` needs the *relational* invariant `mid < hi`, which LLVM's interval-based CVP can't derive, and kāra's `mid = extractvalue(sadd.with.overflow …)` is opaque to its range pass. Teaching karac to emit `assume(lo <= mid < hi)` at the midpoint binding (surfaced and fixed via [#34](../../1-100/34-find-first-and-last-position/)) folds the check, dropping `binary_search` to **39.1 ms — dead even with C (38.8 ms) and 1.31× ahead of Rust**; Go's 35.0 ms keeps a 1.12× edge (its aggressive cross-call inlining of the ~21-iteration search into the K loop still wins the call-overhead-dominated regime). `linear_scan` holds at 1.10× ahead of Rust / 1.07× behind C. The two shapes:

- **`linear_scan` is inner-loop-dominated** — 20 M indexed reads, one compare each. Closed once karac's TargetMachine started passing the host CPU baseline (apple-m1 on macOS arm64) instead of `generic`/`""`, which is what unlocked LLVM's autovectorizer cost-model to interleave by 4 (matching Rust). See [`karac-rust/docs/implementation_checklist/phase-10-targets.md`](../../../../karac-rust/docs/implementation_checklist/phase-10-targets.md) for the CPU-baseline-per-target table mirroring rustc.
- **`binary_search` is call-overhead-dominated** — each call is only ~21 iterations, so we measure how cheaply 2 M function dispatches happen plus the mid-compute and indexing inside. Three karac changes closed the gap, in order: source-level `Vec.with_capacity(n)` (eliminated the doubling-realloc transient 2× RSS and ~22% of the fill cost); type-aware operator dispatch (`u64` `lo`/`hi`/`mid` made LLVM emit the fused `sub + add ..., lsr #1` mid-point and `b.lo` guard — two instructions instead of the signed `cinc + asr` three); and finally the **midpoint bounds-check elision** ([`B-2026-06-16-1`](../../../../kara/docs/bug-ledger.md)), which removed the surviving per-iteration `nums[mid]` check and is what brought the seq lane from 1.76× behind C to parity.

### Codegen vs Python

2026-05-19 readings (the py mirrors are gated off by default; kāra rows updated to 06-05):

| Run | Mean ± σ | Slower than Kāra codegen |
|---|---|---|
| `kara linear_scan` (codegen) | 5.1 ± 0.2 ms | — |
| `py linear_scan` | 271.6 ± 4.1 ms *(05-19)* | **~53×** |
| `kara binary_search` (codegen) | 39.1 ± 1.2 ms | — |
| `py binary_search` | 1329 ± 12 ms *(05-19)* | **~34×** |

Python is ~34–53× slower than Kāra codegen on these workloads. The gap is wider for `linear_scan` because the inner body (one compare, one store) is exactly the regime where CPython bytecode dispatch overhead dominates per-iteration cost.

### Compile time and binary size

Snapshot — M5 Pro, 2026-06-17, hyperfine `--warmup 1 --runs 10` with `--prepare 'rm -f <artifact>'` so each measurement is cold:

| Compiler | Compile time | Binary size |
|---|---|---|
| `karac build linear_scan.kara` | 80.2 ± 0.9 ms | 33.3 KiB |
| `rustc -O linear_scan.rs` | 105.3 ± 1.9 ms | 455.6 KiB |
| `clang -O3 linear_scan.c` | 53.2 ± 1.4 ms | 32.8 KiB |
| `karac build binary_search.kara` | 76.5 ± 1.4 ms | 33.3 KiB |
| `rustc -O binary_search.rs` | 94.4 ± 1.6 ms | 455.7 KiB |
| `clang -O3 binary_search.c` | 47.5 ± 0.7 ms | 32.8 KiB |

Kāra compiles both files **1.23–1.31× faster** than `rustc -O` and produces binaries **~14× smaller** (within ~150 B of clang's). The `linear_scan` binary rebuilds byte-identical to the 06-05 snapshot, but `binary_search`'s codegen **changed** with the midpoint bounds-check elision fix ([`B-2026-06-16-1`](../../../../kara/docs/bug-ledger.md)) — it now emits the `assume(lo <= mid < hi)` facts and folds the loop's `nums[mid]` check, which is the runtime win above; the gated extra `default<O1>` pass that completes the fold is invisible in the cold-compile number (76.5 ms, still 1.23× under `rustc -O`). Compile memory: karac 13.3 / 13.1 MiB vs rustc 29.3 / 27.1 and clang 2.5 / 2.6.

### Runtime memory (peak)

| Run | Peak RSS |
|---|---|
| `kara linear_scan` (codegen) | 16.3 MiB |
| `rust linear_scan` | 16.3 MiB |
| `c    linear_scan` | 16.3 MiB |
| `go   linear_scan` | 18.9 MiB |
| `py linear_scan` | 85.5 MiB *(05-19)* |
| `kara binary_search` (codegen) | 16.3 MiB |
| `rust binary_search` | 16.3 MiB |
| `c    binary_search` | 16.3 MiB |
| `go   binary_search` | 18.9 MiB |
| `py binary_search` | 85.4 MiB *(05-19)* |

Kāra matches Rust's and C's peak RSS within a page (single-shot readings on the shared 16 MiB `Vec[i64]` working set; Go's +2.6 MiB is its GC arena + runtime) — both bench files use `Vec.with_capacity(n)` to pre-allocate the 2M-element fill, so neither the kāra nor the rust path goes through the doubling-realloc transient that left the old kāra peak at 32.8 MiB.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why Rust is in the harness`](../../1-100/1-two-sum/README.md#why-rust-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio for v1 is the codegen-vs-Rust gap above. C calibrates the LLVM-backend floor; Go is the cross-runtime data point — and on `binary_search` it's a useful upset (fastest of the four via cross-call inlining), a reminder that the per-workload winner depends on which overhead regime dominates. Python is the ergonomic foil.
