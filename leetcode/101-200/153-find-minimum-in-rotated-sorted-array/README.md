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

### Why comparing against `hi` works

A rotated sorted array has at most one "drop" — the index where the minimum lives. With the invariant *the minimum is in `[lo, hi]`*, comparing `nums[mid]` against `nums[hi]` partitions cleanly:

- `nums[mid] > nums[hi]` → the drop is strictly right of `mid`, so the minimum is too: `lo := mid + 1`.
- `nums[mid] ≤ nums[hi]` → `mid` and everything to its right is already sorted, so the minimum is at or left of `mid`: `hi := mid`.

Comparing against `hi` (not `lo`) lets the no-rotation case (e.g., `[11, 13, 15, 17]`) terminate cleanly without a special-case first/last guard — every iteration takes the second branch and `hi` shrinks down to 0.

```
lo, hi = 0, n - 1
while lo < hi:
    mid = lo + (hi - lo) / 2
    if nums[mid] > nums[hi]:
        lo = mid + 1
    else:
        hi = mid
return nums[lo]
```

## Kāra features exercised

- **`Slice[i64]` parameter** — function takes an immutable slice; the LeetCode case-driver passes `Array[i64, N]` literals, the bench passes `Vec[i64].as_slice()`.
- **Indexed slice access** — `nums[0]`, `nums[mid]`, `nums[hi]` inside the loops.
- **`for i in 1..n`** (linear) and **`while lo < hi`** (binary) — both loop forms with mutable accumulators.
- **Mutable integer locals updated by guarded `if`** — `m`, `lo`, `hi`.
- **`%` and `/` on `i64`** — bench workload generates the rotated array via `((i + r) % n) + 1`.

No `Map`, no strings, no shared structs.

## API shape

Each solution exposes a pure `find_min(nums) -> i64` (Python: `-> int`) and a thin `report` that prints. `main` calls `report` per test case. Logic is separate from I/O so the function is testable once a harness exists.

## Output format

One integer per line — the minimum for each test case. Kāra and Python output is line-for-line identical so the files can be diffed directly.

```
1
0
11
5
1
```

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

Snapshot — M1, 2026-05-14, hyperfine `--warmup 5 --runs 30 --shell=none`, native binaries via `karac build` and `rustc -O`:

| Workload | Kāra (codegen) | Rust | Gap |
|---|---|---|---|
| `linear_scan` (K=10) | 9.4 ± 0.4 ms | 5.3 ± 1.3 ms | **1.77× of Rust** |
| `binary_search` (K=2M) | 72.1 ± 1.6 ms | 52.9 ± 1.8 ms | **1.36× of Rust** |

The two workloads expose different regimes:

- **`linear_scan` is inner-loop-dominated** — 20 M indexed reads, one compare each. Kāra's gap here is the same shape as 1-two-sum's `brute_force` row: the per-element bounds check blocks LLVM's autovectorizer, so Rust's tighter (or elided-bounds) inner loop wins by ~2×. Closes once bounds-check elision lands (planned P0, path (a) `llvm.assume` reshape; rationale in the [v62 brainstorm archive](../../../../karac-rust/brainstorming/archive/v62_interpreter_perf_and_binary_size.md)).
- **`binary_search` is call-overhead-dominated** — each call is only ~21 iterations, so we measure how cheaply 2 M function dispatches happen, not how the inner compares vectorize. Kāra's gap narrows to **1.36×** here; the residual is per-call setup (slice header materialization, prologue/epilogue) where Kāra's calling convention has slightly more overhead than Rust's. Captured but not P0 v1 — closes after the call-convention pass in the [v62 brainstorm archive](../../../../karac-rust/brainstorming/archive/v62_interpreter_perf_and_binary_size.md) lands (currently P2 deferred).

### Codegen vs Python

| Run | Mean ± σ | Slower than Kāra codegen |
|---|---|---|
| `kara linear_scan` (codegen) | 9.4 ± 0.4 ms | — |
| `rust linear_scan` | 5.3 ± 1.3 ms | — |
| `py linear_scan` | 270.8 ± 2.0 ms | **~29×** |
| `kara binary_search` (codegen) | 72.1 ± 1.6 ms | — |
| `rust binary_search` | 52.9 ± 1.8 ms | — |
| `py binary_search` | 1369 ± 87 ms | **~19×** |

Python is 19–29× slower than Kāra codegen on these workloads. The gap is wider for `linear_scan` because the inner body (one compare, one store) is exactly the regime where CPython bytecode dispatch overhead dominates per-iteration cost.

### Compile time and binary size

Snapshot — M1, 2026-05-14, hyperfine `--warmup 1 --runs 10` with `--prepare 'rm -f <artifact>'` so each measurement is cold:

| Compiler | Compile time | Binary size |
|---|---|---|
| `karac build linear_scan.kara` | 64.4 ± 1.4 ms | 295.8 KiB |
| `rustc -O linear_scan.rs` | 89.4 ± 1.5 ms | 455.7 KiB |
| `karac build binary_search.kara` | 56.2 ± 1.1 ms | 295.8 KiB |
| `rustc -O binary_search.rs` | 76.4 ± 1.3 ms | 455.7 KiB |

Kāra compiles both files **1.36–1.39× faster** than `rustc -O` and produces binaries **~35% smaller**. Further size headroom is locked-P0 for v1 but not yet shipped: `strip -x` + `panic = "abort"` (Phase 1, ~−35% on Map binaries) and `-Wl,-dead_strip` / `--gc-sections` + thin LTO (Phase 2, another 100–300 KB on Linux) — both staged in lines 107–120 of the [v62 brainstorm archive](../../../../karac-rust/brainstorming/archive/v62_interpreter_perf_and_binary_size.md).

### Runtime memory (peak)

| Run | Peak RSS |
|---|---|
| `kara linear_scan` (codegen) | 32.8 MiB |
| `rust linear_scan` | 16.4 MiB |
| `py linear_scan` | 85.4 MiB |
| `kara binary_search` (codegen) | 32.8 MiB |
| `rust binary_search` | 16.4 MiB |
| `py binary_search` | 85.4 MiB |

Same story as 121: Kāra's peak is ~2× Rust's because `Vec[i64].push` doubles capacity on each grow — the final 2M-element Vec is 16 MiB (`i64 × 2M`), and the doubling pass before it allocates an additional 16 MiB transient buffer that sits at peak. Rust's `Vec::with_capacity(N)` short-circuits the doubling. Equivalent capacity-hint support in Kāra (e.g., `Vec.with_capacity(n)`) would close this gap — scoped post-v1 follow-up to the bounds-check elision work in the [v62 brainstorm archive](../../../../karac-rust/brainstorming/archive/v62_interpreter_perf_and_binary_size.md).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why Rust is in the harness`](../../1-100/1-two-sum/README.md#why-rust-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio for v1 is the codegen-vs-Rust gap above. Python is the ergonomic foil.
