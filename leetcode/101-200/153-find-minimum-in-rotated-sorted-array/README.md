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
- **`u64` indices in `binary_search.kara`** — `lo`/`hi`/`mid` carried as `u64` so the backend emits the unsigned mid-compute (`sub + add ..., lsr #1`) instead of the signed-rounding `subs + cinc + add ..., asr #1` shape.

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

Snapshot — M5 Pro, 2026-06-05, hyperfine `--warmup 5 --runs 30 --shell=none`. All mirrors single-threaded (seq-only kata):

| Workload | Kāra (codegen) | Rust | C (clang -O3) | Go | Kāra : Rust |
|---|---|---|---|---|---|
| `linear_scan` (K=10) | 5.2 ± 0.3 ms | 5.6 ± 0.6 ms | 4.7 ± 0.2 ms | 9.7 ± 0.5 ms | **kāra 1.08× faster** |
| `binary_search` (K=2M) | 49.1 ± 0.9 ms | 53.5 ± 0.8 ms | 40.6 ± 0.7 ms | **35.9 ± 1.4 ms** | **kāra 1.09× faster** |

(The 2026-05-19 snapshot read linear 5.0/5.6 and binary 48.0/52.0 for kāra/rust — everything reproduces within ~1σ on byte-identical kāra/rust/C binaries; C and Go rows are benched here for the first time.) Both workloads run at parity-or-faster than `rustc -O`. Against the new comparators: C leads kāra 1.09× on linear and 1.21× on binary (bounds-check-free indexing); Go trails badly on linear (2.06× behind C — per-iteration overhead on the 20 M-read scan) but **wins binary_search outright** (1.13× ahead of even C) — the call-overhead-dominated regime rewards Go's aggressive cross-call inlining of the ~21-iteration search into the K loop. The two shapes:

- **`linear_scan` is inner-loop-dominated** — 20 M indexed reads, one compare each. Closed once karac's TargetMachine started passing the host CPU baseline (apple-m1 on macOS arm64) instead of `generic`/`""`, which is what unlocked LLVM's autovectorizer cost-model to interleave by 4 (matching Rust). See [`karac-rust/docs/implementation_checklist/phase-10-targets.md`](../../../../karac-rust/docs/implementation_checklist/phase-10-targets.md) for the CPU-baseline-per-target table mirroring rustc.
- **`binary_search` is call-overhead-dominated** — each call is only ~21 iterations, so we measure how cheaply 2 M function dispatches happen plus the mid-compute inside. Closing the gap took two changes: source-level `Vec.with_capacity(n)` (eliminated the doubling-realloc transient 2× RSS and ~22% of the fill cost), then type-aware operator dispatch in karac (LLVM was emitting `cinc`-rounded signed mid-compute on the `(hi + lo) / 2` shape because karac codegen unconditionally used signed div/cmp/shr ops; once primitive trait-method dispatch threaded operand signedness through `compile_binop_typed`, switching `lo`/`hi`/`mid` to `u64` made LLVM emit the fused `sub + add ..., lsr #1` mid-point and `b.lo` loop guard — two instructions instead of three in the hot block).

### Codegen vs Python

2026-05-19 readings (the py mirrors are gated off by default; kāra rows updated to 06-05):

| Run | Mean ± σ | Slower than Kāra codegen |
|---|---|---|
| `kara linear_scan` (codegen) | 5.2 ± 0.3 ms | — |
| `py linear_scan` | 271.6 ± 4.1 ms *(05-19)* | **~52×** |
| `kara binary_search` (codegen) | 49.1 ± 0.9 ms | — |
| `py binary_search` | 1329 ± 12 ms *(05-19)* | **~27×** |

Python is ~27–52× slower than Kāra codegen on these workloads. The gap is wider for `linear_scan` because the inner body (one compare, one store) is exactly the regime where CPython bytecode dispatch overhead dominates per-iteration cost.

### Compile time and binary size

Snapshot — M5 Pro, 2026-06-05, hyperfine `--warmup 1 --runs 10` with `--prepare 'rm -f <artifact>'` so each measurement is cold:

| Compiler | Compile time | Binary size |
|---|---|---|
| `karac build linear_scan.kara` | 75.9 ± 1.5 ms | 32.9 KiB |
| `rustc -O linear_scan.rs` | 93.3 ± 2.7 ms | 455.6 KiB |
| `clang -O3 linear_scan.c` | 51.5 ± 1.2 ms | 32.8 KiB |
| `karac build binary_search.kara` | 69.1 ± 1.9 ms | 33.0 KiB |
| `rustc -O binary_search.rs` | 79.9 ± 1.4 ms | 455.7 KiB |
| `clang -O3 binary_search.c` | 45.5 ± 2.1 ms | 32.8 KiB |

Kāra compiles both files **1.16–1.23× faster** than `rustc -O` and produces binaries **~14× smaller** (within ~150 B of clang's) — `strip -x` plus the size-targeted post-link passes have landed since the earlier snapshot, and the `__TEXT,__jittmpl` segment re-scope (karac `e76f42b`, 2026-05-25) reclaimed an additional 16 KiB per Mach-O binary that the original 2026-05-19 snapshot's 49 KiB figures still carried. (The 05-19 snapshot read `karac build` at 62.0 / 55.5 ms against the karac installed at the time; the May-30 karac reinstall plus the 06-05 environment band account for today's 75.9 / 69.1 — both kāra binaries rebuilt **byte-identical**, so codegen output is unchanged. Compile memory, first recorded today: karac 11.0 / 9.5 MiB vs rustc 29.3 / 27.0 and clang 2.6 / 2.5.)

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
