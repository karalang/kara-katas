# 88. Merge Sorted Array

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Array, Two Pointers, Sorting &nbsp;·&nbsp; **Source:** [leetcode.com/problems/merge-sorted-array](https://leetcode.com/problems/merge-sorted-array/)

You are given two integer arrays `nums1` and `nums2`, sorted in non-decreasing order, and integers `m` and `n` representing the number of valid elements in each. `nums1` has length `m + n` — the first `m` slots are the sorted prefix, the last `n` are scratch. Merge so that `nums1` ends up sorted in non-decreasing order. The merge must be in-place; no value is returned.

**Constraints:** `0 ≤ m, n ≤ 200`, `nums1.length == m + n`, `-10⁹ ≤ nums1[i], nums2[i] ≤ 10⁹`.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| Two pointers from the back | O(m + n) time, O(1) extra space | [`two_pointer.kara`](two_pointer.kara) ✓ | [`two_pointer.py`](two_pointer.py) ✓ |

## Why write from the back

A forward merge would have to shift `nums1`'s prefix out of the way before reading it, costing O((m + n)²) or requiring an O(m + n) auxiliary buffer. Writing from the back side-steps this: the write head `k = m + n − 1` is always at or past both read heads `i` and `j` — every cell is written before it would be read, so no shifting and no aux buffer. The loop runs while `j >= 0` rather than while both heads are valid: once `j` falls below zero, any remaining `nums1[0..=i]` entries are already in place. The opposite exhaustion (when `i` falls below zero with `j` still valid) is handled by the `i >= 0 and …` guard, which forces the else-branch to drain `nums2`.

## Kāra features exercised

- **`mut Slice[i64]` parameter** — `merge` mutates the caller's buffer in place.
- **Call-site `mut` marker** — `report(mut a1, 3, b1, 3)` marks the fresh `let mut`; inside `report`, the `merge` call forwards an in-scope `mut Slice` without the marker (design.md Feature 4 Part 1½, Rule 2).
- **Mixed `mut` and read-only slice params on one function** — `merge` takes one of each.
- **Short-circuit `and`** — the `i >= 0 and nums1[i] > nums2[j]` guard relies on left-to-right evaluation to keep `nums1[i]` from indexing with a negative `i`.
- **Signed `i64` indices that go negative** — all three counters decrement past zero before exit.

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
| [`bench/two_pointer.kara`](bench/two_pointer.kara) | m = n = 1_000_000 maximally-alternating inputs (`prefix_a = [0, 2, …, 2m−2]`, `b = [1, 3, …, 2n−1]`), K = 10 outer iterations, refill + merge each iter |
| [`bench/two_pointer.py`](bench/two_pointer.py) | Algorithmic mirror — same m, n, K, alternation |
| [`bench/two_pointer.rs`](bench/two_pointer.rs) | Algorithmic mirror; compiled with `rustc -O` |
| [`bench/two_pointer.c`](bench/two_pointer.c) | Algorithmic mirror, hand-rolled scalar baseline; compiled with `clang -O3` |
| [`bench/go-seq/main.go`](bench/go-seq/main.go) | Algorithmic mirror; compiled with `go build` |

Each iteration refills the front `m` slots of the workspace from a pre-built sorted prefix, then calls `merge` — the merge mutates in place, so without the refill subsequent iterations would be no-ops; the refill is O(m) and is counted identically in every implementation. All mirrors print the same sum-of-results sink (`K × workspace[total − 1] = 10 × 1_999_999 = 19_999_990`) so the algorithm's output participates in I/O and can't be elided; bench.sh fails loudly on mismatch. The maximally-alternating input forces the inner branch to flip every iteration, which is the worst case for the predictor and stresses the compare + conditional store.

### Codegen vs Rust (the headline)

Snapshot — M5 Pro, 2026-06-05, hyperfine `--warmup 5 --runs 30 --shell=none`. All four compiled mirrors single-threaded (seq-only kata — the in-place merge has loop-carried dependencies on all three cursors, so there's no auto-par surface):

| Run | Mean ± σ | Gap |
|---|---|---|
| c    two_pointer (clang -O3) | 11.1 ± 0.8 ms | 1.49× ahead of kāra |
| **kāra two_pointer (codegen)** | **16.5 ± 2.1 ms** | — |
| rust two_pointer | 16.9 ± 1.5 ms | **kāra 1.02× faster than Rust** |
| go   two_pointer | 21.7 ± 5.2 ms | kāra 1.32× ahead of Go |

(Afternoon re-bench under visible system load — σ widened 3–7× across ALL rows and Go shows a 43.7 ms outlier; the Rust and C binaries are byte-identical to the morning artifacts and still moved +0.5/+0.3 ms, anchoring the shift as environment. The morning 2026-06-05 quiet-system snapshot — kāra 14.5 ± 0.5 / rust 16.4 ± 0.5 / c 10.8 ± 0.4 / go 19.3 ± 0.7, itself reproducing the 2026-05-18 numbers within σ — is the better point estimate; the ranking (c ahead, kāra ahead of Rust, Go last) is stable across both. The kāra binary no longer rebuilds byte-for-byte under the post-`a3acedaf` karac — see § Compile time and binary size. One caveat discovered later the same day: kata [#5](../5-longest-palindromic-substring/README.md)'s re-bench proved the panic-site karac change behind the binary-size jump *also costs runtime* on bounds-check-hot inner loops (1.34× there, A/B'd against the pre-`a3acedaf` karac with a `get_unchecked` control). This kata's merge loop runs ~60–80M bounds checks per invocation, so part of kāra's +2.0 ms afternoon move is plausibly that regression rather than pure environment — the post-fix re-bench will separate the two.)

The inner loop is dominated by an unpredictable branch with two indexed reads and one indexed write — a regime where neither frontend can vectorize (the data dependency on `i`/`j`/`k` is loop-carried) and the gap reduces to per-iteration overhead. The maximally-alternating input is the worst case for the branch predictor, so both frontends are emitting essentially the same compare + conditional store sequence; karac's tight inner-loop emission now matches or slightly exceeds rustc here. C's 1.34× lead is the no-bounds-check floor (raw pointer arithmetic on the same loop); Go lands behind all three on per-iteration overhead. Bounds-check elision (still planned P0; rationale in the [v62 brainstorm archive](../../../../karac-rust/brainstorming/archive/v62_interpreter_perf_and_binary_size.md)) would push the margin further but is no longer the headline story.

### `Vec.filled` vs `Vec.with_capacity` — a measured non-win

The bench builds its three input Vecs with `Vec.filled(len, 0)` + indexed writes, a shape chosen back when Kāra had no capacity-only constructor. `Vec.with_capacity` has since landed (karac `c8fd7c42` + typecheck follow-ups), so the corpus-wide workaround audit (2026-06-05) A/B-measured the natural replacement — `Vec.with_capacity(len)` + `push` for the two computed arrays (`prefix_a`, `b`; `workspace` keeps `filled`, it genuinely needs zeros):

| Init shape | Wall time |
|---|---|
| `Vec.filled` + indexed write (shipped) | 15.1 ± 0.9 ms |
| `Vec.with_capacity` + push | 15.4 ± 0.7 ms |

**No win — the shapes are statistically indistinguishable, so the kata keeps `Vec.filled`.** This is a useful datapoint against the "zero-init pass costs an extra O(N) sweep" intuition: at MiB-scale allocations the OS hands back already-zeroed pages, so `filled`'s zero-init is nearly free and the first indexed-write pass pays the page-touch cost either way, while `push` adds a len-increment + capacity check per element. The trade-off would look different for small, hot, repeatedly-allocated Vecs (where the zero pass is real work) — that's the shape kata [#6](../6-zigzag-conversion/)'s per-call row buffers exercise.

### Codegen vs Python

| Run | Mean ± σ |
|---|---|
| `kara two_pointer` (codegen) | 16.5 ± 2.1 ms |
| `rust two_pointer` | 16.9 ± 1.5 ms |
| `py two_pointer` | 710.0 ± 2.7 ms |

Python is **~43× slower** than Kāra codegen (~48× against the quiet-system kāra estimate) — the per-iteration CPython bytecode dispatch dominates everything else when the body is two compares, two reads, and one write.

### Compile time and binary size

Snapshot — M5 Pro, 2026-06-05, hyperfine `--warmup 1 --runs 10` with `--prepare 'rm -f <artifact>'` so each measurement is cold:

| Compiler | Compile time | Binary size |
|---|---|---|
| `karac build two_pointer.kara` | 75.2 ± 2.1 ms | 49.2 KiB |
| `rustc -O two_pointer.rs` | 88.8 ± 1.3 ms | 455.4 KiB |
| `clang -O3 two_pointer.c` | 47.7 ± 1.2 ms | 32.8 KiB |

Kāra compiles this kata **1.18× faster** than `rustc -O` and produces a binary **~89% smaller** than Rust's. (The 2026-05-18 snapshot read `karac build` at 56.1 ± 0.9 ms against the karac installed at the time; reinstall-day drift bands account for today's 75.2 — rustc and clang held flat on byte-identical inputs.)

**The binary was 33.0 KiB — within 184 bytes of C's — until the 2026-06-05 morning snapshot; it now reads 49.2 KiB.** The +16.2 KiB is the same karac-side regression kata [#6](../6-zigzag-conversion/README.md#binary-size) bisected the same day: karac's phase-9 contract-fault categorization (`8183f6c7`) makes every panic site (bounds checks included) reference `karac_runtime_panic_prefix`, whose thread-local data drags one page-aligned writable `__DATA` segment (16 KiB on Apple Silicon) into every binary — even contract-free ones. Filed karac-side with a fix pointer (fold the static prefix when the program contains no contract, letting the symbol and its page dead-strip); when that lands this kata should return to C parity. The rest of the lean profile is unchanged: the workload reaches `Vec.filled` + indexed read/write, `Slice[i64]` indexing, `println(i64)` — and nothing else; cross-archive LTO + DCE (landed 2026-05-12) elides the rest of the runtime (HTTP, JSON, tokio subgraph, `Map`, `String`, shared structs). Same shape as kata [#4](../4-median-of-two-sorted-arrays/#compile-time-and-binary-size).

### Runtime memory (peak)

| Run | Peak RSS |
|---|---|
| `kara two_pointer` (codegen) | 31.7 MiB |
| `c    two_pointer` | 31.6 MiB |
| `rust two_pointer` | 31.7 MiB |
| `go   two_pointer` | 34.3 MiB |
| `py two_pointer` | 100.9 MiB |

**Parity with C and Rust on memory** — today's single-shot readings put kara byte-identical to Rust (33,194,296 B) with C one 16 KiB page below; earlier samples have paired kara with C instead (the 06-05 morning run) or with Rust (2026-05-18). Page-level jitter aside, all three sit on the same 32 MiB working set: the bench holds three `Vec[i64]`s simultaneously — `prefix_a` (1M × 8B = 8 MiB), `b` (8 MiB), and `workspace` (16 MiB). The May-15 snapshot measured kara at 48.2 MiB against the same `Vec.filled(total, 0)` source; the 16 MiB headroom traced to a karac drop / allocator pathway that has since been fixed, and the current build matches Rust's `vec![0; TOTAL]` allocation profile exactly. Go's +3 MiB is GC arena + runtime; Python's 100.9 MiB is per-element PyObject boxing. Same story as kata [#4](../4-median-of-two-sorted-arrays/#runtime-memory-peak) and kata [#121](../121-best-time-to-buy-and-sell-stock/#runtime-memory-peak).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why Rust is in the harness`](../1-two-sum/README.md#why-rust-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio for v1 is the codegen-vs-Rust gap above. C calibrates the LLVM-backend floor (its 1.34× lead here is the no-bounds-check raw-pointer loop), Go is the cross-runtime data point (1.33× behind kāra), and Python is the ergonomic foil.
