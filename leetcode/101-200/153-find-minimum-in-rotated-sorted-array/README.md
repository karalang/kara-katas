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

`bench/bench.sh` builds the Rust files with `rustc -O` and the Kāra files with `karac build` (both cached in `bench/target/`, gitignored), then measures runtime, cold-compile time, binary size, and peak RSS for all six implementations against the same rotated sorted array (`N = 2_000_000`, pivot `R = N/3`, values in `[1, N]`).

| File | What it does |
|---|---|
| [`bench/linear_scan.kara`](bench/linear_scan.kara) | N=2_000_000, K=10 outer iterations, full O(n) scan per call |
| [`bench/linear_scan.py`](bench/linear_scan.py) | Algorithmic mirror — same N, K, generator |
| [`bench/linear_scan.rs`](bench/linear_scan.rs) | Algorithmic mirror; compiled with `rustc -O` |
| [`bench/binary_search.kara`](bench/binary_search.kara) | N=2_000_000, K=2_000_000 outer iterations (each call is ~21 comparisons, so large K is needed for measurable wall time) |
| [`bench/binary_search.py`](bench/binary_search.py) | Algorithmic mirror — same N, K |
| [`bench/binary_search.rs`](bench/binary_search.rs) | Algorithmic mirror; `black_box(&data)` keeps LLVM from hoisting the pure call out of the K loop |

All six print the same sum-of-results sink per workload (linear: `10`; binary: `2_000_000`) so the algorithm's output participates in I/O and can't be elided.

### Codegen vs Rust (the headline)

Snapshot — M5 Pro, 2026-05-19, hyperfine `--warmup 5 --runs 30 --shell=none`, native binaries via `karac build` and `rustc -O`:

| Workload | Kāra (codegen) | Rust | Gap |
|---|---|---|---|
| `linear_scan` (K=10) | 5.0 ± 0.6 ms | 5.6 ± 0.2 ms | **kāra 1.11× faster** |
| `binary_search` (K=2M) | 48.0 ± 0.6 ms | 52.0 ± 1.2 ms | **kāra 1.08× faster** |

Both workloads now run at parity-or-faster than `rustc -O`. The two have different inner-loop shapes:

- **`linear_scan` is inner-loop-dominated** — 20 M indexed reads, one compare each. Closed once karac's TargetMachine started passing the host CPU baseline (apple-m1 on macOS arm64) instead of `generic`/`""`, which is what unlocked LLVM's autovectorizer cost-model to interleave by 4 (matching Rust). See [`karac-rust/docs/implementation_checklist/phase-10-targets.md`](../../../../karac-rust/docs/implementation_checklist/phase-10-targets.md) for the CPU-baseline-per-target table mirroring rustc.
- **`binary_search` is call-overhead-dominated** — each call is only ~21 iterations, so we measure how cheaply 2 M function dispatches happen plus the mid-compute inside. Closing the gap took two changes: source-level `Vec.with_capacity(n)` (eliminated the doubling-realloc transient 2× RSS and ~22% of the fill cost), then type-aware operator dispatch in karac (LLVM was emitting `cinc`-rounded signed mid-compute on the `(hi + lo) / 2` shape because karac codegen unconditionally used signed div/cmp/shr ops; once primitive trait-method dispatch threaded operand signedness through `compile_binop_typed`, switching `lo`/`hi`/`mid` to `u64` made LLVM emit the fused `sub + add ..., lsr #1` mid-point and `b.lo` loop guard — two instructions instead of three in the hot block).

### Codegen vs Python

| Run | Mean ± σ | Slower than Kāra codegen |
|---|---|---|
| `kara linear_scan` (codegen) | 5.0 ± 0.6 ms | — |
| `rust linear_scan` | 5.6 ± 0.2 ms | — |
| `py linear_scan` | 271.6 ± 4.1 ms | **~54×** |
| `kara binary_search` (codegen) | 48.0 ± 0.6 ms | — |
| `rust binary_search` | 52.0 ± 1.2 ms | — |
| `py binary_search` | 1329 ± 12 ms | **~28×** |

Python is 28–54× slower than Kāra codegen on these workloads. The gap is wider for `linear_scan` because the inner body (one compare, one store) is exactly the regime where CPython bytecode dispatch overhead dominates per-iteration cost.

### Compile time and binary size

Snapshot — M5 Pro, 2026-05-19, hyperfine `--warmup 1 --runs 10` with `--prepare 'rm -f <artifact>'` so each measurement is cold:

| Compiler | Compile time | Binary size |
|---|---|---|
| `karac build linear_scan.kara` | 62.0 ± 1.1 ms | 32.9 KiB |
| `rustc -O linear_scan.rs` | 90.8 ± 0.8 ms | 455.6 KiB |
| `karac build binary_search.kara` | 55.5 ± 1.0 ms | 33.0 KiB |
| `rustc -O binary_search.rs` | 78.3 ± 2.2 ms | 455.7 KiB |

Kāra compiles both files **1.41–1.46× faster** than `rustc -O` and produces binaries **~14× smaller** — `strip -x` plus the size-targeted post-link passes have landed since the earlier snapshot, and the `__TEXT,__jittmpl` segment re-scope (karac `e76f42b`, 2026-05-25) reclaimed an additional 16 KiB per Mach-O binary that the original 2026-05-19 snapshot's 49 KiB figures still carried.

### Runtime memory (peak)

| Run | Peak RSS |
|---|---|
| `kara linear_scan` (codegen) | 16.4 MiB |
| `rust linear_scan` | 16.4 MiB |
| `py linear_scan` | 85.5 MiB |
| `kara binary_search` (codegen) | 16.4 MiB |
| `rust binary_search` | 16.4 MiB |
| `py binary_search` | 85.4 MiB |

Kāra now matches Rust's peak RSS — both bench files use `Vec.with_capacity(n)` to pre-allocate the 2M-element fill, so neither the kāra nor the rust path goes through the doubling-realloc transient that left the old kāra peak at 32.8 MiB.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why Rust is in the harness`](../../1-100/1-two-sum/README.md#why-rust-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio for v1 is the codegen-vs-Rust gap above. Python is the ergonomic foil.
