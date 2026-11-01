# 27. Remove Element

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Array, Two Pointers &nbsp;·&nbsp; **Source:** [leetcode.com/problems/remove-element](https://leetcode.com/problems/remove-element/)

Given an integer array `nums` and an integer `val`, remove **all occurrences** of `val` in-place and return `k` — the number of elements that are not `val`. The first `k` slots of `nums` must hold the kept values (any order is accepted; the two-pointer below preserves the original order); what's past `k` doesn't matter.

**Constraints:** `0 ≤ nums.length ≤ 100`, `0 ≤ nums[i] ≤ 50`, `0 ≤ val ≤ 100`.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| Two pointers (slow write head, fast read head) | O(n) time, O(1) extra space | [`two_pointer.kara`](two_pointer.kara) ✓ | [`two_pointer.py`](two_pointer.py) ✓ |

## Why a scalar compare suffices

The invariant: `nums[0..k]` is the compaction of every kept element read so far. The keep test is a single compare of `nums[i]` against the scalar `val` — there is no `nums[k − 1]` lookback and **no sorted-input requirement**, which is the one structural difference from sibling kata [#26 (remove duplicates from sorted array)](../26-remove-duplicates-from-sorted-array/README.md): #26 dedups by comparing each element to the last kept one, #27 filters by comparing each to a fixed value. The read head `i` runs at or ahead of the write head `k`, so no element is overwritten before it is read — the in-place compaction is safe without buffering, and `k` starts at 0 because nothing is kept until the first non-`val` element is seen.

## Kāra features exercised

- **`mut Slice[i64]` parameter that also returns a value** — `remove_element` compacts the caller's buffer in place *and* returns `k`, the mutate-and-return shape.
- **Mixed slice + scalar params** — `remove_element(nums: mut Slice[i64], len: i64, val: i64)` threads the filter value alongside the mutable buffer.
- **Call-site `mut` marker** — `report(mut a1, 4, 3)` marks the fresh `let mut`; inside `report`, the `remove_element(nums, len, val)` call forwards an in-scope `mut Slice` without the marker (design.md Feature 4 Part 1½, Rule 2).
- **`for` range from zero** — `for i in 0..len`, the bare-start shape.
- **Empty array literal** — `Array[i64, 0] = []` drives the never-loops path.

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
| [`bench/two_pointer.kara`](bench/two_pointer.kara) | N = 2_000_000, ~50% of elements equal `val` (= 0, removed) in an unpredictable LCG pattern, the rest a distinct kept value; K = 10 outer iterations, refill + compact each iter |
| [`bench/two_pointer.py`](bench/two_pointer.py) | Algorithmic mirror — same N, K, LCG |
| [`bench/two_pointer.rs`](bench/two_pointer.rs) | Algorithmic mirror; compiled with `rustc -O` |
| [`bench/two_pointer.c`](bench/two_pointer.c) | Algorithmic mirror, hand-rolled scalar baseline; compiled with `clang -O3` |
| [`bench/go-seq/main.go`](bench/go-seq/main.go) | Algorithmic mirror; compiled with `go build` |

The input is built once: each element is set to `val` (removed) or a distinct kept value `i + 1`, chosen by the classic glibc LCG (`a = 1103515245, c = 12345, m = 2³¹`, seeded 1) — every implementation steps the identical generator in plain `i64` arithmetic, so all five see byte-identical input. ~50% of elements equal `val` in an *unpredictable* pattern (a period-2 alternation would be trivially predicted), so the keep/skip branch is a genuine ~50% mispredict load. Each outer iteration refills `workspace` from the pristine `original` (the compaction mutates in place; without the refill, later iterations would be near-no-ops) — the refill is an elementwise O(N) loop *in every mirror*, counted identically. All mirrors print the same sink (`K × (k + workspace[k−1])`) so the compaction participates in I/O and can't be elided; bench.sh fails loudly on mismatch.

### Codegen vs Rust (the headline)

M5 Pro, 2026-10-31 (`results.json` `measured_at` 2026-11-01T01:46Z), karac 0.9.0-dev.14057+g6697158fa (v2/MIR backend), hyperfine `--warmup 5 --runs 30 --shell=none`. All four compiled mirrors single-threaded (seq-only kata — the write head `k` is loop-carried: each element's destination depends on every prior keep/skip decision, so there's no auto-par surface):

| Run | Mean ± σ | Gap |
|---|---|---|
| **kāra two_pointer (codegen)** | **53.8 ± 1.3 ms** | — |
| rust two_pointer (`overflow-checks=on`) | 60.4 ± 1.2 ms | kāra 1.12× ahead |
| rust two_pointer (`-O`, wrapping) | 61.1 ± 0.7 ms | kāra 1.14× ahead |
| c    two_pointer (clang -O3) | 62.7 ± 0.6 ms | kāra 1.17× ahead |
| go   two_pointer | 73.6 ± 1.9 ms | kāra 1.37× ahead |

**Kāra leads the field** on a mispredict-bound compaction: ahead of Rust by 1.14× (1.12× against the overflow-checked build), of C by 1.17×, and of Go by 1.37× — and this is *with* integer-overflow trapping on by default (design.md § Arithmetic Overflow), which Rust's release build omits. On the 2026-07-28 legacy feed Kāra trailed both (Kāra/Rust 1.06×, Kāra/C 1.02×); on the v2/MIR backend those ratios are 0.88× and 0.86×. The cause of the gain has not been attributed. (Every comparator also ran 13–17% slower in absolute ms this session, so compare ratios, not milliseconds.) The per-element body is one compare, one conditional store, and `k += 1`; the increment's overflow check folds (loop-bounded), so there is no trapping-arithmetic cost in the hot loop — the only `with.overflow` checks land in the once-per-outer-iteration sink accumulation. Same regime as sibling kata [#26](../26-remove-duplicates-from-sorted-array/README.md#codegen-vs-rust-the-headline).

**Bounds-check status.** The monotone-variable BCE pass (karac `ef5a02a6`) proves `k ≥ 0` from its zero init + monotone `k += 1` and emits `llvm.assume(k >= k_entry)`, folding the negative-index half of the `nums[k]` write check and the `nums[i]` read check (trip-count-bounded). The **upper** half of `nums[k]` survives — it needs the relational invariant `k ≤ i`, which is the still-open relational tier of the BCE work (tracked in karac `phase-7-codegen.md` § "transitive bounds from induction-variable monotonicity"). This is exactly the residual shape sibling kata #26 documents; closing the relational tier would fold the last check here too.

### Codegen vs Python

| Run | Mean ± σ |
|---|---|
| `kara two_pointer` (codegen) | 53.8 ± 1.3 ms |
| `rust two_pointer` | 61.1 ± 0.7 ms |
| `py two_pointer` — last measured 2026-06-07, not re-run | 882.8 ± 6.7 ms |

Python is not in the 2026-10-31 feed (the run did not set `KARA_BENCH_INCLUDE_PY`); the ratio here is from the 2026-06-07 snapshot, when Python was **~16× slower** than Kāra codegen — per-iteration CPython bytecode dispatch on a body of one compare, one conditional store, and an increment.

### Compile time and binary size

M5 Pro, 2026-10-31, karac g6697158fa (v2/MIR backend), hyperfine `--warmup 1 --runs 10` with `--prepare 'rm -f <artifact>'` so each measurement is cold:

| Compiler | Compile time | Binary size |
|---|---|---|
| `karac build two_pointer.kara` | 114.5 ± 2.5 ms | 295.8 KiB |
| `rustc -O two_pointer.rs` | 90.9 ± 1.0 ms | 455.4 KiB |
| `clang -O3 two_pointer.c` | 48.9 ± 1.0 ms | 32.8 KiB |
| `go build` | — | 2434.1 KiB |

On the v2/MIR backend Kāra compiles this kata **1.26× slower** than `rustc -O` (2.34× clang) and produces a binary at 65% of Rust's. Every v2/MIR Kāra binary is ~300–390 KB where the legacy backend's were ~34 KB, tracked as [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md). The rest of this paragraph is the legacy backend's history: on the 2026-06-07 snapshot Kāra compiled **1.33× faster** than `rustc -O` (74.1 vs 98.8 ms) and produced a binary **~93% smaller** than Rust's — **within ~0.5 KiB of C** (33.3 vs 32.8 KiB; the delta was the overflow-trap landing pads). Same lean profile as kata [#26](../26-remove-duplicates-from-sorted-array/README.md#compile-time-and-binary-size): the workload reaches `Vec.filled` + indexed read/write, `Slice[i64]` indexing, `println(i64)` — and nothing else; cross-archive LTO + DCE elides the rest of the runtime.

### Runtime memory (peak)

| Run | Peak RSS |
|---|---|
| `kara two_pointer` (codegen) | 31.6 MiB |
| `c    two_pointer` | 31.6 MiB |
| `rust two_pointer` | 31.6 MiB |
| `go   two_pointer` | 34.3 MiB |
| `py two_pointer` — last measured 2026-06-07, not re-run | 68.1 MiB |

**Parity with C and Rust** — kāra reads 33,161,576 B against Rust's 33,161,552 B and C's 33,128,784 B. The working set is two `Vec[i64]`s of 2M elements (16 MiB each: `original` + `workspace`). Go's +2.7 MiB is GC arena + runtime; Python's 68.1 MiB is per-element PyObject boxing. Same story as kata [#26](../26-remove-duplicates-from-sorted-array/README.md#runtime-memory-peak).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why Rust is in the harness`](../1-two-sum/README.md#why-rust-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio for v1 is the codegen-vs-Rust gap above. C calibrates the LLVM-backend floor (kāra leads it by 1.17× on the 2026-10-31 feed; it trailed by ~3% on the legacy backend), Go is the cross-runtime data point, and Python is the ergonomic foil.
