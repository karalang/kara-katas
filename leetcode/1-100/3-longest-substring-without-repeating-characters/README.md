# 3. Longest Substring Without Repeating Characters

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** String, Hash Map, Sliding Window &nbsp;·&nbsp; **Source:** [leetcode.com/problems/longest-substring-without-repeating-characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/)

Given a string `s`, find the length of the longest substring without duplicate characters.

**Constraints:** `0 ≤ s.length ≤ 5 × 10⁴`, `s` consists of English letters, digits, symbols, and spaces.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| Sliding window with last-index map | O(n) time, O(min(n, σ)) space | [`sliding_window.kara`](sliding_window.kara) ✓ via `karac run` / `karac build` | [`sliding_window.py`](sliding_window.py) ✓ |

`✓` runs end-to-end today. `σ` is the alphabet size; for ASCII input the space bound is O(min(n, 128)).

### Why one map jump is enough

The naive sliding window shrinks `left` one step at a time on a duplicate — O(n) amortized but with a real factor-of-two penalty. The last-index variant turns each contraction into a single pointer jump: when character `c`'s previously-recorded index `prev` lies inside the current window (`prev >= left`), set `left = prev + 1` directly.

The `prev >= left` guard is the key invariant: a previous occurrence outside the current window is irrelevant and must not shrink the window. Without that guard, the second `a` in `"abba"` shrinks too aggressively and returns 2 instead of 3 (`"bba"`).

## Kāra features exercised

- **`ref String` + `s.chars()`** — read-only string borrow, iterated per Unicode scalar value via an inline byte-offset loop with a runtime UTF-8 decode helper.
- **`Map[char, i64]`** — `char` works as a hash key through the typechecker and the (now monomorphized) runtime Map; the whole algorithm is one Map.
- **`match Option[i64]` on `Map.get()`** — canonical "lookup and act on present/absent" idiom; `None => {}` is the no-op arm.
- **Mutable local accumulators** — `let mut left`, `let mut best`, `let mut right` updated by guarded `if` / `match`.

No `Vec`, no slices, no shared structs.

## Running

```bash
# Kāra (compiled or interpreted — both work)
karac run   sliding_window.kara
karac build sliding_window.kara && ./sliding_window

# Python
python3 sliding_window.py
```

## Benchmarks
<!-- bench-staleness -->
> **Figures in this section are a 2026-05-23 snapshot; the feed was last measured 2026-08-04.** Where the two disagree, [`bench/results.json`](bench/results.json) and the [charts](../../../BENCHMARKS.md) are current; the numbers below are kept because the analysis around them explains *why* the shape is what it is, and that reasoning outlives the milliseconds.
> Comparative claims below ("ahead of C", "leads Rust", ratios) were true of the snapshot and have **not** been re-verified against the current feed — treat them as historical, not as the standing result.

### How to run

```bash
brew install hyperfine    # one-time, also needs rustc (rustup), clang, go, karac
./bench/bench.sh
```

`bench/bench.sh` builds the Rust file with `rustc -O`, the C file with `clang -O3`, the Kāra file with `karac build`, and the Go module with `go build` (all cached in `bench/target/`, gitignored), then runs five passes per the [BENCH.md protocol](../../../BENCH.md):

1. **Sink agreement** — every compiled mirror's stdout must equal `520` (Python opt-in via `KARA_BENCH_INCLUDE_PY=1`).
2. **Runtime (short, compiled)** — `hyperfine --warmup 5 --runs 30 --shell=none` across kara/rust/c/go. Input is the 26-character lowercase alphabet repeated 4000 times (104_000 chars total). `K = 20` outer iterations; each call answers `26` (the longest non-repeating run is exactly one full alphabet cycle).
3. **Runtime (long, py)** — `hyperfine --warmup 2 --runs 10` for the Python mirror in its own batch.
4. **Compile elapsed (cold)** — `hyperfine` with a `--prepare` step that deletes the artifact before every run, so each measurement is a fresh `karac build` / `rustc -O` / `clang -O3` invocation. Go is excluded per BENCH.md — `go build`'s first run mixes module + std-lib link.
5. **Binary size, runtime memory, compile memory** — one row per comparator.

| File | What it does |
|---|---|
| [`bench/sliding_window.kara`](bench/sliding_window.kara) | 26-char alphabet × 4000 = 104K chars, K=20 outer iterations, `Map[char, i64]` last-index map |
| [`bench/sliding_window.rs`](bench/sliding_window.rs) | Algorithmic mirror; `HashMap<char, i64>`; compiled with `rustc -O` |
| [`bench/sliding_window.c`](bench/sliding_window.c) | Algorithmic mirror; custom open-addressing linear-probe hashmap keyed by `int32_t` codepoint (CAP=64, ≥ 2×σ); compiled with `clang -O3` |
| [`bench/go-seq/main.go`](bench/go-seq/main.go) | Algorithmic mirror; `map[rune]int64`; built with `go build` |
| [`bench/sliding_window.py`](bench/sliding_window.py) | Algorithmic mirror — same input, same K, `dict[str, int]` |

