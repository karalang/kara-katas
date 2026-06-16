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

Snapshot — M5 Pro, 2026-06-07, hyperfine `--warmup 5 --runs 30 --shell=none`. All four compiled mirrors single-threaded (seq-only kata — the write head `k` is loop-carried: each element's destination depends on every prior keep/skip decision, so there's no auto-par surface):

| Run | Mean ± σ | Gap |
|---|---|---|
| rust two_pointer | 53.0 ± 0.7 ms | 1.06× ahead of kāra |
| **kāra two_pointer (codegen)** | **56.4 ± 0.6 ms** | — |
| c    two_pointer (clang -O3) | 55.0 ± 0.5 ms | 1.03× ahead of kāra |
| go   two_pointer | 66.1 ± 0.7 ms | kāra 1.17× ahead of Go |

**Kāra trails C by ~3%** (1.03×) and Rust by ~6% on a mispredict-bound compaction — and this is *with* integer-overflow trapping on by default (design.md § Arithmetic Overflow), which Rust's release build omits. The per-element body is one compare, one conditional store, and `k += 1`; the increment's overflow check folds (loop-bounded), so there is no trapping-arithmetic cost in the hot loop — the only `with.overflow` checks land in the once-per-outer-iteration sink accumulation. Same regime as sibling kata [#26](../26-remove-duplicates-from-sorted-array/README.md#codegen-vs-rust-the-headline).

**Bounds-check status.** The monotone-variable BCE pass (karac `ef5a02a6`) proves `k ≥ 0` from its zero init + monotone `k += 1` and emits `llvm.assume(k >= k_entry)`, folding the negative-index half of the `nums[k]` write check and the `nums[i]` read check (trip-count-bounded). The **upper** half of `nums[k]` survives — it needs the relational invariant `k ≤ i`, which is the still-open relational tier of the BCE work (tracked in karac `phase-7-codegen.md` § "transitive bounds from induction-variable monotonicity"). This is exactly the residual shape sibling kata #26 documents; closing the relational tier would fold the last check here too.

### Codegen vs Python

| Run | Mean ± σ |
|---|---|
| `kara two_pointer` (codegen) | 56.4 ± 0.6 ms |
| `rust two_pointer` | 53.0 ± 0.7 ms |
| `py two_pointer` | 882.8 ± 6.7 ms |

Python is **~16× slower** than Kāra codegen — per-iteration CPython bytecode dispatch on a body of one compare, one conditional store, and an increment.

### Compile time and binary size

Snapshot — M5 Pro, 2026-06-07, hyperfine `--warmup 1 --runs 10` with `--prepare 'rm -f <artifact>'` so each measurement is cold:

| Compiler | Compile time | Binary size |
|---|---|---|
| `karac build two_pointer.kara` | 74.1 ± 0.5 ms | 33.3 KiB |
| `rustc -O two_pointer.rs` | 98.8 ± 2.3 ms | 455.4 KiB |
| `clang -O3 two_pointer.c` | 48.0 ± 0.3 ms | 32.8 KiB |
| `go build` | — | 2434.1 KiB |

Kāra compiles this kata **1.33× faster** than `rustc -O` and produces a binary **~93% smaller** than Rust's — **within ~0.5 KiB of C** (33.3 vs 32.8 KiB; the delta is the overflow-trap landing pads). Same lean profile as kata [#26](../26-remove-duplicates-from-sorted-array/README.md#compile-time-and-binary-size): the workload reaches `Vec.filled` + indexed read/write, `Slice[i64]` indexing, `println(i64)` — and nothing else; cross-archive LTO + DCE elides the rest of the runtime.

### Runtime memory (peak)

| Run | Peak RSS |
|---|---|
| `kara two_pointer` (codegen) | 31.6 MiB |
| `c    two_pointer` | 31.6 MiB |
| `rust two_pointer` | 31.6 MiB |
| `go   two_pointer` | 34.5 MiB |
| `py two_pointer` | 68.1 MiB |

**Parity with C and Rust** — the working set is two `Vec[i64]`s of 2M elements (16 MiB each: `original` + `workspace`). Go's +2.9 MiB is GC arena + runtime; Python's 68.1 MiB is per-element PyObject boxing. Same story as kata [#26](../26-remove-duplicates-from-sorted-array/README.md#runtime-memory-peak).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why Rust is in the harness`](../1-two-sum/README.md#why-rust-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio for v1 is the codegen-vs-Rust gap above. C calibrates the LLVM-backend floor (kāra trails it by ~3% here), Go is the cross-runtime data point, and Python is the ergonomic foil.
