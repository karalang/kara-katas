# 26. Remove Duplicates from Sorted Array

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Array, Two Pointers &nbsp;·&nbsp; **Source:** [leetcode.com/problems/remove-duplicates-from-sorted-array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/)

Given an integer array `nums` sorted in non-decreasing order, remove the duplicates **in-place** so that each unique element appears only once, preserving relative order, and return `k` — the number of unique elements. The first `k` slots of `nums` must hold the unique values; what's past `k` doesn't matter.

**Constraints:** `1 ≤ nums.length ≤ 3 × 10⁴`, `-100 ≤ nums[i] ≤ 100`, `nums` sorted non-decreasing.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| Two pointers (slow write head, fast read head) | O(n) time, O(1) extra space | [`two_pointer.kara`](two_pointer.kara) ✓ | [`two_pointer.py`](two_pointer.py) ✓ |

## Why one compare per element suffices

The invariant: `nums[0..k]` is the deduplicated prefix of everything read so far, so `nums[k − 1]` is the largest value kept. Because the input is sorted, "is `nums[i]` a new value?" reduces to a single compare against that one cell — no lookback past it, no hash set. The read head `i` only ever runs at or ahead of the write head `k`, so no element is overwritten before it is read — the in-place compaction is safe without any buffering. The `len == 0` guard exists for completeness (LeetCode's floor is `len ≥ 1`); with it, `k` starts at 1 because the first element is always kept.

## Kāra features exercised

- **`mut Slice[i64]` parameter** — `remove_duplicates` compacts the caller's buffer in place *and* returns a value (`k`), exercising the mutate-and-return shape.
- **Call-site `mut` marker** — `report(mut a1, 3)` marks the fresh `let mut`; inside `report`, the `remove_duplicates(nums, len)` call forwards an in-scope `mut Slice` without the marker (design.md Feature 4 Part 1½, Rule 2).
- **Mixed `return` and tail expression** — the `len == 0` early `return 0;` plus the bare `k` tail.
- **`for` range with a non-zero start** — `for i in 1..len`.
- **Empty array literal** — `Array[i64, 0] = []` drives the guard path.

## Running

```bash
karac run two_pointer.kara
python3 two_pointer.py
diff <(karac run two_pointer.kara) <(python3 two_pointer.py) && echo OK
```

## Benchmarks

### How to run

```bash
brew install hyperfine    # one-time, also needs rustc (rustup) and karac
./bench/bench.sh
```

`bench/bench.sh` builds the Rust file with `rustc -O`, the C file with `clang -O3`, the Go mirror with `go build`, and the Kāra file with `karac build` (all cached in `bench/target/`, gitignored), then runs runtime, compile-cost (cold, via a `--prepare` delete step), binary-size, and peak-RSS passes.

| File | What it does |
|---|---|
| [`bench/two_pointer.kara`](bench/two_pointer.kara) | N = 2_000_000 sorted input with LCG-random unit gaps (~50% duplicate rate), K = 10 outer iterations, refill + dedup each iter |
| [`bench/two_pointer.py`](bench/two_pointer.py) | Algorithmic mirror — same N, K, LCG |
| [`bench/two_pointer.rs`](bench/two_pointer.rs) | Algorithmic mirror; compiled with `rustc -O` |
| [`bench/two_pointer.c`](bench/two_pointer.c) | Algorithmic mirror, hand-rolled scalar baseline; compiled with `clang -O3` |
| [`bench/go-seq/main.go`](bench/go-seq/main.go) | Algorithmic mirror; compiled with `go build` |

The input is built once: `original[i] = original[i − 1] + bit`, where `bit` comes from the classic glibc LCG (`a = 1103515245, c = 12345, m = 2³¹`, seeded 1) — every implementation steps the identical generator in plain `i64` arithmetic, so all five see byte-identical input. ~50% of elements duplicate their predecessor in an *unpredictable* pattern: a maximally-alternating input (kata [#88](../88-merge-sorted-array/README.md)'s choice) has period 2 and modern predictors lock onto it, whereas LCG-random keep/skip is a genuine ~50% mispredict load on the branch that decides whether to write. Each outer iteration refills `workspace` from the pristine `original` (the dedup mutates in place; without the refill, later iterations would be near-no-ops) — the refill is an elementwise O(N) loop *in every mirror*, counted identically. All mirrors print the same sink (`K × (k + workspace[k−1]) = 10 × (1_000_142 + 1_000_141) = 20_002_830`) so the dedup participates in I/O and can't be elided; bench.sh fails loudly on mismatch.

### Codegen vs Rust (the headline)

Snapshot — M5 Pro, 2026-06-07, hyperfine `--warmup 5 --runs 30 --shell=none`. All four compiled mirrors single-threaded (seq-only kata — the write head `k` is loop-carried: each element's destination depends on every prior keep/skip decision, so there's no auto-par surface):

| Run | Mean ± σ | Gap |
|---|---|---|
| rust two_pointer | 57.8 ± 1.4 ms | 1.07× ahead of kāra |
| c    two_pointer (clang -O3) | 59.6 ± 1.5 ms | 1.04× ahead of kāra |
| **kāra two_pointer (codegen)** | **61.7 ± 1.3 ms** | — |
| go   two_pointer | 65.9 ± 0.9 ms | kāra 1.07× ahead of Go |

All four land within 14% of each other — this workload is mispredict-bound, not compute-bound. With keep/skip a coin flip, the ~50% mispredict rate on the conditional write costs ~10 cycles every other element, and that penalty is identical for every backend; what's left to differentiate on is per-iteration overhead. Kāra's 4 ms gap to C is the bounds-check tax on three data-dependent indexed accesses per element (`nums[i]`, `nums[k−1]`, `nums[k]` — `k` is data-dependent, so no frontend can prove the accesses in-range), and Rust pays the same checks yet edges out C here — conditional-store emission roulette, inside overlapping noise bands. Bounds-check elision (planned P0; rationale in the [v62 brainstorm archive](../../../../kara/brainstorming/archive/v62_interpreter_perf_and_binary_size.md)) targets exactly this shape. Same regime as kata [#88](../88-merge-sorted-array/README.md#codegen-vs-rust-the-headline), with the branch made honest.

### Codegen vs Python

| Run | Mean ± σ |
|---|---|
| `kara two_pointer` (codegen) | 61.7 ± 1.3 ms |
| `rust two_pointer` | 57.8 ± 1.4 ms |
| `py two_pointer` | 917.9 ± 7.9 ms |

Python is **~15× slower** than Kāra codegen — per-iteration CPython bytecode dispatch on a body of one compare, one conditional write, and an increment.

### Compile time and binary size

Snapshot — M5 Pro, 2026-06-07, hyperfine `--warmup 1 --runs 10` with `--prepare 'rm -f <artifact>'` so each measurement is cold:

| Compiler | Compile time | Binary size |
|---|---|---|
| `karac build two_pointer.kara` | 74.7 ± 3.2 ms | 33.0 KiB |
| `rustc -O two_pointer.rs` | 85.6 ± 2.3 ms | 455.4 KiB |
| `clang -O3 two_pointer.c` | 48.0 ± 1.7 ms | 32.8 KiB |
| `go build` | — | 2434.1 KiB |

Kāra compiles this kata **1.15× faster** than `rustc -O` and produces a binary **~93% smaller** than Rust's — and **within 184 bytes of C** (33,752 B vs 33,568 B). Same lean profile as kata [#88](../88-merge-sorted-array/README.md#compile-time-and-binary-size): the workload reaches `Vec.filled` + indexed read/write, `Slice[i64]` indexing, `println(i64)` — and nothing else; cross-archive LTO + DCE elides the rest of the runtime.

### Runtime memory (peak)

| Run | Peak RSS |
|---|---|
| `kara two_pointer` (codegen) | 31.6 MiB |
| `c    two_pointer` | 31.6 MiB |
| `rust two_pointer` | 31.6 MiB |
| `go   two_pointer` | 34.2 MiB |
| `py two_pointer` | 98.7 MiB |

**Parity with C and Rust** — kāra's reading is byte-identical to C (33,128,760 B), Rust 32 KiB above. The working set is two `Vec[i64]`s of 2M elements (16 MiB each: `original` + `workspace`). Go's +2.6 MiB is GC arena + runtime; Python's 98.7 MiB is per-element PyObject boxing. Same story as kata [#88](../88-merge-sorted-array/README.md#runtime-memory-peak).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why Rust is in the harness`](../1-two-sum/README.md#why-rust-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio for v1 is the codegen-vs-Rust gap above. C calibrates the LLVM-backend floor (its margin here is small because the mispredict load dominates the bounds-check tax), Go is the cross-runtime data point, and Python is the ergonomic foil.