All five print the same sum-of-results sink (`K × 26 = 520`) so the algorithm's output participates in I/O and can't be elided.

This is a **seq-only kata**: the inner walk is data-dependent on `left` / `last_idx` across `right → right+1`, so it can't be parallelized; the outer `K=20` loop is too small to amortize dispatch. Per the [BENCH.md two-lane protocol](../../../BENCH.md#par-lane--when-the-workload-admits-parallelism), no par lane is shipped.

### Runtime

Snapshot — M5 Pro, 2026-05-23, hyperfine `--warmup 5 --runs 30 --shell=none`, native binaries via `karac build`, `rustc -O`, `clang -O3`, and `go build`. Kara binary verified seq via `nm -gU target/sliding_window_kara | grep karac_par_reduce` (no auto-par symbols present) per BENCH.md § Implicit auto-par.

| Run | Mean ± σ |
|---|---|
| `c    sliding_window` (clang -O3) | **3.0 ± 0.1 ms** |
| `rust sliding_window` (rustc -O)  | 17.3 ± 0.2 ms |
| `rust sliding_window` (rustc -O `-C overflow-checks=on`) | 17.8 ± 0.2 ms |
| `go   sliding_window` (go build)  | 21.7 ± 0.3 ms |
| **`kara sliding_window` (codegen)** | **31.9 ± 0.6 ms** |
| `py   sliding_window` (CPython, separate batch) | 111.8 ± 2.1 ms |

> ### ⚠️ This kata's headline reversed on 2026-09-08, and the reason is instructive
>
> Every version of this file before today led with **"Kāra is ~2.3× faster than
> Rust here."** On the current compiler Kāra is **1.79× SLOWER** than
> equal-safety Rust (31.9 vs 17.8 ms). The kata's source did not change and
> neither did the host — C, Rust and Go each re-read within 6–22% of their
> 2026-08-04 figures on byte-identical binaries, against Kāra's **5.44×**.
>
> The cause is karac `59c8d30cd` (2026-08-22): codegen's integer hash was one
> multiply against a **compile-time-constant seed sitting in the compiler's own
> source**, and is now per-process-seeded SipHash-1-3. That closed a real
> hash-flooding hole — colliding keys could be generated offline by anyone
> reading the compiler.
>
> **The old lead was largely a measurement of that asymmetry.** The paragraph
> below headlined it honestly at the time: Rust "pays a DoS-resistance tax …
> that dominates on tiny-table workloads" while "DoS resistance is not in scope
> for v1." Both halves were true; the second is no longer, so the comparison it
> justified has closed. See kara `B-2026-09-07-42` (bisect) and
> `B-2026-09-07-53` (the corpus-wide measurement, twelve katas).

Kāra checks integer overflow by default; `rustc -O` silently *wraps*. The fair apples-to-apples comparison is therefore the checked Rust lane (`rustc -O -C overflow-checks=on`), which is what Kāra actually does — **1.79×** ahead of Kāra today, against wrapping Rust's 1.85×. That much of the old framing survives: the safety adjustment still moves the comparison in Kāra's favour, it simply no longer moves it far enough to change the sign.

Within the seq lane (all four compiled langs), as of 2026-09-08: Kāra runs **1.85× slower than wrapping Rust** (1.79× slower than checked Rust), **1.47× slower than Go**, and **3.5× faster than Python**; C runs **10.6× faster than Kāra**. The C gap was previously argued to be a workload-shape gap rather than a codegen gap — see "Where C wins" below — and that argument is unaffected by the hash change, but the multiple it applies to has widened from 1.92× to 10.6×. The pre-monomorphization snapshot (2026-05-15, M1) read kara 1620 ms — 98× *slower* than Rust; the gap reversed by ~240× over the next three days. Two karac strands account for the swing:

