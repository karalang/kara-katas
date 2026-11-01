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

M5 Pro, 2026-11-01, karac g6697158fa (0.9.0-dev.14057, the v2/MIR backend), hyperfine `--warmup 5 --runs 30 --shell=none`. All compiled mirrors single-threaded (seq-only kata — the in-place merge has loop-carried dependencies on all three cursors, so there's no auto-par surface; the default build emits no call of `karac_mir_task_spawn`, verified in the emitted IR (`KARAC_MIR_LL`)):

| Run | Mean ± σ | Gap |
|---|---|---|
| c    two_pointer (clang -O3) | 11.0 ± 0.4 ms | 1.60× ahead of kāra |
| **kāra two_pointer (codegen)** | **17.7 ± 1.1 ms** | — |
| rust two_pointer | 17.8 ± 1.1 ms | kāra 1.00× Rust (tie) |
| rust two_pointer (overflow-checks=on, equal-safety) | 17.8 ± 1.2 ms | kāra 1.01× ahead (tie) |
| go   two_pointer | 19.1 ± 0.7 ms | kāra 1.08× ahead of Go |

On the MIR backend kāra **ties both Rust builds** where the July legacy build led them: against the previous feed (2026-07-28) Kāra/Rust went 0.81× → 1.00×, Kāra/C 1.27× → 1.60×, Kāra/Go 0.64× → 0.93×. The gap is in the exact counts, not noise on a short workload: the MIR build retires 1.38× legacy's instructions (0.397 G vs 0.287 G) at 1.23× its cycles, filed as [`B-2026-11-01-19`](../../../../kara/docs/bugs-v2.md).

(History — the earlier evening 2026-06-05 snapshot, quiet system, post-karac-`3f3b34a9`. The afternoon re-bench had read kāra at 16.5 ± 2.1 under visible load and was caveated when kata [#5](../5-longest-palindromic-substring/README.md) proved the same-day panic-site karac change cost *runtime* on bounds-check-hot loops — this kata's merge loop runs ~60–80M bounds checks per invocation. The post-fix re-bench separates the two as promised: with rust/c binaries byte-identical across all three runs, kāra snapped from 16.5 back to **14.6 ± 0.5** — reproducing the morning quiet-system 14.5 ± 0.5 — so roughly +1.4 ms of the afternoon move was the regression (kata #5's mechanism: panic-site printf operand growth pushing hot helpers past the inline threshold) and the remainder load. Ranking (c ahead, kāra ahead of Rust, Go last) was stable throughout.)

The inner loop is dominated by an unpredictable branch with two indexed reads and one indexed write — a regime where neither frontend can vectorize (the data dependency on `i`/`j`/`k` is loop-carried) and the gap reduces to per-iteration overhead. The maximally-alternating input is the worst case for the branch predictor, so both frontends are emitting essentially the same compare + conditional store sequence; karac's inner-loop emission matches rustc's wall time here (it exceeded it on the legacy backend; see above). C's 1.60× lead is the no-bounds-check floor (raw pointer arithmetic on the same loop); Go lands behind all three on per-iteration overhead. Induction-variable bounds-check elision (tracked: [karac phase-7 § transitive bounds from induction-variable monotonicity](../../../../kara/docs/implementation_checklist/phase-7-codegen.md) — this kata's `nums1[k]` is one of its two natural-pull triggers; rationale in the [v62 brainstorm archive](../../../../kara/brainstorming/archive/v62_interpreter_perf_and_binary_size.md)) would push the margin further but is no longer the headline story.

### `Vec.filled` vs `Vec.with_capacity` — a measured non-win

The bench builds its three input Vecs with `Vec.filled(len, 0)` + indexed writes, a shape chosen back when Kāra had no capacity-only constructor. `Vec.with_capacity` has since landed (karac `c8fd7c42` + typecheck follow-ups), so the corpus-wide workaround audit (2026-06-05) A/B-measured the natural replacement — `Vec.with_capacity(len)` + `push` for the two computed arrays (`prefix_a`, `b`; `workspace` keeps `filled`, it genuinely needs zeros):

| Init shape | Wall time |
|---|---|
| `Vec.filled` + indexed write (shipped) | 15.1 ± 0.9 ms |
| `Vec.with_capacity` + push | 15.4 ± 0.7 ms |

**No win — the shapes are statistically indistinguishable, so the kata keeps `Vec.filled`.** This is a useful datapoint against the "zero-init pass costs an extra O(N) sweep" intuition: at MiB-scale allocations the OS hands back already-zeroed pages, so `filled`'s zero-init is nearly free and the first indexed-write pass pays the page-touch cost either way, while `push` adds a len-increment + capacity check per element. The trade-off would look different for small, hot, repeatedly-allocated Vecs (where the zero pass is real work) — that's the shape kata [#6](../6-zigzag-conversion/)'s per-call row buffers exercise.

### Codegen vs Python

Last measured 2026-06-05, not re-run (the 2026-11-01 re-bench did not set `KARA_BENCH_INCLUDE_PY`); all three rows are from that Python session:

| Run | Mean ± σ |
|---|---|
| `kara two_pointer` (codegen) | 12.7 ± 0.3 ms |
| `rust two_pointer` | 15.2 ± 0.4 ms |
| `py two_pointer` | 686.8 ± 2.6 ms |

Python is **~54× slower** than Kāra codegen — the per-iteration CPython bytecode dispatch dominates everything else when the body is two compares, two reads, and one write.

### Compile time and binary size

M5 Pro, 2026-11-01, karac g6697158fa, hyperfine `--warmup 1 --runs 10` with `--prepare 'rm -f <artifact>'` so each measurement is cold:

| Compiler | Compile time | Binary size |
|---|---|---|
| `karac build two_pointer.kara` | 116.0 ± 2.4 ms | 295.8 KiB |
| `rustc -O two_pointer.rs` | 96.8 ± 0.9 ms | 455.4 KiB |
| `clang -O3 two_pointer.c` | 49.6 ± 1.2 ms | 32.8 KiB |

Kāra compiles this kata **1.20× slower** than `rustc -O` (2.34× clang) and produces a binary **~35% smaller** than Rust's. Every MIR Kāra binary is ~300–390 KB where legacy's were ~34 KB, tracked as [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md). (The 2026-05-18 snapshot read `karac build` at 56.1 ± 0.9 ms and the 2026-06-05 one at 72.1 ± 2.0 ms, on the legacy backend.)

The paragraph below is the legacy backend's binary-size history (2026-06-05); as of 2026-11-01 the MIR binary is 302,920 B against C's 33,568 B, so its C-parity claim no longer holds.

**Back to within 136 bytes of C (33,704 B vs 33,568 B).** The binary spent part of 2026-06-05 at 49.2 KiB: karac's phase-9 contract-fault categorization (`8183f6c7`) made every panic site (bounds checks included) reference `karac_runtime_panic_prefix`, whose thread-local data dragged one page-aligned writable `__DATA` segment (16 KiB on Apple Silicon) into every binary — even contract-free ones (the same instance katas [#6](../6-zigzag-conversion/README.md#binary-size) and [#5](../5-longest-palindromic-substring/README.md) measured the same day). The same-day karac fix (`3f3b34a9`) folds the fault prefix static for contract-free programs, the symbol goes unreferenced, and the page dead-strips — the evening rebuild restores C parity, 48 bytes closer than the pre-regression 184-byte gap. The rest of the lean profile is unchanged: the workload reaches `Vec.filled` + indexed read/write, `Slice[i64]` indexing, `println(i64)` — and nothing else; cross-archive LTO + DCE (landed 2026-05-12) elides the rest of the runtime (HTTP, JSON, tokio subgraph, `Map`, `String`, shared structs). Same shape as kata [#4](../4-median-of-two-sorted-arrays/#compile-time-and-binary-size).

### Runtime memory (peak)

| Run | Peak RSS |
|---|---|
| `kara two_pointer` (codegen) | 31.6 MiB |
| `c    two_pointer` | 31.6 MiB |
| `rust two_pointer` | 31.7 MiB |
| `go   two_pointer` | 34.4 MiB |
| `py two_pointer` | 101 MiB (last measured 2026-06-05, not re-run) |

**Parity with C and Rust on memory** — the 2026-11-01 single-shot readings put kara 24 bytes above C (33,177,960 B vs 33,177,936 B) with Rust one 16 KiB page above (33,194,320 B); earlier samples paired kara byte-identical with Rust (the 2026-06-05 evening run), with C (the 06-05 morning run) or with Rust again (2026-05-18). Page-level jitter aside, all three sit on the same 32 MiB working set: the bench holds three `Vec[i64]`s simultaneously — `prefix_a` (1M × 8B = 8 MiB), `b` (8 MiB), and `workspace` (16 MiB). The May-15 snapshot measured kara at 48.2 MiB against the same `Vec.filled(total, 0)` source; the 16 MiB headroom traced to a karac drop / allocator pathway that has since been fixed, and the current build matches the C and Rust (`vec![0; TOTAL]`) allocation profile to within a page. Go's +3 MiB is GC arena + runtime; Python's 101 MiB is per-element PyObject boxing. Same story as kata [#4](../4-median-of-two-sorted-arrays/#runtime-memory-peak) and kata [#121](../121-best-time-to-buy-and-sell-stock/#runtime-memory-peak).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why Rust is in the harness`](../1-two-sum/README.md#why-rust-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio for v1 is the codegen-vs-Rust gap above. C calibrates the LLVM-backend floor (its 1.60× lead here is the no-bounds-check raw-pointer loop), Go is the cross-runtime data point (1.08× behind kāra, 2026-11-01), and Python is the ergonomic foil.

## Bug ledger

**Surfaced [`B-2026-11-01-19`](../../../../kara/docs/bugs-v2.md)** (perf, open). On the MIR backend (karac g6697158fa, 2026-11-01) `bench/two_pointer.kara` retires 1.38× the last legacy build's instructions at 1.23× its cycles: the seq lane went from 0.81× to 1.00× `rustc -O` and from 1.27× to 1.60× clang -O3. Unattributed.