- **Monomorphized `Map[char, i64]`** (phase-7 line 362, slices 1+2, commits `537e5d2` through `48e4963`, 2026-05-15). Replaces the type-erased C runtime's function-pointer hash/eq dispatch + byte-blob key/value storage with a per-`{K, V}` LLVM family (`karac_map_i32_i64_*` covers both `char` and `i32`; `linkonce_odr` linkage dedupes across crates). The mono `get` body inlines the FxHash+linear-probe loop at the call site so the hot path becomes "hash key → index → load i64" — no extern call, no indirect dispatch, no widening shim. The `1b.4` microbench (1M `Map[i64, i64]` insert+get) measured this strand at 1.32× faster than `std::HashMap` on its own.
- **Codegen body cleanup post-Slice 2.** Slice 2's bench-day snapshot (2026-05-15 PM, doc commit `a1aa01b`) still read 95.7× of Rust — only a ~2% delta from the type-erased baseline, with `karac_string_decode_char` per-char FFI fingered as the residual bottleneck. The remaining ~230× evaporated over the next three days of codegen work on adjacent surfaces (per-iter Vec/String leak close on auto-par + slot paths in `daaf2cc`, the cluster of RC-discipline fixes around the Map / shared-struct drop walks in `9d878ae` / `8b13048` / `d329023`, branch-tail fresh-ref detection in `919cfe0`). None of those targeted kata 3, but the cumulative effect on the inner-loop codegen quality is the only thing the gap reversal can be charged to.

**Where the time goes.** The body of `length_of_longest_substring` is ~2M Map operations: 104K chars × 20 outer iterations × (one `Map.get`, one `Map.insert`) per char. At 31.9 ms total that is ~15.3 ns per Map op, against ~3.6 ns before 2026-09-08 — the table still fits in L1 and the probe is unchanged; what grew is the hash itself. SipHash-1-3 on an 8-byte key is ~92 instructions where the old multiply was ~2, and it is already within ~10% of what the permutation costs, so there is no meaningful headroom inside it.

**Why Kāra used to beat Rust and Go here — and why it no longer does.** ⚠️ **Superseded 2026-09-08; kept because it diagnosed the gap correctly and that diagnosis is what closed it.** As written: Rust's `HashMap<char, i64>` is fully monomorphized, but its `RandomState` SipHash13 hasher pays a DoS-resistance tax (per-instance seed + 13-round mixing) that dominates on tiny-table workloads. Go's `map[rune]int64` runtime carries a similar (AES-NI-backed memhash) per-bucket dispatch tax plus per-call map-header alloc on `make(map[...])`. Kāra's hash was FxHash (rotate-5 + XOR + multiply; multiplier `0x517c_c1b7_2722_0a95`), chosen by `karac-rust/bench/hash_quality/` (2026-05-15) as the fastest non-cryptographic option on the per-K matrix. **"DoS resistance is not in scope for v1"** was the stated basis, and the paragraph concluded that "the hasher asymmetry is the headline gap, and it lands in Kāra's favor on this shape."

That was an accurate description of a comparison between two different amounts of work. It stopped being the design in `59c8d30cd`: DoS resistance IS in scope, because the FxHash seed was a compile-time constant in the compiler's source and colliding keys could be generated offline. Kāra now runs the same SipHash-1-3 family Rust does, so the asymmetry this paragraph headlined is gone — and with it the lead it produced. What remains at genuine parity is a real but much smaller gap: an isolated `Map[i64,i64]` lookup microbenchmark puts Kāra at 1.73× Rust's instruction count but only **1.14× its wall clock**.

**Where C wins.** ⚠️ **The mirror this paragraph describes no longer exists — the reasoning below applied to it, and the conclusion it reached has since been retired.** As written, the C mirror used an open-addressing linear-probe hashmap on a *static 64-slot array* keyed by `int32_t` codepoint (workload σ = 26, load factor ~0.4). On a 26-entry working set that table fits entirely in L1, so `clang -O3` laid the inner loop down as ~4 ns per char (memset + 26 stores + 26 loads on a CPU that holds the whole table in registers across the iteration). Kāra and Rust both pay the `Map.new() → drop` round-trip per `length_of_longest_substring` call — the cost of a generic `Map[K, V]` whose capacity isn't proven static at compile time. On that basis C's win was called a *workload-shape* win rather than a codegen-quality one, and the C ratio was deliberately not headlined.

**That excuse is gone.** `f73df9b` (31 Jul 2026) replaced the presized static table with a heap-allocated one that starts at capacity 16, doubles with a full rehash at the same 3/4 load factor the runtime map uses, and hashes with **FxHash under the compiler's own seed** — dropping the splitmix mixer it had used. It now allocates, grows, and rehashes on the same policy as Kāra's `Map`, so the abstraction levels no longer differ and the comparison is apples-to-apples by construction. C got *faster* in the process (the cheaper hash more than paid for the allocation), so the gap widened rather than closed: on the 4 Aug 2026 M5 feed C is **2.36× ahead of Kāra** (2.48 vs 5.87 ms), against 1.92× in the snapshot above.

The right reading now: this is a real per-core codegen gap on a tiny-table hash workload, not a representation mismatch to be set aside. Kāra's standing lead over the *safe* languages is unaffected and also grew — 2.73× over `rustc -O`, 2.86× at equal safety, 3.30× over Go on the same feed.

### Compile time and binary size

Snapshot — M5 Pro, 2026-05-23, hyperfine `--warmup 1 --runs 10` with `--prepare 'rm -f <artifact>'` so each measurement is cold:

| Compiler | Compile time | Binary size |
|---|---|---|
| `clang -O3 sliding_window.c`      | 49.6 ± 0.7 ms | 32.8 KiB |
| **`karac build sliding_window.kara`** | **78.3 ± 0.3 ms** | **279.1 KiB** |
| `rustc -O sliding_window.rs`      | 131.2 ± 2.0 ms | 457.1 KiB |
| `go build` (Go module)            | — (excluded; mixes module + std-lib link) | 2434.4 KiB |

Kāra compiles this kata **1.68× faster** than `rustc -O` and produces a binary **~39% smaller than Rust** (the cross-archive LTO + DCE work landed 2026-05-12 keeps the runtime contribution tight when downstream features (HTTP, JSON, tokio subgraph) aren't reached). `clang -O3` is 1.58× faster still — C carries no stdlib runtime to link, just libc; Kāra's gap to clang here is the inherent cost of the karac runtime support functions (Map mono, String UTF-8 walker, panic infrastructure) that show up linked even when LTO trims hard.

### Runtime memory (peak)

| Run | Peak RSS |
|---|---|
| `c    sliding_window` | 1.1 MiB |
| `rust sliding_window` | 1.2 MiB |
| **`kara sliding_window` (codegen)** | **1.3 MiB** |
| `go   sliding_window` | 3.0 MiB |
| `py   sliding_window` | 7.0 MiB |

The 104K-char String is ~104 KB; the Map holds at most 26 entries; neither dominates allocation. Kāra now sits within 0.1 MiB of Rust and 0.2 MiB of C — the type-erased Map's per-call buffer churn that drove the previous 0.5 MiB headroom went away with monomorphization (one allocator per `{K, V}` instantiation, same shape as Rust's `HashMap<char, i64>`). Go's 3.1 MiB reflects its statically-linked runtime + GC scheduler footprint (visible in the 2.4 MiB binary too).

### Compile memory (cold)

| Compiler | Peak RSS |
|---|---|
| `clang -O3 sliding_window.c`      | 2.5 MiB |
| **`karac build sliding_window.kara`** | **13.4 MiB** |
| `rustc -O sliding_window.rs`      | 37.9 MiB |

Kāra's cold-compile footprint is **2.8× smaller than rustc** and 5.4× larger than clang. The clang gap is the LLVM-context + per-pass scratch we share with rustc; the rustc gap is the absence of an IR-level borrow checker + macro expander.

### Why Rust / C / Go / Python are in the harness

Same rationale as [`1-two-sum/README.md § Why Rust is in the harness`](../1-two-sum/README.md#why-rust-is-in-the-harness) and the [BENCH.md comparator policy](../../../BENCH.md#comparison-baselines):

- **Rust** is Kāra's semantic peer (compiled, ownership-aware, LLVM-backed), so the headline ratio for v1 is the codegen-vs-Rust gap above. This kata used to be the worst codegen-vs-Rust gap in the suite (98× *slower*) and so the most concrete justification for monomorphized collections; with Slice 1+2 of that work shipped it reversed to 2.16× *faster*, and the bench earned its keep as the natural-pull validation workload that originally motivated the strand. As of 2026-09-08 it reads **1.85× slower** than wrapping Rust again — not a reversal of that work, which stands, but the hash change described above. The monomorphized map is still monomorphized; it now hashes with SipHash-1-3 like Rust's does.
- **C** is the codegen calibration point — same LLVM backend as Kāra and Rust, no language runtime overhead. Kāra's gap to C is the cost of using `Map[K, V]` as a generic abstraction (allocator round-trip per call, capacity not proven static); Rust pays the same cost. The Kāra-vs-Rust ratio is the meaningful one *within* the abstraction level both pick.
- **Go** is the cross-runtime data point — GC + scheduler + statically-linked runtime, but a thoroughly-tuned native compiler. Standing baseline since 2026-05-21 (BENCH.md update). The 2.59× Kāra-over-Go gap this kata used to show was the FxHash-vs-Go-memhash + per-call map-header alloc combination; with FxHash retired in `59c8d30cd` the hash half of that is gone and Kāra now reads **1.47× slower** than Go. The map-header alloc difference is unchanged and still real — it is simply no longer enough on its own.
- **Python** is the ergonomic foil — the "is the perf cliff worth the syntax?" framing. Gated behind `KARA_BENCH_INCLUDE_PY=1` in the sink check; always run in its own hyperfine batch so it doesn't slow feedback on the compiled lane.
